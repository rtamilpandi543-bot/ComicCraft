import re
from pathlib import Path
from uuid import uuid4


BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_DIR = BASE_DIR / "static"

PANELS_DIR = STATIC_DIR / "panels"

EXPORTS_DIR = STATIC_DIR / "exports"

TEMPLATES_DIR = BASE_DIR / "templates"


# Create directories automatically.
for folder in (
    PANELS_DIR,
    EXPORTS_DIR,
):
    folder.mkdir(
        parents=True,
        exist_ok=True,
    )


def safe_slug(
    value: str,
    max_len: int = 48,
) -> str:
    """
    Convert text into a safe filename slug.
    """

    slug = re.sub(
        r"[^a-zA-Z0-9_-]+",
        "-",
        value.strip(),
    )

    slug = slug.strip("-").lower()

    return slug[:max_len] or "comic"


def job_id() -> str:
    """
    Generate a unique comic generation ID.
    """

    return uuid4().hex[:12]