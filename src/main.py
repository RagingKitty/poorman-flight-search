import logging
import logging.config
from pathlib import Path
from typing import Final

import yaml

from src.flight_searcher_service import run_flight_offer
from src.utils.date_iterator_handler import is_date_valid
from src.utils.flight_data_printer import print_flight_offers
from src.utils.flight_data_processor import extract_flight_offers

BASE_DIR: Final[Path] = Path(__file__).resolve().parent
CONFIG_FILE_PATH: Final[Path] = BASE_DIR / "config" / "logging.yaml"

DATA_DIR: Final[Path] = Path(__file__).resolve().parents[1] / "data"


def setup_logging(config_path=CONFIG_FILE_PATH) -> None:
    try:
        with config_path.open("r") as file:
            config = yaml.safe_load(file.read())
            logging.config.dictConfig(config)
    except FileNotFoundError:
        print(
            f"ERROR: Logging config file not found at {config_path}, using basic config."
        )
        logging.basicConfig(level=logging.INFO)
    except Exception as exc:
        print(f"Error loading logging config: {exc}")
        logging.basicConfig(level=logging.INFO)


def main():
    is_date_valid("2027-01-01")  # Just testing

    flight_file_path = run_flight_offer()
    if not flight_file_path:
        logging.warning(
            "Flight search failed or returned no offers. Skipping data processing."
        )
        return

    data_model = extract_flight_offers(flight_file_path)
    if not data_model:
        logging.error(
            "Failed to extract data model from saved file: %s", flight_file_path
        )
        return

    print_flight_offers(data_model)


if __name__ == "__main__":
    setup_logging()
    main()
