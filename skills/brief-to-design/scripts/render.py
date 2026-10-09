#!/usr/bin/env python3
"""Render any deliverable to page images so it can be inspected, plus a contact sheet.

    python render.py deck.pptx                 # PowerPoint -> PDF -> PNGs
    python render.py report.docx               # Word -> PDF -> PNGs
    python render.py deck.html                 # HTML deck (has data-deck) -> print PDF -> PNGs
    python render.py site.html --mode screen   # website: full-page desktop + mobile screenshots
    python render.py notes.md                  # pandoc -> HTML -> PDF -> PNGs
    python render.py lab.html --mode screen --width 1600   # direction lab board

Output goes to <out>/ (default: <name>-render/ next to the input):
    page-01.png ...        one per slide/page (or desktop.png / mobile.png in screen mode)
    contact.png            grid of all pages, for judging rhythm and variety at a glance
    qa.txt                 HTML only: overflowing elements, broken images, horizontal scroll

Renderers, in order of preference:
    .pptx/.docx  Microsoft PowerPoint/Word via AppleScript (true fidelity, real fonts),
                 else LibreOffice `soffice` if on PATH.
    .html/.md    Headless Google Chrome over the DevTools protocol (needs `websocket-client`);
                 falls back to Chrome's --print-to-pdf / --screenshot flags without the QA report.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    shutil.which("google-chrome") or "",
    shutil.which("google-chrome-stable") or "",
    shutil.which("chromium") or "",
    shutil.which("chromium-browser") or "",
    shutil.which("msedge") or "",
]
SOFFICE_CANDIDATES = [
    "/Applications/LibreOffice.app/Contents/MacOS/soffice",
    r"C:\Program Files\LibreOffice\program\soffice.exe",
]

# Finds the things a human reviewer would flag first. Runs inside the page.
QA_JS = r"""
(() => {
  const out = [];
  const label = el => {
    const t = (el.innerText || el.alt || '').trim().replace(/\s+/g, ' ').slice(0, 60);
    const slide = el.closest('[data-slide], section, .slide');
    const idx = slide ? [...document.querySelectorAll('[data-slide], .slide')].indexOf(slide) + 1 : 0;
    return (idx > 0 ? `slide ${idx}: ` : '') + `<${el.tagName.toLowerCase()}${el.className && typeof el.className === 'string' ? ' .' + el.className.split(' ')[0] : ''}> "${t}"`;
  };
  for (const el of document.querySelectorAll('body *')) {
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') continue;
    if (['SCRIPT','STYLE','svg','SVG','PATH'].includes(el.tagName)) continue;
    const clips = /(hidden|clip|auto|scroll)/.test(cs.overflow + cs.overflowX + cs.overflowY);
    if (clips && el.clientHeight > 0 && (el.scrollHeight > el.clientHeight + 2 || el.scrollWidth > el.clientWidth + 2)
        && el.innerText && el.innerText.trim().length) {
      const scaled = el.firstElementChild && getComputedStyle(el.firstElementChild).transform !== 'none';  // thumbnails of big canvases
      if (!scaled && !el.hasAttribute('data-qa-allow-overflow')) out.push('OVERFLOW  ' + label(el) + ` (${el.scrollWidth}x${el.scrollHeight} in ${el.clientWidth}x${el.clientHeight})`);
    }
    if (el.tagName === 'IMG' && el.complete && el.naturalWidth === 0) out.push('BROKEN IMG ' + (el.getAttribute('src') || '').slice(0, 80));
  }
  // Text that escapes its slide frame
  for (const s of document.querySelectorAll('[data-slide], .slide')) {
    const r = s.getBoundingClientRect();
    for (const el of s.querySelectorAll('h1,h2,h3,h4,p,li,span,figcaption,td,th')) {
      const e = el.getBoundingClientRect();
      if (e.width && (e.right > r.right + 1 || e.bottom > r.bottom + 1 || e.left < r.left - 1)) {
        out.push('OUTSIDE SLIDE ' + label(el)); break;
      }
    }
  }
  if (!document.querySelector('[data-deck]') && document.documentElement.scrollWidth > window.innerWidth + 1)
    out.push(`HORIZONTAL SCROLL page is ${document.documentElement.scrollWidth}px wide at ${window.innerWidth}px viewport`);
  const fonts = [...document.fonts].filter(f => f.status === 'error').map(f => f.family);
  if (fonts.length) out.push('FONT FAILED ' + [...new Set(fonts)].join(', '));
  return out;
})()
"""


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def office_to_pdf(src: Path, pdf: Path):
    app = {".pptx": "Microsoft PowerPoint", ".ppt": "Microsoft PowerPoint", ".potx": "Microsoft PowerPoint",
           ".docx": "Microsoft Word", ".doc": "Microsoft Word"}[src.suffix.lower()]
    if sys.platform == "darwin" and Path(f"/Applications/{app}.app").exists():
        # Sandboxed Office apps can silently stall on folders they haven't been granted (e.g. under
        # ~/Library); /tmp is always readable, so stage the file there and move the PDF back.
        stage = Path(tempfile.mkdtemp(prefix="cd-render-", dir="/tmp")).resolve()
        s_src, s_pdf = stage / src.name, stage / (src.stem + ".pdf")
        shutil.copy2(src, s_src)
        if app == "Microsoft PowerPoint":
            script = f'''with timeout of 280 seconds
tell application "Microsoft PowerPoint"
  open POSIX file "{s_src}"
  set p to active presentation
  save p in POSIX file "{s_pdf}" as save as PDF
  close p saving no
end tell
end timeout'''
        else:
            script = f'''with timeout of 280 seconds
tell application "Microsoft Word"
  open POSIX file "{s_src}"
  set d to active document
  save as d file name "{s_pdf}" file format format PDF
  close d saving no
end tell
end timeout'''
        r = run(["osascript", "-e", script], timeout=300)
        if s_pdf.exists():
            shutil.move(str(s_pdf), pdf)
            shutil.rmtree(stage, ignore_errors=True)
            return f"{app} (AppleScript)"
        shutil.rmtree(stage, ignore_errors=True)
        print(f"{app} export failed: {r.stderr.strip()}", file=sys.stderr)
    soffice = shutil.which("soffice") or shutil.which("libreoffice") or next((c for c in SOFFICE_CANDIDATES if Path(c).exists()), None)
    if soffice:
        run([soffice, "--headless", "--convert-to", "pdf", "--outdir", str(pdf.parent), str(src)], timeout=300)
        produced = pdf.parent / (src.stem + ".pdf")
        if produced.exists():
            produced.rename(pdf)
            return "LibreOffice (fonts may be substituted — fit checks approximate)"
    sys.exit("No Office renderer: on macOS install Microsoft Office; elsewhere install LibreOffice (free).")


def chrome_bin():
    for c in CHROME_CANDIDATES:
        if c and Path(c).exists():
            return c
    sys.exit("No Chromium browser found: install Google Chrome, Chromium or Microsoft Edge.")


class CDP:
    """Minimal DevTools-protocol client: enough to load a page, run JS, print and screenshot."""

    def __init__(self):
        import websocket  # websocket-client
        self.profile = tempfile.mkdtemp(prefix="cd-chrome-")
        self.proc = subprocess.Popen(
            [chrome_bin(), "--headless=new", "--remote-debugging-port=0", f"--user-data-dir={self.profile}",
             "--hide-scrollbars", "--no-first-run", "--no-default-browser-check", "--force-color-profile=srgb",
             "about:blank"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        port_file = Path(self.profile) / "DevToolsActivePort"
        for _ in range(100):
            if port_file.exists() and port_file.read_text().strip():
                break
            time.sleep(0.1)
        port = port_file.read_text().split()[0]
        targets = json.load(urllib.request.urlopen(f"http://127.0.0.1:{port}/json/list"))
        page = next(t for t in targets if t["type"] == "page")
        self.ws = websocket.create_connection(page["webSocketDebuggerUrl"], timeout=120, suppress_origin=True)
        self.i = 0

    def send(self, method, **params):
        self.i += 1
        self.ws.send(json.dumps({"id": self.i, "method": method, "params": params}))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get("id") == self.i:
                if "error" in msg:
                    raise RuntimeError(f"{method}: {msg['error']}")
                return msg.get("result", {})

    def eval(self, expr):
        r = self.send("Runtime.evaluate", expression=expr, awaitPromise=True, returnByValue=True)
        return r.get("result", {}).get("value")

    def load(self, url, width, height, mobile=False, media=None):
        self.send("Emulation.setDeviceMetricsOverride", width=width, height=height,
                  deviceScaleFactor=2 if mobile else 1, mobile=mobile)
        if media:
            self.send("Emulation.setEmulatedMedia", media=media)
        self.send("Page.enable")
        self.send("Page.navigate", url=url)
        for _ in range(200):
            if self.eval("document.readyState") == "complete":
                break
            time.sleep(0.1)
        # Fonts, images, and any reveal animations settle before we look.
        self.eval("Promise.race([document.fonts.ready, new Promise(r=>setTimeout(r,8000))])")
        self.eval("Promise.all([...document.images].map(i=>i.complete?1:new Promise(r=>{i.onload=i.onerror=r;setTimeout(r,8000)})))")
        self.eval("document.documentElement.classList.add('qa-render'); new Promise(r=>setTimeout(r,600))")

    def close(self):
        try:
            self.ws.close()
        finally:
            self.proc.terminate()
            shutil.rmtree(self.profile, ignore_errors=True)


def html_render(src: Path, out: Path, mode: str, width: int, height: int, desktop_only=False):
    import base64
    url = src.resolve().as_uri()
    try:
        cdp = CDP()
    except ImportError:
        return html_render_flags(src, out, mode, width, height)
    qa = []
    try:
        if mode == "print":
            # Print media lays every slide/page out at once, so QA sees all of them, not just the first.
            cdp.load(url, width, height, media="print")
            qa = cdp.eval(QA_JS) or []
            pdf = cdp.send("Page.printToPDF", printBackground=True, preferCSSPageSize=True,
                           displayHeaderFooter=False)
            (out / "render.pdf").write_bytes(base64.b64decode(pdf["data"]))
            pages = pdf_to_png(out / "render.pdf", out)
        else:
            pages = []
            views = [("desktop", width, height, False)] + ([] if desktop_only else [("mobile", 390, 844, True)])
            for name, w, h, mob in views:
                cdp.load(url, w, h, mobile=mob)
                qa += [f"[{name}] {q}" for q in (cdp.eval(QA_JS) or [])]
                full_h = int(cdp.eval("Math.max(document.documentElement.scrollHeight, document.body.scrollHeight)"))
                shot = cdp.send("Page.captureScreenshot", format="png", captureBeyondViewport=True,
                                clip={"x": 0, "y": 0, "width": w, "height": min(full_h, 16000), "scale": 1})
                p = out / f"{name}.png"
                p.write_bytes(base64.b64decode(shot["data"]))
                pages.append(p)
    finally:
        cdp.close()
    (out / "qa.txt").write_text("\n".join(qa) + ("\n" if qa else "no automated issues found\n"))
    return pages, qa


def html_render_flags(src, out, mode, width, height):
    chrome = chrome_bin()
    if mode == "print":
        run([chrome, "--headless=new", "--no-pdf-header-footer", f"--print-to-pdf={out/'render.pdf'}", src.resolve().as_uri()], timeout=180)
        return pdf_to_png(out / "render.pdf", out), ["(QA skipped: pip install websocket-client for overflow checks)"]
    p = out / "desktop.png"
    run([chrome, "--headless=new", "--hide-scrollbars", f"--window-size={width},{height}", f"--screenshot={p}", src.resolve().as_uri()], timeout=180)
    return [p], ["(QA skipped: pip install websocket-client for overflow checks)"]


def pdf_to_png(pdf: Path, out: Path, dpi=110):
    for old in out.glob("page-*.png"):
        old.unlink()
    run(["pdftoppm", "-png", "-r", str(dpi), str(pdf), str(out / "page")], timeout=300)
    return sorted(out.glob("page-*.png"))


def contact_sheet(pages, dest: Path, cols=3, thumb_w=520):
    from PIL import Image, ImageDraw
    if not pages:
        return None
    ims = [Image.open(p).convert("RGB") for p in pages]
    thumbs = []
    for im in ims:
        h = int(im.height * thumb_w / im.width)
        thumbs.append(im.resize((thumb_w, min(h, thumb_w * 3))))  # cap very tall web pages
    cols = min(cols, len(thumbs))
    rows = (len(thumbs) + cols - 1) // cols
    gap, lab = 24, 22
    cell_h = max(t.height for t in thumbs)
    sheet = Image.new("RGB", (cols * thumb_w + (cols + 1) * gap, rows * (cell_h + lab) + (rows + 1) * gap), "#d9dce1")
    d = ImageDraw.Draw(sheet)
    for i, t in enumerate(thumbs):
        x = gap + (i % cols) * (thumb_w + gap)
        y = gap + (i // cols) * (cell_h + lab + gap)
        d.text((x, y), pages[i].stem, fill="#333")
        sheet.paste(t, (x, y + lab))
    sheet.save(dest)
    return dest


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--out", help="output folder (default: <name>-render next to the file)")
    ap.add_argument("--mode", choices=["auto", "print", "screen"], default="auto",
                    help="HTML only. print = paged (decks, documents); screen = scrolling website screenshots")
    ap.add_argument("--width", type=int, default=1440)
    ap.add_argument("--height", type=int, default=900)
    ap.add_argument("--dpi", type=int, default=110)
    ap.add_argument("--desktop-only", action="store_true", help="screen mode: skip the 390px mobile capture (boards, lab sheets)")
    ap.add_argument("--cols", type=int, default=3, help="contact sheet columns (use 2 for a 2-slides-per-direction lab deck)")
    a = ap.parse_args()

    src = Path(a.file).expanduser().resolve()
    out = Path(a.out).expanduser().resolve() if a.out else src.parent / f"{src.stem}-render"
    out.mkdir(parents=True, exist_ok=True)
    ext = src.suffix.lower()
    qa = []

    if ext in (".pptx", ".ppt", ".potx", ".docx", ".doc"):
        pdf = out / "render.pdf"
        pdf.unlink(missing_ok=True)
        how = office_to_pdf(src, pdf)
        pages = pdf_to_png(pdf, out, a.dpi)
    elif ext in (".md", ".markdown"):
        html = out / (src.stem + ".html")
        css = Path(__file__).resolve().parent.parent / "templates" / "notes.css"
        cmd = ["pandoc", str(src), "-f", "gfm", "-s", "--embed-resources", "-o", str(html), "--metadata", f"title={src.stem}"]
        if css.exists():
            cmd += ["--css", str(css)]
        r = run(cmd, cwd=src.parent)
        if r.returncode:
            sys.exit(r.stderr)
        how = "pandoc + Chrome"
        pages, qa = html_render(html, out, "print", a.width, a.height)
    elif ext in (".html", ".htm"):
        mode = a.mode
        if mode == "auto":
            mode = "print" if "data-deck" in src.read_text(errors="ignore") else "screen"
        how = f"Chrome ({mode})"
        pages, qa = html_render(src, out, mode, a.width, a.height, a.desktop_only)
    elif ext == ".pdf":
        how = "pdftoppm"
        pages = pdf_to_png(src, out, a.dpi)
    else:
        sys.exit(f"Unsupported file type: {ext}")

    sheet = contact_sheet(pages, out / "contact.png", cols=a.cols)
    print(f"renderer: {how}")
    print(f"pages: {len(pages)}")
    for p in pages:
        print(f"  {p}")
    if sheet:
        print(f"contact sheet: {sheet}")
    if qa:
        print(f"QA ({len(qa)}):")
        for q in qa[:40]:
            print("  " + q)


if __name__ == "__main__":
    main()
