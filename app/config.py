from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables
    and the .env file.
    """

    app_name: str = "ComicCraft"

    # Gemini
    gemini_api_key: str = ""

    # Optional Hugging Face token
    hf_api_key: str = ""

    # Gemini models
    gemini_outline_model: str = "gemini-2.5-flash"
    gemini_story_model: str = "gemini-2.5-pro"

    # Image generation
    image_model: str = (
        "stable-diffusion-v1-5/stable-diffusion-v1-5"
    )

    # Feature flags
    enable_local_diffusion: bool = False
    demo_mode: bool = True

    # Comic configuration
    panel_count: int = 5

    # Server
    host: str = "127.0.0.1"
    port: int = 8000

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()