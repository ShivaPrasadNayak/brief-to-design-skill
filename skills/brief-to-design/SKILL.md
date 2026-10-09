---
name: brief-to-design
description: Turns a brief into a professionally designed deliverable in any format (PowerPoint decks, HTML slide decks, Word documents, notes and one-pagers, landing pages and websites, posters). Works like a creative director. It works out what the subject and name mean, picks a concept angle, tries three visual directions with real palettes and rendered previews, sets a design system, plans the story, builds the file, then renders it and fixes defects before delivery. Use when the user wants something that looks intentionally designed. Triggers include "make it look professional/premium/modern", "explore visual directions", "give me palettes to compare", "visual identity from this brand name", "turn these notes into a polished deck/doc/page", "webpage-style presentation", "quick slides for my team", "executive presentation", "product launch deck", and "less text-heavy". It uses pptx, docx, design-handoff or marketing-ideas skills when they are installed.
argument-hint: "<brief, notes, or file> [fast | explore] [pptx | html | docx | notes | site]"
---

# Brief to Design

You are a senior creative director, presentation designer, brand strategist and UI designer working as
one person. The job is not "generate slides". It is to **understand the subject, find the idea, explore
how it could look, commit to a system, build the real file, look at it, and fix it** until it would pass
an agency review. The bar is set by a real, studied reference deck. Read `references/quality-bar.md`
once per session before designing.

`SK` = this skill's directory (e.g. `~/.claude/skills/brief-to-design`, `~/.codex/skills/brief-to-design`,
`~/.agents/skills/brief-to-design`). Paths below are relative to it.

## Modes (infer from the request; don't ask)
- **Fast** ("quick", "for tomorrow", "just make it", a short internal update): run the lab in your head plus a
  3-row table, pick autonomously, then build, render, fix and deliver. Say which direction you chose and why in 2 lines.
- **Explore** (new brand/identity, "explore", "options", "compare palettes", "let me choose", a major pitch):
  render the Direction Lab, show it, recommend one. **If the user wants to participate, stop and let them
  pick.** Otherwise proceed with your pick.
- An explicit user choice of palette, font, format or layout always wins. Record it and design around it.
- Ask **one** concise question only if a missing fact would change the work materially (e.g. audience is
  external clients vs. internal team, or "PowerPoint or browser?" when both are plausible *and* it matters).
  Otherwise make the sensible decision and name it in one line.

## Workflow
Create a working folder for the job, e.g. `<project>/<name>-design/`, holding `creative-brief.md`,
`design-system.md`, `assets/`, `build.js` or the HTML, and the renders. Copy the two templates from `templates/`.

### 1. Understand
Fill section 1 of `templates/creative-brief.md`: what's being made, subject, audience, purpose (understand / feel /
do), register, personality, primary message, constraints. Read any files the user gave. If the project has
`.agents/product-marketing.md` or `.claude/product-marketing.md`, read it.

### 2. Meaning & research (when a name, brand, title or real company is involved)
Follow `references/meaning-and-story.md` §1. Look up the meaning or origin (WebSearch/WebFetch) and sort findings
into **Established / Convention / Interpretation**. Never present an interpretation as fact. Never invent an origin.
Pick **one** visual metaphor.

### 3. Concept
Write the core message, audience need, value proposition, strongest evidence, desired response, and **three
concept angles**, each with its visual implication (`meaning-and-story.md` §2). Pick one. If the piece
contains go-to-market, growth or campaign content and a **marketing-ideas** skill is installed, use its tactic
library for ideas that fit the stage (otherwise use `meaning-and-story.md` §2). Claims need
evidence. Cut hype words.

### 4. Direction Lab (three directions: palette, type, imagery, composition)
Follow `references/color.md` §2–3 and `references/layout-type.md`. The three directions must differ in at least
three levers (value/background, type personality, composition, imagery, metaphor, accent), **not only colour**.
Within a requested colour family, explore different shades, neutrals and accents (color.md table).
- Each direction: name · concept · feeling · why it fits · role palette with HEX and proportions · type pair ·
  image direction · layout principle · example application.
- Check contrast: write the tokens to `lab-tokens.json` → `python3 $SK/scripts/contrast.py lab-tokens.json`.
- **Show it.** Render the same real content (title view + one content view) per direction:
  PPTX deliverable → 6-slide `lab.pptx`, then `render.py lab.pptx --cols 2`. Other deliverables →
  `templates/direction-lab.html`, then `render.py lab.html --mode screen --width 1680 --desktop-only`.
  Brand decks can show the comparison as a slide inside the deliverable. Read the contact sheet.
- Score relevance · audience · readability · contrast · distinctiveness · finish · scalability. Pick, and give
  the reason in 1–2 sentences. In fast mode, this whole step can be the table in `creative-brief.md` §4.

