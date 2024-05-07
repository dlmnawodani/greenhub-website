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

fake = Faker()

class BaseReview(BaseModel):
    id: Optional[Union[PydanticObjectId, str]] = Field(
            default=None, 
            alias="id",
            description="id",
            validation_alias=AliasChoices('id', '_id')
        )
    # user_id: Optional[str] = Field(
    #         default=None, 
    #         alias="user_id",
    #         description="user_id"
    #     )
    # product_id: Optional[str] = Field(
    #         default=None, 
    #         alias="product_id",
    #         description="product_id"
    #     )
    rate_value: Optional[float] = Field(
            default=0, 
            alias="rate_value",
            description="rate_value"
        )
    comment: Optional[str] = Field(
            default=None, 
            alias="comment",
            description="comment"
        )
    is_toxic_comment: Optional[bool] = Field(
            default=False, 
            alias="is_toxic_comment",
            description="is_toxic_comment"
        )
    created_at: Optional[datetime] = Field(
            default=None, 
            alias="created_at",
            description="created_at"
        )
    updated_at: Optional[datetime] = Field(
            default=None, 
            alias="updated_at",
            description="updated_at"
        )
    ip_address: Optional[str] = Field(
            default=None, 
            alias="ip_address",
            description="ip_address"
        )

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
                "id": str(fake.uuid4()),
                # "user_id": str(fake.uuid4()),
                # "product_id": str(fake.uuid4()),
                "rate_value": fake.random_int(min=0, max=10),
                "comment": fake.text(),
                "is_toxic_comment": fake.boolean(),
                "created_at": datetime.now(timezone.utc), # datetime.now(timezone.utc).replace(tzinfo=None) # fake.date_time_between(start_date='-1y', end_date='now')
                "updated_at": datetime.now(timezone.utc), # datetime.now(timezone.utc).replace(tzinfo=None) # fake.date_time_between(start_date='-1y', end_date='now')
                "ip_address": fake.ipv4()
            }
        }
        extra="allow"

# BaseReview.model_rebuild()

__all__ = [
    "BaseReview"
]
