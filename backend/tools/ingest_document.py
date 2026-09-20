import argparse

from backend.services.document_ingestion import (
    ingest_nsg_excel,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Ingest a document into Knowledge Chain."
        )
    )

    parser.add_argument(
        "file_path",
        help="Path to the source document.",
    )

    parser.add_argument(
        "--system-name",
        required=True,
        help="System name associated with the document.",
    )

    parser.add_argument(
        "--sheet-name",
        default=None,
        help="Excel worksheet name.",
    )

    args = parser.parse_args()

    result = ingest_nsg_excel(
        file_path=args.file_path,
        system_name=args.system_name,
        sheet_name=args.sheet_name,
    )

    print()
    print("================================")
    print("Knowledge Chain - Ingestion")
    print("================================")
    print()

    print(
        f"Skipped               : "
        f"{result['skipped']}"
    )

    print(
        f"Source Hash           : "
        f"{result['source_hash']}"
    )

    print(
        f"Excel SourceId        : "
        f"{result['source_id']}"
    )

    print(
        f"Operational SourceId  : "
        f"{result['operational_source_id']}"
    )

    print(
        f"Records               : "
        f"{result['record_count']}"
    )

    print(
        f"Knowledge             : "
        f"{len(result['knowledge_ids'])}"
    )

    print(
        f"Knowledge IDs         : "
        f"{result['knowledge_ids']}"
    )

    print(
        f"Relations             : "
        f"{len(result['relation_ids'])}"
    )

    print(
        f"Relation IDs          : "
        f"{result['relation_ids']}"
    )

    print()

    if result["skipped"]:
        print(
            "Document already ingested. "
            "No new Knowledge was created."
        )
    else:
        print(
            "Document ingestion completed."
        )

    print()
    print("================================")


if __name__ == "__main__":
    main()