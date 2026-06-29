import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from unittest.mock import patch, MagicMock
from src.summarizer import summarize_repos_combined

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


def test_summarize_combined_success():
    mock_json_response = {
        "trend_summary": "Xu hướng công nghệ AI nổi bật gần đây.",
        "repos": [
            {
                "index": 0,
                "summary_vi": "Đây là tóm tắt tiếng Việt."
            }
        ]
    }
    with patch("src.summarizer.genai") as mock_genai:
        mock_model = MagicMock()
        mock_model.generate_content.return_value.text = json.dumps(mock_json_response)
        mock_genai.GenerativeModel.return_value = mock_model

        repos, trend = summarize_repos_combined(
            [repo.copy() for repo in SAMPLE_REPOS],
            api_key="fake-key",
            model="gemini-flash-latest"
        )

    assert trend == "Xu hướng công nghệ AI nổi bật gần đây."
    assert repos[0]["summary_vi"] == "Đây là tóm tắt tiếng Việt."


def test_summarize_combined_fallback_on_error():
    with patch("src.summarizer.genai") as mock_genai:
        mock_genai.GenerativeModel.side_effect = Exception("API error")
        repos, trend = summarize_repos_combined(
            [repo.copy() for repo in SAMPLE_REPOS],
            api_key="fake-key",
            model="gemini-flash-latest"
        )

    assert "hạn ngạch" in trend or "kết nối" in trend
    assert repos[0]["summary_vi"] == SAMPLE_REPOS[0]["description"]
