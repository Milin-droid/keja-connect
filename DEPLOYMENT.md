# KejaConnect free Render hosting

This Render Blueprint creates a free KejaConnect web service and uses the existing `elegance-salon-db` PostgreSQL instance, because Render permits only one active free Postgres database per workspace. KejaConnect tables are placed in a separate `keja_connect` schema; the salon app's tables remain in `public`.

The database instance is shared, so both apps share its storage, connections, and free-tier expiration. Render free Postgres expires after 30 days. Render free web services sleep after 15 minutes without traffic and lose local uploads on restarts or redeploys. Property photos are temporary in this setup.

## Deploy

1. In the failed Blueprint's **Syncs** page, open the failed sync and choose **Manual sync** after the latest `render.yaml` update is pushed to GitHub.
2. Confirm that the only resource to create is the `keja-connect` web service. It should reference the existing `elegance-salon-db` database and must not create another database.
3. Wait for the service build and deploy to complete, then open its `.onrender.com` URL.

The build creates the `keja_connect` schema, applies Django migrations there, seeds the Kenya counties, and gathers static files. Do not paste the database connection URL into a public file or chat.
