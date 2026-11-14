# Proposal B: keep the facts inside the one report: append the JSON object to the dated report itself

## Answer

Yes, persist it, but without a second file: after #539 merges, the sweep appends the same machine-readable JSON object as one fenced block at the end of its dated Markdown report, so each sweep still adds exactly one file (NFR-001 unchanged) and every report carries its own machine facts.

## What happens next if the owner picks it

- SW-11 becomes a small Phase 2 item after SW-05 (the #539 merge): one PR in a master-based worktree changes the report writer (`report.py`, `render` at line 608) to append a block such as "```json ... ```" containing the stdout object (without `report_path`, which names the file itself).
- Tests that pin the report's exact content are updated in the same PR (which ones: UNVERIFIED until the PR is planned); NFR-001's two tests (`test_readonly.py:300`, `test_cli_contract.py:1474`) should pass unchanged because the file count does not change.
- The contract note (XC-05) registry records "sweep report JSON v1 is also embedded in the dated report".
- The stdout JSON stays as it is for the calling coordinator.

## What it unlocks

- Every past sweep becomes machine-readable without a sidecar, a second file, or a rule change; readers find facts by report date.
- v2 (#423) or a Coder#477 status record can read stored sweep facts later with no new producer work (ADJ A-001 names them as the candidate readers).
- No caller has to invent storage rules; retention follows the reports.

## What it costs or risks

- A code and format change to a newly merged tool, with no named reader today (the spec says the consumer today is "the coordinator or a person; no observer consumer", `merged-requirements.md:221`).
- The report file grows; reports are read by people, and a large JSON block makes them harder to read.
- Two copies of the same facts (stdout and embedded) can drift if one is changed without the other; a test must pin that they match.
- Raw worker-written text inside the JSON is sanitized for stdout (design `:563`); the embedded copy needs the same sanitizing in a Markdown context (UNVERIFIED that the existing sanitizer covers fenced blocks).
- It answers a question the spec deliberately left for the first real reader to shape.

## What stays unresolved

Field list and retention for any reader; whether people still want the report readable at a glance.
