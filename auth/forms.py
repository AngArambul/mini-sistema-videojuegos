from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Length
# Este archivo define los formularios de registro e inicio de sesión para la aplicación, utilizando Flask-WTF y WTForms.
class RegistrationForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[
        DataRequired(), 
        EqualTo('password', message='Las contraseñas deben coincidir')
    ])
    submit = SubmitField('Registrarse')
# Formulario de inicio de sesión con campos para usuario, contraseña y opción de "Recordarme".
class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recordarme')
    submit = SubmitField('Iniciar Sesión')