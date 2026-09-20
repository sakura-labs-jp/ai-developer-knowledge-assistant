import hashlib
from pathlib import Path

from backend.loaders.excel_loader import load_excel
from backend.services.sensitive_data_filter import (
    filter_sensitive_data,
)
from backend.services.knowledge_extractor import (
    extract_nsg_knowledge,
)
from backend.repositories.kc_ingestion_repository import (
    insert_knowledge_source,
    get_knowledge_source_by_hash,
    insert_knowledge,
    get_position_id_by_name,
    insert_knowledge_position,
    insert_knowledge_relation,
)


NSG_POSITION_NAME = "Cloud Architect"


def calculate_file_hash(
    file_path: str,
) -> str:
    """
    Calculate SHA-256 for a source file.
    """

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        for chunk in iter(
            lambda: file.read(8192),
            b"",
        ):
            sha256.update(chunk)

    return sha256.hexdigest()


def ingest_nsg_excel(
    file_path: str,
    system_name: str,
    sheet_name: str | None = None,
) -> dict:
    """
    Ingest an NSG Excel document into Knowledge Chain.

    The source file SHA-256 is used to prevent
    duplicate ingestion of identical documents.
    """

    # ---------------------------------------------
    # 1. Calculate source hash
    # ---------------------------------------------

    source_hash = calculate_file_hash(
        file_path
    )

    # ---------------------------------------------
    # 2. Duplicate check
    # ---------------------------------------------

    existing_source = (
        get_knowledge_source_by_hash(
            source_hash
        )
    )

    if existing_source is not None:
        return {
            "source_id": existing_source[
                "SourceId"
            ],
            "operational_source_id": None,
            "record_count": 0,
            "knowledge_ids": [],
            "relation_ids": [],
            "source_hash": source_hash,
            "skipped": True,
        }

    # ---------------------------------------------
    # 3. Load Excel
    # ---------------------------------------------

    records = load_excel(
        file_path=file_path,
        sheet_name=sheet_name,
    )

    if not records:
        return {
            "source_id": None,
            "operational_source_id": None,
            "record_count": 0,
            "knowledge_ids": [],
            "relation_ids": [],
            "source_hash": source_hash,
            "skipped": False,
        }

    # ---------------------------------------------
    # 4. Resolve Position
    # ---------------------------------------------

    position_id = get_position_id_by_name(
        NSG_POSITION_NAME
    )

    if position_id is None:
        raise RuntimeError(
            f"Position not found: {NSG_POSITION_NAME}"
        )

    # ---------------------------------------------
    # 5. Create Excel Source
    # ---------------------------------------------

    first_record = records[0]

    source_id = insert_knowledge_source(
        source_type=first_record.source_type,
        source_location=first_record.source_location,
        title=first_record.source_title,
        system_name=system_name,
        source_hash=source_hash,
    )

    # ---------------------------------------------
    # 6. Create Operational Rule Source
    # ---------------------------------------------

    operational_source_id = insert_knowledge_source(
        source_type="OperationalRule",
        source_location=(
            "Knowledge Chain Operational Rules"
        ),
        title="Network Route Troubleshooting",
        system_name=system_name,
        source_hash=None,
    )

    knowledge_ids = []
    relation_ids = []

    # ---------------------------------------------
    # 7. Process each Excel record
    # ---------------------------------------------

    for record in records:

        # Sensitive data must be removed before
        # Knowledge / embedding / LLM processing.
        safe_record = filter_sensitive_data(
            record
        )

        extracted_list = extract_nsg_knowledge(
            safe_record
        )

        for extracted in extracted_list:

            # -------------------------------------
            # Analysis
            # Source = Excel
            # -------------------------------------

            analysis_id = insert_knowledge(
                source_id=source_id,
                knowledge_type=(
                    extracted.knowledge_type
                ),
                content=extracted.content,
            )

            insert_knowledge_position(
                knowledge_id=analysis_id,
                position_id=position_id,
            )

            knowledge_ids.append(
                analysis_id
            )

            # -------------------------------------
            # Resolution
            # Source = OperationalRule
            # -------------------------------------

            resolution_content = (
                "For this network route, verify the "
                "NSG rule, direction, destination port, "
                "and protocol. "
                "If the network configuration requires "
                "investigation or modification, contact "
                "the DX基盤チーム."
            )

            resolution_id = insert_knowledge(
                source_id=operational_source_id,
                knowledge_type="Resolution",
                content=resolution_content,
            )

            insert_knowledge_position(
                knowledge_id=resolution_id,
                position_id=position_id,
            )

            knowledge_ids.append(
                resolution_id
            )

            # -------------------------------------
            # Analysis -> Resolution
            # -------------------------------------

            relation_id = insert_knowledge_relation(
                from_knowledge_id=analysis_id,
                to_knowledge_id=resolution_id,
                relation_type="RESOLVED_BY",
                confidence=1.0,
            )

            relation_ids.append(
                relation_id
            )

    # ---------------------------------------------
    # 8. Return result
    # ---------------------------------------------

    return {
        "source_id": source_id,
        "operational_source_id": (
            operational_source_id
        ),
        "record_count": len(records),
        "knowledge_ids": knowledge_ids,
        "relation_ids": relation_ids,
        "source_hash": source_hash,
        "skipped": False,
    }