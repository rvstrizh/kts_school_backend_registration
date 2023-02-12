from typing import Optional
from aiohttp_apispec import setup_aiohttp_apispec

from aiohttp.web import Application as AiohttpApplication, run_app as aiohttp_run_app, View as AiohttpView, \
    Request as AiohttpRequest

from app.store import setup_accessors
from app.store.crm.accessor import CrmAccessor
from app.web.config import Config, setup_config
from app.web.middlewares import setup_middlewares
from app.web.routes import setup_routes


class Application(AiohttpApplication):  # создаем базу данных
    config: Optional[Config] = None # добавляем конфигурацию для авторизации
    database: dict = {}
    crm_accessor: Optional[CrmAccessor]


class Request(AiohttpRequest):
    @property
    def app(self) -> "Application":
        return super().app()


class View(AiohttpView): # создаем нашу View что бы были подсказки
    @property
    def request(self) -> Request:
        return super().request


app = Application()


def run_app():
    setup_config(app) # конфигурация авторизации из файла config.yaml
    setup_routes(app) # устанавивает пути нашего приложения и свяхывает с вью
    # CRM Application заголовок для нашей документации, url путь, swagger_path генерация документации что бы другим
    # програмистом было удобно работать с мои api
    setup_aiohttp_apispec(app, title='CRM Application', url='/docs/json', swagger_path='/docs')
    # включаем мидл вар который обрабатывает ошбки
    setup_middlewares(app)
    setup_accessors(app) # работает с базами данных
    aiohttp_run_app(app) # запуск приложения
