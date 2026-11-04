# Evidence Validation Report (reflect Wave 5)

**Report under validation**: REPORT.md.draft
**Source**: evidence-validator agent, persisted by the orchestrator on receipt (2026-11-02T05:37Z)
**Total line-level citations**: 55 (all re-Read; full re-read)  **Verified**: 53  **Dropped**: 1  **Passed through**: 1  **Path-only references checked (exist)**: 9
**Suggested report status**: partial

## Dropped

| location | reason | action taken |
|---|---|---|
| Verification section, "No leftover test shim afterwards." (cited to verify-logs/pytest-ccsession.stdout.txt:17) | line 17 is only `262 passed in 170.66s`; no captured process check exists under verify-logs/ (only invocations.yaml, ruff.stdout.txt, pytest-ccsession.stdout.txt); the only source was the orchestrator's own audit note | sentence removed from REPORT.md; recorded under "Dropped by the evidence validator" with the implement run's logged pgrep checks (package artifacts/t4-tests.log:6-7, t5-checks.log:13-14) |

## Passed through

- Risks, first bullet (shared cgroup; 4013 shim survival), cited to adversarial/invariant-probe.md Resolution: the text says it, including the /proc reads; no raw capture is stored. Kept, labelled orchestrator-observed.

## Verified with notes (applied)

- D-4: added `ccsession:766` (code digest) to the stale-shim link.
- Risks: "six tries" comes from ccsession:769; the port step is +101 (ccsession:770); citation and wording updated.
- D-2: F15 location added (pre-detach.../adversarial/merge-log.md:23), marked not re-read by the validator.
- D-5, t5-checks.log:23-30 vs the cause comment at :31: supported within the cited range.
- Risks, proxy:126: `audit()` called per request at proxy:580; "on every request" holds.
- D-1 "tty branch has no test": grep for `isatty|tty` in tests/unit/test_ccsession_tiers.py returns nothing.
- Counts: 13 AC (plan 32-34, 43-44, 55-56, 67-70, 81-82); merged-verdict.yaml, tier_decision.yaml, input-snapshot.yaml and audit.log consistent with the report.

## Structural assertions

A1-A10 skipped (no assertions_path supplied).
