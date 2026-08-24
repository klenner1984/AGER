#!/usr/bin/env python3
"""Send one wolf-systems email through a configurable SMTP relay.

Default target is Brevo SMTP for the zero-cost mail architecture:
Cloudflare Email Routing (inbound) + Brevo SMTP (outbound).

Secrets are read only from environment variables and are never written to disk
or printed. Multiple recipients are intentionally blocked.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import smtplib
import ssl
from email.message import EmailMessage
from pathlib import Path

PROFILES = {
    "partner": {
        "sender_env": "WOLF_EMAIL_PARTNER",
        "sender_default": "partner@wolf-systems.online",
        "display_name": "Andreas | wolf-systems Partnerships",
    },
    "andreas": {
        "sender_env": "WOLF_EMAIL_ANDREAS",
        "sender_default": "andreas@wolf-systems.online",
        "display_name": "Andreas | wolf-systems",
    },
    "kontakt": {
        "sender_env": "WOLF_EMAIL_KONTAKT",
        "sender_default": "kontakt@wolf-systems.online",
        "display_name": "wolf-systems",
    },
}


def env(name: str, default: str | None = None, *, required: bool = False) -> str:
    value = os.environ.get(name, default)
    if required and not value:
        raise SystemExit(f"Missing required environment variable: {name}")
    return value or ""


def smtp_settings(dry_run: bool) -> dict[str, object]:
    provider = env("WOLF_SMTP_PROVIDER", "brevo").lower()

    if provider == "brevo":
        return {
            "provider": provider,
            "host": env("WOLF_SMTP_HOST", "smtp-relay.brevo.com"),
            "port": int(env("WOLF_SMTP_PORT", "587")),
            "security": env("WOLF_SMTP_SECURITY", "starttls").lower(),
            "username": env("BREVO_SMTP_LOGIN", required=not dry_run),
            "password": env("BREVO_SMTP_KEY", required=not dry_run),
        }

    if provider == "privateemail":
        # Legacy fallback. For this provider the login is normally the mailbox
        # address and the password differs by sender profile, so the caller
        # fills username/password after profile selection.
        return {
            "provider": provider,
            "host": env("WOLF_SMTP_HOST", "mail.privateemail.com"),
            "port": int(env("WOLF_SMTP_PORT", "465")),
            "security": env("WOLF_SMTP_SECURITY", "ssl").lower(),
            "username": "",
            "password": "",
        }

    return {
        "provider": provider,
        "host": env("WOLF_SMTP_HOST", required=True),
        "port": int(env("WOLF_SMTP_PORT", "587")),
        "security": env("WOLF_SMTP_SECURITY", "starttls").lower(),
        "username": env("WOLF_SMTP_USERNAME", required=not dry_run),
        "password": env("WOLF_SMTP_PASSWORD", required=not dry_run),
    }


def connect(settings: dict[str, object]):
    host = str(settings["host"])
    port = int(settings["port"])
    security = str(settings["security"])
    context = ssl.create_default_context()

    if security == "ssl":
        return smtplib.SMTP_SSL(host, port, timeout=30, context=context)

    smtp = smtplib.SMTP(host, port, timeout=30)
    smtp.ehlo()
    if security == "starttls":
        smtp.starttls(context=context)
        smtp.ehlo()
    elif security not in {"none", "plain"}:
        smtp.quit()
        raise SystemExit(f"Unsupported WOLF_SMTP_SECURITY: {security}")
    return smtp


def main() -> int:
    parser = argparse.ArgumentParser(description="Send one wolf-systems SMTP message")
    parser.add_argument("--profile", choices=sorted(PROFILES), default="partner")
    parser.add_argument("--to", required=True, help="Single recipient email address")
    parser.add_argument("--subject", required=True)
    parser.add_argument("--body-file", required=True, help="UTF-8 plain-text body file")
    parser.add_argument("--reply-to", help="Optional Reply-To address")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if any(x in args.to for x in [",", ";", "\n", "\r"]):
        raise SystemExit("Bulk/multiple recipients are intentionally blocked")

    profile = PROFILES[args.profile]
    sender = env(profile["sender_env"], profile["sender_default"])
    body = Path(args.body_file).read_text(encoding="utf-8")
    body_hash = hashlib.sha256(body.encode("utf-8")).hexdigest()
    settings = smtp_settings(args.dry_run)

    if settings["provider"] == "privateemail":
        settings["username"] = sender
        password_env = {
            "partner": "WOLF_EMAIL_PARTNER_PASSWORD",
            "andreas": "WOLF_EMAIL_ANDREAS_PASSWORD",
            "kontakt": "WOLF_EMAIL_KONTAKT_PASSWORD",
        }[args.profile]
        settings["password"] = env(password_env, required=not args.dry_run)

    msg = EmailMessage()
    msg["From"] = f"{profile['display_name']} <{sender}>"
    msg["To"] = args.to
    msg["Subject"] = args.subject
    if args.reply_to:
        msg["Reply-To"] = args.reply_to
    msg.set_content(body)

    if args.dry_run:
        print(
            "DRY-RUN "
            f"provider={settings['provider']} profile={args.profile} "
            f"from={sender} to={args.to} subject={args.subject!r} "
            f"body_sha256={body_hash}"
        )
        return 0

    with connect(settings) as smtp:
        smtp.login(str(settings["username"]), str(settings["password"]))
        smtp.send_message(msg)

    print(
        "SENT "
        f"provider={settings['provider']} profile={args.profile} "
        f"from={sender} to={args.to} subject={args.subject!r} "
        f"body_sha256={body_hash}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
