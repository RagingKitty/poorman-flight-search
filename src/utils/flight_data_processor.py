from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.flight_models import BagAllowance, FlightOffer, Itinerary, Segment
from src.utils.flight_data_printer import print_offers

DATA_DIR = Path(__file__).resolve().parents[2] / "data"


def load_raw_data(filename: str) -> list[dict[str, Any]]:
    file_path = DATA_DIR / filename
    if not file_path.exists():
        print(f"Error: File not found at {file_path}")
        return []

    with file_path.open("r", encoding="utf-8") as file:
        data = json.load(file)
        return data if isinstance(data, list) else []


def data_extraction(filepath: str) -> list[FlightOffer] | None:
    raw_data = load_raw_data(filepath)
    if not raw_data:
        return

    offers: list[FlightOffer] = []
    for offer in raw_data:
        offer_id = offer.get("id", "")
        price_data = offer.get("price", {})
        grand_total = price_data.get("grandTotal", "")
        currency = price_data.get("currency", "")

        itineraries: list[Itinerary] = []
        for itinerary in offer.get("itineraries", []):
            itin_duration = itinerary.get("duration", "")

            segments = [
                Segment(
                    departure_iata=segment.get("departure").get("iataCode", ""),
                    departure_at=segment.get("departure").get("at", ""),
                    arrival_iata=segment.get("arrival").get("iataCode", ""),
                    arrival_at=segment.get("arrival").get("at", ""),
                    seg_duration=segment.get("duration", ""),
                )
                for segment in itinerary.get("segments", [])
            ]

            itineraries.append(Itinerary(itin_duration, segments))

        bag_allowances: list[BagAllowance] = []
        for traveler_data in offer.get("travelerPricings", []):
            for fare_detail_segment in traveler_data.get("fareDetailsBySegment", []):
                checked_data = fare_detail_segment.get("includedCheckedBags", {})
                cabin_data = fare_detail_segment.get("includedCabinBags", {})

                bag_allowances.append(
                    BagAllowance(
                        checked_weight=checked_data.get("weight", ""),
                        checked_unit=checked_data.get("weightUnit", ""),
                        cabin_weight=cabin_data.get("weight", ""),
                        cabin_unit=cabin_data.get("weightUnit", ""),
                    )
                )

        offers.append(
            FlightOffer(offer_id, itineraries, grand_total, currency, bag_allowances)
        )

    return offers


def main() -> None:
    TEST_FILE = "raw_flight_offer5.json"
    data_model = data_extraction(TEST_FILE)
    if not data_model:
        return
    print_offers(data_model)


if __name__ == "__main__":
    main()
