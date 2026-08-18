# Portfolio Backend — Coolify Deployment Guide

## Prerequisites

- A [Coolify](https://coolify.io) instance (self-hosted or cloud)
- A PostgreSQL or MySQL database (can be created in Coolify)
- Backend code pushed to a Git repository (GitHub, GitLab, etc.)

---

## Step 1 — Create the Database in Coolify

1. Go to your Coolify dashboard → **Projects** → select your project
2. Click **+ New Resource** → **Database** → **PostgreSQL** (recommended) or **MySQL**
3. Note the internal connection URL — it will look like:
   ```
   postgresql://postgres:PASSWORD@PROJECT_ID-db:5432/postgres
   ```
4. You'll use this as `DATABASE_URL` in Step 3

---

## Step 2 — Create the Backend Service

1. In the same project, click **+ New Resource** → **Application**
2. Select your Git repository and branch
3. Set **Base Directory** to: `/backend` (if backend and frontend are in the same repo)
4. Set **Build Pack** to: **Dockerfile**
5. Coolify will auto-detect the `Dockerfile` in the backend folder
6. Set **Ports Exposes** to: `8000`

---

## Step 3 — Set Environment Variables

Go to the service **Environment Variables** tab and add:

| Variable | Value | Required |
|---|---|---|
| `SECRET_KEY` | A long random string (use `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`) | **Yes** |
| `DEBUG` | `False` | **Yes** |
| `ALLOWED_HOSTS` | `your-api.yourdomain.com` | **Yes** |
| `DATABASE_URL` | `postgresql://USER:PASS@HOST:5432/DBNAME` (use the internal URL from Step 1) | **Yes** |
| `FRONTEND_URL` | `https://your-frontend.yourdomain.com` | **Yes** |
| `CORS_ALLOWED_ORIGINS` | `https://your-frontend.yourdomain.com` | **Yes** |
| `CLOUDINARY_URL` | `cloudinary://KEY:SECRET@CLOUD` (only if using Cloudinary for media) | No |
| `PUBLIC_API_URL` | `https://your-api.yourdomain.com` (helps build correct absolute media URLs) | Recommended |
| `DB_SSL_REQUIRE` | `true` or `false` (default: `false`) | No |
| `FORCE_HTTPS_MEDIA` | `true` (set if media URLs come out as http) | No |

---

## Step 4 — Configure Domain

1. Go to the **Domains** / **Settings** tab of the service
2. Add your domain: `your-api.yourdomain.com`
3. Enable **HTTPS** (Coolify handles Let's Encrypt automatically)

---

## Step 5 — Deploy

1. Click **Deploy** in Coolify
2. The Dockerfile will:
   - Install Python dependencies
   - Run `python manage.py migrate --noinput` (auto on every deploy)
   - Run `collectstatic`
   - Start Gunicorn on port 8000

---

## Step 6 — Create Superuser (First Time Only)

After the first deploy, open the service **Terminal** in Coolify and run:

```bash
python manage.py createsuperuser
```

---

## Step 7 — Seed Initial Data (Optional)

```bash
python manage.py populate_initial_content --force
```

---

## Persistent Media Storage

If you are **not** using Cloudinary, you must add a **Volume Mount** in Coolify so uploaded files survive redeploys.

Use these exact values:

- `Type`: `Volume Mount`
- `Name`: `portfolio-backend-media`
- `Source Path`: leave empty if Coolify allows it, or keep the default Docker-managed volume path
- `Destination Path`: `/app/media`

Important:

- The only really important field here is `Destination Path = /app/media`
- Do **not** use `/tmp/root`
- Do **not** mount to `/app` or `/root`
- Do **not** use `File Mount`, `Host File Mount`, or `Directory Mount` for this case

Step by step in Coolify:

1. Open your backend resource
2. Go to **Persistent Storage**
3. Click **Add**
4. Choose **Volume Mount**
5. Set `Name` to something like `portfolio-backend-media`
6. Set `Destination Path` to `/app/media`
7. Save
8. Redeploy the backend

After that, Django uploads stored with local media will persist across redeploys.

---

## Health Check (Optional)

You can set the health check URL in Coolify to:

```
/api/profile/public/
```

This endpoint is public and returns a JSON response.

---

## Updating

Push to your Git branch → Coolify auto-deploys (if auto-deploy is enabled) or click **Deploy** manually.
