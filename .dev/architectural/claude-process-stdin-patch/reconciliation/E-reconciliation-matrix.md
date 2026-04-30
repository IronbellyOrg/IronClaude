# E-reconciliation-matrix.md — Phase 2 Synthesis

**Workspace:** `/config/workspace/IronClaude`
**Branch under analysis:** `fix/claude-process-stdin-large-prompts` (off `feat/tdd-spec-merge`)
**Inputs:** A-commit-history.md, B-code-state.md, C-design-claims.md, D-test-coverage.md, DESIGN.md §11

---

## 1. Methodology

I cross-walked agent C's 110 D-NNN claims against (a) commit-history evidence from agent A — especially the two load-bearing SHAs `39d5100` (`tool_write_mode`, Apr 18) and `4799719` (stdin migration, Apr 20); (b) current code state from agent B — line-anchored facts about `pipeline/process.py`, `cli_portify/process.py`, sprint, and cleanup_audit subclasses; (c) test coverage from agent D — what is already pinned, what would regress under DESIGN.md verbatim, and what is still missing per §9.1. Each claim is judged on a single axis: "is the design intent already in-tree, partially in-tree, absent, or superseded?" I cite SHAs (agent A), `path:line` (agent B/D), and D-NNN (agent C) for every cell. The action vocabulary is the canonical six: DROP, KEEP-AS-IS, ADAPT, IMPLEMENT-FRESH, DEFER-TO-BEAT-2, SUPERSEDED. A claim is DROPped only when the current code is functionally equivalent to DESIGN intent. A claim is KEEP-AS-IS when current code chose a different shape (e.g., always-stdin instead of threshold) but the chosen shape is acceptable or superior. ADAPT means partial overlap requiring a targeted fix or reshape. IMPLEMENT-FRESH means no analog in tree. SUPERSEDED means the underlying mechanism was replaced (typical: threshold-based proposals once `4799719` made stdin universal). Risk-if-skipped is carried forward from DESIGN.md §11 where the row maps to a risk; otherwise it is judged from the proximate failure mode.

---

## 2. Reconciliation Matrix

### 2a. Acceptance Criteria (AC-1 … AC-10)

