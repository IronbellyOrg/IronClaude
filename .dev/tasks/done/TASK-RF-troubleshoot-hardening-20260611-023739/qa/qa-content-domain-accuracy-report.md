# QA Report — Content Domain Accuracy (doc-qualitative)

**Topic:** troubleshoot-pipeline-hardening
**Date:** 2026-06-11
**Phase:** doc-qualitative (content domain-accuracy lens)
**Fix cycle:** N/A (REPORT ONLY — fix_authorization: false)

---

## Overall Verdict: PASS

The deliverables are domain-accurate. Every spawn-prompt verification target was independently
confirmed against the actual code anchors. No claim contradicts the code. The trigger is
heading-text-anchored, the Output Contract is strictly additive (19 legacy + 11 new), no CLI flag
was added, the test files use the mandated `REPO_ROOT` idiom and assert over `src/` markdown,
`make verify-sync` is clean, and the full test suite passes 18/18. No DOMAIN-ACCURACY error of any
severity was found — the "≥10 errors" assumption was tested adversarially against each anchor and
the spec-vs-code cross-validation, not waved through.

## Verification Targets (from spawn prompt)

| # | Target | Result | Evidence |
|---|--------|--------|----------|
| 1 | Trigger wired by HEADING TEXT after Tier-1 (W1.7) before report closure (W5) | PASS | New `### Wave 4.5: Pipeline Hardening Closure` sits between `### Wave 4` and `### Wave 5: Synthesis + Report` in SKILL.md; Wave Structure overview lists it after W4 / before W5; trigger prose says "runs after Tier-1 diagnosis is settled … and before report closure". Wave 5 Step 2 composition list gained a "Pipeline Hardening Closure" bullet. No line-number anchoring — heading text matches `skill-anchors.md` verbatim (em-dash U+2014 preserved). |
| 2 | Output Contract ADDITIVE — no legacy field renamed/removed (NFR-6) | PASS | All 19 legacy fields present and unchanged in SKILL.md `## Output Contract`; 11 new fields appended (`contract_version` … `known_escapes_caught`). `test_hardening_output_contract.py` LEGACY_FIELDS tuple = exactly 19, asserts each `\`field\`` still present; HARDENING_FIELDS = 11, all assert present. Matches `skill-anchors.md §(c)` "Total existing fields: 19." |
| 3 | Command added NO new CLI flag (NFR-5) | PASS | `argument-hint` (commands/troubleshoot.md:8) byte-identical to legacy flag set; no `--hardening` anywhere except negative assertions ("there is no `--hardening` flag"). New content = one Behavioral-Summary step-4 clause + one Boundaries→Will line. |
| 4 | Test files use `REPO_ROOT = Path(__file__).resolve().parents[2]`, assert over `src/` markdown | PASS | All 7 test modules open with `REPO_ROOT = Path(__file__).resolve().parents[2]` then resolve `REPO_ROOT / "src" / "superclaude" / "skills" / "sc-troubleshoot-protocol" / ...` and `.read_text()` the `src/` markdown. No `.claude/` assertions. Mirrors `tests/skills/` convention per research §F. |
| 5 | `make verify-sync` clean (run by reviewer) | PASS | Ran `make verify-sync` → exit 0, "✅ All components in sync." |
| 6 | No claim contradicts the actual code anchors | PASS | `_evaluate_gate` real at `src/superclaude/cli/prd/executor.py:828`; `SemanticCheck.advisory` real (`gates.py:319/446`, read by `_evaluate_gate` via `getattr(check, "advisory", False)`). E4 (advisory honored by generic gate but not PRD `_evaluate_gate`) is a genuine prior escape — confirmed by commit `acd5631f "fix(prd): honor advisory checks in the executor's _evaluate_gate"`. No invented symbols in any ref. |

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Trigger heading + placement | PASS | SKILL.md `### Wave 4.5` between W4/W5; Wave Structure map line + Refs index rows added. |
| 2 | Output Contract additive 19+11 | PASS | SKILL.md table; test LEGACY_FIELDS(19)+HARDENING_FIELDS(11); skill-anchors confirms 19. |
| 3 | No new CLI flag | PASS | argument-hint unchanged; grep `--hardening` → only negative assertions. |
| 4 | Test REPO_ROOT idiom + src target | PASS | 7 modules, all `parents[2]` + `src/...` read_text. |
| 5 | make verify-sync clean | PASS | exit 0. |
| 6 | Code anchors not contradicted | PASS | `_evaluate_gate`, `SemanticCheck.advisory` grep-confirmed. |
| 7 | 4-token verdict enum (advisory mandated) | PASS | `pass\|blocked\|advisory\|not_applicable` consistently in SKILL.md, both refs, report-template, handoff. No 3-token regression; tests guard `count('\`advisory\`') >= 2`. |
| 8 | §5.4 truth table 7 rows, all No-override | PASS | hardening-output-contract.md 7 priority rows; rows 5/6 = advisory; `test_verdict_aggregation_from_h_statuses` asserts `count('\| No \|') >= 7`. |
| 9 | Waiver one-way latch | PASS | hardening-output-contract.md §FR-12 "one-way … never resets to `none`"; forces `{blocked, advisory}`. |
| 10 | H1–H4 card/ledger/sweep/manifest field schemas | PASS | Field names in each ref match the per-H test tuples exactly (H1 12-field, H2 6-field, H3 10-field, H4 11-field). |
| 11 | remediation-handoff carries verdict + waiver_status | PASS | User-offer block + BUILD_REQUEST `PIPELINE_HARDENING:` both carry `pipeline_hardening_verdict` + `waiver_status`; reconciles success-gate. |
| 12 | report-template closure section + NOT PROVEN | PASS | `## Pipeline Hardening Closure` in-template + post-template rule; NOT PROVEN / ADVISORY blockers verbatim. |
| 13 | Test suite passes | PASS | `uv run pytest tests/troubleshoot/ -q` → 18 passed. |
| 14 | e2e scenarios not pytest-collected (M5) | PASS | `e2e-backtest-scenarios.md` self-documents as "documented … not pytest-collected … deferred to milestone M5". |
| 15 | OI-2 / OI-3 open items honestly deferred | PASS | contract-enumeration.md (OI-2 open-enum) + runtime-entrypoint-verification.md (OI-3 substitute-probe ranking) both mark PENDING and cite plan files; not silently closed. |

