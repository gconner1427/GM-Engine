# GM Engine

A game master for solo narratives, run by Claude Code. You say what kind of narrative you want (the genre and tone, and whether the world is original or built on D&D or another setting) and make one character. The GM builds the world and keeps it to itself, the way a GM prepares a campaign, so you discover it by playing. After that you say only what your character does. The GM runs everything else (every other person, every monster, every event, and how your actions ripple outward), settles what's uncertain with rules and real dice behind the scenes, and writes what happens as third person limited prose. It reads like a novel, not like a game: no hit points, no damage numbers, no rolls on the page.

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
- `Style Guide.md`: tense, tone, content limits, and writing rules for this narrative.

`GM Only/` is the GM's: the world itself and how it really works, what other people want and know, what's moving off the page, every roll, every ruling. Nothing locks it. It's an honor system.

### The play window

Double-click `Play.cmd`. It opens a desktop window that lists your narratives, creates new ones, and is where you set them up and play them.

- **The narrative** fills the main column and grows as you play. Earlier sessions are in the picker at the top.
- **The message box** at the bottom is how you play. "As my character" sends an action; "To the GM" sends a note in braces for you.
- **The side panel** shows your character as a game sheet (health, strain and marks as bars, attributes and defenses as tiles, skills with rank pips, gear as an inventory), the Journal (what your character knows about the world, its people and its places), and your conversation with the GM. When the sheet changes, the bars slide and show the change.
- **The top bar** has text size (A− and A+), a button to hide the side panel for reading, and the ⋯ menu.
- **To flag a passage,** select it in the narrative and press "Flag this passage," then say what's wrong with it.
- **During setup** the main column is your conversation with the GM: it tells you what your character would know about the world and helps you make them, and the Character tab fills in as you go.

The window hands what you type to Claude Code, the same GM that runs in VS Code, using the copy the VS Code extension installed and your existing sign-in. VS Code doesn't need to be open. The window never shows rolls, rulings, or anything in `GM Only/`.

"Start a fresh GM conversation" in the ⋯ menu is for when the GM seems confused or slow after a very long sitting: nothing in the narrative changes, and the GM rereads its notes on the next message.

### Playing

Use the play window, or open the narrative's folder in VS Code and start a Claude Code conversation there. Either way:

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
| a question about the world | Answered with what your character knows, and no more. |
| a change to the sheet, or to the world | Made. Your word is canon. |

## Starting a narrative

1. Double-click `Play.cmd`. Under "A new narrative," give the genre and tone, choose the world (original, D&D, or another setting you name), add a title if you have one, and press **Create the world**.
2. The GM builds the world. This is the longest wait in the engine, several minutes. It then tells you what your character would know and asks who they are.
3. Make your character with the GM, and say where they are when it opens (or leave that to the GM).
4. Write your character's first action.

The GM asks you nothing else about the world, and never shows you what it built.

Without the window: double-click `New Narrative.cmd`, open the new folder in VS Code, and tell Claude "Set up this narrative."

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
| `engine/` | The scripts behind the `gm` command, including the dice and the play window (`gui.py`, `gui/app.html`) |
| `Play.cmd`, `gm.cmd`, `New Narrative.cmd` | Windows launchers |

## Requirements

- Python 3.10 or later. The scripts use only the standard library.
- The Claude Code extension in VS Code, signed in.
- For the play window in its own desktop window: `pip install pywebview`. Without it, the window opens as a browser tab.

The play window keeps its list of narratives in `.gm-engine/narratives.json` in your home folder. An optional `.gm-engine/config.json` can set `"claude"` (the path to Claude Code, if it isn't found) and `"model"`.

The launchers are Windows `.cmd` files. On other systems, call `python engine/gm.py` directly.
