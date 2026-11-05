# E2E Test Guide — `superclaude prd`, `superclaude cli-portify` and `superclaude cleanup-audit` (`5.0.0`)

- **Capability:** three document and audit pipelines that chain headless Claude sessions: `prd run` turns a one-line request into a Product Requirements Document (`prd resume` restarts it at a step); `cli-portify run` ports a skill folder into a programmatic CLI pipeline spec; `cleanup-audit run` runs a multi-pass repository cleanup audit. Each has a `--dry-run` that starts no Claude session.
- **Audience:** end user / operator
- **Source of truth:** `src/superclaude/cli/prd/commands.py:32-145,148-234`; `src/superclaude/cli/prd/config.py:22-33,91-159`; `src/superclaude/cli/prd/executor.py:185-213,468-483,511-624,718-730,900-1040,1041-1080,1305-1318`; `src/superclaude/cli/prd/models.py:38-63`; `src/superclaude/cli/prd/inventory.py:193-199`; `src/superclaude/cli/cli_portify/commands.py:30-227`; `src/superclaude/cli/cli_portify/config.py:24-35,78-175,268-306`; `src/superclaude/cli/cli_portify/models.py:595-610,718-746`; `src/superclaude/cli/cli_portify/executor.py:66-73,107-183,265-372,507-534,554-743,767-840`; `src/superclaude/cli/cli_portify/steps/__init__.py:43-55`; `src/superclaude/cli/cli_portify/steps/panel_review.py:276-299,352,375-391`; `src/superclaude/cli/cli_portify/resume.py:88-94,168-198`; `src/superclaude/cli/cli_portify/review.py:76-86`; `src/superclaude/cli/cli_portify/workdir.py:15-32,64-80`; `src/superclaude/cli/cleanup_audit/commands.py:24-120`; `src/superclaude/cli/cleanup_audit/config.py:33-48`; `src/superclaude/cli/cleanup_audit/models.py:80-84`; `src/superclaude/cli/cleanup_audit/executor.py:52-184,187-287`; `src/superclaude/cli/cleanup_audit/prompts.py:18-36`; `src/superclaude/cli/pipeline/process.py:134-166,178-183,185-218,286-304`; `docs/releases/v5.0.0.md:229` (Known Issue); `superclaude prd|cli-portify|cleanup-audit <cmd> --help`
- **Est. time:** `Tier A: 1 minute. Tier B: 5 minutes (no Claude call; one step waits 20 seconds). Tier C: 1-3 hours (a lightweight PRD run of about 20 Claude sessions, a cli-portify run of 2 sessions of up to 10 minutes each, the same again for the Ctrl-C check, and one cleanup-audit session).`

## Preconditions

- IronClaude 5.0.0 installed for your user: `superclaude --version` prints `SuperClaude, version 5.0.0`.
- A bash shell on Linux (Step 15 reads `/proc`). Run Tier B in one terminal, in the order given: later steps use files the earlier ones create.
- `/tmp/d13` does not exist (`[ ! -e /tmp/d13 ] && echo OK` prints `OK`). Every file Tier B and Tier C create is under `/tmp/d13`.
- None of `/tmp/src`, `/tmp/pyproject.toml`, `/src`, `/pyproject.toml` exists (`ls -d /tmp/src /tmp/pyproject.toml /src /pyproject.toml 2>/dev/null` prints nothing). `cli-portify` puts its work folder in the first folder above the skill that holds `src/` or `pyproject.toml`, else two levels above the skill (`workdir.py:64-80`); the steps expect `/tmp/d13/b/.dev/portify-workdir/hello`.
- A terminal at least 100 columns wide for the `cleanup-audit` plan table (Step 10); help text is wrapped at 80 columns.
- Tier B never calls Claude. It puts a stand-in `claude` script first on the `PATH` for single commands. All three pipelines start whatever `claude` the `PATH` finds first, send it the prompt on standard input and keep its standard output (`pipeline/process.py:140-166,185-218`), so each rule is checked on a fixed input.
- Tier C only: the `claude` CLI on your `PATH` and logged in; for `prd`, the installed PRD skill references in `~/.claude/skills/prd/refs` (`ls -d ~/.claude/skills/prd/refs` succeeds; `prd/models.py:38-63`). Every Tier C step starts real headless `claude --print` sessions and spends API tokens.
- Tier C sessions run with `--dangerously-skip-permissions` and `--tools default` (the pipeline default, `src/superclaude/cli/pipeline/models.py:285`; `pipeline/process.py:150-154`; the arguments are shown in Steps 5 and 7) in the folder you start them from: Claude can write files there without asking. Start them from the `/tmp/d13/c` folders given.
- Tier C sessions use your real `~/.claude`. They pass `--no-session-persistence`, so Claude Code saves no transcript (`pipeline/process.py:152`), but the hooks installed in `~/.claude/settings.json` still run and write `~/.claude/state/` and `~/.claude/logs/` at session start and on each prompt (`src/superclaude/hooks/hooks.json:18,49`; `src/superclaude/hooks/scripts/freshness-session-start.sh:8-9`; `freshness-user-prompt.sh:8-10`), and `auggie-flag-clear.sh` writes there after auggie tool calls (PostToolUse, `hooks.json:104`; `auggie-flag-clear.sh:10-12`). No step installs, registers or edits anything under `~/.claude`.

