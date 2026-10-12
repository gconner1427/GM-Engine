"""Illustrations: portraits, places, scenes, and items, painted by Codex's image generation.

    gm art portrait "Martin Hale" "<what the character has seen of him>"
    gm art place "The Fleece" "<what it looks like from where she stands>"     also sets the backdrop
    gm art place "The Fleece"                                                  back there again: backdrop only
    gm art scene|item "<name>" "<what it looks like>"
    gm art portrait "Martin Hale" --was "the peddler"                          she's learned his name
    gm art portrait "Martin Hale" "<new look>" --redo                          paint it again
    gm art list
    gm art run                                                                 paint what's waiting, now

The GM asks for a picture with `gm art`, which only writes the request into Art/art.json and
returns at once. The play window paints what's waiting in the background, one at a time, by
running the Codex program that the VS Code extension installed (signed in as the user). Without
the window, `gm art run` does the same. Art/ is the player's to look at, so a request describes
only what the character has seen.
"""

import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import time
import zlib
from pathlib import Path

from narrative import field

KINDS = {"portrait": "Portraits", "place": "Places", "scene": "Scenes", "item": "Items"}
FRAMING = {
    "portrait": "A portrait of one person, head and shoulders, square format, plain dark background.",
    "place": "An establishing view of a place, wide landscape format, with no people prominent in it.",
    "scene": "A single moment, wide landscape format.",
    "item": "One object on its own, square format, plain dark background.",
}
DEFAULT_STYLE = "Painterly illustration with visible brushwork, muted natural colours, soft directional light."
GENERATED = Path.home() / ".codex" / "generated_images"
SETTINGS = Path.home() / ".gm-engine" / "config.json"  # optional: {"codex": "<path to codex>"}
TIMEOUT = 420
PALE_MEAN, PALE_HIGH = 102, 180   # a place's strip is pale above either: its mean brightness, or where its brightest twentieth begins (of 255)
NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)


def safe(name):
    return re.sub(r'[<>:"/\\|?*]', "", name).strip()


def now():
    return datetime.datetime.now().isoformat(timespec="seconds")


# ---- the index ---------------------------------------------------------------

def art_dir(narrative):
    return narrative.root / "Art"


def load(narrative):
    try:
        data = json.loads((art_dir(narrative) / "art.json").read_text(encoding="utf-8-sig"))
    except (OSError, ValueError):
        data = {}
    data.setdefault("backdrop", None)
    data.setdefault("items", [])
    return data


def save(narrative, data):
    folder = art_dir(narrative)
    folder.mkdir(exist_ok=True)
    tmp = folder / "art.tmp"
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, folder / "art.json")


def find(data, kind, name):
    for item in data["items"]:
        if item["kind"] == kind and item["name"].lower() == name.lower():
            return item
    return None


def style(narrative):
    """(on, art style) from the narrative's Style Guide. Illustrations are on unless it says off."""
    guide = narrative.root / "Style Guide.md"
    text = guide.read_text(encoding="utf-8-sig") if guide.exists() else ""
    on = not (field(text, "Illustrations") or "").lower().startswith("off")
    look = field(text, "Art style") or ""
    return on, DEFAULT_STYLE if not look or look.lower().startswith(("unknown", "(")) else look


# ---- asking for a picture ------------------------------------------------------

def request(narrative, kind, name, look=None, was=None, redo=False):
    if kind not in KINDS:
        sys.exit(f"Kinds of picture: {', '.join(KINDS)}.")
    if not safe(name):
        sys.exit("The picture needs a name: who or what it's of, as the character knows it.")
    if not style(narrative)[0]:
        print("Illustrations are off in this narrative's Style Guide. Nothing was asked for.")
        return 0
    data = load(narrative)
    item = find(data, kind, was) if was else None
    if item:
        if find(data, kind, name):
            sys.exit(f"There's already a {kind} called {name!r}.")
        item["name"] = name
        if data["backdrop"] and data["backdrop"].lower() == was.lower():
            data["backdrop"] = name
        print(f"{was} is now {name}.")
    item = item or find(data, kind, name)
    if kind == "place":
        data["backdrop"] = name
    if item and item["status"] == "failed":
        look, redo = look or item.get("look"), True  # asking again is how a failed one gets another try
    if item and not (redo and look):
        save(narrative, data)
        if not was:
            print(f"There's already a {kind} of {name} ({item['status']})." + (" It's the backdrop now." if kind == "place" else ""))
        return 0
    if not look:
        sys.exit(f"No {kind} of {name!r} yet. Say what it looks like, from what the character has seen.")
    if not item:
        item = {"kind": kind, "name": name}
        data["items"].append(item)
    item.update(look=look, status="waiting", asked=now(), session=narrative.config.get("sessions", 0), error="")
    item.pop("file", None)
    item.pop("pale", None)
    save(narrative, data)
    print(f"Asked for a {kind} of {name}. It'll be painted in the background.")
    return 0


