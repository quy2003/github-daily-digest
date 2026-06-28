import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import patch, MagicMock
from src.fetcher import fetch_trending_repos

MOCK_TOPICS = {
    "🤖 AI": ["llm"],
}

MOCK_API_RESPONSE = {
    "items": [
        {
            "full_name": "openai/gpt4",
            "description": "GPT-4 model",
            "stargazers_count": 50000,
            "html_url": "https://github.com/openai/gpt4",
            "language": "Python",
        }
    ]
}


def test_fetch_returns_list_of_repos():
    with patch("src.fetcher.requests.get") as mock_get:
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = MOCK_API_RESPONSE
        mock_get.return_value = mock_resp

        result = fetch_trending_repos(MOCK_TOPICS, per_topic=1)

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["name"] == "openai/gpt4"
    assert result[0]["stars"] == 50000
    assert result[0]["topic_category"] == "🤖 AI"


def test_fetch_handles_api_error_gracefully():
    with patch("src.fetcher.requests.get") as mock_get:
        mock_get.side_effect = Exception("Network error")
        result = fetch_trending_repos(MOCK_TOPICS, per_topic=1)
    assert result == []
