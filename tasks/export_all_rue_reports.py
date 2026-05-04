import json
import os
from pathlib import Path

import dotenv

import pysmartdok

import logging

OUTPUT_DIR = Path("tmp")
OUTPUT_FILE = OUTPUT_DIR / "rue_reports.json"


def main():
    dotenv.load_dotenv()
    client = pysmartdok.ApiClient(api_token=os.getenv("SMARTDOK_API_KEY"))

    logging.getLogger().setLevel(logging.DEBUG)

    reports = client.rue.get_rue_reports()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(
            [r.model_dump(mode="json", by_alias=True) for r in reports],
            f,
            indent=4,
        )

    print(f"Exported {len(reports)} reports to {OUTPUT_FILE}")

    print(f"Exported {len(reports)} reports to {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
