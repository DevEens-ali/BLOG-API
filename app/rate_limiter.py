import time

from fastapi import HTTPException


request_records = {}


def rate_limit(client_ip: str):
    current_time = time.time()

    if client_ip not in request_records:
        request_records[client_ip] = []

    request_records[client_ip] = [
        request_time
        for request_time in request_records[client_ip]
        if current_time - request_time < 60
    ]

    if len(request_records[client_ip]) >= 10:
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Please try again later."
        )

    request_records[client_ip].append(current_time)