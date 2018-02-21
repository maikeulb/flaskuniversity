from flask import jsonify, request, url_for
from app import db
from app.models import User
from app.api import bp
from app.api.errors import bad_request


@api.route('/departments', methods=['GET'])
def get_departments():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Department.to_collection_dict(Department.query, page, per_page, 
                                      'api.get_departments')
    return jsonify(data)


@api.route('/departments/<int:id>/', methods=['GET'])
def get_department(id):
    department = Department.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Department.to_collection_dict(department, page, per_page,
                                   'api.get_department', id=id)
    return jsonify(data)


@api.route('/departments', methods=['POST'])
def create_department():
    data = request.get_json() or {}
    if 'first_name' not in data or 'last_name' not in data or 'enrollment_date' not in data:
        return bad_request('must include first_name, last_name and \
                           enrollment_date fields')
    department = Department()
    department.from_dict(data, new_user=True)
    db.session.add(department)
    db.session.commit()
    response = jsonify(department.to_dict())
    response.status_code = 201
    return response


@bp.route('/departments/<int:id>', methods=['PUT'])
def update_department(id):
    department = Department.query.get_or_404(id)
    data = request.get_json() or {}
    department.from_dict(request.get_json() or {}, new_user=False)
    db.session.commit()
    response.status_code = 204
    return response


@bp.route('/departments/<int:id>', methods=['DELETE'])
def delete_department(id):
    department = Department.query.get_or_404(id)
    db.session.delete(department)
    db.session.commit()
    response.status_code = 204
    return response

