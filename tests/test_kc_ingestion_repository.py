from backend.repositories.kc_ingestion_repository import (
    insert_knowledge_source,
    insert_knowledge,
)


def main():
    source_id = insert_knowledge_source(
        source_type="Excel",
        source_location="test_nsg_routes.xlsx",
        title="NSG Route Test",
        system_name="TEST",
    )

    print(
        f"Created SourceId: {source_id}"
    )

    knowledge_id = insert_knowledge(
        source_id=source_id,
        knowledge_type="Analysis",
        content=(
            "TEST: Web ServerからDB Serverへの"
            "TCP/1433通信ルート。"
        ),
    )

    print(
        f"Created KnowledgeId: {knowledge_id}"
    )

    print(
        "KC ingestion repository test passed."
    )


if __name__ == "__main__":
    main()