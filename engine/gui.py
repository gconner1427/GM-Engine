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
import urllib.parse
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import art
import saves
import scaffold
import session
from narrative import CONFIG, ENGINE, Narrative, field

PAGE = Path(__file__).resolve().parent / "gui" / "app.html"
ICON = PAGE.with_name("dice.ico")   # the d20: the window, the taskbar, the browser tab, the shortcut
THREE = PAGE.with_name("three.min.js")   # three.js r160, kept here so the main menu's die needs no network
STORE = Path.home() / ".gm-engine"
KNOWN = STORE / "narratives.json"
SETTINGS = STORE / "config.json"  # optional: {"claude": "<path to claude>", "model": "<model>"}
PREFS = STORE / "prefs.json"      # the window's own: text size, whether the side panel is hidden, the menu's music, fullscreen, the GM's model
MENU_BGM = ENGINE / "Audio" / "BGM"   # "Menu BGM 1.mp3", "Menu BGM 2.mp3"
LOGO = ENGINE / "Art" / "Studio Logo" / "Gravelight Studios Logo.png"   # the splash before the intro
TITLE = ENGINE / "Art" / "Title Logo" / "GM Engine Title Logo.png"      # the main menu's title
VERSION = ENGINE / "VERSION"   # one line, "Alpha 0.0.1": the corner of the main menu, and About
MENU_TRACKS = ("1", "2")
WORLD_BGM = "World Creation BGM 1.mp3"   # in the same folder: what plays while the GM builds a world
MODELS = ("opus", "sonnet")   # the GM Model setting. Family names: Claude Code runs the newest of each. "" leaves it to Claude Code
ERRORS = STORE / "gui.log"
TOKEN = secrets.token_urlsafe(24)
MAX_BODY = 2_000_000
CHANNEL_KEEP = 400
BUILDING = (   # what the window says the GM is doing while it builds the world, by the file it last wrote
    ("State/Campaign.md", "Preparing the campaign"), ("World Bible.md", "Laying down the world and its laws"),
    ("Names.md", "Gathering names"), ("Map & Travel.md", "Drawing the map"), ("Economy.md", "Counting out the coin"),
    ("Timeline.md", "Writing the history"), ("Rules Kit.md", "Fitting the rules to the world"),
    ("Bestiary.md", "Stocking the wilds"), ("Items.md", "Hiding things worth finding"),
    ("State/Pressures.md", "Setting trouble in motion"), ("State/World State.md", "Setting the opening scene"),
    ("/Groups/", "Raising the powers that be"), ("/Cast/", "Peopling the world"), ("/Places/", "Building its places"),
    ("Journal.md", "Writing what your character would know"), ("Character Sheet.md", "Working on the character sheet"))
UNTITLED = "Untitled Narrative"
IDLE_QUIT = 20 # seconds without a ping before a browser-tab window counts as closed
NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)

