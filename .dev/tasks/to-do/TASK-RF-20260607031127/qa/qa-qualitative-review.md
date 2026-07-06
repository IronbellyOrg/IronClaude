# QA Report — Task File Qualitative Review

**Topic:** TASK-RF-20260607031127 — PR #140 r3 fixes (executor.py) + regression tests
**Date:** 2026-06-07
**Phase:** task-qualitative
**Fix cycle:** N/A (initial review)

---

## Overall Verdict: PASS

All 15 checklist items verified against actual source on branch `feature/prd-input-spec`.
All 5 adversarial axes applied per item. No issues of any severity found.

## Items Reviewed
| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Gate/command dry-run | none | PASS | All commands target real paths. `git rev-parse` (1.2), `uv run pytest tests/cli/prd/test_spec_flag.py` (3.4), `make lint` (4.1), `uv run ruff format --check src/ tests/` (4.2), `uv run pytest tests/cli/prd/ -v` (4.3) all valid; `git diff --stat feature/prd-input-spec` (PG.1) valid. Test file exists (447 lines), suite dir exists. No always-failing gate. |
| 2 | Project convention compliance | none | PASS | executor.py + test_spec_flag.py are plain Python source (NOT `.claude/` mirrors) — task correctly has no `make sync-dev` item (confirmed L55, L124). Both `make lint` (ruff check) AND `uv run ruff format --check` present as separate items 4.1/4.2 per memory `make lint ≠ CI ruff format`. Tests via UV, no inline `python -c`. |
| 3 | Intra-phase execution order simulation | none | PASS | Phase 1 (branch checkout) → Phase 2 (source fixes: 2.1 Fix1, 2.2 helper, 2.3 gate uses 2.2 helper, 2.4 message uses 2.2 helper — correct ordering) → Phase 3 (tests, after fixes exist) → Phase 4 (validation). 2.3/2.4 depend on 2.2's `_bound_spec_paths` being added first; order is correct. |
| 4 | Function signature verification | none | PASS | `_bind_specs(self, parsed: dict) -> dict` at executor.py:1196 ✓. `spec_files = list(self._config.spec_files or [])` at L1209 ✓. `for sp in spec_files:` at L1215 ✓. `p = Path(sp)` at L1216 ✓. `_persist_bound_specs` at L1245 ✓. `_warn_spec_degradation` at L1264 ✓. `specs = ", ".join(self._config.spec_files)` at L1274 ✓. R5 gate `if step_id == "scope-discovery" and self._config.spec_files:` at L645 ✓. ALL anchors EXACT-match. |
| 5 | Module context analysis | none | PASS | `json` imported L23, `Path` imported L30 — task correctly says DO NOT add imports. `_bound_spec_paths` mirrors `_persist_bound_specs` fail-closed pattern (`except (OSError, json.JSONDecodeError)`). `task_dir` is `PrdConfig.task_dir: Path` (models.py:187). SPECS objects carry `"path"` key (executor.py:1224 + test fixtures L239). Method placement (adjacent to spec helpers) matches module grouping. |
| 6 | Downstream consumer analysis | none | PASS | Fix 2 changes the gate condition (L645) and the message source (L1274). BOTH consumers of the resume-path behavior are updated: gate (makes WARN fire) AND message (lists persisted paths). Task explicitly requires both (L53, Key Objective 2, Steps 2.3+2.4). Critically: gate-alone would print empty list — task avoids that incomplete change. Fix 1 changes `spec_files` before SPECS built; downstream `parent_dirs`/WHERE loop reads deduped list correctly. |
| 7 | Test validity | none | PASS | Test 1: real `_bind_specs({})` call with `spec_files=["foo.md","foo.md"]`, asserts SPECS len==1 + WHERE idempotent — FAILS pre-fix (2 entries), PASSES post-fix. Test 2: empty config.spec_files + persisted parsed-request.json SPECS + `_warn_spec_degradation()` direct call — exercises Fix 2c message rewire (`_bound_spec_paths()` reads persisted). Test 3: missing + corrupt JSON → `[]`. No stubs; all exercise real behavior with representative input. |
| 8 | Test coverage of primary use case | none | PASS | Three tests cover both fixes end-to-end: dedup (Fix 1), resume-WARN-from-persisted (Fix 2 message+helper), fail-closed (Fix 2 helper edge). Plus Step 4.3 runs full prd suite (regression guard). Primary use cases of BOTH review comments are covered. |
| 9 | Error path coverage | none | PASS | Test 3 explicitly covers both fail-closed branches: missing parsed-request.json (OSError) and corrupt JSON (JSONDecodeError) → `[]`. Helper also defensively filters non-dict/missing-path SPECS entries (`isinstance(s, dict) and s.get("path")`). Matches `_persist_bound_specs` fail-soft contract. |
| 10 | Runtime failure path trace | none | PASS | Resume flow traced: `resolve_config` omits `spec=` (commands.py:215-224) → config.spec_files empty → pre-fix gate L645 falsy → WARN never fires (the bug). Post-fix: gate `self._bound_spec_paths()` reads persisted SPECS → truthy → `_warn_spec_degradation` → message `", ".join(self._bound_spec_paths())` lists persisted path. No downstream gate/consumer breaks; `_bind_specs` empty-guard preserved so `prd run` path unchanged. |
| 11 | Completion scope honesty | none | PASS | Open Questions section (L329-331) states the one design choice (read persisted SPECS vs add --spec to resume) was resolved upstream → read persisted SPECS. Task implements exactly that; does NOT add --spec to resume (matches rejected-alternative in findings L75). No ignored open questions. |
| 12 | Ambient dependency completeness | none | PASS | No new imports needed (json/Path present). `_bound_spec_paths` is a private method called only intra-class (gate L645, message L1274) — no `__init__.py` export, CLI parser, or registry touchpoint needed. Test imports already present in module (json, Path, PrdConfig, PrdExecutor, resolve_config). No dead-code risk. |
| 13 | Kwarg sequencing red flags | none | PASS | No kwarg-before-signature pattern. Fix 2: helper added (2.2) BEFORE its call sites are rewired (2.3 gate, 2.4 message). Correct deferred-completion ordering. Fix 1 is self-contained (one insertion). |
| 14 | Function existence claims verified | none | PASS | Grep-verified on target branch: `_bound_spec_paths` and `_deduped` do NOT exist yet (correct — to be added). `_bind_specs`, `_persist_bound_specs`, `_warn_spec_degradation` exist at claimed lines. Test idioms `_executor_with_specs` (L161), `_write_parsed` (L58), `_scope_config` (L63), `capsys`+`_warn_spec_degradation` (L350), `PrdConfig(task_dir=...)`, `spec_files` field — ALL exist. |
| 15 | Cross-reference accuracy | none | PASS | Adapted (no template §N refs): all file:line anchors (executor.py:1196/1209/1215/1216/1245/1264/1274/645, models.py spec_files/task_dir, commands.py resume) verified against actual source. research/01-findings.md exists with the verbatim code blocks the task embeds; embedded code matches findings byte-for-byte. |

