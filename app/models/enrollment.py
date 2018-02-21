from app.extensions import db
from sqlalchemy.dialects.postgresql import ENUM
from app.api.mixins import PaginatedAPIMixin

class Enrollment(PaginatedAPIMixin, db.Model):
    __tablename__ = 'enrollments'

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    grade = db.Column("grade", ENUM("A", "B", "C", "D", "F", name="grade_enum",
                                    create_type=False))

    course = db.relationship(
        'Course',
    )
    student = db.relationship(
        'Student',
    )

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'grade': self.last_seen.isoformat() + 'Z',
            '_links': {
                'self': url_for('api.get_enrollment', id=self.id),
            }
        }
        return data

    def from_dict(self, data, new_user=False):
        for field in ['grade']
            if field in data:
                setattr(self, field, data[field])
