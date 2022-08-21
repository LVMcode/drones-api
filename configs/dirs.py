from pathlib import Path


MEDICATION_IMAGES_PATH: str = "static/medication_images"


def create_paths():
    Path(MEDICATION_IMAGES_PATH).mkdir(parents=True, exist_ok=True)
