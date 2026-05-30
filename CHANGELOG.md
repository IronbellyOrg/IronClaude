# Changelog

All notable changes to IronClaude are documented in this file.

## [Unreleased]

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
