# Import required packages and modules
# from __future__ import annotations
# import logging as logging
# import sys as sys
# import os as os
# from decouple import config
import asyncio as asyncio
# from typing import TYPE_CHECKING
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
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

# MongoDB client and database objects
db_client: AsyncIOMotorClient = None
db: AsyncIOMotorDatabase = None

async def connect_to_database() -> AsyncIOMotorClient:
    """
    Connect to the MongoDB database.
    """
    global db_client
    try:
        # Create a new async Motor client and connect to the server
        db_client = AsyncIOMotorClient(
            DATABASE_URI,
            # username=DB_USER,
            # password=DB_PASSWORD,
            # maxPoolSize=DB_MAX_CONN_COUNT,
            # minPoolSize=DB_MIN_CONN_COUNT,
            # uuidRepresentation=DB_UUID_REPRESENTATION,
        )

        if db_client is None:
            # logging.error("Error: Motor client is None")
            # return
            raise Exception("Motor client is None")
        logging.debug("Successfully connected to MongoDB!")
        # db_client.get_io_loop = asyncio.get_event_loop
        return db_client
    # Catch any exceptions that occur during execution
    except Exception as e:
        logging.exception("Could not connect to MongoDB!", e)
        raise e

async def get_database_connection() -> AsyncIOMotorClient:
    """
    Retrieve the MongoDB client connection.
    """
    global db_client
    return db_client

async def get_database() -> AsyncIOMotorDatabase:
    """
    Retrieve the MongoDB database.
    """
    global db
    db = db_client[DB_NAME]
    return db

async def close_database_connection() -> None:
    """
    Close the MongoDB client connection.
    """
    global db_client
    try:
        if db_client is None:
            logging.debug("Connection is None, nothing to close.")
            return
        # Close the client connection
        db_client.close()
        db_client = None
        logging.debug("Mongo connection closed.")
    # Catch any exceptions that occur during execution
    except Exception as e:
        logging.exception("An error occurred while closing the connection", e)
        raise e

async def test_database_connection() -> None:
    """
    Test the MongoDB database connection.
    """
    try:
        await connect_to_database()
        db = await get_database()
        if db is None:
            logging.debug("DB is None")
            return
        # Send a ping to confirm a successful connection
        result = await db.command('ping')
        # If ping is successful, log confirmation message
        logging.debug("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        logging.exception("An error occurred while testing the connection", e)
        raise e


if __name__ == "__main__":
    asyncio.run(test_database_connection())

__all__ = [
    "connect_to_database",
    "get_database",
    "close_database_connection",
    "test_database_connection"
]
