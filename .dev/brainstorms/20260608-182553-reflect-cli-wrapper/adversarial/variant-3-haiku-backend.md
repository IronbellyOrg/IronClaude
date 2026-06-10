# Variant 3 — Thin CLI Wrapper: `superclaude reflect run` (Backend/Haiku Design Spec)

**Author:** Backend persona (subprocess lifecycle, data integrity, deterministic contracts)
**Date:** 2026-06-08
**Status:** Adversarial variant — ready for merge-review

---

## 1. Problem

A tasklist's final item must run the full `/sc:reflect --mode post` (Tier 1 + Tier 2) and capture the verdict back into its own frontmatter so downstream gates can consume it programmatically. The current path — invoking `/sc:reflect` as a skill inside the same Claude Code session — suffers from:

1. **Bias contamination** — the executor that did the work is also the auditor (the protocol explicitly forbids this via the heterogeneous-reviewer mechanism).
2. **No exit-code contract** — the skill emits YAML to `<output>/return-contract.yaml` but the tasklist completion gate has no subprocess exit code to key off.
3. **Subagent limitation** — running reflect in an Agent-tool subagent is forbidden (skill fan-out does not nest).

**Solution:** A thin Python wrapper that spawns a TOP-LEVEL `claude --print` subprocess (its own session, its own model), delivers the reflect prompt via stdin, waits for exit, locates and parses `<output>/return-contract.yaml`, writes the verdict back to the task file's frontmatter atomically, and exits with a status code the gate consumes.

**Hard non-goals:** Not a sc:cli-portify; does NOT reimplement reflect's waves/tiers/taxonomy in Python; never runs reflect in an Agent-tool subagent; no auto-commit; default audit-only (`--no-promote`).

---

## 2. Functional Requirements

### FR-1 — Subprocess Invocation
The wrapper SHALL launch a top-level `claude --print --verbose` subprocess with the reflect prompt delivered via stdin, `--output-format stream-json`, `--output <pinned-dir>`, `--model <resolved>`, and `--dangerously-skip-permissions`. The prompt instructs the child to run `/sc:reflect --mode post` with `--diff HEAD~1..HEAD` (or caller-provided `--diff`), `--output <pinned-dir>`, `--depth deep` (to force Tier 2), and `--no-promote` (default; promotable via `--promote`).

### FR-2 — Return-Contract Consumption
After the subprocess exits (exit code 0 or 124), the wrapper SHALL locate `<output-dir>/return-contract.yaml`, parse it with `yaml.safe_load`, and extract the following fields into an internal `ReflectVerdict` dataclass:
- `status` (str: success|partial|failed|dry-run)
- `tier_reached` (int: 1|2|3)
- `regression_present` (bool)
- `needs_human_decision` (bool)
- `deviation_count_by_class` (dict: authorized/necessary/drift/regression → int)
- `report_path` (str)
- `confidence_calibrated` (float)
- `tasklist_completion_pct` (float|null)
- `citations_dropped` (int)
- `contract_version` (str)

Missing fields default to their YAML-absent sentinel (None for optional, False for bool, 0 for int). The wrapper does NOT validate semantics beyond type coercion — the child skill owns correctness.

### FR-3 — Frontmatter Write-Back
The wrapper SHALL write a `reflect_post` key into the task file's YAML frontmatter:
```yaml
reflect_post:
  verdict: <status>
  run_id: <iso-timestamp>
  report: <report_path>
  tier_reached: <int>
  regression_present: <bool>
  needs_human_decision: <bool>
  deviation_counts:
    authorized: <int>
    necessary: <int>
    drift: <int>
    regression: <int>
  confidence_calibrated: <float>
```

The write is **atomic**: read frontmatter, merge the `reflect_post` key, serialize to a temp file in the same directory, `os.replace()` over the original. The wrapper uses `yaml.safe_dump` with `default_flow_style=False` and a `SafeDumper` subclass that sets `indent = 2` and `mapping = 2` to preserve the project's 2-space indent convention (CLAUDE.md yamllint alignment).

