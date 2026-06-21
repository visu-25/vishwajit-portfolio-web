# Deploy Portfolio on Vercel

Vercel has zero-config Django support. This project includes `pyproject.toml` with the WSGI entrypoint and a build script that runs migrations and seeds case studies.

## Prerequisites

1. A [Vercel account](https://vercel.com/signup)
2. Your GitHub repo connected: `visu-25/vishwajit-portfolio-web`
3. A **PostgreSQL database** reachable from the public internet  
   - If you use Render Postgres, copy the **External Database URL** (not the Internal URL)
4. A Django `SECRET_KEY` (generate with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)

## Option A — Deploy from Vercel Dashboard (recommended)

1. Go to [vercel.com/new](https://vercel.com/new)
2. Import `visu-25/vishwajit-portfolio-web`
3. Framework Preset should auto-detect **Django**
4. Leave Build Command empty (uses `pyproject.toml` → `bash build.sh`)
5. Add **Environment Variables** (Production + Preview):

   | Variable | Value |
   |----------|-------|
   | `DJANGO_SETTINGS_MODULE` | `portfolio.settings.production` |
   | `SECRET_KEY` | your random secret key |
   | `DATABASE_URL` | Render **External** Postgres URL |
   | `SECURE_SSL_REDIRECT` | `true` |

6. Click **Deploy**
7. After deploy, open the site URL (e.g. `https://your-project.vercel.app`)
8. Create admin user (run locally against production DB):

   ```bash
   DJANGO_SETTINGS_MODULE=portfolio.settings.production \
   DATABASE_URL="your-external-url" \
   SECRET_KEY="your-key" \
   python manage.py createsuperuser
   ```

## Option B — Deploy with Vercel CLI

```bash
npm i -g vercel
vercel login
vercel link
vercel env add SECRET_KEY
vercel env add DATABASE_URL
vercel env add DJANGO_SETTINGS_MODULE   # portfolio.settings.production
vercel --prod
```

## How it works

- `pyproject.toml` tells Vercel to use `portfolio.wsgi:application`
- `build.sh` runs `collectstatic`, `migrate`, and `seed_case_studies` on each deploy
- `production.py` adds `.vercel.app` and `VERCEL_URL` to `ALLOWED_HOSTS` automatically
- Static files are served via WhiteNoise + Vercel CDN

## Notes

- Django on Vercel runs as a **single serverless function** — expect cold starts on the free tier
- **Media uploads** (admin file fields) do not persist on serverless; use external storage for production media
- Use the **External** Postgres URL from Render; Internal URLs only work inside Render's network
- Custom domain: Vercel dashboard → Project → Settings → Domains

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `DisallowedHost` | Redeploy after env vars are set; `VERCEL_URL` is added automatically |
| Build fails on `migrate` | Check `DATABASE_URL` is the **external** URL and SSL is enabled |
| Static files 404 | Ensure build completed; check `collectstatic` in deploy logs |
| CSRF error on contact form | Confirm site is accessed via `https://` and `SECURE_SSL_REDIRECT=true` |
