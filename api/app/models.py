from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from .database import Base


class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String(255), nullable=False)
    difficulty_level = Column(String(50), nullable=False)


class PracticeSubmission(Base):
    __tablename__ = "practice_submissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    word_id = Column(Integer, nullable=False)
    submitted_sentence = Column(String(500), nullable=False)
    score = Column(Integer, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
