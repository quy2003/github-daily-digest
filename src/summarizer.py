"""Summarizes GitHub repos in Vietnamese using Google Gemini AI."""
import time
import google.generativeai as genai


def build_prompt(name: str, description: str, category: str) -> str:
    """Build Vietnamese summary prompt for Gemini."""
    return f"""Hãy tóm tắt repo GitHub này bằng tiếng Việt đơn giản, dành cho người không có nền tảng kỹ thuật.
Viết đúng 2-3 câu ngắn gọn theo format:
1. Repo này làm gì (giải thích như nói chuyện bình thường)
2. Tại sao người làm {category} nên biết về nó

Repo: {name}
Mô tả gốc: {description}

Chỉ trả lời bằng tiếng Việt, không cần tiêu đề hay định dạng thêm."""


def summarize_repos(repos: list, api_key: str, model: str) -> list:
    """
    Add Vietnamese AI summary to each repo dict.

    Args:
        repos: list of repo dicts from fetcher
        api_key: Google Gemini API key
        model: Gemini model name (e.g. 'gemini-1.5-flash')

    Returns:
        Same list with 'summary_vi' key added to each repo
    """
    try:
        genai.configure(api_key=api_key)
        gemini = genai.GenerativeModel(model)
    except Exception as e:
        print(f"   ⚠️  Gemini init error: {e}")
        for repo in repos:
            repo["summary_vi"] = repo["description"]
        return repos

    for i, repo in enumerate(repos):
        print(f"   🤖 Summarizing [{i+1}/{len(repos)}]: {repo['name']}")
        try:
            prompt = build_prompt(repo["name"], repo["description"], repo["topic_category"])
            response = gemini.generate_content(prompt)
            repo["summary_vi"] = response.text.strip()
        except Exception as e:
            print(f"      ⚠️  Gemini error for {repo['name']}: {e}")
            repo["summary_vi"] = repo["description"]

        time.sleep(5)  # Avoid Gemini rate limit (15 RPM)

    return repos
