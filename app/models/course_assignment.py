from app.extensions import db


class CourseAssignment(db.Model):
    __tablename__ = 'course_assignments'

    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))

    instructor = db.relationship(
        'Instructor',
    )

    course= db.relationship(
        'Course',
    )

    def to_dict(self):
        data = {
            'instructor_id': self.instructor_id,
            'course_id': self.course_id,
            '_links': {
                'self': url_for('api.get_customer', id=self.id),
            }
        }
        return data

    def from_dict(self, data, new_user=False):
        for field in ['instructor_id', 'course_id']
            if field in data:
                setattr(self, field, data[field])
