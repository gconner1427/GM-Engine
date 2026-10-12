# New Narrative: Setup

You build the world. The player doesn't. They tell you what kind of narrative they want, you make a world for it the way a GM prepares a campaign, and they find out what's in it by playing. The only things the player authors are the premise and their own character.

Every narrative is a campaign. Before the first session you decide what it's about: a goal the character is meant to work toward (bring down a dark lord, stop a war, find someone), what stands against it, and the hook that puts this character in it. The world is built around that, and the first session opens on the hook. The player is free to go after anything else along the way, and the world has plenty else in it, but there is always something they're supposed to be doing.

Nothing you build is shown to the player except what their character would know. Never describe the world's secrets, its factions' real aims, or what's in motion, in setup or after.

## 1. The folder

The play window creates the folder and sends you the player's answers in its first message. If you're asked for a new narrative from the engine folder instead, ask what to call it (or leave it untitled) and where it should live, and whether the narration should be third person (like a novel) or second person ("you," like a GM at the table), run `gm new-narrative "<Name>" --at "<parent folder>"` (adding `--person second` for second person), and tell the player to open that folder. If the folder already exists, this step is done.

## 2. Five questions

These are all you ask about the world. Ask only for the ones the first message didn't answer, in one round:

1. **Genre and tone.** What kind of story, and how it should feel. The play window asks them as two steps and sends them as "Genre" and "Tone." The genre is always given, and it can be more than one (High Fantasy and Slice of Life; Sci-Fi and Space Opera): build one narrative that is all of them, never a pick among them. Slice of life in a high fantasy world is a high fantasy world, built in full, with a campaign on the scale of a life in it (keep the inn open, win the apprenticeship) and not a dark lord. If the tone was left to you, choose one that suits the genre, and you don't say what you chose.
2. **The world.** One of:
   - **Original:** you invent it.
   - **Built on D&D:** a world in that tradition. Ask which published setting, if they have one in mind; otherwise it's a world of your own with that game's peoples, magic, and monsters.
   - **Built on another setting:** Star Wars, Mass Effect, a book series, anything. Ask only which one. If the setting covers very different eras, ask which era, or whether to leave it to you.
   - **Isekai:** the character is a person from our world who ends up in another one. The other world is yours to invent, unless the player names one. Don't ask how they cross over; if the player said (summoned, reborn, pulled into a game), use it, and otherwise it's yours to decide.
   **What's in it,** if they want anything in particular: things the world should have, whichever kind it is. Adventurers and their guilds, kingdoms and empires, dungeons to explore, islands to sail to. The play window asks this as a step of its own and sends it as "In the world." If they name nothing, it's yours to decide.
3. **The story,** if they have one in mind: what the narrative is about, in a line. Fighting a dark lord, saving a princess, winning a war. If not, it's yours to decide, and you don't say what you decided. Either way it becomes the campaign (step 3): no narrative goes without one.
4. **Themes,** if they want any: what the narrative keeps coming back to. Revenge, found family, what power costs. If not, they're yours to decide, and you don't say what you decided.
5. **A title,** if they have one. If not, you'll give it one.

**The content** is the player's too, and the play window sends it as five lines, each yes or no: explicit language, explicit sex on the page, nudity outside sex scenes, graphic violence, gore. If the first message didn't carry them, ask in the same round, with every one a no unless they say otherwise. Write each onto its line under the Style Guide's "Content."
- A yes means it's written in full when the narrative goes there. It doesn't mean it has to be put in, or put in often.
- A no means it's left out: language kept mild, sex faded out, bodies kept out of view, violence told without dwelling on the damage, no gore. The world can still be a hard one; what changes is what the prose shows.
- The window can add one more, **Also include:** other content the player named in their own words (racism, slavery, drug use). It goes on the Style Guide's "Also included" line as they wrote it, and it's a yes like the others: the world can have it and the prose shows it plainly when the narrative goes there, without it having to be put in. Without the window, ask for it in the same round as the five.
- Each line stands alone. Graphic violence without gore is a fight told in full with the wounds left undescribed; nudity without explicit sex is a body described at the bath and a fade when the scene turns to sex.

