from flask_testing import TestCase
from flask import current_app, url_for

from main import app

class MainTest(TestCase):
    def create_app(self):
        app.config['TESTING'] = True # Indicando le a flask que esta en ambiente testing
        app.config['WTF_CSRF_ENABLED'] = False # Desabilita CSRF o tokens de las formas
        return app

    def test_app_exists(self):
        """Testea que la app exista"""
        self.assertIsNotNone(current_app)
    
    def test_app_in_test_mode(self):
        """Testea que la app este en modo Testing"""
        self.assertTrue(current_app.config['TESTING'])

    def test_index_redirects(self):
        response = self.client.get(url_for('index'))

        self.assertRedirects(response, url_for('hello'))

    def test_hello_get(self):
        """Se testea que 'hello' regrese un 200"""
        response = self.client.get(url_for('hello'))
        self.assert200(response)

    def test_hello_post(self):
        """Testea el formulario de 'wtform'"""
        #fake_form = {
        #    'username': 'fake',
        #    'password': 'fake-password'
        #}
        response = self.client.post(url_for('hello'))

        self.assertTrue(response.status_code, 405)

    def test_auth_blueprint_exists(self):
        """Se prueba que el blueprint de 'auth' existe"""
        self.assertIn('auth', self.app.blueprints)

    def test_auth_login_get(self):
        """Se prueba que el 'auth.login' regresa un 200"""
        response = self.client.get(url_for('auth.login'))

        self.assert200(response)

    def test_auth_login_template(self):
            """Se prueba que el 'auth.login' renderiza el template 'login.html'"""
            self.client.get(url_for('auth.login'))

            self.assertTemplateUsed('login.html')

    def test_auth_login_post(self):
        fake_form = {
            'username': 'fake',
            'password': 'fake-password'
        }

        response = self.client.post(url_for('auth.login'), data = fake_form)

        self.assertRedirects(response, url_for('index'))