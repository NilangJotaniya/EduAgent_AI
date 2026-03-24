from __future__ import annotations

import csv
import re
from collections import Counter
from io import BytesIO, StringIO
from typing import Any

import pandas as pd
from pypdf import PdfReader


ENROLLMENT_RE = re.compile(r"\b\d{8,16}\b")


def _normalize_header(value: Any) -> str:
    text = str(value or "").strip().lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_")


def _clean_text(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def _read_csv_records(content: bytes) -> list[dict[str, Any]]:
    last_error: Exception | None = None
    for encoding in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            text = content.decode(encoding)
            reader = csv.DictReader(StringIO(text))
            return [{_normalize_header(k): v for k, v in row.items()} for row in reader]
        except Exception as exc:
            last_error = exc
    raise ValueError(f"Could not read CSV file: {last_error}")


def _read_excel_records(content: bytes) -> list[dict[str, Any]]:
    df = pd.read_excel(BytesIO(content))
    df.columns = [_normalize_header(col) for col in df.columns]
    return df.fillna("").to_dict(orient="records")


def _extract_name_from_pdf_line(line: str) -> str:
    prepared = re.sub(r"([a-z])For\b", r"\1 For", line)
    prepared = re.sub(r"([a-z])Inter\b", r"\1 Inter", prepared)
    prepared = re.sub(r"([a-z])NPTEL\b", r"\1 NPTEL", prepared)
    prepared = re.sub(r"([a-z])Hackathon\b", r"\1 Hackathon", prepared)

    match = ENROLLMENT_RE.search(prepared)
    if not match:
        return ""

    prefix = prepared[: match.start()].strip()
    prefix = re.sub(r"^\d+\s+", "", prefix).strip()
    tokens = prefix.split()
    stop_words = {
        "for",
        "inter",
        "nptel",
        "hackathon",
        "cultural",
        "sport",
        "ncc",
        "organized",
        "volunteer",
        "participated",
        "faculty",
    }

    name_tokens: list[str] = []
    for token in tokens:
        clean = token.strip(",.:;")
        if not clean:
            continue
        if clean.lower() in stop_words:
            break
        if clean.isdigit():
            break
        name_tokens.append(clean)

    return " ".join(name_tokens).strip()


def _read_pdf_records(content: bytes) -> list[dict[str, Any]]:
    reader = PdfReader(BytesIO(content))
    records: list[dict[str, Any]] = []

    for page in reader.pages:
        text = page.extract_text() or ""
        for raw_line in text.splitlines():
            line = _clean_text(raw_line)
            if not line or line.lower().startswith("sr."):
                continue

            enrollment_match = ENROLLMENT_RE.search(line)
            if not enrollment_match:
                continue

            trailing = line[enrollment_match.start() :]
            meta_match = re.match(r"(?P<enrollment>\d{8,16})\s+(?P<semester>\d+)\s+(?P<program>[A-Z]{2,6})\b", trailing)
            if not meta_match:
                continue

            enrollment_no = meta_match.group("enrollment")
            if enrollment_no.upper() == "FACULTY":
                continue

            full_name = _extract_name_from_pdf_line(line)
            if not full_name:
                continue

            records.append(
                {
                    "student_id": enrollment_no,
                    "enrollment_no": enrollment_no,
                    "full_name": full_name,
                    "program": meta_match.group("program"),
                    "semester": int(meta_match.group("semester")),
                    "password": "",
                }
            )

    return records


def _first_non_empty(row: dict[str, Any], keys: list[str]) -> str:
    for key in keys:
        value = _clean_text(row.get(key, ""))
        if value:
            return value
    return ""


def _normalize_program(value: str) -> str:
    return _clean_text(value).upper()


def normalize_student_records(records: list[dict[str, Any]], default_password: str) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    seen: set[str] = set()
    students: list[dict[str, Any]] = []
    skipped = 0
    programs: Counter[str] = Counter()

    for row in records:
        enrollment_no = _first_non_empty(
            row,
            [
                "enrollment_no",
                "enrollment_number",
                "enrollment",
                "en_no",
                "enrolment_no",
                "username",
                "student_id",
                "studentid",
            ],
        )
        full_name = _first_non_empty(row, ["full_name", "student_name", "name", "student"])
        program = _normalize_program(_first_non_empty(row, ["program", "department", "dept", "branch", "stream"]))
        password = _first_non_empty(row, ["password", "pass", "temp_password", "temporary_password"]) or default_password

        semester_raw = _first_non_empty(row, ["semester", "sem"])
        try:
            semester = int(semester_raw) if semester_raw else 0
        except ValueError:
            semester = 0

        if not enrollment_no or not full_name:
            skipped += 1
            continue

        if not ENROLLMENT_RE.fullmatch(enrollment_no):
            skipped += 1
            continue

        if enrollment_no in seen:
            continue

        seen.add(enrollment_no)
        if program:
            programs[program] += 1

        students.append(
            {
                "student_id": enrollment_no,
                "enrollment_no": enrollment_no,
                "full_name": full_name,
                "program": program,
                "semester": semester,
                "password": password,
            }
        )

    summary = {
        "total_rows": len(records),
        "imported_count": len(students),
        "skipped_count": skipped,
        "programs": dict(programs),
    }
    return students, summary


def parse_student_file(filename: str, content: bytes, default_password: str) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    lower = filename.lower()
    if lower.endswith(".csv"):
        raw_records = _read_csv_records(content)
    elif lower.endswith(".xlsx") or lower.endswith(".xls"):
        raw_records = _read_excel_records(content)
    elif lower.endswith(".pdf"):
        raw_records = _read_pdf_records(content)
    else:
        raise ValueError("Unsupported file type. Use PDF, CSV, or Excel.")

    students, summary = normalize_student_records(raw_records, default_password)
    summary["source_file"] = filename
    return students, summary
