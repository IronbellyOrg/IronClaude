# Research Notes: Auto-Resume as Default for Sprint Pipeline (v4.3.5)

**Date:** 2026-06-02
**Scenario:** A (Explicit) — authoritative, code-grounded design.md + merged-requirements.md provided
**Depth Tier:** Standard (single subsystem: src/superclaude/cli/sprint/; 3 new modules + 1 write-path change + CLI wiring + tests)
**Track Count:** 1 (sequential phasing P1→P5; later phases depend on earlier — single cohesive output)
**Build mode:** INLINE single-threaded (agent context cannot spawn nested sub-agents; design.md serves as the verified research corpus and was independently re-verified against the worktree this session).

---

## EXISTING_FILES

All paths under `src/superclaude/cli/sprint/` (re-verified 2026-06-02 this session):

- `commands.py` (17.9 KB) — CLI entrypoints. `run()` at L190 (does NOT take `@click.pass_context` — DD-5 requires adding it); `--start`/`start_phase` default=1 at L76-80; `--end`/`end_phase` default=0; `rerun_tasks()` at L485. **[CODE-VERIFIED]**
- `config.py` (19 KB) — `discover_phases()` L58; `_resolve_release_dir()` L242 (deterministic from index_path, no lock — concurrency caveat §12). **[CODE-VERIFIED]**
- `executor.py` (87 KB) — `_write_phase_result_json()` at L2053; atomic tmp+rename at L2070-2072 (`tmp.replace(out)`); payload dict L2059-2067 (keys: phase, status, exit_code, started_at, finished_at, task_results, recovery_history). Executor loop / `active_phases`. **[CODE-VERIFIED]**
- `logging_.py` (10.7 KB) — `write_phase_start()` L59 (event `phase_start`); `write_phase_interrupt()` L71 (balances start); `write_phase_complete()` L94. Append is non-atomic/non-durable (no fsync/rename) → last line may tear on hard crash (DD-1 rationale). **[CODE-VERIFIED]**
- `rerun_tasks.py` (61 KB) — `_classify_transcript()` L550; `discover_failed_tasks_from_transcripts()` L601; `_content_sha256_excluding_rerun_block()` L688 (used both sides of drift via L1306 source_sha, L1387 current_sha); `_declared_deliverables()` L924; `stash_and_restore_deliverables()` L961; `restore_from_bundle()` L1039. **[CODE-VERIFIED]**
- `recovery.py` (27 KB) — `RecoveryStatus` L58; `RecoveryBundle` L77 with `source_tasklist_sha256` field L111; `write_recovery_audit_log()` L250; `.recovery-locks/phase-{phase}.lock` lock helper L278/L291. **[CODE-VERIFIED]**
- `checkpoints.py` (15.9 KB) — checkpoint/deliverable existence verification logic (reused by integrity gate). **[CODE-VERIFIED present]**
- `models.py` (35 KB) — `execution-log.jsonl` at release root (:543); `results/` (:539); `phase_result_json` path (:570); task transcripts (:561-565); `TaskStatus` (:45-52); `PhaseStatus` (:270); `active_phases` (:550). **[CODE-VERIFIED present; line numbers from design, not independently re-paginated this session]**
- `summarizer.py` (24 KB) — advisory Haiku agent surface (:305). **[CODE-VERIFIED present]**

**Net-new (do not exist yet — confirmed absent this session):** `src/superclaude/cli/sprint/resume/` directory and its four modules (`planner.py`, `integrity.py`, `drift.py`, `models.py`).

**Version anchor:** `pyproject.toml` `version = "4.2.0"`. Design targets **v4.3.5**. The git history shows v4.3.0 rerun-tasks work already merged (commits a77f5fdf..344a754a) but pyproject was not bumped. ⚠️ See AMBIGUITIES_FOR_USER — the version bump target needs confirmation; tasklist treats the changelog/version note as P5 doc work, not a blocker.

## PATTERNS_AND_CONVENTIONS

