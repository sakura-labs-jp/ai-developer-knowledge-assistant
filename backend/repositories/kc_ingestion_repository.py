from datetime import datetime

from backend.database.connection import get_connection


def insert_knowledge_source(
    source_type: str,
    source_location: str,
    title: str | None = None,
    system_name: str | None = None,
    source_created_at: datetime | None = None,
    source_hash: str | None = None,
) -> int:
    """
    Insert a document source and return its SourceId.
    """

    query = """
        INSERT INTO dbo.KC_KnowledgeSource
        (
            SourceType,
            SourceLocation,
            Title,
            SystemName,
            SourceCreatedAt,
            SourceHash
        )
        OUTPUT INSERTED.SourceId
        VALUES (?, ?, ?, ?, ?, ?)
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            query,
            source_type,
            source_location,
            title,
            system_name,
            source_created_at,
            source_hash,
        )

        row = cursor.fetchone()

        if row is None:
            raise RuntimeError(
                "Failed to create KC_KnowledgeSource."
            )

        source_id = int(row.SourceId)

        connection.commit()

        return source_id

    finally:
        connection.close()


def get_knowledge_source_by_hash(
    source_hash: str,
) -> dict | None:
    """
    Find an existing source by SHA-256 hash.
    """

    query = """
        SELECT
            SourceId,
            SourceType,
            SourceLocation,
            Title,
            SystemName,
            SourceHash
        FROM dbo.KC_KnowledgeSource
        WHERE SourceHash = ?
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            query,
            source_hash,
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return {
            "SourceId": int(row.SourceId),
            "SourceType": row.SourceType,
            "SourceLocation": row.SourceLocation,
            "Title": row.Title,
            "SystemName": row.SystemName,
            "SourceHash": row.SourceHash,
        }

    finally:
        connection.close()


def insert_knowledge(
    source_id: int,
    knowledge_type: str,
    content: str,
) -> int:
    """
    Insert one Knowledge Chain knowledge unit
    and return its KnowledgeId.
    """

    query = """
        INSERT INTO dbo.KC_Knowledge
        (
            SourceId,
            KnowledgeType,
            Content
        )
        OUTPUT INSERTED.KnowledgeId
        VALUES (?, ?, ?)
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            query,
            source_id,
            knowledge_type,
            content,
        )

        row = cursor.fetchone()

        if row is None:
            raise RuntimeError(
                "Failed to create KC_Knowledge."
            )

        knowledge_id = int(row.KnowledgeId)

        connection.commit()

        return knowledge_id

    finally:
        connection.close()


def get_position_id_by_name(
    position_name: str,
) -> int | None:
    """
    Get PositionId by position name.
    """

    query = """
        SELECT PositionId
        FROM dbo.KC_Position
        WHERE PositionName = ?
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            query,
            position_name,
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return int(row.PositionId)

    finally:
        connection.close()


def insert_knowledge_position(
    knowledge_id: int,
    position_id: int,
) -> None:
    """
    Associate a knowledge unit with a position.
    """

    query = """
        INSERT INTO dbo.KC_KnowledgePosition
        (
            KnowledgeId,
            PositionId
        )
        VALUES (?, ?)
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            query,
            knowledge_id,
            position_id,
        )

        connection.commit()

    finally:
        connection.close()


def insert_knowledge_relation(
    from_knowledge_id: int,
    to_knowledge_id: int,
    relation_type: str,
    confidence: float | None = None,
) -> int:
    """
    Create a relation between two knowledge units
    and return its RelationId.
    """

    query = """
        INSERT INTO dbo.KC_KnowledgeRelation
        (
            FromKnowledgeId,
            ToKnowledgeId,
            RelationType,
            Confidence
        )
        OUTPUT INSERTED.RelationId
        VALUES (?, ?, ?, ?)
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            query,
            from_knowledge_id,
            to_knowledge_id,
            relation_type,
            confidence,
        )

        row = cursor.fetchone()

        if row is None:
            raise RuntimeError(
                "Failed to create KC_KnowledgeRelation."
            )

        relation_id = int(row.RelationId)

        connection.commit()

        return relation_id

    finally:
        connection.close()