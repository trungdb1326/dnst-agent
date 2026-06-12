"""
Backend cho tool "Sửa hàng loạt PDF Đề Nghị Thanh Toán".
Tool xử lý PDF hoàn toàn ở client; backend chỉ làm 2 việc:
  GET  /         -> phục vụ tool.html
  GET  /health   -> kiểm tra sống
  POST /api/ai   -> nhận {messages, temperature, max_tokens} -> gọi model
                    -> trả {content: "<chuỗi>"}  (đúng hợp đồng tool đang chờ)

Model nối qua 3 biến môi trường (chuẩn OpenAI /chat/completions):
  LLM_BASE_URL, LLM_API_KEY, LLM_MODEL
=> Khi deploy lên AgentBase, Claude Code wiring 3 biến này sang model GreenNode cung cấp.
   Nếu AgentBase dùng giao thức khác, chỉ cần sửa hàm call_model() bên dưới.
"""
import os
import httpx
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI(title="Sửa hàng loạt PDF - Đề Nghị Thanh Toán")
BASE = Path(__file__).parent

@app.get("/", response_class=HTMLResponse)
def index():
    return (BASE / "tool.html").read_text(encoding="utf-8")

@app.get("/health")
def health():
    return {"status": "ok"}

def call_model(messages, temperature=0, max_tokens=1500) -> str:
    """Gọi model OpenAI-compatible, trả về CHUỖI nội dung."""
    base = os.environ.get("LLM_BASE_URL")
    key = os.environ.get("LLM_API_KEY")
    model = os.environ.get("LLM_MODEL", "default")
    if not base or not key:
        raise RuntimeError(
            "Chưa cấu hình model. Set LLM_BASE_URL / LLM_API_KEY / LLM_MODEL "
            "(Claude Code wiring sang model AgentBase khi deploy)."
        )
    r = httpx.post(
        base.rstrip("/") + "/chat/completions",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json={"model": model, "messages": messages,
              "temperature": temperature, "max_tokens": max_tokens},
        timeout=60,
    )
    r.raise_for_status()
    data = r.json()
    return data["choices"][0]["message"]["content"]

@app.post("/api/ai")
async def api_ai(req: Request):
    try:
        body = await req.json()
    except Exception:
        return JSONResponse({"error": "Body không phải JSON hợp lệ."}, status_code=400)

    messages = body.get("messages")
    if not messages:
        return JSONResponse({"error": "Thiếu 'messages'."}, status_code=400)

    try:
        content = call_model(
            messages,
            temperature=body.get("temperature", 0),
            max_tokens=body.get("max_tokens", 1500),
        )
        return {"content": content}
    except RuntimeError as e:
        return JSONResponse({"error": str(e)}, status_code=503)
    except httpx.HTTPStatusError as e:
        return JSONResponse({"error": f"Model trả lỗi {e.response.status_code}."}, status_code=502)
    except Exception as e:
        return JSONResponse({"error": f"Lỗi gọi model: {e}"}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
