# QA Report — Task-Integrity Gate (PG4: CLI Orchestration, Phase 3 + Phase 4)

**Topic:** `superclaude reflect run` CLI wrapper — runner + commands + package surface
**Date:** 2026-06-09
**Phase:** task-integrity (adversarial, fix_authorization: true)
**Fix cycle:** N/A (1st pass)

---

## Overall Verdict: PASS

All 11 mandated invariants verified PASS with file:line evidence AND empirical
(live-CLI) confirmation. Zero issues found; zero fixes required. Ruff check +
ruff format-check + `reflect run --help` all green (exit 0).

Adversarial stance applied: every invariant was checked against the actual
source (not agent claims), and the seven highest-risk invariants (1, 2, 3, 5,
6, 7, 8) were additionally re-confirmed by EXECUTING the CLI (`--print-command`,
`--promote`, `--dry-run`) and grepping the emitted output, not just reading code.

---

## Items Reviewed (per-invariant)

| # | Invariant | Result | Evidence |
|---|-----------|--------|----------|
| 1 | §8 prompt has ONLY real reflect flags (no `--allow-single-vendor`/`--timeout`/`--dry-run`/`--promote`/`--remediate`) | PASS | `runner._build_prompt` runner.py:324-339 emits only `/sc:reflect --mode post [--no-promote] --diff --tasklist [--spec] --depth [--executor-model] --output`. Live `--print-command` emitted exactly that set; grep for the 5 forbidden tokens in `--promote` prompt returned NONE. |
| 2 | `--no-promote` default-on, dropped only when `config.promote` True | PASS | runner.py:329-330 `if not config.promote: parts.append("--no-promote")`. Live: default prompt contains `--no-promote`; `--promote` prompt omits it (verified via stderr grep). |
| 3 | `--depth` never `quick` | PASS | Click `type=Choice(["standard","deep"])` commands.py:84; config floor `"standard" if depth=="quick" else depth` config.py:175. Live `--depth deep` and default `standard` confirmed. |
| 4 | Dry-run/print path NEVER constructs/starts ClaudeProcess nor calls `_child_env`; `preflight` never constructs ClaudeProcess | PASS | runner.py:365-378 short-circuit `return`s before `_child_env()` (line 381) and before the only `ClaudeProcess(...)` launch (line 433). `_claude_argv_preview` (341-348) builds a pure string. `preflight` (250-272) uses `shutil.which` only — explicit docstring + no ClaudeProcess. Live `--dry-run` exit 0 created NO output dir. |
| 5 | ClaudeProcess constructed with `timeout_seconds=config.timeout_seconds` (def 3600), non-empty `model`, `output_format="stream-json"`, `env_vars=None`, `max_turns=config.max_turns` (G1, never primitive 100) | PASS | runner.py:433-442 passes all five exactly. config.py:214 timeout defaults 3600; :215 max_turns defaults 250; :156-157 rejects empty model. Primitive defaults confirmed `max_turns=100`, `timeout_seconds=6300` (process.py:43,46) — wrapper overrides both. Live argv shows `--max-turns 250 --output-format stream-json --model claude-opus-4-8[1m]`. |
| 6 | `--resume` G2 short-circuit: skip+exit-0 when `reflect_post.head == HEAD` AND prior verdict `pass`; else fall through; parses nested mapping directly (NOT `extract_frontmatter`) | PASS | runner.py:405-429: guards `prior.get("head")==config.head and prior.get("verdict")=="pass"` → PASS result, exit 0, sidecar written, return. Parser `_read_existing_reflect_post` (275-308) parses the `reflect_post:` block via regex+`yaml.safe_load`, NOT `extract_frontmatter` (grep confirms `extract_frontmatter` appears ONLY in config.py:22,161). |
| 7 | `write_reflect_post` preserves body bytes + sibling keys (string-splice), compare-before-write (`frontmatter-stale`), randomized-same-dir-temp + `os.replace` | PASS | runner.py:132 `raw = read_bytes()`; 149-167 splices ONLY the `reflect_post:` line range, rejoining body + outer text by offset (sibling keys + body untouched); 170-171 re-reads bytes → `"frontmatter-stale"` on mismatch; `_atomic_write_text` (62-81) uses `f".{name}.tmp.{pid}.{uuid}"` + `os.replace` + `finally` cleanup. |
| 8 | `wrapper-result.yaml` sidecar ALWAYS written (every verdict incl. blocked/preflight and resume) | PASS | `write_sidecar` (177-221) called on: preflight-blocked (396-401), resume-skip (423-428), and normal launch (469-474). Dry-run/print path intentionally exempt (FR-12 "does not edit/launch", commands.py:160 "leaves no output-dir artifacts") — confirmed live: `--dry-run` created no dir. |
| 9 | `--tmux` inverts sprint fail-open → fail-closed (missing/garbage `.reflect-exitcode` → blocked exit 2); ONE window; `sc-reflect-` prefix; sentinel under pinned `--output` | PASS | commands.py `_launch_tmux` 225-249: `new-session -d` ONE window (no split-window/panes, 235); unreadable sentinel → `return _BLOCKED_EXIT` (=2, 247-249); prefix `_TMUX_SESSION_PREFIX="sc-reflect-"` (33), `_session_name` (185-188); sentinel `config.output_dir / _EXIT_SENTINEL_NAME` (244) under the pinned output_dir, also forwarded via inner `--output` (208-211). |
| 10 | Exit codes wire to `Verdict.exit_code` (pass 0/halted 10/degraded 11/blocked 2), not re-hardcoded; frontmatter-stale/unwritable downgrades PASS → non-zero (fail-closed FR-6) | PASS | commands.py:156 `exit_code = result.verdict.exit_code`; map lives once in models.py:44-49. runner.py:466-468 `if write_status != "written" and verdict is PASS: verdict=BLOCKED` (→ exit 2). help text restates the contract. |
| 11 | No cross-subcommand-package imports (no `superclaude.cli.sprint`/`.roadmap`); reflect launched ONLY via ClaudeProcess (no Agent/Task/anthropic surface) | PASS | Recursive grep of `src/superclaude/cli/reflect/` for `sprint`/`roadmap`/`Agent`/`Task`/`anthropic`/`async def`/`await` matches ONLY docstrings/comments — zero real imports or surfaces. The sole launch primitive is `ClaudeProcess` (runner.py:32 import, :433 construct). main.py:436-438 registers via `main.add_command(reflect_group, name="reflect")`. |

