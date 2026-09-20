from backend.loaders.base import DocumentRecord


# Fields that must never be passed to LLM-facing processing.
SENSITIVE_FIELDS = {
    "③送信元IP",
    "⑥送信先IP",
}


def filter_sensitive_data(
    record: DocumentRecord,
) -> DocumentRecord:
    """
    Remove sensitive fields before a document record
    enters LLM-facing knowledge extraction.

    The original DocumentRecord is not modified.
    """

    filtered_data = {
        key: value
        for key, value in record.data.items()
        if key not in SENSITIVE_FIELDS
    }

    return DocumentRecord(
        source_type=record.source_type,
        source_location=record.source_location,
        source_title=record.source_title,
        record_index=record.record_index,
        data=filtered_data,
    )