from pathlib import Path

from openpyxl import Workbook

from backend.database.connection import get_connection
from backend.services.document_ingestion import (
    ingest_nsg_excel,
)


def cleanup_test_data(
    knowledge_ids: list[int],
    source_ids: list[int],
) -> None:
    """
    Remove test data created by this test.
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()

        for knowledge_id in knowledge_ids:

            cursor.execute(
                """
                DELETE FROM dbo.KC_KnowledgeEmbedding
                WHERE KnowledgeId = ?
                """,
                knowledge_id,
            )

            cursor.execute(
                """
                DELETE FROM dbo.KC_KnowledgePosition
                WHERE KnowledgeId = ?
                """,
                knowledge_id,
            )

            cursor.execute(
                """
                DELETE FROM dbo.KC_KnowledgeRelation
                WHERE FromKnowledgeId = ?
                   OR ToKnowledgeId = ?
                """,
                knowledge_id,
                knowledge_id,
            )

        for knowledge_id in knowledge_ids:

            cursor.execute(
                """
                DELETE FROM dbo.KC_Knowledge
                WHERE KnowledgeId = ?
                """,
                knowledge_id,
            )

        for source_id in source_ids:

            cursor.execute(
                """
                DELETE FROM dbo.KC_KnowledgeSource
                WHERE SourceId = ?
                """,
                source_id,
            )

        connection.commit()

    finally:
        connection.close()


def main():

    test_file = Path(
        "test_nsg_ingestion.xlsx"
    )

    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "NSG"

    worksheet.append([
        "優先度",
        "①NSG Rule name",
        "②送信元",
        "③送信元IP",
        "④送信元ポート",
        "⑤送信先",
        "⑥送信先IP",
        "⑦送信先ポート",
        "⑧プロトコル",
        "方向",
        "⑨説明",
        "判定結果",
        "判定結果詳細",
        "追加・変更・削除",
    ])

    worksheet.append([
        100,
        "Allow_Web_DB",
        "Web Server",
        "10.0.1.10",
        "*",
        "DB Server",
        "10.0.2.10",
        1433,
        "TCP",
        "Inbound",
        "Web ServerからDB ServerへのSQL Server通信",
        "NG",
        "NSG Rule不足",
        "追加",
    ])

    workbook.save(
        test_file
    )

    first_result = None

    try:

        # =========================================
        # 1st ingestion
        # =========================================

        first_result = ingest_nsg_excel(
            file_path=str(test_file),
            system_name="TEST",
            sheet_name="NSG",
        )

        assert first_result["skipped"] is False
        assert first_result["source_id"] is not None

        assert (
            first_result["operational_source_id"]
            is not None
        )

        assert first_result["record_count"] == 1

        assert len(
            first_result["knowledge_ids"]
        ) == 2

        assert len(
            first_result["relation_ids"]
        ) == 1

        assert first_result["source_hash"]

        # =========================================
        # Verify source separation
        # =========================================

        analysis_id = (
            first_result["knowledge_ids"][0]
        )

        resolution_id = (
            first_result["knowledge_ids"][1]
        )

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    K.KnowledgeType,
                    S.SourceType,
                    S.SourceHash
                FROM dbo.KC_Knowledge K
                INNER JOIN dbo.KC_KnowledgeSource S
                    ON K.SourceId = S.SourceId
                WHERE K.KnowledgeId IN (?, ?)
                """,
                analysis_id,
                resolution_id,
            )

            rows = cursor.fetchall()

        finally:
            connection.close()

        source_by_type = {
            row.KnowledgeType: row
            for row in rows
        }

        assert (
            source_by_type[
                "Analysis"
            ].SourceType
            == "Excel"
        )

        assert (
            source_by_type[
                "Analysis"
            ].SourceHash
            == first_result["source_hash"]
        )

        assert (
            source_by_type[
                "Resolution"
            ].SourceType
            == "OperationalRule"
        )

        assert (
            source_by_type[
                "Resolution"
            ].SourceHash
            is None
        )

        # =========================================
        # 2nd ingestion
        #
        # Same physical file / same SHA-256.
        # It must NOT create new Knowledge.
        # =========================================

        second_result = ingest_nsg_excel(
            file_path=str(test_file),
            system_name="TEST",
            sheet_name="NSG",
        )

        assert second_result["skipped"] is True

        assert (
            second_result["source_id"]
            == first_result["source_id"]
        )

        assert (
            second_result["source_hash"]
            == first_result["source_hash"]
        )

        assert second_result["record_count"] == 0
        assert second_result["knowledge_ids"] == []
        assert second_result["relation_ids"] == []

        # =========================================
        # Result
        # =========================================

        print(
            "Document ingestion idempotency "
            "test passed."
        )

        print()

        print("1st ingestion")
        print(
            f"Skipped               : "
            f"{first_result['skipped']}"
        )
        print(
            f"Excel SourceId        : "
            f"{first_result['source_id']}"
        )
        print(
            f"Operational SourceId  : "
            f"{first_result['operational_source_id']}"
        )
        print(
            f"Knowledge IDs         : "
            f"{first_result['knowledge_ids']}"
        )
        print(
            f"Relation IDs          : "
            f"{first_result['relation_ids']}"
        )

        print()

        print("2nd ingestion")
        print(
            f"Skipped               : "
            f"{second_result['skipped']}"
        )
        print(
            f"Existing SourceId     : "
            f"{second_result['source_id']}"
        )
        print(
            f"Knowledge IDs         : "
            f"{second_result['knowledge_ids']}"
        )
        print(
            f"Relation IDs          : "
            f"{second_result['relation_ids']}"
        )

        print()

        print(
            "Same SourceId         : "
            f"{second_result['source_id'] == first_result['source_id']}"
        )

        print(
            "Same SHA-256          : "
            f"{second_result['source_hash'] == first_result['source_hash']}"
        )

    finally:

        if test_file.exists():
            test_file.unlink()

        if first_result is not None:

            source_ids = [
                first_result["source_id"],
                first_result[
                    "operational_source_id"
                ],
            ]

            source_ids = [
                source_id
                for source_id in source_ids
                if source_id is not None
            ]

            cleanup_test_data(
                knowledge_ids=first_result[
                    "knowledge_ids"
                ],
                source_ids=source_ids,
            )


if __name__ == "__main__":
    main()