GM_RULE = f'python "{ENGINE.as_posix()}/engine/gm.py" *'
WINDOW_NOTE = """This conversation is driven by the GM Engine play window, not typed into a terminal or VS Code.
- The user sees only your final message of each turn, in a side panel. They read the narrative in the session log, which the window shows live. Chat echo is therefore off whatever `gm status` says: after committing a beat, your whole reply is exactly {added}.
- A conversation's first message opens with your startup reading, which the window loaded for you: every file the narrative's CLAUDE.md and Procedures/Play.md, "Starting a conversation" (steps 1 to 3) tell you to read, as each stands now, then what `gm status` prints, then the end of the latest session log and of its GM log. Don't read any of them again: go on from step 4. (In a narrative that isn't set up yet, the reading is ENGINE.md, GM Rules, Procedures/New Narrative.md, and Core Rules instead.) Where a log is marked "the end of it only" and you need more of it, read the file. What the player sent is everything after the line `===== THE PLAYER'S MESSAGE =====`, and only that is their message.
- Interactive tools (the question tool, plan mode) are not available. Ask questions as plain text in your final message, a few at a time.
- Nothing can prompt the user for permission. If a tool call is denied, don't retry it: work another way, or say plainly what was denied.
- You open every session (Procedures/Play.md, "Opening a session"). Between sessions the window gives the player a Begin button, which sends `{new session}`, and holds back anything typed as the character until a session is open: so `{new session}` is the player sitting down to play, and your whole answer to it is the opening beat, committed, and {added}.
- During setup the window shows your messages as a conversation, and neither side needs braces. The folder already exists, and the first message usually carries the player's answers to the five questions and the content they want: ask only for what's missing.
- The player makes their character on the window's character creator, a step-by-step screen built from the sheet's `## Character creation` section (Procedures/New Narrative.md, step 4). Its first page shows the Journal's "The world as they know it," and the player can't see any other file. So don't repeat the world or the choices in your message and don't interview them: say only that the world is ready and the creator is open. What they made comes back in braces.
- When the user flags a passage, the window quotes it to you in braces.
- An action that ends in `{push}` was sent with the window's Push switch on: the character pushes on that action (Core Rules, "Health").
- When a new level leaves the player choices, the window shows them a level-up screen built from the sheet's `## Level up` section (Procedures/Play.md, "A new level") and sends back what they picked in braces. So don't list the choices in your message: say only that there's a new level to choose for.
- While the sheet has a `## Shop` section, the window shows the player a shop button that opens a shop screen built from it: the stock and its prices, what the keeper would buy, and their money (Procedures/Play.md, "A shop"). So don't list a shop's goods or prices in your message. What they buy and sell comes back as one action that ends in `{trade ...}`, and it's a beat.
- When a session ends, the window shows a summary card built from the Journal's entry for that session and the mark lines under it (Procedures/Play.md, "The end of a session"). So your closing message stays short: the card already shows the marks.
- The window's Undo button sends `{undo}`, and its "I meant" button sends `{I meant: ...}` with the action as the player meant it."""


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


def claude_state():
    """What the window says about Claude Code when it opens: "ready", "signed out", or "missing"."""
    claude = find_claude()
    if not claude:
        return "missing"
    try:
        done = subprocess.run([claude, "auth", "status", "--json"], stdin=subprocess.DEVNULL, capture_output=True,
                              encoding="utf-8", errors="replace", timeout=15, creationflags=NO_WINDOW)
        return "ready" if json.loads(done.stdout)["loggedIn"] else "signed out"
    except (OSError, subprocess.TimeoutExpired, ValueError, KeyError, TypeError):
        return "ready"   # it couldn't say (an older Claude Code can't): if it's signed out, the first message will say so


def opening(root, text):
    """A conversation's first message: the GM's startup reading, then what the player sent. The reading
    holds GM Only docs, so it goes to Claude Code and is never kept in the channel."""
    try:
        reading = session.brief(Narrative(root))
    except Exception:
        log_error()
        return text  # the GM reads the files itself, as it does outside the window
    return f"===== STARTUP READING =====\n\n{reading}\n===== THE PLAYER'S MESSAGE =====\n\n{text}"


