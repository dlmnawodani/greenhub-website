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
# import models
from app.models.Category import Category as CategoryModel
# import schemas
from app.schemas.User import User as UserSchema
from app.schemas.Category import Category as CategorySchema
from app.schemas.CategoryCreateRequest import CategoryCreateRequest as CategoryCreateRequestSchema
from app.schemas.CategoryUpdateRequest import CategoryUpdateRequest as CategoryUpdateRequestSchema
from app.schemas.CategoryReadRequest import CategoryReadRequest as CategoryReadRequestSchema
from app.schemas.PaginateResponse import PaginateResponse as PaginateResponseSchema

class CategoryService:
    def __init__(self):
        self.logger = Logger(__name__)


    async def create_category(
            self, 
            categor_create_request_schema: CategoryCreateRequestSchema, 
            db: AsyncIOMotorDatabase, 
            current_user: Optional[Union[UserSchema, None]], 
            client_ip: Optional[Union[str, None]]
        ) -> Optional[CategorySchema]:
            self.logger.debug("create_category called")
            async with await db.client.start_session() as session:
                try:
                    async with session.start_transaction():
                        categor_create_request_schema_dict = categor_create_request_schema.model_dump(
                            exclude_unset=True,
                            # exclude_none=True
                        )

                        created_at = datetime.now(tz=timezone.utc)
                        categor_create_request_schema_dict["created_at"] = created_at
                        category_instance = CategoryModel(
                            **categor_create_request_schema_dict
                        )

                        # category_instance = await CategoryModel.insert_one(category_instance, session=session)
                        category_instance = await category_instance.create(session=session)

                    # Commit transaction if everything succeeds
                    await session.commit_transaction()

                    return CategorySchema.model_validate(category_instance.model_dump(by_alias=True))
                except Exception as e:
                    # Rollback transaction if an error occurs
                    if not session.has_ended and session.in_transaction:
                        await session.abort_transaction()
                    self.logger.exception("Error in create_category", e)
                    raise e

    async def update_category(
            self, 
            id: str,
            category_update_request_schema: CategoryUpdateRequestSchema, 
            db: AsyncIOMotorDatabase, 
            current_user: Optional[Union[UserSchema, None]], 
            client_ip: Optional[Union[str, None]]
        ) -> Optional[CategorySchema]:
            self.logger.debug("update_category called")
            async with await db.client.start_session() as session:
                try:
                    async with session.start_transaction():
                        category_instance = await CategoryModel.find_one(CategoryModel.id == PydanticObjectId(id))
                        if not category_instance:
                            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

                        category_update_request_schema_dict = category_update_request_schema.model_dump(
                            exclude_unset=True,
                            # exclude_none=True
                        )
                        updated_at = datetime.now(tz=timezone.utc)
                        category_update_request_schema_dict["updated_at"] = updated_at

                        await category_instance.update({"$set": category_update_request_schema_dict}, session=session)
                    # Commit transaction if everything succeeds
                    await session.commit_transaction()

                    return CategorySchema.model_validate(category_instance.model_dump(by_alias=True))
                except Exception as e:
                    # Rollback transaction if an error occurs
                    if not session.has_ended and session.in_transaction:
                        await session.abort_transaction()
                    self.logger.exception("Error in update_category", e)
                    raise e

    async def delete_category(
            self, 
            id: str,
            db: AsyncIOMotorDatabase, 
            current_user: Optional[Union[UserSchema, None]], 
            client_ip: Optional[Union[str, None]]
        ) -> None:
            self.logger.debug("delete_category called")
            async with await db.client.start_session() as session:
                try:
                    async with session.start_transaction():
                        category_instance = await CategoryModel.find_one(CategoryModel.id == PydanticObjectId(id))
                        if not category_instance:
                            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
                        await category_instance.delete(
                                # link_rule=DeleteRules.DELETE_LINKS, 
                                session=session
                            )
                    # Commit transaction if everything succeeds
                    await session.commit_transaction()

                except Exception as e:
                    # Rollback transaction if an error occurs
                    if not session.has_ended and session.in_transaction:
                        await session.abort_transaction()
                    self.logger.exception("Error in delete_category", e)
                    raise e


    async def read_category_by_id(
            self, 
            id: str,
            db: AsyncIOMotorDatabase, 
            current_user: Optional[Union[UserSchema, None]], 
            client_ip: Optional[Union[str, None]]
        ) -> Optional[CategorySchema]:
            self.logger.debug("read_category_by_id called")
            try:
                category_instance = await CategoryModel.find_one(operators.Eq(CategoryModel.id, PydanticObjectId(id)), fetch_links=True)
                if not category_instance:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
                return CategorySchema.model_validate(category_instance.model_dump(by_alias=True))
            except Exception as e:
                self.logger.exception("Error in read_category_by_id", e)
                raise e

    async def read_categories(
            self, 
            category_read_request_schema: CategoryReadRequestSchema, 
            db: AsyncIOMotorDatabase, 
            current_user: Optional[Union[UserSchema, None]], 
            client_ip: Optional[Union[str, None]]
        ) -> Optional[PaginateResponseSchema[List[CategorySchema]]]:
            self.logger.debug("read_categories called")
            try:
                query = CategoryModel.find(fetch_links=True)

                category_read_request_schema_dict = category_read_request_schema.model_dump(
                            exclude_unset=True,
                            # exclude_none=True
                        )
                
                query_filters = {}

                # Filter by name if provided
                name_filter = category_read_request_schema_dict.get("name")
                if name_filter:
                    query = query.find(CategoryModel.name == name_filter)

                # Filter by ids if provided
                ids_filter = category_read_request_schema_dict.get("ids")
                if ids_filter:
                    ids_filter_map = map(lambda id: PydanticObjectId(id), ids_filter)
                    ids_filter_list = list(ids_filter_map)
                    query = query.find(operators.In(CategoryModel.id, ids_filter_list), fetch_links=True)

                total_count = await query.count()

                if "paginate" in category_read_request_schema_dict and category_read_request_schema_dict.get("paginate") == True:
                    query.skip(
                            category_read_request_schema_dict.get("skip", 0)
                        ).limit(
                            category_read_request_schema_dict.get("limit", 0)
                        )
                    
                query = query.sort(
                    [
                        (CategoryModel.id, pymongo.DESCENDING)
                    ]
                )
                
                results = await query.to_list(
                        # length=category_read_request_schema_dict.get("limit", 0)
                    )

                category_schema_list = [CategorySchema.model_validate(v.model_dump(by_alias=True)) for v in results]
                return PaginateResponseSchema[List[CategorySchema]](count=total_count, result=category_schema_list)

            except Exception as e:
                self.logger.exception("Error in read_categories", e)
                raise e


__all__ = [
    "CategoryService"
]
