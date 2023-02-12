import typing
import uuid
from typing import Optional

from app.crm.models import User

if typing.TYPE_CHECKING:
    from app.web.app import Application


class CrmAccessor:
    def __init__(self):
        self.app: Optional["Application"] = None # app либо N one либо Application

    async def connect(self, app: "Application"):# асинхронные методы connect, здесь смодем добавить подключение к базе данных
        self.app = app
        if not self.app.database.get("users"): # если нет пользователей
            self.app.database["users"] = []# тогда создадим их
            print('connect to database')

    async def disconnect(self, app: "Application"): # асинхронный метод дисконект може безопасно отключиться
        self.app = None
        print('disconnect from database')

    async def add_user(self, user: User): # добавление пользоваеля
        self.app.database["users"].append(user)


    async def list_users(self) -> list[User]: # получаем массив с пользователями
        return self.app.database["users"]

    async def get_user(self, id_: uuid.UUID) -> Optional[User]:
        for user in self.app.database["users"]:
            if user.id_ == id_:
                return user
        return None