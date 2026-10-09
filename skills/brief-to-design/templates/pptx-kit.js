// pptx-kit.js — small helpers for pptxgenjs decks built with the brief-to-design skill.
// Usage (from the build folder):
//   const kit = require("<skill-dir>/templates/pptx-kit.js");   // e.g. ~/.claude/skills/brief-to-design
//   const { pres, T } = kit.deck(tokens);          // tokens: see TOKENS below
//   const s = pres.addSlide(); s.background = { color: T.bg };
//   kit.eyebrow(s, T, "WHO IT'S FOR", { x: 0.9, y: 0.75 });
//   kit.title(s, T, "Meet Stretched Sneha", { x: 0.9, y: 1.05, w: 11.5 });
//   kit.footer(s, T, "DaySutra · Team", 2);
//   await pres.writeFile({ fileName: "deck.pptx" });
//
// These are primitives, not layouts. Compose each slide for its own job; don't loop one layout.
// Canvas is LAYOUT_WIDE: 13.333" x 7.5". pptxgenjs gotchas: references/formats.md.

let PptxGenJS;
try { PptxGenJS = require("pptxgenjs"); }
catch (e) { PptxGenJS = require(require("path").join(process.cwd(), "node_modules", "pptxgenjs")); }

const TOKENS = {
  bg: "F3F6FB", surface: "FFFFFF", dark: "0A1630", primary: "2F6BFF", secondary: "1D4ED8",
  accent: "22C3D6", text: "0A1630", muted: "5B6B82", onDark: "FFFFFF", onDarkMuted: "A9B8D6",
  border: "DCE4F0",
  display: "Franklin Gothic Demi", body: "Calibri",   // Office-bundled = renders the same on Mac and Windows
  margin: 0.9,                                        // side margin, inches
};

