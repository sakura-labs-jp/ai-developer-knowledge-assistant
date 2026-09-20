from dataclasses import dataclass
from typing import Any


@dataclass
class DocumentRecord:
    """
    A normalized record loaded from a source document.

    Loaders are responsible only for extracting data.
    They must not generate Knowledge or call an LLM.
    """

    source_type: str
    source_location: str
    source_title: str
    record_index: int
    data: dict[str, Any]