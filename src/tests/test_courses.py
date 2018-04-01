from flask import url_for
from datetime import datetime
import pytest


# def _get_courses(testapp, **kwargs):
#     return testapp.get(url_for('api.get_courses'), **kwargs)


# def _get_course(testapp, id, **kwargs):
#     return testapp.get(url_for('api.get_course', id=id), **kwargs)


# def _post_course(testapp, name, **kwargs):
#     return testapp.post_json(url_for('api.create_course'), {
#         "name": name
#     }, **kwargs)


# def _put_course(testapp, name, id, **kwargs):
#     return testapp.put_json(url_for('api.update_course', id=id), {
#         "name": name
#     }, **kwargs)


# def _patch_course(testapp, name, id, **kwargs):
#     return testapp.patch_json(url_for('api.partial_update_course', id=id), {
#         "name": name
#     }, **kwargs)


# def _delete_course(testapp, id, **kwargs):
#     return testapp.delete(url_for('api.delete_course', id=id), **kwargs)


# @pytest.mark.usefixtures('db')
# class TestCourses:

#     def test_response_headers(self, testapp):
#         _post_course(testapp, 'manhattan')
#         resp = _get_course(testapp, 1)
#         assert resp.headers['Content-Type'] == 'application/json'
#         multi_resp = _get_courses(testapp)
#         assert resp.headers['Content-Type'] == 'application/json'

#     def test_get_courses(self, testapp):
#         _post_course(testapp, 'manhattan')
#         _post_course(testapp, 'queens')
#         resp = testapp.get(url_for('api.get_courses'))
#         assert resp.status_code == 200
#         assert resp.headers['Content-Type'] == 'application/json'
#         assert resp.json['items'][0]['name'] == 'manhattan'
#         assert resp.json['items'][1]['name'] == 'queens'

#     def test_get_course(self, testapp):
#         _post_course(testapp, 'manhattan')
#         resp = _get_course(testapp, 1)
#         assert resp.status_code == 200
#         assert resp.json['id'] == 1

#     def test_create_course(self, testapp):
#         resp = _post_course(testapp, 'manhattan')
#         assert resp.status_code == 201
#         assert resp.json['id'] == 1
#         assert resp.json['name'] == 'manhattan'

#     def test_update_course(self, testapp):
#         _post_course(testapp, 'manhattan')
#         resp = _put_course(testapp, 'brooklyn', 1)
#         assert resp.status_code == 204
#         get_resp = _get_course(testapp, 1)
#         assert get_resp.json['name'] == 'brooklyn'

#     def test_partial_update_course(self, testapp):
#         _post_course(testapp, 'manhattan')
#         resp = _patch_course(testapp, 'brooklyn', 1)
#         assert resp.status_code == 204
#         get_resp = _get_course(testapp, 1)
#         assert get_resp.json['name'] == 'brooklyn'

#     def test_delete_courses(self, testapp):
#         _post_course(testapp, 'manhattan')
#         resp = _delete_course(testapp, 1)
#         assert resp.status_code == 204

#     def test_empty_create_course(self, testapp):
#         resp = testapp.post_json(url_for('api.create_course'), {
#         }, expect_errors=True)
#         assert resp.status_code == 400

#     def test_empty_update_course(self, testapp):
#         _post_course(testapp, 'manhattan')
#         resp = testapp.put_json(url_for('api.update_course', id=1), {
#         }, expect_errors=True)
#         assert resp.status_code == 400

#     def test_empty_partial_update_course(self, testapp):
#         _post_course(testapp, 'manhattan')
#         resp = testapp.put_json(url_for('api.partial_update_course', id=1), {
#         }, expect_errors=True)
#         assert resp.status_code == 400

#     def test_404_course(self, testapp):
#         resp = _patch_course(testapp, 'brooklyn', 2, expect_errors=True)
#         assert resp.status_code == 404
