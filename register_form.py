from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class RegisterModel(FlaskForm):
    user_name = StringField('Логин:', validators=[DataRequired()])
    password = PasswordField('Пароль:', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')
