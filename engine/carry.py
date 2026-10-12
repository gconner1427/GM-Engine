"""What a character carries, counted in slots (Core Rules §14, "Carrying").

One reading of the Character Sheet's gear lines, for everything that needs it: `gm carry` prints it for
the GM, and the play window draws its Inventory tab and its shop's room from it, so the two can't disagree.

    read(sheet_text)                      the things in each place, their slots, the rooms, what is over
    arrange(sheet_text, moves, ...)       the same, as it would stand after these moves and this basket
    wares(sheet_text)                     a shop's shelves, each ware with its size
    report(carry)                         what gm carry prints

It takes text and gives back plain data: it opens no file and knows nothing of narratives. The numbers
below are Core Rules §14's, and tests/test_carry.py fails if the two stop agreeing. A thing's size is only
ever what the sheet marks it as: (small), (bulky), (armload). Nothing is guessed from a name.

A sheet that gives its pack no size, `(pack N)`, was made before the rule and is not counted at all.
"""

import math
import re

READY_ROOM = 4
ARMS_ROOM = 2
BULKY = 2
STACK = 5          # like things written ×N, to a slot
SMALL_FREE = 10    # small things carried before they count
SMALL_PER = 5      # and this many to a slot after that
MOST = 999         # no count or pack on a sheet is read as more than this
PACK_MARK = re.compile(r"\(pack\s+(\d+)\)", re.I)

A = re.ASCII   # every pattern here: the play window read these lines first, and its \d, \w and \b are ASCII
I = re.ASCII | re.IGNORECASE
PLACES = (("worn", "wearing"), ("ready", "ready"), ("ready", "in hand"), ("pack", "carried"), ("arms", "in arms"),
          ("kept", "kept elsewhere"))
TITLES = {"worn": "Wearing", "ready": "Ready", "pack": "Carried", "arms": "In arms", "dropped": ""}
COUNTED = ("ready", "pack", "arms")   # where a thing takes room; Worn and Kept elsewhere never count
SIZES = ("small", "bulky", "armload")
WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
         "ten": 10, "eleven": 11, "twelve": 12, "dozen": 12}

TAG = re.compile(r"[ \t]*\[(?:Setup|GM|Off S\d+|S\d+)\]", A)
ENTRY = re.compile(r"^\s*[-*]\s+\*\*(.+?)\*\*:?\s*(.*)$", A)
BLANK = re.compile(r"^\(|^(unknown|none|nothing|n/a)\b", I)
ASIDE = re.compile(r"\s*\(((?:[^()]|\([^()]*\))*)\)", A)
LEAD = re.compile(r"^(and|plus)\s+", I)
ARTICLE = re.compile(r"^(an?|the|some)\s+", I)
WHERE = re.compile(r"^(.+?)\s+((?:with|without|in|on|at|over|under|through|beside|inside|around|across|cut|drying|"
                   r"hung|hanging|slung|tucked|tied|strung|bloused|wrapped)\s.+)\Z", I)
TRAILS = re.compile(r"^(not|still|now|with|without|in|on|at|by|over|under|through|beside|inside|around|across|tied|"
                    r"strung|hung|hanging|slung|tucked|which|that)\b", I)
NUMBERED = re.compile(r"^(\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|a dozen)\s+(.+)\Z", I)
MEASURE = re.compile(r"^(\w+)\s+of\s+(.+)\Z", A)
TIMES = re.compile(r"^(.+?)\s*[x×]\s*(\d+)\Z", I)
MANY = re.compile(r"^([x×]?)\s*(\d+)\Z", I)
ARMOR = re.compile(r"^(?:(?:light|medium|heavy)\s+)?armou?r,?\s*(\d)\Z", I)
PACK_ASIDE = re.compile(r"^pack\s+(\d+)\Z", I)
SENTENCE = re.compile(r"\.\s+(?=[A-Z])", A)
SEMI = re.compile(r";", A)
COMMA = re.compile(r",", A)
AND = re.compile(r"\s+and\s+(?=(?:an?|the|her|his|their|my|your|some)\s)", I)


