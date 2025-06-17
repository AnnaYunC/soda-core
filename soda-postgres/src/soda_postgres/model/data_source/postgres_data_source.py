import abc
from typing import Literal, Optional

from pydantic import Field, field_validator
from soda_core.model.data_source.data_source import DataSourceBase
from soda_postgres.model.data_source.postgres_connection_properties import (
    PostgresConnectionPassword,
    PostgresConnectionPasswordFile,
    PostgresConnectionProperties,
)


class PostgresDataSource(DataSourceBase, abc.ABC):
    type: Literal["postgres"] = Field("postgres")
    connection_properties: PostgresConnectionProperties = Field(
        ..., alias="connection", description="Data source connection details"
    )
    dwh_schema: Optional[str] = Field(
        description="Data source connection details",
        default=None,
    )

    @field_validator("connection_properties", mode="before")
    def infer_connection_type(cls, value):
        if "password" in value:
            return PostgresConnectionPassword(**value)
        elif "password_file" in value:
            return PostgresConnectionPasswordFile(**value)
        raise ValueError("Unknown connection structure")
