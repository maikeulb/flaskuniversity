import pytest
from flask import url_for
from app import create_app
from app.extensions import db as _db
from webtest import TestApp
from datetime import date
from random import choice, shuffle, sample
from app.auth import User
from app.models import (
    Course,
    Student,
    Department,
    CourseAssignment,
    Enrollment,
    Instructor,
    OfficeAssignment
)


@pytest.fixture
def app():
    _app = create_app('config.TestingConfig')
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture(scope='function')
def testapp(app):
    return TestApp(app)


@pytest.fixture
def token(app, db):
    testapp = TestApp(app)
    user = User(username='demo',
                email='demo@example.com')
    user.set_password('P@ssw0rd!')
    db.session.add(user)
    db.session.commit()
    testapp.authorization = ('Basic', ('demo', 'P@ssw0rd!'))
    resp = testapp.post_json(url_for("api.get_token"))
    token = str(resp.json['token'])
    return token


@pytest.fixture
def user(db):
    user = User(username='demo',
                email='demo@example.com')
    user.set_password('P@ssw0rd!')
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def student(db):
    student = Student(first_name='demo',
                      last_name='demo',
                      enrollment_date=date(2011, 1, 1))
    db.session.add(student)
    db.session.commit()
    return student


@pytest.fixture
def course(db):
    course = Course(id=264,
                    title='demo course',
                    credits=3,
                    department_id=1)
    db.session.add(course)
    db.session.commit()
    return course


@pytest.fixture
def department(db):
    department = Department(name='demo department',
                            budget=2000000,
                            start_date=date(1967, 1, 2),
                            instructor_id=1)
    db.session.add(department)
    db.session.commit()
    return department


@pytest.fixture
def course_assignment(db):
    course_assignment = CourseAssignment(course_id=1,
                                         instructor_id=1)
    db.session.add(course_assignment)
    db.session.commit()
    return course_assignment


@pytest.fixture
def instructor(db):
    instructor = Instructor(first_name='demo',
                            last_name='demo',
                            hire_date=date(2011, 1, 1))
    db.session.add(instructor)
    db.session.commit()
    return instructor


@pytest.fixture
def enrollment(db):
    instructor = Enrollment(course_id=264,
                            student_d=1,
                            grade="A")
    db.session.add(enrollment)
    db.session.commit()
    return instructor


@pytest.fixture
def office_assignment(db):
    office_assignment = OfficeAssignment(location="demo location",
                                         instructor_id=1)
    db.session.add(office_assignment)
    db.session.commit()
    return office_assignment


@pytest.fixture
def db(app):
    _db.app = app
    with app.app_context():
        _db.create_all()

    yield _db

    _db.session.close()
    _db.drop_all()
