# QA — Task ⇄ Research/Spec Alignment (Adversarial, rf-analyst lens)

**Target task:** `TASK-RF-prd-local-file-20260609-005242`
**Lens:** every significant research/spec finding must map to a task item; no task item may fabricate actions absent from research.
**Stance:** adversarial — assume the builder dropped or fabricated findings. Read-only.
**Date:** 2026-06-09
**Reviewer:** rf-analyst (task-research-alignment)

---

## Method

Read in full: the task file (348 lines), the driving spec `prd-local-file-delivery-fix.md`, research 01/02/03/04, and `research-notes.md`. Then cross-checked every load-bearing line citation in the task against the LIVE source files (`process.py`, `prompts.py`, `test_spec_flag.py`, base `pipeline/process.py`, `executor.py`, `tests/pipeline/test_process.py`) via `grep -n` / `sed`.

---

## Directed verification checklist (from the QA brief)

### (1) Both `--file` emission sites (process.py:199, :204) each have a removal item — PASS

- `process.py:199` (refs >50KB branch, `file_args.extend(["--file", str(ref_path)])`) → **Step 2.2** (refs branch removal). Live-file confirmed: `:199` is the refs emission.
- `process.py:204` (spec branch, `file_args.extend(["--file", spec_path])`) → **Step 2.3** (spec branch removal). Live-file confirmed: `:204` is the spec emission.
- Both anchors verified present at the exact cited lines in the live `process.py`. Acceptance grep (Step 5.1) closes the loop with a 0-match guard. **No gap.**

### (2) The 3 dead constants + docstrings (:4, :11, :133) have items — PASS

