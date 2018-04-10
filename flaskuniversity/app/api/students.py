from flask import jsonify, request, url_for
from app.extensions import db
from app.models import Student
from app.api import api
from app.api.errors import bad_request
from app.api.auth import token_auth


@api.route('/students', methods=['GET'])
def get_students():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Student.to_collection_dict(Student.query, page, per_page,
                                      'api.get_students')
    return jsonify(data)


@api.route('/students/<int:id>', methods=['GET'])
def get_student(id):
    student = Student.query.get_or_404(id)
    return jsonify(student.to_dict())


@api.route('/students', methods=['POST'])
@token_auth.login_required
def create_student():
    data = request.get_json() or {}
    if 'first_name' not in data or 'last_name' not in data:
        return bad_request('must include first_name, last_name and enrollment_date fields')
    student = Student()
    student.from_dict(data)
    db.session.add(student)
    db.session.commit()
    response = jsonify(student.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_student', id=student.id)
    return response


@api.route('/students/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_student(id):
    student = Student.query.get_or_404(id)
    data = request.get_json() or {}
    if 'first_name' not in data or 'last_name' not in data:
        return bad_request('must include first_name, last_name and enrollment_date fields')
    student.from_dict(data)
    db.session.commit()
    return '', 204


@api.route('/students/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return '', 204
