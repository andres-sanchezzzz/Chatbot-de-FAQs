from openai import OpenAI
from typing import Dict
import os

from dotenv import load_dotenv
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

SYSTEM_PROMPT = """
Eres un asistente corporativo de Recursos Humanos.
Responde de forma clara, profesional y concisa.

Reglas estrictas:
- Usa ÚNICAMENTE la información proporcionada en la FAQ.
- No inventes información.
- No agregues supuestos.
- Si la información no está explícitamente en la FAQ, no la menciones.
- Incluye la fuente al final en el formato: Fuente: <categoría>.
"""

def generate_answer(user_question, faq, tone):
    prompt = f"""
Pregunta del usuario:
{user_question}
Tono requerido:
{tone}

Información oficial (FAQ):
Categoría: {faq['category']}
Pregunta original: {faq['question']}
Respuesta oficial: {faq['answer']}

Redacta una respuesta clara y útil basada únicamente en la información oficial.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        max_tokens=250,
    )

    final_answer = response.choices[0].message.content.strip()

    if "Fuente:" not in final_answer:
        final_answer += f"\n\nFuente: {faq['category']}"

    return final_answer

def summarize_web_content(user_question, web_text, source_url):
    prompt = f"""
Pregunta del usuario:
{user_question}

Contenido oficial:
{web_text}

Redacta una respuesta clara y concisa usando solo el contenido anterior..
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Eres un asistente legal corporativo. No inventes información.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content.strip() + f"\n\n Fuente: {source_url}"