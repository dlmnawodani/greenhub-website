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
from app.schemas.Order import Order as OrderSchema
from app.schemas.OrderItem import OrderItem as OrderItemSchema
from app.schemas.OrderCreateRequest import OrderCreateRequest as OrderCreateRequestSchema
from app.schemas.OrderUpdateRequest import OrderUpdateRequest as OrderUpdateRequestSchema
from app.schemas.OrderReadRequest import OrderReadRequest as OrderReadRequestSchema
from app.schemas.OrderStatusUpdateRequest import OrderStatusUpdateRequest as OrderStatusUpdateRequestSchema
from app.schemas.PaginateResponse import PaginateResponse as PaginateResponseSchema
# import controllers
from app.controllers.OrderController import OrderController as OrderController
# import dependencies
from app.dependencies.CurrentUserGetter import CurrentUserGetter as CurrentUserGetter
from app.dependencies.ClientIPGetter import ClientIPGetter as ClientIPGetter

router = APIRouter()
order_controller = OrderController()
settings = Setting()

@router.post(
        "/orders", 
        response_model=Optional[OrderSchema], 
        status_code=status.HTTP_201_CREATED, 
        dependencies=[]
    )
async def create_order(
        request_schema: OrderCreateRequestSchema, 
        db: AsyncIOMotorDatabase = Depends(database.get_database), 
        current_user: Optional[UserSchema] = Depends(CurrentUserGetter(is_required=False)), 
        client_ip: Optional[str] = Depends(ClientIPGetter())
    ) -> Optional[OrderSchema]:
        response = await order_controller.create_order(request_schema, db, current_user, client_ip)
        return response

@router.put(
        "/orders/status/{id}", 
        response_model=Optional[OrderSchema], 
        status_code=status.HTTP_200_OK, 
        dependencies=[]
    )
async def update_order_status(
        id: Annotated[str, Path(title="id")],
        request_schema: OrderStatusUpdateRequestSchema,
        db: AsyncIOMotorDatabase = Depends(database.get_database), 
        current_user: Optional[UserSchema] = Depends(CurrentUserGetter(is_required=False)), 
        client_ip: Optional[str] = Depends(ClientIPGetter())
    ) -> Optional[OrderSchema]:
        response = await order_controller.update_order_status(id, request_schema, db, current_user, client_ip)
        return response

@router.delete(
        "/orders/items/{id}", 
        response_model=None, 
        status_code=status.HTTP_204_NO_CONTENT, 
        dependencies=[]
    )
async def delete_order(
        id: Annotated[str, Path(title="id")],
        db: AsyncIOMotorDatabase = Depends(database.get_database), 
        current_user: Optional[UserSchema] = Depends(CurrentUserGetter(is_required=False)), 
        client_ip: Optional[str] = Depends(ClientIPGetter())
    ) -> None:
        await order_controller.delete_order(id, db, current_user, client_ip)

@router.get(
        "/orders", 
        response_model=Optional[PaginateResponseSchema[List[OrderSchema]]], 
        status_code=status.HTTP_200_OK, 
        dependencies=[]
    )
async def read_orders(
        request_schema: OrderReadRequestSchema = Depends(OrderReadRequestSchema),
        db: AsyncIOMotorDatabase = Depends(database.get_database), 
        current_user: Optional[UserSchema] = Depends(CurrentUserGetter(is_required=False)), 
        client_ip: Optional[str] = Depends(ClientIPGetter())
    ) -> Optional[PaginateResponseSchema[List[OrderSchema]]]:
        response = await order_controller.read_orders(request_schema, db, current_user, client_ip)
        return response

@router.get(
        "/orders/{id}", 
        response_model=Optional[OrderSchema], 
        status_code=status.HTTP_200_OK, 
        dependencies=[]
    )
async def read_order_by_id(
        id: Annotated[str, Path(title="id")],
        db: AsyncIOMotorDatabase = Depends(database.get_database), 
        current_user: Optional[UserSchema] = Depends(CurrentUserGetter(is_required=False)), 
        client_ip: Optional[str] = Depends(ClientIPGetter())
    ) -> Optional[OrderSchema]:
        response = await order_controller.read_order_by_id(id, db, current_user, client_ip)
        return response



__all__ = [
    "router"
]
