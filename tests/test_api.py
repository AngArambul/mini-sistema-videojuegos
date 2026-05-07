import unittest, json
from app import app, db
from models import Juego

class APITestCase(unittest.TestCase):
    # Configuramos la app para testing y usamos una base de datos en memoria
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        
        self.client = app.test_client()
        self.ctx = app.app_context()
        self.ctx.push()
        db.create_all()
        
        # Agregamos un juego de prueba a la base de datos
        db.session.add(Juego(titulo='X', genero='Y', plataforma='Switch'))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_get_juegos(self):
        # Hacemos la petición GET a la API
        resp = self.client.get('/api/juegos')
        data = json.loads(resp.data)
        
        # Verificamos código 200 y que la respuesta sea una lista
        self.assertEqual(resp.status_code, 200)
        self.assertIsInstance(data, list)

if __name__ == '__main__':
    unittest.main()