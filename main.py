import os
import smtplib
from email.message import EmailMessage

from flask import Flask, jsonify, request, send_from_directory
from google.cloud import secretmanager

app = Flask(__name__, static_folder=".", static_url_path="")


def _clean(value: str, max_len: int = 1000) -> str:
    text = (value or "").strip()
    return text[:max_len]


def _get_secret(resource_name: str) -> str:
    client = secretmanager.SecretManagerServiceClient()
    response = client.access_secret_version(name=resource_name)
    return response.payload.data.decode("utf-8")


@app.get("/")
def home():
    return send_from_directory(".", "index.html")


@app.get("/<path:path>")
def static_files(path: str):
    return send_from_directory(".", path)


@app.post("/api/book-demo")
def book_demo():
    payload = request.get_json(silent=True) or {}
    name = _clean(payload.get("name"), 120)
    company = _clean(payload.get("company"), 180)
    role = _clean(payload.get("role"), 120)
    mobile = _clean(payload.get("mobile"), 40)
    email = _clean(payload.get("email"), 180)
    challenge = _clean(payload.get("challenge"), 4000)

    if not name or not company or not role or not mobile:
        return jsonify({"ok": False, "error": "Missing required fields"}), 400

    smtp_host = os.getenv("SMTP_HOST")
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")
    smtp_pass_secret = os.getenv("SMTP_PASS_SECRET")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    recipient = os.getenv("DEMO_TO_EMAIL", "rohit@yantrailabs.com")
    sender = os.getenv("DEMO_FROM_EMAIL") or smtp_user

    if not smtp_pass and smtp_pass_secret:
        try:
            smtp_pass = _get_secret(smtp_pass_secret)
        except Exception:
            return jsonify({"ok": False, "error": "Failed to load SMTP secret"}), 500

    if not smtp_host or not smtp_user or not smtp_pass or not sender:
        return jsonify({"ok": False, "error": "Email service not configured"}), 500

    msg = EmailMessage()
    msg["Subject"] = f"New demo request: {company} ({name})"
    msg["From"] = sender
    msg["To"] = recipient
    msg["Reply-To"] = email or sender
    msg.set_content(
        "\n".join(
            [
                "New book-a-demo submission",
                "",
                f"Name: {name}",
                f"Company: {company}",
                f"Role: {role}",
                f"Mobile: {mobile}",
                f"Email: {email or 'Not provided'}",
                "",
                "Challenge:",
                challenge or "Not provided",
            ]
        )
    )

    try:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=20) as smtp:
            smtp.starttls()
            smtp.login(smtp_user, smtp_pass)
            smtp.send_message(msg)
    except Exception:
        return jsonify({"ok": False, "error": "Failed to send email"}), 502

    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
