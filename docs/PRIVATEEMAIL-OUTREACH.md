# wolf-systems PrivateEmail outreach channel

Status: operational design, consent-first.

This channel uses Namecheap Private Email for selective one-to-one B2B outreach and reply evidence. It is deliberately separated from the automated voice-call gate.

## Mail transport

Default service endpoints:

- SMTP SSL: `mail.privateemail.com:465`
- SMTP STARTTLS alternative: `mail.privateemail.com:587`
- IMAP SSL: `mail.privateemail.com:993`
- Username: full wolf-systems email address

Credentials must be supplied locally through environment variables. Never commit the real mailbox password or secrets.

## Environment

```bash
export WOLF_EMAIL='YOUR_MAILBOX@wolf-systems.online'
export WOLF_EMAIL_PASSWORD='LOCAL_SECRET'
export PRIVATEEMAIL_SMTP_HOST='mail.privateemail.com'
export PRIVATEEMAIL_SMTP_PORT='465'
export PRIVATEEMAIL_IMAP_HOST='mail.privateemail.com'
export PRIVATEEMAIL_IMAP_PORT='993'
```

## Selective send

The sender intentionally permits only one recipient per invocation:

```bash
python scripts/privateemail_send.py \
  --to contact@example.com \
  --subject 'Founding-Pilot: AGER' \
  --body-file outreach/example.txt \
  --dry-run
```

Remove `--dry-run` only after the recipient, relevance, channel and message have been reviewed.

## Reply review

```bash
python scripts/privateemail_inbox.py --days 7 --from-address contact@example.com
```

The inbox reader is read-only. It emits Message-ID, sender, subject, date, a SHA-256 of the plain-text body and a limited preview. It does **not** infer consent.

## Convert an explicit reply into call-gate evidence

After a human has read the reply and verified that it actually permits a callback / AI-assisted phone contact:

```bash
python scripts/consent_from_email.py \
  --lead-id lead-example \
  --organization 'Example GmbH' \
  --status explicit_consent \
  --message-id '<message-id@example.com>' \
  --body-sha256 '<sha256-from-inbox-reader>' \
  --out local-consent/example.json

python scripts/call_gate.py local-consent/example.json --json
```

Only `explicit_consent`, `callback_requested` or `booked` may open the automated-call gate. Opt-outs remain blocking evidence.

## Operating rule

1. High-fit lead only.
2. Use an explicitly offered partner/contact channel or another legally appropriate route.
3. Send a short, individualized cooperation request from wolf-systems.
4. Ask separately whether an AI-assisted callback is permitted.
5. Review the actual reply.
6. Preserve Message-ID + body hash as evidence.
7. Generate the AGER contact-consent record.
8. Run `call_gate.py`.
9. CALL-E may be used only if the gate is GREEN.
10. The AI caller identifies itself and wolf-systems at the beginning of the call; recording remains off unless separately permitted.

This is an operational control design and not legal advice.
