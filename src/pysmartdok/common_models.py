from datetime import datetime
from enum import StrEnum
from typing import Optional

from pydantic import BaseModel, Field


class RegistrationStatus(StrEnum):
    """Status felles for QD- og RUE-rapporter (SmartDok `RegistrationStatus`)."""

    UNPROCESSED = "Unprocessed"
    OPEN = "Open"
    CLOSE = "Close"
    DISCARDED = "Discarded"


class GeoLocation(BaseModel):
    """GPS-posisjon. Brukes på tvers av flere ressurser."""

    model_config = {"populate_by_name": True}

    lat: Optional[float] = Field(None, alias="Lat", description="Breddegrad")
    lon: Optional[float] = Field(None, alias="Lon", description="Lengdegrad")


class FileInformation(BaseModel):
    """Filinformasjon for PDF-nedlasting. Brukes av flere endepunkter."""

    model_config = {"populate_by_name": True}

    filename: str = Field(alias="Filename", description="Filnavn")
    download_url: str = Field(alias="DownloadUrl", description="Nedlastingslenke")
    file_size: Optional[int] = Field(None, alias="FileSize", description="Filstørrelse")
    file_date: Optional[datetime] = Field(None, alias="FileDate", description="Fildato")
