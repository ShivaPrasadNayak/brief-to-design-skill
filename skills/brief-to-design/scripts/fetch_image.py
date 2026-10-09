#!/usr/bin/env python3
"""Find and download openly licensed photos from Openverse (Flickr, Wikimedia, etc.), keeping credits.

    python fetch_image.py "rice terraces mist" --out assets/ --n 6             # search, print candidates
    python fetch_image.py "rice terraces mist" --out assets/ --n 6 --download  # also download them
    python fetch_image.py --id <openverse-id> --out assets/ --as hero.jpg      # download one chosen result

Every download is appended to <out>/CREDITS.json (title, creator, license, source URL) so the
deliverable can carry attribution. Defaults to licenses that allow commercial use and modification
(cc0, pdm, by, by-sa). No API key needed; anonymous use is rate-limited.

Always LOOK at a downloaded image before placing it: search relevance is noisy.
"""
import argparse
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://api.openverse.org/v1/images/"
UA = {"User-Agent": "brief-to-design-skill/1.0 (image search for design work)"}


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30)


def search(q, n, orientation, licenses, min_width=1000, source=None):
    params = {"q": q, "page_size": max(n * 4, 20), "license": licenses, "mature": "false"}
    if orientation:
        params["aspect_ratio"] = {"landscape": "wide", "portrait": "tall", "square": "square"}[orientation]
    if source:
        params["source"] = source
    data = json.load(get(API + "?" + urllib.parse.urlencode(params)))
    # Keep slide/hero-usable sizes; many records lack size metadata, so keep unknowns (checked after download).
    # Flickr serves 1024px "large" files; Wikimedia often full resolution (use --source wikimedia for hero shots).
    res = [r for r in data.get("results", []) if (r.get("width") or min_width) >= min_width]
    res.sort(key=lambda r: -(r.get("width") or 0))
    return res[:n]


def credit(r):
    lic = f"CC {r['license'].upper()} {r.get('license_version') or ''}".strip() if r["license"] not in ("cc0", "pdm") else r["license"].upper()
    return {"id": r["id"], "title": r.get("title"), "creator": r.get("creator"), "license": lic,
            "license_url": r.get("license_url"), "source": r.get("foreign_landing_url"), "file": None,
            "line": f"“{r.get('title') or 'Untitled'}” by {r.get('creator') or 'unknown'}, {lic}"}


def download(r, out: Path, name=None):
    ext = (r.get("filetype") or Path(urllib.parse.urlparse(r["url"]).path).suffix.lstrip(".") or "jpg").lower()
    dest = out / (name or f"{r['id'][:8]}.{ext}")
    dest.write_bytes(get(r["url"]).read())
    try:
        from PIL import Image as _I
        if _I.open(dest).width < 1000:
            print(f"  note: {dest.name} is only {_I.open(dest).width}px wide — use small or skip", file=sys.stderr)
    except Exception:
        pass
    try:  # originals are often 6000px+; 2400px is plenty for a 4K slide and keeps decks small
        from PIL import Image
        im = Image.open(dest)
        if im.width > 2400:
            im = im.convert("RGB")
            im.thumbnail((2400, 2400))
            dest = dest.with_suffix(".jpg")
            im.save(dest, quality=85)
    except Exception:
        pass
    c = credit(r)
    c["file"] = dest.name
    log = out / "CREDITS.json"
    entries = json.loads(log.read_text()) if log.exists() else []
    entries = [e for e in entries if e["file"] != dest.name] + [c]
    log.write_text(json.dumps(entries, indent=2))
    return dest


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("query", nargs="?")
    ap.add_argument("--id")
    ap.add_argument("--out", default="assets")
    ap.add_argument("--as", dest="name")
    ap.add_argument("--n", type=int, default=6)
    ap.add_argument("--orientation", choices=["landscape", "portrait", "square"])
    ap.add_argument("--licenses", default="cc0,pdm,by,by-sa")
    ap.add_argument("--min-width", type=int, default=1000, help="1600+ for full-bleed slides")
    ap.add_argument("--source", help="e.g. wikimedia (full-res originals), flickr")
    ap.add_argument("--download", action="store_true")
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)

    if a.id:
        r = json.load(get(f"{API}{a.id}/"))
        print(download(r, out, a.name))
        return
    if not a.query:
        sys.exit("give a query or --id")
    results = search(a.query, a.n, a.orientation, a.licenses, a.min_width, a.source)
    if not results:
        sys.exit(f"no results >= {a.min_width}px wide; broaden the query or lower --min-width")
    for r in results:
        line = f"{r['id']}  {r.get('width')}x{r.get('height')}  {credit(r)['line']}"
        if a.download:
            line += f"  -> {download(r, out)}"
        print(line)


if __name__ == "__main__":
    main()
