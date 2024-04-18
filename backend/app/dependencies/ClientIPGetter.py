# from __future__ import annotations
from fastapi import Depends, HTTPException, status, Request
# from typing import Optional

class ClientIPGetter:
    def __init__(self):
        pass

    async def __call__(self, request: Request) -> str:
        client_ip = None
        # Get the client's IP address from the X-Forwarded-For header
        x_forwarded_for = request.headers.get("X-Forwarded-For")
        if x_forwarded_for:
            # The X-Forwarded-For header can contain a comma-separated list of IP addresses.
            # The first IP address in the list is the client's IP address.
            client_ip = x_forwarded_for.split(",")[0].strip()
        else:
            # If X-Forwarded-For header is not present, use the remote address from the request.
            client_ip = request.client.host
        
        return client_ip


__all__ = [
    'ClientIPGetter'
]