"""Alpesdata — Contact Form API
Self-hosted backend for the contact form on alpesdata.com.
Sends emails via Mailjet SMTP.
"""

import os
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
from dotenv import load_dotenv

load_dotenv()

# ── Logging ──────────────────────────────────────────────
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("alpesdata-api")

# ── Config ───────────────────────────────────────────────
SMTP_HOST = os.getenv("SMTP_HOST", "in-v3.mailjet.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")
FROM_EMAIL = os.getenv("FROM_EMAIL", "contact@alpesdata.com")
FROM_NAME = os.getenv("FROM_NAME", "Alpesdata Contact")
TO_EMAIL = os.getenv("TO_EMAIL", "info@alpesdata.com")
TO_NAME = os.getenv("TO_NAME", "Alpesdata")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "https://alpesdata.com,https://www.alpesdata.com").split(",")

# Formulaire « demande d'étude » du site massagepro.fr — site client servi par la même API.
# Les origines autorisées sont toujours complétées ici : le paramètre ALLOWED_ORIGINS du conteneur
# ne doit pas avoir à être modifié à chaque nouveau site client.
MP_TO_EMAIL = os.getenv("MP_TO_EMAIL", "contact@massagepro.fr")
MP_TO_NAME = os.getenv("MP_TO_NAME", "Robot Masseur — massagepro.fr")
for _origin in ("https://massagepro.fr", "https://www.massagepro.fr"):
    if _origin not in ALLOWED_ORIGINS:
        ALLOWED_ORIGINS.append(_origin)

# Rate limiting (simple in-memory)
RATE_LIMIT_WINDOW = 60  # seconds
RATE_LIMIT_MAX = 5  # max submissions per window per IP
_rate_store: dict[str, list[float]] = {}

# ── FastAPI App ──────────────────────────────────────────
app = FastAPI(
    title="Alpesdata Contact API",
    version="1.0.0",
    description="Handles contact form submissions for alpesdata.com",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["Content-Type"],
    max_age=3600,
)


# ── Models ───────────────────────────────────────────────
class ContactForm(BaseModel):
    name: str = Field(..., min_length=1, max_length=128)
    email: EmailStr
    message: str = Field(..., min_length=10, max_length=5000)


class HealthResponse(BaseModel):
    status: str = "ok"
    timestamp: str = ""


class SubmitResponse(BaseModel):
    success: bool = True
    message: str = "Message envoyé avec succès !"


# ── Helpers ──────────────────────────────────────────────
def _check_rate_limit(ip: str) -> bool:
    """Returns True if the IP is allowed to submit."""
    now = datetime.now().timestamp()
    if ip not in _rate_store:
        _rate_store[ip] = []
    # Remove old entries outside the window
    _rate_store[ip] = [t for t in _rate_store[ip] if now - t < RATE_LIMIT_WINDOW]
    if len(_rate_store[ip]) >= RATE_LIMIT_MAX:
        return False
    _rate_store[ip].append(now)
    return True


def _sanitize(text: str) -> str:
    """Basic input sanitization."""
    import html
    return html.escape(text.strip())


def _send_email(name: str, email: str, message: str) -> bool:
    """Send email via SMTP (Mailjet)."""
    name_clean = _sanitize(name)
    msg_clean = _sanitize(message)

    subject = f"Nouveau message de {name_clean} — Alpesdata Contact"

    html_body = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="font-family: 'Inter', Arial, sans-serif; background: #f7ebed; padding: 40px 20px;">
  <table width="100%" cellpadding="0" cellspacing="0">
    <tr><td align="center">
      <table style="max-width: 600px; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.08);">
        <tr>
          <td style="background: #1B395A; padding: 24px; text-align: center;">
            <h1 style="color: white; margin: 0; font-size: 1.3rem; font-weight: 600;">📬 Nouveau message</h1>
          </td>
        </tr>
        <tr>
          <td style="padding: 32px;">
            <table width="100%" cellpadding="0" cellspacing="0">
              <tr>
                <td style="padding: 8px 0; color: #666; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px;">Expéditeur</td>
              </tr>
              <tr>
                <td style="padding: 0 0 16px; font-size: 1.1rem; color: #1B395A; font-weight: 600;">{name_clean}</td>
              </tr>
              <tr>
                <td style="padding: 8px 0; color: #666; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px;">Email</td>
              </tr>
              <tr>
                <td style="padding: 0 0 16px;"><a href="mailto:{email}" style="color: #806065; font-weight: 500;">{email}</a></td>
              </tr>
              <tr>
                <td style="padding: 8px 0; color: #666; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px;">Message</td>
              </tr>
              <tr>
                <td style="padding: 16px; background: #f7ebed; border-radius: 8px; font-size: 0.95rem; line-height: 1.6; color: #2d2d2d; white-space: pre-wrap;">{msg_clean}</td>
              </tr>
            </table>
          </td>
        </tr>
        <tr>
          <td style="background: #0F2640; padding: 16px; text-align: center;">
            <p style="color: rgba(255,255,255,0.5); margin: 0; font-size: 0.75rem;">Alpesdata · Agence de développement web · Briançon</p>
          </td>
        </tr>
      </table>
    </td></tr>
  </table>
