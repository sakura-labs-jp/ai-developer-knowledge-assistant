from backend.database.connection import get_connection


def get_kc_knowledge_by_id(
    knowledge_id: int,
) -> dict | None:
    """
    Get one Knowledge Chain knowledge unit
    including its source information.
    """

    query = """
        SELECT
            K.KnowledgeId,
            K.KnowledgeType,
            K.Content,
            K.SourceId,

            S.SourceType,
            S.SourceLocation,
            S.Title,
            S.SystemName

        FROM dbo.KC_Knowledge K

        INNER JOIN dbo.KC_KnowledgeSource S
            ON K.SourceId = S.SourceId

        WHERE K.KnowledgeId = ?
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute(
            query,
            knowledge_id,
        )

        row = cursor.fetchone()

        if not row:
            return None

        return {
            "knowledge_id": row.KnowledgeId,
            "knowledge_type": row.KnowledgeType,
            "content": row.Content,
            "source_id": row.SourceId,
            "source_type": row.SourceType,
            "source_location": row.SourceLocation,
            "source_title": row.Title,
            "system_name": row.SystemName,
        }

    finally:
        connection.close()