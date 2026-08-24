# wolf-systems zero-cost email architecture

Target architecture:

- Domain registrar: Namecheap (domain only)
- Authoritative DNS: Cloudflare
- Inbound mail: Cloudflare Email Routing (free)
- Outbound mail: Brevo SMTP Free
- Sender identities:
  - partner@wolf-systems.online
  - andreas@wolf-systems.online
  - kontakt@wolf-systems.online
- AGER sender: `scripts/smtp_send.py`
- Legacy fallback during migration: Namecheap Private Email

## Safety rule

Do not remove the existing Private Email MX records until all of the following are true:

1. wolf-systems.online is active on Cloudflare DNS.
2. All existing non-mail DNS records have been copied and checked.
3. A destination mailbox has been verified in Cloudflare Email Routing.
4. Routing rules for partner@, andreas@ and kontakt@ exist.
5. Brevo has authenticated wolf-systems.online and the sender identities.
6. SPF/DKIM/DMARC have been reviewed for the combined architecture.
7. An outbound Brevo test succeeds.
8. A controlled inbound routing test succeeds after MX cutover.

## Phase 1 — Cloudflare DNS onboarding

- Add `wolf-systems.online` to Cloudflare Free.
- Import/scan the current DNS zone.
- Compare every A/AAAA/CNAME/TXT/MX record with the current Namecheap zone.
- Do not switch nameservers until the imported zone is complete.
- Change the domain nameservers at Namecheap to the pair assigned by Cloudflare.
- Wait until Cloudflare reports the zone as Active.

## Phase 2 — Brevo outbound before MX cutover

Brevo SMTP settings:

- Host: `smtp-relay.brevo.com`
- Recommended port: 587
- Security: STARTTLS
- Username: Brevo SMTP login
- Password: Brevo SMTP key (not API key and not account password)

Authenticate `wolf-systems.online` in Brevo. Add exactly the DNS records Brevo currently provides for domain authentication. Do not invent DKIM selectors or verification values; use the values shown by the Brevo account.

Test locally without sending:

```bash
python scripts/smtp_send.py \
  --profile andreas \
  --to recipient@example.invalid \
  --subject "AGER SMTP dry-run" \
  --body-file outreach/sample.txt \
  --dry-run
```

Then perform one real test to an address controlled by wolf-systems.

## Phase 3 — Cloudflare Email Routing

In Cloudflare Email Routing:

1. Add and verify the destination inbox.
2. Create routes:
   - `andreas@wolf-systems.online` -> verified destination
   - `partner@wolf-systems.online` -> verified destination
   - `kontakt@wolf-systems.online` -> verified destination
3. Leave catch-all disabled initially unless there is a deliberate business reason to enable it.
4. Let Cloudflare add/recommend its Email Routing MX/authentication records.

Cloudflare Email Routing requires Cloudflare DNS and replaces the inbound MX path. Therefore this is the actual inbound cutover point.

## Phase 4 — SPF, DKIM and DMARC review

Important: a domain should publish only one SPF record at the root. When Cloudflare Email Routing and Brevo both require sender-policy data, merge their required mechanisms into one valid SPF policy where technically required; never create two independent `v=spf1` root TXT records.

DKIM records are provider-specific and may coexist under different selectors.

DMARC should start conservatively during migration, for example monitoring mode, then be tightened only after legitimate Cloudflare/Brevo traffic is confirmed aligned. The exact DMARC policy is an operational decision and should not be changed blindly.

## Phase 5 — Cutover and verification

After all prerequisites are green:

- switch/confirm Cloudflare Email Routing MX records;
- send a test from an external mailbox to each wolf-systems address;
- confirm all three arrive at the verified destination;
- send from each AGER sender profile through Brevo;
- inspect message headers for SPF, DKIM and DMARC results;
- check spam placement;
- only then treat Private Email as unnecessary.

## Rollback

Keep a copy of the prior Namecheap MX/TXT records until migration is proven. If inbound delivery fails during cutover, restore the previous MX records while troubleshooting. Do not cancel Private Email before the new path has passed both inbound and outbound tests.

## Cost model

The intended steady-state mail infrastructure has no recurring mailbox subscription:

- Cloudflare Email Routing: inbound forwarding on the free plan
- Brevo Free: outbound SMTP within the current free-plan sending limit
- Namecheap: registrar only

Provider limits and terms can change, so verify them before any future production-scale increase.
