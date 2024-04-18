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
from datetime import datetime, timezone
from uuid import UUID, uuid4
from bson import ObjectId
from decimal import Decimal
from faker import Faker
from app.models.base.BaseOrder import BaseOrder
from app.models.base.BaseUser import BaseUser
from app.models.base.BaseOrderItem import BaseOrderItem
from app.models.base.BasePayment import BasePayment

fake = Faker()

class Order(BaseOrder):
    # pass
    user: Optional[Link[BaseUser]] = Field(
            default=None, 
            alias="user",
            description="user"
        )
    # order_items: Optional[List[BackLink[BaseOrderItem]]] = Field(
    #         default=None, 
    #         alias="order_items",
    #         description="order_items", 
    #         original_field="order"
    #     )
    # payments: Optional[List[BackLink[BasePayment]]] = Field(
    #         default=None, 
    #         description="payments", 
    #         original_field="order"
    #     )


__all__ = [
    "Order"
]
