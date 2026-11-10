# KejaConnect free Render hosting

The repository includes `render.yaml`, which creates a Render free web service and Render free PostgreSQL database. The deployment installs the requirements, gathers static files, applies migrations, seeds Kenya counties, and starts Django with Gunicorn.

This is a no-cost demo setup. Render free web services sleep after 15 minutes without traffic and have temporary local filesystems. Therefore, property photo uploads can disappear after restart or redeployment. Render free PostgreSQL databases expire after 30 days. Free services are intended for demos and hobby use, not production data.

## Deploy

1. Open the Render dashboard and choose **New → Blueprint**.
2. Connect the public GitHub repository `Milin-droid/keja-connect`.
3. Select branch `main` and apply the blueprint from `render.yaml`.
4. Wait for the build to complete, then open the service URL ending in `.onrender.com`.

Render provides `DATABASE_URL`, assigns a secure Django secret key, and exposes its service hostname automatically. The included Django settings configure the database, HTTPS host, CSRF origin, and static files.

## Admin moderation

The free Render web service does not provide a shell. To create the first admin user, run Django from a local terminal configured with the Render `DATABASE_URL` and `KEJACONNECT_DEBUG=False`, then run `python manage.py createsuperuser`. Keep the database URL private.

## Property photos

Uploads are enabled, but on this free setup files are stored temporarily on the web service. Use only demo listings until durable media storage is configured.
