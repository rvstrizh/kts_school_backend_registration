import base64
from typing import Any, Optional

from aiohttp.web_response import Response
from aiohttp.web import json_response as aiohttp_json_response


def json_response(data: Any = None, status: str = 'ok') -> Response:
    if data is None: # если не передали аргумент
        data = {}
    return aiohttp_json_response(
        data={
            "status": status,
            "data": data,
        })


def error_json_response(http_status: int, status: str = 'error', message: Optional[str] = None,
                        data: Optional[dict] = None):
    if data is None:  # если не передали аргумент
        data = {}
    return aiohttp_json_response(
        status=http_status,
        data={
            "status": status,
            "message": str(message),
            "data": data
        })


# из заголовка получить данные
def check_basic_auth(raw_credentials: str, username: str, password: str) -> bool:  # raw_credentials-строка в заголовке
    # преводит base64.b64decode(raw_credentials) из набора символов в b'username:password'
    # в конце .decode() убирает b'
    credentials = base64.b64decode(raw_credentials).decode()
    parts = credentials.split(':')  # разделяем на две части
    if len(parts) != 2:
        return False
    return parts[0] == username and parts[1] == password