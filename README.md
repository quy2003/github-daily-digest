# 📬 GitHub Daily Knowledge Digest

Tool tự động gửi email tóm tắt trending repos GitHub mỗi ngày lúc **9:00 AM** (Giờ Việt Nam) về các lĩnh vực **AI, MMO, Digital Marketing**. Nội dung hoàn toàn bằng **Tiếng Việt**, dễ hiểu với người không có nền tảng kỹ thuật.

---

## 🚀 Hướng dẫn setup (chỉ làm 1 lần, khoảng 15 phút)

### Bước 1: Tạo repo GitHub từ project này

1. Đăng nhập vào [github.com](https://github.com)
2. Nhấn dấu **+** góc trên bên phải → **New repository**
3. Đặt tên repo (ví dụ: `github-daily-digest`)
4. Chọn **Private** hoặc **Public** tuỳ ý → nhấn **Create repository**
5. Upload toàn bộ file trong folder này lên repo vừa tạo

### Bước 2: Lấy Gemini API Key (miễn phí)

1. Vào [aistudio.google.com](https://aistudio.google.com)
2. Đăng nhập bằng tài khoản Google
3. Nhấn **Get API key** → **Create API key in new project**
4. Copy key (dạng `AIza...`)

### Bước 3: Tạo tài khoản Brevo và lấy SMTP (miễn phí)

1. Vào [brevo.com](https://brevo.com) → nhấn **Sign up free**
2. Đăng ký bằng email bất kỳ (email "1 lần" cũng được)
3. Sau khi vào dashboard:
   - Vào **Settings** (bánh răng góc trên phải) → **SMTP & API**
   - Copy **SMTP Login** (dạng email) và **Master password**
4. Vào **Contacts** → **Senders** → **Add a sender**
   - Thêm cùng email đó làm sender được xác thực

### Bước 4: Thêm Secrets vào GitHub repo

Trong repo GitHub vừa tạo:
1. Vào **Settings** → **Secrets and variables** → **Actions**
2. Nhấn **New repository secret** và thêm lần lượt 4 secrets sau:

| Secret Name | Giá trị cần nhập |
|---|---|
| `GEMINI_API_KEY` | API key từ Google AI Studio (Bước 2) |
| `BREVO_SMTP_USER` | SMTP Login từ Brevo (Bước 3) |
| `BREVO_SMTP_PASS` | Master password từ Brevo (Bước 3) |
| `EMAIL_FROM` | Email anh đã thêm vào Brevo Senders (Bước 3) |

### Bước 5: Bật GitHub Actions

1. Trong repo, vào tab **Actions**
2. Nếu thấy thông báo, nhấn **I understand my workflows, go ahead and enable them**

### Bước 6: Test thử ngay bây giờ

1. Vào **Actions** → chọn workflow **📬 GitHub Daily Digest**
2. Nhấn **Run workflow** → **Run workflow** (nút xanh)
3. Chờ khoảng 2-3 phút
4. Kiểm tra hộp thư `quylmhs173279@fpt.edu.vn`

> ✅ Nếu nhận được email → Setup thành công! Tool sẽ tự động gửi mỗi ngày lúc 9:00 AM.

---

## 📅 Lịch gửi tự động

| Thời gian | Múi giờ |
|---|---|
| 9:00 AM mỗi ngày | Giờ Việt Nam (UTC+7) |

---

## 📧 Nội dung email mẫu

```
📬 GitHub Digest · Thứ Hai, 28/06/2026 | AI · MMO · Marketing

🤖 AI & Machine Learning (Top 5)
  → openai/gpt4 ⭐ 50,000
     "Đây là thư viện chính thức của OpenAI để dùng mô hình GPT-4.
      Người làm AI automation nên biết vì đây là nền tảng phổ biến nhất hiện nay."

💰 MMO & Automation (Top 5)
  → ...

📈 Digital Marketing (Top 5)
  → ...
```

---

## 💰 Chi phí vận hành: $0/tháng

| Dịch vụ | Free tier | Dùng thực tế |
|---|---|---|
| GitHub Actions | 2,000 phút/tháng | ~5 phút/ngày = 150 phút ✅ |
| Gemini API | 1,500 requests/ngày | ~20 requests/ngày ✅ |
| Brevo SMTP | 300 email/ngày | 1 email/ngày ✅ |

---

## 🗂️ Cấu trúc dự án

```
📁 github-digest/
├── 📁 .github/workflows/
│   └── daily_digest.yml      ← Tự động chạy 9AM mỗi ngày
├── 📁 src/
│   ├── fetcher.py             ← Lấy data từ GitHub API
│   ├── summarizer.py          ← Tóm tắt bằng Gemini AI
│   ├── email_builder.py       ← Tạo email HTML đẹp
│   └── sender.py              ← Gửi email qua Brevo
├── 📁 templates/
│   └── email_template.html    ← Giao diện email dark mode
├── 📁 tests/                  ← Unit tests
├── config.py                  ← Cấu hình chủ đề & email
├── main.py                    ← Điểm khởi động chính
└── requirements.txt           ← Thư viện Python cần thiết
```

---

## ❓ Hỗ trợ

Nếu có vấn đề, kiểm tra log trong tab **Actions** trên GitHub để xem thông báo lỗi chi tiết.
