from pathlib import Path
import textwrap

from fpdf import FPDF

from app.utils import (
    EXPORTS_DIR,
    safe_slug,
)


def save_pdf(
    layout: list[dict],
    title: str,
    job: str,
) -> str:
    """
    Export the complete comic to PDF.
    """

    pdf = FPDF(
        orientation="P",
        unit="mm",
        format="A4",
    )

    pdf.set_auto_page_break(
        auto=True,
        margin=14,
    )

    for panel in layout:

        pdf.add_page()

        # Panel heading
        pdf.set_font(
            "Helvetica",
            "B",
            18,
        )

        pdf.multi_cell(
            0,
            10,
            (
                f"Panel "
                f"{panel['panel_number']}: "
                f"{panel['title']}"
            ),
            new_x="LMARGIN",
            new_y="NEXT",
        )

        # Find local image.
        image_path = panel.get(
            "image_path",
            "",
        )

        local_path = (
            Path(__file__).resolve().parents[2]
            / image_path.lstrip("/")
        )

        if local_path.exists():

            pdf.image(
                str(local_path),
                x=15,
                y=35,
                w=180,
            )

            pdf.set_y(145)

        # Scene
        pdf.set_font(
            "Helvetica",
            "I",
            11,
        )

        scene = textwrap.fill(
            panel.get(
                "scene_description",
                "",
            ),
            95,
        )

        pdf.multi_cell(
            0,
            7,
            scene,
            new_x="LMARGIN",
            new_y="NEXT",
        )

        pdf.ln(2)

        # Caption
        pdf.set_font(
            "Helvetica",
            "B",
            11,
        )

        caption = textwrap.fill(
            panel.get(
                "caption",
                "",
            ),
            95,
        )

        pdf.multi_cell(
            0,
            7,
            caption,
            new_x="LMARGIN",
            new_y="NEXT",
        )

        # Narration
        pdf.set_font(
            "Helvetica",
            "",
            11,
        )

        narration = textwrap.fill(
            panel.get(
                "narration",
                "",
            ),
            95,
        )

        pdf.multi_cell(
            0,
            7,
            narration,
            new_x="LMARGIN",
            new_y="NEXT",
        )

        # Dialogue
        for line in panel.get(
            "dialogue",
            [],
        ):

            dialogue = textwrap.fill(
                line,
                95,
            )

            pdf.multi_cell(
                0,
                7,
                dialogue,
                new_x="LMARGIN",
                new_y="NEXT",
            )

    filename = (
        f"{safe_slug(title)}-{job}.pdf"
    )

    target = (
        EXPORTS_DIR / filename
    )

    pdf.output(
        str(target)
    )

    return (
        f"/static/exports/{filename}"
    )