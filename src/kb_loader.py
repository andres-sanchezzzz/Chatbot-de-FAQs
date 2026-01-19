import pandas as pd
import json
import re
from pathlib import Path

def normalize_text(text):
    if pd.isna(text):
        return ""

    text = str(text).lower()
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    return text

def load_faq_kb(excel_path, sheet_name):
    df = pd.read_excel(excel_path, sheet_name=sheet_name)

    df = df.rename(
        columns={
            "Segmento/categoria de pregunta": "category",
            "pregunta": "question",
            "respuesta": "answer",
        }
    )

    required_cols = {"category", "question", "answer"}
    if not required_cols.issubset(df.columns):
        raise ValueError(
            f"El Excel debe contener las columnas: {required_cols}"
        )

    df = df.dropna(subset=["question", "answer"])

    df["question_norm"] = df["question"].apply(normalize_text)
    df["category_norm"] = df["category"].apply(normalize_text)

    kb = []
    for idx, row in df.iterrows():
        kb.append(
            {
                "id": idx + 1,
                "category": row["category"],
                "question": row["question"],
                "answer": row["answer"],
                "question_norm": row["question_norm"],
                "category_norm": row["category_norm"],
            }
        )

    return kb

def export_kb_to_json(kb, output_path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(kb, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    kb = load_faq_kb("faqs/faq.xlsx")
    export_kb_to_json(kb, "faqs/faq.json")

    print(f"KB cargada correctamente: {len(kb)} FAQs")