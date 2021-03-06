from app.extensions import db
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import ENUM
from datetime import datetime
from flask import Flask, url_for


class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data


class Student(PaginatedAPIMixin, db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    enrollment_date = db.Column(db.Date, nullable=True)

    enrollments = db.relationship(
        'Enrollment',
    )

    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    def to_dict(self):
        data = {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'enrollment_date': self.enrollment_date,
            '_links': {
                'self': url_for('api.get_student', id=self.id),
            }
        }
        return data

    def from_dict(self, data):
        for field in ['first_name', 'last_name', 'enrollment_date']:
            if field in data:
                setattr(self, field, data[field])


class Course(PaginatedAPIMixin, db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    credits = db.Column(db.Integer)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))

    department = db.relationship(
        'Department',
    )
    enrollments = db.relationship(
        'Enrollment',
    )
    course_assignments = db.relationship(
        'CourseAssignment',
    )

    def to_dict(self):
        data = {
            'id': self.id,
            'title': self.title,
            'credits': self.credits,
            'department_id': self.department_id,
            '_links': {
                'self': url_for('api.get_course', id=self.id),
            }
        }
        return data

    def from_dict(self, data):
        for field in ['id', 'title', 'credits', 'department_id']:
            if field in data:
                setattr(self, field, data[field])


class Instructor(PaginatedAPIMixin, db.Model):
    __tablename__ = 'instructors'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    hire_date = db.Column(db.Date, nullable=True)

    office_assignment = db.relationship(
        'OfficeAssignment',
    )
    course_assignments = db.relationship(
        'CourseAssignment',
    )

    @property
    def full_name(self):
        return '{0}, {1}'.format(self.last_name.title(),
                                 self.first_name.title())

    def to_dict(self):
        data = {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'hire_date': self.hire_date,
            'office_assignment': [oa.to_dict() for oa in
                                  self.office_assignment],
            'course_assignments': [ca.to_dict() for ca in
                                   self.course_assignments],
            '_links': {
                'self': url_for('api.get_instructor', id=self.id),
            }
        }
        return data

    def from_dict(self, data):
        for field in ['first_name', 'last_name', 'hire_date']:
            if field in data:
                setattr(self, field, data[field])


class CourseAssignment(PaginatedAPIMixin, db.Model):
    __tablename__ = 'course_assignments'
    __table_args__ = (
        PrimaryKeyConstraint('instructor_id', 'course_id'),
    )

    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))

    instructor = db.relationship(
        'Instructor',
    )

    course = db.relationship(
        'Course',
    )

    def to_dict(self):
        data = {
            'instructor_id': self.instructor_id,
            'course_id': self.course_id
        }
        return data

    def from_dict(self, data):
        for field in ['instructor_id', 'course_id']:
            if field in data:
                setattr(self, field, data[field])


class OfficeAssignment(PaginatedAPIMixin, db.Model):
    __tablename__ = 'office_assignments'

    location = db.Column(db.String, primary_key=True)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.id'))

    instructor = db.relationship(
        'Instructor',
    )

    def to_dict(self):
        data = {
            'location': self.location,
            'instructor_id': self.instructor_id
        }
        return data

    def from_dict(self, data):
        for field in ['location', 'instructor_id']:
            if field in data:
                setattr(self, field, data[field])


class Department(PaginatedAPIMixin, db.Model):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    budget = db.Column(db.Numeric(8, 2))
    start_date = db.Column(db.Date, nullable=True)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.id'))

    instructor = db.relationship(
        'Instructor',
    )
    courses = db.relationship(
        'Course',
    )

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'budget': self.budget,
            'instructor_id': self.instructor_id,
            'start_date': self.start_date,
            '_links': {
                'self': url_for('api.get_department', id=self.id),
            }
        }
        return data

    def from_dict(self, data):
        for field in ['name', 'budget', 'start_date', 'instructor_id']:
            if field in data:
                setattr(self, field, data[field])


class Enrollment(PaginatedAPIMixin, db.Model):
    __tablename__ = 'enrollments'

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    grade = db.Column("grade", ENUM("A", "B", "C", "D", "F", name="grade_enum",
                                    create_type=False))

    course = db.relationship(
        'Course',
    )
    student = db.relationship(
        'Student',
    )

    def to_dict(self):
        data = {
            'id': self.id,
            'course_id': self.course_id,
            'student_id': self.student_id,
            'grade': self.grade,
            '_links': {
                'self': url_for('api.get_enrollment', id=self.id),
            }
        }
        return data

    def from_dict(self, data):
        for field in ['course_id, student_id, grade']:
            if field in data:
                setattr(self, field, data[field])
