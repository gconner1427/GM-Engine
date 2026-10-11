# Roadmap

Features to add to the engine, and existing ones to expand, when there's time. Nothing here is built yet, and nothing here is a promise: it's where an idea goes so it isn't lost.

This is about the engine only. Nothing from a narrative goes here.

## How it's laid out

Three levels: a category, the part of it an idea belongs to, and how much there is to build. Within each part the entries run from the least work to the most, under one of three sizes:

- **Small:** a contained change to the play window's page, or to the page and one script, using what the GM already writes.
- **Medium:** something new for the GM to keep as well as the page (a rule or a procedure changes, and usually a template), or work that runs across several parts of the window and its scripts.
- **Large:** a new screen with rules of its own, a helper agent, a change to how a beat is played, or a piece of work that stands apart from the play window.

A size with nothing in it is left out. The categories:

- Starting a narrative
- The play window
- Look and feel
- More of a game
- The GM's helpers
- Outside of play

## How to add something

One entry per idea, under the category, the part, and the size it belongs to. Add the part or the size heading if it isn't there yet:

```
##### The name of the feature
What it is and why it's wanted, in a sentence or two.
- **Touches:** the files or parts of the engine it would change, if known.
- **Open questions:** anything that has to be decided before it can be built.
```

Leave out the lines that have nothing to say. When an entry is built, delete it, along with any heading left with nothing under it: the commit history and the README record what the engine does.

## Starting a narrative

Everything before the first beat: setting a narrative up, what's ready-made for it, and how a new player learns the window.

### Setting one up

#### Medium

##### Difficulty settings
A difficulty the player picks during new narrative setup. It raises or lowers the fixed numbers the character is up against: enemy health, enemy base stats, shop prices, and anything else of the kind that can go up or down without breaking the game. It never touches chance: the dice roll the same at every setting. There are three settings:
- **Story:** about half of Normal, for a player who wants to enjoy the narrative with little risk of dying or of a hard time with enemies. Heroic stakes only.
- **Normal:** the numbers as the rules give them. Heroic or Deadly stakes.
- **Hardcore:** twice Normal. Deadly stakes only.

Difficulty doesn't take the place of the stakes (Core Rules §7): setup asks for both, and the difficulty limits which stakes can be chosen.
- **Touches:** the table settings in `Procedures/New Narrative.md`, step 2; the `Style Guide.md` template, which holds them; the play window's New Narrative window (`engine/gui/app.html`); `Rules/Core Rules.md`, the Bestiary and stat lines the GM writes, and the Economy's prices, for how each setting changes the numbers.

### While the world is built

#### Large

##### Things to do while the world is built
A world takes twenty minutes or more to build, and the early steps of the character creator fill five to ten of them. The wait itself is fine; having nothing to do in it isn't. Once the early steps are done, the window offers three things to do, and the player picks whichever they like and can go from one to another:
- **A practice bout:** a fight against a training dummy with the real dice, so the player learns the five outcomes, Push, and how damage works before the first beat. It needs nothing from the world, because the rules are the same in every one.
- **A game of chance:** a small dice or card game in the window, played for nothing, for the player who has had enough of the bout. It could later be the game played in a world's taverns.
- **How to play:** a short page on the window and the rules, for the player who has never played.

None of them is required: a player who wants to walk away still can. They needn't fill the whole wait, and any of them can be dropped the moment the world is ready.
- **Touches:** the character creator and `EARLY_STEPS` in `engine/gui/app.html`, where the wait is spent now; `engine/dice.py` and `engine/gui.py`, for a bout with the real tables. How to play has to say what `Rules/Core Rules.md` says.
- **Open questions:** nothing here can show a word of the world, as `BUILDING` can't. Whether a bout is fought as the player's own character, which needs the creator's later steps, or as a stock one. Which game the game of chance is. What happens to a bout or a game in progress when the world is ready. Whether the three stay within reach after the world is built, from the main menu or About.

### Ready-made worlds and characters

#### Medium

##### Prebuilt characters
Ready-made characters the player can pick instead of making one, so they can start playing sooner once the world is built. The GM makes them to fit the world. The player is asked whether they want prebuilt characters to choose from; if they say yes, they are asked how many, from 1 to 4, and the GM makes that many. Each is built with the narrative in mind, so the player takes one as it is and can't change it: a changed character would no longer fit the narrative it was made for.
- **Touches:** the character creator in the play window (`engine/gui/app.html`, "making the character"); the `## Character creation` section the GM writes (`Procedures/New Narrative.md`, step 4).