# ---- reading the sheet -------------------------------------------------------

def part(text, heading):
    """The '## heading' section, without its heading, up to the next '## ' or a rule."""
    m = re.search(rf"^## {re.escape(heading)}[ \t]*$", text, re.M)
    if not m:
        return ""
    rest = text[m.end():]
    end = re.search(r"^(## |---\s*$)", rest, re.M)
    return (rest[:end.start()] if end else rest).strip()


def entries(sec):
    """(name, text) for each '- **Name:** text' line."""
    out = []
    for line in sec.split("\n"):
        m = ENTRY.match(line)
        if m:
            out.append((re.sub(r":$", "", m.group(1)).strip(), TAG.sub("", m.group(2)).strip()))
    return out


def listed(sec, title):
    """The entries under one '### Title' of a section."""
    m = re.search(rf"^### {re.escape(title)}[ \t]*$", sec, re.M | re.I)
    if not m:
        return []
    rest = sec[m.end():]
    end = re.search(r"^### ", rest, re.M)
    return entries(rest[:end.start()] if end else rest)


def blank(value):
    return not value or bool(BLANK.search(value.strip()))


def might_of(text):
    """Might from the Attributes table, or None when it isn't there to read."""
    rows = [l for l in part(text, "Attributes").split("\n") if l.lstrip().startswith("|") and not set(l.strip()) <= set("|:- \t")]
    if len(rows) < 2:
        return None
    cells = lambda row: [c.strip() for c in re.sub(r"^\||\|$", "", row.strip()).split("|")]
    for name, value in zip(cells(rows[0]), cells(rows[1])):
        if name.lower() == "might":
            m = re.search(r"[-+]?\d+", value.replace("−", "-"), A)
            return int(m.group()) if m else None
    return None


def cut_top(text, at):
    """Split where `at` matches outside parentheses."""
    out, depth, start, i = [], 0, 0, 0
    while i < len(text):
        c = text[i]
        if c == "(":
            depth += 1
        elif c == ")":
            depth = max(0, depth - 1)
        elif not depth:
            m = at.match(text, i)
            if m and m.group():
                out.append(text[start:i])
                start = i = m.end()
                continue
        i += 1
    out.append(text[start:])
    return [s.strip() for s in out if s.strip()]


def slots_of(size, form, count):
    """The room one entry takes. A stack packs five to a slot; a count in front is that many separate things."""
    n = max(count, 1) if form in ("stack", "each") else 1
    if size == "small":
        return 0
    if size == "armload":
        return ARMS_ROOM * n
    if size == "bulky":
        return BULKY * n
    return math.ceil(n / STACK) if form == "stack" else n


