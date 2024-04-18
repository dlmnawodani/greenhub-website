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
from fastapi import FastAPI, APIRouter, Request, Depends, HTTPException, status, security, Query, Body, Form, File, UploadFile
from fastapi.responses import JSONResponse, HTMLResponse, StreamingResponse, FileResponse
# import pymongo as pymongo
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import app.configs.database as database
from app.configs.Setting import Setting as Setting
from app.utils.Logger import Logger as Logger
# import schemas
from app.schemas.HealthResource import HealthResource as HealthResourceSchema
from app.schemas.base.FileInput import FileInput as FileInputSchema
# import services
from app.services.ApplicationService import ApplicationService as ApplicationService

class ApplicationController:
    def __init__(self):
        self.settings = Setting()
        self.logger = Logger(__name__)
        self.application_service = ApplicationService()

    async def check_health(
            self, 
            db: AsyncIOMotorDatabase
        ) -> Optional[HealthResourceSchema]:
        try:
            temp_response = await self.application_service.check_health(db)
            return temp_response
        except (HTTPException) as e:
            raise e
        except Exception as e:
            raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                    detail=f"Internal Server Error: {str(e)}"
                )
        

    async def encode_file(
            self, 
            file: UploadFile
        ) -> Optional[dict]:
        try:
            temp_response = await self.application_service.encode_file(file)
            return temp_response
        except (HTTPException) as e:
            raise e
        except Exception as e:
            raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                    detail=f"Internal Server Error: {str(e)}"
                )
        

    async def decode_file(
            self, 
            file: FileInputSchema
        ) -> Optional[StreamingResponse]:
        try:
            temp_response = await self.application_service.decode_file(file)
            return temp_response
        except (HTTPException) as e:
            raise e
        except Exception as e:
            raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                    detail=f"Internal Server Error: {str(e)}"
                )

__all__ = [
    "ApplicationController"
]