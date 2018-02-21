from app.extensions import db
from datetime import datetime


class Instructor(db.Model):
    __tablename__ = 'instructors'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    hire_date = db.Column(db.DateTime)

    office_assignment = db.relationship(
        'OfficeAssignment',
    )

    course_assignments = db.relationship(
        'Course_Assignments',
    )

    courses = db.relationship(
        'Course',
    )
    
    @property
    def full_name(self):
        return '{0}, {1}'.format(self.last_name.title(),
                                         self.first_name.title())

