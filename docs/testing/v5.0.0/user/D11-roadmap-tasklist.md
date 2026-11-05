# E2E Test Guide — `superclaude roadmap` (run, validate, accept-spec-change) and `superclaude tasklist validate` (`5.0.0`)

- **Capability:** `superclaude roadmap run` turns a spec (plus an optional TDD and PRD) into a roadmap through a chain of headless Claude sessions with a file gate after each step, and validates the result unless `--no-validate`; `--dry-run` prints the step plan; `roadmap validate` reviews a finished run and always exits 0; `roadmap accept-spec-change` records an accepted spec edit; `superclaude tasklist validate` checks a tasklist against its roadmap and exits 1 when the report counts HIGH-severity deviations.
- **Audience:** end user / operator
- **Source of truth:** `src/superclaude/cli/roadmap/commands.py:14-29,32-35,289-401,404-427,430-513`; `src/superclaude/cli/roadmap/executor.py:211-332,2500-2520,2645-2652,2804-2897,3104-3159,3220-3240,3642-3862,4068-4131`; `src/superclaude/cli/roadmap/validate_executor.py:42,188-241,348-525`; `src/superclaude/cli/roadmap/validate_gates.py:31-69`; `src/superclaude/cli/roadmap/spec_patch.py:162-206`; `src/superclaude/cli/roadmap/prompts.py:36-52`; `src/superclaude/cli/tasklist/commands.py:31-185`; `src/superclaude/cli/tasklist/executor.py:40-52,159-244`; `src/superclaude/cli/tasklist/gates.py:23-46`; `src/superclaude/cli/tasklist/prompts.py:49-100`; `src/superclaude/cli/pipeline/executor.py:209-216,366-388`; `src/superclaude/cli/pipeline/process.py:134-166,168-182,218`; `superclaude roadmap <cmd> --help`; `superclaude tasklist validate --help`
- **Est. time:** `Tier A: 1 minute. Tier B: 5 minutes (no Claude call). Tier C: 30-90 minutes (one quick-depth roadmap run of about 15 Claude sessions, then two validations).`

## Preconditions

- IronClaude 5.0.0 installed for your user: `superclaude --version` prints `SuperClaude, version 5.0.0`.
- `jq` on your `PATH`.
- `/tmp/d11` does not exist (`[ ! -e /tmp/d11 ] && echo OK` prints `OK`). Every file this guide creates is under `/tmp/d11`.
- A bash shell. Run Tier B in one terminal, in the order given: later steps use files the earlier ones create. Tier C needs the spec from Step 2.
- Tier B never calls Claude. It puts a stand-in `claude` script first on the `PATH` for single commands, and the pipeline starts whatever `claude` the `PATH` finds first, sends it the prompt on standard input and saves its standard output as the step's output file (`process.py:134-166,218`). The stand-in prints a report you prepare, so each exit-code rule is checked on a fixed input.
- Tier C only: the `claude` CLI on your `PATH` and logged in. Every Tier C step starts real headless `claude --print` sessions and spends API tokens; the roadmap run uses the default agents `opus:architect,sonnet:architect` (`executor.py:3681-3685`).
- Tier C sessions run with `--dangerously-skip-permissions` and `--tools default`, the pipeline defaults (`src/superclaude/cli/pipeline/models.py:285`; `process.py:150-154`), in the folder you start them from: Claude can write files without asking. Start them from `/tmp/d11/c`.
- Tier C sessions use your real `~/.claude`. They pass `--no-session-persistence`, so Claude Code saves no transcript (`process.py:152`), but the hooks installed in `~/.claude/settings.json` still run and write `~/.claude/state/` and `~/.claude/logs/` at session start and on each prompt (`src/superclaude/hooks/hooks.json:18,49`; `src/superclaude/hooks/scripts/freshness-session-start.sh:8-9`; `freshness-user-prompt.sh:8-10`; `auggie-flag-clear.sh:10-12`). No step installs, registers or edits anything under `~/.claude`.

## What you're verifying

