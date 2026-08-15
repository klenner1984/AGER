# Wolf-Systems Operating Rules

## Business calls
- For every call related to wolf-systems, check the target company's currently published business/opening hours and local timezone before initiating the call.
- Place calls only inside those published business hours.
- Do not call on evenings, weekends, or public holidays unless the company explicitly publishes business hours for that period or the user explicitly instructs otherwise for that specific call.
- If business hours cannot be verified, prepare the call but do not execute it until the timing is verified.

## Email / SMTP
- For all wolf-systems business email, use the PrivateEmail SMTP/mailbox setup associated with wolf-systems.online.
- Do not use the connected personal Gmail account as the sender for wolf-systems outreach.
- SMTP credentials must come from the configured local secret/password file or environment variables; never commit credentials, passwords, API keys, or secret values to this repository.
- Before first send in a new runtime, verify that the required SMTP configuration is actually available and valid without exposing secret values.

## Sender identity
- Use Andreas / wolf-systems for wolf-systems business communication unless the user gives a different instruction for a specific contact.