def thing(text, after="", marks=True):
    """One thing a gear line names: what it is, how many, how big, and what's said about it.
    With marks off (a sheet that isn't counted) a size mark is only something said about it."""
    asides, notes = [], []
    name = ASIDE.sub(lambda m: asides.append(m.group(1).strip()) or "", text)
    written = LEAD.sub("", re.sub(r"\.\Z", "", name).strip())
    name = ARTICLE.sub("", written)
    size, pack, two = "ordinary", None, False
    if marks:
        kept = []
        for aside in asides:
            said = []
            for piece in (p.strip() for p in aside.split(",")):
                m = PACK_ASIDE.match(piece)
                if piece.lower() in SIZES and size == "ordinary":
                    size = piece.lower()
                elif m and pack is None:
                    pack = min(int(m.group(1)), MOST)
                else:
                    said.append(piece)
                    two = two or piece.lower() == "two hands"
            if said:
                kept.append(aside if len(said) == aside.count(",") + 1 else ", ".join(said))
        asides = kept
    count, chip, form = 0, "", "one"
    m = WHERE.match(name)
    if m:
        name = m.group(1)
        notes.append(m.group(2))
    m = NUMBERED.match(name)
    if m:
        measure = MEASURE.match(m.group(2))
        if measure:
            chip, name, form = m.group(1) + " " + measure.group(1), measure.group(2), "measure"
        else:
            word = re.sub(r"^a ", "", m.group(1).lower())
            count, name, form = min(int(word), MOST) if word.isdigit() else WORDS.get(word, 0), m.group(2), "each"
    if not count:
        m = TIMES.match(name)
        if m:   # "lamp oil x2"
            name, count, form = m.group(1), min(int(m.group(2)), MOST), "stack"
    for aside in asides:
        many, armor = MANY.match(aside), ARMOR.match(aside)
        if many and not count:   # "(2)", "(x2)": how many, not something said about it
            count, form = min(int(many.group(2)), MOST), "stack" if many.group(1) else "each"
        elif armor and not chip:
            chip = "Armor " + armor.group(1)
        else:
            notes.append(aside)
    if after:
        notes.append(after)
    return {"id": "", "name": name[:1].upper() + name[1:], "written": written, "count": count if count > 1 else 0,
            "chip": chip, "notes": notes, "form": form, "size": size, "slots": slots_of(size, form, count),
            "is_pack": False, "from": "", "pack": pack, "two": two}


def things(text, marks=True):
    """A gear line into its things."""
    out = []
    for sentence in cut_top(text, SENTENCE):
        parts, start = cut_top(sentence, SEMI), len(out)
        if len(parts) > 1:   # a semicolon list: each part is a thing, and what follows its comma is about it
            for one in parts:
                head, *rest = cut_top(one, COMMA) or [""]
                named = cut_top(head, AND)
                for i, n in enumerate(named):
                    out.append(thing(n, re.sub(r"\.\Z", "", ", ".join(rest)) if i == len(named) - 1 else "", marks))
            continue
        lead = ""
        for one in cut_top(sentence, COMMA):
            bit = re.sub(r"\.\Z", "", re.sub(r"^and\s+", "", one, flags=I))
            if TRAILS.match(bit):   # not a thing: it's about the one before it (or the one after, when it comes first)
                if len(out) > start:
                    out[-1]["notes"].append(bit)
                else:
                    lead = lead + ", " + bit if lead else bit
                continue
            for i, n in enumerate(cut_top(bit, AND)):
                out.append(thing(n, "" if i else lead, marks))
                lead = ""
        if lead:
            out.append(thing(lead, "", marks))
    return [t for t in out if t["name"]]


def parse(sheet_text):
    """The gear lines as they are written, before anything is counted."""
    text = (sheet_text or "").replace("\r\n", "\n")
    gear = part(text, "Gear")
    counted = bool(PACK_MARK.search(gear))
    lines, seen, trouble = [], set(), []
    for n, (name, said) in enumerate(entries(gear)):
        if re.match(r"money$", name, I):
            continue
        where = re.match(r"^(.*?)\s*\((.*)\)\Z", name, A)
        title, hint = (where.group(1), where.group(2)) if where else (name, "")
        key = next((k for k, starts in PLACES if title.lower().startswith(starts) and k not in seen), "")
        seen.add(key)
        found = [] if blank(said) else things(said, counted)
        for i, t in enumerate(found):
            t["id"] = f"{key or 'x' + str(n)}:{i}"
        lines.append({"key": key, "title": title, "hint": hint, "text": said, "things": found})
    model = {"counted": counted, "lines": lines, "might": 0, "trouble": trouble}
    if not counted:
        return model
    might = might_of(text)
    if might is None:
        trouble.append("Might could not be read from the Attributes table; it is taken as 0.")
    model["might"] = might or 0
    packs = 0
    for line in lines:
        for t in line["things"]:
            if t["pack"] is not None and line["key"] == "worn":
                packs += 1
                t["is_pack"] = packs == 1
            elif t["pack"] is not None and line["key"] in COUNTED:
                trouble.append(f'"{t["written"]}" is a pack that is not worn; it is counted as a thing.')
            if line["key"] in COUNTED and t["two"] and t["size"] == "ordinary":
                trouble.append(f'"{t["written"]}" is two hands and has no size mark; it is counted as 1.')
            if line["key"] in ("ready", "pack") and t["size"] == "armload":
                trouble.append(f'"{t["written"]}" is marked armload and is on {line["title"]}; it can only be carried in arms.')
    if packs > 1:
        trouble.append("Two packs are on Wearing; the first is counted.")
    return model


