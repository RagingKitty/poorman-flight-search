from __future__ import annotations

import logging
from pathlib import Path

from src.models.flight_models import BagAllowance, FlightOffer, Itinerary, Segment
from src.utils.json_handler import load_raw_json_flight_offers

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def extract_flight_offers(file_path: Path) -> list[FlightOffer] | None:
    raw_data = load_raw_json_flight_offers(file_path)
    if not raw_data:
        logger.error("Raw data at %s is invalid", file_path)
        return

    logger.info("Successfully loaded raw data ---> Proceeding to process data.")

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
