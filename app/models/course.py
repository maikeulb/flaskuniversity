from app.extensions import db
from .mixins import PaginatedAPIMixin


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

    def to_dict(self):
        data = {
            'id': self.id,
            'title': self.title,
            'credits': self.credits,
            'department_id': self.department_id,
            '_links': {
                'self': url_for('api.get_customer', id=self.id),
            }
        }
        return data

    def from_dict(self, data):
        for field in ['title', 'credits', 'department_id']:
            if field in data:
                setattr(self, field, data[field])
