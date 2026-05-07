import unittest
from app import app, db

class RoutesTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        
        self.client = app.test_client()
        self.ctx = app.app_context()
        self.ctx.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_index_access(self):
        # Verificamos que la página de inicio sea accesible (Código 200)
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_profile_requires_login(self):
        # Verificamos que al intentar entrar al perfil te redirija (Código 302)
        resp = self.client.get('/profile')
        self.assertEqual(resp.status_code, 302)
        self.assertIn('/auth/login', resp.headers['Location'])

if __name__ == '__main__':
    unittest.main()