#### Large

##### Prebuilt worlds
Worlds that are already built, so a new narrative can start from one instead of waiting for the GM to build a world from the premise. Each one is a designed narrative, to be played like a finished game the player bought: its genre, its world, and its story are already set, so the player isn't asked for a premise and doesn't name a story. Each ships with the Journal's "The world as they know it" page and the `## Character creation` section already written, so the character creator opens at once: the player makes a character and drops into play. They are kept in a `Worlds` folder in the engine, and the one the player picks is copied into the narrative's folder. The player picks from brief descriptions that say what type of world each one is and give nothing away. A prebuilt world has no characters of its own: the player is asked whether they want prebuilt characters, as in any world. Claude builds each prebuilt world ahead of time from a simple prompt, such as "a fantasy world with dragons" or "a sci-fi universe with many species".
- **Touches:** a new `Worlds` folder; `Procedures/New Narrative.md`, where the GM builds the world; `gm new-narrative` in `engine/gm.py`, to copy the world in; the play window's New Narrative window (`engine/gui.py` and `engine/gui/app.html`), which gets an option for prebuilt worlds.

### Learning the window

#### Small

##### Showing that a passage can be flagged
Flagging a passage is found only by a player who happens to highlight some of the story. The first time a beat arrives, the window says once that any passage can be highlighted to tell the GM what's wrong with it, and About says so too.
- **Touches:** the flag buttons (`#flag`) and the About window in `engine/gui/app.html`; the play window's saved preferences, to remember that it's been said.

##### First-session pointers
In a narrative's first session, the window points once at each thing a new player has to find for themselves: the switch between the character and the GM, Push, flagging a passage, and the side panel. Each pointer is a line beside the thing it names, shown when the thing first matters and never again.
- **Touches:** `engine/gui/app.html`; the play window's saved preferences, to remember which have been shown.
- **Open questions:** whether Settings gets a way to see them again.

## The play window

Making the window easier to use and harder to get lost in. Nothing here changes the game or what the GM does.

### The message box

#### Small

##### Begin in place of the message box
Between sessions the message box sits where it always does, while the one thing to press is a small button in the corner of the header, and the line under the box has to say where it is. While no session is open, the message box gives way to a large Begin button, with a quiet way to write to the GM instead beside it.
- **Touches:** the composer and `#newsession` in `engine/gui/app.html`, and the part of `apply` that holds actions back between sessions.

##### Who is being spoken to
The switch between "As my character" and "To the GM" is small text under the message box, and the only sign of being in the GM's mode is a dashed border. The box itself says who it's addressed to, with a label inside it and a tint of its own for the GM. A key switches between the two, and a message that starts with a brace switches to the GM by itself.
- **Touches:** the composer and `showMode` in `engine/gui/app.html`.
- **Open questions:** which key. Tab is the natural one, but it also moves between buttons.

##### The GM's answers above the message box
When the GM answers something said to it, the window switches the side panel to the GM tab, and opens the panel if it was closed. The answer rises as a card above the message box instead, where the player is already looking, and is dismissed with a click. The GM tab stays as the record of everything said, and the side panel is left on whatever the player had open.
- **Touches:** `apply` in `engine/gui/app.html`, where a new answer sets the GM tab and its badge; the composer, for the card.
- **Open questions:** what happens to a long answer, such as a recap: whether the card scrolls or sends the player to the GM tab.

##### Keyboard shortcuts
Only Enter, Escape, and F11 do anything now. Add a key to save, keys for the side panel's tabs, the up arrow in an empty message box to bring back the last thing sent, and a sheet of all of them on `?`. A dialog puts the cursor in its first field when it opens, and a click outside one closes it.
- **Touches:** the key handlers and the dialogs in `engine/gui/app.html`.

##### Speaking an action
The player can say what their character does instead of typing it. On Windows this already works: with the cursor in the message box, Win+H starts Windows' own dictation, and what's said appears in the box as words, to be read over and changed before it's sent. What's missing is any sign of it. The message box gets a microphone button that starts dictation, so the player doesn't have to know the key, and nothing is ever sent by voice alone, since only what the player states happens.
- **Touches:** the composer in `engine/gui/app.html`; `engine/gui.py`, which would press Win+H for the page, since a page can't start dictation itself. It's for Windows only, as the engine is for now.

### The wait

#### Small

