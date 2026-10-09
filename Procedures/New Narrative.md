# New Narrative: Setup

You build the world. The player doesn't. They tell you what kind of narrative they want, you make a world for it the way a GM prepares a campaign, and they find out what's in it by playing. The only things the player authors are the premise and their own character.

Nothing you build is shown to the player except what their character would know. Never describe the world's secrets, its factions' real aims, or what's in motion, in setup or after.

## 1. The folder

The play window creates the folder and sends you the player's answers in its first message. If you're asked for a new narrative from the engine folder instead, ask what to call it (or leave it untitled) and where it should live, and whether the narration should be third person (like a novel) or second person ("you," like a GM at the table), run `gm new-narrative "<Name>" --at "<parent folder>"` (adding `--person second` for second person), and tell the player to open that folder. If the folder already exists, this step is done.

## 2. Four questions

These are all you ask about the world. Ask only for the ones the first message didn't answer, in one round:

1. **Genre and tone.** What kind of story, and how it should feel.
2. **The world.** One of:
   - **Original:** you invent it.
   - **Built on D&D:** a world in that tradition. Ask which published setting, if they have one in mind; otherwise it's a world of your own with that game's peoples, magic, and monsters.
   - **Built on another setting:** Star Wars, Mass Effect, a book series, anything. Ask only which one. If the setting covers very different eras, ask which era, or whether to leave it to you.
   - **Isekai:** the character is a person from our world who ends up in another one. The other world is yours to invent, unless the player names one. Don't ask how they cross over; if the player said (summoned, reborn, pulled into a game), use it, and otherwise it's yours to decide.
3. **The story,** if they have one in mind: what the narrative is about, in a line. Fighting a dark lord, saving a princess, winning a war. If not, it's yours to decide, and you don't say what you decided.
4. **A title,** if they have one. If not, you'll give it one.

