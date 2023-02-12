import uuid
from dataclasses import dataclass


@dataclass # обычный клас в котром можем поставить атрибуты и не нужно как то обрамлять
class User:
    id_: uuid.UUID
    email: str
