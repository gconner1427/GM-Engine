# Play

How a narrative is run: starting a conversation, the beat, the end of a scene, and the end of a session.

A **session** is one sitting of play. It has one narrative log (`Sessions/Session N.md`, prose only, appended beat by beat) and one GM log (`GM Only/Logs/Session N GM Log.md`). A session stays open across conversations until the user ends it.

## Starting a conversation

1. Read, whole: the engine's `Rules/Core Rules.md`, `Writing/GM Philosophy.md`, `Writing/House Style.md`, and `Writing/Craft Rules.md`; then the narrative's `Style Guide.md`, `GM Only/World/Rules Kit.md`, `Character Sheet.md`, and `GM Only/State/World State.md`.
2. Run `gm status`.
3. Read the end of the latest session log (the last thousand words or so) for where things stopped and how the prose has been sounding, and the end of its GM log.
4. **Check that the state is current.** If the GM log has beats after World State's "State as of" line, the last conversation ended before the bookkeeping did: bring World State and the docs up to date from those beats' notes before anything else.
5. Load the docs for whoever and wherever the scene is (ENGINE.md, "What to load, and when").
6. If no session is open, don't open one yet: wait for the user's first action or `{new session}`. Then answer in one line in braces with where things stand as the character knows it: `{Session 4. Kendrick is at the mill, an hour before dark.}` No recap in prose.
7. **If the narrative's `CLAUDE.md` notes say the GM opens every session in the world,** don't wait: open the session and commit an opening beat that sets the character down where things stand, through their senses, with the world in motion, up to the first thing they'd answer. It never plays the character and never recaps.

## The beat

Every message from the user that isn't in braces is their character acting.

**1. Read it.** What did the user say the character does, says, and intends? That, exactly, is what the character does (GM Rules, "The player's character is the player's"). If it can't be done as stated, say so in braces and stop.

**2. Open a session if none is open:** `gm session start`.

**3. Load what the beat needs** that isn't already in the conversation: the cast doc for anyone it touches (read Changed by and Knows), the place, the item, Economy if money moves, Map & Travel if anyone travels, the Rules Kit entry for a power.

**4. Resolve it.**
- Work out what's uncertain. If nothing is, nothing is rolled.
- For each uncertain thing: set the bonus, the difficulty or defense, and Edge or Setback from the fiction, then roll with `gm`. Give every roll a "why" that names who and what; that line is the GM log's record.
- Decide what everyone else does in answer, from their docs and what they know. Roll for them the same way.
- Open questions about the world go through Core Rules §12.
- Keep going until the beat reaches its end (GM Rules, "Where a beat ends"). One user message is one beat, however many rolls it takes.
- Several `gm` commands can run in one call. Never roll something whose need depends on a roll you haven't seen.

**5. Write it,** to the writing rules, in the Style Guide's tense. Draw any new name with `gm name`.

**6. Commit it.** Write the staging file `GM Only/Logs/beat.md` with the Write tool:

```
<<< PLAYER
(the user's message, word for word)
<<< GM
(rulings: what was at stake, why each difficulty; what others did and why;
 every new fact this beat established: names, prices, layouts, what's now where, who now knows what)
<<< PROSE
(the beat)
```

Then `gm beat`. It appends the prose to the session log and files the rest, with the beat's rolls, in the GM log.

**7. Update the Character Sheet** in the same turn if anything on it changed: HP, Strain, shape, wounds, conditions, gear, money. The **Shape** line is words the user can read at a glance.

**8. Give the beat in the chat,** exactly as committed and nothing else, if `gm status` shows chat echo on. If it's off, reply only `{added}`: the user is reading the log.

Other bookkeeping can wait for the end of the scene. The GM notes can't: they're what the docs get rebuilt from if the conversation ends without warning.

## The end of a scene

A scene ends when the character leaves a place, when time jumps, or when what was happening is over. Before the next beat (or along with it, if the user's action is what ended the scene):

1. **Docs follow the page.** From the GM notes since the last update, write every new fact where it lives, tagged **[S#]**: cast docs (On the page, Now, Knows, Changed by for what will stick), places (Layout, Has, Now), Items, Economy prices, Map & Travel times, the Rules Kit's rulings. Someone new who'll matter gets an entry in Minor Cast, or a doc.
2. **World State.** Rewrite the clock, the character, the scene, people in motion, relationships, Secrets & Knowledge, items, loose ends. Set "State as of" to the session and beat.
3. **The World Turn** (Procedures/World Turn.md), at the size the scene calls for. Most scenes are a minute's thought and one or two lines.
4. Add a line to the sheet's **Changed by** only if the page plainly showed the character changed in a way that will last.

Do all of it in tool calls, without a word in the chat.

## The end of a session

When the user says `{end session}`:

1. Run the end of a scene, above.
2. **The World Turn**, in full, for the session as a whole.
3. **Marks** (Core Rules §16). Decide which of the four were true, add them to the sheet, and note why in the GM log (`gm note`). If the character reached a new level, work out what it gives.
4. **The Journal.** Bring `Journal.md` up to date with what the character now knows: where things stand, what they've learned about the world, people, places, unfinished business, and a paragraph for the session as the character would tell it. Nothing they don't know.
5. **Prune World State** back under its cap: move what the next scenes won't need into the docs' Now sections and the Archive.
6. `gm session end`.
7. Tell the user, in braces and briefly: the session is closed, the marks earned (the count, and the reasons only where the character would know them), and any choices a new level gives them. Apply their choices to the sheet when they answer.

If the user starts playing again without ending the session, it's the same session. If they open a new conversation and say `{new session}` with one still open, end the old one first.

## When things go wrong

- **The user says you misread them** (`{I meant the other door}`): `gm undo`, put back any state the beat changed, and run the beat again from the corrected action. The old rolls are void, since they were for something that didn't happen; anything the corrected action still calls for is rolled fresh.
- **The user dislikes how a beat reads:** that's a correction (Procedures/Corrections.md). The events and the rolls stand; only the writing changes.
- **You broke a rule of the game** (wrong bonus, a forgotten wound, someone acting on what they couldn't know): say so in braces, plainly, fix the page and the state, and note it in the GM log. Reroll only what the mistake made invalid.
- **You wrote the character doing something unstated:** `gm undo`, and write the beat again without it. If it's a pattern, it becomes a rule.
