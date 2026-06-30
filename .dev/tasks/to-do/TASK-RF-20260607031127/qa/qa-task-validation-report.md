# QA Report — Task Integrity

**Topic:** Fix PR #140 review comments (dedup --spec + R5 resume-path WARN) on branch feature/prd-input-spec
**Date:** 2026-06-07
**Phase:** task-integrity
**Fix cycle:** N/A (first pass)
**Task file:** `.dev/tasks/to-do/TASK-RF-20260607031127/TASK-RF-20260607031127.md`
**Template:** 02

---

## Verification Method

All file:line claims in the task and research were verified against the **target branch**
`feature/prd-input-spec` via `git show feature/prd-input-spec:<path>` — NOT the current
checkout (`feature/prd-spec-flag`), where `tests/cli/prd/test_spec_flag.py` does not yet exist.
This is correct: the research notes explicitly state anchors were read from
`origin/feature/prd-input-spec`, and the task's Step 1.2 checks out that branch before any edit.

---

## Overall Verdict: PASS

## Items Reviewed

### A. Spawn-prompt structural checklist (1–9)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | YAML frontmatter complete & well-formed | PASS | Lines 1–43. All template-02 mandatory fields present with non-empty values: `id`, `title`, `status` (🟡 To Do), `created_date`, `type`, `priority`, `assigned_to`, `tags`, `task_type`. `depends_on: []` valid. Parses as block-mapped YAML. |
| 2 | All mandatory template-02 sections present | PASS | Task Overview (L47), Key Objectives (L57), Prerequisites & Dependencies (L66), Execution Context (L110), Detailed Task Instructions w/ phases (L120), Post-Completion Actions (L248), Task Log/Notes w/ findings subsections (L258). |
| 3 | Items self-contained (context+action+output+verification+completion gate) | PASS | Every `- [ ]` item embeds: read-the-evidence context, a concrete action, the output path/effect, an "ensuring …" verification clause, a blocker-logging fallback, and "mark this item as complete" gate. Verified on Steps 2.1–2.4, 3.1–3.5, 4.1–4.3, PG.1–PG.3. |
| 4 | Granularity — no batch items | PASS | Fix 1 (2.1), helper (2.2), gate rewire (2.3), message rewire (2.4) are separate items. Each of the 3 tests is its own item (3.1, 3.2, 3.3). Lint / format / suite are 3 separate items (4.1/4.2/4.3). |
| 5 | Evidence-based — specific file paths/anchors not vague | PASS | Items cite `executor.py` `_bind_specs` (~L1196/1209/1215), helper adjacent to `_persist_bound_specs` (~L1245), gate `executor.py:645`, message `executor.py:1274`, and `tests/cli/prd/test_spec_flag.py`. All anchors verified against target branch (§C). |
| 6 | No items from CODE-CONTRADICTED/UNVERIFIED findings | PASS | research/01-findings.md tags every cited line `[CODE-VERIFIED]`; no `[CODE-CONTRADICTED]` / `[UNVERIFIED]` / `[STALE DOC]` tags present. |
| 7 | Open Questions & remaining gaps documented | PASS | Open Questions (L329-331) records the one design choice resolved upstream (read persisted SPECS, do NOT add `--spec` to resume). research GAPS = "None blocking". |
| 8 | Phase dependencies logical (no circular/missing) | PASS | P1 setup → P2 source (helper 2.2 before gate/message 2.3/2.4 that consume it) → P3 tests → P4 validation → Phase Gate → Post-Completion. Strict forward data flow; no cycles. |
| 9 | Reasonable item count for scope | PASS | 21 items for a 2-fix + 3-test + 3-validation + QA-gate task. Proportionate. |

