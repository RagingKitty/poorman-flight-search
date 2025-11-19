from __future__ import annotations

import json
from collections.abc import Sequence
from pathlib import Path
from typing import Any


def save_to_json(data: Sequence[dict[str, Any]], file_path: Path) -> Path:
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with file_path.open("w", encoding="utf-8") as fp:
        json.dump(data, fp, indent=4, ensure_ascii=False)
    print(f"Saved {len(data)} records -> {file_path}")

    return file_path
