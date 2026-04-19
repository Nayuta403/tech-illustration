# tech-illustration

[English](README.md) · [中文](README_zh.md)

> A Claude [Agent Skill](https://docs.claude.com/en/docs/claude-code/skills) that generates multi-style technical illustrations for articles, slides, and documentation using Google's Gemini 3.1 Flash Image model.

Give it a concept, pick a style, get a publication-ready image.

## Styles

| Style | Preview |
|-------|---------|
| **blueprint** — engineering grid, navy + orange, hand-drawn feel. Default. | ![blueprint](examples/blueprint.png) |
| **clean** — minimalist vector diagram, white background. | ![clean](examples/clean.png) |
| **dynamic** — isometric, glowing energy flows, dark background. | ![dynamic](examples/dynamic.png) |
| **bold** — avant-garde editorial, massive typography. | ![bold](examples/bold.png) |

## Install

### As a Claude skill

Drop the folder into your skills directory:

```bash
# For Claude Code
git clone https://github.com/Nayuta403/tech-illustration.git ~/.claude/skills/tech-illustration
```

Claude will auto-discover it via `SKILL.md`. Ask something like:

> Generate a blueprint-style illustration of our OAuth flow.

### Standalone (no Claude)

The script works on its own — it's just a Python CLI.

```bash
git clone https://github.com/Nayuta403/tech-illustration.git
cd tech-illustration
export GEMINI_API_KEY="your-key-here"

uv run scripts/gen_illustration.py \
  --topic "Your detailed topic" \
  --filename out.png \
  --style blueprint \
  --lang zh
```

## Requirements

- Python 3.10+
- [`uv`](https://docs.astral.sh/uv/) (recommended — inline script deps, no `pip install` needed)
- A Google Gemini API key: <https://aistudio.google.com/app/apikey>

The Python dependencies (`google-genai`, `pillow`) are declared inline in the script, so `uv run` handles the environment automatically.

## CLI

```
uv run scripts/gen_illustration.py \
  --topic  TEXT   # what to draw (see "Writing good topics" below)
  --filename PATH # output .png path
  [--style  blueprint | clean | dynamic | bold]   # default: blueprint
  [--lang   zh | en]                              # default: zh
  [--api-key KEY]                                 # overrides GEMINI_API_KEY
```

## Writing good topics

The quality of the output is bounded by the information density of your topic. A short prompt like *"Microservices architecture"* will give you a generic, empty-feeling image.

Instead, describe:

1. What each element draws (icons, shapes, labels)
2. All the on-image text explicitly
3. Color meanings (e.g. "red = current state")
4. The overall message in one sentence

See `SKILL.md` for a detailed before/after example.

## Model

Uses `gemini-3.1-flash-image-preview`. Since this is a preview model, Google may rename or deprecate it over time — edit the model string in `scripts/gen_illustration.py` if needed.

## Security

The script only reads `GEMINI_API_KEY` from the environment (or `--api-key`). No key is ever written to disk or logged. If you fork this, double-check before committing.

## License

MIT — see [LICENSE](LICENSE).
