from backend.database.connection import get_connection


def get_user_positions(user_id: int) -> list[dict]:
    """
    Get all positions assigned to a user.
    """

    query = """
        SELECT
            P.PositionId,
            P.PositionName
        FROM dbo.KC_UserPosition UP

        INNER JOIN dbo.KC_Position P
            ON UP.PositionId = P.PositionId

        WHERE UP.UserId = ?

        ORDER BY P.PositionId
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute(query, user_id)

        rows = cursor.fetchall()

        return [
            {
                "position_id": row.PositionId,
                "position_name": row.PositionName,
            }
            for row in rows
        ]

    finally:
        connection.close()