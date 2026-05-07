from flask import Blueprint, request
from flask_restful import Api, Resource
from database import db
from models import Juego

# 1. Creamos el Blueprint para la API
api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# 2. Recurso para manejar toda la lista de juegos (GET general y POST)
class JuegoList(Resource):
    def get(self):
        juegos = Juego.query.all()
        # Serializamos: Convertimos los objetos Python a una lista de diccionarios (JSON)
        return [{'id': j.id, 'titulo': j.titulo, 'genero': j.genero, 'plataforma': j.plataforma} for j in juegos], 200

    def post(self):
        datos = request.get_json()
        nuevo_juego = Juego(
            titulo=datos['titulo'],
            genero=datos['genero'],
            plataforma=datos['plataforma']
        )
        db.session.add(nuevo_juego)
        db.session.commit()
        return {'mensaje': 'Juego creado', 'id': nuevo_juego.id}, 201

# 3. Recurso para manejar un juego específico (GET por ID, PUT y DELETE)
class JuegoResource(Resource):
    def get(self, id):
        juego = Juego.query.get_or_404(id)
        return {'id': juego.id, 'titulo': juego.titulo, 'genero': juego.genero, 'plataforma': juego.plataforma}, 200

    def put(self, id):
        juego = Juego.query.get_or_404(id)
        datos = request.get_json()
        
        juego.titulo = datos.get('titulo', juego.titulo)
        juego.genero = datos.get('genero', juego.genero)
        juego.plataforma = datos.get('plataforma', juego.plataforma)
        
        db.session.commit()
        return {'mensaje': 'Juego actualizado'}, 200

    def delete(self, id):
        juego = Juego.query.get_or_404(id)
        db.session.delete(juego)
        db.session.commit()
        return '', 204  # 204 No Content significa que se borró y no hay nada más que decir

# 4. Asignamos las rutas a las clases
api.add_resource(JuegoList, '/juegos')
api.add_resource(JuegoResource, '/juegos/<int:id>')