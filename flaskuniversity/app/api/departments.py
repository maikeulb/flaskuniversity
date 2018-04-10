from flask import jsonify, request, url_for
from app.extensions import db
from app.models import Department
from app.api import api
from app.api.errors import bad_request
from app.api.auth import token_auth


@api.route('/departments', methods=['GET'])
def get_departments():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Department.to_collection_dict(Department.query, page, per_page,
                                         'api.get_departments')
    return jsonify(data)


@api.route('/departments/<int:id>', methods=['GET'])
def get_department(id):
    department = Department.query.get_or_404(id)
    return jsonify(department.to_dict())


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
    response = jsonify(department.to_dict())
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
