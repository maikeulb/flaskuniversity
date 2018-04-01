from flask import url_for
from datetime import datetime
import pytest


def _register_user(testapp, **kwargs):
    return testapp.post_json(url_for("api.create_user"), {
        "username": "demo",
        "email": "demo@example.com",
        "password": "P@ssw0rd!"
    }, **kwargs)

    name = db.Column(db.String)
    budget = db.Column(db.Numeric(8, 2))
    instructor_id = db.Column(db.Integer, db.ForeignKey('departments.id'))


def _get_departments(testapp, **kwargs):
    return testapp.get(url_for('api.get_departments'), **kwargs)


def _get_department(testapp, id, **kwargs):
    return testapp.get(url_for('api.get_department', id=id), **kwargs)


@pytest.mark.usefixtures('db')
class TestDepartments:

    def test_response_headers(self, testapp):
        resp = _get_departments(testapp)
        assert resp.headers['Content-Type'] == 'application/json'

    def test_get_departments(self, testapp):
        resp = testapp.get(url_for('api.get_departments'))
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'application/json'
        assert len(resp.json['items']) is not None

    def test_get_department(self, testapp):
        _register_user(testapp)
        testapp.authorization = ('Basic', ('demo', 'P@ssw0rd!'))
        resp = testapp.post_json(url_for("api.get_token"))
        token = str(resp.json['token'])
        create_resp = testapp.post_json(url_for('api.create_department'), {
            "name": "English",
            "budget": 2000000,
            "instructor_id": 1
        }, headers={
            'Authorization': 'Bearer {}'.format(token)
        })
        get_resp = _get_department(testapp, 3)
        assert get_resp.status_code == 200
        assert get_resp.json['id'] is not None
        assert get_resp.json['name'] is not None
        assert get_resp.json['budget'] is not None
        assert get_resp.json['instructor_id'] is not None

    def test_create_department(self, testapp):
        _register_user(testapp)
        testapp.authorization = ('Basic', ('demo', 'P@ssw0rd!'))
        resp = testapp.post_json(url_for("api.get_token"))
        token = str(resp.json['token'])
        create_resp = testapp.post_json(url_for('api.create_department'), {
            "name": "English",
            "budget": 2000000,
            "instructor_id": 1
        }, headers={
            'Authorization': 'Bearer {}'.format(token)
        })
        assert create_resp.status_code == 201
        assert create_resp.json['id'] == 3

    def test_update_department(self, testapp):
        _register_user(testapp)
        testapp.authorization = ('Basic', ('demo', 'P@ssw0rd!'))
        resp = testapp.post_json(url_for("api.get_token"))
        token = str(resp.json['token'])

        testapp.post_json(url_for('api.create_department'), {
            "name": "English",
            "budget": 2000000,
            "instructor_id": 1
        }, headers={
            'Authorization': 'Bearer {}'.format(token)
        })

        update_resp = testapp.put_json(url_for('api.update_department', id=3), {
            "name": "Political Science",
            "budget": 2000000,
            "instructor_id": 2
        }, headers={
            'Authorization': 'Bearer {}'.format(token)
        })

        assert update_resp.status_code == 204
        get_resp = _get_department(testapp, 3)
        print(get_resp)
        assert get_resp.json['id'] == 3
        assert get_resp.json['name'] == "Political Science"
        assert get_resp.json['instructor_id'] == 2

    def test_delete_departments(self, testapp):
        _register_user(testapp)
        testapp.authorization = ('Basic', ('demo', 'P@ssw0rd!'))
        resp = testapp.post_json(url_for("api.get_token"))
        token = str(resp.json['token'])

        testapp.post_json(url_for('api.create_department'), {
            "name": "English",
            "budget": 2000000,
            "instructor_id": 1
        }, headers={
            'Authorization': 'Bearer {}'.format(token)
        })

        delete_resp = testapp.delete(url_for('api.delete_department', id=3), headers={
            'Authorization': 'Bearer {}'.format(token)
        })

        assert delete_resp.status_code == 204

    def test_empty_create_department(self, testapp):
        _register_user(testapp)
        testapp.authorization = ('Basic', ('demo', 'P@ssw0rd!'))
        resp = testapp.post_json(url_for("api.get_token"))
        token = str(resp.json['token'])

        create_resp = testapp.post_json(url_for('api.create_department'), {
        }, headers={
            'Authorization': 'Bearer {}'.format(token)
        }, expect_errors=True)

        assert create_resp.status_code == 400

    def test_empty_update_department(self, testapp):
        _register_user(testapp)
        testapp.authorization = ('Basic', ('demo', 'P@ssw0rd!'))
        resp = testapp.post_json(url_for("api.get_token"))
        token = str(resp.json['token'])
        testapp.post_json(url_for('api.create_department'), {
            "name": "English",
            "budget": 2000000,
            "instructor_id": 1
        }, headers={
            'Authorization': 'Bearer {}'.format(token)
        })
        update_resp = testapp.put_json(url_for('api.update_department', id=3), {
        }, headers={
            'Authorization': 'Bearer {}'.format(token)
        }, expect_errors=True)
        assert update_resp.status_code == 400

    def test_404_department(self, testapp):
        resp = _get_department(testapp, 422, expect_errors=True)
        assert resp.status_code == 404
