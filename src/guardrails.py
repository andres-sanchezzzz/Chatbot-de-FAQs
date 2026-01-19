from typing import Dict, Tuple

BLOCKED_KEYWORDS = [
    "salario de",
    "documento",
    "cedula",
    "contraseña",
    "password",
    "datos personales",
    "correo personal",
]

DEFAULT_TONE = "neutral"

TONE_RULES = {
    "empatico": [
        "problema",
        "error",
        "no puedo",
        "inconveniente",
        "reclamo",
    ],
    "directo": [
        "cuando",
        "fecha",
        "horario",
        "pago",
    ],
}

OUT_OF_SCOPE_MESSAGE = (
    "Lo siento, esta pregunta está fuera del alcance de la información disponible actualmente."
)

SENSITIVE_MESSAGE = (
    "No puedo ayudar con esa solicitud, ya que involucra información sensible o personal."
)

def apply_guardrails(user_question, retrieval_result):

    question_norm = user_question.lower()

    tone = detect_tone(question_norm)

    for keyword in BLOCKED_KEYWORDS:
        if keyword in question_norm:
            return False, SENSITIVE_MESSAGE, DEFAULT_TONE, False

    if not retrieval_result.get("in_scope", False):
        print("DEBUG | should_use_web_search:", use_web_search(retrieval_result, user_question))
        return False, OUT_OF_SCOPE_MESSAGE, DEFAULT_TONE, use_web_search(retrieval_result, user_question)

    return True, None, tone, False

def detect_tone(question_norm):
    for tone, keywords in TONE_RULES.items():
        for kw in keywords:
            if kw in question_norm:
                return tone

    return DEFAULT_TONE

def use_web_search(retrieval_result, user_question):
    if retrieval_result.get("in_scope"):
        return False

    keywords = [
        "ley",
        "decreto",
        "norma",
        "ministerio",
        "mintrabajo",
        "legal",
    ]

    q = user_question.lower()
    return any(k in q for k in keywords)
    