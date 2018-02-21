from app.extensions import db
from datetime import datetime


class Course(db.Model):
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
