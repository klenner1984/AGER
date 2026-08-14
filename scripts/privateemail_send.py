#!/usr/bin/env python3
"""Send a single wolf-systems outreach email through Namecheap Private Email.

Designed for consent-first, selective B2B outreach. Credentials are read only
from environment variables and are never written to disk or logs.

SMTP security modes:
- ssl: implicit TLS, typically port 465
- starttls: explicit STARTTLS, typically port 587
"""

import argparse
import hashlib
import os
import smtplib
import ssl
from email.message import EmailMessage
from pathlib import Path

PROFILES = {
    "partner": {
        "email_env": "WOLF_EMAIL_PARTNER",
        "password_env": "WOLF_EMAIL_PARTNER_PASSWORD",
        "display_name": "Andreas | wolf-systems Partnerships",
    },
    "andreas": {
        "email_env": "WOLF_EMAIL_ANDREAS",
        "password_env": "WOLF_EMAIL_ANDREAS_PASSWORD",
        "display_name": "Andreas | wolf-systems",
    },
    "kontakt": {
        "email_env": "WOLF_EMAIL_KONTAKT",
        "password_env": "WOLF_EMAIL_KONTAKT_PASSWORD",
        "display_name": "wolf-systems",
    },
}


def require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise SystemExit(f"Missing required environment variable: {name}")
    return value


def smtp_client(host: str, port: int, security: str):
    context = ssl.create_default_context()
    if security == "ssl":
        return smtplib.SMTP_SSL(host, port, timeout=30, context=context)
    if security == "starttls":
        smtp = smtplib.SMTP(host, port, timeout=30)
        smtp.ehlo()
        smtp.starttls(context=context)
        smtp.ehlo()
        return smtp
    raise SystemExit("PRIVATEEMAIL_SMTP_SECURITY must be 'ssl' or 'starttls'")


def main() -> int:
    parser = argparse.ArgumentParser(description="Send one PrivateEmail message")
    parser.add_argument("--profile", choices=sorted(PROFILES), default="partner")
    parser.add_argument("--to", required=True, help="Single recipient email address")
    parser.add_argument("--subject", required=True)
    parser.add_argument("--body-file", required=True, help="UTF-8 plain-text body file")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if "," in args.to or ";" in args.to:
        raise SystemExit("Bulk/multiple recipients are intentionally blocked")

    profile = PROFILES[args.profile]
    sender = require_env(profile["email_env"])
    password = (
        require_env(profile["password_env"])
        if not args.dry_run
        else os.environ.get(profile["password_env"], "")
    )
    host = os.environ.get("PRIVATEEMAIL_SMTP_HOST", "mail.privateemail.com")
    port = int(os.environ.get("PRIVATEEMAIL_SMTP_PORT", "465"))
    security = os.environ.get("PRIVATEEMAIL_SMTP_SECURITY", "ssl").strip().lower()

    body = Path(args.body_file).read_text(encoding="utf-8")
    body_hash = hashlib.sha256(body.encode("utf-8")).hexdigest()

    msg = EmailMessage()
    msg["From"] = f"{profile['display_name']} <{sender}>"
    msg["To"] = args.to
    msg["Subject"] = args.subject
    msg.set_content(body)

    if args.dry_run:
        print(
            f"DRY-RUN profile={args.profile} from={sender} to={args.to} "
            f"subject={args.subject!r} smtp={host}:{port}/{security} "
            f"body_sha256={body_hash}"
        )
        return 0

    with smtp_client(host, port, security) as smtp:
        smtp.login(sender, password)
        smtp.send_message(msg)

    print(
        f"SENT profile={args.profile} from={sender} to={args.to} "
        f"subject={args.subject!r} smtp={host}:{port}/{security} "
        f"body_sha256={body_hash}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
