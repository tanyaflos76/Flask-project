from pathlib import Path
from typing import Self

from dishka import make_container
from dishka.integrations.flask import FlaskProvider, setup_dishka
from flask import Flask
from flask_login import LoginManager
from sqlalchemy.orm import Session

from wishare.core.config import AppConfig
from wishare.core.dependencies.flask import provider
from wishare.lib.models.user import UserModel
from wishare.routers.router import router


BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = BASE_DIR / "app" / "templates"


class App:
    def __init__(self, config: AppConfig, app: Flask | None = None) -> None:
        self.config = config
        self.app = app or Flask(__name__, template_folder=TEMPLATE_DIR)
        self.login_manager = LoginManager()

        self.setup_app()

    @classmethod
    def from_env(cls) -> Self:
        return cls(AppConfig.from_env())

    def setup_app(self) -> None:
        self.app.register_blueprint(router)
        self.app.secret_key = self.config.security.token
        self.container = make_container(provider, FlaskProvider())

        self.login_manager.user_loader(self.load_user)
        self.login_manager.init_app(self.app)

        setup_dishka(container=self.container, app=self.app, auto_inject=True)

    def load_user(self, user_id: int):
        with self.container() as request_container:
            return request_container.get(Session).query(UserModel).get(user_id)


def app() -> Flask:
    return App.from_env().app
