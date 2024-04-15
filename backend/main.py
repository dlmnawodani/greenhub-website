# Import required packages and modules
# from __future__ import annotations
# import logging as logging
# import sys as sys
# import os as os
# from decouple import config
# import asyncio as asyncio
# from typing import TYPE_CHECKING
import uvicorn as uvicorn

'''
# # Add directories to the Python import search path
# sys.path.append(os.path.abspath('.'))
# sys.path.insert(0, "./app")
'''

from app.main import app

if __name__ == "__main__":
    # uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)

