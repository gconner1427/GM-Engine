"""The play window: a desktop window for setting up and playing narratives.

    gm play                       opens the window on the list of narratives
    gm play "<narrative folder>"  opens straight into one
    gm play --browser             the same page in a browser tab instead of its own window

The window is a page served only on this machine (127.0.0.1). It reads the narrative's files
(the session log, the Character Sheet, the Journal) and never anything in GM Only/ except its
own gui.json: the world is the GM's, and the player finds it out by playing. What the user types is handed to Claude Code, run headless in the
narrative's folder, continuing one conversation; Claude Code is the GM, exactly as it is in
VS Code, and the window shows only its final message of each turn.

Every request must carry the random token the page was served with, so no other website open
in a browser can post to it.
"""

import datetime
import json
import os
import re
import secrets
import shutil
import subprocess
import sys
import threading
import time
import traceback
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import scaffold
from narrative import CONFIG, ENGINE, Narrative, field

PAGE = Path(__file__).resolve().parent / "gui" / "app.html"
STORE = Path.home() / ".gm-engine"
KNOWN = STORE / "narratives.json"
SETTINGS = STORE / "config.json"  # optional: {"claude": "<path to claude>", "model": "<model>"}
PREFS = STORE / "prefs.json"      # the window's own: text size, whether the side panel is hidden
ERRORS = STORE / "gui.log"
TOKEN = secrets.token_urlsafe(24)
MAX_BODY = 2_000_000
CHANNEL_KEEP = 400
UNTITLED = "Untitled Narrative"
IDLE_QUIT = 20 # seconds without a ping before a browser-tab window counts as closed
NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)

GM_RULE = f'python "{ENGINE.as_posix()}/engine/gm.py" *'
WINDOW_NOTE = """This conversation is driven by the GM Engine play window, not typed into a terminal or VS Code.
- The user sees only your final message of each turn, in a side panel. They read the narrative in the session log, which the window shows live. Chat echo is therefore off whatever `gm status` says: after committing a beat, your whole reply is exactly {added}.
- Interactive tools (the question tool, plan mode) are not available. Ask questions as plain text in your final message, a few at a time.
- Nothing can prompt the user for permission. If a tool call is denied, don't retry it: work another way, or say plainly what was denied.
- During setup the window shows your messages as a conversation, and neither side needs braces. The folder already exists, and the first message usually carries the player's answers to the three questions: ask only for what's missing. The player can't see any file but the Character Sheet and the Journal, so what they need to know to make a character has to be in your message.
- When the user flags a passage, the window quotes it to you in braces."""


def log_error():
    try:
        STORE.mkdir(parents=True, exist_ok=True)
        with ERRORS.open("a", encoding="utf-8") as f:
            f.write(f"\n--- {datetime.datetime.now().isoformat(timespec='seconds')}\n{traceback.format_exc()}")
    except OSError:
        pass


def read_json(path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError):
        return default


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, path)


def read(path):
    try:
        return path.read_text(encoding="utf-8-sig")
    except OSError:
        return ""


def stamp(path):
    try:
        s = path.stat()
        return f"{s.st_mtime_ns}-{s.st_size}"
    except OSError:
        return ""


# ---- Claude Code -----------------------------------------------------------

def find_claude():
    """The Claude Code program: the one in config.json, on the PATH, or inside the VS Code extension."""
    chosen = read_json(SETTINGS, {}).get("claude")
    if chosen and Path(chosen).exists():
        return chosen
    found = shutil.which("claude")
    if found:
        return found
    version = lambda p: [int(n) for n in re.findall(r"\d+", p.parts[-4])]  # the extension's folder name
    bundled = sorted(Path.home().glob(".vscode*/extensions/anthropic.claude-code-*/resources/native-binary/claude*"), key=version)
    return str(bundled[-1]) if bundled else None


def claude_command(conversation):
    cmd = [find_claude(), "-p", "--output-format", "stream-json", "--verbose", "--permission-mode", "acceptEdits",
           "--add-dir", str(ENGINE), "--allowedTools", f"PowerShell({GM_RULE})", f"Bash({GM_RULE})",
           "--append-system-prompt", WINDOW_NOTE]
    model = read_json(SETTINGS, {}).get("model")
    if model:
        cmd += ["--model", model]
    if conversation:
        cmd += ["--resume", conversation]
    return cmd


