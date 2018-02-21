from app.extensions import db
from datetime import datetime


class Department(db.Model):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    budget = db.Column(db.Numeric(8,2))
    startDate = db.Column(db.DateTime)
    instructor_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    instructor = db.relationship(
        'Instructor',
    )

    courses = db.relationship(
        'Courses',
    )
