from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="Convert simple CSV/JSON rows into MIMIC-style JSONL for training.")
    parser.add_argument("--input", required=True, help="Input file path (.json or .jsonl)")
    parser.add_argument("--output", required=True, help="Output JSONL file path")
    return parser.parse_args()


def read_rows(path: Path):
    if path.suffix.lower() == ".jsonl":
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                yield json.loads(line)
        return

    if path.suffix.lower() == ".json":
        rows = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(rows, list):
            raise ValueError("JSON input must be a list of records")
        for row in rows:
            yield row
        return

    raise ValueError("Unsupported input format. Use .json or .jsonl")


def normalize_record(record: dict) -> dict:
    return {
        "note": str(record.get("note") or record.get("clinical_note") or "").strip(),
        "symptoms": str(record.get("symptoms") or "").strip(),
        "label": str(record.get("label") or record.get("condition") or "").strip(),
        "severity": str(record.get("severity") or "Low").strip(),
        "language": str(record.get("language") or "en").strip(),
    }


def main():
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    count = 0
    with output_path.open("w", encoding="utf-8") as out:
        for row in read_rows(input_path):
            normalized = normalize_record(row)
            if not normalized["note"] and not normalized["symptoms"]:
                continue
            if not normalized["label"]:
                continue
            out.write(json.dumps(normalized, ensure_ascii=False) + "\n")
            count += 1

    print(f"Wrote {count} records to {output_path}")


if __name__ == "__main__":
    main()
