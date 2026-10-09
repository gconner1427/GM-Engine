# Roadmap

Features to add to the engine, and existing ones to expand, when there's time. Nothing here is built yet, and nothing here is a promise: it's where an idea goes so it isn't lost.

This is about the engine only. Nothing from a narrative goes here.

## How to add something

One entry per idea, under the section it belongs to:

```
### The name of the feature
What it is and why it's wanted, in a sentence or two.
- **Touches:** the files or parts of the engine it would change, if known.
- **Open questions:** anything that has to be decided before it can be built.
```

Leave out the lines that have nothing to say. When an entry is built, delete it: the commit history and the README record what the engine does.

## New features

Things the engine doesn't do yet.

### Prebuilt characters
Ready-made characters the player can pick instead of making one, so they can start playing sooner once the world is built. The GM makes them to fit the world. The player is asked whether they want prebuilt characters to choose from; if they say yes, they are asked how many, from 1 to 4, and the GM makes that many. Each is built with the narrative in mind, so the player takes one as it is and can't change it: a changed character would no longer fit the narrative it was made for.
- **Touches:** the character creator in the play window (`engine/gui/app.html`, "making the character"); the `## Character creation` section the GM writes (`Procedures/New Narrative.md`, step 4).

### Prebuilt worlds
Worlds that are already built, so a new narrative can start from one instead of waiting for the GM to build a world from the premise. Each one is a designed narrative, to be played like a finished game the player bought: its genre, its world, and its story are already set, so the player isn't asked for a premise and doesn't name a story. Each ships with the Journal's "The world as they know it" page and the `## Character creation` section already written, so the character creator opens at once: the player makes a character and drops into play. They are kept in a `Worlds` folder in the engine, and the one the player picks is copied into the narrative's folder. The player picks from brief descriptions that say what type of world each one is and give nothing away. A prebuilt world has no characters of its own: the player is asked whether they want prebuilt characters, as in any world. Claude builds each prebuilt world ahead of time from a simple prompt, such as "a fantasy world with dragons" or "a sci-fi universe with many species".
- **Touches:** a new `Worlds` folder; `Procedures/New Narrative.md`, where the GM builds the world; `gm new-narrative` in `engine/gm.py`, to copy the world in; the play window's New Narrative window (`engine/gui.py` and `engine/gui/app.html`), which gets an option for prebuilt worlds.

### AI-controlled companions
Companions who are members of the character's party, run by the GM: more than someone from the cast who happens to be traveling with them. A companion can be met in play, hired in play, or made at setup if the player wants one. Each has a character sheet of their own, shorter and less detailed than the character's, and can level up and carry their own gear. The sheet starts with their stats and their appearance. Their inner life (what they want, and the like) is left off it, and is added as play goes on, if the character gets to know them. The sheet gets its own tab on the play window's side panel. The first version allows one companion, with room for more later.
- **Touches:** `Rules/Core Rules.md`, for how a companion acts in a fight and how one levels up; `Rules/GM Rules.md`, for how the GM plays one; a template for the companion's sheet; `Procedures/New Narrative.md` and the character creator, for a companion made at setup; the play window's side panel (`engine/gui.py` and `engine/gui/app.html`), for the tab.

### Difficulty settings
A difficulty the player picks during new narrative setup. It raises or lowers the fixed numbers the character is up against: enemy health, enemy base stats, shop prices, and anything else of the kind that can go up or down without breaking the game. It never touches chance: the dice roll the same at every setting. There are three settings:
- **Story:** about half of Normal, for a player who wants to enjoy the narrative with little risk of dying or of a hard time with enemies. Heroic stakes only.
- **Normal:** the numbers as the rules give them. Heroic or Deadly stakes.
- **Hardcore:** twice Normal. Deadly stakes only.

Difficulty doesn't take the place of the stakes (Core Rules §7): setup asks for both, and the difficulty limits which stakes can be chosen.
- **Touches:** the table settings in `Procedures/New Narrative.md`, step 2; the `Style Guide.md` template, which holds them; the play window's New Narrative window (`engine/gui/app.html`); `Rules/Core Rules.md`, the Bestiary and stat lines the GM writes, and the Economy's prices, for how each setting changes the numbers.
## To expand

Things the engine already does that should go further.

*(nothing yet)*

## Maybe

Ideas that aren't decided on. Move one up when it's wanted, or delete it when it isn't.

*(nothing yet)*
