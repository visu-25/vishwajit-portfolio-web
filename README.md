# Vishwajit Parmar — Portfolio

Django-powered portfolio with HTML/CSS/JS frontend, PostgreSQL database, and Django Admin CMS for managing case studies.

## Features

- Public pages: Home, About, Skills, Experience, Case Studies, Contact
- Case studies managed via Django Admin (no code changes needed)
- Dark/light theme toggle, responsive mobile layout
- Contact form messages stored in database
- Docker Compose for local development with PostgreSQL

## Quick Start (SQLite — no Docker)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# Set USE_SQLITE=true in .env

python manage.py migrate
python manage.py seed_case_studies
python manage.py createsuperuser
python manage.py runserver
```

Visit http://127.0.0.1:8000 — Admin at http://127.0.0.1:8000/admin/

## Quick Start (Docker + PostgreSQL)

```bash
docker compose up --build
```

This runs migrations, seeds case studies, and starts the dev server on port 8000.

Create an admin user:

```bash
docker compose exec web python manage.py createsuperuser
```

## Environment Variables

Copy `.env.example` to `.env` and adjust:

| Variable | Description |
|----------|-------------|
| `DEBUG` | `True` for development |
| `SECRET_KEY` | Django secret key (required in production) |
| `ALLOWED_HOSTS` | Comma-separated hostnames |
| `USE_SQLITE` | `true` to use SQLite instead of PostgreSQL |
| `POSTGRES_*` | PostgreSQL connection settings |

## Production Deployment

1. Set `DJANGO_SETTINGS_MODULE=portfolio.settings.production`
2. Configure required env vars: `SECRET_KEY`, `POSTGRES_*`, `ALLOWED_HOSTS`
3. Run migrations and collect static files:

```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py seed_case_studies
```

4. Serve with Gunicorn (included in Dockerfile):

```bash
gunicorn portfolio.wsgi:application --bind 0.0.0.0:8000
```

### Recommended hosts

- **Railway** or **Render** — connect PostgreSQL add-on, set env vars, deploy from Dockerfile
- **VPS** — Nginx reverse proxy + Gunicorn + PostgreSQL

Production settings enforce HTTPS cookies and disable debug mode. See `portfolio/settings/production.py`.

## Project Structure

```
Portfolio/
├── core/                   # Models, views, admin, seed command
├── portfolio/              # Django settings (base + production)
├── templates/              # HTML templates
├── static/                 # CSS and JS
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## Managing Content

1. Log in to `/admin/`
2. Add or edit **Case Studies** — upload featured images, set publish/featured flags
3. View **Contact Messages** submitted via the contact form

## License

Private portfolio project.
