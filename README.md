# DRF Notes API

A Django REST Framework API for managing notes with authentication, CRUD operations, search, filtering, bookmarking, and image upload.

## Features
- User Registration & Login (Token Authentication)
- Create, Read, Update, Delete Notes
- Search, Filter, Sort Notes
- Bookmark Notes
- Upload Images with Notes

## API Endpoints

### Auth
POST /api/auth/register/
POST /api/auth/login/

### Notes
GET    /api/notes/
POST   /api/notes/create/
GET    /api/notes/<id>/detail/
PUT    /api/notes/<id>/update/
PATCH  /api/notes/<id>/update/
DELETE /api/notes/<id>/

### Bookmarks
GET    /api/bookmarks/
POST   /api/bookmarks/create/
DELETE /api/bookmarks/delete/

## How to Run

```bash
git clone <your-repo-link>
cd drf-notes
python -m venv venv
source venv/bin/activate
python manage.py migrate
python manage.py runserver
