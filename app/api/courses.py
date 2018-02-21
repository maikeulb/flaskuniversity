from flask import jsonify, request, url_for
from app import db
from app.models import User
from app.api import bp
from app.api.errors import bad_request


@api.route('/courses', methods=['GET'])
def get_courses():
    course_query = Course.query
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Course.to_collection_dict(course_query, page, per_page, 
                                      'api.get_courses')
    return jsonify(data)


@api.route('/courses/<int:id>/', methods=['GET'])
def get_course(id):
    course_query = Course.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Course.to_collection_dict(course_query, page, per_page,
                                   'api.get_course', id=id)
    return jsonify(data)


@api.route('/courses', methods=['POST'])
def create_course():
    data = request.get_json() or {}
    if 'first_name' not in data or 'last_name' not in data or 'enrollment_date' not in data:
        return bad_request('must include first_name, last_name and \
                           enrollment_date fields')
    course = Course()
    course.from_dict(data, new_user=True)
    db.session.add(course)
    db.session.commit()
    response = jsonify(course.to_dict())
    response.status_code = 201
    return response


@api.route('/courses/<int:id>', methods=['PUT'])
def update_course(id):
    course = Course.query.get_or_404(id)
    data = request.get_json() or {}
    course.from_dict(request.get_json() or {}, new_user=False)
    db.session.commit()
    response.status_code = 204
    return response


@api.route('/courses/<int:id>', methods=['DELETE'])
def delete_course(id):
    course = Course.query.get_or_404(id)
    db.session.delete(course)
    db.session.commit()
    response.status_code = 204
    return response