##### A cue when the beat lands
A beat takes about a minute, and a player who has looked away has no way to know it's come. When one arrives while the window isn't in front, it gives a soft chime, changes the window's title, and flashes on the taskbar.
- **Touches:** `apply` in `engine/gui/app.html`, where a finished beat is noticed; `engine/gui.py`, if the taskbar flash has to come from the desktop window; Settings, for turning the chime off.
- **Open questions:** whether pywebview can flash the taskbar.

##### New paragraphs arriving in turn
A new beat's paragraphs come in one after another, not all at once, and the story is left at the beat's first new line, so the player starts reading where the new part begins.
- **Touches:** `renderStory` and the `fresh` paragraphs in `engine/gui/app.html`. It has to respect the reduced-motion setting, as the rest of the window does.

##### Writing ahead during the wait
While the GM is at work the player can go on writing their next action, kept as a draft and sent when the beat has been read, and can read the journal and the gallery without being pulled to another tab.
- **Touches:** the composer in `engine/gui/app.html`. Nothing is sent until the beat is on the page: the character acts on what the player has read.

#### Medium

##### A true line on what the GM is doing
During a beat the window cycles through four lines ("The GM considers", "Dice roll behind the screen"…) on a timer, whatever the GM is doing. While a world is built it already says what kind of thing the GM last wrote. A beat gets the same: the line says the dice are rolling when they are, and that the page is being written when it is.
- **Touches:** `WORKING` in `engine/gui/app.html`; `engine/gui.py`, which would report the stage the way `BUILDING` does. Like `BUILDING`, it must never carry a file's name or a word of its contents.
- **Open questions:** how much of a beat's progress `gui.py` can honestly tell from the GM's run, and whether saying that dice were rolled gives away a roll the character couldn't know about (the same limit as "Visible dice").

### Menus and settings

#### Small

##### A sorted ⋯ menu
The ⋯ menu holds saving, loading, the text size, two recaps, a fresh GM conversation, the narrative's folder, and Settings in one run. It's sorted under small headings (the game, the story so far, the narrative), and "Start a fresh GM conversation" says when it's wanted: when the GM has lost the thread or slowed down.
- **Touches:** `#moreitems` in `engine/gui/app.html`.

##### One Settings screen
The settings are in three places: the text size in the ⋯ menu, the side panel's width on a button in the header, and the rest in Settings. They go in one Settings window, under headings: Reading (text size, the width of the page), Sound, and The GM (the model). The two menu tracks get names in place of "Track 1" and "Track 2".
- **Touches:** `#settingsdialog`, `prefs`, and `applyPrefs` in `engine/gui/app.html`.

##### A session list in the house style
The header's list of sessions is the system's own drop-down, the one control in the window that isn't drawn in its style. It becomes a list of the window's own, and each session can show the date it was played.
- **Touches:** `#sessions` in `engine/gui/app.html`; `engine/gui.py`, if the list carries more than the session's number.

### The side panel

#### Small

##### A side panel that can be resized
The side panel is 420 pixels wide whatever the window's size. Its edge can be dragged, the width is remembered, and on a narrow window it opens over the story instead of squeezing it.
- **Touches:** `--side` and `.body` in `engine/gui/app.html`; the play window's saved preferences.

##### Vitals when the panel is closed
With the side panel closed there's no sign of the character's health or Strain. A thin strip in the header shows both while the panel is shut, and stirs when either changes.
- **Touches:** the header and `readVitals` in `engine/gui/app.html`.

##### Empty tabs that say something
A Journal, Gallery, or Inventory with nothing in it yet shows a line in the window's voice and a small ornament, in place of a blank pane.
- **Touches:** the tabs' render functions in `engine/gui/app.html`.

### When something is wrong

#### Small

##### A notice when the window loses the engine
If the local server stops answering, the page shows the same error again each time it asks. One notice stays up for as long as the engine can't be reached, says what to do about it, and clears itself when the engine is back.
- **Touches:** `tick` and `toast` in `engine/gui/app.html`.

#### Medium

##### Signing in from the play window
When the play window's check finds Claude Code or Codex installed but not signed in, the warning gets a Sign in button, so the player doesn't have to go to VS Code to do it. The button runs the program's own sign-in command (`claude auth login`, `codex login`), which opens the provider's sign-in page in the browser, where the player signs in the way they always do (Google, Apple, or an email and password), and keeps the credentials itself: nothing is typed into the game or a terminal, and the game never sees a password. The window then repeats the check until the program says it's signed in, and clears the warning.
- **Touches:** `claude_state` in `engine/gui.py` and `codex_state` in `engine/art.py`, which make the check; a new route in `engine/gui.py` to start the sign-in; `checkPrograms` and the two warnings in `engine/gui/app.html`.
- **Open questions:** whether either command ever falls back to asking for a code to be pasted in when the browser can't report back, in which case the window would have to show a console for that case only; neither flow has been run yet, and testing Claude Code's means signing out of it.