</body>
</html>"""

    msg = MIMEMultipart("alternative")
    msg["From"] = f"{FROM_NAME} <{FROM_EMAIL}>"
    msg["To"] = f"{TO_NAME} <{TO_EMAIL}>"
    msg["Subject"] = subject
    msg["Reply-To"] = f"{name_clean} <{email}>"
    msg.attach(MIMEText(f"Nom: {name_clean}\nEmail: {email}\nMessage:\n{msg_clean}", "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=15) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(FROM_EMAIL, [TO_EMAIL], msg.as_string())
        logger.info(f"Email sent successfully from {email}")
        return True
    except smtplib.SMTPAuthenticationError:
        logger.error("SMTP authentication failed — check Mailjet API keys")
        raise
    except smtplib.SMTPException as e:
        logger.error(f"SMTP error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error sending email: {e}")
        raise


# ── Routes ───────────────────────────────────────────────
@app.get("/api/health", response_model=HealthResponse)
async def health():
    return HealthResponse(timestamp=datetime.utcnow().isoformat())


@app.post("/api/contact", response_model=SubmitResponse)
async def submit_contact(form: ContactForm, x_forwarded_for: str = ""):
    client_ip = x_forwarded_for.split(",")[0].strip() if x_forwarded_for else "unknown"

    # Rate limiting
    if not _check_rate_limit(client_ip):
        logger.warning(f"Rate limit hit for {client_ip}")
        raise HTTPException(status_code=429, detail="Trop de demandes. Réessayez dans une minute.")

    # Validate
    if not form.name.strip() or not form.message.strip():
        raise HTTPException(status_code=400, detail="Tous les champs sont requis.")

    # Send
    try:
        _send_email(form.name.strip(), form.email, form.message.strip())
        logger.info(f"Contact form submitted by {form.name} <{form.email}> ({client_ip})")
        return SubmitResponse()
    except smtplib.SMTPAuthenticationError:
        raise HTTPException(status_code=500, detail="Erreur de configuration email. Contactez l'administrateur.")
    except Exception:
        raise HTTPException(status_code=500, detail="Erreur lors de l'envoi. Réessayez plus tard.")


# ── Formulaire « demande d'étude » — massagepro.fr ───────
class EtudeForm(BaseModel):
    name: str = Field(..., min_length=1, max_length=128)
    email: EmailStr
    etablissement: str = Field("", max_length=160)
    telephone: str = Field("", max_length=40)
    ville: str = Field("", max_length=120)
    message: str = Field(..., min_length=10, max_length=5000)
    consent: bool = False
    website: str = Field("", max_length=200)  # honeypot anti-robot


def _send_etude(form: "EtudeForm", client_ip: str) -> None:
    """Achemine la demande d'étude vers la boîte du client (contact@massagepro.fr)."""
    name = _sanitize(form.name)
    etab = _sanitize(form.etablissement) or "—"
    tel = _sanitize(form.telephone) or "—"
    ville = _sanitize(form.ville) or "—"
    msg_html = _sanitize(form.message)
    when = datetime.now().strftime("%d/%m/%Y à %H:%M")

    subject = f"Demande d'étude massagepro.fr — {name}" + (f" ({form.ville})" if form.ville else "")

    def row(label: str, value: str) -> str:
        return (
            f'<tr><td style="padding:6px 0;color:#6b7f8a;font-size:12px;text-transform:uppercase;'
            f'letter-spacing:.08em;width:150px;vertical-align:top">{label}</td>'
            f'<td style="padding:6px 0;color:#0e1a22;font-size:15px">{value}</td></tr>'
        )

    html_body = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"></head>
