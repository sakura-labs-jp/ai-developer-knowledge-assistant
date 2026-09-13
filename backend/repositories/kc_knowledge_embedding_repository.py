import json

from backend.database.connection import get_connection


def get_all_kc_knowledge() -> list[dict]:
    """
    Get all Knowledge Chain knowledge units
    for embedding generation.
    """

    query = """
        SELECT
            KnowledgeId,
            KnowledgeType,
            Content
        FROM dbo.KC_Knowledge
        ORDER BY KnowledgeId
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute(query)

        rows = cursor.fetchall()

        return [
            {
                "KnowledgeId": row.KnowledgeId,
                "KnowledgeType": row.KnowledgeType,
                "Content": row.Content,
            }
            for row in rows
        ]

    finally:
        connection.close()


def insert_kc_embedding(
    knowledge_id: int,
    model: str,
    vector: list[float],
) -> None:
    """
    Insert or update an embedding for a KC knowledge unit.
    """

    vector_json = json.dumps(vector)

    query = """
        MERGE dbo.KC_KnowledgeEmbedding AS target

        USING (
            SELECT
                ? AS KnowledgeId,
                ? AS EmbeddingModel,
                ? AS EmbeddingVector
        ) AS source

        ON
            target.KnowledgeId = source.KnowledgeId
            AND target.EmbeddingModel = source.EmbeddingModel

        WHEN MATCHED THEN
            UPDATE SET
                EmbeddingVector = source.EmbeddingVector,
                CreatedAt = SYSDATETIME()

        WHEN NOT MATCHED THEN
            INSERT
            (
                KnowledgeId,
                EmbeddingModel,
                EmbeddingVector
            )
            VALUES
            (
                source.KnowledgeId,
                source.EmbeddingModel,
                source.EmbeddingVector
            );
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            query,
            knowledge_id,
            model,
            vector_json,
        )

        connection.commit()

    finally:
        connection.close()


def get_all_kc_embeddings() -> list[dict]:
    """
    Retrieve all stored KC embeddings.
    """

    query = """
        SELECT
            KnowledgeId,
            EmbeddingModel,
            EmbeddingVector
        FROM dbo.KC_KnowledgeEmbedding
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute(query)

        rows = cursor.fetchall()

        embeddings = []

        for row in rows:
            embeddings.append(
                {
                    "KnowledgeId": row.KnowledgeId,
                    "Model": row.EmbeddingModel,
                    "Vector": json.loads(
                        row.EmbeddingVector
                    ),
                }
            )

        return embeddings

    finally:
        connection.close()