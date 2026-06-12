# Changelog

All notable changes to IronClaude are documented in this file.

## [Unreleased]

### reflect — D13 coverage hardening: inference-assisted extraction + parse-density guard (contract 1.5.0)

#### Added (reflect skill)

- Two-pass requirement extraction (`sc-reflect-protocol` SKILL.md Step 1B.0): Pass 1 stays deterministic/LLM-free (regex ID extraction + range-notation expansion, e.g. `SPEC-001..021` → 21 IDs); Pass 2 reads the full spec body and enumerates requirement-shaped content Pass 1 missed, emitting synthetic `INF-NNN` rows that each MUST carry a verbatim quote + `file:line` citation (an inferred row missing either is dropped at emission and never enters the matrix).
- Parse-density guard (Step 1B.2b): when `inferred_count > parsed_count` (sparse labeling relative to requirement content), emits `coverage_degraded: parsed-sparse` and forbids the Tier-1 stop — a table-wide §5.3 pre-filter routing to Tier 2 (explicit `--tier 1` / `--depth quick` pins still override, with a loud WARN).
- Wave-5 evidence-validator now polices inferred rows identically: an `INF-NNN` row whose quote does not match its cited spec lines is dropped, counted in `citations_dropped`, and `coverage_pct_union` / `unmapped_requirements_union` / `S_dev_density` are recomputed over the surviving union before the report finalizes.

#### Changed (reflect skill)

- Return contract bumped **`1.4.0 → 1.5.0`** (§9.4 additive-only): NEW fields `coverage_pct_union`, `unmapped_requirements_union`, `coverage_degraded`. `coverage_pct` and `unmapped_requirements` KEEP pre-D13 parsed-only semantics, so existing consumers need no change (major-only CLI validator tolerates the minor bump).

### reflect — audit-only wrapper → bounded auto-fix engine (contract 1.4.0)

#### Added (reflect CLI)

- `--fix/--no-fix` flag on `superclaude reflect run` (Click default **`--no-fix`**, i.e. audit-only; the O1/O2 gate callers pass `--fix` explicitly — "gate default --fix" refers to the gate-invocation convention, not the bare-CLI default). When `--fix`, the audit runs with `--remediate` so reflect *authors* (never runs) a Tier-3 corrective MDTM file; on an AUTO-FIXABLE verdict with a present `remediation_task_path`, the wrapper auto-executes `/task <path>` as its own top-level `claude --print` subprocess, then re-runs the audit to verify. Reflect stays read-only; the wrapper is the sole mutator-orchestrator.
- `--max-fix-iterations N` flag (default **2**): bounds the audit→apply→re-verify loop. After N apply→verify cycles without convergence to PASS, terminal HALT (exit 10), no promote; the sidecar records `fix_iterations` and `fix_converged: bool`.
- `--base <ref>` flag (highest precedence). Resolution chain in `config.py`: **explicit `--base` > frontmatter `start_commit` > `git merge-base HEAD master`**. A phase-N gate passes `--base <phase-N-start-sha>` to audit only phase-N work. The F3 de-range is preserved: `--diff <BASE>` is a SINGLE ref vs the working tree, never a `<BASE>..HEAD` commit range.
- `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` recursion breaker: the wrapper exports `=1` into every child it spawns inside the fix subtree (the reflect audit subprocess AND every auto-run `/task`). The primary breaker lives in the `reflect` **group callback**, which runs during Click parsing — so a nested `superclaude reflect run` immediately **exits 0** ("nested gate suppressed") BEFORE the `run` subcommand's `exists=True` tasklist-arg validation, even when the file has since moved. Truthiness is exactly the string `"1"`.
- Pure `classify_fix` carve-out (`contract.py`) off existing contract fields only: **AUTO-FIXABLE** ⇔ HALTED caused solely by `drift>0` and/or `necessary`-class items with no `regression_present`, `needs_human_decision`, `user_decision_required`, or grounding-gaps; **HUMAN-REQUIRED** ⇔ any of those triggers (or a `degraded`/`blocked` verdict). Auto-fix applies to the AUTO-FIXABLE path only.
- `remediation_task_path` contract field — reflect's Wave 6 emits the absolute path of the MDTM file `rf-task-builder` wrote (null when none authored) into `return-contract.yaml`; the wrapper reads it to auto-execute rather than guessing the newest `TASK-RF-*` dir. Skill `sc-reflect-protocol` contract bumped **`1.3.0 → 1.4.0`**.
- Headless `--remediate` auto-authoring: under `--print` (wrapper) mode there is no human to "accept" a Tier-3 offer, so `--remediate` authors the corrective file non-interactively and sets `remediation_task_path`. A HUMAN-REQUIRED deviation set still authors nothing auto-runnable (BUILD_REQUEST with `needs_human_decision: true`) and the wrapper HALTs.

