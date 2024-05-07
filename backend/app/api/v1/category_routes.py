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
from fastapi import FastAPI, APIRouter, Request, Depends, Security, HTTPException, status, Query, Path, Body, Cookie, Header, Form, File, UploadFile
from fastapi.responses import JSONResponse, HTMLResponse, StreamingResponse
# import pymongo as pymongo
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pydantic import Json
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
# import controllers
from app.controllers.CategoryController import CategoryController as CategoryController
# import dependencies
from app.dependencies.CurrentUserGetter import CurrentUserGetter as CurrentUserGetter
from app.dependencies.ClientIPGetter import ClientIPGetter as ClientIPGetter

router = APIRouter()
category_controller = CategoryController()
settings = Setting()


@router.post(
        "/categories", 
        response_model=Optional[CategorySchema], 
        status_code=status.HTTP_201_CREATED, 
        dependencies=[]
    )
async def create_category(
        request_schema: CategoryCreateRequestSchema, 
        db: AsyncIOMotorDatabase = Depends(database.get_database), 
        current_user: Optional[UserSchema] = Depends(CurrentUserGetter(is_required=False)), 
        client_ip: Optional[str] = Depends(ClientIPGetter())
    ) -> Optional[CategorySchema]:
        response = await category_controller.create_category(request_schema, db, current_user, client_ip)
        return response

@router.put(
        "/categories/{id}", 
        response_model=Optional[CategorySchema], 
        status_code=status.HTTP_200_OK, 
        dependencies=[]
    )
async def update_category(
        id: Annotated[str, Path(title="id")],
        request_schema: CategoryUpdateRequestSchema, 
        db: AsyncIOMotorDatabase = Depends(database.get_database), 
        current_user: Optional[UserSchema] = Depends(CurrentUserGetter(is_required=False)), 
        client_ip: Optional[str] = Depends(ClientIPGetter())
    ) -> Optional[CategorySchema]:
        response = await category_controller.update_category(id, request_schema, db, current_user, client_ip)
        return response

@router.delete(
        "/categories/{id}", 
        response_model=None, 
        status_code=status.HTTP_204_NO_CONTENT, 
        dependencies=[]
    )
async def delete_category(
        id: Annotated[str, Path(title="id")],
        db: AsyncIOMotorDatabase = Depends(database.get_database), 
        current_user: Optional[UserSchema] = Depends(CurrentUserGetter(is_required=False)), 
        client_ip: Optional[str] = Depends(ClientIPGetter())
    ) -> None:
        await category_controller.delete_category(id, db, current_user, client_ip)

@router.get(
        "/categories", 
        response_model=Optional[PaginateResponseSchema[List[CategorySchema]]], 
        status_code=status.HTTP_200_OK, 
        dependencies=[]
    )
async def read_categories(
        request_schema: CategoryReadRequestSchema = Depends(CategoryReadRequestSchema),
        db: AsyncIOMotorDatabase = Depends(database.get_database), 
        current_user: Optional[UserSchema] = Depends(CurrentUserGetter(is_required=False)), 
        client_ip: Optional[str] = Depends(ClientIPGetter())
    ) -> Optional[PaginateResponseSchema[List[CategorySchema]]]:
        response = await category_controller.read_categories(request_schema, db, current_user, client_ip)
        return response

@router.get(
        "/categories/{id}", 
        response_model=Optional[CategorySchema], 
        status_code=status.HTTP_200_OK, 
        dependencies=[]
    )
async def read_category_by_id(
        id: Annotated[str, Path(title="id")],
        db: AsyncIOMotorDatabase = Depends(database.get_database), 
        current_user: Optional[UserSchema] = Depends(CurrentUserGetter(is_required=False)), 
        client_ip: Optional[str] = Depends(ClientIPGetter())
    ) -> Optional[CategorySchema]:
        response = await category_controller.read_category_by_id(id, db, current_user, client_ip)
        return response



__all__ = [
    "router"
]
