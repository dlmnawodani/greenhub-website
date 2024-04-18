# Import required packages and modules
# from __future__ import annotations
# import logging as logging
# import sys as sys
# import os as os
# from decouple import config
# import asyncio as asyncio
# from typing import TYPE_CHECKING
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
# from pydantic.json import pydantic_encoder
# from beanie import PydanticObjectId
# from datetime import datetime, timezone, timedelta, date

class MongoSchema(BaseModel):
    @classmethod
    def from_mongo(cls, data: dict):
        if not data:
            return data
        '''
        # id = data.pop("_id", None)
        # newCls = cls(**dict(data, id=id))
        '''
        newCls = cls(**dict(data))
        return newCls

    def mongo(self, **kwargs):
        exclude_unset = kwargs.pop("exclude_unset", True)
        by_alias = kwargs.pop("by_alias", True)

        parsed = self.model_dump(
          exclude_unset=exclude_unset,
          by_alias=by_alias,
          **kwargs,
        )

        if "_id" not in parsed and "id" in parsed:
            parsed["_id"] = parsed.pop("id")

        return parsed

    class Config:
        pass
        # from_attributes = True # orm_mode = True
        # populate_by_name = True
        # arbitrary_types_allowed = True # required for the _id
        # use_enum_values = True
        # json_encoders = {
        #     # CustomType: lambda v: pydantic_encoder(v) if isinstance(v, CustomType) else None,
        #     # datetime: lambda v: v.isoformat() if isinstance(v, datetime) else None,
        #     # BackLink: lambda x: None,  # Exclude BackLink fields from serialization
        # }

# MongoSchema.update_forward_refs()
# MongoSchema.model_rebuild()


__all__ = [
    "MongoSchema"
]