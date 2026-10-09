# Output formats — choose, build, render

`SK` = this skill's directory · render anything with `python3 $SK/scripts/render.py <file>`.

## Choosing the format
| The user says… | Build | Why |
|---|---|---|
| "slides/deck/presentation" + will edit or present from PowerPoint, or shares with a team | **PPTX** | editable, native |
| "webpage-style presentation", "present from the browser", "send a link", heavy imagery/motion | **HTML deck** | full typographic control, web fonts, motion |
| "report / memo / proposal / Word" | **DOCX** | editable, tracked changes possible |
| "notes / summary / one-pager / handout" | **Markdown → styled HTML/PDF** (or DOCX if they live in Word) | fast, portable |
| "landing page / website / microsite" | **HTML (single file)** — or the project's stack if one exists | real product |
| "poster / social image / banner" | HTML → PNG via render.py, or the `canvas-design` skill | pixel output |
| "design spec / handoff" | `design-system.md` + rendered previews; follow /design:design-handoff's format | for builders |
Unclear between PPTX and HTML for a deck? Default to **PPTX** for team/class/corporate use; HTML when the
user says web/browser/link. Don't ask unless the difference matters to them.

## PPTX
- Engine: **pptxgenjs**. Gotchas that corrupt files or silently misrender:
  - Set `pres.layout = "LAYOUT_WIDE"` (13.333×7.5in) before adding slides; off-canvas coordinates aren't clamped.
  - Hex colours without `#` and never 8 digits; use `transparency` (fills/images) for alpha.
  - pptxgenjs mutates option objects: build a fresh object for every `add*` call (shadows especially).
  - Shadow offsets ≥ 0; `charSpacing` (not `letterSpacing`); `rectRadius` only on rounded rectangles.
  - No gradient fills — use a gradient image. Set `margin: 0` on text boxes that must align with shapes.
  - Bullets via `bullet: true` (never a literal •); notes via `slide.addNotes()`.
  - Charts native via `addChart`, with your palette in `chartColors` and data labels on.
  - If an Anthropic `pptx` skill is installed, its `scripts/office/validate.py` catches PowerPoint-only corruption.
- Setup in the build folder: `node -e "require('pptxgenjs')" 2>/dev/null || npm i pptxgenjs` (local install
  only; never global).
- Helpers: `require('<skill-dir>/templates/pptx-kit.js')` →
  `deck(tokens)`, `eyebrow`, `title`, `footer`, `stat`, `panel`, `rankBars`, `photo` (cover-crop + scrim +
  credit), `fits` (pre-render overflow warning). Primitives only — compose each slide yourself.
- Canvas LAYOUT_WIDE 13.333×7.5in. Native text, shapes and charts — never flatten slides to images.
- Fonts from the Office-bundled list (layout-type.md) unless the user confirms otherwise.
- Speaker notes via `slide.addNotes()` when the user will present.
- Render: `render.py deck.pptx` → PowerPoint exports PDF (true fonts) → PNG per slide + `contact.png`.
  render.py stages the file through /tmp, because sandboxed Office can stall silently on folders it hasn't
  been granted. The first run may show a macOS automation prompt. If PowerPoint/Word returns -9074, times out,
  or a quit request comes back "User cancelled", it is blocked by a hidden dialog: ask the user to check the
  app. Don't force-quit it (they may have unsaved work). Meanwhile, work on non-Office parts. LibreOffice is the
  last fallback (font substitution makes fit checks approximate).
- Never give a shape negative `w`/`h` (e.g. a line drawn upward): use `flipV`/`flipH`. Run the pptx skill's
  `scripts/office/validate.py` (if available) after every build.

## HTML deck
- Copy `templates/html-deck.html`; replace `:root` tokens and the Google Fonts link; write slides as
  `<section class="slide" data-slide>` on a fixed 1920×1080 canvas (scaled to any screen).
- Built in: arrows/space/PageUp/PageDown/Home/End, click halves, swipe, `F` fullscreen, `G` grid overview,
  `#n` deep link, progress bar, print = one slide per page (Cmd+P → PDF), reduced-motion respected.
- Self-contained: inline CSS/JS; images as relative files in `assets/` (or base64 for a single-file handoff
  under ~10 MB).
- Render: `render.py deck.html` → print-mode PDF → PNG per slide + `qa.txt` (overflow, text outside slide,
  broken images, failed fonts).

## DOCX
- Engine: **docx** npm (same local-install rule). Gotchas: tables need `columnWidths` *and* a `width` on every
  cell (DXA units); shading uses `ShadingType.CLEAR`; `ImageRun` needs `type`; no `\n` in text (new Paragraph);
  bullets via a numbering config, never a literal •. A4 is the default page size.
- Design system applies: heading font/colour, a cover or title block, callout boxes (shaded paragraphs or
  1-cell tables), real tables with header styling, charts as images rendered in palette, page numbers footer.
- Render: `render.py report.docx` → Word exports PDF → PNG per page.

## Notes / one-pagers (Markdown)
- Write `.md`; copy `templates/notes.css` next to it and set its tokens; render with `render.py notes.md`
  (pandoc GFM → HTML → Chrome PDF). Deliver the `.md` plus the PDF (`<name>-render/render.pdf`).
- Leave a blank line before every table, list and blockquote, or the block is swallowed by the paragraph
  or list above it.

## Website / landing page
- Read `frontend-design` skill guidance for web aesthetics; `dataviz` before any chart.
- Single `index.html` (inline CSS, minimal JS) unless the project has a stack.
- Mobile-first check: 390px and 1440px. Visible focus, semantic landmarks, alt text, `prefers-reduced-motion`.
- Render: `render.py index.html --mode screen` → full-page `desktop.png` (1440) + `mobile.png` (390) + `qa.txt`
  (overflow, horizontal scroll, broken images). The browser pane can also preview interactively.
- Handoff: `design-system.md` doubles as the dev spec (design-handoff shape: tokens, components, states,
  breakpoints, motion, accessibility).

## Direction Lab medium
- PPTX deliverable → a 6-slide `lab.pptx` (title + content per direction), `render.py lab.pptx --cols 2`
  (rows = directions). True fonts.
- Everything else → `templates/direction-lab.html`, `render.py lab.html --mode screen --width 1680 --desktop-only`.
- Brand/identity presentations: the comparison can live *inside* the deliverable as a "directions we
  explored" slide (it's content the audience wants to see), instead of a separate lab file.

## Delivering
Put deliverables where the user asked (or the current project folder), not in scratch. Report: file path(s),
how to open/present, fonts required, credits file, and anything not verified.
