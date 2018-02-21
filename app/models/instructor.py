from app.extensions import db
from datetime import datetime

course_assignments = db.Table(
    'course_assignments',
    db.Column('instructor_id', db.Integer, db.ForeignKey('instructors.id')),
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id'))
)

class Instructor(db.Model):
    __tablename__ = 'instructors'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    hire_date = db.Column(db.String)

    office_assignment = db.relationship(
        'OfficeAssignment',
    )

    course_assignments = db.relationship(
        'course_assignments',
        backref='course_assignments'
    )

    courses = db.relationship(
        'Course',
    )
    
    @property
    def full_name(self):
        return '{0}, {1}'.format(self.last_name.title(),
                                         self.first_name.title())

