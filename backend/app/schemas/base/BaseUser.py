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
from datetime import datetime, timezone, timedelta
# from decimal import Decimal
from faker import Faker
from app.enums.UserRole import UserRole as UserRole
from .GeoObject import GeoObject as GeoObject

fake = Faker()

class BaseUser(BaseModel):
    id: Optional[Union[PydanticObjectId, str]] = Field(
            default=None, 
            alias="id",
            description="id",
            validation_alias=AliasChoices('id', '_id')
        )
    first_name: Optional[str] = Field(
            default=None, 
            alias="first_name",
            description="first_name"
        )
    last_name: Optional[str] = Field(
            default=None, 
            alias="last_name",
            description="last_name"
        )
    email: Optional[str] = Field(
            default=None, 
            alias="email",
            description="email"
        )
    password: Optional[str] = Field(
            default=None, 
            alias="password",
            description="password"
        )
    phone_number: Optional[str] = Field(
            default=None, 
            alias="phone_number",
            description="phone_number"
        )
    image: Optional[str] = Field(
            default=None, 
            alias="image",
            description="image"
        )
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
    user_role: Optional[UserRole] = Field(
            default=None, 
            alias="user_role",
            description="user_role",
            # validate_default=True
        )
    # latitude: Optional[float] = Field(
    #         default=None, 
    #         alias="latitude",
    #         description="latitude"
    #     ) # coordinate that specifies the north–south position of a point on the surface of the Earth or another celestial body. Latitude is given as an angle that ranges from −90° at the south pole to 90° at the north pole, with 0° at the Equator
    # longitude: Optional[float] = Field(
    #         default=None, 
    #         alias="longitude",
    #         description="longitude"
    #     ) # geographic coordinate that specifies the east–west position of a point on the surface of the Earth, or another celestial body. It is an angular measurement, usually expressed in degrees and denoted by the Greek letter lambda
    geo: Optional[Union[GeoObject, dict]] = Field(
            default=None, 
            alias="geo",
            description="geo"
        )
    ip_address: Optional[str] = Field(
            default=None, 
            alias="ip_address",
            description="ip_address"
        )
    
    # @field_validator("reviews", mode="before")
    # @classmethod
    # def convert_int_serial(cls, v):
    #     if isinstance(v, int):
    #         v = str(v).zfill(5)
    #     return v

    class Config:
        # pass
        geo_object_schema = GeoObject.Config.json_schema_extra["example"]
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
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "email": fake.email(),
                "password": fake.password(),
                "phone_number": fake.phone_number(),
                "image": fake.image_url(),
                "created_at": datetime.now(timezone.utc), # datetime.now(timezone.utc).replace(tzinfo=None) # fake.date_time_between(start_date='-1y', end_date='now')
                "updated_at": datetime.now(timezone.utc), # datetime.now(timezone.utc).replace(tzinfo=None) # fake.date_time_between(start_date='-1y', end_date='now')
                "user_role": fake.random_element(elements=[role.value for role in UserRole]),
                # "latitude": fake.latitude(),
                # "longitude": fake.longitude(),
                "ip_address": fake.ipv4(),
                "geo": {
                    **geo_object_schema
                }
            }
        }

# BaseUser.model_rebuild()

__all__ = [
    "BaseUser"
]
