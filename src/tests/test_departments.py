from flask import url_for
from datetime import datetime, date
import pytest


def _register_department(testapp, **kwargs):
    return testapp.post_json(url_for("api.create_student"), {
        "name": "physics",
        "budget": 2000000,
        "start_date": date(1967, 1, 2),
        "instructor_id": 1
    }, **kwargs)


def _get_departments(testapp, **kwargs):
    return testapp.get(url_for('api.get_departments'), **kwargs)


def _get_department(testapp, id, **kwargs):
    return testapp.get(url_for('api.get_department', id=id), **kwargs)


@pytest.mark.usefixtures('db')
class TestDepartments:

    def test_response_headers(self, testapp, department):
        resp = _get_departments(testapp)
        assert resp.headers['Content-Type'] == 'application/json'

    def test_get_departments(self, testapp, department):
        resp = testapp.get(url_for('api.get_departments'))
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'application/json'
        assert len(resp.json['items']) is not None

    def test_get_department(self, testapp, department):
        resp = _get_department(testapp, 1)
        assert resp.status_code == 200
        assert resp.json['id'] is not None
        assert resp.json['name'] is not None
        assert resp.json['budget'] is not None
        assert resp.json['instructor_id'] is not None

    def test_create_department(self, testapp, token):
        create_resp = testapp.post_json(url_for('api.create_department'), {
            "name": "English",
            "budget": 2000000,
            "instructor_id": 1
        }, headers={
            'Authorization': 'Bearer {}'.format(token)
        })
        assert create_resp.status_code == 201
        assert create_resp.json['id'] == 1

    def test_update_department(self, testapp, department, token):
        update_resp = testapp.put_json(url_for('api.update_department', id=1), {
            "name": "Political Science",
            "budget": 2000000,
            "instructor_id": 2
        }, headers={
            'Authorization': 'Bearer {}'.format(token)
        })

        assert update_resp.status_code == 204
        get_resp = _get_department(testapp, 1)
        assert get_resp.json['id'] == 1
        assert get_resp.json['name'] == "Political Science"
        assert get_resp.json['instructor_id'] == 2

    def test_delete_departments(self, testapp, department, token):
        delete_resp = testapp.delete(url_for('api.delete_department', id=1), headers={
            'Authorization': 'Bearer {}'.format(token)
        })

        assert delete_resp.status_code == 204

    def test_empty_create_department(self, testapp, department, token):
        create_resp = testapp.post_json(url_for('api.create_department'), {
        }, headers={
            'Authorization': 'Bearer {}'.format(token)
        }, expect_errors=True)

        assert create_resp.status_code == 400

    def test_empty_update_department(self, testapp, department, token):
        update_resp = testapp.put_json(url_for('api.update_department', id=1), {
        }, headers={
            'Authorization': 'Bearer {}'.format(token)
        }, expect_errors=True)
        assert update_resp.status_code == 400

    def test_404_department(self, testapp, department):
        resp = _get_department(testapp, 422, expect_errors=True)
        assert resp.status_code == 404
