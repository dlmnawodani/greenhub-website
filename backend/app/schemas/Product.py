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
from app.schemas.base.BaseProduct import BaseProduct
from app.schemas.base.BaseReview import BaseReview
from app.schemas.base.BaseCategory import BaseCategory

fake = Faker()

class Product(BaseProduct):
    # pass
    reviews: Optional[List[Union[BaseReview, dict, Any]]] = Field(
            default=None, 
            alias="reviews",
            description="reviews"
        )
    category: Optional[Union[BaseCategory, dict, Any]] = Field(
            default=None, 
            alias="category",
            description="category"
        )

    class Config(BaseProduct.Config):
        # pass
        base_product_schema = BaseProduct.Config.json_schema_extra["example"]
        base_review_schema = BaseReview.Config.json_schema_extra["example"]
        base_category_schema = BaseCategory.Config.json_schema_extra["example"]
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
                **base_product_schema,
                "reviews": [
                    {
                        **base_review_schema
                    }
                ],
                "category": {
                    **base_category_schema
                }
            }
        }

# Product.model_rebuild()

__all__ = [
    "Product"
]
