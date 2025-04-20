from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms.fields import IntegerField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class CreatingWishForm(FlaskForm):
    name = StringField("Название", validators=[DataRequired()])
    description = TextAreaField("Описание")
    link = StringField("Ссылка")
    image = FileField("Фото подарка", validators=[FileAllowed(["jpg", "jpeg", "png", "gif"], "Только изображения!")])
    price = IntegerField("Цена")
    submit = SubmitField("Добавить")
