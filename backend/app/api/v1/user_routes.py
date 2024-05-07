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
from app.schemas.UserCreateRequest import UserCreateRequest as UserCreateRequestSchema
from app.schemas.UserUpdateRequest import UserUpdateRequest as UserUpdateRequestSchema
from app.schemas.UserReadRequest import UserReadRequest as UserReadRequestSchema
from app.schemas.PaginateResponse import PaginateResponse as PaginateResponseSchema
# import controllers
from app.controllers.UserController import UserController as UserController
# import dependencies
from app.dependencies.CurrentUserGetter import CurrentUserGetter as CurrentUserGetter
from app.dependencies.ClientIPGetter import ClientIPGetter as ClientIPGetter

router = APIRouter()
user_controller = UserController()
settings = Setting()


@router.post(
        "/users", 
        response_model=Optional[UserSchema], 
        status_code=status.HTTP_201_CREATED, 
        dependencies=[]
    )
async def create_user(
        request_schema: UserCreateRequestSchema, 
        db: AsyncIOMotorDatabase = Depends(database.get_database), 
        current_user: Optional[UserSchema] = Depends(CurrentUserGetter(is_required=False)), 
        client_ip: Optional[str] = Depends(ClientIPGetter())
    ) -> Optional[UserSchema]:
        response = await user_controller.create_user(request_schema, db, current_user, client_ip)
        return response

@router.put(
        "/users/{id}", 
        response_model=Optional[UserSchema], 
        status_code=status.HTTP_200_OK, 
        dependencies=[]
    )
async def update_user(
        id: Annotated[str, Path(title="id")],
        request_schema: UserUpdateRequestSchema, 
        db: AsyncIOMotorDatabase = Depends(database.get_database), 
        current_user: Optional[UserSchema] = Depends(CurrentUserGetter(is_required=False)), 
        client_ip: Optional[str] = Depends(ClientIPGetter())
    ) -> Optional[UserSchema]:
        response = await user_controller.update_user(id, request_schema, db, current_user, client_ip)
        return response

@router.delete(
        "/users/{id}", 
        response_model=None, 
        status_code=status.HTTP_204_NO_CONTENT, 
        dependencies=[]
    )
async def delete_user(
        id: Annotated[str, Path(title="id")],
        db: AsyncIOMotorDatabase = Depends(database.get_database), 
        current_user: Optional[UserSchema] = Depends(CurrentUserGetter(is_required=False)), 
        client_ip: Optional[str] = Depends(ClientIPGetter())
    ) -> None:
        await user_controller.delete_user(id, db, current_user, client_ip)

@router.get(
        "/users", 
        response_model=Optional[PaginateResponseSchema[List[UserSchema]]], 
        status_code=status.HTTP_200_OK, 
        dependencies=[]
    )
async def read_users(
        request_schema: UserReadRequestSchema = Depends(UserReadRequestSchema),
        db: AsyncIOMotorDatabase = Depends(database.get_database), 
        current_user: Optional[UserSchema] = Depends(CurrentUserGetter(is_required=False)), 
        client_ip: Optional[str] = Depends(ClientIPGetter())
    ) -> Optional[PaginateResponseSchema[List[UserSchema]]]:
        response = await user_controller.read_users(request_schema, db, current_user, client_ip)
        return response


@router.get(
        "/users/{id}", 
        response_model=Optional[UserSchema], 
        status_code=status.HTTP_200_OK, 
        dependencies=[]
    )
async def read_user_by_id(
        id: Annotated[str, Path(title="id")],
        db: AsyncIOMotorDatabase = Depends(database.get_database), 
        current_user: Optional[UserSchema] = Depends(CurrentUserGetter(is_required=False)), 
        client_ip: Optional[str] = Depends(ClientIPGetter())
    ) -> Optional[UserSchema]:
        response = await user_controller.read_user_by_id(id, db, current_user, client_ip)
        return response


@router.get(
        "/users-with-most-sold-product", 
        response_model=Optional[PaginateResponseSchema[List[UserSchema]]], 
        status_code=status.HTTP_200_OK, 
        dependencies=[]
    )
async def read_users_with_most_sold_product(
        request_schema: UserReadRequestSchema = Depends(UserReadRequestSchema),
        db: AsyncIOMotorDatabase = Depends(database.get_database), 
        current_user: Optional[UserSchema] = Depends(CurrentUserGetter(is_required=False)), 
        client_ip: Optional[str] = Depends(ClientIPGetter())
    ) -> Optional[PaginateResponseSchema[List[UserSchema]]]:
        response = await user_controller.read_users_with_most_sold_product(request_schema, db, current_user, client_ip)
        return response



__all__ = [
    "router"
]

     