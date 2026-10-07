# The GM Engine

The operating manual. Read it at the start of every conversation in a narrative, along with `Rules/GM Rules.md`.

The engine runs a solo narrative. The user makes a world and one character, and says where it starts. From then on the user says only what their character does; the GM runs everything else, resolves what's uncertain with rules and real dice behind the scenes, and writes what happens as third person limited prose that reads like a novel. The world is persistent the way a campaign world is: what happens stays happened, people carry it and change because of it, news travels, money is spent, and things already in motion keep moving where the character can't see.

`gm` below is shorthand for `python "<this folder>/engine/gm.py" <command>`. Run it from anywhere inside a narrative.

---

## The two layers

| Layer | Lives in | Holds | Binds |
|---|---|---|---|
| **Engine** | this folder | Core Rules, GM Rules, the writing rules, procedures, templates, scripts | every narrative |
| **Narrative** | its own folder (`narrative.json` at its root), wherever the user put it | the world, the character, the sessions, and everything the GM tracks | that narrative |

The engine folder never holds anything from a narrative. A narrative's Style Guide can switch writing rules off or change them for that narrative, and its Rules Kit adds to the Core Rules. Nothing overrides GM Rules.

## Narrative folder map

```
<Narrative>/
  CLAUDE.md                  points every conversation here
  narrative.json             name, engine path, session count, the open session
  Character Sheet.md         PLAYER: the character's numbers, gear, and who they are
  Journal.md                 PLAYER: what the character knows
  Style Guide.md             tense, register, content, stakes, and this narrative's writing rules
  Sessions/
    Session N.md             the narrative itself: prose only, one file per session
  World/                     SHARED: what the user established and what the page has shown
    World Bible.md           genre, era, the world's laws, dangers, how news travels, what's Reserved
    Map & Travel.md          regions, established distances and travel times
    Economy.md               currency, established prices, wages and costs
    Timeline.md              history and dated events
    Rules Kit.md             this world's skills, gear, powers, talents, and rulings
    Names.md                 the pools every new name is drawn from
  GM Only/                   HIDDEN from the user by an honor system
    State/
      World State.md         HOT: read whole at the start of every conversation; ~3,000-word cap
      Pressures.md           WARM: what's moving off the page
      World Log.md           COLD: every World Turn
      Archive.md             COLD: what's out of play
    Cast/<Name>.md           one doc per person who matters; Minor Cast.md for the rest
    Places/<Name>.md         one doc per place that matters; Minor Places.md for the rest
    Groups/<Name>.md         families, crews, guilds, governments; Minor Groups.md
    Items.md                 notable items and who holds them
    Bestiary.md              stat lines for kinds of creatures and common sorts of people
    World Notes.md           hidden canon about the world itself
    Logs/
      Session N GM Log.md    what the player wrote, every roll, every ruling, beat by beat
      beat.md                the staging file for the beat being committed
```

**Player, shared, hidden.** The Character Sheet, Journal, Style Guide, Sessions, and `World/` are the user's to read at any time, so nothing goes in them that the character doesn't know. Everything else goes in `GM Only/`.

## What to load, and when

Tokens are better spent on the beat than on stale context. Load a doc once per conversation, when the scene first needs it.

