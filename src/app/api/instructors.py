from flask import jsonify, request, url_for
from app.extensions import db
from app.models import Instructor, OfficeAssignment
from app.serializers import instructor_schema, instructors_schema
from app.api import api
from app.api.errors import bad_request
from app.api.auth import token_auth


@api.route('/instructors', methods=['GET'])
def get_instructors():
    instructors = Instructor.query.all()
    result = instructors_schema.dump(instructors)
    return jsonify(result.data)


@api.route('/instructors/<int:id>', methods=['GET'])
def get_instructor(id):
    instructor = Instructor.query.get_or_404(id)
    result = instructor_schema.dump(instructor)
    return jsonify(result.data)


@api.route('/instructors', methods=['POST'])
@token_auth.login_required
def create_instructor():
    data = request.get_json() or {}
    if 'first_name' not in data or 'last_name' not in data:
        return bad_request('must include first_name and last_name')
    instructor = Instructor()
    instructor.from_dict(data)
    # if (instructor.office_assignment != None):
    # office_assignment = OfficeAssignment()
    # office_assignment.instructor_id = instructor.id  # is this not zero?
    # office_assignment.location = instructor.office_assignment
    # instructor.office_assignment = office_assignment
    if (instructor.course_assignments != None):
        for course in instructor.course_assignments:
            course_to_add = CourseAssignment()
            course_to_add.instructor_id = instructor.id
            course_to_add.course_id = course.id
            instructor.CourseAssignments.add(course_to_add)
    db.session.add(instructor)
    db.session.commit()
    result = instructor_schema.dump(instructor)
    response = jsonify(result.data)
    response.status_code = 201
    response.headers['Location'] = url_for(
        'api.get_department', id=instructor.id)
    return response


@api.route('/instructors/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_instructor(id):
    instructor = Instructor.query.get_or_404(id)
    data = request.get_json() or {}
    if 'first_name' not in data or 'last_name' not in data:
        return bad_request('must include first_name, last_name and enrollment_date fields')
    instructor.from_dict(data)
    # add logic for updating office_assignment and course_assignment#
    db.session.commit()
    return '', 204


@api.route('/instructors/<int:id>', methods=['DELETE'])
def delete_instructor(id):
    instructor = Instructor.query.get_or_404(id)
    db.session.delete(instructor)
    db.session.commit()
    return '', 204
