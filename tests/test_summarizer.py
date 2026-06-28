import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import patch, MagicMock
from src.summarizer import summarize_repos, build_prompt

SAMPLE_REPOS = [
    {
        "name": "openai/gpt4",
        "description": "GPT-4 large language model",
        "stars": 50000,
        "url": "https://github.com/openai/gpt4",
        "language": "Python",
        "topic_category": "🤖 AI & Machine Learning",
    }
]


def test_build_prompt_contains_repo_info():
    prompt = build_prompt("openai/gpt4", "GPT-4 large language model", "🤖 AI")
    assert "openai/gpt4" in prompt
    assert "GPT-4 large language model" in prompt
    assert "tiếng Việt" in prompt


def test_summarize_adds_summary_vi_key():
    with patch("src.summarizer.genai") as mock_genai:
        mock_model = MagicMock()
        mock_model.generate_content.return_value.text = "Đây là tóm tắt tiếng Việt."
        mock_genai.GenerativeModel.return_value = mock_model

        result = summarize_repos(
            [repo.copy() for repo in SAMPLE_REPOS],
            api_key="fake-key",
            model="gemini-1.5-flash"
        )

    assert "summary_vi" in result[0]
    assert len(result[0]["summary_vi"]) > 0


def test_summarize_falls_back_on_error():
    with patch("src.summarizer.genai") as mock_genai:
        mock_genai.GenerativeModel.side_effect = Exception("API error")
        result = summarize_repos(
            [repo.copy() for repo in SAMPLE_REPOS],
            api_key="fake-key",
            model="gemini-1.5-flash"
        )

    assert "summary_vi" in result[0]
    assert result[0]["summary_vi"] == SAMPLE_REPOS[0]["description"]
