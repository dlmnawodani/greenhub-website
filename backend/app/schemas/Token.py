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
from datetime import datetime, timezone, timedelta
# from decimal import Decimal
from faker import Faker
from uuid import UUID, uuid4

fake = Faker()

class Token(BaseModel):
    # pass
    access_token: Optional[str] = Field(
            default=None, 
            alias="access_token",
            description="access_token"
        )
    refresh_token: Optional[str] = Field(
            default=None, 
            alias="refresh_token",
            description="refresh_token"
        )
    # token_type: Optional[str] = Field(
    #         default=None, 
    #         alias="token_type",
    #         description="token_type"
    #     )

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
                "access_token": str(fake.uuid4()),
                "refresh_token": str(fake.uuid4()),
                # "token_type": "bearer"
            }
        }


# Token.model_rebuild()

__all__ = [
    "Token"
]
