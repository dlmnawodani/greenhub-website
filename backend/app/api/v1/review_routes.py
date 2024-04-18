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
from fastapi import FastAPI, APIRouter, Request, Depends, HTTPException, status, security, Query, Body, Form, File, UploadFile
from fastapi.responses import JSONResponse, HTMLResponse, StreamingResponse
# import pymongo as pymongo
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pydantic import Json
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
# import controllers
from app.controllers.ReviewController import ReviewController as ReviewController
# import dependencies
from app.dependencies.CurrentUserGetter import CurrentUserGetter as CurrentUserGetter
from app.dependencies.ClientIPGetter import ClientIPGetter as ClientIPGetter

router = APIRouter()
review_controller = ReviewController()
settings = Setting()


@router.post(
        "/reviews", 
        response_model=Optional[ReviewSchema], 
        status_code=status.HTTP_201_CREATED, 
        dependencies=[]
    )
async def create_review(
        request_schema: ReviewCreateRequestSchema, 
        db: AsyncIOMotorDatabase = Depends(database.get_database), 
        current_user: Optional[UserSchema] = Depends(CurrentUserGetter(is_required=False)), 
        client_ip: Optional[str] = Depends(ClientIPGetter())
    ) -> Optional[ReviewSchema]:
        response = await review_controller.create_review(request_schema, db, current_user, client_ip)
        return response

@router.put(
        "/reviews/{id}", 
        response_model=Optional[ReviewSchema], 
        status_code=status.HTTP_200_OK, 
        dependencies=[]
    )
async def update_review(
        id: str,
        request_schema: ReviewUpdateRequestSchema,
        db: AsyncIOMotorDatabase = Depends(database.get_database), 
        current_user: Optional[UserSchema] = Depends(CurrentUserGetter(is_required=False)), 
        client_ip: Optional[str] = Depends(ClientIPGetter())
    ) -> Optional[ReviewSchema]:
        response = await review_controller.update_review(id, request_schema, db, current_user, client_ip)
        return response

@router.delete(
        "/reviews/{id}", 
        response_model=None, 
        status_code=status.HTTP_204_NO_CONTENT, 
        dependencies=[]
    )
async def delete_review(
        id: str,
        db: AsyncIOMotorDatabase = Depends(database.get_database), 
        current_user: Optional[UserSchema] = Depends(CurrentUserGetter(is_required=False)), 
        client_ip: Optional[str] = Depends(ClientIPGetter())
    ) -> None:
        await review_controller.delete_review(id, db, current_user, client_ip)

@router.get(
        "/reviews", 
        response_model=Optional[PaginateResponseSchema[List[ReviewSchema]]], 
        status_code=status.HTTP_200_OK, 
        dependencies=[]
    )
async def read_reviews(
        request_schema: ReviewReadRequestSchema = Depends(ReviewReadRequestSchema),
        db: AsyncIOMotorDatabase = Depends(database.get_database), 
        current_user: Optional[UserSchema] = Depends(CurrentUserGetter(is_required=False)), 
        client_ip: Optional[str] = Depends(ClientIPGetter())
    ) -> Optional[PaginateResponseSchema[List[ReviewSchema]]]:
        response = await review_controller.read_reviews(request_schema, db, current_user, client_ip)
        return response


@router.get(
        "/reviews/{id}", 
        response_model=Optional[ReviewSchema], 
        status_code=status.HTTP_200_OK, 
        dependencies=[]
    )
async def read_review_by_id(
        id: str,
        db: AsyncIOMotorDatabase = Depends(database.get_database), 
        current_user: Optional[UserSchema] = Depends(CurrentUserGetter(is_required=False)), 
        client_ip: Optional[str] = Depends(ClientIPGetter())
    ) -> Optional[ReviewSchema]:
        response = await review_controller.read_review_by_id(id, db, current_user, client_ip)
        return response



__all__ = [
    "router"
]
