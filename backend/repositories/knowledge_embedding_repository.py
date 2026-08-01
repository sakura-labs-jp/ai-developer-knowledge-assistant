from backend.database.connection import get_connection
import json


def get_all_embeddings():

    connection = get_connection()

    cursor = connection.cursor()

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

    cursor.close()
    connection.close()

    return result