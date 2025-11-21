from __future__ import annotations

import logging
import os
from collections.abc import Callable
from dataclasses import asdict
from typing import Any

from amadeus import Client, ResponseError

from src.exceptions.amadeus_exception_handler import AmadeusAPIError
from src.models.amadeus_api_models import FlightDateParam, FlightOffersParam

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class AmadeusAPI:
    def __init__(self) -> None:
        key = os.environ.get("AMADEUS_API_KEY")
        secret = os.environ.get("AMADEUS_API_SECRET")

        if not (key and secret):
            raise ValueError("Amadeus API keys not loaded")

        self.amadeus = Client(
            client_id=key,
            client_secret=secret,
            # log_level="debug",
        )

    def _execute_api_call(
        self,
        api_method: Callable[..., Any],
        context_message: str,
        **kwargs,
    ) -> list[dict[str, Any]] | None:
        try:
            response = api_method(**kwargs)

            logger.info("%s: Successful", context_message)
            return response.data

        except ResponseError as exc:
            response = exc.response
            status = response.status_code
            errors = response.result.get("errors", [])

            detail = (
                errors[0].get("detail", "No additional detail")
                if errors
                else "Unknown error"
            )

            logger.error(
                "API call failure: %s (Status: %d, Detail: %s)",
                context_message,
                status,
                detail,
                exc_info=True,
            )

            raise AmadeusAPIError(
                message=f"{context_message} failed.",
                status_code=status,
                detail=detail,
            ) from exc

    def search_flight_offers(
        self,
        *,
        params: FlightOffersParam,
    ) -> list[dict[str, Any]] | None:
        api_params = asdict(params)

        return self._execute_api_call(
            api_method=self.amadeus.shopping.flight_offers_search.get,
            context_message="search_flight_offers",
            **api_params,
        )

    def search_flight_date(
        self, *, params: FlightDateParam
    ) -> list[dict[str, Any]] | None:
        api_params = asdict(params)

        return self._execute_api_call(
            api_method=self.amadeus.shopping.flight_dates.get,
            context_message="search_flight_dates",
            **api_params,
        )
