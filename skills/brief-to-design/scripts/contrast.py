#!/usr/bin/env python3
"""WCAG contrast check for a palette, with a nudged fix for every failing pair.

    python contrast.py 0A1630 F3F6FB 2F6BFF          # every pair among these colours
    python contrast.py tokens.json                    # {"directions": [{"name":..,"tokens":{..}}]} or {"tokens":{..}}

For a tokens file, pairs checked are the ones that actually occur:
    text, muted on bg and surface; on-primary on primary; accent on bg (as large text / UI).
Thresholds: 4.5 body text, 3.0 large text (>= 24px, or >= 18.5px bold) and UI marks.
"""
import json
import sys
from itertools import permutations
from pathlib import Path


def lum(hex_):
    h = hex_.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def ratio(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def nudge(fg, bg, target):
    """Darken or lighten fg (whichever direction moves away from bg) until it passes."""
    h = fg.lstrip("#")
    rgb = [int(h[i:i + 2], 16) for i in (0, 2, 4)]
    darker = lum(bg) > 0.18
    for step in range(1, 101):
        t = step / 100
        c = [round(v * (1 - t)) if darker else round(v + (255 - v) * t) for v in rgb]
        cand = "".join(f"{v:02X}" for v in c)
        if ratio(cand, bg) >= target:
            return cand
    return None


def check(pairs):
    fails = 0
    for label, fg, bg, need in pairs:
        r = ratio(fg, bg)
        ok = r >= need
        fails += not ok
        fix = "" if ok else f"  -> try {nudge(fg, bg, need)}"
        print(f"  {'PASS' if ok else 'FAIL'} {r:5.2f}:1 (need {need})  {label:<28} #{fg.lstrip('#')} on #{bg.lstrip('#')}{fix}")
    return fails


def token_pairs(t):
    t = {k.lower().replace("-", "_"): v.lstrip("#") for k, v in t.items() if isinstance(v, str) and len(v.lstrip("#")) == 6}
    p = []
    for bgk in ("bg", "background", "surface"):
        if bgk in t:
            for fgk, need in (("text", 4.5), ("muted", 4.5), ("muted_text", 4.5), ("primary", 3.0), ("accent", 3.0)):
                if fgk in t and fgk != bgk:
                    p.append((f"{fgk} on {bgk}", t[fgk], t[bgk], need))
    for base in ("primary", "dark", "bg_dark"):
        for on in dict.fromkeys((f"on_{base}", "on_dark" if base != "primary" else "on_primary")):
            if base in t and on in t:
                p.append((f"{on} on {base}", t[on], t[base], 4.5))
    if "accent" in t and "dark" in t:
        p.append(("accent on dark", t["accent"], t["dark"], 3.0))
    return p


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    total = 0
    if len(args) == 1 and Path(args[0]).exists():
        data = json.loads(Path(args[0]).read_text())
        dirs = data.get("directions") or [{"name": data.get("name", "palette"), "tokens": data.get("tokens", data)}]
        for d in dirs:
            print(d.get("name", "palette"))
            total += check(token_pairs(d["tokens"]))
    else:
        cols = [a.lstrip("#") for a in args]
        total = check([(f"#{a} / #{b}", a, b, 4.5) for a, b in permutations(cols, 2) if lum(a) < lum(b)])
    print(f"\n{total} failing pair(s)" if total else "\nall pairs pass")
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
