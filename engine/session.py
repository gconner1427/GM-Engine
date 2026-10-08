"""Sessions, the two logs, and the name pools.

Each session has two files. Sessions/Session N.md is the narrative: prose only, appended one
beat at a time. GM Only/Logs/Session N GM Log.md is the record behind it: what the player said,
every roll as it was made, and the GM's rulings.

A beat is staged in GM Only/Logs/beat.md and committed with `gm beat`:

    <<< PLAYER
    what the player wrote, word for word
    <<< GM
    rulings, and every new fact the beat established
    <<< PROSE
    the beat

A staging file with no markers is all prose.
"""

import datetime
import re
import sys

import dice
from narrative import ENGINE, field, section

MARKER = re.compile(r"(?m)^<<< (PLAYER|GM|PROSE)[ \t]*$")
USED = re.compile(r"^- ~~(.+?)~~")
BANNED = ENGINE / "Writing" / "Banned Names.md"


def now():
    return datetime.datetime.now().strftime("%H:%M")


def read(path):
    return path.read_text(encoding="utf-8-sig") if path.exists() else ""  # -sig: an editor may have added a BOM


def need_open(narrative):
    number = narrative.open_session()
    if not number:
        sys.exit("No session is open. Run: gm session start")
    return number


# ---- sessions --------------------------------------------------------------

def start(narrative):
    if narrative.open_session():
        sys.exit(f"Session {narrative.open_session()} is still open. Keep playing it, or run: gm session end")
    number = narrative.config.get("sessions", 0) + 1
    today = datetime.date.today().isoformat()
    narrative.sessions_dir.mkdir(exist_ok=True)
    narrative.logs_dir.mkdir(parents=True, exist_ok=True)
    narrative.session_log(number).write_text(f"# Session {number}\n", encoding="utf-8")
    head = (f"# Session {number} GM Log\n\nGM only. Started {today}. Each beat lists what the player wrote, "
            "the rolls made for it in the order they were made, and the rulings.\n\n")
    narrative.gm_log(number).write_text(head, encoding="utf-8")
    narrative.config.update(sessions=number, open_session=number, beats=0, log_mark=len(head))
    narrative.save()
    print(f"Session {number} is open: {narrative.session_log(number).relative_to(narrative.root)}")
    return 0


def end(narrative):
    number = need_open(narrative)
    append_log(narrative, f"\nSession {number} ended {datetime.date.today().isoformat()} after {narrative.config.get('beats', 0)} beats.\n")
    narrative.config["open_session"] = None
    narrative.save()
    print(f"Session {number} is closed.")
    return 0


# ---- the GM log ------------------------------------------------------------

def append_log(narrative, text):
    """Add to the open session's GM log. Silently does nothing between sessions."""
    number = narrative.open_session()
    if not number:
        return False
    path = narrative.gm_log(number)
    path.write_text(read(path) + text, encoding="utf-8")
    return True


def log_roll(narrative, kind, why, lines):
    """Print a roll, and record it if a session is open."""
    print(f"{kind}  {why}" if why else kind)
    for line in lines:
        print(f"  {line}")
    if narrative:
        body = "; ".join(lines)
        append_log(narrative, f"- {now()} {kind} {why + ': ' if why else ''}{body}\n")
    return 0


def note(narrative, text):
    need_open(narrative)
    append_log(narrative, f"- {now()} NOTE {text}\n")
    print("Noted.")
    return 0


# ---- beats -----------------------------------------------------------------

def staged(text):
    """{'PLAYER': ..., 'GM': ..., 'PROSE': ...} from a staging file."""
    found = list(MARKER.finditer(text))
    if not found:
        return {"PROSE": text.strip()}
    parts = {}
    for i, m in enumerate(found):
        stop = found[i + 1].start() if i + 1 < len(found) else len(text)
        parts[m.group(1)] = text[m.end():stop].strip()
    return parts


