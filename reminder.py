# reminder.py
import smtplib
from email.mime.text import MIMEText
import random
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import sys
import traceback

# Load .env locally (harmless in Actions)
load_dotenv()

messages = [
    "🍳 Hey Bhavi! Just a friendly reminder about the kadhai contribution of ₹216. Hope you're doing well! 😊\n\n(This is an automated reminder)",
    "💸 Roses are red, curries are divine,\nBut nothing gets cooked without your ₹216. 🍲\nPay up, legend, before the onions start charging interest. 🧅💀\n\n-- Automated Reminder (Poetry Dept.)",
    "🌌 Bhavi, life is short. You breathe, you blink, you die… but somewhere in between, you still owe ₹216 for the kadhai. ⏳\nBe remembered as a person of honor, not unpaid cookware debt.\n\n-- Automated Reminder (Existential Division)",
    "🔥 Breaking News: Kadhai fund collapses after Bhavi withholds ₹216. Markets in turmoil. Gordon Ramsay crying in a corner. 📉😭",
    "✨ 'Great people aren’t remembered for what they kept, but for the ₹216 they gave towards a kadhai.' - Definitely Not Aristotle 📜",
    "🌱 Every seed grows with water. Every friendship grows with trust. And every kadhai only grows with Bhavi’s ₹216. 🪴",
    "🎤 'I have a dream… that one day, Bhavi will finally pay his ₹216 for the kadhai.' 🏛️",
    "☕ Bhavi, you’ve ignored this ₹216 so long that even your coffee is judging you. ☕😒",
    "⚡ Imagine: thunder cracks, lightning strikes, and a voice from the heavens screams — 'Where is Bhavi’s ₹216?!' ⚡",
    "😂 Bhavi, I set this reminder daily because faith is eternal. Somewhere, deep down, I believe you’ll pay. 🙏"
]

def get_next_index(index_file, total):
    idx = 0
    try:
        with open(index_file, 'r') as f:
            content = f.read().strip()
            if content:
                idx = int(content)
    except Exception:
        idx = 0
    next_idx = idx % total
    try:
        with open(index_file, 'w') as f:
            f.write(str((idx + 1) % total))
    except Exception as e:
        # non-fatal: just warn
        print("WARNING: could not write index file:", e)
    return next_idx

def safe_str(x):
    # ensure we return a normal str (not bytes/None)
    if x is None:
        return ""
    if isinstance(x, bytes):
        try:
            return x.decode('utf-8')
        except Exception:
            return str(x)
    return str(x)

def send_email():
    # sanitize envs to strings (avoid bytes)
    SMTP_HOST = safe_str(os.getenv("SMTP_HOST", "smtp.gmail.com"))
    SMTP_PORT = int(safe_str(os.getenv("SMTP_PORT", "587")) or 587)
    SMTP_USER = safe_str(os.getenv("SMTP_USER", ""))
    SMTP_PASS = safe_str(os.getenv("SMTP_PASS", ""))
    FROM_EMAIL = safe_str(os.getenv("FROM_EMAIL", SMTP_USER))
    TO_EMAIL = safe_str(os.getenv("TO_EMAIL", SMTP_USER))

    # debug prints (safe: don't print passwords)
    print("DEBUG envs types:")
    print(" SMTP_HOST:", type(SMTP_HOST), SMTP_HOST)
    print(" SMTP_PORT:", type(SMTP_PORT), SMTP_PORT)
    print(" SMTP_USER:", type(SMTP_USER), SMTP_USER)
    print(" FROM_EMAIL:", type(FROM_EMAIL), FROM_EMAIL)
    print(" TO_EMAIL:", type(TO_EMAIL), TO_EMAIL)
    # do NOT print SMTP_PASS

    index_file = os.path.join(os.path.dirname(__file__), '.reminder_index')
    msg_idx = get_next_index(index_file, len(messages))
    message_text = messages[msg_idx]

    # show chosen message in logs (so you can verify)
    print("DEBUG: chosen message index:", msg_idx, "-> preview:")
    preview = message_text if len(message_text) < 300 else (message_text[:300] + "...")
    print(preview)

    # build MIMEText explicitly with utf-8
    msg = MIMEText(message_text, "plain", "utf-8")
    msg['Subject'] = "Daily Reminder: Kadhai Contribution"
    msg['From'] = FROM_EMAIL
    msg['To'] = TO_EMAIL

    try:
        # connect and send
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            # explicit ensure str for login params
            server.login(safe_str(SMTP_USER), safe_str(SMTP_PASS))
            # sendmail expects list of recipients; pass a list
            server.sendmail(FROM_EMAIL, [TO_EMAIL], msg.as_string())
        print(f"✅ Email sent successfully at {datetime.utcnow().isoformat()} (UTC). Message {msg_idx+1}/{len(messages)}")
    except Exception as e:
        # print traceback to logs (Action will capture it)
        print("❌ Error sending email:", repr(e))
        traceback.print_exc()
        # re-raise so GH Action marks failure if desired
        raise

if __name__ == "__main__":
    send_email()