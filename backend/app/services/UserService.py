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
from app.utils.Security import Security as Security
from app.utils.FileHandler import FileHandler as FileHandler
# import models
from app.models.User import User as UserModel
from app.models.base.GeoObject import GeoObject as GeoObjectModel
from app.models.Review import Review as ReviewModel
from app.models.Order import Order as OrderModel
from app.models.Product import Product as ProductModel
# import schemas
from app.schemas.User import User as UserSchema
from app.schemas.Product import Product as ProductSchema
from app.schemas.UserCreateRequest import UserCreateRequest as UserCreateRequestSchema
from app.schemas.UserUpdateRequest import UserUpdateRequest as UserUpdateRequestSchema
from app.schemas.UserReadRequest import UserReadRequest as UserReadRequestSchema
from app.schemas.PaginateResponse import PaginateResponse as PaginateResponseSchema

class UserService:
    def __init__(self):
        self.settings = Setting()
        self.security = Security()
        self.file_handler = FileHandler(self.settings.STATIC_IMAGE_FILES_DIRECTORY)
        self.logger = Logger(__name__)


    async def create_user(
            self, 
            user_create_request_schema: UserCreateRequestSchema, 
            db: AsyncIOMotorDatabase, 
            current_user: Optional[Union[UserSchema, None]], 
            client_ip: Optional[Union[str, None]]
        ) -> Optional[UserSchema]:
            self.logger.debug("create_user called")
            async with await db.client.start_session() as session:
                try:
                    async with session.start_transaction():
                        user_create_request_schema_dict = user_create_request_schema.model_dump(
                            exclude_unset=True,
                            # exclude_none=True
                        )
                        created_at = datetime.now(tz=timezone.utc)
                        user_create_request_schema_dict["created_at"] = created_at
                        user_create_request_schema_dict["ip_address"] = client_ip
                        user_create_request_schema_dict["password"] = self.security.create_hashed_str(user_create_request_schema_dict["password"])
                        if "image" in user_create_request_schema_dict and user_create_request_schema_dict.get("image") is not None:
                            input_image = user_create_request_schema_dict.get("image")
                            saved_image = self.file_handler.save_file_from_base64(input_image["content"], input_image["filename"])
                            user_create_request_schema_dict["image"] = saved_image["filename"]
                        user_instance = UserModel(
                            **user_create_request_schema_dict
                        )

                        # user_instance = await UserModel.insert_one(user_instance, session=session)
                        user_instance = await user_instance.create(session=session)

                    # Commit transaction if everything succeeds
                    await session.commit_transaction()

                    return UserSchema.model_validate(user_instance.model_dump(by_alias=True))
                except Exception as e:
                    # Rollback transaction if an error occurs
                    if not session.has_ended and session.in_transaction:
                        await session.abort_transaction()
                    self.logger.exception("Error in create_user", e)
                    raise e

    async def update_user(
            self, 
            id: str,
            user_update_request_schema: UserUpdateRequestSchema, 
            db: AsyncIOMotorDatabase, 
            current_user: Optional[Union[UserSchema, None]], 
            client_ip: Optional[Union[str, None]]
        ) -> Optional[UserSchema]:
            self.logger.debug("update_user called")
            async with await db.client.start_session() as session:
                try:
                    async with session.start_transaction():
                        user_instance = await UserModel.find_one(UserModel.id == PydanticObjectId(id))
                        if not user_instance:
                            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

                        user_update_request_schema_dict = user_update_request_schema.model_dump(
                            exclude_unset=True,
                            # exclude_none=True
                        )
                        updated_at = datetime.now(tz=timezone.utc)
                        user_update_request_schema_dict["updated_at"] = updated_at
                        if "password" in user_update_request_schema_dict and user_update_request_schema_dict.get("password") is not None:
                            user_update_request_schema_dict["password"] = self.security.create_hashed_str(user_update_request_schema_dict["password"])

                        if "image" in user_update_request_schema_dict and user_update_request_schema_dict.get("image") is not None:
                            if user_instance.image is not None:
                                self.file_handler.delete_file(user_instance.image)
                            input_image = user_update_request_schema_dict.get("image")
                            saved_image = self.file_handler.save_file_from_base64(input_image["content"], input_image["filename"])
                            user_update_request_schema_dict["image"] = saved_image["filename"]

                        await user_instance.update({"$set": user_update_request_schema_dict}, session=session)
                    # Commit transaction if everything succeeds
                    await session.commit_transaction()

                    return UserSchema.model_validate(user_instance.model_dump(by_alias=True))
                except Exception as e:
                    # Rollback transaction if an error occurs
                    if not session.has_ended and session.in_transaction:
                        await session.abort_transaction()
                    self.logger.exception("Error in update_user", e)
                    raise e

    async def delete_user(
            self, 
            id: str,
            db: AsyncIOMotorDatabase, 
            current_user: Optional[Union[UserSchema, None]], 
            client_ip: Optional[Union[str, None]]
        ) -> None:
            self.logger.debug("delete_user called")
            async with await db.client.start_session() as session:
                try:
                    async with session.start_transaction():
                        user_instance = await UserModel.find_one(UserModel.id == PydanticObjectId(id))
                        if not user_instance:
                            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
                        await user_instance.delete(
                                # link_rule=DeleteRules.DELETE_LINKS, 
                                session=session
                            )
                        if user_instance.image is not None:
                                self.file_handler.delete_file(user_instance.image)
                    # Commit transaction if everything succeeds
                    await session.commit_transaction()
                    
                except Exception as e:
                    # Rollback transaction if an error occurs
                    if not session.has_ended and session.in_transaction:
                        await session.abort_transaction()
                    self.logger.exception("Error in delete_user", e)
                    raise e


    async def read_user_by_id(
            self, 
            id: str,
            db: AsyncIOMotorDatabase, 
            current_user: Optional[Union[UserSchema, None]], 
            client_ip: Optional[Union[str, None]]
        ) -> Optional[UserSchema]:
            self.logger.debug("read_user_by_id called")
            try:
                user_instance = await UserModel.find_one(operators.Eq(UserModel.id, PydanticObjectId(id)), fetch_links=True)
                if not user_instance:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

                return UserSchema.model_validate(user_instance.model_dump(by_alias=True))
            except Exception as e:
                self.logger.exception("Error in read_user_by_id", e)
                raise e

    async def read_users(
            self, 
            user_read_request_schema: UserReadRequestSchema, 
            db: AsyncIOMotorDatabase, 
            current_user: Optional[Union[UserSchema, None]], 
            client_ip: Optional[Union[str, None]]
        ) -> Optional[PaginateResponseSchema[List[UserSchema]]]:
            self.logger.debug("read_users called")
            try:
                query = UserModel.find(fetch_links=True)
                user_read_request_schema_dict = user_read_request_schema.model_dump(
                            exclude_unset=True,
                            # exclude_none=True
                        )
                
                query_filters = {}
                
                # Filter by first_name if provided
                first_name_filter = user_read_request_schema_dict.get("first_name")
                if first_name_filter:
                    query = query.find(UserModel.first_name == first_name_filter)

                # Filter by last_name if provided
                last_name_filter = user_read_request_schema_dict.get("last_name")
                if last_name_filter:
                    query = query.find(UserModel.last_name == last_name_filter)

                # Filter by email if provided
                email_filter = user_read_request_schema_dict.get("email")
                if email_filter:
                    query = query.find(UserModel.email == email_filter)

                # Filter by user_role if provided
                user_role_filter = user_read_request_schema_dict.get("user_role")
                if user_role_filter:
                    query = query.find(UserModel.user_role == user_role_filter)

                # Filter by geo if provided
                latitude = user_read_request_schema_dict.get("latitude")
                longitude = user_read_request_schema_dict.get("longitude")
                # min_distance = user_read_request_schema_dict.get("min_distance", 0)
                # max_distance = user_read_request_schema_dict.get("max_distance", 0)
                radius = user_read_request_schema_dict.get("radius", 0)
                if latitude and longitude:
                    # point = GeoObjectModel(coordinates=[longitude, latitude])
                    '''
                    # query = query.aggregate(
                    #     [
                    #         {
                    #             "$geoNear": {
                    #                 "near": point.model_dump(),
                    #                 "distanceField": "distance",
                    #                 "maxDistance": max_distance,
                    #             }
                    #         }
                    #     ]
                    # )
                    '''

                    '''
                    # query_filters["geo"] = {
                    #     "$near": {
                    #         "$geometry": point.model_dump(),
                    #         "$minDistance": min_distance,
                    #         "$maxDistance": max_distance
                    #     }
                    # }
                    '''

                    query_filters["geo"] = {
                        "$geoWithin": { 
                            "$center": [ [longitude, latitude], radius ] 
                        }
                    }

                    query = query.find(query_filters, fetch_links=True)


                total_count = await query.count()

                if "paginate" in user_read_request_schema_dict and user_read_request_schema_dict.get("paginate") == True:
                    query.skip(
                            user_read_request_schema_dict.get("skip", 0)
                        ).limit(
                            user_read_request_schema_dict.get("limit", 0)
                        )
                    
                query = query.sort(
                    [
                        (UserModel.id, pymongo.DESCENDING)
                    ]
                )

                results = await query.to_list(
                        # length=user_read_request_schema_dict.get("limit", 0)
                    )

                user_schema_list = [UserSchema.model_validate(v.model_dump(by_alias=True)) for v in results]

                return PaginateResponseSchema[List[UserSchema]](count=total_count, result=user_schema_list)

            except Exception as e:
                self.logger.exception("Error in read_users", e)
                raise e

    async def read_users_with_most_sold_product(
            self, 
            user_read_request_schema: UserReadRequestSchema, 
            db: AsyncIOMotorDatabase, 
            current_user: Optional[Union[UserSchema, None]], 
            client_ip: Optional[Union[str, None]]
        ) -> Optional[PaginateResponseSchema[List[UserSchema]]]:
            self.logger.debug("read_users_with_most_sold_product called")
            try:
                query = UserModel.find(fetch_links=True)
                user_read_request_schema_dict = user_read_request_schema.model_dump(
                            exclude_unset=True,
                            # exclude_none=True
                        )
                
                query_filters = {}
                
                # Filter by first_name if provided
                first_name_filter = user_read_request_schema_dict.get("first_name")
                if first_name_filter:
                    query = query.find(UserModel.first_name == first_name_filter)

                # Filter by last_name if provided
                last_name_filter = user_read_request_schema_dict.get("last_name")
                if last_name_filter:
                    query = query.find(UserModel.last_name == last_name_filter)

                # Filter by email if provided
                email_filter = user_read_request_schema_dict.get("email")
                if email_filter:
                    query = query.find(UserModel.email == email_filter)

                # Filter by user_role if provided
                user_role_filter = user_read_request_schema_dict.get("user_role")
                if user_role_filter:
                    query = query.find(UserModel.user_role == user_role_filter)

                # Filter by geo if provided
                latitude = user_read_request_schema_dict.get("latitude")
                longitude = user_read_request_schema_dict.get("longitude")
                # min_distance = user_read_request_schema_dict.get("min_distance", 0)
                # max_distance = user_read_request_schema_dict.get("max_distance", 0)
                radius = user_read_request_schema_dict.get("radius", 0)
                if latitude and longitude:
                    # point = GeoObjectModel(coordinates=[longitude, latitude])
                    '''
                    # query = query.aggregate(
                    #     [
                    #         {
                    #             "$geoNear": {
                    #                 "near": point.model_dump(),
                    #                 "distanceField": "distance",
                    #                 "maxDistance": max_distance,
                    #             }
                    #         }
                    #     ]
                    # )
                    '''

                    '''
                    # query_filters["geo"] = {
                    #     "$near": {
                    #         "$geometry": point.model_dump(),
                    #         "$minDistance": min_distance,
                    #         "$maxDistance": max_distance
                    #     }
                    # }
                    '''

                    query_filters["geo"] = {
                        "$geoWithin": { 
                            "$center": [ [longitude, latitude], radius ] 
                        }
                    }

                    query = query.find(query_filters, fetch_links=True)


                total_count = await query.count()

                if "paginate" in user_read_request_schema_dict and user_read_request_schema_dict.get("paginate") == True:
                    query.skip(
                            user_read_request_schema_dict.get("skip", 0)
                        ).limit(
                            user_read_request_schema_dict.get("limit", 0)
                        )
                    
                query = query.sort(
                    [
                        (UserModel.id, pymongo.DESCENDING)
                    ]
                )

                results = await query.to_list(
                        # length=user_read_request_schema_dict.get("limit", 0)
                    )

                user_schema_list = [UserSchema.model_validate(v.model_dump(by_alias=True)) for v in results]

                for user_schema in user_schema_list:
                    most_purchased_product, total_quantity = await self.get_most_purchased_product_and_quantity(
                        PydanticObjectId(user_schema.id)
                    )

                    if most_purchased_product:
                        db_most_purchased_product = await ProductModel.find_one(operators.Eq(ProductModel.id, PydanticObjectId(most_purchased_product.id)))
                        if db_most_purchased_product:
                            db_most_purchased_product_schema = ProductSchema.model_validate(db_most_purchased_product.model_dump(by_alias=True))
                            user_schema.most_purchased_product = db_most_purchased_product_schema
                            user_schema.most_purchased_product_quantity = total_quantity

                return PaginateResponseSchema[List[UserSchema]](count=total_count, result=user_schema_list)

            except Exception as e:
                self.logger.exception("Error in read_users_with_most_sold_product", e)
                raise e

    async def get_most_purchased_product_and_quantity(self, user_id: PydanticObjectId) -> tuple[Optional[Any], int]:
        # Define an aggregation pipeline to retrieve most purchased product and total quantity
        aggregation_pipeline = [
            {"$match": {"user.$id": user_id}},
            {"$lookup": {
                "from": "order_items",
                "localField": "_id",
                "foreignField": "order.$id",
                "as": "order_items"
            }},
            {"$unwind": "$order_items"},
            {"$group": {
                "_id": "$order_items.product.$id",
                "product": {"$first": "$order_items.product"},
                "total_quantity": {"$sum": "$order_items.qty"}
            }},
            {"$sort": {"total_quantity": -1}},
            {"$limit": 1}
        ]

        # Execute the aggregation pipeline
        result = await OrderModel.aggregate(aggregation_pipeline).to_list(1)

        if result:
            most_purchased_product = result[0]["product"]
            total_quantity = result[0]["total_quantity"]
            return most_purchased_product, total_quantity

        return None, 0
    
__all__ = [
    "UserService"
]
