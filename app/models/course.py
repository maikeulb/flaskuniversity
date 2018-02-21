from app.extensions import db
from app.api.mixins import PaginatedAPIMixin


class Course(PaginatedAPIMixin, db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    credits = db.Column(db.Integer)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))

    department = db.relationship(
        'Department',
    )
    enrollments = db.relationship(
        'Enrollment',
    )
    course_assignments = db.relationship(
        'CourseAssignment',
    )

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'title': self.username,
            'credits': self.last_seen.isoformat() + 'Z',
            '_links': {
                'self': url_for('api.get_customer', id=self.id),
            }
        }
        return data

    def from_dict(self, data, new_user=False):
        for field in ['title', 'credits']
            if field in data:
                setattr(self, field, data[field])