def line_of(model, key):
    return next((l for l in model["lines"] if l["key"] == key), None)


def tally(model):
    """The count: what read() and arrange() both answer with."""
    public = lambda t: {k: v for k, v in t.items() if k not in ("pack", "two")}
    lines = [dict(l, things=[public(t) for t in l["things"]]) for l in model["lines"]]
    if not model["counted"]:
        return {"counted": False, "lines": lines}
    held = {key: (line_of(model, key) or {"things": []})["things"] for key in COUNTED + ("worn",)}
    used = {key: sum(t["slots"] for t in held[key]) for key in COUNTED}
    small = sum(max(t["count"], 1) for key in COUNTED for t in held[key] if t["size"] == "small")
    extra = math.ceil(max(0, small - SMALL_FREE) / SMALL_PER)
    worn = next((t for t in held["worn"] if t["is_pack"]), None)
    size = worn["pack"] if worn else 0
    room = max(0, size + model["might"]) if size else 0
    big = any(t["size"] == "armload" for t in held["arms"])
    stay = {key: sum(t["slots"] for t in held[key] if not t["from"]) for key in COUNTED}   # without what a move brought
    stays = sum(max(t["count"], 1) for key in COUNTED for t in held[key] if t["size"] == "small" and not t["from"])
    stay["pack"] += math.ceil(max(0, stays - SMALL_FREE) / SMALL_PER)
    coming = {key: max(0, used[key] + (extra if key == "pack" else 0) - stay[key]) for key in COUNTED}
    return {"counted": True, "lines": lines,
            "ready": {"used": used["ready"], "room": READY_ROOM, "over": used["ready"] > READY_ROOM, "coming": coming["ready"]},
            "pack": {"used": used["pack"] + extra, "room": room, "over": used["pack"] + extra > room, "coming": coming["pack"],
                     "name": worn["name"] if worn else "", "written": worn["written"] if worn else "",
                     "size": size, "might": model["might"]},
            "arms": {"used": used["arms"], "room": ARMS_ROOM, "laden": bool(held["arms"]), "coming": coming["arms"],
                     "over": used["arms"] > ARMS_ROOM or (big and len(held["arms"]) > 1)},
            "small": {"count": small, "free": SMALL_FREE, "slots": extra},
            "trouble": list(model["trouble"])}


def read(sheet_text):
    """The sheet's gear, counted. Never raises, whatever the text."""
    try:
        return tally(parse(sheet_text))
    except Exception:   # a sheet half written, or not a sheet at all: nothing to count, and the next reading corrects it
        return {"counted": False, "lines": []}


def report(carry):
    """What gm carry prints."""
    if not carry.get("counted"):
        return "Not counted: this sheet gives its pack no size."
    ready, pack, arms, small = carry["ready"], carry["pack"], carry["arms"], carry["small"]
    said = ARTICLE.sub("", pack["written"]) or "no pack"
    held = next((l["things"] for l in carry["lines"] if l["key"] == "arms"), [])
    out = [f"Ready: {ready['used']} of {ready['room']}",
           f"Pack: {pack['used']} of {pack['room']}  ({said}, size {pack['size']}, Might {pack['might']:+d})" if pack["size"]
           else f"Pack: {pack['used']} of 0  (no pack)",
           f"Small things: {small['count']} ({small['free']} carried free)"
           + (f"; the {small['count'] - small['free']} past that take {small['slots']} of the pack's slots" if small["slots"] else ""),
           "In arms: " + (", ".join(t["written"] for t in held) + f" ({arms['used']} of {arms['room']})" if held else "nothing")]
    for name, place in (("Ready", ready), ("Pack", pack)):
        if place["over"]:
            out.append(f"{name} is over by {place['used'] - place['room']}.")
    if arms["over"]:
        out.append("In arms is over: more than two arms can hold.")
    if arms["laden"]:
        out.append("Laden: arms full.")
    return "\n".join(out + carry["trouble"])


