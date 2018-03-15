from flask import Blueprint

api = Blueprint('api', __name__)

from app.api import courses, departments, instructors, students, errors, tokens, users
