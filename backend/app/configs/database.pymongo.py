# Import required packages and modules
# from __future__ import annotations
# import logging as logging
# import sys as sys
# import os as os
# from decouple import config
# import asyncio as asyncio
# from typing import TYPE_CHECKING
from pymongo.mongo_client import MongoClient
from app.utils.Logger import Logger
from .Setting import Setting as Setting

logging = Logger(__name__)
settings = Setting()

# MongoDB connection parameters
DB_USER=settings.DB_USER
DB_PASSWORD=settings.DB_PASSWORD
DB_HOST=settings.DB_HOST
DB_NAME=settings.DB_NAME
DB_MAX_CONN_COUNT=settings.DB_MAX_CONN_COUNT
DB_MIN_CONN_COUNT=settings.DB_MIN_CONN_COUNT
DB_UUID_REPRESENTATION=settings.DB_UUID_REPRESENTATION

# MongoDB URI
DATABASE_URI = f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/?retryWrites=true&w=majority&appName=Cluster0"  # authMechanism=DEFAULT

# Create a new client and connect to the server
client = MongoClient(DATABASE_URI)

if __name__ == "__main__":
    # Send a ping to confirm a successful connection
    try:
        # Ping the MongoDB deployment
        client.admin.command("ping")
        # If ping is successful, print confirmation message
        logging.debug("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        # If ping fails, print the error message
        logging.exception("Could not connect to MongoDB!", e)