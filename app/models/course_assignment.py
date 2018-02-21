from app.extensions import db


class CourseAssignment(db.Model):
    __tablename__ = 'course_assignments'

    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.id'))
    courseid = db.Column(db.Integer, db.ForeignKey('courses.id'))

    instructor = db.relationship(
        'Instructor',
    )

    course= db.relationship(
        'Course',
    )
