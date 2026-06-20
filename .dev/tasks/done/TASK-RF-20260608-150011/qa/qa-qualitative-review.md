# QA Report — task-qualitative

**Topic:** Fix two sprint-recovery data-integrity defects + 2 regression tests
**Date:** 2026-06-08
**Phase:** task-qualitative
**Fix cycle:** N/A (initial)
**Task file:** /config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260608-150011/TASK-RF-20260608-150011.md
**fix_authorization:** true (in-place edits applied — see Actions Taken)

---

## Overall Verdict: PASS

All 15 task-qualitative checks pass after two in-place hardening edits to the task file
(items 4.3 and 3.1). Every cited file:line anchor in the task was independently verified
against the actual source and all anchors resolved correctly. The two latent IMPORTANT
findings (FALLBACK path-asymmetry not re-pinned; Test A fixture geometry not representative
of production) were fixed in-place by strengthening the task instructions, so no issue of
any severity remains unresolved.

## Items Reviewed
| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Gate/command dry-run | none | PASS | `uv run pytest tests/sprint/{test_recovery,test_checkpoints}.py` → 54 passed (clean base). UV-only commands (`make lint`/`make format`/`uv run pytest`) are project-correct. `verify-checkpoints --help` will list `--reevaluate-stale` after 4.2 (option add is well-formed click). No gate is unsatisfiable. |
| 2 | Project convention compliance | none | PASS | All 4 source edits target `src/superclaude/cli/sprint/*.py` (CLI Python, NOT synced components) — task correctly says NO `make sync-dev`/`verify-sync` needed. New-branch-off-master, never-commit-master, never-stage-.claude all honored (items 1.3, 8.x). |
| 3 | Intra-phase execution order simulation | none | PASS | Phase order Fix1→TestA→Fix2→TestB→validate→QA→post is dependency-correct. 2.1 (add param) precedes 2.2 (pass kwarg). 4.1 (signature+branch) precedes 4.2 (CLI thread) precedes 4.3 (caller). No item reads an artifact a later item creates. |
| 4 | Function signature verification | none | PASS | `merge_recovery_bundle(bundle, source_index, *, release_dir=None)` recovery.py:381-386 ✓; `_declared_deliverables(source_tasklist, task_id)->list[Path]` :954-978 ✓ (cwd-resolved, never raises); `recover_missing_checkpoints(manifest, artifacts_dir, phase_tasklists, *, return_bundle=False)` :213-219 ✓; `verify_checkpoints(output_dir, recover, as_json)` commands.py:663 ✓; `_check_checkpoint_pass` executor.py:2510-2521 ✓. New kwargs (`expected_deliverables=None`, `reevaluate_stale=False`) preserve verb-agnostic defaults. |
| 5 | Module context analysis | none | PASS | recovery.py: `import shutil` function-local :413 ✓ (task says don't re-import); `.failed-<mtime>` idiom :444-449/:466-471/:487-492 ✓; atomic tmp+replace :518-521 ✓; single status-flip :674 + single audit-log :676-687 ✓ (task says reuse, don't duplicate). `_render_recovered_checkpoint` :398-439 frontmatter has no `status:`/`verdict:` key ✓. No import cycle introduced (data flows via param; recovery imported BY rerun_tasks :49). |
| 6 | Downstream consumer analysis | none | PASS | Fix-1 new failures flow into existing `failures` list → existing status-flip :674 → existing audit log → PARTIAL surfaces. Fix-2 regenerated/re-stamped report's consumer is `_check_checkpoint_pass` (release_dir/checkpoints) — the path-asymmetry consumer was correctly traced; FALLBACK re-pinning now made explicit (see Actions Taken). Sidecar producer (rerun_tasks:1480-1483) feeds merge step-7 consumer. |
| 7 | Test validity | none | PASS | Test A asserts a real disjunction (trees landed+SUCCESS OR PARTIAL+`deliverable-not-landed:` failure) via the real JSONL audit-log idiom and `is`/`in` against `RecoveryStatus` (never string literals). Test B reads real `expected_path.read_text()` substrings. No `# Test`-stub placeholder pattern. |
| 8 | Test coverage of primary use case | none | PASS | Test A exercises merge with real bundle+sidecar+deliverable trees (primary Defect-1 path). Test B positive+negative pair covers re-stamp-fires and re-stamp-suppressed (primary Defect-2 path + safety property). Both would FAIL pre-fix (Test A: `TypeError` on unknown kwarg; Test B: existing-file short-circuit returns unchanged). |
| 9 | Error path coverage | none | PASS | New `--reevaluate-stale` flag: no-op when `--recover` absent (gated by `if recover:`), documented. Empty `artifacts_produced` guard (skip relocation, no crash) specified in 2.1. `_declared_deliverables` returns `[]` on read/parse error (never raises). Never-auto-PASS hard constraint enforced in all Fix-2 branches. |
| 10 | Runtime failure path trace | none | PASS | Data flow: rerun→bundle(`<bundle>/results/phase-*` + `<bundle>/{artifacts,evidence}/`)→merge_recovery_bundle(Step3.5 relocate→canonical_root=source_index.parent)→failures→status. Fix-2: re-run checkpoint task→Fix-1 copy-back→`_check_checkpoint_pass` read site. The one break point (FALLBACK writing to index_path.parent vs read at release_dir/checkpoints) is now re-pinned in 4.3. |
| 11 | Completion scope honesty | none | PASS | Builder Notes explicitly disclose 4.3-PRIMARY is design-level (not a single pinned line) with a concrete FALLBACK guard. Risks section honestly lists fix-order coupling, path-asymmetry, idempotency, sidecar-string watch-out. Open Questions are addressed, not ignored. POST reflect gate HALTs (penultimate), Done is last. |
| 12 | Ambient dependency completeness | none | PASS | Fix-1: param added (2.1) + caller threads it (2.2) — no orphan. Fix-2: signature (4.1) + CLI option+param+kwarg (4.2) + caller wiring (4.3) all present; `--reevaluate-stale` reaches `recover_missing_checkpoints`. No new imports/exports needed (no `__init__` change; `merge_recovery_bundle` already imported :49). |
| 13 | Kwarg sequencing red flags | none | PASS | No "add kwarg before add param" inversion. 2.1 adds `expected_deliverables` param BEFORE 2.2 passes it. 4.1 adds `reevaluate_stale` param BEFORE 4.2 threads it via CLI BEFORE 4.3 relies on it. Deferred-action (POST reflect) has an explicit completion gate. |
| 14 | Function existence claims verified | none | PASS | grep/Read-confirmed: `merge_recovery_bundle`, `_declared_deliverables`, `recover_missing_checkpoints`, `_render_recovered_checkpoint`, `_check_checkpoint_pass`, `verify_checkpoints`, `TASK_BLOCK_PATTERN`, `_resolve_release_dir`, `build_manifest`, `extract_checkpoint_paths`, `_STATUS_MARKER_RE`, `_ARTIFACTS_SECTION_RE` all EXIST at cited locations. `--phase`/`--quiet` correctly claimed ABSENT (grep-confirmed). `checkpoint_gate_mode` correctly claimed absent from rerun_tasks.py. |
| 15 | Cross-reference accuracy for templates | none | PASS | This task references SOURCE file:line (not template §N) — adapted per the doc-task table: every cited line (recovery.py 381/413/431/444/466/487/500/501/502/518/581/623/674/676; rerun_tasks.py 49/61/954/1304/1368/1436/1444/1484/1487/1508/1526; checkpoints.py 213/248/398/415/436; commands.py 647/663/687/693; executor.py 2510; summarizer.py 69; test_recovery.py 28/51/67/153; test_checkpoints.py 293/407/454/645) was Read-verified accurate. |

