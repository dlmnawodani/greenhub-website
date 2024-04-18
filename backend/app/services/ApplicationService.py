# Import required packages and modules
# from __future__ import annotations
# import logging as logging
# import sys as sys
import os as os
import platform as platform
import psutil as psutil
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
from fastapi import FastAPI, APIRouter, Request, Depends, HTTPException, status, Body, Query, File, UploadFile
from fastapi.responses import JSONResponse, HTMLResponse, StreamingResponse, FileResponse
# import pymongo as pymongo
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from datetime import datetime, timezone
import base64 as base64
import app.configs.database as database
from app.configs.Setting import Setting as Setting
from app.utils.Logger import Logger as Logger
from app.utils.FileHandler import FileHandler as FileHandler
# import schemas
from app.schemas.HealthResource import HealthResource as HealthResourceSchema
from app.schemas.base.FileInput import FileInput as FileInputSchema

class ApplicationService:
    def __init__(self):
        self.settings = Setting()
        self.file_handler = FileHandler(None)
        self.logger = Logger(__name__)

    async def check_health(
            self, 
            db: AsyncIOMotorDatabase
        ) -> Optional[HealthResourceSchema]:
            self.logger.debug("check_health called")
            db_status: str = None
            system_info: dict = dict()
            try:
                system_info = {
                    "system": platform.system(),
                    "processor": platform.processor(),
                    "architecture": platform.architecture(),
                    "memory": psutil.virtual_memory()._asdict(),
                    "disk": psutil.disk_usage('/')._asdict()
                }
                await db.command("ping")
                db_status = "up"
            except Exception as e:
                db_status = "down"

            return HealthResourceSchema.model_validate({**system_info, db_status: db_status})
    
    async def encode_file(
            self, 
            file: UploadFile
        ) -> Optional[dict]:
            self.logger.debug("encode_file called")
            try:
                encoded_file = await self.file_handler.encode_file(file)
                return encoded_file
            except Exception as e:
                self.logger.exception("Error in encode_file", e)
                raise e
    
    async def decode_file(
            self, 
            file: FileInputSchema
        ) -> Optional[StreamingResponse]:
            self.logger.debug("decode_file called")
            try:
                decoded_file = await self.file_handler.decode_file(file.content, file.filename)
                content = decoded_file["content"]
                filename = decoded_file["filename"]
                media_type = decoded_file["media_type"]
                headers = {"Content-Disposition": f"attachment; filename={filename}"}
                streaming_response = StreamingResponse(content, media_type=media_type, headers=headers)
                return streaming_response
            except Exception as e:
                self.logger.exception("Error in decode_file", e)
                raise e
    


__all__ = [
    "ApplicationService"
]

