from flask import url_for
import pytest


def _register_user(testapp, **kwargs):
    return testapp.post_json(url_for("api.create_user"), {
        "username": "demo",
        "email": "demo@example.com",
        "password": "P@ssw0rd!"
    }, **kwargs)


@pytest.mark.usefixtures('db')
class TestAuthenticate:

    def test_register_user(self, testapp):
        resp = _register_user(testapp)
        assert resp.json['username'] == 'demo'

    def test_user_request_token(self, testapp):
        _register_user(testapp)
        testapp.authorization = ('Basic', ('demo', 'P@ssw0rd!'))
        resp = testapp.post_json(url_for("api.get_token"))
        assert resp.json['token'] is not None
