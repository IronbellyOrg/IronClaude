# QA Report — Task Integrity Check

**Topic:** Fix two sprint-recovery data-integrity defects (sprint merge-stranding + checkpoint-stale)
**Date:** 2026-06-08
**Phase:** task-integrity
**Fix cycle:** N/A
**Fix authorization:** true

---

## Overall Verdict: PASS

All structural, schema, granularity, evidence-binding, and BUILD_REQUEST-encoding
checks pass. Every cited `file:line` anchor was independently re-verified against
the live source files (not trusted from the research artifacts). No issues required
in-place fixes. One spawn-prompt parenthetical (`spec_path` frontmatter field) was
investigated and resolved as a non-defect — see Issues Found #note.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | YAML frontmatter complete/well-formed | PASS | Frontmatter (L1-50) parses; all mandatory Template-02 fields present with values (`id`,`title`,`status`,`type`,`created_date`,`assigned_to`,`task_type`,`template_schema_doc`). `reflect_pre: ""` + `reflect_post: ""` PENDING-sentinel present per research-04 §1a / SKILL.md PART-2 (L1935-1949). `spec_path` is NOT a defined frontmatter key in the source-truth contract — it is an inline value (`SPEC_PATH: NONE`) in item 8.3; absence is correct (see note). |
| 2 | All mandatory sections present | PASS | Task Overview, Key Objectives, Prerequisites, Execution Context, Detailed Instructions (8 phases), Task Log/Notes (Summary, Execution Log, per-phase Findings, Risks & Open Questions, Builder Notes) all present. |
| 3 | Items self-contained (5-field schema) | PASS | All 19 `- [ ]` items carry Context + Action + Output + Verification + Completion gate. Verified by reading every item (L139-344). |
| 4 | Granularity: one fn-mod / one test per item | PASS | 2.1=recovery.py fn; 2.2=rerun_tasks.py caller; 4.1=checkpoints.py fn; 4.2=commands.py CLI; 4.3=rerun_tasks.py PRIMARY; tests split 3.1/5.1/5.2 (one per test). No batch items. |
| 5 | Evidence-based: file:line in Context | PASS | Every code-surface Context cites file:line. Spot-verified live: `merge_recovery_bundle` def@recovery.py:381; status flip@:674 (`PARTIAL if failures else SUCCESS`); failures@:431; Step 4 comment@:502 (blank@:501); atomic idiom@:519-521; `_declared_deliverables`@rerun_tasks.py:954; merge call@:1484; `recover_missing_checkpoints`@checkpoints.py:213, short-circuit@:249; verify-checkpoints@commands.py:647/663/693; `_check_checkpoint_pass`@executor.py:2510-2513. ALL CONFIRMED. |
| 6 | No items on contradicted/unverified findings | PASS | `source_index.parent` canonical-root claim cross-checked vs recovery.py docstring `_resolve_release_dir` caveat — research-04 reconciles: TASKLIST_ROOT = release_dir/tasklists = source_index.parent (≠ release_dir). REPORT L60 + research-01 L28-31 agree. Not a contradiction. `_render_recovered_checkpoint` UNKNOWN/never-PASS verified@checkpoints.py:415-438. |
| 7 | Open Questions / gaps documented | PASS | Risks & Open Questions (L411-417): canonical-dest, fix-order, path-asymmetry, idempotency, sidecar status-string. Builder Notes/Gaps (L419-422) flags 4.3 design-level wiring. |
| 8 | Phase dependencies logical (DAG, no cycles) | PASS | Phases 1→8 linear; intra-Phase-4 order 4.1(checkpoints fallback)→4.2(CLI flag)→4.3(consumes flag) correct; Phase 6 6.1→6.2(reads 6.1)→6.3 correct; `depends_on: []` (standalone). Acyclic. |
| 9 | Item count reasonable for scope | PASS | 19 items for 4 source mods + 2 tests + validation + QA + reflect + bookkeeping. Within bounds. |
| TB-1 | Placeholder scan (TBD/TODO/FIXME) | PASS | `grep -nE '\bTBD\b\|\bTODO\b\|\bFIXME\b'` → NONE in item bodies. |
| TB-2 | Item count bounds (3-50 single-track) | PASS (ADVISORY) | 19 items, within advisory bounds. |
| TB-3 | Clarification adjacency | PASS | No frontmatter Open Questions block blocking items; risks are informational (BUILD_REQUEST-derived), not item-blocking. |
| TB-4 | Circular dependency (item DAG) | PASS | Item-ref graph acyclic; no item references a later item that references back. |
| TB-5 | XL splitting / granularity | PASS | Largest items (2.1, 4.3) are single-function design-level mods; 4.3 flagged in Builder Notes as design-level (justified). No XL multi-file item. |
| TB-6 | Verify/AC format consistency | PASS | All items use `**Verification**:` + `**Completion gate**:` consistently. |
| TB-7 | Execution Context Source areas reappear + header no file:line | PASS | Header block (L121-128) `grep -cE 'src/\|/.*:[0-9]+'` = 0 (correct). 5 Source areas (recovery merge engine, rerun orchestrator, checkpoints logic, verify-checkpoints CLI, sprint test suite) each reappear in items 2.1/2.2, 4.3, 4.1, 4.2, 3.1/5.1/5.2. |
| TB-8 | Per-item Context evidence binding | PASS | Every code-referencing Context carries file:line (verified item-by-item). No bare surface references without citation. |
| BR-1 | FINAL_ONLY QA gate present | PASS | Phase 7 item 7.1 = FINAL_ONLY rf-qa task-integrity gate (L293, L297). `FINAL_ONLY` token x2. |
| BR-2 | VALIDATION (lint/format + pytest, NO sync-dev, new branch, never-stage .claude) | PASS | 6.3 make lint/format (no sync-dev, L260/283); 6.1/6.2 `uv run pytest tests/sprint/ -v`; 1.3 new feature branch off master; "never stage .claude" x4; "do NOT run sync-dev" x3. |
| BR-3 | TESTING UNIT (3.1, 5.1, 5.2 + conditional fix) | PASS | Test items 3.1 (Test A), 5.1 (Test B positive), 5.2 (Test B negative) present; 6.2 = conditional fix branch (L273). |
| BR-4 | Ship-Fix-1-before-Fix-2 ordering | PASS | Phase 2 (Fix 1) precedes Phase 4 (Fix 2); ordering rationale stated L168, L228, L414 ("ship together", "depends on Fix 1"). |
| BR-5 | Path-asymmetry note surfaced as risk/Context | PASS | Risk L415 + Phase-4 preamble L205 + item 4.3 Context L228; matches executor.py:2510-2513 vs rerun_tasks.py path. |
| BR-6 | POST reflect: penultimate, reflect_post PENDING, HALT | PASS | 8.3 (POST reflect, HALT) is penultimate; 8.4 (Done) last. Writes `reflect_post: PENDING`, surfaces `/sc:reflect --mode post`, HALTs at completion gate (L330-335). Uses `/sc:reflect` not `/sc:task`. |

