# CLAUDE.md — Agent: Sửa hàng loạt PDF Đề Nghị Thanh Toán

> Brain của agent. Phần body (server, Docker, deploy) do Claude Code lo theo skill AgentBase.

## 🎯 Use case
Sửa thông tin **hàng loạt** trên các file PDF "Đề nghị thanh toán" mà không phải
chuyển sang Word rồi sửa tay từng cái. Người dùng tải nhiều PDF lên, chọn trường cần
đổi (số tiền, ngày, tên NCC…), tool tìm và thay rồi xuất lại hàng loạt (PDF/Word/zip).

## 📥 Input
- Nhiều file PDF "Đề nghị thanh toán" (tải lên ngay trên giao diện).
- Trường cần thay đổi và giá trị mới (đổi chung cho tất cả, hoặc sửa riêng từng file).

## 🧠 Vai trò của AI
Tool xử lý PDF hoàn toàn ở client. AI chỉ làm **một việc**: khi bấm
"🤖 AI đọc & điền tự động", tool gửi nội dung text từng chứng từ tới `POST /api/ai`
và yêu cầu AI **trích GIÁ TRỊ HIỆN TẠI của từng trường** (mã, ngày, số tiền, tên NCC…)
trả về dưới dạng **một object JSON** (khóa = mã trường, giá trị = chuỗi lấy đúng từ văn bản).
Tool dùng kết quả này điền sẵn cột "giá trị hiện tại" để người dùng so & thay.

## 📤 Output
- Các file PDF đã sửa, tải về hàng loạt (zip), hoặc xuất kèm bản Word.

## 🚫 Rule cứng (đã nhúng trong prompt của tool)
- AI chỉ **trích đúng** giá trị có trong văn bản; không tìm thấy thì trả chuỗi rỗng.
- Chỉ trả về **một object JSON duy nhất**, không giải thích, không markdown.
- AI **không** tự quyết định giá trị mới — việc đổi thành gì do người dùng nhập.

## ⚙️ Ghi chú kỹ thuật cho deploy (cho Claude Code)
- Frontend gọi `POST /api/ai` với body `{messages:[...], temperature, max_tokens}` và
  **chờ nhận về `{content: "<chuỗi>"}`** (chuỗi này chứa JSON; client tự cắt từ `{` đến `}`).
- Backend `agent.py` đã hiện thực đúng hợp đồng đó. Việc còn lại: **wiring model** qua
  3 biến môi trường `LLM_BASE_URL` / `LLM_API_KEY` / `LLM_MODEL` (chuẩn OpenAI
  `/chat/completions`) sang model mà **AgentBase cung cấp**. Nếu AgentBase dùng giao thức
  khác (vd Anthropic), chỉ cần sửa hàm `call_model()` trong `agent.py` cho khớp, nhớ vẫn
  **trả `content` dạng chuỗi**.
- Nếu chưa cấu hình model, `/api/ai` trả lỗi 503 rõ ràng — giao diện vẫn mở được, các
  chức năng sửa/xuất PDF (không cần AI) vẫn chạy bình thường; chỉ nút "AI đọc & điền" cần model.
