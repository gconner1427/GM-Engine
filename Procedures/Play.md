# Play

How a narrative is run: starting a conversation, opening a session, the beat, the end of a scene, the end of a session, the end of the campaign, a new level, and a shop.

A **session** is one sitting of play. It has one narrative log (`Sessions/Session N.md`, prose only, appended beat by beat) and one GM log (`GM Only/Logs/Session N GM Log.md`). A session stays open across conversations until the user ends it.

## Starting a conversation

In the play window, steps 1 to 3 are done for you: the conversation's first message opens with everything they'd have you read, as it stands now. Don't read it again; start at step 4.

1. Read, whole: the engine's `Rules/Core Rules.md`, `Writing/GM Philosophy.md`, `Writing/House Style.md`, and `Writing/Craft Rules.md`; then the narrative's `Style Guide.md`, `GM Only/World/Rules Kit.md`, `Character Sheet.md`, `GM Only/State/Campaign.md`, and `GM Only/State/World State.md`.
2. Run `gm status`.
3. Read the end of the latest session log (the last thousand words or so) for where things stopped and how the prose has been sounding, and the end of its GM log.
4. **Check that the state is current.** If the GM log has beats after World State's "State as of" line, the last conversation ended before the bookkeeping did: bring World State and the docs up to date from those beats' notes before anything else.
5. Load the docs for whoever and wherever the scene is (ENGINE.md, "What to load, and when").
6. **If no session is open, what the user sends decides.**
   - **`{new session}`** opens one, and you go first: "Opening a session," below. In the play window this is the Begin button.
   - **Any other message in braces** never opens a session. Answer it (Procedures/Corrections.md) and leave things as they are: the user can talk with you between sessions for as long as they like.
   - **An action** (anything outside braces) means they want to play. Open the session and commit its opening beat first, as below. Then play their action as the next beat, in the same turn, if it still makes sense where the opening left things. If the opening put something in front of the character that the action doesn't answer, leave the action unplayed and say so in a line in braces after the opening: they'll want to act on what they've just read.

## Opening a session

You go first, every session. A GM at the table doesn't wait for the players to say what they're doing: they set the scene and put something in front of them. The opening is a beat of yours, committed before the player has acted, so they start the session with something to play off.

**1. Open it.** `gm session start` (if a session is still open, end it first: "The end of a session").

**2. Choose what the opening brings.** Something has to be happening that the character would answer. Choose it; don't invent it. Look, in this order, at:
- `Campaign.md`, "Threads" and "Where it stands": is the campaign due to cross their path? If the character has been away from it for a session or more, it usually is.
- What they were in the middle of when the last session ended: the next thing that would happen there.
- World State's People in motion (anyone whose **Next** has come), the Story Clock's Coming up, Loose ends, and Pressures near the page.
- What the last World Turn left on its way to them.

Take the one that gives them the most to do and would honestly reach them here and now. Every one of these is already true in the docs; the opening only decides which arrives first. If nothing would reach them yet, open on the place itself and the people in it, with someone there who wants something.

**3. Write it** as a beat, to the writing rules:
- **Set the scene.** Where the character is, the hour, the weather or the light, who's there, through their senses. A few lines: the player has been away, and this is what puts them back in the room.
- **Then the world moves.** What you chose in step 2 happens, on the page.
- **End on it** (GM Rules, "Where a beat ends"): at the first thing the character would answer. A question put to them, a knock, a rider coming in, a thing found, a face they know. Never with a question to the player or a list of what they could do.
- **It never plays the character.** They're where the last session left them, doing what they were doing. They decide nothing, say nothing new, and go nowhere. Their senses, reflexes, and inner life are yours as always.
- **It never recaps.** Nothing the log already holds is told again (Craft Rules, "No recaps of earlier beats"). The session log picks up where the last one stopped.
- **No time is skipped,** unless the player said in braces how the character spends it. The clock stands where the last session left it.
- **Keep it short.** A few paragraphs. The first session's is the exception.

**4. Commit it** like any beat, with no `<<< PLAYER` part. The GM notes say what the opening brought and which doc it came from. If the place already has a picture, `gm art place "<name>"` in the same call (Procedures/Art.md).

**5. Reply** as for any beat: the opening itself if chat echo is on, `{added}` if it's off.

**The first session** opens on the hook (`Campaign.md`, "The hook"; Procedures/New Narrative.md, step 6). It's longer than other openings, because it carries more: the place and the life the character has in it, as the player described them, and then the event that pulls them into the campaign. Give the ordinary moment enough room that it's worth something when the hook breaks it. End at the first thing they'd answer, with the first step in plain sight.

**A session after a death or a new character** (Core Rules §7) opens on the new character's hook the same way.

## The beat