## Summary
- Checks passed: 15 / 15
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (none required)
- Axis lens status: AX-1 Drift ACTIVE (BUILD_REQUEST.GOAL verbatim available in spawn prompt TRACK GOAL — task title/description/objectives match it exactly, no drift, no scope inflation).

## Adversarial Axis Findings (all 5 applied per item)
- **AX-1 Drift:** ACTIVE. TRACK GOAL = "two fixes to executor.py (r3367342586 low + r3367342583 medium) + regression tests in test_spec_flag.py." Task scope matches exactly. All cited file:line anchors are in-sync with current source on feature/prd-input-spec (no stale citations). No weaker-verb paraphrasing. CLEAN.
- **AX-2 Contradictions:** No item contradicts another or the source. Embedded Fix 1 (8-space indent, method body) and `_bound_spec_paths` (4-space, class-method) indentation match executor.py structure. `json`/`Path` availability matches (no re-import). SPECS `"path"` key consistent across _bind_specs, fixtures, and helper. CLEAN.
- **AX-3 Omissions:** Both required Fix-2 touchpoints present (gate 2.3 + message 2.4 — neither omitted; gate-alone would emit empty list). QA_GATE_REQUIREMENTS=FINAL_ONLY reflected (single Phase Gate, PG.1-PG.3). VALIDATION (lint 4.1 + format 4.2 + pytest 4.3) all present. TESTING=UNIT reflected (3 unit tests + suite run). No upstream requirement dropped. CLEAN.
- **AX-4 Weakened criteria:** Test 2's "either gate branch or `_warn_spec_degradation` directly" is NOT weakening — the gate at L645 is subprocess-bound (requires proc.start_with_retry, output files; see _run_subprocess_step) and impractical to unit-test; the direct-call path is the established module idiom (existing test_warn_emitted_to_stderr) and fully exercises the observable resume-path behavior (message sourcing from persisted SPECS). Acceptance criteria are as strong as evidence warrants. CLEAN.
- **AX-5 Invented content:** Every referenced file/method/idiom exists in source or research evidence. No invented caching, no Redis, no scope inflation. The only new symbols (`_bound_spec_paths`, `_deduped`) are exactly the proposed fixes from research/01-findings.md. CLEAN.

