from pathlib import Path

from dishka import make_container
from dishka.integrations.flask import FlaskProvider, setup_dishka
from flask import Flask
from flask_login import LoginManager
from sqlalchemy.orm import Session

from app.core.dependencies.flask import provider
from app.lib.models.user import UserModel
from app.routers.router import router


def app() -> Flask:
    base_dir = Path(__file__).resolve().parent.parent
    template_dir = base_dir / "app" / "templates"

    app = Flask(__name__, template_folder=template_dir)
    app.register_blueprint(router)
    # TODO: move to envs
    app.secret_key = "lol"

    container = make_container(provider, FlaskProvider())

    def load_user(user_id: int):
        with container() as request_container:
            return request_container.get(Session).query(UserModel).get(user_id)

    login_manager = LoginManager()
    login_manager.user_loader(load_user)
    login_manager.init_app(app)

    setup_dishka(container=container, app=app, auto_inject=True)

    return app