Every message from the user that isn't in braces is their character acting.

**1. Read it.** What did the user say the character does, says, and intends? That, exactly, is what the character does (GM Rules, "The player's character is the player's"). If it can't be done as stated, say so in braces and stop. An action that ends in `{push}` is the character pushing (Core Rules §5): the first roll they make for it has Edge, and 2 Strain comes off the sheet. If that was their last 2, the roll still has its Edge, and they are spent from their next roll on. `{push}` is never part of what the character does or says. An action that ends in `{trade ...}` is a trade made on the shop screen ("A shop," below).

**2. If no session is open,** open one and commit its opening beat before this one ("Opening a session," above).

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

**Gear lines.** The play window builds its inventory from the sheet's gear lines (Wearing, Ready, Carried, In arms, Kept elsewhere), and it takes every comma, semicolon, and "and a/the/her..." outside parentheses as the start of a new thing. So one thing is one unbroken phrase, and everything said about it goes in parentheses straight after its name, where commas are safe. Never describe a thing with a colon and a run of comma'd clauses.
- ✗ `and, at the bottom, wrapped in a rag, her father's keepsake: a disc of black glass in a rim of green bronze, cold to the touch, with a faded stamp` (the window showed two things)
- ✓ `and her father's keepsake (a disc of black glass in a rim of green bronze, cold to the touch, with a faded stamp; wrapped in a rag at the bottom of the pack)`

Armor is written `(armor 1)`. After writing or changing a gear line, read it back as a list split at its commas: each piece should name one thing.

**What the character carries is counted** (Core Rules §14, "Carrying"), by the window and by `gm carry` from the same lines. So write them the way the count reads them:

- **The pack** is a thing on the Wearing line with its size: `a canvas pack (pack 8)`. What's in it is the Carried line, never "a pack holding ...". A character with no pack has `no pack (pack 0)` there. That mark is also what says a sheet is counted, so a counted sheet always has one.
- **A thing's size** goes in parentheses straight after its name, written when the thing comes to the character, and it holds: `(bulky)`, `(small)`, or `(armload)` for something too big for any pack. No mark is one slot. The mark stands alone in its parentheses or is set off by a comma (`(bulky, her mother's)`); inside a phrase it isn't read. Nothing is guessed from a name or a tag: a two-handed sword with no `(bulky)` counts 1. Armor keeps its mark while it's worn (`a mail shirt (armor 2, bulky)`), so it has its size the moment it comes off.
- **How many.** Things that get used up are a stack, written `×N` after the name (`rations ×7`), five to a slot. A count in front of the name (`two daggers`, `3 daggers`) is that many separate things, each at its own size: number words up to twelve, digits above that. A measure is one thing measured out (`fifty feet of rope`, `a quiver of twenty arrows`); several containers of a thing that gets used up are written `×N` (`flasks of oil ×7`, not `7 flasks of oil`). A bulky thing never stacks (`kegs ×2 (bulky)` is 4 slots), and `×N` of a small thing is N small things.
- **Coin.** The Money line counts every coin, and a purse's worth takes no room (Economy, "A purse holds"). Past that, each purse's worth more is a thing on a gear line, one slot, written by what holds it with the sum in parentheses: `a sack of coin (240 crowns)`. Never a number in front: `240 crowns` reads as 240 things.
- **In arms.** What's carried in the arms goes on a line of its own, `- **In arms:**`, between Carried and Kept elsewhere, and the line is deleted when the arms are empty. While anything is on it the character is laden: Conditions says so, Shape says it for the eye ("arms full"), and their running, climbing, swimming, sneaking, and fighting are rolled `--setback`.
- **Never write a total** ("7 of 9") on the sheet. Run `gm carry` after any turn in which a gear line changed: it prints the room used in each place, names any place that's over, and says when a two-handed thing has no size mark. When there's no room for something, it goes in their arms or stays where it is, and the page shows which. Only the player decides what their character drops, packs, or leaves behind: you never drop a thing for them to make room.
- **The pack set down.** Taking the pack off, dropping it, or swapping it is something the player types. Its contents stay in it: retitle the Carried line for the pack and where it lies, and leave what's on it as it is, marks and all (`- **In her pack, by the well:** a bedroll, a lantern, rations ×5`), and Wearing reads `no pack (pack 0)`. A line with a title of its own is shown and never counted. Putting the pack back on makes it the Carried line again. When seconds count, shrugging it off is part of whatever they do, and taking it up again is their action for the exchange.
- **Companions and porters** carry 4 slots Ready and a pack of 8 like anyone, and they're people: they can refuse, tire, be robbed, or walk off (Core Rules §11). Nobody's slots but the player character's are kept on a sheet.
- **On the page** it's never slots, "Ready," or "laden." A full pack is straps that won't buckle; an armload is a load shifted from arm to arm and breath that comes short; the pack in a fight is a knee on the ground and a back turned a breath too long.
- **A sheet with no `(pack N)` anywhere was made before this rule, and is left as it is.** Never add the mark to it, count it, or resize its things: that character carries what a person could carry, as the last paragraph of "Carrying" says.

**Gear moves from the window.** On a counted sheet the player can rearrange their gear in the window's Inventory. What they arranged comes to you as `{gear ...}` after their action, one move to a line: the thing as the sheet writes it, where it is, `to`, and where it goes (`a tin lantern: pack to ready`). The places are `worn`, `ready`, `pack`, `arms`, and `dropped`. Check it against the sheet and the limits, settle the gear lines in the same turn, and run `gm carry`. A dropped thing comes off the sheet and is in the world where it fell; the GM notes say where. Out of danger a move costs nothing and needs no prose of its own: the beat reads as it would have without it. Sent on its own (`I see to my gear. {gear ...}`), it gets a short beat: a few lines of the character doing it, with no numbers and nothing else moved forward. When seconds count, a move that takes a thing from the pack or puts one in is the character's whole action for the exchange; any other move is part of what they do. One such move sent on its own is their action: play it, and everyone else acts. If it came with another action, or there's more than one, play nothing: say in braces that reaching into the pack is all they can do this exchange, and stop, as for anything that can't be done as stated, and the player chooses which they want. In a Heroic narrative the first thing a character takes from their pack in each fight costs nothing: play it with whatever else they do, and write in the GM notes that this fight's is spent. Armor on or off takes minutes, so while seconds count it can't be done: say so in braces.

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
3. **The campaign.** Bring `Campaign.md`, "Where it stands" up to date: the stage, what the character now knows and has, the last time it was put in front of them and what they did, and how long they've been away from it. Add the threads the session made and strike those that are spent. If play has come near the next stage of the road, write that stage out in full. If the goal was reached, or lost for good, see "The end of the campaign."
4. **Marks** (Core Rules §16). Decide which of the four were true, add them to the sheet, and note why in the GM log (`gm note`). If the character reached a new level, see "A new level" below.
5. **The Journal.** Bring `Journal.md` up to date with what the character now knows: where things stand, the goal, what they've learned about the world, people, places, unfinished business, and a paragraph for the session as the character would tell it. Nothing they don't know.

    "The goal" is the campaign as the character understands it: what they're after, why it matters to them, and the next thing they know to do about it. A few lines, rewritten whenever what they know changes, including beliefs that are wrong. It's the one place the player can look to see what they're supposed to be doing, so it's never left stale. Side quests go under "Unfinished business," a line each: what was asked and by whom, and where it stands.

    The session's paragraph goes under "Sessions," headed `**Session N.**`, with the marks listed straight under it, one line for each mark earned. The play window builds its end-of-session card from these lines:

    ```
    **Session 3.** The paragraph, as the character would tell it.
    - **Mark: danger.** The fight at the ford.
    - **Mark: learned.** Who the ferryman answers to.
    ```

    The four are `danger` (came through real danger), `goal` (got something they were after, or lost it for good), `learned` (learned something that changes how things look), and `cost` (a choice or a failure cost them something real). After each, a few words on why, as the character would know it; leave the why off if they wouldn't know. A session that earned none gets the one line `- **Marks:** none.`
6. **Prune World State** back under its cap: move what the next scenes won't need into the docs' Now sections and the Archive.
7. `gm session end`.
8. Tell the user, in braces and briefly: the session is closed, the marks earned (the count, and the reasons only where the character would know them), and that there's a new level to choose for, if there is.

If the user starts playing again without ending the session, it's the same session. If they open a new conversation and say `{new session}` with one still open, end the old one first.

## The end of the campaign

A campaign ends when its goal is reached, or when it's lost for good (the opposition has what it wanted, or the thing the goal was for is gone). It ends on the page, in play, however it honestly came out. You never bring it about, hurry it, or hold it off.

1. Let the scene it happens in play to its end. Don't close the session yourself: the player may want the aftermath.
2. At the end of that session, as part of step 3: write how it ended under `Campaign.md`, "How it could end," tagged **[S#]**, delete or resolve the campaign's pressure, and let the full World Turn carry what the ending does to the world.
3. In your closing line, tell the user in braces that the campaign has ended, and ask which they want: to go on playing this character in the world as it now is, or to stop here.
4. **If they go on,** prepare the next campaign before the next session. It grows out of what the last one left: who gained by how it ended, what was set loose, what the character now has that someone wants. Rewrite `Campaign.md` (the old one's ending goes to the Timeline), give it a pressure, and write a hook for the character as they now are. The next session opens on that hook.

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
- **Lamp oil ×1:** 3 pence. A pint flask.

### Will buy
- **Wolf pelt:** 6 shillings ×2. "Good winter fur."
- **Short sword:** 18 shillings
```

