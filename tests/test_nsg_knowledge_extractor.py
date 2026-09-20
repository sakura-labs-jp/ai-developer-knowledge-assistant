from backend.loaders.base import DocumentRecord
from backend.services.sensitive_data_filter import (
    filter_sensitive_data,
)
from backend.services.knowledge_extractor import (
    extract_nsg_knowledge,
)


def main():
    raw_record = DocumentRecord(
        source_type="Excel",
        source_location="test_nsg_routes.xlsx",
        source_title="test_nsg_routes.xlsx",
        record_index=2,
        data={
            "優先度": 100,
            "①NSG Rule name": "Allow_Web_DB",
            "②送信元": "Web Server",
            "③送信元IP": "10.0.1.10",
            "④送信元ポート": "*",
            "⑤送信先": "DB Server",
            "⑥送信先IP": "10.0.2.10",
            "⑦送信先ポート": 1433,
            "⑧プロトコル": "TCP",
            "方向": "Inbound",
            "⑨説明": "Web ServerからDB ServerへのSQL Server通信",
            "判定結果": "NG",
            "判定結果詳細": "NSG Rule不足",
            "追加・変更・削除": "追加",
        },
    )

    safe_record = filter_sensitive_data(
        raw_record
    )

    knowledge_list = extract_nsg_knowledge(
        safe_record
    )

    assert len(knowledge_list) == 1

    knowledge = knowledge_list[0]

    assert knowledge.knowledge_type == "Analysis"

    # Sensitive values must never reach generated Knowledge.
    assert "10.0.1.10" not in knowledge.content
    assert "10.0.2.10" not in knowledge.content

    print("Knowledge extraction test passed.")

    print("\n--- Generated Knowledge ---")
    print(f"Type: {knowledge.knowledge_type}")
    print(knowledge.content)


if __name__ == "__main__":
    main()