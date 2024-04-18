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
from decimal import Decimal
from faker import Faker

fake = Faker()

class BasePayment(BaseModel):
    id: Optional[Union[PydanticObjectId, str]] = Field(
            default=None, 
            alias="id",
            description="id",
            validation_alias=AliasChoices('id', '_id')
        )
    # order_id: Optional[str] = Field(
    #         default=None, 
    #         alias="order_id",
    #         description="order_id"
    #     )
    amount: Optional[float] = Field(
            default=float(0.0), 
            alias="amount",
            description="amount"
        ) # Optional[condecimal(decimal_places=2, max_digits=10)] # Optional[float]
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
    remark: Optional[str] = Field(
            default=None, 
            alias="remark",
            description="remark"
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
                # "order_id": str(fake.uuid4()),
                "amount": float(fake.pydecimal(min_value=10, max_value=1000, right_digits=2)),
                "created_at": datetime.now(timezone.utc), # datetime.now(timezone.utc).replace(tzinfo=None) # fake.date_time_between(start_date='-1y', end_date='now')
                "updated_at": datetime.now(timezone.utc), # datetime.now(timezone.utc).replace(tzinfo=None) # fake.date_time_between(start_date='-1y', end_date='now')
                "remark": fake.text()
            }
        }

# BasePayment.model_rebuild()

__all__ = [
    "BasePayment"
]
