# GM Engine

This folder is the engine: the rules, writing rules, procedures, templates, and scripts that every narrative uses. No narrative is played from here, and nothing from a narrative is ever stored here. `README.md` describes the whole thing; `ENGINE.md` is the manual the GM follows.

**If the user asks for a new narrative:** follow `Procedures/New Narrative.md`, step 1. Ask for its name and where it should live, run `python engine/gm.py new-narrative "<Name>" --at "<folder>"`, and tell them to open that folder in VS Code to set it up and play.

**If the user is working on the engine itself:**
- A change to how the game works goes in `Rules/Core Rules.md`. The tables in `engine/dice.py` (outcome margins, fate odds, how damage is halved and doubled) have to match it.
- A change to how the GM behaves goes in `Rules/GM Rules.md` or the procedure it belongs to.
- A writing rule goes in `Writing/Craft Rules.md`, in the house format (the rule in bold, exceptions, an example), with its reason in `Writing/Craft Rules History.md`. Rules come from what the user flags, never from outside benchmarks.
- A change to a template changes only narratives made afterward. Say so, and offer to apply it to existing ones if the user names them.
- The engine was forked from the Living World Engine (`C:/Users/grant/Living World Engine`). The two are separate: nothing here reads from it, and changes here don't go back to it.
