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
from fastapi import APIRouter, Request, Depends, HTTPException, status, Body, Query
# import pymongo as pymongo
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import app.configs.database as database
from app.configs.Setting import Setting as Setting
from app.utils.Logger import Logger as Logger
# import schemas
from app.schemas.User import User as UserSchema
from app.schemas.Payment import Payment as PaymentSchema
from app.schemas.PaymentCreateRequest import PaymentCreateRequest as PaymentCreateRequestSchema
from app.schemas.PaymentUpdateRequest import PaymentUpdateRequest as PaymentUpdateRequestSchema
from app.schemas.PaymentReadRequest import PaymentReadRequest as PaymentReadRequestSchema
from app.schemas.PaginateResponse import PaginateResponse as PaginateResponseSchema
# import services
from app.services.PaymentService import PaymentService as PaymentService

class PaymentController:
    def __init__(self):
        self.settings = Setting()
        self.logger = Logger(__name__)
        self.payment_service = PaymentService()

    async def create_payment(
            self, 
            payment_create_request_schema: PaymentCreateRequestSchema, 
            db: AsyncIOMotorDatabase, 
            current_user: Optional[Union[UserSchema, None]], 
            client_ip: Optional[Union[str, None]]
        ) -> Optional[PaymentSchema]:
        try:
            temp_response = await self.payment_service.create_payment(payment_create_request_schema, db, current_user, client_ip)
            return temp_response
        except (HTTPException) as e:
            raise e
        except Exception as e:
            raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                    detail=f"Internal Server Error: {str(e)}"
                )

    async def update_payment(
            self, 
            id: str,
            payment_update_request_schema: PaymentUpdateRequestSchema, 
            db: AsyncIOMotorDatabase, 
            current_user: Optional[Union[UserSchema, None]], 
            client_ip: Optional[Union[str, None]]
        ) -> Optional[PaymentSchema]:
        try:
            temp_response = await self.payment_service.update_payment(id, payment_update_request_schema, db, current_user, client_ip)
            return temp_response
        except (HTTPException) as e:
            raise e
        except Exception as e:
            raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                    detail=f"Internal Server Error: {str(e)}"
                )

    async def delete_payment(
            self, 
            id: str,
            db: AsyncIOMotorDatabase, 
            current_user: Optional[Union[UserSchema, None]], 
            client_ip: Optional[Union[str, None]]
        ) -> None:
        try:
            await self.payment_service.delete_payment(id, db, current_user, client_ip)
        except (HTTPException) as e:
            raise e
        except Exception as e:
            raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                    detail=f"Internal Server Error: {str(e)}"
                )

    async def read_payments(
            self, 
            payment_read_request_schema: PaymentReadRequestSchema, 
            db: AsyncIOMotorDatabase, 
            current_user: Optional[Union[UserSchema, None]], 
            client_ip: Optional[Union[str, None]]
        ) -> Optional[PaginateResponseSchema[List[PaymentSchema]]]:
        try:
            temp_response = await self.payment_service.read_payments(payment_read_request_schema, db, current_user, client_ip)
            return temp_response
        except (HTTPException) as e:
            raise e
        except Exception as e:
            raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                    detail=f"Internal Server Error: {str(e)}"
                )

    async def read_payment_by_id(
            self, 
            id: str, 
            db: AsyncIOMotorDatabase, 
            current_user: Optional[Union[UserSchema, None]], 
            client_ip: Optional[Union[str, None]]
        ) -> Optional[PaymentSchema]:
        try:
            temp_response = await self.payment_service.read_payment_by_id(id, db, current_user, client_ip)
            return temp_response
        except (HTTPException) as e:
            raise e
        except Exception as e:
            raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                    detail=f"Internal Server Error: {str(e)}"
                )

__all__ = [
    "PaymentController"
]