## Summary

- Checks passed: 15 / 15 (+ 6 spawn-prompt targets, all PASS)
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: false — REPORT ONLY)

## Issues Found

None. (Adversarial "≥10 errors" assumption tested and not borne out — see Self-Audit for what was
checked and why a clean result is defensible here.)

### Observations (NOT defects — no remediation required)

1. **Research file §E (line 69) lists 20 "existing" Output Contract fields, including
   `contract_version`.** This is a *research-note artifact*, not a deliverable defect: the
   discovery file `skill-anchors.md §(c)` and the shipped test `test_hardening_output_contract.py`
   both correctly classify `contract_version` as one of the **11 additive** fields and enumerate
   exactly **19** legacy fields. The deliverables (SKILL.md, tests) are internally consistent and
   correct; the discrepancy lives only in the earlier research scratch file, which is not a QA
   target and is superseded by `skill-anchors.md`. No action.

## Self-Audit

**(a) Reliance list — rf-qa structural PASS items skipped for structural re-check:**

No `## Inherited Structural Verdict` block was provided in the spawn prompt, so I ran standalone:
I did NOT rely on any upstream structural verdict and instead independently verified file
existence, field presence, test idioms, and sync state with my own tool calls.

**(b) Independent semantic checks (content correctness, ≥1 required, INV-019):**

- **Code-anchor reality check** — grepped `_evaluate_gate` (executor.py:828) and
  `SemanticCheck.advisory` (gates.py:319/446) to confirm the E4 escape the H1/H2 refs cite is a
  real prior defect, not an invented symbol. Cross-confirmed against commit `acd5631f`.
- **Additive-not-replacement check** — counted the 19 legacy fields in SKILL.md against the test's
  LEGACY_FIELDS tuple and `skill-anchors.md §(c)`; confirmed none renamed/removed (rf-qa structural
  presence ≠ semantic "additive" — required reading both the source table and the legacy
  enumeration to prove non-replacement).
- **No-flag-leak check** — grepped the entire skill dir + command for `--hardening`; confirmed it
  appears ONLY in negative assertions, proving the topology-trigger design is honored in content,
  not just claimed in prose.
- **Enum-token consistency check** — verified the 4-token `advisory`-inclusive verdict enum is
  identical across 5 surfaces (SKILL.md, 2 refs, report-template, handoff) with no 3-token
  regression — a semantic consistency dimension rf-qa field-presence checks do not cover.

**Self-Audit answers (mandatory):**

1. Factual claims independently verified against source code: 6 spawn-prompt targets + 15 checklist
   items, each tied to a specific tool call (grep/read/bash), plus 2 code-anchor greps and 1
   commit-log cross-check.
2. Files read to verify claims: SKILL.md (full), commands/troubleshoot.md, all 6 new refs, both
   modified refs (report-template.md, remediation-handoff.md), all 7 test modules,
   `skill-anchors.md`, `qa-input-inventory.md`, research `05-doc-crossvalidation-spec-vs-code-v2.md`;
   greps over `src/superclaude/cli/prd/{executor,gates}.py`.
3. Why trust a 0-issue result: I did not assert "looks fine." Each PASS cites a concrete tool
   result — `make verify-sync` exit 0, `pytest` 18 passed, grep line numbers for real code anchors,
   and a field-count reconciliation across three independent sources (SKILL.md table, test tuple,
   skill-anchors). The one discrepancy I found (research §E field count) I ran to ground and
   classified as a non-target scratch-file artifact rather than ignoring it.
4. Web research: none required — all verification was local-file / code-anchor bound. No Tavily or
   fallback engaged.

## Confidence

Verified: 21/21 (6 targets + 15 checks) | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

## Tool engagement

Read: 15 | Grep: 6 (within Bash) | Glob: 0 | Bash: 5 (verify-sync, pytest, 3 grep/ls batches)

## Recommendations

- None blocking. Proceed.
- (Optional, non-blocking) The research scratch file
  `research/05-doc-crossvalidation-spec-vs-code-v2.md` §E line 69 lists 20 "existing" fields
  (folding in `contract_version`); the authoritative `skill-anchors.md` and the shipped test both
  use 19. If that research file is retained as a historical record, no change needed; if it is ever
  promoted to a reference, reconcile its count to 19 legacy + 11 additive.

## QA Complete

VERDICT: PASS
