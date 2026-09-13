from backend.database.connection import get_connection


def get_relations_from_knowledge(
    knowledge_id: int,
) -> list[dict]:
    """
    Get outgoing relations and the positions
    associated with each destination knowledge unit.
    """

    query = """
        SELECT
            KR.RelationId,
            KR.FromKnowledgeId,
            KR.ToKnowledgeId,
            KR.RelationType,
            KR.Confidence,

            K.KnowledgeType,
            K.Content,
            K.SourceId,

            KS.SourceType,
            KS.SourceLocation,
            KS.Title,
            KS.SystemName,

            P.PositionId,
            P.PositionName

        FROM dbo.KC_KnowledgeRelation KR

        INNER JOIN dbo.KC_Knowledge K
            ON KR.ToKnowledgeId = K.KnowledgeId

        INNER JOIN dbo.KC_KnowledgeSource KS
            ON K.SourceId = KS.SourceId

        LEFT JOIN dbo.KC_KnowledgePosition KP
            ON K.KnowledgeId = KP.KnowledgeId

        LEFT JOIN dbo.KC_Position P
            ON KP.PositionId = P.PositionId

        WHERE KR.FromKnowledgeId = ?

        ORDER BY
            KR.RelationId,
            P.PositionId
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute(query, knowledge_id)

        rows = cursor.fetchall()

        relations_by_id = {}

        for row in rows:

            relation_id = row.RelationId

            if relation_id not in relations_by_id:

                relations_by_id[relation_id] = {
                    "relation_id": row.RelationId,
                    "from_knowledge_id": row.FromKnowledgeId,
                    "to_knowledge_id": row.ToKnowledgeId,
                    "relation_type": row.RelationType,
                    "confidence": (
                        float(row.Confidence)
                        if row.Confidence is not None
                        else None
                    ),
                    "knowledge": {
                        "knowledge_id": row.ToKnowledgeId,
                        "knowledge_type": row.KnowledgeType,
                        "content": row.Content,
                        "source_id": row.SourceId,
                        "source_type": row.SourceType,
                        "source_location": row.SourceLocation,
                        "source_title": row.Title,
                        "system_name": row.SystemName,
                    },
                    "positions": [],
                }

            if row.PositionId is not None:
                relations_by_id[relation_id]["positions"].append(
                    {
                        "position_id": row.PositionId,
                        "position_name": row.PositionName,
                    }
                )

        return list(relations_by_id.values())

    finally:
        connection.close()