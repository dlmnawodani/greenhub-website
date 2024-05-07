# Import required packages and modules
# from __future__ import annotations
# import logging as logging
# import sys as sys
import os as os
from pathlib import Path as PathLibPath
# from decouple import config
# import asyncio as asyncio
# from typing import TYPE_CHECKING
from typing import TYPE_CHECKING, Optional, Any, Type, TypeVar, Generic, ForwardRef, Annotated, Union, List
from contextlib import asynccontextmanager
from fastapi import FastAPI, APIRouter, Request, Depends, Security, HTTPException, status, Query, Path, Body, Cookie, Header, Form, File, UploadFile
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from beanie import init_beanie
from app.configs.database import connect_to_database, close_database_connection, get_database
from app.errors.BadRequest import BadRequest
from app.errors.UnprocessableError import UnprocessableError
from app.utils.Logger import Logger as Logger
from app.configs.Setting import Setting as Setting
# import routes
from app.api.v1 import application_routes as application_routes
from app.api.v1 import auth_routes as auth_routes
from app.api.v1 import user_routes as user_routes
from app.api.v1 import product_routes as product_routes
from app.api.v1 import review_routes as review_routes
from app.api.v1 import cart_routes as cart_routes
from app.api.v1 import order_routes as order_routes
from app.api.v1 import payment_routes as payment_routes
from app.api.v1 import category_routes as category_routes
# import models
from app.models.User import User as UserModel
from app.models.Review import Review as ReviewModel
from app.models.Product import Product as ProductModel
from app.models.Payment import Payment as PaymentModel
from app.models.OrderItem import OrderItem as OrderItemModel
from app.models.Order import Order as OrderModel
from app.models.Cart import Cart as CartModel
from app.models.Category import Category as CategoryModel
 
logging = Logger(__name__)
settings = Setting()

'''
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     logging.debug("startup has begun!!")
#     yield
#     logging.debug("shutdown has begun!!")
# app = FastAPI(lifespan=lifespan)
'''

# Ensure the static directories exists
'''
# if not os.path.exists(settings.STATIC_FRONTEND_FILES_DIRECTORY):
#     os.makedirs(settings.STATIC_FRONTEND_FILES_DIRECTORY)
'''
PathLibPath(settings.STATIC_FRONTEND_FILES_DIRECTORY).mkdir(parents=True, exist_ok=True)
PathLibPath(settings.STATIC_IMAGE_FILES_DIRECTORY).mkdir(parents=True, exist_ok=True)

app = FastAPI()

# Middlewares
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# mounting static folder on serve for fetching static files
app.mount("/static", StaticFiles(directory=settings.STATIC_FRONTEND_FILES_DIRECTORY), name="static")
app.mount("/images", StaticFiles(directory=settings.STATIC_IMAGE_FILES_DIRECTORY), name="images")

async def connect_and_init_db():
    try:
        await connect_to_database()
        db = await get_database()
        await init_beanie(
            database=db,
            document_models= [
                UserModel,
                CategoryModel,
                ProductModel,
                ReviewModel,
                CartModel,
                OrderModel,
                OrderItemModel,
                PaymentModel
            ]
        )
        logging.debug("database initialized")
    except Exception as e:
        logging.exception("An error occurred while initializing the database", e)

# DB Events
app.add_event_handler("startup", connect_and_init_db)
app.add_event_handler("shutdown", close_database_connection)

# openapi schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        routes=app.routes
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi


# HTTP error responses
@app.exception_handler(BadRequest)
async def bad_request_handler(req: Request, exc: BadRequest) -> JSONResponse:
    return exc.gen_err_resp()


@app.exception_handler(RequestValidationError)
async def invalid_req_handler(
    req: Request,
    exc: RequestValidationError
) -> JSONResponse:
    logging.error(f"Request invalid. {str(exc)}")
    return JSONResponse(
        status_code=400,
        content={
            "type": "about:blank",
            "title": "Bad Request",
            "status": 400,
            "detail": [str(exc)]
        }
    )


@app.exception_handler(UnprocessableError)
async def unprocessable_error_handler(
    req: Request,
    exc: UnprocessableError
) -> JSONResponse:
    return exc.gen_err_resp()


# # API Path
# # # Application
app.include_router(
    application_routes.router,
    prefix=settings.API_ROUTE_PREFIX,
    tags=["application"]
)

# # # Auth
app.include_router(
    auth_routes.router,
    prefix=settings.API_ROUTE_PREFIX,
    tags=["auth"]
)

# # # User
app.include_router(
    user_routes.router,
    prefix=settings.API_ROUTE_PREFIX,
    tags=["user"]
)

# # # Product
app.include_router(
    product_routes.router,
    prefix=settings.API_ROUTE_PREFIX,
    tags=["product"]
)

# # # Review
app.include_router(
    review_routes.router,
    prefix=settings.API_ROUTE_PREFIX,
    tags=["review"]
)

# # # Cart
app.include_router(
    cart_routes.router,
    prefix=settings.API_ROUTE_PREFIX,
    tags=["cart"]
)

# # # Order
app.include_router(
    order_routes.router,
    prefix=settings.API_ROUTE_PREFIX,
    tags=["order"]
)

# # # Payment
app.include_router(
    payment_routes.router,
    prefix=settings.API_ROUTE_PREFIX,
    tags=["payment"]
)

# # # Category
app.include_router(
    category_routes.router,
    prefix=settings.API_ROUTE_PREFIX,
    tags=["category"]
)


__all__ = [
    "app"
]
