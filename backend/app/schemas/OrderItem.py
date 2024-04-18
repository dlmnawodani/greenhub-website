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
from app.schemas.base.BaseOrderItem import BaseOrderItem
from app.schemas.base.BaseOrder import BaseOrder
from app.schemas.base.BaseProduct import BaseProduct

fake = Faker()

class OrderItem(BaseOrderItem):
    # pass
    order: Optional[Union[BaseOrder, dict, Any]] = Field(
            default=None, 
            alias="order",
            description="order"
        )
    product: Optional[Union[BaseProduct, dict, Any]] = Field(
            default=None, 
            alias="product",
            description="product"
        )
    

    class Config(BaseOrderItem.Config):
        # pass
        base_order_item_schema = BaseOrderItem.Config.json_schema_extra["example"]
        base_order_schema = BaseOrder.Config.json_schema_extra["example"]
        base_product_schema = BaseProduct.Config.json_schema_extra["example"]
        populate_by_name = True
        arbitrary_types_allowed = True # required for the _id
        use_enum_values = True
        json_encoders = {
            # CustomType: lambda v: pydantic_encoder(v) if isinstance(v, CustomType) else None,
            # datetime: lambda v: v.isoformat() if isinstance(v, datetime) else None,
            BackLink: lambda x: None,  # Exclude BackLink fields from serialization
        }
        json_schema_extra = {
            "example": {
                **base_order_item_schema,
                "order": {
                    **base_order_schema
                },
                "product": {
                    **base_product_schema
                }
            }
        }

# OrderItem.model_rebuild()

__all__ = [
    "OrderItem"
]
