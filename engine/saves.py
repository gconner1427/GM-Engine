"""Saved games: the whole narrative folder as it stood, kept on this computer.

    gm save ["<a name for it>"]
    gm saves
    gm load <number from gm saves>

A save is a Git commit in the narrative's own folder, with no remote: nothing is uploaded.
The player never sees Git. Each save records which session it was made in and the character's
name and level, and that's how the play window lists them.

Loading puts every file back the way the save had it. The game as it stood is saved first, so
loading never loses anything, and a later save can always be loaded again.
"""

import json
import re
import shutil
import subprocess
import sys

from narrative import CONFIG, field

MARK = "gm-save: "
IGNORE = ["GM Only/Logs/gui.json", "*.tmp"]  # the window's own conversation isn't part of the game
NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)
SETTINGS = ["-c", "user.name=GM Engine", "-c", "user.email=saves@gm-engine.invalid", "-c", "core.autocrlf=false",
            "-c", "core.safecrlf=false", "-c", "core.quotepath=false", "-c", "commit.gpgsign=false"]


def git(narrative, *args, check=True):
    program = shutil.which("git")
    if not program:
        raise ValueError("Saving needs Git, and it isn't installed on this computer.")
    done = subprocess.run([program, *SETTINGS, *args], cwd=narrative.root, capture_output=True, encoding="utf-8",
                          errors="replace", creationflags=NO_WINDOW)
    if check and done.returncode:
        raise ValueError(f"Saving hit a problem: {(done.stderr or done.stdout).strip()[-300:]}")
    return done


def ready(narrative):
    """Make sure the narrative folder can hold saves."""
    if not (narrative.root / ".git").exists():
        git(narrative, "init", "-q", "-b", "saves")
    ignore = narrative.root / ".gitignore"
    have = ignore.read_text(encoding="utf-8").splitlines() if ignore.exists() else []
    missing = [line for line in IGNORE if line not in have]
    if missing:
        ignore.write_text("\n".join(have + missing) + "\n", encoding="utf-8")


def standing(narrative):
    """Where the game is right now: what a save's card shows."""
    cfg = json.loads((narrative.root / CONFIG).read_text(encoding="utf-8-sig"))
    sheet = narrative.sheet.read_text(encoding="utf-8-sig") if narrative.sheet.exists() else ""
    name = field(sheet, "Name") or ""
    return {"session": cfg.get("sessions", 0), "open": bool(cfg.get("open_session")), "beats": cfg.get("beats", 0),
            "character": "" if name.lower().startswith(("unknown", "(")) else name, "level": field(sheet, "Level") or "",
            "title": cfg.get("name", narrative.name)}


def save(narrative, label="", auto=False):
    """Save the game as it stands. Returns the save, or None for an autosave with nothing new in it."""
    ready(narrative)
    git(narrative, "add", "-A")
    first = git(narrative, "rev-parse", "--verify", "-q", "HEAD", check=False).returncode != 0
    changed = first or git(narrative, "diff", "--cached", "--quiet", check=False).returncode != 0
    if auto and not changed:
        return None
    info = dict(standing(narrative), label=re.sub(r"\s+", " ", label or "").strip()[:80], auto=auto)
    subject = info["label"] or f"Session {info['session']}"
    git(narrative, "commit", "-q", "--allow-empty", "-m", f"{subject}\n\n{MARK}{json.dumps(info, ensure_ascii=False)}")
    return listing(narrative)[0]


def listing(narrative):
    """Every save, newest first."""
    if not (narrative.root / ".git").exists():
        return []
    log = git(narrative, "log", "--format=%H%x1f%cI%x1f%B%x1e", check=False)
    found = []
    for record in (log.stdout or "").split("\x1e"):
        parts = record.strip().split("\x1f")
        if len(parts) != 3:
            continue
        mark = next((line for line in parts[2].splitlines() if line.startswith(MARK)), None)
        if not mark:
            continue
        try:
            info = json.loads(mark[len(MARK):])
        except ValueError:
            continue
        found.append(dict(info, id=parts[0], when=parts[1]))
    return found


def load(narrative, save_id):
    """Put the narrative back the way a save had it. The game as it stands is saved first."""
    chosen = next((s for s in listing(narrative) if s["id"] == save_id), None)
    if not chosen:
        raise ValueError("That save isn't in this narrative.")
    save(narrative, "Before loading an earlier save", auto=True)
    git(narrative, "read-tree", "-u", "--reset", save_id)  # every saved file back as it was; later ones removed
    return chosen


# ---- the command line --------------------------------------------------------

def describe(s):
    who = f"{s['character']}, level {s['level']}" if s.get("character") else "no character yet"
    where = f"Session {s['session']}" + ("" if s.get("open") else " (between sessions)") if s.get("session") else "before the first session"
    return f"{s['when'][:16].replace('T', ' ')}  {where}  {who}" + (f"  \"{s['label']}\"" if s.get("label") else "") + ("  [autosave]" if s.get("auto") else "")


def run(narrative, cmd, args):
    try:
        if cmd == "save":
            print("Saved: " + describe(save(narrative, " ".join(args))))
        elif cmd == "saves":
            found = listing(narrative)
            for n, s in enumerate(found, 1):
                print(f"{n:>3}. {describe(s)}")
            if not found:
                print("No saves yet. Run: gm save")
        else:
            found = listing(narrative)
            if not args or not args[0].isdigit() or not 1 <= int(args[0]) <= len(found):
                sys.exit("Usage: gm load <number from gm saves>")
            print("Loaded: " + describe(load(narrative, found[int(args[0]) - 1]["id"])))
    except ValueError as e:
        sys.exit(str(e))
    return 0
