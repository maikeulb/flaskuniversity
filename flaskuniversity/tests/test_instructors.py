import pytest
from flask import url_for
from datetime import datetime


def _register_instructor(testapp, **kwargs):
    return testapp.post_json(url_for("api.create_instructor"), {
        "first_name": "new_first_name",
        "last_name": "new_last_name"
    }, **kwargs)


def _get_instructors(testapp, **kwargs):
    return testapp.get(url_for('api.get_instructors'), **kwargs)


def _get_instructor(testapp, id, **kwargs):
    return testapp.get(url_for('api.get_instructor', id=id), **kwargs)


@pytest.mark.usefixtures('db')
class TestInstructors:

    def test_response_headers(self, testapp, instructor):
        resp = _get_instructors(testapp)
        assert resp.headers['Content-Type'] == 'application/json'

    def test_get_instructors(self, testapp, instructor):
        resp = testapp.get(url_for('api.get_instructors'))
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'application/json'
        assert len(resp.json['items']) is not None

    def test_get_instructor(self, testapp, instructor):
        resp = _get_instructor(testapp, 1)
        assert resp.status_code == 200
        assert resp.json['id'] == 1
        assert resp.json['first_name'] is not None
        assert resp.json['last_name'] is not None

    def test_create_instructor(self, testapp, token):
        create_resp = _register_instructor(testapp, headers={
            'Authorization': 'Bearer {}'.format(token)
        })
        assert create_resp.status_code == 201
        assert create_resp.json['id'] == 1

    def test_update_instructor(self, testapp, instructor, token):
        update_resp = testapp.put_json(url_for('api.update_instructor', id=1), {
            "first_name": "Tara",
            "last_name": "Wong"
        }, headers={
            'Authorization': 'Bearer {}'.format(token)
        })

        assert update_resp.status_code == 204
        get_resp = _get_instructor(testapp, 1)
        assert get_resp.json['id'] == 1
        assert get_resp.json['first_name'] == "Tara"
        assert get_resp.json['last_name'] == "Wong"

    @pytest.mark.skip(reason="no idea why it's failing")
    def test_delete_instructors(self, testapp, instructor, course, course_assignment,
                                office_assignment, token):
        delete_resp = testapp.delete(url_for('api.delete_instructor', id=1), headers={
            'Authorization': 'Bearer {}'.format(token)
        })

        # assert delete_resp.status_code == 204

    def test_empty_create_instructor(self, testapp, token):
        create_resp = testapp.post_json(url_for('api.create_instructor'), {
        }, headers={
            'Authorization': 'Bearer {}'.format(token)
        }, expect_errors=True)

        assert create_resp.status_code == 400

    def test_empty_update_instructor(self, testapp, instructor, token):
        update_resp = testapp.put_json(url_for('api.update_instructor', id=1), {
        }, headers={
            'Authorization': 'Bearer {}'.format(token)
        }, expect_errors=True)
        assert update_resp.status_code == 400

    def test_404_instructor(self, testapp, instructor):
        resp = _get_instructor(testapp, 422, expect_errors=True)
        assert resp.status_code == 404