## Look and feel

How the window looks and sounds: the things that make it read as one piece of work.

### The house style

#### Small

##### Tooltips in the house style
Every hint in the window is the system's own tooltip: slow to appear and drawn in the system's style, the one thing on screen that doesn't match. They become the window's own: quick, in its type and its colours, and placed so they never cover what they describe.
- **Touches:** every `title` in `engine/gui/app.html`, and the ones the page sets as it runs.

##### Named colours
The gold is typed out with a different transparency dozens of times across the stylesheet (`#c9a25b55`, `#c9a25b2e`, `#c9a25b1f`…). The ones that mean something (a glow, a wash, a hairline) get names in `:root`, so every panel uses the same few.
- **Touches:** the stylesheet in `engine/gui/app.html`.

##### A scale of text sizes
The page's text comes in more than a dozen sizes a half-pixel or a pixel apart (9.5, 10, 10.5, 11, 12, 12.5, 13…). They're brought down to about six, named in `:root`, so the same kind of thing is the same size everywhere. The smallest becomes 11 pixels, and `--faint` is lightened, since the small capitals in it are hard to read against the dark.
- **Touches:** the whole stylesheet in `engine/gui/app.html`. It's a pass of its own, since it changes every part of the window a little.

### Sound and light

#### Small

##### Sounds in play
Only the main menu (its music, and a tick and a clack as its entries are moved through and chosen) and the world's building have sound. Play gets a few quiet ones: a page turning when a beat arrives, a click on the menus, and a chime for a new level. They have a volume of their own in Settings, apart from the music's.
- **Touches:** the audio code in `engine/gui/app.html`, which plays the menu's music and the build's now; Settings.
- **Open questions:** whether the sounds are recorded files or made by the page, as the main menu's are for now (`SFX` in `engine/gui/app.html`, where a recorded file can take a made one's place).

#### Medium

##### A daylight theme
A light, paper-coloured version of the story column for reading in a bright room, chosen in Settings. The panels and the menus can stay dark around it.
- **Touches:** the colours in `:root` in `engine/gui/app.html`; Settings. It builds on "Named colours", since a theme is a second set of the same names.
- **Open questions:** whether it covers the whole window or only the page the story is on.

### Narratives and saves

#### Small

##### Fuller Narratives and Load lists
A row in the Narratives list and a save in the Load list each show the character's portrait, their level, the session reached, and when it was last played, so a narrative can be recognised at a glance. The main menu's Continue already names the narrative, the session, the character and their level; it gets the portrait.
- **Touches:** `.slot` and the two lists in `engine/gui/app.html`; `engine/gui.py`, for what it sends about each narrative; `engine/saves.py`, whose saves already carry the session, the character's name, and the level.

## More of a game

The engine tells a story well, but there's little to do in it besides type: one box, a wait of about a minute, and everything a game would let the player feel (the roll, the foe weakening, the time running out) kept out of sight. These features make it a mix of game and story.

**One rule holds for all of them: the game lives in the window, around the story.** The session files are the manuscript, and a narrative may be made into a novel one day, so no feature here may put a number, a roll, or a button's wording into `Sessions/`. The prose reads as a novel always. Nothing here may show the player anything from `GM Only/` either: where a feature needs something the GM knows, the GM writes a player-safe copy for the window to read, the way it writes the sheet's `## Shop` section.

### Rolls and fights

#### Small

##### Visible dice
When a beat turned on a roll, the window shows the die land, how hard the thing was in words (Core Rules §3: Simple to Legendary), and which of the five outcomes came up. Then the prose appears. The roll has already been made by then, so it adds no wait. It's what makes the stakes felt: the player sees that it could have gone the other way.
- **Touches:** `log_roll` in `engine/session.py`, which records rolls only in the GM's log now and would have to leave a player-safe record as well; `engine/gui.py`, to pass it to the page; `engine/gui/app.html`, which already draws a die for the main menu.
- **Open questions:** which rolls are shown. A roll the character couldn't know was made (someone sneaking past their Notice, a fate question about the world) can't be, since the die alone would give it away. Whether the player sees the number or only the outcome. Whether a setting turns the dice off for a player who wants only the story.

