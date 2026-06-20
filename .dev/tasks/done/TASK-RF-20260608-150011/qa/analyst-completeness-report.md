# Research Completeness Verification

**Topic:** task-builder — fix sprint recovery stranded-deliverables + stale-checkpoint defects (single track)
**Date:** 2026-06-08
**Files analyzed:** 4 (01-fix-site-signatures.md, 02-test-fixtures.md, 03-checkpoint-gate-plumbing.md, 04-template-and-conventions.md)
**Depth tier:** Deep (file:line evidence, design-fork resolution, data-flow tracing expected)
**Analyst:** rf-analyst (sole instance — no partition; all 4 assigned files in scope)

---

## Verdict: PASS

All 9 spawn-prompt criteria are satisfied with evidence-based, file:line-grounded research. No critical or important gaps block task-file construction. Minor observations are recorded below as advisories for the builder, not blockers.

---

## Per-Criterion Findings

### Criterion 1 — Source files identified with paths and exports (4 fix-site functions, exact signatures + insertion anchors): PASS

File 01 captures all four fix-site functions with exact current signatures and line ranges:

| Function | File:line | Signature captured | Insertion anchor |
|----------|-----------|--------------------|------------------|
| `merge_recovery_bundle` | recovery.py:381-386 | full (incl. `*, release_dir: Optional[Path]=None`) | new step inserts at recovery.py:501→502 (blank after Step-3 loop end :500, before Step-4 comment :502); renumber Steps 4-7 if claiming "Step 4" |
| merge site in `run_rerun_tasks` | rerun_tasks.py:1451-1486 | RecoveryBundle construction (:1451-1459) + merge call (:1484-1486) | call to update for `expected_deliverables` kwarg; `phase_obj.file`+`resolved` in scope |
| `recover_missing_checkpoints` | checkpoints.py:213-219 | full (incl. `*, return_bundle: bool=False`) | Defect-2 short-circuit at checkpoints.py:249-260 (before `continue`) |
| `verify_checkpoints` CLI | commands.py:647-663 | full decorators+signature | new `@click.option` after :656; thread kwarg at call :693 |

Supporting exports are also pinned: `write_recovery_audit_log` (recovery.py:250), `finalize_checkboxes_on_success` (rerun_tasks.py:888-890), `_declared_deliverables` full body (rerun_tasks.py:954-978), `_render_recovered_checkpoint` (checkpoints.py:398-403), and supporting regexes. Dataclasses `RecoveryBundle` (recovery.py:76-114), `RecoveryStatus` (recovery.py:58-68), `CheckpointEntry` (models.py:485-514) all enumerated field-by-field with required-vs-defaulted noted. The 7 merge-step boundaries are individually line-anchored (recovery.py:433/459/481/502/525/576/601). Strong evidence quality — no unsupported architectural claims.

### Criterion 2 — Output paths/formats clear (which file each fix lands in; where 2 tests go): PASS

Fix landing sites are explicit:
- Fix 1 (stranded deliverables): new merge step in recovery.py (insert :501→502), plus the `produced` glob root cause identified at rerun_tasks.py:1444-1446 ("never globs bundle-root deliverable trees `artifacts/`, `evidence/`"), plus the thread-in point at the merge call rerun_tasks.py:1484-1486.
- Fix 2 (stale checkpoint): primary = re-run checkpoint T-ID task; fallback re-stamp branch at checkpoints.py:249-260; CLI flag at commands.py:652-662 + call :693.

Test landing sites (File 02): Test A → `tests/sprint/test_recovery.py::TestMergeRecoveryBundle` (class at line 153, reusing `_seed_release` lines 28-48 / `_bundle_with_sidecar` lines 51-79). Test B → `tests/sprint/test_checkpoints.py::TestRecoverMissingCheckpoints` (class at line 407, modeled on `test_does_not_overwrite_pre_existing_file` line 454). Audit-log JSONL format and assertion idiom captured verbatim. Recovered-report frontmatter format (`checkpoint:/phase:/recovered: true/generated_at:`, verdict as `## Result` body token) fully specified.