#### Changed (reflect CLI)

- `--promote/--no-promote` default flipped **`False → True`** (FR-5): promote-by-default. The wrapper never force-sets `--no-promote` — it has no O2-detection surface, so the **generator** passes `--no-promote` explicitly on its O2 per-phase gate calls; a defaulted O2 promote is a harmless no-op (reflect's Wave-7 finds no per-phase adapter and safely skips `adapter-unresolved`), never a mis-promote.
- `_build_inner_command` now forwards `--promote/--no-promote` **and** `--base` explicitly under `--tmux`, so a `--tmux + --no-promote` (or `--tmux + --base`) outer call does not silently default to promote-on or lose the base ref in the inner foreground reinvocation.

#### Guarantees (reflect CLI)

- Fail-closed: DEGRADED and BLOCKED verdicts are never auto-fixed; a failed `/task` apply HALTs (never silently passes); thinness holds (no `cli.sprint`/`cli.roadmap` import, no `async`, `ClaudeProcess`-only launch). Test suite: **75 passed / 1 justified xfail**.

### Sprint CLI — wire the per-task execution path + runner-owned typed handoff (Stages 0-3, TASK-RF-SPRINTCLI-WIRE-DEAD-20260603-024610)

#### Added (sprint CLI)

- `--handoff/--no-handoff` flag on `superclaude sprint run` (default: **enabled**). When enabled, the per-task execution path writes one typed `HandoffRecord` JSON per task and a `task_complete` ledger event; `--no-handoff` reproduces legacy behavior exactly (no handoff records, no `task_complete` events). Threaded through all three layers (`commands.py` click option → `load_sprint_config` → `SprintConfig.handoff_enabled`).
- `--resume <task_id>` flag on `superclaude sprint run`: resumes a per-task sprint by skipping *validated-successful* tasks (handoff record with `status == "pass"` AND a successful gate outcome). The argument is a `T<PP>.<TT>` task id; it composes with the phase-granular `--start/--end` (those bound the phase range, the validated-success skip suppresses already-done tasks within it). Resuming against a pre-Stage-1 `release_dir` (no `handoff/` directory) degrades gracefully to phase-granular behavior. Non-success tasks (`FAIL_*`/`INCOMPLETE`/`SKIPPED`, PASS-with-gate-fail) are never skipped.
- `handoff/` results subdirectory: per-task handoff records are persisted to `<results_dir>/handoff/phase-{N}-task-{task_id}.json` (phase-qualified key, since the bare `T<PP>.<TT>` id is not sprint-unique). Written via an atomic temp+replace `FileHandoffStore` (`src/superclaude/cli/sprint/handoff.py`).
- `task_complete` execution-log JSONL event — the first-run sibling of `task_rerun_complete`, with the identical field set `{event, phase, task_id, status, turns, duration_sec, timestamp}` (discriminator: `task_complete` = first run, `task_rerun_complete` = rerun).
- Typed, schema-versioned `HandoffRecord` dataclass (`models.py`) constructed by the runner from each finalized `TaskResult` plus `produced_artifacts[]`/`consumed_upstreams[]`; forward-compatible (`from_dict` tolerates unknown keys).
- `--task-parallelism K` flag on `superclaude sprint run` (default: **1 = sequential**). `K > 1` executes up to `K` tasks concurrently per dependency wave (topological order built on the existing `rerun_tasks` dependency-edge shape; cycles surfaced, not dropped). Concurrency is made safe by a lock-guarded `SprintLogger._jsonl`, a lock-guarded `TurnLedger` with an atomic `try_launch` (prevents budget over-commit), and per-task atomic handoff-file writes. `K = 1` preserves byte-identical legacy behavior.

#### Changed (sprint CLI)

- Per-task subprocesses now receive full per-task isolation env (own `CLAUDE_SETTINGS_DIR`/`CLAUDE_PLUGIN_DIR` under `<results_dir>/.isolation`), and the per-phase fallback path additionally seeds the two settings/plugin keys while keeping its phase-scoped `CLAUDE_WORK_DIR`.
- Per-task `turns_consumed` is now parsed from the stream-json terminal `result` event's `num_turns` (previously hard-coded `0`).
- Prior-task context (`build_task_context`) is now injected into each per-task prompt.
- The per-task heading router emits a warn-only near-miss diagnostic when a phase file has headings that look like `### T<PP>.<TT>` but miss the strict format (it never reclassifies the phase).

### sprint — auto-resume as the default for `run` / `rerun-tasks` (v4.3.5, TASK-RF-20260602-sprint-auto-resume)

#### Behavior change (READ THIS if you script `superclaude sprint`)

- **`superclaude sprint run <index>` with no `--start/--end` now AUTO-RESUMES.** An interrupted sprint is detected from on-disk state (the atomic `phase-N-result.json` is the truth anchor) and resumes at the boundary phase, re-running only the unfinished task on the task-level path. Before proceeding it prints the resume plan + drift + integrity report and (interactively) asks for confirmation.
- **`superclaude sprint rerun-tasks <index>` with no `--phase/--tasks/--from-reflect-report` now AUTO-DETECTS** the boundary phase and its recoverable failed-task set, then runs exactly as if those flags had been supplied (identical result to the explicit invocation).
- **Opt-out / explicit control is unchanged.** An explicit `--start`/`--end` (run) or `--phase`/`--tasks` (rerun-tasks) — *including `--start 1`* — disables auto-detection and preserves today's exact behavior (detected via Click parameter source, not value comparison). `--fresh` (alias `--restart`) ignores prior on-disk state and runs clean from phase 1.
- **CI / non-interactive:** pass `--yes` (or set `SUPERCLAUDE_SPRINT_ASSUME_YES=1` / `CI=1`) to skip the confirmation prompt. A non-interactive session without assent stops with guidance rather than hanging.

#### Added (sprint auto-resume)

- New read-first package `src/superclaude/cli/sprint/resume/`:
  - `planner.py` (`ResumePlanner`) — pure-read reconstruction of the resume plan from `execution-log.jsonl` + `phase-N-result.json` + transcripts. `result.json` presence with a PASS-family status is the authoritative phase-completion signal (a torn/dropped ledger line cannot demote it). Flags ambiguous state (multiple plausible release dirs / interleaved ledger / unreadable core files) and refuses to auto-pick.
  - `drift.py` (`DriftAssessor`) — tiered safety-of-resume scoring. Tier 0 exact normalized-content hash match; Tier 1 whitespace-insensitive cosmetic + structural task-ID diff (only the 0.8 confidence boundary gates resume); Tier 2 additive `git diff` annotation behind a capability check.
  - `integrity.py` (`BoundaryIntegrityGate`) — the resume-seam safety gate. Doubly-validates the last-completed task (persisted status ∧ transcript re-derivation ∧ artifact existence), surfaces next-unfinished partial work, and offers opt-in reversible copy-to-quarantine. The gate verdict is a pure function of deterministic signals; an advisory coherence read can annotate but never change it.
  - `models.py` — `ResumePlan`, `BoundaryReport`, `DriftAssessment`, `BoundaryTask`, `Granularity`, `ResumeDecision`.
- `--fresh` / `--restart`, `--yes` / `-y` flags on both `sprint run` and `sprint rerun-tasks`.
- `phase-N-result.json` now records `tasklist_sha256` (normalized-content hash of the per-phase tasklist) so a later resume can detect drift. Backward-compatible: result files written before v4.3.5 simply lack the key and resume falls back to structural drift scoring.

#### Safety properties

- **Non-destructive by default (NFR-1):** the integrity gate performs zero `results/` mutation unless cleanup is opted into; quarantine is a `shutil.copy2` (originals untouched), lock-guarded, audit-logged, and reversible by the existing `rerun-tasks --restore` (`restore_from_bundle`).
- **LLM is advisory-only (NFR-3):** the coherence read is CI-safe (empty verdict when `claude` is absent/times out) and can never flip the gate verdict.

#### Validated (sprint auto-resume)

- 17 deterministic unit/integration tests (`tests/sprint/test_resume.py`) mapping 1:1 to AC-1..AC-9 + the validator-corrected invariants (INV-001 same-fn hash, FR-2.5 non-destructive/reversible quarantine, DD-2 advisory-only coherence) + a mutation-proved hard-STOP guard.
- 3 real-`claude`-subprocess e2e tests (`tests/sprint/e2e_real/test_e2e_resume.py`) proving bare `rerun-tasks` auto-detect, bare `sprint run` task-level auto-resume, and hard-crash phase-level re-run end-to-end.
- Five in-band phase-gate `rf-qa` reviews (adversarial, fix-authorized) + Phase-4 caught a runtime-only dispatch defect (missing `run_rerun_tasks` kwargs) that mocked tests had hidden.

### sc:cleanup-audit — bake hidden + BMAD scope exclusions into defaults (TASK-RF-20260529-162751)

#### Added (sc:cleanup-audit)

- `DEFAULT_EXCLUDES` regex floor in `src/superclaude/skills/sc-cleanup-audit-protocol/scripts/repo-inventory.sh`: hidden paths (any leading-`.` or `/.` segment), BMAD directories (`_bmad/`, `_bmad-output/`, `_planning-input/`), and audit output (`.claude-audit/`). Applied to BOTH the `git ls-files` branch and the `find` fallback branch via a shared `apply_scope()` filter — every downstream artifact (type distribution, domain classification, batch assignments, summary) inherits the filter automatically.
- Per-project override mechanism: `.claude-audit/SCOPE.md` lines of the form `EXCLUDE: <regex>` are added to the exclusion set. Default exclusions cannot be removed — they are a floor, not a ceiling. Override file path is configurable via `SCOPE_FILE` env var.
- `=== ACTIVE SCOPE RULES ===` diagnostic block emitted at the top of `repo-inventory.sh` output so operators can see what was excluded without re-deriving the regex.
- "Default scope exclusions" paragraph under the Discover step + "Scope Floor" Key Patterns bullet in `src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md` documenting the new floor + per-project override semantics.
- "Scope rule (inherited from `repo-inventory.sh`)" defense-in-depth section in `rules/pass{1,2,3}-*.md` so audit-scanner / audit-analyzer / audit-comparator subagents don't classify out-of-scope paths even if a leaked path appears in a grep result.
- `In-scope after default excludes:` line in the `## Repository Context` block of `src/superclaude/commands/cleanup-audit.md` (alongside the renamed `Total tracked files:`) using the same regex byte-for-byte. **Three-site lockstep** between `scripts/repo-inventory.sh:20`, `commands/cleanup-audit.md:16`, and `SKILL.md:38` — any future regex change must update all three.

#### Changed (sc:cleanup-audit)

- `commands/cleanup-audit.md` Repository Context: `Total files:` relabeled to `Total tracked files:` (clearer, since `git ls-files` only lists tracked files).
- `templates/pass-summary.md` Coverage Metrics "Exclusions applied" item now enumerates the three exclusion layers (Default / Find-fallback / Project) separately so generated reports are accurate post-default-excludes.
- `templates/final-report.md` Exclusions block updated analogously.

#### Validated

- TUIBBS smoke (post-edit): `Total files: 389` matches `progress.json:current_scope.in_scope_paths` from the 2026-05-29 TUIBBS audit (the manually-derived in-scope count) — defaults reproduce the prior hand-authored scope with zero per-project setup.
- 0 hidden/BMAD paths leak into any batch assignment.
- Per-project override fixture (`EXCLUDE: ^vendor/`) tightens scope correctly (3 files → 2 files).
- `sh -n` clean on `repo-inventory.sh`; POSIX-sh compatibility preserved.
- 7 in-band QA reports (5 phase-gate `rf-qa` + post-completion `rf-qa` structural + `rf-qa-qualitative` operational, all PASS-after-fixes) + post-execution `/sc:reflect --mode post` (T1, calibrated 0.88, 0 regressions, 5 deviations classified under §10 taxonomy).

### cliEval — Phase 5+6 remediation (TASK-RF-20260522-153212)

#### Added (cliEval)

- `src/superclaude/cli/eval/exit_codes.py` with exactly 4 canonical exit codes (`SUCCESS=0`, `FAILURES=1`, `USAGE_ERROR=2`, `INTERRUPTED=3`). All 11 `*_EXIT_CODE` constants in the eval module re-export from here via top-of-file `from . import exit_codes as _exit_codes` + local `NAME: int = _exit_codes.VALUE` assignments (CC2 / OQ-2).
- `orchestrator.allocate_session_id(*, run_id, eval_id)` helper — the canonical session-id allocator; `commands.py::_run_one_spec` now threads `run_id` through and calls the helper instead of constructing `f"sess-{spec.id}"` ad-hoc (M5).
- `eval doctor --output-dir` Click option now carries `file_okay=False`, symmetric with `eval run --output-dir` (M6).
- Stderr WARNING emitted at the `_NullLifecycleExecutor` call site on every `eval run` until the production executor lands (M2 / CC3): `eval run: WARNING: _NullLifecycleExecutor active — non-production executor selected; run results MUST NOT be treated as authoritative.`
- User-facing operator guide at `docs/user-guide/eval-pipeline.md` covering all four subcommands, exit codes, output layout, and the AC12 scratch-root policy.

#### Changed (cliEval)

- `eval run --output-dir <X>` is now the OUTPUT ROOT: artifacts land at `<X>/.dev/eval-runs/<YYYY-MM-DD>/<run-id>/` (anchored via `compose_run_dir`) instead of a flat layout under `<X>` (H1 / FR-G4).
- `_format_run_summary_line` renders the full DM-012 taxonomy `P/F/S/E/I/T` (passed/failed/skipped/errored/interrupted/timeout) instead of eliding `ERRORED`/`INTERRUPTED`/`TIMEOUT` (H3).
- FR-G5 coverage gate now fails closed (`CoverageResult(passed=False, parse_error=...)`) on corrupt `~/.claude/settings.json` instead of silently passing (H2).
- `resolve_scratch_root("/tmp/eval-runs")` (bare allowlist prefix with no sub-path) now raises `ScratchRootViolation`; only strict sub-paths are accepted (H4 / AC12). Closes the AC12 tautology where the check would silently accept the prefix as a "match" of itself.
- Runtime allowlist extension now happens **before** any `mkdir(parents=True)` at both `commands.py::eval_run` and `isolation.py::HomeIsolation.setup` call sites (H5a, H5b / OPS-002 / NFR-SEC2). No filesystem write before allowlist validation.
- `EVAL_ID_PATTERN` (the FR-SCH2 schema regex) is now the single source of truth in `artifact_layout.py`; `loader.EVAL_ID_REGEX` is preserved as an import alias for backward-compat. The previously-private `_EVAL_ID_RE` (the path-safety regex) was renamed to `_EVAL_ID_PATH_SAFETY_PATTERN` to disambiguate the defense-in-depth layers (CC1 / OQ-1).
- Both `Reporter.write` and `write_aggregated_report` now emit `summary.yaml` alongside `summary.md` / `summary.json` via the shared `_write_artifact_set` helper (M4 — closes the previous +1 yaml divergence between the two writers).
- `RunTotals` keys derived from `EVAL_STATUSES` partitions in `models.py` (no hardcoded literals). New module-level constants: `PASSED_STATUSES`, `FAILED_STATUSES`, `SKIPPED_STATUSES` (M3).

#### Fixed (cliEval)

- The previously-blocking `NameError: '_new_run_id' is not defined` from `eval run` was already closed at PR #66 (`dce3c3cb`); the Phase 5+6 remediation confirmed the helpers (`_new_run_id` at `commands.py:1326`, `_default_output_dir` at `:1339`) are present and layered the canonical exit-code module, `orchestrator.allocate_session_id`, and the FR-G4 `compose_run_dir` anchoring on top. **B1 follow-up resolved.**
- Documentation drift across `docs/eval/{validation-commands,release-checklist,retention,runtime,retry,scratch-roots}.md` corrected per `.dev/audit-reports/docs-audit-2026-05-22.md`.

#### Notes (cliEval)

- `INTERRUPTED` canonical exit code is **`3`** (matches `signal_handler.EXIT_INTERRUPTED` + `tests/cli/eval/test_exit_codes.py` design-spec §4 docstring), not the POSIX `signal+128 = 130` convention. CI scripts keying off the SIGINT exit code should match `3` exactly. Rationale documented inline in `exit_codes.py`.
- AC matrix at `.dev/tasks/to-do/TASK-RF-20260522-153212/phase-outputs/reports/06-ac-matrix.md` maps every H/M/CC finding ID to its remediation step, test, and verification evidence. PG-FINAL composite task-integrity gate verdict: PASS at cycle 1 (22/22 spec rows + 6/6 auxiliary VALIDATION_REQUIREMENTS checks).

---

### Added

- **Context Freshness System** (`src/superclaude/hooks/scripts/freshness-*.sh`) — seven active shell hooks plus `install_hooks.py` that:
  - Inject a `<session-context>` envelope on every user prompt (turn counter, Δ-since-last-prompt, dirty-git probe, background-agent count).
  - Block `Edit` / `Write` / `mcp__serena__replace_*` / `mcp__serena__insert_*_symbol` against files that have not been Read in the last 30 minutes.
  - Track every Read into `~/.claude/state/reads.jsonl`.
  - Emit telemetry to `~/.claude/logs/freshness-hook.jsonl` for week-1 tuning.
- New `superclaude install` step (`install_hooks`) — atomically copies hook scripts to `~/.claude/hooks/` and additively merges hook registrations into `~/.claude/settings.json` (existing user hooks preserved; backup at `~/.claude/settings.json.bak.<ISO-8601>` before any write).
- `make sync-dev` now also syncs `src/superclaude/hooks/scripts/*.sh` and `src/superclaude/scripts/session-init.sh` into `.claude/hooks/` for local development.
- Context freshness discipline section appended to `src/superclaude/core/CLAUDE.md` — codifies the five content-signal triggers (S1–S5) for citations that hooks cannot catch.

### Fixed

- `src/superclaude/hooks/hooks.json` `session-init.sh` command path changed from the fragile relative `./scripts/session-init.sh` to `~/.claude/hooks/session-init.sh` (Option B from `docs/analysis/hooks-json-relative-path-issue.md`).
- `src/superclaude/hooks/scripts/freshness-pre-edit.sh` now allows `Write` to nonexistent paths via a new `create_allowed` decision (Proposal A from `freshness-hook-fix-debate.md`). Resolves the catch-22 where the gate blocked new-file creation because there was no prior `Read`, and the `Read` itself failed because the file did not exist. `Edit` and `Write` against existing-but-unread files continue to block (`no_prior_read`). New telemetry reason `create_allowed` appears in `~/.claude/logs/freshness-hook.jsonl`. Defense-in-depth regression guard added: `tests/cli/test_install_hooks.py::test_real_hooks_json_gates_write_in_pre_tool_use` pins the matcher.

### Known v1 limitation

- **External-modification detection is not active in v1.** The design called for a `FileChanged` hook to populate `~/.claude/state/changes.jsonl` and feed the `external_change` block reason in the freshness gate. Live probing in T05.01 revealed that Claude Code's `FileChanged` matcher only accepts pipe-separated literal filenames (not regex, not "watch all"), so the design's `matcher: ".*"` registration silently watched nothing. The FileChanged registration has been removed from v1; the `freshness-file-changed.sh` script remains in `src/` for v1.5 re-implementation. The `freshness-pre-edit.sh` gate still blocks on `no_prior_read` and `read_too_old`, which cover the two highest-impact stale-fact scenarios.
- **`Write` to nonexistent files is blocked.** The freshness gate fires on any `Write` target with no prior Read tracker, which is correct per the design (the gate doesn't check file existence). For fresh-session new-file creation, use Bash heredocs (`cat > new_file <<'EOF'…EOF`). v1.5 may add a "Write to nonexistent path → allow" branch.

### v1.5 work items (freshness-system)

- **FileChanged redesign.** Two viable approaches: (a) static per-project watch list via `|`-separated literal filenames in `matcher`; (b) dynamic via `hookSpecificOutput.watchPaths` returned from `PostToolUse(Read)` — needs a fresh probe to confirm Claude Code accepts watchPaths from non-FileChanged events. After redesign, re-run Test 1 to verify `external_change` block reason fires correctly.
- **`Write`-to-new-file refinement.** Add a "if target path does not exist on disk, allow" branch to `freshness-pre-edit.sh`. Verify the change doesn't introduce a false-allow path (e.g., for race conditions where file was deleted between Read and Write).
- **`install_hooks --no-orphans` flag.** Exclude scripts from the copy list that aren't currently registered in `src/superclaude/hooks/hooks.json`. Cleaner for strict-only deployments; preserves current v1 behavior by default. Today the package copies `freshness-file-changed.sh` even though it's unregistered.
- **`reads.jsonl` rotation.** File grows unbounded; PreToolUse gate scans it on every Edit. Design §2.1 calls for keeping the oldest 3 sessions; implement before users accumulate >10K rows.
- **`session_id` sanitization.** Hook scripts interpolate `session_id` into filenames without a regex check. `validate_session_id()` helper exists in `install_hooks.py` but isn't called by the hook scripts themselves. Defense-in-depth hardening; low priority since Claude Code session_ids are platform-generated UUIDs.

### Notes

- Hooks are user-scope only (`~/.claude/settings.json`). Repo-local hooks are silently bypassed when `--add-dir` is used. To opt out, remove the relevant entries from `~/.claude/settings.json` and delete the corresponding scripts from `~/.claude/hooks/`. See [docs/user-guide/freshness-hooks.md](docs/user-guide/freshness-hooks.md).
