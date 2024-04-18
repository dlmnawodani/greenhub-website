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
from app.models.base.BaseUser import BaseUser
from app.models.base.BaseCart import BaseCart
from app.models.base.BaseOrder import BaseOrder
from app.models.base.BasePayment import BasePayment
from app.models.base.BaseReview import BaseReview

fake = Faker()

class User(BaseUser):
    pass
    # carts: Optional[List[BackLink[BaseCart]]] = Field(
    #         default=None, 
    #         alias="carts",
    #         description="carts", 
    #         original_field="user"
    #     )
    # orders: Optional[List[BackLink[BaseOrder]]] = Field(
    #         default=None, 
    #         alias="orders",
    #         description="orders", 
    #         original_field="user"
    #     )
    # payments: Optional[List[BackLink[BasePayment]]] = Field(
    #         default=None, 
    #         alias="payments",
    #         description="payments", 
    #         original_field="user"
    #     )
    # reviews: Optional[List[BackLink[BaseReview]]] = Field(
    #         default=None, 
    #         alias="reviews",
    #         description="reviews", 
    #         original_field="user"
    #     )


__all__ = [
    "User"
]

