from flask_wtf import FlaskForm
from wtforms.fields import FileField, IntegerField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class CreatingWishForm(FlaskForm):
    name = StringField("Название", validators=[DataRequired()])
    description = TextAreaField("Описание")
    image = FileField("Фото подарка")
    price = IntegerField("Цена")
    submit = SubmitField("Добавить")
