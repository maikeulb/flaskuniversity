from flask import jsonify, request, url_for
from app.extensions import db
from app.models import Department
from app.serializers import department_schema, departments_schema
from app.api import api
from app.api.errors import bad_request
from app.api.auth import token_auth


@api.route('/departments', methods=['GET'])
def get_departments():
    departments = Department.query.all()
    result = departments_schema.dump(departments)
    return jsonify(result.data)


@api.route('/departments/<int:id>', methods=['GET'])
def get_department(id):
    department = Department.query.get_or_404(id)
    result = department_schema.dump(department)
    return jsonify(result.data)


@api.route('/departments', methods=['POST'])
@token_auth.login_required
def create_department():
    data = request.get_json() or {}
    if 'name' not in data or 'budget' not in data or 'budget' not in data or 'instructor_id' not in data:
        return bad_request('must include first_name, last_name and enrollment_date fields')
    department = Department()
    department.from_dict(data)
    db.session.add(department)
    db.session.commit()
    result = department_schema.dump(department)
    response = jsonify(result.data)
    response.status_code = 201
    response.headers['Location'] = url_for(
        'api.get_department', id=department.id)
    return response


@api.route('/departments/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_department(id):
    department = Department.query.get_or_404(id)
    data = request.get_json() or {}
    if 'name' not in data or 'budget' not in data or 'budget' not in data or 'instructor_id' not in data:
        return bad_request('must include first_name, last_name and enrollment_date fields')
    department.from_dict(data)
    db.session.commit()
    return '', 204


@api.route('/departments/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_department(id):
    department = Department.query.get_or_404(id)
    db.session.delete(department)
    db.session.commit()
    return '', 204
