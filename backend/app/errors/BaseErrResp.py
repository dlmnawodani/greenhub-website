# Import required packages and modules
# from __future__ import annotations
# import logging as logging
# import sys as sys
# import os as os
# from decouple import config
# import asyncio as asyncio
# from typing import TYPE_CHECKING
from fastapi.responses import JSONResponse

class BaseErrResp(Exception):
    def __init__(self, status: int, title: str, details: list) -> None:
        self.__status = status
        self.__title = title
        self.__detail = details

    def gen_err_resp(self) -> JSONResponse:
        return JSONResponse(
            status_code=self.__status,
            content={
                "type": "about:blank",
                'title': self.__title,
                'status': self.__status,
                'detail': self.__detail
            }
        )

