from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class AddNewsForm(FlaskForm):
    title = StringField('Название заметки', validators=[DataRequired()])
    content = TextAreaField('Текст заметки', validators=[DataRequired()])
    submit = SubmitField('Добавить')
