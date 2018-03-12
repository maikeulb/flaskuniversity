from app.extensions import db
from datetime import datetime


class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.Integer)
    enrollment_date = db.Column(db.Integer)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))

    enrollments = db.relationship(
        'Enrollment',
    )

    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)
