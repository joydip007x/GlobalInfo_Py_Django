
# World Atlas Explorer

A Django application to fetch, store, and serve country data via a RESTful API and a simple web interface. Data is sourced from restcountries.com and stored in PostgreSQL.


## Project Demo

[![Project Demo Video - Click to Watch](https://cdn.loom.com/sessions/thumbnails/e0e4c429294648b6a522247324124ac9-95aba059b3a2a4a1-full-play.gif)](https://www.loom.com/share/e0e4c429294648b6a522247324124ac9)

*Click the preview above to watch the full demo on Loom.*

## Setup Instructions

### 1. Prerequisites

*   Python 3.8+ & Pip
*   PostgreSQL

### 2. Clone Repository

```bash
git clone https://github.com/joydip007x/GlobalInfo_Py_Django
cd <repository-folder>
```

### 3. Setup Virtual Environment

```bash
python -m venv venv
# Windows: .\venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```
Key dependencies: Django, djangorestframework, psycopg2-binary, requests. (See `requirements.txt` for specific versions).

### 5. PostgreSQL Database Setup

**a. Create Database & User:**
Connect to PostgreSQL (e.g., via `psql`) and execute:

```sql
CREATE DATABASE worldatlas_db;
CREATE USER worldatlas_user WITH PASSWORD 'your_secure_password'; -- Use a strong password
ALTER ROLE worldatlas_user SET client_encoding TO 'utf8';
ALTER ROLE worldatlas_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE worldatlas_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE worldatlas_db TO worldatlas_user;

-- If connecting as a different user to grant schema permissions:
-- \c worldatlas_db
-- GRANT USAGE, CREATE ON SCHEMA public TO worldatlas_user;
```


**b. Configure Django Settings:**
Update `config/settings.py` (or your project's settings file) with your PostgreSQL credentials:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'worldatlas_db',
        'USER': 'worldatlas_user',
        'PASSWORD': 'your_secure_password', 
        'HOST': 'localhost', 
        'PORT': '5432',    
    }
}
```

### 6. Apply Database Migrations

```bash
python manage.py makemigrations countries
python manage.py migrate
```

### 7. Fetch Initial Country Data

```bash
python manage.py fetch_countries
```
(This command populates the database from restcountries.com and may take a moment.)

### 8. Create Superuser (for Admin Access)

```bash
python manage.py createsuperuser
```
Follow the prompts to set up an admin user.

## Running the Application

```bash
python manage.py runserver
```
*   **Web Interface:** `http://127.0.0.1:8000/`
*   **API Root:** `http://127.0.0.1:8000/api/`
*   **Django Admin:** `http://127.0.0.1:8000/admin/`

---
