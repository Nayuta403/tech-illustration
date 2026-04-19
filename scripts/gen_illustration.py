#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "google-genai>=1.0.0",
#     "pillow>=10.0.0",
# ]
# ///
"""
Generate technical illustrations using Gemini 3.1 Flash Image.
Supports multiple styles (blueprint, clean, dynamic, bold).

Usage:
    uv run gen_illustration.py --topic "Kubernetes Architecture" --filename "k8s_arch.png" --style blueprint --lang zh
"""

import argparse
import os
import sys
from pathlib import Path
from io import BytesIO
import base64

# Defined Styles
STYLES = {
    "blueprint": (
        ", technical illustration in hand-drawn engineering sketch style, white background with subtle "
        "light grey engineering grid pattern, thin decorative border with corner brackets, "
        "ONLY two colors: deep navy blue (#1a3a5c) for lines and text, vibrant orange (#e8742a) for accents and highlights, "
        "hand-drawn line art aesthetic with slight sketch feel, objects drawn with light isometric perspective giving subtle 3D depth, "
        "scattered decorative technical elements: small gears, circuit board traces, connection nodes, "
        "bold large Chinese title text in top-left area, organic asymmetric layout (not rigid grid), "
        "mix of text annotations on one side and illustrated objects on the other, "
        "detailed illustrative icons (not simple geometric shapes), "
        "high quality, 8k resolution, professional tech presentation slide --ar 16:9"
    ),
    "clean": (
        ", clean technical illustration style, vector art aesthetic, minimalist engineering diagram, "
        "schematic blueprint elements, wireframe details, tech blue and vibrant orange accent colors "
        "on white background, subtle engineering grid pattern, professional presentation slide layout, "
        "high quality, 8k resolution, clear visual hierarchy --ar 16:9"
    ),
    "dynamic": (
        ", dynamic technical illustration style, bold isometric composition, rich data visualization elements, "
        "floating UI holographic interfaces, connected nodes and network flows, vibrant gradients (tech blue, neon orange, cyber green), "
        "complex but organized layout, futuristic dashboard aesthetic, high contrast, detailed icons and labels, "
        "cinematic lighting, 8k resolution, award-winning graphic design --ar 16:9"
    ),
    "bold": (
        ", Bold avant-garde technical illustration, massive typography integration, breaking the grid layout, "
        "exaggerated schematic elements, dynamic perspective, high-impact visual hierarchy, abstract data visualization metaphors, "
        "tech blue and neon orange, clean but rebellious design, 8k resolution, editorial style --ar 16:9"
    )
}

LANG_PROMPTS = {
    "zh": "IMPORTANT: All text labels, titles, annotations and descriptions in the image MUST be written in Simplified Chinese (简体中文). Do NOT use English for any visible text. ",
    "en": ""
}

def get_api_key(provided_key):
    if provided_key:
        return provided_key
    return os.environ.get("GEMINI_API_KEY")

def main():
    parser = argparse.ArgumentParser(
        description="Generate Tech Illustrations (Gemini Flash)"
    )
    parser.add_argument(
        "--topic", "-t",
        required=True,
        help="The technical topic or concept to illustrate"
    )
    parser.add_argument(
        "--filename", "-f",
        required=True,
        help="Output filename (e.g., arch_diagram.png)"
    )
    parser.add_argument(
        "--style", "-s",
        choices=STYLES.keys(),
        default="blueprint",
        help="Illustration style: blueprint (default, minimalist grid), clean, dynamic (futuristic), or bold (avant-garde)"
    )
    parser.add_argument(
        "--lang", "-l",
        choices=["zh", "en"],
        default="zh",
        help="Language for text labels in the image (default: zh for Chinese)"
    )
    parser.add_argument(
        "--api-key", "-k",
        help="Gemini API key"
    )

    args = parser.parse_args()

    api_key = get_api_key(args.api_key)
    if not api_key:
        print("Error: No API key provided (set GEMINI_API_KEY).", file=sys.stderr)
        sys.exit(1)

    from google import genai
    from google.genai import types
    from PIL import Image as PILImage

    client = genai.Client(api_key=api_key)
    output_path = Path(args.filename)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Get selected style prompt
    style_prompt = STYLES[args.style]
    lang_prompt = LANG_PROMPTS[args.lang]

    # Combine: language instruction + user topic + style
    full_prompt = f"{lang_prompt}{args.topic}{style_prompt}"
    print(f"Generating illustration for: '{args.topic}'")
    print(f"Style: {args.style}, Language: {args.lang}")
    print(f"Full Prompt: {full_prompt}")

    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-image-preview",
            contents=full_prompt,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
            )
        )

        image_saved = False
        parts = []
        if response.candidates and response.candidates[0].content:
            parts = response.candidates[0].content.parts or []
        if parts:
            for part in parts:
                if part.inline_data:
                    image_data = part.inline_data.data
                    if isinstance(image_data, str):
                        image_bytes = base64.b64decode(image_data)
                    else:
                        image_bytes = image_data

                    image = PILImage.open(BytesIO(image_bytes))
                    image.save(str(output_path), "PNG")
                    image_saved = True
                    break

        if image_saved:
            full_path = output_path.resolve()
            print(f"\nImage saved: {full_path}")
            print(f"MEDIA: {full_path}")
        else:
            print("Error: No image generated.", file=sys.stderr)
            sys.exit(1)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
