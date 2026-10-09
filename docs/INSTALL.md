# Install Brief to Design in your AI tool

Brief to Design is a standard Agent Skill: a folder (`skills/brief-to-design/`) with a `SKILL.md` inside.
Every tool below reads that same folder; only the location differs.

## Any agent, one command
```bash
npx skills add ShivaPrasadNayak/brief-to-design-skill
```
Uses the open-source [skills CLI](https://github.com/vercel-labs/skills); add `-g` to install for your user, `-a <agent>` to target one tool.

## Claude Code
**Plugin marketplace** (gets updates):
```
/plugin marketplace add ShivaPrasadNayak/brief-to-design-skill
/plugin install brief-to-design@brief-to-design-skill
```
**Manual:**
```bash
git clone https://github.com/ShivaPrasadNayak/brief-to-design-skill
cp -R brief-to-design-skill/skills/brief-to-design ~/.claude/skills/
```
Use it by asking naturally ("make quick slides for my team") or with `/brief-to-design <brief>`.

## Claude.ai and Claude Desktop
1. Download [`dist/brief-to-design.zip`](../dist/brief-to-design.zip).
2. Open **Customize → Skills**, click **+**, upload the zip. Code execution must be enabled.

## OpenAI Codex (CLI, IDE, app)
```bash
cp -R brief-to-design-skill/skills/brief-to-design ~/.codex/skills/
```
Or in Codex: `$skill-installer` with `https://github.com/ShivaPrasadNayak/brief-to-design-skill/tree/main/skills/brief-to-design`.
Per-project: put the folder in `.agents/skills/` inside the repo.

## GitHub Copilot (agent mode, CLI, cloud agent)
- Personal: `~/.copilot/skills/brief-to-design/` (Copilot also reads `~/.claude/skills` and `~/.agents/skills`)
- One repository: `.github/skills/brief-to-design/`

## Cursor, Gemini CLI, OpenCode and other Agent Skills tools
Copy the folder to `~/.agents/skills/brief-to-design/` (or the tool's own skills folder, e.g. `~/.cursor/skills/`).

## ChatGPT, Grok, Gemini web and other chat apps
If your plan supports Skills, upload the zip. Otherwise create a Project and add `SKILL.md` and the files in
`references/` and `templates/` as project knowledge, then ask for a deck. The design method works; the
render-and-fix scripts need a tool that can run code, so check the output yourself.

## Requirements for the helper scripts
Node.js 18+, Python 3.9+ with Pillow, Chrome/Chromium/Edge, and Microsoft Office (macOS) or LibreOffice to
render PPTX/DOCX. Optional: `pip install websocket-client` (HTML overflow QA), `pandoc`, `poppler` (`pdftoppm`).
```bash
# macOS
brew install pandoc poppler && pip3 install pillow websocket-client
# Ubuntu/Debian
sudo apt install pandoc poppler-utils libreoffice chromium && pip3 install pillow websocket-client
```
