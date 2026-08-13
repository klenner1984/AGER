#!/usr/bin/env python3
"""Inspect recent PrivateEmail replies and emit evidence-friendly JSON.

This tool is read-only. It does not mark messages read, move mail, or infer legal
consent automatically. Human review is required before creating a GREEN call gate.
"""

import argparse
import email
import hashlib
import imaplib
import json
import os
from datetime import datetime, timedelta, timezone
from email.header import decode_header, make_header
from email.message import Message

PROFILES = {
    "partner": ("WOLF_EMAIL_PARTNER", "WOLF_EMAIL_PARTNER_PASSWORD"),
    "andreas": ("WOLF_EMAIL_ANDREAS", "WOLF_EMAIL_ANDREAS_PASSWORD"),
    "kontakt": ("WOLF_EMAIL_KONTAKT", "WOLF_EMAIL_KONTAKT_PASSWORD"),
}


def require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise SystemExit(f"Missing required environment variable: {name}")
    return value


def text_body(msg: Message) -> str:
    parts = []
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            disp = str(part.get("Content-Disposition", ""))
            if ctype == "text/plain" and "attachment" not in disp.lower():
                payload = part.get_payload(decode=True) or b""
                charset = part.get_content_charset() or "utf-8"
                parts.append(payload.decode(charset, errors="replace"))
    elif msg.get_content_type() == "text/plain":
        payload = msg.get_payload(decode=True) or b""
        charset = msg.get_content_charset() or "utf-8"
        parts.append(payload.decode(charset, errors="replace"))
    return "\n".join(parts).strip()


def decode(value: str | None) -> str:
    return str(make_header(decode_header(value or "")))


def main() -> int:
    parser = argparse.ArgumentParser(description="Read recent PrivateEmail replies")
    parser.add_argument("--profile", choices=sorted(PROFILES), default="partner")
    parser.add_argument("--days", type=int, default=7)
    parser.add_argument("--from-address", default=None)
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()

    email_env, password_env = PROFILES[args.profile]
    username = require_env(email_env)
    password = require_env(password_env)
    host = os.environ.get("PRIVATEEMAIL_IMAP_HOST", "mail.privateemail.com")
    port = int(os.environ.get("PRIVATEEMAIL_IMAP_PORT", "993"))

    since = (datetime.now(timezone.utc) - timedelta(days=args.days)).strftime("%d-%b-%Y")
    criteria = ["SINCE", since]
    if args.from_address:
        criteria += ["FROM", f'"{args.from_address}"']

    with imaplib.IMAP4_SSL(host, port) as imap:
        imap.login(username, password)
        imap.select("INBOX", readonly=True)
        status, data = imap.search(None, *criteria)
        if status != "OK":
            raise SystemExit("IMAP search failed")

        ids = data[0].split()[-args.limit:]
        out = []
        for msg_id in reversed(ids):
            status, payload = imap.fetch(msg_id, "(RFC822)")
            if status != "OK" or not payload or not isinstance(payload[0], tuple):
                continue
            raw = payload[0][1]
            msg = email.message_from_bytes(raw)
            body = text_body(msg)
            out.append({
                "mailbox_profile": args.profile,
                "mailbox": username,
                "imap_id": msg_id.decode(),
                "message_id": msg.get("Message-ID", ""),
                "from": decode(msg.get("From")),
                "to": decode(msg.get("To")),
                "subject": decode(msg.get("Subject")),
                "date": msg.get("Date", ""),
                "body_sha256": hashlib.sha256(body.encode("utf-8")).hexdigest(),
                "body_preview": body[:1200],
            })

    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
