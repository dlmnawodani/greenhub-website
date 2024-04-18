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
import app.configs.database as database
from app.configs.Setting import Setting as Setting
from app.utils.Logger import Logger as Logger
# import schemas
from app.schemas.User import User as UserSchema
from app.schemas.Token import Token as TokenSchema
from app.schemas.TokenPayload import TokenPayload as TokenPayloadSchema
# import services
from app.services.AuthService import AuthService as AuthService

class AuthController:
    def __init__(self):
        self.settings = Setting()
        self.logger = Logger(__name__)
        self.auth_service = AuthService()

    async def login(
            self,
            form_data: OAuth2PasswordRequestForm,
            db: AsyncIOMotorDatabase
        ) -> Optional[TokenSchema]:
            try:
                temp_response = await self.auth_service.login(form_data, db)
                return temp_response
            except (HTTPException) as e:
                raise e
            except Exception as e:
                raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                        detail=f"Internal Server Error: {str(e)}"
                    )

    async def test_token(
            self,
            current_user: Optional[Union[UserSchema, None]],
        ) -> Optional[UserSchema]:
            try:
                temp_response = await self.auth_service.test_token(current_user)
                return temp_response
            except (HTTPException) as e:
                raise e
            except Exception as e:
                raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                        detail=f"Internal Server Error: {str(e)}"
                    )

    async def refresh_token(
            self,
            refresh_token: str,
            db: AsyncIOMotorDatabase
        ) -> Optional[TokenSchema]:
            try:
                temp_response = await self.auth_service.refresh_token(refresh_token, db)
                return temp_response
            except (HTTPException) as e:
                raise e
            except Exception as e:
                raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                        detail=f"Internal Server Error: {str(e)}"
                    )


__all__ = [
    "AuthController"
]