# C-design-claims.md — Catalog of Design Claims

**Agent:** C (Design-Doc Cataloger)
**Mode:** Read-only extraction. No value judgments. No modifications to design files.
**Sources:** DESIGN.md, adversarial/merged-output.md, adversarial/debate-transcript.md, adversarial/merge-log.md, adversarial/refactor-plan.md
**Numbering:** Stable D-NNN, sequential. Adversarial provenance IDs (S/C/X/U/A) traced from debate-transcript.md scoring matrix and merge-log.md change records.

---

## Section 1: Acceptance Criteria

Source: DESIGN.md §14 ("Acceptance Criteria"). AC IDs preserved verbatim.

| AC-ID | D-NNN | Source | Claim | Adversarial provenance | File/method touched |
|-------|-------|--------|-------|------------------------|---------------------|
| AC-1 | D-001 | DESIGN.md §14 | "A 400 KB prompt produces a successful `claude --print` invocation; output round-trips byte-identical (verified by `test_huge_prompt_delivered_via_stdin`)." | C-007 (B), C-001 (A) — merged threshold + streaming | process.py: start(), _iter_prompt_chunks() |
| AC-2 | D-002 | DESIGN.md §14 | "A small prompt's argv is byte-identical to pre-patch behavior (verified by `test_small_prompt_still_uses_argv`)." | C-005 (A) — constructor signature stability | process.py: build_command() |
| AC-3 | D-003 | DESIGN.md §14 | "No argv element ever exceeds `MAX_ARG_STRLEN = 128 KiB`, regardless of prompt size (verified by `test_argv_total_byte_size_bounded_for_huge_prompt`)." | X-001 (A) — margin sizing | process.py: build_command() invariant |
| AC-4 | D-004 | DESIGN.md §14 | "PortifyProcess produces byte-identical argv layout for small prompts (verified by `test_portify_add_dir_insertion_unchanged_for_small_prompt`)." | C-003 / X-002 (A) — Portify anchor change | cli_portify/process.py: build_command() |
| AC-5 | D-005 | DESIGN.md §14 | "SIGTERM during stdin write does not leak the writer thread (verified by `test_terminate_during_stdin_write_no_hang`)." | INV-002 (HIGH ADDRESSED) | process.py: terminate(), _join_stdin_writer() |
| AC-6 | D-006 | DESIGN.md §14 | "200 KB UTF-8 multibyte prompt round-trips correctly (verified by `test_huge_utf8_emoji_prompt_round_trip`)." | Change #4 (B§8.2) — UTF-8 multibyte test | process.py: _iter_prompt_chunks() |
| AC-7 | D-007 | DESIGN.md §14 | "A prompt above `PROMPT_MAX_BYTES` raises `PromptTooLargeForArgv` before `fork()` (verified by `test_prompt_max_bytes_guard`)." | U-003 (B), U-001 (A) — typed error + size cap | process.py: start() sanity check |
| AC-8 | D-008 | DESIGN.md §14 | "P0 release-gate probe passes — verified 2026-04-30 on `claude 2.1.123` with stdin-only and ~200 KB stdin payload, exit 0 in both cases." | A-001 / INV-005 (UNADDRESSED → resolved) | external probe; gates entire patch |
| AC-9 | D-009 | DESIGN.md §14 | "`make verify-sync` passes after `src/superclaude/` edits → `make sync-dev`." | DESIGN-NEW (deployment) | Makefile / repo-level |
| AC-10 | D-010 | DESIGN.md §14 | "Full `make test` suite passes." | DESIGN-NEW (deployment) | full test suite |

---

## Section 2: Risks

Source: DESIGN.md §11 ("Risk Register"). Risk numbers and L/I/Score preserved verbatim.

| Risk-ID | D-NNN | Source | Claim | L/I/Score | Adversarial provenance | File/method touched |
|---------|-------|--------|-------|-----------|------------------------|---------------------|
| Risk #1 | D-011 | DESIGN.md §11 | "A-001 / INV-005 — pinned `claude` does not read stdin in `--print` when positional arg is omitted — VERIFIED RESOLVED. Verified 2026-04-30 against `claude 2.1.123 (Claude Code)`. Three probes passed: (a) baseline with positional prompt; (b) stdin-only, no positional arg; (c) ~200 KB stdin prompt." | —/—/0 (closed) | A-001, INV-005 (was HIGH UNADDRESSED) | external probe; entire stdin path |
| Risk #2 | D-012 | DESIGN.md §11 | "PortifyProcess `cmd.index('-p')` raises ValueError for theoretical large Portify prompts." | L/M/2 | C-003 / X-002 (A) | cli_portify/process.py:209-213 |
| Risk #3 | D-013 | DESIGN.md §11 | "Writer thread leak if stdin close path is missed." Mitigation: "`try/finally close()`; `_join_stdin_writer(timeout=5)` in both `wait()` and `terminate()`; daemon=True bounds leak." | L/H/3 | INV-002 (ADDRESSED) | process.py: writer thread, _join_stdin_writer() |
| Risk #4 | D-014 | DESIGN.md §11 | "Prompt-size explosion now that stdin 'just works'." Mitigation: "`PROMPT_MAX_BYTES` cap (16 MiB default, env-overridable) raises `PromptTooLargeForArgv` before fork; debug log records `prompt_bytes=N` for monitoring." | M/M/4 | U-001 (A) — PROMPT_MAX_BYTES; U-003 (B) — typed error | process.py: PROMPT_MAX_BYTES, start() |
| Risk #5 | D-015 | DESIGN.md §11 | "claude CLI behavior change in a future Anthropic release." Mitigation: "Pin `claude` CLI version range in installation docs; sidecar (when enabled) gives prompt replay capability." | L/H/3 | U-004 (B) — sidecar; (provenance partial) | install docs; sidecar |
| Risk #6 | D-016 | DESIGN.md §11 | "Sidecar file disk-bloat." Mitigation: "Off by default; opt-in only; cleanup follows existing `output_file` lifecycle; automated rotation deferred to beat 2." | L/L/1 | U-004 (B) tempered by A's disk-bloat concern | process.py: prompt_sidecar kwarg |