const W = 13.333, H = 7.5;
const strip = o => Object.fromEntries(Object.entries(o).map(([k, v]) => [k, typeof v === "string" ? v.replace(/^#/, "") : v]));

function deck(tokens = {}, meta = {}) {
  const T = strip({ ...TOKENS, ...tokens });
  const pres = new PptxGenJS();
  pres.layout = "LAYOUT_WIDE";
  if (meta.title) pres.title = meta.title;
  if (meta.author) pres.author = meta.author;
  pres.theme = { headFontFace: T.display, bodyFontFace: T.body };
  return { pres, T, W, H };
}

// Small tracked uppercase label above a title. Encodes the section, not decoration.
function eyebrow(s, T, text, o = {}) {
  s.addText(text.toUpperCase(), {
    x: o.x ?? T.margin, y: o.y ?? 0.7, w: o.w ?? 8, h: 0.3, margin: 0,
    fontFace: o.font ?? T.body, fontSize: o.size ?? 11, bold: true, charSpacing: 3,
    color: o.color ?? (o.dark ? T.accent : T.primary),
  });
}

// Headline. Write it as the takeaway ("63 names tested. One clear winner."), not a topic label.
function title(s, T, text, o = {}) {
  s.addText(text, {
    x: o.x ?? T.margin, y: o.y ?? 1.0, w: o.w ?? W - 2 * T.margin, h: o.h ?? 0.9, margin: 0,
    fontFace: o.font ?? T.display, fontSize: o.size ?? 36, bold: o.bold ?? false,
    color: o.color ?? (o.dark ? T.onDark : T.text), valign: o.valign ?? "top", fit: "none",
    lineSpacingMultiple: o.lineSpacing ?? 0.95,
  });
}

function footer(s, T, left, n, o = {}) {
  const color = o.dark ? T.onDarkMuted : T.muted;
  const base = { y: H - 0.55, h: 0.3, margin: 0, fontFace: T.body, fontSize: 10, color };
  s.addText(left, { ...base, x: T.margin, w: 8 });
  if (n != null) s.addText(String(n).padStart(2, "0"), { ...base, x: W - T.margin - 1, w: 1, align: "right" });
}

// Big number + short label. value carries the meaning; keep label to one line.
function stat(s, T, value, label, o = {}) {
  const x = o.x ?? T.margin, y = o.y ?? 2, w = o.w ?? 3;
  s.addText(value, { x, y, w, h: o.h ?? 1.1, margin: 0, fontFace: T.display, fontSize: o.size ?? 60, bold: true, color: o.color ?? T.primary, valign: "bottom" });
  s.addText(label, { x, y: y + (o.h ?? 1.1) + 0.08, w, h: 0.6, margin: 0, fontFace: T.body, fontSize: o.labelSize ?? 13, color: o.dark ? T.onDarkMuted : T.muted, valign: "top" });
}

// Rounded panel. Prefer tint over borders; no edge stripes.
function panel(s, T, o) {
  s.addShape("roundRect", {
    x: o.x, y: o.y, w: o.w, h: o.h, rectRadius: o.radius ?? 0.18,
    fill: { color: o.fill ?? T.surface, transparency: o.transparency ?? 0 },
    line: o.line ? { color: o.line, width: 0.75 } : { type: "none" },
    shadow: o.shadow ? { type: "outer", color: "0A1630", opacity: 0.08, blur: 12, offset: 3, angle: 90 } : undefined,
  });
}

// Ranked horizontal bars drawn as shapes (exact control over highlight + labels).
// data: [{ label, value, highlight? }]; max: scale maximum. Use native addChart for real charts with axes.
function rankBars(s, T, data, o = {}) {
  const x = o.x ?? T.margin, y = o.y ?? 3, labelW = o.labelW ?? 2.2, valueW = o.valueW ?? 1.4;
  const w = o.w ?? W - 2 * T.margin, rowH = o.rowH ?? 0.42, barH = o.barH ?? 0.22, max = o.max ?? Math.max(...data.map(d => d.value));
  const trackW = w - labelW - valueW - 0.2;
  data.forEach((d, k) => {
    const ry = y + k * rowH, hi = !!d.highlight;
    s.addText(d.label, { x, y: ry, w: labelW, h: rowH, margin: 0, fontFace: T.body, fontSize: 13, bold: hi, color: T.text, valign: "middle" });
    s.addShape("roundRect", { x: x + labelW, y: ry + (rowH - barH) / 2, w: trackW, h: barH, rectRadius: barH / 2, fill: { color: o.track ?? T.border }, line: { type: "none" } });
    s.addShape("roundRect", { x: x + labelW, y: ry + (rowH - barH) / 2, w: Math.max(barH, trackW * d.value / max), h: barH, rectRadius: barH / 2, fill: { color: hi ? T.primary : (o.rest ?? T.secondary), transparency: hi ? 0 : 45 }, line: { type: "none" } });
    s.addText(d.display ?? String(d.value), { x: x + w - valueW, y: ry, w: valueW, h: rowH, margin: 0, fontFace: T.body, fontSize: 13, bold: hi, color: hi ? T.primary : T.text, align: "right", valign: "middle" });
  });
}

// Photo cropped to fill a frame (no distortion). Add a credit line when the license needs it.
function photo(s, T, path, o) {
  s.addImage({ path, x: o.x, y: o.y, w: o.w, h: o.h, sizing: { type: "cover", w: o.w, h: o.h }, rounding: !!o.round });
  if (o.scrim) s.addShape("rect", { x: o.x, y: o.y, w: o.w, h: o.h, fill: { color: o.scrim, transparency: o.scrimT ?? 45 }, line: { type: "none" } });
  if (o.credit) s.addText(o.credit, { x: o.x + 0.15, y: o.y + o.h - 0.32, w: o.w - 0.3, h: 0.25, margin: 0, fontFace: T.body, fontSize: 7, color: o.creditColor ?? "FFFFFF", align: "right" });
}

// Rough pre-render fit check: warns when text likely needs more lines than the box allows.
// avgChar ~0.5em for most sans, ~0.55 for wide geometric faces. The PowerPoint render is the truth.
function fits(text, pt, wIn, hIn, { avgChar = 0.52, lineSpacing = 1.15 } = {}) {
  const charsPerLine = Math.max(1, Math.floor((wIn * 72) / (pt * avgChar)));
  const lines = text.split("\n").reduce((n, para) => n + Math.max(1, Math.ceil(para.length / charsPerLine)), 0);
  const need = (lines * pt * lineSpacing) / 72;
  if (need > hIn) console.warn(`[fit] "${text.slice(0, 40)}…" needs ~${need.toFixed(2)}in, box is ${hIn}in`);
  return need <= hIn;
}

module.exports = { deck, eyebrow, title, footer, stat, panel, rankBars, photo, fits, TOKENS, W, H };
