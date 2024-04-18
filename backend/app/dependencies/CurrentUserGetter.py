# Import required packages and modules
# from __future__ import annotations
# import logging as logging
# import sys as sys
# import os as os
# import platform as platform
# import psutil as psutil
# from decouple import config
# import asyncio as asyncio 
from typing import TYPE_CHECKING, \
    Optional, \
    Any, \
    Union, \
    Type, \
    TypeVar, \
    Generic, \
    ForwardRef, \
    Annotated, \
    List
from fastapi import APIRouter, Request, Depends, HTTPException, status, Body, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# import pymongo as pymongo
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from beanie import PydanticObjectId
from datetime import datetime, timezone
from jose import jwt, JWTError
from pydantic import ValidationError
import app.configs.database as database
from app.configs.Setting import Setting as Setting
from app.utils.Logger import Logger as Logger
from app.utils.Security import Security as Security
# import models
from app.models.User import User as UserModel
# import schemas
from app.schemas.User import User as UserSchema
from app.schemas.Token import Token as TokenSchema
from app.schemas.TokenPayload import TokenPayload as TokenPayloadSchema
# import services
from app.services.UserService import UserService as UserService

logging = Logger(__name__)
settings = Setting()
security = Security()

oauth2_scheme = OAuth2PasswordBearer(
        tokenUrl=settings.JWT_TOKEN_URL, 
        auto_error=settings.JWT_TOKEN_AUTO_ERROR, 
        # scheme_name=settings.JWT_TOKEN_SCHEME_NAME
    )

class CurrentUserGetter:
    def __init__(self, is_required=False):
        # pass
        self.is_required = is_required

    async def __call__(self, token: str = Depends(oauth2_scheme), db: AsyncIOMotorDatabase = Depends(database.get_database)) -> Optional[UserSchema]:
        current_user = None
        try:
            payload = security.decode_access_token(token)

            if not payload:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            token_data = TokenPayloadSchema(**payload)
            
            if datetime.fromtimestamp(token_data.exp) < datetime.now():
                raise HTTPException(
                    status_code = status.HTTP_401_UNAUTHORIZED,
                    detail="Token expired",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            current_user = await UserModel.find_one(UserModel.id == PydanticObjectId(token_data.sub))
            current_user = UserSchema.model_validate(current_user.model_dump(by_alias=True))

            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Could not find user",
                )
        except HTTPException as e:
            if self.is_required:
                raise e
        except (JWTError, ValidationError, Exception) as e:
            if self.is_required:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        
        return current_user

__all__ = [
    'CurrentUserGetter'
]
