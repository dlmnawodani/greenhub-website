# Import required packages and modules
# from __future__ import annotations
# import logging as logging
# import sys as sys
# import os as os
# from decouple import config
# import asyncio as asyncio
from typing import TYPE_CHECKING, \
    Optional, \
    Any, \
    Union
from datetime import datetime, timezone, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
import hashlib as hashlib
from app.configs.Setting import Setting as Setting
from .Logger import Logger as Logger

class Security:
    # pass
    def __init__(self):
        self.settings = Setting()
        self.logger = Logger(__name__)
        self.crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_access_token(self, subject: Union[str, Any], expires_delta: int = None) -> str:
        try:
            token_access_secret_key = self.settings.JWT_TOKEN_ACCESS_SECRET_KEY
            token_algorithm = self.settings.JWT_TOKEN_ALGORITHM
            token_access_expire_minutes = self.settings.JWT_TOKEN_ACCESS_EXPIRE_MINUTES

            if expires_delta is not None:
                expires_delta = datetime.now(tz=timezone.utc) + expires_delta
            else:
                expires_delta = datetime.now(tz=timezone.utc) + timedelta(minutes=token_access_expire_minutes)

            to_encode = dict(sub = str(subject), exp = expires_delta)
            # to_encode.update({"exp": expires_delta})

            encoded_jwt = jwt.encode(to_encode, token_access_secret_key, token_algorithm)
            return encoded_jwt
        except Exception as e:
            self.logger.exception("Could create a access token", e)
            raise e

    def create_refresh_token(self, subject: Union[str, Any], expires_delta: int = None) -> str:
        try:
            token_refresh_secret_key = self.settings.JWT_TOKEN_REFRESH_SECRET_KEY
            token_algorithm = self.settings.JWT_TOKEN_ALGORITHM
            token_refresh_expire_minutes = self.settings.JWT_TOKEN_REFRESH_EXPIRE_MINUTES

            if expires_delta is not None:
                expires_delta = datetime.now(tz=timezone.utc) + expires_delta
            else:
                expires_delta = datetime.now(tz=timezone.utc) + timedelta(minutes=token_refresh_expire_minutes)

            to_encode = dict(sub = str(subject), exp = expires_delta)
            # to_encode.update({"exp": expires_delta})

            encoded_jwt = jwt.encode(to_encode, token_refresh_secret_key, token_algorithm)
            return encoded_jwt
        except Exception as e:
            self.logger.exception("Could create a token refresh", e)
            raise e

    def decode_access_token(self, token: str) -> Optional[dict]:
        try:
            token_access_secret_key = self.settings.JWT_TOKEN_ACCESS_SECRET_KEY
            token_algorithm = self.settings.JWT_TOKEN_ALGORITHM
            payload = jwt.decode(token, token_access_secret_key, algorithms=[token_algorithm])
            # sub: str = payload.get("sub")
            return payload
        except (JWTError, Exception) as e:
            self.logger.exception("Could not decode access token", e)
            return None

    def decode_refresh_token(self, token: str) -> Optional[dict]:
        try:
            token_refresh_secret_key = self.settings.JWT_TOKEN_REFRESH_SECRET_KEY
            token_algorithm = self.settings.JWT_TOKEN_ALGORITHM
            payload = jwt.decode(token, token_refresh_secret_key, algorithms=[token_algorithm])
            # sub: str = payload.get("sub")
            return payload
        except (JWTError, Exception) as e:
            self.logger.exception("Could not decode refresh token", e)
            return None

    def create_hashed_str(self, plain_str: str) -> str:
        hashed_str = self.crypt_context.hash(plain_str)
        return hashed_str

    def verify_hashed_str(self, plain_str: str, hashed_str: str) -> bool:
        is_verified = self.crypt_context.verify(plain_str, hashed_str)
        return is_verified


__all__ = [
    "Security"
]


        