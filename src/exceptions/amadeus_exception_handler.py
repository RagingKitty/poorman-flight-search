class AmadeusAPIError(Exception):
    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        detail: str | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.detail = detail

    def __str__(self) -> str:
        if self.status_code:
            detail = self.detail or "No additional detail"
            return f"[{self.status_code}] AmadeusAPIError: {self.args[0]}. Detail: {detail}"
        return f"AmadeusAPIError: {self.args[0]}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(status_code={self.status_code!r}, detail={self.detail!r})"
