"""Summarizes GitHub repos in Vietnamese using Google Gemini AI."""
import json
import google.generativeai as genai


def summarize_repos_combined(repos: list, api_key: str, model: str) -> tuple:
    """
    Summarize all repos and generate a trend summary in a single Gemini API call.
    Returns: (list_of_repos, trend_summary_string)
    """
    if not repos:
        return [], "Không có repository nào để phân tích hôm nay."

    repo_data = []
    for i, r in enumerate(repos):
        repo_data.append({
            "index": i,
            "name": r["name"],
            "description": r["description"],
            "category": r["topic_category"]
        })

    prompt = f"""Bạn là một chuyên gia phân tích công nghệ. Hãy phân tích danh sách các repository đang trending trên GitHub dưới đây và thực hiện hai nhiệm vụ:

1. Viết một đoạn tóm tắt xu hướng nổi bật gần đây trên GitHub (khoảng 3-4 câu) bằng tiếng Việt dễ hiểu cho người không có nền tảng kỹ thuật (non-tech).
2. Tóm tắt từng repository bằng tiếng Việt (2-3 câu ngắn gọn) giải thích repo làm gì và tại sao người làm trong lĩnh vực đó nên biết.

Danh sách các repository:
{json.dumps(repo_data, ensure_ascii=False, indent=2)}

Bạn PHẢI trả về kết quả dưới dạng JSON object có cấu trúc chính xác như sau:
{{
  "trend_summary": "đoạn tóm tắt xu hướng nổi bật gần đây của GitHub ở đây",
  "repos": [
    {{
      "index": 0,
      "summary_vi": "tóm tắt tiếng Việt của repo thứ nhất ở đây"
    }},
    {{
      "index": 1,
      "summary_vi": "tóm tắt tiếng Việt của repo thứ hai ở đây"
    }}
  ]
}}

Chú ý: Trả về kết quả CHỈ chứa chuỗi JSON hợp lệ, không có ký tự bao quanh như ```json ... ```.
"""

    try:
        genai.configure(api_key=api_key)
        gemini = genai.GenerativeModel(model)
        
        response = gemini.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        
        result = json.loads(response.text.strip())
        trend_summary = result.get("trend_summary", "Không có tóm tắt xu hướng hôm nay.")
        
        repo_summaries = {item["index"]: item["summary_vi"] for item in result.get("repos", [])}
        for i, repo in enumerate(repos):
            repo["summary_vi"] = repo_summaries.get(i, repo["description"])
            
        print("   ✅ Successfully summarized all repos and generated trend summary in a single call!")
        return repos, trend_summary

    except Exception as e:
        print(f"   ⚠️  Gemini combined summary error: {e}")
        for repo in repos:
            repo["summary_vi"] = repo["description"]
        return repos, "Không thể tải phân tích xu hướng hôm nay do lỗi hạn ngạch hoặc kết nối API."

