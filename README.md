# YantrAI

Marketing website for YantrAI — AI agents that know your business.

## Stack

Static HTML + CSS + minimal JavaScript frontend with a small Flask backend for form delivery.

```
index.html      Home page
styles.css      All styles (Manrope, gradient brand, dark + light sections)
script.js       Scroll-reveal + agent tabs + mobile menu + demo form submit
main.py         Flask app serving site + /api/book-demo endpoint
requirements.txt Python dependencies for App Engine runtime
assets/team/    Founder portraits
```

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

Then open `http://127.0.0.1:8080/`.

## Demo form email configuration

Set SMTP credentials before deploying so `Book a demo` sends email to `rohit@yantrailabs.com`:

```bash
export SMTP_HOST="smtp.gmail.com"
export SMTP_PORT="587"
export SMTP_USER="your-smtp-username"
export SMTP_PASS="your-smtp-password-or-app-password"
export DEMO_FROM_EMAIL="no-reply@yantrailabs.com"
export DEMO_TO_EMAIL="rohit@yantrailabs.com"
```

## Deploy to Google App Engine

```bash
gcloud config set project yantraivisionos
gcloud app create --region=asia-south1
gcloud app deploy
```

Run `gcloud app create` only once per Google Cloud project. If App Engine already exists for the project, skip that command.

After deploy, open the URL printed by `gcloud`.

If the first deploy fails because the App Engine service account cannot access `staging.yantraivisionos.appspot.com`, grant it Storage Admin and redeploy:

```bash
gcloud projects add-iam-policy-binding yantraivisionos \
  --member="serviceAccount:yantraivisionos@appspot.gserviceaccount.com" \
  --role="roles/storage.admin"

gcloud app deploy
```

If the build then fails with `artifactregistry.repositories.downloadArtifacts` for `asia.gcr.io/yantraivisionos/app-engine-tmp`, grant Artifact Registry create-on-push access and redeploy:

```bash
gcloud services enable artifactregistry.googleapis.com

gcloud projects add-iam-policy-binding yantraivisionos \
  --member="serviceAccount:yantraivisionos@appspot.gserviceaccount.com" \
  --role="roles/artifactregistry.createOnPushWriter"

gcloud app deploy
```

## Connect a GoDaddy Domain

In Google Cloud Console, go to App Engine > Settings > Custom Domains. Add a custom domain, verify the naked domain, then map both the naked domain and `www` subdomain.

After Google shows the DNS records, open GoDaddy > My Products > Domains > DNS for the domain and add the records Google provides. Typically this means `A` and `AAAA` records with host `@` for the naked domain, and a `CNAME` record with host `www` for the `www` subdomain.

Use Google's displayed record values as the source of truth. After saving DNS changes, wait for propagation and for App Engine's managed SSL certificate to become active.

## Sections

1. Hero — *AI agents that know your business.* + memory graph
2. Customer logos
3. Three pillars — Remember · Act · Govern (dark)
4. Memory Layer flow — Sources → Memory → Agents
5. Agent tabs — Retail · Productivity · Custom (with in-page demo CTA links)
6. Integrations — connector chips on gradient
7. How we deploy — 4 commitments
8. Team — founder cards
9. Book a demo — full form, response within 2 hours, backend email delivery

## Contact

rohit@yantrailabs.com · +91 96434 98089
