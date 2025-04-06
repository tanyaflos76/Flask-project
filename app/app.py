import os
from pathlib import Path

from dishka import make_container
from dishka.integrations.flask import FlaskProvider, setup_dishka
from flask import Flask

from app.core.dependencies.flask import provider
from app.routers.router import router


def app() -> Flask:
    base_dir = Path(__file__).resolve().parent.parent
    template_dir = base_dir / "app" / "templates"
    app = Flask(__name__, template_folder=template_dir)
    app.register_blueprint(router)
    container = make_container(provider, FlaskProvider())
    setup_dishka(container=container, app=app, auto_inject=True)

    return app
