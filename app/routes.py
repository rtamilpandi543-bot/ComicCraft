from fastapi import (
    APIRouter,
    Form,
    HTTPException,
    Request,
)

from fastapi.responses import (
    HTMLResponse,
    JSONResponse,
)

from fastapi.templating import Jinja2Templates


from app.config import get_settings

from app.models import PromptRequest

from app.services.gemini_flash import (
    generate_outline,
)

from app.services.gemini_pro import (
    generate_story,
)

from app.services.image_generator import (
    generate_image,
)

from app.services.layout_builder import (
    build_comic_layout,
)

from app.services.exporters import (
    save_pdf,
)

from app.utils import (
    TEMPLATES_DIR,
    job_id,
)


templates = Jinja2Templates(
    directory=str(TEMPLATES_DIR)
)

router = APIRouter()


def generate_comic(
    request: PromptRequest,
):
    """
    Complete comic generation pipeline.

    1. Generate outline.
    2. Generate story.
    3. Generate images.
    4. Build layout.
    5. Export PDF.
    """

    settings = get_settings()

    # Step 1
    outlines = generate_outline(
        request,
        settings,
    )

    # Step 2
    stories = generate_story(
        request,
        outlines,
        settings,
    )

    # Step 3
    job = job_id()

    images = []

    for panel in stories:
        image_path = generate_image(
            panel.image_prompt,
            panel.panel_number,
            settings,
            job,
        )

        images.append(image_path)

    # Step 4
    layout = build_comic_layout(
        stories,
        images,
    )

    # Step 5
    pdf_path = save_pdf(
        layout,
        request.character_name,
        job,
    )

    return layout, pdf_path


@router.get(
    "/",
    response_class=HTMLResponse,
)
def home(request: Request):
    """
    Home page.
    """

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
        },
    )


@router.post(
    "/generate",
    response_class=HTMLResponse,
)
def generate_form(
    request: Request,

    story_prompt: str = Form(...),

    character_name: str = Form(...),

    setting: str = Form(...),

    tone: str = Form(...),

    art_style: str = Form(...),
):
    """
    Generate comic from HTML form.
    """

    try:

        payload = PromptRequest(
            story_prompt=story_prompt,
            character_name=character_name,
            setting=setting,
            tone=tone,
            art_style=art_style,
        )

        layout, pdf_path = generate_comic(
            payload
        )

        return templates.TemplateResponse(
            request=request,
            name="comic_preview.html",
            context={
                "request": request,
                "layout": layout,
                "pdf_path": pdf_path,
                "input": payload.model_dump(),
            },
        )

    except Exception as exc:

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "request": request,
                "error": str(exc),
                "input": {
                    "story_prompt": story_prompt,
                    "character_name": character_name,
                    "setting": setting,
                    "tone": tone,
                    "art_style": art_style,
                },
            },
            status_code=500,
        )


@router.post("/generate-comic/json")
def generate_json(
    payload: PromptRequest,
):
    """
    JSON API endpoint.
    """

    try:

        layout, pdf_path = generate_comic(
            payload
        )

        return JSONResponse(
            {
                "success": True,
                "panels": layout,
                "pdf_path": pdf_path,
            }
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


@router.get(
    "/export-success",
    response_class=HTMLResponse,
)
def export_success(
    request: Request,
    pdf_path: str = "/",
):
    """
    PDF export success page.
    """

    return templates.TemplateResponse(
        request=request,
        name="export_success.html",
        context={
            "request": request,
            "pdf_path": pdf_path,
        },
    )


@router.get("/test-image")
def test_image(
    prompt: str = (
        "A brave fox in an enchanted "
        "forest, comic book art"
    ),
):
    """
    Test image-generation endpoint.
    """

    try:

        path = generate_image(
            prompt,
            0,
            get_settings(),
            job_id(),
        )

        return {
            "success": True,
            "image_path": path,
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc