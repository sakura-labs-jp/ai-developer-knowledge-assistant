from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from openpyxl import Workbook

from backend.tools.dry_run_document import (
    dry_run_nsg_excel,
)


def main() -> None:
    """
    Verify that the dry-run pipeline removes
    sensitive IP fields before console output.
    """

    test_file = Path(
        "test_nsg_dry_run.xlsx"
    )

    # These values must NEVER appear in
    # the dry-run output.
    source_ip = "10.0.1.10"
    destination_ip = "10.0.2.10"

    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "NSG"

    worksheet.append([
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
    ])

    worksheet.append([
        100,
        "Allow_Web_DB",
        "Web Server",
        source_ip,
        "*",
        "DB Server",
        destination_ip,
        1433,
        "TCP",
        "Inbound",
        "Web ServerからDB ServerへのSQL Server通信",
        "NG",
        "NSG Rule不足",
        "追加",
    ])

    workbook.save(
        test_file
    )

    try:
        # Capture dry-run console output.
        output_buffer = StringIO()

        with redirect_stdout(
            output_buffer
        ):
            dry_run_nsg_excel(
                file_path=str(test_file),
                sheet_name="NSG",
            )

        output = output_buffer.getvalue()

        # -----------------------------------------
        # Sensitive data must NOT appear.
        # -----------------------------------------

        assert source_ip not in output
        assert destination_ip not in output

        assert "③送信元IP" not in output
        assert "⑥送信先IP" not in output

        # -----------------------------------------
        # Safe route information SHOULD appear.
        # -----------------------------------------

        assert "Web Server" in output
        assert "DB Server" in output
        assert "1433" in output
        assert "TCP" in output
        assert "Inbound" in output
        assert "Allow_Web_DB" in output
        assert "NSG Rule不足" in output

        # -----------------------------------------
        # Dry-run safety declarations.
        # -----------------------------------------

        assert "NO DATABASE WRITE" in output
        assert "NO EMBEDDING" in output
        assert "NO GEMINI CALL" in output

        print(
            "Document dry-run safety test passed."
        )

        print()
        print("Sensitive data check")
        print(
            f"Source IP removed      : "
            f"{source_ip not in output}"
        )
        print(
            f"Destination IP removed : "
            f"{destination_ip not in output}"
        )
        print(
            "Sensitive field names  : removed"
        )

        print()
        print("Safe data check")
        print("Web Server             : present")
        print("DB Server              : present")
        print("Port 1433              : present")
        print("Protocol TCP           : present")
        print("Direction Inbound      : present")

        print()
        print("External processing")
        print("Database write         : none")
        print("Embedding              : none")
        print("Gemini call            : none")

        print()
        print("----- Captured Dry Run -----")
        print(output)

    finally:
        if test_file.exists():
            test_file.unlink()


if __name__ == "__main__":
    main()