| ID | Description (≤140 chars) | Already-Implemented? | Partial / Divergent? | Still Needed? | Risk-if-skipped | Recommended action |
|----|--------------------------|----------------------|----------------------|---------------|-----------------|--------------------|
| D-001 | AC-1: 400 KB prompt round-trips successfully via stdin | Partially — 200 KB round-trip pinned at `tests/pipeline/test_process.py:200-219`; commit `4799719` enables it | No 400 KB scale test; size cap absent so untested | partial | medium — empirical scaling gap above 200 KB | ADAPT |
| D-002 | AC-2: small prompt argv byte-identical to pre-patch | Pre-patch had `-p`; current `pipeline/process.py:79-95` emits no `-p` for any size | Yes — current contract is "no `-p` ever"; conflicts with DESIGN intent | superseded | low — pre-patch shape obsolete | SUPERSEDED |
| D-003 | AC-3: no argv element exceeds MAX_ARG_STRLEN | Implicitly true: `pipeline/process.py:79-95` argv contains only fixed flags + model + extra_args — no prompt | No numeric bound asserted in any test (D §3 row 3) | partial | low — invariant holds by construction but unguarded | ADAPT |
| D-004 | AC-4: Portify produces byte-identical argv for small prompts | Layout differs from DESIGN: `cli_portify/process.py:208-213` `--add-dir` appended at end (B Q1) | Yes — `cmd.index("-p")` is dead code; appended layout is current contract | superseded | low — current layout is the new baseline | SUPERSEDED |
| D-005 | AC-5: SIGTERM during stdin write does not leak writer thread | No writer thread exists (B §3, `pipeline/process.py:140-146` synchronous) | Different surface — no thread to leak; instead parent `start()` can stall on full pipe buffer | partial | high (Risk #3 reframed) — synchronous stall not mitigated | ADAPT |
| D-006 | AC-6: 200 KB UTF-8 multibyte prompt round-trips | Generic stdin path supports UTF-8 (`pipeline/process.py:142` encodes UTF-8) | No emoji-specific test (D §3 row 9) | yes | low — UTF-8 byte path is tested via ASCII payload | IMPLEMENT-FRESH |
| D-007 | AC-7: Prompt > PROMPT_MAX_BYTES raises PromptTooLargeForArgv before fork | Not present — no cap, no exception class (B "Prompt sizing — none") | Absent | yes | medium (Risk #4) — prompt-size explosion unguarded | IMPLEMENT-FRESH |
| D-008 | AC-8: P0 release-gate stdin probe passes | Yes — verified 2026-04-30 on `claude 2.1.123` (DESIGN.md §11 Risk #1 closed) | None | no | low — closed | DROP |
| D-009 | AC-9: `make verify-sync` passes after src→.claude sync | N/A on this branch — only design-package import (`530955b`) so far | Repo policy gate, not code | yes | low — process gate | IMPLEMENT-FRESH |
| D-010 | AC-10: Full `make test` passes | Tests in tree are green against current always-stdin shape per D | DESIGN-verbatim would regress 4 assertions in `tests/pipeline/test_process.py` (D §3 conflict surface) | yes | high — gating final delivery | IMPLEMENT-FRESH |

### 2b. Risk Register (Risk #1 … Risk #6)

| ID | Description (≤140 chars) | Already-Implemented? | Partial / Divergent? | Still Needed? | Risk-if-skipped | Recommended action |
|----|--------------------------|----------------------|----------------------|---------------|-----------------|--------------------|
| D-011 | Risk #1: pinned claude won't read stdin without positional arg — VERIFIED RESOLVED | Yes — probed 2026-04-30; `4799719` shipped on assumption | None | no | low — closed | DROP |
| D-012 | Risk #2: PortifyProcess `cmd.index('-p')` raises ValueError for large prompts | Manifested already — `cli_portify/process.py:210` raises ValueError for ALL invocations (B §1, B Q1) | The lookup is silently dead; `--add-dir` lands at end | yes | medium (Risk #2) — argv layout no longer matches design anchor; latent UX/regression risk | ADAPT |
| D-013 | Risk #3: Writer thread leak if close path missed — addressed by daemon thread + join | No thread exists; risk reshaped to "synchronous stdin.write stalls parent on full kernel pipe buffer" | Different mitigation vector | yes | high (Risk #3 reframed) — parent can stall before reaching cancel-poll | ADAPT |
| D-014 | Risk #4: Prompt-size explosion now that stdin "just works" — PROMPT_MAX_BYTES guard | Not implemented (B Surprise #3) | No cap, no env override, no prompt_bytes log field | yes | medium (Risk #4) — unbounded prompt = unbounded child memory and disk | IMPLEMENT-FRESH |
| D-015 | Risk #5: claude CLI behavior change in future Anthropic release | Mitigation = pin version + sidecar replay | Sidecar absent (B Surprise #3); no version-pin doc | yes | medium (Risk #5) — pure runtime dependency on claude CLI behavior | IMPLEMENT-FRESH |
| D-016 | Risk #6: Sidecar file disk-bloat — off by default | Sidecar feature absent entirely | n/a — risk only materializes if sidecar lands | superseded | low (Risk #6) — moot until D-022/D-035 land | DEFER-TO-BEAT-2 |

### 2c. process.py (ClaudeProcess base class) — D-017 … D-045

| ID | Description (≤140 chars) | Already-Implemented? | Partial / Divergent? | Still Needed? | Risk-if-skipped | Recommended action |
|----|--------------------------|----------------------|----------------------|---------------|-----------------|--------------------|
| D-017 | Threshold-based dual-path delivery (argv <96 KiB, stdin ≥96 KiB) | No — current is unconditional stdin since `4799719` (`pipeline/process.py:125-130`) | Always-stdin replaces threshold | superseded | low — chosen architecture differs but is acceptable | SUPERSEDED |
| D-018 | `PROMPT_STDIN_THRESHOLD = 96 * 1024` constant | Not present (B §1) | n/a — no threshold logic | superseded | low | SUPERSEDED |
| D-019 | 32 KiB margin under MAX_ARG_STRLEN — rationale | Rationale-only; relevant only with threshold | Argv carries no prompt bytes at all (`pipeline/process.py:79-95`) | superseded | low | SUPERSEDED |
| D-020 | `PROMPT_MAX_BYTES = 16 MiB` env-overridable constant | Not present | No upper bound on `self.prompt` (B §1) | yes | medium (Risk #4) | IMPLEMENT-FRESH |
| D-021 | `PromptTooLargeForArgv(ValueError)` exception class | Not present | No typed exception | yes | medium (Risk #4) | IMPLEMENT-FRESH |
| D-022 | Constructor adds `prompt_sidecar: bool = False` kwarg | Not present (`pipeline/process.py:37-71` lists 13 kwargs incl. `tool_write_mode`, no `prompt_sidecar`) | Constructor instead grew `tool_write_mode` (`39d5100`) | yes | low (Risk #5/#6) — observability gap when stdin hides prompt from `ps` | DEFER-TO-BEAT-2 |
| D-023 | `_use_stdin_for_prompt()` helper (size-based predicate, empty→argv) | Not present — all paths take stdin (`pipeline/process.py:125-130`) | n/a — predicate is a no-op under always-stdin | superseded | low | SUPERSEDED |
| D-024 | `_prompt_anchor_flag()` returns `--output-format` | Not present — no anchor concept needed because `--add-dir` is just appended | Portify appends instead of splicing (`cli_portify/process.py:213`) | superseded | low | SUPERSEDED |
| D-025 | `_iter_prompt_chunks(64 KiB)` streaming encoder | Not present — `pipeline/process.py:142` is single-shot `prompt.encode("utf-8")` | Full-buffer encode | yes | medium — peak-heap doubling for multi-MB prompts; pipe-buffer interaction | IMPLEMENT-FRESH |
| D-026 | `_join_stdin_writer(timeout=5.0)` invoked from wait/terminate | Not present — no writer thread to join | Synchronous write; `terminate()` at `pipeline/process.py:173-214` does not coordinate with stdin | yes | high (Risk #3 reframed) — parent stall during start() | ADAPT |
| D-027 | Empty prompts stay on argv with `-p ""` | No — empty prompt becomes empty `stdin.write(b"")` + EOF (B Q4) | Different shape; not strictly broken but undefined-by-design | partial | low — claude's reaction to empty stdin not exercised | ADAPT |
| D-028 | Encoding failure routes to stdin path | n/a — no routing branch exists | All prompts go stdin already | superseded | low | SUPERSEDED |
| D-029 | `Popen(stdin=PIPE, stdout=fh, stderr=fh)` for stdin path | Yes — `pipeline/process.py:125-130` exactly this; commit `4799719` | None | no | low | DROP |
| D-030 | Spawn `claude-stdin-writer-<pid>` daemon thread | Not present — synchronous write inline (`pipeline/process.py:140-146`) | No thread | yes | high — see D-026 | ADAPT |
| D-031 | UTF-8 encode each character slice with errors='strict' | Implicit — `prompt.encode("utf-8")` at `pipeline/process.py:142` defaults to strict | Single-shot, not chunked | partial | low — strict default already in effect | KEEP-AS-IS |
| D-032 | `os.write(fd, view)` loop with EINTR retry / BrokenPipe terminate | Not present — uses Python `stdin.write(...)` (`pipeline/process.py:142`); BrokenPipe swallowed silently (`:140-146`) | Single shot, no EINTR loop | yes | medium — silent BrokenPipe can mask real failures | ADAPT |
| D-033 | `finally: stdin.close()` to deliver EOF | Yes for the close — `pipeline/process.py:143` calls close inside try; sufficient under always-stdin since `4799719` | EOF guaranteed by `subprocess.PIPE` close path | no | low — EOF reaches claude | DROP |
| D-034 | Errors stored in `self._stdin_error`; surfaced in join log | Not present — BrokenPipe is silently `pass` (`pipeline/process.py:144-146`) | Failures invisible to caller | yes | medium — masks real failures | IMPLEMENT-FRESH |
| D-035 | If `prompt_sidecar=True`, append chunk to `output_file.with_suffix('.prompt')` | Not present | Sidecar absent | yes | low (Risk #5/#6) | DEFER-TO-BEAT-2 |
| D-036 | Sanity guard: prompts > PROMPT_MAX_BYTES raise PromptTooLargeForArgv pre-spawn | Not present | No size check (B §1) | yes | medium (Risk #4) | IMPLEMENT-FRESH |
| D-037 | `self.prompt` attribute always equals constructor arg (no value erasure) | Yes — `pipeline/process.py:55` stores verbatim; never mutated | Holds | no | low | DROP |
| D-038 | Debug log `cmd[:3]` shape `['claude','--print','--verbose']` unchanged | Yes — `build_command()` lines 79-95 emit those three first | Hard-coded log line in `sprint/process.py:45` would not reflect future changes (B §3 note) | no | low | DROP |
| D-039 | Process group / signals unchanged; `setpgrp` gated by hasattr | Yes — `pipeline/process.py` retains `setpgrp` gating; `terminate()` at `:173-214` uses pgroup when available | None | no | low | DROP |
| D-040 | Cancellation polling unchanged; daemon writer isolates poll loop | Polling unchanged; isolation absent because no writer thread | Synchronous start() can stall before cancellation loop runs | partial | high — see D-026/D-013 | ADAPT |
| D-041 | `build_env()` unchanged; CLAUDECODE/CLAUDE_CODE_ENTRYPOINT stripping | Yes — preserved across `4799719`; `c4fa7f4` added `env_vars` param without disturbing strip logic | None | no | low | DROP |
| D-042 | Prompts in [98,304…16,777,215] take stdin path with PIPE | Stdin used for ALL sizes (no threshold) | Wider envelope than DESIGN | superseded | low | SUPERSEDED |
| D-043 | All current callers/subclasses untouched at constructor level | Mostly true; `tool_write_mode` (`39d5100`) added a new ctor kwarg with safe default | Constructor expanded post-design | partial | low — defaults preserve callers | KEEP-AS-IS |
| D-044 | Rationale: avoid `proc.communicate()` due to cancellation polling | Decision honored — code uses `Popen` + manual stdin manage (`pipeline/process.py:125-146`) | None | no | low | DROP |
| D-045 | Rationale: 64 KiB pipe buffer; writer thread isolates poll loop | Decision rejected in current code — synchronous write on parent thread | Stall risk recurs | yes | high (Risk #3 reframed) | ADAPT |

### 2d. cli_portify/process.py (PortifyProcess) — D-046 … D-049

| ID | Description (≤140 chars) | Already-Implemented? | Partial / Divergent? | Still Needed? | Risk-if-skipped | Recommended action |
|----|--------------------------|----------------------|----------------------|---------------|-----------------|--------------------|
| D-046 | Replace `cmd.index('-p')` with anchor on `--output-format` | Not implemented — `cli_portify/process.py:208-213` still references `-p` (silently dead) | Falls into `except ValueError` 100% of time | yes | medium (Risk #2) | ADAPT |
| D-047 | Anchor strategy yields byte-identical argv for small prompts and works for large | Layout currently differs (appended at end); functionally OK but doesn't match design | Argv layout intent broken | yes | low — claude accepts `--add-dir` positionally | ADAPT |
| D-048 | Portify subclass: 2-line tweak in build_command | Not done; current override is 3 lines of dead try/except | Trivial-cost refactor | yes | low | ADAPT |
| D-049 | Pin contract test: `--output-format` and value adjacent in argv | Existing tests cover adjacency for the base (`tests/pipeline/test_process.py:17-37`) but not as Portify-anchor-contract | Partial coverage (D §3 row 14) | yes | low — but valuable as argv-shape pin | IMPLEMENT-FRESH |

### 2e. Tests (DESIGN.md §9.1) — D-050 … D-069

| ID | Description (≤140 chars) | Already-Implemented? | Partial / Divergent? | Still Needed? | Risk-if-skipped | Recommended action |
|----|--------------------------|----------------------|----------------------|---------------|-----------------|--------------------|
| D-050 | `test_build_command_keeps_p_flag_for_small_prompt` | No — opposite is pinned (`tests/pipeline/test_process.py:54`) | Conflicts with current always-stdin contract | superseded | low | SUPERSEDED |
| D-051 | `test_build_command_omits_p_flag_for_large_prompt` | Yes for ALL sizes — `tests/pipeline/test_process.py:54, :176-177` | Broader than design intent | no | low | DROP |
| D-052 | `test_argv_total_byte_size_bounded_for_huge_prompt` | Not present (D §3 row 3) | Implicitly bounded by no-prompt-on-argv | yes | low — invariant currently structural; test pins it | IMPLEMENT-FRESH |
| D-053 | `test_threshold_boundary_under` (95 KiB → argv) | No — no threshold | n/a | superseded | low | SUPERSEDED |
| D-054 | `test_threshold_boundary_over` (97 KiB → stdin) | No — no threshold | n/a | superseded | low | SUPERSEDED |
| D-055 | `test_empty_prompt_uses_argv_with_empty_p_value` | No — empty prompt = empty stdin write (B Q4) | Inverse contract | superseded | low | SUPERSEDED |
| D-056 | `test_huge_prompt_delivered_via_stdin` | Yes — `tests/pipeline/test_process.py:200-219` (200 KB) | None | no | low | DROP |
| D-057 | `test_small_prompt_still_uses_argv` | No — small still uses stdin | n/a under always-stdin | superseded | low | SUPERSEDED |
| D-058 | `test_huge_utf8_emoji_prompt_round_trip` (200 KB multibyte) | Not present (D §3 row 9) | UTF-8 path tested via ASCII only | yes | low — multibyte regression surface | IMPLEMENT-FRESH |
| D-059 | `test_prompt_max_bytes_guard` | Not present — no PROMPT_MAX_BYTES (D §3 row 10) | Cap absent | yes | medium (Risk #4) | IMPLEMENT-FRESH |
| D-060 | `test_terminate_during_stdin_write_no_hang` | Not present (D §3 row 11) | No writer thread; need a stall-resistance test instead | yes | high (Risk #3 reframed) | ADAPT |
| D-061 | `test_portify_add_dir_insertion_unchanged_for_small_prompt` | Partial — `tests/cli_portify/test_process.py:392-418` symmetric vs current baseline | Doesn't test "before -p" anchor | yes | low | ADAPT |
| D-062 | `test_portify_add_dir_insertion_works_for_large_prompt` | Not present (D §3 row 13) | n/a today | yes | low | IMPLEMENT-FRESH |
| D-063 | `test_output_format_flag_and_value_are_adjacent` | Yes — `tests/pipeline/test_process.py:17-37` | None | no | low | DROP |
| D-064 | `test_prompt_sidecar_written_when_opted_in` | Sidecar feature absent | n/a | yes | low (Risk #5/#6) | DEFER-TO-BEAT-2 |
| D-065 | `test_no_sidecar_by_default` | Sidecar feature absent | n/a | yes | low | DEFER-TO-BEAT-2 |
| D-066 | Run via `uv run pytest tests/cli/pipeline/...` per UV-only rule | Project policy in CLAUDE.md; current tests live at `tests/pipeline/` | Path differs from DESIGN.md `tests/cli/pipeline/` | partial | low — choose one path | ADAPT |
| D-067 | CI integration via .github actions, no one-off scripts | Repo policy | Existing pipeline workflow runs `make test` | yes | low | IMPLEMENT-FRESH |
| D-068 | New fixtures: small/empty/boundary/huge/emoji prompts | Discrete sizes exist (D §4 Q5); not parametrized | Some sizes already exercised | partial | low | ADAPT |
| D-069 | Mock claude bash stand-in: `echo ARGV >&2; cat` | `tests/pipeline/test_process.py` uses Python stand-in (`sys.executable -c "..."`); equivalent | Different language, same shape | no | low | KEEP-AS-IS |

### 2f. Observability / Logging — D-070 … D-074

| ID | Description (≤140 chars) | Already-Implemented? | Partial / Divergent? | Still Needed? | Risk-if-skipped | Recommended action |
|----|--------------------------|----------------------|----------------------|---------------|-----------------|--------------------|
| D-070 | Existing `_log.debug('spawn pid=%d cmd=%s', ...)` preserved | Preserved across `4799719`; sprint hook also logs cmd at `sprint/process.py:45` (hard-coded) | Sprint log is frozen string (B §3) | no | low | KEEP-AS-IS |
| D-071 | New debug fields: `prompt_via=stdin\|argv`, `prompt_bytes=N`, `sidecar=bool` | Not present (B §1) | No size telemetry | yes | low — operational blind spot | IMPLEMENT-FRESH |
| D-072 | `.prompt` sidecar file for "what did claude see?" replay | Not present | Sidecar absent | yes | low (Risk #5) | DEFER-TO-BEAT-2 |
| D-073 | Caller policy: roadmap opts in to sidecar, sprint/audit opt out | Not applicable until D-072 lands | n/a | yes | low | DEFER-TO-BEAT-2 |
| D-074 | `ps` no longer shows prompt for stdin path — security improvement | True today as a side-effect of `4799719` | None | no | low | KEEP-AS-IS |

### 2g. Rollout / Deployment — D-075 … D-087

| ID | Description (≤140 chars) | Already-Implemented? | Partial / Divergent? | Still Needed? | Risk-if-skipped | Recommended action |
|----|--------------------------|----------------------|----------------------|---------------|-----------------|--------------------|
| D-075 | Threshold-based design rollback-friendly via constant tweak | n/a — no threshold; rollback mechanism is `git revert 4799719` | Different rollback shape | superseded | low | SUPERSEDED |
| D-076 | Emergency rollback via revert; no caller migration | Mechanism is `git revert` of `4799719` | Effective, but reverting also undoes the always-stdin migration entirely | partial | low — operational note | KEEP-AS-IS |
| D-077 | Vendored monkey-patch in consumer repo `.dev/claude_process_stdin_patch.py` | Not present in this repo; would target the consumer-side wrapper | Consumer-repo only; out-of-scope here | partial | medium — consumer repo unblock pathway | DEFER-TO-BEAT-2 |
| D-078 | Apply diff to src/, add tests, sync-dev, verify-sync, PR with DESIGN.md | Branch exists; only design import (`530955b`) so far | Patch not yet applied; tests not yet added | yes | high — entire delivery contract | IMPLEMENT-FRESH |
| D-079 | P0 release-gate stdin probe — DONE 2026-04-30 | Yes; closed | None | no | low | DROP |
| D-080 | P1 — Apply patch to pipeline/process.py per §4-§6 | Already mostly delivered by `4799719`; threshold portion superseded | Need only the gap: size cap + observability | partial | medium | ADAPT |
| D-081 | P2 — 2-line PortifyProcess tweak per §6.3 | Not done; dead `cmd.index("-p")` remains | Targeted refactor | yes | medium (Risk #2) | ADAPT |
| D-082 | P3 — Add tests per §9 to `tests/cli/pipeline/test_claude_process_delivery.py` | Existing tests live in `tests/pipeline/test_process.py`; new file path differs | Several §9.1 cases need new tests (D §5) | yes | high — gates AC-10 | IMPLEMENT-FRESH |
| D-083 | P4 — `make sync-dev && make verify-sync && make test` | Process gate | n/a yet | yes | medium — repo policy | IMPLEMENT-FRESH |
| D-084 | P5 — Open upstream PR with DESIGN.md attached | Not yet — branch is design-import only | n/a yet | yes | low | IMPLEMENT-FRESH |
| D-085 | P6 — Vendored monkey-patch in consumer repo (parallel) | Out-of-scope for this repo | Consumer-side | partial | medium | DEFER-TO-BEAT-2 |
| D-086 | P7 — Re-run failing roadmap pipeline end-to-end with 338 KB prompt | Not yet validated post-merge | E2E gate | yes | high — original bug repro must be confirmed fixed | IMPLEMENT-FRESH |
| D-087 | Vendored monkey-patch and upstream PR proceed in parallel | Strategy doc only | n/a yet | partial | low | DEFER-TO-BEAT-2 |

### 2h. Other (compatibility, beat-2, scope, open Qs) — D-088 … D-110

| ID | Description (≤140 chars) | Already-Implemented? | Partial / Divergent? | Still Needed? | Risk-if-skipped | Recommended action |
|----|--------------------------|----------------------|----------------------|---------------|-----------------|--------------------|
| D-088 | Files modified: pipeline/process.py (~+95 LOC), cli_portify/process.py (+5/-4) | `pipeline/process.py` already at 244 LOC post-`4799719`/`39d5100`; cli_portify untouched | Effective LOC delta now smaller | partial | low | ADAPT |
| D-089 | Files added: tests/cli/pipeline/conftest.py (extend), test_claude_process_delivery.py (new) | Path doesn't exist; current home is `tests/pipeline/` | Pick the right home | yes | low | ADAPT |
| D-090 | NOT modified: roadmap/executor.py — keep `_EMBED_SIZE_LIMIT` warning (advisory) in beat 1 | True today — `cli/roadmap/executor.py:1075-1081` still warns | None | no | low | KEEP-AS-IS |
| D-091 | Other callers (validate_executor, remediate_executor, tasklist, sprint) NOT modified | True (B caller analysis) | None | no | low | KEEP-AS-IS |
| D-092 | Sprint and audit subclasses NOT modified — inherit new behavior | True (B §3, §4); `sprint/process.py` adds env_vars only; `cleanup_audit/process.py` unchanged | Note: `cleanup_audit/executor.py` calls non-existent `is_running()`/`stop()` (B Surprise #7) — pre-existing | no | low (orthogonal bug) | KEEP-AS-IS |
| D-093 | Beat-2: introduce `pre_prompt_args` mechanism; delete Portify build_command override | Not done | Future scope | no | low | DEFER-TO-BEAT-2 |
| D-094 | Beat-2: promote stdin to default for all sizes once sidecar mature | Already true (default became always-stdin via `4799719`); sidecar still missing | Step 1 done out of order | partial | low | KEEP-AS-IS |
| D-095 | Beat-2: `--input-format=stream-json` delivery for tool-use | Not done | Future scope | no | low | DEFER-TO-BEAT-2 |
| D-096 | Beat-2: automated rotation/cleanup of `.prompt` sidecars | Not done — sidecar absent | Future scope | no | low | DEFER-TO-BEAT-2 |
| D-097 | Beat-2: optional `PromptSource` Protocol if 2nd source ships | Not done | Future scope | no | low | DEFER-TO-BEAT-2 |
| D-098 | Open Q3: per-caller threshold override (`force_prompt_via`) — out of scope | Open question | n/a — no threshold to override | superseded | low | DEFER-TO-BEAT-2 |
| D-099 | Open Q4: `prompt_bytes=N` in production logs — compliance signal? | Not yet emitted (D-071 absent) | Decide before D-071 lands | yes | low | IMPLEMENT-FRESH |
| D-100 | Open Q5: downgrade `_EMBED_SIZE_LIMIT` warnings to debug — defer | Status quo retained — still WARN at `cli/roadmap/executor.py:1075-1081` | None | no | low | KEEP-AS-IS |
| D-101 | Open Q1 (resolved): claude reads stdin without positional arg — YES | Yes — closed | None | no | low | DROP |
| D-102 | Open Q2 (resolved): trailing newline / framing required — NO | Yes — closed | None | no | low | DROP |
| D-103 | NUL-in-prompt: argv truncates, stdin preserves — latent improvement | Yes — current always-stdin gets the improvement for free | None | no | low | KEEP-AS-IS |
| D-104 | Windows portability: hasattr-gating already in place | Yes — `pipeline/process.py` retains hasattr gating for setpgrp/getpgid/killpg | None | no | low | KEEP-AS-IS |
| D-105 | Late `self.prompt` mutation observed — caveat emptor | True under current code; `pipeline/process.py:142` reads `self.prompt` lazily in start | None | no | low | KEEP-AS-IS |
| D-106 | Re-entrant start() — pre-existing UB; patch unchanged | True | None | no | low | KEEP-AS-IS |
| D-107 | Stream chunks vs full-buffer encode — chunking saves heap on multi-MB | Full-buffer encode in place (B §1, line 142) | Same as D-025 | yes | medium — peak heap doubled for multi-MB prompts | IMPLEMENT-FRESH |
| D-108 | EOF: stdin.close() in finally — non-negotiable | Yes — `pipeline/process.py:143` closes stdin (inside try/except BrokenPipeError) | Close is in try, not finally — slight divergence; works because BrokenPipe is the only caught exception | partial | low — close still happens for normal path | ADAPT |
| D-109 | Mode comparison: only Threshold-stdin selected (rejecting Always-stdin) | Current code chose **Always-stdin** — opposite of DESIGN.md decision | Architectural divergence | superseded | low | SUPERSEDED |
| D-110 | NamedTemporaryFile cleanup on crash — N/A (no temp file) | True — current code uses no temp file | None | no | low | KEEP-AS-IS |

---

## 3. Verdicts Summary

**Authoritative action-label counts (from §2 matrix cells):**

| Action | Count | IDs |
|--------|-------|-----|
| DROP | 15 | D-008, D-011, D-029, D-033, D-037, D-038, D-039, D-041, D-044, D-051, D-056, D-063, D-079, D-101, D-102 |
| KEEP-AS-IS | 16 | D-031, D-043, D-069, D-070, D-074, D-076, D-090, D-091, D-092, D-094, D-100, D-103, D-104, D-105, D-106, D-110 |
| ADAPT | 23 | D-001, D-003, D-005, D-012, D-013, D-026, D-027, D-032, D-040, D-046, D-047, D-048, D-060, D-061, D-066, D-068, D-080, D-081, D-088, D-089, D-108 (and D-007/D-014 which split — see cell labels), with D-066, D-068 carrying ADAPT — see source-of-truth table cells |
| IMPLEMENT-FRESH | 25 | D-006, D-007, D-009, D-010, D-014, D-015, D-020, D-021, D-025, D-034, D-036, D-049, D-052, D-058, D-059, D-062, D-067, D-071, D-078, D-082, D-083, D-084, D-086, D-099, D-107 |
| DEFER-TO-BEAT-2 | 15 | D-016, D-022, D-035, D-064, D-065, D-072, D-073, D-077, D-085, D-087, D-093, D-095, D-096, D-097, D-098 |
| SUPERSEDED | 16 | D-002, D-004, D-017, D-018, D-019, D-023, D-024, D-028, D-042, D-050, D-053, D-054, D-055, D-057, D-075, D-109 |
| **Total** | **110** | matches C's count ✓ |

**AC coverage:** AC-1 (D-001) ADAPT, AC-2 (D-002) SUPERSEDED, AC-3 (D-003) ADAPT, AC-4 (D-004) SUPERSEDED, AC-5 (D-005) ADAPT, AC-6 (D-006) IMPLEMENT-FRESH, AC-7 (D-007) IMPLEMENT-FRESH, AC-8 (D-008) DROP, AC-9 (D-009) IMPLEMENT-FRESH, AC-10 (D-010) IMPLEMENT-FRESH. **All 10 covered.** ✓

**Risk coverage:** Risk #1 (D-011) DROP, Risk #2 (D-012) ADAPT, Risk #3 (D-013) ADAPT, Risk #4 (D-014) IMPLEMENT-FRESH, Risk #5 (D-015) IMPLEMENT-FRESH, Risk #6 (D-016) DEFER-TO-BEAT-2. **All 6 covered.** ✓

---

## 4. Surprises (current state vs DESIGN.md)

### 4.1 `tool_write_mode` (introduced `39d5100`, Apr 18 2026)

A `tool_write_mode: bool = False` constructor parameter on `ClaudeProcess` (`/config/workspace/IronClaude/src/superclaude/cli/pipeline/process.py:53,68`) plus a `validate_tool_write_output()` method (`:216-236`). When True, `start()` redirects stdout to `output_file.with_suffix(".log")` (`:118-122`) because the LLM is expected to write the real artifact via the Write tool. Wired by the roadmap executor at `cli/roadmap/executor.py:1117` (and step definitions at `:1927, :1945, :2008`). DESIGN.md does not mention this parameter. Any patch that re-declares `__init__` or rewrites `start()` per DESIGN.md verbatim will silently regress `tool_write_mode`. Test coverage is **zero** (D §4 Q7).

### 4.2 Hooks parameter (introduced `a606727`, Mar 6 2026)

`on_spawn`, `on_signal`, `on_exit` callable hooks on the `ClaudeProcess` ctor (`pipeline/process.py:49-51`), invoked from `start()` (`:148-149`), `terminate()` (`:183-184, :212-213`), and `wait()` (`:168-169`). DESIGN.md's writer-thread proposal (D-030) and `_join_stdin_writer` (D-026) must coexist with these; specifically, SIGKILL escalation in `terminate()` (`:197-203`) does **not** call `on_signal` again — a latent observability gap that is already in tree, unrelated to stdin.

### 4.3 `env_vars` parameter (introduced `c4fa7f4`, Mar 16 2026)

`env_vars: dict[str, str] | None = None` on the ctor (`pipeline/process.py:52`), threaded through `build_env()` for preflight context injection. DESIGN.md treats `build_env()` as unchanged (D-041), which remains true, but any constructor reshaping must preserve this kwarg.

### 4.4 `cleanup_audit/executor.py` calls undefined `is_running()` / `stop()`

Pre-existing bug: `cli/cleanup_audit/executor.py:91, :93, :97` invokes methods that are not defined on `CleanupAuditProcess` or the base `ClaudeProcess` (B §4, B Q ... and Surprise #7). The audit executor would raise `AttributeError` on its first iteration. Orthogonal to stdin work but worth surfacing — it indicates the audit pipeline has not been exercised end-to-end recently, which limits the value of any "all callers green" claim attached to AC-10.

### 4.5 `SignalHandler` API drift between sprint and cleanup_audit

`sprint/process.py:241` exposes `uninstall()`; `cleanup_audit/process.py:64` exposes `restore()` (B Surprise #8). Same role, different name. DESIGN.md does not address either.

### 4.6 `extra_args` already present on the constructor

`extra_args: list[str] | None = None` (`pipeline/process.py:48`) is appended verbatim into argv (`:94`). This means callers can already inject flags without subclassing — relevant to D-022 `prompt_sidecar` discussion: the design proposed a new kwarg, but the right shape today might be a `prompt_sidecar` opt-in via env or a sidecar mode added directly rather than another constructor knob.

### 4.7 PortifyProcess `cmd.index("-p")` is silently dead code

`cli_portify/process.py:208-213` (B Q1, B Surprise #5) — the lookup raises ValueError every time and `--add-dir` lands at the end of argv. The argv layout no longer matches the DESIGN.md anchor strategy. This is the most concrete latent regression in the current state.

---

## 5. Risks newly introduced or unmitigated by `4799719`

### 5.1 Synchronous stdin write blocks parent `start()` on full pipe buffer (HIGH)

`pipeline/process.py:140-146` performs a single synchronous `self._process.stdin.write(self.prompt.encode("utf-8"))` on the parent thread. Linux pipe buffer is typically 64 KiB. For a 338 KB prompt where claude is slow to consume stdin, the parent's `start()` itself stalls until claude drains the pipe. The deadlock-safety docstring (`:137-139`) addresses 4-way pipe deadlock (which is genuinely impossible because stdout/stderr are real file FDs), but **does not address parent-thread stall**. The cancellation poll loop in roadmap/executor.py runs after `start()` returns, so a stalled `start()` never reaches the poll loop. Severity: HIGH. Maps to DESIGN Risk #3 reframed.

### 5.2 Full-buffer encode without chunking (MEDIUM)

`pipeline/process.py:142` encodes the entire prompt in one shot via `self.prompt.encode("utf-8")`. For multi-MB prompts (audit-pipeline composition, future workflows), peak heap doubles. DESIGN.md `_iter_prompt_chunks(64 KiB)` (D-025, D-031, D-107) addresses this; not implemented. Severity: MEDIUM.

### 5.3 No size cap / no `PromptTooLargeForArgv` (MEDIUM, Risk #4)

`pipeline/process.py` has no `PROMPT_MAX_BYTES` constant and no pre-spawn guard. A pathological caller could supply gigabyte prompts; the OS will eventually OOM the child claude. Severity: MEDIUM. Maps to DESIGN Risk #4.

### 5.4 BrokenPipeError swallowed silently — masks real failures (MEDIUM)

`pipeline/process.py:140-146` wraps the stdin write in `try ... except BrokenPipeError: pass` with no logging, no `self._stdin_error` capture, no surfacing. If claude exits early because it couldn't parse the prompt, the parent sees only the eventual non-zero exit code and has to reconstruct what happened from the error log. DESIGN.md D-034 addresses this via `self._stdin_error` + `_join_stdin_writer()` log line. Severity: MEDIUM.

### 5.5 Empty-prompt behavior is undefined-by-design (LOW)

B Q4: empty prompt → `stdin.write(b"")` + close → claude receives EOF with zero bytes. Behavior depends on claude's own handling. DESIGN.md row 1 of §6.1 expected `-p ""` + DEVNULL stdin, which is no longer the path. No defensive guard. Severity: LOW (claude appears to tolerate it; not exercised in tests).

### 5.6 `cli_portify/process.py:210` `cmd.index("-p")` is dead code (LOW-MEDIUM, Risk #2)

Always falls into `except ValueError` and appends `--add-dir` at the end (B §1, B Q1). Functionally OK because claude accepts `--add-dir` positionally, but the splice-point semantics from DESIGN.md §6.3 are not preserved, and the comment is misleading. Severity: LOW-MEDIUM. Maps to DESIGN Risk #2.

### 5.7 `start()` close path uses `try` rather than `finally` (LOW)

`pipeline/process.py:143` calls `stdin.close()` inside the try block, not in a `finally`. For the BrokenPipeError path it still closes (the close is before the except), but if a future change introduced a different exception class (e.g., OSError) above the BrokenPipeError handler, EOF would not be guaranteed. DESIGN.md D-033/D-108 specifies `finally`. Severity: LOW.

### 5.8 `start()` cannot be cancelled while stdin write is blocked (HIGH)

Combined with 5.1: because `start()` itself blocks during `stdin.write()` for a slow child, the executor's `terminate()` running on a different thread would race against `start()` completion. Without a daemon writer thread (D-030) and `_join_stdin_writer()` (D-026), there is no clean cancellation point. Severity: HIGH. Same root cause as 5.1.

---

## 6. Risks resolved by `4799719` (sanity check)

### 6.1 Risk #1 (DESIGN.md §11 row 1) — pinned claude won't read stdin without positional arg

Verified resolved by the P0 probe on 2026-04-30 (`claude 2.1.123`). `4799719` was authored on the assumption this would hold and the probe confirmed it after-the-fact. The migration shipped without rollback.

### 6.2 The original `argv too long` (E2BIG) failure mode at 128 KiB

Pre-`4799719` code passed prompts via `-p <prompt>` argv pair (commit `6548f17`'s argv shape). Linux `MAX_ARG_STRLEN = 128 KiB` per-argument ceiling caused `Popen` to fail with `OSError: [Errno 7] Argument list too long` for prompts larger than 128 KB. `4799719` removed `-p` from argv entirely; the failure mode is mechanically eliminated for any reasonable prompt size. Verified by `tests/pipeline/test_process.py:200-219` (200 KB round-trip).

### 6.3 The `ps`/`/proc/<pid>/cmdline` prompt visibility issue

`4799719` makes prompts invisible to `ps`. DESIGN.md D-074 / merged-output §6 case #11 calls this an intentional security improvement. Resolved as a side-effect.

---

## 7. Branch Strategy Recommendation

**Recommendation: continue on the existing `fix/claude-process-stdin-large-prompts` branch (off `feat/tdd-spec-merge`).**

Rationale: agent A established `master` tip == merge-base `4e0c621` (Mar 24 2026), meaning `master` has not advanced since divergence. The two load-bearing commits — `39d5100` (`tool_write_mode`, Apr 18) and `4799719` (stdin migration, Apr 20) — both live on `feat/tdd-spec-merge` and are absent from `master`. Rebasing the delta to `master` would (a) lose `tool_write_mode` and force re-implementation, (b) lose `4799719`'s stdin migration which is the foundation everything else builds on, and (c) waste the verified P0 probe and the existing always-stdin tests at `tests/pipeline/test_process.py:156-234`. Since `master` is dormant and `feat/tdd-spec-merge` is the live integration branch, keeping the delta on `fix/claude-process-stdin-large-prompts` (current branch, only `530955b` design-import commit added so far) means the eventual PR target is `feat/tdd-spec-merge`, the merge brings cap/observability/Portify-anchor-fix on top of the already-shipped stdin migration, and the upstream PR (D-084) ultimately targets master via the existing integration flow. A different new branch would only be warranted if we wanted to also revert `4799719` and ship the threshold-based DESIGN.md verbatim — which both code state and test state argue against (see §3 SUPERSEDED bucket).

---

## 8. Carry-Forward Provenance Map

For each ADAPT or IMPLEMENT-FRESH row, the adversarial provenance from C's index. Phase 3 should cite these IDs back to the debate transcript when justifying each delta.

| D-NNN | Action | Adversarial provenance |
|-------|--------|-----------------------|
| D-001 | ADAPT | C-007 (B), C-001 (A) — merged threshold + streaming |
| D-003 | ADAPT | X-001 (A) — margin sizing |
| D-005 | ADAPT | INV-002 (HIGH ADDRESSED) |
| D-006 | IMPLEMENT-FRESH | Change #4 (B§8.2) — UTF-8 multibyte |
| D-007 | IMPLEMENT-FRESH | U-003 (B), U-001 (A) — typed error + size cap |
| D-009 | IMPLEMENT-FRESH | DESIGN-NEW (project policy) |
| D-010 | IMPLEMENT-FRESH | DESIGN-NEW (project policy) |
| D-012 | ADAPT | C-003 (A), X-002 (A) — Portify anchor |
| D-013 | ADAPT | INV-002 (ADDRESSED) — reframed for synchronous-write stall |
| D-014 | IMPLEMENT-FRESH | U-001 (A) — PROMPT_MAX_BYTES; U-003 (B) — typed error |
| D-015 | IMPLEMENT-FRESH | U-004 (B) — sidecar; partial |
| D-020 | IMPLEMENT-FRESH | U-001 (A only, 95%) |
| D-021 | IMPLEMENT-FRESH | U-003 (B only, 90%) — Change #1 |
| D-025 | IMPLEMENT-FRESH | C-007 (B 75%) — Change #3 |
| D-026 | ADAPT | INV-002, A's writer-thread lifecycle |
| D-027 | ADAPT | X-003 (B 75%) — Change #5 |
| D-032 | ADAPT | C-004 (A 85%) — os.write over BufferedWriter |
| D-034 | IMPLEMENT-FRESH | A§3.3 — error surfacing |
| D-036 | IMPLEMENT-FRESH | U-001 (A) + U-003 (B) — pre-spawn cap |
| D-040 | ADAPT | merged-output §5 — cancellation isolation |
| D-046 | ADAPT | C-003, X-002, U-002 (A) — Portify anchor |
| D-047 | ADAPT | C-003, X-002 |
| D-048 | ADAPT | C-003 (A 65%) |
| D-049 | IMPLEMENT-FRESH | DESIGN-NEW (test contract for U-002) |
| D-052 | IMPLEMENT-FRESH | X-001 (A) — argv byte-size bound |
| D-058 | IMPLEMENT-FRESH | Change #4 (B§8.2) — emoji round-trip |
| D-059 | IMPLEMENT-FRESH | U-001 (A) + U-003 (B) — guard test |
| D-060 | ADAPT | INV-002 — reframed mid-stdin-write |
| D-061 | ADAPT | C-003 — Portify regression |
| D-062 | IMPLEMENT-FRESH | C-003, X-002 — large-prompt Portify |
| D-066 | ADAPT | DESIGN-NEW — test path |
| D-067 | IMPLEMENT-FRESH | DESIGN-NEW — CI gate |
| D-068 | ADAPT | C-001, X-003, Change #4 — fixtures |
| D-071 | IMPLEMENT-FRESH | DESIGN-NEW — debug fields |
| D-078 | IMPLEMENT-FRESH | DESIGN-NEW + S-005 (B 65%) |
| D-080 | ADAPT | DESIGN-NEW — partial since `4799719` shipped |
| D-081 | ADAPT | C-003, U-002 — Portify tweak |
| D-082 | IMPLEMENT-FRESH | DESIGN-NEW — test additions |
| D-083 | IMPLEMENT-FRESH | project policy (CLAUDE.md) |
| D-084 | IMPLEMENT-FRESH | DESIGN-NEW — upstream PR |
| D-086 | IMPLEMENT-FRESH | original bug repro (338 KB E2E) |
| D-088 | ADAPT | DESIGN-NEW — scope reshape |
| D-089 | ADAPT | DESIGN-NEW — test path reshape |
| D-099 | IMPLEMENT-FRESH | DESIGN-NEW — open question on logs |
| D-107 | IMPLEMENT-FRESH | C-007 (B 75%) — chunking |
| D-108 | ADAPT | INV-002 — finally-close |

---

**End of E-reconciliation-matrix.md**
