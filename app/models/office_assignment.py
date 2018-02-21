from app.extensions import db
from datetime import datetime


class OfficeAssignment(db.Model):
    __tablename__ = 'office_assignments'

    location = db.Column(db.Integer, primary_key=True)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.id'))

    instructor = db.relationship(
        'Instructor',
    )
