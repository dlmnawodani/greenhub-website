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
from beanie import PydanticObjectId, MergeStrategy, UpdateResponse
from beanie import operators as operators
from datetime import datetime, timezone
import app.configs.database as database
from app.configs.Setting import Setting as Setting
from app.utils.Logger import Logger as Logger
from app.enums.OrderStatus import OrderStatus as OrderStatus
# import models
from app.models.Order import Order as OrderModel
from app.models.OrderItem import OrderItem as OrderItemModel
from app.models.Cart import Cart as CartModel
from app.models.User import User as UserModel
from app.models.Product import Product as ProductModel
from app.models.Payment import Payment as PaymentModel
# import schemas
from app.schemas.User import User as UserSchema
from app.schemas.Order import Order as OrderSchema
from app.schemas.OrderItem import OrderItem as OrderItemSchema
from app.schemas.Payment import Payment as PaymentSchema
from app.schemas.OrderCreateRequest import OrderCreateRequest as OrderCreateRequestSchema
from app.schemas.OrderUpdateRequest import OrderUpdateRequest as OrderUpdateRequestSchema
from app.schemas.OrderReadRequest import OrderReadRequest as OrderReadRequestSchema
from app.schemas.OrderStatusUpdateRequest import OrderStatusUpdateRequest as OrderStatusUpdateRequestSchema
from app.schemas.PaginateResponse import PaginateResponse as PaginateResponseSchema

