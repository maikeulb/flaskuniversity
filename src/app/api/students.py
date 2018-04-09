from flask import jsonify, request, url_for
from app.extensions import db
from app.models import Student
from app.serializers import student_schema, students_schema
from app.api import api
from app.api.errors import bad_request
from app.api.auth import token_auth


@api.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    result = students_schema.dump(students)
    return jsonify(result.data)


@api.route('/students/<int:id>', methods=['GET'])
def get_student(id):
    student = Student.query.get_or_404(id)
    result = student_schema.dump(student)
    return jsonify(result.data)


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
    result = student_schema.dump(student)
    response = jsonify(result.data)
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
