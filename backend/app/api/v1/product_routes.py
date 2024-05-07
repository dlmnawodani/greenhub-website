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
from app.schemas.Product import Product as ProductSchema
from app.schemas.ProductCreateRequest import ProductCreateRequest as ProductCreateRequestSchema
from app.schemas.ProductUpdateRequest import ProductUpdateRequest as ProductUpdateRequestSchema
from app.schemas.ProductReadRequest import ProductReadRequest as ProductReadRequestSchema
from app.schemas.PaginateResponse import PaginateResponse as PaginateResponseSchema
# import controllers
from app.controllers.ProductController import ProductController as ProductController
# import dependencies
from app.dependencies.CurrentUserGetter import CurrentUserGetter as CurrentUserGetter
from app.dependencies.ClientIPGetter import ClientIPGetter as ClientIPGetter

router = APIRouter()
product_controller = ProductController()
settings = Setting()


@router.post(
        "/products", 
        response_model=Optional[ProductSchema], 
        status_code=status.HTTP_201_CREATED, 
        dependencies=[]
    )
async def create_product(
        request_schema: ProductCreateRequestSchema, 
        db: AsyncIOMotorDatabase = Depends(database.get_database), 
        current_user: Optional[UserSchema] = Depends(CurrentUserGetter(is_required=False)), 
        client_ip: Optional[str] = Depends(ClientIPGetter())
    ) -> Optional[ProductSchema]:
        response = await product_controller.create_product(request_schema, db, current_user, client_ip)
        return response

@router.put(
        "/products/{id}", 
        response_model=Optional[ProductSchema], 
        status_code=status.HTTP_200_OK, 
        dependencies=[]
    )
async def update_product(
        id: Annotated[str, Path(title="id")],
        request_schema: ProductUpdateRequestSchema, 
        db: AsyncIOMotorDatabase = Depends(database.get_database), 
        current_user: Optional[UserSchema] = Depends(CurrentUserGetter(is_required=False)), 
        client_ip: Optional[str] = Depends(ClientIPGetter())
    ) -> Optional[ProductSchema]:
        response = await product_controller.update_product(id, request_schema, db, current_user, client_ip)
        return response

@router.delete(
        "/products/{id}", 
        response_model=None, 
        status_code=status.HTTP_204_NO_CONTENT, 
        dependencies=[]
    )
async def delete_product(
        id: Annotated[str, Path(title="id")],
        db: AsyncIOMotorDatabase = Depends(database.get_database), 
        current_user: Optional[UserSchema] = Depends(CurrentUserGetter(is_required=False)), 
        client_ip: Optional[str] = Depends(ClientIPGetter())
    ) -> None:
        await product_controller.delete_product(id, db, current_user, client_ip)

@router.get(
        "/products", 
        response_model=Optional[PaginateResponseSchema[List[ProductSchema]]], 
        status_code=status.HTTP_200_OK, 
        dependencies=[]
    )
async def read_products(
        request_schema: ProductReadRequestSchema = Depends(ProductReadRequestSchema),
        db: AsyncIOMotorDatabase = Depends(database.get_database), 
        current_user: Optional[UserSchema] = Depends(CurrentUserGetter(is_required=False)), 
        client_ip: Optional[str] = Depends(ClientIPGetter())
    ) -> Optional[PaginateResponseSchema[List[ProductSchema]]]:
        response = await product_controller.read_products(request_schema, db, current_user, client_ip)
        return response

@router.get(
        "/products/{id}", 
        response_model=Optional[ProductSchema], 
        status_code=status.HTTP_200_OK, 
        dependencies=[]
    )
async def read_product_by_id(
        id: Annotated[str, Path(title="id")],
        db: AsyncIOMotorDatabase = Depends(database.get_database), 
        current_user: Optional[UserSchema] = Depends(CurrentUserGetter(is_required=False)), 
        client_ip: Optional[str] = Depends(ClientIPGetter())
    ) -> Optional[ProductSchema]:
        response = await product_controller.read_product_by_id(id, db, current_user, client_ip)
        return response



__all__ = [
    "router"
]
