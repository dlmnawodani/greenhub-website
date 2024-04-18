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
from .PaginateRequest import PaginateRequest

fake = Faker()

class ProductReadRequest(PaginateRequest):
    sku: Optional[str] = Field(
            default=None, 
            alias="sku",
            description="sku"
        )
    name: Optional[str] = Field(
            default=None, 
            alias="name",
            description="name"
        )

    class Config:
        # pass
        paginate_request_schema = PaginateRequest.Config.json_schema_extra["example"]
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
                **paginate_request_schema,
                "sku": str(fake.uuid4()), # fake.uuid4().hex[:12],
                "name": fake.word()
            }
        }

# ProductReadRequest.model_rebuild()

__all__ = [
    "ProductReadRequest"
]
