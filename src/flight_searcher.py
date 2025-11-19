from __future__ import annotations

from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from amadeus_api import AmadeusAPI
from exceptions.amadeus_exception_handler import AmadeusAPIError
from json_handler import save_to_json
from settings import (
    ADULTS,
    CURRENCY,
    DESTINATION,
    END_DATE,
    MAX_PRICE,
    ORIGIN,
    START_DATE,
)

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)
DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def _search_and_save(
    method: Callable[..., Sequence[dict[str, Any]] | None],
    params: dict[str, Any],
    outfile: Path,
) -> Path | None:
    try:
        data = method(**params)
    except AmadeusAPIError as exc:
        print(f"\nAPI Search Failed for {method.__name__}: {exc}")
        return None

    if not data:
        print(f"No data returend for {method.__name__}")
        return None

    return save_to_json(data, outfile)


def run_flight_offer() -> Path | None:
    return _search_and_save(
        AmadeusAPI().search_flight_offers,
        {
            "origin": ORIGIN,
            "destination": DESTINATION,
            "departure_date": START_DATE,
            "return_date": END_DATE,
            "currency": CURRENCY,
            "max_price": MAX_PRICE,
            "adults": ADULTS,
        },
        DATA_DIR / "raw_flight_offer5.json",
    )


# Problematic API
def run_flight_search() -> Path | None:
    return _search_and_save(
        AmadeusAPI().search_flight_date,
        {"origin": ORIGIN, "destination": DESTINATION},
        DATA_DIR / "raw_flight_date1.json",
    )


def main():
    run_flight_offer()


if __name__ == "__main__":
    main()
