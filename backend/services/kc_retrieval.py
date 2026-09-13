from backend.services.embedding import (
    create_embedding,
    EMBEDDING_MODEL,
)
from backend.services.similarity import cosine_similarity
from backend.repositories.kc_knowledge_embedding_repository import (
    get_all_kc_embeddings,
)


def search_kc_knowledge(
    question: str,
    top_k: int = 3,
) -> list[dict]:
    """
    Semantic search for Knowledge Chain knowledge units.
    """

    question_vector = create_embedding(question)

    embeddings = get_all_kc_embeddings()

    results = []

    for item in embeddings:

        if item["Model"] != EMBEDDING_MODEL:
            continue

        score = cosine_similarity(
            question_vector,
            item["Vector"],
        )

        results.append(
            {
                "KnowledgeId": item["KnowledgeId"],
                "Score": score,
            }
        )

    results.sort(
        key=lambda x: x["Score"],
        reverse=True,
    )

    return results[:top_k]


if __name__ == "__main__":

    question = (
        "Why did the nightly batch processing become slow?"
    )

    results = search_kc_knowledge(question)

    print("\n=== KC Semantic Search ===\n")
    print(f"Question: {question}\n")

    for result in results:
        print(
            f"KnowledgeId: {result['KnowledgeId']} "
            f"Score: {result['Score']:.4f}"
        )