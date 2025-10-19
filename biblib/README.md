# Auth and Books API implementation | Biblib Project

## What used

* Python 3.12+
* Django 5.2.6
* Django REST Framework
* SimpleJWT 
* SQLite3
* jQuery + HTML + CSS
* CORS Headers

## How to run
```bash
git clone https://github.com/yuliaHlazk/biblioteque.git
cd biblioteque

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate     # macOS/Linux
venv\Scripts\activate        # Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# (optional) Create superuser
python manage.py createsuperuser

# Start the server
python manage.py runserver
```

## How to run tests
```bash
pytest -v

# If Django settings module is not detected automatically specify manually
pytest -v --ds=biblib.settings
```

## authentication endpoints

### `POST /api/token`
**Used to:** login user and get access or refresh token
**Auth:** Not required

**Request Body:**
```json
{
  "username": "user1",
  "password": "s1e2c3ret"
}
```

**Response 200 OK:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGci...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5..."
}
```

### `POST /api/token/refresh`
**Used to:** Refresh access token
**Auth:** Not required

**Request Body:**
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5..."
}
```

**Response 200 OK:**
```json
{
  "access": "newAccessTokenHere"
}
```

### `POST /api/auth/register`
**Used to:** Register new user  
**Auth:** Not required

**Request Body:**
```json
{
  "username": "user1",
  "email": "user1@edu.ua",
  "password": "secret123",
  "password2": "secret123"
}
```

**Response 201 Created:**
```json
{
  "message": "User registered successfully",
}
```

### `GET /api/auth/profile`
**Used to:** Get current user's profile  
**Auth:** Required (`<access_token>`)

**Headers:**
```
Key: Authorization: Bearer siwcat7C1SB..
Key: Content-Type: application/json

```

**Response 200 OK:**
```json
{
  "id": 1,
  "username": "yulia",
  "email": "yulia@gmail.com",
  "first_name": "",
  "last_name": ""
}
```

### `PUT /api/auth/profile`
**Used to:** Update profile info  
**Auth:** Required (`<access_token>`)

**Request Body:**
```json
{
  "first_name": "Yulia",
  "last_name": "Lalala",
  "email": "yulia@gmail.com"
}
```

**Response 200 OK:**
```json
{
  "message": "Profile updated successfully",
  "username": "yulia",
  "email": "yulia@gmail.com",
  "first_name": "Yulia",
  "last_name": "Lalala"
}
```

## Book Endpoints

### `GET /api/books`
**Used to:** Get all books  
**Auth:** No Required - for all users

**Response 200 OK:**
```json
[
  {
    "id": 1,
    "title": "The City",
    "genre": "Novel",
    "price": 250,
    "author": "1",
    "publisher": "2",
    "author_name": "Valerian Pidmohylnyi",
    "publisher_name": "A-BA-BA-HA-LA-MA-HA",
    "description": "A Ukrainian classic novel..."
  }
]
```


### `POST /api/books`
**Used to:** Add a new book  *(admin only)*
**Auth:** Required (`<access_token>`)


**Request body:**
```json
[
  {
    "title": "The City",
    "genre": "Novel",
    "price": 250,
    "author": "1",
    "publisher": "2",
    "description": "optional: A Ukrainian classic novel..."
  }
]
```

**Response 201 CREATED:**
```json
[
  {
    "id": 1,
    "title": "The City",
    "genre": "Novel",
    "price": 250,
    "author_name": "Valerian Pidmohylnyi",
    "publisher_name": "A-BA-BA-HA-LA-MA-HA",
    "description": "null or A Ukrainian classic novel..."
  }
]
```

### `GET /api/books/:book_id`
**Used to:** Get book details by its id 
**Auth:** Required (`<access_token>`)

**Response 200 OK:**
```json
{
  "id": 1,
  "title": "The City",
  "genre": "Novel",
  "price": 250,
  "description": "A Ukrainian classic novel about the urban soul.",
  "author": 2,
  "publisher": 1,
  "author_name": "Valerian Pidmohylnyi",
  "publisher_name": "A-BA-BA-HA-LA-MA-HA",
}
```

### `PUT /api/books/:book_id`
**Used to:** Update an existing book by its id  *(admin only)*
**Auth:** Required (`<access_token>`)


**Request body:**
```json
[
  {
    "title": "The City",
    "genre": "Novel",
    "price": 250,
    "author": "1",
    "publisher": "2",
    "description": "optional: Updated edition: A Ukrainian classic novel..."
  }
]

**Response 200 OK:**
```json
[
  {
    "id": 1,
    "title": "The City",
    "genre": "Novel",
    "price": 250,
    "author_name": "Valerian Pidmohylnyi",
    "publisher_name": "A-BA-BA-HA-LA-MA-HA",
    "description": "null or Updated edition: A Ukrainian classic novel..."
  }
]
```

### `DELETE /api/books/:book_id`
**Used to:** Delete a book  *(admin only)*
**Auth:** Required (`<access_token>`)

**Response 200 OK:**
```json
{
  "message": "Book deleted successfully"
}
```


## Front

| File | For |
|------|----------|
| `index.html` | Public homepage: displays all books, required login for showing "View details" |
| `private.html` | Authenticated page: shows user's profile, book list |
| `scripts/script.js` | For loading books for public |
| `scripts/private-script.js` | Handles books, user's profile, and logout |
