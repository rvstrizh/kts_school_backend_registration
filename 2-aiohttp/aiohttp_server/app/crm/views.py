import uuid

from aiohttp.web_exceptions import HTTPNotFound, HTTPUnauthorized, HTTPForbidden
from aiohttp_apispec import docs, request_schema, response_schema, querystring_schema

from app.crm.models import User
from app.crm.schemes import ListUsersResponseSchema, UserGetRequestSchema, UserGetResponseSchema, \
    UserAddSchema, UserSchema
from app.web.app import View
from app.web.schemes import OkResponseSchema
from app.web.utils import json_response, check_basic_auth


class AddUserView(View):  # наследуемся от нашего View
    # все декораторы представляют собой валидацию
    @docs(tags=['crm'], summery='Add new user', description='Add new user to database') # добавляем документацию summery- общее описание метода
    @request_schema(UserAddSchema) # добавляется маршмеллоу схема
    @response_schema(OkResponseSchema, 200) # как мы будем отвеать на наш запрос
    async def post(self):
        # self.request.app.database # берет данные из нашего database
        # data = await self.request.json() без валилации# получаем данные в формате json, await асинхронность данных этих запросов
        data = self.request['data'] # когда прошла валидация
        print(data)
        user = User(email=data['email'], id_=uuid.uuid4()) # создаем пользователя
        await self.request.app.crm_accessor.add_user(user)
        return json_response()


class ListUsersView(View): # получаем список пользователей
    @docs(tags=['crm'], summery='List users', description='List users from database') # добавляем документацию summery- общее описание метода
    # request_schema у на нет так как ничего не приходит
    @response_schema(ListUsersResponseSchema, 200) # как мы будем отвеать на наш запрос
    async def get(self):
        if not self.request.headers.get("Authorization"): # если нет заголовка Authorization
            raise HTTPUnauthorized # нет авторизации 401
        if not check_basic_auth(self.request.headers["Authorization"], username=self.request.app.config.username, password=self.request.app.config.password):
            raise HTTPForbidden # 403
        users = await self.request.app.crm_accessor.list_users()
        # преобразовываем пользователей к нормальному виду который потом можем перевести в json
        raw_users =  [UserSchema().dump(user) for user in users]
        return json_response(data={'users': raw_users})


class GetUserView(View): # получаем пользователя через id
    @docs(tags=['crm'], summery='Get user',
          description='Get user from database')  # добавляем документацию summery- общее описание метода
    # request только к json данным относится, если передаем в query параметрах нужно querystring_schema
    @querystring_schema(UserGetRequestSchema)
    @response_schema(UserGetResponseSchema, 200)  # как мы будем отвеать на наш запрос
    async def get(self):
        # базовая авторизация
        if not self.request.headers.get("Authorization"): # если нет заголовка Authorization
            raise HTTPUnauthorized # нет авторизации 401
        if not check_basic_auth(self.request.headers["Authorization"], username=self.request.app.config.username, password=self.request.app.config.password):
            raise HTTPForbidden # 403
        # print(self.request.app.config.username) # выдавст имя в файле config.yaml
        user_id = self.request.query["id"]
        user = await self.request.app.crm_accessor.get_user(uuid.UUID(user_id))
        if user:
            # return json_response(data={'user': {'email': user.email, 'id': str(user.id_)}}) было
            return json_response(data={'user': UserSchema().dump(user)}) # стало
        else:
            raise HTTPNotFound
