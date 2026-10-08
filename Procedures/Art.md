# Art

A narrative can be illustrated: a portrait of the player character, portraits of the people they meet, backdrops of the places they go, and now and then a scene or an object. You decide what gets a picture and say what it shows. Codex paints it in the background, and the play window shows it: the character's portrait on their sheet, the current place above the narrative, faces beside names in the Journal, and everything in the Gallery.

You never wait for a picture. `gm art` writes the request down and returns at once; the painting takes a minute or two and happens while play goes on.

Skip all of this if the Style Guide says **Illustrations: off**.

## Asking for a picture

```
gm art portrait "<name>" "<what they look like>"
gm art place "<name>" "<what it looks like>"
gm art scene "<name>" "<what it shows>"
gm art item "<name>" "<what it looks like>"
```

Run it in the same call as `gm beat`, after the beat is committed. Asking again for something that already has a picture does nothing, so there's no need to check first.

**The name** is what the character calls them, and it's what the player sees under the picture. Someone whose name she doesn't know yet is "the grey-bearded peddler," never the name in your docs. When she learns it: `gm art portrait "Martin Hale" --was "the grey-bearded peddler"`.

**The description** is for a painter who knows nothing about the narrative. Two or three sentences of what the eye would see:
- A person: age, build, face, hair, what they're wearing, their bearing or expression, and the light or weather they were met in.
- A place: what it is, what it's made of, its size and state, the time of day and weather, what's around it.
- Plain visual words. No names, no backstory, no feelings, nothing that isn't visible.
- **Be exact. The painter takes liberties with anything left unsaid, and gets it wrong.** A scene, or any picture where pose matters, spells out all of it and runs as long as it needs to:
    - where the viewer stands and what they're looking toward;
    - each figure: where they are in the frame, which way their body faces, which way their head is turned, and what their eyes are on (say outright "not looking at the viewer" when they aren't);
    - what's in each hand, what each is wearing, and its state (wet, torn, smeared);
    - who is aware of whom, and who has their back to whom;
    - what must not be in the picture ("no other people").
    - ✗ "stands on the bottom steps, looking back over her shoulder... just below her, with their backs to her, stand three figures" (she came out facing the camera, body toward the people) → ✓ "Her body faces away from the viewer, up the stairs: we see her back. Only her head is turned, over her right shoulder, so her face is in right profile; her eyes look down at the backs of the cloaked figures below her, not at the viewer."
- If the narrative is built on an existing setting, describe what's seen in ordinary words rather than by the setting's trademarks or its famous characters.

The art style comes from the Style Guide's **Art style** line and is added for you: leave style out of the description. If the Style Guide has no art style yet, write one that suits the genre and tone before the first request.

## Only what the character has seen

`Art/` is the player's to look at. A picture is the same as a sentence on the page (GM Rules, "What's hidden"):

- Paint a person only once the character has had a clear look at them, and only as they appeared to her. A disguise is painted as the disguise.
- Paint a place only as far as she's seen it: the outside when she's outside it.
- Never ask for a picture of someone or something she hasn't met, and never let a description show what's hidden (the knife behind his back, the brand under the sleeve).
- A picture can't be more revealing than the prose was. If the beat kept someone in shadow, there's no portrait yet.

## What gets a picture

Only the moments that feel major. A picture marks something: when one appears, the player should feel that this person, this place, this thing matters. Painting everything makes none of it matter, and each one costs the player a minute or two of Codex. Most beats ask for nothing, and many whole scenes do too.

**Paint these:**
- **The player character:** once, at the end of setup, from the sheet's Looks. Ask again (`--redo`) only when their appearance changes for good (a scar, years passing) or the player asks.
- **Arriving somewhere that matters:** the first sight of a town or a city, a castle, a stronghold, a ship, a ruin, a landmark. The kind of place a traveler would stop and look at.
- **A new person who matters:** someone with a name and a part to play, met face to face: the lord, the rival, the stranger who changes the day, a companion.
- **Something found:** an object that matters (the blade, the letter with the broken seal, the thing in the chest).
- **A mystery:** the strange thing come upon (the door that shouldn't be there, the markings, what's in the clearing), painted exactly as far as she can see it.
- **A moment the narrative will remember,** rarely: the kind of scene that would be a full-page plate in a book.

**Don't paint these:**
- Ordinary rooms, roads, camps, shops, and stretches of country. A common inn or a farm gets nothing, unless what happens there makes it a place that matters.
- Passers-by, guards, servants, shopkeepers, and anyone met once in passing. If one of them turns out to matter later, paint them then.
- Everyday gear and anything bought over a counter.
- The same thing twice.

When in doubt, don't. No more than one request in most beats that have any, and never more than two.

**Coming back.** When the character returns to a place that already has a picture, run `gm art place "<name>"` (no description) and it becomes the backdrop again. When she leaves a pictured place for somewhere that won't get one, the old backdrop stays until the next place that does.

**A new session.** `gm session start` takes the backdrop down. The top of the narrative stays bare until this session paints a place or comes back to one, so if the session opens somewhere that already has a picture, run `gm art place "<name>"` with the first beat.

Keep it within the Style Guide's content lines, and plainer than that: no gore, no nudity, nothing a painter would refuse. If a request fails, leave it; asking again later retries it.

## When the player asks

- `{redo her portrait, she should look older}`: write a new description with the change and `gm art portrait "<name>" "<description>" --redo`.
- `{paint that}` about something on the page: ask for it, if the character has seen it.
- `{no more pictures}` or `{pictures on}`: set **Illustrations** in the Style Guide.
- A change of style: set **Art style** in the Style Guide. Pictures already painted stay as they are unless the player asks for them to be redone.