#### Medium

##### Clocks and how a foe is faring
Two things the rules already track, put on screen while they matter. A long task (Core Rules §10) shows as a ring that fills, with the danger closing in beside it. In a fight, each foe shows how they're faring in the words of Core Rules §5 (fresh, hurt, bloodied, in bad shape, down), never their HP.
- **Touches:** a section the GM writes on the sheet while a clock or a fight is running and deletes after, like `## Shop`; `Procedures/Play.md`, for when it's written; `engine/gui/app.html`, to draw it.
- **Open questions:** whether the player sees how many steps a clock has, or only that it's filling.

#### Large

##### A fight screen
While a fight is on, the window shows it as one: the character's health and Strain, each foe and how they're faring, and what the character can do as buttons built from their sheet (attack with what they're holding, guard, use a power, use an item, run), with Push and their once-a-sleep tricks beside them. Typing anything else is always open, since a fight has no fixed list of moves (Core Rules §6). The GM still writes every exchange as prose.
- **Touches:** `Rules/Core Rules.md` §6, if any of the buttons needs a rule it doesn't have (guarding has none now); `Procedures/Play.md`, for the section the GM writes while a fight is on; `engine/gui/app.html`. It builds on "Clocks and how a foe is faring".
- **Open questions:** whether the script settles an exchange's rolls itself and the GM only writes what happened, which would make a fight much quicker. That would take the choice of what each foe does away from the GM, or need it decided ahead, and what a foe does is meant to come from who they are.

##### Deciding at the roll
A beat stops at the moment of risk. The player sees what's being tried and how hard it looks, chooses whether to Push or spend a trick, and rolls the die themselves. Then the GM writes what came of it. Push is chosen blind now, before the player knows a roll is coming.
- **Touches:** `Rules/Core Rules.md` §5, on when Push is declared; `Procedures/Play.md`, "The beat"; `engine/dice.py` and `engine/gui.py`, so the roll is made when the player presses; `engine/gui/app.html`. It builds on "Visible dice".
- **Open questions:** it adds a second wait to every beat with a roll in it, which may cost more than the choice is worth. Whether it's kept for the rolls that matter most. The same limit as visible dice: a roll the character couldn't know about can't stop the beat.

### The character and their things

#### Small

##### Clickable inventory
The item slots on the Inventory tab get things to do: use, equip, put away, drop, give. Each one writes an ordinary action for the player to send, the way the shop's basket does, so the GM plays it as a beat and settles the sheet. The page never changes the sheet itself.
- **Touches:** the Inventory tab in `engine/gui/app.html` (`inventoryHtml`, `things`, `kindOf`), which already knows each thing's kind.
- **Open questions:** whether a click sends the action at once or puts it in the message box to be added to.

##### Rest buttons
A breather, a night's sleep, and a full day's rest (Core Rules §8) as buttons, each showing what it would give back before it's pressed. Pressing one sends the action; the GM decides whether the character can rest here and what happens while they do.
- **Touches:** `engine/gui/app.html`, which works out what each rest restores from the sheet's Vitals; the amounts have to match `Rules/Core Rules.md` §8.
- **Open questions:** how the page knows a breather has already been taken since the last sleep.

#### Medium

##### Loot as item cards
A thing worth having arrives as a card: its picture, what kind of thing it is, what it does, and what's known of where it came from. A card fills in as the character learns more about the thing. The Inventory's slots already open to what's known about an item; this makes finding one an event.
- **Touches:** the Gear section of the `Character Sheet.md` template; `Procedures/Art.md`, for which finds get a picture; the Inventory tab in `engine/gui/app.html`.
- **Open questions:** whether things have a rarity, and what it would mean in a world with no such idea.

##### Talents ahead
The world's talents shown before they're earned, so the player has something to plan for and look forward to between levels. The new-level screen already lists what can be picked at that level; this shows the rest.
- **Touches:** the Rules Kit's talents, which are the GM's, so the GM writes a player-safe list on the sheet; the Character tab and the new-level screen in `engine/gui/app.html`.
- **Open questions:** whether every talent is shown, or some are found only in play.

##### The day and supplies
The time of day and the date in the world shown in the window, and the things that run out (food, water, light, ammunition) counted and shown as running low. It gives travel and rest a cost the player can see.
- **Touches:** the GM's Story Clock (`GM Only/State/World State.md`), of which the window would need a player-safe copy; the Gear section of the sheet; `Rules/Core Rules.md`, for what going without does.
- **Open questions:** whether supplies are counted in every narrative or are a table setting, since in some stories they'd only be bookkeeping.

### What the character knows

#### Small

##### A quest log
The Journal's goal and unfinished business shown as things to do, each with where it stands, and marked when it's done or lost, so the player can see what they're working toward at a glance. It's the Journal's own contents in a better shape: it holds nothing the character doesn't know.
- **Touches:** the Journal tab in `engine/gui/app.html`; the `Journal.md` template ("The goal", "Unfinished business"), if each entry needs a line for where it stands; `Procedures/Play.md`, "The end of a session", where the Journal is updated.

#### Medium

##### Standing
Where the character stands with the groups and people they've dealt with, as the character understands it: a few words and a meter for each. It moves when the character helps, crosses, or lies to someone (Core Rules §11: people remember), and the player sees it move.
- **Touches:** the `Journal.md` template ("People", and a new part for groups); `Rules/GM Rules.md`, for how the GM keeps it true to what the character could know; the Journal tab in `engine/gui/app.html`.
- **Open questions:** what's shown when the character is wrong about where they stand. The honest answer is what they believe, and the truth stays in `GM Only/`.

##### A bestiary
A book of the creatures and kinds of foe the character has met, filling in as they learn: first a name and a picture, then what it does, what hurts it, and what it fears. It's the player's own, built from what the character has seen. The GM's `Bestiary.md` stays hidden.
- **Touches:** a new player-facing doc and its template; `Procedures/Play.md`, for when an entry is added or grows; `Procedures/Art.md`; a new tab or a page of the Journal in `engine/gui/app.html`.

##### Achievements
A record of what the player has done across the narrative: firsts, feats, and the turns the campaign took. Each is awarded after the fact, for what happened, and never shown ahead of time, so the list can't give the campaign away or steer the player toward an ending.
- **Touches:** a new player-facing doc; `Procedures/Play.md`, "The end of a session", where they'd be awarded with the marks; `engine/gui/app.html`.
- **Open questions:** whether they're the same in every narrative, written by the GM for each world, or both.

#### Large

##### A map
The places the character has found, drawn as a map: each a point with its picture, joined by the roads they know, with the travel times they've learned. Clicking a place sets out for it, as an action. Nothing is on it that the character hasn't seen or been told of, and what they were told wrongly is drawn wrong.
- **Touches:** the `Journal.md` template ("Places"), which would have to say where each place lies and what joins it; the GM's `Map & Travel.md`, which stays hidden; `Procedures/Play.md`, for when the map grows; `engine/art.py`, if the map is painted; a new tab in `engine/gui/app.html`.
- **Open questions:** whether the page draws it from the Journal or Codex paints it. A painted map looks better and can't be clicked on as easily, and it would have to be painted again each time it grows.

### Choosing what to do

#### Medium

##### Suggested actions
After a beat, a few things the character might do next, as buttons beside the message box. Typing anything else is always open, and the character still never acts unless the player says so. It's for the moment a player doesn't know what's possible.
- **Touches:** `Rules/GM Rules.md` and `Procedures/Play.md`, "The beat", for what the GM may suggest; `gm beat` in `engine/session.py`, to carry the suggestions outside the session file; `engine/gui/app.html`.
- **Open questions:** whether it makes play feel like picking from a menu, in which case it should be a setting, off unless asked for. A suggestion must never point at something the character hasn't noticed.

## The GM's helpers

Helper agents that work for the GM or beside it. Each one is Large: a helper costs a wait and usage, and has to be kept from knowing what it shouldn't.

### In the party

#### Large

##### AI-controlled companions
Companions who are members of the character's party, run by the GM: more than someone from the cast who happens to be traveling with them. A companion can be met in play, hired in play, or made at setup if the player wants one. Each has a character sheet of their own, shorter and less detailed than the character's, and can level up and carry their own gear. The sheet starts with their stats and their appearance. Their inner life (what they want, and the like) is left off it, and is added as play goes on, if the character gets to know them. The sheet gets its own tab on the play window's side panel. The first version allows one companion, with room for more later.

**A companion is played by an agent of their own.** This is the use of helper agents that matters most to the engine: with it, the player is playing with a party, the way they would at a table with other people, and it's what could make the engine something special. The companion's agent knows only what the companion knows, wants what the companion wants, and decides for itself what they do and say, so they can disagree with the character, keep something back, or do the thing nobody expected. It's worth what it costs in wait and usage, so it isn't kept for chosen scenes: wherever the companion is present, they're played this way. The GM still writes everything the player reads, and still has the final say on the world: the agent says what the companion does and says, and the GM resolves it with the rules and puts it on the page.

It has to be built well or it's worse than not having it. A companion who answers slowly, forgets what happened yesterday, or knows what they couldn't know breaks the feeling of a party faster than a GM-run one would.

**What a companion knows.** Nothing of the GM's world. Their agent never reads `GM Only/`. It has what the companion would know on the day they join (their own life, their trade, the common knowledge of where they're from) and what they learn in the campaign from then on: what they see, hear, and are told, and nothing they weren't there for.

