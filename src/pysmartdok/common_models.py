from enum import StrEnum


class RegistrationStatus(StrEnum):
    """Status felles for QD- og RUE-rapporter (SmartDok `RegistrationStatus`)."""

    UNPROCESSED = "Unprocessed"
    OPEN = "Open"
    CLOSE = "Close"
    DISCARDED = "Discarded"
