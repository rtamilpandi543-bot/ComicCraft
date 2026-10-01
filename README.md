# ComicCraft — AI Comic Story Creator

ComicCraft is an AI-powered web application that converts
a user's story idea into a five-panel comic.

The application uses:

- FastAPI
- Jinja2
- Google Gemini
- Hugging Face Diffusers
- Stable Diffusion
- Pillow
- FPDF2
- Pydantic
- Pytest


# Features

## Story generation

The user provides:

- Story prompt
- Main character
- Setting
- Tone
- Art style

The system creates a five-panel comic.


## AI pipeline

The application follows this pipeline:

User Prompt
    |
    v
Gemini Outline Generation
    |
    v
Gemini Story Generation
    |
    v
Image Generation
    |
    v
Comic Layout
    |
    v
PDF Export


# Development mode

The application supports demo mode.

Demo mode does not require:

- Gemini API key
- Stable Diffusion
- GPU

Set:

DEMO_MODE=true


# Installation

Windows PowerShell:

    cd ComicCraft

    py -3 -m venv .venv

    .\.venv\Scripts\Activate.ps1

    python -m pip install --upgrade pip

    pip install -r requiyements.txt


# Environment configuration

Copy:

    .env.example

to:

    .env


For demo mode:

    DEMO_MODE=true

    ENABLE_LOCAL_DIFFUSION=false


For Gemini:

    GEMINI_API_KEY=your_api_key


# Run application

    uvicorn app.main:app --reload


Open:

    http://127.0.0.1:8000


# API documentation

Open:

    http://127.0.0.1:8000/docs


# Health endpoint

Open:

    http://127.0.0.1:8000/health


# Image test endpoint

Open:

    http://127.0.0.1:8000/test-image


# API generation

POST:

    /generate-comic/json


Example:

    {
        "story_prompt": "A brave fox explores an enchanted forest",
        "character_name": "Kavi",
        "setting": "forest",
        "tone": "dramatic",
        "art_style": "comic book"
    }


# Testing

Run:

    pytest -q


# Stable Diffusion

Local Stable Diffusion can be enabled with:

    ENABLE_LOCAL_DIFFUSION=true

The system will then attempt to load:

    stable-diffusion-v1-5/stable-diffusion-v1-5

Local image generation can require significant disk space,
RAM and GPU resources.

If image generation fails and demo mode is enabled,
ComicCraft automatically creates placeholder artwork.


# Project structure

ComicCraft/

    app/

        __init__.py

        config.py

        main.py

        models.py

        routes.py

        utils.py

        services/

            __init__.py

            gemini_flash.py

            gemini_pro.py

            image_generator.py

            layout_builder.py

            exporters.py


    templates/

        base.html

        index.html

        comic_preview.html

        export_success.html


    static/

        css/

            styles.css

        js/

            app.js

        panels/

        exports/


    tests/

        test_app.py


    .env.example

    .gitignore

    requirements.txt

    pyproject.toml

    README.md