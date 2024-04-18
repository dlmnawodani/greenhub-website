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
    List, \
    Tuple
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

class GeoObject:
    type: str = Field(
            default="Point", 
            alias="type",
            description="type"
        )
    coordinates: Tuple[float, float] = Field(
            # default=None, 
            alias="coordinates",
            description="coordinates [If specifying latitude and longitude coordinates, list the longitude first, and then latitude.]"
        )


__all__ = [
    "GeoObject"
]
