from database import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
# Este archivo define los modelos de datos para la aplicación, utilizando SQLAlchemy como ORM.
class User(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(256))

    @property
    def password(self):
        raise AttributeError('La contraseña es de solo escritura')

    @password.setter
    def password(self, pwd):
        self.password_hash = generate_password_hash(pwd)

    def verify_password(self, pwd):
        return check_password_hash(self.password_hash, pwd)
# Modelo para representar un videojuego en la base de datos, con campos para título, género y plataforma.
class Juego(db.Model):
    __tablename__ = 'juegos'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False, unique=True)
    genero = db.Column(db.String(50), nullable=False)
    plataforma = db.Column(db.Enum('PlayStation', 'Xbox', 'Switch', 'PC', 'Dispositivos Móviles', 'Plataformas de Nube', 'Multiplataforma'), nullable=False)