# Research Completeness Verification

**Topic:** Corrective MDTM task for sprint auto-resume reflection findings (F-3, F-2, F-4, CG-4)
**Date:** 2026-06-03
**Files analyzed:** 5 (research/01-drift-f3.md, 02-integrity-boundary-f2.md, 03-planner-commands-f4.md, 04-tests-coverage-gaps.md, 05-spec-cg4.md)
**Track goal:** Materialize a corrective MDTM task that fixes F-3 (HIGH regression-class drift gap), F-2 (partial-work paths not surfaced), F-4 (PHASE hard-crash skips prior-phase-tail validation), and resolves spec contradiction CG-4.

---

## Status: COMPLETE

All 5 assigned files read in full. Each was read end-to-end (no skimming): 01 (134 L), 02 (350 L), 03 (184 L), 04 (404 L), 05 (457 L).

---

## Criterion 1 — Source files identified with paths and exports? — PASS

Every named target is present with concrete file:line anchors and exported shapes.

| Required source | Covered by | Evidence |
|---|---|---|
| drift.py | 01 | full `DriftAssessor.assess()` control flow with per-branch line table (`drift.py:29-60`, branch table 32-187); `_current_task_ids` (209-216); `_annotate_git` (218-265); `_recorded_sha` (267-281) |
| integrity.py | 02 | `_detect_partial` (134-173), `_surface_partial` (197-208), `_verdict` (306-314), `_validate_last_completed` (86-130), caller (63-67) |
| models.py | 01, 02, 05 | `ResumePlan` (55-69), `BoundaryTask` (37-53), `BoundaryReport` full 6-field list (84-101), `Granularity` (29-34), `ResumeDecision` (104-118) |
| planner.py | 03 | `ResumePlanner.plan` (36-116), `_build_boundary` (120-169), hard-crash branch quoted (158-169), `_classify_phase`/`_find_interrupted` |
| commands.py | 02, 03 | `_print_resume_decision` quoted (498-536), call sites (293, 441), `assume_yes` wiring (265-269), gate call (400) |
| executor.py | 01 | `_write_phase_result_json` payload keys (2069-2078), `tasklist_sha256` at 2077 |
| test_resume.py | 04 | all 17 tests enumerated by class→name→line→assertion; builders `_build_task_interrupted` (175-216), `_build_gate_fixture` (433-472), `_P3` (220) |
| design.md | 05 | §7 (292-296), §4(a) (148-154), §4(b) (172-180), §4(c) (184-187), §2 dataclass (84-93) — all VERBATIM |
| merged-requirements.md | 05 | FR-2.1 (76-79), FR-2.4 (85-87), AC-3 (141-143) — all VERBATIM |

Supporting exports also located beyond the required list: `extract_checkpoint_paths` (`checkpoints.py:40-98`), `_declared_deliverables` (`rerun_tasks.py:924-948`), `_content_sha256_excluding_rerun_block` (`rerun_tasks.py:688-701`), `parse_tasklist_file` (`config.py:501-515`). No required source file is missing.

## Criterion 2 — Output paths and formats clear / inferable? — PASS

The corrective MDTM task's concrete deliverable surfaces are pinned in every research file:
- F-3: edit `drift.py:177-187` fall-through branch; principled variant also touches `executor.py:2069-2078` (persist `tasklist_sha256_ws`) + a reader in drift (01 §5).
- F-2: Option A adds `BoundaryReport.partial_paths: list[Path] = field(default_factory=list)` at `models.py:84-101`, set in `integrity.run()` at `integrity.py:64`; print site `commands.py:520-536` (02 §6, 03 §3.4, 05 §3d).
- F-4: append one `BoundaryTask(role="last_completed")` in planner (`planner.py:158-169` region) + a phase field on `BoundaryTask` + `_read_transcript` phase fix in integrity (03 §2, 02 §5).
- CG-4: decision record skeleton ready to fill (05 §5), with exact spec-edit line targets.
- Tests: CG-1/CG-2/CG-3 land in `tests/sprint/test_resume.py` with named test functions, class placement, and paste-ready bodies (04 §3-5).
The §2 amendment text for design.md is even pre-written (05 §3d). Formats are unambiguous.

