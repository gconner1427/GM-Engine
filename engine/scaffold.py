"""Creates narratives and entity docs from the templates in Templates/.

    gm new-narrative "The Shattered Coast" --at "D:/Narratives"
    gm add cast "Mara Hale"          also: place, group

Placeholders in templates: {{NARRATIVE}} {{ENGINE}} {{DATE}} {{NAME}}.
"""

import datetime
import json
import re
import shutil
import sys
from pathlib import Path

from narrative import CONFIG, ENGINE

TEMPLATES = ENGINE / "Templates"
DEFAULT_PARENT = Path.home() / "GM Narratives"
TEXT = {".md", ".json", ".txt", ""}
ADD_KINDS = {"cast": "Cast", "place": "Places", "group": "Groups"}


def safe(name):
    return re.sub(r'[<>:"/\\|?*]', "", name).strip()


def fill(folder, values):
    for p in folder.rglob("*"):
        if p.is_file() and p.suffix in TEXT:
            text = p.read_text(encoding="utf-8")
            for k, v in values.items():
                text = text.replace("{{" + k + "}}", v)
            p.write_text(text, encoding="utf-8")


def today():
    return datetime.date.today().isoformat()


def create_narrative(name, parent=None):
    """Make the narrative folder from the template. Returns its path; raises ValueError if it's taken."""
    if not safe(name):
        raise ValueError("The narrative needs a name.")
    target = Path(parent or DEFAULT_PARENT) / safe(name)
    if target.exists() and any(target.iterdir()):
        raise ValueError(f"{target} already exists and isn't empty.")
    shutil.copytree(TEMPLATES / "Narrative", target, dirs_exist_ok=True)
    for empty in ("Sessions", "GM Only/Logs"):
        (target / empty).mkdir(parents=True, exist_ok=True)
    fill(target, {"NARRATIVE": name, "ENGINE": ENGINE.as_posix(), "DATE": today()})
    config = {"name": name, "engine": ENGINE.as_posix(), "created": today(), "set_up": False,
              "chat_echo": True, "sessions": 0, "open_session": None, "beats": 0, "log_mark": 0}
    (target / CONFIG).write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    return target


def new_narrative(name, parent=None):
    try:
        target = create_narrative(name, parent)
    except ValueError as e:
        sys.exit(str(e))
    print(f"Created narrative: {target}")
    print(f'Next: set it up and play it in the window (gm play "{target}"),')
    print('      or open that folder in VS Code and tell Claude "Set up this narrative."')
    return 0


def add(narrative, kind, name):
    kind = kind.lower()
    if kind not in ADD_KINDS:
        sys.exit(f"Can add: {', '.join(ADD_KINDS)}. Items, threats, pressures, and minor entries are ### entries in their shared files.")
    folder = narrative.gm_dir / ADD_KINDS[kind]
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{safe(name)}.md"
    if path.exists():
        sys.exit(f"Already exists: {path.relative_to(narrative.root)}")
    text = (TEMPLATES / "Entries" / f"{kind.title()}.md").read_text(encoding="utf-8").replace("{{NAME}}", name)
    path.write_text(text, encoding="utf-8")
    print(f"Created {path.relative_to(narrative.root)}")
    return 0
