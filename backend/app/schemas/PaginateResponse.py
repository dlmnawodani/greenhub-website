# Import required packages and modules
# from __future__ import annotations
# import logging as logging
# import sys as sys
# import os as os
# from decouple import config
# import asyncio as asyncio 
from typing import TYPE_CHECKING, \
    Optional, \
    Any, \
    TypeVar, \
    Generic, \
    ForwardRef, \
    Annotated, \
    Union, \
    List
from pydantic import BaseModel, \
    dataclasses, \
    ConfigDict, \
    ValidationError, \
    ValidationInfo, \
    validator, \
    field_validator, \
    field_serializer, \
    model_serializer, \
    Field, \
    AliasChoices, \
    condecimal, \
    GetJsonSchemaHandler
from pydantic.json import pydantic_encoder
from beanie import PydanticObjectId, BackLink
# from datetime import datetime, timezone, timedelta
# from decimal import Decimal
from faker import Faker

fake = Faker()

# Define generic type variables with defaults
ResultType = TypeVar('ResultType', List[Any], Any)

class PaginateResponse(BaseModel, Generic[ResultType]):
    count: Optional[int] = Field(
            default=None, 
            alias="count",
            description="count"
        )
    result: Optional[ResultType] = Field(
            default=None, 
            alias="result",
            description="result"
        )
    metadata: Optional[Any] = Field(
            default=None, 
            alias="metadata",
            description="metadata"
        )

    class Config:
        # pass
        populate_by_name = True
        arbitrary_types_allowed = True # required for the _id
        use_enum_values = True
        # json_encoders = {
        #     # CustomType: lambda v: pydantic_encoder(v) if isinstance(v, CustomType) else None,
        #     # datetime: lambda v: v.isoformat() if isinstance(v, datetime) else None,
        #     # BackLink: lambda x: None,  # Exclude BackLink fields from serialization
        # }
        json_schema_extra = {
            "example": {
                "count": None,
                "result": None,
                "metadata": None
            }
        }

# PaginateResponse.model_rebuild()

__all__ = [
    "PaginateResponse"
]
