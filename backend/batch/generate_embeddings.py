from backend.repositories.knowledge_repository import get_all_knowledge
from backend.services.knowledge_formatter import create_knowledge_text
from backend.services.embedding import create_embedding
from backend.repositories.knowledge_embedding_repository import insert_embedding


def generate_embeddings():

    rows = get_all_knowledge()

    print(f"{len(rows)} knowledge records found.")

    for row in rows:

        text = create_knowledge_text(row)

        print("====================")
        print(text)
        print("====================")

        vector = create_embedding(text)

        insert_embedding(
            row.KnowledgeId,
            "gemini-embedding-001",
            vector
        )

        print("Embedding saved")

if __name__ == "__main__":
    generate_embeddings()

    