from backend.repositories.kc_knowledge_embedding_repository import (
    get_all_kc_knowledge,
    insert_kc_embedding,
)
from backend.services.embedding import (
    create_embedding,
    EMBEDDING_MODEL,
)


def build_kc_embeddings() -> None:

    knowledge_list = get_all_kc_knowledge()

    print(
        f"Found {len(knowledge_list)} KC knowledge units."
    )

    for knowledge in knowledge_list:

        knowledge_id = knowledge["KnowledgeId"]
        knowledge_type = knowledge["KnowledgeType"]
        content = knowledge["Content"]

        # Include type in the embedded text.
        # This gives the semantic representation a little
        # more context than embedding Content alone.
        text = (
            f"Knowledge Type: {knowledge_type}\n"
            f"Content: {content}"
        )

        print(
            f"Creating embedding: "
            f"KnowledgeId={knowledge_id}"
        )

        vector = create_embedding(text)

        insert_kc_embedding(
            knowledge_id=knowledge_id,
            model=EMBEDDING_MODEL,
            vector=vector,
        )

    print("KC embedding generation completed.")


if __name__ == "__main__":
    build_kc_embeddings()