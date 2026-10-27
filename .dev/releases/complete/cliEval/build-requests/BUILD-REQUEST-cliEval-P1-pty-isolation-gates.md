# BUILD REQUEST: cliEval-P1 — Vendored ptytest + HomeIsolation + Capability Gates + `eval doctor`

## What This Is

Phase 1 of the **cliEval release** — a real-world eval harness for IronClaude's hook system. This phase is the **viability gate**: if vendored `ptytest` can drive a real Claude Code TTY subprocess and `HomeIsolation` provides clean per-eval `HOME` isolation, the rest of the harness is straightforward. If this phase fails, the architecture pivots.

The task file MUST produce a working `superclaude eval doctor` subcommand that prints a green-checklist verification of all hard requirements (claude binary, make, jq, git) and optional capabilities (3 MCP servers).

## Why It Matters

PR #49 (merged 2026-05-18) introduced detection for hook drift (sync-orphans, installer-orphans, matcher↔case-body inconsistency). But unit tests cannot validate **real-world hook lifecycle** — e.g., that a real `mcp__auggie-mcp__ask_question` MCP call actually triggers `auggie-flag-clear.sh` to clear the sticky in `~/.claude/state/auggie-first-pending/<sid>.txt` and append a `sticky_cleared` event to `~/.claude/logs/auggie-first.jsonl`.

This phase lays the foundation: a PTY driver, per-eval HOME isolation, capability gates, and the diagnostic subcommand. Phase 2/3/4 build on top.

## Inputs (read before starting)

- **Design spec:** `.dev/releases/current/cliEval/design-spec.md` — full architecture. Read §2 (component architecture), §3 (directory layout), §7 (HomeIsolation), §11 (capability gating), §13 (fork strategy).
- **Decisions log:** `.dev/releases/current/cliEval/decisions.md` — read D-1 (PTY layer = fork ptytest) and D-3 (HomeIsolation composes IsolationLayers).
- **Existing primitive to compose:** `src/superclaude/cli/sprint/executor.py:107-182` `IsolationLayers` — read this; do NOT modify.
- **Existing primitive for reference:** `src/superclaude/cli/install_hooks.py:install_hooks` — call this from `HomeIsolation.setup()` to populate per-eval HOMEs.
- **Existing primitive to mirror:** `src/superclaude/cli/prd/` (sub-package layout); `src/superclaude/cli/pipeline/process.py:24-150` `ClaudeProcess` (subprocess driver scaffolding).
- **Upstream to fork:** `https://github.com/brandon-fryslie/ptytest` — MIT, Python 3.8+. Vendor under `src/superclaude/cli/eval/pty/`. Preserve LICENSE verbatim.

## Scope (what THIS task builds)

### Files to create

1. `src/superclaude/cli/eval/__init__.py` — exports `eval_group` (the Click group; commands themselves arrive in P2/P3)
2. `src/superclaude/cli/eval/config.py` — `EvalConfig` dataclass (paths, defaults)
3. `src/superclaude/cli/eval/pty/__init__.py` — vendored ptytest fork entry point
4. `src/superclaude/cli/eval/pty/driver.py` — `PtyDriver` class (was upstream `PtySession`)
5. `src/superclaude/cli/eval/pty/stream.py` — ANSI strip + line buffering (was upstream `_stream.py`)
6. `src/superclaude/cli/eval/pty/LICENSE` — upstream MIT verbatim
7. `src/superclaude/cli/eval/pty/PROVENANCE.md` — fork SHA, what was changed, why
8. `src/superclaude/cli/eval/isolation.py` — `HomeIsolation` (composes `IsolationLayers`)
9. `src/superclaude/cli/eval/capability_gates.py` — `Capability` dataclass + `CAPABILITIES` registry + `check_all()`
10. `src/superclaude/cli/eval/commands.py` — Click group with ONLY `eval doctor` subcommand (others land in P2/P3)
11. `tests/cli/test_eval/__init__.py`
12. `tests/cli/test_eval/test_isolation.py` — HOME override correctness; setup/teardown idempotence
13. `tests/cli/test_eval/test_capability_gates.py` — all gates, including missing-binary failure modes
14. `tests/cli/test_eval/test_pty_vendor.py` — vendored ptytest still passes upstream's own tests after our diffs