## What you're verifying

- `prd run --dry-run` prints the resolved request, tier, output folder and turn budget and starts no session. Without `--output`, the output folder is the current folder, **except** in a folder that has a `.dev/` folder: there it is `.dev/eval-workspaces`, which the dry run creates (the help says "default: current directory").
- A PRD step whose output fails its gate halts the run: stderr shows only `Pipeline finished with outcome: halt` and the exit code is 1; the reason is in the task folder's `execution-log.md`.
- `cli-portify run --dry-run` validates the target and prints the derived CLI name, then returns. **It runs no pipeline step** although its help says it executes the PREREQUISITES/ANALYSIS/USER_REVIEW/SPECIFICATION steps (follow-up O5). The help examples `sc:roadmap` and `~/.claude/skills/sc-roadmap` are not accepted: the target must be a skill folder path, and the installed `sc-roadmap-protocol` folder derives the reserved name `roadmap`.
- A real `cli-portify run` stops at the step `user-review-p1`, which has no step function, so it never reaches the specification, synthesis or panel-review steps. The command prints nothing and **exits 0 whatever the outcome**; the outcome is only in `return-contract.yaml`.
- `--max-convergence 3` has no effect (Known Issue, `docs/releases/v5.0.0.md:229`): the panel review always runs one iteration and one Claude session.
- Ctrl-C on `cli-portify run` does not stop the running Claude session: the command waits for it, records `outcome: INTERRUPTED` in `return-contract.yaml`, prints nothing and exits 0. The `EXIT_RECOMMENDATION: INTERRUPTED` line in the code is not reached during a run.
- `cleanup-audit run --dry-run` prints a 6-step plan; `--pass` does not change it. A real `cleanup-audit run` **crashes** with `AttributeError: 'CleanupAuditProcess' object has no attribute 'is_running'` right after it starts the first Claude session, exits 1, and leaves that session running.

Settings this guide does not exercise: `prd run --where/--spec/--model/--max-turns`, `prd resume` past its step-id check, `cli-portify --commands-dir/--skills-dir/--agents-dir/--include-agent/--save-manifest/--gate-mode soft|full`, `cleanup-audit --batch-size/--focus/--max-turns/--model`. All are listed by the `--help` of each command.

---

## Steps

### Tier A — free smoke (read-only)

#### Step 1 — Version, subcommands and the two help texts under test `[FREE]`

**Do:**

```bash
superclaude --version
superclaude prd --help | sed -n '/^Commands:/,$p'
superclaude cli-portify --help | sed -n '/^Commands:/,$p'
superclaude cleanup-audit --help | sed -n '/^Commands:/,$p'
superclaude cli-portify run --help | grep -A1 -- '--dry-run'
superclaude cli-portify run --help | grep -A4 -- '--max-convergence'
```

**Expected result:**

```text
SuperClaude, version 5.0.0
Commands:
  resume  Resume a previously interrupted PRD pipeline from a specific step.
  run     Execute the PRD generation pipeline.
Commands:
  run  Portify WORKFLOW into a programmatic CLI pipeline.
Commands:
  run  Execute the Cleanup Audit pipeline.
  --dry-run                       Execute only PREREQUISITES/ANALYSIS/USER_REV
                                  IEW/SPECIFICATION steps (SC-012)
  --max-convergence INTEGER       Maximum convergence iterations for panel-
                                  review (default: 1; follows the 2-fix-cycle
                                  cap). The value is stored in the run config,
                                  but nothing reads it yet: the review loop
                                  always runs 1 iteration.
```

