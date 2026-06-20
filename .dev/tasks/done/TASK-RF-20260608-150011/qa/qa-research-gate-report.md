# QA Report — Research Gate

**Topic:** Fix two data-integrity defects in src/superclaude/cli/sprint/{recovery.py,rerun_tasks.py,checkpoints.py,commands.py} + 2 regression tests
**Date:** 2026-06-08
**Phase:** research-gate
**Fix cycle:** N/A
**Assigned files:** 01-fix-site-signatures.md, 02-test-fixtures.md, 03-checkpoint-gate-plumbing.md, 04-template-and-conventions.md (sole instance — verified all 4)

---

## Overall Verdict: PASS

Every load-bearing claim in the four research files was independently re-verified against the actual source on branch `fix/prd-document-capture-hotfix`. All cited line numbers, signatures, fixture bodies, negative claims, and the Fix-2 feasibility verdict are ACCURATE. No CRITICAL or IMPORTANT issues. Two MINOR observations are logged below; neither blocks the builder.

This was an adversarial pass: I opened each cited source file and confirmed the line numbers byte-for-byte rather than trusting the research. The research is unusually precise — anchored to a prior troubleshoot diagnosis — and survived zero-trust verification.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | File inventory (4 files, Status: Complete, Summary) | PASS | All 4 present; each opens `Status: Complete` (01:3, 02:3, 03:3, 04:3) and ends with a "Summary for the builder" section. |
| 2 | Evidence density | PASS (Dense) | >95% of claims carry `file:line`. Spot-verified ~30 distinct anchors below; all matched. |
| 3 | Scope coverage (6 EXISTING_FILES) | PASS | recovery.py, rerun_tasks.py, checkpoints.py, commands.py, test_recovery.py, test_checkpoints.py all examined across 01/02/03/04. |
| 4 | Doc cross-validation tags | PASS (N/A) | Research is code-traced, not doc-sourced; no untagged doc-architecture claims. CLAUDE.md conventions in 04 are correctly cited to file:line. |
| 5 | Contradiction resolution | PASS | The two apparent inconsistencies (sidecar "pass"/"passed"; path release_dir/index.parent) are BOTH explicitly surfaced by the research itself as deliberate facts, not unresolved conflicts. Verified real (see below). |
| 6 | Gap severity (all gaps = FAIL) | PASS | research-notes GAPS 1-3 are all RESOLVED by 01/02/03. GAP 4 (pipx drift) is marked Informational and out-of-scope (fix targets src/). No open gaps. |
| 7 | Depth appropriateness (Standard) | PASS | File-level + function-level coverage achieved; 01 traces the full 7-step merge data flow end-to-end. |
| 8 | Integration point coverage | PASS | 03 documents the rerun→verify-checkpoints subprocess data flow, the executor `_check_checkpoint_pass` consumer, and the release_dir/index.parent asymmetry. |
| 9 | Pattern documentation | PASS | Atomic tmp+replace, `.failed-<mtime>` forensic rename, failures→status flip, local-import-to-avoid-cycle, 5-field item schema all documented + verified. |
| 10 | Incremental writing | PASS | Files show iterative section growth (mtimes staggered 15:04–15:16; 02 written last/largest); not one-shot. |

---

## Independent verification log (zero-trust — what I actually checked)

**recovery.py (research 01) — ALL EXACT:**
- `merge_recovery_bundle` signature at 381-386 ✓ (read 381-386).
- `release_dir is None` lazy-import `_resolve_release_dir` at 415-420 ✓.
- Path anchors 425-431 (`results_dir`/`execlog_path`/`audit_log`/`phase`/`bundle_id`/`failures`) ✓.
- Step boundaries: Step1 @433, Step2 @459, Step3 @481, **Step4 @502**, Step5 @525, Step6 @576, Step7 @601 — ALL EXACT ✓.
- **Insertion anchor:** Step-3 loop ends at line 500 (`failures.append(f"copy-errors...")`), line 501 BLANK, line 502 = `# Step 4` comment — EXACT ✓. The "insert after Step 3, before Step 4 at 501→502" anchor is correct.
- Atomic tmp+replace at 519-521 ✓; result.json variant at 667-669 ✓.
- `.failed-<mtime>` rename idiom at 444-449 ✓.
- **Status flip at 674** (`PARTIAL if failures else SUCCESS`) — EXACT ✓.
- `write_recovery_audit_log` call 676-687 ✓; signature at 250 ✓.
- `RecoveryBundle` dataclass 76-114; required fields `bundle_id` (105) + `affected_phase` (106) only; all defaults verified ✓.
- `RecoveryStatus` enum 58-68 ✓.
- NEGATIVE: `grep _declared_deliverables recovery.py` → 0 hits ✓; no `rerun_tasks` import in recovery.py → 0 hits (cycle-free claim confirmed) ✓.

