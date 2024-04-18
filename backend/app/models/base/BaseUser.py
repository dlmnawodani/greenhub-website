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
    Dict
import pymongo as pymongo
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
    GetJsonSchemaHandler, \
    EmailStr
from pydantic.json import pydantic_encoder
from datetime import datetime, timezone
from uuid import UUID, uuid4
from bson import ObjectId
from decimal import Decimal
from faker import Faker
from app.enums.UserRole import UserRole as UserRole
from .GeoObject import GeoObject as GeoObject

fake = Faker()

class BaseUser(Document):
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
        ) # Indexed(str, unique=True)
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
            # default=None, 
            alias="created_at",
            description="created_at", 
            default_factory=datetime.now
        )
    updated_at: Optional[datetime] = Field(
            # default=None, 
            alias="updated_at",
            description="updated_at", 
            default_factory=datetime.now
        )
    user_role: Optional[UserRole] = Field(
            default=None, 
            alias="user_role",
            description="user_role"
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
    
    '''
    # def model_dump(self, **kwargs) -> Dict[str, Any]:
    #     return super().model_dump(**kwargs)

    # def model_dump_json(self, **kwargs) -> str:
    #     return super().model_dump_json(**kwargs)
    '''

    @property
    def jwt_subject(self) -> dict[str, Any]:
        """JWT subject fields."""
        return dict(_id = self._id)
    
    @before_event(Insert)
    async def before_insert(self):
       # # Generate id if not provided
        # if not self.id:
        #     self.id = str(uuid.uuid4())

        # Generate created_at if not provided
        if not self.created_at:
            self.created_at = datetime.now(timezone.utc)

    @before_event(Replace)
    async def before_ubdate(self):
        # Generate updated_at if not provided
        if not self.updated_at:
            self.updated_at = datetime.now(timezone.utc)

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
        name = "users"
        # is_root = True
        # max_nesting_depth = 1
        # max_nesting_depths_per_field = {}
        indexes = [
            [("geo", pymongo.GEOSPHERE)],  # GEO index
        ]

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
    "BaseUser"
]
