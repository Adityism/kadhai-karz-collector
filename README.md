# Kadhai Karz Collector 🍳💸

## What is this?

This is the world's most persistent, slightly passive-aggressive, and definitely automated daily reminder system for collecting that one kadhai (wok) contribution your friend Bhavi keeps forgetting to pay. 

Every day, this codebase will send a new, witty, and occasionally existential email to Bhavi, reminding him to cough up his ₹216 for the legendary kadhai. The reminders are so creative, even Gordon Ramsay would be proud (or at least mildly amused).

## Why does this exist?

Because friendship is built on trust, laughter, and the relentless pursuit of unpaid cookware debts. Also, because Bhavi still hasn't paid.

## How does it work?

- Stores a list of hilarious reminder messages.
- Rotates through them daily, so Bhavi never gets bored (or comfortable).
- Sends an email using your SMTP credentials (set in `.env`).
- Logs everything, so you can prove you tried your best.

## Setup

1. Clone this repo.
2. Copy `.env.example` to `.env` and fill in your SMTP details.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run it:
   ```bash
   python3 reminder.py
   ```

## Environment Variables

- `SMTP_HOST` - Your SMTP server (e.g., smtp.gmail.com)
- `SMTP_PORT` - SMTP port (e.g., 587)
- `SMTP_USER` - Your email address
- `SMTP_PASS` - Your email password or app password
- `FROM_EMAIL` - (Optional) Sender email (defaults to SMTP_USER)
- `TO_EMAIL` - (Optional) Recipient email (defaults to SMTP_USER)

## Can I use this for other debts?

Absolutely! Just change the messages and recipient. But remember: with great power comes great responsibility (and possibly annoyed friends).

