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
# import pymongo as pymongo
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import app.configs.database as database
from app.configs.Setting import Setting as Setting
from app.utils.Logger import Logger as Logger
# import schemas
from app.schemas.User import User as UserSchema
from app.schemas.UserCreateRequest import UserCreateRequest as UserCreateRequestSchema
from app.schemas.UserUpdateRequest import UserUpdateRequest as UserUpdateRequestSchema
from app.schemas.UserReadRequest import UserReadRequest as UserReadRequestSchema
from app.schemas.PaginateResponse import PaginateResponse as PaginateResponseSchema
# import services
from app.services.UserService import UserService as UserService

class UserController:
    def __init__(self):
        self.settings = Setting()
        self.logger = Logger(__name__)
        self.user_service = UserService()

    async def create_user(
            self, 
            user_create_request_schema: UserCreateRequestSchema, 
            db: AsyncIOMotorDatabase, 
            current_user: Optional[Union[UserSchema, None]], 
            client_ip: Optional[Union[str, None]]
        ) -> Optional[UserSchema]:
        try:
            temp_response = await self.user_service.create_user(user_create_request_schema, db, current_user, client_ip)
            return temp_response
        except (HTTPException) as e:
            raise e
        except Exception as e:
            raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                    detail=f"Internal Server Error: {str(e)}"
                )

    async def update_user(
            self, 
            id: str,
            user_update_request_schema: UserUpdateRequestSchema, 
            db: AsyncIOMotorDatabase, 
            current_user: Optional[Union[UserSchema, None]], 
            client_ip: Optional[Union[str, None]]
        ) -> Optional[UserSchema]:
        try:
            temp_response = await self.user_service.update_user(id, user_update_request_schema, db, current_user, client_ip)
            return temp_response
        except (HTTPException) as e:
            raise e
        except Exception as e:
            raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                    detail=f"Internal Server Error: {str(e)}"
                )

    async def delete_user(
            self, 
            id: str,
            db: AsyncIOMotorDatabase, 
            current_user: Optional[Union[UserSchema, None]], 
            client_ip: Optional[Union[str, None]]
        ) -> None:
        try:
            await self.user_service.delete_user(id, db, current_user, client_ip)
        except (HTTPException) as e:
            raise e
        except Exception as e:
            raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                    detail=f"Internal Server Error: {str(e)}"
                )

    async def read_users(
            self, 
            user_read_request_schema: UserReadRequestSchema, 
            db: AsyncIOMotorDatabase, 
            current_user: Optional[Union[UserSchema, None]], 
            client_ip: Optional[Union[str, None]]
        ) -> Optional[PaginateResponseSchema[List[UserSchema]]]:
        try:
            temp_response = await self.user_service.read_users(user_read_request_schema, db, current_user, client_ip)
            return temp_response
        except (HTTPException) as e:
            raise e
        except Exception as e:
            raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                    detail=f"Internal Server Error: {str(e)}"
                )

    async def read_user_by_id(
            self, 
            id: str, 
            db: AsyncIOMotorDatabase, 
            current_user: Optional[Union[UserSchema, None]], 
            client_ip: Optional[Union[str, None]]
        ) -> Optional[UserSchema]:
        try:
            temp_response = await self.user_service.read_user_by_id(id, db, current_user, client_ip)
            return temp_response
        except (HTTPException) as e:
            raise e
        except Exception as e:
            raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                    detail=f"Internal Server Error: {str(e)}"
                )

__all__ = [
    "UserController"
]