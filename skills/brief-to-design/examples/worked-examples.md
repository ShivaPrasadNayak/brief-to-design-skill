# Worked examples — three tested runs (Oct 2026)

These were run end to end with this skill and rendered at every step. Same skill, three different results:
the point is that subject, audience and meaning drive the design, not a template.

| | 1 · Corporate | 2 · Marketing | 3 · Brand meaning |
|---|---|---|---|
| Brief | Leadership proposal: consolidate 14 regional dashboards into one self-serve platform. "Cool blue palette." | Campaign pitch "Second Wind": trade-in + resale of refurbished running shoes (fictional brand Stride Again). Energetic, webpage-like, real imagery. | Identity + brand deck for "Saarthi", AI career guidance for Indian college students, "based on the meaning of the name". |
| Format | PPTX (7 slides) | HTML deck (8 slides) | PPTX (7 slides) + DOCX one-pager + MD notes |
| Mode | Fast, with a rendered lab (cool-blue exploration requested) | Explore: HTML lab board | Explore: comparison as a slide inside the deck |
| Lab directions | A Arctic Ledger (light, Franklin Gothic, number-led) · B Deep Harbour (dark, night-port photo, amber note) · C Blueprint (cobalt + grid linework, diagram-led) | A Lap Two (white, Bricolage, signal orange, hard photo crops) · B Mileage (asphalt, Anton, lime lane lines) · C Full Circle (forest, Fraunces, loop motif) | Dawn Road (plum to marigold, reins mark) · Steady Hand (teal/sand counsel) · Epic Gold (black/temple gold, chariot wheel) |
| Pick and why | **C Blueprint**: "a platform we build" metaphor; diagram-led clarity for leadership. B failed readability (subtitle lost on photo reflections). | **A Lap Two**: energy matches the idiom "second wind"; real worn-shoe photos are its main material. B's lane lines kept for the signature slide. | **Dawn Road**: hopeful and warm for anxious 20-year-olds; Epic Gold rejected as devotional overreach, Steady Hand as bank-like. |
| Meaning work | n/a (no name) | "Second wind" = renewed energy after exhaustion (idiom, established). Laps/lanes = interpretation. | *Sārathi* = charioteer; Krishna as Arjuna's charioteer counselling him at his moment of doubt (sourced, Wikipedia). Interpretation: "a charioteer steers, the archer decides". Risks: devotional connotation, name crowding. |
| Signature moment | 14 tiles showing 14 different "on-time %" values for the same KPI | Orange slide with a hang-tag mock-up: "Previously run 412 km. Your turn." | Established / Convention / Interpretation slide; reins-to-road concept mark |
| Type | Franklin Gothic Demi/Book + Consolas labels | Bricolage Grotesque + Figtree (web fonts) | Candara + Corbel (+ Consolas for hex) |
| Imagery | None in final: diagrams and data carry it (night-port photo tried in lab B) | 3 Openverse CC BY photos, credited on-slide | Built visuals only: concept mark, app mock-up, social post |

## Defects the render caught (what the loop is for)
- **Contrast checker, before any build**: cyan accents failed on light and could not pass on cobalt at any
  shade → split accent roles. Signal orange on white 3.4:1 → large text only; `orange-ink #D63E18` for small text.
- **T1, PowerPoint render**: Gill Sans MT's "1" read as "I" ("phase I", "I2-week") → switched to Franklin
  Gothic. Headline wrapped into the chart label → shortened. Lower thirds empty → content scaled to fill.
- **T2, Chrome render**: slides 3/4/7 had dead lower halves; "06" collided with a label; poster mock-up had an
  empty dark band → re-composed. Lab board: headline A ran into the photo → fixed in the build.
- **T3**: phone mock-up overflowed into the footer; app icon invisible (plum on plum); Corbel old-style figures
  jumbled hex codes → set codes in Consolas.
- **Image vetting**: rejected photos with visible ASICS logos (fictional brand), and a historic shoe-workshop
  photo whose source was a reform school with a dark history.
- **Notes path**: Markdown without blank lines collapsed into one paragraph → render.py now uses GFM; the
  blank-line-before-tables rule went into formats.md.
- **Tooling**: PowerPoint stalled on a sandboxed folder and then blocked on a hidden dialog → render.py stages
  Office files through /tmp; the skill now says to ask the user rather than force-quit.

## Sample invocation → what happens
> "Make quick slides to pitch our new campus ambassador programme to the dean. Something that feels like a serious institution, not a startup."

1. Understand: audience = dean (institutional, decision-maker), purpose = approval, register = formal-educational.
2. No name to research; concept angles: "Students as the institution's voice" / "Proof before scale" /
   "A programme that pays for itself". Pick by the evidence available.
3. Fast mode: lab as a 3-row table (e.g. Calm Institutional, Cambria + Calibri, deep green-navy; vs. two
   alternatives), pick, state why in 2 lines.
4. design-system.md → story plan: decision on slide 2, evidence, risks, cost, next steps.
5. pptxgenjs + pptx-kit → render.py → fix → deliver a .pptx with native text, plus the reasoning in 5 lines.
