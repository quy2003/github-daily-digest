"""Sends HTML email via Brevo SMTP."""
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def build_subject(prefix: str) -> str:
    """Build email subject with Vietnamese weekday and today's date."""
    today = datetime.now().strftime("%d/%m/%Y")
    day_vi = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"]
    weekday = day_vi[datetime.now().weekday()]
    return f"{prefix} · {weekday}, {today} | AI · MMO · Marketing"


def send_email(html: str, recipient: str, smtp_host: str, smtp_port: int,
               smtp_user: str, smtp_pass: str, email_from: str,
               subject_prefix: str) -> bool:
    """
    Send HTML email via SMTP.

    Args:
        html: Complete HTML email content
        recipient: Destination email address
        smtp_host: SMTP server hostname
        smtp_port: SMTP server port
        smtp_user: SMTP username
        smtp_pass: SMTP password
        email_from: Sender email address
        subject_prefix: Email subject prefix string

    Returns:
        True if sent successfully, False otherwise
    """
    subject = build_subject(subject_prefix)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"GitHub Digest 📬 <{email_from}>"
    msg["To"] = recipient
    msg.attach(MIMEText(html, "html", "utf-8"))

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.ehlo()
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.sendmail(email_from, [recipient], msg.as_string())
        print(f"   ✅ Email sent to {recipient}")
        return True
    except Exception as e:
        print(f"   ❌ Failed to send email: {e}")
        return False