def listing(narrative):
    data = load(narrative)
    on, look = style(narrative)
    print(f"Illustrations: {'on' if on else 'off'}   Style: {look}")
    print(f"Backdrop: {data['backdrop'] or 'none'}")
    for item in data["items"]:
        print(f"  {item['status']:8} {item['kind']:9} {item['name']}" + (f"   ({item['error']})" if item.get("error") else ""))
    return 0


# ---- painting ------------------------------------------------------------------

def find_codex():
    """The Codex program: the one in config.json, on the PATH, or inside the VS Code extension."""
    try:
        chosen = json.loads(SETTINGS.read_text(encoding="utf-8-sig")).get("codex")
    except (OSError, ValueError):
        chosen = None
    if chosen and Path(chosen).exists():
        return chosen
    found = shutil.which("codex")
    if found:
        return found
    version = lambda p: [int(n) for n in re.findall(r"\d+", p.parts[-4])]  # the extension's folder name
    bundled = sorted(Path.home().glob(".vscode*/extensions/openai.chatgpt-*/bin/*/codex*"), key=version)
    bundled = [p for p in bundled if p.stem == "codex"]
    return str(bundled[-1]) if bundled else None


def codex_state():
    """What the play window says about Codex when it opens: "ready", "signed out", or "missing"."""
    codex = find_codex()
    if not codex:
        return "missing"
    try:
        done = subprocess.run([codex, "login", "status"], stdin=subprocess.DEVNULL, capture_output=True,
                              encoding="utf-8", errors="replace", timeout=15, creationflags=NO_WINDOW)
    except (OSError, subprocess.TimeoutExpired):
        return "signed out"
    said = f"{done.stdout}\n{done.stderr}"   # "Logged in using ChatGPT"; signed out, it says it's not logged in
    return "ready" if re.search(r"^\s*logged in", said, re.IGNORECASE | re.MULTILINE) else "signed out"


def brief(kind, look, art_style):
    return ("Use your image generation tool to make exactly one image. Do not run any shell commands, and do not "
            "copy, move, or edit any files.\n\n"
            f"{FRAMING[kind]}\n\nWhat it shows: {look}\n\nStyle: {art_style}\n\n"
            "No text, lettering, captions, borders, or signatures anywhere in the image.\n\n"
            "When it is done, reply with only the full path of the generated PNG file.")


def newest_since(started):
    if not GENERATED.exists():
        return None
    fresh = [p for p in GENERATED.rglob("*.png") if p.stat().st_mtime >= started]
    return max(fresh, key=lambda p: p.stat().st_mtime) if fresh else None


def paint(narrative, item, codex):
    """Have Codex paint one request. Returns the saved file's path relative to Art/, or raises ValueError."""
    folder = art_dir(narrative)
    started = time.time() - 2
    try:
        done = subprocess.run([codex, "exec", "--skip-git-repo-check", "--sandbox", "read-only", "--ephemeral",
                               "-C", str(folder), "-"],
                              input=brief(item["kind"], item["look"], style(narrative)[1]), capture_output=True,
                              encoding="utf-8", errors="replace", timeout=TIMEOUT, creationflags=NO_WINDOW)
    except subprocess.TimeoutExpired:
        raise ValueError("Codex took too long.")
    said = (done.stdout or "").strip()
    named = re.findall(r"[A-Za-z]:[\\/][^\r\n\"'<>|]*?\.png|/[^\r\n\"'<>|]*?\.png", said)
    source = next((Path(p) for p in reversed(named) if Path(p).exists()), None) or newest_since(started)
    if not source:
        tail = (said or done.stderr or "").strip().splitlines()
        raise ValueError(tail[-1][:300] if tail else "Codex made no image.")
    target = folder / KINDS[item["kind"]] / f"{safe(item['name'])}.png"
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    return target.relative_to(folder).as_posix()


