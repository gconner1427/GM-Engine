"""Finds the narrative a command is running in and knows its layout.

A narrative is any folder with a narrative.json at its root. Commands run from anywhere inside
it (or pass --narrative). Everything other modules need to know about the layout lives here.
"""

import json
import re
import sys
from pathlib import Path

ENGINE = Path(__file__).resolve().parents[1]
CONFIG = "narrative.json"


def utf8_stdout():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")


class Narrative:
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.config_path = self.root / CONFIG
        self.config = json.loads(self.config_path.read_text(encoding="utf-8"))
        self.name = self.config["name"]
        self.sessions_dir = self.root / "Sessions"
        self.gm_dir = self.root / "GM Only"
        self.world_dir = self.gm_dir / "World"
        if not self.world_dir.exists() and (self.root / "World").exists():
            self.world_dir = self.root / "World"  # a narrative made when the player wrote the world
        self.state_dir = self.gm_dir / "State"
        self.logs_dir = self.gm_dir / "Logs"
        self.sheet = self.root / "Character Sheet.md"
        self.staging = self.logs_dir / "beat.md"
        self.last_beat = self.logs_dir / "last beat.md"

    def save(self):
        self.config_path.write_text(json.dumps(self.config, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    def open_session(self):
        """The number of the session being played, or None between sessions."""
        return self.config.get("open_session")

    def session_log(self, number):
        return self.sessions_dir / f"Session {number}.md"

    def gm_log(self, number):
        return self.logs_dir / f"Session {number} GM Log.md"

    def pressures(self):
        path = self.state_dir / "Pressures.md"
        return entries(path.read_text(encoding="utf-8")) if path.exists() else []


def find_narrative(explicit=None, required=True):
    if explicit:
        root = Path(explicit)
        if not (root / CONFIG).exists():
            sys.exit(f"No {CONFIG} in {root}")
        return Narrative(root)
    here = Path.cwd().resolve()
    for p in [here] + list(here.parents):
        if (p / CONFIG).exists():
            return Narrative(p)
    if required:
        sys.exit(f"Not inside a narrative (no {CONFIG} here or above). Run from a narrative folder or pass --narrative <path>.")
    return None


# ---- text helpers ----------------------------------------------------------

def entries(text):
    """(name, text) for every '### Name' entry in a shared file. Format samples in ``` fences don't count."""
    text = re.sub(r"(?ms)^```.*?^```[^\n]*$", "", text)
    parts = re.split(r"(?m)^### ", text)[1:]
    return [(p.split("\n", 1)[0].strip(), "### " + p.strip()) for p in parts]


def field(text, name):
    m = re.search(rf"(?m)^(?:- )?\*\*{re.escape(name)}:\*\*(.*)$", text)
    return m.group(1).strip() if m else None


def section(text, heading):
    """The '## heading' section up to the next '## ' heading, or None."""
    m = re.search(rf"(?m)^## {re.escape(heading)}\s*$", text)
    if not m:
        return None
    rest = text[m.start():]
    nxt = re.search(r"(?m)^(## |---\s*$)", rest[3:])
    return rest[: nxt.start() + 3].strip() if nxt else rest.strip()
