import json
import sys
from pathlib import Path


def get_application_directory() -> Path:

    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent

    return Path(__file__).resolve().parent.parent

def get_resource_directory() -> Path:
    if getattr(sys, "frozen", False):
        return Path(getattr(sys, "_MEIPASS"))

    return Path(__file__).resolve().parent


def load_api_base_url() -> str:

    config_path = get_application_directory() / "config.json"

    if not config_path.exists():
        raise FileNotFoundError(
            f"Configuration file was not found:\n{config_path}"
        )

    try:
        with config_path.open("r", encoding="utf-8") as config_file:
            config = json.load(config_file)
    except json.JSONDecodeError as error:
        raise ValueError(
            f"The configuration file contains invalid JSON:\n{error}"
        ) from error

    api_base_url = config.get("api_base_url")

    if not isinstance(api_base_url, str) or not api_base_url.strip():
        raise ValueError(
            "'api_base_url' is missing or invalid in config.json."
        )

    return api_base_url.rstrip("/")


API_BASE_URL = load_api_base_url()