- `roadmap run --dry-run` prints the 12-step plan and starts no Claude session, but it **creates the output directory first** (follow-up O17). The group help still says "an 8-step pipeline"; the plan lists 12 steps and a halt report lists 14 step ids (`commands.py:18`; `executor.py:2876-2897`).
- `roadmap run` accepts 1-3 input files; 4 or more stop with a usage error, exit 2, before anything is written.
- A step whose output fails its gate is retried once; when the retry fails too, the run prints a halt report on stderr and exits 1, keeping `.roadmap-state.json` with the failed step.
- `roadmap validate` exits 0 even when the review finds blocking issues: this is the coded design (comment "exit 0 per NFR-006"). It also exits 0, reporting `0 blocking`, when the review session itself fails.
- `tasklist validate` exits 1 with `FAIL: HIGH-severity deviations found` when the report's `high_severity_count` is above 0, and exits 0 with `PASS: No HIGH-severity deviations` when it is 0.
- A real `roadmap run --depth quick` produces the roadmap files and an auto-validation, and a real `tasklist validate` on a tasklist that does not match the roadmap exits 1.

Settings this guide does not exercise: `--resume` (skips steps whose output already passes its gate, `commands.py:57-64`; `executor.py:3744-3748`), `--no-convergence`, `--retrospective`, `--allow-regeneration`, the `--tool-write-*` flags and the cosmetic-remediation switches. All are listed by `superclaude roadmap run --help`.

---

## Steps

### Tier A — free smoke (read-only)

#### Step 1 — Version and subcommands `[FREE]`

**Do:**

```bash
superclaude --version
superclaude roadmap --help | sed -n '/^Commands:/,$p'
superclaude tasklist --help | sed -n '/^Commands:/,$p'
superclaude roadmap run --help | grep -A1 -- '--depth'
```

**Expected result:**

```text
SuperClaude, version 5.0.0
Commands:
  accept-spec-change  Update spec_hash after accepted deviation records.
  run                 Run the roadmap generation pipeline on INPUT_FILES.
  validate            Validate roadmap pipeline outputs in OUTPUT_DIR.
Commands:
  validate  Validate tasklist fidelity against a roadmap.
  --depth [quick|standard|deep]   Debate round depth: quick=1, standard=2,
                                  deep=3. Default: standard.
```