def claude_command(conversation):
    cmd = [find_claude(), "-p", "--output-format", "stream-json", "--verbose", "--permission-mode", "acceptEdits",
           "--add-dir", str(ENGINE), "--allowedTools", f"PowerShell({GM_RULE})", f"Bash({GM_RULE})",
           "--append-system-prompt", WINDOW_NOTE]
    chosen = read_json(PREFS, {}).get("model")   # the GM Model setting; left at Default, config.json's, if it names one
    model = chosen if chosen in MODELS else read_json(SETTINGS, {}).get("model")
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
        self.art_trouble = None
        threading.Thread(target=self.painter, daemon=True).start()

    def painter(self):
        """Paint whatever the GM has asked for, one picture at a time, for as long as the window is open."""
        while True:
            try:
                if art.paint_next(self.narrative):
                    self.art_trouble = None
                    continue
            except ValueError as e:      # no Codex on this machine
                self.art_trouble = str(e)
                time.sleep(60)
            except Exception:
                log_error()
                time.sleep(60)
            time.sleep(4)

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
                try:
                    saves.save(self.narrative, "End of session", auto=True)
                except ValueError:
                    pass  # no Git here: the session still ended
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
        self.process.stdin.write(text if conversation else opening(self.root, text))
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
               "steps": self.steps, "can_undo": bool(cfg.get("open_session") and read(self.narrative.last_beat).strip()),
               "channel_count": len(self.data["channel"]), "stamps": {}, "texts": {}}
        for key, path in files.items():
            mark = f"{viewing if key == 'log' else ''}:{stamp(path)}"
            out["stamps"][key] = mark
            if have.get(key) != mark:
                out["texts"][key] = read(path)
        if have.get("channel") != len(self.data["channel"]):
            out["channel"] = self.data["channel"]
        if out["busy"] and not out["set_up"]:
            out["building"] = self.building()
        if not have:  # the window has just opened this narrative
            out["draft"] = self.data.get("draft")
        mark = stamp(art.art_dir(self.narrative) / "art.json") + str(self.art_trouble)
        out["stamps"]["art"] = mark
        if have.get("art") != mark:
            index = art.load(self.narrative)
            out["art"] = {"backdrop": index["backdrop"], "trouble": self.art_trouble,
                          "items": [{k: i.get(k) for k in ("kind", "name", "status", "file", "painted", "error")} for i in index["items"]]}
        return out

    def building(self):
        """During setup: what the GM is at work on, as a line for the player to watch. It says which kind of
        thing was last written (the map, the people), from the file's place in the folder, and never a word of it."""
        newest, line = self.started or 0, "Imagining the world"
        hidden = [p for p in self.narrative.gm_dir.rglob("*.md") if p.parent != self.narrative.logs_dir]
        for path in hidden + [self.root / "Journal.md", self.narrative.sheet]:
            try:
                changed = path.stat().st_mtime
            except OSError:
                continue
            if changed > newest:
                where = path.relative_to(self.root).as_posix()
                newest, line = changed, next((say for part, say in BUILDING if part in where), line)
        return line

    def keep_draft(self, draft):
        """The character creator's answers so far, so a character half made survives the window closing."""
        with self.lock:
            self.data["draft"] = draft if isinstance(draft, dict) else None
            self.save()

    def save_game(self, label):
        if self.busy():
            raise ValueError("Wait for the GM to finish, then save.")
        return saves.save(self.narrative, label)

    def load_game(self, save_id):
        if self.busy():
            raise ValueError("Wait for the GM to finish, then load.")
        chosen = saves.load(self.narrative, save_id)
        with self.lock:
            self.data["conversation"] = None  # the GM's memory of what came after has to go too
            self.save()
        where = f"Session {chosen['session']}" if chosen.get("session") else "before the first session"
        self.say("note", f"Loaded a save from {where}" + (f": {chosen['label']}" if chosen.get("label") else "") +
                 ". The game as it stood was saved first, so you can load it back.")
        return chosen

    def picture(self, file):
        """The bytes of one finished picture, and nothing from outside Art/."""
        folder = art.art_dir(self.narrative).resolve()
        path = (folder / file).resolve()
        if folder not in path.parents or path.suffix.lower() != ".png" or not path.is_file():
            raise ValueError("No such picture.")
        return path.read_bytes()


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
    return {"narratives": listed, "default_parent": str(scaffold.DEFAULT_PARENT), "claude": claude_state(),
            "codex": art.codex_state(), "prefs": read_json(PREFS, {})}


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