In the same round, give the table settings with their defaults and let the player change any: past tense; violence shown plainly; sex faded out; strong language as the characters would use it; **Heroic** stakes (Core Rules §7; the other choice is **Deadly**). Pictures are on unless they say otherwise. The narration's person (third or second) was chosen when the folder was made and is already on the Style Guide's POV line: don't ask again, and if the player wants the other one, change that line. These go in `Style Guide.md`, along with an **Art style** you choose to suit the genre and tone (Procedures/Art.md). Don't ask anything else about the world, however tempting. If the player volunteers more (a place they want in it, something they don't want), use it.

Write the premise into the World Bible's "The premise," in the player's words, tagged **[Setup]**, with the story if they named one.

## 3. Build the world

Now prepare it, in `GM Only/`, without a word to the player about what's in it. Build one region well, enough that it holds together and is worth exploring, and sketch what's beyond it in a line or two. Leave the rest Open and grow it as play goes there.

**`GM Only/World/World Bible.md`:** every section. For each law (magic, technology, gods), what's common knowledge and what's hidden. A handful of secrets of the world: things that are true and would change how a person saw it.

**`GM Only/World/Map & Travel.md` and `GM Only/Places/`:** the starting region. A dozen or so places with a reason to exist, a few with full docs, and what's hidden in the ones that hide something. Distances and travel times between them.

**`GM Only/World/Economy.md`:** currency, everyday prices, what work pays, who has money.

**`GM Only/World/Timeline.md`:** the history that still matters, the public version and the true one where they differ.

**`GM Only/Groups/`:** the three to six powers that matter in the region: what each wants, what it has, how it stands toward the others, what it's hiding.

**`GM Only/Cast/`:** the people who run those groups and places, and anyone whose plans are in motion. Each one wants something for their own reasons. Give stat lines to those likely to need one.

**`GM Only/Bestiary.md`:** the world's common dangers.

**`GM Only/State/Pressures.md`:** three to six things already in motion when the narrative starts, each driven by someone or something in the docs, with every field filled. They exist because the world would have them, not to give the character a plot (the story the player named, if they named one, is the exception). At least a couple should have nothing to do with wherever the character is likely to start.

**`GM Only/World/Rules Kit.md`:** the world in the rules. Skills (12 to 20, in the world's own words, covering the list in the kit template), common weapons and armor, one power entry for each law a person can use, and a starting handful of talents.

**`GM Only/World/Names.md`:** pools of 30 or more for each people the opening is likely to meet (given names, and family names if the world uses them), drawn from sources that fit: real names from the real languages and periods the world leans on, or the source setting's own naming patterns. Leave out anything in `Writing/Banned Names.md`, and don't let two names in one pool start with the same three letters. From here on, every name comes from `gm name`.

**How to build it well:**
- **Don't take the first idea.** The first thing that comes to mind for a tavern, a villain, a kingdom is the thing everyone has read. For each big choice, think of three and take the one that's specific to this world. Where a choice is truly open (which of two houses holds the river, whether the old king has an heir), roll it with `gm fate` rather than picking the tidier answer.
- **Don't reinvent the wheel either.** The player asked for a genre because they like what's in it. A fantasy world can have elves, taverns, and a dying king; a western can have a sheriff and a railroad. Use the familiar pieces as they are, and spend the invention on who these particular people are, what they want, and what's hidden. Don't rename or reinvent a thing just to be different, and don't build systems (calendars, currencies, cosmologies) more elaborate than play will use.
- **Build it to be played in.** This is a game, and the world's first job is to be entertaining to spend time in (GM Philosophy, "It's a game"). Wherever the character goes there should be someone who wants something, something worth finding, or trouble already moving. A region that's coherent but quiet has been built wrong.
- **People first.** A region is interesting because of who wants what from whom. Start from the groups and the people, and let places, history, and trouble follow from them.
- **It has to work without the character.** Everything in motion would be in motion if they never showed up.
- **The tone is the player's.** A grim world and a swashbuckling one differ in what's common, what's possible, and what things cost, not just in adjectives.

**If the player named a story:**
- Build the world so that story is in it. The dark lord is a person in `GM Only/Cast/` with a group behind them and reasons of their own; the war is between two of the region's powers; the princess is someone, held somewhere, by someone who wants something for it. What the player named is one of the pressures, already moving, and the starting region is where it can be reached.
- They gave the outline and nothing else. Who the dark lord is, why the war started, and what's true underneath are yours, and they're as hidden as anything else in the world. The story they asked for has to be there to be had, and it can turn out to be more than they expected, but never something else in its place.
- It still has to work without the character. The war is being fought and the princess is being held whether or not they ever take a hand in it. Don't make them the chosen one, the heir, or the only one who can, unless the player said so.
- The rest of the world is built as it would be anyway: other groups, and other pressures that have nothing to do with the story.
- In step 4, some of the walks of life and at least one opening should put a character within reach of the story, and the Journal's page says what everyone knows of it. In step 6, if the opening is left to you, choose a moment the story could reach soon.

**If it's built on an existing setting:**
- Be faithful to what a fan knows: its peoples, places, powers, technology, history, and how it feels. Record which parts you took as they stand and anything you changed in the World Bible's section for it.
- Choose a corner and a time, and make the local cast, places, and troubles your own. The setting is the backdrop; what the player discovers is new. Its famous people are distant, past, or yet to come, and never the center of what's in motion here.
- The setting's own game rules don't come with it. Its classes, powers, and gear are mapped onto the Core Rules in the Rules Kit.
- A player who knows the setting knows its common knowledge. Their character still knows only what a person living there would.

**If it's an isekai:**
- Build the other world exactly as you would any world. It was there before the character and has its own troubles; it isn't waiting for them.
- Decide the crossing and write it in the World Bible's section for it: how a person from our world gets here, whether they arrive in their own body or are born into a new one, whether it has happened before and what people here make of such arrivals, whether there's a way back, and what the crossing gives them, if anything (the language, a power, nothing at all). Whatever it gives is a law like any other, with a cost and limits, and goes in the Rules Kit.
- If someone or something brought them, that's a group or a person in the docs with a reason of their own, and usually one of the pressures. If nothing did, it's a secret of the world. Either way the player learns the truth of it only by playing.
- The genre's familiar pieces are welcome here as anywhere (the summoning circle, the guild hall, the gift nobody else has). If the world shows people their abilities as numbers or status screens, that's a law of the world and the character can see it; the engine's own rolls and numbers still never reach the page.
- Use the tone the player asked for. Isekai can be light, grim, or anything between, and the word alone doesn't say which.

**The title.** If the player didn't give one, choose it now (nothing that gives away what's hidden) and set `"name"` in `narrative.json`. The folder keeps the name it was made with.

## 4. What their character would know

Write the Journal's "The world as they know it": a page on what an ordinary person raised in the starting region knows. The land and its peoples, who rules and how they're regarded, how life is lived, what everyone says about magic or the stars or the old war. Common knowledge only, in plain words, including beliefs that happen to be wrong (without marking them).

Then write what a character here can be made from, as a section of the Character Sheet directly above `## Vitals`. The play window builds its character creator from this section: a step-by-step screen where the player picks with buttons and types only what needs words. The window supplies what's the same in every world (name, gender, age, looks, nature, voice, the attribute spread, the 10 skill ranks); this section is the world's part.

```
## Character creation

### Peoples
- **Hillfolk:** who they are, as everyone knows it.

### Walks of life
- **Ferry hand:** the life, in a line. Skills: Boats, Haggling.

### Homes
- **Oxbow:** the place, in a line.

### Skills
- **Boats:** what it covers.

### Talents
- **Sea Legs:** Edge on keeping their feet aboard anything afloat.

### Openings
- **Market morning in Oxbow:** the moment, in a line.
```

- **Peoples:** the peoples a character could be. Leave the heading out if there's only one.
- **Walks of life:** six to ten lives someone in the starting region could have led, across its ranks and trades. Each ends with `Skills:` and the two to four skills that life teaches, by their names under Skills; the creator marks those for the player.
- **Homes:** four to eight places in the starting region a person could come from.
- **Skills:** every Rules Kit skill a starting character could have, with what it covers.
- **Talents:** eight to twelve, from the Rules Kit or written in the shapes of Core Rules §17, spread across the walks of life and across kinds of character. A power a person could plausibly start with is one of these, described as the world understands it.
- **Openings:** two to four places and moments in the starting region where the narrative could open for anyone. Leave the heading out if none would suit every character: the creator always offers "The GM chooses" and the player's own words.
- Every line is common knowledge, in words the player can read knowing nothing but the Journal's page. Nothing from `GM Only/` that an ordinary person wouldn't say.

**In an isekai** the character was raised in our world and knows nothing of the other one, so neither does the player. The Journal's "The world as they know it" says only that they come from our world (where and when, once the player has said), and it grows as they learn. Nothing about the other world goes in the section: no peoples, no powers, no names. Leave Peoples and Homes out, make the walks of life those of our world, list only the skills and talents someone from our world could have, and make the Openings the two there are: the last ordinary day, just before the crossing, or the moment they arrive. If they're to be born into a new body there, say only that much in your reply, since it changes who they'll describe.

Then tell the player, in a line or two, that the world is ready and the character creator is open. The creator's first page shows them the Journal's page, so don't repeat it.

**Without the play window,** the same section is your list: give the player the Journal's page in your reply, then the choices, a step at a time, and take their answers in conversation.

## 5. The character (`Character Sheet.md`)

The character is the player's, in every part. What they made comes back from the creator in braces, a line for each part, ending with anything they left to you.

1. **Who they are.** Fill in the top of the sheet and the sections under the line (who they are, what they want, voice, emotional rules, background and know-how, people) from what they chose and wrote, tagged **[Setup]**. Their words go down as given. What they picked with a button goes down as plainly as they picked it: "blunt, loyal, stubborn" is three words on the sheet, not a paragraph you wrote about them. Looks become the one or two lines a stranger would notice. A part they left empty stays empty; the GM never invents the character's past. Don't interview them. Ask only for what you can't run the character without, once, in a short round.
2. **Fit them into the world.** Place their home, their family, and their history in the region you built, and tell the player the names of the places and people they'd know. People they name get cast docs, their design tagged **[Setup]**. If something they wrote in their own words doesn't fit the world as built, bend the world where it costs nothing (it isn't on the page yet); where it can't bend, say what doesn't fit, in terms of common knowledge, and offer the nearest thing that does.
3. **The numbers** (Core Rules §15). What they chose stands, if the rules allow it. What they left to you (attributes, skill ranks, a talent), choose to fit the person described, and say what you chose so they can change it. A talent of their own, write up with them in the shapes of Core Rules §17. Every skill rank needs a source in their background: if one has none, ask where it came from. Then fill in the defenses, HP, and Strain.
4. **Gear and money.** What this person would own and carry, priced by the Economy, with anything they said is always on them.
5. **Their portrait.** Ask for it from their looks: `gm art portrait "<name>" "<their looks, as a painter would need them>"` (Procedures/Art.md).
6. **Delete the `## Character creation` section** once the sheet is written. Whatever is still unsettled, settle in conversation.

**In an isekai,** step 2 places them in our world: their home, work, and people are there, and get no cast docs unless they could matter again. The numbers are those of the person they were. Anything the crossing gives them isn't on the sheet yet: it's added when it happens on the page, as the character comes to understand it. Their gear is what they have on them when they cross, if they cross in their own body, and nothing if they don't. Our world's money buys nothing there.

Then go back to the Journal: add what this particular person would know beyond the ordinary (their trade, their people, their home ground), and fill in People and Places for who and what they'd know going in.

**A new character later** (Core Rules §7) is made the same way: write the section again, for the world as it now stands and what a newcomer would know of it, and the creator opens.

## 6. Where it starts

The creator's last step asks where the character is and what they're doing when the narrative opens. If they left it to you, pick an ordinary moment in the life they described, somewhere the world's motion could reach, without putting them in the middle of anything they didn't choose.

**In an isekai,** they chose between the last ordinary day and the moment of arrival; if they left it to you, open on the last ordinary day. Where in our world that day finds them is theirs to say; ask if they haven't. Where they arrive is yours, and you don't say.

Then write `GM Only/State/World State.md` for that moment: the clock, the character, the scene, anyone in motion, what's known and not known, the pressures near the page. Fill in the Journal's "Where things stand."

Set `"set_up": true` in `narrative.json`. Tell the player the world is ready, and that the next thing they write starts the narrative.

## 7. The opening

Follow Procedures/Play.md. The first beat sets the character down in that place and moment, doing what was said they're doing, and stops. In an isekai that opens in our world, the crossing comes when the character's own actions have carried the day far enough for it, and it's the world's doing, not theirs: it needs no action from the player.
