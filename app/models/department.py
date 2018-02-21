from app.extensions import db
from datetime import datetime


class Department(db.Model):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    budget = db.Column(db.Integer)
    startDate = db.Column(db.Integer)
    instructor_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    instructor = db.relationship(
        'Instructor',
    )

    Courses = db.relationship(
        'Courses',
    )
