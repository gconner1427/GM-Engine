"""The carry count (engine/carry.py) against Core Rules §14, "Carrying".

    python -m unittest discover tests        from the engine's folder

Sheets are made from the Character Sheet template, so a change to the template's Gear lines is tested too.
"""

import re
import sys
import unittest
from pathlib import Path

ENGINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ENGINE / "engine"))

import carry  # noqa: E402

TEMPLATE = (ENGINE / "Templates" / "Narrative" / "Character Sheet.md").read_text(encoding="utf-8")
LOADOUT = ("a bedroll, fifty feet of rope, a lantern, lamp oil ×3, rations ×5, a waterskin, a healer's kit, spare clothes, "
           "a tinderbox (small), a whetstone (small), a letter (small)")
SHOP = """## Shop

**Name:** Harrow's Chandlery
**Keeper:** Old Harrow

### Coins
- **shilling:** 1

### For sale
{sale}

### Will buy
{buys}

"""


def sheet(might=1, wearing="travel leathers (armor 1), a canvas pack (pack 8)", ready="", carried=LOADOUT, arms=None,
          kept="", shop=None):
    """A sheet from the template with these gear lines. `arms` adds the In arms line; `shop` is (for sale, will buy)."""
    text = re.sub(r"\| 0 \| 0 \| 0 \| 0 \| 0 \| 0 \|", f"| {might} | 0 | 0 | 0 | 0 | 0 |", TEMPLATE, count=1)
    for name, said in (("Wearing", wearing), ("Ready", ready), ("Carried", carried), ("Kept elsewhere", kept)):
        text, n = re.subn(rf"(?m)^- \*\*{name}:\*\*.*$", lambda m: f"- **{name}:** {said}", text, count=1)
        assert n == 1, name
    if arms is not None:
        text = text.replace("- **Kept elsewhere:**", f"- **In arms:** {arms}\n- **Kept elsewhere:**", 1)
    if shop:
        lines = lambda wares: "\n".join(f"- **{w}:** 2 shillings" for w in wares)
        text = text.replace("## Vitals", SHOP.format(sale=lines(shop[0]), buys=lines(shop[1])) + "## Vitals", 1)
    return text


def used(place, said, **more):
    """The slots a gear line takes when it is all there is in that place."""
    return carry.read(sheet(**{"carried": "", place: said}, **more))["pack" if place == "carried" else place]["used"]


def moves(*pairs):
    return [{"id": i, "to": to} for i, to in pairs]


def named(c, key):
    return [t["name"] for l in c["lines"] if l["key"] == key for t in l["things"]]


