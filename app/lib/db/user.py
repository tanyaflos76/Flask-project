from sqlalchemy.orm import Session

from app.lib.forms.user import RegisterForm
from app.lib.models.user import UserModel


def get_user_by_email(db: Session, email: str | None):
    return db.query(UserModel).filter(UserModel.email == email).first()


def create_user(db: Session, form: RegisterForm):
    user = UserModel(
        username=form.name.data,
        email=form.email.data,
    )
    user.set_password(form.password.data)
    db.add(user)
    db.flush()
