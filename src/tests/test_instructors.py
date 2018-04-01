from flask import url_for
from datetime import datetime
import pytest


def _register_user(testapp, **kwargs):
    return testapp.post_json(url_for("api.create_user"), {
        "username": "demo",
        "email": "demo@example.com",
        "password": "P@ssw0rd!"
    }, **kwargs)


def _get_instructors(testapp, **kwargs):
    return testapp.get(url_for('api.get_instructors'), **kwargs)


def _get_instructor(testapp, id, **kwargs):
    return testapp.get(url_for('api.get_instructor', id=id), **kwargs)


@pytest.mark.usefixtures('db')
class TestInstructors:

    def test_response_headers(self, testapp):
        resp = _get_instructors(testapp)
        assert resp.headers['Content-Type'] == 'application/json'

    def test_get_instructors(self, testapp):
        resp = testapp.get(url_for('api.get_instructors'))
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'application/json'
        assert len(resp.json['items']) is not None

    def test_get_instructor(self, testapp):
        _register_user(testapp)
        testapp.authorization = ('Basic', ('demo', 'P@ssw0rd!'))
        resp = testapp.post_json(url_for("api.get_token"))
        token = str(resp.json['token'])
        create_resp = testapp.post_json(url_for('api.create_instructor'), {
            "first_name": "Kim",
            "last_name": "Hyonny"
        }, headers={
            'Authorization': 'Bearer {}'.format(token)
        })
        get_resp = _get_instructor(testapp, 5)
        assert get_resp.status_code == 200
        assert get_resp.json['id'] == 5

    def test_create_instructor(self, testapp):
        _register_user(testapp)
        testapp.authorization = ('Basic', ('demo', 'P@ssw0rd!'))
        resp = testapp.post_json(url_for("api.get_token"))
        token = str(resp.json['token'])
        create_resp = testapp.post_json(url_for('api.create_instructor'), {
            "first_name": "Kim",
            "last_name": "Hyonny"
        }, headers={
            'Authorization': 'Bearer {}'.format(token)
        })
        assert create_resp.status_code == 201
        assert create_resp.json['id'] == 5

    def test_update_instructor(self, testapp):
        _register_user(testapp)
        testapp.authorization = ('Basic', ('demo', 'P@ssw0rd!'))
        resp = testapp.post_json(url_for("api.get_token"))
        token = str(resp.json['token'])

        testapp.post_json(url_for('api.create_instructor'), {
            "first_name": "Kim",
            "last_name": "Hyonny"
        }, headers={
            'Authorization': 'Bearer {}'.format(token)
        })

        update_resp = testapp.put_json(url_for('api.update_instructor', id=5), {
            "first_name": "Tara",
            "last_name": "Wong"
        }, headers={
            'Authorization': 'Bearer {}'.format(token)
        })

        assert update_resp.status_code == 204
        get_resp = _get_instructor(testapp, 5)
        assert get_resp.json['id'] == 5
        assert get_resp.json['first_name'] == "Tara"
        assert get_resp.json['last_name'] == "Wong"

    def test_delete_instructors(self, testapp):
        _register_user(testapp)
        testapp.authorization = ('Basic', ('demo', 'P@ssw0rd!'))
        resp = testapp.post_json(url_for("api.get_token"))
        token = str(resp.json['token'])

        testapp.post_json(url_for('api.create_instructor'), {
            "first_name": "Tara",
            "last_name": "Wong"
        }, headers={
            'Authorization': 'Bearer {}'.format(token)
        })

        delete_resp = testapp.delete(url_for('api.delete_instructor', id=5), headers={
            'Authorization': 'Bearer {}'.format(token)
        })

        assert delete_resp.status_code == 204

    def test_empty_create_instructor(self, testapp):
        _register_user(testapp)
        testapp.authorization = ('Basic', ('demo', 'P@ssw0rd!'))
        resp = testapp.post_json(url_for("api.get_token"))
        token = str(resp.json['token'])

        create_resp = testapp.post_json(url_for('api.create_instructor'), {
        }, headers={
            'Authorization': 'Bearer {}'.format(token)
        }, expect_errors=True)

        assert create_resp.status_code == 400

    def test_empty_update_instructor(self, testapp):
        _register_user(testapp)
        testapp.authorization = ('Basic', ('demo', 'P@ssw0rd!'))
        resp = testapp.post_json(url_for("api.get_token"))
        token = str(resp.json['token'])
        testapp.post_json(url_for('api.create_instructor'), {
            "first_name": "Tara",
            "last_name": "Wong"
        }, headers={
            'Authorization': 'Bearer {}'.format(token)
        })
        update_resp = testapp.put_json(url_for('api.update_instructor', id=5), {
        }, headers={
            'Authorization': 'Bearer {}'.format(token)
        }, expect_errors=True)
        assert update_resp.status_code == 400

    def test_404_instructor(self, testapp):
        resp = _get_instructor(testapp, 422, expect_errors=True)
        assert resp.status_code == 404