# ---- one narrative, open in the window ---------------------------------------

class Game:
    def __init__(self, root):
        self.narrative = Narrative(root)
        self.root = self.narrative.root
        self.file = self.narrative.logs_dir / "gui.json"
        self.lock = threading.Lock()
        self.data = read_json(self.file, {})
        self.data.setdefault("conversation", None)
        self.data.setdefault("channel", [])
        self.process = None
        self.thread = None
        self.started = None
        self.steps = 0
        self.stopped = False
        self.error = None

    def busy(self):
        return self.thread is not None and self.thread.is_alive()

    def save(self):
        self.data["channel"] = self.data["channel"][-CHANNEL_KEEP:]
        write_json(self.file, self.data)

    def say(self, who, text):
        with self.lock:
            self.data["channel"].append({"who": who, "text": text, "at": datetime.datetime.now().isoformat(timespec="seconds")})
            self.save()

    def config(self):
        return read_json(self.root / CONFIG, self.narrative.config)

    # ---- sending ---------------------------------------------------------

    def send(self, text):
        text = text.strip()
        if not text:
            raise ValueError("There's nothing to send.")
        if self.busy():
            raise ValueError("The GM is still working on the last message.")
        if not find_claude():
            raise ValueError("Can't find Claude Code. Install the Claude Code extension in VS Code, or put the path to "
                             f"claude in {SETTINGS} as {{\"claude\": \"...\"}}.")
        if re.search(r"\{\s*new session\s*\}", text, re.IGNORECASE):
            self.data["conversation"] = None  # a new session starts with a clean head
        self.error, self.stopped, self.steps, self.started = None, False, 0, time.time()
        self.say("you", text)
        self.thread = threading.Thread(target=self.run, args=(text,))
        self.thread.start()

    def run(self, text):
        try:
            reply, failure = self.ask(text, self.data["conversation"])
            if failure and self.data["conversation"] and "conversation found" in failure.lower():
                self.data["conversation"] = None  # the old conversation is gone (another machine, or cleared)
                reply, failure = self.ask(text, None)
            if self.stopped:
                self.say("note", "Stopped. If a beat was half written, {undo} takes it back out.")
            elif failure:
                self.error = failure
                self.say("note", failure)
            elif reply and not re.fullmatch(r"\{\s*added\.?\s*\}", reply, re.IGNORECASE):
                self.say("gm", reply)
            if re.search(r"\{\s*end session\s*\}", text, re.IGNORECASE) and not failure and not self.stopped:
                with self.lock:
                    self.data["conversation"] = None
                    self.save()
        except Exception:
            log_error()
            self.error = f"The window hit an error talking to Claude Code. Details are in {ERRORS}."
            self.say("note", self.error)

    def ask(self, text, conversation):
        """Run one turn. Returns (the GM's final message, or an error to show)."""
        self.process = subprocess.Popen(claude_command(conversation), cwd=self.root, stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8",
                                        errors="replace", creationflags=NO_WINDOW)
        errors = []
        drain = threading.Thread(target=lambda: errors.extend(self.process.stderr), daemon=True)
        drain.start()
        self.process.stdin.write(text)
        self.process.stdin.close()
        reply, failure = "", None
        for line in self.process.stdout:
            try:
                event = json.loads(line)
            except ValueError:
                continue
            kind = event.get("type")
            if kind == "assistant":
                self.steps += sum(1 for b in event.get("message", {}).get("content", []) if b.get("type") == "tool_use")
            elif kind == "result":
                if event.get("session_id"):
                    with self.lock:
                        self.data["conversation"] = event["session_id"]
                        self.save()
                reply = (event.get("result") or "").strip()
                if event.get("is_error") or event.get("subtype") != "success":
                    failure = reply or f"Claude Code stopped early ({event.get('subtype')})."
        self.process.wait()
        drain.join(timeout=2)
        said = "".join(l for l in errors if not l.startswith("Ignoring ")).strip()  # project settings are replaced by flags
        if not reply and not failure and not self.stopped:
            failure = said[-600:] or "Claude Code returned nothing."
        return reply, failure

    def stop(self):
        process = self.process
        if not self.busy() or not process or process.poll() is not None:
            return
        self.stopped = True
        if os.name == "nt":  # claude starts children of its own
            subprocess.run(["taskkill", "/T", "/F", "/PID", str(process.pid)], capture_output=True, creationflags=NO_WINDOW)
        else:
            process.terminate()

    # ---- what the window shows ---------------------------------------------

    def state(self, viewing, have):
        cfg = self.config()
        sessions = cfg.get("sessions", 0)
        viewing = viewing if viewing and 1 <= viewing <= sessions else sessions
        files = {"sheet": self.narrative.sheet, "journal": self.root / "Journal.md"}
        if viewing:
            files["log"] = self.narrative.session_log(viewing)
        out = {"name": cfg.get("name", self.narrative.name), "path": str(self.root), "set_up": bool(cfg.get("set_up")),
               "sessions": sessions, "open_session": cfg.get("open_session"), "viewing": viewing,
               "busy": self.busy(), "elapsed": int(time.time() - self.started) if self.busy() else 0,
               "steps": self.steps, "channel_count": len(self.data["channel"]), "stamps": {}, "texts": {}}
        for key, path in files.items():
            mark = f"{viewing if key == 'log' else ''}:{stamp(path)}"
            out["stamps"][key] = mark
            if have.get(key) != mark:
                out["texts"][key] = read(path)
        if have.get("channel") != len(self.data["channel"]):
            out["channel"] = self.data["channel"]
        return out