# ---- what if: moves made in the window, and a shop's basket ------------------------------

TO = ("ready", "pack", "worn", "arms", "dropped")


def find(model, tid):
    for line in model["lines"]:
        for t in line["things"]:
            if t["id"] == tid:
                return line, t
    return None, None


def place(model, key):
    """The line for one place, made if the sheet has none (In arms is only there while something is carried so)."""
    line = line_of(model, key)
    if not line:
        line = {"key": key, "title": TITLES[key], "hint": "", "text": "", "things": []}
        model["lines"].append(line)
    return line


def refusal(code, need=0, room=0):
    return {"code": code, "need": need, "room": max(0, room)}


def big(model):
    """Whether the arms hold one thing too big to pack, which is all they can hold."""
    return any(t["size"] == "armload" for t in place(model, "arms")["things"])


def put(model, t, here, there):
    """Take a thing from one line to another. Back on its own line it goes where the sheet has it."""
    home = t["from"] or here["key"]
    here["things"].remove(t)
    if there["key"] != home:
        t["from"] = home
        return there["things"].append(t)
    t["from"] = ""
    at = int(t["id"].rsplit(":", 1)[1])
    stayed = [o for o in there["things"] if not o["from"] and int(o["id"].rsplit(":", 1)[1]) < at]
    there["things"].insert(len(stayed), t)


def allowed(model, tid, to):
    """Whether one thing may go to one place as the arrangement stands: None, or why not. Every move made
    and every place offered for an opened thing is judged here, so the two can't disagree."""
    line, t = find(model, tid)
    if not t or to not in TO:
        return refusal("gone")
    home = t["from"] or line["key"]
    if home in ("kept", "", "shop"):
        return refusal("fixed")
    if t["is_pack"]:
        return refusal("the_pack")
    if line["key"] == to:
        return refusal("here")
    if to == "dropped":
        return None
    if to == "worn":
        if not t["chip"].startswith("Armor"):   # only armor is put on from the window; what was worn goes back on
            return None if home == "worn" else refusal("not_armor")
        on = any(w["chip"].startswith("Armor") for w in place(model, "worn")["things"])
        return refusal("not_worn") if on else None
    if t["size"] == "armload" and to in ("ready", "pack"):
        return refusal("too_big")
    before = tally(model)
    free = lambda key: max(0, before[key]["room"] - before[key]["used"])
    if to == "arms":
        held = place(model, "arms")["things"]
        if big(model) or (t["size"] == "armload" and held) or t["slots"] > free("arms"):
            return refusal("arms_full", t["slots"], 0 if big(model) else free("arms"))
    if to == "ready" and t["slots"] > free("ready"):
        return refusal("full", t["slots"], free("ready"))
    there, at, was = place(model, to), line["things"].index(t), t["from"]
    put(model, t, line, there)
    after = tally(model)["pack"]
    there["things"].remove(t)   # and back exactly where it was: the question moves nothing
    line["things"].insert(at, t)
    t["from"] = was
    if after["used"] > after["room"] and after["used"] > before["pack"]["used"]:   # the small things' charge is the pack's too
        return refusal("full", after["used"] - before["pack"]["used"], free("pack"))
    return None


