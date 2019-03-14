from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SubmitField
from wtforms.validators import DataRequired


class BooksForm(FlaskForm):
    title = StringField('Название и автор', validators=[DataRequired()])
    content = TextAreaField("Аннотация", validators=[DataRequired()])
    year = StringField('Год написания', validators=[DataRequired()])
    submit = SubmitField('Добавить')
