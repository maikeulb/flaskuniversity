import pytest
from flask import url_for


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
        assert resp.status_code == 200

    def test_user_revoke_token(self, testapp):
        _register_user(testapp)
        testapp.authorization = ('Basic', ('demo', 'P@ssw0rd!'))
        resp = testapp.post_json(url_for("api.get_token"))
        token = str(resp.json['token'])
        del_resp = testapp.delete(url_for('api.revoke_token'), headers={
            'Authorization': 'Bearer {}'.format(token)
        })
        assert del_resp.status_code == 204

    def test_user_wrong_token(self, testapp):
        _register_user(testapp)
        testapp.authorization = ('Basic', ('demo', 'P@ssw0rd!'))
        resp = testapp.post_json(url_for("api.get_token"))
        token = str(resp.json['token'])
        del_resp = testapp.delete(url_for('api.revoke_token'), headers={
            'Authorization': 'Bearer {}'.format('nottherighttoken')
        }, expect_errors=True)
        assert del_resp.status_code == 401
