# Import required packages and modules
# from __future__ import annotations
# import logging as logging
# import sys as sys
# import os as os
from decouple import config
# import asyncio as asyncio
from typing import TYPE_CHECKING, \
    Optional, \
    Any, \
    TypeVar, \
    ForwardRef, \
    Annotated, \
    Union, \
    List, \
    Dict
from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

def cast_or_default(v, cast_type, default_val=None):
    try:
        if v is None:
            return v
        return cast_type(v)
    except (ValueError, TypeError, Exception) as e:
        return default_val

def cast_to_bool(v):
    bool_val = False
    try:
        if v is None:
            return v
        elif v.lower() in ('true', 'yes', 'on', '1'):
            bool_val = True
        elif v.lower() in ('false', 'no', 'off', '0'):
            bool_val = False
    except (ValueError, TypeError, Exception) as e:
        bool_val = False
    return bool_val

class Setting(BaseSettings):
    # pass
    '''
    # def __init__(self, **data):
    #     pass
    '''
    ## api
    APP_NAME: Optional[str] = config(
        "APP_NAME", 
        default=None, 
        cast=lambda v: cast_or_default(v, str, v)
    )
    APP_VERSION: Optional[str] = config(
        "APP_VERSION", 
        default=None, 
        cast=lambda v: cast_or_default(v, str, v)
    )
    APP_DEBUG: Optional[bool] = config(
        "APP_DEBUG", 
        default=False, 
        cast=lambda v: cast_to_bool(v)
    )
    APP_URL: Optional[str] = config(
        "APP_URL", 
        default=None, 
        cast=lambda v: cast_or_default(v, str, v)
    )
    API_ROUTE_PREFIX: Optional[str] = config(
        "API_ROUTE_PREFIX", 
        default="/v1", 
        cast=lambda v: cast_or_default(v, str, v)
    )
    STATIC_FRONTEND_FILES_DIRECTORY: Optional[str] = config(
        "STATIC_FRONTEND_FILES_DIRECTORY", 
        default="static", 
        cast=lambda v: cast_or_default(v, str, v)
    )
    STATIC_IMAGE_FILES_DIRECTORY: Optional[str] = config(
        "STATIC_IMAGE_FILES_DIRECTORY", 
        default="images", 
        cast=lambda v: cast_or_default(v, str, v)
    )
    # BACKEND_CORS_ORIGINS: Optional[List[AnyHttpUrl]] = config(
    #     "BACKEND_CORS_ORIGINS", 
    #     default="http://localhost:3000", 
    #     cast=lambda v: [s.strip() for s in v.split(',')] if isinstance(v, str) else v
    # )
    ## database
    DB_USER: Optional[str] = config(
        "DB_USER", 
        default=None, 
        cast=lambda v: cast_or_default(v, str, v)
    )
    DB_PASSWORD: Optional[str] = config(
        "DB_PASSWORD", 
        default=None, 
        cast=lambda v: cast_or_default(v, str, v)
    )
    DB_HOST: Optional[str] = config(
        "DB_HOST", 
        default=None, 
        cast=lambda v: cast_or_default(v, str, v)
    )
    # DB_PORT: Optional[int] = config(
    #     "DB_PORT", 
    #     default=None, 
    #     cast=lambda v: cast_or_default(v, int, v)
    # )
    DB_NAME: Optional[str] = config(
        "DB_NAME", 
        default=None, 
        cast=lambda v: cast_or_default(v, str, v)
    )
    DB_MAX_CONN_COUNT: Optional[int] = config(
        "DB_MAX_CONN_COUNT", 
        default=0, 
        cast=lambda v: cast_or_default(v, int, v)
    )
    DB_MIN_CONN_COUNT: Optional[int] = config(
        "DB_MIN_CONN_COUNT", 
        default=0, 
        cast=lambda v: cast_or_default(v, int, v)
    )
    DB_UUID_REPRESENTATION: Optional[str] = config(
        "DB_UUID_REPRESENTATION", 
        default="standard", 
        cast=lambda v: cast_or_default(v, str, v)
    )
    ## JWT
    ## openssl rand -hex 32
    JWT_TOKEN_ACCESS_SECRET_KEY: Optional[str] = config(
        "JWT_TOKEN_ACCESS_SECRET_KEY", 
        default=None, 
        cast=lambda v: cast_or_default(v, str, v)
    )
    JWT_TOKEN_REFRESH_SECRET_KEY: Optional[str] = config(
        "JWT_TOKEN_REFRESH_SECRET_KEY", 
        default=None, 
        cast=lambda v: cast_or_default(v, str, v)
    )
    JWT_TOKEN_ALGORITHM: Optional[str] = config(
        "JWT_TOKEN_ALGORITHM", 
        default="HS256", 
        cast=lambda v: cast_or_default(v, str, v)
    )
    JWT_TOKEN_ACCESS_EXPIRE_MINUTES: Optional[int] = config(
        "JWT_TOKEN_ACCESS_EXPIRE_MINUTES", 
        default=(1440 * 365 * 10), 
        cast=lambda v: cast_or_default(v, int, v)
    )
    JWT_TOKEN_REFRESH_EXPIRE_MINUTES: Optional[int] = config(
        "JWT_TOKEN_REFRESH_EXPIRE_MINUTES", 
        default=(1440 * 365 * 10), 
        cast=lambda v: cast_or_default(v, int, v)
    )
    JWT_TOKEN_URL: Optional[str] = config(
        "JWT_TOKEN_URL", 
        default=None, 
        cast=lambda v: cast_or_default(v, str, v)
    )
    JWT_TOKEN_AUTO_ERROR: Optional[bool] = config(
        "JWT_TOKEN_AUTO_ERROR", 
        default=False, 
        cast=lambda v: cast_to_bool(v)
    )
    JWT_TOKEN_SCHEME_NAME: Optional[str] = config(
        "JWT_TOKEN_SCHEME_NAME", 
        default="JWT", 
        cast=lambda v: cast_or_default(v, str, v)
    )

    '''
    # @classmethod
    # def cast_or_default(cls, v, cast_type, default_val=None):
    #     try:
    #         if v is None:
    #             return v
    #         return cast_type(v)
    #     except (ValueError, TypeError):
    #         return default_val
    '''
    '''
    # @staticmethod
    # def cast_or_default(v, cast_type, default_val=None):
    #     try:
    #         if v is None:
    #             return v
    #         return cast_type(v)
    #     except (ValueError, TypeError):
    #         return default_val
    '''

    class Config:
        # pass
        case_sensitive = True
        validate_default=False

if __name__ == "__main__":
    print(Setting().model_dump())

__all__ = [
    "Setting"
]
