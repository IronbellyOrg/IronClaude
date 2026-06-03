# QA Report — Research Gate (Partition B of 2)

**Topic:** Post-R1 roadmap-pipeline brittleness-elimination follow-ups (A–E)
**Date:** 2026-06-03
**Phase:** research-gate
**Fix cycle:** N/A
**Fix authorization:** false (report-only)

**Assigned files (Partition B):**
- research/05-area-de-dualwrite-vectorA-registry.md
- research/06-template-examples-sprintcli.md
- research/07-test-verification.md

[PARTITION NOTE: Cross-file checks (contradictions, scope coverage) limited to assigned subset. Full cross-file verification requires merging all partition reports.]

---

## Verification log (incremental)

All 3 assigned files read in full. Highest-stakes claims independently re-tested with Read/Grep/Bash against live source. Findings below.

---

## Confidence

**Verified:** 10/10 | **Unverifiable:** 0 | **Unchecked:** 0 | **Confidence: 100%**

**Tool engagement:** Read: 4 | Grep: 0 (via Bash grep) | Glob: 0 | Bash: 7 (each maps to a specific claim cluster: cutover yaml counts; writer/reader/parser callers; remediation-test + WIRING_GATE; live pytest --collect-only; sprint-CLI + executor-B wiring; conftest/MD-family/contracts/commit; Contract#9-MERGE_GATE wiring + PHASE_FILE_PATTERN; status headers). No web research performed (all claims local source-truth). tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0.

Tool-engagement check: 11 tool calls vs 10 checklist items — above the minimum; every call targeted a specific claim.

---

## Highest-stakes claims — RE-TESTED myself

| Claim | Source | My verification | Result |
|---|---|---|---|
| CUTOVER PRECONDITION NOT-MET: all 13 steps `release_marker_count: 0`, `cutover_eligible: false`, `cutover_at_count: 3` | 05 F1 | Read `.dev/migrations/r1-4-cutover-counters.yaml` fully + grep-count | **CONFIRMED EXACT.** 13 step entries, every one 0/false/3. D/E correctly authored as HALT items. |
| 05: spec_id_registry.json single writer; gate reader `_roadmap_ids_within_spec` reads the JSON file + fails closed | 05 F3 | grep executor.py (`_save_id_registry` L611, `set_id_registry_sidecar_path` L661-663) + gates.py (`_roadmap_ids_within_spec` L996, `read_text` L1021, fail-shut L1013-1025, wired into `MERGE_GATE` L1218/L1268) | **CONFIRMED.** Single writer, one live fail-closed reader, reads JSON not envelope. Stranding risk real. |
| 05: remediate_parser.py ZERO production callers in src/ | 05 F4 | grep `parse_validation_report\|parse_individual_reports` across src/ → 0 hits outside its own def; 391 LOC confirmed | **CONFIRMED.** Zero src/ callers. |
| 06: "Sprint-CLI-compatible" = template-02 + /task-executable (NOT `sprint run`) | 06 §2 | Read sprint/commands.py (INDEX_PATH/tasklist-index L19/L210), config.py (`PHASE_FILE_PATTERN` L20, `_TASK_ID_HEADING_RE` L31, Execution Mode + ClickException), process.py (`/sc:task` L170) | **CONFIRMED.** sprint run consumes tasklist-index + per-phase files; MDTM single-file is /task-run. |
| 07: `uv run pytest --collect-only` → 1 collection error (Area A file) | 07 §0 | Ran `uv run pytest --collect-only -q` live | **CONFIRMED EXACT:** "7909 tests collected, 1 error", "Interrupted: 1 error during collection", root = `test_wiring_pipeline.py:28` ImportError on `WIRING_GATE` from `cli.roadmap.gates`. |

---

## Per-checklist findings

1. **File inventory** — All 3 files present, each ends with `## Status: Complete` (05 L141, 06 L310, 07 L180) and a Summary section. NOTE: 05 (L3) and 07 (L3) carry a contradictory top-of-file `**Status:** In Progress` header that was never flipped — the operative terminal status is Complete. MINOR cosmetic inconsistency, not a completeness failure.
2. **Evidence density** — DENSE (>80% evidenced). Every substantive claim carries a file:line citation; I independently opened the cited files and the line targets land within 0-15 lines of the cited anchors (e.g. writer cited L650 actually L611-665; reader L996 exact; tool_writer fns L344/421/455 exact; executor B-wiring L1269-1296 exact). No vague "the backend" assertions.
3. **Scope coverage (D/E/template/tests within partition)** — D, E covered exhaustively by 05; template/sprint-CLI/placement by 06; test landscape + per-area test design by 07. Areas A/B/C are touched by 07 (A baseline, B already-built finding, C non-unit-testable note). No unexamined key file within partition scope.
4. **Documentation cross-validation** — Doc-sourced claims ARE tagged: 05 uses `[CODE-VERIFIED]`, `[CODE-CONTRADICTED]` (F1 provenance), `[doc-cross-validated]`. The Vector-A-doc "no 3-release-cycles" claim verified (grep returns 0 matches; doc = 244 lines exact). I verified every `[CODE-VERIFIED]` cluster above. PASS.
5. **Contradiction resolution (within partition)** — No cross-file contradiction between 05/06/07. 05↔07 agree on the stranded-reader (gates.py:996) and envelope.py:165 R1.6 TODO. Consistent.
6. **Gap severity** — See Issues table. Two accuracy defects found (one IMPORTANT, one MINOR) plus a structural note: none of the 3 files has a labelled "Gaps and Questions" section — blockers are surfaced inline as HALT designs/recommendations instead. The substantive gaps ARE documented; the missing labelled section is a template-conformance MINOR.
7. **Depth appropriateness (Deep tier)** — 05 F6 traces an end-to-end ordering chain (reader-repoint → writer-deletion → per-step markdown deletion → parser deletion). 07 traces the phantom-ID data flow (extraction.json → spec_ids → validate_id_subset → render gate → StepResult FAIL). Deep-tier depth satisfied.
8. **Integration point coverage** — Contract #9 / MERGE_GATE wiring documented + verified (gates.py L1218/L1268); envelope↔registry absorption (envelope.py L146-167); executor↔tool_writer dispatch (executor.py L1269). PASS.
9. **Pattern documentation** — 06 documents Template-02 B2/E1-E4/F1 patterns + the rf-qa adversarial gate triplet; 07 documents the tool-writer test idiom (pure-fn over tmp_path, no mocking). PASS.
10. **Incremental writing compliance** — Files show incremental structure (numbered Findings with per-finding evidence logs; 05 explicitly "Evidence Log (incremental)"). Not one-shot-perfect. PASS.

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | IMPORTANT | 05 Finding 3, L90 | Overstated claim: "the only `spec_ids` consumer is the round-trip serializer in envelope.py." grep shows `verify_implementation.py` L57-120 is a substantial ACTIVE consumer of `envelope.spec_ids` (`.fr_ids`, `.accepted_deviation_ids`). The narrower claim ("no reader of envelope.spec_ids **for Contract #9**") is TRUE and the HALT design is unaffected — but the absolute parenthetical is false. Direction of error is an UNDER-claim of available infra (it actually means a working `envelope.spec_ids` accessor pattern already exists for the E-reader-repoint to reuse), so it does not weaken the HALT recommendation. Still a verified-fact misstatement. | Narrow the claim to "no Contract #9 / MERGE_GATE reader of envelope.spec_ids exists; note verify_implementation.py L57+ already consumes envelope.spec_ids.fr_ids and is the repoint template." Task-builder should fold this into the E-reader-repoint item as the reuse model. |
| 2 | MINOR | 05 Finding 4, L102 + L107/L179 | Conflation: lists `test_tool_write_step_remediation.py` among "4 test files [that] exercise" the parser. grep shows only **3** files call `parse_validation_report`/`parse_individual_reports`; `test_tool_write_step_remediation.py` only references `remediate_parser.py` in a docstring FLAG (L38-41), not via a function call. R5's downstream "deletion requires also removing/retargeting those tests" is overstated for the 4th file (deleting the parser would orphan a comment, not break a test). The "test_tool_write_step_remediation.py:40 MUST NOT be deleted... >= 3 release cycles" quote IS accurate (L40 verified). | Correct to "3 test files call the parser functions (test_remediate_parser.py, test_pipeline_integration.py, test_phase7_hardening.py); test_tool_write_step_remediation.py references it only in a docstring deferral FLAG." |
| 3 | MINOR | 05, 07 top-of-file (L3) | Header `**Status:** In Progress` contradicts the terminal `## Status: Complete`. Stale template header. | Flip L3 to Complete (cosmetic; does not affect downstream task design). |
| 4 | MINOR | 05/06/07 structure | No labelled "Gaps and Questions" section in any file (checklist item 6 / template conformance). Substantive blockers ARE documented inline (HALT designs, stranded-reader, deferral). | Optional: add a short "Gaps & Open Questions" section per file, or task-builder rolls the inline blockers into the task Open Questions. Non-blocking for actionability. |

---

## Actionability assessment

The partition is HIGHLY actionable for a task builder:
- 05 gives ready-to-use HALT-item designs for D and E with exact precondition checks (read the yaml; check `cutover_eligible`; PENDING marker + HALT). This directly honors the [Human-decision items must HALT, not auto-default] memory.
- 06 gives a complete Template-02 skeleton, frontmatter block, phase-gate triplet pattern, and the correct placement path.
- 07 gives exact verification commands per area, the precise Area A surgical fix (`git rm tests/integration/test_wiring_pipeline.py`), the over-delete warning (WIRING_GATE survives in cli/audit), and the missing-test gap for Area B (new executor-integration test).

The two accuracy defects (Issues 1-2) do NOT change the task design — both are mis-statements that, if anything, under-claim available infrastructure. But under zero-tolerance research-gate rules, ANY gap/defect regardless of severity = FAIL.

---

## Overall Verdict: FAIL

Per the research-gate zero-tolerance rule ("ALL gaps regardless of severity = overall FAIL; no severity level is exempt"), the presence of Issue #1 (IMPORTANT, verified-fact misstatement) plus three MINOR issues forces a FAIL verdict for this partition. The defects are small and correctable; the core safety-critical claims (cutover NOT-MET, stranded-reader, Area A collection error, sprint-CLI distinction) are all VERIFIED ACCURATE.

**Severity-rated issues:**
- CRITICAL: 0
- IMPORTANT: 1 (Issue #1 — 05 F3 absolute "only consumer" claim contradicted by verify_implementation.py)
- MINOR: 3 (Issue #2 parser test-count conflation; Issue #3 stale status header; Issue #4 no labelled gaps section)

**Recommendation to orchestrator:** Issues #1 and #2 should be corrected in 05 before synthesis (one-line edits). #3/#4 are cosmetic/template and can be deferred or folded into the task's Open Questions. After correcting #1-#2, this partition is green. No HALT escalation warranted — defects are minor and the high-stakes design hinges all verified.

[PARTITION NOTE: Cross-file contradiction/scope checks limited to assigned files 05/06/07. Full cross-file verification (vs files 01-04) requires merging all partition reports.]

## QA Complete