## Criterion 3 — Logical breakdown of phases/steps present? — PASS

The work decomposes cleanly along the requested axes and the research supports each:
- CG-4 decision (must come first — it gates F-1 disposition and confirms F-2 Option A is in-scope): 05 §2 + §5.
- F-3 (drift): 01 with minimal vs principled fix paths.
- F-2 (partial paths): 02 §6 + 03 §3 + 05 §3.
- F-4 (prior-phase tail): 03 §2 + 02 §5 (co-dependency).
- Verification: 04 specifies CG-1/CG-2/CG-3 and the existing 17-test baseline (`17 passed in 0.20s`, verified this session).
Ordering dependencies are explicit (CG-2 depends on F-3 fix; CG-1 depends on F-2 option; CG-3 depends on F-4 fix).

## Criterion 4 — Patterns and conventions documented with examples? — PASS

- **pytest builders:** 04 §2 documents `_write_index`, `_complete_phase`, `_write_log`, `_task_block`, `_build_task_interrupted`, `_build_gate_fixture`, `_P3`, `PASS_TRANSCRIPT` with signatures and behavior. The AC-tagged docstring convention is captured (e.g. `"""AC-5: ..."""`) and the autouse `_stub_invoke_sonnet` fixture is noted so new tests inherit no-LLM behavior.
- **NFR-3 deterministic-core:** 01 §4 + §6 confirm `_annotate_git` never sets `confidence` (gate is pure Tier-0/Tier-1); 02 §4 confirms `_verdict` is `accept_suspect or validated_last` with coherence warnings explicitly excluded. The fix-placement constraint ("must not make the gate depend on git") is stated.
- **§2 field-exactness:** 05 §3a quotes the 6-field dataclass VERBATIM and 02 §6 / 05 §3d carry the exact one-field amendment. The models.py module docstring's "Field names/types follow design.md §2 verbatim" is cited.
- **UV-only:** 04 §6 gives all run commands as `uv run pytest ...` and explicitly notes "Per CLAUDE.md: UV only — never bare pytest / python -m," plus the benign `/lsiopy VIRTUAL_ENV` warning.

## Criterion 5 — MDTM template notes present with rule references? — PARTIAL PASS (acceptable)

The research files are research outputs, not the task file, so they do not contain MDTM frontmatter templates. However they DO supply everything the task-builder needs to author compliant items: per-fix file:line surfaces, paste-ready test code with node IDs, explicit AC/FR/INV linkage tags (AC-3/AC-4/AC-5, FR-2.2/FR-2.4, NFR-3, CG-1/2/3/4), and rule references (UV-only, no-writes invariant locked by `test_planner_performs_no_writes`, §2 field-exactness). This is the correct division of labor — MDTM template assembly is the builder's job, and the raw material for rule-referenced checklist items is complete. Not a blocking gap.

## Criterion 6 — Granularity sufficient for per-file/per-component checklist items? — PASS

Each fix and each new test is individually addressable:
- F-3: drift branch edit (item), executor WS-hash persist (item, principled variant), drift WS-hash reader (item).
- F-2: models field add (item), integrity.run assignment (item), commands print loop (item), design §2 amendment (item).
- F-4: planner emit (item), BoundaryTask phase field (item), integrity `_read_transcript` phase fix (item), no-writes test extension (item).
- CG-4: decision record (item), design.md §4(c)/§7 spec edits (item), §4(a)/AC-3 secondary (item).
- Tests: CG-1 (one item, two variants), CG-2 (one item), CG-3 (one item + negative companion).
Granularity is at or below the per-component level requested.

## Criterion 7 — Documentation cross-validation tags present? — PASS (exemplary)

Research 05 is the doc-sourced file and it tags EVERY spec claim. A tag legend is defined up front (lines 11-15). Verified tag assignments:

