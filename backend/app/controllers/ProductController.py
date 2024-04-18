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
from app.schemas.Product import Product as ProductSchema
from app.schemas.ProductCreateRequest import ProductCreateRequest as ProductCreateRequestSchema
from app.schemas.ProductUpdateRequest import ProductUpdateRequest as ProductUpdateRequestSchema
from app.schemas.ProductReadRequest import ProductReadRequest as ProductReadRequestSchema
from app.schemas.PaginateResponse import PaginateResponse as PaginateResponseSchema
# import services
from app.services.ProductService import ProductService as ProductService

class ProductController:
    def __init__(self):
        self.settings = Setting()
        self.logger = Logger(__name__)
        self.product_service = ProductService()

    async def create_product(
            self, 
            product_create_request_schema: ProductCreateRequestSchema, 
            db: AsyncIOMotorDatabase, 
            current_user: Optional[Union[UserSchema, None]], 
            client_ip: Optional[Union[str, None]]
        ) -> Optional[ProductSchema]:
        try:
            temp_response = await self.product_service.create_product(product_create_request_schema, db, current_user, client_ip)
            return temp_response
        except (HTTPException) as e:
            raise e
        except Exception as e:
            raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                    detail=f"Internal Server Error: {str(e)}"
                )

    async def update_product(
            self, 
            id: str,
            product_update_request_schema: ProductUpdateRequestSchema, 
            db: AsyncIOMotorDatabase, 
            current_user: Optional[Union[UserSchema, None]], 
            client_ip: Optional[Union[str, None]]
        ) -> Optional[ProductSchema]:
        try:
            temp_response = await self.product_service.update_product(id, product_update_request_schema, db, current_user, client_ip)
            return temp_response
        except (HTTPException) as e:
            raise e
        except Exception as e:
            raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                    detail=f"Internal Server Error: {str(e)}"
                )

    async def delete_product(
            self, 
            id: str,
            db: AsyncIOMotorDatabase, 
            current_user: Optional[Union[UserSchema, None]], 
            client_ip: Optional[Union[str, None]]
        ) -> None:
        try:
            await self.product_service.delete_product(id, db, current_user, client_ip)
        except (HTTPException) as e:
            raise e
        except Exception as e:
            raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                    detail=f"Internal Server Error: {str(e)}"
                )

    async def read_products(
            self, 
            product_read_request_schema: ProductReadRequestSchema, 
            db: AsyncIOMotorDatabase, 
            current_user: Optional[Union[UserSchema, None]], 
            client_ip: Optional[Union[str, None]]
        ) -> Optional[PaginateResponseSchema[List[ProductSchema]]]:
        try:
            temp_response = await self.product_service.read_products(product_read_request_schema, db, current_user, client_ip)
            return temp_response
        except (HTTPException) as e:
            raise e
        except Exception as e:
            raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                    detail=f"Internal Server Error: {str(e)}"
                )

    async def read_product_by_id(
            self, 
            id: str, 
            db: AsyncIOMotorDatabase, 
            current_user: Optional[Union[UserSchema, None]], 
            client_ip: Optional[Union[str, None]]
        ) -> Optional[ProductSchema]:
        try:
            temp_response = await self.product_service.read_product_by_id(id, db, current_user, client_ip)
            return temp_response
        except (HTTPException) as e:
            raise e
        except Exception as e:
            raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                    detail=f"Internal Server Error: {str(e)}"
                )

__all__ = [
    "ProductController"
]