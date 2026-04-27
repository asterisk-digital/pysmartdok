from datetime import datetime
from enum import StrEnum
from typing import Optional

from pydantic import BaseModel, Field


class RueStatus(StrEnum):
    UNPROCESSED = "Unprocessed"
    OPEN = "Open"
    CLOSE = "Close"
    DISCARDED = "Discarded"


class AbsenceAppliesTo(StrEnum):
    NOT_RELEVANT = "NotRelevant"
    SUBCONTRACTOR = "Subcontractor"
    EMPLOYEE = "Employee"


class RueValueType(StrEnum):
    EVENT_TYPE = "EventType"
    EVENT_INVOLVED = "EventInvolved"
    CAUSE_OF_EVENT = "CauseOfEvent"
    WORK_OPERATION = "WorkOperation"
    DESCRIPTION = "Description"
    SEVERITY = "Severity"
    IMMEDIATE_MEASURES = "ImmediateMeasures"
    POSITION = "Position"
    SUBMIT_ANONYMOUSLY = "SubmitAnonymously"
    PHOTOS = "Photos"
    TITLE = "Title"


class GeoLocation(BaseModel):
    model_config = {"populate_by_name": True}

    lat: Optional[float] = Field(None, alias="Lat", description="Breddegrad")
    lon: Optional[float] = Field(None, alias="Lon", description="Lengdegrad")


class RueValue(BaseModel):
    """Egendefinert feltverdi."""

    model_config = {"populate_by_name": True}

    id: int = Field(alias="Id", description="Verdi-ID")
    name: Optional[str] = Field(None, alias="Name", description="Visningsnavn")
    key: Optional[str] = Field(None, alias="Key", description="Programmatisk nøkkel")
    type: RueValueType = Field(alias="Type", description="Verditype")
    sequence: float = Field(alias="Sequence", description="Sorteringsrekkefølge")


class RueValueGroup(BaseModel):
    """Gruppe av egendefinerte feltverdier."""

    model_config = {"populate_by_name": True}

    id: int = Field(alias="Id", description="Gruppe-ID")
    type: RueValueType = Field(alias="Type", description="Verditype")
    values: list[RueValue] = Field(alias="Values", description="Valgte verdier")


class RueReportSummary(BaseModel):
    """Sammendrag av en RUE-rapport."""

    model_config = {"populate_by_name": True}

    id: int = Field(alias="Id", description="Unik rapport-ID")
    event_id: int = Field(alias="EventId", description="Hendelsesnummer")
    title: Optional[str] = Field(None, alias="Title", description="Tittel")
    status: RueStatus = Field(alias="Status", description="Status")
    severity: str = Field(alias="Severity", description="Alvorlighetsgrad")
    submit_date: datetime = Field(alias="SubmitDate", description="Innsendt dato")
    event_time: datetime = Field(alias="EventTime", description="Hendelsestidspunkt")
    deadline_date_time: Optional[datetime] = Field(
        None, alias="DeadlineDateTime", description="Frist"
    )
    project_id: int = Field(alias="ProjectId", description="Prosjekt-ID")
    sub_project_id: Optional[int] = Field(
        None, alias="SubProjectId", description="Underprosjekt-ID"
    )
    owner_id: str = Field(alias="OwnerId", description="Saksbehandler-ID")
    submitter_id: Optional[str] = Field(
        None, alias="SubmitterId", description="Innmelder-ID"
    )


class RueReport(BaseModel):
    """Deprecated: Rapport fra GET /rue."""

    model_config = {"populate_by_name": True}

    id: int = Field(alias="Id", description="Unik rapport-ID")
    project_id: int = Field(alias="ProjectId", description="Prosjekt-ID")
    sub_project_id: Optional[int] = Field(
        None, alias="SubProjectId", description="Underprosjekt-ID"
    )
    submit_date: datetime = Field(alias="SubmitDate", description="Innsendt dato")
    submitter_name: Optional[str] = Field(
        None, alias="SubmitterName", description="Innmelders navn"
    )
    case_worker_name: Optional[str] = Field(
        None, alias="CaseWorkerName", description="Saksbehandlers navn"
    )
    status: RueStatus = Field(alias="Status", description="Status")
    title: Optional[str] = Field(None, alias="Title", description="Tittel")
    lat: Optional[float] = Field(None, alias="Lat", description="Breddegrad")
    lon: Optional[float] = Field(None, alias="Lon", description="Lengdegrad")
    accuracy: Optional[int] = Field(
        None, alias="Accuracy", description="GPS-nøyaktighet (meter)"
    )
    event_id: int = Field(alias="EventId", description="Hendelsesnummer")


