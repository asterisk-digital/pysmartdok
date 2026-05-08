from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from .common_models import GeoLocation


class ProjectMin(BaseModel):
    """Minimal prosjektrepresentasjon. Kilde: nøstet i SubProject."""

    model_config = {"populate_by_name": True}

    project_id: int = Field(alias="ProjectId", description="Prosjekt-ID")
    project_name: str = Field(alias="ProjectName", description="Prosjektnavn")
    project_number: str = Field(alias="ProjectNumber", description="Prosjektnummer")


class Project(BaseModel):
    """Prosjekt. Kilde: GET /Projects og GET /Projects/{id}."""

    model_config = {"populate_by_name": True}

    id: int = Field(alias="Id", description="Prosjekt-ID")
    project_name: str = Field(alias="ProjectName", description="Prosjektnavn")
    project_number: str = Field(alias="ProjectNumber", description="Prosjektnummer")
    departments: list[int] = Field(alias="Departments", description="Avdelings-ID-er")
    is_absence_project: Optional[bool] = Field(
        None, alias="IsAbsenceProject", description="Er fraværsprosjekt"
    )
    is_active: Optional[bool] = Field(None, alias="IsActive", description="Aktiv")
    is_order: Optional[bool] = Field(None, alias="IsOrder", description="Er ordre")
    order_type_id: Optional[int] = Field(
        None, alias="OrderTypeId", description="Ordre-type-ID"
    )
    external_reference: Optional[str] = Field(
        None, alias="ExternalReference", description="Ekstern referanse"
    )
    customer_id: Optional[int] = Field(None, alias="CustomerId", description="Kunde-ID")
    start_date: Optional[datetime] = Field(
        None, alias="StartDate", description="Startdato"
    )
    end_date: Optional[datetime] = Field(None, alias="EndDate", description="Sluttdato")
    location: str = Field(alias="Location", description="Lokasjon")
    project_owner_name: str = Field(
        alias="ProjectOwnerName", description="Prosjektansvarlig navn"
    )
    project_owner_email: str = Field(
        alias="ProjectOwnerEmail", description="Prosjektansvarlig e-post"
    )
    project_owner_mobile: str = Field(
        alias="ProjectOwnerMobile", description="Prosjektansvarlig mobil"
    )
    client_company_name: str = Field(
        alias="ClientCompanyName", description="Kundens firmanavn"
    )
    client_company_contact: str = Field(
        alias="ClientCompanyContact", description="Kundens kontaktperson"
    )
    client_company_email: str = Field(
        alias="ClientCompanyEmail", description="Kundens e-post"
    )
    client_company_mobile: str = Field(
        alias="ClientCompanyMobile", description="Kundens mobil"
    )
    description_text: str = Field(alias="DescriptionText", description="Beskrivelse")
    document_url: str = Field(alias="DocumentUrl", description="Dokument-URL")
    calculated_time_consumption: Optional[int] = Field(
        None,
        alias="CalculatedTimeConsumption",
        description="Beregnet tidsforbruk",
    )
    internal_cost_per_hour: Optional[float] = Field(
        None, alias="InternalCostPerHour", description="Intern timepris"
    )
    hourly_rate: Optional[float] = Field(
        None, alias="HourlyRate", description="Ekstern timepris"
    )
    finished: Optional[bool] = Field(None, alias="Finished", description="Ferdig")
    to_be_invoiced: Optional[bool] = Field(
        None, alias="ToBeInvoiced", description="Skal faktureres"
    )
    geo_location: Optional[GeoLocation] = Field(
        None, alias="GeoLocation", description="Posisjon"
    )
    user_ids: list[str] = Field(alias="UserIds", description="Brukere med tilgang")
    updated: Optional[datetime] = Field(
        None, alias="Updated", description="Sist oppdatert"
    )
    created: Optional[datetime] = Field(None, alias="Created", description="Opprettet")
    invoice_calculation_note: Optional[str] = Field(
        None, alias="InvoiceCalculationNote", description="Fakturareferanse"
    )
    hse_responsible_id: Optional[str] = Field(
        None, alias="HSEResponsibleId", description="HMS-ansvarlig"
    )
    qa_responsible_id: Optional[str] = Field(
        None, alias="QAResponsibleId", description="KS-ansvarlig"
    )
    time_consumption: Optional[float] = Field(
        None, alias="TimeConsumption", description="Sum registrerte timer"
    )


class SubProject(BaseModel):
    """Underprosjekt. Kilde: GET /Projects/{projectId}/SubProjects."""

    model_config = {"populate_by_name": True}

    id: Optional[int] = Field(None, alias="Id", description="Underprosjekt-ID")
    project_id: Optional[int] = Field(
        None, alias="ProjectId", description="Foreldreprosjekt-ID"
    )
    sub_project_name: str = Field(
        alias="SubProjectName", description="Underprosjektnavn"
    )
    sub_project_number: str = Field(
        alias="SubProjectNumber", description="Underprosjektnummer"
    )
    is_active: Optional[bool] = Field(None, alias="IsActive", description="Aktiv")
    start_date: Optional[datetime] = Field(
        None, alias="StartDate", description="Startdato"
    )
    end_date: Optional[datetime] = Field(None, alias="EndDate", description="Sluttdato")
    description_text: Optional[str] = Field(
        None, alias="DescriptionText", description="Beskrivelse"
    )
    client_company_name: Optional[str] = Field(
        None, alias="ClientCompanyName", description="Kundens firmanavn"
    )
    document_url: Optional[str] = Field(
        None, alias="DocumentUrl", description="Dokument-URL"
    )
    calculated_hour_use: Optional[float] = Field(
        None, alias="CalculatedHourUse", description="Beregnet timeforbruk"
    )
    location: Optional[str] = Field(None, alias="Location", description="Lokasjon")
    geo_location: Optional[GeoLocation] = Field(
        None, alias="GeoLocation", description="Posisjon"
    )
    project: ProjectMin = Field(alias="Project", description="Foreldreprosjekt")
    updated: Optional[datetime] = Field(
        None, alias="Updated", description="Sist oppdatert"
    )
    invoice_calculation_note: Optional[str] = Field(
        None, alias="InvoiceCalculationNote", description="Fakturareferanse"
    )
    hse_responsible_id: Optional[str] = Field(
        None, alias="HSEResponsibleId", description="HMS-ansvarlig"
    )
