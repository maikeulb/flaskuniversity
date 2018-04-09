# Flask University

Restful API backend for Microsoft's Contoso University sample application, but
written in Flask. Features include token-based authentication system (using
JWTs + Authorization headers), and CORS. The majority of it is complete but
I still have to add flask-marshmallow (for serialization/validation) and a few
more resources.

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
| `GET`      | `/api/courses/{id}`                  | `Retrieve course`                         |
| `POST`     | `/api/courses`                        | `Create course`                           |
| `PUT`      | `/api/courses/{id}`                  | `Update course`                           |
| `DELETE`   | `/api/courses/{id}          `        | `Delete course`                           |

### Students
| Method     | URI                                   | Action                                    |
|------------|---------------------------------------|-------------------------------------------|
| `GET`      | `/api/students`                       | `Retrieve all students`                   |
| `GET`      | `/api/students/{id}`                 | `Retrieve student`                        |
| `POST`     | `/api/students`                       | `Create student`                          |
| `PUT`      | `/api/students/{id}`                 | `Update student`                          |
| `DELETE`   | `/api/students/{id}`                 | `Delete student`                          |

### Instructors
| Method     | URI                                   | Action                                    |
|------------|---------------------------------------|-------------------------------------------|
| `GET`      | `/api/instructors`                    | `Retrieve all instructors`                |
| `GET`      | `/api/instructors/{id}`              | `Retrieve instructor`                     |
| `POST`     | `/api/instructors`                    | `Create instructor`                       |
| `PUT`      | `/api/instructors/{id}`              | `Update instructor`                       |
| `DELETE`   | `/api/instructors/{id}`              | `Delete instructor`                       |

### Departments
| Method     | URI                                   | Action                                    |
|------------|---------------------------------------|-------------------------------------------|
| `GET`      | `/api/departments`                    | `Retrieve all departments`                |
| `GET`      | `/api/departments/{id}`              | `Retrieve department`                     |
| `POST`     | `/api/departments`                    | `Create department`                       |
| `PUT`      | `/api/departments/{id}`              | `Update department`                       |
| `DELETE`   | `/api/departments/{id}`              | `Delete department`                       |

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
| `POST`     | `/auth/tokens`                         | `Retrieve Token`                          |
| `DELETE`   | `/auth/tokens`                         | `Revoke token `                           |

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

`http --auth-type=jwt --auth="sUboXR2NkQRDhyJ1QoyQm4kjBfi8EAoz" post localhost:5000/api/courses id:=333 credits:=3 department_id:=2 title="mechanical vibrations"`

```
{
    "_links": {
        "self": "/api/courses/333"
    }, 
    "credits": 3, 
    "department_id": 2, 
    "id": 333, 
    "title": "mechanical vibrations"
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
Add new read-only resources for course_assignment, enrollment, and office_assignment
(read-only)
Add flask-marshmallow 
