from __future__ import annotations

import re
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

DATE_RE = re.compile(r"^(\d{4})(?:-(0[1-9]|1[0-2]))?(?:-(0[1-9]|[12]\d|3[01]))?$")


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="allow")


class Verification(StrictModel):
    status: Literal["verified", "partial", "unverified"]
    source: str | None = None
    notes: str | None = None


class Location(StrictModel):
    city: str | None = None
    state: str | None = None
    country: str


class DateRange(StrictModel):
    start: str
    end: str | None = None

    @field_validator("start", "end")
    @classmethod
    def validate_iso_date_precision(cls, value: str | None) -> str | None:
        if value is None:
            return value
        if not DATE_RE.fullmatch(value):
            raise ValueError("must use YYYY, YYYY-MM, or YYYY-MM-DD")
        return value


class ProfileData(StrictModel):
    full_name: str
    preferred_name: str | None = None
    headline: str | None = None
    positioning: str | None = None
    location: Location | None = None
    links: dict[str, str] = Field(default_factory=dict)


class Experience(StrictModel):
    id: str
    company: str
    role: str
    dates: DateRange
    current: bool
    domains: list[str] = Field(default_factory=list)
    highlights: list[str] = Field(default_factory=list)
    verification: Verification

    @model_validator(mode="after")
    def validate_current_period(self) -> "Experience":
        if self.current and self.dates.end is not None:
            raise ValueError("current experience must omit dates.end")
        if not self.current and self.dates.end is None:
            raise ValueError("completed experience must define dates.end")
        return self


class Education(StrictModel):
    id: str
    institution: str
    degree: str
    dates: DateRange
    location: Location | None = None
    grade: str | None = None
    verification: Verification


class Credential(StrictModel):
    id: str
    name: str
    issuer: str
    type: Literal["certification", "training", "course"]
    issued: str | None = None
    expires: str | None = None
    credential: dict[str, str] | None = None
    verification: Verification

    @field_validator("issued", "expires")
    @classmethod
    def validate_dates(cls, value: str | None) -> str | None:
        if value is not None and not DATE_RE.fullmatch(value):
            raise ValueError("must use YYYY, YYYY-MM, or YYYY-MM-DD")
        return value
