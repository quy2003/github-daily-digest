import os
from dotenv import load_dotenv

# Load .env file nếu chạy local (GitHub Actions dùng Secrets thay thế)
load_dotenv()

TOPICS = {
    "🤖 AI & Machine Learning": [
        "llm", "agent", "generative-ai", "machine-learning", "ai-tools"
    ],
    "💰 MMO & Automation": [
        "scraper", "automation", "bot", "affiliate", "web-scraping"
    ],
    "📈 Digital Marketing": [
        "seo", "analytics", "email-marketing", "social-media-automation", "growth-hacking"
    ],
}

REPOS_PER_TOPIC = 5
EMAIL_RECIPIENT = "quylmhs173279@fpt.edu.vn"
EMAIL_SUBJECT_PREFIX = "📬 GitHub Digest"
GEMINI_MODEL = "gemini-2.0-flash"

SMTP_HOST = "smtp-relay.brevo.com"
SMTP_PORT = 587
SMTP_USER = os.environ.get("BREVO_SMTP_USER", "")
SMTP_PASS = os.environ.get("BREVO_SMTP_PASS", "")
EMAIL_FROM = os.environ.get("EMAIL_FROM", SMTP_USER)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