def paint_next(narrative):
    """Paint the oldest waiting request. Returns it as it now stands, or None when nothing is waiting."""
    waiting = [i for i in load(narrative)["items"] if i["status"] == "waiting"]
    if not waiting or not style(narrative)[0]:
        return None
    codex = find_codex()
    if not codex:
        raise ValueError("Can't find Codex. Install the Codex extension in VS Code and sign in, or put the path to "
                         f"codex in {SETTINGS} as {{\"codex\": \"...\"}}.")
    job = waiting[0]
    try:
        result = {"file": paint(narrative, job, codex), "status": "ready", "painted": now(), "error": ""}
        if job["kind"] == "place":
            result["pale"] = pale(art_dir(narrative) / result["file"])
    except ValueError as e:
        result = {"status": "failed", "error": str(e)}
    data = load(narrative)  # reread: the GM may have asked for more in the meantime
    item = find(data, job["kind"], job["name"])
    if item and item.get("asked") == job.get("asked"):
        item.update(result)
        save(narrative, data)
    return dict(job, **result)


# ---- how pale a place is ---------------------------------------------------------

def pale(path):
    """Whether the strip of a place's picture that the play window shows above the story is a pale one, which the
    window then darkens further so the painting is never the brightest thing over the prose. True as well for a
    picture that can't be measured. The PNG is read here, a row at a time and only as far down as the strip goes."""
    try:
        raw = Path(path).read_bytes()
        if raw[:8] != b"\x89PNG\r\n\x1a\n":
            return True
        at, packed, head = 8, [], None
        while at + 8 <= len(raw):
            size, kind = int.from_bytes(raw[at:at + 4], "big"), raw[at + 4:at + 8]
            body = raw[at + 8:at + 8 + size]
            if kind == b"IHDR":
                head = body
            elif kind == b"IDAT":
                packed.append(body)
            elif kind == b"IEND":
                break
            at += 12 + size
        w, h = int.from_bytes(head[:4], "big"), int.from_bytes(head[4:8], "big")
        if head[8] != 8 or head[9] not in (2, 6) or head[12]:   # eight bits a channel, in colour, not interlaced
            return True
        n = 3 if head[9] == 2 else 4
        # the strip: as wide as the story's side of the window and as shallow as the band, a little above the middle
        shown = min(h, round(w * 96 / 1420))
        top = round((h - shown) * .42)
        left, right = round(w * .22), round(w * .78)
        step = max(1, (right - left) // 256)
        line = 1 + w * n
        rows = zlib.decompressobj().decompress(b"".join(packed), line * (top + shown))
        if len(rows) < line * (top + shown):
            return True
        above, seen = bytearray(w * n), []
        for y in range(top + shown):
            how, row = rows[y * line], bytearray(rows[y * line + 1:(y + 1) * line])
            if how == 1:
                for i in range(n, len(row)):
                    row[i] = (row[i] + row[i - n]) & 255
            elif how == 2:
                for i in range(len(row)):
                    row[i] = (row[i] + above[i]) & 255
            elif how == 3:
                for i in range(len(row)):
                    row[i] = (row[i] + ((row[i - n] if i >= n else 0) + above[i] >> 1)) & 255
            elif how == 4:
                for i in range(len(row)):
                    a, b, c = (row[i - n], above[i], above[i - n]) if i >= n else (0, above[i], 0)
                    p = a + b - c
                    pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                    row[i] = (row[i] + (a if pa <= pb and pa <= pc else b if pb <= pc else c)) & 255
            elif how:
                return True
            if y >= top:
                seen += [(2126 * row[x * n] + 7152 * row[x * n + 1] + 722 * row[x * n + 2]) // 10000 for x in range(left, right, step)]
            above = row
        seen.sort()
        return sum(seen) / len(seen) > PALE_MEAN or seen[len(seen) * 95 // 100] > PALE_HIGH
    except Exception:
        return True


def measure_next(narrative):
    """Measure one place that was painted before its paleness was kept. Returns whether one was written down."""
    todo = next((i for i in load(narrative)["items"] if i["kind"] == "place" and i["status"] == "ready" and i.get("file") and "pale" not in i), None)
    if not todo:
        return False
    found = pale(art_dir(narrative) / todo["file"])
    data = load(narrative)  # reread: it may have been painted again in the meantime
    item = find(data, "place", todo["name"])
    if not item or "pale" in item or item.get("file") != todo["file"] or item.get("painted") != todo.get("painted"):
        return False
    item["pale"] = found
    save(narrative, data)
    return True


def run(narrative):
    count = 0
    try:
        while True:
            item = paint_next(narrative)
            if not item:
                break
            count += 1
            print(f"  {item['status']}: {item['name']}" + (f" ({item['error']})" if item.get("error") else ""))
    except ValueError as e:
        sys.exit(str(e))
    print(f"Painted {count}." if count else "Nothing is waiting.")
    return 0
