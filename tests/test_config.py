import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


def test_topics_has_three_categories():
    assert len(config.TOPICS) == 3


def test_each_topic_has_keywords():
    for name, keywords in config.TOPICS.items():
        assert len(keywords) >= 3, f"{name} needs at least 3 keywords"


def test_email_recipient_is_set():
    assert "@" in config.EMAIL_RECIPIENT


def test_repos_per_topic_is_positive():
    assert config.REPOS_PER_TOPIC > 0
