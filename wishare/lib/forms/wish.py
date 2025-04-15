from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired


class CreatingWishForm(FlaskForm):
    name = StringField("Название", validators=[DataRequired()])
    description = TextAreaField("Описание")
    link = StringField("Ссылка, где можно купить")
    price = IntegerField("Цена")
    submit = SubmitField("Добавить")