(source: `pyproject.toml:7`; commands `roadmap/commands.py:32,404,430`; `tasklist/commands.py:31`; `--depth` option `roadmap/commands.py:51-56`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

### Tier B — local runs with a stand-in `claude` (no API call)

#### Step 2 — Create the spec and the stand-in `claude` `[LOCAL-WRITE]`

**Do:**

```bash
[ ! -e /tmp/d11 ] || echo "STOP: remove /tmp/d11 first"
mkdir -p /tmp/d11/b /tmp/d11/stub && cd /tmp/d11/b
cat > spec.md <<'EOF'
# Release spec: hello CLI

## 1. Problem

Users need a small command that prints a greeting.

## 2. Functional requirements

- FR-001: `hello` prints `Hello, world` and exits 0.
- FR-002: `hello --name NAME` prints `Hello, NAME` and exits 0.

## 3. Non-functional requirements

- NFR-001: `hello` starts and finishes in under one second.
EOF
cat > /tmp/d11/stub/claude <<'EOF'
#!/bin/sh
# Stand-in for the claude CLI: read the prompt from stdin, then print the
# file named by D11_STUB_REPORT (or one short line), and exit with D11_STUB_EXIT.
cat >/dev/null
if [ -n "${D11_STUB_REPORT:-}" ]; then cat "$D11_STUB_REPORT"; else echo "stub output"; fi
exit "${D11_STUB_EXIT:-0}"
EOF
chmod +x /tmp/d11/stub/claude
PATH="/tmp/d11/stub:$PATH" command -v claude
```

**Expected result:** no `STOP` line, then `/tmp/d11/stub/claude`. Every later command that sets `PATH="/tmp/d11/stub:$PATH"` reaches this script, not the real `claude`: the pipeline runs the bare name `claude` and passes your environment through (`process.py:141,178,218`).

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 3 — `roadmap run --dry-run` prints the plan and creates the output directory (O17) `[LOCAL-WRITE]`

**Do:** (from `/tmp/d11/b`)

```bash
[ ! -e rm-dry ] && echo "rm-dry absent"
superclaude roadmap run spec.md --dry-run --output /tmp/d11/b/rm-dry > dry.out; echo "exit=$?"
grep -E '^Step [0-9]+' dry.out
sed -n '/^Step 1: extract/,/^$/p' dry.out
[ -d rm-dry ] && echo "rm-dry exists, entries: $(ls -A rm-dry | wc -l)"
```

**Expected result:** `rm-dry absent`; then on stderr `[roadmap] Input type: spec (spec=spec.md, tdd=None, prd=None)` and `exit=0`; then:

```text
Step 1: extract
Step 2 (parallel): generate-opus-architect
Step 3 (parallel): generate-sonnet-architect
Step 4: diff
Step 5: debate
Step 6: score
Step 7: merge
Step 8: anti-instinct
Step 9: test-strategy
Step 10: spec-fidelity
Step 11: deviation-analysis
Step 12: remediate
Step 1: extract
  Output: /tmp/d11/b/rm-dry/extraction.md
  Timeout: 300s
  Gate tier: STRICT
  Gate min_lines: 50
  Gate frontmatter: spec_source|spec_sources, generated, generator, functional_requirements, nonfunctional_requirements, total_requirements, complexity_score, complexity_class, domains_detected, risks_identified, dependencies_identified, success_criteria_count, extraction_mode
  Semantic checks: complexity_class_valid, extraction_mode_valid

rm-dry exists, entries: 0
```

The empty `rm-dry` directory is there although `--dry-run` "exits without launching subprocesses": `execute_roadmap` creates the output directory on its first line, before the dry-run branch (follow-up O17). Without `--output` the directory is the spec's own folder (`commands.py:331`), so always pass `--output` to a scratch path for a dry run. The plan has 12 steps; the group help says 8 (`commands.py:18`). (source: input-type line `commands.py:387-393`; `mkdir` `executor.py:3670`; dry-run branch `executor.py:3735-3737`; printout `executor.py:3126-3159`; step list `executor.py:2500-2520`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 4 — More than 3 inputs is a usage error `[LOCAL-WRITE]`

**Do:**

```bash
cp spec.md s2.md; cp spec.md s3.md; cp spec.md s4.md
superclaude roadmap run spec.md s2.md s3.md s4.md --dry-run --output /tmp/d11/b/four; echo "exit=$?"
ls -d /tmp/d11/b/four 2>&1
```

**Expected result:**

```text
Usage: superclaude roadmap run [OPTIONS] INPUT_FILES...
Try 'superclaude roadmap run --help' for help.

Error: Expected 1-3 input files, got 4. Provide at most one spec, one TDD, and one PRD.
exit=2
ls: cannot access '/tmp/d11/b/four': No such file or directory
```

The count is checked before any routing or directory creation, so nothing is written. (source: `commands.py:299-303`; the same check again in `_route_input_files`, `executor.py:224-231`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 5 — A step that fails its gate twice halts the run, exit 1 `[LOCAL-WRITE]`

**Do:** (the stand-in answers every prompt with the one line `stub output`)

```bash
PATH="/tmp/d11/stub:$PATH" superclaude roadmap run spec.md --depth quick --output /tmp/d11/b/halt > halt.out 2> halt.err; echo "exit=$?"
cat halt.out; echo "----- stderr"; cat halt.err
ls -A halt
jq -c '{depth, input_type, steps: (.steps | map_values(.status))}' halt/.roadmap-state.json
```

**Expected result:** `exit=1`, then (the elapsed time can read `0s` or `1s`):

```text
[roadmap] Starting step: extract
[roadmap] Step extract  FAIL (attempt 2, 1s)
           Reason: Below minimum line count: 1 < 50 in /tmp/d11/b/halt/extraction.md
----- stderr
[roadmap] Input type: spec (spec=spec.md, tdd=None, prd=None)
Structural audit skipped: no frontmatter in extraction
Structural audit skipped: no frontmatter in extraction
ERROR: Roadmap pipeline halted at step 'extract' (attempt 2/2)
  Gate failure: Below minimum line count: 1 < 50 in /tmp/d11/b/halt/extraction.md
  Output file: /tmp/d11/b/halt/extraction.md
  Output size: 12 bytes (1 lines)
  Step timeout: 300s | Elapsed: 1s

Completed steps: none
Failed step:     extract (FAIL, attempt 2)
Skipped steps:   generate-opus-architect, generate-sonnet-architect, diff, debate, score, merge, anti-instinct, test-strategy, spec-fidelity, deviation-analysis, remediate, certify, verify-implementation

To retry from this step:
  superclaude roadmap run /tmp/d11/b/spec.md --resume

To inspect the failing output:
  cat /tmp/d11/b/halt/extraction.md
.roadmap-state.json
extraction.err
extraction.md
spec.compressed.md
spec_id_registry.json
{"depth":"quick","input_type":"spec","steps":{"extract":"FAIL"}}
```

The extract output has 1 line where its gate needs 50, so the step runs a second time (`retry_limit=1` means 2 attempts) and then halts the pipeline. The spec was compressed into `spec.compressed.md` before the first step (skipped only by `--dry-run` or `--no-compress`). **Note:** the retry hint drops `--output`; run as printed, `--resume` would look for state in the spec's folder (`/tmp/d11/b`), not in `halt/`. Add `--output /tmp/d11/b/halt` yourself. Record this as observed-as-coded. (source: step prints `executor.py:3104-3123`; retry loop `pipeline/executor.py:209-216,366-388`; halt text `executor.py:2804-2873`; halt and exit `executor.py:3824-3826`; state `executor.py:3220-3240,3796`; compression `executor.py:3722-3730`; audit warning `executor.py:773-776`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 6 — `roadmap validate` exits 0 with blocking issues (NFR-006) `[LOCAL-WRITE]`

**Do:** (a run folder holding the three required inputs, and a report that counts 2 blocking issues)

```bash
mkdir -p /tmp/d11/b/v && cd /tmp/d11/b/v
printf '# Roadmap\n' > roadmap.md; printf '# Test strategy\n' > test-strategy.md; printf '# Extraction\n' > extraction.md
{ printf -- '---\nblocking_issues_count: 2\nwarnings_count: 1\ntasklist_ready: false\n---\n\n# Validation report\n\n'; seq -f 'Finding line %g' 1 14; printf -- '- [INFO] first note\n- [INFO] second note\n'; } > /tmp/d11/report-blocking.md
D11_STUB_REPORT=/tmp/d11/report-blocking.md PATH="/tmp/d11/stub:$PATH" superclaude roadmap validate /tmp/d11/b/v; echo "exit=$?"
ls validate
sed -n 2,3p validate/validation-report.md
```

**Expected result:**

```text
WARNING: 2 blocking issue(s) found
Warnings: 1
Info: 2

[validate] Complete: 2 blocking, 1 warning, 2 info
exit=0
validation-report.err
validation-report.md
blocking_issues_count: 2
warnings_count: 1
```

`exit=0` although 2 blocking issues were found: the command only prints the counts (the `WARNING` line is yellow on a terminal) and never sets a non-zero exit code, by design. The default `--agents opus:architect` is one agent, so one review session writes `validate/validation-report.md`; the counts come from its `blocking_issues_count` and `warnings_count` fields and the `[INFO]` lines of its body. (source: `commands.py:432-439,483-513`, comment "exit 0 per NFR-006" `:497`; required inputs `validate_executor.py:42,204-209`; single-agent step `validate_executor.py:244-281`; counts `validate_executor.py:348-394`; gate `validate_gates.py:31-46`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 7 — `roadmap validate` also exits 0 when the review session fails `[LOCAL-WRITE]`

**Do:** (the stand-in prints `stub output` and exits 1)

```bash
rm -rf validate
D11_STUB_EXIT=1 PATH="/tmp/d11/stub:$PATH" superclaude roadmap validate /tmp/d11/b/v; echo "exit=$?"
cat validate/validation-report.md
```

**Expected result:** on stderr `Validation pipeline halted: 1 step(s) failed`, then:

```text

[validate] Complete: 0 blocking, 0 warning, 0 info
exit=0
stub output
```

The review session failed, yet the command reports `0 blocking` and exits 0: a report without frontmatter counts as zero findings. A failed validation therefore looks like a clean one. Check the stderr line, not the exit code. Record this as observed-as-coded. (source: failure only logged `validate_executor.py:519-523`; counts default to 0 `validate_executor.py:354-361`; `commands.py:495-513`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 8 — `tasklist validate` exits 1 on a HIGH deviation `[LOCAL-WRITE]`

**Do:**

```bash
cd /tmp/d11/b
mkdir -p tl-out/tasklist && printf '# Roadmap\n' > tl-out/roadmap.md && printf '# Phase 1\n' > tl-out/tasklist/phase-1-tasklist.md
fid() { { printf -- '---\nhigh_severity_count: %s\nmedium_severity_count: 0\nlow_severity_count: 1\ntotal_deviations: %s\nvalidation_complete: true\ntasklist_ready: %s\n---\n\n# Tasklist fidelity\n\n' "$1" "$2" "$3"; seq -f 'Deviation line %g' 1 14; } > "$4"; }
fid 1 2 false /tmp/d11/report-high.md
fid 0 1 true /tmp/d11/report-clean.md
D11_STUB_REPORT=/tmp/d11/report-high.md PATH="/tmp/d11/stub:$PATH" superclaude tasklist validate tl-out --tasklist-dir tl-out/tasklist; echo "exit=$?"
sed -n 2p tl-out/tasklist-fidelity.md
```

**Expected result:** on stderr `Tasklist validation pipeline halted: 1 step(s) failed`, then:

```text
[tasklist validate] Report written to /tmp/d11/b/tl-out/tasklist-fidelity.md
FAIL: HIGH-severity deviations found
exit=1
high_severity_count: 1
```

The report fails the gate check `high_severity_count_zero`, so the session runs twice and the step fails; either way the exit code follows the report's `high_severity_count`. The `FAIL` line is red on a terminal. (source: report path and messages `tasklist/commands.py:173-185`; step, `retry_limit=1` `tasklist/executor.py:170-186`; HIGH check `tasklist/executor.py:189-216,219-244`; gate `tasklist/gates.py:23-46`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 9 — `tasklist validate` exits 0 with no HIGH deviation `[LOCAL-WRITE]`

**Do:**

```bash
D11_STUB_REPORT=/tmp/d11/report-clean.md PATH="/tmp/d11/stub:$PATH" superclaude tasklist validate tl-out --tasklist-dir tl-out/tasklist; echo "exit=$?"
```

**Expected result:**

```text
[tasklist validate] Report written to /tmp/d11/b/tl-out/tasklist-fidelity.md
PASS: No HIGH-severity deviations
exit=0
```

Nothing on stderr. (source: `tasklist/commands.py:173-185`; `tasklist/executor.py:207-214`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

### Tier C — real runs (`[API-LONG]`, Claude API)

#### Step 10 — Quick-depth roadmap run `[API-LONG]`

**Do:** (needs the spec from Step 2; the run prints progress until it ends)

```bash
mkdir -p /tmp/d11/c && cd /tmp/d11/c && cp /tmp/d11/b/spec.md spec.md
superclaude roadmap run spec.md --depth quick --output /tmp/d11/c/out; echo "exit=$?"
ls out
jq -c '{depth, steps: (.steps | map_values(.status)), validation: .validation.status}' out/.roadmap-state.json
grep -m1 '^rounds_completed:' out/debate-transcript.md
```

**Expected result:**

- On stderr `[roadmap] Input type: spec (spec=spec.md, tdd=None, prd=None)`; on stdout a `[roadmap] Starting step: <id>` line and a `[roadmap] Step <id>  PASS (attempt <n>, <s>s)` line for each step, then `[roadmap] Pipeline complete: <N> steps passed`, then `[roadmap] Auto-invoking validation...` and `[validate] Complete: <B> blocking, <W> warning, <I> info`; `exit=0`. Lines about certify and `[roadmap] Verify-implementation ...` may appear between the two; a `Verify-implementation FAILED` line is a recorded caveat and does not change the exit code.
- `ls out` includes `extraction.md`, `roadmap-opus-architect.md`, `roadmap-sonnet-architect.md`, `diff-analysis.md`, `debate-transcript.md`, `base-selection.md`, `roadmap.md`, `anti-instinct-audit.md`, `test-strategy.md` and the folder `validate`, which holds `reflect-opus-architect.md`, `reflect-sonnet-architect.md` and `validation-report.md` (the auto-validation uses the run's two agents).
- The state line shows `"depth":"quick"`, the steps with `"PASS"` and `"validation":"pass"` (0 blocking) or `"fail"` (blocking issues). `fail` here does not change the exit code.
- `rounds_completed: 1`: the quick depth asks the debate for a single round. The value is written by the model; record a different value in the notes.

If a step fails its gate twice, the run ends with the halt report of Step 5 and `exit=1`: mark FAIL and note the step and its `Gate failure` line. The step outputs are written by Claude, so their content is not fixed; the step names, files, state keys and exit codes are. (source: progress `executor.py:3104-3123,3787-3793`; completion `executor.py:3828`; certify and verify `executor.py:3836-3841,2446-2469`; auto-validation with up to 2 agents `executor.py:3843-3862,4094-4131`; multi-agent files `validate_executor.py:284-345`; state `executor.py:3220-3240,4068-4090`; depth wording `prompts.py:36-52`, passed to the debate `executor.py:2645-2652`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 11 — `roadmap validate` on the real run `[API-LONG]`

**Do:**

```bash
cd /tmp/d11/c
superclaude roadmap validate /tmp/d11/c/out; echo "exit=$?"
sed -n '2,/^---$/p' out/validate/validation-report.md | grep -E '^(blocking_issues_count|warnings_count):'
```

**Expected result:** an optional `WARNING: <B> blocking issue(s) found` line, optional `Warnings:` and `Info:` lines, then `[validate] Complete: <B> blocking, <W> warning, <I> info` and **`exit=0` whatever `<B>` is**. One `opus` review session (default `--agents opus:architect`) rewrites `out/validate/validation-report.md`; its `blocking_issues_count` and `warnings_count` equal `<B>` and `<W>`. If `<B>` is above 0 and the exit is still 0, that is the NFR-006 design shown in Step 6, not a failure. If stderr shows `Validation pipeline halted`, the counts mean nothing (Step 7): mark FAIL. (source: `commands.py:430-513`; `validate_executor.py:244-281,348-394,519-523`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 12 — `tasklist validate` on a tasklist that does not match the roadmap `[API-LONG]`

**Do:**

```bash
mkdir -p /tmp/d11/c/tasklist && cd /tmp/d11/c
cat > tasklist/phase-1-tasklist.md <<'EOF'
# Phase 1 -- Payment gateway

### T01.01 -- Build a payment gateway

**Roadmap Item IDs:** R-999

**Deliverables:** D-9999 (payment gateway service)

**Dependencies:** None
EOF
superclaude tasklist validate /tmp/d11/c/out --tasklist-dir /tmp/d11/c/tasklist; echo "exit=$?"
sed -n '2,/^---$/p' out/tasklist-fidelity.md | grep -E '^(high_severity_count|tasklist_ready):'
```

**Expected result:** `[tasklist validate] Report written to /tmp/d11/c/out/tasklist-fidelity.md`, `FAIL: HIGH-severity deviations found`, `exit=1`; then `high_severity_count:` with a value of 1 or more and `tasklist_ready: false`. The tasklist cites a roadmap item and a deliverable that do not exist and covers none of the roadmap's items, which the prompt defines as HIGH ("fabricated traceability", "has no corresponding task"). The gate fails on a HIGH count, so expect two sessions (stderr `Tasklist validation pipeline halted: 1 step(s) failed`). No `Auto-wired` line appears: the run's `.roadmap-state.json` records no TDD or PRD. The HIGH count is the model's judgement; the exit code follows it. (source: severity rules `tasklist/prompts.py:49-57,94-100`; auto-wire `tasklist/commands.py:113-159`; `tasklist/commands.py:173-185`; `tasklist/executor.py:170-186,219-244`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

---

## Edge cases (optional but recommended)

Run these in the Tier B terminal, from `/tmp/d11/b`, after Step 9.

| Try this | Expected behavior | Source | Pass/Fail |
|---|---|---|---|
| `[FREE]` `superclaude roadmap run spec.md s2.md --dry-run --output /tmp/d11/b/two; echo "exit=$?"` | `Error: Multiple files detected as spec: spec.md, s2.md. Use --input-type to disambiguate.` and `exit=2`; `two` is not created | `executor.py:247-257` | ☐ |
| `[FREE]` `superclaude roadmap run nope.md --dry-run; echo "exit=$?"` | `Error: Invalid value for 'INPUT_FILES...': Path 'nope.md' does not exist.` and `exit=2` | `commands.py:33-35` | ☐ |
| `[FREE]` `superclaude roadmap run spec.md --depth fast --dry-run; echo "exit=$?"` | `Error: Invalid value for '--depth': 'fast' is not one of 'quick', 'standard', 'deep'.` and `exit=2` | `commands.py:51-56` | ☐ |
| `[FREE]` `superclaude roadmap accept-spec-change /tmp/d11/b/halt; echo "exit=$?"` | `Spec hash is already current. Nothing to do.` and `exit=0` (the spec is unchanged since Step 5) | `spec_patch.py:200-206` | ☐ |
| `[FREE]` `superclaude roadmap accept-spec-change /tmp/d11/b/rm-dry; echo "exit=$?"` | ``No .roadmap-state.json found in /tmp/d11/b/rm-dry. Run `roadmap run` first.`` and `exit=1` | `spec_patch.py:169-177` | ☐ |
| `[LOCAL-WRITE]` `mkdir -p empty; superclaude roadmap validate /tmp/d11/b/empty 2>&1 \| tail -1; echo "exit=${PIPESTATUS[0]}"` | A Python traceback ending `FileNotFoundError: Required validation input not found: /tmp/d11/b/empty/roadmap.md`, `exit=1`: missing inputs give a traceback, not a one-line error | `validate_executor.py:204-209`; `commands.py:495` | ☐ |
| `[LOCAL-WRITE]` `superclaude tasklist validate /tmp/d11/b/tl-new 2>&1 \| tail -1; echo "exit=${PIPESTATUS[0]}"; ls -d tl-new` | Traceback ending `FileNotFoundError: No markdown files found in tasklist directory: /tmp/d11/b/tl-new`, `exit=1`, and `tl-new` now exists: the output folder is created before the inputs are checked | `tasklist/commands.py:100-111`; `tasklist/executor.py:40-52` | ☐ |
| `[LOCAL-WRITE]` `D11_STUB_REPORT=/tmp/d11/report-blocking.md PATH="/tmp/d11/stub:$PATH" superclaude roadmap validate /tmp/d11/b/v --agents opus:architect,sonnet:qa; echo "exit=$?"; sed -n 2,3p v/validate/validation-report.md` | stderr `Validation partial failure: passed=['reflect-opus-architect', 'reflect-sonnet-qa'], failed=['adversarial-merge']` and `Wrote degraded validation report to /tmp/d11/b/v/validate/validation-report.md`; stdout `[validate] Complete: 0 blocking, 0 warning, 0 info`; `exit=0`; then `validation_complete: false` and `blocking_issues_count: 0`. Both reviews counted 2 blocking issues, but the merge report (which needs an agreement table) failed and the degraded report records 0 | `validate_executor.py:284-345,397-445,507-518`; `validate_gates.py:48-69` | ☐ |

Without `--tasklist-dir`, `tasklist validate` reads every `.md` file in OUTPUT_DIR as a tasklist file, which in a roadmap run folder includes `roadmap.md`, `extraction.md` and the other step outputs (`tasklist/commands.py:109-111`; `tasklist/executor.py:40-52`). Pass `--tasklist-dir` as Steps 8, 9 and 12 do.

## Cleanup

```bash
cd /tmp && rm -rf /tmp/d11
```

The stand-in `claude` lived only in `/tmp/d11/stub` and was on the `PATH` only for the commands that set it. What stays under your real `~/.claude` after Tier C is what the installed hooks write for any Claude Code session: rows in `~/.claude/state/` and `~/.claude/logs/`; the pipeline sessions saved no transcript (`--no-session-persistence`, `src/superclaude/cli/pipeline/process.py:152`).

## Overall result

☐ **PASS** — capability works as documented for `5.0.0`
☐ **FAIL** — see failing step(s) above

**Tester:** `<name>`  **Date:** `<date>`  **Build:** `5.0.0 (tag v5.0.0, commit d953b983)`