### B. Task-specific correctness points (per spawn prompt)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| B1 | Fix 1 embeds order-preserving dedup keyed on `str(Path(sp))` in `_bind_specs` | PASS | Step 2.1 code block (L149-156): `_seen`/`_deduped`, `key = str(Path(sp))`, order preserved; prose L159 reaffirms. Matches research Finding 1 verbatim. |
| B2 | `_bound_spec_paths()` fails closed (returns `[]`) on OSError/JSONDecodeError | PASS | Step 2.2 code L176-177 `except (OSError, json.JSONDecodeError): return []`. Mirrors verified `_persist_bound_specs` (executor.py:1255-1256 target branch). |
| B3 | Gate rewire targets executor.py:645; message rewire targets executor.py:1274 | PASS | Verified target branch: L645 gate, L1274 message — exact match. Steps 2.3/2.4 target exactly these, single-expression replacement. |
| B4 | NO task item adds `--spec` to the prd resume command | PASS | Only NEGATIVE statements (L55, L331: "Do NOT add `--spec` to the resume command"). No commands.py edit item exists. |
| B5 | No item instructs adding imports for Path or json | PASS | Every `import` mention (L116/L140/L159/L182) = "already imported / DO NOT add". `json` (executor L23), `Path` (executor L30) confirmed imported on target branch. |
| B6 | Validation includes BOTH `make lint` AND `uv run ruff format --check src/ tests/` | PASS | Step 4.1 = `make lint`; Step 4.2 = `uv run ruff format --check src/ tests/`, noting CI runs them separately (matches memory `make lint ≠ CI ruff format`). |
| B7 | Branch = feature/prd-input-spec; executor.py canonical (NO sync-dev) | PASS | Step 1.2 confirms/checks out the branch. Both `sync-dev` mentions (L55, L124) are negative ("NO `make sync-dev` step"). |

### C. Source-truth cross-validation (verified against `feature/prd-input-spec`)

