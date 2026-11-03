# E2E Test Guide — `superclaude eval` and `/sc:cli-eval` (`5.0.0`)

- **Capability:** `superclaude eval` is the cliEval harness for maintainers: `list` shows the bundled eval suites, `describe` prints one suite after validation, `doctor` checks that the host can run evals, and `run` runs a suite and writes `summary.md`, `summary.json`, `summary.yaml` (and `junit.xml` on request) into a run folder; `/sc:cli-eval` is the Claude Code command that authors a new suite (`create`) or picks, runs and reports on an existing one (`run`).
- **Audience:** maintainer / QA (not an end-user feature)
- **Source of truth:** `src/superclaude/cli/eval/commands.py:601-606,642-647,740-753,821-971,1205-1288,1357-1405,1530-1550,1555-2004`; `src/superclaude/cli/eval/config.py:42-70,165-248`; `src/superclaude/cli/eval/artifact_layout.py:76,151-199`; `src/superclaude/cli/eval/run_report.py:391-408`; `src/superclaude/cli/eval/coverage.py:78,84,99-103`; `src/superclaude/cli/eval/exit_codes.py:21-24`; `src/superclaude/cli/eval/suites/` (17 manifests); `src/superclaude/hooks/hooks.json:100`; `src/superclaude/commands/cli-eval.md:12-52`; `src/superclaude/skills/sc-cli-eval-protocol/SKILL.md:46-58,117-165,197-208`; `superclaude eval --help` and the `--help` of its four subcommands
- **Est. time:** `Tier A: 5 minutes. Tier B: 10 minutes (no API call). Tier C: 15-20 minutes (one interactive Claude Code session).`

## Preconditions

- IronClaude 5.0.0 installed for your user: `superclaude --version` prints `SuperClaude, version 5.0.0`.
- A Linux host. `eval doctor` refuses any other system with exit 2 (`commands.py:843-849`); `list`, `describe` and `run` have no platform check in the code.
- `claude`, `make`, `jq` and `git` on your `PATH`, `claude --version` at least 0.5.0, and a `~/.claude/` folder: these are the HARD rows of `eval doctor` (Step 5). The steps use `jq` to read JSON.
- A bash shell. None of these paths exist: `/tmp/d15` and `/tmp/eval-runs/t1` to `/tmp/eval-runs/t7` (Step 7 checks). `/tmp/eval-runs` itself may already exist and hold other people's runs; this guide writes only into its own `t1`-`t7` sub-folders.
- Every file Tier B and Tier C create is under `/tmp/d15` or `/tmp/eval-runs/t1`..`t7`. No step installs, registers or edits anything under `~/.claude`. `eval run` reads `~/.claude/settings.json` for its coverage gate (Step 13) and writes nothing there.
- Tier C only (Step 15): the `claude` CLI logged in, and `uv` on your `PATH` (the `/sc:cli-eval` protocol runs the CLI as `uv run superclaude eval ...`, `SKILL.md:124,150`; outside a uv project `uv run superclaude` runs the installed command). The session uses your real `~/.claude`: Claude Code keeps the session in your normal history, and the hooks installed in `~/.claude/settings.json` also write `~/.claude/state/` and `~/.claude/logs/`: the freshness hooks at session start and on each prompt (`src/superclaude/hooks/hooks.json:18,49`; `src/superclaude/hooks/scripts/freshness-session-start.sh:8-9`; `freshness-user-prompt.sh:8-10`) and `auggie-flag-clear.sh` after auggie tool calls (`hooks.json:104`; `auggie-flag-clear.sh:10-12`).

## What you're verifying

