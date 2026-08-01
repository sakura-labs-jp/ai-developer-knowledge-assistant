from backend.services.embedding import create_embedding
from backend.services.similarity import cosine_similarity
from backend.repositories.knowledge_embedding_repository import get_all_embeddings


def search_knowledge(question: str, top_k: int = 3):
    """
    Perform semantic search using embedding vectors.

    The user question is converted into an embedding vector,
    compared against stored knowledge embeddings using cosine
    similarity, and the top-k most relevant knowledge IDs are returned.
    """

    # Generate an embedding vector for the user question
    question_vector = create_embedding(question)

    # Load all stored knowledge embeddings
    embeddings = get_all_embeddings()

    results = []

    for item in embeddings:

        score = cosine_similarity(
            question_vector,
            item["Vector"]
        )

        results.append(
            {
                "KnowledgeId": item["KnowledgeId"],
                "Score": score
            }
        )

    # Sort results by similarity score (highest first)
    results.sort(
        key=lambda x: x["Score"],
        reverse=True
    )

    return results[:top_k]