#!/usr/bin/env python3
"""Send a single wolf-systems outreach email through Namecheap Private Email.

Designed for consent-first, selective B2B outreach. Credentials are read only
from environment variables and are never written to disk or logs.
"""

import argparse
import hashlib
import os
import smtplib
from email.message import EmailMessage
from pathlib import Path


def require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise SystemExit(f"Missing required environment variable: {name}")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description="Send one PrivateEmail message")
    parser.add_argument("--to", required=True, help="Single recipient email address")
    parser.add_argument("--subject", required=True)
    parser.add_argument("--body-file", required=True, help="UTF-8 plain-text body file")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if "," in args.to or ";" in args.to:
        raise SystemExit("Bulk/multiple recipients are intentionally blocked")

    sender = require_env("WOLF_EMAIL")
    password = require_env("WOLF_EMAIL_PASSWORD") if not args.dry_run else os.environ.get("WOLF_EMAIL_PASSWORD", "")
    host = os.environ.get("PRIVATEEMAIL_SMTP_HOST", "mail.privateemail.com")
    port = int(os.environ.get("PRIVATEEMAIL_SMTP_PORT", "465"))

    body = Path(args.body_file).read_text(encoding="utf-8")
    body_hash = hashlib.sha256(body.encode("utf-8")).hexdigest()

    msg = EmailMessage()
    msg["From"] = f"Andreas | wolf-systems <{sender}>"
    msg["To"] = args.to
    msg["Subject"] = args.subject
    msg.set_content(body)

    if args.dry_run:
        print(f"DRY-RUN to={args.to} subject={args.subject!r} body_sha256={body_hash}")
        return 0

    with smtplib.SMTP_SSL(host, port, timeout=30) as smtp:
        smtp.login(sender, password)
        smtp.send_message(msg)

    print(f"SENT to={args.to} subject={args.subject!r} body_sha256={body_hash}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
