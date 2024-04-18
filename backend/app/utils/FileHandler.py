# Import required packages and modules
# from __future__ import annotations
# import logging as logging
# import sys as sys
import os as os
# from decouple import config
# import asyncio as asyncio
from typing import TYPE_CHECKING, \
    Optional, \
    Any, \
    Union
from datetime import datetime, timezone, timedelta
import base64 as base64
import mimetypes as mimetypes
from io import BytesIO
from fastapi import FastAPI, File, UploadFile
# from fastapi.responses import JSONResponse, HTMLResponse, StreamingResponse, FileResponse
from app.configs.Setting import Setting as Setting
from .Logger import Logger as Logger

class FileHandler:
    # pass
    def __init__(self, directory):
        self.settings = Setting()
        self.logger = Logger(__name__)
        self.directory = directory

    '''
    # @staticmethod
    # def b64_encode(file_contents):
    #     encoded_string = base64.b64encode(file_contents).decode("utf-8")
    #     return encoded_string

    # @staticmethod
    # def b64_decode(encoded_string):
    #     decoded_bytes = base64.b64decode(encoded_string)
    #     return decoded_bytes
    '''

    def encode_file_to_base64(self, file_contents) -> str:
        encoded_string = base64.b64encode(file_contents).decode("utf-8")
        return encoded_string

    def decode_base64_to_file(self, encoded_string) -> BytesIO:
        decoded_bytes = base64.b64decode(encoded_string)
        return BytesIO(decoded_bytes)
    
    def get_mime_type(self, filename: str) -> str:
        # mime_type, mime_encoding = mimetypes.guess_type(filename)
        mime_type, _ = mimetypes.guess_type(filename)
        return mime_type

    async def encode_file(self, file: File) -> dict:
        try:
            file_contents = await file.read()
            encoded_string = self.encode_file_to_base64(file_contents)
            # mime_type, mime_encoding = mimetypes.guess_type(file.filename)
            filename = file.filename
            mimetype = file.content_type
            return dict(
                encoded_string = encoded_string,
                filename = filename,
                mimetype = mimetype
            )
        except Exception as e:
            raise e
        
  
    async def decode_file(self, encoded_string: str, filename: str) -> dict:
        try:
            decoded_file = self.decode_base64_to_file(encoded_string)
            mime_type, mime_encoding = mimetypes.guess_type(filename)
            # headers = {"Content-Disposition": f"attachment; filename={filename}"}
            # streaming_response = StreamingResponse(decoded_file, media_type=mime_type, headers=headers)
            return dict(
                content = decoded_file,
                filename = filename,
                media_type = mime_type
            )
        except Exception as e:
            raise e
        
    def save_file_from_base64(self, encoded_string: str, filename: str) -> dict:
        try:
            file_path = os.path.join(self.directory, filename)
            decoded_file = self.decode_base64_to_file(encoded_string)
            with open(file_path, "wb") as file:
                # file.write(decoded_file.getbuffer().tobytes())
                file.write(decoded_file.getvalue())
            mime_type, mime_encoding = mimetypes.guess_type(filename)
            # FileResponse(file_path, filename=filename)
            return dict(
                filename = file_path,
                media_type = mime_type
            )
        except Exception as e:
            raise e
        
    def delete_file(self, filename: str) -> None:
        try:
            image_path = os.path.relpath(filename, self.directory)
            file_path = os.path.join(self.directory, image_path)
            if os.path.exists(file_path):
                os.remove(file_path)
            else:
                self.logger.debug(f"File {file_path} does not exist")
        except Exception as e:
            raise e

__all__ = [
    "FileHandler"
]

