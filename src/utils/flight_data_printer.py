from src.flight_models import FlightOffer


def print_offers(offers: list[FlightOffer]) -> None:
    print("-------- DATA EXTRACTION --------")
    print(f"No. of Entry: {len(offers)}")

    for offer in offers:
        print(f"\n{offer.offer_id} {offer.grand_total} {offer.currency}")

        for index, itinerary in enumerate(offer.itineraries, 1):
            print(f"  > ITINERARY {index}  {itinerary.itin_duration}")
            for segment in itinerary.segments:
                print(
                    f"    - {segment.departure_iata} → {segment.arrival_iata}  ({segment.seg_duration})"
                )

        print("  > BAG ALLOWANCE:")
        for index, bag_allowance in enumerate(offer.bag_allowances, 1):
            print(
                f"    Allowance {index}: {bag_allowance.checked_weight}{bag_allowance.checked_unit} checked / "
                f"{bag_allowance.cabin_weight}{bag_allowance.cabin_unit} cabin"
            )
