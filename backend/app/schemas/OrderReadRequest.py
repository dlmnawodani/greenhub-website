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
    GetJsonSchemaHandler, \
    EmailStr
from pydantic.json import pydantic_encoder
from beanie import PydanticObjectId, BackLink
from fastapi import FastAPI, Query
from datetime import datetime, timezone, timedelta
# from decimal import Decimal
from faker import Faker
from app.enums.OrderStatus import OrderStatus as OrderStatus
from .PaginateRequest import PaginateRequest

fake = Faker()

class OrderReadRequest(PaginateRequest):
    order_status: Optional[OrderStatus] = Field(
            default=None, 
            alias="order_status",
            description="order_status",
            # validate_default=True
        )
    user_id: Optional[str] = Field(
            default=None, 
            alias="user_id",
            description="user_id"
        )
    date_from: Optional[datetime] = Field(
            default=None, 
            alias="date_from",
            description="date_from"
        )
    date_to: Optional[datetime] = Field(
            default=None, 
            alias="date_to",
            description="date_to"
        )
    # ids: Optional[List[str]] = Field(
    #         Query(
    #             # default=None,
    #             alias="ids",
    #             description="ids",
    #             default_factory=list
    #         ),
    #     )
    ids: List[str] = Field(
            Query(
                # default=None,
                alias="ids",
                description="ids",
                default_factory=list
            )
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
                "order_status": fake.random_element(elements=[status.value for status in OrderStatus]),
                "date_from": datetime.now(timezone.utc), # datetime.now(timezone.utc).replace(tzinfo=None) # fake.date_time_between(start_date='-1y', end_date='now')
                "date_to": datetime.now(timezone.utc), # datetime.now(timezone.utc).replace(tzinfo=None) # fake.date_time_between(start_date='-1y', end_date='now')
            }
        }

# OrderReadRequest.model_rebuild()

__all__ = [
    "OrderReadRequest"
]
