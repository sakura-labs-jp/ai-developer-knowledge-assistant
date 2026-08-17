def create_knowledge_text(row) -> str:
    """
    Create a text representation of a knowledge record
    for embedding generation.
    """

    text = f"""
Category:
{row.Category}

Technology:
{row.Technology}

Title:
{row.Title}

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

Keywords:
{row.Keywords}
"""

    return text.strip()


def create_context(rows) -> str:
    """
    Create context from knowledge records for the Gemini prompt.
    """

    context = "\n\n".join(
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

    return context.strip()