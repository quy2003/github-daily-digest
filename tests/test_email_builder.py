import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.email_builder import build_email_html
import config

SAMPLE_REPOS = [
    {
        "name": "openai/gpt4",
        "description": "GPT-4 model",
        "stars": 50000,
        "url": "https://github.com/openai/gpt4",
        "language": "Python",
        "topic_category": "🤖 AI & Machine Learning",
        "summary_vi": "Đây là mô hình AI mạnh nhất của OpenAI.",
    },
    {
        "name": "scrapy/scrapy",
        "description": "A scraping framework",
        "stars": 30000,
        "url": "https://github.com/scrapy/scrapy",
        "language": "Python",
        "topic_category": "💰 MMO & Automation",
        "summary_vi": "Framework để tự động thu thập dữ liệu từ web.",
    },
]


def test_build_email_returns_html_string():
    html = build_email_html(SAMPLE_REPOS, config.TOPICS)
    assert isinstance(html, str)
    assert "<html" in html


def test_build_email_contains_repo_names():
    html = build_email_html(SAMPLE_REPOS, config.TOPICS)
    assert "openai/gpt4" in html
    assert "scrapy/scrapy" in html


def test_build_email_contains_vietnamese_summary():
    html = build_email_html(SAMPLE_REPOS, config.TOPICS)
    assert "Đây là mô hình AI" in html


def test_build_email_contains_category_headers():
    html = build_email_html(SAMPLE_REPOS, config.TOPICS)
    assert "🤖 AI" in html
    assert "💰 MMO" in html