### FR-4 — Exit-Code Contract
The wrapper exits with:
- **0** — Clean success: `status == "success"`, `regression_present == False`, `needs_human_decision == False`, `deviation_count_by_class.drift == 0`.
- **1** — Deviations found: `status == "partial"` or (`drift > 0` or `regression > 0` or `needs_human_decision == True`). The tasklist gate reads this as "halt and surface to user."
- **2** — Infra-failure: subprocess exit code 124 (timeout), return-contract.yaml missing or unparseable, subprocess exit code not 0/124, or frontmatter write fails.

### FR-5 — CLI Subcommand
The wrapper exposes `superclaude reflect run <taskfile> [OPTIONS]` as a Click command group registered on `main`. Options: `--model`, `--diff`, `--max-turns`, `--timeout`, `--promote`, `--output-dir`, `--no-mcp`.

### FR-6 — Env/Isolation Inheritance
The child subprocess inherits the parent's environment with:
- `CLAUDECODE` and `CLAUDE_CODE_ENTRYPOINT` removed (per `pipeline/process.py` `build_env` pattern, preventing nested-session detection).
- All `ANTHROPIC_DEFAULT_*_MODEL` env vars inherited as-is so the child's reflect skill resolves its own model aliases.
- MCP server config inherited (child reads `~/.claude/settings.json` for MCP definitions).

---

## 3. Non-Functional Requirements

### NFR-1 — Thin Delegation
The wrapper contains zero reflect logic. It is a subprocess launcher + YAML parser + frontmatter merger. All waves, tiers, taxonomy, and calibration live in the child skill.

### NFR-2 — Idempotent
Running `superclaude reflect run` on the same task file twice is safe. The `reflect_post` key is overwritten (not appended). The child's `<output-dir>` gets a timestamped suffix if collision (handled by the skill itself).

### NFR-3 — Hermetic
The wrapper does not modify any file outside (a) the task file's frontmatter and (b) the pinned `<output-dir>`. No git operations. No commit.

### NFR-4 — Timeout-Bounded
Default timeout: 3600s (60 min), configurable via `--timeout`. Maps to the child's `--max-turns 300` (300 turns × 120s/turn cap ≈ 60 min). Timeout kills the child process group and exits 2.

### NFR-5 — No New External Dependencies
Uses only stdlib + click + PyYAML (already in project deps via `pyproject.toml`).

### NFR-6 — Structured Logging
All wrapper operations emit debug-level logs to `superclaude.reflect.runner` logger. PIDs, exit codes, contract field presence, and frontmatter write paths are logged at DEBUG. Errors at ERROR with full context.

---

## 4. Subprocess Lifecycle

### 4.1 Command Construction

The wrapper builds the prompt string and the `claude` argv separately, following the `pipeline/process.py` pattern:

```python
prompt = (
    "/sc:reflect --mode post "
    f"--diff {diff_ref} "
    f"--output {output_dir} "
    "--depth deep "
    "--no-promote"
    + (f" --tasklist {tasklist_path}" if tasklist_path else "")
    + (f" --spec {spec_path}" if spec_path else "")
    + (" --promote" if promote else "")
)

cmd = [
    "claude",
    "--print",
    "--verbose",
    "--dangerously-skip-permissions",
    "--no-session-persistence",
    "--tools", "default",
    "--max-turns", "300",
    "--output-format", "stream-json",
    "--output", str(output_dir),
    "--model", model,  # resolved from ANTHROPIC_DEFAULT_SONNET_MODEL or caller --model
]
```

**Prompt delivery:** via stdin (`Popen.stdin.write`), not `-p` argv, to bypass Linux `MAX_ARG_STRLEN` (128 KB). Identical to `pipeline/process.py` line 142.

