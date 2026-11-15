---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-exporterNotice-20261114-000002
version: "1"
priority: Medium
created_date: "2026-11-14"
---

# Add a notice builder and a retention helper to the exporter

Source: ./source.md
Goal: `make test` exits 0 with the notice builder and the retention helper in place.

## Constraints

- New code lives under `src/exporter/` and its tests under `tests/`.
- The helper takes its age limit as a function argument.

## Phase 1: Notice builder

## Task 1: Create the notice builder

Create `src/exporter/notice.py` with a function `build_notice` that takes a report id and an expiry date and returns one text line. Create `tests/test_notice.py` for it.

Acceptance criteria:
- `build_notice` called with the report id `alpha` and the expiry date `2027-01-01` returns the text `Report alpha expires on 2027-01-01`.
- `tests/test_notice.py` holds the test `test_notice_text` and that test passes.

## Phase 2: Retention helper

## Task 2: Create the retention helper

Create `src/exporter/retention.py` with a function `is_expired` that takes the age of a report in days and the age limit in days and returns a boolean. Create `tests/test_retention.py` for it.

Acceptance criteria:
- `is_expired(31, 30)` returns `True` and `is_expired(30, 30)` returns `False`.
- `tests/test_retention.py` holds the test `test_expiry_edge` and that test passes.

## Task 3: Run the final check

Run the test suite for the new files.

Acceptance criteria:
- `make test` exits 0.
- The new test files are `tests/test_notice.py` and `tests/test_retention.py`.
