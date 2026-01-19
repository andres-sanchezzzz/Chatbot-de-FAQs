import streamlit as st

from src.kb_loader import load_faq_kb
from src.retriever import retrieve_faq
from src.llm import generate_answer, summarize_web_content
from src.guardrails import apply_guardrails
from src.web_search import google_search, extract_page_text

ALLOWED_WEB_DOMAINS = [
    "mintrabajo.gov.co"
    "minjusticia.gov.co"
]

st.set_page_config(
    page_title="Chatbot FAQs - Nómina y Contratación",
    layout="centered",
)

st.title("Chatbot de FAQs - Nómina y Contratación")
st.caption(
    "Este asistente responde únicamente con base en la información oficial "
    "contenida en la base de conocimiento."
)

@st.cache_data
def load_kb():
    return load_faq_kb("C:\\Users\\Andres\\Desktop\\prueba IA\\faqs\\FAQ_Chatbot_Nomina.xlsx", "Sheet1")


kb = load_kb()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Escribe tu pregunta aquí...")

if user_input:
    st.session_state.chat_history.append(
        {"role": "user", "content": user_input}
    )
    with st.chat_message("user"):
        st.markdown(user_input)

    result = retrieve_faq(
        user_question=user_input,
        kb=kb,
        threshold=80,
        top_k=3,
    )

    allowed, block_message, tone, use_web_search = apply_guardrails(
        user_question=user_input,
        retrieval_result=result,
    )

    if allowed:
        faq = result["best_match"]["faq"]
        answer = generate_answer(
            user_question=user_input,
            faq=faq,
            tone=tone
        )
    elif use_web_search:
        web_results = google_search(user_input, max_results=3)
        
        if web_results:
            page = web_results[0]
            text = extract_page_text(page["url"])
            answer = summarize_web_content(
                user_question=user_input,
                web_text=text,
                source_url=page["url"],
            )
        else:
            answer = "No se encontró información oficial disponible."
    else:
        answer = block_message

    st.session_state.chat_history.append(
        {"role": "assistant", "content": answer}
    )

    with st.chat_message("assistant"):
        st.markdown(answer)

st.divider()

if st.button("Reiniciar conversación"):
    st.session_state.chat_history = []
    st.experimental_rerun()
