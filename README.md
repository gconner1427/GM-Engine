# GM Engine

A game master for solo narratives, run by Claude Code. You make a world and one character and say where it starts. After that you say only what your character does. The GM runs everything else (every other person, every monster, every event, and how your actions ripple outward), settles what's uncertain with rules and real dice behind the scenes, and writes what happens as third person limited prose. It reads like a novel, not like a game: no hit points, no damage numbers, no rolls on the page.

It grew out of the Living World Engine and keeps its idea of a persistent world. The difference is who's in charge. There, the engine proposes and the author decides everything. Here, you control one person and the GM decides the rest.

## How it works

### Two folders

| | Lives in | Holds |
|---|---|---|
| **The engine** | this folder | The rules, the writing rules, the procedures, the templates, and the scripts. Shared by every narrative. |
| **A narrative** | its own folder, wherever you choose | One world, one character, its sessions, and everything the GM tracks for it. |

You play from the narrative's folder. It points back at this one, so improving the engine improves every narrative. If you ever move this folder, each narrative's `CLAUDE.md`, `narrative.json`, and `.claude/settings.json` need the new path.

### What you can read

Inside a narrative:

- `Sessions/Session N.md`: the narrative itself, one file per session, growing as you play.
- `Character Sheet.md`: level, HP, attributes, skills, gear, money, and who your character is.
- `Journal.md`: what your character knows about people, places, and unfinished business.
- `World/`: the world as you set it up, plus what the page has shown since.
- `Style Guide.md`: tense, tone, content limits, and writing rules for this narrative.

`GM Only/` is the GM's: what other people want and know, what's moving off the page, every roll, every ruling. Nothing locks it. It's an honor system.

### Playing

Open the narrative's folder in VS Code and start a Claude Code conversation.

- **Anything you write outside braces is your character acting**, in first or third person: `I swing my sword at the goblin` or `Kendrick swings his sword at the goblin`. Say what they do, say, or try. The GM works out what comes of it and writes the beat, which stops when your character would have to do something you haven't said.
- **Anything in `{braces}` is you talking to the GM.** It never goes in the narrative.

Your character never does anything you didn't state: no picking things up, no starting conversations, no decisions. The GM does write their thoughts and reactions, from the personality on your sheet, so keep that part of the sheet true to who they are.

### Fixing the writing

When something reads wrong, say so in braces: `{that line sounds stiff}`, `{too flowery}`, `{that name sounds generated}`. The GM rewrites just that part in the session log and adds a writing rule so it doesn't happen again. Rules that would apply anywhere go in `Writing/Craft Rules.md` here; rules about one world go in that narrative's Style Guide. You can change or strike any rule.

### Other things to say in braces

| | |
|---|---|
| `{new session}` / `{end session}` | Start or close a session. Ending one updates the Journal and awards marks toward the next level. |
| `{sheet}` | Show the character sheet. |
| `{recap}` | Where things stand, as your character knows it. |
| `{undo}` | Take back the last beat. |
| `{I meant ...}` | The GM misread your action: it's replayed. |
| `{echo off}` | Beats go only to the session log, not the chat (faster, if you read from the file). |
| a question | Answered from what your character knows. |
| a change to the world or the sheet | Made. Your word is canon. |

## Starting a narrative

1. Double-click `New Narrative.cmd` and give it a name and a folder. (Or open this folder in VS Code and tell Claude "new narrative.")
2. Open the new folder in VS Code and tell Claude **"Set up this narrative."** It interviews you about the world, builds your character with you, and asks where the narrative starts.
3. Write your character's first action.

## What's in this folder

| Path | What it is |
|---|---|
| `ENGINE.md` | The operating manual: the folder map, what's tracked where, the loops, the principles |
| `Rules/Core Rules.md` | The game underneath: attributes, the roll and its five outcomes, health, fights, powers, growth. The same in every world. |
| `Rules/GM Rules.md` | The standing rules for the GM: who decides what, where a beat ends, honest dice, what's hidden |
| `Writing/Craft Rules.md` | The writing rules for every narrative (`Craft Rules History.md` has the reasons) |
| `Writing/House Style.md` | The prose defaults |
| `Writing/GM Philosophy.md` | Character first, no plot, an honest world |
| `Writing/Banned Names.md` | Names that are never used |
| `Procedures/` | New Narrative, Play, World Turn, Corrections |
| `Templates/` | What a new narrative, cast member, place, or group starts as |
| `engine/` | The scripts behind the `gm` command, including the dice |
| `gm.cmd`, `New Narrative.cmd` | Windows launchers |

## Requirements

- Python 3.10 or later. The scripts use only the standard library.
- Claude Code in VS Code, opened in a narrative folder.

The launchers are Windows `.cmd` files. On other systems, call `python engine/gm.py` directly.
