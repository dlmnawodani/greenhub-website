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
from app.schemas.Cart import Cart as CartSchema
from app.schemas.CartItemCreateRequest import CartItemCreateRequest as CartItemCreateRequestSchema
from app.schemas.CartItemUpdateRequest import CartItemUpdateRequest as CartItemUpdateRequestSchema
from app.schemas.CartReadRequest import CartReadRequest as CartReadRequestSchema
from app.schemas.PaginateResponse import PaginateResponse as PaginateResponseSchema
# import controllers
from app.controllers.CartController import CartController as CartController
# import dependencies
from app.dependencies.CurrentUserGetter import CurrentUserGetter as CurrentUserGetter
from app.dependencies.ClientIPGetter import ClientIPGetter as ClientIPGetter

router = APIRouter()
cart_controller = CartController()
settings = Setting()

@router.post(
        "/carts/items", 
        response_model=Optional[CartSchema], 
        status_code=status.HTTP_201_CREATED, 
        dependencies=[]
    )
async def create_review(
        request_schema: CartItemCreateRequestSchema, 
        db: AsyncIOMotorDatabase = Depends(database.get_database), 
        current_user: Optional[UserSchema] = Depends(CurrentUserGetter(is_required=False)), 
        client_ip: Optional[str] = Depends(ClientIPGetter())
    ) -> Optional[CartSchema]:
        response = await cart_controller.create_cart_item(request_schema, db, current_user, client_ip)
        return response

@router.put(
        "/carts/items/{id}", 
        response_model=Optional[CartSchema], 
        status_code=status.HTTP_200_OK, 
        dependencies=[]
    )
async def update_cart_item(
        id: str,
        request_schema: CartItemUpdateRequestSchema,
        db: AsyncIOMotorDatabase = Depends(database.get_database), 
        current_user: Optional[UserSchema] = Depends(CurrentUserGetter(is_required=False)), 
        client_ip: Optional[str] = Depends(ClientIPGetter())
    ) -> Optional[CartSchema]:
        response = await cart_controller.update_cart_item(id, request_schema, db, current_user, client_ip)
        return response

@router.delete(
        "/carts/items/{id}", 
        response_model=None, 
        status_code=status.HTTP_204_NO_CONTENT, 
        dependencies=[]
    )
async def delete_cart_item(
        id: str,
        db: AsyncIOMotorDatabase = Depends(database.get_database), 
        current_user: Optional[UserSchema] = Depends(CurrentUserGetter(is_required=False)), 
        client_ip: Optional[str] = Depends(ClientIPGetter())
    ) -> None:
        await cart_controller.delete_cart_item(id, db, current_user, client_ip)

@router.get(
        "/carts/items", 
        response_model=Optional[PaginateResponseSchema[List[CartSchema]]], 
        status_code=status.HTTP_200_OK, 
        dependencies=[]
    )
async def read_carts(
        request_schema: CartReadRequestSchema = Depends(CartReadRequestSchema),
        db: AsyncIOMotorDatabase = Depends(database.get_database), 
        current_user: Optional[UserSchema] = Depends(CurrentUserGetter(is_required=False)), 
        client_ip: Optional[str] = Depends(ClientIPGetter())
    ) -> Optional[PaginateResponseSchema[List[CartSchema]]]:
        response = await cart_controller.read_carts(request_schema, db, current_user, client_ip)
        return response


@router.get(
        "/carts/items/{id}", 
        response_model=Optional[CartSchema], 
        status_code=status.HTTP_200_OK, 
        dependencies=[]
    )
async def read_cart_item_by_id(
        id: str,
        db: AsyncIOMotorDatabase = Depends(database.get_database), 
        current_user: Optional[UserSchema] = Depends(CurrentUserGetter(is_required=False)), 
        client_ip: Optional[str] = Depends(ClientIPGetter())
    ) -> Optional[CartSchema]:
        response = await cart_controller.read_cart_item_by_id(id, db, current_user, client_ip)
        return response

@router.delete(
        "/carts/items", 
        response_model=None, 
        status_code=status.HTTP_204_NO_CONTENT, 
        dependencies=[]
    )
async def delete_cart(
        db: AsyncIOMotorDatabase = Depends(database.get_database), 
        current_user: Optional[UserSchema] = Depends(CurrentUserGetter(is_required=False)), 
        client_ip: Optional[str] = Depends(ClientIPGetter())
    ) -> None:
        await cart_controller.delete_cart(db, current_user, client_ip)


__all__ = [
    "router"
]