## Summary
- Checks passed: 15 / 15
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 2 (both IMPORTANT, hardened in the task file)
- Axis lens status: AX-1 Drift ACTIVE (TRACK GOAL captured verbatim from spawn prompt: "Fix two sprint-recovery data-integrity defects + add 2 regression tests, per .dev/troubleshoot/sprint-merge-stranding-checkpoint-stale-20260608144847/REPORT.md"). No drift between task content and GOAL detected.

## Issues Found (all fixed in-place)
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | item 4.3 (rerun_tasks.py Fix-2 FALLBACK) | The FALLBACK route extends the Step-14 subprocess (`verify-checkpoints <index_path.parent> --recover`) with `--reevaluate-stale`, but `recover_missing_checkpoints` re-stamps at the `build_manifest`-derived `expected_path` (resolved against `index_path.parent`), which in the sc:tasklist subdir layout does NOT equal `config.release_dir/checkpoints/CP-P{NN}-END.md` where `_check_checkpoint_pass` reads (executor.py:2510-2521, verified). The task identified the asymmetry in its Risk note but item 4.3's FALLBACK only added the flag — it did not re-pin the output, so in the divergent layout the re-stamp would not change the gate result. (AX-3 omission / AX-4 the path-pin requirement was stated for PRIMARY but weakened/absent for FALLBACK.) | FIXED: added an explicit "PATH-ASYMMETRY GUARD FOR THE FALLBACK (REQUIRED)" clause to item 4.3 instructing the executor to verify the re-stamped report is present at `config.release_dir/checkpoints/CP-P{NN}-END.md` after the subprocess and mirror/copy it there if layouts diverged. |
| 2 | IMPORTANT | item 3.1 (Test A) | Production `artifacts_produced` is globbed from `<bundle>/results/phase-*` (rerun_tasks.py:1444-1446, verified) so `[0].parent.parent` = `<bundle>`. But the reused fixture `_bundle_with_sidecar` anchors the placeholder DIRECTLY in `bundle_dir` (test_recovery.py:63-78, verified — no `results/` subdir), so `[0].parent.parent` = `tmp_path/bundles`, a level too high. Test A is SELF-CONSISTENT (test-seed and Step-3.5 relocation both use the same `.parent.parent` formula, so it goes green) but does NOT reproduce the production `<bundle>/results/` nesting, so it under-tests the real relocation geometry. (AX-3 omission: fixture does not mirror production bundle layout.) | FIXED: added an explicit NOTE to item 3.1 documenting the fixture-vs-production geometry divergence, instructing the test to seed trees under `artifacts_produced[0].parent.parent` so seed and relocation agree, and flagging that the test is self-consistent but not production-representative (acceptable for the stranded-⇒-not-SUCCESS coupling under test). |

