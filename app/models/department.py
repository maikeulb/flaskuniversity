from app.extensions import db
from datetime import datetime
from .mixins import PaginatedAPIMixin


class Department(PaginatedAPIMixin, db.Model):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    budget = db.Column(db.Numeric(8, 2))
    start_date = db.Column(db.DateTime)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.id'))

    instructor = db.relationship(
        'Instructor',
    )

    courses = db.relationship(
        'Courses',
    )

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'budget': self.budget,
            'start_date': self.start_date,
            '_links': {
                'self': url_for('api.get_department', id=self.id),
            }
        }
        return data

    def from_dict(self, data):
        for field in ['name', 'budget', 'start_date']:
            if field in data:
                setattr(self, field, data[field])
