---
name: tech-illustration
description: Generate multi-style technical illustrations (blueprint, clean, dynamic, bold) for articles, slides, and docs using Google's Gemini 3.1 Flash Image model. Use when the user asks to create a tech diagram, infographic, architecture illustration, or article cover image.
---

# Tech Illustration Generator

Generate technical illustrations with multiple styles for tech articles, presentation slides, and documentation. Uses Google's Gemini 3.1 Flash Image model.

## Supported Styles

- **blueprint** (default): White/light background, engineering grid, navy blue + orange two-color scheme, clean line art, flat design. Matches the style of professional tech presentation slides.
- **clean**: Minimalist engineering diagram, vector art aesthetic, white background.
- **dynamic**: Dynamic isometric composition, glowing energy flows, dark background, rich data visualization elements.
- **bold**: Avant-garde editorial style, massive typography, high-impact visual hierarchy, rebellious design.

See `examples/` for a rendered sample of each style.

## Language Support

- `--lang zh` (default): All text in the image will be in Simplified Chinese.
- `--lang en`: All text in English.

## Topic description principles (important)

The core variable for image quality is the information density of the `topic`. Short topics produce sparse, empty-looking images. Before calling the script, expand the topic into a detailed visual description:

1. **Describe what each element draws** — not "four stages", but "four cards, each containing icon + title + one-line caption".
2. **Specify concrete icons** — not "with icon", but "a popup saying 'Allow / Deny'" or "a folder with a lock".
3. **Write out all on-image text** — every label that should appear must be in the topic; don't expect the model to fill it in.
4. **Specify color meaning** — e.g., "red = danger / current state", "green = mature", "dashed = future / uncertain".
5. **State the overall message** — end with a line like "Overall message: ...".

**Weak example** (low information density):

```
"Android permission evolution vs Skill trust evolution timeline"
```

**Strong example** (rich information, good result):

```
"Technical infographic: Android permission evolution vs Skill trust evolution.
Top half: four stages —
  (1) Pre-Android 4.0: a popup showing 'Location, Camera, Contacts' all checked, marked red, with caption 'Install-time permission list, user can only accept all';
  (2) Android 6.0: a small popup saying 'Allow / Deny', caption 'Runtime permission prompts';
  (3) Android 10: a folder with a lock, caption 'Scoped storage';
  (4) Android 12: a dashboard, caption 'Privacy panel showing which app accessed what, when'.
Bottom half 'Skill trust evolution': first node solid red 'Current: no permission model — one SKILL.md + GitHub account can publish', followed by three dashed nodes with question marks. Labeled 'Skills are roughly here'.
Overall message: the Skill trust system is still at where Android was a decade ago."
```

## Usage

```bash
export GEMINI_API_KEY="your-key-here"

uv run scripts/gen_illustration.py \
  --topic "Your detailed topic" \
  --filename "output.png" \
  --style blueprint \
  --lang zh
```

## Parameters

| Flag | Short | Required | Default | Description |
|------|-------|----------|---------|-------------|
| `--topic` | `-t` | yes | — | The technical concept to illustrate (see principles above). |
| `--filename` | `-f` | yes | — | Output file path (`.png`). |
| `--style` | `-s` | no | `blueprint` | One of `blueprint`, `clean`, `dynamic`, `bold`. |
| `--lang` | `-l` | no | `zh` | `zh` for Simplified Chinese labels, `en` for English. |
| `--api-key` | `-k` | no | `$GEMINI_API_KEY` | Override the API key from env. |

## Requirements

- Python 3.10+
- [`uv`](https://docs.astral.sh/uv/) (recommended) — the script declares its deps inline; no `pip install` needed.
- A Google Gemini API key — get one at <https://aistudio.google.com/app/apikey>.
