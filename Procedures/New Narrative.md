# New Narrative: Setup

A narrative starts with three things from the user: a world, a character, and a place to begin. The world and the character are built from the user's answers, not from invention. "I don't know yet" is a good answer. "You decide" is a good answer too: it becomes **Open**, and you settle it when play needs it. Only what the user says they want to keep for themselves becomes **Reserved**.

## 1. Create the folder

Ask the user two things: what the narrative is called, and where on their computer it should live. Then:

```
gm new-narrative "<Name>" --at "<parent folder>"
```

It creates the folder from the template, pointed at this engine. Tell the user to open that folder in VS Code and say **"Set up this narrative."** Everything from here happens in that folder, and every later session is played from it.

(The user can also do this step alone by double-clicking `New Narrative.cmd` in the engine folder.)

## 2. The interview

Ask in short rounds, a few questions at a time, using the question tool where it helps. Write each answer into its doc as you go, tagged **[Setup]**. Take whatever the user gives in whatever form: if they paste pages of world notes, file them and ask only about the gaps. Skip what they say doesn't apply. Ask only for what the opening needs; the world grows as play needs it.

**The world (`World/World Bible.md`)**
- Genre and tone. Our world, our world with a difference, or its own world?
- Era and technology. How do people communicate, travel, fight, heal?
- The laws: anything that works differently from our world (magic, technology, gods, monsters, biology). For each: what it can do, what it can't, what it costs, who can use it, and what everyone knows about it.
- Dangers: what can hurt a person here, and how common it is.
- Law and justice. How news travels, and how fast. Whether death is final.
- Naming: how names work, and for which peoples.
- Anything the user wants Reserved.

**Where (`World/Map & Travel.md`)**
- The region the narrative starts in, and what's around it.
- How people get around, and how long common trips take.
- The place it starts. What it is, who runs it, what it holds. (Its doc goes in `GM Only/Places/`.)

**Money (`World/Economy.md`)**
- Currency. Rough prices of everyday things. What ordinary work pays.
- Who has money and who doesn't. Anything scarce.

**People and groups (`GM Only/Cast/`, `GM Only/Groups/`)**
- Anyone the user wants in the world: family, friends, enemies, rulers. For each, as much of the cast template as they care to give. Design the user gives is tagged **[Setup]** even though the doc is GM only.
- The groups that matter: what each wants, its standing, who's in it.

**History and motion (`World/Timeline.md`, `GM Only/State/Pressures.md`)**
- What happened before that still matters.
- Whether anything is already building when the narrative starts: a debt, a feud, a war, a plan.

**How it reads (`Style Guide.md`)**
- Tense: past or present.
- Register: how the narration should sound.
- Content: how graphic the violence, whether sex is on the page, language, anything off the table.
- Stakes: **Deadly** (the character can die whenever they honestly would) or **Heroic** (down means captured, robbed, hurt, left for dead; death only by the user's choice).

## 3. The rules kit (`World/Rules Kit.md`)

Build it from the world, and show the user before play starts:

- **Skills:** 12 to 20, in the world's own words, covering the list in the kit template.
- **Weapons and armor:** the common ones, with sizes and tags (Core Rules §14).
- **Powers:** one entry per usable law in the World Bible. The cost and what goes wrong have to match what the user said the law costs.
- **Talents:** a starting handful that fit the world, plus the two the character takes.

## 4. The character (`Character Sheet.md`)

The character is the user's, in every part.

1. **Who they are.** Name, age, looks, concept, and the sections under the line on the sheet: who they are, what they want, voice, emotional rules, background and know-how, people. Ask for these in the user's own words and write them down as given. This is what you'll draw on for every thought the character has, so ask follow-ups where it's thin: how do they talk, what do they do when they're scared, what would they never do.
2. **The numbers** (Core Rules §15). Propose attributes, skills, and two talents that fit the person described, and let the user change anything. Then fill in the defenses, HP, and Strain.
3. **Gear and money.** What this person would own and carry, priced by the Economy.

## 5. Names (`World/Names.md`)

For each people the opening is likely to meet, build pools (given names, family names if the world uses them) of 30 or more each. Draw them from sources that fit: real names from the real languages and periods the user's world leans on, or names built on the patterns the user set. Leave out anything in `Writing/Banned Names.md` and anything that shares its first letters with a name already in the world. Show the pools to the user and strike whatever they dislike; a name they call generated-sounding goes in Banned Names.

## 6. Fill in behind the scenes

Now the part the user doesn't see. From what they gave you, and only as far as the opening needs:

- Give each cast member who's near the opening what the template asks for and the user left Open, tagged **[GM]**: what they want, what they know, where they are.
- Write stat lines for anyone likely to need one, and Bestiary entries for the world's common dangers.
- Turn what's in motion into pressures, with every field filled. Add ones the world implies (winter coming, a tax due) if they'd honestly touch the opening. Don't invent a villain to have one.
- Put what you decide about the world's hidden side in `GM Only/World Notes.md`.

Roll what's truly open with `gm fate` rather than choosing.

## 7. Where it starts

Ask the user where and when the narrative begins and what their character is doing there. Then write `GM Only/State/World State.md` for that moment: the clock, the character, the scene, anyone in motion, what's known and not known, the pressures near the page. Start `Journal.md` with what the character knows going in.

Set `"set_up": true` in `narrative.json`. Tell the user in braces that the world is ready, and that the next thing they write, outside braces, starts the narrative.

## 8. The opening

Follow Procedures/Play.md. The first beat sets the character down in the place and moment the user named, doing what the user said they're doing, and stops.