**Process group:** `preexec_fn=os.setpgrp` so SIGTERM/SIGKILL kills the entire child tree (Claude's own MCP subprocesses included).

### 4.2 Lifecycle Hooks

Reuses `pipeline.process.ClaudeProcess` directly — no new subprocess abstraction. Instantiation:

```python
proc = ClaudeProcess(
    prompt=prompt,
    output_file=output_dir / "stream.json",
    error_file=output_dir / "error.log",
    max_turns=300,
    model=model,
    permission_flag="--dangerously-skip-permissions",
    timeout_seconds=timeout,  # default 3600
    output_format="stream-json",
    env_vars=_build_env(),    # removes CLAUDECODE, inherits ANTHROPIC_DEFAULT_*_MODEL
)
proc.start()
rc = proc.wait()
```

`_build_env()` follows `pipeline/process.py` `build_env()`: copies `os.environ`, pops `CLAUDECODE` and `CLAUDE_CODE_ENTRYPOINT`, and returns the dict. No additional env vars are injected.

### 4.3 Timeout Handling

`proc.wait()` returns 124 on `TimeoutExpired`, matching the `pipeline/process.py` convention. The wrapper treats 124 as infra-failure (exit 2) — the child did not complete within budget, and the return contract is absent.

---

## 5. Return-Contract Consumption

### 5.1 Location

After `proc.wait()` returns, the wrapper scans `<output-dir>/return-contract.yaml`. The output dir is pinned at invocation time (`--output <dir>`), so the path is deterministic:

```python
contract_path = output_dir / "return-contract.yaml"
if not contract_path.exists():
    _log.error("return-contract.yaml not found at %s", contract_path)
    return ExitCode.INFRA_FAILURE  # 2
```

### 5.2 Parsing

```python
import yaml

with open(contract_path) as f:
    contract = yaml.safe_load(f)

# The contract may be a single dict or have top-level keys
# under a "stable" block; handle both shapes.
if isinstance(contract, dict):
    # v1.2.0 shape: flat dict with all §9.1 fields at top level
    pass
elif isinstance(contract, dict) and "stable" in contract:
    contract = contract["stable"]
```

### 5.3 Field Extraction (exact reads)

```python
@dataclass
class ReflectVerdict:
    status: str = "unknown"
    tier_reached: int = 0
    regression_present: bool = False
    needs_human_decision: bool = False
    deviation_count_by_class: dict = field(default_factory=dict)
    report_path: str = ""
    confidence_calibrated: float = 0.0
    tasklist_completion_pct: float | None = None
    citations_dropped: int = 0
    contract_version: str = "unknown"

def parse_verdict(contract: dict) -> ReflectVerdict:
    return ReflectVerdict(
        status=contract.get("status", "unknown"),
        tier_reached=contract.get("tier_reached", 0),
        regression_present=bool(contract.get("regression_present", False)),
        needs_human_decision=bool(contract.get("needs_human_decision", False)),
        deviation_count_by_class=contract.get("deviation_count_by_class", {}),
        report_path=contract.get("report_path", ""),
        confidence_calibrated=float(contract.get("confidence_calibrated", 0.0)),
        tasklist_completion_pct=contract.get("tasklist_completion_pct"),
        citations_dropped=int(contract.get("citations_dropped", 0)),
        contract_version=str(contract.get("contract_version", "unknown")),
    )
```

No validation beyond type coercion. The skill owns semantic correctness.

---

## 6. Frontmatter Write-Back (Atomic)

### 6.1 Target

The task file (passed as `<taskfile>` positional). Must be a markdown file with YAML frontmatter (`---` delimited).

### 6.2 Algorithm

1. Read the file content.
2. Locate the frontmatter block: text between the first `---` line and the next `---` line.
3. Parse frontmatter with `yaml.safe_load`.
4. Inject the `reflect_post` key (overwrite if present).
5. Serialize with a custom `SafeDumper` subclass that sets `indent=2`, `default_flow_style=False`.
6. Write to `<taskfile>.tmp` in the same directory.
7. `os.replace(<taskfile>.tmp, <taskfile>)` — atomic on POSIX.

```python
import re
import yaml
from pathlib import Path

class _IndentedDumper(yaml.SafeDumper):
    """Preserve 2-space indent to satisfy yamllint."""
    pass

def increase_indent(self, flow=False, indentless=False):
    return super().increase_indent(flow, False)

_IndentedDumper.add_representer(type(None), lambda d, x: d.represent_scalar('tag:yaml.org,2002:null', ''))
_IndentedDumper.increase_indent = increase_indent

def write_reflect_verdict(taskfile: Path, verdict: ReflectVerdict) -> None:
    content = taskfile.read_text(encoding="utf-8")

    # Locate frontmatter
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        raise ValueError(f"No YAML frontmatter found in {taskfile}")

    fm_yaml = yaml.safe_load(match.group(1)) or {}
    fm_yaml["reflect_post"] = {
        "verdict": verdict.status,
        "run_id": datetime.now(timezone.utc).isoformat(),
        "report": verdict.report_path,
        "tier_reached": verdict.tier_reached,
        "regression_present": verdict.regression_present,
        "needs_human_decision": verdict.needs_human_decision,
        "deviation_counts": verdict.deviation_count_by_class,
        "confidence_calibrated": verdict.confidence_calibrated,
    }

    new_fm = yaml.dump(fm_yaml, Dumper=_IndentedDumper, allow_unicode=True)
    new_content = f"---\n{new_fm}---\n{content[match.end():]}"

    tmp = taskfile.with_suffix(taskfile.suffix + ".tmp")
    tmp.write_text(new_content, encoding="utf-8")
    os.replace(tmp, taskfile)
```

### 6.3 Corruption Safety

- The temp file is written to the **same directory** as the task file (same filesystem → `os.replace` is atomic).
- If the write fails, the original file is untouched.
- The temp file is cleaned up on success (replaced) or left on failure (diagnostic).

---

## 7. Exit-Code Contract

| Exit Code | Meaning | Tasklist Gate Behavior |
|-----------|---------|----------------------|
| **0** | Clean pass: `status=="success"`, no regressions, no drift, no human-decision-needed | Continue to next phase / mark task done |
| **1** | Deviations detected: `status=="partial"` or `drift>0` or `regression>0` or `needs_human_decision==True` | Halt, surface verdict + report path to user |
| **2** | Infra-failure: subprocess timeout (124), contract missing/unparseable, subprocess crash (non-0/124), frontmatter write error | Halt with error message; do NOT modify frontmatter |

The tasklist completion gate reads the exit code directly. Exit 1 is a **soft halt** (deviations surfaced, user can audit and decide). Exit 2 is a **hard halt** (infrastructure failure, no verdict available).

### 7.1 Gate Consumption Pattern

In a tasklist's final item, the instruction reads:

```markdown
After completing all prior tasks, run:
```
superclaude reflect run <this-task-file> --diff HEAD~1..HEAD
```
If the command exits 0, write `status: done` to the frontmatter.
If it exits 1, write `status: review-needed` and halt.
If it exits 2, write `status: reflect-failed` and halt.
```

---

## 8. CLI Subcommand & Registration

### 8.1 File Layout

```
src/superclaude/cli/reflect/
├── __init__.py          # exports reflect_group
├── commands.py          # @reflect_group.command() — run, status, list
├── models.py            # ReflectRunConfig dataclass, ReflectVerdict dataclass
├── config.py            # defaults (model, timeout, max-turns, output-dir pattern)
└── runner.py            # subprocess lifecycle, contract parse, frontmatter write
```

### 8.2 models.py

```python
@dataclass
class ReflectRunConfig:
    taskfile: Path
    diff: str = "HEAD~1..HEAD"
    model: str = ""          # empty → resolved from env at runtime
    max_turns: int = 300
    timeout: int = 3600
    output_dir: Path | None = None  # None → .dev/reflect/post-<slug>-<timestamp>
    promote: bool = False
    spec: str | None = None
    tasklist: str | None = None
    no_mcp: bool = False
```

### 8.3 config.py

```python
DEFAULT_MODEL_ENV = "ANTHROPIC_DEFAULT_SONNET_MODEL"
DEFAULT_FALLBACK_MODEL = "claude-sonnet-4-20250514"  # only if env var unset
DEFAULT_MAX_TURNS = 300
DEFAULT_TIMEOUT = 3600
OUTPUT_DIR_PATTERN = ".dev/reflect/post-{slug}-{timestamp}"
```

### 8.4 commands.py

```python
import click
from pathlib import Path
from .models import ReflectRunConfig
from .runner import run_reflect

@click.group()
def reflect_group():
    """Run sc:reflect as an isolated subprocess."""
    pass

@reflect_group.command("run")
@click.argument("taskfile", type=click.Path(exists=True, path_type=Path))
@click.option("--diff", default="HEAD~1..HEAD", help="Git diff ref for reflect")
@click.option("--model", default="", help="Model for the child session")
@click.option("--max-turns", default=300, type=int)
@click.option("--timeout", default=3600, type=int, help="Subprocess timeout in seconds")
@click.option("--output-dir", type=click.Path(path_type=Path), default=None)
@click.option("--promote", is_flag=True, help="Enable Wave 7 promotion")
@click.option("--spec", default=None, help="Spec/PRD path for reflect")
@click.option("--tasklist", default=None, help="Tasklist path for reflect")
@click.option("--no-mcp", is_flag=True)
def run(taskfile, diff, model, max_turns, timeout, output_dir, promote, spec, tasklist, no_mcp):
    """Run /sc:reflect --mode post as an isolated claude -p subprocess."""
    config = ReflectRunConfig(
        taskfile=taskfile, diff=diff, model=model,
        max_turns=max_turns, timeout=timeout,
        output_dir=output_dir, promote=promote,
        spec=spec, tasklist=tasklist, no_mcp=no_mcp,
    )
    exit_code = run_reflect(config)
    raise SystemExit(exit_code)
```

### 8.5 main.py Registration

Add the following import + registration line at the bottom of `src/superclaude/cli/main.py`, following the existing deferred-import pattern:

```python
from superclaude.cli.reflect import reflect_group  # noqa: E402,I001  # intentional: deferred subcommand registration

main.add_command(reflect_group, name="reflect")
```

This is added after the existing `init_lite_command` registration (line 434), before the `if __name__ == "__main__"` block.

---

## 9. Env/Isolation Wiring

### 9.1 Child Environment

The child `claude -p` process receives:

```python
def _build_env() -> dict[str, str]:
    env = os.environ.copy()
    env.pop("CLAUDECODE", None)
    env.pop("CLAUDE_CODE_ENTRYPOINT", None)
    return env
```

This is identical to `pipeline/process.py` `build_env()`. The following are inherited naturally:

- `ANTHROPIC_DEFAULT_OPUS_MODEL` — drives the T2 opus reviewer
- `ANTHROPIC_DEFAULT_SONNET_MODEL` — drives the T2 sonnet reviewer
- `ANTHROPIC_DEFAULT_HAIKU_MODEL` — drives the T2 haiku reviewer
- `ANTHROPIC_API_KEY` — API access
- `HOME` — for `~/.claude/settings.json` MCP config
- `PATH` — for `claude` binary resolution
- `CLAUDE_WORK_DIR` (if set) — working directory override

### 9.2 MCP Inheritance

The child reads MCP server definitions from `~/.claude/settings.json` (or the project-level `.claude/settings.json`). Since `CLAUDECODE` is removed, the child does not detect itself as nested and loads all configured MCP servers normally. This is the same isolation pattern the sprint executor uses.

### 9.3 Working Directory

The child runs in the same CWD as the wrapper (the project root). The `--output` dir is resolved relative to CWD. This ensures the child's `--diff HEAD~1..HEAD` resolves against the same git repo.

---

## 10. Resolved Open Questions

### Q1: Which model does the child reflect session use?
**Resolution:** Default to `$ANTHROPIC_DEFAULT_SONNET_MODEL` (the executor's class). The child's reflect skill then uses the three `ANTHROPIC_DEFAULT_*_MODEL` aliases for Tier 2 reviewer composition (haiku + sonnet + opus), so the child is already on a different model than the executor. Caller can override with `--model`.

### Q2: How is the `--diff` resolved for the final task?
**Resolution:** Default `HEAD~1..HEAD` (last commit). The tasklist instruction can provide a more precise ref (e.g., `TASK_START_SHA..HEAD` or a branch name). The wrapper accepts `--diff` as a string passed verbatim to the child.

### Q3: Where does `<output-dir>` go?
**Resolution:** Default `.dev/reflect/post-<taskfile-stem>-<YYYYMMDD-HHMMSS>/`. This matches the reflect skill's own default pattern. The wrapper pins it via `--output` so the return-contract path is deterministic post-exit.

### Q4: What if the task file has no frontmatter?
**Resolution:** Exit 2 (infra-failure). The wrapper requires frontmatter to write the verdict back. The tasklist template guarantees frontmatter on generated task files.

### Q5: How does the wrapper handle the child writing `return-contract.yaml` to a different path?
**Resolution:** It doesn't. The wrapper pins `--output <dir>` on the child invocation. The reflect skill writes `return-contract.yaml` to `<output>/return-contract.yaml` by contract (§9). If the child ignores `--output` (skill bug), the wrapper exits 2.

### Q6: What if multiple reflect runs target the same task file concurrently?
**Resolution:** Out of scope. The tasklist sequential execution guarantees single-threaded task execution. The wrapper does not implement file locking.

### Q7: Should the wrapper validate the return contract before writing frontmatter?
**Resolution:** No. The wrapper is a thin delegation layer. It reads fields, coerces types, and writes. Semantic validation (e.g., "status:success with regression_present:true is contradictory") is the skill's responsibility. The wrapper exits 2 only on structural failures (missing file, unparseable YAML).

### Q8: Does the wrapper support UC-1 (pre-execution) mode?
**Resolution:** Not in v1. The wrapper is designed for UC-2 (post-execution) as the tasklist final-item gate. UC-1 support (pre-execution coverage check) can be added as a second subcommand (`superclaude reflect pre`) if needed. The architecture supports it: same subprocess launch, different prompt flags.

---

## 11. Scope Boundaries

### In Scope
- Spawning a top-level `claude --print` subprocess with reflect prompt
- Waiting for exit with timeout
- Locating and parsing `return-contract.yaml`
- Writing `reflect_post` verdict to task file frontmatter
- Exit-code signaling for gate consumption
- CLI subcommand registration on `superclaude`

### Out of Scope
- Reimplementing reflect waves/tiers/taxonomy
- Running reflect in an Agent-tool subagent
- Auto-commit or git mutation
- UC-1 (pre-execution) mode
- Promotion mutation (delegated to the child skill; wrapper passes `--no-promote` by default)
- Retry logic (if the child fails, the wrapper exits 2; retry is the caller's concern)
- Multi-task tasklist parallel reflect (one task file = one reflect run)

---

## 12. Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Child skill changes `return-contract.yaml` schema | Wrapper reads missing fields → defaults apply | Contract version field checked; WARN if `contract_version != "1.2.0"` |
| Child ignores `--output` flag | `return-contract.yaml` not found → exit 2 | Pin `--output` in argv; verify path exists after exit |
| Subprocess timeout at boundary (299s of 300 turns) | Exit 2, no verdict | Document timeout as hard boundary; caller can increase with `--timeout` |
| Frontmatter YAML format drift (non-standard delimiters) | Parse fails → exit 2 | The `---\n...\n---\n` pattern is enforced by the task-builder skill |
| `os.replace` atomicity on non-POSIX (Windows) | Potential race | Document POSIX-only; Windows not a target platform |
| Child skill's `--no-promote` default bypassed by upstream change | Wrapper would need to add explicit flag | Add `--no-promote` to the prompt string (not just omit `--promote`); it is already there as a hard flag |

---

*End of spec.*
