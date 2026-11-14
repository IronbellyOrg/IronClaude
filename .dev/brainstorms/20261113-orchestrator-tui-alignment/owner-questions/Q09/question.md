# Q9: should the sweep's machine-readable JSON ever be kept, and how

## The question, verbatim from the spec row

Source: `merged-requirements.md:536` (section 3, "Owner decisions").

> | Q9 | Store the sweep JSON beside the report, capture from stdout, or neither | Not now; Phase 2 caller-side stdout capture first; relax NFR-001 only if a stored file is needed | ADJ: Phase 2; NFR-001 unchanged | SW-11 | W5 |

Original wording (ADJ Part 7, `alignment-findings-adjudicated.md:779`): "Should the sweep's JSON ever be stored beside the report (which needs you to relax 'a sweep adds exactly one report file', NFR-001), or captured from stdout by the caller, or not at all?"

## Spec's recommended answer

"Not now. Phase 2: caller-side stdout capture first; relax NFR-001 only if a stored file is needed" (ADJ:779; `merged-requirements.md:536`).

## Default if unanswered

ADJ: persistence is a Phase 2 matter and NFR-001 is unchanged (`merged-requirements.md:536`).

## What it gates (work items, in words)

- SW-11, DEFERRED: the sweep JSON persistence decision. If a stored file is chosen, NFR-001's design line and two pinned tests change in the same pull request, and the contract note's registry (XC-05, the planned note between the observer and the sweep) is amended (`merged-requirements.md:200`).
- Through SW-11: OB-09 (observer release 3) only if Q17 (show sweep facts in the observer) is answered yes; V2-04 (the first release of Orchestrator v2, issue #423) only if v2 reads stored sweep facts (`merged-requirements.md:200`, `:401`).
- Wave W5 (later phases, each behind its own gate; not scheduled by the spec, `merged-requirements.md:865`).

## Facts the question depends on

| Fact | Source |
|---|---|
| The sweep ("sweep report JSON v1": `schema_version`, snake_case, `null`, rows keyed `row_id` = `orca:<dispatch>`) is printed to stdout only | ADJ E-05 (line 131) |
| `superclaude sweep run` always writes a dated report before it prints JSON; NFR-001 "a sweep adds exactly one report file" is pinned by the design (`docs/designs/orchestrator-mode.md:128`) and two tests (`tests/sweep/test_readonly.py:300`, `tests/sweep/test_cli_contract.py:1474`) | ADJ E-07 (line 133); spec K-NFR001 row (`merged-requirements.md:618`) |
| On exit 0 the sweep produces "1 report and 1 JSON object"; the JSON is printed only after the report's commit point and carries `report_path` | `docs/designs/orchestrator-mode.md:331`, `:347`, `:563`; `src/superclaude/cli/sweep/report.py:613-694` (read 2026-11-14) |
| The dated Markdown report does not embed the JSON object (no JSON block written by `render`) | `src/superclaude/cli/sweep/report.py:608` (grep 2026-11-14; UNVERIFIED beyond that grep) |
| Today's sweep consumer is the coordinator or a person; there is no observer consumer; "Consumers never run another sweep merely to fetch status" | `merged-requirements.md:221` |
| Sweep JSON is a candidate carrier only for v2 and for a Coder#477 status record, not for the observer (78 percent) | ADJ A-001 (line 361) |
| A "no write" status criterion cannot be met because a sweep always writes a report | ADJ X-004 (line 346) |
| No JSON key and no sidecar file may be added inside PR #539 (A-004) | `merged-requirements.md:194`, `:661` |
| A coordinator may sweep at most once per 5 minutes (worker-contract rule WC-16) | ADJ glossary line 81 |
| Q17 (observer showing sweep facts) is recommended "No, not now; if yes later, Q9 becomes a real requirement" | `merged-requirements.md:544` |