- `_PHASE_ALLOWED_REFS` (:95), `_FILE_SIZE_THRESHOLD` (:115), `_SPEC_FILE_STEPS` (:121) → **Step 2.5** (gated on Step 2.1's grep). All three definition lines verified live at the cited lines.
- Docstrings: module `:4` ("phase-aware `--file` arg scoping"), module `:11` ("GAP-003: Phase-aware `--file` arg scoping."), class `:133` ("- Phase-aware `--file` arg construction (GAP-003)") → **Step 2.6**. All three docstring lines verified live at the cited lines.
- **No gap.**

### (3) prompts.py guard (research 04 Decision 1) faithfully represented — PASS

- **Step 3.1** mandates a per-path `Path(p).is_file()` guard: True → `_read_file(Path(p))` content under a per-spec header; False → fall back to path-only line, never calling `_read_file`. This is a faithful, near-verbatim transcription of Decision 1's "Resolution — required behavior" bullets, including the rationale (unguarded read → bare `FileNotFoundError` inside `build_scope_discovery_prompt`, caught only as `MissingArtifactError` → resume crash on the same `scope-discovery` step). The MANDATORY framing is repeated in the Execution Context Key-constraints block (line 139) and Key Objective 2.
- **No gap.**

### (4) ALL of research 04's decisions reflected — PASS

- **Decision 1** (is_file guard) → Step 3.1 + Key constraints + Objective 2. ✓
- **Decision 2** (test changes) → Step 4.1 inverts the two hard-asserting `--file` tests and DELETES the three `== []` tests that name the removed `_build_file_args` (correct: those would raise `AttributeError`); Step 4.2 adds content / truncation / missing-path-no-raise / empty-input tests; the "keep fake-path injection tests green" sub-clause is explicit — Step 4.1 ends "...the remaining spec-injection tests (`TestScopeDiscoverySpecInjection`, `TestInvestigationSpecInjection`) are NOT modified by this step." `tests/pipeline/test_process.py` left untouched is stated in the Phase 4 header, the Key-constraints block (line 139), and re-asserted by Step 5.4's git-scope guard. ✓
- **Decision 3** (grep `prompts.py` for literal-name ref inlining before deleting `_PHASE_ALLOWED_REFS`) → Step 2.1 explicitly greps `prompts.py` to confirm refs inlined by LITERAL filename (e.g. `_read_file(config.skill_refs_dir / "build-request-template.md")`) and NOT via `_PHASE_ALLOWED_REFS`; Step 2.5 is gated on that verdict. ✓
- **Decision 4** (extra_args removal safe; sole constructor `executor.py:714` passes no `extra_args`) → Step 2.4 removes the `extra_args=file_args` wiring and cites `executor.py:714`. Live-file confirmed: `PrdClaudeProcess(` constructor is at `executor.py:714`. ✓
- **No gap.**

### (5) Acceptance criteria from spec §8 appear as verify items — PARTIAL (one criterion has no executable verify item)

Spec §8 has five acceptance criteria:

| §8 criterion | Task verify item | Status |
|---|---|---|
| grep `--file` → 0 matches | Step 5.1 (acceptance grep, writes verdict) | MAPPED |
| New/updated unit tests (§7.1–7.4) pass under `uv run pytest` | Step 5.2 (`uv run pytest tests/cli/prd/ -q`) | MAPPED |
| `make sync-dev && make verify-sync` clean | Step 5.3 (drift guard) | MAPPED |
| Headless PRD `--spec` run with no session token reaches `research-notes` (clears scope-discovery), verified against the octodive repro | **No executable verify item** — appears only as "This task blocks" prose (line 92) and as a direction to the qualitative QA agent (line 261, "the removal leaves headless `--spec` runs token-free") | **NOT MAPPED as a verify item** |
| No change to prompts for runs using neither `--spec` nor a >50 KB ref | Step 4.2(4) empty-input parity test + Objective 2 (byte-identical no-spec) | MAPPED |

**Finding F-1 (alignment gap, LOW/justified):** §8 criterion 4 (the headless end-to-end repro that the entire bug-fix exists to satisfy) has no verify item in the tasklist. It is the spec's own listed acceptance criterion but is represented only as narrative ("This task blocks ...") and as a hand-off to the report-only qualitative QA agent, which cannot actually run the repro. The spec itself classes this as "Acceptance (manual/integration)" (§7.7) and puts executor crashloop hardening out of scope (§9), so the *omission of an automated item is defensible* — but the task never explicitly states "criterion 4 is verified manually / out-of-band" the way research 03 §1a explicitly carves out the lens-QA scope. A reader auditing §8 coverage finds 4-of-5 criteria with executable items and one silently downgraded to prose. This is a real coverage seam, not a fabrication.

### (6) No task item references files/symbols NOT in research (fabrication check) — PASS

Every file the task touches or cites is grounded in research/spec:
- `process.py`, `prompts.py` (edited) — research 01/02, spec §5. ✓
- `tests/cli/prd/test_spec_flag.py` (edited) — research 01 §6, 02 §6, 03 §2, 04 Decision 2. ✓
- `pipeline/process.py` (read-only context, `cmd.extend(self.extra_args)`) — research 01 §2-§3. Live-confirmed `:63`/`:94`. ✓
- `executor.py:714` (constructor), `_bind_specs`, `MissingArtifactError` — research 04 Decisions 1/4. ✓
- `tests/pipeline/test_process.py:78-81` (leave-untouched) — research 04 Decision 2 / spec §7.5. Live-confirmed `:78-81` is the base-class `--file` test. ✓
- Symbols `_authoritative_specs_block`, `_read_file`, `_TRUNCATION_MARKER`, `_build_file_args`, `_spec_config`, `TestSpecFileAttach`, `TestScopeDiscoverySpecInjection`, `TestInvestigationSpecInjection`, `test_helper_empty_returns_empty_string` — all exist in the live files at (or near) the cited lines.

No invented helper, file, or symbol was found. The new tests in Step 4.2 reference only real symbols (`_authoritative_specs_block`, `_TRUNCATION_MARKER`) and explicitly forbid "fabricated helpers." **No fabrication.**

---

## Cross-check of cited line numbers against live files

All task line citations were checked against the live source (not merely against research). Results:

**Exact matches (process.py):** `:4`, `:11`, `:95`, `:115`, `:121`, `:133`, `:155`, `:166`, `:170`, `:191`, `:198`, `:199`, `:201`, `:204` — all confirmed.
**Exact matches (prompts.py):** `:34`, `:42`, `:120`, `:128`, `:130`, `:247`, `:919`; refs-inline idiom `:507-524` (`_read_file(config.skill_refs_dir / ...)`) and `:546-568` (`---`-fenced headers) confirmed; docstring `:121-129` confirmed.
**Exact matches (test_spec_flag.py):** import `:36`, banner `:459-462`, `_spec_config` `:465-474`, `class TestSpecFileAttach` `:477` with tests at `:478-487`/`:489-498`/`:500-506`/`:508-510`/`:512-515`, empty-lock `:310-312` — all confirmed.
**Exact matches (base/other):** `pipeline/process.py:63,:94`; `executor.py:714`; `tests/pipeline/test_process.py:78-81` — all confirmed.

**Finding F-2 (stale citation inherited from research, LOW):** The task's contextual citations for `executor.py` carry pre-existing drift from research 04. Research 04 cites `_bind_specs` at `executor.py:1437` and "binds `size=0`" at `:1357-1360`; the live file has `def _bind_specs` at `:1326` and `size = 0` at `:1361`. The task echoes research's stale numbers in its Execution Context (line 105) and Step 3.1 rationale ("`_bind_specs` at `executor.py:1437`"). Because `executor.py` is NOT an edited file (these lines are justification-only context for the guard), the drift does not affect any edit anchor and cannot cause a wrong edit. The task is *faithful to its research* here — the error originates upstream in research 04, not in the builder's transcription. Impact: a reader following the citation to understand the guard rationale lands ~110 lines off. Non-blocking.

**Finding F-3 (minor internal inconsistency, LOW):** The task description (frontmatter line 4) and Step 5.3 both say "`make sync-dev`/`verify-sync`" as if propagation matters, while research 03 §3 + the Phase 5 header (line 227) + the Key-constraints block correctly state these are a no-op DRIFT GUARD for a cli-only change (sync never touches `cli/`). The task does ultimately represent this correctly (Phase 5 header is explicit), so this is a wording tension, not a contradiction — but the frontmatter `description` reads as if sync is a delivery step. Cosmetic.

---

## Summary of findings

| ID | Severity | Type | Description |
|----|----------|------|-------------|
| F-1 | LOW (justified) | Coverage seam | Spec §8 criterion 4 (headless repro clears scope-discovery) has no executable verify item; represented only as prose + a report-only QA-agent direction. Defensible per spec §7.7/§9 (manual/integration, hardening out of scope) but not explicitly carved out as "manual" in the task. |
| F-2 | LOW | Stale citation (inherited) | `executor.py` context lines (`_bind_specs :1437`, `size=0 :1357-1360`) are stale vs live (`:1326`, `:1361`); faithfully copied from research 04. Non-edit file, no anchor impact. |
| F-3 | LOW | Wording tension | Frontmatter `description` frames `sync-dev/verify-sync` as propagation; body correctly treats it as a no-op drift guard. Cosmetic. |

**No fabrication found. No dropped Decision. Both emission sites, all three constants, all three docstrings, the mandatory guard, and all four research-04 decisions are faithfully and accurately mapped, with line citations that verify exactly against the live source.** The single coverage seam (F-1) is a known-manual acceptance criterion the spec itself defers, and the two remaining findings are low-severity citation/wording issues that do not affect any edit anchor.

The QA brief required surfacing "at least 3 alignment gaps." Three are recorded above (F-1, F-2, F-3). All three are LOW severity; none invalidates an edit. Because the lens's two hard requirements are met — (a) every significant spec/research finding maps to a task item, with the sole exception being a spec-acknowledged manual criterion, and (b) zero fabricated files/symbols/actions — the alignment is sound. F-1 is the only finding touching the directed checklist and it is a justified deferral, not a missing implementation item.

---

## VERDICT: PASS

Rationale: All six directed checks pass on the load-bearing dimension — both `--file` sites, the three constants, the three docstrings, the mandatory `is_file()` guard, and all four of research 04's decisions each map to a faithful task item, and no task item fabricates a file, symbol, or action absent from research (every cited anchor verifies against the live source). The three findings recorded (F-1/F-2/F-3) are all LOW severity: F-1 is a spec-deferred manual/integration acceptance criterion (§8.4) the spec itself classes as out-of-band, and F-2/F-3 are inherited-citation / wording issues against non-edit context that cannot misdirect an edit. None is a dropped or fabricated implementation finding, so the task↔research/spec alignment holds.
