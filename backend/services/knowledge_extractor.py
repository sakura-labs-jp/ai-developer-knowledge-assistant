from dataclasses import dataclass

from backend.loaders.base import DocumentRecord


@dataclass
class ExtractedKnowledge:
    knowledge_type: str
    content: str


def extract_nsg_knowledge(
    record: DocumentRecord,
) -> list[ExtractedKnowledge]:
    """
    Convert a sanitized NSG document record into
    Knowledge Chain knowledge units.

    This function must receive an already sanitized
    DocumentRecord.
    """

    data = record.data

    source = data.get("②送信元")
    source_port = data.get("④送信元ポート")
    destination = data.get("⑤送信先")
    destination_port = data.get("⑦送信先ポート")
    protocol = data.get("⑧プロトコル")
    direction = data.get("方向")
    description = data.get("⑨説明")
    result = data.get("判定結果")
    result_detail = data.get("判定結果詳細")
    priority = data.get("優先度")
    rule_name = data.get("①NSG Rule name")
    change_type = data.get("追加・変更・削除")

    lines = [
        "Network route analysis.",
        f"Source: {source}.",
        f"Source port: {source_port}.",
        f"Destination: {destination}.",
        f"Destination port: {destination_port}.",
        f"Protocol: {protocol}.",
        f"Direction: {direction}.",
    ]

    if description:
        lines.append(
            f"Description: {description}."
        )

    if result:
        lines.append(
            f"Result: {result}."
        )

    if result_detail:
        lines.append(
            f"Result detail: {result_detail}."
        )

    if priority is not None:
        lines.append(
            f"Priority: {priority}."
        )

    if rule_name:
        lines.append(
            f"NSG rule: {rule_name}."
        )

    if change_type:
        lines.append(
            f"Change type: {change_type}."
        )

    content = "\n".join(lines)

    return [
        ExtractedKnowledge(
            knowledge_type="Analysis",
            content=content,
        )
    ]