### Criterion 3 — Logical breakdown of phases/steps (sequence Fix 1 → Test A → Fix 2 → Test B → validation): PASS

File 04 §1e + Summary item 2 prescribe the "Build → Test → Fix" phase shape (Template :828-829) with concrete sequencing: Phase 1 builds both defect fixes (one item each with `file.py:NN` Context), Phase 2 adds both regression tests (one item each), a mandatory I18+L3 testing item runs `uv run pytest tests/sprint/test_recovery.py tests/sprint/test_checkpoints.py -v` plus `make lint`/`make format`. The Fix-1-before-Fix-2 ordering and the test-after-fix ordering are derivable; the 7-step merge sequence in File 01 lets the builder place the new step precisely. Sufficient to sequence the requested Fix 1 → Test A → Fix 2 → Test B → validation flow.

### Criterion 4 — Patterns/conventions documented with examples (atomic write, failures→status, fixture shapes, UV/lint/branch rules): PASS

All requested patterns are present with concrete examples:
- **Atomic write idiom**: File 01 §1 quotes the `.tmp` + `tmp.replace()` idiom verbatim (recovery.py:519-521, repeated :667-669), and explicitly flags that NO recursive tree-copy helper exists (`shutil` function-local at :413) — a load-bearing caveat for a Fix-1 that must copy deliverable *trees*.
- **failures→status mechanism**: File 01 documents that `failures.append(...)` is the ONLY mechanism downgrading status to PARTIAL (flip at recovery.py:674), with all existing append sites enumerated, plus the surfacing into the audit-log event. The recommended new failure string `deliverable-not-landed:{task_id}:{rel}` is given.
- **`.failed-<ts>` clobber-preserve idiom**: captured at recovery.py:444-449/466-471/487-492 with `orig_ts = int(canonical.stat().st_mtime)`.
- **Fixture shapes**: File 02 quotes `_seed_release`, `_bundle_with_sidecar`, `_seed_sprint`, `_full_recovery_manifest` in FULL BODY, with return-tuple shapes, sidecar JSON shapes, and the `release_dir == tmp_path` convention. The sidecar `status` string inconsistency (`"pass"` vs `"passed"` across helpers) is explicitly flagged.
- **UV/lint/branch rules**: File 04 §3 documents UV-only (`uv run pytest`, `make lint`, `make format`), the NO-`make sync-dev`-for-CLI-`.py` rule (with rationale: sync gate is for skills/agents/commands only), feature-branch-only (current `fix/prd-document-capture-hotfix` is unrelated — new branch required), and the never-stage-`.claude/` rule (task touches none).

### Criterion 5 — MDTM template notes with rule references (template 02, 5-field item form, anti-orphaning, POST reflect item): PASS

File 04 is comprehensive on template/rule references:
- **Template 02 structure**: PART 1 (orchestrator-only, :51-867) vs PART 2 (output, :876+) distinction made; the SKILL.md PART-2 skeleton (`SKILL.md:1951-2019`) identified as the simpler shape actually emitted.
- **5-field item form**: the `Context / Action / Output / Verification / Completion gate` schema quoted (`SKILL.md:1980-1985`) with the validation criterion (`SKILL.md:2030`) and the B2 6→5 mapping rationale.
- **Anti-orphaning**: Template C4/I13 + `SKILL.md:2040` cited; completion items live inside final phase, worked-example placement shown.
- **POST reflect item**: the verbatim `N.{X-1}` templated item quoted (`SKILL.md:1994-1999`), trigger (`POST_REFLECT_GATE: ENABLED`, `SKILL.md:2108`), penultimate-position validation criterion (`SKILL.md:2051`), frontmatter sentinel (`reflect_post: ""`, `SKILL.md:1942`), and the final Update-status-to-Done item (`SKILL.md:2001-2006`). MALFORMED-on-omission rule captured.

