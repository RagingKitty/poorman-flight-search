import logging
from datetime import datetime
from typing import Final

SAMPLE_DATE: Final[str] = "2027-02-20"
DATE_FORMAT: Final[str] = "%Y-%m-%d"

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def is_date_valid(date: str) -> bool:
    try:
        datetime.strptime(date, DATE_FORMAT)
        logger.info("Successfully validated date: %s", date)
        return True
    except ValueError as exc:
        logger.error("Date parsing failed: %s\n----> Detail: %s", date, exc)
        return False
