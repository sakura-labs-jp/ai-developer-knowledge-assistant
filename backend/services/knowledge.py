from repositories.knowledge_repository import search_knowledge
from services.gemini import ask_gemini


def ask_with_knowledge(question: str):
    """
    Retrieve relevant knowledge from SQL Server and
    augment the prompt before sending it to Gemini.
    """

    rows = search_knowledge(question)

    knowledge = "\n\n".join(
        [
            f"""
Title:
{row.Title}

Category:
{row.Category}

Technology:
{row.Technology}

Problem:
{row.Problem}

Analysis:
{row.Analysis}

Solution:
{row.Solution}

Result:
{row.Result}

Lessons Learned:
{row.LessonsLearned}
"""
            for row in rows
        ]
    )

    prompt = f"""
You are an AI Developer Knowledge Assistant.

Answer the user's question using the knowledge below whenever it is relevant.

Knowledge:
{knowledge}

User Question:
{question}
"""

    return ask_gemini(prompt)