from flask import url_for
from datetime import datetime
import pytest


def _register_user(testapp, **kwargs):
    return testapp.post_json(url_for("api.create_user"), {
        "username": "demo",
        "email": "demo@example.com",
        "password": "P@ssw0rd!"
    }, **kwargs)


def _get_courses(testapp, **kwargs):
    return testapp.get(url_for('api.get_courses'), **kwargs)


def _get_course(testapp, id, **kwargs):
    return testapp.get(url_for('api.get_course', id=id), **kwargs)


@pytest.mark.usefixtures('db')
class TestCourses:

    def test_response_headers(self, testapp):
        resp = _get_course(testapp, 221)
        assert resp.headers['Content-Type'] == 'application/json'

    def test_get_courses(self, testapp):
        resp = testapp.get(url_for('api.get_courses'))
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'application/json'
        assert len(resp.json['items']) is not None

    def test_get_course(self, testapp):
        resp = _get_course(testapp, 221)
        assert resp.status_code == 200
        assert resp.json['id'] is not None
        assert resp.json['title'] is not None
        assert resp.json['credits'] is not None
        assert resp.json['department_id'] is not None

    def test_create_course(self, testapp):
        _register_user(testapp)
        testapp.authorization = ('Basic', ('demo', 'P@ssw0rd!'))
        resp = testapp.post_json(url_for("api.get_token"))
        token = str(resp.json['token'])
        create_resp = testapp.post_json(url_for('api.create_course'), {
            "id": 264,
            "title": "Algorithms",
            "credits": 5,
            "department_id": 1
        }, headers={
            'Authorization': 'Bearer {}'.format(token)
        })
        assert create_resp.status_code == 201
        assert create_resp.json['id'] == 264

    def test_update_course(self, testapp):
        _register_user(testapp)
        testapp.authorization = ('Basic', ('demo', 'P@ssw0rd!'))
        resp = testapp.post_json(url_for("api.get_token"))
        token = str(resp.json['token'])

        testapp.post_json(url_for('api.create_course'), {
            "id": 264,
            "title": "Algorithms",
            "credits": 5,
            "department_id": 1
        }, headers={
            'Authorization': 'Bearer {}'.format(token)
        })

        update_resp = testapp.put_json(url_for('api.update_course', id=264), {
            "id": 264,
            "title": "Databases",
            "credits": 3,
            "department_id": 1
        }, headers={
            'Authorization': 'Bearer {}'.format(token)
        })

        assert update_resp.status_code == 204
        get_resp = _get_course(testapp, 264)
        assert get_resp.json['id'] == 264
        assert get_resp.json['title'] == "Databases"
        assert get_resp.json['credits'] == 3
        assert get_resp.json['department_id'] == 1

    def test_delete_courses(self, testapp):
        _register_user(testapp)
        testapp.authorization = ('Basic', ('demo', 'P@ssw0rd!'))
        resp = testapp.post_json(url_for("api.get_token"))
        token = str(resp.json['token'])

        testapp.post_json(url_for('api.create_course'), {
            "id": 264,
            "title": "Algorithms",
            "credits": 5,
            "department_id": 1
        }, headers={
            'Authorization': 'Bearer {}'.format(token)
        })

        delete_resp = testapp.delete(url_for('api.delete_course', id=264), headers={
            'Authorization': 'Bearer {}'.format(token)
        })

        assert delete_resp.status_code == 204

    def test_empty_create_course(self, testapp):
        _register_user(testapp)
        testapp.authorization = ('Basic', ('demo', 'P@ssw0rd!'))
        resp = testapp.post_json(url_for("api.get_token"))
        token = str(resp.json['token'])

        create_resp = testapp.post_json(url_for('api.create_course'), {
        }, headers={
            'Authorization': 'Bearer {}'.format(token)
        }, expect_errors=True)

        assert create_resp.status_code == 400

    def test_empty_update_course(self, testapp):
        _register_user(testapp)
        testapp.authorization = ('Basic', ('demo', 'P@ssw0rd!'))
        resp = testapp.post_json(url_for("api.get_token"))
        token = str(resp.json['token'])
        testapp.post_json(url_for('api.create_course'), {
            "id": 264,
            "title": "Algorithms",
            "credits": 5,
            "department_id": 1
        }, headers={
            'Authorization': 'Bearer {}'.format(token)
        })
        update_resp = testapp.put_json(url_for('api.update_course', id=264), {
        }, headers={
            'Authorization': 'Bearer {}'.format(token)
        }, expect_errors=True)
        assert update_resp.status_code == 400

    def test_404_course(self, testapp):
        resp = _get_course(testapp, 422, expect_errors=True)
        assert resp.status_code == 404