---

## Section 3: Recommendations / Design Choices

### 3a. process.py (ClaudeProcess base class)

| D-NNN | Source | Claim | Provenance | File/method |
|-------|--------|-------|------------|-------------|
| D-017 | DESIGN.md §3 | "Threshold-based dual-path delivery for the prompt." (paraphrase) Argv path for prompts <96 KiB; stdin path for ≥96 KiB. | S-001 (A wins), C-001 (A) | process.py: build_command(), start() |
| D-018 | DESIGN.md §3, §4.3, merged-output.md §3.1 | "`PROMPT_STDIN_THRESHOLD: int = 96 * 1024`  # 98,304 bytes" | C-001 (A 90%), X-001 (A 95%) — both advocates converged on 96 KiB | process.py: module-level constant |
| D-019 | DESIGN.md §3 | "The threshold leaves a 32 KiB margin under `MAX_ARG_STRLEN`, accommodating other argv elements, environment-variable budget pressure on `ARG_MAX`, and kernel-version drift." | X-001 (A) — margin sizing | rationale only |
| D-020 | DESIGN.md §4.3, merged-output.md §3.1 | "`PROMPT_MAX_BYTES: int = int(os.environ.get('SUPERCLAUDE_PROMPT_MAX_BYTES', 16 * 1024 * 1024))`" — default 16 MiB env-overridable | U-001 (A only, 95%) | process.py: module-level constant |
| D-021 | DESIGN.md §4.3, merge-log Change #1 | "`class PromptTooLargeForArgv(ValueError): ...` Subclass of ValueError for backward-compat with callers catching ValueError." | U-003 (B only, 90%) — Change #1 | process.py: exception class |
| D-022 | DESIGN.md §4.1 | Constructor adds one new kwarg: "`prompt_sidecar: bool = False  # NEW (default off)`" — all other kwargs unchanged. | U-004 (B only, 80%) — Change #2 | process.py: ClaudeProcess.__init__ |
| D-023 | DESIGN.md §4.2 | "`def _use_stdin_for_prompt(self) -> bool`: True iff encoded prompt size >= PROMPT_STDIN_THRESHOLD. Empty prompts (size 0) explicitly stay on argv path." | C-001 (A); X-003 (B 75%) — empty prompt explicitness | process.py: new private helper |
| D-024 | DESIGN.md §4.2 | "`def _prompt_anchor_flag(self) -> str`: Returns '--output-format' — present in both delivery modes, immediately preceding the prompt-delivery flags." | U-002 (A only, 70%) | process.py: new private helper |
| D-025 | DESIGN.md §4.2, merge-log Change #3 | "`def _iter_prompt_chunks(self, chunk_size: int = 64 * 1024) -> Iterator[bytes]`: Stream-encode the prompt in chunks. Slices the source string by character index, encodes each slice. O(chunk_size) memory." | C-007 (B 75%) — Change #3 | process.py: new private helper |
| D-026 | DESIGN.md §4.2 | "`def _join_stdin_writer(self, timeout: float = 5.0) -> None`: Best-effort join on the prompt-writer thread; called from wait() and terminate() before _close_handles()." | INV-002, A's writer-thread lifecycle | process.py: new private helper |
| D-027 | DESIGN.md §6.1 (decision table), merged-output.md §3.2 | "Empty prompts (size 0) explicitly stay on argv path with `-p ""`; we do not silently switch to stdin for empty strings." | X-003 (B 75%) — Change #5 | process.py: _use_stdin_for_prompt() |
| D-028 | DESIGN.md §6.1 | "Encoding failure → True (route to stdin path)." (paraphrase: catch UnicodeEncodeError/AttributeError, treat as large) | DESIGN-NEW (defensive, A-derived) | process.py: _use_stdin_for_prompt() |
| D-029 | DESIGN.md §6.2 | "`subprocess.Popen(..., stdin=subprocess.PIPE, stdout=fh, stderr=fh)` for stdin path; stdin=DEVNULL for argv path." | A§3.3, base behavior | process.py: start() |
| D-030 | DESIGN.md §6.2 | "Spawn `threading.Thread(daemon=True)` named `claude-stdin-writer-<pid>`." | A§3.3 | process.py: start() |
| D-031 | DESIGN.md §6.2 | "Encode each character slice as UTF-8 with `errors='strict'`." | C-007 + Change #4 | process.py: _iter_prompt_chunks() |
| D-032 | DESIGN.md §6.2 | "For each chunk, `os.write(fd, view)` in a loop until fully written; retry on `InterruptedError` (EINTR); terminate on `BrokenPipeError`." | C-004 (A 85%) — os.write over BufferedWriter | process.py: writer thread closure |
| D-033 | DESIGN.md §6.2 | "**`finally`**: close child stdin (delivers EOF; required by `claude --print`), close sidecar handle." | INV-002 (HIGH ADDRESSED); merged-output §5 ("EOF non-negotiable") | process.py: writer thread finally |
| D-034 | DESIGN.md §6.2 | "Errors stored in `self._stdin_error`; surfaced in `_join_stdin_writer()` log line." | A§3.3 | process.py: writer + _join_stdin_writer |
| D-035 | DESIGN.md §6.2 | "If `prompt_sidecar=True`, also append the chunk to `output_file.with_suffix('.prompt')`." | U-004 (B 80%) — Change #2 | process.py: writer thread |
| D-036 | DESIGN.md §6.1 | "Sanity guard: prompts > PROMPT_MAX_BYTES (16 MiB) raise PromptTooLargeForArgv in start() before spawn." | U-001 (A) + U-003 (B) | process.py: start() pre-spawn check |
| D-037 | DESIGN.md §7 (Compatibility Contract) | "`self.prompt` attribute always equals the constructor's `prompt` argument (no value-erasure for large prompts)." | X-004 (A 80%) — B conceded | process.py: ClaudeProcess.prompt invariant |
| D-038 | DESIGN.md §7 | "`cmd[:3]` debug log unchanged: `['claude', '--print', '--verbose']` in both modes (sprint/audit log scrapers continue to work)." | A§3.3, S-001 | process.py: start() debug log prefix |
| D-039 | DESIGN.md §7 | "Process group / signals unchanged. `preexec_fn=os.setpgrp` still gates child into its own pgroup." | base behavior, unchanged | process.py: start() preexec_fn |
| D-040 | DESIGN.md §7 | "Cancellation polling unchanged. Daemon writer thread isolates parent's poll loop from stdin write progress." | merged-output §5 ("Why not communicate") | process.py: terminate() / cancellation |
| D-041 | DESIGN.md §7 | "Environment handling: `build_env()` unchanged; same `CLAUDECODE` / `CLAUDE_CODE_ENTRYPOINT` stripping." | edge case #7 | process.py: build_env() (unchanged) |
| D-042 | DESIGN.md §6.1 | "Prompts in [98,304 … 16,777,215 bytes] take stdin path with PIPE." (paraphrase of decision-table row) | C-001, U-001 | process.py: _use_stdin_for_prompt() |
| D-043 | DESIGN.md §4.1 | "All current callers/subclasses untouched at constructor level; `prompt_sidecar=False` default preserves them." | C-005 (A 70%) | roadmap/executor.py:749, validate_executor.py:117, remediate_executor.py:245, tasklist/executor.py:127 |
| D-044 | merged-output.md §5 | "Why not `proc.communicate(input=prompt_bytes)`? communicate() insists on managing stdout/stderr and blocks calling thread, breaking cancellation polling at roadmap/executor.py:763-775 et al." | A§3.3 design rationale | process.py: choice of writer thread |
| D-045 | merged-output.md §5 | "OS pipe buffer is 64 KiB on Linux; writer thread isolates parent's poll loop from a slow child." | A's design rationale | process.py: thread justification |