class Counting(unittest.TestCase):
    def test_the_loadout(self):
        c = carry.read(sheet())
        self.assertEqual((c["pack"]["used"], c["pack"]["room"], c["pack"]["over"]), (8, 9, False))
        self.assertEqual((c["pack"]["size"], c["pack"]["might"], c["pack"]["written"]), (8, 1, "a canvas pack"))
        self.assertEqual(carry.report(c).splitlines()[:2], ["Ready: 0 of 4", "Pack: 8 of 9  (canvas pack, size 8, Might +1)"])

    def test_over(self):
        c = carry.read(sheet(carried=LOADOUT + ", a mail shirt (bulky)"))
        self.assertEqual((c["pack"]["used"], c["pack"]["room"], c["pack"]["over"]), (10, 9, True))
        self.assertIn("Pack is over by 1.", carry.report(c))

    def test_stacks_and_counts(self):
        for said, slots in (("rations ×7", 2), ("rations ×5", 1), ("rations x7", 2), ("rations (×7)", 2), ("two daggers", 2),
                            ("daggers ×2", 1), ("daggers (2)", 2), ("daggers (×2)", 1), ("50 feet of rope", 1),
                            ("a quiver of 20 arrows", 1), ("7 flasks of oil", 1), ("flasks of oil ×7", 2),
                            ("two tents (bulky)", 4), ("tents ×2 (bulky)", 4), ("a dagger", 1), ("fifteen torches", 1)):
            self.assertEqual(used("carried", said), slots, said)

    def test_forms(self):
        forms = {t["written"]: (t["form"], t["count"], t["chip"]) for t in carry.things("a dagger, daggers ×2, two knives, 50 feet of rope")}
        self.assertEqual(forms, {"a dagger": ("one", 0, ""), "daggers ×2": ("stack", 2, ""), "two knives": ("each", 2, ""),
                                 "50 feet of rope": ("measure", 0, "50 feet")})

    def test_small_things(self):
        smalls = lambda n: ", ".join(f"a key to door {chr(97 + i)} (small)" for i in range(n))
        for n, slots in ((10, 0), (11, 1), (15, 1), (16, 2)):
            c = carry.read(sheet(carried="a bedroll", ready=smalls(n)))
            self.assertEqual((c["small"]["count"], c["small"]["slots"]), (n, slots))
            self.assertEqual((c["pack"]["used"], c["ready"]["used"]), (1 + slots, 0), "the pack pays, never Ready")
        for said in ("keys ×3 (small)", "3 keys (small)"):
            c = carry.read(sheet(carried=said))
            self.assertEqual((c["small"]["count"], c["pack"]["used"]), (3, 0), said)

    def test_marks(self):
        self.assertEqual(used("ready", "a greatsword (bulky)"), 2)
        c = carry.read(sheet(ready="a greatsword (two hands)"))
        self.assertEqual(c["ready"]["used"], 1)
        self.assertEqual(len(c["trouble"]), 1)
        self.assertIn("no size mark", c["trouble"][0])
        self.assertIn(c["trouble"][0], carry.report(c))
        t = carry.read(sheet(ready="a longbow (bulky, two hands; her mother's)"))["lines"][1]["things"][0]
        self.assertEqual((t["size"], t["notes"]), ("bulky", ["two hands; her mother's"]))
        worn = carry.read(sheet(wearing="a mail shirt (medium armor 2, bulky), a canvas pack (pack 8)"))
        self.assertEqual((worn["lines"][0]["things"][0]["chip"], worn["lines"][0]["things"][0]["size"]), ("Armor 2", "bulky"))
        self.assertEqual(worn["ready"]["used"] + worn["pack"]["used"], 8, "worn armor keeps its mark and is not counted")

    def test_arms(self):
        c = carry.read(sheet(arms="a sea chest (armload)"))
        self.assertEqual((c["arms"]["over"], c["arms"]["laden"], c["arms"]["used"]), (False, True, 2))
        self.assertIn("Laden: arms full.", carry.report(c))
        self.assertTrue(carry.read(sheet(arms="a sea chest (armload), a key (small)"))["arms"]["over"])
        self.assertFalse(carry.read(sheet(arms="a mail shirt (bulky)"))["arms"]["over"])
        self.assertTrue(carry.read(sheet(arms="a mail shirt (bulky), a lantern"))["arms"]["over"])
        self.assertFalse(carry.read(sheet())["arms"]["laden"])

    def test_pack_room(self):
        for might, wearing, room in ((-1, "a satchel (pack 4)", 3), ("−1", "a satchel (pack 4)", 3), (5, "a great pack (pack 12)", 17),
                                     ("+2", "a pack (pack 8)", 10), (5, "no pack (pack 0)", 0), (0, "no pack (pack 0)", 0),
                                     (-5, "a satchel (pack 4)", 0)):
            self.assertEqual(carry.read(sheet(might=might, wearing=wearing))["pack"]["room"], room, (might, wearing))
        c = carry.read(sheet(might="strong", wearing="a pack (pack 8)"))
        self.assertEqual(c["pack"]["room"], 8)
        self.assertTrue(any("Might" in line for line in c["trouble"]))

    def test_packs(self):
        two = carry.read(sheet(wearing="a canvas pack (pack 8), a great pack (pack 12)"))
        self.assertEqual(two["pack"]["size"], 8)
        self.assertIn("Two packs are on Wearing; the first is counted.", two["trouble"])
        off = carry.read(sheet(wearing="a shirt", carried="a satchel (pack 4)"))
        self.assertEqual((off["counted"], off["pack"]["room"], off["pack"]["used"]), (True, 0, 1))

    def test_not_counted(self):
        for text in (TEMPLATE, sheet(wearing="a shirt, a canvas pack"), "", "not a sheet at all", None):
            c = carry.read(text)
            self.assertFalse(c["counted"])
            self.assertEqual(carry.report(c), "Not counted: this sheet gives its pack no size.")
            self.assertNotIn("pack", c)
        old = carry.read(sheet(wearing="a shirt", carried="a canvas pack holding a blanket, a ring (small), two daggers"))
        self.assertEqual(named(old, "pack"), ["Canvas pack holding a blanket", "Ring", "Daggers"])
        self.assertEqual(old["lines"][2]["things"][1]["notes"], ["small"], "on a sheet not counted a mark is only a note")

    def test_never_raises(self):
        full = sheet(ready="a sword, a shield", arms="a chest (armload)", shop=(["Mail shirt (bulky)"], ["Bedroll"]))
        lines = full.split("\n")
        for n in range(len(lines) + 1):
            text = "\n".join(lines[:n])
            self.unguarded(text)
        for cut in range(0, len(full), 7):   # and cut anywhere inside a line
            self.unguarded(full[:cut])
        for junk in ([None], [3], [{"id": None, "to": []}], "pack:1", None):
            carry.arrange(full, junk, junk, junk, junk)
        self.assertEqual(carry.read(sheet(wearing="a pack (pack 99999999999999999999)", carried="rations ×99999999999"))["pack"]["room"], carry.MOST + 1)

    def unguarded(self, text):
        """The work under read, wares and arrange, without the nets that keep those three from ever raising."""
        model = carry.parse(text)
        carry.report(carry.tally(model))
        shelf = carry.shelves(model, text)
        if model["counted"]:
            carry.moved(model, moves(("ready:0", "pack"), ("pack:0", "arms"), ("nothing", "worn")))
            for to in carry.TO:
                carry.allowed(model, "pack:0", to)
            carry.trade(model, shelf, [{"written": "Mail shirt (bulky)", "n": 2}], [{"written": "Bedroll", "n": 1}])
            carry.tally(model)

    def test_the_procedure_examples(self):
        play = (ENGINE / "Procedures" / "Play.md").read_text(encoding="utf-8")
        good = re.search(r"^- ✓ `(.+?)`", play, re.M).group(1)
        self.assertEqual(len(carry.things(good)), 1)