| # | Claim | Result | Evidence |
|---|-------|--------|----------|
| C1 | executor.py = 1306 lines; test module = 447 lines | PASS | `wc -l` on target-branch blobs: 1306 / 447 — matches research-notes L18/L24. |
| C2 | `_bind_specs` ~L1196, `spec_files=list(...)` L1209, guard L1210-1211, `for sp` L1215, `p=Path(sp)` L1216 | PASS | sed 1196–1244 confirms structure; docstring L1205-1206 promises idempotency. |
| C3 | R5 gate L645 `...and self._config.spec_files:` | PASS | sed 645 target branch: exact match. |
| C4 | `_persist_bound_specs` L1245 swallows OSError/JSONDecodeError; `_warn_spec_degradation` L1264; message L1274 | PASS | sed 1245-1290: fail-soft pattern, `task_dir / "parsed-request.json"`, message at L1274. |
| C5 | SPECS objects carry `"path"` key (helper's `s["path"]` valid) | PASS | `_bind_specs` builds `{"path": str(p), ...}` (target L1228); helper filter `s.get("path")` consistent. |
| C6 | Test idioms exist: `_executor_with_specs`, `_write_parsed`, `capsys`+`_warn_spec_degradation`, `PrdConfig(task_dir=...)`, `spec_files` field | PASS | test_spec_flag.py L58-71, L161-165, L350-360, L370-389; models.py `spec_files` L183 + `task_dir` L187. All 3 test items reuse existing patterns. |
| C7 | All research line citations [CODE-VERIFIED]; none contradicted/unverified | PASS | research/01-findings.md: every Evidence bullet `[CODE-VERIFIED]`; rejected-alternative also CODE-VERIFIED. |

### D. Structural Gate Additions (TB-Add-1 … TB-Add-8)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| TB-Add-1 | Placeholder scan (no TBD/TODO/FIXME; no title-only items) | PASS | grep TBD/TODO/FIXME = NONE. Every item has full context+action+output+verification body. |
| TB-Add-2 | Item-count bounds (≥3, ≤50 single-track) | PASS (advisory) | 21 items, within advisory bounds. Check is ADVISORY pending calibration; non-blocking. |
| TB-Add-3 | Clarification adjacency | N/A | No blocked items; sole Open Question resolved upstream (not a blocker). Vacuously satisfied. |
| TB-Add-4 | Circular dependency detection (DAG) | PASS | Item refs form a DAG: 2.3/2.4→2.2; 3.x→2.x; 4.x/PG→earlier outputs. No back-edges. |
| TB-Add-5 | Granularity / XL splitting | PASS | No XL item; longest items (2.1, 2.2) embed one code block + single-method edit, justified inline. |
| TB-Add-6 | Verification/AC format consistency | PASS | All items use the uniform "ensuring … / If unable … log … then mark complete" shape across phases. |
| TB-Add-7 | Execution Context Source areas reappear in items | PASS | Header Source areas (L115): `_bind_specs` (10 hits), `_persist_bound_specs` (3), `_warn_spec_degradation` (4), scope-discovery/R5 gate (10), commands run/resume (10), test module (12). Consumer-side `grep` for `.py:NN` inside block L110-117 = 0. Block carries the reader-aid disclaimer (L112). |
| TB-Add-8 | Per-item Context evidence binding (file:line or evidence-absence) | PASS | Code-referencing items cite file:line: 2.1 (L1196/1209/1215/1216), 2.2 (L1245), 2.3 (`executor.py:645`), 2.4 (`executor.py:1274`). New-test items 3.1-3.3 cite the test module + research anchors; new functions legitimately have no source line yet — covered by "read module first to mirror idioms" context. |

## Summary

- Checks passed: 30 / 30 substantive (9 structural + 7 task-specific + 7 source-truth + 7 TB-Add; TB-Add-2 advisory-pass, TB-Add-3 N/A vacuous)
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (none required)

## Adversarial Notes (things specifically probed, found clean)

1. **Branch mismatch trap.** Current checkout is `feature/prd-spec-flag`; the test file does NOT exist there. Verified all anchors on `feature/prd-input-spec` (the task's target), where the file does exist (447 lines). The task's Step 1.2 correctly checks out the right branch before any edit — so the executor will not edit the wrong tree. Not a defect.
2. **Dedup insertion ambiguity.** research/01-findings.md Finding-1 code block re-prints the `spec_files = list(...)` + guard lines as leading context, which could tempt an executor to duplicate them. The TASK's Step 2.1 resolves this: its embedded block starts at the dedup comment (no guard lines) and the prose pins the anchor "immediately AFTER the empty-guard `return parsed` and BEFORE the `SPECS` array is built" (real gap between target L1211 and L1213). No duplication risk in the task.
3. **`_bind_specs({})` in Test 1.** With `spec_files=["foo.md","foo.md"]` the guard does not early-return; `parsed.get("WHERE") or []` = `[]` so the WHERE-idempotency assertion is well-defined. Achievable with `_executor_with_specs` + direct `_bind_specs({})` (existing idiom L161-174).
4. **commands.py named but never edited.** Header Source areas names "prd commands module (run vs resume config resolution)" but no item modifies commands.py — intentional (resolved design reads persisted SPECS). The area is referenced in item Context for orientation/rationale; TB-Add-7 satisfied. Not drift.
5. **Helper `s["path"]` vs `s.get("path")`.** Embedded helper uses `s["path"]` inside a comprehension already guarded by `isinstance(s, dict) and s.get("path")`, so the subscript is safe. SPECS objects always carry `"path"` (verified L1228). Defensive and correct.

## Confidence Gate

- **Confidence:** Verified: 30/30 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 3 | Grep: 0 (folded into Bash grep) | Glob: 0 | Bash: 7
  - Tool-engagement note: structural checks were executed via `git show | grep/sed` (Bash) against the target-branch blobs because the files do not exist on the working checkout — Read cannot reach a non-checked-out branch. Each Bash call mapped to a specific checklist item (anchor verification, placeholder scan, negative-constraint scan, source-area cross-validation). No padding calls.
  - No web research performed (all claims local/source-truth); tavily/web fallback counts: 0.

## Actions Taken

None — no issues found requiring fix. `fix_authorization: true` was available but unused.

## Recommendations

- Green light to proceed to execution. The task is well-formed, evidence-anchored to the correct branch, and the embedded code matches the verified source on `feature/prd-input-spec`.
- Minor non-blocking nicety (NOT a defect, do not gate on it): when executed, Step 2.1 should take care to insert only between the guard and the `specs` initialization; the task prose already states this, so no change needed.

## QA Complete

VERDICT: PASS
