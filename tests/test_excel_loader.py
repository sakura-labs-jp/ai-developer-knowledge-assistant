from pathlib import Path

from openpyxl import Workbook

from backend.loaders.excel_loader import load_excel


def main():
    test_file = Path("test_nsg_routes.xlsx")

    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "NSG"

    headers = [
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
    ]

    worksheet.append(headers)

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

    workbook.save(test_file)

    try:
        records = load_excel(
            str(test_file),
            sheet_name="NSG",
        )

        print(f"Records: {len(records)}")

        for record in records:
            print("\n--- DocumentRecord ---")
            print(f"Source Type : {record.source_type}")
            print(f"Source      : {record.source_title}")
            print(f"Row         : {record.record_index}")

            for key, value in record.data.items():
                print(f"{key}: {value}")

    finally:
        if test_file.exists():
            test_file.unlink()


if __name__ == "__main__":
    main()