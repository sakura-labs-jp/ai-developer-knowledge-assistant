from database.connection import get_connection


def search_knowledge(keyword: str):
    """
    Search knowledge records by keyword.

    The keyword is matched against multiple columns
    using SQL LIKE conditions.
    """

    conn = get_connection()
    cursor = conn.cursor()

    search = f"%{keyword}%"

    cursor.execute(
        """
        SELECT *
        FROM Knowledge
        WHERE
               Category       LIKE ?
            OR Technology     LIKE ?
            OR Title          LIKE ?
            OR Problem        LIKE ?
            OR Analysis       LIKE ?
            OR Solution       LIKE ?
            OR Result         LIKE ?
            OR LessonsLearned LIKE ?
            OR Keywords       LIKE ?
        """,
        search,
        search,
        search,
        search,
        search,
        search,
        search,
        search,
        search,
    )

    rows = cursor.fetchall()

    conn.close()

    return rows