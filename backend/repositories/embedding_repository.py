from database.connection import get_connection


def insert_embedding(
    knowledge_id: int,
    model: str,
    vector: str
):
    """
    Store an embedding vector.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO KnowledgeEmbedding
        (
            KnowledgeId,
            EmbeddingModel,
            EmbeddingVector
        )
        VALUES (?, ?, ?)
        """,
        knowledge_id,
        model,
        vector
    )

    conn.commit()
    conn.close()