- `eval list` shows 17 suites (87 evals in total; `real` has 17) and exits 0; `eval describe` prints a validated suite as YAML or JSON and exits 2 for an unknown suite or eval id.
- `eval doctor --json --no-mcp` exits 0 on a ready host: 11 rows, no HARD failure, the four MCP rows skipped by the flag and `vendored.ptytest` a soft skip (the PTY harness is not shipped).
- `--output-dir` must be a strict sub-folder of `/tmp/eval-runs` or of `<current folder>/.dev/eval-runs`; the bare `/tmp/eval-runs` and any other path exit 2 with the scratch-root policy text, before anything is written (`config.py:241-248`).
- `eval run --suite real --no-pty --no-mcp --output-dir /tmp/eval-runs/t1 --junit` exits 0, marks all 17 evals `SKIPPED` (`--no-pty`), and writes `summary.md`, `summary.json`, `summary.yaml` and `junit.xml` into `/tmp/eval-runs/t1/.dev/eval-runs/<YYYY-MM-DD>/<HHMMSSZ>-<8 hex>/`: `--output-dir` is the output root, not the run folder (`commands.py:1721-1737`; `artifact_layout.py:151-199`).
- **Results are not authoritative in 5.0.0.** `eval run` always uses `_NullLifecycleExecutor`, which starts no Claude process and returns exit 0 with empty output for every eval (`commands.py:1357-1405`), and prints `eval run: WARNING: _NullLifecycleExecutor active — non-production executor selected; run results MUST NOT be treated as authoritative.` on stderr unless `--json` is given (`commands.py:1879-1885`). Without `--no-pty` the `real` suite reports 17 `PASS` in well under a second (Step 12): that is the stub, not a test result.
- Exit codes of `eval run`: 0 clean, 1 at least one FAIL / ERRORED / TIMEOUT / XPASS, 2 harness rejection (bad flag, scratch-root violation, unknown suite or eval, coverage gate, disk budget), 3 interrupted (`commands.py:1989-2004`; `exit_codes.py:21-24`; `eval run --help`).
- `/sc:cli-eval run` lists suites through the CLI, asks you to pick one and confirm the exact command and flags, runs it, and reports per-eval status from `summary.json`, labelling an all-`SKIPPED` run as skipped (not passed) and a null-executor run as non-authoritative.
- **Observed-as-coded in 5.0.0** (record, do not mark FAIL):
  - `eval run` creates the run folder and its empty `homes/` before it looks up the suite and the `--eval` ids, so an unknown suite or eval id exits 2 but leaves that folder behind (`commands.py:1753-1811`; Step 11).
  - The coverage-gate failure message of `eval run` starts with `eval doctor:` (one formatter serves both commands, `commands.py:642-647,1828`; Step 13).
  - `eval run --help` says `--output-dir` "Defaults to `.dev/eval-runs/<run-id>/`"; the code uses `<current folder>/.dev/eval-runs/<YYYY-MM-DD>/<run-id>/` (`commands.py:1331-1339`; Step 14).
  - Two runs of the same suite started in the same second get the same run id, because the id is a hash of the suite name and the start time in whole seconds (`artifact_layout.py:151-171`; Step 10).
  - The policy text lists "`--output-dir <path>` -- extends the allowlist", but the `--output-dir` value must itself sit under one of the two roots (`commands.py:1727-1734`; `config.py:241-248`; Step 6).

Settings this guide does not exercise: `--keep-home` (nothing to keep: the null executor passes and per-eval HOMEs are removed on PASS), `--timeout-mult` above 0, `--max-disk-mb` above 0 and the disk-budget breach, `eval doctor --parallel 15` on a host with less than 2.25 GB free RAM, and the `/sc:cli-eval create` pipeline (it writes a new suite into the package source and runs `/sc:spec-panel` and `/sc:adversarial`, `SKILL.md:66-113`).

---

## Steps

### Tier A — free smoke (read-only)

Run Tier A from `/tmp` (`cd /tmp`). These commands write nothing.

#### Step 1 — Version and the `eval` subcommands `[FREE]`

**Do:**

```bash
cd /tmp
superclaude --version
superclaude eval --help | sed -n '/^Commands:/,$p'
superclaude eval run --help | grep -E -- '^  --(suite|parallel|eval|no-mcp|no-pty|output-dir|keep-home|timeout-mult|max-disk-mb|json|verbose|junit) '
```

**Expected result:**

```text
SuperClaude, version 5.0.0
Commands:
  describe  Print a validated, post-parameterize-expansion manifest.
  doctor    Verify host preconditions for ``superclaude eval run``.
  list      Enumerate suite manifests under ``cli/eval/suites/``.
  run       Run a cliEval suite end-to-end (FR-CLI1 / D-0072).
  --suite TEXT            Suite name, filename stem, or path to a manifest.
  --parallel INTEGER      Worker concurrency. Values below 1 clamp to 1;
  --eval TEXT             Filter to one or more post-expansion eval ids (e.g.
  --no-mcp                Mark MCP capabilities as skipped-by-flag (FR-CLI1 /
  --no-pty                Run without the vendored PTY harness (degrades
  --output-dir DIRECTORY  Destination directory for ``summary.{md,json,yaml}``
  --keep-home             Preserve per-eval HOME directories on PASS (default
  --timeout-mult FLOAT    Multiplier applied to each spec's ``timeout_sec``
  --max-disk-mb INTEGER   Disk-budget ceiling for ``output_dir`` in megabytes.
  --json                  Emit the run summary as JSON to stdout in addition
  --verbose               Print a human-readable summary line to stdout when
  --junit                 Also write a JUnit XML report (``junit.xml``) into
```

