# Flask University

Restful API backend for Microsoft's Contoso University sample application, but
written in Flask. Features include token-based authentication system (using
JWTs + Authorization headers), and CORS. There are two branches: `master` and
`marshmallow` (in-progress). The `master` branch implements simple
serializations and minimal validation (e.g. only checking for null values for
required fields). The `marshmallow` branch will implement more complex
serializations and more complete validations.

Technology
----------
* Flask
* PostgreSQL

Endpoints
---------

### Courses
| Method     | URI                                   | Action                                    |
|------------|---------------------------------------|-------------------------------------------|
| `GET`      | `/api/courses`                        | `Retrieve all courses`                    |
| `GET`      | `/api/courses/{bid}`                  | `Retrieve course`                         |
| `POST`     | `/api/courses`                        | `Create course`                           |
| `PUT`      | `/api/courses/{bid}`                  | `Update course`                           |
| `DELETE`   | `/api/courses/{bid}          `        | `Delete course`                           |

### Students
| Method     | URI                                   | Action                                    |
|------------|---------------------------------------|-------------------------------------------|
| `GET`      | `/api/students`                       | `Retrieve all students`                   |
| `GET`      | `/api/students/{bid}`                 | `Retrieve student`                        |
| `POST`     | `/api/students`                       | `Create student`                          |
| `PUT`      | `/api/students/{bid}`                 | `Update student`                          |
| `DELETE`   | `/api/students/{bid}`                 | `Delete student`                          |

### Instructors
| Method     | URI                                   | Action                                    |
|------------|---------------------------------------|-------------------------------------------|
| `GET`      | `/api/instructors`                    | `Retrieve all instructors`                |
| `GET`      | `/api/instructors/{bid}`              | `Retrieve instructor`                     |
| `POST`     | `/api/instructors`                    | `Create instructor`                       |
| `PUT`      | `/api/instructors/{bid}`              | `Update instructor`                       |
| `DELETE`   | `/api/instructors/{bid}`              | `Delete instructor`                       |

### Departments
| Method     | URI                                   | Action                                    |
|------------|---------------------------------------|-------------------------------------------|
| `GET`      | `/api/departments`                    | `Retrieve all departments`                |
| `GET`      | `/api/departments/{bid}`              | `Retrieve department`                     |
| `POST`     | `/api/departments`                    | `Create department`                       |
| `PUT`      | `/api/departments/{bid}`              | `Update department`                       |
| `DELETE`   | `/api/departments/{bid}`              | `Delete department`                       |

### Users
| Method     | URI                                   | Action                                    |
|------------|---------------------------------------|-------------------------------------------|
| `GET`      | `/api/users`                          | `Retrieve all users`                      |
| `GET`      | `/api/users/{id}`                     | `Retrieve user`                           |
| `POST`     | `/api/users`                          | `Register user `                          |
| `PUT`      | `/api/users`                          | `Update users`                            |

### Auth
| Method     | URI                                   | Action                                    |
|------------|---------------------------------------|-------------------------------------------|
| `POST`     | `/auth/tokens`                        | `Retrieve Token`                          |
| `DELETE`   | `/auth/tokens`                        | `Revoke token `                           |

Sample Usage
---------------
`http post localhost:5000/api/users username=user password=pass
email=user@example.com`
```
{
    "_links": {
        "self": "/api/users/4"
    }, 
    "id": 4, 
    "username": "user"
}
```

`http --auth user:pass post localhost:5000/auth/tokens` (http basic authentication)
```
{
    "token": "sUboXR2NkQRDhyJ1QoyQm4kjBfi8EAoz"
}
```

`http --auth-type=jwt --auth="sUboXR2NkQRDhyJ1QoyQm4kjBfi8EAoz" post localhost:5000/api/instructors first_name:='sanjay' last_name='govindjee' course_assignments:=[201, 302] office_assignments='davis hall'

```
{
    "_links": {
        "self": "/api/instructors/10"
    }, 
    "course_assignments": [
        {
            "course_id": 201, 
            "instructor_id": 10
        }, 
        {
            "course_id": 302, 
            "instructor_id": 10
        }
    ], 
    "first_name": "sanjay", 
    "id": 10, 
    "last_name": "govindjee", 
    "office_assignment": [
        {
            "instructor_id": 10, 
            "location": "davis hall"
        }
    ]
}
```

Run
---
If you have docker installed,
```
docker-compose build
docker-compose up
Go to http://localhost:5000 and visit one of the above endpoints
```

Otherwise, go to `config.py` and point the PostgreSQL variable to your server
URI, set the `FLASK_APP` env variable to flaskuniversity.py, and pip install
the requirements. 

After all that has been taken care of,
```
flask db upgrade
flask seed-db
flask run
Go to http://localhost:5000 and visit one of the above endpoints
```

TODO
----
Finish flask-marshmallow 
