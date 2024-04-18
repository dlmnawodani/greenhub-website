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
from app.schemas.Review import Review as ReviewSchema
from app.schemas.ReviewCreateRequest import ReviewCreateRequest as ReviewCreateRequestSchema
from app.schemas.ReviewUpdateRequest import ReviewUpdateRequest as ReviewUpdateRequestSchema
from app.schemas.ReviewReadRequest import ReviewReadRequest as ReviewReadRequestSchema
from app.schemas.PaginateResponse import PaginateResponse as PaginateResponseSchema
# import services
from app.services.ReviewService import ReviewService as ReviewService

class ReviewController:
    def __init__(self):
        self.settings = Setting()
        self.logger = Logger(__name__)
        self.review_service = ReviewService()

    async def create_review(
            self, 
            review_create_request_schema: ReviewCreateRequestSchema, 
            db: AsyncIOMotorDatabase, 
            current_user: Optional[Union[UserSchema, None]], 
            client_ip: Optional[Union[str, None]]
        ) -> Optional[ReviewSchema]:
        try:
            temp_response = await self.review_service.create_review(review_create_request_schema, db, current_user, client_ip)
            return temp_response
        except (HTTPException) as e:
            raise e
        except Exception as e:
            raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                    detail=f"Internal Server Error: {str(e)}"
                )

    async def update_review(
            self, 
            id: str,
            review_update_request_schema: ReviewUpdateRequestSchema, 
            db: AsyncIOMotorDatabase, 
            current_user: Optional[Union[UserSchema, None]], 
            client_ip: Optional[Union[str, None]]
        ) -> Optional[ReviewSchema]:
        try:
            temp_response = await self.review_service.update_review(id, review_update_request_schema, db, current_user, client_ip)
            return temp_response
        except (HTTPException) as e:
            raise e
        except Exception as e:
            raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                    detail=f"Internal Server Error: {str(e)}"
                )

    async def delete_review(
            self, 
            id: str,
            db: AsyncIOMotorDatabase, 
            current_user: Optional[Union[UserSchema, None]], 
            client_ip: Optional[Union[str, None]]
        ) -> None:
        try:
            await self.review_service.delete_review(id, db, current_user, client_ip)
        except (HTTPException) as e:
            raise e
        except Exception as e:
            raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                    detail=f"Internal Server Error: {str(e)}"
                )

    async def read_reviews(
            self, 
            review_read_request_schema: ReviewReadRequestSchema, 
            db: AsyncIOMotorDatabase, 
            current_user: Optional[Union[UserSchema, None]], 
            client_ip: Optional[Union[str, None]]
        ) -> Optional[PaginateResponseSchema[List[ReviewSchema]]]:
        try:
            temp_response = await self.review_service.read_reviews(review_read_request_schema, db, current_user, client_ip)
            return temp_response
        except (HTTPException) as e:
            raise e
        except Exception as e:
            raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                    detail=f"Internal Server Error: {str(e)}"
                )

    async def read_review_by_id(
            self, 
            id: str, 
            db: AsyncIOMotorDatabase, 
            current_user: Optional[Union[UserSchema, None]], 
            client_ip: Optional[Union[str, None]]
        ) -> Optional[ReviewSchema]:
        try:
            temp_response = await self.review_service.read_review_by_id(id, db, current_user, client_ip)
            return temp_response
        except (HTTPException) as e:
            raise e
        except Exception as e:
            raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                    detail=f"Internal Server Error: {str(e)}"
                )

__all__ = [
    "ReviewController"
]