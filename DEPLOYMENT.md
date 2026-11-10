# KejaConnect free demo hosting preparation

Recommended demo setup: a Render free web service, Neon free PostgreSQL, and Cloudinary free image storage. Render's free web service sleeps after 15 minutes without incoming traffic and its filesystem is temporary, so it cannot store landlord uploads. The app can now read a Neon `DATABASE_URL` and serve collected static assets, but property image storage must be connected to Cloudinary before deploying real listings or enabling image uploads.

Free hosting is suitable for a low-traffic demonstration. It is not a reliable production setup: free quotas can pause the service, and free plans and limits can change.

## Required production settings

Set these in the hosting provider's private environment settings. Do not commit their values to the project:

| Variable | Purpose |
| --- | --- |
| `KEJACONNECT_DEBUG` | Set to `False` in production. |
| `KEJACONNECT_SECRET_KEY` | A unique, randomly generated Django signing key. |
| `KEJACONNECT_ALLOWED_HOSTS` | Comma-separated hostnames, such as `keja.example,www.keja.example`. |
| `KEJACONNECT_CSRF_TRUSTED_ORIGINS` | Comma-separated full origins including `https://`. |
| `DATABASE_URL` | PostgreSQL connection URL from Neon. SSL is required in production. Alternatively, use the individual `KEJACONNECT_DB_*` variables. |
| `KEJACONNECT_DB_HOST` | Hostname of the production PostgreSQL database when not using `DATABASE_URL`. |
| `KEJACONNECT_DB_NAME` | Database name; defaults to `keja_connect_db`. |
| `KEJACONNECT_DB_USER` | Database user; defaults to `postgres`. |
| `KEJACONNECT_DB_PASSWORD` | Production database password. |
| `KEJACONNECT_DB_PORT` | Database port; defaults to `5432`. |
| `KEJACONNECT_MEDIA_ROOT` | Persistent directory for uploaded property photos on a host that supports a persistent disk. Render's free web service does not. |

`KEJACONNECT_HTTPS` defaults to `True` when debug mode is off. Keep it enabled only when the app is served through HTTPS and the hosting proxy sets `X-Forwarded-Proto` correctly. `KEJACONNECT_HSTS_SECONDS` defaults to `0`; enable HSTS after HTTPS has been confirmed on the live domain.

## Release steps

1. Create accounts for Render, Neon, and Cloudinary. Keep database and Cloudinary credentials private in the hosting provider's environment settings.
2. Install the pinned application dependencies with `pip install -r requirements.txt`.
3. Run `python manage.py migrate --noinput` and `python manage.py collectstatic --noinput` during release.
4. Create a staff administrator with `python manage.py createsuperuser` so listing moderation is available at `/admin/`.
5. Seed the Kenya county list if the production database is empty: `python manage.py seed_counties`.
6. Connect Cloudinary-backed storage and transfer the existing `properties/` photos before the public launch. Do not rely on Render's local filesystem for uploads.
7. Initialize or connect a private GitHub repository, then connect it to Render. Review the files and remove any local database, credentials, or private user data before pushing.
8. Create a staff administrator, then confirm the site's sign-up, enquiry, landlord inbox, image upload, and admin approval flows on the deployed URL.

The app now recognizes Render's assigned hostname, configures the matching HTTPS CSRF origin, parses `DATABASE_URL`, and uses WhiteNoise for static files. No external account was created and no code, listing, or photo has been uploaded.
