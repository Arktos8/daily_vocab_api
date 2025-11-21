from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

# -----------------------------
# Import จากโฟลเดอร์ api/app
# -----------------------------
from .app.database import get_db
from .app.models import Word, PracticeSubmission
from .app.utils import mock_ai_validation

# -----------------------------
# สร้าง FastAPI App
# -----------------------------
app = FastAPI(
    title="Vocabulary Practice API",
    version="1.0.0",
    description="API for vocabulary practice and learning",
)

# อนุญาตให้เว็บจาก port 3000 ยิงได้
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Request Body Model
# -----------------------------
class SentenceRequest(BaseModel):
    word_id: int
    sentence: str

# -----------------------------
# Endpoints
# -----------------------------
@app.get("/api/word")
def get_random_word(db: Session = Depends(get_db)):
    word = db.query(Word).first()
    if not word:
        raise HTTPException(status_code=404, detail="No word found in database")

    return {
        "word": {
            "id": word.id,
            "word": word.word,
            "meaning": word.meaning,
            "difficulty": word.difficulty_level,
        }
    }


@app.post("/api/validate-sentence")
def validate_sentence(request: SentenceRequest, db: Session = Depends(get_db)):

    # หา word จาก DB
    word = db.query(Word).filter(Word.id == request.word_id).first()
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")

    # ประมวลผล mock AI
    result = mock_ai_validation(
        sentence=request.sentence,
        word=word.word,
        difficulty_level=word.difficulty_level,
    )

    # บันทึกลงฐานข้อมูล
    submission = PracticeSubmission(
        user_id=1,
        word_id=word.id,
        submitted_sentence=request.sentence,
        score=result["score"],
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)

    return result


@app.get("/")
def read_root():
    return {
        "message": "Vocabulary Practice API",
        "version": "1.0.0",
        "endpoints": {
            "random_word": "/api/word",
            "validate": "/api/validate-sentence",
            "summary": "/api/summary",
            "history": "/api/history",
        },
    }
