from flask import jsonify, request, url_for
from app import db
from app.models import User
from app.api import bp
from app.api.errors import bad_request


@api.route('/instructors', methods=['GET'])
def get_instructors():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Instructor.to_collection_dict(Instructor.query, page, per_page, 
                                      'api.get_instructors')
    return jsonify(data)


@api.route('/instructors/<int:id>/', methods=['GET'])
def get_instructor(id):
    instructor = Instructor.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Instructor.to_collection_dict(instructor, page, per_page,
                                   'api.get_instructor', id=id)
    return jsonify(data)


@api.route('/instructors', methods=['POST'])
def create_instructor():
    data = request.get_json() or {}
    if 'first_name' not in data or 'last_name' not in data or 'enrollment_date' not in data:
        return bad_request('must include first_name, last_name and \
                           enrollment_date fields')
    instructor = Instructor()
    instructor.from_dict(data, new_user=True)
    db.session.add(instructor)
    db.session.commit()
    response = jsonify(instructor.to_dict())
    response.status_code = 201
    return response


@bp.route('/instructors/<int:id>', methods=['PUT'])
def update_instructor(id):
    instructor = Instructor.query.get_or_404(id)
    data = request.get_json() or {}
    instructor.from_dict(request.get_json() or {}, new_user=False)
    db.session.commit()
    response.status_code = 204
    return response


@bp.route('/instructors/<int:id>', methods=['DELETE'])
def delete_instructor(id):
    instructor = Instructor.query.get_or_404(id)
    db.session.delete(instructor)
    db.session.commit()
    response.status_code = 204
    return response

