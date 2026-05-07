from database import db
from models import Juego

# Sirve para consultar todos los registros de la tabla usando el ORM
def obtener_juegos():
    return Juego.query.all()

# Sirve para crear un nuevo objeto Juego y guardarlo en la base de datos
def insertar_juego(titulo, genero, plataforma):
    nuevo_juego = Juego(titulo=titulo, genero=genero, plataforma=plataforma)
    db.session.add(nuevo_juego)
    db.session.commit()

# Sirve para buscar un juego por su ID y eliminarlo si existe
def eliminar_juego(id_juego):
    juego = Juego.query.get(id_juego)
    if juego:
        db.session.delete(juego)
        db.session.commit()