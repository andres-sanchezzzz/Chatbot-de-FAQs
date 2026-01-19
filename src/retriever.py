from rapidfuzz import fuzz, process
from typing import List, Dict, Optional

DEFAULT_THRESHOLD = 60
DEFAULT_TOP_K = 3

def retrieve_faq(user_question, kb, threshold, top_k):

    if not user_question or not user_question.strip():
        return _out_of_scope("Pregunta vacía")

    user_question_norm = _normalize_text(user_question)

    questions_norm = [item["question_norm"] for item in kb]

    matches = process.extract(
        user_question_norm,
        questions_norm,
        scorer=fuzz.token_sort_ratio,
        limit=top_k,
    )

    candidates = []
    for match_text, score, idx in matches:
        candidates.append(
            {
                "score": score,
                "faq": kb[idx],
            }
        )

    best = candidates[0] if candidates else None

    if best and best["score"] >= threshold:
        return {
            "in_scope": True,
            "best_match": best,
            "candidates": candidates,
        }

    return {
        "in_scope": False,
        "best_match": None,
        "candidates": candidates,
        "reason": f"Score máximo ({best['score'] if best else 0}) bajo el umbral ({threshold})",
    }

def _normalize_text(text):
    import re

    text = text.lower().strip()
    text = re.sub(r"\s+", " ", text)
    return text


def _out_of_scope(reason):
    return {
        "in_scope": False,
        "best_match": None,
        "candidates": [],
        "reason": reason,
    }
