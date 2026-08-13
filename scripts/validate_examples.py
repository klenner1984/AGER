#!/usr/bin/env python3
import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]

PAIRS = [
    ("schemas/ager-record.schema.json", "examples/voice-agent.json"),
    ("schemas/change-event.schema.json", "examples/change-event.json"),
    ("schemas/incident.schema.json", "examples/incident.json"),
]


def load(path: str):
    with (ROOT / path).open("r", encoding="utf-8") as fh:
        return json.load(fh)


def main() -> int:
    failures = 0
    for schema_path, example_path in PAIRS:
        schema = load(schema_path)
        example = load(example_path)
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        errors = sorted(validator.iter_errors(example), key=lambda e: list(e.path))
        if errors:
            failures += 1
            print(f"FAIL {example_path} against {schema_path}")
            for error in errors:
                location = ".".join(str(p) for p in error.path) or "<root>"
                print(f"  - {location}: {error.message}")
        else:
            print(f"OK   {example_path}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
