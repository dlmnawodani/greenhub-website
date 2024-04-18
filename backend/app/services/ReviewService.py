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
from app.utils.CommentClassifier import CommentClassifier as CommentClassifier
# import models
from app.models.Review import Review as ReviewModel
from app.models.User import User as UserModel
from app.models.Product import Product as ProductModel
# import schemas
from app.schemas.User import User as UserSchema
from app.schemas.Review import Review as ReviewSchema
from app.schemas.ReviewCreateRequest import ReviewCreateRequest as ReviewCreateRequestSchema
from app.schemas.ReviewUpdateRequest import ReviewUpdateRequest as ReviewUpdateRequestSchema
from app.schemas.ReviewReadRequest import ReviewReadRequest as ReviewReadRequestSchema
from app.schemas.PaginateResponse import PaginateResponse as PaginateResponseSchema

class ReviewService:
    def __init__(self):
        self.settings = Setting()
        self.file_handler = FileHandler(self.settings.STATIC_IMAGE_FILES_DIRECTORY)
        self.logger = Logger(__name__)
        self.comment_classifier = CommentClassifier()
        self.comment_classifier.load()


    async def create_review(
            self, 
            review_create_request_schema: ReviewCreateRequestSchema, 
            db: AsyncIOMotorDatabase, 
            current_user: Optional[Union[UserSchema, None]], 
            client_ip: Optional[Union[str, None]]
        ) -> Optional[ReviewSchema]:
            self.logger.debug("create_review called")
            async with await db.client.start_session() as session:
                try:
                    async with session.start_transaction():
                        review_create_request_schema_dict = review_create_request_schema.model_dump(
                            exclude_unset=True,
                            # exclude_none=True
                        )
                        created_at = datetime.now(tz=timezone.utc)
                        review_create_request_schema_dict["created_at"] = created_at
                        review_create_request_schema_dict["ip_address"] = client_ip
                        
                        user_instance = await UserModel.find_one(UserModel.id == PydanticObjectId(current_user.id))
                        if not user_instance:
                            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
                        review_create_request_schema_dict["user"] = user_instance
                        
                        product_id = review_create_request_schema_dict.get("product_id")
                        product_instance = await ProductModel.find_one(ProductModel.id == PydanticObjectId(product_id))
                        if not product_instance:
                            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
                        review_create_request_schema_dict["product"] = product_instance

                        rate_value, is_toxic_comment = self.comment_classifier.predict(review_create_request_schema_dict["comment"])
                        review_create_request_schema_dict["rate_value"] = rate_value
                        review_create_request_schema_dict["is_toxic_comment"] = is_toxic_comment
                        
                        review_instance = ReviewModel(
                            **review_create_request_schema_dict
                        )

                        # review_instance = await ReviewModel.insert_one(review_instance, session=session)
                        review_instance = await review_instance.create(session=session)

                    # Commit transaction if everything succeeds
                    await session.commit_transaction()
                    return ReviewSchema.model_validate(review_instance.model_dump(by_alias=True))
                except Exception as e:
                    # Rollback transaction if an error occurs
                    if not session.has_ended and session.in_transaction:
                        await session.abort_transaction()
                    self.logger.exception("Error in create_review", e)
                    raise e

    async def update_review(
            self, 
            id: str,
            review_update_request_schema: ReviewUpdateRequestSchema, 
            db: AsyncIOMotorDatabase, 
            current_user: Optional[Union[UserSchema, None]], 
            client_ip: Optional[Union[str, None]]
        ) -> Optional[ReviewSchema]:
            self.logger.debug("update_review called")
            async with await db.client.start_session() as session:
                try:
                    async with session.start_transaction():
                        review_instance = await ReviewModel.find_one(ReviewModel.id == PydanticObjectId(id))
                        if not review_instance:
                            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")

                        review_update_request_schema_dict = review_update_request_schema.model_dump(
                            exclude_unset=True,
                            # exclude_none=True
                        )
                        updated_at = datetime.now(tz=timezone.utc)
                        review_update_request_schema_dict["updated_at"] = updated_at

                        user_instance = await UserModel.find_one(UserModel.id == PydanticObjectId(current_user.id))
                        if not user_instance:
                            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
                        review_update_request_schema_dict["user"] = user_instance
                        
                        product_id = review_update_request_schema_dict.get("product_id")
                        product_instance = await ProductModel.find_one(ProductModel.id == PydanticObjectId(product_id))
                        if not product_instance:
                            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
                        review_update_request_schema_dict["product"] = product_instance

                        rate_value, is_toxic_comment = self.comment_classifier.predict(review_update_request_schema_dict["comment"])
                        review_update_request_schema_dict["rate_value"] = rate_value
                        review_update_request_schema_dict["is_toxic_comment"] = is_toxic_comment

                        await review_instance.update({"$set": review_update_request_schema_dict}, session=session)
                    # Commit transaction if everything succeeds
                    await session.commit_transaction()

                    return ReviewSchema.model_validate(review_instance.model_dump(by_alias=True))
                except Exception as e:
                    # Rollback transaction if an error occurs
                    if not session.has_ended and session.in_transaction:
                        await session.abort_transaction()
                    self.logger.exception("Error in update_review", e)
                    raise e

    async def delete_review(
            self, 
            id: str,
            db: AsyncIOMotorDatabase, 
            current_user: Optional[Union[UserSchema, None]], 
            client_ip: Optional[Union[str, None]]
        ) -> None:
            self.logger.debug("delete_review called")
            async with await db.client.start_session() as session:
                try:
                    async with session.start_transaction():
                        review_instance = await ReviewModel.find_one(ReviewModel.id == PydanticObjectId(id))
                        if not review_instance:
                            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
                        await review_instance.delete(
                                # link_rule=DeleteRules.DELETE_LINKS, 
                                session=session
                            )
                    # Commit transaction if everything succeeds
                    await session.commit_transaction()

                except Exception as e:
                    # Rollback transaction if an error occurs
                    if not session.has_ended and session.in_transaction:
                        await session.abort_transaction()
                    self.logger.exception("Error in delete_review", e)
                    raise e


    async def read_review_by_id(
            self, 
            id: str,
            db: AsyncIOMotorDatabase, 
            current_user: Optional[Union[UserSchema, None]], 
            client_ip: Optional[Union[str, None]]
        ) -> Optional[ReviewSchema]:
            self.logger.debug("read_review_by_id called")
            try:
                review_instance = await ReviewModel.find_one(operators.Eq(ReviewModel.id, PydanticObjectId(id)), fetch_links=True)
                if not review_instance:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")

                return ReviewSchema.model_validate(review_instance.model_dump(by_alias=True))
            except Exception as e:
                self.logger.exception("Error in read_review_by_id", e)
                raise e

    async def read_reviews(
            self, 
            review_read_request_schema: ReviewReadRequestSchema, 
            db: AsyncIOMotorDatabase, 
            current_user: Optional[Union[UserSchema, None]], 
            client_ip: Optional[Union[str, None]]
        ) -> Optional[PaginateResponseSchema[List[ReviewSchema]]]:
            self.logger.debug("read_reviews called")
            try:
                query = ReviewModel.find(fetch_links=True)
                review_read_request_schema_dict = review_read_request_schema.model_dump(
                            exclude_unset=True,
                            # exclude_none=True
                        )
                
                # Filter by rate_value if provided
                rate_value_filter = review_read_request_schema_dict.get("rate_value")
                if rate_value_filter:
                    query = query.find(ReviewModel.rate_value == rate_value_filter)

                # Filter by is_toxic_comment if provided
                is_toxic_comment_filter = review_read_request_schema_dict.get("is_toxic_comment")
                if is_toxic_comment_filter:
                    query = query.find(ReviewModel.is_toxic_comment == is_toxic_comment_filter)

                # Filter by user_id if provided
                user_id_filter = review_read_request_schema_dict.get("user_id")
                if user_id_filter:
                    query = query.find(ReviewModel.user.id == user_id_filter, fetch_links=True)

                # Filter by product_id if provided
                product_id_filter = review_read_request_schema_dict.get("product_id")
                if product_id_filter:
                    query = query.find(ReviewModel.product.id == product_id_filter, fetch_links=True)
                
                total_count = await query.count()

                if "paginate" in review_read_request_schema_dict and review_read_request_schema_dict.get("paginate") == True:
                    query.skip(
                            review_read_request_schema_dict.get("skip", 0)
                        ).limit(
                            review_read_request_schema_dict.get("limit", 0)
                        )
                    
                query = query.sort(
                    [
                        (ReviewModel.id, pymongo.DESCENDING)
                    ]
                )
                
                results = await query.to_list(
                        # length=review_read_request_schema_dict.get("limit", 0)
                    )

                product_schema_list = [ReviewSchema.model_validate(v.model_dump(by_alias=True)) for v in results]
                return PaginateResponseSchema[List[ReviewSchema]](count=total_count, result=product_schema_list)

            except Exception as e:
                self.logger.exception("Error in read_reviews", e)
                raise e


__all__ = [
    "ReviewService"
]
