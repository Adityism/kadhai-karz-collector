import smtplib
from email.mime.text import MIMEText
import random
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
FROM_EMAIL = os.getenv("FROM_EMAIL", SMTP_USER)
TO_EMAIL = os.getenv("TO_EMAIL", SMTP_USER)  # fallback to self if not set

messages = [
    # 1. Polite baseline
    "🍳 Hey Bhavi! Just a friendly reminder about the kadhai contribution of ₹216. Hope you're doing well! 😊\n\n(This is an automated reminder)",

    # 2. Poetic roast
    "💸 Roses are red, curries are divine,\nBut nothing gets cooked without your ₹216. 🍲\nPay up, legend, before the onions start charging interest. 🧅💀\n\n-- Automated Reminder (Poetry Dept.)",

    # 3. Existential wisdom
    "🌌 Bhavi, life is short. You breathe, you blink, you die… but somewhere in between, you still owe ₹216 for the kadhai. ⏳\nBe remembered as a man of honor, not a man of unpaid cookware debt. ⚔️\n\n-- Automated Reminder (Existential Crisis Division)",

    # 4. Savage roast
    "🔥 Breaking News: Kadhai fund collapses after Bhavi withholds ₹216. Markets in turmoil. Economists baffled. Gordon Ramsay crying in a corner. 📉😭\nBe the hero, Bhavi. Send the money.\n\n-- Automated Reminder (CNBC Edition)",

    # 5. Fake motivational quote
    "✨ 'Great men aren’t remembered for what they kept, but for the ₹216 they gave towards a kadhai.' - Definitely Not Aristotle 📜\n\nBhavi, make history. Pay the fund.\n\n-- Automated Reminder (Fake Quotes Inc.)",

    # 6. Absurd life lesson
    "🌱 Every seed grows with water. Every friendship grows with trust. And every kadhai only grows with Bhavi’s ₹216. 🪴\nIf you don’t pay, tomorrow’s sabzi is just boiled sadness. 🥦😭\n\n-- Automated Reminder (Philosophy Kitchen)",

    # 7. Mock inspirational speech
    "🎤 'I have a dream… that one day, Bhavi will finally pay his ₹216 for the kadhai.' - Martin Luth— ok maybe not him, but definitely me. 🤷‍♂️\nDon’t kill the dream, bro. Pay today.\n\n-- Automated Reminder (History Remix)",

    # 8. Brutal life roast
    "☕ Bhavi, you’ve ignored this ₹216 so long that even your coffee is judging you. The beans are whispering: 'Wow, still no kadhai money?' ☕😒\nSave your reputation. Send it now.\n\n-- Automated Reminder (Coffee Council)",

    # 9. Over-the-top dramatic
    "⚡ Imagine: thunder cracks, lightning strikes, and a voice from the heavens screams — 'Where is Bhavi’s ₹216?!' ⚡\nDon’t anger the gods of cookware, my friend.\n\n-- Automated Reminder (Divine Intervention Squad)",

    # 10. Savage but funny
    "😂 Bhavi, I set this reminder daily because faith is eternal. Somewhere, deep down, I believe you’ll pay ₹216 for the kadhai. 🙏\nDon’t make me automate this into the afterlife.\n\n-- Automated Reminder (Haunting Services Inc.)"
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
    with open(index_file, 'w') as f:
        f.write(str((idx + 1) % total))
    return next_idx

def send_email():
    index_file = os.path.join(os.path.dirname(__file__), '.reminder_index')
    msg_idx = get_next_index(index_file, len(messages))
    message_text = messages[msg_idx]
    msg = MIMEText(message_text)
    msg['Subject'] = "Daily Reminder: Kadhai Contribution"
    msg['From'] = FROM_EMAIL
    msg['To'] = TO_EMAIL

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(FROM_EMAIL, TO_EMAIL, msg.as_string())
        print(f"✅ Email sent successfully at {datetime.now()} (Message {msg_idx+1} of {len(messages)})")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    send_email()
