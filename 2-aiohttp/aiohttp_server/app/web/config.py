import typing
from dataclasses import dataclass

import yaml

if typing.TYPE_CHECKING:
    from app.web.app import Application


@dataclass
class Config: # в нем будут содержаться только данные
    username: str
    password: str


def setup_config(app: "Application"):# при загрузке  приложения нам нужно конфиг чем-то заполнить
    with open("./config/config.yaml", "r") as f: # нужно взять и считать этот yaml файл
        raw_config = yaml.safe_load(f) # здесь будет словарь из файла config.yaml

    app.config = Config(
        username=raw_config["credentials"]["username"],
        password=raw_config["credentials"]["password"]
    )
