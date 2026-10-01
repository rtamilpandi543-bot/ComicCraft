from app.models import PanelStory


def build_comic_layout(
    stories: list[PanelStory],
    image_paths: list[str],
) -> list[dict]:
    """
    Combine generated story data and image paths.
    """

    if len(stories) != len(image_paths):
        raise ValueError(
            "Number of stories and images must match."
        )

    layout = []

    for index, story in enumerate(stories):

        panel = {
            **story.model_dump(),
            "image_path": image_paths[index],
        }

        layout.append(panel)

    return layout