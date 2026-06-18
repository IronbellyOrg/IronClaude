# /sc:cli-eval run — eval_smoke — Step Trace (with_skill, iteration-2)

Date: 2026-06-12. Working dir (worktree):
`/config/workspace/IronClaude/.dev/worktrees/troubleshoot-hardening-evals`
Mode: non-interactive subagent (AskUserQuestion steps replaced by "state the menu, pick default").
Constraints honored: UV only; every command capped with `timeout 180`; read-only except this output trace.

---

## Wave 0 — Fresh-context load (mandatory, both pipelines)

Per SKILL.md Wave 0, the contract surface is re-read and cited before any action. (A live run would
delegate this to the `eval-docs-loader` agent; as a constrained subagent I read the canonical sources
directly.)

Fresh-context citations (all re-read this turn):

- **Exit codes** — `src/superclaude/cli/eval/exit_codes.py:21-24`: `SUCCESS=0`, `FAILURES=1`,
  `USAGE_ERROR=2` (operator misuse / config / harness / **FR-G5 coverage gate**), `INTERRUPTED=3`.
- **Suite manifest** — `src/superclaude/cli/eval/suites/eval_smoke.yaml:29-113`: `name: eval_smoke`,
  `version: "1.0"`, 3 evals **ES1/ES2/ES3, each `no_pty: skip`**, `home_strategy: ephemeral`,
  `timeout_sec` 60/60/120. So a `--no-pty` run SKIPs the whole suite (CI-canary, not a real pass).
- **`eval run` flag surface** — `src/superclaude/cli/eval/commands.py:1555-1650`: `--suite`,
  `--parallel`, `--eval`, `--no-mcp`, `--no-pty`, `--output-dir`, `--keep-home`, `--timeout-mult`,
  `--max-disk-mb`, `--json`, `--verbose`, `--junit`. (Confirms the run command adds NO new flags.)
- **AUTHORITATIVENESS — the executor** — `commands.py:1357-1405`: `_resolve_executor_factory()`
  unconditionally returns a factory that constructs `_NullLifecycleExecutor` (production
  `ClaudeProcessAdapter`+`PtyDriver` lands at milestone M5/M6, NOT yet wired). The factory is tagged
  `produces_null_executor = True`. `_NullLifecycleExecutor.observe()` returns canned
  `exit_code=0, stdout="", stderr="", duration=0.0` — no subprocess spawned.
- **Warning + its `--json` suppression** — `commands.py:1879-1885`: when the factory
  `produces_null_executor` **and `not as_json`**, the runner emits to stderr:
  `eval run: WARNING: _NullLifecycleExecutor active — non-production executor selected; run results
  MUST NOT be treated as authoritative.` The `--json` guard suppresses it for clean machine output —
  this is exactly the line the skill's W5 / eval-run-reporter spec mandates capturing via `--verbose`.
- **FR-G5 + empty-HOME workaround** — `docs/eval/suites-guide.md:32-35, 526-537`: the FR-G5 doctor
  preflight checks every `~/.claude/settings.json` PreToolUse/PostToolUse matcher against the suite;
  uncovered matchers → exit 2 `coverage gate FAILED`. Workaround: `TMPHOME=$(mktemp -d) && HOME=$TMPHOME
  uv run superclaude eval run --suite <name> --no-mcp; rm -rf "$TMPHOME"` (empty HOME has no matchers).
- **AC12 scratch-root allowlist** — discovered at runtime (see Step W3-probe): `--output-dir` must
  resolve under `/tmp/eval-runs/` or `<repo>/.dev/eval-runs/`; arbitrary `--output-dir` → exit 2.
- **Host preflight** — `command -v claude jq make git` → all present
  (`/config/.local/bin/claude`, `/usr/bin/jq`, `/usr/bin/make`, `/usr/bin/git`); the 4 `failure_mode:
  hard` binaries are satisfied. Host `HOME=/config`, `~/.claude/settings.json` exists (3043 bytes) →
  FR-G5 is a live risk → empty-HOME workaround required for a real run.

Gate: no canonical source missing/moved. Digest complete. Proceed to run branch.

---

## RUN PIPELINE

### W1 — Enumerate via the CLI

```
timeout 180 uv run superclaude eval list --json
```
EXIT=0. Returned a JSON array of 13 suites. `eval_smoke` present: `{ "name": "eval_smoke",
"version": "1.0", "eval_count": 3 }`. (Going through the loader, not scraping the dir, so the menu
matches what `eval run --suite` accepts.)

### W2 — Interactive selection (menu I WOULD show; default picked)

Menu (AskUserQuestion in a live run):
```
1. adversarial_merge_consistency — v1.0 — 3 evals
2. agent_grounding_drift — v1.0 — 2 evals
3. audit_wiring_guard — v1.0 — 2 evals
4. eval_cli_doc_parity — v1.0 — 3 evals
5. eval_smoke — v1.0 — 3 evals        <-- DEFAULT (task target)
6. freshness_blocks_unread_edit — v1.0 — 3 evals
7. frontier_vs_cheap_combo — v1.0 — 4 evals
8. hook_latency_drift — v1.0 — 3 evals
9. installer_sync_drift — v1.0 — 1 eval
10. model_capability_matrix — v1.0 — 8 evals
11. real — v1.0 — 17 evals
12. task_classification_contract — v1.0 — 2 evals
13. tasklist_deterministic_shape — v1.0 — 1 eval
```
Selected: **eval_smoke** (all 3 evals, no `--eval` filter).

