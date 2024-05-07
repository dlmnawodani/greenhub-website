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
from fastapi import FastAPI, APIRouter, Request, Depends, Security, HTTPException, status, Query, Path, Body, Cookie, Header, Form, File, UploadFile
from fastapi.responses import JSONResponse, HTMLResponse, StreamingResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# import pymongo as pymongo
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import app.configs.database as database
from app.configs.Setting import Setting as Setting
from app.utils.Logger import Logger as Logger
# import schemas
from app.schemas.User import User as UserSchema
from app.schemas.Token import Token as TokenSchema
from app.schemas.TokenPayload import TokenPayload as TokenPayloadSchema
# import controllers
from app.controllers.AuthController import AuthController as AuthController
# import dependencies
from app.dependencies.CurrentUserGetter import CurrentUserGetter as CurrentUserGetter
from app.dependencies.ClientIPGetter import ClientIPGetter as ClientIPGetter

router = APIRouter()
auth_controller = AuthController()

@router.post(
        "/login", 
        response_model=Optional[TokenSchema], 
        status_code=status.HTTP_200_OK, 
        dependencies=[]
    )
async def login(
        request_schema: OAuth2PasswordRequestForm = Depends(), 
        db: AsyncIOMotorDatabase = Depends(database.get_database)
    ) -> Optional[TokenSchema]:
        response = await auth_controller.login(request_schema, db)
        return response

@router.post(
        "/test-token", 
        response_model=Optional[UserSchema], 
        status_code=status.HTTP_200_OK, 
        dependencies=[]
    )
async def test_token(
        current_user: Optional[UserSchema] = Depends(CurrentUserGetter(is_required=True)), 
    ) -> Optional[UserSchema]:
        response = await auth_controller.test_token(current_user)
        return response

@router.post(
        "/refresh-token", 
        response_model=Optional[TokenSchema], 
        status_code=status.HTTP_200_OK, 
        dependencies=[]
    )
async def refresh_token(
        refresh_token: str = Body(...), 
        db: AsyncIOMotorDatabase = Depends(database.get_database), 
    ) -> Optional[TokenSchema]:
        response = await auth_controller.refresh_token(refresh_token, db)
        return response


__all__ = [
    "router"
]
