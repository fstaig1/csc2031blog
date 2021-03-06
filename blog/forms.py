from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import Required, Email


class PostForm(FlaskForm):
    title = StringField(validators=[Required()])
    body = TextAreaField(validators=[Required()])
    submit = SubmitField()


class LoginForm(FlaskForm):
    username = StringField(validators=[Required(), Email()])
    password = PasswordField(validators=[Required()])
    pinkey = StringField(validators=[Required()])
    recaptcha = RecaptchaField()
    submit = SubmitField()

