# Colour — meaning, palette generation, experimentation

## 1. Associations are contextual, not laws
These are common **design conventions** in Western/global commercial design. They shift by industry, culture
and the brand's competitors. Say "commonly reads as" — never "psychologically causes".

| Family | Common associations | Watch-outs |
|---|---|---|
| Blue (cobalt, royal) | trust, stability, technology, clarity | the default of fintech/SaaS/healthcare — hard to stand out |
| Navy | authority, maturity, seriousness | can read cold or bureaucratic; needs a warm or bright accent |
| Sky / ice blue | calm, openness, air | weak contrast as text; use as surfaces |
| Cyan | digital, fresh, energetic | fails contrast on white as text; accent only |
| Teal | balance, modern health, tech-meets-nature | crowded in wellness/health |
| Indigo / violet | imagination, premium, AI/"magic" | AI products have overused violet gradients since 2023 |
| Lavender (muted) | softness, creativity, calm | can feel juvenile at high saturation |
| Green | growth, money, sustainability, "go" | finance (gains) vs eco (nature) read differently |
| Red | urgency, energy, danger, loss | in finance = losses; in China = luck/prosperity |
| Orange | warmth, action, approachability | cheapness at full saturation; great CTA accent |
| Yellow | optimism, attention | unreadable as text on white |
| Black / charcoal | elegance, authority, luxury | heavy for long reading; use for stage moments |
| White / cool white | clarity, openness, minimalism | needs typographic strength or feels empty |
| Warm neutrals (stone, sand) | craft, heritage, calm | cream + serif + terracotta is the AI-default look — avoid unless the brief asks |

Culture flags to check when the audience is specific: white (mourning in parts of East Asia), saffron (sacred/
political in India), green (Islam, Ireland, politics), red (luck in China, danger in the West), purple (mourning in
Brazil/Thailand). If unsure and the audience is local, ask or pick neutral roles for the risky hue.

Every important colour gets a one-line rationale tied to the **subject or audience**, never "it looks nice".

## 2. Generating a palette (method)
1. **Anchor in meaning.** List 2–3 sources from the brief: the subject's materials and world (ocean → deep
   water, foam, kelp), the name's meaning, the audience's environment, competitor colours to avoid.
2. **Choose a dominant hue + temperature.** One colour owns ~60% of visual weight (often a near-neutral of
   the hue: ice, stone, ink). Never give all colours equal weight.
3. **Build the role set** (not just "5 nice colours"): bg · surface · dark · primary · secondary · accent ·
   text · muted · on-dark · border (+ status colours only if data needs them).
   - Neutrals carry a tint of the hue (navy-tinted greys, not pure #888).
   - `text` is a very dark version of the hue, rarely pure black.
   - `accent` is the one contrasting note: complementary, split-complementary, or a hot/cold flip
     (e.g. a coral spark in a blue system). Used ≤5%.
4. **Proportions.** ~60 bg/neutral · ~25 dark/primary blocks · ~10 secondary · ≤5 accent.
5. **Contrast pass.** `python scripts/contrast.py tokens.json` — body text ≥4.5:1, large text & UI marks ≥3:1.
   Fix by nudging lightness, not by swapping the hue.
   If no shade of the accent passes on both the light and dark surfaces (common for cyan on cobalt), split it into
   two roles, `accent` (on light) and `accent-on-dark` (e.g. a pale tint or the warm note), and record which is used where. Light-on-colour (white on mid-blue) usually fails at body sizes.
6. **Data colours.** Categorical series in a fixed order from the palette; highlight = primary, others =
   secondary at reduced opacity; don't encode meaning by hue alone (add labels/patterns). Use the `dataviz`
   skill for chart-heavy work.
7. **Dark & light check.** Every token pair that appears together on a dark slide/page is checked too.

## 3. Experimenting — the Direction Lab
For a new brand, a major deck, or when the user asks to explore: **three directions** that differ in more
than colour. Vary at least three of: palette temperature/value · background (dark-led vs light-led) ·
type personality · composition (editorial asymmetry, grid/bento, full-bleed image, typographic poster) ·
imagery (photo, illustration, abstract, none) · visual metaphor.

When the user named a colour family ("cool blue"), all three stay inside it but explore *different blues*:
| Lever | Example within "blue" |
|---|---|
| Value | ink-navy led (dark) vs ice-white led (light) vs mid cobalt field |
| Neighbour | blue + teal (fresh) vs blue + slate/silver (premium) vs blue + indigo/lavender (creative) |
| Accent | cyan spark · warm coral spark · no accent, tonal only |
| Neutral temperature | cool grey vs warm stone vs pure white |

For each direction record: name · concept · emotional intention · why it fits · primary · secondary ·
background · text · accent (+ surface, muted) with HEX · proportions · contrast results · example application
("navy title slides, ice content slides, cyan only on the one number that matters").

**Show, don't list.** Render the same two pieces of real content (title + one content view) in each direction
— `templates/direction-lab.html` for web/HTML/docs, or a 6-slide lab PPTX for PowerPoint deliverables —
and compare the rendered images. Score on: relevance · audience · readability · contrast · distinctiveness ·
professional finish · holds across many slides. Pick the strongest, state the reason in one or two sentences.

If the user chose a palette, use it; the lab then explores composition/type only, or is skipped in fast mode.

## 4. Starting points (adapt, never paste)
| Name | bg | dark | primary | secondary | accent | text | muted | Suits |
|---|---|---|---|---|---|---|---|---|
| Arctic Intelligence | F4F8FC | 0F2F52 | 2563A6 | 7FA7CF | 56C5E8 | 142536 | 5C7186 | enterprise tech, data |
| Midnight Premium | F5F5F3 | 12161D | 2B3A4E | 9AA5B1 | C9A86A | 151A21 | 6A7380 | finance, leadership, luxury-adjacent |
| Cobalt Signal | FFFFFF | 0B1B4D | 1F48FF | 0C8CE9 | FF6B4A | 0B1533 | 59617A | launches, bold product |
| Tidal Teal | F2F7F7 | 0E3A40 | 127C80 | 6FB7B3 | F2B544 | 102A2D | 4F6B6E | health, climate, education |
| Indigo Studio | F3F2FB | 1A1446 | 4B3FD8 | 9C92F2 | 3FE0C5 | 18143A | 625D85 | creative, AI, culture |
| Slate & Signal | F4F5F7 | 1E252E | 3A4757 | 8893A1 | E8553D | 1A2028 | 646E7B | analytical, engineering, ops |
| Grove | F5F7F2 | 1D3324 | 2F6B3F | 97B88A | E9A23B | 18261C | 5D6B5F | sustainability, food, growth |
| Ember | FFF9F5 | 2A1410 | C2412D | F08A4B | 2A6FDB | 2A1A16 | 7A625A | marketing, events, energy |
Run contrast.py on whatever you derive — these rows are starting hues, not verified systems.
