# QA Report — Task Integrity (Phase 2 Gate)

**Topic:** R5 Investigation & Reproduction (Steps 2.1-2.4)
**Date:** 2026-06-02
**Phase:** task-integrity / phase-2-gate
**Fix cycle:** N/A

---

## Overall Verdict: PASS

Every recorded value in all six output files was independently re-derived by re-running
the cited commands / scripts. Zero fabrications, zero unsupported determinations, zero
recorded-vs-rerun mismatches. No fixes were required.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | AC#1 — r5-current-state.md grep output is actual, confirms NO MD / NO md_ids / NO allowlist | PASS | Re-ran all 3 greps: `grep MD…pattern` → `no MD in ID_PATTERNS`; `grep md_ids` → 0 matches; `grep non_ref` → `no allowlist subsystem`. Independently confirmed ID_PATTERNS = FR/NFR/SC/G/D only (`__init__.py:64-69`), no MD key. File's claims match re-run byte-for-byte. |
| 2 | AC#2 — tokenizer probe output is literal; bare-D extraction from M{n}-D{nn} noted | PASS | Re-ran exact probe via `uv run python`. Output `{'D': ['D01', 'D02']}` — identical to recorded line 29. File explicitly notes the M{n}- prefix is discarded and M1-D01/M2-D01 collide (lines 32-35). Accurate. |
| 3 | AC#3 — every finding verbatim from captured output; FP-reproduces is evidence-based | PASS | Re-ran asymmetric `check_signatures` probe (spec M1-D01,M2-D01,M3-D01 vs roadmap M1-D01,M1-D02,M2-D03). Got `total findings: 2`, `HIGH phantom_id count: 2`, roadmap_quote D02/D03, spec_quote `[MISSING]` — identical to r5-repro-output.txt L4-9 and r5-reproduction.md L23-27. Also re-ran symmetric fixture → `total findings: 0` matching L14. |
| 4 | AC#4 — scope determination grounded in repro evidence + research, with rationale, carries to Phase 3 | PASS | Determination = MD-FAMILY-PLUS-ALLOWLIST. Verified oracle test #1 (`git show 861047c2 …:436-520`) uses `_write_md_fixture_with_allowlist`, roadmap body carries standalone bare-D `D01..D05` + `**Explicit non-references (do not resolve against spec):**` annotation. Tests #2/#3 (L520-560) use plain `_write_id_fixture` (no allowlist) as the table claims. Rationale + Phase-3 carry-forward present (L25-32). |

## ZERO-TRUST RE-RUN LEDGER

| Recorded claim | Source file:line | Re-run result | Match? |
|---|---|---|---|
| `no MD in ID_PATTERNS` | r5-current-state.md:7 | `no MD in ID_PATTERNS` | ✅ |
| `md_ids` 0 matches | r5-current-state.md:13 | `grep -rn md_ids …` → 0 | ✅ |
| `no allowlist subsystem` | r5-current-state.md:17 | `no allowlist subsystem` | ✅ |
| Tokenizer `{'D': ['D01', 'D02']}` | r5-current-state.md:29 | `{'D': ['D01', 'D02']}` | ✅ |
| Asymmetric `total findings: 2` / HIGH=2 / D02,D03 `[MISSING]` | r5-reproduction.md:23-27, r5-repro-output.txt:6-9 | `total findings: 2`, HIGH=2, D02/D03 `[MISSING]` | ✅ |
| Symmetric `total findings: 0`, 5→`{D01,D02}` | r5-reproduction.md:12-14, r5-repro-output.txt:2 | `total findings: 0`, extract `{'D': ['D01','D02']}` | ✅ |
| Spec collapse `{'D': ['D01']}`, road `{'D':['D01','D02','D03']}` | r5-repro-output.txt:4-5 | identical | ✅ |
| Oracle #1 uses `_write_md_fixture_with_allowlist` + bare-D D01..D05 + allowlist annotation | r5-scope-determination.md:19 | `git show 861047c2 …:436-520` confirms helper, roadmap body `reference D01..D05`, `**Explicit non-references…**` annotation | ✅ |
| Oracle #2 (`_write_id_fixture`, no allowlist) | r5-scope-determination.md:20 | L497-518 confirms plain `_write_id_fixture`, D1/D3/D5↔D01/D03/D05 → 3 drift | ✅ |
| Oracle #3 (`_write_id_fixture`, no allowlist, D9 phantom) | r5-scope-determination.md:21 | L520-548 confirms plain helper, 1 HIGH phantom D9 | ✅ |
| ID_PATTERNS families FR/NFR/SC/G/D, bare-D body `D-?\d+` | r5-current-state.md:8,35 | `__init__.py:64-69` confirms exactly those 5 keys + `D: D-?\d+` | ✅ |

## Summary
- Checks passed: 4 / 4 acceptance criteria + 11 / 11 zero-trust re-runs
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (none required)

## Issues Found
None.

## Adversarial Notes (why this PASS is trustworthy)
- I did NOT rely on the recorded `r5-repro-output.txt`; I rebuilt the asymmetric probe from
  scratch with fresh temp fixtures and got the identical 2-HIGH result, including the exact
  `roadmap_quote`/`spec_quote` values.
- I checked the oracle test at the actual cited commit `861047c2` and read the full helper +
  all three test bodies — confirming the allowlist dependency is structural (oracle #1's
  roadmap text contains standalone bare-D `D01..D05` that only the
  `**Explicit non-references…**` annotation can exempt). The scope=MD-FAMILY-PLUS-ALLOWLIST
  determination is genuinely evidence-forced, not a speculative scope expansion.
- The symmetric-vs-asymmetric distinction in r5-reproduction.md is a sophisticated, correct
  observation: the prescribed identical-set fixture (Step 2.3 as literally written) yields 0
  findings, and the investigator correctly recognized that the realistic FP requires asymmetry
  and constructed/recorded both. This is more rigorous than the step required, not less.

## Confidence Gate
- **Confidence:** Verified: 4/4 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 7 | Grep: 0 (greps issued via Bash) | Glob: 0 | Bash: 8
  - (Tool-engagement minimum satisfied: 15 tool calls ≥ 4 checklist items; every Bash call
    maps to a specific re-run in the ledger above. No web research performed — all claims
    were local/code-bound, so Tavily-first rule did not trigger.)

## Actions Taken
None — no fixable doc errors found; all recorded values matched re-runs exactly.

## Recommendations
- Green light to proceed to Phase 3. The scope carry-forward
  (`decision: PROCEED`, `scope: MD-FAMILY-PLUS-ALLOWLIST`) is evidence-grounded and the
  Phase 4 allowlist port (item 4.4) + 3-oracle port (item 4.12) are correctly scoped IN.

## QA Complete