### 3b. cli_portify/process.py (PortifyProcess)

| D-NNN | Source | Claim | Provenance | File/method |
|-------|--------|-------|------------|-------------|
| D-046 | DESIGN.md §6.3 | "Replace direct `cmd.index('-p')` lookup with `anchor = cmd.index(self._prompt_anchor_flag()); insert_at = anchor + 2` (skip flag and its value)." | C-003 (A 65%), X-002 (A 60%), U-002 (A only) | cli_portify/process.py:209-213 |
| D-047 | DESIGN.md §6.3 | "For all current Portify invocations (small prompts), this produces byte-identical argv. For future large Portify prompts, `--add-dir` flags land in the same relative position even when `-p` is absent." | C-003, X-002 | cli_portify/process.py: build_command() |
| D-048 | DESIGN.md §7 | "Portify subclass: 2-line tweak in `build_command()` to use `_prompt_anchor_flag()`; produces byte-identical argv for small prompts." (paraphrase) | C-003 (A 65%) | cli_portify/process.py |
| D-049 | merged-output.md §4 | "A unit test pins the contract: `build_command()` must emit `--output-format` and its value as adjacent argv elements; if any future flag is inserted between them, CI catches the violation." | DESIGN-NEW (test contract for U-002) | tests/cli/pipeline/ — output-format adjacency test |

### 3c. Tests (DESIGN.md §9.1 coverage matrix; merged-output.md §7)

