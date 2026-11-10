# KejaConnect hosting: Render + Neon + Cloudinary

Render runs the existing Django website. Neon provides a separate PostgreSQL database, so KejaConnect does not use the salon database. Cloudinary stores landlord photos so they survive Render restarts.

## Prepare the free services

1. Create a free Neon PostgreSQL project and copy its connection string. Use Neon's pooled connection string if shown.
2. Create a free Cloudinary account and copy the `CLOUDINARY_URL` from its API environment settings.
3. Keep both values private. Enter them only in Render's Blueprint secret prompts; never commit them to GitHub or send them in chat.

## Create the Render service

The earlier failed Blueprint has no resources. Create a **new Blueprint instance** from `Milin-droid/keja-connect`, branch `main`, file `render.yaml`. Use a name such as `keja-connect-neon`.

During its initial setup, Render prompts for `DATABASE_URL` and `CLOUDINARY_URL`. Paste the Neon connection string and Cloudinary URL into their matching prompts. The Blueprint creates one free web service and does not create or change a Render database.

The build applies Django migrations, seeds the Kenya counties, and gathers static files. Render provides the HTTPS hostname and generated Django secret key.

## Free-tier limits

Render's free web service sleeps when idle. Neon and Cloudinary have their own free usage limits. This is suitable for a demo; monitor the providers' usage pages as activity grows.
