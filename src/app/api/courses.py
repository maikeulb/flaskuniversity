from flask import jsonify, request, url_for
from app.extensions import db
from app.models import Course
from app.serializers import course_schema, courses_schema
from app.api import api
from app.api.errors import bad_request
from app.api.auth import token_auth


@api.route('/courses', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    result = courses_schema.dump(courses)
    return jsonify(result.data)


@api.route('/courses/<int:id>', methods=['GET'])
def get_course(id):
    course = Course.query.get_or_404(id)
    result = course_schema.dump(course)
    return jsonify(result.data)


@api.route('/courses', methods=['POST'])
@token_auth.login_required
def create_course():
    data = request.get_json() or {}
    if 'id' not in data or 'title' not in data or 'credits' not in data:
        return bad_request('must include id, title, credits, and department_id')
    course = Course()
    course.from_dict(data)
    db.session.add(course)
    db.session.commit()
    result = course_schema.dump(course)
    response = jsonify(result.data)
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_course', id=course.id)
    return response


@api.route('/courses/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_course(id):
    course = Course.query.get_or_404(id)
    data = request.get_json() or {}
    if 'id' not in data or 'title' not in data or 'credits' not in data:
        return bad_request('must include id, title, credits, and department_id')
    course.from_dict(data)
    db.session.commit()
    return '', 204


@api.route('/courses/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_course(id):
    course = Course.query.get_or_404(id)
    db.session.delete(course)
    db.session.commit()
    return '', 204
