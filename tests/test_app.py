import os
import json
import app.app as app
import unittest
import tempfile

class FlaskAlchemyTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()
        with app.app.app_context():
            app.db.create_all()

    def test_ping(self):
        req = self.app.get('/api/v1/ping')
        self.assertEqual(b'PONG', req.data)

    def test_create_user(self):
        req = self.app.post('/api/v1/user',
                            data=json.dumps(dict(username='foo', ip=123456)),
                            content_type='application/json')
        self.assertEqual(req.status_code, 200)
        self.assertEqual(req.data, b'DONE')

    def tearDown(self):
        os.close(self.db_fd)
        app.db.close()
        os.unlink(app.app.config['DATABASE'])

if __name__ == '__main__':
    unittest.main()
