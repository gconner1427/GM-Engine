# Play

How a narrative is run: starting a conversation, the beat, the end of a scene, the end of a session, a new level, and a shop.

A **session** is one sitting of play. It has one narrative log (`Sessions/Session N.md`, prose only, appended beat by beat) and one GM log (`GM Only/Logs/Session N GM Log.md`). A session stays open across conversations until the user ends it.

## Starting a conversation

1. Read, whole: the engine's `Rules/Core Rules.md`, `Writing/GM Philosophy.md`, `Writing/House Style.md`, and `Writing/Craft Rules.md`; then the narrative's `Style Guide.md`, `GM Only/World/Rules Kit.md`, `Character Sheet.md`, and `GM Only/State/World State.md`.
2. Run `gm status`.
3. Read the end of the latest session log (the last thousand words or so) for where things stopped and how the prose has been sounding, and the end of its GM log.
4. **Check that the state is current.** If the GM log has beats after World State's "State as of" line, the last conversation ended before the bookkeeping did: bring World State and the docs up to date from those beats' notes before anything else.
5. Load the docs for whoever and wherever the scene is (ENGINE.md, "What to load, and when").
6. **If no session is open, what the user sends decides.**
   - **An action** (anything outside braces) starts the next session by itself: open it and play the action as a beat, straight away. The user never has to ask for a session first, and you don't answer with a line about where things stand in place of the beat.
   - **A message in braces** never opens a session. Answer it (Procedures/Corrections.md) and leave things as they are: the user can talk with you between sessions for as long as they like. The one exception is `{new session}` itself, which opens one; answer that in one line in braces with where things stand as the character knows it: `{Session 4. Kendrick is at the mill, an hour before dark.}` No recap in prose.
7. **If the narrative's `CLAUDE.md` notes say the GM opens every session in the world,** don't wait: open the session and commit an opening beat that sets the character down where things stand, through their senses, with the world in motion, up to the first thing they'd answer. It never plays the character and never recaps.

## The beat

Every message from the user that isn't in braces is their character acting.

**1. Read it.** What did the user say the character does, says, and intends? That, exactly, is what the character does (GM Rules, "The player's character is the player's"). If it can't be done as stated, say so in braces and stop. An action that ends in `{push}` is the character pushing (Core Rules §5): the first roll they make for it has Edge, and 2 Strain comes off the sheet. `{push}` is never part of what the character does or says. An action that ends in `{trade ...}` is a trade made on the shop screen ("A shop," below).

**2. Open a session if none is open:** `gm session start`. An action is all it takes to begin one.

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

**6a. Ask for a picture, only if the beat was a major moment** (Procedures/Art.md): the first sight of a town, a castle, or somewhere else that matters; a new person with a part to play; an object or a mystery found. `gm art ...` in the same call as `gm beat`. Most beats ask for nothing.

**7. Update the Character Sheet** in the same turn if anything on it changed: HP, Strain, shape, wounds, conditions, gear, money. The **Shape** line is words the user can read at a glance. If the beat took the character into a shop or out of one, open or close it ("A shop," below).

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
3. **Marks** (Core Rules §16). Decide which of the four were true, add them to the sheet, and note why in the GM log (`gm note`). If the character reached a new level, see "A new level" below.
4. **The Journal.** Bring `Journal.md` up to date with what the character now knows: where things stand, what they've learned about the world, people, places, unfinished business, and a paragraph for the session as the character would tell it. Nothing they don't know.

    The session's paragraph goes under "Sessions," headed `**Session N.**`, with the marks listed straight under it, one line for each mark earned. The play window builds its end-of-session card from these lines:

    ```
    **Session 3.** The paragraph, as the character would tell it.
    - **Mark: danger.** The fight at the ford.
    - **Mark: learned.** Who the ferryman answers to.
    ```

    The four are `danger` (came through real danger), `goal` (got something they were after, or lost it for good), `learned` (learned something that changes how things look), and `cost` (a choice or a failure cost them something real). After each, a few words on why, as the character would know it; leave the why off if they wouldn't know. A session that earned none gets the one line `- **Marks:** none.`
5. **Prune World State** back under its cap: move what the next scenes won't need into the docs' Now sections and the Archive.
6. `gm session end`.
7. Tell the user, in braces and briefly: the session is closed, the marks earned (the count, and the reasons only where the character would know them), and that there's a new level to choose for, if there is.

If the user starts playing again without ending the session, it's the same session. If they open a new conversation and say `{new session}` with one still open, end the old one first.

## A new level

When the marks reach what the next level takes (Core Rules §16):

1. On the sheet, raise **Level**, raise HP and Strain by their formulas, and reset **Marks** to what's left over, out of what the level after takes.
2. Write what the level leaves the user to choose as a section of the sheet, directly above `## Vitals`. The play window builds its level-up screen from this section, and works out the rest (3 skill ranks, the cap on a skill, an attribute at levels 3, 6, and 9) from the level:

    ```
    ## Level up

    **Reached:** Level 4

    ### New skills
    - **Sailing:** three days working the ferry

    ### Talents
    - **Sea Legs:** Edge on keeping her feet aboard anything afloat.
    ```

    - **New skills:** the skills the character doesn't have that they could start now, each with its source in what they've been doing. Leave the heading out if there are none. Skills they already have aren't listed: the screen reads those from the sheet.
    - **Talents:** at an even level only. Three or four that fit who the character has become, from the Rules Kit or written for them in the shapes of Core Rules §17, each in words the user can read with nothing they don't already know.
    - Like everything on the sheet, the section holds only what the character knows.