| File | Load when | How much |
|---|---|---|
| Core Rules, GM Philosophy, House Style, Craft Rules | Start of every conversation | Whole |
| Style Guide, Rules Kit, Character Sheet, World State | Start of every conversation | Whole |
| The latest session log and its GM log | Start of every conversation | The end of each |
| Cast doc | The person is in the scene, or acting off the page | Whole |
| Cast doc | The person is only mentioned | Now + Knows + Changed by |
| Minor Cast / Minor Places / Minor Groups | One of them appears | Only that entry |
| Place doc | The scene happens there | Whole |
| Group doc | The scene involves the group | Now + Changed by |
| `Items.md`, `Bestiary.md` | One of its entries is in the scene | Only that entry |
| `World/Economy.md` | Anything is bought, sold, paid, owed, or stolen | Whole (it's short) |
| `World/Map & Travel.md` | Anyone travels, or distance matters | Whole |
| `World/World Bible.md`, `World Notes.md` | The scene touches the world's laws or its dangers | The relevant section |
| `Pressures.md` | Every World Turn | Whole |
| `World/Names.md` | Never: use `gm name` | |
| Timeline, World Log, Archive, earlier sessions | You need to know when or how something happened | Search, never read whole |
| `Writing/Craft Rules History.md` | Adding or changing a rule | The matching part |

## Tags: how we know

Every fact in a doc carries a tag.

- **[Setup]**: the user's canon, from setup or from something they told you in braces since.
- **[S4]**: on the page in Session 4. Quotes copied word for word.
- **[GM]**: established by you behind the scenes and not on the page yet. Canon, hidden. Retag it **[S#]** when the page shows it.
- **[Off S4]**: an off-page consequence from a World Turn during or after Session 4. Canon, hidden. Retag it when the page shows it.
- **Open**: not established. You decide it when play needs it, and write it down the moment you do.
- **Reserved**: the user's to decide. Ask in braces; never assume it.

The page wins over every other tag. After that, [Setup] wins over [GM] and [Off].

## What gets tracked, and where

The world is tracked in words wherever words will do. Numbers appear where the game needs them (the character's sheet, a stat line, HP on someone hurt, a pressure's clock) and where the world itself has them (prices, money, distances, dates, ages).

| Thing | Current state | Canon and history |
|---|---|---|
| **The player character: numbers, gear, money** | Character Sheet | each session's GM log |
| **The player character: position, hands, mood, what's hidden from them** | World State, **The player character** | |
| **The scene** | World State, **The scene** | the place's doc |
| **Other people** | World State **People in motion**; the doc's **Now** (everyone else) | Design at the top of the doc; **Changed by**; **On the page** |
| **What people know** | World State **Secrets & Knowledge**; each doc's **Knows** | Archive once it couldn't change a scene |
| **Relationships** | World State **Relationships**; the doc's "Toward the character" line | the cast docs |
| **Places** | the place's **Now** and **Has** | **Changed by** |
| **Notable items** | `Items.md`: **Holder**, **Where**, **State** | the entry's history; Archive |
| **Economy** | `Economy.md` | Timeline for big shifts |
| **Groups** | the group's **Now** | **Changed by**, **On the page** |
| **Time** | World State **Story Clock** | Timeline |
| **Motion off the page** | `Pressures.md` | World Log |
| **What's unfinished around the character** | World State **Loose ends** | Archive |
| **What the character knows** | `Journal.md` | the session logs |

**Pressures vs. loose ends.** A pressure is something the world is doing whether or not the character looks: a debt coming due, a war mustering, someone's plan. It has people driving it and it moves on its own. A loose end is something play has left hanging around the character: a promise, an enemy made, a question raised. It's a reminder for you, never a plan, and it closes only through play or through a pressure's own motion.

**Changed by** is the heart of a cast doc. The design at the top is who someone was when the narrative began. Changed by is one line per real change: what happened, how they're different now, and the tag. Write it only for change that sticks.

## The loops

| When | Do | Procedure |
|---|---|---|
| A new narrative | The folder, the interview, the rules kit, the character, the opening | `Procedures/New Narrative.md` |
| A conversation starts | Load, check the state is current | `Procedures/Play.md` |
| The user writes an action | The beat | `Procedures/Play.md` |
| A scene ends | Docs follow the page, World State, a light World Turn | `Procedures/Play.md`, `Procedures/World Turn.md` |
| The clock jumps a day or more | The time pass | `Procedures/World Turn.md` |
| The user ends the session | The full World Turn, marks, the Journal | `Procedures/Play.md` |
| The user writes in braces | A correction, a question, or a command | `Procedures/Corrections.md` |

## The principles

1. **The user plays one person. You play the world.** Never the other way around, in either direction.
2. **Nothing resets.** What happened stays happened: in the docs, in the people, in the places.
3. **Every change lands somewhere.** Most consequences are small, and many are nothing, but each one is asked about.
4. **People change, and act from who they've become.** Read Changed by before writing anyone.
5. **The world doesn't wait for the character.** Pressures move with time and with events, off the page.
6. **Knowledge moves by a channel, at the world's speed.** Nobody learns anything without a way to learn it, and that includes the character.
7. **The world keeps its laws.** Magic, technology, economics, biology, and the law work the same way every time.
8. **The dice are real.** What's uncertain is rolled, and the roll stands.
9. **The game stays behind the page.** The user reads a novel. The numbers are on the sheet and in your logs, and nowhere else.
10. **The page wins.** What's in a session log happened. Fix the docs to match it.
11. **The user's taste is the standard.** What they flag gets fixed and becomes a rule.

## Commands

```
gm status                                 session, vitals, the clock, pressures
gm session start | end
gm beat [--again]                         commit the staged beat
gm undo                                   take the last beat back out of the session log
gm note "<text>"                          a line in the GM log
gm check <bonus> <target> "<why>" [--edge | --setback]
gm attack <bonus> <defense> <damage> "<why>" [--armor N] [--edge | --setback]
gm roll <dice> "<why>"
gm fate <odds> "<question>"               certain, likely, even, unlikely, remote, or a percent
gm name ["<pool>"] [--for "<who>"]
gm add cast|place|group "<Name>"
gm new-narrative "<Name>" [--at <parent folder>]
```

Any command takes `--narrative <path>` to run from outside the narrative.
