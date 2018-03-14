from app.extensions import db
from datetime import datetime
from .mixins import PaginatedAPIMixin


class Instructor(PaginatedAPIMixin, db.Model):
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

    def to_dict(self):
        data = {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_seen,
            'hire_date': self.hire_date,
            '_links': {
                'self': url_for('api.get_instructor', id=self.id),
            }
        }
        return data

    def from_dict(self, data):
        for field in ['first_name', 'last_name', 'hire_date']:
            if field in data:
                setattr(self, field, data[field])
