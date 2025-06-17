from __future__ import annotations

from datetime import datetime
from typing import Optional, Literal

from pydantic import BaseModel, Field


class SodaCloudDiagnostics(BaseModel):
    blocks: Optional[list[SodaCloudDiagnosticBlock]] = Field()
    value: Optional[int | float] = Field()
    fail: Optional[SodaCloudThresholdDiagnostic] = Field()

    # # Necessary to handle Numbers that can be int or floats
    # model_config = ConfigDict(arbitrary_types_allowed=True)


class SodaCloudThresholdDiagnostic(BaseModel):
    greaterThan: Optional[int | float] = Field()
    greaterThanOrEqual: Optional[int | float] = Field()
    lessThan: Optional[int | float] = Field()
    lessThanOrEqual: Optional[int | float] = Field()

    # # Necessary to handle Numbers that can be int or floats
    # model_config = ConfigDict(arbitrary_types_allowed=True)


class SodaCloudDiagnosticBlock(BaseModel):
    type: str


class SodaCloudNumericMetricValuesDiagnosticBlock(SodaCloudDiagnosticBlock):
    type: Literal["numericMetricValues"] = "numericMetricValues"
    thresholdMetricName: Optional[str] = Field(...)
    values: dict[str, int | float] = Field()

    # # Necessary to handle Numbers that can be int or floats
    # model_config = ConfigDict(arbitrary_types_allowed=True)


class SodaCloudSchemaDiagnosticBlock(SodaCloudDiagnosticBlock):
    type: Literal["schema"] = "schema"
    expectedColumns: list[SodaCloudSchemaColumnInfo] = Field()
    actualColumns: list[SodaCloudSchemaColumnInfo] = Field()
    expectedColumnNamesNotActual: list[str] = Field()
    actualColumnNamesNotExpected: list[str] = Field()
    columnDataTypeMismatches: list[SodaCloudSchemaDataTypeMismatch] = Field()
    areColumnsOutOfOrder: Optional[bool] = Field()


class SodaCloudSchemaDataTypeMismatch(BaseModel):
    column: str
    expectedDataType: Optional[str] = Field()
    actualDataType: Optional[str] = Field()
    expectedCharacterMaximumLength: Optional[int] = Field()
    actualCharacterMaximumLength: Optional[int] = Field()


class SodaCloudSchemaColumnInfo(BaseModel):
    name: str
    dataType: Optional[str] = Field()
    characterMaximumLength: Optional[int] = Field()


class SodaCloudFreshnessDiagnosticBlock(SodaCloudDiagnosticBlock):
    type: Literal["freshness"] = "freshness"
    maxTimestamp: Optional[datetime]
    maxTimestampUtc: Optional[datetime]
    dataTimestamp: datetime
    dataTimestampUtc: datetime
    freshness: Optional[str] = None
    freshnessInSeconds: Optional[int] = None
    unit: Optional[str] = None
