# GM Engine

A game master for solo narratives, run by Claude Code. You say what kind of narrative you want (the genre and tone, whether the world is original, built on D&D or another setting, or an isekai, and what the story is about, if you have one in mind) and make one character. The GM builds the world and a campaign in it, the way a GM prepares one before the players sit down, and keeps both to itself, so you discover them by playing. The campaign has a goal your character is meant to work toward (bring down a dark lord, stop a war, find someone) and a hook that pulls them into it, and the GM opens every session by setting the scene, so you always have something to play off. You can still go after anything else you like: side quests and detours are part of the game. After that you say only what your character does. The GM runs everything else (every other person, every monster, every event, and how your actions ripple outward), settles what's uncertain with rules and real dice behind the scenes, and writes what happens as prose: third person limited, or second person ("You push the door open") if you'd rather it sound like a GM at the table. You choose when you make the narrative. It reads like a novel, not like a game: no hit points, no damage numbers, no rolls on the page.

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
- `Journal.md`: what your character knows: the goal they're working toward, people, places, and unfinished business.
- `Style Guide.md`: tense, tone, content limits, and writing rules for this narrative.

`GM Only/` is the GM's: the world itself and how it really works, what other people want and know, what's moving off the page, every roll, every ruling. Nothing locks it. It's an honor system.

### The play window

Double-click `Play.cmd`. It opens a desktop window that lists your narratives, creates new ones, and is where you set them up and play them. Once you've opened one, Continue at the top of the main menu goes straight back into the narrative you opened last.

For a launcher with the dice icon, run `gm shortcut` once: it makes `Play` (a shortcut) beside `Play.cmd`. `gm shortcut --desktop` puts one named `GM Engine` on the desktop instead. A shortcut remembers where the engine folder is, so make it again if the folder moves.

