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
from app.schemas.base.BaseUser import BaseUser
from app.schemas.base.BaseCart import BaseCart
from app.schemas.base.BaseOrder import BaseOrder
from app.schemas.base.BasePayment import BasePayment
from app.schemas.base.BaseReview import BaseReview

fake = Faker()

class User(BaseUser):
    # pass
    carts: Optional[List[Union[BaseCart, dict, Any]]] = Field(
            default=None, 
            alias="carts",
            description="carts"
        )
    orders: Optional[List[Union[BaseOrder, dict, Any]]] = Field(
            default=None, 
            alias="orders",
            description="orders"
        )
    payments: Optional[List[Union[BasePayment, dict, Any]]] = Field(
            default=None, 
            alias="payments",
            description="payments"
        )
    reviews: Optional[List[Union[BaseReview, dict, Any]]] = Field(
            default=None, 
            alias="reviews",
            description="reviews"
        )
    

    class Config(BaseUser.Config):
        # pass
        base_user_schema = BaseUser.Config.json_schema_extra["example"]
        base_cart_schema = BaseCart.Config.json_schema_extra["example"]
        base_order_schema = BaseOrder.Config.json_schema_extra["example"]
        base_payment_schema = BasePayment.Config.json_schema_extra["example"]
        base_review_schema = BaseReview.Config.json_schema_extra["example"]
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
                **base_user_schema,
                "carts": [
                    {
                        **base_cart_schema
                    }
                ],
                "orders": [
                    {
                        **base_order_schema
                    }
                ],
                "payments": [
                    {
                        **base_payment_schema
                    }
                ],
                "reviews": [
                    {
                        **base_review_schema
                    }
                ]
            }
        }

# User.model_rebuild()

__all__ = [
    "User"
]
