# Images, logos and visual assets

## 1. Decide the image direction first (it's part of the design system)
State it in one line: *what* (people at work · product UI · places · materials/macro · abstract light ·
diagrams only), *treatment* (natural colour · duotone in palette · desaturated + one colour · high-key ·
low-key with scrim), *framing* (full-bleed · framed with radius · circular crops for people).
"None — type, diagrams and data carry this deck, because …" is a valid answer.

Every image must earn its place: it shows the subject, the audience, the product, the place, or the
metaphor. Decoration-only stock ("handshake", "lightbulb", "people pointing at laptop") is cut.

## 2. Where assets come from (in order)
1. **User-provided** files, logos, screenshots, brand kits. Always first; ask once if the deliverable clearly
   needs a logo/photo the user probably has.
2. **Real product / site screenshots** — capture with the browser pane (`mcp__Claude_Browser__*`, screenshot)
   or headless Chrome via `scripts/render.py page.html --mode screen`.
3. **Openly licensed photos** — `scripts/fetch_image.py "query" --out assets --n 6 --orientation landscape`
   (Openverse: Flickr, Wikimedia Commons, etc.; CC0/PDM/BY/BY-SA by default; writes `assets/CREDITS.json`).
   Flickr results are 1024px (fine for half-slide); for full-bleed use `--source wikimedia --min-width 1600`.
   Search concretely ("container port cranes dusk", not "logistics"); fetch 6, **Read each image**, keep the
   best 1–2. Credit BY/BY-SA images on the slide (small, corner) or on a credits slide/page.
4. **Built visuals** — charts, diagrams, device/browser mockups, motifs drawn in SVG/HTML/shapes. Often
   better than a photo: they carry information and match the palette perfectly.
5. **Generated imagery** (image-generation skills, Gemini/other APIs) — costs money: **say what you'll
   generate and why, and wait for the user's yes** before calling any paid API. Label generated images as such
   when they could be mistaken for real photos of real people/places.
6. **Icons** — `react-icons` → SVG → PNG (see the pptx skill), or inline SVG (Lucide/Tabler shapes) in HTML.
   One icon family per piece, one stroke weight.

## 3. Rules
1. High resolution: ≥ 1600px wide for full-bleed slides, ≥ 1200px for half-slide.
2. Reject images with a clearly visible real brand logo (e.g. a sportswear mark) in a fictional or other
   brand's piece, and check the image's context (title, source page): a historic photo can carry
   connotations that are wrong for the brief.
3. No watermarks, no visible stock-site branding, no AI artefacts (hands, text, warped logos).
4. Don't reuse the same image twice in one piece unless it's a deliberate callback.
5. Consistent treatment across the set (same temperature, contrast, crop logic).
6. Crop with intent: faces looking into the slide, horizon on a third, the subject not cut at joints.
7. Text over images needs a scrim or a calm area — check contrast in the render, not in your head.
8. Real people and real brands: don't alter their appearance or imply endorsement.
9. Respect licences: keep `CREDITS.json`; BY/BY-SA require attribution; NC licences are not for commercial
   decks; Wikimedia logo files are often trademarked even when the file is "free".

## 4. Logos
- **User's logo** → use it; keep clear space ≈ the logo's x-height; never recolour beyond its official variants.
- **Real third-party logo** (client, partner, competitor) → official press/brand page or Wikimedia's file
  (check the licence note). If you can't get a reliable file, set the company name in clean type instead.
  Never redraw a real logo and present it as official.
- **New brand concept** → design a concept mark (SVG/shapes) from the name's metaphor; label it
  "concept mark". Show it on dark and light, at small size (favicon/app icon), and in one mockup.

## 5. Mockups that sell the idea
Browser frame (address bar, 3 dots, real URL) · phone frame (rounded rect, status bar, real UI copy) ·
app card on a phone · social post · poster in context. Build them from shapes/HTML in the palette with real
copy — they read as designed, not as clip art.
