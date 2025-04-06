from flask import Blueprint, render_template


router = Blueprint("router", __name__)


@router.route("/")
def read_root():
    return render_template("index.html", name="World")


@router.route("/<name>")
def read_item(name: str):
    return render_template("index.html", name=name)
