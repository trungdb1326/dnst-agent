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
Tool xử lý PDF hoàn toàn ở client. AI đảm nhận **hai chế độ**, đều qua `POST /api/ai`:

**Chế độ 1 — "AI đọc & điền tự động"**
Tool gửi nội dung text từng chứng từ và yêu cầu AI **trích GIÁ TRỊ HIỆN TẠI** của từng
trường (mã, ngày, số tiền, tên NCC…), trả về một object JSON (khóa = mã trường, giá trị =
chuỗi lấy đúng từ văn bản). Tool điền sẵn cột "giá trị hiện tại" để người dùng so & thay.

**Chế độ 2 — "Sửa hàng loạt bằng câu lệnh tiếng Việt"**
Người dùng nhập câu lệnh tự nhiên (vd: *"đổi tên NCC của file Sacombank thành Công ty XYZ"*).
Tool gửi câu lệnh + nội dung từng file tới AI; AI xác định file nào bị tác động, trường nào
cần đổi và giá trị mới là gì — trả về JSON dạng `{filename: {field: newValue}}`. Tool áp
dụng kết quả ngay, người dùng xem lại ở bước 3 trước khi xuất.

## 📤 Output
- Các file PDF đã sửa, tải về hàng loạt (zip), hoặc xuất kèm bản Word.

## 🚫 Rule cứng (đã nhúng trong prompt của tool)
- Chế độ 1: AI chỉ **trích đúng** giá trị có trong văn bản; không tìm thấy thì trả chuỗi rỗng.
- Chế độ 2: AI chỉ tác động đúng file/trường khớp câu lệnh; file không liên quan bỏ qua hoàn toàn.
- Cả hai chế độ: chỉ trả về **một object JSON duy nhất**, không giải thích, không markdown.

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
