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
from decimal import Decimal
from faker import Faker
from app.schemas.base.FileInput import FileInput

fake = Faker()

class ProductCreateRequest(BaseModel):
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
    qty_in_stock: Optional[int] = Field(
            default=0,
            alias="qty_in_stock", 
            description="qty_in_stock"
        )
    price: Optional[float] = Field(
            default=float(0.0), 
            alias="price",
            description="price"
        ) # Optional[condecimal(decimal_places=2, max_digits=10)] # Optional[float]
    image: Optional[FileInput] = Field(
            default=None, 
            alias="image",
            description="image"
        )
    remark: Optional[str] = Field(
            default=None, 
            alias="remark",
            description="remark"
        )
    category_id: Optional[str] = Field(
            default=None, 
            alias="category_id",
            description="category_id"
        )

    class Config:
        # pass
        file_input_schema = FileInput.Config.json_schema_extra["example"]
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
                "sku": str(fake.uuid4()), # fake.uuid4().hex[:12],
                "name": fake.word(),
                "qty_in_stock": fake.random_int(min=0, max=100),
                "price": float(fake.pydecimal(min_value=10, max_value=1000, right_digits=2)),
                "image": {
                    **file_input_schema
                },
                "remark": fake.text(),
                "category_id": str(fake.uuid4()),
            }
        }

# ProductCreateRequest.model_rebuild()

__all__ = [
    "ProductCreateRequest"
]

