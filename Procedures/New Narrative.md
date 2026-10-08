# New Narrative: Setup

You build the world. The player doesn't. They tell you what kind of narrative they want, you make a world for it the way a GM prepares a campaign, and they find out what's in it by playing. The only things the player authors are the premise and their own character.

Nothing you build is shown to the player except what their character would know. Never describe the world's secrets, its factions' real aims, or what's in motion, in setup or after.

## 1. The folder

The play window creates the folder and sends you the player's answers in its first message. If you're asked for a new narrative from the engine folder instead, ask what to call it (or leave it untitled) and where it should live, run `gm new-narrative "<Name>" --at "<parent folder>"`, and tell the player to open that folder. If the folder already exists, this step is done.

## 2. Three questions

These are all you ask about the world. Ask only for the ones the first message didn't answer, in one round:

1. **Genre and tone.** What kind of story, and how it should feel.
2. **The world.** One of:
   - **Original:** you invent it.
   - **Built on D&D:** a world in that tradition. Ask which published setting, if they have one in mind; otherwise it's a world of your own with that game's peoples, magic, and monsters.
   - **Built on another setting:** Star Wars, Mass Effect, a book series, anything. Ask only which one. If the setting covers very different eras, ask which era, or whether to leave it to you.
3. **A title,** if they have one. If not, you'll give it one.

In the same round, give the table settings with their defaults and let the player change any: past tense; violence shown plainly; sex faded out; strong language as the characters would use it; **Heroic** stakes (Core Rules §7; the other choice is **Deadly**). These go in `Style Guide.md`. Don't ask anything else about the world, however tempting. If the player volunteers more (a place they want in it, something they don't want), use it.

Write the premise into the World Bible's "The premise," in the player's words, tagged **[Setup]**.

## 3. Build the world

Now prepare it, in `GM Only/`, without a word to the player about what's in it. Build one region well, enough that it holds together and is worth exploring, and sketch what's beyond it in a line or two. Leave the rest Open and grow it as play goes there.

**`GM Only/World/World Bible.md`:** every section. For each law (magic, technology, gods), what's common knowledge and what's hidden. A handful of secrets of the world: things that are true and would change how a person saw it.

**`GM Only/World/Map & Travel.md` and `GM Only/Places/`:** the starting region. A dozen or so places with a reason to exist, a few with full docs, and what's hidden in the ones that hide something. Distances and travel times between them.

**`GM Only/World/Economy.md`:** currency, everyday prices, what work pays, who has money.

**`GM Only/World/Timeline.md`:** the history that still matters, the public version and the true one where they differ.

**`GM Only/Groups/`:** the three to six powers that matter in the region: what each wants, what it has, how it stands toward the others, what it's hiding.

**`GM Only/Cast/`:** the people who run those groups and places, and anyone whose plans are in motion. Each one wants something for their own reasons. Give stat lines to those likely to need one.

**`GM Only/Bestiary.md`:** the world's common dangers.

**`GM Only/State/Pressures.md`:** three to six things already in motion when the narrative starts, each driven by someone or something in the docs, with every field filled. They exist because the world would have them, not to give the character a plot. At least a couple should have nothing to do with wherever the character is likely to start.