def moved(model, moves):
    """Every move in the order made, each on what the ones before left. Returns why the first that can't be
    done can't, with its place in the list, or None."""
    for at, m in enumerate(moves or ()):
        m = m if isinstance(m, dict) else {}
        tid, to = str(m.get("id", "")), m.get("to")
        why = allowed(model, tid, to)
        if why and why["code"] != "here":
            return dict(why, at=at)
        if not why:
            line, t = find(model, tid)
            put(model, t, line, place(model, to))
    return None


def unmarked(name):
    """A ware's name as the shelf shows it: without its size mark."""
    def keep(m):
        said = [p.strip() for p in m.group(1).split(",")]
        said = [p for p in said if p.lower() not in SIZES and not PACK_ASIDE.match(p)]
        return f" ({', '.join(said)})" if said else ""
    return ASIDE.sub(keep, name).strip()


def same(a, b):
    return ARTICLE.sub("", a.strip()).lower() == ARTICLE.sub("", b.strip()).lower()


def owned(model, name):
    """The thing on the sheet a keeper would buy, by its name: from the pack first."""
    for key in ("pack", "ready", "arms", "worn", "kept"):
        for t in (line_of(model, key) or {"things": []})["things"]:
            if same(t["name"], thing(name)["name"]):
                return t
    return None


def shelves(model, text):
    shop = part(text, "Shop")
    name = next((m.group(1) for m in [re.search(r"^(?:- )?\*\*Name:\*\*[ \t]*(.*)$", shop, re.M)] if m), "")
    if not model["counted"] or blank(TAG.sub("", name).strip()):
        return {"buy": [], "sell": []}
    out = {"buy": [], "sell": []}
    for side, title in (("buy", "For sale"), ("sell", "Will buy")):
        for written, _ in listed(shop, title):
            t = thing(written)
            ware = {"written": written, "name": unmarked(written), "size": t["size"], "form": t["form"], "count": t["count"],
                    "slots": 0 if t["pack"] is not None else t["slots"], "is_pack": t["pack"] is not None}
            if side == "sell":
                has = owned(model, written)
                ware.update(id=has["id"] if has else "", size=has["size"] if has else "ordinary",
                            slots=slots_of(has["size"], "one", 0) if has else 1)
            out[side].append(ware)
    return out


def wares(sheet_text):
    """A shop's shelves as the counter reads them: {"buy": what is for sale, "sell": what the keeper would take},
    each ware with its size and the room one of it takes. Both empty with no shop, or on a sheet not counted."""
    try:
        text = (sheet_text or "").replace("\r\n", "\n")
        return shelves(parse(text), text)
    except Exception:
        return {"buy": [], "sell": []}


def number(value):
    try:
        return max(0, int(value))
    except (TypeError, ValueError):
        return 0


