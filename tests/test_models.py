import unittest
from app import app, db
from models import Juego

class ModelTestCase(unittest.TestCase):
    def setUp(self):
        # Configuramos la app para testing y usamos una base de datos en memoria
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        
        self.ctx = app.app_context()
        self.ctx.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_juego_creation(self):
        # Creamos un nuevo juego y lo guardamos en la base de datos
        j = Juego(titulo='Test', genero='Desc', plataforma='PC')
        db.session.add(j)
        db.session.commit()
        
        # Verificamos que se haya guardado 1 juego
        self.assertEqual(Juego.query.count(), 1)

if __name__ == '__main__':
    unittest.main()