- **Atomic writes:** tmp+rename convention (`out.with_suffix(".json.tmp")`; `tmp.replace(out)`) — executor.py:2070-2072 and checkpoints.py. New `tasklist_sha256` field must ride the SAME atomic writer (no separate write).
- **Non-destructive recovery:** `preserved/` + `manifest.json` bundle shape; `restore_from_bundle()` reverses it; `write_recovery_audit_log()` appends JSON-line audit events; `.recovery-locks/phase-{phase}.lock` acquired before results/ mutation. The feature REUSES these — no new restore verb.
- **Click options:** `@sprint_group.command()` + `@click.option(...)` decorators; params bound by name. DD-5 mandates `ctx.get_parameter_source(name) == ParameterSource.COMMANDLINE` for explicit-flag detection (requires `@click.pass_context` on `run()`), NOT value comparison.
- **Dataclasses + Enum** for structured results (mirrors existing `RecoveryBundle`, `TaskStatus`, `PhaseStatus`).
- **LLM isolation (NFR-3):** any LLM step (Haiku coherence read, drift explainer) is advisory; deterministic core never depends on it; CI without `claude` behaves identically (empty-verdict path).
- **Python env:** UV only (`uv run pytest`); tests under `tests/`; `make sync-dev` / `make verify-sync` for component sync (N/A here — this is CLI source, not skills/agents).

## GAPS_AND_QUESTIONS

- Exact insertion point inside `_write_phase_result_json` payload for `tasklist_sha256` — design says extend dict L2059-2067; builder encodes it as a discrete sub-item. Resolved: append one key computed via `_content_sha256_excluding_rerun_block(phase_obj.file)`.
- `models.py` line numbers (539/543/570/561-565/550) are from design.md and were verified as "file present" but not re-paginated symbol-by-symbol this session. Tasklist items instruct the executor to locate symbols by name (grep) rather than trusting line numbers — robust to drift.
- Version bump (4.2.0 → 4.3.5) handling — see AMBIGUITIES_FOR_USER.

## RECOMMENDED_OUTPUTS

Single MDTM task file encoding §10 phasing P1–P5 as phases, AC-1..AC-9 + INV-001 + DD-1..DD-5 invariants as verification clauses and a dedicated test phase. Template 02 (complex: discovery + build + test + docs, conditional LLM-capability branches).

## SUGGESTED_PHASES

Mirror design §10 exactly:
- Phase 1: `resume/models.py` dataclasses + `ResumePlanner` (read-only) + the ONE write-path change (`tasklist_sha256` in `_write_phase_result_json`, backward-compatible).
- Phase 2: `DriftAssessor` (deterministic tiers 0/1; git tier behind capability check; INV-001 same-fn-same-file).
- Phase 3: `BoundaryIntegrityGate` (doubly-validate last; report-only default + opt-in copy quarantine; advisory Haiku TASK-only; `.recovery-locks`).
- Phase 4: CLI wiring in `run()` + `rerun_tasks()`; `--fresh`/`--restart`, `--yes`, `--dry-run`; Click parameter-source detection.
- Phase 5: tests (§9 table, AC-1..AC-9 + advisory-only + non-destructive) + docs/changelog (R5 behavior-change note) + version bump note.

## TEMPLATE_NOTES

Template **02** (complex). Tier **Standard**. Use A3/A4 granular per-component items; B2 self-contained 5-field items (Context/Action/Output/Verification/Completion gate). Encode AC mapping in test-phase items. Phase dependencies are strictly sequential (P1 unblocks all; P4 depends on P1-P3; P5 depends on P4).

## AMBIGUITIES_FOR_USER

1. **Version bump target.** `pyproject.toml` is at 4.2.0 while design targets v4.3.5 and v4.3.0 rerun-tasks code is already merged without a pyproject bump. The tasklist includes a P5 item to (a) add the changelog entry and (b) bump the version, but the exact target string (4.3.5 vs catching up intermediate bumps) should be operator-confirmed. Not a code blocker — treated as documentation/release hygiene.
2. **`--yes` env var name.** Design suggests `SUPERCLAUDE_SPRINT_ASSUME_YES=1` as an example; the canonical name is the team's call. Tasklist uses the design's suggested name and flags it as confirmable.
