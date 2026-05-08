from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from .common_models import RegistrationStatus


class QDReport(BaseModel):
    """Kvalitetsavviksrapport. Kilde: GET /qd/v2."""

    model_config = {"populate_by_name": True}

    id: int = Field(alias="Id", description="Unik rapport-ID")
    status: RegistrationStatus = Field(alias="Status", description="Status")
    submit_date: datetime = Field(alias="SubmitDate", description="Innsendt dato")
    title: Optional[str] = Field(None, alias="Title", description="Tittel")
    description: Optional[str] = Field(
        None, alias="Description", description="Beskrivelse"
    )
    event_id: int = Field(alias="EventId", description="Hendelsesnummer")
    project_id: int = Field(alias="ProjectId", description="Prosjekt-ID")
    sub_project_id: Optional[int] = Field(
        None, alias="SubProjectId", description="Underprosjekt-ID"
    )
    submitter_name: Optional[str] = Field(
        None, alias="SubmitterName", description="Innmelders navn"
    )
    case_worker_name: Optional[str] = Field(
        None, alias="CaseWorkerName", description="Saksbehandlers navn"
    )
    lat: Optional[float] = Field(None, alias="Lat", description="Breddegrad")
    lon: Optional[float] = Field(None, alias="Lon", description="Lengdegrad")
    accuracy: Optional[int] = Field(
        None, alias="Accuracy", description="GPS-nøyaktighet (meter)"
    )
    cause: Optional[str] = Field(None, alias="Cause", description="Årsak")
    concerning: Optional[str] = Field(None, alias="Concerning", description="Gjelder")
    relates_to: Optional[str] = Field(
        None, alias="RelatesTo", description="Relaterer til"
    )
