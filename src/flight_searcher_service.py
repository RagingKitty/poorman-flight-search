from __future__ import annotations

import logging
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
from src.models.amadeus_api_models import FlightOffersParam
from src.utils.json_handler import save_offers_to_json

BASE_DIR = Path(__file__).resolve().parents[1]
env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path)
DATA_DIR = BASE_DIR / "data"

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def _search_and_save(
    method: Callable[..., Sequence[dict[str, Any]] | None],
    params: object,
    output_file: Path,
) -> Path | None:
    try:
        data = method(params=params)
    except AmadeusAPIError as exc:
        logger.error(
            "API search failed for %s. Details: %s",
            method.__name__,
            exc,
            exc_info=True,
        )
        return None

    if data is None:
        logger.warning(
            "API call succeeded but returned unexpected 'None' for %s", method.__name__
        )
        return None

    if len(data) == 0:
        logger.warning(
            "Search successful but no results found for %s.", method.__name__
        )
        return None

    logger.info("Successfully retrieved %d flight offers.", len(data))
    return save_offers_to_json(data, output_file)


def run_flight_offer() -> Path | None:
    flight_offer_params = FlightOffersParam(
        ORIGIN, DESTINATION, START_DATE, END_DATE, CURRENCY, MAX_PRICE, ADULTS
    )

    return _search_and_save(
        AmadeusAPI().search_flight_offers,
        flight_offer_params,
        DATA_DIR / "raw_flight_offer9.json",  # make dynamic
    )