class Arranging(unittest.TestCase):
    def setUp(self):
        self.sheet = sheet(ready="a sword, a mail shirt (bulky)")   # the pack is 8 of 9

    def test_read_is_arrange_with_nothing(self):
        for text in (self.sheet, sheet(arms="a chest (armload)"), TEMPLATE, ""):
            self.assertEqual(carry.read(text), carry.arrange(text, [])["carry"])
        self.assertNotIn("fits", carry.arrange(self.sheet, []))
        self.assertTrue(all(t["from"] == "" for l in carry.read(self.sheet)["lines"] for t in l["things"]))

    def test_a_move_and_back(self):
        a = carry.arrange(self.sheet, moves(("pack:3", "ready")))["carry"]
        last = a["lines"][1]["things"][-1]
        self.assertEqual((last["id"], last["from"], a["ready"]["used"], a["pack"]["used"]), ("pack:3", "pack", 4, 7))
        b = carry.arrange(self.sheet, moves(("pack:3", "ready"), ("ready:0", "pack"), ("pack:3", "arms")))["carry"]
        held = next(l for l in b["lines"] if l["key"] == "arms")["things"]
        self.assertEqual([(t["id"], t["from"]) for t in held], [("pack:3", "pack")])
        self.assertTrue(b["arms"]["laden"])
        back = carry.arrange(self.sheet, moves(("pack:3", "ready"), ("pack:3", "arms"), ("pack:3", "pack")))["carry"]
        self.assertEqual(back, carry.read(self.sheet))
        cloak = sheet(wearing="a cloak, travel leathers (armor 1), a canvas pack (pack 8)", carried="a bedroll")
        self.assertEqual(carry.arrange(cloak, moves(("worn:0", "pack"), ("worn:0", "worn")))["carry"], carry.read(cloak), "what was worn goes back on")
        self.assertEqual(carry.arrange(cloak, moves(("pack:0", "worn")))["refused"]["code"], "not_armor")

    def test_a_question_moves_nothing(self):
        two = moves(("pack:1", "arms"), ("pack:0", "arms"))
        for tid in ("pack:1", "pack:0", "ready:0", "worn:0"):
            self.assertEqual(carry.arrange(self.sheet, two, fit=tid)["carry"], carry.arrange(self.sheet, two)["carry"], tid)
        swapped = carry.arrange(self.sheet, moves(("ready:0", "pack"), ("pack:0", "ready")))["carry"]
        self.assertEqual((swapped["ready"]["coming"], swapped["pack"]["coming"], carry.read(self.sheet)["pack"]["coming"]), (1, 1, 0))
        ten = ", ".join(f"a key to door {chr(97 + i)} (small)" for i in range(10))
        eleventh = carry.arrange(sheet(wearing="a ring (small), a canvas pack (pack 8)", carried="a bedroll", ready=ten), moves(("worn:0", "ready")))["carry"]
        self.assertEqual((eleventh["pack"]["used"], eleventh["pack"]["coming"], eleventh["ready"]["coming"]), (2, 1, 0), "the slot its charge takes is on its way too")

    def test_dropped(self):
        self.assertNotIn("dropped", [l["key"] for l in carry.read(self.sheet)["lines"]])
        a = carry.arrange(self.sheet, moves(("pack:0", "dropped")))["carry"]
        self.assertEqual(a["lines"][-1]["key"], "dropped")
        self.assertEqual([(t["id"], t["from"]) for t in a["lines"][-1]["things"]], [("pack:0", "pack")])
        self.assertEqual(a["pack"]["used"], 7)
        self.assertEqual(carry.arrange(self.sheet, moves(("pack:0", "dropped"), ("pack:0", "pack")))["carry"], carry.read(self.sheet))

    def test_refusals(self):
        refused = lambda text, *pairs: carry.arrange(text, moves(*pairs))["refused"]
        self.assertEqual(refused(self.sheet, ("ready:1", "pack")), {"code": "full", "need": 2, "room": 1, "at": 0})
        self.assertEqual(refused(self.sheet, ("pack:0", "ready"), ("pack:1", "ready")), {"code": "full", "need": 1, "room": 0, "at": 1})
        self.assertEqual(refused(self.sheet, ("ready:1", "pack"), ("pack:0", "ready"))["at"], 0, "the earlier bad move is the one reported")
        self.assertEqual(refused(self.sheet, ("worn:1", "dropped"))["code"], "the_pack")
        self.assertEqual(refused(self.sheet, ("pack:99", "ready"))["code"], "gone")
        self.assertEqual(refused(self.sheet, ("pack:0", "the moon"))["code"], "gone")
        chest = sheet(arms="a sea chest (armload)")
        self.assertEqual(refused(chest, ("arms:0", "ready"))["code"], "too_big")
        self.assertEqual(refused(chest, ("arms:0", "pack"))["code"], "too_big")
        self.assertEqual(refused(chest, ("pack:0", "arms")), {"code": "arms_full", "need": 1, "room": 0, "at": 0})

    def test_the_eleventh_small_thing(self):
        ten = ", ".join(f"a key to door {chr(97 + i)} (small)" for i in range(10))
        full = "a bedroll, a rope, a lantern, a pot, a tent (bulky), a waterskin, a kit, a cloak"   # 9 of 9
        for wearing, carried in (("a ring (small), a canvas pack (pack 8)", full), ("a ring (small), no pack (pack 0)", "")):
            text = sheet(wearing=wearing, carried=carried, ready=ten)
            fits = carry.arrange(text, [], fit="worn:0")["fits"]
            for to in ("ready", "pack", "arms"):
                self.assertEqual(fits[to], {"code": "full", "need": 1, "room": 0}, (wearing, to))
            self.assertEqual(carry.arrange(text, moves(("worn:0", "ready")))["refused"]["code"], "full")

    def test_fits(self):
        fits = carry.arrange(self.sheet, [], fit="ready:1")["fits"]
        self.assertEqual(fits, {"ready": {"code": "here", "need": 0, "room": 0}, "pack": {"code": "full", "need": 2, "room": 1},
                                "arms": None, "dropped": None, "worn": {"code": "not_armor", "need": 0, "room": 0}})
        armor = lambda wearing: carry.arrange(sheet(wearing=wearing, ready="a mail shirt (armor 2, bulky)"), [], fit="ready:0")["fits"]["worn"]
        self.assertEqual(armor("travel leathers (armor 1), a canvas pack (pack 8)")["code"], "not_worn")
        self.assertIsNone(armor("a shirt, a canvas pack (pack 8)"))
        chest = lambda arms: carry.arrange(sheet(ready="a sea chest (armload)", arms=arms), [], fit="ready:0")["fits"]
        self.assertEqual((chest(None)["ready"]["code"], chest(None)["pack"]["code"], chest(None)["arms"]), ("here", "too_big", None))
        self.assertEqual(carry.arrange(sheet(arms="a sea chest (armload)"), moves(("arms:0", "dropped")), fit="arms:0")["fits"]["ready"]["code"], "too_big")
        self.assertEqual(chest("a lantern")["arms"], {"code": "arms_full", "need": 2, "room": 1})
        self.assertEqual(carry.arrange(sheet(arms="a sea chest (armload)"), [], fit="pack:0")["fits"]["arms"],
                         {"code": "arms_full", "need": 1, "room": 0})
        over = sheet(ready="a sword", carried=LOADOUT + ", a mail shirt (bulky)")
        self.assertIsNone(carry.arrange(over, [], fit="pack:0")["fits"]["ready"])
        self.assertEqual(carry.arrange(over, [], fit="ready:0")["fits"]["pack"]["code"], "full")
        kept = sheet(kept="a horse, a chest of clothes")
        for tid, code in (("worn:1", "the_pack"), ("kept:0", "fixed"), ("nothing:7", "gone")):
            self.assertEqual({why["code"] for why in carry.arrange(kept, [], fit=tid)["fits"].values()}, {code}, tid)

    def test_fits_and_moves_agree(self):
        text = sheet(ready="a sword, a shield, a mail shirt (armor 2, bulky)", arms="a lantern", kept="a horse")
        for line in carry.read(text)["lines"]:
            for t in line["things"]:
                fits = carry.arrange(text, [], fit=t["id"])["fits"]
                for to in carry.TO:
                    answer = carry.arrange(text, moves((t["id"], to)))
                    if fits[to] is None or fits[to]["code"] == "here":
                        self.assertIn("carry", answer, (t["id"], to))
                    else:
                        self.assertEqual(answer["refused"], dict(fits[to], at=0), (t["id"], to))