---

## Summary

- Checks passed: 11 / 11
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (none required)

**Confidence:** Verified: 11/11 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 7 | Grep: 5 | Glob: 0 | Bash: 6 (incl. 4 live-CLI executions)

Tool engagement (16 verifying calls) exceeds the 11-item checklist minimum;
each call mapped to a specific invariant (no padding). The 4 live-CLI runs
(`--print-command`, `--print-command --promote`, `--dry-run`, `--help`) provide
independent empirical corroboration beyond source reading for invariants 1-5, 8.

---

## Issues Found

None.

---

## Actions Taken

No fixes applied — no issues found. Verification commands run from worktree root
`/config/workspace/IronClaude/.claude/worktrees/reflectWrapper`:

- `uv run ruff check src/superclaude/cli/reflect/ src/superclaude/cli/main.py` → **All checks passed!**
- `uv run ruff format --check src/superclaude/cli/reflect/ src/superclaude/cli/main.py` → **7 files already formatted**
- `uv run superclaude reflect run --help` → **exit 0**, all 9 §9 options listed (`--tmux`, `--print-command`, `--promote/--no-promote`, `--timeout`, `--depth`, `--output`, `--allow-single-vendor`, `--dry-run`, `--resume`)

---

## Adversarial Residual Observations (non-blocking, NOT issues)

These are documented for completeness per zero-trust discipline. None are
defects; none warrant a fix. Recorded so a later reviewer need not re-derive.

1. **`--spec` / `--executor-model` absent in the live `--print-command` prompt.**
   Correct behaviour: the probe tasklist (`research/01-claudeprocess-primitive.md`)
   has no `spec_path`/`executor_model_class` frontmatter and no `EXECUTOR_MODEL_CLASS`
   env, so both flags are conditionally omitted (runner.py:333-337). When present
   they are appended as `--spec <abs>` / `--executor-model <class>` per §8. Not a gap.

2. **Write-back TOCTOU window (compare-then-replace).** A microscopic window exists
   between the byte re-read (runner.py:170) and `os.replace` inside `_atomic_write_text`.
   This is inherent to compare-before-write and explicitly accepted by the spec/FR-6
   ("last-write-wins window is bounded", runner.py:16-17) and the
   `feedback_parallel_sessions_share_index` guidance (run the gate from the tasklist's
   own worktree). Acceptable by design.

3. **Dry-run prompt routed to stderr, argv to stdout** (runner.py:366-367). This is a
   deliberate stdout/stderr split, not a defect — the argv is the machine-consumable
   line; the prompt is informational. Help text covers both ("argv + prompt").

---

## Recommendations

Green light to proceed. Phase 3 (runner) and Phase 4 (commands + registration)
of the `superclaude reflect run` wrapper satisfy all 11 task-integrity invariants
against the merged-requirements spec (FR-1, FR-6, FR-7, FR-9, FR-10, FR-12, §5,
§8, §9). No remediation required before downstream phases.

## QA Complete