| Spec passage | Tag | Code anchor checked |
|---|---|---|
| design §7:293 (passed=True, quarantine opt-in) | [CODE-VERIFIED] | `integrity.py:314`, docstring 310-312 |
| design §4(c):186 (third conjunct) | [CODE-CONTRADICTED] | `integrity.py:314` omits the 2 conjuncts |
| FR-2.4(a) merged-req:85-87 | [CODE-CONTRADICTED] (cond (a) only) | `integrity.py:66-67` opt-in quarantine |
| FR-2.1 merged-req:76-79 | [CODE-VERIFIED] | `integrity.py:90-101` |
| design §2 dataclass:84-93 | [CODE-VERIFIED] | `models.py:84-101` (6 fields) |
| design §4(b):173 "(always)" | [CODE-CONTRADICTED] | `integrity.py:63-67` paths discarded |
| AC-3 merged-req:141-143 | [UNVERIFIED] (spec text) + [CODE-CONTRADICTED] tagged separately at §4c | `planner.py:158-169` + `integrity.py:97-101` |
| design §4(a):148-154 | [CODE-VERIFIED] (followed) | `planner.py:158-169` |

No doc-sourced architectural claim is left untagged. The two `[CODE-CONTRADICTED]` findings (§4(c) and §4(b)) are NOT reported as current fact — they are explicitly framed as the divergence the remediation must reconcile, surfaced into the CG-4 decision (§5) and the F-2 option analysis (§3). This satisfies the staleness-check requirement and the "contradicted claims must not be presented as fact" critical-flag rule. Files 01-04 cite code directly (no doc-sourced claims requiring tags), so the convention is correctly scoped to 05.

## Criterion 8 — Solution research evaluated approaches? — PASS

- **F-3 (01 §5):** two approaches contrasted with explicit tradeoffs — (a) **minimal** conservative <0.8 flip of `drift.py:177-187` (no schema change) and (b) **principled** WS-normalized hash `tasklist_sha256_ws` persisted in executor. The minimal option's AC-4 regression risk is identified and the principled option is shown to be the only way to deterministically separate AC-4 (cosmetic) from AC-5 (material) from persisted data. Backward-compat handling (missing key ⇒ conservative fallback) is specified. A third literal reading (checkpoint/deliverable diff per design §5) is evaluated and correctly rejected as not achievable as a true diff today.
- **F-2 (02 §6 + 05 §3):** Option A (BoundaryReport field) vs Option B (print-only) with pros/cons, type-match note (zero conversion), test-robustness argument, and a §4(b)-faithfulness analysis. Both files independently land on Option A with consistent reasoning; the §2-amendment cost is shown to already be in-scope.

## Criterion 9 — Critical cross-file dependencies surfaced and consistent? — PASS

This is the highest-risk criterion. All three named cross-file dependencies are surfaced, captured as real requirements, and NOT contradictory across files.

### 9a. F-3 data-availability blocker vs CG-2 test consistency — CONSISTENT

- Research 01 (§3, §5, Summary) states unambiguously: **no per-task content baseline exists in result.json** — only per-task status + whole-file `tasklist_sha256` (`executor.py:2069-2078`); `BoundaryTask`/`ResumePlan` carry no baseline; `extract_checkpoint_paths`/`_declared_deliverables` parse only the CURRENT file. This is labeled the "data-availability blocker" and forces either a conservative <0.8 default or a persisted WS-hash.
- Research 04's CG-2 spec (§3) asserts `confidence < 0.8` + `cosmetic_only is False` for a same-ID material edit, using `_build_task_interrupted(..., record_hash=True, recorded_body=_P3)` to fabricate a Tier-0 hash MISS, then a same-ID body/deliverable edit. **This test is consistent with BOTH F-3 fix variants:** the conservative minimal fix and the principled WS-hash fix both yield <0.8 for a *material* (non-whitespace) same-ID edit. 04 explicitly states the test is "RED today (gets 0.9), green after researcher-01's F-3 fix" and confirms via `rerun_tasks.py:688-701` that the hash-strip excludes only the RERUN block (so a deliverable/body edit reliably misses Tier 0). No inconsistency: 04 does not assume a specific variant, and the assertion holds under either.
- **One nuance correctly handled:** 04 §3 notes that if a pure-prose variant is preferred over the deliverable variant, the `_task_block` helper needs an inline body — this is flagged, not skipped.

