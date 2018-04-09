from app.extensions import ma, db
from app.models import (
    Student,
    Course,
    Instructor,
    CourseAssignment,
    OfficeAssignment,
    Department,
    Enrollment
)


class DepartmentSchema(ma.ModelSchema):
    class Meta:
        model = Department
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.get_department', id='<id>'),
        'collection': ma.URLFor('api.get_departments')
    })


department_schema = DepartmentSchema()
departments_schema = DepartmentSchema(many=True)


class CourseAssignmentSchema(ma.ModelSchema):
    class Meta:
        model = CourseAssignment


course_assignment_schema = CourseAssignmentSchema()
courses_schema = CourseAssignmentSchema(many=True)


class EnrollmentSchema(ma.ModelSchema):
    class Meta:
        model = Enrollment


class CourseSchema(ma.ModelSchema):
    class Meta:
        model = Course
    enrollments = ma.Nested(EnrollmentSchema, many=True)
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.get_course', id='<id>'),
        'collection': ma.URLFor('api.get_courses')
    })


class CoursesSchema(ma.ModelSchema):
    class Meta:
        model = Course
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.get_course', id='<id>'),
        'collection': ma.URLFor('api.get_courses')
    })


course_schema = CourseSchema()
courses_schema = CoursesSchema(many=True)


class StudentsSchema(ma.ModelSchema):
    class Meta:
        model = Student
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.get_student', id='<id>'),
        'collection': ma.URLFor('api.get_students')
    })


class StudentSchema(ma.ModelSchema):
    class Meta:
        model = Student
    enrollments = ma.Nested(EnrollmentSchema, many=True)
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.get_student', id='<id>'),
        'collection': ma.URLFor('api.get_students')
    })


student_schema = StudentSchema()
students_schema = StudentsSchema(many=True)


class OfficeAssignmentSchema(ma.ModelSchema):
    class Meta:
        model = OfficeAssignment


class InstructorSchema(ma.ModelSchema):
    class Meta:
        model = Instructor
    office_assignment = ma.Nested(OfficeAssignmentSchema)
    course_assignments = ma.Nested(CourseAssignmentSchema, many=True)
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.get_instructor', id='<id>'),
        'collection': ma.URLFor('api.get_instructors')
    })


instructor_schema = InstructorSchema()
instructors_schema = InstructorSchema(many=True)