**rerun_tasks.py (research 01/02) — ALL EXACT:**
- `merge_recovery_bundle` imported at line 49 (within the 42-block `from .recovery import (...)`) ✓.
- `produced` glob at 1444-1446 — globs ONLY `<bundle>/results/phase-{phase}-*`, never bundle-root trees — Defect-1 root CONFIRMED ✓.
- `RecoveryBundle(...)` construction 1451-1459 ✓.
- merge call at **1484-1486** ✓; `finalize_checkboxes_on_success` at 1487 ✓.
- Step-14 verify-checkpoints subprocess 1508-1532; passes `str(config.index_path.parent)` @1526, `--recover` @1527 ✓; inline comment 1518-1525 documents NOT release_dir ✓.
- `_declared_deliverables` full body 954-978 ✓ (resolves relative paths against `Path.cwd()` @977).
- `TASK_BLOCK_PATTERN = ^### (T\d{2}\.\d{2})\b...` at 61-63 ✓.

**checkpoints.py (research 01/03) — ALL EXACT:**
- `recover_missing_checkpoints` signature 213-219 ✓.
- **Existence short-circuit at 248-260** (file exists → append unchanged → `continue` @260; verdict NEVER read) — Defect-2 site CONFIRMED ✓.
- Second short-circuit `entry.exists or phase not in tasklists` at 262-264 ✓.
- `_render_recovered_checkpoint` 398-439; frontmatter 415-421 has NO `status:`/`verdict:` key ✓.
- **UNKNOWN-not-PASS at 435-438** (``## Result`` + `` `UNKNOWN` ``) — hard constraint CONFIRMED ✓. (Research 01 cites "~436"; exact span 435-438 — within tolerance, body header @435.)

**commands.py (research 01) — ALL EXACT:**
- `verify_checkpoints` decorators+signature 647-663; only `--recover` + `--json`, no `--phase`/`--quiet` ✓.
- `recover_missing_checkpoints` call at 693 (3 positional args, `return_bundle` defaults False) ✓.

**models.py — ALL EXACT:**
- `CheckpointEntry` dataclass 485-514; fields phase/name/expected_path/exists (required) + recovered/recovery_source (default) — NO verdict/status field CONFIRMED ✓.
- `checkpoint_gate_mode: Literal[...] = "shadow"` at 566 ✓.

**executor.py (research 03) — ALL EXACT:**
- `_check_checkpoint_pass` 2510-2521; reads `config.release_dir/checkpoints/CP-P{n:02d}-END.md`; matches `"STATUS: PASS"` or `"**RESULT**: PASS"` after `.upper()` ✓.

**test fixtures (research 02) — ALL EXACT:**
- `_seed_release` 28-48: returns `(source_index, tmp_path, results_dir)` with `release_dir == tmp_path` ✓.
- `_bundle_with_sidecar` 51-79: sidecar status `"pass"` @67 ✓.
- `_seed_sprint` 293-320: returns `(index, p1, p2, p3)`; P3 End checkpoint carries `**Verification:**` ✓.
- `test_does_not_overwrite_pre_existing_file` 454-466: hand-builds `CheckpointEntry(phase=5,...,exists=False)`, asserts body verbatim + `exists is True` ✓ — correct Defect-2 baseline.
- `_full_recovery_manifest` 600-654: bundle under `results/rerun-bundle`, sidecar status `"passed"` @645 ✓.

**Fix-2 feasibility (research 03) — VERIFIED via external + in-repo corroboration:**
- External `/config/workspace/TUIBBS-scp/.dev/releases/current/v1-MVP/tasklists/phase-12-tasklist.md` (832 lines) reachable: `### T12.17 -- Checkpoint: End of Phase 12` @783 ✓, `**Checkpoint Report Path:** ...CP-P12-END.md` @802 ✓, `status: PASS` acceptance @822 ✓, mid-phase checkpoint tasks T12.06 @249 / T12.16 @732 ✓.
- IN-REPO corroboration: `.dev/e2e-reflect/live-tl/bundle/phase-2-tasklist.md` has `### T02.03 -- Checkpoint: End of Phase 02` @115 + `CP-P02-END.md` @134 — same heading form, matches `TASK_BLOCK_PATTERN` → end-of-phase checkpoint IS a selectable rerun target ✓. **Fix-2 PRIMARY feasibility verdict is SOUND.**

**Cited template/example/diagnosis files (research 04) — ALL EXIST:**
- REPORT.md, worked example task file, Template-02, task-builder SKILL.md (`reflect_post` @1942, POST item @1996) all present ✓.

**Path-asymmetry claim (research 03) — VERIFIED LOAD-BEARING:**
- `_resolve_release_dir` (config.py:242) returns `index_path.parent` in flat layout but the grandparent in `tasklist/` subdir layout. So `config.release_dir` (read by `_check_checkpoint_pass`) and `config.index_path.parent` (passed to Step-14 subprocess) genuinely DIVERGE in the subdir layout. Research 03's "pin the target explicitly rather than assume equality" is a correct, important warning ✓.

---

## Cross-file contradiction analysis (zero-trust focus item #4)

Both flagged "inconsistencies" are REAL CODE FACTS that the research correctly surfaces rather than errors:

1. **Sidecar status string "pass" vs "passed"** — VERIFIED REAL. `_bundle_with_sidecar` (test_recovery.py:67) writes `"status": "pass"`; `_full_recovery_manifest` (test_checkpoints.py:645) writes `"status": "passed"`. Research 02 explicitly calls this out (02:110, 02:337, 02:486) and instructs the builder to "match whichever helper you reuse." This is a pre-existing test-suite inconsistency, not a research defect. NOT a blocker — but see MINOR-2.

2. **Path asymmetry config.release_dir vs config.index_path.parent** — VERIFIED REAL and load-bearing (see verification log). Research 03 surfaces it as a "watch-out" with a concrete mitigation. Correct.

No unresolved contradictions BETWEEN the four research files. Where the same fact appears in multiple files (e.g. `recover_missing_checkpoints` 213-219 in both 01 and 02; UNKNOWN-not-PASS in both 01 and 03; the existence short-circuit in both 01 and 03), the citations AGREE.

---

## Summary

- Checks passed: 10 / 10
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: N/A (fix_authorization: false)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | MINOR | research 01, anchors "~436"/"~248-264"/"~674" etc. | A handful of REPORT-sourced anchors use "~" approximations; the research's OWN re-derived exact lines (435-438, 249-260, 674) are correct and present. The "~" forms could mislead a careless builder by ±1-2 lines. | None required for accuracy (research already gives the exact lines alongside). Builder should use the research's exact spans, not the "~REPORT cited" parentheticals. Non-blocking. |
| 2 | MINOR | research 02 / builder hand-off | The "pass" vs "passed" sidecar inconsistency is correctly surfaced but the builder must not introduce a THIRD variant in new test code. The merge engine reads `status` opaquely (recovery.py splices by `task_id`, never matches the literal), so either string works; risk is only cosmetic test-suite drift. | Builder: when writing Test A, reuse one existing helper verbatim and match its status literal. Already advised in 02:486. Non-blocking. |

## Recommendations

- GREEN LIGHT for synthesis / task-building. The research is dense, code-traced, and survived independent line-by-line verification with zero accuracy defects.
- The builder should treat the research's EXACT line spans (not the "~REPORT cited" approximations) as authoritative — they were re-derived directly and I confirmed them.
- Defect-1 fix: thread declared deliverables IN as a new optional param to `merge_recovery_bundle` (do NOT import `_declared_deliverables` — confirmed cycle risk). New failures must go through `failures.append(...)` to drive the 674 status flip.
- Defect-2 fix: the stale-FAIL case is genuinely net-new (recover only handles MISSING files); any re-stamp must emit `UNKNOWN`, never auto-PASS (checkpoints.py:435-438 constraint confirmed), and must land where `_check_checkpoint_pass` reads (`config.release_dir/checkpoints`, not `index.parent`) — pin explicitly.

---

## Confidence

**Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 14 | Grep: 0 | Glob: 0 | Bash: 5 (each Bash bundled multiple targeted grep/sed verifications mapping to specific checklist items: negative-claim greps, signature greps, external-tasklist anchors, sidecar-status diff, `_resolve_release_dir` body)

All 10 checklist items VERIFIED with cited tool output. No UNCHECKED or UNVERIFIABLE items. Tool-call count (14 Read + 5 multi-target Bash) exceeds the 10-item checklist minimum; each call targeted a specific claim (recovery.py spans, checkpoints.py spans, models.py fields, test fixtures, external tasklist anchors, negative-claim greps), none were padding.

No web research was performed (all claims were intrinsically local/codebase-bound; no external standard/URL/third-party-API claim required Tavily).

## QA Complete
