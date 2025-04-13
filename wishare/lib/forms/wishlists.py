from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.simple import BooleanField, TextAreaField
from wtforms.validators import DataRequired


class CreatingListForm(FlaskForm):
    title = StringField("Название", validators=[DataRequired()])
    description = TextAreaField("Описание/свои комментарии")
    is_public = BooleanField("Могут видеть все")
    submit = SubmitField("Сохранить")
