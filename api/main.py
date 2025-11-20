from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .app.database import get_db
from .app.models import Word, PracticeSubmission
from .app.utils import mock_ai_validation


app = FastAPI(
    title="Vocabulary Practice API",
    version="1.0.0",
    description="API for vocabulary practice and learning"
)


class SentenceRequest(BaseModel):
    word_id: int
    sentence: str


@app.get("/api/word")
def get_random_word():
    return {
        "word": "example",
        "definition": "a representative form or pattern",
        "difficulty_level": "Beginner"
    }


@app.post("/api/validate-sentence")
def validate_sentence(request: SentenceRequest, db: Session = Depends(get_db)):
    word = db.query(Word).filter(Word.id == request.word_id).first()
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")

    result = mock_ai_validation(
        sentence=request.sentence,
        word=word.word,
        difficulty_level=word.difficulty_level
    )

    submission = PracticeSubmission(
        user_id=1,
        word_id=request.word_id,
        submitted_sentence=request.sentence,
        score=result["score"]
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
            "history": "/api/history"
        }
    }
