# Layout, hierarchy and typography

## 1. Hierarchy in three levels
Every view has exactly one **first read** (the headline, the number, or the image), one **second read**
(supporting line or chart), and **quiet chrome** (eyebrow, footer, source). Create the levels with size first,
then weight, then colour, then position. If two things compete for first read, shrink one.

Size ratios that work: hero ≥ 2× title; title ≥ 2.2× body; body ≥ 1.3× caption.

## 2. Composition library (choose per slide job; vary neighbours)
| Job | Composition |
|---|---|
| Open / big idea | type-led hero on dark field + one motif from the metaphor; or full-bleed photo with scrim and left-set headline |
| Section change | single oversized word/number on colour field |
| One number matters | giant numeral (140–200px@1920) left, one-line meaning right, source small |
| Compare 2–3 options | columns with the recommended one inverted (dark) — not three identical cards |
| Ranking / scores | horizontal bars, winner in primary, others muted, values right-aligned |
| Process / flow | 3–5 steps on a line or arrows; numbers only because order matters |
| Funnel / narrowing | 63 → 6 → 1 chips with arrows, the final one filled |
| Persona / quote | big quote panel (dark) + 2–3 stat chips |
| Show the product | browser or phone frame mockup with real copy; annotate 2–3 callouts |
| Architecture / system | layered diagram, labelled planes, one highlighted path |
| Evidence | chart takes ≥ 60% of the area; headline says what it shows |
| Image story | split screen 50/50 or 60/40 photo + text; or photo grid with one caption |
| Summary / ask | 3 numbered actions with owners/dates, on dark |
| Agenda (only if > 10 slides) | short list, current section highlighted |

**Rhythm:** alternate dark/light deliberately (opening, section breaks, close = dark); no two adjacent slides
with the same composition; rounded-card grids on at most half the slides; one signature slide that only this
deck could have.

**Avoid:** title + bullets as the default · accent lines under titles · edge stripes on cards · random blobs ·
gradients everywhere (one subtle radial for depth is enough) · drop shadows on everything (one level, soft) ·
centred body text · more than ~40 words on a slide (excluding data labels) · 3 fonts.

## 3. Grids and spacing
- HTML slides 1920×1080: margins 120px, top title zone 100–120px, footer 56px from bottom, 12-col grid, gutters 40px.
- PPTX 13.333×7.5in: margins 0.9in, title at y≈0.7–1.0in, footer at y≈6.95in, gaps 0.3in or 0.5in (pick one).
- Docs: A4 with 20–25mm margins, one column for prose, max ~75 characters per line.
- Web: max content width 1120–1240px, section padding 96–128px desktop / 56–72px mobile, 16px mobile gutter.
- Spacing scale (pick one, use only it): 8 · 16 · 24 · 40 · 64 · 96 · 128.

## 4. Typography by medium

### PPTX / DOCX (fonts render on the viewer's machine — choose fonts they have)
Office bundles these on **both Mac and Windows** (safe to share):
Calibri · Cambria · Candara · Constantia · Corbel · Consolas · Franklin Gothic (Book/Medium/Demi/Heavy) ·
Gill Sans MT · Century Gothic · Rockwell · Garamond · Bookman Old Style · Century Schoolbook · Book Antiqua ·
Perpetua · Georgia · Arial · Verdana · Trebuchet MS · Aptos (Office 2023+ only — avoid for wide sharing).

| Personality | Display | Body |
|---|---|---|
| Confident editorial | Franklin Gothic Demi / Heavy | Franklin Gothic Book |
| Modern geometric, friendly | Century Gothic (bold) | Calibri |
| Calm humanist | Gill Sans MT | Gill Sans MT / Calibri |
| Classic premium | Garamond / Perpetua Titling | Calibri or Garamond |
| Industrial, engineering | Rockwell (bold) | Calibri / Franklin Gothic Book |
| Soft creative | Candara (bold) | Candara / Corbel |
| Authoritative report | Cambria / Constantia | Calibri |
Mac-only (fine if only the user presents from a Mac): Avenir Next, Futura, Helvetica Neue, Didot, Charter, Optima.
Custom web fonts (Sora, DM Sans…) in PPTX fall back silently on machines without them — use only if the
user confirms they're installed everywhere, or embed by exporting to PDF for distribution.

### HTML (decks, pages, sites)
Google Fonts via `<link>` (with system fallbacks in the stack). Pairings by personality:
| Personality | Display | Body | Utility |
|---|---|---|---|
| Precise tech | Sora / Space Grotesk | DM Sans / Inter | JetBrains Mono |
| Premium editorial | Fraunces / Instrument Serif | Inter Tight / Source Sans 3 | IBM Plex Mono |
| Confident product | Manrope / Plus Jakarta Sans | Plus Jakarta Sans | |
| Bold marketing | Bricolage Grotesque / Syne | Figtree / Outfit | |
| Calm institutional | Newsreader / Source Serif 4 | Source Sans 3 | |
| Cultural / heritage | Cormorant / Playfair Display | Work Sans / Karla | |
| Engineering | IBM Plex Sans (700) | IBM Plex Sans | IBM Plex Mono |
Rotate away from whatever was used in the last project; Inter + a purple gradient is the AI default.

### Type rules
- **Check the numerals before committing a face** (found in testing): Gill Sans MT's "1" reads as a capital I
  ("phase I", "I2 weeks"), so don't use it where numbers matter. Candara, Corbel and Constantia default to old-style
  (descending) figures: fine in prose, messy in hex codes, tables and KPIs, so set those in Consolas or a
  lining-figure face (Franklin Gothic, Calibri).
- Display tracking −2% to −4% at large sizes; caps eyebrows +12–14%.
- Line height: display 0.95–1.05, headings 1.1–1.2, body 1.4–1.55.
- Weights: two per family, at most three across the piece.
- Numbers in tables/data: tabular figures, right-aligned.
- Minimum sizes: slides — body 24px@1920 / 14pt PPTX, captions 18px / 10pt; docs 10.5pt body; web 16–18px body.
