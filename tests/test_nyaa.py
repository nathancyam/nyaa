import os
import unittest
import tempfile
import flask
from flask.testing import FlaskClient as BaseFlaskClient
from flask_wtf.csrf import generate_csrf
from nyaa import app, db


# Flask's assumptions about an incoming request don't quite match up with
# what the test client provides in terms of manipulating cookies, and the
# CSRF system depends on cookies working correctly. This little class is a
# fake request that forwards along requests to the test client for setting
# cookies.
class RequestShim(object):
    """
    A fake request that proxies cookie-related methods to a Flask test client.
    """
    def __init__(self, client):
        self.client = client

    def set_cookie(self, key, value='', *args, **kwargs):
        "Set the cookie on the Flask test client."
        server_name = flask.current_app.config["SERVER_NAME"] or "localhost"
        return self.client.set_cookie(
            server_name, key=key, value=value, *args, **kwargs
        )

    def delete_cookie(self, key, *args, **kwargs):
        "Delete the cookie on the Flask test client."
        server_name = flask.current_app.config["SERVER_NAME"] or "localhost"
        return self.client.delete_cookie(
            server_name, key=key, *args, **kwargs
        )


# We're going to extend Flask's built-in test client class, so that it knows
# how to look up CSRF tokens for you!
class FlaskClient(BaseFlaskClient):
    @property
    def csrf_token(self):
        # First, we'll wrap our request shim around the test client, so that
        # it will work correctly when Flask asks it to set a cookie.
        request = RequestShim(self)
        # Next, we need to look up any cookies that might already exist on
        # this test client, such as the secure cookie that powers `flask.session`,
        # and make a test request context that has those cookies in it.
        environ_overrides = {}
        self.cookie_jar.inject_wsgi(environ_overrides)
        with flask.current_app.test_request_context(
                "/login", environ_overrides=environ_overrides,
        ):
            # Now, we call Flask-WTF's method of generating a CSRF token...
            csrf_token = generate_csrf()
            # ...which also sets a value in `flask.session`, so we need to
            # ask Flask to save that value to the cookie jar in the test
            # client. This is where we actually use that request shim we made!
            flask.current_app.save_session(flask.session, request)
            # And finally, return that CSRF token we got from Flask-WTF.
            return csrf_token

    # Feel free to define other methods on this test client. You can even
    # use the `csrf_token` property we just defined, like we're doing here!
    def login(self, email, password):
        return self.post("/login", data={
            'username': email,
            'password': password,
            "csrf_token": self.csrf_token,
        }, follow_redirects=True)

    def logout(self):
        return self.get("/logout", follow_redirects=True)


class NyaaTestCase(unittest.TestCase):

    def setUp(self):
        self.db, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True

        with app.app_context():
            app.test_client_class = FlaskClient
            self.app = app.test_client()
            db.create_all()

    def tearDown(self):
        os.close(self.db)

    def test_index_url(self):
        rv = self.app.get('/')
        assert b'Browse :: Nyaa' in rv.data
        assert b'Guest' in rv.data

    def test_upload_url(self):
        rv = self.app.get('/upload')
        assert b'Upload Torrent' in rv.data
        assert b'You are not logged in, and are uploading anonymously.' in rv.data

    def test_rules_url(self):
        rv = self.app.get('/rules')
        assert b'Site Rules' in rv.data

    def test_help_url(self):
        rv = self.app.get('/help')
        assert b'Using the Site' in rv.data

    def test_rss_url(self):
        rv = self.app.get('/?page=rss')
        assert b'/xmlns/nyaa' in rv.data

    def test_login_url(self):
        rv = self.app.get('/login')
        assert b'Username or email address' in rv.data

    def test_registration_url(self):
        rv = self.app.get('/register')
        assert b'Username' in rv.data
        assert b'Password' in rv.data

    def test_failed_login(self):
        with app.app_context():
            rv = self.app.login('test@example.com', 'fail')
            assert b'Incorrect' in rv.data

if __name__ == '__main__':
    unittest.main()