GAMES = {}
games_lock = threading.Lock()
dialog_lock = threading.Lock()


def game(path):
    root = Path(path or "").resolve()
    if not path or not (root / CONFIG).exists():
        raise ValueError("That isn't a narrative folder.")
    with games_lock:
        if str(root) not in GAMES:
            GAMES[str(root)] = Game(root)
        return GAMES[str(root)]


# ---- the list of narratives ------------------------------------------------

def known():
    return [p for p in read_json(KNOWN, []) if isinstance(p, str)]


def remember(path):
    path = str(Path(path).resolve())
    write_json(KNOWN, [path] + [p for p in known() if p != path])
    return path


def forget(path):
    write_json(KNOWN, [p for p in known() if p != str(Path(path).resolve())])


def home():
    listed = []
    for path in known():
        root = Path(path)
        cfg = read_json(root / CONFIG, None)
        sessions = (cfg or {}).get("sessions", 0)
        sheet = read(root / "Character Sheet.md")
        name, played = field(sheet, "Name") or "", None
        try:
            played = datetime.datetime.fromtimestamp((root / "Sessions" / f"Session {sessions}.md").stat().st_mtime).isoformat()
        except OSError:
            pass
        listed.append({"path": path, "missing": cfg is None, "name": (cfg or {}).get("name", root.name),
                       "set_up": bool((cfg or {}).get("set_up")), "sessions": sessions, "played": played,
                       "character": "" if name.lower().startswith(("unknown", "(")) else name, "level": field(sheet, "Level") or ""})
    return {"narratives": listed, "default_parent": str(scaffold.DEFAULT_PARENT), "claude": find_claude(),
            "prefs": read_json(PREFS, {})}


def pick_folder(start=None):
    """A folder chooser from the system, since a page can't ask for one itself."""
    import tkinter
    from tkinter import filedialog
    with dialog_lock:
        root = tkinter.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        try:
            return filedialog.askdirectory(parent=root, initialdir=start or str(Path.home()), mustexist=False) or ""
        finally:
            root.destroy()


def create(name, parent):
    """A new narrative folder. With no title yet, it gets a placeholder and the GM titles it during setup."""
    parent = Path(parent or scaffold.DEFAULT_PARENT)
    name = scaffold.safe(name or "")
    if not name:
        name, n = UNTITLED, 1
        while (parent / name).exists():
            n += 1
            name = f"{UNTITLED} {n}"
    return remember(scaffold.create_narrative(name, parent))