- **The narrative** fills the main column and grows as you play. Earlier sessions are in the picker at the top.
- **Begin** starts a session, and the GM goes first: it sets the scene and puts something in front of your character, and you play from there. The first session's opening is the hook, the event that pulls your character into the campaign.
- **The message box** at the bottom is how you play. "As my character" sends an action; "To the GM" sends a note in braces for you. Between sessions it speaks to the GM only.
- **Push** (under the message box) is for when your character gives an action everything they have. Switch it on before you send: it costs 2 Strain and gives them a better chance on that action's first roll. If nothing needed rolling, nothing is spent. It switches itself off after each action.
- **Undo** and **I meant…** (shown while a session is open) take back the last beat. Undo removes it and everything it changed; press it twice to confirm. "I meant…" is for when the GM misread you: it shows what you wrote, you correct it, and the beat is played again from that.
- **In a shop,** a button with the shop's name appears above the message box. It opens the shop: what's for sale and for how much, what the keeper would buy from you and what they'd pay, and your money. Click things into your basket on the Buy and Sell tabs, see what it comes to and what you'd have left, and press **Make the trade**. The GM plays the trade as a short beat and settles your money and your gear. To haggle, ask for something that isn't on the shelf, or steal, type it as your character as usual. The button goes when your character leaves.
- **When a session ends,** a card shows the session as your character would tell it, which of the four marks it earned and why, and how far that puts you toward the next level. "How the last session ended" in the ⋯ menu shows it again.
- **A new level** opens its own screen after that card, at the end of the session that earned it: place your three skill ranks, pick a talent or an attribute when the level gives one, and confirm. "Later" puts it off, and a button on the Character tab brings it back.
- **The side panel** shows your character as a game sheet (health, strain and marks as bars, attributes and defenses as tiles, skills with rank pips), the Inventory (their money as counted coins, and what they wear, hold and carry as item slots, each with a picture for its kind and a count; click one to read the rest of what's known about it), the Journal (the goal your character is working toward, and what they know about the world, its people and its places), and your conversation with the GM. When the sheet changes, the bars slide and show the change.
- **The top bar** has the button that ends or starts a session, a button to hide the side panel for reading, and the ⋯ menu, where Save game, Load game, and the text size are.
- **To flag a passage,** select it in the narrative and press "Flag this passage," then say what's wrong with it. Or press "Add to 'To the GM'" to quote it in the message box, switched to speak to the GM, and write the correction there; select and add more passages to send several at once.
- **During setup** the main column is your conversation with the GM: it tells you what your character would know about the world and helps you make them, and the Character tab fills in as you go.

The window hands what you type to Claude Code, the same GM that runs in VS Code, using the copy the VS Code extension installed and your existing sign-in. VS Code doesn't need to be open. Every time the window opens, it looks for Claude Code and for Codex and says so if either is missing or isn't signed in: without Claude Code there is no GM, and without Codex the game plays but no pictures are painted. The window never shows rolls, rulings, or anything in `GM Only/`.

**GM Model** in Settings chooses which Claude model runs the GM: Default (whichever Claude Code uses on your plan), Opus, or Sonnet. Opus is the strongest writer and uses the most of your plan; Sonnet uses less, for making a plan last. It can be changed at any time, and the GM's next message is written by the one chosen. Pictures aren't affected.

"Start a fresh GM conversation" in the ⋯ menu is for when the GM seems confused or slow after a very long sitting: nothing in the narrative changes, and the GM rereads its notes on the next message.

### Pictures

The GM has pictures painted for the major moments: your character's portrait at the end of setup, the first sight of a town, a castle, or another place that matters, a new person with a part to play, and an object or a mystery found. Ordinary rooms, roads, and passers-by get nothing. They're painted by Codex's image generation, using the Codex program its VS Code extension installed and your Codex sign-in, so Codex needs to be installed and signed in.

- Each picture takes a minute or two and arrives while you keep playing. A new face slides in at the corner of the narrative when it's ready.
- Your portrait sits on your character sheet, the current place is a strip across the top of the narrative, faces appear beside names in the Journal, and everything is in the **Gallery** tab. Click any picture to see it large.
- A picture only ever shows what your character has seen, under the name they know it by.
- Pictures are painted while the play window is open. Playing in VS Code instead, run `gm art run` to paint what's waiting.
- In braces: `{redo her portrait, she should look older}`, `{paint that}`, `{no more pictures}`. The art style for a narrative is a line in its Style Guide.

The files are in the narrative's `Art/` folder.

### Saving and loading

A narrative has saved games, kept in its own folder on your computer. Nothing is uploaded.

- **Save game** (in the ⋯ menu) saves the game exactly as it stands. Give the save a name if you like.
- **Load game** lists your saves like save slots: the session each was made in, your character's name and level, and when. Pick one and the whole narrative goes back to that point: the story, your sheet, the Journal, the pictures, and everything the GM tracks behind the scenes.
- The game also saves itself at the end of every session, and again just before any load, so loading never loses anything. You can always load your way back.
- After a load, the GM starts from its notes as they were at that save and remembers nothing that came after.

Writing rules you've taught the engine are not rolled back by a load: they belong to the engine, not to one narrative.

Without the window: `gm save "a name"`, `gm saves`, and `gm load <number>` from the narrative's folder.

### Playing

Use the play window, or open the narrative's folder in VS Code and start a Claude Code conversation there. Either way:

- **The GM opens each session.** Say `{new session}` (the window's Begin button) and the GM sets the scene and brings something to your character. You answer it, or do something else entirely.
- **Anything you write outside braces is your character acting**, in first or third person: `I swing my sword at the goblin` or `Kendrick swings his sword at the goblin`. Say what they do, say, or try. The GM works out what comes of it and writes the beat, which stops when your character would have to do something you haven't said.
- **Anything in `{braces}` is you talking to the GM.** It never goes in the narrative.

Your character never does anything you didn't state: no picking things up, no starting conversations, no decisions. The GM does write their thoughts and reactions, from the personality on your sheet, so keep that part of the sheet true to who they are.

### Fixing the writing

When something reads wrong, say so in braces: `{that line sounds stiff}`, `{too flowery}`, `{that name sounds generated}`. The GM rewrites just that part in the session log and adds a writing rule so it doesn't happen again. Rules that would apply anywhere go in `Writing/Craft Rules.md` here; rules about one world go in that narrative's Style Guide. You can change or strike any rule.

### Other things to say in braces

| | |
|---|---|
| `{new session}` / `{end session}` | Start or close a session. The GM opens a new one by setting the scene. Ending one updates the Journal and awards marks toward the next level. |
| `{sheet}` | Show the character sheet. |
| `{recap}` | Where things stand, as your character knows it. |
| `{undo}` | Take back the last beat. |
| `{push}` after an action | Your character gives it everything: 2 Strain for a better chance on its first roll. |
| `{I meant ...}` | The GM misread your action: it's replayed. |
| `{echo off}` | Beats go only to the session log, not the chat (faster, if you read from the file). |
| a question | Answered from what your character knows. |
| a question about the world | Answered with what your character knows, and no more. |
| a change to the sheet, or to the world | Made. Your word is canon. |

## Starting a narrative

1. Double-click `Play.cmd`. Under "A new narrative," pick the genre (high fantasy, low fantasy, sci-fi, space opera, slice of life, any of them together, or one of your own) and the tone (mature, dark, grim, comedy, light hearted, or your own), choose the world (original, D&D, another setting you name, or isekai: someone from our world who ends up in another), name anything you want the world to have in it, pick its size (small, medium, or large; a space opera counts them in worlds and systems, and adds a whole galaxy), say what the story is about if you have one in mind (fighting a dark lord, winning a war), name any themes you want in it, pick the content you want included (explicit language, explicit sex, nudity, graphic violence, gore; whatever you don't pick is left out), choose the narration (third person, or second person), add a title if you have one, and press **Create the world**.
2. The GM builds the world (see "Installing a new narrative" below: allow 10 to 20 minutes for a medium one). While it does, you can start on your character: the parts that are the same in any world (who they are, their looks, their nature, their attributes) open at once. When the world is done, the rest of the character creator opens, starting with a page on what your character would know.
3. Make your character on the character creator, a step at a time: buttons for what can be picked, a box where it takes words. Where the story opens is the GM's to choose, as at any table.
4. Press **Begin**. The GM opens the first session: it sets the scene and hooks your character into the campaign. Then it's your move.

The GM asks you nothing else about the world, and never shows you what it built.

### Installing a new narrative

Think of creating a narrative as installing a new game. Pressing **Create the world** starts the install, and a medium world takes **10 to 20 minutes**. A small one takes less and a large one more: the size you pick is how much the GM has to build. A space opera's whole galaxy is the exception: it can take **1 to 2 hours** and a lot of your usage, and the window asks you twice before it starts.

A game install copies a world that someone already made onto your machine. This one makes the world while you wait. During the install the GM is building everything the game will run on:

- the world itself: its lands, peoples, history, laws, and secrets;
- the starting region, with its towns, roads, and the places worth finding;
- the factions, and the people who run them and what each one wants;
- the campaign: what your character will be working toward, who stands against it, and how it could end;
- the trouble already in motion before you arrive;
- the rules for this world: its skills, gear, powers, and dangers;
- the pools of names every character will be drawn from.

You don't have to sit and watch. As soon as the install starts, the character creator opens on the parts of a character that don't depend on the world: their name, gender and age, their looks, their nature, and their attributes. Anything you set there is kept, and you can change it once you've seen the world. "The GM's side" at the bottom shows your conversation with the GM, and the button that stops the build.

The bottom of the creator shows what the GM is working on (drawing the map, peopling the world, setting trouble in motion) with a running timer. It says only what kind of thing is being made, never what's in it. There's no progress bar, since the GM is writing, not copying, so the time varies with the world you asked for: a small one is quicker, a large one or one built on a big existing setting takes longer.

When the install finishes, the rest of the creator opens: a page on what your character would know, then the world's own choices (their people, their walk of life, where they're from, their skills and talents). Their portrait is painted while you finish.

Like any install, it happens once. After that the narrative opens straight from the title screen, and a beat of play takes about a minute.

Without the window: double-click `New Narrative.cmd`, open the new folder in VS Code, and tell Claude "Set up this narrative."

## What's in this folder

| Path | What it is |
|---|---|
| `ENGINE.md` | The operating manual: the folder map, what's tracked where, the loops, the principles |
| `ROADMAP.md` | Features to add or expand later |
| `VERSION` | The engine's version, shown in the corner of the main menu and in About |
| `Rules/Core Rules.md` | The game underneath: attributes, the roll and its five outcomes, health, fights, powers, growth. The same in every world. |
| `Rules/GM Rules.md` | The standing rules for the GM: who decides what, where a beat ends, honest dice, what's hidden |
| `Writing/Craft Rules.md` | The writing rules for every narrative (`Craft Rules History.md` has the reasons) |
| `Writing/House Style.md` | The prose defaults |
| `Writing/GM Philosophy.md` | It's a game: a campaign with no script, an honest world |
| `Writing/Banned Names.md` | Names that are never used |
| `Procedures/` | New Narrative, Play, World Turn, Corrections, Art |
| `Templates/` | What a new narrative, cast member, place, or group starts as |
| `engine/` | The scripts behind the `gm` command, including the dice and the play window (`gui.py`, `gui/app.html`, its icon `gui/dice.ico`, and `gui/three.min.js`, the three.js library that draws the main menu's die) |
| `Play.cmd`, `gm.cmd`, `New Narrative.cmd` | Windows launchers |

## Requirements

- Python 3.10 or later. The scripts use only the standard library.
- The Claude Code extension in VS Code, signed in.
- For pictures: the Codex extension in VS Code, signed in.
- For the play window in its own desktop window: `pip install pywebview`. Without it, the window opens as a browser tab.

The play window keeps its list of narratives in `.gm-engine/narratives.json` in your home folder. An optional `.gm-engine/config.json` can set `"claude"` (the path to Claude Code, if it isn't found) and `"model"` (a model for the GM, used while the GM Model setting is at Default).

The launchers are Windows `.cmd` files. On other systems, call `python engine/gm.py` directly.
