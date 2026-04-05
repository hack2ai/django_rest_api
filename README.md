# Django REST Framework — User Profile API

## What This Project Does

This is a REST API built with Django and Django REST Framework.
It lets you create, read, update, and delete user profiles through
HTTP endpoints. All data is stored in a SQLite database.

---

## Project Structure

```
myapi/
├── manage.py
├── db.sqlite3
├── README.md
├── myapi/
│   ├── settings.py       <- Django settings, installed apps
│   └── urls.py           <- main URL config, includes /api/
└── users/
    ├── models.py         <- UserProfile model
    ├── serializers.py    <- converts model to/from JSON
    ├── views.py          <- ListCreateAPIView + RetrieveUpdateDestroyAPIView
    ├── permissions.py    <- custom permission class
    ├── filters.py        <- filter users by name or location
    ├── urls.py           <- /api/users/ and /api/users/<id>/ routes
    └── migrations/       <- database migration files
```

---

## How to Install and Run

### Step 1: Install packages
```
pip install django djangorestframework
```

### Step 2: Run migrations
```
python manage.py makemigrations
python manage.py migrate
```

### Step 3: Start the server
```
python manage.py runserver
```

Server runs at: http://127.0.0.1:8000

---

## API Endpoints

| Method | URL | What it does |
|--------|-----|--------------|
| GET    | /api/users/       | List all user profiles |
| POST   | /api/users/       | Create a new user profile |
| GET    | /api/users/<id>/  | Get one user by ID |
| PUT    | /api/users/<id>/  | Update a user completely |
| PATCH  | /api/users/<id>/  | Update a user partially |
| DELETE | /api/users/<id>/  | Delete a user |

---

## Example API Requests (curl)

### Create a user
```
curl -X POST http://127.0.0.1:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Rahul Sharma","email":"rahul@example.com","bio":"Developer","location":"Mumbai","age":25}'
```

### List all users
```
curl http://127.0.0.1:8000/api/users/
```

### Filter by location
```
curl http://127.0.0.1:8000/api/users/?location=Mumbai
```

### Filter by name
```
curl http://127.0.0.1:8000/api/users/?name=Rahul
```

### Get one user
```
curl http://127.0.0.1:8000/api/users/1/
```

### Update a user
```
curl -X PUT http://127.0.0.1:8000/api/users/1/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Rahul Sharma","email":"rahul@example.com","bio":"Senior dev","location":"Pune","age":26}'
```

### Delete a user
```
curl -X DELETE http://127.0.0.1:8000/api/users/1/
```

---

## UserProfile Fields

| Field      | Type    | Required | Notes                    |
|------------|---------|----------|--------------------------|
| id         | int     | auto     | set by database          |
| name       | string  | yes      | max 100 characters       |
| email      | string  | yes      | must be unique           |
| bio        | text    | no       | short description        |
| location   | string  | no       | city or country          |
| age        | int     | no       | must be 0 or above       |
| created_at | datetime| auto     | set when profile created |

---

## How the Views Work

**UserListCreateView** (inherits ListCreateAPIView):
- GET /api/users/ → returns list of all users
- POST /api/users/ → creates a new user
- also runs filter_users() to filter by name or location

**UserDetailView** (inherits RetrieveUpdateDestroyAPIView):
- GET /api/users/<id>/ → returns one user
- PUT /api/users/<id>/ → replaces the user data
- PATCH /api/users/<id>/ → partial update
- DELETE /api/users/<id>/ → deletes the user

---

## Running the Tests

### Unit tests (no server needed)
```
python manage.py test users --verbosity=2
```
Expected output:
```
Ran 15 tests in 0.094s
OK
```

Tests cover:
- Model creation and `__str__`
- GET list returns all users
- POST creates user (201)
- POST with missing email returns 400
- POST with duplicate email returns 400
- POST with negative age returns 400
- Filter by location
- Filter by name
- GET single user (200)
- GET non-existent user (404)
- PUT full update (200)
- PATCH partial update (200)
- DELETE (204)
- Response has all required fields

### Live endpoint test (server must be running)
```
python manage.py runserver
python test_api.py
```