def create(name, parent, person="third"):
    """A new narrative folder. With no title yet, it gets a placeholder and the GM titles it during setup."""
    parent = Path(parent or scaffold.DEFAULT_PARENT)
    name = scaffold.safe(name or "")
    if not name:
        name, n = UNTITLED, 1
        while (parent / name).exists():
            n += 1
            name = f"{UNTITLED} {n}"
    return remember(scaffold.create_narrative(name, parent, person))


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

    def send_media(self, data, kind="audio/mpeg"):
        """An <audio> or a <video> seeks and loops by asking for byte ranges, so answer them."""
        start, end = 0, len(data) - 1
        m = re.fullmatch(r"bytes=(\d*)-(\d*)", self.headers.get("Range") or "")
        if m and (m[1] or m[2]):
            if m[1]:
                start, end = int(m[1]), min(int(m[2]), end) if m[2] else end
            else:
                start = max(0, len(data) - int(m[2]))
            if start > end:
                self.send_response(416)
                self.send_header("Content-Range", f"bytes */{len(data)}")
                return self.end_headers()
            self.send_response(206)
            self.send_header("Content-Range", f"bytes {start}-{end}/{len(data)}")
        else:
            self.send_response(200)
        self.send_header("Content-Type", kind)
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Length", str(end - start + 1))
        self.send_header("Cache-Control", "private, max-age=3600")
        self.end_headers()
        try:
            self.wfile.write(data[start:end + 1])
        except OSError:  # the player stopped listening partway
            pass

    def do_GET(self):
        route, _, query = self.path.partition("?")
        asked = urllib.parse.parse_qs(query)
        one = lambda key: (asked.get(key) or [""])[0]
        if route == "/bgm":  # the music: a menu track, or "world" for the build; like a picture, the token rides in the address
            if one("t") != TOKEN:
                return self.send(403, {"error": "Not allowed."})
            if one("n") not in MENU_TRACKS + ("world",):
                return self.send(404, {"error": "No such track."})
            try:
                return self.send_media((MENU_BGM / (WORLD_BGM if one("n") == "world" else f"Menu BGM {one('n')}.mp3")).read_bytes())
            except OSError:
                return self.send(404, {"error": "No such track."})
        if route == "/logo":  # the studio's logo, for the splash before the intro
            if one("t") != TOKEN:
                return self.send(403, {"error": "Not allowed."})
            try:
                return self.send_media(LOGO.read_bytes(), "image/png")
            except OSError:
                return self.send(404, {"error": "No logo."})
        if route == "/title":  # the main menu's title
            if one("t") != TOKEN:
                return self.send(403, {"error": "Not allowed."})
            try:
                return self.send_media(TITLE.read_bytes(), "image/png")
            except OSError:
                return self.send(404, {"error": "No title."})
        if route == "/art":  # an <img> can't send a header, so the token rides in the address
            if one("t") != TOKEN:
                return self.send(403, {"error": "Not allowed."})
            try:
                data = game(one("p")).picture(one("f"))
            except (ValueError, OSError):
                return self.send(404, {"error": "No such picture."})
            self.send_response(200)
            self.send_header("Content-Type", "image/png")
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Cache-Control", "private, max-age=31536000")  # the address changes when the picture does
            self.end_headers()
            return self.wfile.write(data)
        if route == "/favicon.ico":  # the browser asks before the page has a token to send; it's only the die
            try:
                return self.send(200, ICON.read_bytes(), "image/x-icon")
            except OSError:
                return self.send(404, {"error": "Not found"})
        if route == "/three.js":  # a public library, and a <script> can't send a header either
            try:
                return self.send_media(THREE.read_bytes(), "text/javascript")
            except OSError:
                return self.send(404, {"error": "Not found"})
        if route not in ("/", "/index.html"):
            return self.send(404, {"error": "Not found"})
        html = read(PAGE).replace("__GM_TOKEN__", TOKEN)
        try:
            version = VERSION.read_text(encoding="utf-8").strip()
        except OSError:
            version = ""
        html = html.replace("__GM_VERSION__", version.replace("&", "&amp;").replace("<", "&lt;"))
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
        if route == "/api/exit":
            threading.Timer(0.3, close_window, [self.server]).start()   # after the answer has gone back
            return {"ok": True}
        if route == "/api/prefs":
            bgm = str(data["prefs"].get("bgm", 2))
            write_json(PREFS, {"size": int(data["prefs"].get("size", 18)), "wide": bool(data["prefs"].get("wide")),
                               "bgm": int(bgm) if bgm in ("0",) + MENU_TRACKS else 2,   # 0 is off
                               "volume": min(100, max(0, int(data["prefs"].get("volume", 60)))),
                               "fullscreen": bool(data["prefs"].get("fullscreen")),
                               "model": data["prefs"].get("model") if data["prefs"].get("model") in MODELS else ""})
            return {"ok": True, "desktop": set_fullscreen(self.server, bool(data["prefs"].get("fullscreen")))}
        if route == "/api/pick-folder":
            return {"path": pick_folder(data.get("start"))}
        if route == "/api/create":
            return {"path": create(data.get("name"), (data.get("parent") or "").strip() or None, data.get("person") or "third")}
        if route == "/api/add":
            game(path)
            return {"path": remember(path)}
        if route == "/api/opened":  # to the top of the list, which is what the main menu's Continue opens
            if (Path(path) / CONFIG).exists():
                remember(path)
            return {"ok": True}
        if route == "/api/forget":
            forget(path)
            return {"ok": True}
        if route == "/api/state":
            return game(path).state(data.get("viewing"), data.get("have") or {})
        if route == "/api/send":
            game(path).send(data.get("text") or "")
            return {"ok": True}
        if route == "/api/draft":
            game(path).keep_draft(data.get("draft"))
            return {"ok": True}
        if route == "/api/save":
            return {"save": game(path).save_game(data.get("label") or "")}
        if route == "/api/saves":
            return {"saves": saves.listing(game(path).narrative)}
        if route == "/api/load":
            return {"save": game(path).load_game(data.get("id") or "")}
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


