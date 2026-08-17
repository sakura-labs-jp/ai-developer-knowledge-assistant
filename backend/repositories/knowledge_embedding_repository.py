from backend.database.connection import get_connection
import json


def get_all_embeddings():
    """
    Retrieve all stored knowledge embeddings.
    """

    connection = get_connection()
    cursor = connection.cursor()

    try:
        sql = """
        SELECT
            KnowledgeId,
            EmbeddingModel,
            EmbeddingVector
        FROM dbo.KnowledgeEmbedding
        """

        cursor.execute(sql)
        rows = cursor.fetchall()

        result = []

        for row in rows:
            result.append(
                {
                    "KnowledgeId": row.KnowledgeId,
                    "Model": row.EmbeddingModel,
                    "Vector": json.loads(row.EmbeddingVector)
                }
            )

        return result

    finally:
        cursor.close()
        connection.close()


def upsert_embedding(
    knowledge_id: int,
    model: str,
    vector: str
):
    """
    Insert a new embedding or update an existing embedding
    for the same KnowledgeId and EmbeddingModel.
    """

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            UPDATE dbo.KnowledgeEmbedding
            SET
                EmbeddingVector = ?,
                CreatedAt = SYSDATETIME()
            WHERE
                KnowledgeId = ?
                AND EmbeddingModel = ?
            """,
            vector,
            knowledge_id,
            model
        )

        if cursor.rowcount == 0:
            cursor.execute(
                """
                INSERT INTO dbo.KnowledgeEmbedding
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

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()