from backend.services.retrieval import search_knowledge
from backend.services.gemini import ask_gemini
from backend.services.knowledge_formatter import create_context
from backend.repositories.knowledge_repository import get_knowledge_by_id


def ask_with_knowledge(question: str) -> dict:
    """
    Retrieve relevant knowledge and generate an answer using Gemini.
    """

    # 1. Semantic Search
    results = search_knowledge(question)

    # 2. Retrieve knowledge details
    matched_results = []

    for result in results:
        row = get_knowledge_by_id(
            result["KnowledgeId"]
        )

        if row:
            matched_results.append(
                {
                    "result": result,
                    "row": row
                }
            )

    rows = [
        item["row"]
        for item in matched_results
    ]

    # 3. Create context for Gemini
    context = create_context(rows)

    # 4. Generate answer
    prompt = f"""
You are an AI Developer Knowledge Assistant.

Answer the user's question using the knowledge below whenever it is relevant.

If the knowledge does not contain enough information to answer the question,
clearly state that the available knowledge is insufficient.

Knowledge:
{context}

User Question:
{question}
"""

    answer = ask_gemini(prompt)

    # 5. Return answer + source information
    source = None

    if matched_results:
        top_result = matched_results[0]["result"]
        top_row = matched_results[0]["row"]

        source = {
            "knowledge_id": top_result["KnowledgeId"],
            "title": top_row.Title,
            "category": top_row.Category,
            "technology": top_row.Technology,
            "similarity": top_result["Score"]
        }

    return {
        "answer": answer,
        "source": source
    }