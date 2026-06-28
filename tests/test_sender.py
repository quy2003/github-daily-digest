import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import patch, MagicMock
from src.sender import send_email, build_subject


def test_build_subject_contains_prefix():
    subject = build_subject("📬 GitHub Digest")
    assert "📬 GitHub Digest" in subject
    assert len(subject) > len("📬 GitHub Digest")  # Has date appended


def test_send_email_returns_true_on_success():
    with patch("src.sender.smtplib.SMTP") as mock_smtp_class:
        mock_smtp = MagicMock()
        mock_smtp_class.return_value.__enter__.return_value = mock_smtp

        result = send_email(
            html="<html><body>Test</body></html>",
            recipient="test@example.com",
            smtp_host="smtp-relay.brevo.com",
            smtp_port=587,
            smtp_user="user@test.com",
            smtp_pass="password",
            email_from="user@test.com",
            subject_prefix="📬 GitHub Digest",
        )

    assert result is True
    assert mock_smtp.sendmail.called


def test_send_email_returns_false_on_smtp_error():
    with patch("src.sender.smtplib.SMTP") as mock_smtp_class:
        mock_smtp_class.side_effect = Exception("SMTP connection failed")

        result = send_email(
            html="<html><body>Test</body></html>",
            recipient="test@example.com",
            smtp_host="smtp-relay.brevo.com",
            smtp_port=587,
            smtp_user="user@test.com",
            smtp_pass="password",
            email_from="user@test.com",
            subject_prefix="📬 GitHub Digest",
        )

    assert result is False
