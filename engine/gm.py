"""GM Engine: one command for every script.

Run from anywhere inside a narrative (a folder with narrative.json), or pass --narrative <path>.

    gm play ["<narrative folder>"] [--browser]   the play window: set up and play narratives
    gm new-narrative "<Name>" [--at <parent folder>]
    gm status                                 session, vitals, the clock, pressures

    gm session start | end
    gm beat [--again]                          commit the staged beat (GM Only/Logs/beat.md)
    gm undo                                    take the last beat back out of the session log
    gm note "<text>"                           a line in the GM log

    gm check <bonus> <target> "<why>" [--edge | --setback]
    gm attack <bonus> <defense> <damage> "<why>" [--armor N] [--edge | --setback]
    gm roll <dice> "<why>"                     2d6+3, d20, 1d8-1
    gm fate <odds> "<question>"                certain, likely, even, unlikely, remote, or a percent

    gm name                                    the name pools and how many names each has left
    gm name "<pool>" [--for "<who>"]           draw an unused name and mark it used
    gm add cast|place|group "<Name>"

    gm art portrait|place|scene|item "<name>" ["<what it looks like>"] [--was "<old name>"] [--redo]
    gm art list | run                          what's been asked for; paint what's waiting

    gm save ["<a name for it>"]                save the game as it stands (kept on this computer only)
    gm saves                                   every save, newest first
    gm load <number>                           put the narrative back the way a save had it

Every roll made while a session is open is written to that session's GM log.
"gm" is shorthand for: python "<engine folder>/engine/gm.py"
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import dice  # noqa: E402
import scaffold  # noqa: E402
import session  # noqa: E402
from narrative import find_narrative, utf8_stdout  # noqa: E402

ROLLS = {"check", "attack", "roll", "fate"}


def take(args, name, has_value=True):
    """Pull --name value / --name=value / --name out of args."""
    for i, a in enumerate(args):
        if a == f"--{name}":
            if not has_value:
                del args[i]
                return True
            value = args[i + 1] if i + 1 < len(args) else ""
            del args[i:i + 2]
            return value
        if has_value and a.startswith(f"--{name}="):
            del args[i]
            return a.split("=", 1)[1]
    return False if not has_value else None


def number(text, what):
    try:
        return int(text)
    except ValueError:
        sys.exit(f"{what} has to be a whole number, got {text!r}.")


def rolls(cmd, args, narrative):
    edge, setback = take(args, "edge", False), take(args, "setback", False)
    armor = take(args, "armor")
    if cmd == "check":
        if len(args) < 2:
            sys.exit('Usage: gm check <bonus> <target> "<why>" [--edge | --setback]')
        _, text = dice.check(number(args[0], "The bonus"), number(args[1], "The target"), edge, setback)
        return session.log_roll(narrative, "CHECK", " ".join(args[2:]), [text])
    if cmd == "attack":
        if len(args) < 3:
            sys.exit('Usage: gm attack <bonus> <defense> <damage> "<why>" [--armor N] [--edge | --setback]')
        _, lines = dice.attack(number(args[0], "The bonus"), number(args[1], "The defense"), args[2],
                               number(armor, "Armor") if armor else 0, edge, setback)
        return session.log_roll(narrative, "ATTACK", " ".join(args[3:]), lines)
    if cmd == "roll":
        if not args:
            sys.exit('Usage: gm roll <dice> "<why>"')
        total, shown = dice.roll(args[0])
        return session.log_roll(narrative, "ROLL", " ".join(args[1:]), [f"{args[0]}: {shown} = {total}"])
    if len(args) < 1:
        sys.exit('Usage: gm fate <odds> "<question>"')
    _, text = dice.fate(args[0])
    return session.log_roll(narrative, "FATE", " ".join(args[1:]), [text])


def main(argv):
    utf8_stdout()
    args = list(argv)
    if not args or args[0] in ("-h", "--help", "help"):
        print(__doc__)
        return 0
    cmd, args = args[0], args[1:]
    path = take(args, "narrative")

    if cmd == "play":
        import gui
        browser = take(args, "browser", False)
        return gui.run(args[0] if args else path, browser)
    if cmd == "new-narrative":
        at = take(args, "at")
        if not args:
            sys.exit('Usage: gm new-narrative "<Name>" [--at <parent folder>]')
        return scaffold.new_narrative(args[0], at)
    if cmd in ROLLS:  # dice work anywhere; they're only logged inside a narrative
        return rolls(cmd, args, find_narrative(path, required=False))

    narrative = find_narrative(path)
    if cmd == "status":
        return session.status(narrative)
    if cmd == "session":
        if args[:1] == ["start"]:
            return session.start(narrative)
        if args[:1] == ["end"]:
            return session.end(narrative)
        sys.exit("Usage: gm session start | end")
    if cmd == "beat":
        return session.beat(narrative, take(args, "again", False))
    if cmd == "undo":
        return session.undo(narrative)
    if cmd == "note":
        return session.note(narrative, " ".join(args)) if args else sys.exit('Usage: gm note "<text>"')
    if cmd == "name":
        who = take(args, "for")
        return session.name(narrative, args[0] if args else None, who)
    if cmd in ("save", "saves", "load"):
        import saves
        return saves.run(narrative, cmd, args)
    if cmd == "art":
        import art
        was, redo = take(args, "was"), take(args, "redo", False)
        if args[:1] == ["list"]:
            return art.listing(narrative)
        if args[:1] == ["run"]:
            return art.run(narrative)
        if len(args) < 2:
            sys.exit('Usage: gm art portrait|place|scene|item "<name>" ["<what it looks like>"] [--was "<old name>"] [--redo]')
        return art.request(narrative, args[0].lower(), args[1], " ".join(args[2:]) or None, was, redo)
    if cmd == "add":
        return scaffold.add(narrative, args[0], " ".join(args[1:])) if len(args) >= 2 else sys.exit('Usage: gm add cast|place|group "<Name>"')
    sys.exit(f"Unknown command: {cmd}. Run gm --help.")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]) or 0)
