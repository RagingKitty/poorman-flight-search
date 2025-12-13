from __future__ import annotations

import json
import logging
from collections.abc import Sequence
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def load_raw_json_flight_offers(file_path: Path) -> list[dict[str, Any]]:
    if not file_path.exists():
        logger.error("File not found at %s", file_path)
        return []

    try:
        with file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except json.JSONDecodeError:
        logger.error("Failed to decode JSON from %s", file_path, exc_info=True)
        return []


def save_offers_to_json(data: Sequence[dict[str, Any]], file_path: Path) -> Path | None:
    file_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with file_path.open("w", encoding="utf-8") as fp:
            json.dump(data, fp, indent=4, ensure_ascii=False)
        logger.info("Saved %d records -> %s", len(data), file_path)
    except Exception as exc:
        logger.error("Error saving data to json: %s", exc, exc_info=True)
        return None

    return file_path
