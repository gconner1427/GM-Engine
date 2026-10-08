# GM Engine

This folder is the engine: the rules, writing rules, procedures, templates, and scripts that every narrative uses. No narrative is played from here, and nothing from a narrative is ever stored here. `README.md` describes the whole thing; `ENGINE.md` is the manual the GM follows.

**If the user asks for a new narrative:** the play window (`Play.cmd`) is the usual way. Otherwise follow `Procedures/New Narrative.md`, step 1: ask for its name and where it should live, run `python engine/gm.py new-narrative "<Name>" --at "<folder>"`, and tell them to open that folder to set it up and play.

**The world belongs to the GM.** In a narrative, the GM builds the world from a three-question premise and the user discovers it by playing. Nothing in the engine, the templates, or the play window may show the user the world docs.

**If the user is working on the engine itself:**
- A change to how the game works goes in `Rules/Core Rules.md`. The tables in `engine/dice.py` (outcome margins, fate odds, how damage is halved and doubled) have to match it.
- A change to how the GM behaves goes in `Rules/GM Rules.md` or the procedure it belongs to.
- A writing rule goes in `Writing/Craft Rules.md`, in the house format (the rule in bold, exceptions, an example), with its reason in `Writing/Craft Rules History.md`. Rules come from what the user flags, never from outside benchmarks.
- The play window is `engine/gui.py` (a local server that runs Claude Code headless in the narrative's folder) and `engine/gui/app.html` (the page). It reads only player-safe files; never make it show anything from `GM Only/`. Project settings are ignored in headless runs of an untrusted folder, so the permissions the GM needs are passed as flags in `claude_command`. What the GM is told about the window is `WINDOW_NOTE`.
- A change to a template changes only narratives made afterward. Say so, and offer to apply it to existing ones if the user names them.
- The engine was forked from the Living World Engine (`C:/Users/grant/Living World Engine`). The two are separate: nothing here reads from it, and changes here don't go back to it.
