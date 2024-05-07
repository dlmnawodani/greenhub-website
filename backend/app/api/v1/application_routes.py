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
from fastapi.responses import JSONResponse, HTMLResponse, StreamingResponse, FileResponse
# import pymongo as pymongo
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import app.configs.database as database
from app.configs.Setting import Setting as Setting
from app.utils.Logger import Logger as Logger
# import schemas
from app.schemas.HealthResource import HealthResource as HealthResourceSchema
from app.schemas.base.FileInput import FileInput as FileInputSchema
# import controllers
from app.controllers.ApplicationController import ApplicationController as ApplicationController

router = APIRouter()
application_controller = ApplicationController()

@router.get(
        "/applications/check-health", 
        response_model=Optional[HealthResourceSchema], 
        status_code=status.HTTP_200_OK, 
        dependencies=[]
    )
async def check_health(
        db: AsyncIOMotorDatabase = Depends(database.get_database)
    ) -> Optional[HealthResourceSchema]:
        response = await application_controller.check_health(db)
        return response

@router.post(
        "/applications/encode-file", 
        response_model=Optional[dict], 
        status_code=status.HTTP_200_OK, 
        dependencies=[]
    )
async def encode_file(
        file: UploadFile = File(...)
    ) -> Optional[dict]:
        # pass
        response = await application_controller.encode_file(file)
        return response

@router.post(
        "/applications/decode-file", 
        response_model=Any, 
        status_code=status.HTTP_200_OK, 
        dependencies=[]
    )
async def decode_file(
        file: FileInputSchema
    ) -> Optional[Any]:
        # pass
        response = await application_controller.decode_file(file)
        return response


__all__ = [
    "router"
]

