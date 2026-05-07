from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
# Este archivo define el formulario para agregar un nuevo juego, utilizando Flask-WTF y WTForms.
class JuegoForm(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired()])
    genero = StringField('Género', validators=[DataRequired()])
    plataforma = SelectField('Plataforma', choices=[
        ('', '--- Selecciona una plataforma ---'),
        ('PlayStation', 'PlayStation'),
        ('Xbox', 'Xbox'),
        ('Switch', 'Switch'),
        ('PC', 'PC'),
        ('Dispositivos Móviles', 'Dispositivos Móviles'),
        ('Plataformas de Nube', 'Plataformas de Nube'),
        ('Multiplataforma', 'Multiplataforma')
    ], validators=[DataRequired(message="Debes seleccionar una opción")])
    submit = SubmitField('Agregar')