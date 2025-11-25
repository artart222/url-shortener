# url-shortener

## A url shortener + analytics

This is a URL shortening service with built-in analytics, built using Django REST Framework. This project allows you to generate short links, track clicks, and gain insights about your users’ behavior. Ideal for developers and teams who want a lightweight but fully-featured link management tool.


## ✨ Features

URL Shortening: Create short URLs from long links quickly.

Analytics: Track visitor IP, browser, operating system, and country for each click.

JWT Authentication: Secure your API endpoints with JSON Web Tokens.

Async Processing: Background tasks (like analytics logging) handled with Celery.

Simple Setup: Ready to run locally or deploy to production.

## 🚀 Quick Start

Generate short URLs and track analytics in minutes.

### 1. Clone the repository
```
git clone https://github.com/artart222/url-shortener.git
cd url-shortener
```

### 2. Create and activate a virtual environment
```
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies
```
pip install -r requirements.txt
```

### 4. Configure your environment

If you want you can make an .env file and put ***django*** SECRET_KEY in it


### 5. Apply migrations
```
python manage.py makemigrations
python manage.py migrate
```

### 6. Run the server
```
python manage.py runserver
```

Your API is now live at ***http://127.0.0.1:8000/***

## 🏗️ Project Structure

```
url-shortener
├── LICENSE
├── README.md
├── URL Shortener API
│   ├── add new URL.bru
│   ├── bruno.json
│   └── list all items.bru
├── analytics
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   ├── 0002_rename_shortener_analytics_shortener_id_and_more.py
│   │   └── __init__.py
│   ├── models.py
│   ├── serializer.py
│   ├── tasks.py
│   ├── tests.py
│   └── views.py
├── config
│   ├── __init__.py
│   ├── asgi.py
│   ├── celery.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── db.sqlite3
├── geoip
│   └── dbip-country-lite-2025-11.mmdb
├── main.py
├── manage.py
├── requirements.txt
└── shortener
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── base62.py
    ├── migrations
    │   ├── 0001_initial.py
    │   ├── 0002_alter_shortener_shortened_url.py
    │   ├── 0003_analytics.py
    │   ├── 0004_delete_analytics.py
    │   ├── 0005_shortener_base62_code.py
    │   └── __init__.py
    ├── models.py
    ├── serializer.py
    ├── tests.py
    └── views.py
```

## 🔧 How It Works

### URL Creation:

POST requests to /api/shortener/urls/ with the ***request body*** of ``` {"original_url": "string"} ``` create a short link.

### Redirection:

Visiting ``` URL_SHORTENER_BASE/<short_code>/ ``` redirects the user to the original URL.

URL_SHORTENER_BASE is defined in settings.py and by default it is localhost

### Analytics Tracking:
Each visit logs IP, browser, OS, and geolocation in the Analytics model.

### Background Tasks:
Analytics recording can be handled asynchronously with Celery to keep redirects fast.

## API Endpoints:

``` POST /api/shortener/url/ json-body: {original_url: "string"} ``` ==> create short URL

``` GET  /<code>/ ```                                          ==> redirect to original URL

``` GET  /api/shortener/urls/ ```                              ==> list all short URL

``` GET  /api/shortener/url/<code>/ ```                        ==> details for a specific short URL

``` GET  /api/analytics/ ```                                   ==> list all analytics records

``` GET  /api/analytics/<code>/ ```                          ==> get specific analytics record

## 🛠️ Tech Stack

Backend: Python 3.10+, Django, Django REST Framework

Async Tasks: Celery

Database: SQLite

Analytics: Custom Django models and Celery async logging

Authentication: JWT

## 📝 License

Distributed under the MIT License. See LICENSE for details.

## 🙋‍♂️ Why I Built This

I built this project to explore Python API development, async processing with Celery, and building a production-ready service with full analytics capabilities. It demonstrates clean Django architecture and REST API design with JWT authentication.
