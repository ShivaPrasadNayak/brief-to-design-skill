# Design system — {project}

> Mini design system for one deliverable. Every colour, size and spacing used in the build must come
> from here. For HTML/web builds this doubles as the developer handoff (same shape as
> /design:design-handoff: tokens, components, states, responsive, accessibility).

## Direction
{name} — {one-sentence concept}. Signature element: {the one memorable thing}.

## Colour
| Token | Hex | Role | Share |
|---|---|---|---|
| `bg` | | content background | ~60% |
| `surface` | | cards, panels | |
| `dark` | | title / section / closing slides | ~25% |
| `primary` | | headings accents, key data | ~10% |
| `secondary` | | supporting data, links | |
| `accent` | | one highlight per view | ≤5% |
| `text` | | body on bg | |
| `muted` | | captions, footers | |
| `on-dark` / `on-dark-muted` | | text on dark | |
| `border` | | hairlines, tracks | |
| status (if data needs it) | | good / warn / bad — never rely on hue alone | |

Contrast (scripts/contrast.py): text/bg …:1 · muted/bg …:1 · on-dark/dark …:1 · accent use limited to ≥24px or non-text marks if < 4.5:1.

## Type
| Role | Family (fallback) | Weight | Size (slide @1920 / PPTX pt / doc pt / web px) | Line height | Tracking |
|---|---|---|---|---|---|
| Hero | | | 120–140 / 54–66 / — / clamp(48,7vw,104) | 1.0 | −3% |
| Title | | | 64–76 / 32–40 / 22–26 / 40–56 | 1.05 | −2% |
| Subhead | | | 36–44 / 18–22 / 14–15 / 22–28 | 1.2 | |
| Body | | | 26–30 / 13–16 / 10.5–11.5 / 17–19 | 1.45 | 0 |
| Caption / eyebrow | | | 20–22 / 10–11 / 8.5–9 / 13–14 | 1.2 | +12–14% caps |
Max line length: ~60–75 characters for body copy.

## Layout
- Canvas: {1920×1080 HTML · 13.333×7.5 in PPTX · A4/Letter doc · responsive web}
- Grid: {12 col, 120px margins @1920 / 0.9 in PPTX}; spacing scale {8 · 16 · 24 · 40 · 64 · 96}
- Alignment: left-aligned text; centre only single-line statements
- Density: {max words per slide ~40 excl. data; one idea per slide}
- Image treatment: {full-bleed / framed / duotone / scrim %}; corners {radius}

## Components
| Component | Spec |
|---|---|
| Title block | eyebrow (caps, tracked) + headline-as-claim |
| Data callout | number in display face, label ≤ 8 words |
| Chart | palette order, highlighted series = primary, rest = secondary @ 55% |
| Table | header row muted caps, hairline rows, numbers right-aligned tabular |
| Image frame | |
| Footer | left: deck/brand name · right: page number, muted, 10pt / 20px |

## Motion (HTML only)
| Element | Trigger | Animation | Duration | Easing |
|---|---|---|---|---|
| Slide | navigate | fade + 12px rise | 450ms | ease |
Respect `prefers-reduced-motion`.

## Accessibility
Focus visible · keyboard nav · alt text on meaningful images · no information by colour alone.
