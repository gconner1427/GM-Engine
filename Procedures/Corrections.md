# Braces: Corrections, Questions, Commands

Anything the user writes in `{braces}` is the user talking to you, not their character acting. Answer in braces, briefly. Nothing said in braces, by either of you, goes in the session log.

A message can hold both: an action, and a note in braces. Handle the braces first.

## Corrections to the writing

The user will flag anything that reads wrong to them: a line of dialogue that sounds stiff or written, prose that's too flowery, a name that sounds generated, a tic. This is how the engine gets better. Every correction does two things: it fixes the passage, and it leaves a rule behind so the same thing isn't written again.

**1. Find the passage.** If the note doesn't say which, it's about the last beat. If it could be two things, ask.

**2. Understand what's wrong with it,** in the user's terms. Take the note at its word: "too flowery" means plainer, not differently ornate. If you can't tell what they want instead, ask one short question before rewriting.

**3. Rewrite only that part.** What happened doesn't change: the events, the outcomes, and the rolls stand, and so does everything the user didn't flag. Replace the passage in the session log with the Edit tool. If the fix makes a neighboring line wrong (a pronoun, a repeated word), fix that too and nothing else.

**4. Take the rule from it.** Name the pattern in a line: the general thing this passage did that the user doesn't want.
- Search `Writing/Craft Rules.md` and the narrative's Style Guide first. If a rule already covers it, the rule wasn't enough: sharpen it and add this passage as an example. Check `Craft Rules History.md` for whether it has come up before.
- If nothing covers it, write a new rule in the house format: the rule in bold, what it means, its exceptions if the user's note implies any, and the example (✗ what was written → ✓ what replaced it).
- **Where it goes.** A rule that would hold in any narrative goes in the engine's `Writing/Craft Rules.md`, in the section it fits. A rule that names a character or depends on this world, era, or cast goes in this narrative's `Style Guide.md`, "Rules for this narrative." If you can't tell, ask.
- Record why in `Writing/Craft Rules History.md`, under Corrections, with the user's words.
- Keep the rule as wide as the note and no wider. One stiff line from one character is a note about how that person talks (their cast doc's Voice), not a law about all dialogue, unless the user says it is.
- Skip the rule only for a plain slip that an existing rule already forbids clearly (a continuity error, a typo). Fix it and move on.

**5. Sweep the session.** Search the open session's log for the same pattern and fix what you find. Leave earlier sessions alone unless the user asks.

**6. Answer in braces:** the rewritten passage, then one line naming the rule and where it went.

```
{Rewritten:

"You'll want the south road," she said. "The other one floods."

Rule added (house, Dialogue): people giving directions say what they'd say, in the order they'd think of it.}
```

The user can change or strike the rule in reply. Their wording wins.

### A name the user rejects

1. Add it to `Writing/Banned Names.md` if they said it sounds generated. If it just doesn't suit this person, don't.
2. Draw a new one (`gm name`), or use the one the user gives.
3. Change it everywhere: every session log, the Journal, the Character Sheet, World State, the cast doc (rename the file), every doc that mentions them, and `World/Names.md`. Search the whole narrative folder for the old name afterward to be sure.
4. If the user says what was wrong with it (too soft, too many vowels, sounds like every fantasy name), put that in the Style Guide's rules or the World Bible's Naming, and strike the names in the pools that share the fault.

## Corrections to the game

- **"I meant something else."** You misread the action: Procedures/Play.md, "When things go wrong."
- **"He wouldn't have done that."** About their own character: they're right, always. Undo, and write it without the thing. It becomes a line in the sheet's Emotional rules or Voice so it doesn't happen again.
- **"She wouldn't have done that."** About anyone else: check the doc. If you wrote someone against their doc or their knowledge, say so and fix it. If the doc supports it, say that there's a reason the character doesn't know, and no more.
- **"That's not how this world works."** The user made the world. Fix the World Bible or Rules Kit, tagged [Setup], and then the page.
- **A rules dispute** (the outcome seems wrong): check the GM log. If you made a mistake, own it and fix it. If the roll was honest, it stands. Tell them the outcome was rolled fairly; give the numbers only if they ask for them.

## Questions

Answer from what the character knows and can perceive: the Journal, the sheet, what the page has shown. If the honest answer is in `GM Only/`, the answer is that the character doesn't know.

- What does my character see, have, know, remember about someone: answer plainly. Looking around is free when nothing is hiding; if something is, they see what a glance would catch, and searching is an action.
- How the rules work: answer plainly, from Core Rules and the Rules Kit. The user is allowed to understand the game.
- How hard something would be: what the character could judge by looking, in words ("a hard climb for him, worse in the rain"), never a number.

## Commands

| The user says | Do |
|---|---|
| `{new session}` | End the open session if there is one, then `gm session start`. |
| `{end session}` | Procedures/Play.md, "The end of a session." |
| `{sheet}` | Show the Character Sheet's top half (through Gear), as it stands. |
| `{journal}` | Bring `Journal.md` up to date now and say it's done. |
| `{recap}` | A few lines on where things stand, from what the character knows. |
| `{undo}` | `gm undo`, restore the state the beat changed, and say so. |
| `{echo off}` / `{echo on}` | Set `chat_echo` in `narrative.json`. Off means beats go only to the session log. |
| a change to the world, the sheet, or the Style Guide | Make it. Their word is canon. If it contradicts the page, ask which gives. |
