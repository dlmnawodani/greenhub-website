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
    List, \
    Tuple
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

fake = Faker()

class FileInput(BaseModel):
    content: str = Field(
            default=None, 
            alias="content",
            description="content"
        )
    filename: str = Field(
            default=None, 
            alias="filename",
            description="filename"
        )
    # content_type: str = Field(
    #         default=None, 
    #         alias="content_type",
    #         description="content_type"
    #     )

    class Config:
        # pass
        populate_by_name = True
        arbitrary_types_allowed = True # required for the _id
        use_enum_values = True
        # from_attributes = True
        # json_encoders = {
        #     # CustomType: lambda v: pydantic_encoder(v) if isinstance(v, CustomType) else None,
        #     # datetime: lambda v: v.isoformat() if isinstance(v, datetime) else None,
        #     # BackLink: lambda x: None,  # Exclude BackLink fields from serialization
        # }
        json_schema_extra = {
            "example": {
                "content": "base64",
                "filename": "str",
                # "content_type": "str"
            }
        }
        extra="allow"

# FileInput.model_rebuild()

__all__ = [
    "FileInput"
]
