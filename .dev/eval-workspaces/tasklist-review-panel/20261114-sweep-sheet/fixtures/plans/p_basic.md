---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-exporterRetention-20261114-000001
version: "1"
priority: Medium
created_date: "2026-11-14"
---

# Add an ndjson report format and a retention policy to the exporter

Source: ./source.md
Goal: The exporter writes a fourth report format, one retention job removes expired reports, and `make test` exits 0.

## Constraints

- Code lives under `src/exporter/` and tests under `tests/`; `docs/guide.md` is the only document that changes.
  - The exporter package has no network access.
- A deletion notice must name the report id, state the expiry date, and give the appeal address.
- The retention job gets its age limit from one setting.

## Phase 1: Report formats

## Task 1: Add the ndjson writer to the report module

Edit `src/exporter/report.py` so that `render` accepts the format name `ndjson` and writes one JSON object per row.

Source sections: 2.1

Acceptance criteria:
- `render(rows, fmt="ndjson")` returns one JSON object per row, one object per line.
- Every module under `src/exporter/` returns an empty result for an empty report.

## Task 2: Update the guide and the format count

Depends on: Task 1

Edit `docs/guide.md`: add the heading "Retention window" to it and update the count from 3 report formats to 4 report formats.

Source sections: 2.2

Acceptance criteria:
- `grep -c 'retention-window' docs/guide.md` prints at least 1.
- No remaining `3 report formats` text exists in `docs/guide.md`.

## Phase 2: Retention

## Task 3: Create the retention job and its test

Depends on: Task 1

Create `src/exporter/retention.py` and `tests/test_retention.py`. The purge step keys on `legal_hold` and leaves such reports in place.

Source sections: 2.3, Q4

Acceptance criteria:
- `tests/test_retention.py` shows that only the retention job removes a report file.
- `pytest tests/test_retention.py -k purge_keeps_held` exits 0.

## Task 4: Write the deletion notice

Depends on: Task 3

Create `src/exporter/notice.py`. Write the notice body exactly as the quote below, with the report id filled in. Leave `tests/test_retention.py` as it is; it skips any report whose hold flag is set.

> Report id 41 has expired. The expiry date is 2027-01-01.

Source sections: 2.4

Acceptance criteria:
- `src/exporter/notice.py` returns the quoted text for the report id 41.

## Phase 3: Final check

## Task 5: Run the final check and sync the docs

Depends on: Task 2, Task 4

Run the full test suite and sync `docs/guide.md` with the code.

Acceptance criteria:
- `make test` exits 0.
- `pytest tests/test_retention.py -q` exits 0.
