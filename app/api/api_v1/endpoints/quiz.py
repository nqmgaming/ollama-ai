from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.token import Token
from ollama import chat

router = APIRouter()

@router.post("/generate_quiz")
def generate_quiz(topic: str, db: Session = Depends(get_db)):
    """
    Tạo quiz dựa trên chủ đề được cung cấp.
    """
    prompt = f"""Bạn là một người tạo câu đố.
    Tạo một câu đố gồm 5 câu hỏi trắc nghiệm về {topic}. 
    Mỗi câu hỏi nên có 4 lựa chọn (A, B, C, D) và chỉ có một đáp án đúng.

    Trả về kết quả ở định dạng JSON như ví dụ sau:
    ```json
    [
      {{
        "question": "Câu hỏi...",
        "choices": ["A) ...", "B) ...", "C) ...", "D) ..."],
        "answer": "Đáp án..." 
      }},
      // ... các câu hỏi khác ...
    ]
    ``` 
    """

    response = chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}],
        format="json",
    )

    # Kiểm tra xem response có phải là JSON hợp lệ hay không
    if isinstance(response, dict) and "message" in response and "content" in response["message"]:
        quiz_json = response["message"]["content"]
        return {"quiz": quiz_json, "message": "Quiz generated successfully"}
    else:
        return {"error": "Invalid JSON format from Ollama."}, 500
