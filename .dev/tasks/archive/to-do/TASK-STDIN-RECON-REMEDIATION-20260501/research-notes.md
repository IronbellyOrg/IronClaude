# Research Notes: stdin-patch adversarial-recon remediation (18 items)

**Date:** 2026-05-01
**Scenario:** A (Explicit) — user provided full BUILD_REQUEST with file paths, item structure, output shape
**Depth Tier:** Standard (5 researchers, 0 web — refactor-plan is canonical, work is verification + lift not exploration)
**Track Count:** 1 (single cohesive task file output covering 6 phases of remediation)
**Template:** 02 (Complex) — discovery → build → test → verify, multi-phase with conditional flows
**Task ID (user-specified):** `TASK-STDIN-RECON-REMEDIATION-20260501` (overrides default `TASK-RF-*`)
**Task folder:** `.dev/tasks/to-do/TASK-STDIN-RECON-REMEDIATION-20260501/`

---

## Note on Branch State

User's BUILD_REQUEST specifies `base_commit: fde1431`. Current HEAD is `2c21279`. The two commits between (`db8cffe`, `2c21279`) are docs-only (F-strict-review and adversarial-recon doc imports — no source changes). All cited source line numbers in the refactor plan are valid against current HEAD. Researchers SHOULD verify against current HEAD (`2c21279`) and note any drift in their findings.

---

## EXISTING_FILES

