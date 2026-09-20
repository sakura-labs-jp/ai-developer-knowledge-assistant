from backend.repositories.kc_knowledge_embedding_repository import (
    get_kc_knowledge_without_embedding,
    insert_kc_embedding,
)
from backend.services.embedding import (
    create_embedding,
    EMBEDDING_MODEL,
)


def build_kc_embeddings() -> None:
    """
    Generate embeddings only for KC knowledge units
    that do not yet have an embedding for the
    current embedding model.
    """

    knowledge_list = (
        get_kc_knowledge_without_embedding(
            EMBEDDING_MODEL
        )
    )

    print(
        f"Found {len(knowledge_list)} "
        f"KC knowledge units without embeddings."
    )

    for knowledge in knowledge_list:

        knowledge_id = knowledge["KnowledgeId"]
        knowledge_type = knowledge["KnowledgeType"]
        content = knowledge["Content"]

        # Include type in the embedded text.
        # This gives the semantic representation
        # additional context.
        text = (
            f"Knowledge Type: {knowledge_type}\n"
            f"Content: {content}"
        )

        print(
            f"Creating embedding: "
            f"KnowledgeId={knowledge_id}"
        )

        vector = create_embedding(
            text
        )

        insert_kc_embedding(
            knowledge_id=knowledge_id,
            model=EMBEDDING_MODEL,
            vector=vector,
        )

    print(
        "KC embedding generation completed."
    )


if __name__ == "__main__":
    build_kc_embeddings()