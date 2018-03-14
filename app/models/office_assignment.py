from app.extensions import db
from datetime import datetime


class OfficeAssignment(db.Model):
    __tablename__ = 'office_assignments'

    location = db.Column(db.Integer, primary_key=True)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.id'))

    instructor = db.relationship(
        'Instructor',
    )

    def to_dict(self):
        data = {
            'id': self.id,
            'location': self.location,
            'instructor_id': self.instructor_id,
            '_links': {
                'self': url_for('api.get_instructor', id=self.id),
            }
        }
        return data

    def from_dict(self, data):
        for field in ['location', 'instructor_id']:
            if field in data:
                setattr(self, field, data[field])
