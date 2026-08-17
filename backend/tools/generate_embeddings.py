import json

from backend.repositories.knowledge_repository import get_all_knowledge
from backend.repositories.knowledge_embedding_repository import upsert_embedding
from backend.services.embedding import create_embedding, EMBEDDING_MODEL
from backend.services.knowledge_formatter import create_knowledge_text


def main():

    rows = get_all_knowledge()

    print(f"{len(rows)} records found.")

    for row in rows:

        text = create_knowledge_text(row)

        vector = create_embedding(text)

        upsert_embedding(
            knowledge_id=row.KnowledgeId,
            model=EMBEDDING_MODEL,
            vector=json.dumps(vector)
        )

        print(
            f"Embedded: {row.KnowledgeId}"
        )


if __name__ == "__main__":
    main()