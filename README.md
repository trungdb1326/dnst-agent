# Agent: Sửa hàng loạt PDF Đề Nghị Thanh Toán

Tool sửa thông tin hàng loạt trên PDF "Đề nghị thanh toán" — xử lý PDF ngay trên trình
duyệt (pdf.js + pdf-lib), xuất hàng loạt PDF/Word/zip. Có nút "AI đọc & điền tự động"
để AI trích sẵn giá trị hiện tại của từng trường.

## Cấu trúc
```
dnst-agent/
├── CLAUDE.md         # brain
├── agent.py          # backend: phục vụ tool + proxy /api/ai
├── tool.html         # tool (toàn bộ giao diện + xử lý PDF, client-side)
├── requirements.txt
└── Dockerfile
```

## Chạy thử local
```bash
pip install -r requirements.txt
python agent.py        # mở http://localhost:8000
```
Mọi chức năng sửa/xuất PDF chạy được ngay. Riêng nút "AI đọc & điền" cần model (xem dưới).

## Bật AI (Claude Code wiring theo skill AgentBase)
```
LLM_BASE_URL=...   LLM_API_KEY=...   LLM_MODEL=...
```

## Deploy GreenNode AgentBase
Đặt folder này cạnh bộ skill `.agentbase`, để Claude Code chạy skill deploy (Recommended / PUBLIC).