### Criterion 6 — Granularity sufficient for per-file/per-component checklist items: PASS

File 04 §1d (Rule A3) + Summary item 1 explicitly translate the granularity rule to THIS task: "one item per defect fix (per modified function/file), one item per added regression test, separate items for the pytest run and the lint/format run. No 'fix both defects' mega-item." Combined with File 01's per-function line anchors and File 02's per-test fixture mappings, the builder has enough to author atomic, per-component items. The worked-example item shapes (File 04 §2a: "Modify function X", "Add test to class Z", "Lint/pytest validation") give copy-ready templates.

### Criterion 7 — Doc/code cross-validation: are claims file:line evidence-based?: PASS

Every load-bearing claim across all 4 files is anchored to `file:line` read directly on branch `fix/prd-document-capture-hotfix`, 2026-06-08 (File 01 header line 8 states this explicitly). Spot-validation of representative claims against the actual files:
- File 01's claim that `_declared_deliverables` has 0 hits in recovery.py is presented as a verified `grep` result (line 150) with the cycle-direction rationale (recovery imported BY rerun_tasks at rerun_tasks.py:49) — a genuine cross-validation, not an assertion.
- File 03's PRIMARY-feasibility verdict is backed by a real generated tasklist (`/config/workspace/TUIBBS-scp/.dev/releases/current/v1-MVP/tasklists/phase-12-tasklist.md`) with quoted line numbers (783/802/816-819/822), cross-checked against both parser patterns (`TASK_BLOCK_PATTERN` rerun_tasks.py:61-63; `CHECKPOINT_HEADING_PATTERN` checkpoints.py:34-37). This is true doc-vs-code triangulation.
- `_check_checkpoint_pass` is quoted verbatim (executor.py:2510-2521) and its consumer traced to `_determine_phase_status` (executor.py:2788). No doc-sourced claim appears without a code anchor; no `[UNVERIFIED]`/`[CODE-CONTRADICTED]` tags were needed because the research reads code directly rather than relying on documentation. Evidence quality: Strong across all four files.

### Criterion 8 — Design-fork resolution (Fix-2 primary-vs-fallback resolved with evidence; is end-of-phase checkpoint a runnable task?): PASS

This is the highest-risk criterion and File 03 resolves it decisively and up-front:
- **VERDICT (File 03 lines 11-13):** "PRIMARY (re-run the gated checkpoint TASK after a successful merge) IS FEASIBLE in this codebase."
- **Evidence the end-of-phase checkpoint is a RUNNABLE TASK (File 03 §3):** `### T12.17 -- Checkpoint: End of Phase 12` carries a T-ID heading, an executable `**Steps:**` block ending in "Write the checkpoint report", and a `**Checkpoint Report Path:**` resolving to `CP-P12-END.md`. It matches `TASK_BLOCK_PATTERN` (rerun_tasks.py:61-63), so `rerun-tasks` can select it by heading. Re-running it produces a real `status: PASS` verdict that `_check_checkpoint_pass` reads.
- **Fallback retained with justification (File 03 lines 32, 139-145, 153):** re-stamp stale FAIL/BLOCKED → UNKNOWN is required as a guard for tasklists lacking a runnable end-of-phase checkpoint task, and is net-new (recover only writes on MISSING files, checkpoints.py:248-264; never overwrites/auto-PASSes). The reusable asset (the `_render_recovered_checkpoint` UNKNOWN/`recovered: true` shape, checkpoints.py:398-439) is identified.
- **Discovery hook for the checkpoint T-ID** is provided (scan for `### T<PP>.<NN> -- Checkpoint:` whose path resolves to `CP-P{phase:02d}-END.md`). The fork is resolved with primary + guarded fallback, both evidence-backed.

### Criterion 9 — Unresolved ambiguities documented (e.g. path asymmetry config.release_dir vs index_path.parent): PASS

