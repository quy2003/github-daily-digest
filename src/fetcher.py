"""Fetches trending repositories from GitHub API by topic."""
import time
import requests


def fetch_trending_repos(topics: dict, per_topic: int) -> list:
    """
    Fetch top repos per topic category from GitHub Search API.

    Args:
        topics: dict mapping category name to list of topic keywords
        per_topic: number of repos to fetch per topic keyword

    Returns:
        List of repo dicts with keys: name, description, stars, url, language, topic_category
    """
    results = []

    for category, keywords in topics.items():
        category_repos = []
        seen = set()

        for keyword in keywords:
            repos = _search_github(keyword, per_topic)
            for repo in repos:
                if repo["name"] not in seen:
                    seen.add(repo["name"])
                    repo["topic_category"] = category
                    category_repos.append(repo)

            time.sleep(1)  # Respect GitHub API rate limit

        # Take top per_topic repos by stars for this category
        category_repos.sort(key=lambda r: r["stars"], reverse=True)
        results.extend(category_repos[:per_topic])

    return results


def _search_github(keyword: str, count: int) -> list:
    """Search GitHub for repos with given topic, sorted by stars."""
    url = "https://api.github.com/search/repositories"
    params = {
        "q": f"topic:{keyword}",
        "sort": "stars",
        "order": "desc",
        "per_page": count,
    }
    headers = {"Accept": "application/vnd.github.v3+json"}

    try:
        resp = requests.get(url, params=params, headers=headers, timeout=10)
        resp.raise_for_status()
        items = resp.json().get("items", [])
        return [
            {
                "name": item["full_name"],
                "description": item.get("description") or "Không có mô tả.",
                "stars": item.get("stargazers_count", 0),
                "url": item["html_url"],
                "language": item.get("language") or "N/A",
            }
            for item in items
        ]
    except Exception as e:
        print(f"   ⚠️  GitHub API error for keyword '{keyword}': {e}")
        return []