**The size** is the player's too: **Small**, **Medium**, or **Large**. It says how much world they want and how long a narrative, and it decides how much you build (step 3, "How much to build"). The play window asks it as a step of its own and sends it as "Size." Without the window, ask in the same round, with Medium unless they say otherwise.
- **Small:** one place and what's around it, and a short campaign: a handful of sessions, about five.
- **Medium:** a region, and a full campaign: ten to twenty sessions.
- **Large:** a wide world, and a long campaign: dozens of sessions.
- **In a space opera** the three are counted in worlds, and the window names them that way after the size: Small is one world (a single planet or space station), Medium is one system (several planets and places in space), Large is a few systems. There's a fourth, **Galaxy**, offered only for a space opera: a whole galaxy, with many systems and a campaign that can run as long as the player likes. The window warns the player what a galaxy costs to build and makes them confirm it, so don't ask again. Without the window, offer Galaxy only for a space opera, and say first that it can take one to two hours to build and a great deal of usage.

In the same round, give the other table settings with their defaults and let the player change any: past tense; **Heroic** stakes (Core Rules §7; the other choice is **Deadly**). Pictures are on unless they say otherwise. The narration's person (third or second) was chosen when the folder was made and is already on the Style Guide's POV line: don't ask again, and if the player wants the other one, change that line. These go in `Style Guide.md`, along with an **Art style** you choose to suit the genre and tone (Procedures/Art.md). Don't ask anything else about the world, however tempting. If the player volunteers more (a place they want in it, something they don't want), use it.

Write the premise into the World Bible's "The premise," in the player's words, tagged **[Setup]**, with what they wanted in the world, the size, the story, and the themes if they named any.

## 3. Build the campaign and the world

Now prepare it, in `GM Only/`, without a word to the player about what's in it. Build one region well, enough that it holds together and is worth exploring, and sketch what's beyond it in a line or two. Leave the rest Open and grow it as play goes there.

**How much to build** is set by the size the player chose. Where the docs below give a count, it's this one:

| | Small | Medium | Large |
|---|---|---|---|
| The campaign | about five sessions | ten to twenty | dozens |
| The road's stages | two or three | three to five | five to seven |
| The starting region | one place and what's around it: a town and its valley, a station, a single city district | a region | a region, with the two or three lands next to it sketched in a paragraph each |
| Places | about six, two with full docs | a dozen or so, a few with full docs | about twenty, five or six with full docs |
| Groups | two or three | three to six | five to eight |
| Pressures | two or three | three to six | five to eight |
| The campaign's clock | 4 steps | 6 steps | 8 steps |
| Secrets of the world | two or three | a handful | a handful, and one for each neighboring land |
| Name pools | 15 or more each | 30 or more each | 30 or more each, and a pool for each neighboring people |
| Walks of life, homes, talents (step 4) | four to six, two to four, six to eight | six to ten, four to eight, eight to twelve | eight to twelve, six to ten, ten to fourteen |

- **In a space opera,** the starting region is the size's reach, and the counts are the same. Small: one planet or station, and its places are its cities, decks, and wilds. Medium: one system, and its places are spread across its planets, moons, and stations, with travel times between them. Large: the starting system in full, and one or two more with their main worlds sketched in a paragraph each.
- **A galaxy** is the Large column and more. The starting system is built in full. Five to eight more systems each get a paragraph, their main worlds and places in space in a line each, and one or two places with full docs. Across all of it: about forty places, ten or so with full docs; eight to twelve groups, several of them powers that span systems; six to ten pressures; a road of six to eight stages that crosses systems; an 8-step clock; a name pool for each people; and walks of life, homes, and talents as at Large. How ships cross between systems, how long it takes, and what it costs go in `Map & Travel.md`. Even here the far side of the galaxy is a line or two and Open: it's built when play goes there.
- **A small world is a whole one, only close in.** Everything is still built (every doc below, every section), and built as well: it's the counts that shrink, and what's past the horizon gets a line. The goal is one that can be reached in a handful of sessions (clear the mine, find the missing girl, win the election), and nothing in the docs is put there for a session that won't be played. Don't build more than the size calls for because the genre seems to want it: the player chose Small to be playing sooner.
- **A large world is still one region at a time.** Build the starting region in full and the lands next to it in outline, and put the road's later stages out there. They get their full docs when play comes near them, never now.
- **The sessions are a measure, never a limit.** They say how big a goal to choose and how long its road should be. Once play starts the campaign takes as long as it takes (GM Rules, "The campaign").
- Write the size in `Campaign.md`, "The size."

**`GM Only/State/Campaign.md`, first.** Decide what this narrative is about before you build anything else, because everything else is built around it:
- **The goal:** what the character is meant to do, in a line, and what would count as done. If the player named a story, this is it. If they didn't, choose one that suits the genre, the tone, and the themes, and that one person could plausibly see through. It needs an end: "survive" and "explore" aren't goals; "get the plague cure to the capital before the passes close" is.
- **What's at stake** and **the opposition:** who wants what the goal is against, why, and what happens if nobody stops them. The opposition is a person or a group in the docs below, with reasons that make sense from where they stand.
- **The road:** the stages between the start and the end (three to five, at Medium), each something that has to be learned, won, reached, or decided. Milestones, never scenes. Write the first in full and the rest in a line each.
- **How it could end:** two or three honest ways.
- Leave **The hook** until the character is made (step 6), and **Where it stands** until play starts.

Then the world, built so the campaign is in it and can be reached from the starting region:

**`GM Only/World/World Bible.md`:** every section. For each law (magic, technology, gods), what's common knowledge and what's hidden. The secrets of the world (a handful, at Medium): things that are true and would change how a person saw it.

**`GM Only/World/Map & Travel.md` and `GM Only/Places/`:** the starting region. Its places (a dozen or so, at Medium), each with a reason to exist, a few with full docs, and what's hidden in the ones that hide something. Distances and travel times between them.

**`GM Only/World/Economy.md`:** currency, everyday prices, what work pays, who has money.

**`GM Only/World/Timeline.md`:** the history that still matters, the public version and the true one where they differ.

**`GM Only/Groups/`:** the powers that matter in the region (three to six, at Medium): what each wants, what it has, how it stands toward the others, what it's hiding. The campaign's opposition is one of them, or is behind one, and at least one other has a reason to want the goal reached.

**`GM Only/Cast/`:** the people who run those groups and places, and anyone whose plans are in motion. Each one wants something for their own reasons. Give stat lines to those likely to need one. Among them: the opposition, and the people the first stage of the road runs through (who knows something, who needs help, who's in the way).

**`GM Only/Bestiary.md`:** the world's common dangers.

**`GM Only/State/Pressures.md`:** the things already in motion when the narrative starts (three to six, at Medium), each driven by someone or something in the docs, with every field filled. One is the campaign's: what the opposition is doing, heading toward what's at stake, on a clock as long as the campaign (6 steps, at Medium) so there's a campaign's worth of time before it fills. The others exist because the world would have them, and they're where side quests come from: at least a couple should have nothing to do with the campaign, and at least a couple should be within reach of wherever the character is likely to start.

**`GM Only/World/Rules Kit.md`:** the world in the rules. Skills (12 to 20, in the world's own words, covering the list in the kit template), common weapons and armor, one power entry for each law a person can use, and a starting handful of talents.

**`GM Only/World/Names.md`:** pools (of 30 or more, at Medium) for each people the opening is likely to meet (given names, and family names if the world uses them), drawn from sources that fit: real names from the real languages and periods the world leans on, or the source setting's own naming patterns. Leave out anything in `Writing/Banned Names.md`, and don't let two names in one pool start with the same three letters. From here on, every name comes from `gm name`.

**How to build it well:**
- **Start from the campaign.** A GM preparing a campaign knows what it's about before drawing the map. Put the goal's opposition and the road's first stage in the starting region or within a few days of it, and let the region's groups, people, and places take their shape from where they stand on it. Then build the rest, which has nothing to do with it.
- **Don't take the first idea.** The first thing that comes to mind for a tavern, a villain, a kingdom is the thing everyone has read. For each big choice, think of three and take the one that's specific to this world. Where a choice is truly open (which of two houses holds the river, whether the old king has an heir), roll it with `gm fate` rather than picking the tidier answer.
- **Don't reinvent the wheel either.** The player asked for a genre because they like what's in it. A fantasy world can have elves, taverns, and a dying king; a western can have a sheriff and a railroad. Use the familiar pieces as they are, and spend the invention on who these particular people are, what they want, and what's hidden. Don't rename or reinvent a thing just to be different, and don't build systems (calendars, currencies, cosmologies) more elaborate than play will use.
- **Build it to be played in.** This is a game, and the world's first job is to be entertaining to spend time in (GM Philosophy, "It's a game"). Wherever the character goes there should be someone who wants something, something worth finding, or trouble already moving. A region that's coherent but quiet has been built wrong.
- **People first.** A region is interesting because of who wants what from whom. Start from the groups and the people, and let places, history, and trouble follow from them.
- **It has to work without the character.** Everything in motion would be in motion if they never showed up, the campaign's opposition included. The hook is what puts the character in its way; nothing in the world was waiting for them.
- **The tone is the player's.** A grim world and a swashbuckling one differ in what's common, what's possible, and what things cost, not just in adjectives.
- **Themes are built in, never stated.** A theme the player named (or one you chose) belongs in who wants what and what it costs them: several of the groups, people, and pressures should turn on it, each from a different side. Nobody in the world says it out loud, and the prose never does.

**If the player named a story:**
- That story is the campaign, and its goal is the one they named. The dark lord is a person in `GM Only/Cast/` with a group behind them and reasons of their own; the war is between two of the region's powers; the princess is someone, held somewhere, by someone who wants something for it. What the player named is the campaign's pressure, already moving, and the starting region is where it can be reached.
- They gave the outline and nothing else. Who the dark lord is, why the war started, and what's true underneath are yours, and they're as hidden as anything else in the world. The story they asked for has to be there to be had, and it can turn out to be more than they expected, but never something else in its place.
- It still has to work without the character. The war is being fought and the princess is being held whether or not they ever take a hand in it. Don't make them the chosen one, the heir, or the only one who can, unless the player said so.
- The rest of the world is built as it would be anyway: other groups, and other pressures that have nothing to do with the story.
- The Journal's page (step 4) says what everyone knows of it.

**If the player named things for the world:**
- Every one of them is in the world, in the starting region or within reach of it, as something the character can go to, join, deal with, or run into. A thing that's only mentioned hasn't been put in.
- They gave the names and nothing else. Which kingdoms, who runs the guild, what's at the bottom of the dungeon are yours, and as hidden as anything else.
- Work them into the campaign where they fit honestly (the road runs through the dungeon, the guild is one of the region's powers) and into the pressures where they don't, so they're there for side quests. Don't bend the campaign to touch every one.
- If one doesn't fit the genre or the setting as it stands, put in the nearest thing that does, and say so in a line when you tell the player the world is ready.
- The Journal's page (step 4) says what everyone knows of them, and the walks of life, homes, and talents offer a way into them where a person could have one (an adventurer, a guild clerk, an islander).

**If it's built on an existing setting:**
- Be faithful to what a fan knows: its peoples, places, powers, technology, history, and how it feels. Record which parts you took as they stand and anything you changed in the World Bible's section for it.
- Choose a corner and a time, and make the local cast, places, and troubles your own. The setting is the backdrop; what the player discovers is new. Its famous people are distant, past, or yet to come, and never the center of what's in motion here.
- The setting's own game rules don't come with it. Its classes, powers, and gear are mapped onto the Core Rules in the Rules Kit.
- A player who knows the setting knows its common knowledge. Their character still knows only what a person living there would.

**If it's an isekai:**
- Build the other world exactly as you would any world. It was there before the character and has its own troubles; it isn't waiting for them.
- Decide the crossing and write it in the World Bible's section for it: how a person from our world gets here, whether they arrive in their own body or are born into a new one, whether it has happened before and what people here make of such arrivals, whether there's a way back, and what the crossing gives them, if anything (the language, a power, nothing at all). Whatever it gives is a law like any other, with a cost and limits, and goes in the Rules Kit.
- If someone or something brought them, that's a group or a person in the docs with a reason of their own, and usually one of the pressures. If nothing did, it's a secret of the world. Either way the player learns the truth of it only by playing.
- The crossing is the first half of the hook, never the whole of it, and "get home" is the goal only if the player asked for that. The campaign is something in the other world, and the hook (step 6) is what puts this newcomer in it once they've arrived.
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

```

- **Peoples:** the peoples a character could be. Leave the heading out if there's only one.
- **Walks of life:** six to ten lives (at Medium; the counts in this list follow the size, step 3) someone in the starting region could have led, across its ranks and trades. Every one has to be a life the campaign could reach: before you list one, be sure you could write a hook for it. Each ends with `Skills:` and the two to four skills that life teaches, by their names under Skills; the creator marks those for the player.
- **Homes:** four to eight places in the starting region a person could come from.
- **Skills:** every Rules Kit skill a starting character could have, with what it covers.
- **Talents:** eight to twelve, from the Rules Kit or written in the shapes of Core Rules §17, spread across the walks of life and across kinds of character. A power a person could plausibly start with is one of these, described as the world understands it.
- The creator doesn't ask where the narrative opens, and neither do you. That's yours to decide (step 6).
- Every line is common knowledge, in words the player can read knowing nothing but the Journal's page. Nothing from `GM Only/` that an ordinary person wouldn't say.

**In an isekai** the character was raised in our world and knows nothing of the other one, so neither does the player. The Journal's "The world as they know it" says only that they come from our world (where and when, once the player has said), and it grows as they learn. Nothing about the other world goes in the section: no peoples, no powers, no names. Leave Peoples and Homes out, make the walks of life those of our world, and list only the skills and talents someone from our world could have. If they're to be born into a new body there, say only that much in your reply, since it changes who they'll describe.

Then tell the player, in a line or two, that the world is ready and the character creator is open. The creator's first page shows them the Journal's page, so don't repeat it.

**Without the play window,** the same section is your list: give the player the Journal's page in your reply, then the choices, a step at a time, and take their answers in conversation.

## 5. The character (`Character Sheet.md`)

The character is the player's, in every part. What they made comes back from the creator in braces, a line for each part, ending with anything they left to you.

1. **Who they are.** Fill in the top of the sheet and the sections under the line (who they are, what they want, voice, emotional rules, background and know-how, people) from what they chose and wrote, tagged **[Setup]**. Their words go down as given. What they picked with a button goes down as plainly as they picked it: "blunt, loyal, stubborn" is three words on the sheet, not a paragraph you wrote about them. Looks become the one or two lines a stranger would notice. A part they left empty stays empty; the GM never invents the character's past. Don't interview them. Ask only for what you can't run the character without, once, in a short round.
2. **Fit them into the world.** Place their home, their family, and their history in the region you built, and tell the player the names of the places and people they'd know. People they name get cast docs, their design tagged **[Setup]**. Only the character is the player's: everyone else in their life, family included, is yours to fill in around what the player gave (where a father soldiered, how a mother died, who a mentor answers to), tagged **[GM]**. Fitting what they gave into the world is your job, so do it and don't ask. If something they wrote in their own words doesn't fit the world as built, bend the world where it costs nothing (it isn't on the page yet); where it can't bend, say what doesn't fit, in terms of common knowledge, and offer the nearest thing that does.
3. **The numbers** (Core Rules §15). What they chose stands, if the rules allow it. What they left to you (attributes, skill ranks, a talent), choose to fit the person described, and say what you chose so they can change it. A talent of their own, write up with them in the shapes of Core Rules §17. Never ask why they picked a skill, an attribute, or a talent, or where it came from: the build is theirs, for their own reasons, as at any table. Then fill in the defenses, HP, and Strain.
4. **Gear and money.** What this person would own and carry, priced by the Economy, with anything they said is always on them. Write each gear line the way the play window's inventory reads it (Procedures/Play.md, "Gear lines").
5. **Their portrait.** Ask for it from their looks: `gm art portrait "<name>" "<their looks, as a painter would need them>"` (Procedures/Art.md).
6. **Delete the `## Character creation` section** once the sheet is written. Whatever is still unsettled, settle in conversation.

**In an isekai,** step 2 places them in our world: their home, work, and people are there, and get no cast docs unless they could matter again. The numbers are those of the person they were. Anything the crossing gives them isn't on the sheet yet: it's added when it happens on the page, as the character comes to understand it. Their gear is what they have on them when they cross, if they cross in their own body, and nothing if they don't. Our world's money buys nothing there.

Then go back to the Journal: add what this particular person would know beyond the ordinary (their trade, their people, their home ground), and fill in People and Places for who and what they'd know going in.

**A new character later** (Core Rules §7) is made the same way: write the section again, for the world as it now stands and what a newcomer would know of it, and the creator opens. They need a hook of their own (step 6) into the campaign as it now stands, and the session after they're made opens on it.

## 6. The hook, and where it starts

Now there's a campaign and a character, and the hook joins them. It's the answer to why this person is in this story at all, and no narrative starts without one. Write it in `Campaign.md`, "The hook."

- **Make it theirs.** Read the sheet for what the player gave this person: what they want, who they love, what they owe, their trade, where they're from. The hook catches one of those, so going after the goal is something the character has a reason of their own to do. A stranger offering a job to whoever's nearest is the weakest hook there is; the same job offered because of who their mother was, or because it's their village on the road, is a hook.
- **It's something that happens.** A hook is an event the world brings to the character, on the page, in the first session: someone arrives, something is found, something is taken, something goes wrong in front of them. It leaves them with a first step they can see, and it usually shows them only that step, never the whole campaign.
- **It comes from the docs.** Someone in the cast does it, for their own reasons, as part of what's already in motion. If the campaign as built can't reach this character honestly, change the campaign's first stage (it isn't on the page yet) rather than force it.
- **It never plays the character.** The hook can't depend on what they decide once it arrives: whether they take it up, and how, is the player's. Make it one they'd want to take up. If they turn it down, the campaign goes on moving and reaches for them again another way (GM Rules, "The campaign").
- **You write it, and you don't ask.** A GM at a table doesn't ask the players where they start or whether the hook suits them: the GM starts them, with the hook. Never put the opening or the hook to the player for approval. If it needs the character to be somewhere or on their way to something, build that from what the player already gave (what they want, their trade, where they're from), so the step is one they'd plainly have taken. If the campaign can't reach them without a past the player didn't give, change the hook, never the character.
- **They aren't chosen.** Unless the player said so, the character isn't the heir, the prophesied one, or the only one who can. They're the one it happened to.

**Where it starts** is yours to decide, the way a GM tells the table where they are when the game begins. The player isn't asked. Choose the place and the moment where the hook would find this person: somewhere in the life they described (their home, their trade, the people they named), on a day that would be ordinary if the hook didn't come. What they're doing there is what that life, and what they said they want, has them doing (someone who wants to join the guild can open on the road to its door). You don't ask whether it suits. If the player volunteered where they want to start, use it.

**In an isekai,** whether it opens on the last ordinary day or at the moment of arrival is yours too; the ordinary day is the default, since it shows who they were. Where that day finds them comes from the life in our world the player described. Where they arrive is yours, and you don't say. The hook is in the other world, where they arrive or soon after.

Then write `GM Only/State/World State.md` for that moment: the clock, the character, the scene, anyone in motion (whoever is bringing the hook among them), what's known and not known, the pressures near the page. Fill in `Campaign.md`, "Threads" and "Where it stands," and the Journal's "Where things stand." The Journal's "The goal" waits until the character has one: it's written at the end of the first session, from what the hook showed them.

Set `"set_up": true` in `narrative.json`. Tell the player the world is ready and that you'll open the first session when they begin it (the window gives them a Begin button; without it, they say `{new session}`).

## 7. The first session

You open it (Procedures/Play.md, "Opening a session"). The opening sets the scene, with the character in the place and moment you chose, and then the hook arrives. It ends at the first thing the character would answer, and from there it's theirs.

In an isekai that opens in our world, the opening is the ordinary day. The crossing comes when the character's own actions have carried the day far enough for it, and it's the world's doing, not theirs: it needs no action from the player. The hook follows on the other side.
