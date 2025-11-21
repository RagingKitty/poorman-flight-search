from __future__ import annotations

from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from src.api.amadeus_api import AmadeusAPI
from src.config.settings import (
    ADULTS,
    CURRENCY,
    DESTINATION,
    END_DATE,
    MAX_PRICE,
    ORIGIN,
    START_DATE,
)
from src.exceptions.amadeus_exception_handler import AmadeusAPIError
from src.models.amadeus_api_models import FlightDateParam, FlightOffersParam
from src.utils.json_handler import save_offers_to_json

from .__version__ import __version__

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)
DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def _search_and_save(
    method: Callable[..., Sequence[dict[str, Any]] | None],
    params: object,
    outfile: Path,
) -> Path | None:
    try:
        data = method(params=params)
    except AmadeusAPIError as exc:
        print(f"\nAPI Search Failed for {method.__name__}: {exc}")
        return None

    if not data:
        print(f"No data returend for {method.__name__}")
        return None

    return save_offers_to_json(data, outfile)


def run_flight_offer() -> Path | None:
    flight_offer_params = FlightOffersParam(
        ORIGIN, DESTINATION, START_DATE, END_DATE, CURRENCY, MAX_PRICE, ADULTS
    )

    return _search_and_save(
        AmadeusAPI().search_flight_offers,
        flight_offer_params,
        DATA_DIR / "raw_flight_offer7.json",
    )


# Problematic API
def run_flight_search() -> Path | None:
    flight_data_params = FlightDateParam(ORIGIN, DESTINATION)
    return _search_and_save(
        AmadeusAPI().search_flight_date,
        flight_data_params,
        DATA_DIR / "raw_flight_date1.json",
    )


def main():
    print(f"--- Starting Poor Man's Flight Searcher (v{__version__}) ---")
    run_flight_offer()


if __name__ == "__main__":
    main()