class Shop(unittest.TestCase):
    def test_wares(self):
        w = carry.wares(sheet(shop=(["Mail shirt (bulky)", "Chalk (small)", "Sea chest (armload)", "Arrows ×20", "Great pack (pack 12)",
                                     "Rope, fifty feet"], ["Bedroll", "Wolf pelt"])))
        got = [(b["written"], b["name"], b["size"], b["slots"], b["is_pack"]) for b in w["buy"]]
        self.assertEqual(got, [("Mail shirt (bulky)", "Mail shirt", "bulky", 2, False), ("Chalk (small)", "Chalk", "small", 0, False),
                               ("Sea chest (armload)", "Sea chest", "armload", carry.ARMS_ROOM, False), ("Arrows ×20", "Arrows ×20", "ordinary", 4, False),
                               ("Great pack (pack 12)", "Great pack", "ordinary", 0, True), ("Rope, fifty feet", "Rope, fifty feet", "ordinary", 1, False)])
        self.assertEqual([(s["written"], s["id"]) for s in w["sell"]], [("Bedroll", "pack:0"), ("Wolf pelt", "")])
        tent = carry.wares(sheet(carried="a tent (bulky)", shop=(["Chalk"], ["Tent"])))["sell"][0]
        self.assertEqual((tent["id"], tent["size"], tent["slots"]), ("pack:0", "bulky", 2), "a ware the keeper would buy has its thing's size")
        priced = sheet(shop=(["Chalk"], [])).replace("- **Chalk:** 2 shillings", "- **Chalk:** 2 shillings ×3. White.")
        self.assertEqual(carry.wares(priced)["buy"][0]["slots"], 1, "how many the keeper has is never a stack")
        for text in (sheet(), sheet(wearing="a shirt", shop=(["Chalk"], [])), sheet(shop=(["Chalk"], [])).replace("Harrow's Chandlery", "(unknown)")):
            self.assertEqual(carry.wares(text), {"buy": [], "sell": []})

    def test_the_procedure_example(self):
        play = (ENGINE / "Procedures" / "Play.md").read_text(encoding="utf-8")
        shop = re.search(r"```\n(## Shop\n.*?)```", play, re.S).group(1)
        w = carry.wares(sheet().replace("## Vitals", shop + "\n## Vitals", 1))
        self.assertEqual([b["written"] for b in w["buy"]], ["Tin lantern", "Rope, fifty feet", "Lamp oil ×1"])
        self.assertEqual([s["written"] for s in w["sell"]], ["Wolf pelt", "Short sword"])

    def basket(self, buy, sell=(), **gear):
        wares = ["Tin lantern", "Mail shirt (bulky)", "Sea chest (armload)", "Lamp oil", "Chalk (small)", "Great pack (pack 12)", "Rope"]
        want = lambda names: [{"written": n, "n": k} for n, k in names]
        return carry.arrange(sheet(shop=(wares, ["Bedroll"]), **gear), [], buy=want(buy), sell=want(sell))

    def test_the_basket(self):
        full = "a bedroll, a rope, a lantern, a pot, a tent (bulky), a waterskin, a kit, a cloak"   # 9 of 9
        a = self.basket([("Tin lantern", 1)])
        self.assertEqual((a["spill"], a["carry"]["pack"]["used"], a["carry"]["arms"]["laden"]), (0, 9, False))
        a = self.basket([("Mail shirt (bulky)", 1)])
        self.assertEqual((a["spill"], a["carry"]["pack"]["used"], a["carry"]["arms"]["laden"]), (2, 8, True))
        self.assertEqual(self.basket([("Tin lantern", 3)], carried=full)["refused"], {"code": "full", "need": 3, "room": 2, "at": -1})
        for order in ([("Tin lantern", 1), ("Mail shirt (bulky)", 1)], [("Mail shirt (bulky)", 1), ("Tin lantern", 1)]):
            a = self.basket(order, carried="a bedroll, a rope, a lantern, a pot, a tent (bulky), a waterskin", arms="a keg")   # 7 of 9
            self.assertEqual((a["spill"], a["carry"]["pack"]["used"]), (1, 9), "the bulky ware is placed first")
        self.assertEqual(self.basket([("Sea chest (armload)", 1)])["spill"], 2)
        self.assertEqual(self.basket([("Sea chest (armload)", 1)], arms="a keg")["refused"]["code"], "full")
        a = self.basket([("Lamp oil", 2)], carried=full.replace("a cloak", "lamp oil ×3"))
        self.assertEqual((a["spill"], a["carry"]["pack"]["used"]), (0, 9), "it joins the stack already in the pack")
        a = self.basket([("Tin lantern", 1)], [("Bedroll", 1)], carried=full)
        self.assertEqual((a["spill"], a["carry"]["pack"]["used"]), (0, 9))
        ten = ", ".join(f"a key to door {chr(97 + i)} (small)" for i in range(10))
        self.assertEqual(self.basket([("Chalk (small)", 1)], carried=full, ready=ten)["refused"]["code"], "full")
        self.assertEqual(self.basket([("Chalk (small)", 1)], ready=ten)["spill"], 0)
        for order in ([("Chalk (small)", 1), ("Tin lantern", 1)], [("Tin lantern", 1), ("Chalk (small)", 1)]):   # 8 of 9: the chalk's charge takes the slot
            a = self.basket(order, carried=full.replace(", a cloak", ""), ready=ten)
            self.assertEqual((a["spill"], a["carry"]["pack"]["used"]), (1, 9), "small wares are placed first")
        sold = carry.arrange(sheet(shop=(["Chalk"], ["Canvas pack"])), [], sell=[{"written": "Canvas pack", "n": 1}])
        self.assertEqual(sold["carry"]["pack"], carry.read(sheet())["pack"], "the worn pack sold is the GM's to settle")
        a = self.basket([("Great pack (pack 12)", 1)], carried=full)
        self.assertEqual((a["spill"], a["carry"]["pack"]), (0, carry.read(sheet(carried=full))["pack"]))


class Rules(unittest.TestCase):
    def test_the_numbers_are_the_rules(self):
        rules = (ENGINE / "Rules" / "Core Rules.md").read_text(encoding="utf-8")
        gear = rules[rules.index("## 14. Gear"):rules.index("## 15.")]
        words = {4: "4", 2: "2", 5: "five", 10: "ten"}
        for said in (f"| {words[carry.READY_ROOM]} slots |", "A satchel is 4, a pack 8, a great pack 12", "the pack's size + Might",
                     f"A **bulky** thing takes {words[carry.BULKY]}", f"pack {words[carry.STACK]} to a slot",
                     f"Past {words[carry.SMALL_FREE]} small things, every {words[carry.SMALL_PER]} more take a slot",
                     f"up to {words[carry.ARMS_ROOM]} slots of things"):
            self.assertIn(said, gear)


if __name__ == "__main__":
    unittest.main()
