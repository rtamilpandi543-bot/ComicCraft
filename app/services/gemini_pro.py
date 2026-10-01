import json

from app.config import Settings

from app.models import (
    PanelOutline,
    PanelStory,
    PromptRequest,
)


def _demo_story(
    request: PromptRequest,
    outlines: list[PanelOutline],
) -> list[PanelStory]:
    """
    Generate demo story content.
    """

    result = []

    for outline in outlines:

        result.append(
            PanelStory(
                **outline.model_dump(),

                caption=(
                    f"{outline.title}: "
                    "the adventure unfolds."
                ),

                narration=(
                    f"{request.character_name} moves "
                    f"through the {request.setting}, "
                    "balancing curiosity with courage. "
                    f"{outline.scene_description}"
                ),

                dialogue=[
                    (
                        f"{request.character_name}: "
                        "We can do this!"
                    )
                ],
            )
        )

    return result


def generate_story(
    request: PromptRequest,
    outlines: list[PanelOutline],
    settings: Settings,
) -> list[PanelStory]:
    """
    Generate polished narration and dialogue
    using Gemini.
    """

    if not settings.gemini_api_key:

        if settings.demo_mode:

            return _demo_story(
                request,
                outlines,
            )

        raise RuntimeError(
            "GEMINI_API_KEY is not configured."
        )

    from google import genai
    from google.genai import types

    client = genai.Client(
        api_key=settings.gemini_api_key
    )

    outline_json = json.dumps(
        [
            outline.model_dump()
            for outline in outlines
        ],
        ensure_ascii=False,
    )

    prompt = f"""
Expand this comic outline into polished,
panel-by-panel narration and dialogue.

Return ONLY valid JSON.

Character:
{request.character_name}

Setting:
{request.setting}

Tone:
{request.tone}

Art style:
{request.art_style}

Outline:
{outline_json}

Requirements:

1. Preserve panel numbers.
2. Preserve titles.
3. Preserve scene descriptions.
4. Preserve image prompts.
5. Create natural narration.
6. Create short dialogue.
7. Maintain continuity between panels.
8. Match the requested tone.
9. Avoid excessive text.
"""

    response = client.models.generate_content(
        model=settings.gemini_story_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=list[PanelStory],
            temperature=0.9,
        ),
    )

    if response.parsed is not None:

        data = response.parsed

    else:

        data = json.loads(
            response.text
        )

    return [
        PanelStory.model_validate(item)
        for item in data
    ]