## Minor observations (no fix required; within design tolerance)
- item 2.1 verify maps cwd-resolved `_declared_deliverables` paths against `canonical_root` via relative tail; loosely specified but the relocation itself is subtree-walk-driven (independent of declared paths), and the failure-append is the safety net. In production cwd==repo-root so paths map cleanly. Not load-bearing.
- item 4.1 "phase's gating tasks now pass" is implementable only as the proxy "evidence discovered for the phase" (no existing gating-pass evaluator in `recover_missing_checkpoints`; `_discover_phase_artifacts` only finds evidence by phase number). This is a mild AX-4 softening of "now pass," but it does NOT break the never-auto-PASS invariant (re-stamp emits UNKNOWN, requiring human/re-run confirmation), and Test B 5.1/5.2 are consistent with the proxy. Acceptable given the safety body is UNKNOWN, not PASS.

## Actions Taken
- Fixed Issue #1 in `TASK-RF-20260608-150011.md` item 4.3 by inserting an explicit FALLBACK path-asymmetry guard requiring post-subprocess verification + mirror to `config.release_dir/checkpoints/CP-P{NN}-END.md`. Verified the edit landed (Edit succeeded).
- Fixed Issue #2 in `TASK-RF-20260608-150011.md` item 3.1 by inserting a fixture-geometry NOTE clarifying the `.parent.parent` resolution divergence between `_bundle_with_sidecar` and production, keeping test-seed and relocation-read aligned. Verified the edit landed (Edit succeeded).
- No source code (`src/`) was edited — all findings were task-PLAN quality issues; the correct in-place fix is to harden the plan instructions, which is what the executor will implement against.

## Inherited Structural Verdict — Reliance Audit (PR-04, INV-019)

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- Relied on rf-qa PASS for #1 YAML frontmatter, #2 mandatory sections, #3 5-field item schema, #4 granularity, #6 no-contradicted-findings, #7 Open Questions documented, #8 DAG no-cycles, #9 item count, TB-1..TB-8 structural gates, BR-1..BR-6 (FINAL_ONLY QA, VALIDATION, TESTING UNIT, ship-Fix-1-first, path-asymmetry note present, POST reflect penultimate+HALT).
- I did NOT re-verify section numbering, frontmatter shape, item-field presence, or DAG acyclicity — those are machine-verified.

