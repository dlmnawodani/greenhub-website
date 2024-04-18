# Import required packages and modules
# from __future__ import annotations
# import logging as logging
# import sys as sys
# import os as os
# from decouple import config
import asyncio as asyncio
# from typing import TYPE_CHECKING
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import ServerSelectionTimeoutError
from app.utils.Logger import Logger as Logger
from .Setting import Setting as Setting

class MongoDB:
    def __init__(self, uri: str, database_name: str) -> None:
        self.uri = uri
        self.database_name = database_name
        self.client: AsyncIOMotorClient = None
        self.db: AsyncIOMotorDatabase = None
        self.logger = Logger(__name__)

    async def connect_to_database(self) -> None:
        """
        Connect to the MongoDB database.
        """
        try:
            # Create a new async Motor client and connect to the server
            self.client = AsyncIOMotorClient(self.uri)
            # self.db = self.client[self.database_name]
            self.logger.debug("Successfully connected to MongoDB!")
        # Catch any exceptions that occur during execution
        except (ServerSelectionTimeoutError, Exception) as e:
            self.logger.exception("Could not connect to MongoDB!", e)
            raise e
        
    async def get_database_connection(self) -> AsyncIOMotorClient:
        try:
            if self.client is None:
                await self.connect_to_database()
            return self.client
        except Exception as e:
            self.logger.exception("An error occurred while getting the connection:", e)
            raise e
        
    async def get_database(self) -> AsyncIOMotorDatabase:
        try:
            if self.client is None:
                await self.connect_to_database()
            return self.client[self.database_name]
        except Exception as e:
            self.logger.exception("An error occurred while getting the database:", e)
            raise e

    async def close_database_connection(self) -> None:
        """
        Close the MongoDB client connection.
        """
        try:
            if self.client is None:
                self.logger.debug("Connection is None, nothing to close.")
                return
            # Close the client connection
            self.client.close()
            # self.client = None
            self.logger.debug("MongoDB connection closed.")
        # Catch any exceptions that occur during execution
        except Exception as e:
            self.logger.exception("An error occurred while closing the connection", e)
            raise e

    async def test_connection(self) -> None:
        """
        Test the MongoDB database connection.
        """
        try:
            if self.client is None:
                await self.connect_to_database()
            db = self.client[self.database_name]
            if db is None:
                self.logger.debug("DB is None")
                return
            # Send a ping to confirm a successful connection
            result = await db.command('ping')
            # If ping is successful, log confirmation message
            self.logger.debug("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            self.logger.exception("An error occurred while testing the connection", e)
            raise e

if __name__ == "__main__":
    async def main():
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

        mongo: MongoDB = None

        try:
            # Initialize MongoDB connection
            mongo = MongoDB(
                uri=DATABASE_URI,
                database_name=DB_NAME
            )
            await mongo.connect_to_database()
            # Test MongoDB connection
            await mongo.test_connection()
        finally:
            # Close MongoDB connection
            await mongo.close_database_connection()

    # Call the main async function
    asyncio.run(main())


__all__ = [
    "MongoDB"
]