class OrderService:
    def __init__(self):
        self.settings = Setting()
        self.logger = Logger(__name__)


    async def create_order(
            self, 
            order_create_request_schema: OrderCreateRequestSchema, 
            db: AsyncIOMotorDatabase, 
            current_user: Optional[Union[UserSchema, None]], 
            client_ip: Optional[Union[str, None]]
        ) -> Optional[OrderSchema]:
            self.logger.debug("create_order called")
            async with await db.client.start_session() as session:
                try:
                    async with session.start_transaction():
                        order_create_request_schema_dict = order_create_request_schema.model_dump(
                            exclude_unset=True,
                            # exclude_none=True
                        )
                        created_at = datetime.now(tz=timezone.utc)
                        order_create_request_schema_dict["created_at"] = created_at
                        order_create_request_schema_dict["ip_address"] = client_ip

                        user_instance = await UserModel.find_one(UserModel.id == PydanticObjectId(current_user.id))
                        if not user_instance:
                            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
                        order_create_request_schema_dict["user"] = user_instance
                        
                        order_instance = OrderModel(
                            **order_create_request_schema_dict,
                            order_total_amount=0,
                            order_due_amount=0,
                            order_status=OrderStatus.PENDING
                        )

                        order_instance = await order_instance.create(session=session)

                        cart_read_query = CartModel.find(fetch_links=True)
                        cart_read_query = cart_read_query.find(CartModel.user.id == PydanticObjectId(user_instance.id), fetch_links=True)
                        cart_items = await cart_read_query.to_list()

                        if not cart_items:
                            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart Items not found")

                        for cart_item in cart_items:
                            product_instance = await ProductModel.find_one(ProductModel.id == PydanticObjectId(cart_item.product.id))
                            order_item_instance = await OrderItemModel(
                                    order=order_instance,
                                    product=product_instance,
                                    qty=cart_item.qty,
                                    price=product_instance.price
                                ).create(session=session)
                            await product_instance.update(operators.Inc({ProductModel.qty_in_stock: -abs(cart_item.qty)}), session=session)
                            await cart_item.delete(
                                # link_rule=DeleteRules.DELETE_LINKS, 
                                session=session
                            )
                                
                        cart_total_amount = await self.calculate_cart_total_amount(cart_items)
                        await order_instance.update({"$set": dict(order_total_amount=cart_total_amount, order_due_amount=cart_total_amount)}, session=session)
                        
                    # Commit transaction if everything succeeds
                    await session.commit_transaction()
                    return OrderSchema.model_validate(order_instance.model_dump(by_alias=True))
                except Exception as e:
                    # Rollback transaction if an error occurs
                    if not session.has_ended and session.in_transaction:
                        await session.abort_transaction()
                    self.logger.exception("Error in create_order", e)
                    raise e

    async def update_order_status(
            self, 
            id: str,
            order_status_update_request_schema: OrderStatusUpdateRequestSchema, 
            db: AsyncIOMotorDatabase, 
            current_user: Optional[Union[UserSchema, None]], 
            client_ip: Optional[Union[str, None]]
        ) -> Optional[OrderSchema]:
            self.logger.debug("update_order_status called")
            async with await db.client.start_session() as session:
                try:
                    async with session.start_transaction():
                        order_instance = await OrderModel.find_one(OrderModel.id == PydanticObjectId(id))
                        if not order_instance:
                            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

                        order_status_update_request_schema_dict = order_status_update_request_schema.model_dump(
                            exclude_unset=True,
                            # exclude_none=True
                        )
                        updated_at = datetime.now(tz=timezone.utc)
                        order_status_update_request_schema_dict["updated_at"] = updated_at

                        await order_instance.update({"$set": order_status_update_request_schema_dict}, session=session)
                    # Commit transaction if everything succeeds
                    await session.commit_transaction()

                    return OrderSchema.model_validate(order_instance.model_dump(by_alias=True))
                except Exception as e:
                    # Rollback transaction if an error occurs
                    if not session.has_ended and session.in_transaction:
                        await session.abort_transaction()
                    self.logger.exception("Error in update_order_status", e)
                    raise e

    async def delete_order(
            self, 
            id: str,
            db: AsyncIOMotorDatabase, 
            current_user: Optional[Union[UserSchema, None]], 
            client_ip: Optional[Union[str, None]]
        ) -> None:
            self.logger.debug("delete_order called")
            async with await db.client.start_session() as session:
                try:
                    async with session.start_transaction():
                        order_instance = await OrderModel.find_one(OrderModel.id == PydanticObjectId(id))
                        if not order_instance:
                            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
                        
                        await OrderItemModel.find(OrderItemModel.order.id == PydanticObjectId(order_instance.id)).delete(
                            # link_rule=DeleteRules.DELETE_LINKS, 
                            session=session
                        )

                        await PaymentModel.find(PaymentModel.order.id == PydanticObjectId(order_instance.id)).delete(
                            # link_rule=DeleteRules.DELETE_LINKS, 
                            session=session
                        )
                        
                        await order_instance.delete(
                                # link_rule=DeleteRules.DELETE_LINKS, 
                                session=session
                            )
                    # Commit transaction if everything succeeds
                    await session.commit_transaction()

                except Exception as e:
                    # Rollback transaction if an error occurs
                    if not session.has_ended and session.in_transaction:
                        await session.abort_transaction()
                    self.logger.exception("Error in delete_order", e)
                    raise e


    async def read_order_by_id(
            self, 
            id: str,
            db: AsyncIOMotorDatabase, 
            current_user: Optional[Union[UserSchema, None]], 
            client_ip: Optional[Union[str, None]]
        ) -> Optional[OrderSchema]:
            self.logger.debug("read_order_by_id called")
            try:
                order_instance = await OrderModel.find_one(operators.Eq(OrderModel.id, PydanticObjectId(id)), fetch_links=True)
                if not order_instance:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
                
                order_items = await OrderItemModel.find(OrderItemModel.order.id == PydanticObjectId(order_instance.id), fetch_links=True).to_list()

                payments = await PaymentModel.find(PaymentModel.order.id == PydanticObjectId(order_instance.id), fetch_links=True).to_list()

                return OrderSchema.model_validate({
                    **order_instance.model_dump(by_alias=True),
                    "order_items": [OrderItemSchema.model_validate(v.model_dump(by_alias=True)) for v in order_items],
                    "payments": [PaymentSchema.model_validate(v.model_dump(by_alias=True)) for v in payments]
                })
            except Exception as e:
                self.logger.exception("Error in read_order_by_id", e)
                raise e

    async def read_orders(
            self, 
            order_read_request_schema: OrderReadRequestSchema, 
            db: AsyncIOMotorDatabase, 
            current_user: Optional[Union[UserSchema, None]], 
            client_ip: Optional[Union[str, None]]
        ) -> Optional[PaginateResponseSchema[List[OrderSchema]]]:
            self.logger.debug("read_orders called")
            try:
                query = OrderModel.find(fetch_links=True)
                order_read_request_schema_dict = order_read_request_schema.model_dump(
                            exclude_unset=True,
                            # exclude_none=True
                        )
                
                query_filters = {}
                
                # Filter by user_id if provided
                user_id_filter = order_read_request_schema_dict.get("user_id")
                if user_id_filter:
                    query = query.find(OrderModel.user.id == PydanticObjectId(user_id_filter), fetch_links=True)

                # Filter by order_status if provided
                order_status_filter = order_read_request_schema_dict.get("order_status")
                if order_status_filter:
                    query = query.find(OrderModel.order_status == order_status_filter, fetch_links=True)

                # Filter by date_from if provided
                date_from_filter = order_read_request_schema_dict.get("date_from")
                if date_from_filter:
                    # date_from_filter = datetime.strptime(date_from_filter, "%Y-%m-%d").replace(hour=0, minute=0, second=0)
                    date_from_filter = datetime.combine(date_from_filter, datetime.min.time())
                    query_filters.setdefault("created_at", {}).update({"$gte": date_from_filter})
                    query = query.find(query_filters, fetch_links=True)

                # Filter by date_to if provided
                date_to_filter = order_read_request_schema_dict.get("date_to")
                if date_to_filter:
                    # date_to_filter = datetime.strptime(date_to_filter, "%Y-%m-%d").replace(hour=23, minute=59, second=59)
                    date_to_filter = datetime.combine(date_to_filter, datetime.max.time())
                    query_filters.setdefault("created_at", {}).update({"$lt": date_to_filter})
                    query = query.find(query_filters, fetch_links=True)

                # Filter by ids if provided
                ids_filter = order_read_request_schema_dict.get("ids")
                if ids_filter:
                    ids_filter_map = map(lambda id: PydanticObjectId(id), ids_filter)
                    ids_filter_list = list(ids_filter_map)
                    query = query.find(operators.In(ProductModel.id, ids_filter_list), fetch_links=True)

                total_count = await query.count()

                if "paginate" in order_read_request_schema_dict and order_read_request_schema_dict.get("paginate") == True:
                    query.skip(
                            order_read_request_schema_dict.get("skip", 0)
                        ).limit(
                            order_read_request_schema_dict.get("limit", 0)
                        )
                    
                query = query.sort(
                    [
                        (OrderModel.id, pymongo.DESCENDING)
                    ]
                )
                
                results = await query.to_list(
                        # length=cart_read_request_schema_dict.get("limit", 0)
                    )
                
                product_schema_list = [OrderSchema.model_validate(v.model_dump(by_alias=True)) for v in results]
                return PaginateResponseSchema[List[OrderSchema]](count=total_count, result=product_schema_list)

            except Exception as e:
                self.logger.exception("Error in read_orders", e)
                raise e
            

    async def calculate_cart_total_amount(self, cart_items: List[CartModel]) -> float:
        total_amount = 0.0

        for cart_item in cart_items:
            if cart_item.product and cart_item.product.price is not None:
                total_amount += cart_item.product.price * cart_item.qty

        return total_amount
                

__all__ = [
    "OrderService"
]
