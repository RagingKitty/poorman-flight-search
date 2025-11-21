from __future__ import annotations

from dataclasses import dataclass


@dataclass
class BagAllowance:
    checked_weight: str
    checked_unit: str
    cabin_weight: str
    cabin_unit: str


@dataclass
class Segment:
    departure_iata: str
    departure_at: str
    arrival_iata: str
    arrival_at: str
    seg_duration: str


@dataclass
class Itinerary:
    itin_duration: str
    segments: list[Segment]


@dataclass
class FlightOffer:
    offer_id: str
    itineraries: list[Itinerary]
    grand_total: str
    currency: str
    bag_allowances: list[BagAllowance]