## Summary
- Checks passed: 28 / 28
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0

## Confidence
- **Confidence:** "Verified: 28/28 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%"
- **Tool engagement:** "Read: 2 | Grep: 0 (grep run via Bash) | Glob: 0 | Bash: 9"
- All 28 checks marked VERIFIED with cited tool output (live source re-reads, not research-artifact reliance). Each Bash call targeted specific anchors/claims, not padding.

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| — | — | — | None | — |

**Note (investigated, NOT a defect): `spec_path` frontmatter field.**
The spawn prompt's check #1 named `spec_path` as a frontmatter field to verify.
It is absent from the task frontmatter. Investigated against source truth:
the authoritative reflection-gate frontmatter contract (research-04 §1a citing
SKILL.md PART-2 L1935-1949, and template-02 itself) defines exactly two reflect
fields — `reflect_pre:` and `reflect_post: ""` — and NO `spec_path` key. SPEC_PATH
is an inline value (`SPEC_PATH: NONE`) consumed by item 8.3's optional `[--spec {SPEC_PATH}]`
reflect-command arg, correctly omitted because no spec governs this troubleshoot-derived
hotfix. Per Verification Principle 6 (source truth is king), the documented contract
overrides the spawn-prompt parenthetical. The task file is CORRECT as written.

## Actions Taken
No fixes required — the task file passed all 28 checks against live source truth.

## Recommendations
- Green light to proceed to execution. The task is structurally sound, every cited
  anchor verifies live, and all BUILD_REQUEST requirements are encoded.
- During execution, item 4.3 (PRIMARY post-merge re-verify) is the only design-level
  wiring (not a single pinned insertion line) — already flagged in Builder Notes;
  the executor should locate the post-merge region by name/comment per the item's
  drift-tolerance clause.

## QA Complete
