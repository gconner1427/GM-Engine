# Core Rules

The game underneath the prose. It's the same in every world: fantasy, science fiction, the present day, after the end. Each narrative's `Rules Kit.md` names what that world puts on top (its skills, gear, powers, and talents).

The rules exist to keep the world honest. They decide what happens when it's truly uncertain, so the outcome comes from the character's ability, the difficulty, and chance, never from what would make the better scene. None of it reaches the page: the user sees numbers only on the Character Sheet.

`gm` below is `python "<engine>/engine/gm.py"`. Every roll is made with it. Never invent a result.

---

## 1. Attributes

Six, the same for everyone. Each is a number added to rolls: 0 is an ordinary adult, +2 is notably good, +4 is the best most people ever meet, +5 is the limit for a person. Below 0 is a real weakness.

| Attribute | Covers |
|---|---|
| **Might** | strength, force, lifting, hitting hard |
| **Agility** | speed, balance, aim, quiet feet, quick hands |
| **Vigor** | health, stamina, shrugging off pain, poison, and cold |
| **Wits** | reasoning, memory, noticing, working things out |
| **Will** | nerve, focus, patience, holding out |
| **Presence** | force of personality, reading people, being believed |

## 2. Skills

Trained ability, ranked 0 to 5: 0 untrained, 1 familiar, 2 trained, 3 skilled, 4 expert, 5 master. The list is the world's (Rules Kit). A skill isn't tied to one attribute: pair it with whichever attribute fits how the thing is being done (climbing a wall by strength is Might, by nimbleness Agility).

## 3. The roll

Roll only when both are true: the outcome is uncertain, and each way it could go would matter. Otherwise it just happens the way this person's ability says it would: a locksmith opens an ordinary lock, and nobody talks a guard into treason with one sentence.

**d20 + attribute + skill** against a **Difficulty**. Set the Difficulty before rolling, from the fiction alone.

| Difficulty | | Meaning |
|---|---|---|
| Simple | 8 | most people manage it |
| Moderate | 12 | takes training or luck |
| Hard | 15 | a trained person often fails |
| Severe | 18 | an expert's work |
| Extreme | 22 | the best in the land might |
| Legendary | 26 | people will tell stories |

**Five outcomes**, by how far the total lands from the Difficulty:

| Outcome | Margin | What it means |
|---|---|---|
| **Critical** | 10 or more over | It works, and better than hoped: faster, cleaner, with something extra. |
| **Success** | met or beaten | It works. |
| **Partial** | 1 to 4 under | It works with a cost, or only part of it works. Pick whichever the moment makes true: a price paid, a complication, a lesser result, a harder position. |
| **Failure** | 5 to 9 under | It doesn't work, and the situation moves on because of it. |
| **Disaster** | 10 or more under | It doesn't work, and the worst reasonable thing that was at risk happens. |

A natural 20 moves the outcome one step up. A natural 1 moves it one step down.

**Edge and Setback.** When circumstances clearly help (high ground, the right tool, a friend's help, a foe who can't see), roll with Edge: two d20, keep the higher. When they clearly hurt (wounded, rushed, the wrong tool, darkness), roll with Setback: keep the lower. One of each cancels. Don't stack small bonuses; Edge and Setback are the whole of it.

**No repeats.** A roll stands for the whole attempt. Trying again needs something to have changed: a new approach, a new tool, more time, help.

**The cost of failing fits the stakes.** A Disaster while picking a lock in an empty house is a broken pick. A Disaster on a ledge is a fall.

`gm check <bonus> <difficulty> "<who and what>" [--edge | --setback]`

## 4. Defenses

When someone acts against someone else, the one acting rolls against the other's defense. A defense is 10 plus what protects them.

| Defense | Is | Against |
|---|---|---|
| **Guard** | 10 + Agility + half their rank in a close-fighting skill (rounded down) | blows, shots, grabs. A shield or good cover adds 1 or 2. Someone unaware or helpless has Guard 8. |
| **Toughness** | 10 + Vigor | poison, sickness, cold, exhaustion, being knocked flat |
| **Resolve** | 10 + Will | fear, pressure, torment, powers that reach the mind |
| **Notice** | 10 + Wits + rank in the world's noticing skill | someone sneaking, lying, hiding something |

