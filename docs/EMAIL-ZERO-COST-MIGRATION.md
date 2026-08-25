# wolf-systems zero-cost email architecture

Target architecture:

- Domain registrar: Namecheap (domain only)
- Authoritative DNS: Cloudflare
- Inbound mail: Cloudflare Email Routing (free)
- Outbound mail: Brevo SMTP Free
- Authenticated outbound domain: `outreach.wolf-systems.online`
- Outbound sender identities:
  - `partner@outreach.wolf-systems.online`
  - `andreas@outreach.wolf-systems.online`
  - `kontakt@outreach.wolf-systems.online`
- Transitional Reply-To / legacy inbound identities:
  - `partner@wolf-systems.online`
  - `andreas@wolf-systems.online`
  - `kontakt@wolf-systems.online`
- AGER sender: `scripts/smtp_send.py`
- Legacy fallback during migration: Namecheap Private Email

## Current state

Completed:

1. Namecheap nameservers changed to Cloudflare-assigned nameservers.
2. Existing website and Private Email DNS records preserved in Cloudflare.
3. `outreach.wolf-systems.online` added to Brevo as the dedicated sending domain.
4. Brevo-Code, DKIM 1, DKIM 2, DMARC and branded tracking CNAME records added in Cloudflare.
5. Brevo verified all required records successfully and the sending domain was authenticated.
6. SMTP relay settings confirmed:
   - Host: `smtp-relay.brevo.com`
   - Port: `587`
   - Security: STARTTLS
   - Login: `b6a71e001@smtp-brevo.com`
7. A Brevo SMTP key named `wolf-systems-ager` was generated. The secret value must never be committed.

Still pending:

- Securely load `BREVO_SMTP_KEY` on the machine/runtime that sends mail.
- Add/verify the required Brevo sender identities if Brevo asks for them separately.
- Perform a controlled outbound test.
- Configure Cloudflare Email Routing and verify the destination inbox.
- Cut inbound MX from Private Email to Cloudflare only after routing tests are ready.

## Safety rule

Do not remove the existing Private Email MX records until all of the following are true:

1. All existing non-mail DNS records remain present and checked in Cloudflare.
2. A destination mailbox has been verified in Cloudflare Email Routing.
3. Routing rules for partner@, andreas@ and kontakt@ exist.
4. The Brevo outbound sending domain and sender identities are accepted.
5. SPF/DKIM/DMARC have been reviewed for the combined architecture.
6. An outbound Brevo test succeeds.
7. A controlled inbound routing test succeeds after MX cutover.

## Brevo outbound configuration

The live authenticated sending domain is `outreach.wolf-systems.online` rather than the root domain. This isolates outbound reputation from the legacy mailbox domain while Private Email remains active.

Environment variables:

```text
WOLF_SMTP_PROVIDER=brevo
WOLF_SMTP_HOST=smtp-relay.brevo.com
WOLF_SMTP_PORT=587
WOLF_SMTP_SECURITY=starttls
BREVO_SMTP_LOGIN=b6a71e001@smtp-brevo.com
BREVO_SMTP_KEY=<secret, load locally only>
WOLF_EMAIL_PARTNER=partner@outreach.wolf-systems.online
WOLF_EMAIL_ANDREAS=andreas@outreach.wolf-systems.online
WOLF_EMAIL_KONTAKT=kontakt@outreach.wolf-systems.online
```

Never commit the real SMTP key. `.gitignore` excludes local environment and secret files.

Test locally without sending:

```bash
python scripts/smtp_send.py \
  --profile andreas \
  --to recipient@example.invalid \
  --subject "AGER SMTP dry-run" \
  --body-file outreach/sample.txt \
  --reply-to andreas@wolf-systems.online \
  --dry-run
```

For the first real test, keep `--reply-to andreas@wolf-systems.online` while root-domain inbound mail still uses Private Email.

## Cloudflare Email Routing

In Cloudflare Email Routing:

1. Add and verify the destination inbox.
2. Create routes for the intended inbound addresses.
3. Leave catch-all disabled initially unless there is a deliberate business reason to enable it.
4. Let Cloudflare provide the Email Routing MX/authentication records.
5. Only then replace the legacy Private Email MX path.

Cloudflare Email Routing is the actual inbound cutover point. Until then, Private Email remains the rollback path.

## SPF, DKIM and DMARC

The root domain currently retains the Private Email SPF record while legacy outbound service remains available. Do not add a second independent root SPF record.

The dedicated Brevo sending subdomain is authenticated through Brevo-provided records, including DKIM selectors and DMARC. Provider-specific DKIM records may coexist because they use distinct selectors.

DMARC should remain conservative during migration until legitimate traffic is confirmed aligned, then it can be tightened deliberately.

## Cutover and verification

After all prerequisites are green:

- send a test through Brevo from each intended AGER sender profile;
- inspect delivered headers for DKIM and DMARC alignment;
- check spam placement;
- configure Cloudflare Email Routing destination and aliases;
- switch/confirm Cloudflare Email Routing MX records;
- send external inbound tests to all business addresses;
- only then treat Private Email as unnecessary.

## Rollback

Keep a copy of the prior Namecheap/Private Email MX and TXT records until migration is proven. If inbound delivery fails during cutover, restore the previous MX records while troubleshooting. Do not cancel Private Email before the new path has passed both inbound and outbound tests.

## Cost model

The intended steady-state mail infrastructure has no recurring mailbox subscription:

- Cloudflare Email Routing: inbound forwarding on the free plan
- Brevo Free: outbound SMTP within the current free-plan sending limit
- Namecheap: registrar only

Provider limits and terms can change, so verify them before any future production-scale increase.
