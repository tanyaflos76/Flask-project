from flask import Blueprint, render_template

from .user import router as user_router
from .wish_list import router as wish_list_router


router = Blueprint("router", __name__)


@router.route("/")
def index():
    return render_template("start_window.html")


for i in [
    user_router,
    wish_list_router,
]:
    router.register_blueprint(i)