def shortcut(desktop=False):
    """A shortcut to the play window with the die on it; a .cmd file can't carry an icon of its own."""
    if os.name != "nt":
        sys.exit("Shortcuts are a Windows thing. Here, run: gm play")
    pythonw = shutil.which("pythonw")
    env = dict(os.environ, GM_ICON=str(ICON), GM_HOME=str(ENGINE), GM_DESKTOP="1" if desktop else "",
               GM_TARGET=pythonw or str(ENGINE / "Play.cmd"),
               GM_ARGS=f'"{ENGINE / "engine" / "gm.py"}" play' if pythonw else "",
               GM_STYLE="1" if pythonw else "7")   # 7: Play.cmd's console opens minimized. pythonw has none, and would pass 7 on to the window
    script = ("$dir = if ($env:GM_DESKTOP) { [Environment]::GetFolderPath('Desktop') } else { $env:GM_HOME }; "
              "$name = if ($env:GM_DESKTOP) { 'GM Engine.lnk' } else { 'Play.lnk' }; "
              "$link = (New-Object -ComObject WScript.Shell).CreateShortcut((Join-Path $dir $name)); "
              "$link.TargetPath = $env:GM_TARGET; $link.Arguments = $env:GM_ARGS; $link.WorkingDirectory = $env:GM_HOME; "
              "$link.IconLocation = $env:GM_ICON + ',0'; $link.Description = 'GM Engine: the play window'; "
              "$link.WindowStyle = [int]$env:GM_STYLE; $link.Save(); $link.FullName")
    done = subprocess.run(["powershell", "-NoProfile", "-Command", script], env=env, capture_output=True, text=True,
                          creationflags=NO_WINDOW)
    if done.returncode:
        sys.exit(f"Couldn't make the shortcut: {done.stderr.strip()}")
    print(f"Made {done.stdout.strip()}. Double-click it to play; it can be moved or pinned anywhere.")


def close_window(server):
    """Exit Game: close the desktop window, or stop waiting on the browser tab."""
    server.quit = True
    for window in list(getattr(sys.modules.get("webview"), "windows", [])):
        window.destroy()


def set_fullscreen(server, on):
    """The Fullscreen setting, for the desktop window. False if there isn't one: a browser tab does its own."""
    windows = list(getattr(sys.modules.get("webview"), "windows", []))
    if windows and on != server.fullscreen:   # pywebview can only toggle, so which way the window is gets kept here
        windows[0].toggle_fullscreen()
        if not on:
            windows[0].maximize()   # a window that opened fullscreen would otherwise come back small
        server.fullscreen = on
    return bool(windows)


def finish():
    """Let a beat in progress finish writing before the program exits."""
    for g in list(GAMES.values()):
        if g.thread and g.thread.is_alive():
            g.thread.join(timeout=600)


def serve(start):
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    server.start = remember(start) if start and (Path(start) / CONFIG).exists() else None
    server.seen = None
    server.quit = False
    server.fullscreen = False
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
            # Lets the menu's music start without waiting for a click (the window is WebView2 on Windows).
            os.environ.setdefault("WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS", "--autoplay-policy=no-user-gesture-required")
            if os.name == "nt":  # its own taskbar button with the die on it, not one grouped under Python's
                import ctypes
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("GMEngine.Play")
            server.fullscreen = bool(read_json(PREFS, {}).get("fullscreen"))
            webview.create_window("GM Engine", url, width=1360, height=900, min_size=(900, 600), maximized=True,
                                  fullscreen=server.fullscreen, text_select=True)   # off by default in pywebview; flagging a passage needs it
            webview.start(icon=str(ICON))
        else:
            print(f"GM Engine: {url}\nRunning on this computer only. Close the tab, or press Ctrl+C here, to stop.")
            webbrowser.open(url)
            try:
                while not server.quit and (server.seen is None or time.time() - server.seen < IDLE_QUIT):
                    time.sleep(1)
            except KeyboardInterrupt:
                pass
    finally:
        finish()
        server.shutdown()
        server.server_close()
    return 0