3. The user's choices come back in braces, from the screen or in their own words. Check them against the rules, apply them to the sheet (ranks, the talent, the attribute and any defense, HP, or Strain it changes), and delete the `## Level up` section. If a choice can't stand, or they've asked for a skill or talent that wasn't listed, settle it with them in braces and leave the section until it's settled.

Without the window, put the same choices to the user in braces.

## A shop

When the character is somewhere that sells (a shop, a stall, a peddler's cart, a quartermaster's window) and whoever keeps it is ready to deal, the play window gives the user a shop screen: what's for sale and for how much, what the keeper would buy from them, and their money. The user fills a basket and makes the trade, and it comes to you as one action.

**1. Open it.** In the same turn as the beat that brings the character in, write the shop as a section of the sheet, directly above `## Vitals`. The play window builds its shop screen from this section:

```
## Shop

**Name:** Harrow's Chandlery
**Keeper:** Old Harrow

### Coins
- **crown:** 240
- **shilling:** 12
- **penny (pence):** 1

### For sale
- **Tin lantern:** 4 shillings ×1. Horn pane, a little dented.
- **Rope, fifty feet:** 2 shillings, 6 pence ×3
- **Lamp oil, a pint:** 3 pence

### Will buy
- **Wolf pelt:** 6 shillings ×2. "Good winter fur."
- **Short sword:** 18 shillings
```

- **Name** and **Keeper:** what the character knows them as. "A stall under a blue awning," "the woman with ink on her hands," until they learn better.
- **Coins:** every coin of the world's currency, each with what it's worth in the smallest one, from the Economy. The plural goes in parentheses when it isn't the name with an s. A currency written with a sign goes in as the sign (`- **$:** 1`), and its prices are written `$4.50`. The window does its sums with this list, so it has to be there even when there's only one coin.
- **For sale:** what the character can see on the shelves or has been told is to be had, one line each: the name, the price, `×` and how many there are, then a full stop and anything worth saying about it, in a line. Leave the count off only where there's plenty (bread, nails, lamp oil). Nothing kept under the counter is listed until the keeper brings it out.
- **Will buy:** each thing in the character's gear that this keeper would take, under the name it has on the sheet, with what they'd pay for one, and `×` how many the character has if it's more than one. What the keeper has no use for isn't listed. Leave the heading out if they buy nothing.
- **Prices** are the keeper's, set before the character asks (Core Rules §14, "Buying and selling"): an established price holds, and the rest come from the Economy, the keeper's nature, what they make of the character, and whatever is moving prices. Write a price as coins and nothing else (`1 crown, 4 shillings`), or the window can't add it up.
- Like everything on the sheet, the section holds only what the character knows.

**2. A trade** arrives as an action that ends in `{trade ...}`, listing what the character buys and sells, each price, and what it comes to. It's the character acting, so it's a beat:

- Check it against the section and the sheet: the stock, the prices, and their money. If it can't be done as stated, say so in braces and stop.
- Nothing is rolled unless something is uncertain. A trade at the keeper's own prices isn't.
- Write it short: the goods and the coin change hands on the page in a few lines, with whatever the keeper says or does. The character buys and sells exactly what's listed and does nothing else. Per the Craft Rules, the payment is on the page and the number usually isn't.
- In the same turn, settle the sheet to the coin (the money, and each thing bought or sold in its gear line) and the section (what's left of the stock, what the character still has to sell). The prices paid go in the beat's GM notes, and from there to the Economy. The keeper's money and the shop's **Has** follow at the end of the scene.

**3. Everything else is played as it always is.** Haggling, asking for what isn't on the shelf, a favor, a theft: the user types it and it's a beat like any other (Core Rules §11). Whatever it changes, change in the section in the same turn: a price that came down, a thing brought out from the back, a keeper who won't sell to them now.

**4. Close it.** Delete the `## Shop` section in the turn the character leaves, the keeper stops dealing, or the scene turns into something else. A shop left open after the character has walked out is a mistake.

Without the window, the section is still written (the user can open the sheet to see what's for sale), and they buy and sell by saying so.

## When things go wrong

- **The user says you misread them** (`{I meant the other door}`): `gm undo`, put back any state the beat changed, and run the beat again from the corrected action. The old rolls are void, since they were for something that didn't happen; anything the corrected action still calls for is rolled fresh. If the misread action was pushed, the corrected one is too, unless the user says otherwise.
- **The user dislikes how a beat reads:** that's a correction (Procedures/Corrections.md). The events and the rolls stand; only the writing changes.
- **You broke a rule of the game** (wrong bonus, a forgotten wound, someone acting on what they couldn't know): say so in braces, plainly, fix the page and the state, and note it in the GM log. Reroll only what the mistake made invalid.
- **You wrote the character doing something unstated:** `gm undo`, and write the beat again without it. If it's a pattern, it becomes a rule.