(source: `pyproject.toml:7`; `prd/commands.py:102,193`; `cli_portify/commands.py:137`; `cleanup_audit/commands.py:72`; option help `cli_portify/commands.py:83-107`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 2 — The `cli-portify` help examples are rejected `[FREE]`

**Do:** (reads `~/.claude/skills` only; writes nothing)

```bash
cd /tmp
superclaude cli-portify run sc:roadmap --dry-run; echo "exit=$?"
superclaude cli-portify run ~/.claude/skills/sc-roadmap --dry-run; echo "exit=$?"
superclaude cli-portify run ~/.claude/skills/sc-roadmap-protocol --dry-run; echo "exit=$?"
```

**Expected result:** (`<home>` is your home folder)

```text
Error: Workflow path does not exist: /tmp/sc:roadmap
exit=1
Error: Workflow path does not exist: <home>/.claude/skills/sc-roadmap
exit=1
Error: CLI name 'roadmap' collides with existing module 'roadmap' — use --name to choose a different name
exit=1
```

The group help shows `superclaude cli-portify run sc:roadmap --dry-run` and the `run` help names `~/.claude/skills/sc-roadmap`, but the target is only ever resolved as a path from the current folder, and the installed skill folder is `sc-roadmap-protocol`, whose derived name `roadmap` is reserved. Use `--name` with that folder, or a skill folder of your own as Tier B does. (source: help examples `cli_portify/commands.py:21-25,139-140`; path resolved as given `config.py:78`; checks `config.py:143-145,166-173`; reserved names `config.py:24-35,280-287`; name derivation `models.py:718-746`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

### Tier B — local runs with a stand-in `claude` (no API call)

#### Step 3 — Create the stand-in `claude`, a sample skill and a sample project `[LOCAL-WRITE]`

**Do:**

```bash
[ ! -e /tmp/d13 ] || echo "STOP: remove /tmp/d13 first"
mkdir -p /tmp/d13/stub /tmp/d13/b/skills/sc-hello-protocol /tmp/d13/b/proj/src
cat > /tmp/d13/stub/claude <<'EOF'
#!/bin/sh
# Stand-in for the claude CLI: record the arguments, read the prompt from
# stdin, wait D13_STUB_SLEEP seconds (default 0), print one line, exit 0.
printf '%s\n' "$*" >> /tmp/d13/stub/calls.log
cat >/dev/null
sleep "${D13_STUB_SLEEP:-0}"
echo "stub output"
EOF
chmod +x /tmp/d13/stub/claude
cat > /tmp/d13/b/skills/sc-hello-protocol/SKILL.md <<'EOF'
---
name: sc-hello-protocol
description: Print a greeting for a given name.
---

# Hello protocol

1. Read the name the user gave (default `world`).
2. Print `Hello, <name>`.
EOF
printf 'def hello():\n    return "hi"\n' > /tmp/d13/b/proj/src/app.py
printf 'print("old")\n' > /tmp/d13/b/proj/src/old_unused.py
printf '# Proj\n' > /tmp/d13/b/proj/README.md
PATH="/tmp/d13/stub:$PATH" command -v claude
```

**Expected result:** no `STOP` line, then `/tmp/d13/stub/claude`. Every later command that sets `PATH="/tmp/d13/stub:$PATH"` reaches this script, not the real `claude`: the pipelines run the bare name `claude` and pass your environment through (`pipeline/process.py:140-141,178-183,218`). Each call adds one line to `/tmp/d13/stub/calls.log`.

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 4 — `prd run --dry-run`, its default output folder and its usage errors `[LOCAL-WRITE]`

**Do:**

```bash
cd /tmp/d13/b
superclaude prd run "MVP spec" --dry-run; echo "exit=$?"
[ -e .dev ] || echo "no .dev created"
mkdir -p dev-repo/.dev && cd dev-repo
superclaude prd run "MVP spec" --dry-run --tier lightweight; echo "exit=$?"
find .dev | sort
cd /tmp/d13/b
superclaude prd run "MVP spec" --tier huge --dry-run; echo "exit=$?"
superclaude prd resume bogus; echo "exit=$?"
```

**Expected result:**

```text
Dry run: config validated successfully.
  Request: MVP spec
  Tier:    standard
  Output:  /tmp/d13/b
  Turns:   300
exit=0
no .dev created
Dry run: config validated successfully.
  Request: MVP spec
  Tier:    lightweight
  Output:  /tmp/d13/b/dev-repo/.dev/eval-workspaces
  Turns:   300
exit=0
.dev
.dev/eval-workspaces
Usage: superclaude prd run [OPTIONS] REQUEST
Try 'superclaude prd run --help' for help.

Error: Invalid value for '--tier': 'huge' is not one of 'lightweight', 'standard', 'heavyweight'.
exit=2
Error: Unrecognised resume step ID: 'bogus'. Expected a known step pattern like 'parse-request', 'investigation-3', 'qa-synthesis-gate', etc.
exit=1
```

In a folder with a `.dev/` folder the default output moves to `.dev/eval-workspaces`, and the dry run creates it, although the `--output` help says "default: current directory". Record this as observed-as-coded. The task folder (`prd-task`, or `prd-<product slug>` with `--product`) is not printed and not created by a dry run. (source: dry-run lines `prd/commands.py:132-138`; output default `prd/config.py:110-124`; task folder `prd/config.py:126-132`; `--tier` choice `prd/commands.py:63-68`; step-id check `prd/config.py:26-33,99-107`, `prd/commands.py:225-227`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 5 — A PRD step that fails its gate halts the run, exit 1 `[LOCAL-WRITE]`

**Do:** (the stand-in answers with the one line `stub output`; on a terminal a live progress table may flash on stderr, it is not checked)

```bash
cd /tmp/d13/b
PATH="/tmp/d13/stub:$PATH" superclaude prd run "Hello CLI that prints a greeting" --tier lightweight --output /tmp/d13/b/prd-out; echo "exit=$?"
ls /tmp/d13/b/prd-out/prd-task
sed -n '/^| Step/,$p' /tmp/d13/b/prd-out/prd-task/execution-log.md
tail -1 /tmp/d13/stub/calls.log
```

**Expected result:**

```text
Pipeline finished with outcome: halt
exit=1
execution-log.jsonl
execution-log.md
parse-request-error.txt
parse-request-output.txt
parsed-request.json
qa
research
results
reviews
synthesis
| Step | Status | Duration | Details |
|------|--------|----------|---------|
| check-existing | RUNNING | - | Started: Check Existing Work |
| check-existing | PASS | 0.0s | exit=0 |
| parse-request | RUNNING | - | Started: Parse Request |
| parse-request | GATE FAIL | - | Missing required fields: GOAL, PRODUCT_SLUG, PRD_SCOPE, SCENARIO |
| parse-request | HALT | 0.0s | exit=0 |
--print --verbose --dangerously-skip-permissions --no-session-persistence --tools default --max-turns 300 --output-format stream-json
```

`check-existing` runs in Python; `parse-request` is the first Claude session. Its answer lacks the four required fields, its gate is STRICT, so the run halts after one session. The terminal shows only the outcome; the reason is in `execution-log.md`. The last line is the argument list the pipeline passed to `claude`. (source: steps `prd/executor.py:468-483,645-651`; halt on a STRICT gate failure `prd/executor.py:583-598`; task subfolders `prd/inventory.py:193-199`; step files `prd/executor.py:718-720`; outcome line and exit `prd/commands.py:143-145`; command `pipeline/process.py:140-166`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 6 — `cli-portify run --dry-run` runs no pipeline step (O5) `[LOCAL-WRITE]`

**Do:**

```bash
cd /tmp/d13/b
PATH="/tmp/d13/stub:$PATH" superclaude cli-portify run skills/sc-hello-protocol --dry-run; echo "exit=$?"
PATH="/tmp/d13/stub:$PATH" superclaude cli-portify run skills/sc-hello-protocol --dry-run --max-convergence 3; echo "exit=$?"
[ -e .dev ] || echo "no .dev: no pipeline step ran"
wc -l < /tmp/d13/stub/calls.log
superclaude cli-portify run skills/sc-hello-protocol --dry-run --output /tmp/d13/b/gen; echo "exit=$?"
[ -d gen ] && echo "gen created, entries: $(ls -A gen | wc -l)"
```

**Expected result:**

```text
cli-portify dry-run: skills/sc-hello-protocol
Derived CLI name: hello
exit=0
cli-portify dry-run: skills/sc-hello-protocol
Derived CLI name: hello
exit=0
no .dev: no pipeline step ran
1
cli-portify dry-run: skills/sc-hello-protocol
Derived CLI name: hello
exit=0
gen created, entries: 0
```

The help says `--dry-run` executes the PREREQUISITES/ANALYSIS/USER_REVIEW/SPECIFICATION steps, but the command prints two lines and returns before `run_portify`: no work folder, no `return-contract.yaml`, no Claude call (the call count is still the 1 call of Step 5). That is follow-up O5. The dry run still creates the `--output` folder, because the config check creates a missing output folder. The `sc-` prefix and `-protocol` suffix are stripped to derive `hello`. (source: `cli_portify/commands.py:83-88,196-204`; dry-run filter never reached `executor.py:66-73,540-544`; output folder `config.py:153-164`; derivation `models.py:718-746`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 7 — A `cli-portify` run stops at `user-review-p1` and exits 0 `[LOCAL-WRITE]`

**Do:**

```bash
cd /tmp/d13/b
PATH="/tmp/d13/stub:$PATH" superclaude cli-portify run skills/sc-hello-protocol --max-convergence 3; echo "exit=$?"
W=/tmp/d13/b/.dev/portify-workdir/hello
ls $W; ls $W/results
grep -E '^(outcome|status|resume_command):' $W/return-contract.yaml
sed -n '/^gate_results:/,/^outcome:/p' $W/return-contract.yaml
grep -c max_convergence $W/portify-config.yaml
wc -l < /tmp/d13/stub/calls.log
```

**Expected result:** (on a terminal a live progress display may appear; nothing else is printed)

```text
exit=0
diagnostics.md
execution-log.jsonl
execution-log.md
portify-config.yaml
results
return-contract.yaml
validate-config-result.json
analyze-workflow-error.log
component-inventory.md
portify-analysis.md
outcome: FAILURE
resume_command: superclaude cli-portify run --resume step-graph-design
status: failed
gate_results:
  analysis-synthesis: fail
  discover-components: pass
  protocol-mapping: fail
  user-review-p1: error
  validate-config: pass
outcome: FAILURE
0
3
```

`validate-config` and `discover-components` run in Python; `protocol-mapping` and `analysis-synthesis` each start one Claude session (calls 2 and 3); `user-review-p1` has no step function, so it returns an error and the run ends with `outcome: FAILURE`. `user-review-p2`, the specification steps, `release-spec-synthesis` and `panel-review` are never reached in any run without `--resume`. The command discards the outcome and **exits 0**. `--max-convergence` is not even written to `portify-config.yaml`. Note also that the printed `resume_command` has no TARGET and fails as written (edge case table). Record these as observed-as-coded. (source: work folder `workdir.py:15-32,64-80`; steps `executor.py:107-183`; missing step function `steps/__init__.py:43-55`, `executor.py:578-581`; loop and outcomes `executor.py:656-743`; contract `executor.py:265-267,283-372`; outcome ignored `cli_portify/commands.py:204`; config file `workdir.py:35-61`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 8 — `--max-convergence 3` still gives one panel-review session `[LOCAL-WRITE]`

**Do:** (same terminal as Step 7, which set `W`; panel review is reachable only with `--resume`; seed its two inputs in both places the code looks, and answer its prompt with end-of-input)

```bash
cd /tmp/d13/b
printf '# Synthesized spec\n' > $W/synthesized-spec.md; printf '# Gaps\n' > $W/brainstorm-gaps.md
cp $W/synthesized-spec.md $W/brainstorm-gaps.md $W/results/
PATH="/tmp/d13/stub:$PATH" superclaude cli-portify run skills/sc-hello-protocol --resume panel-review --max-convergence 3 < /dev/null; rc=$?; echo; echo "exit=$rc"
wc -l < /tmp/d13/stub/calls.log
sed -n 2,3p $W/results/panel-report.md
grep -E '^(outcome|status):|panel-review:' $W/return-contract.yaml
```

**Expected result:**

```text

[Review] Step 'panel-review' produced artifact: /tmp/d13/b/.dev/portify-workdir/hello/results/panel-reviewed-spec.md
Accept and continue? [y/N]
exit=0
4
terminal_state: converged
iteration_count: 1
  panel-review: fail
outcome: SUCCESS
status: success
```

Exactly one Claude session ran for the panel review (calls 3 → 4) and the report shows `iteration_count: 1` although `--max-convergence 3` was given: the step builds its convergence engine with a fixed `max_iterations=1`. This is the Known Issue in `docs/releases/v5.0.0.md:229`. End-of-input at the `[y/N]` prompt counts as a rejection, so the step is `fail`, yet the run outcome is `SUCCESS` and the exit is 0: a failed (not errored) step does not stop the run. The resume check reads the two inputs from the work folder while the step reads them from `results/`, which is why the step seeds both. (source: `steps/panel_review.py:276-299,352,375-391`; prompt `review.py:76-86`; resume check `resume.py:88-94,168-198`; outcome rules `executor.py:693-704`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 9 — Ctrl-C waits for the running session, records INTERRUPTED and exits 0 `[LOCAL-WRITE]`

**Do:** (the stand-in now takes 20 seconds per call; press **Ctrl-C** about 3 seconds after you start the command)

```bash
cd /tmp/d13/b && rm -rf /tmp/d13/b/.dev
date +%T; D13_STUB_SLEEP=20 PATH="/tmp/d13/stub:$PATH" superclaude cli-portify run skills/sc-hello-protocol; echo "exit=$?"; date +%T
grep -E '^(outcome|status):' /tmp/d13/b/.dev/portify-workdir/hello/return-contract.yaml
sed -n '/^gate_results:/,/^outcome:/p' /tmp/d13/b/.dev/portify-workdir/hello/return-contract.yaml
```

**Expected result:** after `^C` the command keeps running until the stand-in's 20 seconds are over; then `exit=0`, the second time is about 20 seconds after the first, and **no `EXIT_RECOMMENDATION: INTERRUPTED` line** appears. Then:

```text
outcome: INTERRUPTED
status: partial
gate_results:
  discover-components: pass
  protocol-mapping: fail
  validate-config: pass
outcome: INTERRUPTED
```

The executor replaces the Ctrl-C handler for the whole run with one that only sets a flag; the flag is checked after the current step ends. The Claude session runs in its own process group, so Ctrl-C does not reach it. `analysis-synthesis` never starts. The `except KeyboardInterrupt` branch that prints `EXIT_RECOMMENDATION: INTERRUPTED` and exits 0 is reached only by an interrupt outside the executor's run (the milliseconds of config loading), so the planned "exits 0 with `EXIT_RECOMMENDATION: INTERRUPTED`" is half right: exit 0, no line. (source: handler `executor.py:507-534`; checks `executor.py:666-669,706-709`; contract `executor.py:335-343`; process group `pipeline/process.py:212-213`; branch `cli_portify/commands.py:218-220`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 10 — `cleanup-audit run --dry-run` prints the plan; `--pass` does not change it `[LOCAL-WRITE]`

**Do:**

```bash
cd /tmp/d13/b/proj
superclaude cleanup-audit run . --dry-run --pass surface; echo "exit=$?"
superclaude cleanup-audit run . --dry-run --output /tmp/d13/b/ca-dry > /dev/null; echo "exit=$?"
[ -d /tmp/d13/b/ca-dry ] && echo "ca-dry created, entries: $(ls -A /tmp/d13/b/ca-dry | wc -l)"
```

**Expected result:** (colours not shown)

```text
                                    Cleanup Audit Pipeline Plan
┏━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┓
┃ Step  ┃ Pass Type     ┃ Output                        ┃ Gate Tier ┃ Timeout ┃ Agent              ┃
┡━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━┩
│ G-001 │ surface       │ surface-scan-result.md        │ LIGHT     │ 600s    │ audit-scanner      │
│ G-002 │ structural    │ structural-analysis-result.md │ STANDARD  │ 900s    │ audit-analyzer     │
│ G-003 │ structural    │ per-file-profiles-result.md   │ STANDARD  │ 900s    │ audit-analyzer     │
│ G-004 │ cross_cutting │ cross-cutting-result.md       │ STRICT    │ 900s    │ audit-comparator   │
│ G-005 │ consolidation │ consolidation-result.md       │ STRICT    │ 600s    │ audit-consolidator │
│ G-006 │ validation    │ validation-result.md          │ STANDARD  │ 600s    │ audit-validator    │
└───────┴───────────────┴───────────────────────────────┴───────────┴─────────┴────────────────────┘
exit=0
exit=0
ca-dry created, entries: 0
```

`--pass surface` still lists all six steps: the step list ignores `--pass`, and `--batch-size` and `--focus` are only written to the log header. The output file names are relative to the output folder, which defaults to the audited folder itself. Like `cli-portify`, the dry run creates a missing `--output` folder. (source: `cleanup_audit/commands.py:85-87,93-120`; steps `cleanup_audit/executor.py:187-287`; options used only in `cleanup_audit/logging_.py:39-53`; output default `cleanup_audit/config.py:48`; folder created `cleanup_audit/models.py:80-84`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 11 — A `cleanup-audit` run crashes after starting its first session `[LOCAL-WRITE]`

**Do:** (the stand-in takes 5 seconds; `--output` keeps the results out of the sample project)

```bash
cd /tmp/d13/b/proj
D13_STUB_SLEEP=5 PATH="/tmp/d13/stub:$PATH" superclaude cleanup-audit run . --output /tmp/d13/b/ca-run > /tmp/d13/b/ca.out 2> /tmp/d13/b/ca.err; echo "exit=$?"
tail -1 /tmp/d13/b/ca.err
ls /tmp/d13/b/ca-run
cat /tmp/d13/b/ca-run/G-001-output.jsonl; echo "(end of first read)"
sleep 7; cat /tmp/d13/b/ca-run/G-001-output.jsonl
```

**Expected result:**

```text
exit=1
AttributeError: 'CleanupAuditProcess' object has no attribute 'is_running'
G-001-error.log
G-001-output.jsonl
execution-log.jsonl
execution-log.md
(end of first read)
stub output
```

The command exits 1 within a second with a Python traceback. The supervision loop calls `process.is_running()`, but the shared pipeline process class has no such method (nor the `stop()` and `started_at` the loop also uses), so **every non-dry `cleanup-audit run` crashes** right after it starts G-001. The `claude` it started keeps running: its output file is empty at the first read and holds `stub output` 5 seconds later, written after the command had exited. `ca.out` holds the runner's panel and is not checked. Record this as a failure of the coded path (new code observation). (source: `cleanup_audit/executor.py:82-89,118,126`; methods of the base class `pipeline/process.py:85-373` define `start`, `wait`, `terminate` only; step files `cleanup_audit/process.py:29-42`; exit code `cleanup_audit/commands.py:89-90` is never reached)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

### Tier C — real runs (`[API-LONG]`, Claude API)

#### Step 12 — One lightweight PRD run `[API-LONG]`

**Do:** (the run prints nothing until it ends, apart from a live table on a terminal)

```bash
mkdir -p /tmp/d13/c && cd /tmp/d13/c
superclaude prd run "A command-line tool that prints a greeting for a given name" --product "Hello CLI" --tier lightweight --output /tmp/d13/c/prd; echo "exit=$?"
ls /tmp/d13/c/prd/prd-hello-cli
sed -n '/^| Step/,$p' /tmp/d13/c/prd/prd-hello-cli/execution-log.md | tail -4
find /tmp/d13/c/prd -name '*.md' -newer /tmp/d13/c/prd/prd-hello-cli/parsed-request.json | sort
```

**Expected result:**

- `exit=0` and no `Pipeline finished with outcome:` line: the outcome was `success`. If that line shows `halt` and `exit=1`, mark FAIL and note the last `HALT` or `GATE FAIL` row of `execution-log.md`.
- `ls` shows the task folder of the product slug `hello-cli` with `research`, `synthesis`, `qa`, `reviews`, `results`, `parsed-request.json`, `execution-log.md`, `execution-log.jsonl` and one `<step>-output.txt` / `<step>-error.txt` pair per Claude step.
- Each step logs a `RUNNING` row and a result row; the last rows are those of `present-complete`, which runs after `assembly`, `structural-qa` and `qualitative-qa`. Lightweight runs 3 investigation sessions and 1 web-research session where standard runs 5 and 2.
- The assembled PRD is written by the `assembly` session to the `--output` path; its file name is chosen by the model (UNVERIFIED), so look for it in the `find` list.

(source: steps `prd/executor.py:468-483,900-1040`; lightweight counts `prd/executor.py:1041-1080`; task folder `prd/config.py:126-132`, `prd/inventory.py:193-199`; assembly output path `prd/prompts.py:1391`; outcome `prd/executor.py:615-618`, `prd/commands.py:140-145`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 13 — One real `cli-portify` run with `--max-convergence 3` `[API-LONG]`

**Do:**

```bash
mkdir -p /tmp/d13/c && cp -r /tmp/d13/b/skills /tmp/d13/c/ && cd /tmp/d13/c
superclaude cli-portify run skills/sc-hello-protocol --max-convergence 3; echo "exit=$?"
W=/tmp/d13/c/.dev/portify-workdir/hello
grep -E '^(outcome|status):' $W/return-contract.yaml
sed -n '/^gate_results:/,/^outcome:/p' $W/return-contract.yaml
ls $W/results
```

**Expected result:** after two Claude sessions (`protocol-mapping` and `analysis-synthesis`, up to 600 seconds each) `exit=0` with nothing printed; then `outcome: FAILURE`, `status: failed`; `gate_results` has `user-review-p1: error`, `validate-config: pass`, `discover-components: pass` and a `pass` or `fail` for the two analysis steps (the model's answer decides). `results` holds `component-inventory.md` and `portify-analysis.md`; there is no `portify-spec.md`, `synthesized-spec.md` or `panel-report.md`, so the panel review, the only reader of `--max-convergence`, never ran. If `protocol-mapping: error` appears instead, the Claude session itself failed: still `exit=0`. (source: as Step 7; step timeouts `executor.py:120-131`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 14 — Ctrl-C on a real `cli-portify` run `[API-LONG]`

**Do:** (press **Ctrl-C** about 10 seconds after you start the command)

```bash
cd /tmp/d13/c && rm -rf /tmp/d13/c/.dev
date +%T; superclaude cli-portify run skills/sc-hello-protocol; echo "exit=$?"; date +%T
grep -E '^outcome:' /tmp/d13/c/.dev/portify-workdir/hello/return-contract.yaml
```

**Expected result:** the command does not stop at `^C`; it returns when the running `protocol-mapping` session ends (up to 600 seconds), prints no `EXIT_RECOMMENDATION` line, and shows `exit=0` and `outcome: INTERRUPTED`. `analysis-synthesis` does not start. (source: as Step 9)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 15 — One real `cleanup-audit` run `[API-LONG]`

**Do:** (starts one real Claude session in `/tmp/d13/c/proj` that outlives the command; the last line stops it)

```bash
mkdir -p /tmp/d13/c && cp -r /tmp/d13/b/proj /tmp/d13/c/ && cd /tmp/d13/c/proj
superclaude cleanup-audit run . --output /tmp/d13/c/ca-run > /tmp/d13/c/ca.out 2> /tmp/d13/c/ca.err; echo "exit=$?"
tail -1 /tmp/d13/c/ca.err
for p in $(pgrep -f 'claude --print'); do [ "$(readlink /proc/$p/cwd)" = /tmp/d13/c/proj ] && ps -o pid=,etime=,args= -p "$p"; done
# then stop that session: kill <pid from the line above>
```

**Expected result:** within a few seconds `exit=1` and `AttributeError: 'CleanupAuditProcess' object has no attribute 'is_running'`, as in Step 11. The loop prints one line for a `claude --print ... --output-format stream-json` process still running in `/tmp/d13/c/proj`, started by the crashed command; it keeps writing `/tmp/d13/c/ca-run/G-001-output.jsonl` until it ends or you `kill` it. Its prompt is a `/sc:task` surface-scan request with an empty file list and no target path, so what it scans is the folder it runs in. A completed audit cannot be observed in 5.0.0. (source: `cleanup_audit/executor.py:82-89`; prompt `cleanup_audit/prompts.py:18-36` with `[]` from `cleanup_audit/executor.py:195`; child cwd is the caller's `pipeline/process.py:206-216`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

---

## Edge cases (optional but recommended)

Run these in the Tier B terminal, from `/tmp/d13/b`, after Step 11.

| Try this | Expected behavior | Source | Pass/Fail |
|---|---|---|---|
| `[LOCAL-WRITE]` `mkdir -p skills/sc-roadmap-protocol && cp skills/sc-hello-protocol/SKILL.md skills/sc-roadmap-protocol/ && superclaude cli-portify run skills/sc-roadmap-protocol --dry-run --name rm-port; echo "exit=$?"` | `cli-portify dry-run: skills/sc-roadmap-protocol`, `Derived CLI name: rm-port`, `exit=0`: `--name` avoids the reserved-name error of Step 2 | `cli_portify/commands.py:32-38`; `models.py:595-603` | ☐ |
| `[FREE]` `superclaude cli-portify run skills/sc-hello-protocol/SKILL.md --dry-run; echo "exit=$?"` | `Derived CLI name: skill-md`, `exit=0`: a `SKILL.md` path is accepted, but the name is derived from the file name, not the folder | `models.py:605-610,718-746` | ☐ |
| `[LOCAL-WRITE]` `mkdir -p skills/empty && superclaude cli-portify run skills/empty --dry-run; echo "exit=$?"` | `Error: SKILL.md not found at /tmp/d13/b/skills/empty`, `exit=1` | `config.py:148-150`; `cli_portify/commands.py:190-194` | ☐ |
| `[FREE]` `superclaude cli-portify run skills/sc-hello-protocol --dry-run --gate-mode strict; echo "exit=$?"` | `Error: Invalid value for '--gate-mode': 'strict' is not one of 'shadow', 'soft', 'full'.`, `exit=2` | `cli_portify/commands.py:114-119` | ☐ |
| `[FREE]` `superclaude cli-portify run --resume step-graph-design; echo "exit=$?"` (the `resume_command` of Step 7, as written) | `Error: Missing argument 'TARGET'.`, `exit=2` | `executor.py:265-267`; `cli_portify/commands.py:31` | ☐ |
| `[FREE]` `superclaude cleanup-audit run /tmp/d13/b/nope --dry-run 2>&1 \| tail -1; echo "exit=${PIPESTATUS[0]}"` | A traceback ending `FileNotFoundError: Target path does not exist: /tmp/d13/b/nope`, `exit=1` (no one-line error) | `cleanup_audit/config.py:33-35`; `cleanup_audit/commands.py:73` | ☐ |
| `[FREE]` `superclaude cleanup-audit run proj --dry-run --pass bogus; echo "exit=$?"` | `Error: Invalid value for '--pass': 'bogus' is not one of 'surface', 'structural', 'cross-cutting', 'all'.`, `exit=2` | `cleanup_audit/commands.py:26-31` | ☐ |

## Cleanup

```bash
for p in $(pgrep -f 'claude --print'); do [ "$(readlink /proc/$p/cwd)" = /tmp/d13/c/proj ] && kill "$p"; done
cd /tmp && rm -rf /tmp/d13
```

The first line stops a Step 15 session that is still running. The stand-in `claude` lived only in `/tmp/d13/stub` and was on the `PATH` only for the commands that set it. Tier A and B write nothing outside `/tmp/d13`. What stays under your real `~/.claude` after Tier C is what the installed hooks write for any Claude Code session: rows in `~/.claude/state/` and `~/.claude/logs/`; the pipeline sessions saved no transcript (`--no-session-persistence`, `src/superclaude/cli/pipeline/process.py:152`).

## Overall result

☐ **PASS** — capability works as documented for `5.0.0`
☐ **FAIL** — see failing step(s) above

**Tester:** `<name>`  **Date:** `<date>`  **Build:** `5.0.0 (tag v5.0.0, commit d953b983)`
