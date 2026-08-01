from backend.database.connection import get_connection


def _convert_to_dict(cursor, rows):
    """
    Convert database rows to dictionary format.
    """

    columns = [column[0] for column in cursor.description]

    return [
        dict(zip(columns, row))
        for row in rows
    ]


def get_all_knowledge():
    """
    Retrieve all knowledge records.
    """

    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                KnowledgeId,
                Title,
                Content,
                Category,
                CreatedDate,
                UpdatedDate
            FROM Knowledge
            ORDER BY KnowledgeId
        """)

        rows = cursor.fetchall()

        return _convert_to_dict(cursor, rows)

    finally:
        if conn:
            conn.close()


def get_knowledge_by_id(knowledge_id: int):
    """
    Retrieve knowledge record by id.
    """

    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                KnowledgeId,
                Title,
                Content,
                Category,
                CreatedDate,
                UpdatedDate
            FROM Knowledge
            WHERE KnowledgeId = ?
        """, (knowledge_id,))

        row = cursor.fetchone()

        if row is None:
            return None

        return _convert_to_dict(cursor, [row])[0]

    finally:
        if conn:
            conn.close()