The full `run` help lists the exit codes 0, 1, 2 and 3 and the defaults `--parallel 8`, `--timeout-mult 1.0`, `--max-disk-mb 1024`. (source: `pyproject.toml:7`; options `commands.py:1555-1654`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 2 — `eval list` `[FREE]`

**Do:**

```bash
cd /tmp
superclaude eval list; echo "exit=$?"
superclaude eval list --json | jq -r 'length, (map(.eval_count) | add)'
```

**Expected result:**

```text
superclaude eval list:
  - adversarial_merge_consistency (version 1.0, 3 evals)
  - agent_grounding_drift (version 1.0, 2 evals)
  - audit_wiring_guard (version 1.0, 2 evals)
  - cli_eval_skill_contract (version 1.0, 2 evals)
  - eval_cli_doc_parity (version 1.0, 3 evals)
  - eval_smoke (version 1.0, 3 evals)
  - freshness_blocks_unread_edit (version 1.0, 3 evals)
  - frontier_vs_cheap_combo (version 1.0, 4 evals)
  - hook_latency_drift (version 1.0, 3 evals)
  - installer_sync_drift (version 1.0, 1 eval)
  - model_capability_matrix (version 1.0, 8 evals)
  - post_release_command_contract (version 1.0, 4 evals)
  - real (version 1.0, 17 evals)
  - suite_schema_guard (version 1.0, 2 evals)
  - task_classification_contract (version 1.0, 2 evals)
  - tasklist_deterministic_shape (version 1.0, 1 eval)
  - workflow_vs_task_builder (version 1.0, 27 evals)
exit=0
17
87
```

The count is after parameterized rows are expanded; a suite with one eval says `1 eval`. (source: `commands.py:924-971`, row format `commands.py:740-753`; manifests in `src/superclaude/cli/eval/suites/`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 3 — `eval describe` `[FREE]`

**Do:**

```bash
cd /tmp
superclaude eval describe --suite eval_smoke | grep -E '^(name|version):|^- id:|^  no_pty:|^- name:'; echo "exit=${PIPESTATUS[0]}"
superclaude eval describe --suite eval_smoke --json | jq -r '.evals[].id'
superclaude eval describe --suite eval_smoke --eval ES2 | head -3
```

**Expected result:**

```text
name: eval_smoke
version: '1.0'
- name: claude
- name: jq
- name: make
- name: git
- id: ES1
  no_pty: skip
- id: ES2
  no_pty: skip
- id: ES3
  no_pty: skip
exit=0
ES1
ES2
ES3
id: ES2
title: eval list --json enumerates suite manifests
category: cli-smoke
```

Default output is YAML, `--json` gives JSON, `--eval` prints only that eval. `--suite` also accepts a file stem or a path to a manifest. Every `eval_smoke` eval carries `no_pty: skip`, so `--no-pty` skips the whole suite. (source: `commands.py:1205-1288`; `src/superclaude/cli/eval/suites/eval_smoke.yaml`; `eval describe --help`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 4 — `eval describe` rejections `[FREE]`

**Do:**

```bash
cd /tmp
superclaude eval describe --suite nope; echo "exit=$?"
superclaude eval describe --suite eval_smoke --eval ES9; echo "exit=$?"
```

**Expected result:**

```text
eval describe: SuiteNotFound: no manifest matched --suite 'nope' in <install path>/superclaude/cli/eval/suites
exit=2
eval describe: EvalNotFound: eval 'ES9' not in suite 'eval_smoke' (known: ES1, ES2, ES3)
exit=2
```

`<install path>` is the `site-packages` folder of your install (for a pipx install, `~/.local/share/pipx/venvs/superclaude/lib/python3.<n>/site-packages`). (source: `commands.py:1264-1281`; `eval describe --help`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 5 — `eval doctor` `[FREE]`

**Do:**

```bash
cd /tmp
superclaude eval doctor --json --no-mcp | jq -c '{hard_failures, skip_flags, soft_skips, coverage_gate, rows: (.report|length)}'; echo "exit=${PIPESTATUS[0]}"
superclaude eval doctor --json --no-mcp | jq -r '.report[] | "\(.name) \(.passed) \(.failure_mode)"'
superclaude eval doctor --no-mcp | tail -3; echo "exit=${PIPESTATUS[0]}"
```

**Expected result:**

```text
{"hard_failures":[],"skip_flags":["--no-mcp"],"soft_skips":["mcp_server.auggie","mcp_server.auggie-mcp","mcp_server.airis-mcp-gateway","mcp_server.tavily","vendored.ptytest"],"coverage_gate":{"requested":false,"status":"skipped"},"rows":11}
exit=0
binary.claude true hard
binary.make true hard
binary.jq true hard
binary.git true hard
mcp_server.auggie false skip
mcp_server.auggie-mcp false skip
mcp_server.airis-mcp-gateway false skip
mcp_server.tavily false skip
claude.min_version true hard
filesystem.claude_home true hard
vendored.ptytest false skip
skip flags: --no-mcp
all HARD capabilities satisfied
soft skips: mcp_server.auggie, mcp_server.auggie-mcp, mcp_server.airis-mcp-gateway, mcp_server.tavily, vendored.ptytest
exit=0
```

The four MCP rows carry `skipped_by_flag: true`. `vendored.ptytest` is a soft skip on every 5.0.0 install: its detail says `<install path>/superclaude/cli/eval/pty/__init__.py not found (vendored at M2)`. A missing HARD row prints `eval doctor: HARD failures` on stderr and exits 2 (edge-case table). (source: `commands.py:821-921`; rows `commands.py:159-200,427`, `src/superclaude/cli/eval/capabilities.py:186-234`; `eval doctor --help`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 6 — The scratch-root rule, checked by `doctor --output-dir` `[FREE]`

**Do:**

```bash
cd /tmp
superclaude eval doctor --no-mcp --output-dir /tmp/eval-runs/t1 >/dev/null; echo "exit=$?"
ls -d /tmp/eval-runs/t1 2>/dev/null || echo "no t1"
superclaude eval doctor --no-mcp --output-dir /tmp/eval-runs >/dev/null; echo "exit=$?"
superclaude eval doctor --no-mcp --output-dir /tmp/d15/out 2>&1 >/dev/null | head -1; echo "exit=${PIPESTATUS[0]}"
```

**Expected result:**

```text
exit=0
no t1
eval doctor: scratch path escapes AC12 allowlist: path=/tmp/eval-runs resolved=/tmp/eval-runs allowed=[/tmp/eval-runs, /tmp/.dev/eval-runs]

cliEval scratch root policy (AC12 / OPS-002):
  Scratch HOMEs, per-eval working trees, and --output-dir targets MUST
  resolve under one of these allowed roots:
    1. /tmp/eval-runs/        -- canonical M1 scratch root
    2. <repo>/.dev/eval-runs/ -- repo-relative scratch root
    3. --output-dir <path>    -- extends the allowlist for the current
                                  invocation only (call-scoped, never
                                  mutates EvalConfig.allowed_scratch_roots)
  Anything else is rejected before any filesystem write.
  Authoritative reference: docs/eval/scratch-roots.md.
exit=2
eval doctor: scratch path escapes AC12 allowlist: path=/tmp/d15/out resolved=/tmp/d15/out allowed=[/tmp/eval-runs, /tmp/.dev/eval-runs]
exit=2
```

`doctor --output-dir` only checks the path and creates nothing. The second allowed root is `.dev/eval-runs` under the current folder (here `/tmp`), not a fixed repo path. Only strict sub-folders pass: the bare root is refused (rule H4). `docs/eval/scratch-roots.md` is a file in the source repo, not installed. Observed-as-coded: item 3 of the policy does not let an arbitrary `--output-dir` through (third command). (source: `commands.py:851-859`; policy `config.py:42-53`; roots `config.py:65-70`; check `config.py:227-248`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

### Tier B — local runs (no API call)

Run Tier B in one terminal, in the order given.

#### Step 7 — Create the sandbox `[LOCAL-WRITE]`

**Do:**

```bash
for d in /tmp/d15 /tmp/eval-runs/t1 /tmp/eval-runs/t2 /tmp/eval-runs/t3 /tmp/eval-runs/t4 /tmp/eval-runs/t5 /tmp/eval-runs/t6 /tmp/eval-runs/t7; do [ ! -e "$d" ] || echo "STOP: $d exists"; done
mkdir -p /tmp/d15 && cd /tmp/d15 && pwd
grep -c 'mcp__auggie__' ~/.claude/settings.json 2>/dev/null || echo "no matcher"
```

**Expected result:** no `STOP` line, then `/tmp/d15`. The last line is a number of at least `1` if the IronClaude hooks are installed in your `~/.claude/settings.json` (the `auggie-flag-clear.sh` PostToolUse matcher, `hooks.json:100`), else `0` or `no matcher`. Write it down: Step 13 depends on it. (source: `src/superclaude/hooks/hooks.json:98-108`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 8 — `eval run --suite real --no-pty` with JUnit `[LOCAL-WRITE]`

**Do:**

```bash
cd /tmp/d15
superclaude eval run --suite real --no-pty --no-mcp --output-dir /tmp/eval-runs --junit; echo "exit=$?"
superclaude eval run --suite real --no-pty --no-mcp --output-dir /tmp/eval-runs/t1 --junit; echo "exit=$?"
find /tmp/eval-runs/t1 -mindepth 1 | sort
```

**Expected result:**

```text
scratch path escapes AC12 allowlist: path=/tmp/eval-runs resolved=/tmp/eval-runs allowed=[/tmp/eval-runs, /tmp/d15/.dev/eval-runs]

cliEval scratch root policy (AC12 / OPS-002):
  ... (the same nine policy lines as Step 6)
exit=2
eval run: WARNING: _NullLifecycleExecutor active — non-production executor selected; run results MUST NOT be treated as authoritative.
exit=0
/tmp/eval-runs/t1/.dev
/tmp/eval-runs/t1/.dev/eval-runs
/tmp/eval-runs/t1/.dev/eval-runs/<YYYY-MM-DD>
/tmp/eval-runs/t1/.dev/eval-runs/<YYYY-MM-DD>/<RUN>
/tmp/eval-runs/t1/.dev/eval-runs/<YYYY-MM-DD>/<RUN>/homes
/tmp/eval-runs/t1/.dev/eval-runs/<YYYY-MM-DD>/<RUN>/junit.xml
/tmp/eval-runs/t1/.dev/eval-runs/<YYYY-MM-DD>/<RUN>/summary.json
/tmp/eval-runs/t1/.dev/eval-runs/<YYYY-MM-DD>/<RUN>/summary.md
/tmp/eval-runs/t1/.dev/eval-runs/<YYYY-MM-DD>/<RUN>/summary.yaml
```

The bare root is refused before anything is written (no `eval run:` prefix on this message). `<YYYY-MM-DD>` is today's UTC date and `<RUN>` is `<HHMMSSZ>-<8 hex>`, the UTC start time plus a hash of the suite name and start time; `homes/` stays empty. The WARNING goes to stderr. (source: scratch root `commands.py:1727-1751`; layout `artifact_layout.py:151-199`; WARNING `commands.py:1879-1885`; reports `run_report.py:391-408`, JUnit only with `--junit`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 9 — Read the reports `[FREE]`

**Do:**

```bash
R=$(ls -d /tmp/eval-runs/t1/.dev/eval-runs/*/*/); echo "$R"
grep '^## Result' "$R/summary.md"
jq -c '.totals' "$R/summary.json"
jq -c '.counts' "$R/summary.json"
jq -r '.evals[] | "\(.eval_id) \(.status) \(.skip_reason)"' "$R/summary.json" | head -3
jq -r '.evals | length' "$R/summary.json"
grep -o 'tests="[0-9]*" failures="[0-9]*" errors="[0-9]*" skipped="[0-9]*"' "$R/junit.xml"
grep -E '^(run_id|parallel|manifest_version):' "$R/summary.yaml"
```

**Expected result:**

```text
/tmp/eval-runs/t1/.dev/eval-runs/<YYYY-MM-DD>/<RUN>/
## Result: 0 passed, 0 failed, 17 skipped, 0 errored, 0 interrupted, 0 timeout
{"passed":0,"failed":0,"skipped":17,"errored":0,"interrupted":0,"timeout":0}
{"manifest_n":17,"expanded_n_prime":17,"kept_k":0,"skipped_s":17,"kept_plus_skipped_equals_n_prime":true}
E1 SKIPPED --no-pty
E2.1 SKIPPED --no-pty
E2.2 SKIPPED --no-pty
17
tests="17" failures="0" errors="0" skipped="17"
run_id: <RUN>
manifest_version: '1.0'
parallel: 8
```

`summary.md` has a table row per eval (E1, E2.1-E2.3, E3-E7, E9-E16) with status `SKIPPED` and note `--no-pty`. Every `real` eval is tagged `no_pty: skip`, and with `--no-pty` such an eval is marked `SKIPPED` before any per-eval HOME is made. A skipped run is not a pass. (source: skip `commands.py:1887-1905`; summary fields `commands.py:1953-1974`; `src/superclaude/cli/eval/suites/real.yaml` `no_pty: skip` on every eval)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 10 — `--verbose` and `--json` `[LOCAL-WRITE]`

**Do:**

```bash
cd /tmp/d15
superclaude eval run --suite real --no-pty --no-mcp --output-dir /tmp/eval-runs/t2 --verbose; echo "exit=$?"
superclaude eval run --suite real --no-pty --no-mcp --output-dir /tmp/eval-runs/t3 --json 2>&1 | head -2; echo "exit=${PIPESTATUS[0]}"
```

**Expected result:**

```text
eval run: WARNING: _NullLifecycleExecutor active — non-production executor selected; run results MUST NOT be treated as authoritative.
run <RUN>: 0P/0F/17S/0E/0I/0T in 0.00s -> /tmp/eval-runs/t2/.dev/eval-runs/<YYYY-MM-DD>/<RUN>
exit=0
{
  "run_id": "<RUN>",
exit=0
```

`--verbose` adds the one-line summary (passed / failed / skipped / errored / interrupted / timeout). `--json` prints the whole summary on stdout and suppresses the WARNING, even with stderr merged as here: use `--verbose` when you need to see it. Observed-as-coded: if both runs start in the same second they show the same `<RUN>`. (source: summary line `commands.py:1530-1550,1983-1984`; JSON `commands.py:1979-1982`; WARNING guard `commands.py:1879`; run id `artifact_layout.py:151-171`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 11 — `--eval` filter and an unknown id `[LOCAL-WRITE]`

**Do:**

```bash
cd /tmp/d15
superclaude eval run --suite real --no-pty --no-mcp --eval E1 --eval E2.1 --output-dir /tmp/eval-runs/t4 --verbose 2>/dev/null; echo "exit=$?"
superclaude eval run --suite real --no-pty --no-mcp --eval E99 --output-dir /tmp/eval-runs/t5; echo "exit=$?"
find /tmp/eval-runs/t5 -mindepth 1 | sort
```

**Expected result:**

```text
run <RUN>: 0P/0F/2S/0E/0I/0T in 0.00s -> /tmp/eval-runs/t4/.dev/eval-runs/<YYYY-MM-DD>/<RUN>
exit=0
eval run: EvalNotFound: no specs match ['E99'] in suite='real'
exit=2
/tmp/eval-runs/t5/.dev
/tmp/eval-runs/t5/.dev/eval-runs
/tmp/eval-runs/t5/.dev/eval-runs/<YYYY-MM-DD>
/tmp/eval-runs/t5/.dev/eval-runs/<YYYY-MM-DD>/<RUN>
/tmp/eval-runs/t5/.dev/eval-runs/<YYYY-MM-DD>/<RUN>/homes
```

`--eval` can be repeated. Observed-as-coded: the unknown id exits 2 only after the run folder and `homes/` were created, and no summary is written; `--suite nope` behaves the same way. (source: `commands.py:1753-1811`; `eval run --help`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 12 — Without `--no-pty`: the null executor "passes" everything `[LOCAL-WRITE]`

**Do:**

```bash
cd /tmp/d15
superclaude eval run --suite real --no-mcp --output-dir /tmp/eval-runs/t6 --verbose; echo "exit=$?"
R=$(ls -d /tmp/eval-runs/t6/.dev/eval-runs/*/*/)
ls "$R"; ls "$R/per-eval" | wc -l; ls "$R/homes" | wc -l
```

**Expected result:**

```text
eval run: WARNING: _NullLifecycleExecutor active — non-production executor selected; run results MUST NOT be treated as authoritative.
run <RUN>: 17P/0F/0S/0E/0I/0T in <well under 1>s -> /tmp/eval-runs/t6/.dev/eval-runs/<YYYY-MM-DD>/<RUN>
exit=0
homes
per-eval
summary.json
summary.md
summary.yaml
17
0
```

All 17 evals report `PASS` within a fraction of a second, but no Claude process was started: the 5.0.0 executor's `spawn` and `inject` do nothing and `observe` returns exit 0 with empty output. `per-eval/<id>/artifacts/` folders are created and stay empty; per-eval HOMEs are removed on PASS. This is the plumbing check the WARNING refers to, not a real test result. (source: `commands.py:1357-1405,1906-1916`; `eval run --help` `--keep-home`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 13 — The coverage gate and the empty-HOME workaround `[LOCAL-WRITE]`

**Do:**

```bash
cd /tmp/d15
superclaude eval run --suite eval_smoke --no-pty --no-mcp --output-dir /tmp/eval-runs/t7 --verbose; echo "exit=$?"
ls -A /tmp/eval-runs/t7/.dev/eval-runs/*/*/
TMPHOME=$(mktemp -d /tmp/d15/home.XXXX)
HOME=$TMPHOME superclaude eval run --suite eval_smoke --no-pty --no-mcp --output-dir /tmp/eval-runs/t7/empty-home --verbose; echo "exit=$?"
ls -A "$TMPHOME" | wc -l; rm -rf "$TMPHOME"
```

**Expected result** when Step 7 printed a number of at least `1` (IronClaude hooks installed):

```text
eval doctor: coverage gate FAILED — uncovered matcher patterns:
  - PostToolUse: mcp__auggie__.*|mcp__auggie-mcp__.*|mcp__airis-mcp-gateway__auggie_.*
exit=2
coverage_missing:mcp__auggie__.__mcp__auggie-mcp__.__mcp__airis-mcp-gateway__auggie_._
homes
eval run: WARNING: _NullLifecycleExecutor active — non-production executor selected; run results MUST NOT be treated as authoritative.
run <RUN>: 0P/0F/3S/0E/0I/0T in 0.00s -> /tmp/eval-runs/t7/empty-home/.dev/eval-runs/<YYYY-MM-DD>/<RUN>
exit=0
0
```

Before any eval starts, `eval run` reads every auggie / AIRIS tool matcher in `~/.claude/settings.json` and requires an eval in the selected suite to cover it. `eval_smoke` covers none, so the run stops with exit 2 and an empty `coverage_missing:<pattern>` marker file in the run folder; `real` covers them (E2.1-E2.3), which is why Steps 8-12 passed the gate. With `HOME` pointing at an empty folder there is no `settings.json`, the matcher set is empty, the gate passes, and the run writes nothing into that HOME. Observed-as-coded: the message starts with `eval doctor:`.

When Step 7 printed `0` or `no matcher`: the first command already passes (`run <RUN>: 0P/0F/3S/0E/0I/0T ...`, exit 0) and the folder holds `homes` and the three `summary.*` files; the second command gives the same result. (source: gate `commands.py:1813-1829`; message `commands.py:642-647`; prefixes `coverage.py:99-103`; marker `coverage.py:84`; exit `coverage.py:78`; matcher `src/superclaude/hooks/hooks.json:100`; workaround `src/superclaude/skills/sc-cli-eval-protocol/SKILL.md:141-143`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 14 — Default output folder (no `--output-dir`) `[LOCAL-WRITE]`

**Do:**

```bash
cd /tmp/d15
superclaude eval run --suite real --no-pty --no-mcp --verbose 2>/dev/null; echo "exit=$?"
find /tmp/d15/.dev -maxdepth 3 | sort
```

**Expected result:**

```text
run <RUN>: 0P/0F/17S/0E/0I/0T in 0.00s -> /tmp/d15/.dev/eval-runs/<YYYY-MM-DD>/<RUN>
exit=0
/tmp/d15/.dev
/tmp/d15/.dev/eval-runs
/tmp/d15/.dev/eval-runs/<YYYY-MM-DD>
/tmp/d15/.dev/eval-runs/<YYYY-MM-DD>/<RUN>
```

Without `--output-dir` the run folder is `.dev/eval-runs/<date>/<run-id>/` under the current folder, wherever you are: run `eval run` from a scratch folder, not from a repo you care about. Observed-as-coded: `eval run --help` names `.dev/eval-runs/<run-id>/` without the date level. (source: `commands.py:1331-1339,1738-1748`; `config.py:65-70`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

### Tier C — Claude Code session

#### Step 15 — `/sc:cli-eval run` `[CLAUDE-SESSION]`

**Do:** in a shell, prepare a scratch project and start `claude` in it:

```bash
mkdir -p /tmp/d15/proj && cd /tmp/d15/proj && claude
```

Send this prompt. When it asks you to confirm the invocation, ask for `--no-pty --no-mcp --output-dir /tmp/eval-runs/t7/cli-eval --verbose`; if it offers the empty-HOME workaround, accept it:

```text
/sc:cli-eval run --suite eval_smoke
```

Then, in a shell:

```bash
ls -d /tmp/eval-runs/t7/cli-eval/.dev/eval-runs/*/*/
R=$(ls -d /tmp/eval-runs/t7/cli-eval/.dev/eval-runs/*/*/ | tail -1); ls -A "$R"
jq -c '.totals' "$R/summary.json" 2>/dev/null || echo "no summary"
ls -A /tmp/d15/proj
```

**Expected result:**

- The session loads the `sc:cli-eval-protocol` skill and first delegates a fresh read of the eval docs and CLI flags (the `eval-docs-loader` agent) before running anything.
- It runs `uv run superclaude eval list --json`, shows the suite (pre-selected by `--suite`), may show the `eval describe` details (three evals, all `no_pty: skip`), and asks you to confirm the exact command and flags. It warns that `--no-pty` turns these evals into `SKIPPED` and that the coverage gate can stop the run with exit 2.
- If your `settings.json` has the auggie matcher (Step 7), the first run exits 2 at the coverage gate and it offers the empty-HOME rerun (`TMPHOME=$(mktemp -d) HOME=$TMPHOME ...; rm -rf "$TMPHOME"`).
- Its report (from the `eval-run-reporter` agent) gives the run folder, the exit code, and 3 `SKIPPED` evals with reason `--no-pty`; it says the run was skipped, not passed, and labels the result NON-AUTHORITATIVE because of the null-executor WARNING.
- The shell check shows one run folder (two if the gate stopped the first run: the first holds only `coverage_missing:...` and `homes`), the last with `homes`, `summary.json`, `summary.md`, `summary.yaml` and totals `{"passed":0,"failed":0,"skipped":3,"errored":0,"interrupted":0,"timeout":0}`. `/tmp/d15/proj` stays empty (`uv run` outside a uv project creates nothing).
- The wording, menus and order are the model's choices and are not fixed; the files on disk are. (source: `src/superclaude/commands/cli-eval.md:12-52,67-73`; `src/superclaude/skills/sc-cli-eval-protocol/SKILL.md:46-58` fresh-context load, `:122-133` list and menu, `:135-146` confirm and gotchas, `:148-153` run, `:155-165` report and NON-AUTHORITATIVE label, `:205-208` error handling)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

---

## Edge cases (optional but recommended)

Run these from `/tmp/d15` after Step 14.

| Try this | Expected behavior | Source | Pass/Fail |
|---|---|---|---|
| `[FREE]` `superclaude eval run --suite real --timeout-mult 0 --output-dir /tmp/eval-runs/t7/x; echo "exit=$?"; ls -d /tmp/eval-runs/t7/x` | `eval run: --timeout-mult must be > 0; got 0.0`, `exit=2`, and no `x` folder (checked before any write) | `commands.py:1697-1702` | ☐ |
| `[FREE]` `superclaude eval run --suite real --max-disk-mb -1 --output-dir /tmp/eval-runs/t7/x; echo "exit=$?"` | `eval run: --max-disk-mb must be >= 0; got -1 (use 0 to disable the budget)` and `exit=2` | `commands.py:1704-1710` | ☐ |
| `[LOCAL-WRITE]` `superclaude eval run --suite real --no-pty --no-mcp --parallel 99 --output-dir /tmp/eval-runs/t7/p99 --json \| jq .parallel` | `15`; with `--parallel 0` (output dir `/tmp/eval-runs/t7/p0`) it is `1`. Out-of-range values are clamped, not refused | `commands.py:1692-1695`; `eval run --help` | ☐ |
| `[LOCAL-WRITE]` `superclaude eval run --suite nope --no-pty --output-dir /tmp/eval-runs/t7/n; echo "exit=$?"` | `eval run: SuiteNotFound: no manifest matched --suite 'nope' in <install path>/superclaude/cli/eval/suites`, `exit=2`; the run folder with an empty `homes/` is left behind (observed-as-coded) | `commands.py:1753,1785-1789` | ☐ |
| `[FREE]` `superclaude eval run --suite real --no-pty --output-dir /tmp/d15/out >/dev/null 2>&1; echo "exit=$?"; ls -d /tmp/d15/out` | `exit=2` and no `/tmp/d15/out` | `commands.py:1727-1751` | ☐ |
| `[LOCAL-WRITE]` `mkdir -p empty; superclaude eval list --suites-dir /tmp/d15/empty; echo "exit=$?"` | `superclaude eval list:`, then `(no suites found)` indented by two spaces, then `exit=0` (a missing folder gives the same) | `commands.py:740-747,941-971` | ☐ |
| `[LOCAL-WRITE]` `mkdir -p bad; printf 'name: Bad\nversion: "1.0"\nevals: []\n' > bad/bad.yaml; superclaude eval list --suites-dir /tmp/d15/bad; echo "exit=$?"` | `eval list: SchemaError: Manifest schema validation failed: /tmp/d15/bad/bad.yaml` followed by four `- $: '<field>' is a required property` lines (`defaults`, `description`, `optional_capabilities`, `required_binaries`), `exit=2` | `commands.py:958-966`; `src/superclaude/cli/eval/suites/suite.schema.json` | ☐ |
| `[FREE]` `superclaude eval doctor --output-dir /tmp/d15/bad/bad.yaml; echo "exit=$?"` | Click usage error ending `Error: Invalid value for '--output-dir': Directory '/tmp/d15/bad/bad.yaml' is a file.` and `exit=2` | `commands.py:787-797` (`file_okay=False`) | ☐ |
| `[LOCAL-WRITE]` `T=$(mktemp -d /tmp/d15/home.XXXX); HOME=$T superclaude eval doctor --no-mcp; echo "exit=$?"; rm -rf "$T"` | stderr `eval doctor: HARD failures` and `- filesystem.claude_home (~/.claude/ directory exists): <T>/.claude not found`; the checklist shows `[XX] ~/.claude/ directory exists (HARD)` and ends `HARD failures: filesystem.claude_home`; `exit=2`. The empty-HOME workaround is for `eval run`, not `doctor` | `commands.py:200,915-917` | ☐ |
| `[LOCAL-WRITE]` `superclaude eval doctor --no-mcp --check-coverage --suite eval_smoke >/dev/null; echo "exit=$?"` | With the auggie matcher in your `settings.json` (Step 7): stderr `eval doctor: coverage gate FAILED — uncovered matcher patterns:` plus the `PostToolUse` line, `exit=2`; without it, `exit=0`. With `--check-coverage --suite real`, `exit=0` | `commands.py:868-885,919-921` | ☐ |
| `[FREE]` Ctrl-C during `eval run` | Exit 3 (cooperative cancellation). UNVERIFIED by hand: with the 5.0.0 null executor a run ends in well under a second, so there is no time to press Ctrl-C | `commands.py:1932-1939,1989-1990`; `exit_codes.py:24` | ☐ |
| `[FREE]` `eval doctor` on macOS or another non-Linux host | stderr `eval doctor: unsupported platform: 'Darwin'. The cliEval harness ships Linux-only for v1 (AC1, roadmap R-109). ...` and exit 2. Code only, not rehearsed | `commands.py:601-606,843-849` | ☐ |
| `[CLAUDE-SESSION]` `/sc:cli-eval` with no argument | It stops and asks whether you want `create` or `run`; nothing is run | `src/superclaude/commands/cli-eval.md:14-17`; `SKILL.md:39,201` | ☐ |

## Cleanup

```bash
cd /tmp
rm -rf /tmp/d15 /tmp/eval-runs/t1 /tmp/eval-runs/t2 /tmp/eval-runs/t3 /tmp/eval-runs/t4 /tmp/eval-runs/t5 /tmp/eval-runs/t6 /tmp/eval-runs/t7
rmdir /tmp/eval-runs 2>/dev/null || true
```

`rmdir` removes `/tmp/eval-runs` only if it is now empty, so other people's runs stay. Tier A wrote nothing. What stays under your real `~/.claude` after Step 15 is the session in your Claude Code history and what the installed hooks write for any session: rows in `~/.claude/state/` and `~/.claude/logs/`.

## Overall result

☐ **PASS** — capability works as documented for `5.0.0`
☐ **FAIL** — see failing step(s) above

**Tester:** `<name>`  **Date:** `<date>`  **Build:** `5.0.0 (tag v5.0.0, commit d953b983)`
