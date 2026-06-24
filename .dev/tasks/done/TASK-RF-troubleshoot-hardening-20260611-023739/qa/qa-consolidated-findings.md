# Consolidated QA Findings — FINAL_ONLY Gate (Step 8.9)

Consolidation of the 7 lens reports (Steps 8.2–8.8). Deduplicated; each finding carries
severity, originating lens(es), affected file, disposition, and required fix.

## Per-lens verdicts

| # | Lens | Agent | Verdict |
|---|------|-------|---------|
| 8.2 | Structural — template/schema conformance | rf-qa | FAIL (1 MINOR) |
| 8.3 | Structural — internal consistency | rf-qa | FAIL (1 IMPORTANT) |
| 8.4 | Structural — completeness | rf-qa | FAIL (doc count-drift; physical set 15/15 COMPLETE) |
| 8.5 | Content — actionability/spec-fidelity | rf-qa-qualitative | FAIL (1 IMPORTANT design-note + 2 MINOR) |
| 8.6 | Content — domain accuracy vs code anchors | rf-qa-qualitative | **PASS** |
| 8.7 | Content — cross-reference chain integrity | rf-qa-qualitative | **PASS** |
| 8.8 | Domain — advisory 4-token invariant | rf-qa | **PASS** (critical regression guard clean) |

**Consolidated verdict: FAIL → fixes required.** The advisory invariant (the exact regression that
caused this rebuild) is CLEAN across all artifacts (8.8 PASS, independently confirmed by 8.3/8.6/8.7).
No schema field is missing/renamed/fabricated; no 3-token enum exists anywhere; 18/18 tests pass.

## Findings (deduplicated)

### C-1 [MINOR → FIX] MD040 bare fences in `commands/troubleshoot.md`
- **Lens:** 8.2 (MINOR-1).
- **File:** `src/superclaude/commands/troubleshoot.md` — 5 fenced blocks in the `## Examples` section open with a bare ` ``` ` (no language tag). Pre-existing (git diff shows this task only added 1 advertise sentence + 1 Will line) but the file is a listed deliverable, and Step 7.21 did NOT lint it (it linted only the 9 skill files, not the command).
- **Disposition:** FIX. Tag each bare opener ` ```text ` (content-preserving; same fix already applied to `remediation-handoff.md` in Phase 6). Makes the command file markdownlint-clean.

### C-2 [IMPORTANT → FIX] H1 card label "11-field" is inconsistent with the actual 10-row / 12-token schema
- **Lens:** 8.3 (F1); echoed by 8.4 (H1 label) and 8.7 (informational).
- **Files:** `tests/troubleshoot/test_hardening_h1.py` (docstring + comment say "11-field"); `phase-outputs/reports/qa-input-inventory.md:14` ("§5.6 11-field card"). The shipped REF (`runtime-entrypoint-verification.md`) is CORRECT — a verbatim 10-row §5.6 table with no missing field (8.2 confirmed). The test's assertion loop correctly checks all 12 atomic field tokens and is GREEN. Only the descriptive label "11" (which matches neither 10 rows nor 12 tokens) is wrong.
- **Disposition:** FIX (doc/comment-only). Harmonize the label to the ref's actual structure ("H1 card schema — 10 rows / 12 field tokens"); leave the 12-token assertion loop unchanged so the suite stays green.

### C-3 [OUT-OF-SCOPE — DOCUMENT] Stale internal counts in `research/08-v1.1.0-deliverable-reconciliation.md`
- **Lens:** 8.4 (G1: "17" vs 18 tests; G2: §5.5 "10" vs 11 fields wording; G3–G11 minor count drift); 8.7 (informational, L129 "17").
- **File:** `research/08-v1.1.0-deliverable-reconciliation.md` — a **frozen prior-stage research INPUT**, NOT a deliverable authored by this implementation task. Its authoritative header (L49-51) and the as-built reality both say 18; an interior line (L129) carries a stale pre-G-PRE-1 "17".
- **Disposition:** DO NOT MODIFY (frozen input — mutating prior-stage research mid-execution corrupts provenance and is out of scope). The SHIPPED deliverables are correct (18 tests, 11 additive fields, verified by 8.4's own 15/15 physical-completeness pass). The drift is inert: the tasklist is already built+executed, so research 08 will not be re-consumed to regenerate anything. Documented as non-blocking.

### C-4 [BY-DESIGN — DOCUMENT] Tests are content-assertion markers, not behavioral gates
- **Lens:** 8.5 (F1).
- **Detail:** All 18 tests assert that the rule STRING is documented in the `src/` markdown; none constructs e.g. an empty ledger and observes a runtime FAIL. This is the **designed** executable-validation architecture for this increment (spec §4.7; the `tests/skills/` content-assertion pattern the task mandates). Behavioral replay (the E1–E5 backtest suite) is explicitly spec-deferred to milestone M5 / NFR-1 and documented as such in `pytest-summary.md` and `e2e-backtest-scenarios.md`.
- **Disposition:** NOT a defect — designed scope. No fix. (Caveat already surfaced: "18/18 PASS" proves the rules are documented, not that gates behaviorally fail-closed; M5 validates the latter.)

### C-5 [SPEC-FAITHFUL — DOCUMENT] FR-4 `forbidden_interpretation` is "yes when applicable"
- **Lens:** 8.5 (F2/F3).
- **Detail:** `runtime-entrypoint-verification.md` marks `forbidden_interpretation` "yes when applicable" and the negative-witness requirement as conditional on "every contract with a forbidden interpretation." This reproduces spec §5.6 / FR-4 VERBATIM.
- **Disposition:** NOT a defect — the ref is spec-faithful; tightening it would DEVIATE from the spec. No fix.

## Fix plan (Step 8.10)

Apply C-1 and C-2 only (both content-preserving, neither alters spec-faithful content):
1. C-1: tag the 5 bare ` ``` ` fences in `commands/troubleshoot.md` `## Examples` as ` ```text `.
2. C-2: harmonize the "11-field" H1 label in `test_hardening_h1.py` + `qa-input-inventory.md` to the actual 10-row/12-token structure (assertion loop unchanged).

C-3/C-4/C-5 require no change (out-of-scope frozen input / by-design / spec-faithful). After C-1+C-2, re-run markdownlint (command file) + pytest (suite stays green) + verify advisory invariant intact.
