from backend.database.connection import get_connection


def get_all_knowledge():
    """
    Retrieve all knowledge records.
    """

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT *
            FROM dbo.Knowledge
            ORDER BY KnowledgeId
            """
        )

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()


def get_knowledge_by_id(knowledge_id: int):
    """
    Retrieve a knowledge record by KnowledgeId.
    """

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT *
            FROM dbo.Knowledge
            WHERE KnowledgeId = ?
            """,
            (knowledge_id,)
        )

        return cursor.fetchone()

    finally:
        cursor.close()
        connection.close()