class RueReportDetail(BaseModel):
    """Fullstendig RUE-rapport (Rapport om Uønskede Hendelser)."""

    model_config = {"populate_by_name": True}

    id: int = Field(alias="Id", description="Unik rapport-ID")
    event_id: int = Field(alias="EventId", description="Hendelsesnummer")
    title: Optional[str] = Field(None, alias="Title", description="Tittel")
    description: Optional[str] = Field(
        None, alias="Description", description="Beskrivelse"
    )
    status: RueStatus = Field(alias="Status", description="Status")
    severity: str = Field(alias="Severity", description="Alvorlighetsgrad")
    submit_date: datetime = Field(alias="SubmitDate", description="Innsendt dato")
    event_time: datetime = Field(alias="EventTime", description="Hendelsestidspunkt")
    deadline_date_time: Optional[datetime] = Field(
        None, alias="DeadlineDateTime", description="Frist"
    )
    project_id: int = Field(alias="ProjectId", description="Prosjekt-ID")
    sub_project_id: Optional[int] = Field(
        None, alias="SubProjectId", description="Underprosjekt-ID"
    )
    submitter_id: Optional[str] = Field(
        None, alias="SubmitterId", description="Innmelder-ID"
    )
    owner_id: str = Field(alias="OwnerId", description="Saksbehandler-ID")
    immediate_measures_description: Optional[str] = Field(
        None,
        alias="ImmediateMeasuresDescription",
        description="Strakstiltak",
    )
    permanent_measures_description: Optional[str] = Field(
        None,
        alias="PermanentMeasuresDescription",
        description="Varige tiltak",
    )
    consequence_analysis: Optional[str] = Field(
        None, alias="ConsequenceAnalysis", description="Konsekvensanalyse"
    )
    conclusion: Optional[str] = Field(
        None, alias="Conclusion", description="Konklusjon"
    )
    conclusion_visible_to_submitter: Optional[bool] = Field(
        None,
        alias="ConclusionVisibleToSubmitter",
        description="Konklusjon synlig for innmelder",
    )
    estimated_cost: Optional[float] = Field(
        None, alias="EstimatedCost", description="Estimert kostnad"
    )
    actual_cost: Optional[float] = Field(
        None, alias="ActualCost", description="Faktisk kostnad"
    )
    absence_days: Optional[int] = Field(
        None, alias="AbsenceDays", description="Fraværsdager"
    )
    absence_applies_to: Optional[AbsenceAppliesTo] = Field(
        None, alias="AbsenceAppliesTo", description="Fravær gjelder"
    )
    geo_location: Optional[GeoLocation] = Field(
        None, alias="GeoLocation", description="Posisjon"
    )
    location_accuracy: Optional[int] = Field(
        None, alias="LocationAccuracy", description="GPS-nøyaktighet (meter)"
    )
    reported_by_subcontractor: bool = Field(
        alias="ReportedBySubcontractor",
        description="Rapportert av underentreprenør",
    )
    values: list[RueValueGroup] = Field(
        alias="Values", description="Egendefinerte feltverdier"
    )
    definition_id: Optional[int] = Field(
        None, alias="DefinitionId", description="RUE-definisjon-ID"
    )


class RueEventLog(BaseModel):
    """Hendelseslogg / endringslogg."""

    model_config = {"populate_by_name": True}

    id: int = Field(alias="Id", description="Loggoppføring-ID")
    description: Optional[str] = Field(
        None, alias="Description", description="Beskrivelse av endring"
    )
    change_time: datetime = Field(alias="ChangeTime", description="Endringstidspunkt")
    user_id: Optional[str] = Field(None, alias="UserId", description="Bruker-ID")


class RueMessage(BaseModel):
    """Melding/kommentar på en RUE-rapport."""

    model_config = {"populate_by_name": True}

    id: int = Field(alias="Id", description="Melding-ID")
    message: Optional[str] = Field(None, alias="Message", description="Meldingsinnhold")
    submitter_id: str = Field(alias="SubmitterId", description="Forfatter-ID")
    timestamp: datetime = Field(alias="TimeStamp", description="Tidspunkt")


class FileInformation(BaseModel):
    """Filinformasjon for PDF-nedlasting."""

    model_config = {"populate_by_name": True}

    filename: str = Field(alias="Filename", description="Filnavn")
    download_url: str = Field(alias="DownloadUrl", description="Nedlastingslenke")
    file_size: Optional[int] = Field(None, alias="FileSize", description="Filstørrelse")
    file_date: Optional[datetime] = Field(None, alias="FileDate", description="Fildato")
