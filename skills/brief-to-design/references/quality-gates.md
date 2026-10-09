# Quality gates — inspect the render, not the code

Run after every build: `render.py <file>`, then **Read `contact.png` first** (rhythm, variety, balance across
the whole piece), then **Read every page/slide image** at full size, then read `qa.txt` (HTML).
Never report "visually inspected" for something that wasn't rendered and looked at.

## Defect hunt (in this order — the first ones are the most common)
1. Text overflow / clipped / outside the frame / colliding with footer.
2. Broken or missing images; wrong crop (cut faces, cut subject); low resolution / blur.
3. Contrast: light text on light, text over busy image without scrim, muted text too faint.
4. Overlaps: shapes through words, chart labels colliding, icons touching text.
5. Spacing: uneven gaps, cramped edges (< margin), large unplanned empty zones.
6. Alignment: columns/titles not on the same x; baselines drifting slide to slide.
7. Hierarchy: two elements competing for first read; headline not the biggest thing.
8. Typography: wrong/fallback font, orphan word on a headline line, inconsistent sizes for same role.
9. Repetition: adjacent slides with the same layout; too many card grids.
10. Charts: unreadable labels, no highlight, legend where direct labels would do, colours off-palette.
11. Content: typos, placeholder text, wrong order, missing sections, unsourced numbers.

Fix meaningful issues → re-render → re-inspect the changed pages. Usually 1–3 rounds. Log rounds in the
brief's QA table.

## Gates before delivery
**Content** — main message clear in one sentence · logical narrative · claims accurate and sourced or labelled ·
fits the audience.
**Design** — palette intentional with rationale · contrast passes (contrast.py + eye on render) · type readable
at presenting distance · obvious hierarchy · varied but consistent layouts · images relevant and credited ·
looks agency-made (compare against `quality-bar.md`).
**Implementation** — opens in its target app · HTML navigation works (keys, click, print) · images load ·
no QA flags left unexplained · fonts available where it'll be shown.
**Business value** — the audience gets it in a skim of headlines · the ending is an action or decision.

## Self-critique questions (answer honestly before delivering)
- If I swapped this palette and type into a different topic, would it still "work"? Then it isn't specific enough.
- Which slide/section is the signature? If none, make one.
- What would the reference deck do better here? (quality-bar.md)
- Remove one accessory: what decoration can go without loss?