## Issues Found
None.

## Actions Taken
None — no issues required fixing. Task file is correct as written.

## Observation (non-blocking, informational only — NOT a finding)
Test 2 (Step 3.2), if executed via the direct `_warn_spec_degradation()` call (the practical path), exercises Fix 2c (message rewire) but not Fix 2b (gate condition L645), because the gate is embedded in `_run_subprocess_step` behind a live subprocess and is not unit-reachable with existing fixtures. This is acceptable and does NOT lower any acceptance criterion: (a) the task explicitly offers both paths and does not claim gate-branch coverage; (b) the gate rewire is a one-token change verified structurally by rf-qa (PG.2) and protected by the full prd suite (4.3); (c) the resume-path observable behavior — message listing persisted paths — IS exercised. No action needed.

## Self-Audit
**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- Relied on rf-qa PASS for frontmatter shape, mandatory template-02 sections, item self-containment, granularity, logical DAG phase deps, reasonable item count (21), TB-Add-1..8.
- Relied on rf-qa PASS for the machine-verified file:line anchors as STRUCTURALLY present (section numbering / item structure) — but re-verified them SEMANTICALLY (see below).

**(b) Independent semantic checks where rf-qa PASS was INSUFFICIENT (≥1 required, INV-019):**
- **Fix-2 completeness (gate + message both required):** rf-qa verified the gate rewire→L645 and message rewire→L1274 exist as items. My own work traced the RESUME DATA FLOW (commands.py:215-224 omits `spec=` → config.spec_files empty → gate falsy pre-fix) to confirm BOTH edits are semantically required and that gate-alone would emit an empty list. Tool evidence: `git show feature/prd-input-spec:commands.py` sed 211-235; `git show ...executor.py` sed 635-660 + 1190-1306.
- **Test 2 exercises the real fix, not a stub:** rf-qa confirmed `capsys`+`_warn_spec_degradation` idiom exists. My own work confirmed that with empty config.spec_files + persisted parsed-request.json, the direct `_warn_spec_degradation()` call routes through `_bound_spec_paths()` (Fix 2c) and lists the persisted path — failing pre-fix, passing post-fix. Tool evidence: read full test_spec_flag.py (447 lines) + traced `_bound_spec_paths` logic against models.py:187 task_dir.
- **Fix 1 dedup placement before SPECS loop:** rf-qa confirmed order-preserving dedup keyed on `str(Path(sp))`. My own work confirmed the insertion point (after L1211 guard, before L1213 `specs=[]`) ensures duplicates never enter SPECS. Tool evidence: executor.py:1190-1306 line-mapped.

## Confidence
- **Confidence:** Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 2 | Grep (via git show|grep): 4 | Glob: 0 | Bash: 8
- Each tool call mapped to specific checklist verifications — no padding. Several Bash calls each verified multiple items (e.g., the 1190-1306 + 635-660 dumps together verified items 3,4,5,6,9,10,13,14). All 15 items have cited source evidence.
- UNCHECKED items: none.
- UNVERIFIABLE items: none.

## Recommendations
- Task is ready to execute as written. No changes needed.
- During execution: confirm Step 3.4's new-test names don't collide with existing 33 test functions (none prescribed by task → low risk; executor chooses descriptive names).

## QA Complete
