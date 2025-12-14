import logging
from collections.abc import Generator
from datetime import date as _date
from datetime import timedelta
from typing import Final

DATE_FORMAT: Final[str] = "%Y-%m-%d"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def is_date_valid(date: str) -> bool:
    try:
        _date.fromisoformat(date)
        logger.info("Successfully validated date: %s", date)
        return True
    except ValueError:
        logger.exception("Date parsing failed: %s", date)
        return False


def iterate_date_by_duration(
    initial_departure_date: str,
    trip_duration_days: int,
    search_window_days: int,
) -> Generator[dict[str, str], None, None]:
    if not is_date_valid(initial_departure_date):
        raise ValueError("Cannot proceed with date iteration.")

    base_date: _date = _date.fromisoformat(initial_departure_date)
    trip_duration_timedelta: timedelta = timedelta(days=trip_duration_days)

    return (
        {
            "start_date": (base_date + timedelta(days=day)).strftime(DATE_FORMAT),
            "end_date": (
                base_date + timedelta(days=day) + trip_duration_timedelta
            ).strftime(DATE_FORMAT),
        }
        for day in range(search_window_days)
    )
