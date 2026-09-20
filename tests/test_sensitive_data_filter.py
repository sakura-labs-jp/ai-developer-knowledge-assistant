from backend.loaders.base import DocumentRecord
from backend.services.sensitive_data_filter import (
    filter_sensitive_data,
)


def main():
    record = DocumentRecord(
        source_type="Excel",
        source_location="test_nsg_routes.xlsx",
        source_title="test_nsg_routes.xlsx",
        record_index=2,
        data={
            "②送信元": "Web Server",
            "③送信元IP": "10.0.1.10",
            "⑤送信先": "DB Server",
            "⑥送信先IP": "10.0.2.10",
            "⑦送信先ポート": 1433,
            "⑧プロトコル": "TCP",
            "判定結果": "NG",
        },
    )

    safe_record = filter_sensitive_data(record)

    assert "③送信元IP" not in safe_record.data
    assert "⑥送信先IP" not in safe_record.data

    assert safe_record.data["②送信元"] == "Web Server"
    assert safe_record.data["⑤送信先"] == "DB Server"
    assert safe_record.data["⑦送信先ポート"] == 1433

    # Original raw record must remain unchanged.
    assert record.data["③送信元IP"] == "10.0.1.10"
    assert record.data["⑥送信先IP"] == "10.0.2.10"

    print("Sensitive data filter test passed.")
    print("\nSafe data:")

    for key, value in safe_record.data.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()