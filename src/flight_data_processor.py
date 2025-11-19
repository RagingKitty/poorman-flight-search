# Testing phase:
# 1. drop json into this script.
# 2. clean-up json and get the price for args[0]

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_raw_data(filename: str) -> list[dict[str, Any]] | None:
    file_path = DATA_DIR / filename
    if not file_path.exists():
        print(f"Error: File not found at {file_path}")
        return None

    with file_path.open("r", encoding="utf-8") as file:
        return json.load(file)


# def test_minimal_extraction(filename: str):
#     raw_offers = load_raw_data(filename)

#     if not raw_offers:
#         return

#     offers_to_process = raw_offers[:5]

#     print("--- Extraction Test ---")
#     print(f"Target File: {filename}")

#     for index, offer in enumerate(offers_to_process):
#         offer_id = offer.get("id")
#         price_data = offer.get("price", {})
#         grand_total = price_data.get("grandTotal")
#         currency = price_data.get("currency", "")

#         print(f"Offer #{index + 1} (ID: {offer_id}) -> Price: {grand_total} {currency}")

#     print("-------------------------------")


def test_complex_extraction(filename: str):
    raw_offers = load_raw_data(filename)
    if not raw_offers:
        return

    offers_to_process = raw_offers[:5]

    print("--- Complex Extraction Test ---")
    print(f"Target File: {filename}")
    print(f"Offers Processed: {len(offers_to_process)}")

    for offer_index, offer in enumerate(offers_to_process):
        offer_id = offer.get("id")
        price_data = offer.get("price", {})

        grand_total = price_data.get("grandTotal")
        currency = price_data.get("currency", "")

        print("\n===================================")
        print(
            f"OFFER {offer_index + 1} (ID: {offer_id}) | Total: {grand_total} {currency}"
        )

        for itinerary_index, itinerary in enumerate(offer.get("itineraries", [])):
            itinerary_duration = itinerary.get("duration")
            print(
                f"  > ITINERARY {itinerary_index + 1} (Duration: {itinerary_duration})"
            )

            for segment_index, segment in enumerate(itinerary.get("segments", [])):
                departure = segment.get("departure", {})
                arrival = segment.get("arrival", {})
                print(f"    - SEGMENT {segment_index+1}:")
                print(
                    f"      Departure: {departure.get('iataCode')} at {departure.get('at')}"
                )
                print(
                    f"      Arrival:   {arrival.get('iataCode')} at {arrival.get('at')}"
                )
                print(f"      Flight Time: {segment.get('duration')}")

        print("\n  > BAG ALLOWANCE DETAILS:")

        for travel_index, travel in enumerate(offer.get("travelerPricings", [])):

            for segment_detail_index, segment_detail in enumerate(
                travel.get("fareDetailsBySegment", [])
            ):
                checked_bags = segment_detail.get("includedCheckedBags", {})
                cabin_bags = segment_detail.get("includedCabinBags", {})

                checked_weight = checked_bags.get("weight", 0)
                checked_unit = checked_bags.get("weightUnit", "KG")

                cabin_weight = cabin_bags.get("weight", 0)
                cabin_unit = cabin_bags.get("weightUnit", "KG")

                print(
                    f"      Segment {segment_detail_index + 1}: Checked Bags: {checked_weight} {checked_unit} | Cabin Bags: {cabin_weight} {cabin_unit}"
                )

    print("\n--- Extraction Test Complete ---")


def main() -> None:
    TEST_FILE = "raw_flight_offer4.json"
    # test_minimal_extraction(TEST_FILE)
    test_complex_extraction(TEST_FILE)


if __name__ == "__main__":
    main()
