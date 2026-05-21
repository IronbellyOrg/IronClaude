# cliEval — Design Specification

**Status:** 🟡 DRAFT-R2 2026-05-18 (revised to resolve spec-panel CRITICAL findings)
**Author:** Claude Opus 4.7 (via /sc:design, /sc:spec-panel, /sc:design revise)
**Reviewers:** RyanW (maintainer)
**Scope:** Architecture, components, CLI surface, isolation model, integration points, run-artifact schema. NOT implementation code (only interface signatures where they sharpen the contract).

**Revision log:**
- R1 (2026-05-18): Initial DRAFT.
- R2 (2026-05-18): Resolves 4 CRITICAL findings from `spec-panel-review.md`: W-1 (falsifiable G5), N-2 (`--max-disk-mb` consistency), Wh-1 (eval_id regex + path-containment guard), Pipeline-CRITICAL (reporter consumes N' not K + status taxonomy + orchestrator→reporter contract). See `decisions.md` D-5..D-8 for new ADRs.


## 1. Goals & Non-goals

### Goals

1. **Drive a real Claude Code subprocess** through a PTY for each eval — no mocks, no synthetic stubs, no in-process SDK clients.
2. **Run all 15 evals in parallel** (default concurrency=8, max=15) with strict isolation: each eval owns its own `HOME` directory, its own session_id, and its own state/telemetry namespace.
3. **Plug cleanly into the existing IronClaude CLI** — new `superclaude eval --suite real` subcommand, no breaking changes to existing subcommands, ~60% scaffolding reused from `cli/sprint`, `cli/prd`, `cli/pipeline`.
4. **Produce reproducible artifacts** under `.dev/eval-runs/<ISO>/<run-id>/` — structured per-eval logs, aggregate report (Markdown + JSON), failure stack traces, captured TTY transcripts.
5. **Catch the bug PR #49 fixed and any equivalent future hook-matcher regression.** Falsifiable definition: for every PostToolUse hook H with matcher pattern P registered in `~/.claude/settings.json`, an eval exists in the `real` suite that (a) issues a real MCP tool call whose name matches P, (b) reads the per-eval `~/.claude/logs/<hook>.jsonl` telemetry, and (c) asserts H fired with the matching tool name. Concretely the v1 suite covers the three known auggie-prefix matchers (`mcp__auggie__*`, `mcp__auggie-mcp__*`, `mcp__airis-mcp-gateway__*`) via E1 and E2.{1,2,3}. The harness FAILS the run if any matcher P registered in `hooks.json` lacks a corresponding eval in the loaded suite (gate enforced by `eval doctor --check-coverage` and re-checked at the top of `eval run`).
6. **Be runnable locally today** with a single command: `uv run superclaude eval --suite real`.

### Non-goals

- CI integration (deferred per maintainer directive).
- Eval body implementations (the 15 evals themselves are a separate workstream).
- Web UI / dashboard (text + markdown artifacts only).
- Cross-platform support (Linux only for now — Claude Code TTY behavior is platform-specific; macOS support is a follow-up).
- Pure API-SDK eval mode (the harness is TTY-driven by design; tool-call observability comes from the JSONL hook telemetry, not from intercepting the SDK).


## 2. Component Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                  superclaude eval --suite real                       │
│                  src/superclaude/cli/eval/commands.py                │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
              ┌─────────────┴──────────────┐
              ▼                            ▼
┌──────────────────────┐    ┌────────────────────────────────┐
│  Suite Loader        │    │  Run Orchestrator              │
│  cli/eval/loader.py  │    │  cli/eval/orchestrator.py      │
│  ─ reads YAML        │    │  ─ ThreadPoolExecutor          │
│  ─ validates schema  │    │  ─ as_completed iteration      │
│  ─ resolves          │    │  ─ per-eval timeout            │
│    capability gates  │    │  ─ failure aggregation         │
└──────────────────────┘    └──────────────┬─────────────────┘
                                           │
                            ┌──────────────┴──────────────┐
                            ▼                             ▼
        ┌──────────────────────────┐    ┌─────────────────────────────────┐
        │  EvalRunner              │    │  Reporter                       │
        │  cli/eval/runner.py      │    │  cli/eval/reporter.py           │
        │  ─ build HomeIsolation   │    │  ─ AggregatedRunReport          │
        │  ─ deploy hooks to HOME  │    │  ─ to_markdown / to_json        │
        │  ─ spawn ClaudeProcess   │    │  ─ writes artifact tree         │
        │    via PtyDriver         │    │                                 │
        │  ─ inject test inputs    │    └─────────────────────────────────┘
        │  ─ observe JSONL +       │
        │    state side-effects    │
        │  ─ apply Expect.*        │
        │    assertions            │
        │  ─ teardown HOME         │
        └────────────┬─────────────┘
                     │
       ┌─────────────┴──────────────┐
       ▼                            ▼
┌──────────────────┐    ┌──────────────────────────────┐
│  PtyDriver       │    │  HomeIsolation               │
│  cli/eval/pty/   │    │  cli/eval/isolation.py       │
│  (vendored       │    │  (extends sprint/executor.py │
│   ptytest fork)  │    │   :107-182 IsolationLayers)  │
│  ─ spawn TTY     │    │  ─ adds HOME override        │
│  ─ stdin write   │    │  ─ pre-deploys hooks         │
│  ─ stdout read   │    │  ─ pre-seeds state           │
│  ─ exit capture  │    │  ─ post-teardown cleanup     │
└──────────────────┘    └──────────────────────────────┘
       │
       ▼
┌──────────────────────────┐
│  Real Claude Code        │
│  subprocess (TTY)        │
│  ─ reads ~/.claude/...   │
│  ─ runs hooks            │
│  ─ writes JSONL          │
└──────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────────┐
│  Expect.* DSL (cli/eval/expect.py)                           │
│  ─ Expect.file(path).exists()                                │
│  ─ Expect.jsonl(path).contains_event(name=, session_id=)     │
│  ─ Expect.settings_json(path).has_registration(matcher=, …)  │
│  ─ Expect.exit_code(==0)                                     │
│  ─ Expect.stderr().contains(pattern)                         │
│  ─ Expect.duration(< timedelta)                              │
│  (Port of mcp-eval's Expect.tools.* idea; no upstream dep)   │
└──────────────────────────────────────────────────────────────┘
```

**Module count:** 8 new modules under `cli/eval/` + vendored `pty/` subdirectory. All Python; no new external dependencies (except the vendored ptytest fork which pins `pexpect>=4.9`).


## 3. Directory layout

```
src/superclaude/cli/eval/
├── __init__.py              # exports `eval_group` (Click group)
├── commands.py              # CLI surface: eval_group, run subcommand, --suite/--parallel/--no-mcp flags
├── config.py                # EvalConfig dataclass (paths, defaults)
├── models.py                # EvalSpec, EvalResult, RunSummary, ExpectFailure
├── loader.py                # YAML manifest loader + schema validator
├── orchestrator.py          # parallel scheduling (ThreadPoolExecutor + as_completed)
├── runner.py                # per-eval lifecycle: setup → drive → assert → teardown
├── isolation.py             # HomeIsolation (extends sprint/executor.py IsolationLayers)
├── expect.py                # Expect.* assertion DSL (file/jsonl/settings_json/exit_code/stderr/duration)
├── reporter.py              # AggregatedRunReport (mirrors sprint/executor.py AggregatedPhaseReport)
├── capability_gates.py      # which_or_skip("jq"), mcp_server_available("auggie"), etc.
├── pty/                     # VENDORED — forked ptytest
│   ├── __init__.py
│   ├── driver.py            # PtyDriver class wrapping pexpect.spawn
│   ├── stream.py            # ANSI strip, line buffering, timeout handling
│   ├── LICENSE              # upstream MIT
│   └── PROVENANCE.md        # fork SHA, what we changed, why
└── suites/
    ├── real.yaml            # the 15-eval suite manifest
    └── README.md            # how to author a suite manifest

.dev/eval-runs/              # runtime artifact destination (gitignored)
└── 2026-05-18T18-30-12_run-abc123/
    ├── manifest.snapshot.yaml    # frozen copy of real.yaml at run time
    ├── summary.md                 # human-readable run report
    ├── summary.json               # machine-readable run report
    ├── junit.xml                  # optional CI export
    └── evals/
        ├── E01-sticky-lifecycle/
        │   ├── result.json
        │   ├── stdout.log         # captured Claude Code TTY stdout
        │   ├── stderr.log
        │   ├── home/              # the per-eval HOME at end of eval (gitignored)
        │   │   ├── .claude/state/...
        │   │   ├── .claude/logs/auggie-first.jsonl
        │   │   └── .claude/settings.json
        │   └── expect-trace.md    # assertion log: which Expect.* fired and what they observed
        ├── E02-matcher-coverage/
        │   └── …
        ├── …
        └── E15-hook-timeout/
            └── …

tests/cli/test_eval/
├── test_commands.py         # Click CliRunner tests for the CLI surface
├── test_loader.py           # manifest validation
├── test_orchestrator.py     # scheduling logic (no real subprocesses)
├── test_runner.py           # mock PtyDriver, real isolation
├── test_expect.py           # assertion DSL unit tests
└── test_isolation.py        # HOME override correctness
```


## 4. CLI surface

### Command form

```
superclaude eval [OPTIONS] COMMAND [ARGS]...
```

### Subcommands

|Subcommand|Purpose|
|---|---|
|`superclaude eval run --suite SUITE`|Execute a suite end-to-end. Primary entry point.|
|`superclaude eval list`|Enumerate available suites (read from `cli/eval/suites/*.yaml`).|
|`superclaude eval describe --suite SUITE [--eval ID]`|Print the manifest content for a suite or single eval.|
|`superclaude eval doctor`|Verify the harness's own preconditions (claude binary on PATH, jq/make available, ~/.claude exists, ptytest vendored, etc.).|

### Flags for `eval run`

|Flag|Default|Purpose|
|---|---|---|
|`--suite SUITE`|required|Suite name (matches a `*.yaml` in `cli/eval/suites/`). For now only `real`.|
|`--parallel N`|`8`|Concurrency. Clamped to `[1, 15]`.|
|`--eval ID[,ID…]`|(all)|Run a subset (e.g., `--eval E1,E2,E3`).|
|`--no-mcp`|`false`|Skip evals that require a live MCP server (E1, E2, D1 sub-evals).|
|`--no-pty`|`false`|Skip evals that need a real TTY (most of A/D categories). For "logic-only" runs in constrained environments.|
|`--output-dir PATH`|`.dev/eval-runs/<ISO>/<run-id>/`|Override the artifact destination.|
|`--keep-home`|`false`|Preserve per-eval HOME directories on success (default: deleted; failures always kept).|
|`--timeout-mult FLOAT`|`1.0`|Multiply all per-eval timeouts (useful for slow machines).|
|`--max-disk-mb INT`|`1024`|Soft cap on cumulative artifact size under `--output-dir`. Polled every 5s by the orchestrator; on breach, in-flight evals run to completion, no new evals scheduled, run exits 2 with `disk_budget_exceeded` reason. Set to `0` to disable.|
|`--json`|`false`|Emit machine-readable JSON to stdout in addition to artifacts.|
|`--verbose`|`false`|Stream per-eval progress to terminal (default: spinner only).|

### Exit codes

|Code|Meaning|
|---|---|
|`0`|All evals PASSED (or correctly SKIPPED due to capability gates).|
|`1`|At least one eval FAILED.|
|`2`|Harness error (manifest invalid, claude binary missing, etc.).|
|`3`|Interrupted (SIGINT during run).|

### Example invocations

```bash
# Full suite
uv run superclaude eval run --suite real

# Quick subset, verbose
uv run superclaude eval run --suite real --eval E1,E2,E11 --verbose

# Skip MCP-dependent evals (no auggie binary available)
uv run superclaude eval run --suite real --no-mcp

# CI-style with JUnit XML
uv run superclaude eval run --suite real --output-dir /tmp/ci-run --json > /tmp/ci-run/stdout.json
```


## 5. Suite manifest schema (`suites/*.yaml`)

```yaml
# yaml-language-server: $schema=./suite.schema.json
name: real                    # suite name; matches CLI --suite arg
version: "1.0"                 # schema version
description: "15 real-world evals for IronClaude hooks + installer + verify-sync"

defaults:
  per_eval_timeout_sec: 120
  per_eval_memory_mb: 512
  capture_tty: true
  keep_home_on_success: false

# Capability gates checked once per run; failure skips ALL gated evals
required_binaries:
  - { name: claude, min_version: "0.5.0", failure_mode: hard }    # hard: abort run
  - { name: make,    failure_mode: hard }
  - { name: jq,      failure_mode: hard }
  - { name: git,     failure_mode: hard }

optional_capabilities:
  - { name: mcp_server.auggie,            gate_flag: --no-mcp,  failure_mode: skip }
  - { name: mcp_server.auggie-mcp,        gate_flag: --no-mcp,  failure_mode: skip }
  - { name: mcp_server.airis-mcp-gateway, gate_flag: --no-mcp,  failure_mode: skip }

evals:
  - id: E1
    title: "auggie-first sticky lifecycle — set → MCP call → clear"
    category: hook-lifecycle
    requires: [mcp_server.auggie]
    timeout_sec: 90
    isolation:
      home_strategy: ephemeral             # ephemeral | seeded | shared
      seed_state:
        - path: state/last-prompt-ts/{session_id}.txt
          content: "{now - 4h}"            # forces CROSSED=threshold
    inputs:
      - prompt: "What does the auggie-flag-clear hook do?"
        expect_tool_call: mcp__auggie__codebase-retrieval
    expects:
      - { type: file_exists,       path: state/auggie-first-pending/{session_id}.txt, when: pre_tool_call }
      - { type: file_absent,       path: state/auggie-first-pending/{session_id}.txt, when: post_tool_call }
      - { type: jsonl_event,       path: logs/auggie-first.jsonl, event: sticky_cleared, session_id: "{session_id}" }
      - { type: exit_code,         value: 0 }

  - id: E2
    title: "matcher coverage across 3 auggie prefixes"
    category: hook-lifecycle
    parameterize:
      - { prefix: mcp__auggie__,              tool: codebase-retrieval }
      - { prefix: mcp__auggie-mcp__,          tool: ask_question }
      - { prefix: mcp__airis-mcp-gateway__,   tool: auggie_search }
    requires: [mcp_server.{{prefix.split('__')[1]}}]
    # … (each parameter generates a sub-eval E2.1, E2.2, E2.3)

  # … E3 through E15 …
```

**Schema enforcement:** `loader.py` validates with `jsonschema` (already a transitive dep) against `suites/suite.schema.json`. Validation runs in `eval doctor` and at the top of `eval run`.

**Identifier validation (security-critical):** Every `id:` field in the manifest — including IDs generated by `parameterize:` expansion — MUST match the regex `^[A-Z][A-Za-z0-9]*([0-9]+(\.[0-9]+)?)?$` (e.g., `E1`, `E2.1`, `D15`). The loader REJECTS any other shape with `InvalidEvalId` and exits 2 BEFORE any filesystem operations are attempted. This closes the path-traversal attack surface (manifest IDs are interpolated into `home_root / eval_id / home` by `HomeIsolation`; without this guard, an ID like `../../../etc` would escape the scratch root). Template tokens inside `id:` (e.g., `{session_id}`) are rejected — IDs are static strings only.


## 6. Eval lifecycle (per-eval sequence)

```
RunOrchestrator           EvalRunner              HomeIsolation       PtyDriver         Real Claude Code
       │                        │                       │                  │                    │
       │  schedule(eval_spec)   │                       │                  │                    │
       ├───────────────────────►│                       │                  │                    │
       │                        │  build(eval_id)       │                  │                    │
       │                        ├──────────────────────►│                  │                    │
       │                        │                       │ mkdtemp HOME     │                    │
       │                        │                       │ deploy hooks     │                    │
       │                        │                       │ seed state       │                    │
       │                        │                       │ write settings   │                    │
       │                        │  HOME path            │                  │                    │
       │                        │◄──────────────────────┤                  │                    │
       │                        │  spawn(HOME=…)        │                  │                    │
       │                        ├──────────────────────────────────────────►│                   │
       │                        │                       │                  │ pexpect.spawn      │
       │                        │                       │                  ├────────────────────►
       │                        │                       │                  │                    │ session_start
       │                        │                       │                  │                    │ hook fires
       │                        │  inject(prompts)      │                  │                    │
       │                        ├──────────────────────────────────────────►│                   │
       │                        │                       │                  │ stdin write        │
       │                        │                       │                  ├────────────────────►
       │                        │                       │                  │                    │ user_prompt_submit
       │                        │                       │                  │                    │ hook fires
       │                        │                       │                  │                    │ pre/post tool hooks
       │                        │                       │                  │                    │ fire
       │                        │  wait_for_idle()      │                  │                    │
       │                        ├──────────────────────────────────────────►│                   │
       │                        │                       │                  │ read stdout        │
       │                        │                       │                  │◄───────────────────│
       │                        │                       │                  │ until prompt-ready │
       │                        │  apply Expect.*       │                  │                    │
       │                        │  (reads HOME state)   │                  │                    │
       │                        │                       │                  │                    │
       │                        │  capture_tty()        │                  │                    │
       │                        ├──────────────────────────────────────────►│                   │
       │                        │  result(PASS/FAIL,    │                  │                    │
       │                        │         expect_log,   │                  │                    │
       │                        │         tty_log,      │                  │                    │
       │                        │         duration)     │                  │                    │
       │                        │  teardown(HOME)       │                  │                    │
       │                        ├──────────────────────►│                  │                    │
       │                        │                       │ rm -rf HOME      │                    │
       │                        │                       │ (unless KEEP)    │                    │
       │  EvalResult            │                       │                  │                    │
       │◄───────────────────────┤                       │                  │                    │
       │                        │                       │                  │                    │
   continue until                                                                          (subprocess
   as_completed exhausted                                                                   exits or
                                                                                            timeout-killed)
```


## 7. HomeIsolation — extension of existing `IsolationLayers`

### Existing primitive (read-only — cite for reuse)

`src/superclaude/cli/sprint/executor.py:107-182` `IsolationLayers` already implements 4-layer per-subprocess isolation:

|Layer|Env var|Purpose|
|---|---|---|
|Working directory|`CLAUDE_WORK_DIR`|Per-task cwd|
|Git ceiling|`GIT_CEILING_DIRECTORIES`|Prevents accidental parent-repo writes|
|Plugin dir|`CLAUDE_PLUGIN_DIR`|Isolates plugin discovery|
|Settings dir|`CLAUDE_SETTINGS_DIR`|Isolates `settings.json` per subprocess|

### What we add (new — `cli/eval/isolation.py`)

`HomeIsolation` subclasses or composes `IsolationLayers` and adds:

|Layer|Env var|Purpose|
|---|---|---|
|**HOME**|`HOME` (and `XDG_*` overrides)|Per-eval `~/.claude/` — full hook+state+log isolation|
|**Session ID stamp**|`CLAUDE_SESSION_ID`|Deterministic session_id for assertion lookups (eval-id-derived)|
|**Time offset**|`CLAUDE_FAKE_TIME_OFFSET`|Optional; lets evals advance the clock for 30-min freshness tests (E3)|

### Interface signature (not implementation)

```python
@dataclass(frozen=True)
class HomeIsolation:
    eval_id: str                   # e.g., "E1" or "E2.1"
    home_root: Path                # /tmp/eval-runs/<run>/E1/home
    session_id: str                # deterministic: hash(eval_id + run_id)[:16]
    time_offset_sec: int = 0

    def setup(self) -> None:
        """Create HOME/.claude/{hooks,state,logs}; deploy 9 freshness scripts;
        write settings.json; seed state files per manifest."""

    def env(self) -> dict[str, str]:
        """Return env-var overlay for the subprocess: HOME, XDG_*, CLAUDE_*,
        plus pass-through of PATH, USER, TERM, LANG, CI."""

    def teardown(self, keep: bool) -> None:
        """rm -rf home_root unless keep=True or eval failed."""

    def state_path(self, suffix: str) -> Path:
        """Resolve {suffix} template — {session_id}, {project_key}, etc."""
```

### Key correctness invariants

1. `HOME` is set *before* spawn; child cannot see test-runner's `~/.claude/`.
2. Per-eval HOMEs are sibling directories under `home_root` — no two evals share a `HOME`, even at `--parallel 15`.
3. Teardown is best-effort; failure to `rm -rf` is logged but does not affect eval result.
4. Failed evals **always** retain HOME for post-mortem (the `keep=True` override).
5. **Path containment guard (security-critical).** Before any filesystem write, `HomeIsolation.setup()` MUST:
   - (a) Reject any `eval_id` not matching the loader regex (defense-in-depth — loader already validated, but HomeIsolation re-checks).
   - (b) Compute `home_path = (home_root / eval_id / "home").resolve(strict=False)` AND `scratch_root = home_root.resolve(strict=False)`.
   - (c) Verify `home_path.is_relative_to(scratch_root)` (Python 3.9+). If False, raise `HomeContainmentViolation` and abort the eval (mark ERRORED, no teardown attempt on the partial dir).
   - (d) Verify `scratch_root` itself matches one of the allowed prefixes: `/tmp/eval-runs/`, `<repo_root>/.dev/eval-runs/`, or the path passed via `--output-dir` after equivalent resolution + prefix check against an allowlist set in `EvalConfig.allowed_scratch_roots`.
   - (e) Resolve all symlinks under `home_path` after creation but BEFORE deploying hooks (catches the "scratch dir is a symlink to `$HOME`" attack).
6. **Atomic setup contract.** `HomeIsolation.setup()` is wrapped in try/except; on any exception after `mkdtemp` succeeds, the partial HOME is preserved (status ERRORED, `keep=True` forced) and a `setup_failed` artifact tag is written. Distinguishes harness-side bugs from eval-body failures in the report.


## 8. Expect.* assertion DSL

Port of `lastmile-ai/mcp-eval`'s API surface as Python primitives — **no upstream dependency**, just the mental model. Each `Expect.*` returns a callable `(EvalContext) -> ExpectResult`.

### Interface (not implementation)

```python
from pathlib import Path
import re

class Expect:
    """Fluent assertion DSL for eval post-conditions."""

    @staticmethod
    def file(path: str | Path) -> "FileExpect": ...

    @staticmethod
    def jsonl(path: str | Path) -> "JsonlExpect": ...

    @staticmethod
    def settings_json(path: str | Path) -> "SettingsExpect": ...

    @staticmethod
    def exit_code() -> "ExitCodeExpect": ...

    @staticmethod
    def stderr() -> "StreamExpect": ...

    @staticmethod
    def stdout() -> "StreamExpect": ...

    @staticmethod
    def duration() -> "DurationExpect": ...


class FileExpect:
    def exists(self) -> ExpectCallable: ...
    def absent(self) -> ExpectCallable: ...
    def has_mode(self, mode: int) -> ExpectCallable: ...           # e.g., 0o755
    def has_content_matching(self, pattern: str | re.Pattern) -> ExpectCallable: ...

class JsonlExpect:
    def contains_event(self, *, event: str, **fields) -> ExpectCallable: ...
    def event_count(self, *, event: str, op: str, n: int) -> ExpectCallable: ...
    def is_valid_jsonl(self) -> ExpectCallable: ...

class SettingsExpect:
    def has_registration(self, *, event: str, matcher: str) -> ExpectCallable: ...
    def hooks_count(self, *, event: str, op: str, n: int) -> ExpectCallable: ...

class ExitCodeExpect:
    def equals(self, n: int) -> ExpectCallable: ...
    def in_(self, codes: list[int]) -> ExpectCallable: ...

class StreamExpect:
    def contains(self, pattern: str | re.Pattern) -> ExpectCallable: ...
    def does_not_contain(self, pattern: str | re.Pattern) -> ExpectCallable: ...
    def matches_line(self, pattern: str | re.Pattern) -> ExpectCallable: ...

class DurationExpect:
    def less_than(self, seconds: float) -> ExpectCallable: ...
    def greater_than(self, seconds: float) -> ExpectCallable: ...
```

### Usage in manifest (declarative)

```yaml
expects:
  - { type: file_exists,       path: state/auggie-first-pending/{session_id}.txt, when: pre_tool_call }
  - { type: jsonl_event,       path: logs/auggie-first.jsonl, event: sticky_cleared, session_id: "{session_id}" }
  - { type: exit_code,         value: 0 }
```

### Usage in code (programmatic, for parameterized evals)

```python
result = runner.run(eval_spec)
Expect.file(home / ".claude/state/auggie-first-pending" / f"{sid}.txt").absent()(ctx)
Expect.jsonl(home / ".claude/logs/auggie-first.jsonl").contains_event(
    event="sticky_cleared", session_id=sid)(ctx)
Expect.exit_code().equals(0)(ctx)
```

The manifest's declarative form is parsed by `loader.py` into a list of `ExpectCallable` instances. Programmatic form is for evals whose post-conditions can't be expressed in YAML (rare; allow escape hatch).


## 9. Reporting & artifacts

### `summary.md` (human-readable)

```markdown
# Eval Run: 2026-05-18T18:30:12 / run-abc123
**Suite:** real | **Parallel:** 8 | **Duration:** 4m 12s

## Result: ✅ 14 passed, ❌ 1 failed, ⏭️  0 skipped

| ID | Title | Status | Duration | Notes |
|---|---|---|---|---|
| E1 | auggie-first sticky lifecycle | ✅ PASS | 8.3s | — |
| E2.1 | matcher coverage mcp__auggie__ | ✅ PASS | 7.1s | — |
| E2.2 | matcher coverage mcp__auggie-mcp__ | ✅ PASS | 7.4s | — |
| … |
| E15 | hook timeout fail-open | ❌ FAIL | 12.0s | timeout enforcement off-spec |

## Failures (1)
### E15: hook timeout fail-open
**Expected:** Edit completes with allow-fallback after hook timeout
**Observed:** Edit blocked with stale-block reason
**Artifacts:** `evals/E15-hook-timeout/` (home preserved)
**TTY excerpt:** ```...```
**Expect-trace:** `evals/E15-hook-timeout/expect-trace.md`
```

### `summary.json` (machine-readable)

**Dimensional invariant:** `len(evals[])` MUST equal N' — the post-loader, post-parameterize-expansion count — NOT the K-kept subset that actually ran. Every skipped eval appears in the list with `status: "SKIPPED"` and a `skip_reason` field. This preserves the audit trail when capability gates (e.g., `--no-mcp`) silently drop evals.

```json
{
  "run_id": "run-abc123",
  "started_at": "2026-05-18T18:30:12Z",
  "duration_sec": 252,
  "suite": "real",
  "manifest_version": "1.0",
  "parallel": 8,
  "counts": {
    "manifest_n": 15,
    "expanded_n_prime": 17,
    "kept_k": 12,
    "skipped_s": 5,
    "kept_plus_skipped_equals_n_prime": true
  },
  "totals": { "passed": 11, "failed": 1, "skipped": 5, "errored": 0, "interrupted": 0, "timeout": 0 },
  "evals": [
    {
      "id": "E1",
      "title": "auggie-first sticky lifecycle",
      "status": "PASS",
      "duration_sec": 8.3,
      "expects": [
        { "type": "file_exists", "passed": true, "evidence": "…/sid.txt size=33" },
        { "type": "jsonl_event", "passed": true, "evidence": "line 3: event=sticky_cleared" }
      ],
      "artifacts": { "stdout": "evals/E01-sticky-lifecycle/stdout.log", "..." }
    },
    {
      "id": "E2.3",
      "title": "matcher coverage mcp__airis-mcp-gateway__",
      "status": "SKIPPED",
      "skip_reason": "capability_gate:mcp_server.airis-mcp-gateway",
      "skip_flag_triggered": "--no-mcp",
      "duration_sec": 0.0,
      "expects": [],
      "artifacts": {}
    }
  ]
}
```

### Status taxonomy

The reporter classifies every eval into exactly one of:

|Status|Meaning|Counts as failure?|
|---|---|---|
|`PASS`|All Expect assertions returned true; exit code matched.|No|
|`FAIL`|At least one Expect assertion returned false.|Yes|
|`ERRORED`|Setup raised (e.g., HomeContainmentViolation, setup_failed), hook deploy crashed, manifest validation rejected post-load. Distinct from FAIL.|Yes|
|`TIMEOUT`|Per-eval timeout fired; subprocess SIGKILL'd.|Yes|
|`INTERRUPTED`|SIGINT/SIGTERM during run; eval was mid-flight.|Yes|
|`SKIPPED`|Capability gate fired (e.g., `--no-mcp` and `mcp_server.auggie` required); eval never ran.|No|
|`XFAIL`|Manifest declares `xfail_if:` and condition matched; ran-and-failed-as-expected.|No|
|`XPASS`|Manifest declares `xfail_if:` matched but eval passed anyway (surprise success — investigate).|Yes (treated as MAJOR signal)|

Exit code from §4 maps: 0 ⇔ no eval in {FAIL, ERRORED, TIMEOUT, XPASS}; 1 ⇔ at least one; 2 ⇔ harness error before any eval ran; 3 ⇔ INTERRUPTED.

### `junit.xml` (optional, for future CI plumbing)

Standard JUnit format mapped from `summary.json`; one `<testcase>` per eval. Generated only when `--junit` is passed.

### Aggregator data contract

Orchestrator → Reporter handoff is a list of `EvalOutcome` records with shape:

```python
@dataclass(frozen=True)
class EvalOutcome:
    eval_id: str
    title: str
    status: Literal["PASS","FAIL","ERRORED","TIMEOUT","INTERRUPTED","SKIPPED","XFAIL","XPASS"]
    duration_sec: float           # 0.0 for SKIPPED
    expects: list[ExpectResult]   # [] for SKIPPED
    skip_reason: str | None       # populated only when status == "SKIPPED"
    skip_flag_triggered: str | None
    artifacts: dict[str, str]     # path-relative artifact map; {} for SKIPPED
    error_class: str | None       # e.g., "HomeContainmentViolation" for ERRORED
```

The orchestrator emits one `EvalOutcome` per expanded EvalSpec (N' total). Capability filtering does NOT remove SpecS from the list — it stamps them as SKIPPED with reason. The reporter trusts the invariant `len(outcomes) == counts.expanded_n_prime` and asserts it at the top of `AggregatedRunReport.from_outcomes(...)`; mismatch raises `ReporterContractViolation` and the run exits 2.

### Aggregator reuse

The aggregator borrows directly from `src/superclaude/cli/sprint/executor.py:190-335` `AggregatedPhaseReport`:

- `to_markdown()` — reuse signature, swap "phase" terminology for "eval"
- `to_yaml()` — same
- Add `to_json()` and `to_junit()` (new methods, ~50 LOC each)


## 10. Integration with existing IronClaude code

### Files MODIFIED (additive, low-risk)

|File|Change|Lines added|Risk|
|---|---|---|---|
|`src/superclaude/cli/main.py:369-391`|`from .eval import eval_group` + `main.add_command(eval_group)`|2|LOW|
|`Makefile`|Optional new target `make eval-real` → `uv run superclaude eval run --suite real`|3|LOW|
|`.gitignore`|Add `.dev/eval-runs/*/evals/*/home/` and `.dev/eval-runs/*/evals/*/stdout.log`|2|LOW|

### Files REUSED (read-only — depend on existing API)

|File|What we use|Reason it's stable|
|---|---|---|
|`cli/pipeline/process.py:24-150` `ClaudeProcess`|Subprocess scaffolding for spawn+capture|Used by `cli/sprint` + `cli/prd` + `cli/cli_portify`; stable API surface.|
|`cli/sprint/executor.py:107-182` `IsolationLayers`|Base class for `HomeIsolation`|Used by sprint; we EXTEND not replace, so no breaking change.|
|`cli/sprint/executor.py:190-335` `AggregatedPhaseReport`|Pattern reference for `AggregatedRunReport`|We copy the shape; no runtime dependency.|
|`cli/prd/executor.py:774-802` `ThreadPoolExecutor` + `as_completed`|Reference pattern for `orchestrator.py`|Idiomatic stdlib; no import dependency.|
|`tests/cli/test_install_hooks.py`|Reference for fixture patterns|Test scaffolding only.|
|`src/superclaude/hooks/scripts/*.sh`|Deployed into per-eval HOMEs as-is|Read-only; we copy via shutil.|
|`src/superclaude/hooks/hooks.json`|Source for per-eval `~/.claude/settings.json`|Read-only; we feed through `install_hooks.py`.|
|`src/superclaude/cli/install_hooks.py:install_hooks`|Called by `HomeIsolation.setup()` to populate per-eval HOMEs|Public API; stable.|

### Files NEW (cli/eval/ + vendored pty/)

13 new files under `src/superclaude/cli/eval/` and `cli/eval/pty/` (vendored ptytest). See §3 directory layout.

### Test coverage for the harness itself

6 new test files under `tests/cli/test_eval/` (see §3). These are pytest-based and DO use mocks — the harness *itself* is the system under test; we mock the spawned subprocess for harness unit tests, then E1-E15 are the real-subprocess validation of the harness in production mode.


## 11. Capability gating

### Three tiers of gates

|Tier|Trigger|Behavior|
|---|---|---|
|**HARD**|`which claude` returns nonzero|Abort run with exit code 2 + error msg. Cannot proceed.|
|**SOFT-SKIP**|User passed `--no-mcp` or `mcp_server.auggie` check fails|Mark gated evals as SKIPPED with reason. Continue.|
|**SOFT-XFAIL**|Manifest declares `xfail_if: <condition>`|Run, but expected-fail. Status is XPASS if it passes anyway.|

### Capability check implementation (interface only)

```python
# cli/eval/capability_gates.py

@dataclass
class Capability:
    name: str
    check: Callable[[], bool]
    failure_mode: Literal["hard", "skip", "xfail"]
    skip_flag: Optional[str] = None    # CLI flag that forces skip (e.g., --no-mcp)
    description: str = ""

CAPABILITIES = [
    Capability("binary.claude",  lambda: shutil.which("claude")  is not None, "hard"),
    Capability("binary.make",    lambda: shutil.which("make")    is not None, "hard"),
    Capability("binary.jq",      lambda: shutil.which("jq")      is not None, "hard"),
    Capability("binary.git",     lambda: shutil.which("git")     is not None, "hard"),
    Capability("mcp_server.auggie",            mcp_server_reachable("auggie"),            "skip", "--no-mcp"),
    Capability("mcp_server.auggie-mcp",        mcp_server_reachable("auggie-mcp"),        "skip", "--no-mcp"),
    Capability("mcp_server.airis-mcp-gateway", mcp_server_reachable("airis-mcp-gateway"), "skip", "--no-mcp"),
]

def check_all(skip_flags: set[str]) -> CapabilityReport:
    """Run all checks; return per-cap status + which evals are blocked."""
```

### `eval doctor` output

```
🔧 superclaude eval doctor

Hard requirements:
  ✅ claude:  /usr/local/bin/claude (v0.5.3)
  ✅ make:    /usr/bin/make
  ✅ jq:      /usr/bin/jq
  ✅ git:     /usr/bin/git

Optional capabilities:
  ✅ mcp_server.auggie:            reachable via stdio
  ✅ mcp_server.auggie-mcp:        reachable via stdio
  ❌ mcp_server.airis-mcp-gateway: unreachable (1 eval will skip)

Verdict: READY (1 eval will be skipped without --no-mcp override)
```


## 12. Concurrency model

### Default: `ThreadPoolExecutor(max_workers=8)`

The orchestrator uses `concurrent.futures.ThreadPoolExecutor` (matching `cli/prd/executor.py:774-802`'s pattern, NOT the heavier `execution/parallel.py`). Each eval runs in its own thread; the thread blocks on `PtyDriver.wait()` which is itself a `pexpect` blocking read.

### Isolation guarantees at high concurrency

1. **No shared mutable state** — each eval has its own `HomeIsolation` with its own HOME dir.
2. **No shared file handles** — each eval opens its own `auggie-first.jsonl` under its HOME.
3. **No port collisions** — Claude Code TTY doesn't bind ports for the evals we run.
4. **Bounded process count** — at `--parallel 8`, max 8 `claude` subprocesses concurrently. At `--parallel 15`, 15. Each consumes ~150MB resident; 15-way needs ~2.25GB free.

### Bounded retry (no infinite retry)

Failed evals are NOT retried by default. The harness produces a deterministic single-pass run. The user can re-run with `--eval <failed-ids>` after diagnosing.

### Signal handling

- `SIGINT` (Ctrl-C): Cancel all running evals, mark in-flight as INTERRUPTED, write partial summary, exit 3.
- `SIGTERM`: Same as SIGINT.
- Per-eval timeout: kill the `PtyDriver` subprocess + reap zombie; mark eval as TIMEOUT (counts as FAIL).

### What we DON'T do at high concurrency

- No fancy async/await. Each eval is a blocking thread; the orchestrator just collects results via `as_completed`.
- No process supervisor / reaper daemon. Python's `concurrent.futures` cleans up worker threads on shutdown.
- No distributed mode. Single-host only.


## 13. Fork strategy — vendored `ptytest`

### What we fork

`brandon-fryslie/ptytest` (MIT, Python 3.8+). The repo has 1 star / 0 forks — bus-factor risk is real. Mitigation: **fork-and-own**.

### Vendoring layout

```
src/superclaude/cli/eval/pty/
├── __init__.py
├── driver.py        # PtyDriver (was: ptytest/__init__.py PtySession)
├── stream.py        # ANSI strip + line buffer (was: ptytest/_stream.py)
├── LICENSE          # upstream MIT, verbatim
└── PROVENANCE.md    # fork SHA, what we changed, why
```

### What we change vs upstream

|Change|Reason|
|---|---|
|Rename `PtySession` → `PtyDriver`|Avoid pytest-fixture connotation; we use it in a non-pytest context too.|
|Remove pytest-plugin entry-point|We don't need fixture autoloading.|
|Add `expect_prompt_ready(timeout=)` method|Cleaner waiting for Claude Code's TTY-prompt signal (the `>` or `$` indicator that input is welcome).|
|Add `inject_prompt(text)` method|Adds CR-LF + flushes — wraps stdin writes for Claude Code idioms.|
|Tighten dependency to `pexpect>=4.9`|The vendored ptytest doesn't pin pexpect tightly.|
|Apply ANSI-strip aggressively|Claude Code emits rich ANSI; the eval's TTY assertions need plain text.|

### What we DON'T change

- Core `pexpect.spawn` mechanics — leave it alone.
- The Docker-isolation mode (we don't need it; per-eval HOME isolation is enough).
- The original test suite — we vendor it under `tests/cli/test_eval/test_pty_vendor.py` to catch regressions during future ptytest re-syncs.

### Upstream resync policy

The vendored fork is "frozen at the fork SHA." If upstream releases significant changes (e.g., `pexpect` major-version bump, important bugfix), the `PROVENANCE.md` documents the resync procedure: pull upstream, three-way merge our changes, re-run vendored tests.

### License compliance

ptytest is MIT. We retain the upstream LICENSE verbatim in `cli/eval/pty/LICENSE` and reference it in IronClaude's top-level NOTICE (if one exists; otherwise add one).


## 14. Risks & mitigations

|ID|Risk|Severity|Probability|Mitigation|
|---|---|---|---|---|
|R1|**Claude Code TTY behavior changes between versions** breaks the PtyDriver|HIGH|MEDIUM|Pin `claude` version range in `eval doctor`; capture full TTY transcripts so version-shift regressions are diagnosable.|
|R2|**Per-eval HOME setup is slow** (deploy 9 scripts × 15 evals = 135 file ops)|MEDIUM|HIGH|Reuse `install_hooks.py` (already optimized). At ~10ms per `cp`, full setup is ~1.4s per eval. Acceptable.|
|R3|**MCP server flakiness** causes E1/E2 false failures|MEDIUM|MEDIUM|Per-eval retry-once on MCP-specific failure modes (timeout, unreachable). Document in failure as "MCP-server-flaky" tag distinct from "hook-broken."|
|R4|**Concurrent HOMEs exhaust disk** (15 × ~5MB = 75MB; with TTY logs maybe 300MB)|LOW|LOW|`--keep-home false` is default; failed HOMEs preserved. `--max-disk-mb` flag (§4, default 1024) polls cumulative artifact size every 5s and aborts the run with exit 2 + `disk_budget_exceeded` reason when breached.|
|R5|**Ptytest fork drift from upstream** — we miss security/correctness fixes|LOW|LOW|Quarterly review of upstream `pexpect` releases (the durable dependency).|
|R6|**15-eval suite takes too long** (>10 min) → adoption friction|MEDIUM|MEDIUM|`--eval <subset>` flag; document "quick smoke" subset (3-4 evals) in `suites/quick.yaml` follow-up.|
|R7|**Maintainer accidentally runs harness against real `~/.claude/`** (no HOME isolation)|HIGH|LOW|Hard guard in `HomeIsolation.setup()`: refuse if HOME points outside a known eval-runs scratch dir.|
|R8|**Existing `cli/sprint/executor.py IsolationLayers` changes shape** breaking our extension|MEDIUM|LOW|Vendor a copy of the relevant class if upstream-refactor risk grows; for now, inherit + pin to a tested SHA.|
|R9|**PR scope creep** as evals get added|MEDIUM|HIGH|Ship the HARNESS as PR 1 (this design's scope). E1-E15 land as PR 2 in batches of 3-5.|


## 15. Out of scope (explicit non-goals from §1, restated for clarity)

- **CI integration** (deferred per maintainer; `superclaude eval` runs locally only)
- **Eval body implementations** (15 eval implementations are a follow-up workstream)
- **Cross-platform support** (Linux first; macOS / Windows are follow-ups)
- **Distributed / multi-host eval runs**
- **Web UI / live dashboard**
- **Replay-from-recording** mode (ptytest has it; we don't enable it in v1)
- **LLM-judge assertions** (mcp-eval has this; we don't need it for hook-side-effect validation)


## 16. Acceptance criteria for the design

This design is approved when:

- [ ] Maintainer (RyanW) signs off on the 4 original decisions + 4 new ADRs (D-5..D-8) in [`decisions.md`][ref-1]
- [ ] All 15 eval IDs (E1-E15) from `/sc:brainstorm` are addressable by the manifest schema (§5) AND match the §5 eval_id regex
- [ ] No new external Python deps required beyond `pexpect` (vendored via ptytest) and `jsonschema` (transitive)
- [ ] Effort estimate (~1,340 LOC harness + 15 eval bodies — +150 LOC for R2 path-guard, status taxonomy, disk-budget poller, EvalOutcome contract) is acknowledged
- [ ] Open-question list in [`decisions.md`][ref-1] is fully resolved before `/sc:roadmap`


## 17. Implementation order (proposed for /sc:workflow input)

1. **Phase 1 (~400 LOC, 1 day):** vendored `pty/` + `HomeIsolation` + `capability_gates.py` + `eval doctor` subcommand. Validate by `superclaude eval doctor` printing the green checklist on a clean dev machine.
2. **Phase 2 (~350 LOC, 1 day):** `loader.py` + `models.py` + `expect.py` + `eval describe`/`list`. Validate by feeding a minimal 1-eval manifest and seeing the parsed structure.
3. **Phase 3 (~440 LOC, 1 day):** `orchestrator.py` + `runner.py` + `reporter.py` + `eval run`. Validate with a stub 1-eval suite (E1 only) end-to-end. Real Claude Code subprocess spawn confirmed working.
4. **Phase 4 (~150 LOC, 0.5 day):** wire into `cli/main.py`, add `Makefile` target, update `.gitignore`. Run `make verify-sync` post-changes — must still EXIT=0.
5. **Phase 5 (eval bodies, ~3000-4500 LOC, 1-2 weeks):** implement E1 through E15 in batches of 3-5. Each batch is a separate PR.

Total: **~1,340 LOC of harness in 3.5 days** + eval bodies on a longer cadence.

---

**End of design-spec.md.**

[ref-1]: ./decisions.md
