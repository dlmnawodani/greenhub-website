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
from app.schemas.Payment import Payment as PaymentSchema
from app.schemas.PaymentCreateRequest import PaymentCreateRequest as PaymentCreateRequestSchema
from app.schemas.PaymentUpdateRequest import PaymentUpdateRequest as PaymentUpdateRequestSchema
from app.schemas.PaymentReadRequest import PaymentReadRequest as PaymentReadRequestSchema
from app.schemas.PaginateResponse import PaginateResponse as PaginateResponseSchema
# import controllers
from app.controllers.PaymentController import PaymentController as PaymentController
# import dependencies
from app.dependencies.CurrentUserGetter import CurrentUserGetter as CurrentUserGetter
from app.dependencies.ClientIPGetter import ClientIPGetter as ClientIPGetter

router = APIRouter()
payment_controller = PaymentController()
settings = Setting()


@router.post(
        "/payments", 
        response_model=Optional[PaymentSchema], 
        status_code=status.HTTP_201_CREATED, 
        dependencies=[]
    )
async def create_payment(
        request_schema: PaymentCreateRequestSchema, 
        db: AsyncIOMotorDatabase = Depends(database.get_database), 
        current_user: Optional[UserSchema] = Depends(CurrentUserGetter(is_required=False)), 
        client_ip: Optional[str] = Depends(ClientIPGetter())
    ) -> Optional[PaymentSchema]:
        response = await payment_controller.create_payment(request_schema, db, current_user, client_ip)
        return response

@router.put(
        "/payments/{id}", 
        response_model=Optional[PaymentSchema], 
        status_code=status.HTTP_200_OK, 
        dependencies=[]
    )
async def update_payment(
        id: str,
        request_schema: PaymentUpdateRequestSchema, 
        db: AsyncIOMotorDatabase = Depends(database.get_database), 
        current_user: Optional[UserSchema] = Depends(CurrentUserGetter(is_required=False)), 
        client_ip: Optional[str] = Depends(ClientIPGetter())
    ) -> Optional[PaymentSchema]:
        response = await payment_controller.update_payment(id, request_schema, db, current_user, client_ip)
        return response

@router.delete(
        "/payments/{id}", 
        response_model=None, 
        status_code=status.HTTP_204_NO_CONTENT, 
        dependencies=[]
    )
async def delete_payment(
        id: str,
        db: AsyncIOMotorDatabase = Depends(database.get_database), 
        current_user: Optional[UserSchema] = Depends(CurrentUserGetter(is_required=False)), 
        client_ip: Optional[str] = Depends(ClientIPGetter())
    ) -> None:
        await payment_controller.delete_payment(id, db, current_user, client_ip)

@router.get(
        "/payments", 
        response_model=Optional[PaginateResponseSchema[List[PaymentSchema]]], 
        status_code=status.HTTP_200_OK, 
        dependencies=[]
    )
async def read_payments(
        request_schema: PaymentReadRequestSchema = Depends(PaymentReadRequestSchema),
        db: AsyncIOMotorDatabase = Depends(database.get_database), 
        current_user: Optional[UserSchema] = Depends(CurrentUserGetter(is_required=False)), 
        client_ip: Optional[str] = Depends(ClientIPGetter())
    ) -> Optional[PaginateResponseSchema[List[PaymentSchema]]]:
        response = await payment_controller.read_payments(request_schema, db, current_user, client_ip)
        return response


@router.get(
        "/payments/{id}", 
        response_model=Optional[PaymentSchema], 
        status_code=status.HTTP_200_OK, 
        dependencies=[]
    )
async def read_payment_by_id(
        id: str,
        db: AsyncIOMotorDatabase = Depends(database.get_database), 
        current_user: Optional[UserSchema] = Depends(CurrentUserGetter(is_required=False)), 
        client_ip: Optional[str] = Depends(ClientIPGetter())
    ) -> Optional[PaymentSchema]:
        response = await payment_controller.read_payment_by_id(id, db, current_user, client_ip)
        return response



__all__ = [
    "router"
]
