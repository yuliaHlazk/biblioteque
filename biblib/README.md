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

## Endpoints

### `POST /api/token`
**Used to:** Access and refresh token
**Auth:** Not required

**Request Body:**
```json
{
  "username": "user1",
  "password": "secret"
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
  "username": "user1"
}
```

### `POST /api/auth/login`
**Used to:** Login user and get JWT token  
**Auth:** Not required  

**Request Body:**
```json
{
  "username": "user1",
  "password": "secret123"
}
```

**Response 200 OK:**
```json
{
  "access": "OiJKV1QiLCJhbGci...",
  "refresh": "OiJIUzI1NiIsInR5..."
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
**Auth:** Required (`<access_token>`)

**Response 200 OK:**
```json
[
  {
    "id": 1,
    "title": "The City",
    "genre": "Novel",
    "price": 250,
    "author": "Valerian Pidmohylnyi",
    "publisher": "A-BA-BA-HA-LA-MA-HA",
    "description": "A Ukrainian classic novel..."
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
  "author": {"id": 2, "name": "Valerian Pidmohylnyi"},
  "publisher": {"id": 1, "name": "A-BA-BA-HA-LA-MA-HA"}
}
```

## Front

| File | For |
|------|----------|
| `index.html` | Public homepage: displays all books, required login for showing "View details" |
| `private.html` | Authenticated page: shows user's profile, book list |
| `scripts/script.js` | For loading books for public |
| `scripts/private-script.js` | Handles books, user's profile, and logout |