| D-NNN | Source | Claim (test name) | Provenance | File/method |
|-------|--------|-------------------|------------|-------------|
| D-050 | DESIGN.md §9.1 | `test_build_command_keeps_p_flag_for_small_prompt` — Small prompt → argv path | C-005 | tests/cli/pipeline/test_claude_process_delivery.py |
| D-051 | DESIGN.md §9.1 | `test_build_command_omits_p_flag_for_large_prompt` — Huge prompt → stdin path, `-p` absent | C-001, C-002 | same test file |
| D-052 | DESIGN.md §9.1 | `test_argv_total_byte_size_bounded_for_huge_prompt` — No argv element exceeds MAX_ARG_STRLEN | X-001 | same |
| D-053 | DESIGN.md §9.1 | `test_threshold_boundary_under` — 95 KiB → argv | C-001 | same |
| D-054 | DESIGN.md §9.1 | `test_threshold_boundary_over` — 97 KiB → stdin | C-001 | same |
| D-055 | DESIGN.md §9.1 | `test_empty_prompt_uses_argv_with_empty_p_value` — Empty prompt preserved on argv (`-p ""`) | X-003 (B), Change #5 | same |
| D-056 | DESIGN.md §9.1 | `test_huge_prompt_delivered_via_stdin` — End-to-end huge prompt round-trip via stdin | C-007, AC-1 | same |
| D-057 | DESIGN.md §9.1 | `test_small_prompt_still_uses_argv` — End-to-end small prompt still uses argv | C-005, AC-2 | same |
| D-058 | DESIGN.md §9.1 | `test_huge_utf8_emoji_prompt_round_trip` — UTF-8 multibyte (200 KB emoji) round-trip | Change #4 (B§8.2) | same |
| D-059 | DESIGN.md §9.1 | `test_prompt_max_bytes_guard` — `PROMPT_MAX_BYTES` cap raises typed exception | U-001 (A) + U-003 (B), AC-7 | same |
| D-060 | DESIGN.md §9.1 | `test_terminate_during_stdin_write_no_hang` — SIGTERM mid-write does not hang or leak the writer thread | INV-002, AC-5 | same |
| D-061 | DESIGN.md §9.1 | `test_portify_add_dir_insertion_unchanged_for_small_prompt` — Portify regression — small prompt argv layout unchanged | C-003, AC-4 | same |
| D-062 | DESIGN.md §9.1 | `test_portify_add_dir_insertion_works_for_large_prompt` — Portify regression — large prompt still gets `--add-dir` | C-003, X-002 | same |
| D-063 | DESIGN.md §9.1 | `test_output_format_flag_and_value_are_adjacent` — `--output-format` and value are adjacent argv elements | U-002, contract pin | same |
| D-064 | DESIGN.md §9.1 | `test_prompt_sidecar_written_when_opted_in` — Sidecar is written when opted in | U-004 (B), Change #2 | same |
| D-065 | DESIGN.md §9.1 | `test_no_sidecar_by_default` — No sidecar by default | U-004 (B), opt-in safety | same |
| D-066 | DESIGN.md §9.2, merged-output.md §7 | "Run via `uv run pytest tests/cli/pipeline/test_claude_process_delivery.py -v` (per CLAUDE.md UV-only rule)." | DESIGN-NEW (project policy) | test runner |
| D-067 | DESIGN.md §9.2 | "CI integration: per project policy ('Validation should be done via the .github actions'), add the suite to the existing pipeline workflow. No one-off scripts." | DESIGN-NEW (project policy) | .github actions |
| D-068 | merged-output.md §7.1 | New fixtures: `mock_claude_bin`, `small_prompt`, `empty_prompt`, `boundary_prompt_under` (95 KiB), `boundary_prompt_over` (97 KiB), `huge_prompt` (400 KiB), `emoji_prompt` (200 KB of "🦀"). | C-001, X-003, Change #4 | tests/cli/pipeline/conftest.py |
| D-069 | merged-output.md §7.1 | "Mock claude that dumps argv to stderr and stdin to stdout" via bash script `echo "ARGV: $@" >&2; cat`. | DESIGN-NEW (test fixture design) | tests/cli/pipeline/conftest.py |

### 3d. Observability / logging

| D-NNN | Source | Claim | Provenance | File/method |
|-------|--------|-------|------------|-------------|
| D-070 | DESIGN.md §10.1 | "Existing `_log.debug('spawn pid=%d cmd=%s', ..., self.build_command()[:3])` is preserved unchanged." | S-001, A§3.3 | process.py: start() debug log |
| D-071 | DESIGN.md §10.1 | "New fields appended to the same debug line: `prompt_via=stdin\|argv`, `prompt_bytes=N`, `sidecar=bool`." | DESIGN-NEW (new log fields) | process.py: start() debug log |
| D-072 | DESIGN.md §10.1 | "Optional `.prompt` sidecar file (opt-in via `prompt_sidecar=True`) provides an operator-readable 'what did claude actually see?' record when stdin mode hides the prompt from `ps`." | U-004 (B) | process.py: writer thread sidecar |
| D-073 | DESIGN.md §10.1 | "Recommended caller policy: roadmap-family executors opt in to the sidecar (large prompts, debugging value); sprint/audit opt out (high-frequency phases, disk-bloat avoidance)." | refactor-plan Change #2 | caller config (roadmap/, sprint/, cleanup_audit/) |
| D-074 | DESIGN.md §6.1 edge case #11, merged-output.md §6 | "`ps`/`/proc/<pid>/cmdline` no longer shows prompt for stdin path. Intentional — and arguably a security improvement." | A's argument; merged-output §6 case 11 | operational behavior |

