"""Builds HTML email from repo list using Jinja2 template."""
from datetime import datetime
from collections import defaultdict
from pathlib import Path
from jinja2 import Environment, FileSystemLoader


def build_email_html(repos: list, topics: dict) -> str:
    """
    Render HTML email from repo list.

    Args:
        repos: list of repo dicts (each must have summary_vi, topic_category)
        topics: dict mapping category names to keywords (used for ordering)

    Returns:
        Complete HTML string
    """
    # Group repos by category
    grouped_repos = defaultdict(list)
    for repo in repos:
        grouped_repos[repo["topic_category"]].append(repo)

    # Sort repos within each category by stars (descending)
    for cat in grouped_repos:
        grouped_repos[cat].sort(key=lambda r: r["stars"], reverse=True)

    # Build template context
    today = datetime.now().strftime("%d/%m/%Y")
    context = {
        "date": today,
        "grouped_repos": dict(grouped_repos),
        "total_repos": len(repos),
        "total_categories": len(grouped_repos),
    }

    # Load and render Jinja2 template
    template_dir = Path(__file__).parent.parent / "templates"
    env = Environment(loader=FileSystemLoader(str(template_dir)))
    template = env.get_template("email_template.html")
    return template.render(**context)
