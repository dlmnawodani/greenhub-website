# Import required packages and modules
# from __future__ import annotations
# import logging as logging
# import sys as sys
import os as os
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
from fastapi import FastAPI, APIRouter, Request, Depends, HTTPException, status, Body, Query
import pymongo as pymongo
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from beanie import PydanticObjectId, MergeStrategy
from beanie import operators as operators
from datetime import datetime, timezone
import app.configs.database as database
from app.configs.Setting import Setting as Setting
from app.utils.Logger import Logger as Logger
from app.utils.FileHandler import FileHandler as FileHandler
# import models
from app.models.Payment import Payment as PaymentModel
from app.models.Order import Order as OrderModel
# import schemas
from app.schemas.User import User as UserSchema
from app.schemas.Payment import Payment as PaymentSchema
from app.schemas.PaymentCreateRequest import PaymentCreateRequest as PaymentCreateRequestSchema
from app.schemas.PaymentUpdateRequest import PaymentUpdateRequest as PaymentUpdateRequestSchema
from app.schemas.PaymentReadRequest import PaymentReadRequest as PaymentReadRequestSchema
from app.schemas.PaginateResponse import PaginateResponse as PaginateResponseSchema

class PaymentService:
    def __init__(self):
        self.settings = Setting()
        self.logger = Logger(__name__)


    async def create_payment(
            self, 
            payment_create_request_schema: PaymentCreateRequestSchema, 
            db: AsyncIOMotorDatabase, 
            current_user: Optional[Union[UserSchema, None]], 
            client_ip: Optional[Union[str, None]]
        ) -> Optional[PaymentSchema]:
            self.logger.debug("create_payment called")
            async with await db.client.start_session() as session:
                try:
                    async with session.start_transaction():
                        payment_create_request_schema_dict = payment_create_request_schema.model_dump(
                            exclude_unset=True,
                            # exclude_none=True
                        )
                        created_at = datetime.now(tz=timezone.utc)
                        payment_create_request_schema_dict["created_at"] = created_at

                        order_id = payment_create_request_schema_dict.get("order_id")
                        order_instance = await OrderModel.find_one(OrderModel.id == PydanticObjectId(order_id))
                        if not order_instance:
                            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
                        payment_create_request_schema_dict["order"] = order_instance
                        
                        payment_instance = PaymentModel(
                            **payment_create_request_schema_dict
                        )
                        
                        # payment_instance = await PaymentModel.insert_one(payment_instance, session=session)
                        payment_instance = await payment_instance.create(session=session)

                        await order_instance.update(operators.Inc({OrderModel.order_due_amount: -abs(payment_instance.amount)}), session=session)

                    # Commit transaction if everything succeeds
                    await session.commit_transaction()

                    return PaymentSchema.model_validate(payment_instance.model_dump(by_alias=True))
                except Exception as e:
                    # Rollback transaction if an error occurs
                    if not session.has_ended and session.in_transaction:
                        await session.abort_transaction()
                    self.logger.exception("Error in create_payment", e)
                    raise e

    async def update_payment(
            self, 
            id: str,
            payment_update_request_schema: PaymentUpdateRequestSchema, 
            db: AsyncIOMotorDatabase, 
            current_user: Optional[Union[UserSchema, None]], 
            client_ip: Optional[Union[str, None]]
        ) -> Optional[PaymentSchema]:
            self.logger.debug("update_payment called")
            async with await db.client.start_session() as session:
                try:
                    async with session.start_transaction():
                        payment_instance = await PaymentModel.find_one(PaymentModel.id == PydanticObjectId(id), fetch_links=True)
                        if not payment_instance:
                            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")

                        payment_update_request_schema_dict = payment_update_request_schema.model_dump(
                            exclude_unset=True,
                            # exclude_none=True
                        )
                        updated_at = datetime.now(tz=timezone.utc)
                        payment_update_request_schema_dict["updated_at"] = updated_at

                        order_instance = await OrderModel.find_one(OrderModel.id == PydanticObjectId(payment_instance.order.id))
                        if not order_instance:
                            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
                        
                        await order_instance.update(operators.Inc({OrderModel.order_due_amount: (-1 * (payment_instance.amount - payment_update_request_schema_dict.get("amount")))}), session=session)

                        await payment_instance.update({"$set": payment_update_request_schema_dict}, session=session)
                    # Commit transaction if everything succeeds
                    await session.commit_transaction()

                    return PaymentSchema.model_validate(payment_instance.model_dump(by_alias=True))
                except Exception as e:
                    # Rollback transaction if an error occurs
                    if not session.has_ended and session.in_transaction:
                        await session.abort_transaction()
                    self.logger.exception("Error in update_payment", e)
                    raise e

    async def delete_payment(
            self, 
            id: str,
            db: AsyncIOMotorDatabase, 
            current_user: Optional[Union[UserSchema, None]], 
            client_ip: Optional[Union[str, None]]
        ) -> None:
            self.logger.debug("delete_payment called")
            async with await db.client.start_session() as session:
                try:
                    async with session.start_transaction():
                        payment_instance = await PaymentModel.find_one(PaymentModel.id == PydanticObjectId(id))
                        if not payment_instance:
                            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")
                        await payment_instance.delete(
                                # link_rule=DeleteRules.DELETE_LINKS, 
                                session=session
                            )
                    # Commit transaction if everything succeeds
                    await session.commit_transaction()

                except Exception as e:
                    # Rollback transaction if an error occurs
                    if not session.has_ended and session.in_transaction:
                        await session.abort_transaction()
                    self.logger.exception("Error in delete_payment", e)
                    raise e


    async def read_payment_by_id(
            self, 
            id: str,
            db: AsyncIOMotorDatabase, 
            current_user: Optional[Union[UserSchema, None]], 
            client_ip: Optional[Union[str, None]]
        ) -> Optional[PaymentSchema]:
            self.logger.debug("read_payment_by_id called")
            try:
                payment_instance = await PaymentModel.find_one(operators.Eq(PaymentModel.id, PydanticObjectId(id)), fetch_links=True)
                if not payment_instance:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")
                return PaymentSchema.model_validate(payment_instance.model_dump(by_alias=True))
            except Exception as e:
                self.logger.exception("Error in read_payment_by_id", e)
                raise e

    async def read_payments(
            self, 
            payment_read_request_schema: PaymentReadRequestSchema, 
            db: AsyncIOMotorDatabase, 
            current_user: Optional[Union[UserSchema, None]], 
            client_ip: Optional[Union[str, None]]
        ) -> Optional[PaginateResponseSchema[List[PaymentSchema]]]:
            self.logger.debug("read_payments called")
            try:
                query = PaymentModel.find(fetch_links=True)

                payment_read_request_schema_dict = payment_read_request_schema.model_dump(
                            exclude_unset=True,
                            # exclude_none=True
                        )

                # Filter by order_id if provided
                order_id_filter = payment_read_request_schema_dict.get("order_id")
                if order_id_filter:
                    query = query.find(PaymentModel.order.id == order_id_filter, fetch_links=True)

                total_count = await query.count()

                if "paginate" in payment_read_request_schema_dict and payment_read_request_schema_dict.get("paginate") == True:
                    query.skip(
                            payment_read_request_schema_dict.get("skip", 0)
                        ).limit(
                            payment_read_request_schema_dict.get("limit", 0)
                        )
                    
                query = query.sort(
                    [
                        (PaymentModel.id, pymongo.DESCENDING)
                    ]
                )
                
                results = await query.to_list(
                        # length=product_read_request_schema_dict.get("limit", 0)
                    )

                payment_schema_list = [PaymentSchema.model_validate(v.model_dump(by_alias=True)) for v in results]
                return PaginateResponseSchema[List[PaymentSchema]](count=total_count, result=payment_schema_list)

            except Exception as e:
                self.logger.exception("Error in read_payments", e)
                raise e


__all__ = [
    "PaymentService"
]