Drill-in:
```
timeout 180 uv run superclaude eval describe --suite eval_smoke
```
EXIT=0. Confirmed ES1/ES2/ES3, all `no_pty: skip`, `home_strategy: ephemeral`, timeouts 60/60/120s.

### W3 — Confirm invocation + flags (menu I WOULD show; default picked) + gotchas surfaced

**Gotcha 1 — FR-G5 coverage gate (exit 2):** host `~/.claude/settings.json` is populated, so a run
under the real `$HOME` risks `coverage gate FAILED`. → use the empty-HOME workaround.

**Gotcha 2 — `--no-pty` → SKIPPED:** every eval_smoke entry is `no_pty: skip`, so `--no-pty` would
short-circuit ALL 3 to SKIPPED (`skip_reason="--no-pty"`, exit 0). That is the CI-canary path, NOT a
real pass. To get real PASS/FAIL I must OMIT `--no-pty`.

**Authoritativeness decision (skill W5):** prefer `--verbose` over `--json` so the
`_NullLifecycleExecutor` warning is NOT suppressed. Chosen invocation (default):
```
TMPHOME=$(mktemp -d) && HOME=$TMPHOME uv run superclaude eval run \
  --suite eval_smoke --no-mcp --verbose --junit ; rm -rf "$TMPHOME"
```
(omit `--no-pty` for a real run; omit `--output-dir` so the default FR-G4 layout under
`<repo>/.dev/eval-runs/` stays inside the AC12 allowlist; `--no-mcp` for host-agnostic gates.)

### W3-probe — first attempt hit AC12 (my error, corrected)

```
TMPHOME=$(mktemp -d) && HOME=$TMPHOME timeout 180 uv run superclaude eval run \
  --suite eval_smoke --no-mcp --verbose --junit --output-dir "$TMPHOME/evalout"
```
EXIT=2 — NOT FR-G5. The `--output-dir` under `$TMPHOME` escaped the **AC12 scratch-root allowlist**
(`/tmp/eval-runs/` or `<repo>/.dev/eval-runs/`). Corrected by dropping `--output-dir`.

### W4 — Run (bounded foreground; 0.01s so no background needed)

```
TMPHOME=$(mktemp -d) && HOME=$TMPHOME timeout 180 uv run superclaude eval run \
  --suite eval_smoke --no-mcp --verbose --junit ; rm -rf "$TMPHOME"
```
EXIT=0. Captured output (decisive):
```
eval run: WARNING: _NullLifecycleExecutor active — non-production executor selected;
  run results MUST NOT be treated as authoritative.
run 140645Z-4e7503b0: 3P/0F/0S/0E/0I/0T in 0.01s ->
  .../.dev/eval-runs/2026-06-12/140645Z-4e7503b0
```
The `MUST NOT be treated as authoritative` warning fired on the `--verbose` path. **This is the
authoritativeness tell.** Because `--no-pty` was omitted, the `no_pty: skip` short-circuit did NOT
fire — the evals went "through" the executor path, but that path is the null stub returning canned
exit 0 in 0.01s with no `claude` subprocess.

### W4-contrast — `--json` suppresses the warning (proves the skill's W5 point)

```
TMPHOME=$(mktemp -d) && HOME=$TMPHOME timeout 180 uv run superclaude eval run \
  --suite eval_smoke --no-mcp --json 2>&1 | grep -c "MUST NOT be treated as authoritative"
```
Result: **0** warning lines. Confirms `--json` hides the non-production-executor warning — which is
exactly why the protocol mandates a `--verbose` run for the authoritativeness probe.

### W5 — Parse summary.json + report

Run dir: `<repo>/.dev/eval-runs/2026-06-12/140645Z-4e7503b0/`
Files: `summary.{md,json,yaml}`, `junit.xml`, `per-eval/`, `homes/` (empty).

`summary.json` (truth): `totals: passed=3 failed=0 skipped=0 errored=0 interrupted=0 timeout=0`;
`counts.manifest_n=3 kept_k=3 skipped_s=0`. Each eval ES1/ES2/ES3: `status: "PASS"`,
`duration_sec: 0.0`, **`expects: []`** (no assertions evaluated), **`artifacts: {}`** (no preserved
HOME). `homes/` dir is empty — null executor returned PASS so HOMEs were removed (none to forensically
preserve).

Process exit reconciliation: exit 0 ↔ totals (0 failed/errored/timeout). Consistent — but the PASS is
the stub's canned `exit_code=0`, NOT a real eval assertion pass.

**Verdict: PASS (3/3), but NON-AUTHORITATIVE (plumbing only).** See report.md.
