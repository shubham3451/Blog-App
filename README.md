# Django Project

This is a Django project designed to handle user profiles, posts, and media uploads such as images, videos, and audio. It includes functionality for user authentication, updating profiles, and password management. The project also includes a search bar for searching users and a dynamic post section where users can share content.

## Features

- User authentication (login, registration, reset password with email)
- User profile management (view,edit and delete profile)
- Post creation with media (image, video, audio)
- Dynamic post display with content visibility
- User search bar
- Profile URL and edit buttons
- Change password functionality
- Responsive design for mobile and desktop views

## Technologies Used

- **Django**: Backend framework
- **SQLite**: Database
- **HTML/CSS**: Frontend
- **Gunicorn**: WSGI server

## Prerequisites

Before setting up the project, ensure you have the following installed:

- Python 3.x
- pip (Python package installer)
- Git (to clone the repository)
- PostgreSQL (if running locally)

## Setup and Installation

### 1. Clone the Repository

Start by cloning the repository to your local machine:

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git
cd YOUR_REPOSITORY_NAME
```

### 2. Create a Virtual Environment

To isolate the project dependencies, create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

Install the project dependencies listed in the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

You need to configure the following environment variables in your local setup:

- `DJANGO_SECRET_KEY`: Your Django secret key.
- `DJANGO_DEBUG`: Set to `True` for development or `False` for production.
- `DJANGO_ALLOWED_HOSTS`: Set to your domain or `*` for local testing.

You can create a `.env` file at the root of your project and add the following:

```bash
DJANGO_SECRET_KEY='your_secret_key'
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
```

### 5. Configure Database (PostgreSQL)

If you're using PostgreSQL, make sure you have it installed and set up a new database. Update your `DATABASES` setting in `settings.py` to match your local PostgreSQL credentials:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database_name',
        'USER': 'your_database_user',
        'PASSWORD': 'your_database_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 6. Apply Migrations

Apply the database migrations to set up your database schema:

```bash
python manage.py migrate
```

### 7. Create a Superuser

To access the Django admin, create a superuser:

```bash
python manage.py createsuperuser
```

Follow the prompts to create a superuser account.

### 8. Run the Development Server

Start the Django development server:

```bash
python manage.py runserver
```

You can now access the application at [http://127.0.0.1:8000](http://127.0.0.1:8000).