**What the player can do with one.** What they can do with anyone else in the world, and no more. The player doesn't control a companion, give them orders that have to be followed, or choose their actions in a fight. Their character can ask, argue, dismiss them, try to romance them, or kill them, and the companion answers as the person they are.

**They mustn't overthink.** A companion who weighs every choice makes every beat slow, and a slow companion is useless. They decide the way a person in the moment does: quickly, from who they are and what's in front of them.
- **Touches:** `Rules/Core Rules.md`, for how a companion acts in a fight and how one levels up; `Rules/GM Rules.md`, for how the GM plays one and how it uses what the agent says; `Procedures/Play.md`, "The beat," for when the companion's agent is asked; a template for the companion's sheet, and a doc of what they know and remember; `Procedures/New Narrative.md` and the character creator, for a companion made at setup; `engine/gui.py`, to run the agent; the play window's side panel (`engine/gui.py` and `engine/gui/app.html`), for the tab.

**What the agent is given, each time it's asked.** Two things and nothing else:
- **The companion's own character document,** which says who they are and how they'd act. Their inner life is theirs: what they think and feel comes from this and from the agent, never from the GM.
- **A brief of the moment, written for them.** It's the counterpart of what the player gets: the same outward events (what's happening, what's said and done, what can be seen and heard), told from where the companion stands. It has nothing from inside the player character's head, just as the player's page has nothing from inside the companion's.

