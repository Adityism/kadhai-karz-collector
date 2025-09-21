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

   "🎤 Imagine the crowd cheering: ‘Bhavi did it! The kadhai is complete!’ All it takes is ₹216 to make the story real. This is an automated reminder.",

    "🌌 Bhavi, life is short. You breathe, you blink, you die… but somewhere in between, you still owe ₹216 for the kadhai. This is an automated reminder.",

    "📰 Breaking News: The kadhai fund is still short by ₹216. Economists confused 📉, chefs worried 👨‍🍳, friends waiting. This is an automated reminder.",

    "📜 ‘Great people aren’t remembered for what they kept, but for the ₹216 they gave towards a kadhai.’ Time to make history — This is an automated reminder.",

    "🌱 Every seed grows with water. Every friendship grows with trust. And this kadhai fund grows only when Bhavi pays ₹216. This is an automated reminder.",

    "🎤 I have a dream… that one day, Bhavi will finally pay his ₹216 for the kadhai. Until then, this is an automated reminder.",

    "⚡ Bhavi, thunder strikes, lightning cracks, and somewhere a kadhai still waits for ₹216. Don’t test destiny — this is an automated reminder.",

    "🙏 Faith is eternal. That’s why I send this daily. Deep down, I believe you’ll pay ₹216 for the kadhai. This is an automated reminder.",

    "🙏 Heaven is closed, Bhavi. Not because you sinned, but because St. Peter is short ₹216 for the kadhai fund. They don’t take excuses at the gate. This is an automated reminder."
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
