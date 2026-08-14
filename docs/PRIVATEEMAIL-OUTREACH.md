# wolf-systems PrivateEmail outreach channel

Status: operational design, consent-first.

This channel uses Namecheap Private Email for selective one-to-one B2B outreach and reply evidence. It is deliberately separated from the automated voice-call gate.

## Mailbox roles

- `partner@wolf-systems.online` — primary sender for cooperation requests, Founding Pilots and partner programs.
- `andreas@wolf-systems.online` — personal sender for technical follow-ups, named pilot conversations and direct replies from Andreas.
- `kontakt@wolf-systems.online` — general website/contact mailbox and neutral inbound route.

Default outreach profile is `partner`.

## Mail transport

Default service endpoints:

- SMTP implicit TLS: `mail.privateemail.com:465`
- SMTP STARTTLS alternative: `mail.privateemail.com:587`
- IMAP SSL: `mail.privateemail.com:993`
- Username: full wolf-systems email address

The sender supports both SMTP modes through `PRIVATEEMAIL_SMTP_SECURITY=ssl|starttls`.

Credentials must be supplied locally through environment variables. Never commit real mailbox passwords or secrets.

## Secure Windows local setup

Recommended Windows setup stores each password with Windows DPAPI under the current Windows user rather than in a plaintext `.env` file.

The local setup bootstrap creates:

- `%APPDATA%\wolf-systems\privateemail\partner.password.dpapi`
- `%APPDATA%\wolf-systems\privateemail\andreas.password.dpapi`
- `%APPDATA%\wolf-systems\privateemail\kontakt.password.dpapi`
- `%APPDATA%\wolf-systems\privateemail\load-privateemail.ps1`

The generated loader decrypts the DPAPI secrets only into the current PowerShell process and sets the AGER environment variables. It also configures SMTP 465/SSL by default and can use 587/STARTTLS when needed.

In every new PowerShell session load the credentials with:

```powershell
. "$env:APPDATA\wolf-systems\privateemail\load-privateemail.ps1"
```

Then verify authentication without sending mail:

```powershell
python scripts/privateemail_auth_test.py
```

## Environment

```bash
export WOLF_EMAIL_PARTNER='partner@wolf-systems.online'
export WOLF_EMAIL_PARTNER_PASSWORD='LOCAL_SECRET'
export WOLF_EMAIL_ANDREAS='andreas@wolf-systems.online'
export WOLF_EMAIL_ANDREAS_PASSWORD='LOCAL_SECRET'
export WOLF_EMAIL_KONTAKT='kontakt@wolf-systems.online'
export WOLF_EMAIL_KONTAKT_PASSWORD='LOCAL_SECRET'
export PRIVATEEMAIL_SMTP_HOST='mail.privateemail.com'
export PRIVATEEMAIL_SMTP_PORT='465'
export PRIVATEEMAIL_SMTP_SECURITY='ssl'
export PRIVATEEMAIL_IMAP_HOST='mail.privateemail.com'
export PRIVATEEMAIL_IMAP_PORT='993'
```

For the STARTTLS alternative use port `587` and `PRIVATEEMAIL_SMTP_SECURITY=starttls`.

## SMTP authentication test

`privateemail_auth_test.py` logs into all three configured mailboxes and exits without sending any message:

```bash
python scripts/privateemail_auth_test.py
```

A successful setup prints `SMTP AUTH OK` for `partner`, `andreas` and `kontakt`.

## Selective send

The sender intentionally permits only one recipient per invocation. Partner outreach defaults to the `partner` profile:

```bash
python scripts/privateemail_send.py \
  --profile partner \
  --to contact@example.com \
  --subject 'Founding-Pilot: AGER' \
  --body-file outreach/example.txt \
  --dry-run
```

Use `--profile andreas` only when the communication has moved to a named/personal technical or pilot conversation. Use `--profile kontakt` for neutral general correspondence.

Remove `--dry-run` only after the recipient, relevance, channel and message have been reviewed.

## Reply review

```bash
python scripts/privateemail_inbox.py --profile partner --days 7 --from-address contact@example.com
```

The inbox reader is read-only. It emits mailbox profile, Message-ID, sender, subject, date, a SHA-256 of the plain-text body and a limited preview. It does **not** infer consent.

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
3. Send a short, individualized cooperation request from `partner@wolf-systems.online`.
4. Ask separately whether an AI-assisted callback is permitted.
5. Review the actual reply.
6. Preserve Message-ID + body hash as evidence.
7. Generate the AGER contact-consent record.
8. Run `call_gate.py`.
9. CALL-E may be used only if the gate is GREEN.
10. The AI caller identifies itself and wolf-systems at the beginning of the call; recording remains off unless separately permitted.
11. Once a named pilot contact exists, continue personally from `andreas@wolf-systems.online`.

This is an operational control design and not legal advice.
