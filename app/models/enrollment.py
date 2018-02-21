from app.extensions import db
from datetime import datetime
from enum import Enum
from sqlalchemy.dialects.postgresql import ENUM

class Enrollment(db.Model):
    __tablename__ = 'enrollments'

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    grade = db.Column("grade", Enum("A", "B", "C", "D", "F", name="grade_enum",
                                    create_type=False))

    course = db.relationship(
        'Course',
    )

    student = db.relationship(
        'Student',
    )