It gets no tools and no files to open, and it's asked for a few lines of what the companion does and says. That keeps it quick, and having nothing to open is also what keeps the GM's world out of its reach.
- **Open questions:** what the companion remembers from earlier sessions, and whether that lives in their character document. Whether the agent is asked in every beat or only when the companion would act.

### Behind the screen

#### Large

##### An archivist
A helper agent that keeps an index of everything that has happened in a narrative and answers the GM's lookups: what an innkeeper promised three sessions ago, who knows the character's real name, where a thing was left. It's what lets a campaign stay consistent at any length, since the GM can't hold forty sessions in its head. It reads and it answers; it never writes the story and never changes the world.

The rule for how it's built: whatever is most efficient without making the narrative worse. That points to these, to be confirmed when it's built:
- **A script keeps the index, as each beat is committed.** `gm beat` already receives every new fact a beat established, so filing them costs no usage and no wait, and the index is never behind the page. An agent building it after each session would spend usage on what a script does for nothing.
- **The agent only answers.** It's started when the GM has a question the index alone doesn't settle, reads the index and the passages it points to, and replies in a few lines.
- **The GM looks up only what a beat turns on.** What's in its startup reading (the campaign, the world state, the sheet, the end of the latest session) it just knows. It asks when a beat depends on something older than that: a promise, a debt, a price once paid, who was told what. A lookup is a wait for the player, so it's never done for a detail that doesn't matter.
- **Touches:** `gm beat` in `engine/session.py`, to file each beat's facts in the index; `GM Only/State/Archive.md` and the session logs, which the index points into; `Procedures/Play.md`, for when the GM asks.

Nothing has to be decided before it's built. Whether the efficient version holds up can only be seen by playing a long campaign on it: if the GM gets things wrong that a lookup would have caught, it has to ask more often.

##### The world turn, between sessions
The world turn (`Procedures/World Turn.md`) run by a helper agent in the background once a session ends, so the opposition and everyone off the page have already moved by the time the player comes back, and the GM opens the next session without doing it first.

A new session can't begin until the world turn has finished: the play window holds Begin back while it runs, and says why.

The GM always reviews it. What the helper decided is a proposal: the GM reads it before the next session opens, changes or throws out whatever it disagrees with, and only then is it canon. The GM has the final say on everything in the world.
- **Touches:** `Procedures/World Turn.md`; `Procedures/Play.md`, "The end of a session" and "Opening a session"; `engine/gui.py`, to run it after `{end session}`; the Begin button in `engine/gui/app.html`, to hold it back.

