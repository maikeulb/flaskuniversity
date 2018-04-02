# Flask University

Restful API backend for Microsoft's Contoso University sample application, but 
written in Flask and with token-based authentication system (using JWTs). 

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
| `POST`     | `/api/tokens`                         | `Retrieve Token`                          |
| `DELETE`   | `/api/tokens`                         | `Revoke token `                           |

Sample Response
---------------
[TODO]

Run
---
If you have docker installed,
```
docker-compose build
docker-compose up
Go to http://localhost:5000 and visit one of the above endpoints
```

Otherwise, go to config.py and point the PostgreSQL and Elasticsearch variables
so that they point to your server URI's, set the FLASK_APP env variable to
landmarks.py, and pip install the requirements. 

After all that has been taken care of,
```
flask db upgrade
flask seed-db
flask run
Go to http://localhost:5000 and visit one of the above endpoints
```

TODO
----
Add course assignment
Add instructor assignment
