from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():
    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"


def test_home():
    response = client.get("/")

    assert response.status_code == 200

    assert "ComicCraft" in response.text


def test_json_generation_demo():

    response = client.post(
        "/generate-comic/json",
        json={
            "story_prompt": (
                "A fox explores "
                "an enchanted forest"
            ),
            "character_name": "Kavi",
            "setting": "forest",
            "tone": "dramatic",
            "art_style": "comic book",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True

    assert len(
        data["panels"]
    ) == 5

    assert data[
        "pdf_path"
    ].endswith(".pdf")