import json
from typing import Any

from app.config import Settings
from app.models import (
    PanelOutline,
    PromptRequest,
)


def _demo_outline(
    request: PromptRequest,
    count: int,
) -> list[PanelOutline]:
    """
    Generate deterministic demo outlines.

    This allows the application to run without
    a Gemini API key.
    """

    beats = [
        (
            "The Spark",
            (
                "The hero discovers the first clue "
                "that something unusual is happening."
            ),
        ),
        (
            "Into the Unknown",
            (
                "The hero enters the setting and "
                "follows the mystery deeper."
            ),
        ),
        (
            "The Challenge",
            (
                "A surprising obstacle forces the "
                "hero to make a brave choice."
            ),
        ),
        (
            "The Turning Point",
            (
                "The hero uses creativity and courage "
                "to change the situation."
            ),
        ),
        (
            "A New Beginning",
            (
                "The adventure resolves with a memorable "
                "final image and a hint of what comes next."
            ),
        ),
    ]

    result = []

    for i in range(count):

        title, description = beats[
            i % len(beats)
        ]

        scene = (
            f"{description} "
            f"Story premise: {request.story_prompt}"
        )

        image_prompt = (
            f"{request.art_style} illustration, "
            f"{description} "
            f"Main character: {request.character_name}. "
            f"Setting: {request.setting}. "
            f"Tone: {request.tone}. "
            "Consistent character design, "
            "cinematic composition, "
            "no text."
        )

        result.append(
            PanelOutline(
                panel_number=i + 1,
                title=title,
                scene_description=scene,
                image_prompt=image_prompt,
            )
        )

    return result


def generate_outline(
    request: PromptRequest,
    settings: Settings,
) -> list[PanelOutline]:
    """
    Generate comic outline using Gemini.

    Falls back to demo mode when Gemini is not configured.
    """

    if not settings.gemini_api_key:

        if settings.demo_mode:

            return _demo_outline(
                request,
                settings.panel_count,
            )

        raise RuntimeError(
            "GEMINI_API_KEY is not configured."
        )

    # Import only when Gemini is actually needed.
    from google import genai
    from google.genai import types

    client = genai.Client(
        api_key=settings.gemini_api_key
    )

    prompt = f"""
Create a structured {settings.panel_count}-panel comic outline.

Return ONLY valid JSON.

Story:
{request.story_prompt}

Main character:
{request.character_name}

Setting:
{request.setting}

Tone:
{request.tone}

Art style:
{request.art_style}

Each panel must contain:

- panel_number
- title
- scene_description
- image_prompt

Requirements:

1. Keep the main character visually consistent.
2. Create a clear beginning, middle and ending.
3. Make each panel visually interesting.
4. Do not put dialogue inside image prompts.
5. Avoid text inside generated artwork.
"""

    response = client.models.generate_content(
        model=settings.gemini_outline_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=list[PanelOutline],
            temperature=0.9,
        ),
    )

    data: Any

    if response.parsed is not None:

        data = response.parsed

    else:

        data = json.loads(
            response.text
        )

    return [
        PanelOutline.model_validate(item)
        for item in data
    ]