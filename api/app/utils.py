def mock_ai_validation(sentence: str, word: str, difficulty_level: str):
    score = 85
    level = "Intermediate"
    suggestion = "Good job! Just a minor correction needed."
    corrected_sentence = "This is the corrected sentence."

    return {
        "score": score,
        "level": level,
        "suggestion": suggestion,
        "corrected_sentence": corrected_sentence
    }
