# Wagtail Starter Kit

A boilerplate Wagtail CMS project built on Django 6, PostgreSQL, htmx, and Sass.

## Prerequisites

- Python 3.14+
- PostgreSQL
- Node.js (for Sass compilation)
- [libpq](https://formulae.brew.sh/formula/libpq) (PostgreSQL client libraries, required to build `psycopg2`)

On macOS:

```bash
brew install postgresql libpq
echo 'export PATH="/opt/homebrew/opt/libpq/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

## Local setup

All commands run from the `site/` directory.

**1. Create and activate a virtual environment**

```bash
cd site
python -m venv venv
source venv/bin/activate
```

**2. Install Python dependencies**

```bash
pip install -r requirements.txt
```

**3. Install the local form builder dependency**

This project depends on a fork of [wagtail-advanced-form-builder](https://github.com/andreobrien/wagtail-advanced-form-builder). Clone it and install it in editable mode:

```bash
git clone https://github.com/andreobrien/wagtail-advanced-form-builder.git
pip install -e /path/to/wagtail-advanced-form-builder
```

> Replace `/path/to/wagtail-advanced-form-builder` with wherever you cloned it.

**4. Install Node dependencies**

```bash
npm install
```

**5. Create a `.env` file**

Create `site/.env` with the following (minimum required):

```env
DJANGO_SECRET_KEY=your-secret-key-here
DATABASE_URL=postgres://username:password@localhost:5432/your_db_name
DJANGO_DEBUG=True
DOMAIN=localhost
```

Optional settings:

```env
RECAPTCHA_PUBLIC_KEY=
RECAPTCHA_PRIVATE_KEY=
EMAIL_HOST=localhost
EMAIL_PORT=1025
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL=
FORM_SUBMISSION_EMAIL=
```

Generate a secret key with:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**6. Create the database**
Optional, depending if/how you choose to run Postgres:~~~~

```bash
brew services start postgresql
createdb your_db_name
createuser admin --createdb # or however you prefer to create a db role
```

**7. Run migrations**

```bash
python manage.py migrate
```

**8. Create a superuser**

```bash
python manage.py createsuperuser
```

**9. Start the development server**

```bash
python manage.py runserver
```

The site will be at http://localhost:8000 and the Wagtail admin at http://localhost:8000/admin.

## CSS

Compile Sass once:

```bash
npm run build
```

Or watch for changes during development:

```bash
npm run watch
```

## Docker

Build the image:

```bash
docker build -t wagtail-starter-kit .
```

Run the container (pass environment variables via `--env-file` or `-e`):

```bash
docker run -p 8000:8000 --env-file .env wagtail-starter-kit
```

The container runs migrations and starts Gunicorn on port 8000 automatically.

> **Note:** For production deployments, running migrations in the `CMD` is a convenience shortcut. Use your platform's release phase or run migrations manually before deploying.

## Project structure

```
site/
├── base/           # Shared models, blocks, mixins, templatetags
├── home/           # Home app (default Wagtail landing page)
├── project/        # Django project: settings, URLs, templates, static files
│   ├── settings/
│   │   ├── base.py
│   │   └── dev.py
│   ├── static/
│   │   └── sass/   # Sass source files
│   └── templates/
├── search/         # Wagtail search view
├── manage.py
├── requirements.txt
└── Dockerfile
```

## Settings

Settings are split into `base.py` (shared) and `dev.py` (local overrides). `manage.py` defaults to `project.settings.dev`.

All configuration is loaded from environment variables via [python-decouple](https://github.com/HBNetwork/python-decouple). Place them in `site/.env` for local development.
