from app.extensions import db
from datetime import datetime
from app.api.mixins import PaginatedAPIMixin


class Department(PaginatedAPIMixin, db.Model):
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

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'name': self.username,
            'budget': self.last_seen.isoformat() + 'Z',
            'startDate': self.last_seen.isoformat() + 'Z',
            '_links': {
                'self': url_for('api.get_department', id=self.id),
            }
        }
        return data

    def from_dict(self, data, new_user=False):
        for field in ['name', 'budget', 'startDate']
            if field in data:
                setattr(self, field, data[field])