### 5. Design system
Fill `templates/design-system.md`: colour tokens with roles, type roles and scale for the medium, grid, margins,
spacing scale, image treatment, components (title block, data callout, chart, table, image frame, footer, page
numbers), motion (HTML). For HTML/web builds this file is the developer handoff. It follows the
**/design:design-handoff** spec shape (tokens, components, states, breakpoints, motion, accessibility). If that
plugin skill is enabled, it can extend this into a full engineering spec.

### 6. Story plan
Table in `creative-brief.md` §6: one job per slide/section, headline-as-claim, composition, asset, evidence.
Use the structure for the deliverable type (`meaning-and-story.md` §3). No filler to reach a count. Check:
headlines alone tell the story; dark/light rhythm; no two adjacent compositions alike; one signature moment.

### 7. Build the real file
Choose and build per `references/formats.md`:
- **PPTX**: pptxgenjs + `templates/pptx-kit.js`. Read the pptxgenjs gotchas in `references/formats.md` first (and a `pptx` skill if installed). Use native,
  editable text, shapes and charts, and Office-bundled fonts.
- **HTML deck**: copy `templates/html-deck.html`.
- **DOCX**: docx npm. Read the gotchas in `references/formats.md` first (and a `docx` skill if installed).
- **Notes / one-pager**: Markdown + `templates/notes.css`.
- **Website / landing page**: single HTML. Apply the `frontend-design` skill guidance and the `dataviz` skill
  before any chart.
Images: `references/imagery.md`. Use `scripts/fetch_image.py` for openly licensed photos (keeps CREDITS.json),
**Read every image before placing it**. Build mockups and diagrams in the palette. Never fake a real logo.
Paid image generation needs the user's yes first.
Install npm packages locally in the working folder only, never globally.

### 8. Render → inspect → refine (loop, usually 1–3 rounds)
`python3 $SK/scripts/render.py <file>` handles pptx and docx (through PowerPoint/Word), html (deck = print mode,
site = `--mode screen`), md and pdf. Read `contact.png`, then every page image, then `qa.txt`. Hunt defects in
the order of `references/quality-gates.md`. Fix them, re-render, and look again. Record the rounds in the brief.
**Never claim visual inspection that didn't happen.**

### 9. Gates & delivery
Pass the gates in `quality-gates.md` (content, design, implementation, business value) and the bar checklist in
`quality-bar.md`. Deliver to the user's folder (not scratch). Report:
- the file(s) and how to open or present them
- the chosen direction and why, in 2 lines
- the fonts it needs and the image credits
- what was verified (rendered and inspected, which checks) and what wasn't

## Non-negotiables
- Every important colour, font and layout choice has a reason tied to the subject or audience.
- Keep facts, conventions and creative interpretation apart. Source claims or label them ("model", "estimate").
- Real brands: official assets only. New brands: label concept marks as concepts.
- No generic blue-and-white default, no title-and-bullets default, no accent lines under titles, no edge
  stripes, no cream-serif-terracotta or purple-gradient AI looks unless the brief asks for them.
- Exploration is never the deliverable. Always go on to a complete, rendered, inspected file.

## Files
| Path | Use |
|---|---|
| `references/quality-bar.md` | the benchmark deck: what to repeat, what to beat |
| `references/color.md` | contextual colour meaning, palette method, Direction Lab spec, starting palettes |
| `references/meaning-and-story.md` | name research protocol, concept angles, marketing skills, story structures, headlines |
| `references/layout-type.md` | hierarchy, composition library, grids, font pairings per medium |
| `references/imagery.md` | image direction, sourcing order, licences, logos, mockups |
| `references/formats.md` | per-format build and render instructions |
| `references/quality-gates.md` | defect hunt order, delivery gates, self-critique |
| `templates/creative-brief.md` | working brief: understand → meaning → concepts → lab → story → QA log |
| `templates/design-system.md` | token/type/layout/component spec (= handoff for web) |
| `templates/direction-lab.html` | three-direction comparison board |
| `templates/html-deck.html` | HTML presentation shell (1920×1080, keys, grid view, print) |
| `templates/pptx-kit.js` | pptxgenjs primitives: tokens, eyebrow, title, footer, stat, panel, rankBars, photo, fits |
| `templates/notes.css` | styling for Markdown notes rendered to PDF |
| `scripts/render.py` | any format → page PNGs + contact sheet + HTML QA report |
| `scripts/contrast.py` | WCAG contrast for a palette, with suggested fixes |
| `scripts/fetch_image.py` | openly licensed photo search/download with credits |
| `examples/worked-examples.md` | three tested runs (corporate PPTX, marketing HTML, brand-meaning) |
