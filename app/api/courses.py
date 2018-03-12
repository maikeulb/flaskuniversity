from flask import jsonify, request, url_for
from app import db
from app.models import Course
from app.api import api
from app.api.errors import bad_request


@api.route('/courses', methods=['GET'])
def get_courses():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Course.to_collection_dict(Course.query, page, per_page,
                                     'api.get_courses')
    return jsonify(data), 200


@api.route('/courses/<int:id>/', methods=['GET'])
def get_course(id):
    course = Course.query.get_or_404(id)
    return jsonify(course.to_dict()), 200


@api.route('/courses', methods=['POST'])
def create_course():
    data = request.get_json() or {}
    if 'course_id' not in data or 'title' not in data or 'credits' not in data
    'deparment_id' not in data:
        return bad_request('must include course_id, title, credits, and \
        department_id')
    course = Course()
    course.from_dict(data)
    db.session.add(course)
    db.session.commit()
    return jsonify(course.to_dict()), 201


@api.route('/courses/<int:id>', methods=['PUT'])
def update_course(id):
    course = Course.query.get_or_404(id)
    data = request.get_json() or {}
    course.from_dict(data)
    db.session.commit()
    return '', 204


@api.route('/courses/<int:id>', methods=['DELETE'])
def delete_course(id):
    course = Course.query.get_or_404(id)
    db.session.delete(course)
    db.session.commit()
    return '', 204
