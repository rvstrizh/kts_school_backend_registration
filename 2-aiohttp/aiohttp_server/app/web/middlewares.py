import json
import typing

from aiohttp_apispec.middlewares import validation_middleware
from aiohttp.web import middleware
from aiohttp.web_exceptions import HTTPException, HTTPUnprocessableEntity

from app.web.utils import error_json_response

if typing.TYPE_CHECKING:
    from app.web.app import Application


@middleware
# в middleware всешда передаются два аргумента делаем ее асинхронной т.к. ответ получается асинхронный
async def error_handling_middleware(request, handler):
    try:
        response = await handler(request)# нужно получить ответ, в момене получения response мы можем получить исключение
        return response
        # поймать исключение которое выбрасывается aiohttp_apispec когда не проходим валидацию схемы когда вместо 400
        # выводится 422, так как он не может сказать что это не преобразуемая сущность
    except HTTPUnprocessableEntity as e:
        # когда ее ловим выдаем не 422 а 400
        return error_json_response(http_status=400, status='bad request', message=e.reason,
                                   data=json.loads(e.text)) # преобразовываем e.text в json

    except HTTPException as e:
        return error_json_response(http_status=e.status, status='error', message=str(e))
    except Exception as e: # ловим любое исключение
        return error_json_response(http_status=500, status='internal server error', message=str(e))


def setup_middlewares(app: "Application"):
    # мидл вары выполяются в обратном порядке
    app.middlewares.append(error_handling_middleware) # добавляем в список мидваров
    app.middlewares.append(validation_middleware)