### 9b. F-4 co-dependency (planner fix alone insufficient; BoundaryTask phase field needed) — SURFACED, CONSISTENT, AND CG-3 MARKED UNVERIFIED

- Research 03 (§2.2 "Important scoping nuance", §5) explicitly flags that integrity's `_validate_last_completed`/`_read_transcript` key the transcript on `plan.interrupted_phase` (`integrity.py:112-114`), which is the WRONG phase for a prior-phase tail, so **"the planner fix ALONE is insufficient"** and a `BoundaryTask` phase field (or plan-level prior-phase number) is required. Marked `[->r02]` co-dependency.
- Research 02 (§5) independently corroborates from the integrity side: the gate "has no input that points it at the prior phase" and "Any F-4 fix that wants the prior tail validated must either have the planner inject a synthetic last_completed BoundaryTask for the prior phase, or add a prior-phase validation entry point." The two files agree on the requirement; neither contradicts the other on ownership (03 owns planner emit, 02 owns the model/`_read_transcript` change).
- Research 04 (§5) marks the CG-3 assertion target appropriately: the role name and the source the fix reads P2's tail from (transcript vs result.json) are explicitly **"Unverified which source the fix reads P2's tail from"**, with `_complete_phase` writing `task_results: []` flagged as a possible issue for researcher-03. The CG-3 test is written against `role=="last_completed"` + `task_id=="T02.01"` as the default with a documented swap-if-different instruction. This is the correct "documented ambiguity, not silently skipped" handling.

### 9c. F-2 option consistency across files — CONSISTENT (all settle on Option A)

- Research 02 (§6, Summary): lead recommendation Option A (`BoundaryReport.partial_paths: list[Path] = field(default_factory=list)`), with §2 amendment owned by researcher-05.
- Research 05 (§3c, §3d, Summary): "Option A ... is decisively MORE faithful to §4(b)"; supplies the exact §2 amendment field text.
- Research 03 (§3.4): owns the print site (`commands.py:520-536`), and route 1 (preferred) is the `BoundaryReport.partial_paths` field — explicitly defers the model change to researcher-02.
- Research 04 (§4): writes CG-1 in BOTH variants (A = field assertion, B = printed-output assertion) and explicitly states the task picks one after F-2 is decided, preferring Variant A.
**No two files assume different options as settled.** 03 and 02/05 converge on Option A; 04 keeps both variants but defers the choice rather than presupposing it. The print-site owner (03) and the model owner (02) are non-overlapping. This is internally consistent.

---

## Completeness check (per-file)

| File | Status | Summary/§ | Gaps surfaced | Key Takeaways | Rating |
|---|---|---|---|---|---|
| 01-drift-f3 | Complete | Yes (Summary) | Yes (data-availability blocker, AC-4 vs AC-5 tension) | Yes | Complete |
| 02-integrity-boundary-f2 | Complete | Yes (Summary + handoff) | Yes (F-4 integrity co-dep, F-1×F-2 interaction) | Yes | Complete |
| 03-planner-commands-f4 | Complete | Yes (Summary) | Yes (co-dep flag, F-1 --yes bypass) | Yes | Complete |
| 04-tests-coverage-gaps | Complete | Yes (Summary) | Yes (CG-3 source Unverified, Variant B caveat) | Yes | Complete |
| 05-spec-cg4 | Complete | Yes (Summary) | Yes (secondary §4(a)/AC-3 gap, NO-leaning counter-evidence) | Yes | Complete |

All five carry Status: Complete and a Date of 2026-06-03. None is In Progress.

## Cross-reference check — PASS

Handoff ownership is explicit and non-conflicting throughout: 02 §4/§6 hands the print surface and prompt semantics to 03; 03 hands the model field and `_read_transcript` fix to 02; both hand the §2 amendment and CG-4 ruling to 05; 04 consumes all of the above for the three test specs. Every `[->r02]`/`[->r03]`/`[->r05]` cross-reference resolves to a real, reciprocated claim in the target file.

