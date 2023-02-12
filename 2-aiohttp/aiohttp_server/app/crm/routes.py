# сущность котора похволяет нам связать ссылку с тем местом куда нужно передать

import typing

if typing.TYPE_CHECKING: # если идет проверка типов то импортируем для того что бы application брался наш а не из aiohttp

    from app.web.app import Application


# def setup_routes(app: Application):
#     app.router.add_get('/index', index)  # переход на страницу индекс и вызываем функцию index

def setup_routes(app: "Application"):
    from app.crm.views import AddUserView # если сюда не всавить будет циклично работать и выдаст ошибку
    from app.crm.views import ListUsersView
    from app.crm.views import GetUserView

    app.router.add_view("/add_user", AddUserView)
    app.router.add_view("/list_users", ListUsersView)
    app.router.add_view("/get_user", GetUserView)
