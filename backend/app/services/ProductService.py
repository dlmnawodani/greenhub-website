# Import required packages and modules
# from __future__ import annotations
# import logging as logging
# import sys as sys
import os as os
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
import pymongo as pymongo
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from beanie import PydanticObjectId, MergeStrategy
from beanie import operators as operators
from datetime import datetime, timezone
import app.configs.database as database
from app.configs.Setting import Setting as Setting
from app.utils.Logger import Logger as Logger
from app.utils.FileHandler import FileHandler as FileHandler
# import models
from app.models.Product import Product as ProductModel
# import schemas
from app.schemas.User import User as UserSchema
from app.schemas.Product import Product as ProductSchema
from app.schemas.ProductCreateRequest import ProductCreateRequest as ProductCreateRequestSchema
from app.schemas.ProductUpdateRequest import ProductUpdateRequest as ProductUpdateRequestSchema
from app.schemas.ProductReadRequest import ProductReadRequest as ProductReadRequestSchema
from app.schemas.PaginateResponse import PaginateResponse as PaginateResponseSchema

class ProductService:
    def __init__(self):
        self.settings = Setting()
        self.file_handler = FileHandler(self.settings.STATIC_IMAGE_FILES_DIRECTORY)
        self.logger = Logger(__name__)


    async def create_product(
            self, 
            product_create_request_schema: ProductCreateRequestSchema, 
            db: AsyncIOMotorDatabase, 
            current_user: Optional[Union[UserSchema, None]], 
            client_ip: Optional[Union[str, None]]
        ) -> Optional[ProductSchema]:
            self.logger.debug("create_product called")
            async with await db.client.start_session() as session:
                try:
                    async with session.start_transaction():
                        product_create_request_schema_dict = product_create_request_schema.model_dump(
                            exclude_unset=True,
                            # exclude_none=True
                        )
                        created_at = datetime.now(tz=timezone.utc)
                        product_create_request_schema_dict["created_at"] = created_at
                        product_create_request_schema_dict["ip_address"] = client_ip
                        if "image" in product_create_request_schema_dict and product_create_request_schema_dict.get("image") is not None:
                            input_image = product_create_request_schema_dict.get("image")
                            saved_image = self.file_handler.save_file_from_base64(input_image["content"], input_image["filename"])
                            product_create_request_schema_dict["image"] = saved_image["filename"]
                        product_instance = ProductModel(
                            **product_create_request_schema_dict
                        )

                        # product_instance = await ProductModel.insert_one(product_instance, session=session)
                        product_instance = await product_instance.create(session=session)

                    # Commit transaction if everything succeeds
                    await session.commit_transaction()

                    return ProductSchema.model_validate(product_instance.model_dump(by_alias=True))
                except Exception as e:
                    # Rollback transaction if an error occurs
                    if not session.has_ended and session.in_transaction:
                        await session.abort_transaction()
                    self.logger.exception("Error in create_product", e)
                    raise e

    async def update_product(
            self, 
            id: str,
            product_update_request_schema: ProductUpdateRequestSchema, 
            db: AsyncIOMotorDatabase, 
            current_user: Optional[Union[UserSchema, None]], 
            client_ip: Optional[Union[str, None]]
        ) -> Optional[ProductSchema]:
            self.logger.debug("update_product called")
            async with await db.client.start_session() as session:
                try:
                    async with session.start_transaction():
                        product_instance = await ProductModel.find_one(ProductModel.id == PydanticObjectId(id))
                        if not product_instance:
                            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

                        product_update_request_schema_dict = product_update_request_schema.model_dump(
                            exclude_unset=True,
                            # exclude_none=True
                        )
                        updated_at = datetime.now(tz=timezone.utc)
                        product_update_request_schema_dict["updated_at"] = updated_at

                        if "image" in product_update_request_schema_dict and product_update_request_schema_dict.get("image") is not None:
                            if product_instance.image is not None:
                                self.file_handler.delete_file(product_instance.image)
                            input_image = product_update_request_schema_dict.get("image")
                            saved_image = self.file_handler.save_file_from_base64(input_image["content"], input_image["filename"])
                            product_update_request_schema_dict["image"] = saved_image["filename"]

                        await product_instance.update({"$set": product_update_request_schema_dict}, session=session)
                    # Commit transaction if everything succeeds
                    await session.commit_transaction()

                    return ProductSchema.model_validate(product_instance.model_dump(by_alias=True))
                except Exception as e:
                    # Rollback transaction if an error occurs
                    if not session.has_ended and session.in_transaction:
                        await session.abort_transaction()
                    self.logger.exception("Error in update_product", e)
                    raise e

    async def delete_product(
            self, 
            id: str,
            db: AsyncIOMotorDatabase, 
            current_user: Optional[Union[UserSchema, None]], 
            client_ip: Optional[Union[str, None]]
        ) -> None:
            self.logger.debug("delete_product called")
            async with await db.client.start_session() as session:
                try:
                    async with session.start_transaction():
                        product_instance = await ProductModel.find_one(ProductModel.id == PydanticObjectId(id))
                        if not product_instance:
                            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
                        await product_instance.delete(
                                # link_rule=DeleteRules.DELETE_LINKS, 
                                session=session
                            )
                        if product_instance.image is not None:
                                self.file_handler.delete_file(product_instance.image)
                    # Commit transaction if everything succeeds
                    await session.commit_transaction()

                except Exception as e:
                    # Rollback transaction if an error occurs
                    if not session.has_ended and session.in_transaction:
                        await session.abort_transaction()
                    self.logger.exception("Error in delete_product", e)
                    raise e


    async def read_product_by_id(
            self, 
            id: str,
            db: AsyncIOMotorDatabase, 
            current_user: Optional[Union[UserSchema, None]], 
            client_ip: Optional[Union[str, None]]
        ) -> Optional[ProductSchema]:
            self.logger.debug("read_product_by_id called")
            try:
                product_instance = await ProductModel.find_one(operators.Eq(ProductModel.id, PydanticObjectId(id)), fetch_links=True)
                if not product_instance:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
                return ProductSchema.model_validate(product_instance.model_dump(by_alias=True))
            except Exception as e:
                self.logger.exception("Error in read_product_by_id", e)
                raise e

    async def read_products(
            self, 
            product_read_request_schema: ProductReadRequestSchema, 
            db: AsyncIOMotorDatabase, 
            current_user: Optional[Union[UserSchema, None]], 
            client_ip: Optional[Union[str, None]]
        ) -> Optional[PaginateResponseSchema[List[ProductSchema]]]:
            self.logger.debug("read_products called")
            try:
                query = ProductModel.find(fetch_links=True)

                product_read_request_schema_dict = product_read_request_schema.model_dump(
                            exclude_unset=True,
                            # exclude_none=True
                        )

                # Filter by SKU if provided
                sku_filter = product_read_request_schema_dict.get("sku")
                if sku_filter:
                    query = query.find(ProductModel.sku == sku_filter)

                # Filter by name if provided
                name_filter = product_read_request_schema_dict.get("name")
                if name_filter:
                    query = query.find(ProductModel.name == name_filter)

                total_count = await query.count()

                if "paginate" in product_read_request_schema_dict and product_read_request_schema_dict.get("paginate") == True:
                    query.skip(
                            product_read_request_schema_dict.get("skip", 0)
                        ).limit(
                            product_read_request_schema_dict.get("limit", 0)
                        )
                    
                query = query.sort(
                    [
                        (ProductModel.id, pymongo.DESCENDING)
                    ]
                )
                
                results = await query.to_list(
                        # length=product_read_request_schema_dict.get("limit", 0)
                    )

                product_schema_list = [ProductSchema.model_validate(v.model_dump(by_alias=True)) for v in results]
                return PaginateResponseSchema[List[ProductSchema]](count=total_count, result=product_schema_list)

            except Exception as e:
                self.logger.exception("Error in read_products", e)
                raise e


__all__ = [
    "ProductService"
]
