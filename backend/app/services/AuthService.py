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
from fastapi import FastAPI, APIRouter, Request, Depends, HTTPException, status, Body, Query
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

class AuthService:
    def __init__(self):
        self.settings = Setting()
        self.security = Security()
        self.logger = Logger(__name__)

    '''
    # @staticmethod
    # async def get_user_by_email(email: str) -> Optional[UserModel]:
    #     user_instance = await UserModel.find_one(UserModel.email == email)
    #     return user_instance
    '''
    
    '''
    # @staticmethod
    # async def get_user_by_id(id: str) -> Optional[UserModel]:
    #     user_instance = await UserModel.find_one(UserModel.id == PydanticObjectId(id))
    #     return user_instance
    '''

    async def authenticate_user(
            self, 
            email: str,
            password: str,
            db: AsyncIOMotorDatabase
        ) -> Optional[UserSchema]:
            self.logger.debug("authenticate_user called")
            try:
                user_instance = await UserModel.find_one(UserModel.email == email)
                if not user_instance:
                    return None

                if not self.security.verify_hashed_str(password, user_instance.password):
                    return None

                return UserSchema.model_validate(user_instance.model_dump(by_alias=True))
            except Exception as e:
                self.logger.exception("Error in read_user_by_id", e)
                raise e

    async def login(
            self,
            form_data: OAuth2PasswordRequestForm,
            db: AsyncIOMotorDatabase
        ) -> Optional[TokenSchema]:
            user_instance = await self.authenticate_user(email=form_data.username, password=form_data.password, db=db)
            if not user_instance:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Incorrect email or password"
                )

            access_token = self.security.create_access_token(user_instance.id)
            refresh_token = self.security.create_refresh_token(user_instance.id)
            
            return TokenSchema(
                access_token = access_token,
                refresh_token = refresh_token
            )

    async def test_token(
            self,
            current_user: Optional[Union[UserSchema, None]], 
        ) -> Optional[UserSchema]:
            return current_user

    
    async def refresh_token(
            self,
            refresh_token: str,
            db: AsyncIOMotorDatabase
        ) -> Optional[TokenSchema]:
            try:
                payload = self.security.decode_refresh_token(refresh_token)
                token_data = TokenPayloadSchema(**payload)
            except (JWTError, ValidationError):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid token",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            user_instance = await UserModel.find_one(UserModel.id == PydanticObjectId(token_data.sub))

            if not user_instance:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Invalid token for user",
                )

            access_token = self.security.create_access_token(user_instance.id)
            refresh_token = self.security.create_refresh_token(user_instance.id)
            
            return TokenSchema(
                access_token = access_token,
                refresh_token = refresh_token
            )


__all__ = [
    'AuthService'
]