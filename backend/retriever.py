import os
from dotenv import load_dotenv
from sqlalchemy import text
from sentence_transformers import SentenceTransformer
import numpy as np

from database import engine

load_dotenv()

# ────────────────────────────────────────────────
# EMBEDDING MODEL
# ────────────────────────────────────────────────
model = SentenceTransformer(
    "BAAI/bge-base-en-v1.5",
    trust_remote_code=True
)

# ────────────────────────────────────────────────
# RELATIONAL QUERY
# ────────────────────────────────────────────────
def query_relational_db(sql: str):
    try:
        with engine.connect() as conn:
            result = conn.execute(text(sql))
            rows = result.fetchall()
        return rows or []
    except Exception as e:
        print("❌ Relational DB error:", e)
        return []


# ────────────────────────────────────────────────
# VECTOR SEARCH
# ────────────────────────────────────────────────
def _clean(text_query: str):
    import re
    stopwords = {
        "event","workshop","happen","when","what","where","who","tell",
        "me","about","the","a","an","of","in","on","is","was","did","for"
    }
    text_query = re.sub(r"[^\w\s]", " ", text_query.lower())
    tokens = [w for w in text_query.split() if w not in stopwords]
    return " ".join(tokens) if tokens else text_query


def query_vector_db(text_query: str):
    query = _clean(text_query)

    try:
        embedding = model.encode(query)
        if isinstance(embedding, np.ndarray):
            embedding = embedding.tolist()
    except Exception as e:
        print("❌ Embedding error:", e)
        return ["Embedding failed"]

    try:
        with engine.connect() as conn:
            result = conn.execute(
                text("""
                    SELECT
                        name_of_event,
                        event_domain,
                        date_of_event,
                        time_of_event,
                        venue,
                        description_insights
                    FROM events
                    ORDER BY embedding <-> (:vec)::vector
                    LIMIT 5
                """),
                {"vec": embedding},
            )


            rows = result.fetchall()

        if not rows:
            return ["No matching events found"]

        return [
            f"📌 {r[0]}\n"
            f"• Domain: {r[1]}\n"
            f"• Date: {r[2]}\n"
            f"• Time: {r[3]}\n"
            f"• Venue: {r[4]}\n"
            f"• Details: {r[5]}"
            for r in rows
        ]

    except Exception as e:
        print("❌ Vector DB error:", e)
        return ["Vector search failed"]


# ────────────────────────────────────────────────
# INSERT NEW EVENT (THIS WAS MISSING 🚨)
# ────────────────────────────────────────────────
def add_new_event(form_data: dict):
    try:
        search_text = (
            f"{form_data.get('name_of_event', '')} "
            f"{form_data.get('event_domain', '')} "
            f"{form_data.get('description_insights', '')} "
            f"{form_data.get('perks', '')}"
        )

        embedding = model.encode(search_text)
        if isinstance(embedding, np.ndarray):
            embedding = embedding.tolist()

        with engine.begin() as conn:  # ✅ auto-commit
            conn.execute(
                text(
                    """
                    INSERT INTO events (
                        name_of_event,
                        event_domain,
                        date_of_event,
                        time_of_event,
                        faculty_coordinators,
                        student_coordinators,
                        venue,
                        mode_of_event,
                        registration_fee,
                        speakers,
                        perks,
                        collaboration,
                        description_insights,
                        search_text,
                        embedding
                    )
                    VALUES (
                        :name_of_event,
                        :event_domain,
                        :date_of_event,
                        :time_of_event,
                        :faculty_coordinators,
                        :student_coordinators,
                        :venue,
                        :mode_of_event,
                        :registration_fee,
                        :speakers,
                        :perks,
                        :collaboration,
                        :description_insights,
                        :search_text,
                        :embedding
                    )
                    """
                ),
                {
                    **form_data,
                    "search_text": search_text,
                    "embedding": embedding,
                },
            )

        return {"status": "success"}

    except Exception as e:
        print("❌ Insert error:", e)
        return {"status": "error", "message": str(e)}