- **Name** and **Keeper:** what the character knows them as. "A stall under a blue awning," "the woman with ink on her hands," until they learn better.
- **Coins:** every coin of the world's currency, each with what it's worth in the smallest one, from the Economy. The plural goes in parentheses when it isn't the name with an s. A currency written with a sign goes in as the sign (`- **$:** 1`), and its prices are written `$4.50`. The window does its sums with this list, so it has to be there even when there's only one coin.
- **For sale:** what the character can see on the shelves or has been told is to be had, one line each: the name, the price, `×` and how many there are, then a full stop and anything worth saying about it, in a line. Leave the count off only where there's plenty (bread, nails, lamp oil). Nothing kept under the counter is listed until the keeper brings it out. On a counted sheet ("Gear lines," above), a ware that's bulky, small, or too big to pack carries its mark straight after its name, inside the bold and before the colon (`- **Mail shirt (bulky):** 30 shillings ×1`); no mark is one slot. A pack for sale carries its size the same way (`- **Frame pack (pack 12):** 9 shillings ×1`). A ware that gets used up is written as a stack, `×N` at the end of its name for how many one purchase is (`- **Rations ×5:** 1 shilling`, `- **Lamp oil ×1:** 3 pence`); without it, several bought are that many separate things. The mark is written when the shop is opened and holds, and it's the mark the thing has on the sheet once bought. The `×` after the price is always how many the keeper has, never a stack.
- **Will buy:** each thing in the character's gear that this keeper would take, under the name it has on the sheet, with what they'd pay for one, and `×` how many the character has if it's more than one. What the keeper has no use for isn't listed. Leave the heading out if they buy nothing.
- **Prices** are the keeper's, set before the character asks (Core Rules §14, "Buying and selling"): an established price holds, and the rest come from the Economy, the keeper's nature, what they make of the character, and whatever is moving prices. Write a price as coins and nothing else (`1 crown, 4 shillings`), or the window can't add it up.
- Like everything on the sheet, the section holds only what the character knows.

**2. A trade** arrives as an action that ends in `{trade ...}`, listing what the character buys and sells, each price, and what it comes to. It's the character acting, so it's a beat:

- Check it against the section and the sheet: the stock, the prices, and their money. On a counted sheet, check the room too: what's bought goes in the pack (like things joining a stack already there), what the pack can't hold is carried out in their arms, and a trade that fits neither can't be done. If it can't be done as stated, say so in braces and stop.
- Nothing is rolled unless something is uncertain. A trade at the keeper's own prices isn't.
- Write it short: the goods and the coin change hands on the page in a few lines, with whatever the keeper says or does. The character buys and sells exactly what's listed and does nothing else. Per the Craft Rules, the payment is on the page and the number usually isn't.
- In the same turn, settle the sheet to the coin (the money, and each thing bought or sold in its gear line, with its mark; then `gm carry`) and the section (what's left of the stock, what the character still has to sell). A pack bought is worn in place of the old one only if the player said so or that's plainly why they bought it; the one not worn is a thing that takes its slot and gives no room. The prices paid go in the beat's GM notes, and from there to the Economy. The keeper's money and the shop's **Has** follow at the end of the scene.

**3. Everything else is played as it always is.** Haggling, asking for what isn't on the shelf, a favor, a theft: the user types it and it's a beat like any other (Core Rules §11). Whatever it changes, change in the section in the same turn: a price that came down, a thing brought out from the back, a keeper who won't sell to them now.

**4. Close it.** Delete the `## Shop` section in the turn the character leaves, the keeper stops dealing, or the scene turns into something else. A shop left open after the character has walked out is a mistake.

Without the window, the section is still written (the user can open the sheet to see what's for sale), and they buy and sell by saying so.

## When things go wrong

- **The user says you misread them** (`{I meant the other door}`): `gm undo`, put back any state the beat changed, and run the beat again from the corrected action. The old rolls are void, since they were for something that didn't happen; anything the corrected action still calls for is rolled fresh. If the misread action was pushed, the corrected one is too, unless the user says otherwise.
- **The user dislikes how a beat reads:** that's a correction (Procedures/Corrections.md). The events and the rolls stand; only the writing changes.
- **You broke a rule of the game** (wrong bonus, a forgotten wound, someone acting on what they couldn't know): say so in braces, plainly, fix the page and the state, and note it in the GM log. Reroll only what the mistake made invalid.
- **You wrote the character doing something unstated:** `gm undo`, and write the beat again without it. If it's a pattern, it becomes a rule.
