import sys
import os
import click
from app.extensions import db
from app.models import (
    Course,
    Student,
    Department,
    CourseAssignment,
    Enrollment,
    Instructor,
    OfficeAssignment
)
from flask import current_app
from datetime import date
from random import choice, shuffle, sample


HERE = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.join(HERE, os.pardir)
TEST_PATH = os.path.join(PROJECT_ROOT, 'tests')


def register(app):
    @app.cli.command("seed-db")
    def seed_db():
        print('Starting DB seed')
        db.drop_all()
        db.create_all()

        seed_students()
        seed_instructors()
        seed_departments()
        seed_courses()
        seed_course_assignments()
        seed_enrollments()
        seed_office_assignments()
        db.session.commit()
        print('DB seed complete')

    def seed_students():
        print('Adding students')

        first_names = ['nik', 'kim', 'amy', 'marco', 'jake', 'allison', 'eva',
                       'com', 'elizier', 'nylah', 'marissa', 'camerson',
                       'andrea', 'keon']

        last_names = ['klaw', 'lowe', 'kombrough', 'ramsburg', 'mathews',
                      'braun', 'hunger', 'folwers', 'gross', 'barber',
                      'stanton', 'mckinney', 'craig', 'stone']

        enrollment_dates = [date(2001, 1, 2),
                            date(2001, 1, 2),
                            date(2001, 1, 2),
                            date(2009, 1, 2),
                            date(2009, 1, 2),
                            date(2009, 1, 2),
                            date(2009, 1, 2),
                            date(2011, 1, 2),
                            date(2011, 1, 2),
                            date(2011, 1, 2),
                            date(2011, 1, 2),
                            date(2017, 1, 2),
                            date(2017, 1, 2),
                            date(2017, 1, 2)]

        for s in range(0, len(last_names)):
            db.session.add(Student(first_name=first_names[s],
                                   last_name=last_names[s],
                                   enrollment_date=enrollment_dates[s]))

    def seed_instructors():
        print('Adding instructors')

        last_names = ['dalton', 'henderson', 'cruz', 'walker']
        first_names = ['nik', 'david', 'james', 'angela']
        hire_dates = [date(1987, 1, 2), date(1967, 1, 2), date(2001, 1, 2),
                      date(1957, 1, 2)]

        for i in range(0, len(last_names)):
            db.session.add(Instructor(first_name=first_names[i],
                                      last_name=last_names[i],
                                      hire_date=hire_dates[i]))

    def seed_departments():
        print('Adding departments')

        names = ['civil engineering', 'mechanical engineering']
        budgets = [205000, 250000]
        start_dates = [date(1987, 1, 2), date(1967, 1, 2)]
        instructor_ids = [1, 2]

        for d in range(0, len(names)):
            db.session.add(Department(name=names[d],
                                      budget=budgets[d],
                                      start_date=start_dates[d],
                                      instructor_id=instructor_ids[d]))

    def seed_courses():
        print('Adding courses')

        ids = [201, 221, 225, 321, 301, 302]
        titles = ['structural analysis i', 'structural analysis ii',
                  'structural dynamics', 'mechanical vibrations',
                  'finite element analysis i', 'finite element analysis ii']
        credits_lst = [3, 3, 3, 3, 3, 3]
        department_ids = [1, 1, 1, 2, 2, 2]

        for c in range(0, len(ids)):
            db.session.add(Course(id=ids[c],
                                  title=titles[c],
                                  credits=credits_lst[c],
                                  department_id=department_ids[c]))

    def seed_course_assignments():
        print('Adding course assignments')

        course_ids = [201, 221, 225, 321, 301, 302]
        instructor_ids = [1, 2, 2, 3, 4, 1]

        for c in range(0, len(course_ids)):
            db.session.add(CourseAssignment(course_id=course_ids[c],
                                            instructor_id=instructor_ids[c]))

    def seed_enrollments():
        print('Adding enrollments')

        course_ids = [201, 221, 225, 321, 301, 302]
        student_ids = list(range(1, 15))
        grades = ["A", "B", "C", "D", "F"]
        for course in course_ids:
            shuffled_ids = sample(student_ids, len(student_ids))
            for s in range(0, len(shuffled_ids)):
                db.session.add(Enrollment(course_id=course,
                                          student_id=shuffled_ids.pop(),
                                          grade=choice(grades)))

    def seed_office_assignments():
        print('Adding office assignments')

        locations = ['Soda Hall', 'Davis Hall', 'Peterson Hall', 'Revel Hall']
        instructor_ids = [1, 2, 3, 4]

        for i in range(0, len(locations)):
            db.session.add(OfficeAssignment(location=locations[i],
                                            instructor_id=instructor_ids[i]))

    @app.cli.command("test")
    def test():
        import pytest
        rv = pytest.main([TEST_PATH, '--verbose'])
        exit(rv)