### Acceptance criteria (per design-spec §7, §11, §13)

- **AC-P1.1:** `uv run superclaude eval doctor` prints a green-checklist for: `claude`, `make`, `jq`, `git` binaries + 3 MCP servers (reachable / unreachable). Exit 0 if all hard requirements met; exit 2 if any hard requirement missing.
- **AC-P1.2:** `HomeIsolation(eval_id="P1-smoke")` produces a unique tempdir under `home_root`; `setup()` deploys 9 hook scripts + writes settings.json + seeds requested state files; `env()` returns dict with `HOME`, `XDG_*`, `CLAUDE_SESSION_ID`, plus passthrough of `PATH`, `USER`, `TERM`, `LANG`, `CI`; `teardown(keep=False)` rm -rf's the dir.
- **AC-P1.3:** `PtyDriver.spawn("claude", env=...)` returns a usable driver; `.expect_prompt_ready(timeout=30)` blocks until Claude Code is interactive-ready; `.inject_prompt("hello")` sends text + CR-LF; `.read_until(pattern)` captures output. `.terminate()` kills cleanly.
- **AC-P1.4:** Vendored ptytest's own test suite (whatever upstream ships) passes under `uv run pytest tests/cli/test_eval/test_pty_vendor.py`.
- **AC-P1.5:** PROVENANCE.md documents: upstream URL, fork SHA, rename `PtySession → PtyDriver`, removed pytest-fixture autoloader, added `expect_prompt_ready` + `inject_prompt`, tightened pexpect to `>=4.9`, aggressive ANSI strip.
- **AC-P1.6:** Hard guard in `HomeIsolation.setup()` REFUSES to operate if `home_root` is outside a known eval-runs scratch dir (e.g., `/tmp/eval-runs/...` or `.dev/eval-runs/...`). Prevents foot-gun where a typo blows away the real `~/.claude/`.
- **AC-P1.7:** `make verify-sync` still EXIT=0 after this phase lands (no regression).
- **AC-P1.8:** All new tests pass: `uv run pytest tests/cli/test_eval/test_isolation.py tests/cli/test_eval/test_capability_gates.py tests/cli/test_eval/test_pty_vendor.py -v` → all PASS.

### Out of scope for THIS task (deferred to P2/P3/P4)

- `eval run`, `eval list`, `eval describe` subcommands
- YAML manifest loader
- Expect.* assertion DSL
- Run orchestrator (ThreadPoolExecutor scheduling)
- `Reporter` / `AggregatedRunReport`
- Wiring into `cli/main.py` (P4 only)

## Naming convention

- Task file path: `.dev/tasks/to-do/TASK-RF-20260518-cliEval-P1-pty-isolation-gates/TASK-RF-20260518-cliEval-P1-pty-isolation-gates.md`
- Branch (for execution): `feat/cliEval-P1-pty-isolation-gates`
- PR title (when ready): `feat(eval): cliEval P1 — vendor ptytest + HomeIsolation + capability gates + eval doctor`

## Open questions for the executor

- Q1: Confirm `pexpect>=4.9` is acceptable as a new runtime dep (it's transitively pulled by some existing packages but not directly required). If not, the vendored ptytest needs to vendor pexpect too.
- Q2: Verify upstream ptytest's MIT license and ensure NOTICE/LICENSE handling matches IronClaude's existing conventions.
- Q3: Verify Claude Code's TTY behavior on Linux (the target platform) — specifically, does it emit a deterministic prompt-ready signal that `expect_prompt_ready` can match? If not, document the heuristic chosen (e.g., regex for `^> $` or `^\$ $` or idle-stdout-for-N-seconds).

## Dependencies

- **Depends on:** Nothing (this is the first phase)
- **Blocks:** P2 (needs `pty/`, `isolation.py`, `capability_gates.py`), P3, P4

## Estimated LOC: ~400

(Per design-spec §17: vendored pty/ ~150 LOC adapted, isolation.py ~120 LOC, capability_gates.py ~80 LOC, commands.py [doctor only] ~50 LOC, tests ~150-200 LOC across 3 files.)