## Contradictions Found — NONE

No cross-file contradiction detected. The three high-risk seams (F-3 fix variant vs CG-2 test, F-4 co-dependency, F-2 option) are all consistent (Criterion 9). The only divergences are *intentional open decisions* (CG-4 YES/NO ruling; F-3 minimal vs principled; F-2 Option A vs B), and each is presented AS an open decision with a recommended default — not as conflicting settled facts.

## Compiled Gaps

### Critical Gaps (block synthesis) — NONE

### Important Gaps (carry into the task as explicit decision/dependency items)
These are correctly surfaced by the research (not analyst-discovered omissions); listed so the builder makes them first-class task items rather than burying them:
1. **CG-4 ruling is an operator decision** the task cannot self-resolve — must be a gating decision-record item (05 §5). It determines whether F-1 closes as-designed and whether F-2 is promoted to mandatory.
2. **F-3 fix-variant selection** (minimal conservative <0.8 vs principled WS-hash) must be an explicit decision item — the minimal variant regresses AC-4 unless the WS-hash is added (01 §5). The task should not leave this implicit.
3. **F-4 is a two-file change, not one** — the planner emit is insufficient without the `BoundaryTask` phase field + `_read_transcript` phase fix (03 §2.2, 02 §5). Both must be sibling items with an ordering/blocking link.
4. **CG-3 assertion source is Unverified** — whether the F-4 fix reads P2's tail from transcript or result.json is open (04 §5); `_complete_phase` writing `task_results: []` may require the test fixture to add a real P2 entry. Carry as a test-construction caveat.

### Minor Gaps (must still be addressed)
5. **F-2 Variant B `--dry-run` caveat** — 04 §4 flags that `--dry-run` may return before the gate runs (`commands.py:399-404`), so a print-based CG-1 test must use the `--yes` path. Only relevant if Option B is chosen; Variant A sidesteps it.
6. **No-writes test extension** — 03 §2.3 recommends extending `test_planner_performs_no_writes` to also snapshot the tasklist dir (currently only `results/`) to lock the new prior-phase read as read-only. Should be an explicit test item.

## Depth Assessment

**Expected depth:** Deep (corrective remediation requiring data-flow traces, integration-point mapping, and cross-file dependency analysis).
**Actual depth achieved:** Deep — exceeds tier. Evidence: full control-flow traces of `assess()` and `_build_boundary`; data-availability trace proving the absence of a per-task baseline (01 §3); the F-4 transcript-keying co-dependency caught at `integrity.py:112-114` (a non-obvious integration bug that a shallow pass would miss); VERBATIM spec quotes with per-line code cross-validation (05); paste-ready test bodies reusing existing builders (04). The research verified the baseline test suite actually runs (`17 passed in 0.20s`).
**Missing depth elements:** None.

---

## Recommendations

1. Build the task with CG-4 as the FIRST item (a decision record) — its ruling gates F-1 disposition and confirms F-2 Option A scope.
2. Make F-3 fix-variant a recorded decision; if the minimal variant is chosen, pair it with the WS-hash schema change or accept the AC-4 caveat explicitly.
3. Model F-4 as ≥3 linked items (planner emit, BoundaryTask phase field, integrity `_read_transcript` fix) with blocking dependencies, not a single planner item.
4. Author CG-1 with Variant A (deterministic field assertion) as the default and keep Variant B only as a fallback tied to the F-2 option ruling.
5. Carry the CG-3 "Unverified source" caveat and the no-writes test extension as explicit test items.

---

## VERDICT: PASS

All 9 requested criteria PASS (Criterion 5 is a PARTIAL PASS that is acceptable — MDTM template assembly is correctly the builder's job, and the rule-referenced raw material is complete). No critical gaps, no cross-file contradictions. The three high-risk cross-file dependencies (F-3 blocker↔CG-2, F-4 co-dependency↔CG-3-Unverified, F-2 Option A across 02/03/05) are all surfaced and mutually consistent. The four "Important Gaps" are open decisions the research correctly flagged for the task to own as first-class items — they do not block synthesis. Research is ready to proceed to task materialization.