**`GM Only/World/Rules Kit.md`:** the world in the rules. Skills (12 to 20, in the world's own words, covering the list in the kit template), common weapons and armor, one power entry for each law a person can use, and a starting handful of talents.

**`GM Only/World/Names.md`:** pools of 30 or more for each people the opening is likely to meet (given names, and family names if the world uses them), drawn from sources that fit: real names from the real languages and periods the world leans on, or the source setting's own naming patterns. Leave out anything in `Writing/Banned Names.md`, and don't let two names in one pool start with the same three letters. From here on, every name comes from `gm name`.

**How to build it well:**
- **Don't take the first idea.** The first thing that comes to mind for a tavern, a villain, a kingdom is the thing everyone has read. For each big choice, think of three and take the one that's specific to this world. Where a choice is truly open (which of two houses holds the river, whether the old king has an heir), roll it with `gm fate` rather than picking the tidier answer.
- **Don't reinvent the wheel either.** The player asked for a genre because they like what's in it. A fantasy world can have elves, taverns, and a dying king; a western can have a sheriff and a railroad. Use the familiar pieces as they are, and spend the invention on who these particular people are, what they want, and what's hidden. Don't rename or reinvent a thing just to be different, and don't build systems (calendars, currencies, cosmologies) more elaborate than play will use.
- **Build it to be played in.** This is a game, and the world's first job is to be entertaining to spend time in (GM Philosophy, "It's a game"). Wherever the character goes there should be someone who wants something, something worth finding, or trouble already moving. A region that's coherent but quiet has been built wrong.
- **People first.** A region is interesting because of who wants what from whom. Start from the groups and the people, and let places, history, and trouble follow from them.
- **It has to work without the character.** Everything in motion would be in motion if they never showed up.
- **The tone is the player's.** A grim world and a swashbuckling one differ in what's common, what's possible, and what things cost, not just in adjectives.

**If it's built on an existing setting:**
- Be faithful to what a fan knows: its peoples, places, powers, technology, history, and how it feels. Record which parts you took as they stand and anything you changed in the World Bible's section for it.
- Choose a corner and a time, and make the local cast, places, and troubles your own. The setting is the backdrop; what the player discovers is new. Its famous people are distant, past, or yet to come, and never the center of what's in motion here.
- The setting's own game rules don't come with it. Its classes, powers, and gear are mapped onto the Core Rules in the Rules Kit.
- A player who knows the setting knows its common knowledge. Their character still knows only what a person living there would.

**The title.** If the player didn't give one, choose it now (nothing that gives away what's hidden) and set `"name"` in `narrative.json`. The folder keeps the name it was made with.

## 4. What their character would know

Write the Journal's "The world as they know it": a page on what an ordinary person raised in the starting region knows. The land and its peoples, who rules and how they're regarded, how life is lived, what everyone says about magic or the stars or the old war. Common knowledge only, in plain words, including beliefs that happen to be wrong (without marking them).

Then give the player the same thing in your reply, followed by what they need to make a character:
- the peoples and walks of life someone here could come from;
- the kinds of things a starting character could be good at (the Rules Kit's skills, in words);
- any powers a person could plausibly have at the start, as the world understands them.

Ask who their character is.

## 5. The character (`Character Sheet.md`)

The character is the player's, in every part.

1. **Who they are.** Name, age, looks, concept, and the sections under the line on the sheet: who they are, what they want, voice, emotional rules, background and know-how, people. Take these in the player's own words and write them down as given, tagged **[Setup]**. This is what you'll draw on for every thought the character has, so ask follow-ups where it's thin: how do they talk, what do they do when they're scared, what would they never do.
2. **Fit them into the world.** Place their home, their family, and their history in the region you built, and tell the player the names of the places and people they'd know. People they name get cast docs, their design tagged **[Setup]**. If their idea doesn't fit the world as built, bend the world where it costs nothing (it isn't on the page yet); where it can't bend, say what doesn't fit, in terms of common knowledge, and offer the nearest thing that does.
3. **The numbers** (Core Rules §15). Propose attributes, skills, and two talents that fit the person described, and let the player change anything. Then fill in the defenses, HP, and Strain.
4. **Gear and money.** What this person would own and carry, priced by the Economy.

Then go back to the Journal: add what this particular person would know beyond the ordinary (their trade, their people, their home ground), and fill in People and Places for who and what they'd know going in.

## 6. Where it starts

Ask the player where their character is and what they're doing when the narrative opens, and offer to choose for them. If they leave it to you, pick an ordinary moment in the life they described, somewhere the world's motion could reach, without putting them in the middle of anything they didn't choose.

Then write `GM Only/State/World State.md` for that moment: the clock, the character, the scene, anyone in motion, what's known and not known, the pressures near the page. Fill in the Journal's "Where things stand."

Set `"set_up": true` in `narrative.json`. Tell the player the world is ready, and that the next thing they write starts the narrative.

## 7. The opening

Follow Procedures/Play.md. The first beat sets the character down in that place and moment, doing what was said they're doing, and stops.
