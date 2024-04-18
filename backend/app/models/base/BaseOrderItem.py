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
    Union, \
    List
# import pymongo as pymongo
from beanie import Document, Indexed, PydanticObjectId, Link, BackLink, before_event, after_event, Insert, Replace, Before, After
from pydantic import BaseModel, \
    dataclasses, \
    ConfigDict, \
    ValidationError, \
    validator, \
    field_validator, \
    field_serializer, \
    model_serializer, \
    Field, \
    AliasChoices, \
    condecimal, \
    GetJsonSchemaHandler
from pydantic.json import pydantic_encoder
from datetime import datetime, timezone
from uuid import UUID, uuid4
from bson import ObjectId
from decimal import Decimal
from faker import Faker

fake = Faker()

class BaseOrderItem(Document):
    # id: Optional[UUID] = Field(
    #         # default=None, 
    #         alias="id",
    #         description="id"
    #         default_factory=uuid4
    #     )
    # id: Optional[PydanticObjectId] = Field(
    #         default=None, 
    #         alias="id",
    #         description="id"
    #     )
    # order_id: Optional[PydanticObjectId] = Field(
    #         default=None, 
    #         alias="order_id",
    #         description="order_id"
    #     )
    # product_id: Optional[PydanticObjectId] = Field(
    #         default=None, 
    #         alias="product_id",
    #         description="product_id"
    #     )
    qty: Optional[int] = Field(
            default=0, 
            alias="qty",
            description="qty"
        )
    price: Optional[float] = Field(
            default=float(0.0), 
            alias="price",
            description="price"
        ) # Optional[float]
    
    '''
    # def model_dump(self, **kwargs) -> Dict[str, Any]:
    #     return super().model_dump(**kwargs)

    # def model_dump_json(self, **kwargs) -> str:
    #     return super().model_dump_json(**kwargs)
    '''

    '''
    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     for key, value in kwargs.items():
    #         setattr(self, key, value)

    # def __new__(cls, *args, **kwargs):
    #     instance = super().__new__(cls)
    #     # instance.__init__(*args, **kwargs)
    #     return instance
    '''

    # '''
    # def __repr__(self) -> str:
    #     class_name = self.__class__.__name__
    #     result = f"<{class_name} {getattr(self, 'id', '')}>"
    #     return result

    # def __str__(self) -> str:
    #     return str(getattr(self, 'id', ''))

    # def __hash__(self) -> int:
    #     return hash(getattr(self, 'id', ''))

    # def __eq__(self, other: object) -> bool:
    #     '''
    #     # if isinstance(other, self.__class__):
    #     #     for attr_name in self.__dict__:
    #     #         if getattr(self, attr_name) != getattr(other, attr_name):
    #     #             return False
    #     #     return True
    #     # return False
    #     '''
    #     if isinstance(other, self.__class__):
    #         return getattr(self, 'id', '') == getattr(other, 'id', '')
    #     return False
    # '''

    class Settings:
        name = "order_items"
        # is_root = True
        # max_nesting_depth = 1
        # max_nesting_depths_per_field = {}

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


__all__ = [
    "BaseOrderItem"
]