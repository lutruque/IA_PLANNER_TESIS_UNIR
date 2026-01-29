import os, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

from pathlib import Path
ENV_PATH = Path(__file__).resolve().parent / "correo.env"
load_dotenv(dotenv_path=ENV_PATH)



SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")

def itinerary_to_html(itinerary: dict) -> str:
    summary = itinerary.get("summary", {})
    days = itinerary.get("days", [])

    parts = []

    for d in days:
        parts.append(f"<h3>Día {d.get('day','')} — {d.get('city','')}</h3>")

        slots = d.get("slots", {})
        for key, label in [("morning", "Mañana"), ("afternoon", "Tarde"), ("evening", "Noche")]:
            blk = slots.get(key)
            if blk and blk.get("activity"):
                parts.append(f"<p><b>{label}:</b> {blk['activity']}</p>")
                if blk.get("description"):
                    parts.append(f"<p style='margin-left:12px'>{blk['description']}</p>")

        parts.append("<hr/>")

    return "".join(parts)


def send_itinerary_email(to_email: str, subject: str, itinerary: dict):
    if not (SMTP_USER and SMTP_PASS):
        raise RuntimeError("SMTP_USER/SMTP_PASS no configurados. Revisa tu .env")
    html = itinerary_to_html(itinerary)

    msg = MIMEMultipart("alternative")
    msg["From"] = SMTP_USER
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(html, "html", "utf-8"))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)

