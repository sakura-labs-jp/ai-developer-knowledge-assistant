from backend.services.retrieval import search_knowledge
from backend.services.gemini import ask_gemini
from backend.services.knowledge_formatter import create_context
from backend.repositories.knowledge_repository import get_knowledge_by_id


def ask_with_knowledge(question: str):
    """
    Retrieve relevant knowledge and generate an answer using Gemini.
    """

    # 1. Semantic Search
    results = search_knowledge(question)

    # 2. Retrieve knowledge details
    rows = []

    for result in results:

        row = get_knowledge_by_id(
            result["KnowledgeId"]
        )

        if row:
            rows.append(row)

    # 3. Create context for Gemini
    context = create_context(rows)

    # 4. Generate answer
    prompt = f"""
You are an AI Developer Knowledge Assistant.

Answer the user's question using the knowledge below whenever it is relevant.

Knowledge:
{context}

User Question:
{question}
"""

    return ask_gemini(prompt)