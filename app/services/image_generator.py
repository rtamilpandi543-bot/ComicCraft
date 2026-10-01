from pathlib import Path

from PIL import Image, ImageDraw

from app.config import Settings

from app.utils import (
    PANELS_DIR,
    safe_slug,
)


# Cached Stable Diffusion pipeline.
_PIPELINE = None


def _placeholder(
    prompt: str,
    path: Path,
    panel_number: int,
) -> None:
    """
    Create placeholder comic artwork.

    Used in demo mode or if Stable Diffusion
    is unavailable.
    """

    image = Image.new(
        "RGB",
        (768, 512),
        "#f7efe2",
    )

    draw = ImageDraw.Draw(image)

    # Border
    draw.rectangle(
        (18, 18, 750, 494),
        outline="#1f2937",
        width=8,
    )

    draw.text(
        (48, 48),
        f"COMICCRAFT • PANEL {panel_number}",
        fill="#1f2937",
    )

    # Limit text size.
    prompt_text = prompt[:240]

    draw.text(
        (48, 130),
        prompt_text,
        fill="#374151",
    )

    draw.text(
        (48, 420),
        (
            "Demo artwork — enable local "
            "Diffusers for AI images"
        ),
        fill="#6b7280",
    )

    image.save(
        path,
        format="PNG",
    )


def generate_image(
    prompt: str,
    panel_number: int,
    settings: Settings,
    job: str,
) -> str:
    """
    Generate an image for a comic panel.

    Uses local Stable Diffusion when enabled.
    Otherwise uses deterministic placeholder artwork.
    """

    path = (
        PANELS_DIR
        / f"{safe_slug(job)}-panel-{panel_number}.png"
    )

    if settings.enable_local_diffusion:

        try:

            global _PIPELINE

            if _PIPELINE is None:

                import torch

                from diffusers import (
                    StableDiffusionPipeline,
                )

                dtype = (
                    torch.float16
                    if torch.cuda.is_available()
                    else torch.float32
                )

                _PIPELINE = (
                    StableDiffusionPipeline
                    .from_pretrained(
                        settings.image_model,
                        torch_dtype=dtype,
                    )
                )

                device = (
                    "cuda"
                    if torch.cuda.is_available()
                    else "cpu"
                )

                _PIPELINE = _PIPELINE.to(
                    device
                )

            result = _PIPELINE(
                prompt,
                num_inference_steps=20,
                guidance_scale=7.0,
            )

            image = result.images[0]

            image.save(
                path,
                format="PNG",
            )

            return (
                f"/static/panels/{path.name}"
            )

        except Exception:

            if not settings.demo_mode:

                raise

    # Demo fallback.
    _placeholder(
        prompt,
        path,
        panel_number,
    )

    return (
        f"/static/panels/{path.name}"
    )