# ---- the server --------------------------------------------------------------

class Handler(BaseHTTPRequestHandler):
    server_version = "GMEngine"

    def log_message(self, fmt, *args):  # keep the terminal quiet
        pass

    def send(self, code, body, kind="application/json"):
        data = body if isinstance(body, bytes) else json.dumps(body).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", kind + "; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path.split("?")[0] not in ("/", "/index.html"):
            return self.send(404, {"error": "Not found"})
        html = read(PAGE).replace("__GM_TOKEN__", TOKEN)
        html = html.replace("__GM_START__", json.dumps(getattr(self.server, "start", None)).replace("<", "\\u003c"))
        self.send(200, html.encode("utf-8"), "text/html")

    def do_POST(self):
        if self.headers.get("X-GM-Token") != TOKEN:
            return self.send(403, {"error": "This window's session has expired. Close it and open it again."})
        length = int(self.headers.get("Content-Length") or 0)
        if length > MAX_BODY:
            return self.send(413, {"error": "That's too much to send at once."})
        try:
            data = json.loads(self.rfile.read(length) or b"{}")
        except ValueError:
            return self.send(400, {"error": "The window sent something unreadable."})
        self.server.seen = time.time()
        try:
            return self.send(200, self.route(self.path.split("?")[0], data))
        except ValueError as e:
            return self.send(400, {"error": str(e)})
        except Exception:
            log_error()
            return self.send(500, {"error": f"Something went wrong. Details are in {ERRORS}."})

    def route(self, route, data):
        path = data.get("path")
        if route == "/api/ping":
            return {"ok": True}
        if route == "/api/home":
            return home()
        if route == "/api/prefs":
            write_json(PREFS, {"size": int(data["prefs"].get("size", 18)), "wide": bool(data["prefs"].get("wide"))})
            return {"ok": True}
        if route == "/api/pick-folder":
            return {"path": pick_folder(data.get("start"))}
        if route == "/api/create":
            return {"path": create(data.get("name"), (data.get("parent") or "").strip() or None)}
        if route == "/api/add":
            game(path)
            return {"path": remember(path)}
        if route == "/api/forget":
            forget(path)
            return {"ok": True}
        if route == "/api/state":
            return game(path).state(data.get("viewing"), data.get("have") or {})
        if route == "/api/send":
            game(path).send(data.get("text") or "")
            return {"ok": True}
        if route == "/api/stop":
            game(path).stop()
            return {"ok": True}
        if route == "/api/fresh":
            g = game(path)
            if g.busy():
                raise ValueError("Wait for the GM to finish first.")
            g.data["conversation"] = None
            g.save()
            g.say("note", "The next message starts a fresh conversation with the GM. Nothing in the narrative changes; the GM rereads its notes.")
            return {"ok": True}
        if route == "/api/open-folder":
            if hasattr(os, "startfile"):
                os.startfile(str(game(path).root))
            return {"ok": True}
        raise ValueError("Not found")


def finish():
    """Let a beat in progress finish writing before the program exits."""
    for g in list(GAMES.values()):
        if g.thread and g.thread.is_alive():
            g.thread.join(timeout=600)


def serve(start):
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    server.start = remember(start) if start and (Path(start) / CONFIG).exists() else None
    server.seen = None
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, f"http://127.0.0.1:{server.server_address[1]}/"


def run(start=None, browser=False):
    server, url = serve(start)
    try:
        webview = None
        if not browser:
            try:
                import webview
            except ImportError:
                print("The desktop window needs pywebview (pip install pywebview). Opening in the browser instead.")
        if webview:
            webview.create_window("GM Engine", url, width=1360, height=900, min_size=(900, 600))
            webview.start()
        else:
            print(f"GM Engine: {url}\nRunning on this computer only. Close the tab, or press Ctrl+C here, to stop.")
            webbrowser.open(url)
            try:
                while server.seen is None or time.time() - server.seen < IDLE_QUIT:
                    time.sleep(1)
            except KeyboardInterrupt:
                pass
    finally:
        finish()
        server.shutdown()
        server.server_close()
    return 0