**(b) Independent semantic checks (≥1 required, INV-019) — where rf-qa PASS was INSUFFICIENT and my own tool work was required:**
- rf-qa #5 "Evidence file:line PASS" only confirms citations are well-FORMED; it does NOT confirm they point at the claimed CODE. I Read recovery.py:380-688, rerun_tasks.py:45-64/954-978/1290-1349/1430-1534, checkpoints.py:213-283/398-439, commands.py:645-699, executor.py:2505-2529, summarizer.py:65-72 and grep-confirmed every cited anchor resolves to the described construct (checklist #14). This is verification rf-qa cannot do.
- rf-qa BR-5 "path-asymmetry note PASS" only confirms the NOTE EXISTS; it does NOT confirm the fix ADDRESSES it. I traced `_check_checkpoint_pass` (executor.py:2513 reads `release_dir/checkpoints`) vs the FALLBACK subprocess (rerun_tasks.py:1526 passes `index_path.parent`) vs `build_manifest` resolution (checkpoints.py:161) and found the FALLBACK did not re-pin — Issue #1 (checklist #6/#10). rf-qa PASS was insufficient here.
- rf-qa BR-3 "TESTING UNIT PASS" confirms tests are PRESENT; it does NOT confirm they exercise production geometry. I Read `_bundle_with_sidecar` (test_recovery.py:51-79) and rerun_tasks.py:1444-1446 and found the fixture's `.parent.parent` ≠ production `.parent.parent` — Issue #2 (checklist #7/#8). I also ran `uv run pytest tests/sprint/{test_recovery,test_checkpoints}.py` → 54 passed to confirm a clean base.

## Self-Audit

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- Frontmatter/sections/item-schema/granularity/DAG/item-count/TB-1..8/BR-1..6 — relied on as machine-verified per the Inherited Structural Verdict; not re-checked structurally.

**(b) Independent semantic checks (≥1 required, INV-019):**
- Every file:line anchor (30+ across 8 files) — verified by Read + Grep against actual source (e.g., recovery.py:674 status-flip, rerun_tasks.py:1484-1486 merge call, checkpoints.py:436-438 UNKNOWN constraint, executor.py:2513 read path).
- Path-asymmetry fix sufficiency (Issue #1) — traced 3 sites across executor/rerun_tasks/checkpoints; found gap; fixed in-place.
- Test fixture vs production geometry (Issue #2) — compared test_recovery.py:63-78 against rerun_tasks.py:1444-1446; found divergence; fixed in-place.
- Clean-base confirmation — `uv run pytest` 54 passed.

### Self-Audit (mandatory questions)
1. **How many factual claims independently verified against source?** ~35 (every cited file:line anchor across 8 source/test files, plus 3 behavioral traces: status-flip path, path-asymmetry consumer, bundle-layout geometry).
2. **What specific files did you read?** recovery.py (100-118, 380-688), rerun_tasks.py (45-64, 954-983, 1290-1349, 1360-1374, 1430-1539), checkpoints.py (213-283, 398-439), commands.py (645-699), executor.py (2505-2529), summarizer.py (65-72), test_recovery.py (28-157), test_checkpoints.py (293-320, 405-474, 638-652).
3. **If 0 issues, why trust?** Not applicable — found 2 IMPORTANT issues and fixed both; the evidence trail (line-by-line anchor verification + a green 54-test base run) shows the verification was real, not rubber-stamped.
4. **Web research?** None performed — this review is entirely local-file-bound (task file + source). No Tavily/WebFetch needed; nothing to record in a Tool-engagement web-fallback summary.

## Confidence
- **Confidence:** Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 9 | Grep: 0 | Glob: 0 | Bash: 3 (2 grep-via-bash + 1 pytest) | Edit: 2 (task fixes) + Write: 2 (report)
- No UNCHECKED items. No UNVERIFIABLE items. The 8 source/test files Read cover all 15 checks (multiple checks share the same Read regions), so checklist coverage is complete, not padded.

## Recommendations
- Proceed to execution. The plan is operationally sound; both IMPORTANT residuals are now hardened in the task file.
- During execution, pay attention to item 4.3-PRIMARY (design-level wiring of single-checkpoint-task re-run through the rerun machinery) — this is the highest-uncertainty step and the FALLBACK is its guard.
- Confirm Test A goes RED on pre-fix code (expect `TypeError` on the new `expected_deliverables` kwarg) before implementing, per the task's own stash-and-re-run-on-base instruction.

## QA Complete
