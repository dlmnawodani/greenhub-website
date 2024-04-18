# Import required packages and modules
# from __future__ import annotations
# import logging as logging
# import sys as sys
# import os as os
# from decouple import config
# import asyncio as asyncio
# from typing import TYPE_CHECKING
from .BaseErrResp import BaseErrResp

class UnprocessableError(BaseErrResp):
    def __init__(self, details: list):
        super(UnprocessableError, self).__init__(
            422,
            "Unprocessable Entity",
            details
        )