### 3e. Rollout / deployment

| D-NNN | Source | Claim | Provenance | File/method |
|-------|--------|-------|------------|-------------|
| D-075 | DESIGN.md §10.2 | "Threshold-based design is naturally rollback-friendly: setting `PROMPT_STDIN_THRESHOLD = 2**31` reverts to argv-only behavior without code change." | DESIGN-NEW (rollback ergonomics) | process.py: constant tweak |
| D-076 | DESIGN.md §10.2 | "For emergency rollback at runtime: revert the patched `process.py` from git; no caller code or data migration is required." | DESIGN-NEW | git revert |
| D-077 | DESIGN.md §10.3 | "Immediate (operator unblock today): vendored monkey-patch in the consumer repo at `.dev/claude_process_stdin_patch.py`, imported via the project's superclaude wrapper. Survives `pipx upgrade`." | merged-output §8 | .dev/claude_process_stdin_patch.py + wrapper |
| D-078 | DESIGN.md §10.3 / §15 | "Durable: Branch `fix/claude-process-stdin-large-prompts`. Apply diffs to `src/superclaude/cli/pipeline/process.py` and `src/superclaude/cli/cli_portify/process.py`. Add `tests/cli/pipeline/test_claude_process_delivery.py`. `make sync-dev && make verify-sync && make test`. PR with this DESIGN.md as the design doc. After merge & release: `pipx upgrade superclaude` ships the fix." | DESIGN-NEW + S-005 (B 65%, two-beat staging) | branch, repo files |
| D-079 | DESIGN.md §15 | "P0 — Risk-gate verification: run the live `claude` stdin probe — DONE 2026-04-30. Verified on `claude 2.1.123`; all 3 probes passed." | A-001 / INV-005 | external probe |
| D-080 | DESIGN.md §15 | "P1 — Apply patch to `src/superclaude/cli/pipeline/process.py` per §4-§6." | DESIGN-NEW | src/superclaude/cli/pipeline/process.py |
| D-081 | DESIGN.md §15 | "P2 — Apply 2-line PortifyProcess tweak per §6.3." | C-003, U-002 | src/superclaude/cli/cli_portify/process.py |
| D-082 | DESIGN.md §15 | "P3 — Add tests per §9 to `tests/cli/pipeline/test_claude_process_delivery.py`." Test suite green locally via `uv run pytest`. | DESIGN-NEW | tests/cli/pipeline/ |
| D-083 | DESIGN.md §15 | "P4 — `make sync-dev && make verify-sync && make test`. `.claude/` synced; CI-equivalent green." | project policy (CLAUDE.md) | Makefile |
| D-084 | DESIGN.md §15 | "P5 — Open upstream PR with this DESIGN.md attached." | DESIGN-NEW | GitHub PR |
| D-085 | DESIGN.md §15 | "P6 — Vendored monkey-patch in consumer repo for immediate unblock." | DESIGN-NEW (parallel deploy) | .dev/claude_process_stdin_patch.py |
| D-086 | DESIGN.md §15 | "P7 — Re-run failing roadmap pipeline command end-to-end. Successful `superclaude roadmap run …` with 338 KB composed prompt." | original bug repro | superclaude roadmap run end-to-end |
| D-087 | DESIGN.md §15 | "The vendored monkey-patch (P6) and upstream PR (P5) proceed in parallel. When the upstream release ships, `pipx upgrade superclaude` makes the monkey-patch redundant and it can be removed." | DESIGN-NEW | dual-track delivery |

### 3f. Other (compatibility, beat-2, scope, open questions)

