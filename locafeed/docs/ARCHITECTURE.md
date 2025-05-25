# LocaFeed Application Architecture

## Overview

LocaFeed is a location-based social media application that allows users to post short messages with location data. The application features user authentication, message posting with location tagging, an interactive map, and an API for data access.

## Technology Stack

- **Backend**: Django (Python web framework)
- **Database**: SQLite (can be migrated to other DB systems)
- **Frontend**: Bootstrap (responsive design), jQuery (JavaScript)
- **Map Integration**: Leaflet.js (interactive maps)
- **Package Manager**: Poetry (for dependency management)

## Application Structure

### 1. Entity Relationship Diagram (ERD)

#### Core Entities

- **User**
  - id (PK)
  - username
  - password
  - email
  - date_joined
  - last_login

- **Post**
  - id (PK)
  - user_id (FK to User)
  - content (max 140 characters)
  - created_at
  - location_name
  - latitude
  - longitude

### 2. Application Pages

#### a. Login Page

- Username and password form
- Error notification for invalid credentials
- Redirect to Dashboard upon successful login

#### b. Dashboard

- Display posts with pagination (5 posts per page)
- Each post shows:
  - Date and time of posting
  - Username
  - Message content
  - Clickable location link to map view
- Navigation to other app sections

#### c. Map Page

- Interactive map using Leaflet.js
- Display marker for selected post location
- Pop-up with post details when marker is clicked
- Return option to Dashboard

#### d. API Page

- Documentation of available endpoints
- Access to post data in JSON format
- Authentication requirements

### 3. Application Flow

```ascii
┌───────────┐    success    ┌───────────┐     click      ┌───────────┐
│           │──────────────▶│           │───location────▶│           │
│  Login    │               │ Dashboard │                │   Map     │
│           │◀──────────────│           │◀───────────────│           │
└───────────┘     back      └───────────┘     back       └───────────┘
                                ▲
                                │
                                │
                                ▼
                           ┌───────────┐
                           │           │
                           │    API    │
                           │           │
                           └───────────┘
```

## Features Implementation

### 1. User Authentication

- Django's built-in authentication system
- Form validation with error notifications
- Session management for logged-in users

### 2. Post Creation

- Text limited to 140 characters
- Required location data (name and coordinates)
- Timestamp recording for each post

### 3. Dashboard

- Chronological display of posts (newest first)
- Pagination (5 posts per page)
- Location hyperlinks to map view

### 4. Map Integration

- Leaflet.js for interactive maps
- Marker placement based on post coordinates
- Information pop-ups with post details

### 5. API Endpoints

- GET `/api/posts/` - List all posts
- GET `/api/posts/{id}/` - Get specific post details
- Authentication required for API access

## Directory Structure

```text
locafeed/
├── core/                  # Main application
│   ├── models.py          # Data models
│   ├── views.py           # View controllers
│   ├── urls.py            # URL routing
│   ├── forms.py           # Form definitions
│   ├── admin.py           # Admin interface
│   └── templates/         # HTML templates
├── locafeed/              # Project settings
│   ├── settings.py        # Configuration
│   ├── urls.py            # Main URL routing
│   └── wsgi.py            # WSGI configuration
├── static/                # Static assets
│   ├── css/               # Stylesheets
│   ├── js/                # JavaScript files
│   └── images/            # Image assets
├── docs/                  # Documentation
│   ├── TASK.md            # Requirements
│   └── ARCHITECTURE.md    # This document
└── manage.py              # Django management script
```

## Deployment Instructions

### Local Development Environment Setup

1. **Clone the repository**

2. **Activate Poetry shell**

   ```bash
   # Ensure Poetry is installed (https://python-poetry.org/docs/#installation)
   # Activate the Poetry shell
   poetry shell  # This activates the virtual environment (code-test-mFtvg3Ha-py3.12)
   ```

3. **Install dependencies**

   ```bash
   poetry install  # Installs all dependencies defined in pyproject.toml
   ```

4. **Run migrations**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser**

   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server**

   ```bash
   poetry run python manage.py runserver  # Run through Poetry
   # Or if you're already in Poetry shell:
   python manage.py runserver
   ```

> **Important**: Always use Poetry for managing dependencies and running Python commands. If you need to add a new package, use `poetry add package-name` instead of pip.

### Production Deployment

1. **Configure production settings in `settings.py`**
   - Set `DEBUG = False`
   - Update `ALLOWED_HOSTS`
   - Configure secure cookies

2. **Set up a web server (Nginx/Apache)**

3. **Configure WSGI (Gunicorn)**

   ```bash
   poetry run gunicorn locafeed.wsgi:application  # Run through Poetry
   ```

4. **Set up SSL certificate**

5. **Configure database (if not using SQLite)**

6. **Deploy to hosting service**
