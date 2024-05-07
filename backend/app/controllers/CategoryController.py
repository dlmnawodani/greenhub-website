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
from app.schemas.Category import Category as CategorySchema
from app.schemas.CategoryCreateRequest import CategoryCreateRequest as CategoryCreateRequestSchema
from app.schemas.CategoryUpdateRequest import CategoryUpdateRequest as CategoryUpdateRequestSchema
from app.schemas.CategoryReadRequest import CategoryReadRequest as CategoryReadRequestSchema
from app.schemas.PaginateResponse import PaginateResponse as PaginateResponseSchema
# import services
from app.services.CategoryService import CategoryService as CategoryService

class CategoryController:
    def __init__(self):
        self.settings = Setting()
        self.logger = Logger(__name__)
        self.category_service = CategoryService()

    async def create_category(
            self, 
            category_create_request_schema: CategoryCreateRequestSchema, 
            db: AsyncIOMotorDatabase, 
            current_user: Optional[Union[UserSchema, None]], 
            client_ip: Optional[Union[str, None]]
        ) -> Optional[CategorySchema]:
        try:
            temp_response = await self.category_service.create_category(category_create_request_schema, db, current_user, client_ip)
            return temp_response
        except (HTTPException) as e:
            raise e
        except Exception as e:
            raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                    detail=f"Internal Server Error: {str(e)}"
                )

    async def update_category(
            self, 
            id: str,
            category_update_request_schema: CategoryUpdateRequestSchema, 
            db: AsyncIOMotorDatabase, 
            current_user: Optional[Union[UserSchema, None]], 
            client_ip: Optional[Union[str, None]]
        ) -> Optional[CategorySchema]:
        try:
            temp_response = await self.category_service.update_category(id, category_update_request_schema, db, current_user, client_ip)
            return temp_response
        except (HTTPException) as e:
            raise e
        except Exception as e:
            raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                    detail=f"Internal Server Error: {str(e)}"
                )

    async def delete_category(
            self, 
            id: str,
            db: AsyncIOMotorDatabase, 
            current_user: Optional[Union[UserSchema, None]], 
            client_ip: Optional[Union[str, None]]
        ) -> None:
        try:
            await self.category_service.delete_category(id, db, current_user, client_ip)
        except (HTTPException) as e:
            raise e
        except Exception as e:
            raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                    detail=f"Internal Server Error: {str(e)}"
                )

    async def read_categories(
            self, 
            category_read_request_schema: CategoryReadRequestSchema, 
            db: AsyncIOMotorDatabase, 
            current_user: Optional[Union[UserSchema, None]], 
            client_ip: Optional[Union[str, None]]
        ) -> Optional[PaginateResponseSchema[List[CategorySchema]]]:
        try:
            temp_response = await self.category_service.read_categories(category_read_request_schema, db, current_user, client_ip)
            return temp_response
        except (HTTPException) as e:
            raise e
        except Exception as e:
            raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                    detail=f"Internal Server Error: {str(e)}"
                )

    async def read_category_by_id(
            self, 
            id: str, 
            db: AsyncIOMotorDatabase, 
            current_user: Optional[Union[UserSchema, None]], 
            client_ip: Optional[Union[str, None]]
        ) -> Optional[CategorySchema]:
        try:
            temp_response = await self.category_service.read_category_by_id(id, db, current_user, client_ip)
            return temp_response
        except (HTTPException) as e:
            raise e
        except Exception as e:
            raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                    detail=f"Internal Server Error: {str(e)}"
                )

__all__ = [
    "CategoryController"
]