<body style="margin:0;padding:32px 16px;background:#eef2f0;font-family:Arial,Helvetica,sans-serif">
  <table width="100%" cellpadding="0" cellspacing="0"><tr><td align="center">
    <table width="600" cellpadding="0" cellspacing="0" style="max-width:600px;background:#fff;border-radius:14px;overflow:hidden">
      <tr><td style="background:#0b141b;padding:26px 30px">
        <div style="color:#7fd6c4;font-size:12px;letter-spacing:.14em;text-transform:uppercase">massagepro.fr</div>
        <div style="color:#fff;font-size:21px;font-weight:bold;margin-top:6px">Nouvelle demande d'étude d'implantation</div>
      </td></tr>
      <tr><td style="padding:26px 30px 8px">
        <table width="100%" cellpadding="0" cellspacing="0">
          {row("Contact", f"<strong>{name}</strong>")}
          {row("Établissement", etab)}
          {row("E-mail", f'<a href="mailto:{form.email}" style="color:#0a5a4e">{form.email}</a>')}
          {row("Téléphone", f'<a href="tel:{tel}" style="color:#0a5a4e">{tel}</a>' if form.telephone else "—")}
          {row("Ville", ville)}
          {row("Reçue le", when)}
        </table>
      </td></tr>
      <tr><td style="padding:10px 30px 30px">
        <div style="color:#6b7f8a;font-size:12px;text-transform:uppercase;letter-spacing:.08em;margin-bottom:8px">Message</div>
        <div style="background:#f4f8f6;border-left:3px solid #0f7d6c;border-radius:6px;padding:16px;color:#1b2b33;font-size:15px;line-height:1.6;white-space:pre-wrap">{msg_html}</div>
      </td></tr>
      <tr><td style="background:#f0f4f2;padding:16px 30px;color:#7a8f99;font-size:12px">
        Répondez directement à cet e-mail : la réponse part vers {form.email}.<br>
        Formulaire du site massagepro.fr · G.O PARTNERS SAS
      </td></tr>
    </table>
  </td></tr></table>
</body></html>"""

    text_body = (
        f"Demande d'étude d'implantation — massagepro.fr\n\n"
        f"Contact : {name}\nÉtablissement : {etab}\nE-mail : {form.email}\n"
        f"Téléphone : {tel}\nVille : {ville}\nReçue le : {when}\n\nMessage :\n{form.message}\n"
    )

    msg = MIMEMultipart("alternative")
    msg["From"] = f"massagepro.fr <{FROM_EMAIL}>"
    msg["To"] = f"{MP_TO_NAME} <{MP_TO_EMAIL}>"
    msg["Subject"] = subject
    msg["Reply-To"] = f"{name} <{form.email}>"
    msg.attach(MIMEText(text_body, "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=15) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(FROM_EMAIL, [MP_TO_EMAIL], msg.as_string())
    logger.info(f"Demande d'étude massagepro envoyée : {form.email} ({client_ip})")


@app.post("/api/contact-massagepro", response_model=SubmitResponse)
async def submit_etude(form: EtudeForm, request: Request):
    client_ip = (request.headers.get("x-forwarded-for", "").split(",")[0].strip()
                 or (request.client.host if request.client else "unknown"))

    # Piège à robots : le champ caché doit rester vide. On répond « succès » pour ne pas les alerter.
    if form.website.strip():
        logger.info(f"Honeypot massagepro déclenché ({client_ip}) — message ignoré")
        return SubmitResponse(message="Merci, votre demande a bien été envoyée.")

    if not form.consent:
        raise HTTPException(status_code=400, detail="Merci de cocher la case d'information sur vos données.")

    if not _check_rate_limit(client_ip):
        logger.warning(f"Rate limit massagepro pour {client_ip}")
        raise HTTPException(status_code=429, detail="Trop de demandes. Réessayez dans une minute.")

    try:
        _send_etude(form, client_ip)
        return SubmitResponse(message="Merci ! Votre demande est envoyée, nous revenons vers vous sous 24 h ouvrées.")
    except smtplib.SMTPAuthenticationError:
        logger.error("SMTP auth failed (massagepro)")
        raise HTTPException(status_code=500, detail="Erreur de configuration e-mail. Écrivez à contact@massagepro.fr.")
    except Exception as e:
        logger.error(f"Erreur envoi demande d'étude : {e}")
        raise HTTPException(status_code=500, detail="L'envoi a échoué. Réessayez ou écrivez à contact@massagepro.fr.")