When two people are trying to do the same thing at once (a race, a grab for the same knife), both roll and the better outcome wins; on the same outcome, the higher total.

## 5. Health

**HP** is how much punishment a person can take before they go down: 8 + twice Vigor + 4 per level.

**Strain** is what they have left to give: 4 + twice Will + their level. It pays for powers (Rules Kit), it's what fear and horror take away, and it can be spent to push: 2 Strain for Edge on one roll, said before the roll, when the character would truly be giving it everything. The player says when their character pushes, with `{push}` after the action (the play window's Push switch adds it); you never push for them. The Edge goes on the first roll the character makes for that action. If the action needs no roll, or they have less than 2 Strain, nothing is spent. At 0 Strain a person is spent, and has Setback on everything until they rest.

**Wounds.** A single blow that takes half a person's full HP or more also leaves a wound: a named injury (a cracked rib, a gash down the forearm, a concussion) that gives Setback on whatever it would hamper and heals on its own time, whatever their HP says. Light wounds take days, serious ones weeks, grievous ones months or never.

**Conditions.** Anything else wrong with someone is a condition in plain words (winded, blinded, poisoned, bound, drunk, terrified). It gives Setback on what it would hamper, or rules an action out, and ends when the fiction says it would.

**What the numbers look like on the page:**

| HP left | The person is |
|---|---|
| more than three quarters | fresh, or scuffed: nothing that slows them |
| half to three quarters | hurt: bruised, bleeding a little, breathing hard |
| a quarter to half | bloodied: real injuries, favoring something, slowing |
| under a quarter | in bad shape: barely standing, one more good hit from down |
| 0 | down |

## 6. Fights and other danger

There are no turns and no grid. A fight moves in **exchanges**: the player says what their character does, that action is resolved, and then everyone else who can act does one thing each. What they do comes from who they are and what they want (press, flank, grab the bag, run, beg), not from what would be the hardest fight.

- **Who goes first.** Whoever starts it, or whoever has the drop. Someone taken by surprise loses their first action and has Guard 8 until they've acted. If nobody has the drop, the player character's action resolves first.
- **Attacking.** Roll a fighting skill against Guard. On a hit, roll damage and take off the target's armor.
    - **Success:** full damage, at least 1.
    - **Partial:** half damage, and armor may turn it entirely. Or full damage at a cost (off balance, weapon stuck, ground lost) when the moment makes that truer.
    - **Critical:** add the most the damage dice could show, on top of the roll. The attacker also gets something extra: the foe disarmed, knocked down, driven back.
    - **Failure:** a miss.
    - **Disaster:** a miss that leaves the attacker badly placed: open to the next blow (Guard 8 against it), weapon dropped, footing lost.
- **Doing anything else.** Everything that isn't an attack is an ordinary roll: shoving someone off a bridge is Might against their Guard or Toughness, scaring off a wolf is Presence against its Resolve.
- **Nerve.** Almost nothing fights to the death. When a side loses its leader, loses half its number, or sees it can't win, each of them does what they'd do: most break, some yield, a few go berserk. When it isn't obvious, roll their bonus against a Difficulty set by how bad it looks.
- **Mobs.** A pack of lesser foes acting as one can be run as one creature a tier higher, with their HP added together. It loses members as it loses HP.
- **Scale.** Some things are simply bigger than a person: a warship, a dragon, a tank. Hand weapons do nothing to them unless the fiction says how, and what they do to a person isn't rolled as an ordinary blow; it's a danger to get out of the way of (a roll against a Difficulty, with harm on anything short of Success).

`gm attack <bonus> <Guard> <damage> "<who and what>" [--armor N] [--edge | --setback]` rolls the attack and the damage together.

**Other harm.** Falls, fire, drowning, and the like: d6 for something that hurts, 2d6 for something that maims, 4d6 for something that kills, more for the plainly unsurvivable.

## 7. Down and dying

At 0 HP a person is down. For most of the world's people that's the end of them as the fiction says: dead, dying, out cold, or done fighting.

When the player character goes down, roll Vigor against Difficulty 12 (`gm check`). The narrative's Style Guide sets the stakes:

| Outcome | Deadly | Heroic |
|---|---|---|
| Critical | Still up, at 1 HP. | Still up, at 1 HP. |
| Success | Out, and stable. They wake within the hour at 1 HP. | Out, and stable. They wake within the hour at 1 HP. |
| Partial | Out, with a serious wound. | Out, with a light wound. |
| Failure | Dying. Dead in minutes unless someone tends them (Difficulty 12 with a healing skill, or anything the world's healing can do). | Out for hours, with a serious wound. |
| Disaster | Dead. | Out for hours, with a grievous wound, and something lost. |

Whatever the roll, the world then does what it would with a helpless person: enemies who want them dead finish it (in a Deadly narrative), captors bind them, thieves rob them, the cold keeps working, friends drag them out. In a Heroic narrative the world stops short of killing them unless the player knowingly chooses a death.

If the player character dies, the narrative says so plainly and the session ends. The world goes on: the user can bring a new character into it.

## 8. Rest and healing

- **A breather** (an hour, with food or water and a chance to bind things up): recover HP equal to level + Vigor (at least 1) and 2 Strain. Once between sleeps.
- **A night's sleep:** recover half of full HP, and all Strain.
- **A full day of real rest:** all HP.
- **Tending:** a healing skill against Difficulty 12 doubles what a breather gives, and is what stops someone dying. A world's medicine or magic can do more (Rules Kit, "Healing").
- **Wounds** heal on their own time, and faster only by the world's means. A night in a ditch is not a night's sleep.

## 9. Powers

Magic, psionics, implants, mutations: whatever the World Bible's laws allow a person to do. Each power is an entry in the Rules Kit with its skill, reach, limits, and cost. Unless the kit says otherwise:

| Size of the effect | Difficulty | Strain |
|---|---|---|
| Minor: a light, a nudge, a whisper | 12 | 1 |
| Significant: what a skilled person with tools could do | 15 | 2 |
| Major: beyond any tool, on one target or one room | 18 | 4 |
| Grand: a building, a crowd, an hour's work in a breath | 22 | 6 |

A Partial works and costs more (double Strain, a side effect, an unwanted witness). A Disaster does what the kit says a Disaster does. A power can never do what the World Bible says it can't.

## 10. Long tasks

Something that can't be settled in one roll (a chase, a long climb, tracking through a storm, breaking a cipher, a siege of someone's patience) gets a clock of 4, 6, or 8 steps. Each roll fills it: Partial 1, Success 2, Critical 3. A Failure or Disaster moves the danger closer instead, in whatever form it takes (the quarry gains, the rope frays, the guard comes back). Each roll is its own beat; the player says what their character does next.

## 11. Dealing with people

A roll never moves someone against their nature. Before any roll, decide from their doc what this person wants and where they stand: if they'd agree, there's no roll; if nothing would move them, there's no roll either. In between, the roll is how well the character's approach lands, against Resolve or against:

| They are | Difficulty |
|---|---|
| open to it | 12 |
| reluctant | 15 |
| set against it | 18 |

What the character actually says and offers matters more than the roll: a good reason given to the right person can make a roll unnecessary, and a bad one gives Setback. A Partial gets agreement with a condition, a price, or a doubt. People remember being lied to, leaned on, and helped.

## 12. Questions about the world

When play needs a fact that nothing establishes (is the ferry running, does the guard know that face, is anyone on the road tonight):

1. If the docs answer it, that's the answer.
2. If the people involved would decide it, they decide it, from their docs.
3. If the world's laws or plain likelihood answer it, that's the answer.
4. Only if it's truly open, ask fate: set the odds from the fiction (certain, likely, even, unlikely, remote) and roll. "And more" and "and worse" push the answer further the same way.

Write the answer down wherever it belongs. It's canon now.

`gm fate <odds> "<the question>"`

## 13. Everyone else

Nobody but the player character has a full sheet. Everyone and everything else has a **stat line**, built from a tier:

| Tier | Is | Bonus | Defenses | HP | Damage |
|---|---|---|---|---|---|
| 0 | harmless: a child, a rat | +0 | 9 | 3 | d4 |
| 1 | ordinary: a farmer, a clerk, a stray dog | +2 | 11 | 8 | d6 |
| 2 | trained: a soldier, a wolf, a street tough who's good at it | +4 | 13 | 14 | d8+1 |
| 3 | veteran: a knight, a bear, a hired killer | +6 | 15 | 24 | d10+2 |
| 4 | elite: a champion, a troll, a war machine | +8 | 17 | 40 | d12+3 |
| 5 | dreadful: a warlord in their prime, a young dragon | +10 | 19 | 65 | 2d8+4 |
| 6 | legendary | +12 | 21 | 100 | 2d10+6 |

