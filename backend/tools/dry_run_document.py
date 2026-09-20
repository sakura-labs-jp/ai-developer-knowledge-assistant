import argparse

from backend.loaders.excel_loader import load_excel
from backend.services.sensitive_data_filter import (
    filter_sensitive_data,
)
from backend.services.knowledge_extractor import (
    extract_nsg_knowledge,
)


def dry_run_nsg_excel(
    file_path: str,
    sheet_name: str | None = None,
) -> None:
    """
    Preview Knowledge generated from an NSG Excel file.

    IMPORTANT:
    - Does NOT write to SQL Server.
    - Does NOT create embeddings.
    - Does NOT call Gemini.
    - Sensitive fields are removed before preview.
    """

    records = load_excel(
        file_path=file_path,
        sheet_name=sheet_name,
    )

    print()
    print("================================")
    print("Knowledge Chain - Dry Run")
    print("================================")
    print()
    print(f"File    : {file_path}")
    print(f"Records : {len(records)}")
    print()
    print("NO DATABASE WRITE")
    print("NO EMBEDDING")
    print("NO GEMINI CALL")
    print()

    if not records:
        print("No records found.")
        return

    for record in records:

        safe_record = filter_sensitive_data(
            record
        )

        knowledge_list = extract_nsg_knowledge(
            safe_record
        )

        print("--------------------------------")
        print(
            f"Excel Row: {record.record_index}"
        )
        print("--------------------------------")

        print()
        print("[SAFE FIELDS]")

        for key, value in safe_record.data.items():
            print(
                f"{key}: {value}"
            )

        print()
        print("[GENERATED KNOWLEDGE]")

        for knowledge in knowledge_list:
            print()
            print(
                f"Knowledge Type: "
                f"{knowledge.knowledge_type}"
            )
            print(
                knowledge.content
            )

        print()

    print("================================")
    print("Dry run completed.")
    print("Nothing was written to the database.")
    print("Nothing was sent to Gemini.")
    print("================================")


def main() -> None:

    parser = argparse.ArgumentParser(
        description=(
            "Preview document ingestion without "
            "database writes or external AI calls."
        )
    )

    parser.add_argument(
        "file_path",
        help="Path to the Excel document.",
    )

    parser.add_argument(
        "--sheet-name",
        default=None,
        help="Excel worksheet name.",
    )

    args = parser.parse_args()

    dry_run_nsg_excel(
        file_path=args.file_path,
        sheet_name=args.sheet_name,
    )


if __name__ == "__main__":
    main()