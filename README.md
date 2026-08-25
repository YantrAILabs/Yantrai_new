# yantrailabs.com

Flask app serving the **AiFA — AI Teams for Finance** landing page at `/`.

## Where this actually runs

**Cloud Run**, service `yantrai-website`, project `gen-lang-client-0024674990`,
region `asia-south1`. Not App Engine — `app.yaml` survives only because the
Python buildpack reads its `entrypoint`; its `handlers` and `env_variables` are
ignored, and the `yantraivisionos` project it references has billing disabled.

Every request goes through `main.py`. There is no static-file layer in front.

## Layout

```
aifa/            the site — built elsewhere, see below
legacy/          the previous company site, kept for reference, NOT deployed
main.py          routes + the two form endpoints
robots.txt, sitemap.xml
```

| Route | Serves |
|---|---|
| `/` | `aifa/index.html` |
| `/<path>` | files from the repo root; anything under `legacy/` is 404 |
| `POST /api/savings-check` | the AiFA form → email |
| `POST /api/book-demo` | the old company-site form → email |

`legacy/` is excluded by `.gcloudignore`, so it never reaches the container.

## Deploying

Pushing to `main` deploys automatically (`.github/workflows/deploy.yml`).
To deploy by hand:

```bash
gcloud run deploy yantrai-website --source . \
  --region asia-south1 --project gen-lang-client-0024674990
```

## Email configuration

Both form endpoints need these set **on the Cloud Run service** — `app.yaml`'s
`env_variables` do nothing here:

`SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `DEMO_FROM_EMAIL`, `DEMO_TO_EMAIL`,
and `SMTP_PASS` (mounted from the `smtp-pass` secret).

Without them `_send_mail()` returns 500 "Email service not configured" and the
forms fail — which is what was happening before August 2026.

## Changing the AiFA page

The page is generated from a Claude Design canvas, not hand-edited here. Source
and build instructions: `~/Desktop/memory/aifa_site/README.md`. Build with the
sub-path prefix and copy in:

```bash
cd ~/Desktop/memory/aifa_site
AIFA_BASE=aifa AIFA_FORM_ENDPOINT=/api/savings-check \
AIFA_SITE_URL=https://yantrailabs.com python3 build.py
cp index.html site.css app.js ~/Desktop/memory/Yantrai_new/aifa/
rsync -a assets/ ~/Desktop/memory/Yantrai_new/aifa/assets/
```

## Local

```bash
python3 -m venv .venv-local && ./.venv-local/bin/pip install -r requirements.txt
./.venv-local/bin/python main.py     # :8080
```