File 03 explicitly surfaces the path asymmetry rather than glossing it:
- §4 "Canonical release dir confirmation" + Summary "Path-asymmetry watch-out" (File 03 lines 134-137, 156): `_check_checkpoint_pass` derives the checkpoint from `config.release_dir / "checkpoints"` (executor.py:2512-2514), whereas the verify-checkpoints recover subprocess operates on `config.index_path.parent` (= OUTPUT_DIR positional, rerun_tasks.py:1526). It states these coincide in the flat layout but DIFFER in the `sc:tasklist` subdir layout, and instructs: "The builder should pin the write target explicitly rather than assume equality."
- File 01 §1 surfaces a related TASKLIST_ROOT subtlety: `release_dir` is resolved via `_resolve_release_dir(source_index)`, NOT a naive `source_index.parent` (TASKLIST_ROOT = `release_dir/tasklists` in the sc:tasklist layout). This pre-empts a likely builder mis-assumption.
- File 02 flags the sidecar `status` string inconsistency (`"pass"` vs `"passed"`) and the absence of a `_full_recovery_manifest` helper in test_recovery.py. Ambiguities are documented, not silently resolved.

---

## Coverage Audit

| Scope Item (track goal) | Covered By | Status |
|-------------------------|------------|--------|
| recovery.py fix site | File 01 §1 (merge_recovery_bundle, insert anchor :501→502) | COVERED |
| rerun_tasks.py fix site | File 01 §2 (produced glob :1444-1446, merge call :1484-1486) | COVERED |
| checkpoints.py fix site | File 01 §3 + File 03 §4 (short-circuit :249-260, render :398-439) | COVERED |
| commands.py fix site | File 01 §4 (verify_checkpoints CLI :647-702) | COVERED |
| tests/sprint/test_recovery.py | File 02 §1 (fixtures + TestMergeRecoveryBundle) | COVERED |
| tests/sprint/test_checkpoints.py | File 02 §2 (fixtures + TestRecoverMissingCheckpoints) | COVERED |
| Diagnosis REPORT.md anchors | Files 01/02/03 cross-reference REPORT line cites throughout | COVERED |
| Design fork (Fix-2 primary/fallback) | File 03 (feasibility verdict + fallback) | COVERED |
| Template-02 + builder conventions | File 04 (all sections) | COVERED |

Every track-goal source file and the requested decision points are covered. No scope gaps.

## Evidence Quality

| Research File | Evidence basis | Unsupported claims | Quality Rating |
|---------------|----------------|--------------------|----------------|
| 01-fix-site-signatures.md | file:line throughout; verbatim code blocks; grep result cited | 0 | Strong |
| 02-test-fixtures.md | FULL-BODY fixture quotes + line ranges | 0 | Strong |
| 03-checkpoint-gate-plumbing.md | file:line + real generated-tasklist evidence + dual-parser cross-check | 0 | Strong |
| 04-template-and-conventions.md | template:line + SKILL.md:line + worked-example:line + CLAUDE.md cites | 0 | Strong |

## Documentation Staleness

No doc-sourced architectural claim is presented as current fact without a code anchor. The research reads code directly. File 04 cites CLAUDE.md rules (UV-only, branch policy, `.claude/` staging), which are governance docs (not stale-able architecture claims) and are correctly applied. No `[CODE-CONTRADICTED]` claims. No staleness flags required.

## Completeness

| Research File | Status | Summary | Gaps Section | Key Takeaways | Rating |
|---------------|--------|---------|--------------|---------------|--------|
| 01-fix-site-signatures.md | Complete | Y (§"Summary of load-bearing anchors") | partial (caveats embedded inline, e.g. no tree-copy helper, cycle direction) | Y | Complete |
| 02-test-fixtures.md | Complete | Y ("Summary for the builder") | partial (inconsistencies flagged inline) | Y | Complete |
| 03-checkpoint-gate-plumbing.md | Complete | Y ("Summary for the builder") | Y (stale-FAIL gap, path-asymmetry, gate-mode-orthogonal explicitly called out) | Y | Complete |
| 04-template-and-conventions.md | Complete | Y ("Summary for the builder") | partial (omitted-section rationale embedded) | Y | Complete |

