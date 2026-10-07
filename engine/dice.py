"""The dice. Every random result in a narrative comes from here, never from the GM's head.

    gm roll 2d6+3 "what it's for"
    gm check +5 13 "Kendrick swings at the goblin" [--edge | --setback]
    gm attack +5 13 1d8+2 "Kendrick swings at the goblin" [--armor 1] [--edge | --setback]
    gm fate likely "Is the gate guarded tonight?"

Grades and odds are defined in Rules/Core Rules.md; the tables here have to match it.
"""

import re
import secrets
import sys

RNG = secrets.SystemRandom()

GRADES = ["Disaster", "Failure", "Partial", "Success", "Critical"]
ODDS = {"certain": 90, "likely": 70, "even": 50, "unlikely": 30, "remote": 10}
TERM = re.compile(r"([+-]?)(?:(\d*)d(\d+)|(\d+))")


def die(sides):
    return RNG.randint(1, sides)


def signed(n):
    return f"+{n}" if n >= 0 else str(n)


def parse(expr):
    """'2d6+3' -> [(sign, count, sides)] for dice and [(sign, n, 0)] for constants."""
    compact = expr.replace(" ", "").lower()
    terms, pos = [], 0
    for m in TERM.finditer(compact):
        if m.start() != pos:
            break
        pos = m.end()
        sign = -1 if m.group(1) == "-" else 1
        if m.group(3):
            terms.append((sign, int(m.group(2) or 1), int(m.group(3))))
        else:
            terms.append((sign, int(m.group(4)), 0))
    if pos != len(compact) or not terms:
        sys.exit(f"Can't read dice expression: {expr!r}. Examples: d20, 2d6+3, 1d8-1")
    return terms


def roll(expr, crit=False):
    """(total, breakdown). A critical adds the most each die could show on top of what's rolled."""
    total, parts = 0, []
    for sign, n, sides in parse(expr):
        if sides:
            faces = [die(sides) for _ in range(n)]
            sub = sum(faces) + (n * sides if crit else 0)
            parts.append(("-" if sign < 0 else "") + "[" + ",".join(map(str, faces)) + "]" + (f"+{n * sides} crit" if crit else ""))
        else:
            sub = n
            parts.append(signed(sign * n))
        total += sign * sub
    return total, " ".join(parts)


def d20(edge=False, setback=False):
    """(kept face, text). Edge and setback cancel; otherwise two dice, keep the high or the low."""
    if edge == setback:
        face = die(20)
        return face, f"d20({face})"
    a, b = die(20), die(20)
    face = max(a, b) if edge else min(a, b)
    return face, f"d20({a},{b} {'edge' if edge else 'setback'} keeps {face})"


def grade(face, total, target):
    margin = total - target
    step = 4 if margin >= 10 else 3 if margin >= 0 else 2 if margin >= -4 else 1 if margin >= -9 else 0
    if face == 20:
        step = min(step + 1, 4)
    if face == 1:
        step = max(step - 1, 0)
    return GRADES[step], margin


def check(bonus, target, edge=False, setback=False):
    """(grade, text) for d20 + bonus against a difficulty or a defense."""
    face, shown = d20(edge, setback)
    total = face + bonus
    result, margin = grade(face, total, target)
    natural = " natural 20" if face == 20 else " natural 1" if face == 1 else ""
    return result, f"{shown} {signed(bonus)} = {total} vs {target} -> {result} (margin {signed(margin)}{natural})"


def attack(bonus, defense, damage, armor=0, edge=False, setback=False):
    """(grade, lines). A Partial lands half; a Critical adds the dice's maximum; armor comes off last."""
    result, text = check(bonus, defense, edge, setback)
    lines = [text]
    if result in ("Disaster", "Failure"):
        lines.append("no damage")
        return result, lines
    rolled, shown = roll(damage, crit=result == "Critical")
    dealt = rolled // 2 if result == "Partial" else rolled
    floor = 0 if result == "Partial" else 1
    final = max(dealt - armor, floor)
    steps = f"damage {damage}: {shown} = {rolled}"
    if result == "Partial":
        steps += f", halved {dealt}"
    if armor:
        steps += f", armor {armor}"
    lines.append(f"{steps} -> {final}")
    return result, lines


def fate(odds):
    """(answer, text) for a yes/no question about the world. odds is a name in ODDS or a percent."""
    key = str(odds).lower().rstrip("%")
    if key in ODDS:
        chance = ODDS[key]
    elif key.isdigit() and 1 <= int(key) <= 99:
        chance = int(key)
    else:
        sys.exit(f"Odds are one of: {', '.join(ODDS)}, or a percent from 1 to 99.")
    face = die(100)
    if face <= chance:
        answer = "Yes, and more" if face <= max(chance // 5, 1) else "Yes"
    else:
        answer = "No, and worse" if face > 100 - max((100 - chance) // 5, 1) else "No"
    return answer, f"d100({face}) vs {chance}% -> {answer}"
