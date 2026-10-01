from typing import List

from pydantic import BaseModel, Field, field_validator


TONES = {
    "light-hearted",
    "dramatic",
    "poetic",
    "funny",
}

STYLES = {
    "anime",
    "pixel art",
    "comic book",
    "realistic",
}

SETTINGS = {
    "school",
    "forest",
    "space",
    "city",
}


class PromptRequest(BaseModel):
    """
    User input for comic generation.
    """

    story_prompt: str = Field(
        min_length=5,
        max_length=1000,
    )

    character_name: str = Field(
        min_length=1,
        max_length=80,
    )

    setting: str = Field(
        min_length=1,
        max_length=80,
    )

    tone: str = Field(
        min_length=1,
        max_length=40,
    )

    art_style: str = Field(
        min_length=1,
        max_length=80,
    )

    @field_validator(
        "story_prompt",
        "character_name",
        "setting",
        "tone",
        "art_style",
    )
    @classmethod
    def clean_text(cls, value: str) -> str:
        """
        Remove unnecessary whitespace.
        """
        return " ".join(value.strip().split())


class PanelOutline(BaseModel):
    """
    Gemini's comic panel outline.
    """

    panel_number: int
    title: str
    scene_description: str
    image_prompt: str


class PanelStory(BaseModel):
    """
    Complete panel story.
    """

    panel_number: int
    title: str
    scene_description: str
    image_prompt: str

    caption: str = ""

    narration: str = ""

    dialogue: List[str] = Field(
        default_factory=list
    )


class ComicLayout(BaseModel):
    """
    Final comic layout.
    """

    panels: List[PanelStory]

    pdf_path: str | None = None