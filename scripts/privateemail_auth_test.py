#!/usr/bin/env python3
"""Authenticate all configured wolf-systems PrivateEmail mailboxes without sending mail."""

import os
import smtplib
import ssl
import sys

PROFILES = {
    "partner": ("WOLF_EMAIL_PARTNER", "WOLF_EMAIL_PARTNER_PASSWORD"),
    "andreas": ("WOLF_EMAIL_ANDREAS", "WOLF_EMAIL_ANDREAS_PASSWORD"),
    "kontakt": ("WOLF_EMAIL_KONTAKT", "WOLF_EMAIL_KONTAKT_PASSWORD"),
}


def connect(host: str, port: int, security: str):
    context = ssl.create_default_context()
    if security == "ssl":
        return smtplib.SMTP_SSL(host, port, timeout=20, context=context)
    if security == "starttls":
        smtp = smtplib.SMTP(host, port, timeout=20)
        smtp.ehlo()
        smtp.starttls(context=context)
        smtp.ehlo()
        return smtp
    raise ValueError("security must be ssl or starttls")


def main() -> int:
    host = os.environ.get("PRIVATEEMAIL_SMTP_HOST", "mail.privateemail.com")
    port = int(os.environ.get("PRIVATEEMAIL_SMTP_PORT", "465"))
    security = os.environ.get("PRIVATEEMAIL_SMTP_SECURITY", "ssl").strip().lower()

    failures = 0
    print(f"Testing SMTP authentication at {host}:{port}/{security}")
    for profile, (email_env, pw_env) in PROFILES.items():
        email = os.environ.get(email_env)
        password = os.environ.get(pw_env)
        if not email or not password:
            print(f"{profile}: MISSING ENV")
            failures += 1
            continue
        try:
            with connect(host, port, security) as smtp:
                smtp.login(email, password)
            print(f"{profile}: SMTP AUTH OK ({email})")
        except Exception as exc:
            print(f"{profile}: SMTP AUTH FAIL ({email}) - {type(exc).__name__}: {exc}")
            failures += 1

    return 0 if failures == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
