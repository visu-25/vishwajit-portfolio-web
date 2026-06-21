# Render Deployment Guide

Deploy the Django portfolio to [Render](https://render.com) with PostgreSQL, Gunicorn, and WhiteNoise.

**GitHub repo:** [visu-25/vishwajit-portfolio-web](https://github.com/visu-25/vishwajit-portfolio-web)

**Render project:** [Open Web Service setup](https://dashboard.render.com/project/prj-ctsg509u0jms73baahl0/environment/evm-ctsg509u0jms73baahlg/web/new)

---

## Prerequisites

- GitHub repo pushed and up to date
- [Render account](https://dashboard.render.com/) (free tier works)
- Render connected to your GitHub account

---

## Option A — Docker (Render auto-detects this)

If Render shows **Language: Docker** (because the repo has a `Dockerfile`), use these settings on the [New Web Service](https://dashboard.render.com/project/prj-ctsg509u0jms73baahl0/environment/evm-ctsg509u0jms73baahlg/web/new) page:

| Field | Value |
|-------|-------|
| **Source Code** | `visu-25 / vishwajit-portfolio-web` |
| **Name** | `vishwajit-portfolio-web` |
| **Language** | **Docker** *(auto-detected — keep it)* |
| **Branch** | `main` |
| **Region** | Oregon (US West) or nearest to you |
| **Root Directory** | *(leave blank)* |
| **Instance Type** | Free |

No separate Build/Start command is needed — the `Dockerfile` and `entrypoint.sh` handle everything.

### Environment variables (required)

Scroll to **Environment Variables** and add:

| Key | Value |
|-----|-------|
| `DJANGO_SETTINGS_MODULE` | `portfolio.settings.production` |
| `SECRET_KEY` | Generate a random key (see Step 3 below) |
| `DATABASE_URL` | Link from **portfolio-db** → Internal Database URL |
| `SECURE_SSL_REDIRECT` | `true` |

### Email notifications (contact form)

**Render free tier blocks SMTP ports 587/465.** Gmail SMTP will time out on free instances.
Use one of these options:

#### Option 1 — Resend via HTTPS (recommended on Render free tier)

1. Create a free account at [resend.com](https://resend.com) **using the same email where you want alerts** (`vishwajit25401@gmail.com`)
2. Create an API key
3. Add to Render environment variables:

| Key | Value |
|-----|-------|
| `RESEND_API_KEY` | your Resend API key |
| `RESEND_FROM_EMAIL` | `Portfolio <onboarding@resend.dev>` |
| `CONTACT_NOTIFICATION_EMAIL` | `vishwajit25401@gmail.com` *(must match your Resend signup email until you verify a domain)* |
| `SITE_URL` | `https://vishwajit-portfolio-web.onrender.com` |

> **Important:** With the free test sender `onboarding@resend.dev`, Resend only delivers to **your Resend account email**. Do **not** use `parmardummy@gmail.com` in `RESEND_FROM_EMAIL` — that causes **403 Forbidden**.

> To send to any address, verify your own domain at [resend.com/domains](https://resend.com/domains) and set e.g. `RESEND_FROM_EMAIL=Portfolio <hello@yourdomain.com>`.

When `RESEND_API_KEY` is set, the app sends email over HTTPS (port 443) instead of SMTP.

#### Option 2 — Gmail SMTP (paid Render instance only)

| Key | Value |
|-----|-------|
| `EMAIL_HOST` | `smtp.gmail.com` |
| `EMAIL_PORT` | `587` |
| `EMAIL_USE_TLS` | `true` |
| `EMAIL_HOST_USER` | `parmardummy@gmail.com` *(send account)* |
| `EMAIL_HOST_PASSWORD` | Gmail App Password for send account |
| `DEFAULT_FROM_EMAIL` | `Portfolio <parmardummy@gmail.com>` |
| `CONTACT_NOTIFICATION_EMAIL` | `vishwajit25401@gmail.com` *(receive alerts)* |
| `SITE_URL` | `https://vishwajit-portfolio-web.onrender.com` |

> **Send from:** `parmardummy@gmail.com` · **Receive at:** `vishwajit25401@gmail.com`

> Messages are always saved in Django Admin even if email delivery fails.

> `RENDER_EXTERNAL_HOSTNAME` is set automatically by Render.

Click **Create Web Service** when done.

---

## Option B — Python 3 (no Docker)

If you prefer **Python 3** instead of Docker, change **Language** from Docker to **Python 3** on the same form.

| Field | Value |
|-------|-------|
| **Build Command** | `./build.sh` |
| **Start Command** | `gunicorn portfolio.wsgi:application --bind 0.0.0.0:$PORT` |

Add the same environment variables as Option A, plus:

| Key | Value |
|-----|-------|
| `PYTHON_VERSION` | `3.12.3` |
| `WEB_CONCURRENCY` | `4` |

---

## Option C — Manual Setup (full walkthrough)

Follow these steps in the Render dashboard.

### Step 1: Create PostgreSQL Database

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **New +** → **PostgreSQL**
3. Configure:
   - **Name:** `portfolio-db`
   - **Database:** `portfolio`
   - **User:** `portfolio`
   - **Plan:** Free (or Starter for production)
4. Click **Create Database**
5. Wait until status is **Available**
6. Copy the **Internal Database URL** (used when web service is on Render)

### Step 2: Create Web Service

1. Open your project web service page:  
   [Create Web Service](https://dashboard.render.com/project/prj-ctsg509u0jms73baahl0/environment/evm-ctsg509u0jms73baahlg/web/new)
2. Connect **GitHub** → select repo **`visu-25/vishwajit-portfolio-web`**
3. Use **Option A (Docker)** or **Option B (Python 3)** settings above.

4. Click **Advanced** → add environment variables:

| Key | Value |
|-----|-------|
| `DJANGO_SETTINGS_MODULE` | `portfolio.settings.production` |
| `SECRET_KEY` | Generate a long random string (see below) |
| `DATABASE_URL` | Link from **portfolio-db** → Internal Database URL |
| `SECURE_SSL_REDIRECT` | `true` |

   Render sets `RENDER_EXTERNAL_HOSTNAME` automatically — no need to add it manually.

5. Click **Create Web Service**

### Step 3: Generate SECRET_KEY

Run locally:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Paste the output into Render as `SECRET_KEY`.

### Step 4: First Deploy

Render will automatically:

1. Install dependencies from `requirements.txt`
2. Run `collectstatic` (via `build.sh`)
3. Run database migrations
4. Seed case studies
5. Start Gunicorn

Watch the **Logs** tab. A successful deploy ends with:

```
Your service is live at https://vishwajit-portfolio-web.onrender.com
```

### Step 5: Create Admin User

After the first successful deploy, open **Shell** in the Render web service dashboard and run:

```bash
python manage.py createsuperuser
```

Then visit:

- Site: `https://<your-service>.onrender.com`
- Admin: `https://<your-service>.onrender.com/admin/`

---

## Option D — Blueprint (render.yaml)

Deploy database + web service in one step using the included [`render.yaml`](render.yaml).

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **New +** → **Blueprint**
3. Connect repo **`visu-25/vishwajit-portfolio-web`**
4. Render reads `render.yaml` and creates:
   - PostgreSQL: `portfolio-db`
   - Web Service: `vishwajit-portfolio-web`
5. Click **Apply**
6. After deploy, run `createsuperuser` in the Shell (Step 5 above)

---

## Environment Variables Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `DJANGO_SETTINGS_MODULE` | Yes | `portfolio.settings.production` |
| `SECRET_KEY` | Yes | Django secret key (50+ random chars) |
| `DATABASE_URL` | Yes | Auto-linked from Render PostgreSQL |
| `RENDER_EXTERNAL_HOSTNAME` | Auto | Set by Render (e.g. `*.onrender.com`) |
| `PYTHON_VERSION` | Recommended | `3.12.3` |
| `WEB_CONCURRENCY` | Optional | Gunicorn workers (default `4`) |
| `SECURE_SSL_REDIRECT` | Optional | `true` on Render |
| `ALLOWED_HOSTS` | Optional | Extra custom domains, comma-separated |

---

## Custom Domain (Optional)

1. In Render web service → **Settings** → **Custom Domains**
2. Add your domain (e.g. `portfolio.yourdomain.com`)
3. Update DNS as Render instructs
4. Add the domain to `ALLOWED_HOSTS` in Render env vars:

```
ALLOWED_HOSTS=portfolio.yourdomain.com,www.portfolio.yourdomain.com
```

---

## Media / Uploaded Files

On Render’s free tier, the filesystem is **ephemeral**. Case study images uploaded via Django Admin are lost on redeploy.

For production uploads, use external storage (e.g. AWS S3, Cloudinary). Until then, seed data and static assets work fine; re-upload images after redeploys if needed.

---

## Troubleshooting

### Build fails on `collectstatic`

- Check **Logs** for missing static files
- Ensure `build.sh` is executable in repo: `chmod +x build.sh`

### `DisallowedHost` error

- Confirm `RENDER_EXTERNAL_HOSTNAME` is set (automatic on Render)
- For custom domains, add them to `ALLOWED_HOSTS`

### Database connection error

- Use **Internal Database URL** (not External) for the web service
- Verify `DATABASE_URL` is linked to `portfolio-db`

### CSRF error on contact form

- Production settings add `CSRF_TRUSTED_ORIGINS` from allowed hosts
- Ensure you access the site via `https://` not `http://`

### Free tier cold starts

- Free web services spin down after inactivity (~50 s first load)
- Upgrade to Starter plan for always-on service

---

## Redeploy After Code Changes

Push to GitHub `main` branch — Render auto-deploys:

```bash
git add .
git commit -m "Update portfolio"
git push origin main
```

Manual redeploy: Render dashboard → **Manual Deploy** → **Deploy latest commit**

---

## Local Production Test (Optional)

Test production settings locally before deploying:

```bash
export DJANGO_SETTINGS_MODULE=portfolio.settings.production
export SECRET_KEY=your-local-test-key
export DATABASE_URL=postgres://portfolio:portfolio@localhost:5432/portfolio
export ALLOWED_HOSTS=localhost,127.0.0.1

python manage.py collectstatic --no-input
python manage.py migrate
gunicorn portfolio.wsgi:application --bind 0.0.0.0:8000
```

---

## Quick Checklist

- [ ] PostgreSQL database created on Render
- [ ] Web service connected to GitHub repo
- [ ] `DJANGO_SETTINGS_MODULE=portfolio.settings.production`
- [ ] `SECRET_KEY` set
- [ ] `DATABASE_URL` linked to PostgreSQL
- [ ] Build command: `./build.sh`
- [ ] Start command: `gunicorn portfolio.wsgi:application --bind 0.0.0.0:$PORT`
- [ ] First deploy succeeded (check Logs)
- [ ] `createsuperuser` run in Shell
- [ ] Site loads at `https://<service>.onrender.com`
