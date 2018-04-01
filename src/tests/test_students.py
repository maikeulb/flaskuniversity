from flask import url_for
from datetime import datetime
import pytest


def _register_user(testapp, **kwargs):
    return testapp.post_json(url_for("api.create_user"), {
        "username": "demo",
        "email": "demo@example.com",
        "password": "P@ssw0rd!"
    }, **kwargs)


def _get_students(testapp, **kwargs):
    return testapp.get(url_for('api.get_students'), **kwargs)


def _get_student(testapp, id, **kwargs):
    return testapp.get(url_for('api.get_student', id=id), **kwargs)


@pytest.mark.usefixtures('db')
class TestStudents:

    def test_response_headers(self, testapp):
        resp = _get_students(testapp)
        assert resp.headers['Content-Type'] == 'application/json'

    def test_get_students(self, testapp):
        resp = testapp.get(url_for('api.get_students'))
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'application/json'
        assert len(resp.json['items']) is not None

    def test_get_student(self, testapp):
        resp = _get_student(testapp, 1)
        assert resp.status_code == 200
        assert resp.json['id'] == 1

    def test_create_student(self, testapp):
        _register_user(testapp)
        testapp.authorization = ('Basic', ('demo', 'P@ssw0rd!'))
        resp = testapp.post_json(url_for("api.get_token"))
        token = str(resp.json['token'])
        create_resp = testapp.post_json(url_for('api.create_student'), {
            "first_name": "Jack",
            "last_name": "Smith"
        }, headers={
            'Authorization': 'Bearer {}'.format(token)
        })
        assert create_resp.status_code == 201
        assert create_resp.json['id'] == 15

    def test_update_student(self, testapp):
        _register_user(testapp)
        testapp.authorization = ('Basic', ('demo', 'P@ssw0rd!'))
        resp = testapp.post_json(url_for("api.get_token"))
        token = str(resp.json['token'])

        testapp.post_json(url_for('api.create_student'), {
            "first_name": "Jack",
            "last_name": "Smith"
        }, headers={
            'Authorization': 'Bearer {}'.format(token)
        })

        update_resp = testapp.put_json(url_for('api.update_student', id=15), {
            "first_name": "Kyle",
            "last_name": "Reese"
        }, headers={
            'Authorization': 'Bearer {}'.format(token)
        })

        assert update_resp.status_code == 204
        get_resp = _get_student(testapp, 15)
        assert get_resp.json['id'] == 15
        assert get_resp.json['first_name'] == "Kyle"
        assert get_resp.json['last_name'] == "Reese"

    def test_delete_students(self, testapp):
        _register_user(testapp)
        testapp.authorization = ('Basic', ('demo', 'P@ssw0rd!'))
        resp = testapp.post_json(url_for("api.get_token"))
        token = str(resp.json['token'])

        testapp.post_json(url_for('api.create_student'), {
            "first_name": "Jack",
            "last_name": "Smith"
        }, headers={
            'Authorization': 'Bearer {}'.format(token)
        })

        delete_resp = testapp.delete(url_for('api.delete_student', id=15), headers={
            'Authorization': 'Bearer {}'.format(token)
        })

        assert delete_resp.status_code == 204

    def test_empty_create_student(self, testapp):
        _register_user(testapp)
        testapp.authorization = ('Basic', ('demo', 'P@ssw0rd!'))
        resp = testapp.post_json(url_for("api.get_token"))
        token = str(resp.json['token'])

        create_resp = testapp.post_json(url_for('api.create_student'), {
        }, headers={
            'Authorization': 'Bearer {}'.format(token)
        }, expect_errors=True)

        assert create_resp.status_code == 400

    def test_empty_update_student(self, testapp):
        _register_user(testapp)
        testapp.authorization = ('Basic', ('demo', 'P@ssw0rd!'))
        resp = testapp.post_json(url_for("api.get_token"))
        token = str(resp.json['token'])
        testapp.post_json(url_for('api.create_student'), {
            "first_name": "Jack",
            "last_name": "Smith"
        }, headers={
            'Authorization': 'Bearer {}'.format(token)
        })
        update_resp = testapp.put_json(url_for('api.update_student', id=15), {
        }, headers={
            'Authorization': 'Bearer {}'.format(token)
        }, expect_errors=True)
        assert update_resp.status_code == 400

    def test_404_student(self, testapp):
        resp = _get_student(testapp, 422, expect_errors=True)
        assert resp.status_code == 404