def trade(model, shelf, buy, sell):
    """A basket, settled as the GM will settle it: what is sold leaves and frees its room; what is bought goes to
    the pack, like things joining a stack already there; what the pack can't take is carried out in the arms.
    Returns (why not, or None; the slots that went to the arms)."""
    named = lambda side, b: next((w for w in shelf[side] if isinstance(b, dict) and w["written"] == b.get("written")), None)
    for s in sell or ():
        w, n = named("sell", s), number(s.get("n") if isinstance(s, dict) else 0)
        line, t = find(model, w["id"]) if w and w["id"] else (None, None)
        if not t or not n or t["is_pack"]:   # the worn pack sold is the GM's to settle, like one bought
            continue
        has = max(t["count"], 1)
        if t["form"] in ("stack", "each") and has > n:
            t["count"] = has - n if has - n > 1 or t["form"] == "stack" else 0
            t["slots"] = slots_of(t["size"], t["form"], has - n)
        else:
            line["things"].remove(t)
    start = tally(model)
    pack, arms = place(model, "pack"), place(model, "arms")
    free = 0 if big(model) else max(0, ARMS_ROOM - start["arms"]["used"])
    pieces, wanted = [], []
    for i, b in enumerate(buy or ()):
        w, n = named("buy", b), number(b.get("n") if isinstance(b, dict) else 0)
        if w and n and not w["is_pack"]:   # which pack is worn after the sale is the GM's to settle
            wanted.append((i, w, n))
    for i, w, n in wanted:   # small wares first: they take no room of their own, and past ten the pack pays
        if w["size"] == "small":
            units = n * (max(w["count"], 1) if w["form"] in ("stack", "each") else 1)
            pack["things"] += [dict(thing(w["written"]), id=f"buy:{i}.{k}", form="one", count=0, slots=0, **{"from": "shop"}) for k in range(units)]
    now = tally(model)["pack"]
    over = max(0, now["used"] - max(now["room"], start["pack"]["used"]))
    for i, w, n in wanted:
        if w["size"] == "small":
            continue
        new = lambda k, form, count: dict(thing(w["written"]), id=f"buy:{i}.{k}", form=form, slots=slots_of(w["size"], form, count),
                                          count=count if count > 1 or form == "stack" else 0, **{"from": "shop"})
        heap = next((t for t in pack["things"] if t["form"] == "stack" and same(t["name"], thing(w["written"])["name"])), None)
        if heap:   # like things that get used up join the stack already in the pack, if the pack then holds
            was, units = heap["count"], n * max(w["count"], 1) if w["form"] in ("stack", "each") else n
            heap["count"] = max(was, 1) + units
            heap["slots"] = slots_of(heap["size"], "stack", heap["count"])
            now = tally(model)["pack"]
            if now["used"] <= max(now["room"], start["pack"]["used"] + over):
                continue
            heap["count"], heap["slots"] = was, slots_of(heap["size"], "stack", max(was, 1))
        if w["form"] == "stack":
            pieces += [new(k, "stack", max(w["count"], 1)) for k in range(n)]
        else:
            pieces += [new(k, "one", 0) for k in range(n * (max(w["count"], 1) if w["form"] == "each" else 1))]
    spill = left = 0
    for t in sorted(pieces, key=lambda t: -t["slots"]):   # biggest first
        now = tally(model)
        if t["size"] != "armload":
            pack["things"].append(t)
            after = tally(model)["pack"]
            if after["used"] <= after["room"]:
                continue
            pack["things"].remove(t)
        if not big(model) and not (t["size"] == "armload" and arms["things"]) and t["slots"] <= ARMS_ROOM - now["arms"]["used"]:
            arms["things"].append(t)
            spill += t["slots"]
        else:
            left += t["slots"]
    return (dict(refusal("full", spill + left + over, free), at=-1) if left or over else None), spill


def arrange(sheet_text, moves, buy=(), sell=(), fit=""):
    """The count as it would stand after these moves and this basket: {"carry": ...}, with "fits" (each of the
    five places for the thing `fit` names: None where it may go, or why not) and "spill" (the slots a basket puts
    in the arms) when asked; or {"refused": {"code", "need", "room", "at"}} for the first move, or the basket
    (at -1), that can't be done. It changes nothing: it is a question, and it never raises."""
    try:
        text = (sheet_text or "").replace("\r\n", "\n")
        model = parse(text)
        if not model["counted"]:
            return {"carry": tally(model)}
        sheet = {l["key"] for l in model["lines"]}
        why = moved(model, moves if isinstance(moves, (list, tuple)) else [])
        if why:
            return {"refused": why}
        out = {}
        if buy or sell:
            why, out["spill"] = trade(model, shelves(parse(text), text), buy if isinstance(buy, (list, tuple)) else [],
                                      sell if isinstance(sell, (list, tuple)) else [])
            if why:
                return {"refused": why}
        if fit:
            out["fits"] = {to: allowed(model, str(fit), to) for to in TO}
        model["lines"] = [l for l in model["lines"] if l["key"] in sheet or l["things"]]
        model["lines"].sort(key=lambda l: l["key"] == "dropped")   # what is put down comes last
        return dict(out, carry=tally(model))
    except Exception:
        return {"refused": dict(refusal("gone"), at=-1)}