def beat(narrative, again=False):
    number = need_open(narrative)
    parts = staged(read(narrative.staging))
    prose = parts.get("PROSE", "")
    if not prose:
        sys.exit(f"Nothing staged: {narrative.staging.relative_to(narrative.root)} has no prose.")
    if not again and prose == read(narrative.last_beat).strip():
        sys.exit("That beat is already in the session log. Stage the next one, or pass --again to repeat it.")

    session = narrative.session_log(number)
    session.write_text(read(session).rstrip("\n") + "\n\n" + prose + "\n", encoding="utf-8")
    narrative.last_beat.write_text(prose + "\n", encoding="utf-8")

    count = narrative.config.get("beats", 0) + 1
    log = narrative.gm_log(number)
    text = read(log)
    mark = min(narrative.config.get("log_mark", len(text)), len(text))
    entry = text[:mark] + f"### Beat {count}\n"
    if parts.get("PLAYER"):
        entry += f"**Player:** {parts['PLAYER']}\n"
    entry += text[mark:]  # the rolls made for this beat, already logged
    if parts.get("GM"):
        entry += f"**GM:** {parts['GM']}\n"
    entry += "\n"
    log.write_text(entry, encoding="utf-8")
    narrative.config.update(beats=count, log_mark=len(entry))
    narrative.save()
    print(f"Beat {count} added to Session {number}.")
    return 0


def undo(narrative):
    """Take the last beat back out of the session log. The GM log keeps its record."""
    number = need_open(narrative)
    last = read(narrative.last_beat).strip()
    session = narrative.session_log(number)
    text = read(session).rstrip("\n")
    if not last or not text.endswith(last):
        sys.exit("The session log no longer ends with the last beat (it was edited, or already withdrawn). Remove it by hand.")
    session.write_text(text[: -len(last)].rstrip("\n") + "\n", encoding="utf-8")
    narrative.last_beat.write_text("", encoding="utf-8")
    append_log(narrative, f"- {now()} WITHDRAWN Beat {narrative.config.get('beats', 0)} was taken out of the session log.\n\n")
    narrative.config["log_mark"] = len(read(narrative.gm_log(number)))
    narrative.save()
    print(f"Beat {narrative.config.get('beats', 0)} withdrawn from Session {number}.")
    return 0


# ---- names -----------------------------------------------------------------

def banned():
    return {m.group(1).strip().lower() for m in re.finditer(r"(?m)^- (.+)$", read(BANNED))}


def pools(text):
    """[(section title, [line index of every unused name])] for the world's Names.md."""
    lines, out, current = text.split("\n"), [], None
    fenced = False
    for i, line in enumerate(lines):
        if line.startswith("```"):
            fenced = not fenced
        if fenced:
            continue
        if line.startswith("## "):
            current = (line[3:].strip(), [])
            out.append(current)
        elif current and line.startswith("- ") and not USED.match(line) and line[2:].strip():
            current[1].append(i)
    return lines, out


def name(narrative, pool=None, who=None):
    path = narrative.world_dir / "Names.md"
    lines, found = pools(read(path))
    never = banned()
    found = [(t, [i for i in free if lines[i][2:].strip().lower() not in never]) for t, free in found]
    if not pool:
        print("Name pools in Names.md (unused names left):")
        for title, free in found:
            print(f"  {title}: {len(free)}")
        return 0
    matches = [(t, free) for t, free in found if pool.lower() in t.lower()]
    if len(matches) != 1:
        sys.exit(f"{len(matches)} pools match {pool!r}. Pools: {', '.join(t for t, _ in found) or 'none'}")
    title, free = matches[0]
    if not free:
        sys.exit(f"No unused names left in {title!r}. Add more to {path.relative_to(narrative.root)}.")
    i = dice.RNG.choice(free)
    picked = lines[i][2:].strip()
    lines[i] = f"- ~~{picked}~~" + (f" ({who})" if who else "")
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"{picked}  (from {title}; {len(free) - 1} left)")
    if narrative.open_session():
        append_log(narrative, f"- {now()} NAME {picked} from {title}{' for ' + who if who else ''}\n")
    return 0


# ---- status ----------------------------------------------------------------

def status(narrative):
    cfg = narrative.config
    print(f"{narrative.name}")
    if not cfg.get("set_up"):
        print("  Not set up yet: Procedures/New Narrative.md")
    opened = narrative.open_session()
    print(f"  Sessions: {cfg.get('sessions', 0)}" + (f"   Open: Session {opened}, {cfg.get('beats', 0)} beats" if opened else "   None open"))
    print(f"  Chat echo: {'on' if cfg.get('chat_echo', True) else 'off'}")
    vitals = section(read(narrative.sheet), "Vitals")
    if vitals:
        print("\n" + vitals)
    clock = section(read(narrative.state_dir / "World State.md"), "Story Clock")
    if clock:
        print("\n" + clock)
    found = narrative.pressures()
    print(f"\nPressures: {len(found)}")
    for title, text in found:
        print(f"  {title} [{field(text, 'Clock') or 'no clock'}]: {field(text, 'Stands') or ''}")
    return 0