##### A continuity check
A helper agent that reads each new beat against the world docs, the sheet, and what has already happened, and tells the GM about contradictions (a dead man speaking, a sword that was sold, a two-day road walked in an hour), so the GM can correct them before the player has to flag them.
- **Touches:** `Procedures/Corrections.md`, for how the GM acts on what it's told; `engine/gui.py`, to run it in the background after a beat.
- **Open questions:** whether it runs after every beat or at the end of a session; how its findings reach the GM without the player seeing them; how much usage it's worth.

##### Minds for major characters
In a scene that matters, a major member of the cast is played by a helper agent that is given only that person's doc and what they know, so they keep real secrets and pursue their own ends, where the GM playing everyone knows everything. The GM asks the agent what the person does and says, and writes it. For pivotal scenes only: it costs a wait and usage on every exchange.
- **Touches:** `Rules/GM Rules.md`, for when the GM hands a character over and how it uses the answer; the cast template (`Templates/Entries/Cast.md`), which has to say plainly what the person knows.
- **Open questions:** who decides a scene is pivotal; how the agent is kept from learning what its character doesn't know.

## Outside of play

What's done with the engine and its narratives away from the table.

### The story as a book

#### Small

##### A manuscript
The whole narrative as one clean document: the sessions joined in order, with chapter breaks, ready to be edited into a novel. It's small because of the rule above: the session files carry nothing but prose.
- **Touches:** a new `gm manuscript` in `engine/gm.py`; the ⋯ menu in `engine/gui/app.html`.
- **Open questions:** whether a session is a chapter, or chapters are cut some other way; what format it's written in.

### Getting the engine onto a machine

#### Medium

##### Choosing where the engine is installed
The player chooses the folder the engine goes in, the way a game's installer asks where to install, and the engine runs from wherever that is. The scripts already find the engine from where they sit, so the folder can be anywhere. A narrative doesn't follow it: each one records the engine's full path when it's made (`"engine"` in `narrative.json`, and the paths written into its `CLAUDE.md`), so an engine that's moved or installed again somewhere else leaves its narratives pointing at the old place. The play window notices when it opens one and points it at the engine it's running from.
- **Touches:** `engine/scaffold.py`, which writes the engine's path into a new narrative; `Templates/Narrative/CLAUDE.md`, which carries it; `engine/gui.py`, to repoint a narrative when it's opened. It builds on "An installer", which would do the asking.
- **Open questions:** whether a narrative should record the engine's path at all, or be told it each time the play window starts the GM.

#### Large

##### An installer
The engine packaged so it can be installed on another machine and played there, without copying the folder over and setting up Python by hand. It's for the user's own machines, not for handing out. The installer installs everything it can: Python is bundled, and so is Git, which saved games need. What it can't carry, it checks for and reports:
- **Claude Code** is required. If it's missing, the installer says so and says the engine can't run without it.
- **Codex** is optional. If it's missing, the installer says pictures won't be painted, and carries on.

The play window already makes the same check every time it opens, and asks each program whether it's signed in (`claude_state` in `engine/gui.py`, `codex_state` in `engine/art.py`), so the installer's check should use the same two.

The installer doesn't move narratives. Getting one to another machine is the user's to do however they like (a flash drive, cloud storage), and "Add an existing folder" in the play window's Narratives list brings it in once it's there.
- **Touches:** `Play.cmd`, which starts the play window now; `engine/gui.py`, which has to find the engine's rules, templates, and page from wherever it was installed; `engine/art.py`, which finds the `codex` program; `engine/saves.py`, which has to run the bundled Git; `VERSION`, which the installer would carry.

### Making the engine public

Not planned yet. These are what has to be done first when it is.

#### Small

##### A CLAUDE.md written for the user
The engine's `CLAUDE.md` is written for its author: it names a folder on their machine (the Living World Engine it was forked from) and is mostly notes for working on the engine itself. Before the engine is public it's rewritten for someone who has just got it: what the engine is, how to open the play window and start a narrative, and nothing that's true on only one machine. The notes for working on the engine are kept, in a part of their own or in a doc it points to.
- **Touches:** `CLAUDE.md`; `README.md`, which may take some of what comes out of it.
- **Open questions:** whether the public repository starts from a fresh history, since every commit so far carries the author's name and email.

## Maybe

Ideas that aren't decided on. Move one up when it's wanted, or delete it when it isn't.

*(nothing yet)*
