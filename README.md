# Agent: Sửa hàng loạt PDF Đề Nghị Thanh Toán và Biên Bản Đối Soát

Tool sửa thông tin hàng loạt trên PDF "Đề nghị thanh toán" — xử lý PDF ngay trên trình
duyệt (pdf.js + pdf-lib), xuất hàng loạt PDF/Word/zip. Hai chế độ AI:
- **"AI đọc & điền tự động"** — trích giá trị hiện tại của từng trường từ văn bản PDF.
- **"Sửa bằng câu lệnh tiếng Việt"** — nhập lệnh tự nhiên, AI hiểu và áp dụng đúng file/trường.

## Mô tả giải pháp

**Vấn đề.** Tại nhiều doanh nghiệp, bộ phận vận hành và kế thường xuyên phải chỉnh sửa thông tin lặp đi lặp lại trên hàng loạt chứng từ "Đề nghị thanh toán" và "Biên bản đối soát" dạng PDF — như tên đơn vị thụ hưởng, số tài khoản,số tiền hay đơn giá. Thường những yêu cầu này xảy ra gấp rút nên đội Tech chưa có timeline để chỉnh sửa tự động thông tin trên hệ thống kịp lúc, cần phải thực hiện manual
Cách làm thủ công hiện nay là chuyển từng file PDF sang Word rồi sửa tay: vừa tốn nhiều giờ đồng hồ, vừa dễ sai sót, làm vỡ bố cục gốc và mất hiệu lực chữ ký số. Khi số lượng chứng từ lên tới hàng chục, hàng trăm file mỗi kỳ, công việc này trở thành gánh nặng thực sự.

**Người dùng.** Nhân viên kế toán và vận hành xử lý chứng từ thanh toán định kỳ

**Agent giải quyết như thế nào.** Người dùng tải nhiều PDF lên; toàn bộ xử lý chạy ngay trên trình duyệt nên dữ liệu nhạy cảm không rời khỏi máy. Agent cung cấp hai chế độ AI: (1) tự động đọc và trích giá trị hiện tại của từng trường để chỉnh sửa, và (2) sửa hàng loạt bằng câu lệnh tiếng Việt tự nhiên — AI hiểu được cả điều kiện riêng cho từng file (ví dụ "giữ nguyên file này, đổi tên thụ hưởng các file còn lại"). Tool giữ nguyên bố cục gốc, xuất lại đúng định dạng PDF/Word và đóng gói .zip; hỗ trợ Biên bản đối soát (thêm cột Đơn giá, tự tính phí, mẫu Điện lực/EVN với đơn giá riêng từng đơn vị) và chế độ "Chọn tay" để chỉ định trực tiếp vị trí cần sửa ngay trên file.

**Giá trị mang lại.** Rút ngắn thời gian từ nhiều giờ xuống còn vài phút, giảm sai sót thủ công, giữ trọn định dạng bản gốc, và an toàn dữ liệu nhờ xử lý hoàn toàn phía client. Giao diện và câu lệnh bằng tiếng Việt giúp cả người không rành kỹ thuật cũng dùng được ngay, không cần đào tạo.

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
