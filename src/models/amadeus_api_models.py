from dataclasses import dataclass


@dataclass(frozen=True)
class FlightOffersParam:
    originLocationCode: str
    destinationLocationCode: str
    departureDate: str
    returnDate: str
    currencyCode: str = "MYR"
    maxPrice: int | None = None
    adults: int = 1


@dataclass(frozen=True)
class FlightDateParam:
    origin: str
    destination: str