| D-NNN | Source | Claim | Provenance | File/method |
|-------|--------|-------|------------|-------------|
| D-088 | DESIGN.md §8.1 | Files modified: `src/superclaude/cli/pipeline/process.py` (~+95 LOC), `src/superclaude/cli/cli_portify/process.py` (+5/-4). | DESIGN-NEW | scope of edit |
| D-089 | DESIGN.md §8.2 | Files added: `tests/cli/pipeline/conftest.py` (extend), `tests/cli/pipeline/test_claude_process_delivery.py` (new). | DESIGN-NEW | tests |
| D-090 | DESIGN.md §8.3 | Files NOT modified: "`roadmap/executor.py` — `_EMBED_SIZE_LIMIT` warning at lines 735-742 stays as advisory; remove in beat 2 once stdin path is proven." | refactor-plan rejection: "Removal of `_EMBED_SIZE_LIMIT` warning at call sites — keep advisory in beat 1" | roadmap/executor.py (untouched) |
| D-091 | DESIGN.md §8.3 | "All other callers (`validate_executor.py`, `remediate_executor.py`, `tasklist/executor.py`, `sprint/executor.py`) NOT modified." | C-005 (A) | callers (untouched) |
| D-092 | DESIGN.md §8.3 | "Sprint and audit subclasses NOT modified." | C-005, "no code change. Inherits new behavior; sprint prompts (~few KB) always take argv path" | sprint/process.py, cleanup_audit/process.py |
| D-093 | DESIGN.md §13 | Beat-2 follow-up: "Introduce `pre_prompt_args: list[str]` mechanism on base; migrate `PortifyProcess` to set it in `__init__` and delete its `build_command` override entirely." | refactor-plan reject: deferred from C-002/C-005 | future |
| D-094 | DESIGN.md §13 | Beat-2 follow-up: "Promote stdin to default delivery for all prompt sizes once the sidecar observability story is mature." | DESIGN-NEW | future |
| D-095 | DESIGN.md §13 | Beat-2 follow-up: "`--input-format=stream-json` delivery for tool-use orchestration." | refactor-plan reject (B's stream-json deferred) | future |
| D-096 | DESIGN.md §13 | Beat-2 follow-up: "Automated rotation/cleanup of `.prompt` sidecars (TTL or pipeline-bound)." | Risk #6 mitigation (deferred) | future |
| D-097 | DESIGN.md §13 | Beat-2 follow-up: "Optional `PromptSource` Protocol if a second concrete source (file, stream-json) actually ships." | refactor-plan reject C-002 (YAGNI) | future |
| D-098 | DESIGN.md §12 | Open Q3: "Per-caller threshold override? Out of scope for this design. Add `force_prompt_via` kwarg in beat 2 if needed." | refactor-plan reject C-005 | future |
| D-099 | DESIGN.md §12 | Open Q4: "`prompt_bytes=N` in production debug logs — acceptable? Sizes are not content but may be a compliance signal in some contexts. Decide before merging." | DESIGN-NEW | open question |
| D-100 | DESIGN.md §12 | Open Q5: "Downgrade `_EMBED_SIZE_LIMIT` warnings at call sites to debug? Defer until stdin path proves stable." | refactor-plan reject (keep advisory) | open question |
| D-101 | DESIGN.md §12 | Open Q1 (resolved): "Does pinned `claude --print` accept a missing positional prompt argument and read stdin? YES — verified 2026-04-30 on `claude 2.1.123`." | A-001 / INV-005 (resolved) | external probe |
| D-102 | DESIGN.md §12 | Open Q2 (resolved): "Trailing newline / framing requirements? None — `echo` adds a trailing newline and probe 2 passed; the 200 KB probe also worked. No defensive `\n` needed." | A-001 / INV-005 follow-up | claude CLI behavior |
| D-103 | DESIGN.md §6.1 edge case #4 / merged-output §6 case #4 | "Embedded NULs in prompt: Argv path silently truncates at first `\\x00` (execve uses C strings). Stdin path preserves them — latent improvement." | merged-output §6 | process.py behavior diff |
| D-104 | merged-output.md §6 case #6 | "Windows portability: Linux-only `os.setpgrp`/`os.killpg`/`os.getpgid` already gated by `hasattr` checks. Windows `CreateProcess` 32 KiB total cmdline limit means stdin path triggers more eagerly there." | DESIGN-NEW (cross-platform note) | process.py: hasattr gating |
| D-105 | merged-output.md §6 case #13 | "Prompt mutated after construction: `self.prompt` is read in `_use_stdin_for_prompt()` and lazily in `_iter_prompt_chunks()`. If a caller mutates `self.prompt` between `__init__` and `start()`, the mutation is observed (caveat emptor; existing behavior unchanged)." | DESIGN-NEW (semantics doc) | process.py: behavior |
| D-106 | merged-output.md §6 case #14 | "Re-entrancy of `start()`: existing pre-condition (already undefined behavior); patch does not change." | DESIGN-NEW | process.py: behavior |
| D-107 | merged-output.md §5 | "Streaming chunks rather than full-buffer encode: For ordinary roadmap usage (~300 KB), full-buffer encode is fine. For audit-pipeline composition (multi-MB) or future workflows, full-buffer encode doubles peak heap. `_iter_prompt_chunks(64 KB)` streams." | C-007 (B 75%) | process.py: _iter_prompt_chunks() |
| D-108 | merged-output.md §5 | "EOF: `stdin_fh.close()` in `finally` is non-negotiable. `claude --print` requires EOF to begin processing. Closing in `finally` guarantees EOF even on exception." | INV-002 (HIGH ADDRESSED) | process.py: writer finally |
| D-109 | DESIGN.md §3 / merged-output §2 | Mode comparison table excluding "Always-stdin" (loses argv visibility) and "Opt-in flag" (forces every call site to know about argv limits); only Threshold-stdin selected. | A's design rationale | architectural decision |
| D-110 | merged-output.md §6 case #5 | "NamedTemporaryFile cleanup on crash: N/A — no temp file used." | DESIGN-NEW (rejects file-based delivery) | process.py: design choice |

---

## Section 4: Provenance Index

Sortable mapping of each D-NNN to its adversarial provenance. Sources: debate-transcript.md scoring matrix, merge-log.md change records, refactor-plan.md.

| D-NNN | Provenance ID(s) | Provenance type |
|-------|-------------------|-----------------|
| D-001 | C-007 (B), C-001 (A) | Merged: streaming + threshold |
| D-002 | C-005 (A) | A wins |
| D-003 | X-001 (A) | A wins (margin sizing) |
| D-004 | C-003 (A), X-002 (A) | A wins (Portify anchor) |
| D-005 | INV-002 (HIGH ADDRESSED) | Invariant probe |
| D-006 | Change #4 (B§8.2) | B incorporated |
| D-007 | U-003 (B only), U-001 (A only) | Merged unique |
| D-008 | A-001 / INV-005 | Was UNADDRESSED → resolved |
| D-009 | DESIGN-NEW | Project policy |
| D-010 | DESIGN-NEW | Project policy |
| D-011 | A-001, INV-005 | Resolved invariant |
| D-012 | C-003 (A), X-002 (A) | A wins |
| D-013 | INV-002 | Invariant ADDRESSED |
| D-014 | U-001 (A), U-003 (B) | Merged unique |
| D-015 | U-004 (B partial) | Partial provenance |
| D-016 | U-004 (B) tempered by A | Merged tradeoff |
| D-017 | S-001, C-001 | A wins |
| D-018 | C-001 (A 90%), X-001 (A 95%) | Both converged on 96 KiB |
| D-019 | X-001 (A) | A wins |
| D-020 | U-001 (A only, 95%) | A unique |
| D-021 | U-003 (B only, 90%) — Change #1 | B unique, applied |
| D-022 | U-004 (B only, 80%) — Change #2 | B unique, applied |
| D-023 | C-001 (A), X-003 (B) | Merged |
| D-024 | U-002 (A only, 70%) | A unique |
| D-025 | C-007 (B 75%) — Change #3 | B incorporated |
| D-026 | INV-002 | Invariant |
| D-027 | X-003 (B 75%) — Change #5 | B incorporated |
| D-028 | DESIGN-NEW | A-derived defensive |
| D-029 | A§3.3 base | A baseline |
| D-030 | A§3.3 | A baseline |
| D-031 | C-007 + Change #4 | Merged |
| D-032 | C-004 (A 85%) | A wins |
| D-033 | INV-002, merged-output §5 | Invariant ADDRESSED |
| D-034 | A§3.3 | A baseline |
| D-035 | U-004 (B), Change #2 | B incorporated |
| D-036 | U-001 (A) + U-003 (B) | Merged |
| D-037 | X-004 (A 80%) | A wins, B conceded |
| D-038 | S-001, A§3.3 | A wins (preserve log shape) |
| D-039 | base | unchanged |
| D-040 | merged-output §5 | A's design rationale |
| D-041 | edge case #7 | unchanged |
| D-042 | C-001, U-001 | Merged |
| D-043 | C-005 (A 70%) | A wins |
| D-044 | A§3.3 | A baseline rationale |
| D-045 | A | A rationale |
| D-046 | C-003, X-002, U-002 | A wins |
| D-047 | C-003, X-002 | A wins |
| D-048 | C-003 (A 65%) | A wins |
| D-049 | DESIGN-NEW (test contract for U-002) | A unique extension |
| D-050 | C-005 | A |
| D-051 | C-001, C-002 | A |
| D-052 | X-001 | A |
| D-053 | C-001 | A |
| D-054 | C-001 | A |
| D-055 | X-003 (B), Change #5 | B incorporated |
| D-056 | C-007, AC-1 | Merged |
| D-057 | C-005, AC-2 | A |
| D-058 | Change #4 (B§8.2) | B incorporated |
| D-059 | U-001 (A) + U-003 (B), AC-7 | Merged |
| D-060 | INV-002, AC-5 | Invariant |
| D-061 | C-003, AC-4 | A |
| D-062 | C-003, X-002 | A |
| D-063 | U-002 | A unique |
| D-064 | U-004 (B), Change #2 | B incorporated |
| D-065 | U-004 (B) | B incorporated |
| D-066 | DESIGN-NEW (project policy) | CLAUDE.md UV rule |
| D-067 | DESIGN-NEW (project policy) | CLAUDE.md CI rule |
| D-068 | C-001, X-003, Change #4 | Merged |
| D-069 | DESIGN-NEW | Test fixture design |
| D-070 | S-001, A§3.3 | A wins |
| D-071 | DESIGN-NEW | New log fields |
| D-072 | U-004 (B) | B incorporated |
| D-073 | refactor-plan Change #2 | Caller policy |
| D-074 | merged-output §6 case #11 | A's argument |
| D-075 | DESIGN-NEW | Rollback ergonomics |
| D-076 | DESIGN-NEW | Rollback |
| D-077 | merged-output §8 | A's deployment |
| D-078 | DESIGN-NEW + S-005 (B 65%) | Two-beat staging |
| D-079 | A-001 / INV-005 | Resolved |
| D-080 | DESIGN-NEW | Implementation plan |
| D-081 | C-003, U-002 | A wins |
| D-082 | DESIGN-NEW | Implementation plan |
| D-083 | project policy (CLAUDE.md) | repo policy |
| D-084 | DESIGN-NEW | Implementation plan |
| D-085 | DESIGN-NEW | Parallel deploy |
| D-086 | original bug repro | DESIGN-NEW |
| D-087 | DESIGN-NEW | Dual-track |
| D-088 | DESIGN-NEW | Scope |
| D-089 | DESIGN-NEW | Scope |
| D-090 | refactor-plan rejection | "keep advisory in beat 1" |
| D-091 | C-005 (A) | A wins |
| D-092 | C-005 + DESIGN.md §8.3 | A wins |
| D-093 | refactor-plan reject C-002/C-005 | Deferred B item |
| D-094 | DESIGN-NEW | Beat-2 future |
| D-095 | refactor-plan reject (B's stream-json deferred) | Deferred |
| D-096 | Risk #6 mitigation (deferred) | Future |
| D-097 | refactor-plan reject C-002 | Deferred B item |
| D-098 | refactor-plan reject C-005 | Deferred |
| D-099 | DESIGN-NEW | Open question |
| D-100 | refactor-plan reject (keep advisory) | Deferred |
| D-101 | A-001 / INV-005 (resolved) | Resolved |
| D-102 | A-001 / INV-005 follow-up | Resolved |
| D-103 | merged-output §6 case #4 | DESIGN-NEW behavior diff |
| D-104 | DESIGN-NEW (cross-platform note) | New |
| D-105 | DESIGN-NEW | Semantics doc |
| D-106 | DESIGN-NEW | Behavior |
| D-107 | C-007 (B 75%) | B incorporated |
| D-108 | INV-002 | Invariant |
| D-109 | A's design rationale | A wins (mode selection) |
| D-110 | DESIGN-NEW | Design choice |

**Provenance legend:**
- **S-NNN / C-NNN / X-NNN / U-NNN / A-NNN** — diff points from `diff-analysis.md` and scored in `debate-transcript.md` scoring matrix.
- **INV-NNN** — invariant findings from `invariant-probe.md`.
- **Change #N** — applied incorporations recorded in `merge-log.md`.
- **DESIGN-NEW** — claim novel to DESIGN.md (or merged-output.md), not directly traceable to a debate provenance ID.

---

## Section 5: Coverage Check

### Acceptance Criteria coverage

DESIGN.md §14 enumerates AC-1 through AC-10. All ten captured:
- AC-1 → D-001
- AC-2 → D-002
- AC-3 → D-003
- AC-4 → D-004
- AC-5 → D-005
- AC-6 → D-006
- AC-7 → D-007
- AC-8 → D-008
- AC-9 → D-009
- AC-10 → D-010

**Coverage: 10/10 (complete).**

### Risk register coverage

DESIGN.md §11 enumerates Risk #1 through Risk #6. All six captured:
- Risk #1 → D-011
- Risk #2 → D-012
- Risk #3 → D-013
- Risk #4 → D-014
- Risk #5 → D-015
- Risk #6 → D-016

**Coverage: 6/6 (complete).**

### Test cases coverage (DESIGN.md §9.1)

DESIGN.md §9.1 enumerates 16 test cases. All sixteen captured:
- `test_build_command_keeps_p_flag_for_small_prompt` → D-050
- `test_build_command_omits_p_flag_for_large_prompt` → D-051
- `test_argv_total_byte_size_bounded_for_huge_prompt` → D-052
- `test_threshold_boundary_under` → D-053
- `test_threshold_boundary_over` → D-054
- `test_empty_prompt_uses_argv_with_empty_p_value` → D-055
- `test_huge_prompt_delivered_via_stdin` → D-056
- `test_small_prompt_still_uses_argv` → D-057
- `test_huge_utf8_emoji_prompt_round_trip` → D-058
- `test_prompt_max_bytes_guard` → D-059
- `test_terminate_during_stdin_write_no_hang` → D-060
- `test_portify_add_dir_insertion_unchanged_for_small_prompt` → D-061
- `test_portify_add_dir_insertion_works_for_large_prompt` → D-062
- `test_output_format_flag_and_value_are_adjacent` → D-063
- `test_prompt_sidecar_written_when_opted_in` → D-064
- `test_no_sidecar_by_default` → D-065

**Coverage: 16/16 (complete).**

### Sections walked

- DESIGN.md §1 Problem Statement → context for D-017+
- DESIGN.md §2 Architectural Context → scope captured (D-088, D-091, D-092)
- DESIGN.md §3 Design Overview → D-017, D-018, D-019, D-109
- DESIGN.md §4 Component Interface → D-020, D-021, D-022, D-023, D-024, D-025, D-026
- DESIGN.md §5 Sequence Diagrams → behavior captured in D-029, D-030, D-040
- DESIGN.md §6 Detailed Behavior → D-027, D-028, D-029-D-035, D-103
- DESIGN.md §6.3 PortifyProcess change → D-046, D-047, D-048
- DESIGN.md §7 Compatibility Contract → D-037, D-038, D-039, D-040, D-041, D-043, D-048
- DESIGN.md §8 Module Layout → D-088, D-089, D-090, D-091, D-092
- DESIGN.md §9 Test Strategy → D-050-D-067
- DESIGN.md §10 Operational Considerations → D-070, D-071, D-072, D-073, D-074, D-075, D-076, D-077, D-078
- DESIGN.md §11 Risk Register → D-011-D-016
- DESIGN.md §12 Open Questions → D-098, D-099, D-100, D-101, D-102
- DESIGN.md §13 Beat-2 Follow-ups → D-093, D-094, D-095, D-096, D-097
- DESIGN.md §14 Acceptance Criteria → D-001-D-010
- DESIGN.md §15 Implementation Plan → D-079-D-087
- merged-output.md unique additions → D-044, D-045, D-049, D-068, D-069, D-103, D-104, D-105, D-106, D-107, D-108, D-110

**No TODOs / no missing items identified.**

---

**End of C-design-claims.md.**
