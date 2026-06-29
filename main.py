"""Entry point — orchestrates the full digest pipeline."""
from src.fetcher import fetch_trending_repos
from src.summarizer import summarize_repos
from src.email_builder import build_email_html
from src.sender import send_email
import config


def run():
    print("🚀 GitHub Digest starting...")

    print("📡 Fetching trending repos from GitHub...")
    repos = fetch_trending_repos(config.TOPICS, config.REPOS_PER_TOPIC)
    print(f"   Found {len(repos)} repos")

    print("🤖 Summarizing with Gemini AI...")
    repos = summarize_repos(repos, config.GEMINI_API_KEY, config.GEMINI_MODEL)

    print("🤖 Generating overall trend summary...")
    from src.summarizer import generate_trend_summary
    trend_summary = generate_trend_summary(repos, config.GEMINI_API_KEY, config.GEMINI_MODEL)

    print("📧 Building email...")
    html = build_email_html(repos, config.TOPICS, trend_summary)

    print(f"📨 Sending to {config.EMAIL_RECIPIENT}...")
    send_email(html, config.EMAIL_RECIPIENT, config.SMTP_HOST, config.SMTP_PORT,
               config.SMTP_USER, config.SMTP_PASS, config.EMAIL_FROM,
               config.EMAIL_SUBJECT_PREFIX)

    print("✅ Done! Email sent successfully.")


if __name__ == "__main__":
    run()