All four marked Status: Complete with a builder-facing Summary. Gaps/caveats are surfaced inline and in summaries rather than under a literal "Gaps and Questions" heading — acceptable for this research style; no missing-finding gap results.

## Contradictions Found

None across the four files. Cross-file consistency is in fact reinforced:
- The `recover_missing_checkpoints` short-circuit at checkpoints.py:248-264 is described identically in File 01 §3, File 02 §2.5/§4, and File 03 §4.
- The UNKNOWN-not-PASS hard constraint (checkpoints.py:435-438) is stated consistently in Files 01, 02, and 03.
- The path-asymmetry / `release_dir` vs `index_path.parent` distinction in File 03 is consistent with File 01's `_resolve_release_dir` note (both reject the naive `source_index.parent` assumption).

## Compiled Gaps

### Critical Gaps (block synthesis/build)
None.

### Important Gaps (affect quality)
None.

### Minor Gaps / Advisories (builder should carry forward, not blockers)
- **Sidecar status-string inconsistency** (`"pass"` in `_bundle_with_sidecar` vs `"passed"` in `_full_recovery_manifest`) — File 02 already flags it; builder must match whichever helper the new test reuses. Source: File 02 §1.3, §2.4, Summary.
- **Path-target pinning for Fix-2** — `config.release_dir` vs `config.index_path.parent` coincide in flat layout but differ in sc:tasklist subdir layout; the regenerated/re-stamped `CP-Pxx-END.md` must land where `_check_checkpoint_pass` reads. Builder must pin explicitly. Source: File 03 §4, Summary.
- **No recursive tree-copy helper in recovery.py** — Fix-1 copying deliverable *trees* (`artifacts/`, `evidence/`) has no existing precedent; only single-file `shutil.copy2` exists. Builder must introduce tree-copy carefully (and add a failures-append on non-landing). Source: File 01 §1.
- **Defect-2 reads verdict from `## Result` body, not frontmatter** — `CheckpointEntry` has no verdict field and recovered reports carry no `status:` key; a Fix-2 re-stamp must parse the body token. A reusable verdict regex exists at summarizer.py:69 (`PASS|FAIL|...|BLOCKED|SKIP`). Source: File 01 §5, File 02 §4.

## Depth Assessment

**Expected depth:** Deep — exact signatures, insertion anchors, data-flow tracing, design-fork resolution.
**Actual depth achieved:** Deep. Verbatim signature/body quotes, individually line-anchored 7-step merge sequence, full-body fixture quotes, data-flow trace from rerun Step-14 → verify-checkpoints CLI → `recover_missing_checkpoints`, and an evidence-backed primary-vs-fallback feasibility verdict using a real generated tasklist. Dual-parser cross-validation (selection pattern + checkpoint-heading pattern) exceeds Standard tier.
**Missing depth elements:** None material.

## Recommendations

1. Proceed to task-file construction — research is build-ready; no gap-fill round required.
2. Builder should carry the 4 minor advisories above into the relevant items' Context/Verification fields (especially the path-target pinning for Fix-2 and the no-tree-copy-helper caveat for Fix-1).
3. Emit Fix-2 as PRIMARY (re-run end-of-phase checkpoint T-ID) WITH the guarded FALLBACK (re-stamp stale → UNKNOWN) per File 03's resolved fork — do not collapse to fallback-only.
4. Ensure the new Fix-1 merge step appends a `deliverable-not-landed:...` failure string so a stranded deliverable downgrades status to PARTIAL (the only status-downgrade mechanism, recovery.py:674).

---

## VERDICT: PASS

All 9 criteria PASS. 0 critical gaps, 0 important gaps, 4 minor advisories (already surfaced by the research itself). Research is complete, evidence-based, internally consistent, and build-ready for task-file construction.
