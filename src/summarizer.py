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


def generate_trend_summary(repos: list, api_key: str, model: str) -> str:
    """
    Generate a 3-4 sentence overview of the latest GitHub trends based on the gathered repos.
    """
    if not repos:
        return "Hôm nay không có xu hướng nổi bật nào được ghi nhận."

    repo_list_str = ""
    for r in repos:
        repo_list_str += f"- {r['name']} ({r['topic_category']}): {r['description']}\n"

    prompt = f"""Dưới đây là danh sách các repository đang thịnh hành (trending) trên GitHub hôm nay trong các lĩnh vực AI, MMO, và Digital Marketing:

{repo_list_str}

Hãy viết một đoạn tóm tắt ngắn (khoảng 3-4 câu) bằng tiếng Việt để giải thích xu hướng công nghệ nổi bật nhất gần đây trên GitHub là gì dựa trên danh sách này.
Yêu cầu:
- Viết bằng ngôn ngữ tiếng Việt đơn giản, dễ hiểu cho người không có nền tảng kỹ thuật (non-tech).
- Không dùng thuật ngữ kỹ thuật quá chuyên sâu mà không giải thích.
- Đi thẳng vào nội dung chính, không chào hỏi hay có tiêu đề.
"""
    try:
        genai.configure(api_key=api_key)
        gemini = genai.GenerativeModel(model)
        response = gemini.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"   ⚠️  Gemini trend summary error: {e}")
        return "Không thể tải tóm tắt xu hướng hôm nay do lỗi kết nối AI."
