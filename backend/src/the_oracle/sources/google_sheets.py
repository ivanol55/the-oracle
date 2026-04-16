import os


def load_entries() -> list[dict]:
    sheet_id = os.environ["GOOGLE_SHEET_ID"]
    raise NotImplementedError(
        f"Google Sheets source not yet implemented (sheet: {sheet_id})"
    )