The bonus is for what they're made to do. They get +2 on what they're **strong at** and -2 on what they're **weak at**, and half the bonus (rounded down) at anything outside their line of work. Adjust a single number when the person calls for it (a frail old master: tier 4 bonus, tier 1 HP). Armor, a weapon's tags, and anything strange about them are added in words.

A tier says how dangerous someone is, never how important. Most people the character meets are tier 1.

## 14. Gear

**Weapons** deal damage by size, plus Might for anything swung, thrown, or drawn by muscle:

| Size | Damage | Such as |
|---|---|---|
| Slight | d4 | a fist, a knife, a rock |
| Light | d6 | a short blade, a club, a holdout pistol |
| Medium | d8 | a sword, a spear, a bow, a sidearm |
| Heavy | d10 | a greataxe, a rifle, a crossbow |
| Massive | d12 | a siege weapon carried by one person, an anti-materiel gun |

Tags say what else is true of a weapon, in words that mean what they say: reach, two hands, concealed, loud, slow to reload, hits an area, pierces armor (ignores that much).

**Armor** takes damage off every blow: light 1, medium 2, heavy 3 (and Setback on sneaking, swimming, and long exertion). The world's best might reach 4.

**Everything else** does what it would do. The right tool can give Edge, or make a thing possible at all. A person carries what a person could carry; past that they're slowed, and the page shows it.

**Money** is counted in the world's own currency, to the coin, on the Character Sheet (Craft Rules, "Track props and transactions").

**Buying and selling.** A thing costs what the world's Economy says it costs, and a price the page has set holds. Someone who deals in a thing buys it for about half of what they'd sell it for: more if it's scarce or they have a buyer waiting, less if it's worn or hard to move, and nothing if they have no use for it. The keeper names the price, and the character can take it, leave it, or try to change it (§11). While the character is in a shop, what's for sale and what would be bought are listed for the user (Procedures/Play.md, "A shop").

## 15. Making the player character

Done by the user during setup, on the play window's character creator or in conversation (Procedures/New Narrative.md). Whatever they leave open, the GM chooses to fit the person they described:

1. **Attributes:** +2, +1, +1, 0, 0, -1, one to each attribute.
2. **Skills:** 10 ranks, no skill above 2, each with a source in the character's background.
3. **Talents:** two. One from their background, one that's simply theirs.
4. **Defenses, HP, Strain:** from the formulas above.
5. **Gear and money:** what this person would own, by the world's Economy.

## 16. Growing

**Marks** are what experience leaves. At the end of each session, the character earns one for each of these that was true of the session, four at most:

- they came through real danger;
- they got something they were after, or lost it for good;
- they learned something that changes how things look;
- a choice or a failure cost them something real.

The next level takes **4 + twice their current level** marks (6 to reach level 2, 8 to reach level 3). Level 10 is the top.

On a new level:

- HP and Strain go up by their formulas.
- **3 skill ranks.** No skill above 2 at levels 1 and 2, above 3 at levels 3 and 4, above 4 at levels 5 to 7. A new skill, or a big jump, needs a source in what the character has been doing.
- **A talent** at every even level.
- **+1 to one attribute** at levels 3, 6, and 9, to a limit of +5.

Every choice on a new level is the user's. Put the choices to them at the end of the session (Procedures/Play.md, "A new level") and apply what they pick. None of it is mentioned on the page: the character is simply better at what they've been doing.

## 17. Talents

A talent is one thing a character can do that others can't, or can't as well. The Rules Kit lists the world's; write new ones with the user in these shapes:

- **Edge in a narrow place:** Edge on rolls of one kind in one circumstance (tracking in snow, reading a liar, fighting two at once).
- **A thing they can simply do:** no roll where others would need one (never lost in a city they've walked, sleeps light enough that nothing surprises them).
- **A power:** access to one of the world's powers, or a new use of one they have.
- **Harder to hurt:** +1 to one defense, or 1 armor against one kind of harm.
- **More to give:** +3 HP or +2 Strain.
- **A trick:** once between sleeps, something sure (turn a Partial into a Success with one skill, act first in a fight).

A talent never does what the World Bible says can't be done.
