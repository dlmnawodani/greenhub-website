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

class PaginateRequest(BaseModel):
    skip: Optional[int] = Field(
            default=0, 
            alias="skip",
            description="skip"
        )
    limit: Optional[int] = Field(
            default=10, 
            alias="limit",
            description="limit"
        )
    paginate: Optional[bool] = Field(
            default=False, 
            alias="paginate",
            description="paginate"
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
                "skip": fake.random_int(min=0, max=100),
                "limit": fake.random_int(min=0, max=100),
                "paginate": False
            }
        }

# PaginateRequest.model_rebuild()

__all__ = [
    "PaginateRequest"
]