### Source files referenced by the 18 items (must verify line numbers against HEAD)
- `src/superclaude/cli/pipeline/process.py` — base ClaudeProcess class. Touched by P-009 (env-var helper at L27-29), P-011 (init `_stdin_error` in `__init__` around L56-90), P-012 (debug log at L181-186), T-012 (`n=0` capture at L216-218). Already 304 lines per prior review.
- `src/superclaude/cli/cli_portify/process.py` — PortifyProcess subclass. Referenced only by D-FOLLOW-006 (deferred). Mostly unchanged in current delta (P-001 already landed in `526a606`).
- `src/superclaude/cli/prd/process.py` — PrdClaudeProcess subclass. Touched by P-006 (4-line surfacing block at L277). Override of base `terminate()` at L239-279 per refactor plan.
- `tests/pipeline/test_process_stdin.py` — test file from prior delta. Touched by P-013 (replace conditional T-011 at L465-488 — but the actual T-011 lines may differ from the refactor plan's anchor since the file was extended in two test commits). T-013, T-014, T-015, T-016 append to this file.
- `tests/pipeline/test_prd_process_stdin.py` — NEW FILE for P-007 PRD regression test.
- `tests/pipeline/test_subclass_terminate_invariant.py` — NEW FILE for P-008 parametric subclass test.

### Spec/doc files referenced
- `.dev/architectural/claude-process-stdin-patch/RECONCILED_DESIGN.md` — original spec. P-010 amends §4 P-004 acceptance block. P-014 needs §3.2 SUPERSEDED list. P-015 needs §11 provenance map.
- `.dev/architectural/claude-process-stdin-patch/BEAT_2_BACKLOG.md` — NEW FILE for P-014 (15 deferred items + optional SUPERSEDED appendix).
- `.dev/architectural/claude-process-stdin-patch/TRACEABILITY.md` — NEW FILE for P-015 (commit→D-NNN map).

### Build files
- `Makefile` — append `ship-coder` target for P-016. Existing targets at `/config/workspace/IronClaude/Makefile`.

### Source documents (read-only research inputs — researchers MUST NOT modify)
- `.dev/architectural/claude-process-stdin-patch/adversarial-recon/adversarial/refactor-plan.md` — CANONICAL INPUT. Each P-NNN/T-NNN entry maps 1:1 to a B2 self-contained checklist item.
- `.dev/architectural/claude-process-stdin-patch/adversarial-recon/merged-output.md` — verdict document. Source for §5.3 D-FOLLOW table (Phase 5 GH issues).
- `.dev/architectural/claude-process-stdin-patch/RECONCILED_DESIGN.md` — original spec, source for §3.2 (BEAT_2_BACKLOG) and §11 (TRACEABILITY).
- `.dev/architectural/claude-process-stdin-patch/reconciliation/F-strict-review.md` — prior STRICT review, cross-reference for severity calibration notes.

---

## PATTERNS_AND_CONVENTIONS

### Code patterns the executor must respect (researchers must verify these are still current)
- Pipeline test fixtures pattern: `tests/pipeline/test_process_stdin.py` uses `_stdin_echo_argv()` helper + `patch.object(ClaudeProcess, "build_command", return_value=stand_in)` to inject Python stand-in subprocesses. New tests should follow the same shape.
- Logging pattern: `_log = logging.getLogger("superclaude.pipeline.process")` at module top. New log lines use `_log.warning(...)` / `_log.debug(...)`.
- Exception subclassing: `class PromptTooLargeForArgv(ValueError):` — backward compat with callers catching `ValueError`. Same pattern if any new exception classes are introduced.
- Defensive attribute access: `getattr(self, "_stdin_error", None)` is currently used in `terminate()` (asymmetric vs `wait()`'s direct access — this is exactly what P-011 fixes).
- F1-loop B2 self-contained items: each checklist item embeds context + action + output + verification + completion gate. No "see SKILL.md" references.

### Project conventions from CLAUDE.md
- UV-only Python: `uv run pytest`, `uv pip install`. Never bare `python -m` or `pip install`.
- Source of truth: `src/superclaude/`. Edits flow `src → make sync-dev → .claude/`. `.claude/` drift is acceptable for items missing in src (pre-existing per prior session).
- Branch policy: feature branches off integration; this delta lives on `fix/claude-process-stdin-large-prompts` off `feat/tdd-spec-merge`.
- Existing 64 sprint test failures (`tests/sprint/`) are pre-existing and out of scope per `git stash` test confirmed pre-delta.

---

## GAPS_AND_QUESTIONS

### Resolved by user-provided BUILD_REQUEST
- Item enumeration: refactor-plan.md has all 18 items with full metadata. Researcher just lifts them.
- Phase grouping: user explicitly specified Phases 1-6 mapping.
- Tracking artifact content sources: user pointed at RECONCILED_DESIGN.md §3.2 and §11 explicitly.
- Severity calibration: user asked to preserve refactor-plan.md labels but flag the over-calibration of A-FINDING-004/006/007 in `## Task Log / Notes`.

### Open during research
- Exact line numbers in `tests/pipeline/test_process_stdin.py` for T-011 BrokenPipe assertion — refactor-plan cites L465-488 but the file was extended after the original review. Researcher verifies against current HEAD.
- Existence of any pre-existing test files like `tests/pipeline/test_prd_process_stdin.py` or `tests/pipeline/test_subclass_terminate_invariant.py` — research must confirm these are NEW.
- PRD `terminate()` exact line range — refactor-plan cites L239-279; researcher verifies against current `prd/process.py`.
- Existing Makefile targets — need to confirm P-016's `ship-coder` doesn't conflict with anything existing.
- The 13 D-FOLLOW items in merged-output §5.3 vs the 12 in refactor-plan.md table — there's a discrepancy in count between the two documents (D-FOLLOW-001..D-FOLLOW-012 in refactor-plan but a 13-row table in merged-output §5.3). Researcher reconciles.

### Researcher MUST verify
- Every cited file:line anchor in refactor-plan.md is still valid at current HEAD.
- No NEW files (P-007, P-008 test files; BEAT_2_BACKLOG.md; TRACEABILITY.md) already exist (overwrite would be wrong).
- 4 acceptance criteria for `make verify-sync` are achievable given pre-existing rf-* / skill-creator drift (per prior session, drift is pre-existing — task constrains executor to NOT fix it).

---

## RECOMMENDED_OUTPUTS

### Researcher output files (all in `${TASK_DIR}research/`)
1. `01-source-code-verification.md` — all source line-number citations verified against HEAD = 2c21279
2. `02-test-infrastructure.md` — existing test patterns and fixture inventory for the 5 new tests
3. `03-refactor-plan-content-lift.md` — per-item metadata extraction (18 P-NNN/T-NNN items)
4. `04-doc-source-extraction.md` — content for BEAT_2_BACKLOG.md (§3.2), TRACEABILITY.md (§11), P-010 spec amendment text, D-FOLLOW table from merged-output §5.3
5. `05-mdtm-template-and-examples.md` — MDTM template 02 rules, recent task folder examples for B2 format reference

### Builder output
- Task file: `.dev/tasks/to-do/TASK-STDIN-RECON-REMEDIATION-20260501/TASK-STDIN-RECON-REMEDIATION-20260501.md`

---

## SUGGESTED_PHASES

### Researcher 1 — Source Code Verification (File Inventory + Doc Cross-Validator hybrid)
**Scope:**
- `/config/workspace/IronClaude/src/superclaude/cli/pipeline/process.py` (~304 LOC)
- `/config/workspace/IronClaude/src/superclaude/cli/prd/process.py` (verify L239-279 + L277 anchor)
- `/config/workspace/IronClaude/src/superclaude/cli/cli_portify/process.py` (sanity check; mostly unchanged)
**Focus:**
- Verify each line number anchor in refactor-plan.md against HEAD = 2c21279.
- For each P-NNN/T-NNN code item, capture the actual current line range and a short Before/After snippet excerpt.
- Flag any line drift in a "Drift Log" section.
- Confirm `_stdin_error` attribute is currently set in `start()` (and not in `__init__`) for P-011's "Before" state.
- Confirm `prompt_via=stdin` is NOT currently in the spawn debug log for P-012's "Before" state.
**Output:** `${TASK_DIR}research/01-source-code-verification.md`
**Other researchers covering:** R3 lifts metadata (severity, owner, risk, LOC), R2 covers tests, R4 covers spec docs.

### Researcher 2 — Test Infrastructure
**Scope:**
- `/config/workspace/IronClaude/tests/pipeline/test_process_stdin.py` (full file)
- `/config/workspace/IronClaude/tests/pipeline/conftest.py` (if exists)
- `/config/workspace/IronClaude/tests/pipeline/test_process.py` (existing baseline)
- `/config/workspace/IronClaude/pyproject.toml` (pytest config)
**Focus:**
- Extract the existing test patterns: `_stdin_echo_argv()` helper, `patch.object(...)` mocking style, `caplog` usage, `monkeypatch` patterns, `tmp_path` usage.
- Document fixtures available to new tests in test_prd_process_stdin.py and test_subclass_terminate_invariant.py.
- Verify these two test files do NOT yet exist (NEW FILE markers in refactor-plan).
- Confirm exact T-011 line range in current test_process_stdin.py for P-013's edit anchor.
- List existing test count / passing baseline (1294 from prior session).
**Output:** `${TASK_DIR}research/02-test-infrastructure.md`
**Other researchers covering:** R1 covers source code, R5 covers MDTM template patterns.

### Researcher 3 — Refactor-Plan Content Lift
**Scope:**
- `/config/workspace/IronClaude/.dev/architectural/claude-process-stdin-patch/adversarial-recon/adversarial/refactor-plan.md` (full file, 18 items)
**Focus:**
- For each of P-006 through P-016, T-012 through T-016: extract the full metadata table (Type / Target / Description / Provenance / Severity / Owner / Risk / Estimated lines) into a structured per-item record.
- For each code item, extract any "Before" and "After" code snippets cited in the refactor plan.
- For each test item, extract the assertion intent + mocking strategy + pass/fail criteria.
- Map each item to its phase grouping per user's BUILD_REQUEST (Phase 1 MUST: P-006/P-007/P-009; Phase 2 SHOULD: P-011/P-013/T-012/T-013/T-014; Phase 3 NICE: P-008/P-010/P-012; Phase 4 Tracking: P-014/P-015/P-016).
- Tag the 3 over-calibrated MEDIUMs (A-FINDING-004 → P-012, A-FINDING-006 → P-011, A-FINDING-007 → T-012) so the builder can flag them in `## Task Log / Notes`.
**Output:** `${TASK_DIR}research/03-refactor-plan-content-lift.md`
**Other researchers covering:** R1 verifies anchors, R4 covers cross-doc deferral artifact content.

### Researcher 4 — Doc Source Extraction
**Scope:**
- `/config/workspace/IronClaude/.dev/architectural/claude-process-stdin-patch/RECONCILED_DESIGN.md` (sections §3.2, §4 P-004, §11)
- `/config/workspace/IronClaude/.dev/architectural/claude-process-stdin-patch/adversarial-recon/merged-output.md` (§5.3 D-FOLLOW table)
- `/config/workspace/IronClaude/.dev/architectural/claude-process-stdin-patch/reconciliation/F-strict-review.md` (cross-reference)
- `git log --oneline 142ce15..HEAD` for TRACEABILITY commit list
**Focus:**
- Extract verbatim content of §3.2 SUPERSEDED list — count and list 12 items (per refactor-plan §"Changes NOT Being Made" D-FOLLOW-012 reference) or 15 items (per user's BUILD_REQUEST). Reconcile any count discrepancy and pick canonical list for P-014 BEAT_2_BACKLOG.md.
- Extract §4 P-004 acceptance block text — this becomes the "Before" content for P-010's amendment.
- Extract §11 provenance map for the seed of P-015 TRACEABILITY.md (then enrich with `git log` commit→file map for SHAs 526a606..fde1431).
- Extract the merged-output.md §5.3 13-row D-FOLLOW table with suggested issue titles + owners. This becomes Phase 5's checklist item content.
- Reconcile 12-vs-13 D-FOLLOW count between refactor-plan (D-FOLLOW-001..D-FOLLOW-012) and merged-output §5.3 (13-row table including W-M10 R-5 telemetry which refactor-plan tracks separately).
**Output:** `${TASK_DIR}research/04-doc-source-extraction.md`
**Other researchers covering:** R3 covers refactor-plan items themselves.

### Researcher 5 — MDTM Template & Recent Examples
**Scope:**
- `/config/workspace/IronClaude/.claude/templates/workflow/02_mdtm_template_complex_task.md` (PART 1 fully)
- `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-*` (recent examples — pick 1-2 for B2 format reference)
**Focus:**
- Document MDTM template 02 PART 1 rules: A3 (Complete Granular Breakdown), A4 (Iterative Process Structure), B2 (self-contained items), L1-L6 handoff patterns if applicable, completion gate format, anti-orphaning rule for final phase.
- Find a recent multi-phase task file (e.g., a recent TASK-RF-* with 4+ phases) to use as a B2 format reference. Note any patterns the builder should follow for: code-fix items, test-creation items, doc-creation items, verification-gate items.
- Document the frontmatter schema requirements, especially the `template_schema_doc` pointer and the `task_type: static` field.
**Output:** `${TASK_DIR}research/05-mdtm-template-and-examples.md`
**Other researchers covering:** R3 covers refactor-plan content.

---

## TEMPLATE_NOTES

- **Template selection:** 02 (Complex Task). Justification: 6 phases involving (a) discovery in Phase 0 (source verification), (b) implementation in Phases 1-3, (c) tracking artifact creation in Phase 4, (d) GH issue filing in Phase 5, (e) verification gate in Phase 6. Mixed activity types + sequential dependencies make this Complex.
- **Tier:** Standard (4-5 researchers, 0-1 web). 5 researchers chosen because: (1) source code spans 3 files, (2) test infrastructure has 1 existing file + 2 new files, (3) refactor-plan content is 18 items × 8 metadata fields = 144 data points to lift, (4) doc source extraction touches 4 source docs, (5) MDTM template is a separate verification surface. Web research not needed — refactor-plan is canonical and codebase-grounded.
- **MDTM features required in generated task file:**
  - Self-contained B2 items per A3/A4 rules (one item per P-NNN/T-NNN; no batches except Phase 5's 13-D-FOLLOW collapse, which is justified by user explicitly per BUILD_REQUEST).
  - Completion gate per item with measurable criteria.
  - Anti-orphaning: task-completion items must be inside Phase 6, not in a separate post-completion section.
  - Frontmatter must include user-specified fields: `id`, `title`, `status: 🟡 To Do`, `created_date: 2026-05-01`, `branch`, `base_commit`, `source_plan`.
- **QA_GATE_REQUIREMENTS:** PER_PHASE — given the safety-critical subsystem and the 1294/1294 pre-existing test baseline that must be preserved, each phase should have a "verify tests pass" gate before advancing. Phase 6 itself is the final integration verification.
- **VALIDATION_REQUIREMENTS:** "uv run pytest tests/pipeline tests/cli_portify -v passes; make sync-dev clean; make verify-sync ignores pre-existing rf-* / skill-creator drift; pipx install --force from local wheel succeeds; superclaude --version works."
- **TESTING_REQUIREMENTS:** UNIT (per-test pass/fail per item) + INTEGRATION (full pipeline + cli_portify suites at Phase 6). No E2E required — the 338 KB Coder roadmap repro is deferred to D-FOLLOW-001 (release-engineer post-merge).

---

## AMBIGUITIES_FOR_USER

1. **D-FOLLOW count: 12 vs 13.** Refactor-plan.md table has D-FOLLOW-001..D-FOLLOW-012. merged-output.md §5.3 lists 13 deferred items including a "W-M10 R-5 telemetry" row. Researcher 4 reconciles; if unresolved, the task file's Phase 5 will list 13 issues (the merged-output count) and reference both sources.
2. **P-013 line anchor drift.** Refactor-plan cites `tests/pipeline/test_process_stdin.py:465-488` for the T-011 conditional. The test file was extended in two test commits after T-011 was originally written. Researcher 2 will document the actual current T-011 line range and the task item will use that.
3. **Phase 5 atomicity.** User explicitly chose to collapse 13 D-FOLLOW items into ONE checklist item that opens 13 GH issues. This is a deliberate deviation from the "one P-NNN per item" rule. The task file will preserve this and document the rationale in `## Task Log / Notes`.

None of these are blockers. Proceeding with research.
