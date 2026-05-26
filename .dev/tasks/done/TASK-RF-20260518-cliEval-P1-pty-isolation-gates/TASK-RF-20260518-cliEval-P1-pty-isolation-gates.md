---
id: "TASK-RF-20260518-cliEval-P1-pty-isolation-gates"
title: "cliEval Phase 1 — Vendored ptytest + HomeIsolation + Capability Gates + `eval doctor`"
description: "Phase 1 of the cliEval release — the viability gate. Vendor brandon-fryslie/ptytest under src/superclaude/cli/eval/pty/, implement HomeIsolation (compose IsolationLayers) + capability_gates.py + a Click `eval doctor` subcommand, and add three unit-test files. Produces a working `uv run superclaude eval doctor` that prints green-checklist verification of hard requirements (claude/make/jq/git) and optional MCP capabilities. Output is NOT runnable by Sprint CLI; this task file is executed manually via `/task`."
status: "🟡 To Do"
type: "🆕 Feature"
priority: "🔼 High"
created_date: "2026-05-18"
updated_date: "2026-05-18"
assigned_to: "orchestrator"
autogen: false
autogen_method: ""
coordinator: orchestrator
parent_task: ""
depends_on: []
related_docs:
- path: ".dev/releases/current/cliEval/design-spec.md"
  description: "Authoritative design spec — §2 (component architecture), §3 (directory layout), §7 (HomeIsolation), §11 (capability gating), §13 (fork strategy)."
- path: ".dev/releases/current/cliEval/decisions.md"
  description: "Architectural decisions log — D-1 (PTY layer = fork ptytest, vendor under cli/eval/pty/) and D-3 (HomeIsolation COMPOSES IsolationLayers, has-a not is-a)."
- path: ".dev/releases/current/cliEval/build-requests/BUILD-REQUEST-cliEval-P1-pty-isolation-gates.md"
  description: "BUILD_REQUEST for this task — scope, files-to-create list, 8 acceptance criteria (AC-P1.1..AC-P1.8), and 3 open questions for the executor."
- path: "src/superclaude/cli/sprint/executor.py"
  description: "Existing 4-layer IsolationLayers primitive at lines 107-182. READ-ONLY reference; HomeIsolation composes (not extends) this class per D-3."
- path: "src/superclaude/cli/prd/__init__.py"
  description: "Sub-package layout to mirror — Click group export pattern (`from .commands import prd_group; __all__ = ['prd_group', ...]`). HomeIsolation analogue for cli/eval/__init__.py."
- path: "src/superclaude/cli/pipeline/process.py"
  description: "Existing subprocess driver reference (ClaudeProcess at lines 24-150). Scaffolding pattern for PtyDriver; PtyDriver is a PTY equivalent, not an extension."
- path: "src/superclaude/cli/install_hooks.py"
  description: "Existing installer — HomeIsolation.setup() MUST call install_hooks(target_path=home_root/'.claude', force=True) to deploy the 9-script hook set + settings.json + seed files into per-eval HOMEs."
template_schema_doc: ".claude/templates/workflow/02_mdtm_template_complex_task.md"
estimation: "~400 LOC (per design-spec §17 Phase 1 estimate)"
sprint: "cliEval-P1"
due_date: ""
start_date: ""
completion_date: ""
blocker_reason: ""
ai_model: ""
model_settings: ""
review_info:
  last_reviewed_by: ""
  last_review_date: ""
  next_review_date: ""
task_type: static
tags:
- "cliEval"
- "phase-1"
- "pty"
- "isolation"
- "capability-gates"
- "vendoring"
- "feature"
---

# cliEval Phase 1 — Vendored ptytest + HomeIsolation + Capability Gates + `eval doctor`

## Task Overview

This task implements **Phase 1 of the cliEval release** — a real-world eval harness for IronClaude's hook system. Phase 1 is the **viability gate**: if vendored `ptytest` can drive a real Claude Code TTY subprocess and `HomeIsolation` provides clean per-eval `HOME` isolation, the rest of the harness (Phases 2-5) is straightforward. If Phase 1 fails, the architecture pivots. The task file ends with a working `uv run superclaude eval doctor` subcommand that prints a green-checklist verification of all hard requirements (claude binary, make, jq, git) and optional capabilities (3 MCP servers).

The task uses **Template 02 (Complex Task)** because it requires discovery before building (decisions log + design-spec must be cross-checked against current source line ranges), parallel-style independent build streams (vendored `pty/`, `isolation.py`, `capability_gates.py`, and `commands.py` are largely independent files), test/execute steps (vendored pytest suite must pass), QA gate checkpoints between major implementation phases (PG-1 through PG-4 per the I15/I16 convention), and conditional fix cycles (failed QA gates trigger up to 3 fix cycles per gate type with the Retry Monotonicity Protocol from rf-task-builder Critical Rule 14 applied). Output target line count is **~400 LOC** across 14 new files (per design-spec §17 Phase 1 estimate: pty/ ~150 LOC adapted, isolation.py ~120 LOC, capability_gates.py ~80 LOC, commands.py doctor-only ~50 LOC, tests ~150-200 LOC across 3 files).

The task file is **NOT runnable by Sprint CLI** — it is built for manual execution via the `/task` skill per the user's 2026-05-18 directive. The branch for execution will be `feat/cliEval-P1-pty-isolation-gates` and the PR title will be `feat(eval): cliEval P1 — vendor ptytest + HomeIsolation + capability gates + eval doctor`.

## Key Objectives

The following objectives MUST be achieved by this task. Each maps to one or more of the 8 acceptance criteria from the BUILD_REQUEST (AC-P1.1 through AC-P1.8) — see the **Acceptance Criteria Mapping** section below for the per-AC checklist-item index.

1. **Vendor brandon-fryslie/ptytest fork under `src/superclaude/cli/eval/pty/`** with the upstream MIT LICENSE preserved verbatim, PROVENANCE.md documenting fork SHA + rename PtySession→PtyDriver + removed pytest-fixture autoloader + added expect_prompt_ready/inject_prompt + tightened pexpect>=4.9 + aggressive ANSI strip (AC-P1.4, AC-P1.5).
2. **Implement `HomeIsolation` in `src/superclaude/cli/eval/isolation.py`** as a class that COMPOSES (has-a, not is-a) the existing `IsolationLayers` from `src/superclaude/cli/sprint/executor.py:107-182`, adding HOME / XDG_* / CLAUDE_SESSION_ID overrides; `setup()` deploys 9 hook scripts via `install_hooks` + writes settings.json + seeds requested state files; `env()` returns the env-var overlay including passthrough of PATH/USER/TERM/LANG/CI; `teardown(keep=False)` rm-rf's the dir unless keep=True (AC-P1.2, AC-P1.6).
3. **Implement `capability_gates.py`** with the `Capability` dataclass + `CAPABILITIES` registry (4 hard binaries + 3 optional MCP servers per design-spec §11) + `check_all(skip_flags)` returning a `CapabilityReport` consumed by `eval doctor` (AC-P1.1).
4. **Implement Click sub-package `cli/eval/`** with `__init__.py` exporting `eval_group`, `config.py` with `EvalConfig` dataclass, and `commands.py` with ONLY the `eval doctor` subcommand wired (`eval run`, `eval list`, `eval describe` are explicitly out-of-scope for Phase 1 — they land in P2/P3) (AC-P1.1).
5. **Add three pytest test files under `tests/cli/test_eval/`**: `test_isolation.py` (HOME override correctness + setup/teardown idempotence), `test_capability_gates.py` (all gates including missing-binary failure modes), `test_pty_vendor.py` (vendored ptytest's own upstream test suite still passes after our diffs) (AC-P1.3, AC-P1.4, AC-P1.8).
6. **Hard guard in `HomeIsolation.setup()`** that REFUSES to operate if `home_root` is outside a known eval-runs scratch dir (e.g., `/tmp/eval-runs/...` or `.dev/eval-runs/...`) — prevents the foot-gun where a typo blows away the real `~/.claude/` (AC-P1.6).
7. **No regression to `make verify-sync`** — after this phase lands, `make verify-sync` MUST still exit 0. The PRE/POST verify-sync runs are encoded as explicit validation items (AC-P1.7).
8. **All new tests pass** — `uv run pytest tests/cli/test_eval/test_isolation.py tests/cli/test_eval/test_capability_gates.py tests/cli/test_eval/test_pty_vendor.py -v` returns 0 with all tests PASS (AC-P1.8).

## Prerequisites & Dependencies

### Parent Task & Dependencies

- **Parent Task:** None (first phase of cliEval release; no upstream task).
- **Blocking Dependencies:** None at task-start — the design-spec and decisions log are already published; the upstream ptytest repo at <https://github.com/brandon-fryslie/ptytest> is publicly reachable.
- **This task blocks:** cliEval Phase 2 (loader.py + models.py + expect.py + eval describe/list), Phase 3 (orchestrator.py + runner.py + reporter.py + eval run), Phase 4 (wire into cli/main.py + Makefile + .gitignore), and Phase 5 (eval body implementations E1-E15).

### Required Inputs (read in Phase 1)

The Stage A-equivalent (design + decisions + BUILD_REQUEST) has already produced the inputs listed below. The actual checklist items for reading these inputs appear in Phase 1.

- **Design spec:** `.dev/releases/current/cliEval/design-spec.md` — Purpose: §2 component architecture, §3 directory layout (PHASE-1 SUBSET), §7 HomeIsolation interface signature + key correctness invariants, §11 capability gating tiers, §13 fork strategy + what-we-change-vs-upstream table.
- **Decisions log:** `.dev/releases/current/cliEval/decisions.md` — Purpose: D-1 (PTY layer = fork ptytest, vendor under cli/eval/pty/), D-3 (HomeIsolation COMPOSES IsolationLayers, has-a not is-a).
- **BUILD_REQUEST:** `.dev/releases/current/cliEval/build-requests/BUILD-REQUEST-cliEval-P1-pty-isolation-gates.md` — Purpose: 14 files-to-create list, 8 acceptance criteria, 3 open questions, scope of OUT-of-scope items deferred to P2/P3/P4.
- **Existing primitive (READ-ONLY reference):** `src/superclaude/cli/sprint/executor.py:107-182` `IsolationLayers` — Purpose: D-3 composition target. MUST NOT be modified by this task.
- **Existing primitive (reference, ANALOGOUS pattern):** `src/superclaude/cli/pipeline/process.py:24-150` `ClaudeProcess` — Purpose: subprocess driver scaffolding pattern; PtyDriver is the PTY equivalent.
- **Existing primitive (CALLED FROM HomeIsolation.setup):** `src/superclaude/cli/install_hooks.py:install_hooks` — Purpose: deploys the 9-script hook set + settings.json + seed files into per-eval HOMEs.
- **Existing sub-package layout to mirror:** `src/superclaude/cli/prd/` — Purpose: Click group export pattern (commands.py + __init__.py re-export).
- **Upstream to fork:** `https://github.com/brandon-fryslie/ptytest` (MIT, Python 3.8+) — Purpose: vendor under `src/superclaude/cli/eval/pty/`. Preserve LICENSE verbatim.

### Handoff File Convention

This task uses intra-task handoff patterns (Template 02 Section L). Items write intermediate outputs to:

**`.dev/tasks/to-do/TASK-RF-20260518-cliEval-P1-pty-isolation-gates/phase-outputs/`** with the following pre-created subdirectories:

- `discovery/` — Phase 1 pre-implementation research (L1 discovery items): line-number drift verification, ptytest upstream-SHA + LICENSE confirmation, IsolationLayers API surface inventory, install_hooks contract extraction.
- `test-results/` — Phase 6 test execution captures (L3 test items): pytest output for each of the 3 test files, plus `make verify-sync` PRE/POST captures.
- `reviews/` — Phase-gate QA reports (PG-1 through PG-5): rf-qa task-integrity reports for each gate.
- `plans/` — Phase 7 conditional fix plans (L5 conditional items) if any PG fails.
- `reports/` — Phase 8 aggregation reports (L6 aggregation items): the per-AC verification matrix and the final task-completion summary.

These files persist across all batches and session rollovers. Later items read them by path.

### Frontmatter Update Protocol

YOU MUST update the frontmatter at these MANDATORY checkpoints:

- **Upon Task Start:** Update `status` to "🟠 Doing" and `start_date` to current date (Phase 1 Step 1.1).
- **Upon Completion:** Update `status` to "🟢 Done" and `completion_date` to current date (Phase 8 final step).
- **If Blocked:** Update `status` to "⚪ Blocked" and populate `blocker_reason`.
- **After Each Work Session:** Update `updated_date` to current date.

DO NOT modify any other frontmatter fields unless explicitly directed by the user.

### Acceptance Criteria Mapping

Each acceptance criterion from the BUILD_REQUEST §"Acceptance criteria" maps to one or more checklist items in this task file. The mapping table:

| AC-ID | Brief | Encoded by checklist items |
|---|---|---|
| AC-P1.1 | `eval doctor` green-checklist + exit 0/2 | 4.1, 4.2, 4.3, 6.3, 8.2 |
| AC-P1.2 | `HomeIsolation` setup/env/teardown contract | 3.1, 3.2, 3.3, 6.1, 8.2 |
| AC-P1.3 | `PtyDriver` spawn/expect_prompt_ready/inject_prompt/terminate | 2.3, 2.4, 6.2, 8.2 |
| AC-P1.4 | Vendored ptytest upstream test suite passes | 2.5, 5.3, 6.2, 8.2 |
| AC-P1.5 | PROVENANCE.md documents all 6 documented diffs | 2.6, 8.2 |
| AC-P1.6 | Hard guard refuses HOME outside scratch dir | 3.2, 5.1, 8.2 |
| AC-P1.7 | `make verify-sync` EXIT=0 PRE and POST | 1.5, 7.1, 8.2 |
| AC-P1.8 | All new tests pass under uv run pytest | 5.1, 5.2, 5.3, 6.1, 6.2, 6.3, 8.2 |

The Phase 8 aggregation report (`phase-outputs/reports/per-ac-verification-matrix.md`) materializes this table with PASS/FAIL evidence per AC at task completion.

---

## Detailed Task Instructions

### Phase 1: Pre-Implementation Discovery & Open-Question Resolution

YOU MUST complete EVERY item in this phase IN ORDER before any source-file is created. This phase resolves the 3 open questions from the BUILD_REQUEST and writes line-number-verified discovery artifacts to `phase-outputs/discovery/` for downstream phases to consume. Mark each item complete before proceeding.

**Step 1.1:** Update task status to "🟠 Doing"

- [ ] Update the `status` field in the frontmatter at the top of this task file from "🟡 To Do" to "🟠 Doing" and update the `start_date` field to today's date (use the current date from the session-context envelope, NOT a hard-coded value), then add a timestamped entry to the `### Execution Log` in the `## Task Log / Notes` section at the bottom of this task file using the format `**[YYYY-MM-DD HH:MM]** - Task started: Updated status to "🟠 Doing" and start_date.`, ensuring no other frontmatter fields are modified. If unable to edit the frontmatter due to file access issues, log the specific blocker using the templated format in the `### Phase 1 Findings` section of the `## Task Log / Notes` at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 1.2:** Verify pre-created task folder structure (L1 Discovery)

- [ ] Use Glob on `.dev/tasks/to-do/TASK-RF-20260518-cliEval-P1-pty-isolation-gates/phase-outputs/*` to confirm that the five pre-created subdirectories `discovery/`, `test-results/`, `reviews/`, `plans/`, `reports/` all exist under the task folder (these were pre-created by the task-builder; this task MUST NOT create a new dated task folder), ensuring every subdirectory listed in the "Handoff File Convention" section of this task file is present and writable. If any subdirectory is missing, create it with `mkdir -p` and log the unexpected absence as a finding in the `### Phase 1 Findings` section of the `## Task Log / Notes` at the bottom of this task file. Once done, mark this item as complete.

**Step 1.3:** Verify IsolationLayers API surface (L1 Discovery — composition target)

- [ ] Read the file `src/superclaude/cli/sprint/executor.py` at lines 100-185 using Read tool to extract the verbatim current line range and content of the `IsolationLayers` dataclass (BUILD_REQUEST cites lines 107-182; verify the current actual line range matches), then write the file `.dev/tasks/to-do/TASK-RF-20260518-cliEval-P1-pty-isolation-gates/phase-outputs/discovery/01-isolation-layers-api.md` containing (a) the verified-current line range of the dataclass, (b) the verbatim 4 field names (scoped_work_dir, git_boundary, plugin_dir, settings_dir), (c) the `env_vars` property return-dict structure (CLAUDE_WORK_DIR, GIT_CEILING_DIRECTORIES, CLAUDE_PLUGIN_DIR, CLAUDE_SETTINGS_DIR), (d) the `layers_active` property structure, (e) a notation that the class is `@dataclass` (not frozen), (f) an explicit "MUST NOT be modified" marker per D-3 — ensuring all extracted facts come directly from the file with no fabrication, and the discovery file ends with a `## Composition Plan` section showing how `HomeIsolation` will take an `IsolationLayers` instance as a constructor argument and merge env-var dicts. If the line range has drifted ≥5 lines from BUILD_REQUEST citation, also append a `## Drift Notice` subsection with the verified-current line range as the source of truth for downstream items. If unable to read the source file or write the output file, log the specific blocker using the templated format in the `### Phase 1 Findings` section of the `## Task Log / Notes`, then mark this item complete. Once done, mark this item as complete.

**Step 1.4:** Verify install_hooks contract (L1 Discovery — called from HomeIsolation.setup)

- [ ] Read the file `src/superclaude/cli/install_hooks.py` at lines 1-120 using Read tool to extract the `install_hooks` function signature, the `_FRESHNESS_SCRIPTS` list contents (count of script files that will be deployed), the `_LEGACY_SCRIPTS` list, the `_SEED_FILES` list, and the `target_path: Path | None = None, force: bool = False` parameter defaults, then write the file `.dev/tasks/to-do/TASK-RF-20260518-cliEval-P1-pty-isolation-gates/phase-outputs/discovery/02-install-hooks-contract.md` containing (a) the verbatim function signature including parameter types and defaults, (b) the explicit list of scripts that will be deployed (count must match BUILD_REQUEST AC-P1.2's "9 hook scripts" claim — record the actual count even if it differs and flag the discrepancy), (c) where the function reads source scripts from (relative to package), (d) any preconditions (atomic write, backup before overwrite, malformed-target refusal), (e) a `## Call Plan` section showing HomeIsolation.setup() will invoke `install_hooks(target_path=home_root / '.claude', force=True)` with rationale (per-eval HOME is ephemeral; force=True is safe). If the script count does NOT match the BUILD_REQUEST's "9 hook scripts" assertion, append a `## Count Drift` subsection — the verified-current count is the source of truth; the BUILD_REQUEST assertion is informational only. If unable to read the source file or write the output file, log the specific blocker using the templated format in the `### Phase 1 Findings` section, then mark this item complete. Once done, mark this item as complete.

**Step 1.5:** Capture PRE-state `make verify-sync` exit code (AC-P1.7 baseline)

- [ ] Run `make verify-sync` from the repository root using Bash tool and capture both the exit code and the full stdout/stderr output to the file `.dev/tasks/to-do/TASK-RF-20260518-cliEval-P1-pty-isolation-gates/phase-outputs/test-results/00-verify-sync-PRE.txt` with a leading header line `# PRE-state make verify-sync — baseline before any cliEval-P1 file is created\n# Date: [today]\n# Exit code: <N>\n---\n` followed by the captured output, ensuring the exit code is captured exactly via `$?` immediately after the command runs. If the PRE-state exit code is NOT 0, append a `BLOCKER` line at the top of the capture file and log the blocker in the `### Phase 1 Findings` section of the `## Task Log / Notes` — the task SHOULD NOT proceed if the working tree is already out-of-sync before any work begins (a non-0 PRE-state exit means AC-P1.7 is unmeasurable). Once done, mark this item as complete.

**Step 1.6:** Resolve Open Question Q1 — pexpect>=4.9 acceptability (L1 Discovery)

- [ ] Run `uv pip list 2>&1 | grep -i pexpect` from the repository root using Bash tool and capture the output, then read `pyproject.toml` at the repo root using Read tool to check whether `pexpect` is declared as a direct dependency or only transitively pulled, then write the file `.dev/tasks/to-do/TASK-RF-20260518-cliEval-P1-pty-isolation-gates/phase-outputs/discovery/03-pexpect-acceptability.md` containing (a) the current installed pexpect version (if any), (b) whether pexpect is in `[project].dependencies` of pyproject.toml or only transitive, (c) the BUILD_REQUEST Q1 verbatim ("Confirm `pexpect>=4.9` is acceptable as a new runtime dep"), (d) a `## Decision` section with one of: ACCEPTABLE (add `pexpect>=4.9` to `[project].dependencies` in pyproject.toml as part of Phase 2), CONDITIONAL (acceptable IF a specific condition is met — describe), DEFERRED-TO-VENDOR (vendor pexpect inside cli/eval/pty/vendor/pexpect/ if Q1 cannot be resolved by checking installed state) — pick the option supported by the evidence found. If neither pyproject.toml nor `uv pip list` is readable, log the specific blocker in `### Phase 1 Findings` and pick DEFERRED-TO-VENDOR as the safe default. Once done, mark this item as complete.

**Step 1.7:** Resolve Open Question Q2 — upstream ptytest MIT license verification (L1 Discovery)

- [ ] Use WebFetch on `https://github.com/brandon-fryslie/ptytest/blob/main/LICENSE` with prompt "Return the full verbatim text of the LICENSE file, plus the SPDX identifier if present, plus the copyright holder line." then also WebFetch `https://github.com/brandon-fryslie/ptytest` with prompt "Return the latest commit SHA on the default branch and the date of that commit." then write the file `.dev/tasks/to-do/TASK-RF-20260518-cliEval-P1-pty-isolation-gates/phase-outputs/discovery/04-ptytest-license-and-sha.md` containing (a) the verbatim upstream LICENSE text, (b) the SPDX identifier (expected: MIT), (c) the copyright holder line, (d) the fork SHA captured at this discovery time (to be embedded byte-for-byte in PROVENANCE.md in Phase 2), (e) the date of the fork SHA, (f) a `## Decision` section confirming MIT compatibility with IronClaude — IronClaude is licensed permissively; MIT is compatible; LICENSE reproduction in `cli/eval/pty/LICENSE` is sufficient license compliance (no NOTICE file required for MIT-into-MIT/Apache contexts; if the IronClaude top-level license is not MIT/Apache-permissive, append a `## NOTICE Requirement` subsection). If WebFetch is unavailable, log the blocker and substitute with a placeholder fork-SHA-marker `FORK_SHA_TBD_VIA_GIT_CLONE_IN_PHASE_2` — Phase 2 Step 2.1 will resolve it from the cloned working tree. Once done, mark this item as complete.

**Step 1.8:** Resolve Open Question Q3 — Claude Code TTY prompt-ready signal heuristic (L1 Discovery)

- [ ] Use WebSearch for "Claude Code CLI TTY interactive prompt regex pattern" and "Claude Code REPL prompt detection pexpect" to gather public information on Claude Code's interactive prompt format, then write the file `.dev/tasks/to-do/TASK-RF-20260518-cliEval-P1-pty-isolation-gates/phase-outputs/discovery/05-prompt-ready-heuristic.md` containing (a) the BUILD_REQUEST Q3 verbatim ("Verify Claude Code's TTY behavior on Linux — specifically, does it emit a deterministic prompt-ready signal that `expect_prompt_ready` can match?"), (b) any external evidence found, (c) a `## Decision` section selecting ONE primary heuristic and ONE fallback heuristic. The primary heuristic SHOULD be a compiled regex that matches one of `^> $`, `^\$ $`, `^claude> $`, or `^❯ $` (whichever is observed in any captured Claude Code TTY transcript referenced in the repo — search `.dev/` for `*.log` files containing claude-code output). The fallback heuristic SHOULD be an idle-stdout timeout (e.g., 1.5 seconds of no new bytes), used when the regex does not match within `timeout` seconds. The decision MUST be encoded in `PROVENANCE.md` in Phase 2 Step 2.6 and reflected in `PtyDriver.expect_prompt_ready` implementation in Phase 2 Step 2.4. If no external evidence is found and no in-repo TTY transcripts exist, document the gap and pick the default heuristic `^> $` with the idle-timeout fallback — surface this as an Open Question in the Open Questions section at the bottom of this task file (the executor should re-run with verbose logging during AC-P1.3 verification and update the heuristic if needed). Once done, mark this item as complete.

---

#### PG-1: Phase-Gate QA — Pre-Implementation Discovery Verification

**Context:** This is the first phase-gate QA checkpoint per the I15/I16 convention from rf-task-builder. It verifies that Phase 1's discovery artifacts are evidence-based and complete BEFORE any source file is created. A FAIL verdict triggers a fix cycle (max 3 cycles per task-integrity gate type, per rf-qa.md fix-cycle limits). The Retry Monotonicity Protocol (regression check FIRST, then `|F_n| >= |F_{n-1}|` halt) applies — see PG-2 for the full halt-message specification.

**Step PG-1.1:** Spawn rf-qa to verify Phase 1 discovery outputs

- [ ] Spawn the rf-qa subagent in a single Agent tool call (subagent_type: "rf-qa", mode: "bypassPermissions") with the prompt below; the subagent MUST verify the 5 discovery files written in Phase 1 Steps 1.3, 1.4, 1.6, 1.7, 1.8 plus the PRE-state verify-sync capture from Step 1.5, and write its report to `.dev/tasks/to-do/TASK-RF-20260518-cliEval-P1-pty-isolation-gates/phase-outputs/reviews/PG-1-rf-qa-report.md`. The prompt is:

> ```
> QA_MODE: task-integrity
> fix_authorization: false
>
> **ADVERSARIAL STANCE:** Assume the work contains errors. Your job is to find what was missed, not confirm everything is fine. Verify every claim exhaustively. A verdict of 0 issues requires evidence you thoroughly checked.
>
> TASK FILE: .dev/tasks/to-do/TASK-RF-20260518-cliEval-P1-pty-isolation-gates/TASK-RF-20260518-cliEval-P1-pty-isolation-gates.md
> SCOPE: Phase 1 (Pre-Implementation Discovery) ONLY — Steps 1.1 through 1.8.
> INPUTS TO VERIFY:
>   - phase-outputs/discovery/01-isolation-layers-api.md
>   - phase-outputs/discovery/02-install-hooks-contract.md
>   - phase-outputs/discovery/03-pexpect-acceptability.md
>   - phase-outputs/discovery/04-ptytest-license-and-sha.md
>   - phase-outputs/discovery/05-prompt-ready-heuristic.md
>   - phase-outputs/test-results/00-verify-sync-PRE.txt
>
> ESCALATION — CRITICAL OVERRIDE: You have NO team context. Do NOT use SendMessage, TaskCreate, TaskUpdate, or TaskList. Return your verdict and report file path as your final output.
>
> Checklist (verify each — ALL findings must be resolved regardless of severity per zero-trust QA):
> 1. Discovery file 01: Does the cited line range of IsolationLayers verify against current src/superclaude/cli/sprint/executor.py? Use Read tool to re-verify, do not trust the discovery file.
> 2. Discovery file 02: Does the install_hooks deployed-script count match the BUILD_REQUEST AC-P1.2 "9 hook scripts" claim? If different, is the drift flagged in the file?
> 3. Discovery file 03: Is the pexpect decision (ACCEPTABLE / CONDITIONAL / DEFERRED-TO-VENDOR) supported by the captured `uv pip list` output and pyproject.toml content?
> 4. Discovery file 04: Is the upstream MIT LICENSE text verbatim and the fork SHA recorded (or marked FORK_SHA_TBD_VIA_GIT_CLONE_IN_PHASE_2 if WebFetch was unavailable)?
> 5. Discovery file 05: Does the prompt-ready heuristic decision specify both a primary regex AND a fallback idle-timeout? Are unresolved gaps flagged as Open Questions?
> 6. PRE-state verify-sync: Exit code is 0? If not, is the blocker flagged in Phase 1 Findings?
>
> OUTPUT FILE: phase-outputs/reviews/PG-1-rf-qa-report.md
> Write the file IMMEDIATELY with a header, then append findings incrementally.
>
> Conclude with: VERDICT: PASS or FAIL, with severity-rated issues if FAIL (CRITICAL / IMPORTANT / MINOR).
> ```

After the subagent returns, read `phase-outputs/reviews/PG-1-rf-qa-report.md` and check the final VERDICT. If PASS, proceed to Phase 2. If FAIL, proceed to Step PG-1.2 fix cycle. Once done, mark this item as complete.

**Step PG-1.2:** Conditional fix cycle for PG-1 (L5 Conditional-Action)

- [ ] If the PG-1 rf-qa report VERDICT is PASS, write a single-line file `.dev/tasks/to-do/TASK-RF-20260518-cliEval-P1-pty-isolation-gates/phase-outputs/plans/PG-1-fix-plan.md` containing only `PG-1: PASS on first attempt — no fix cycle needed.` and mark this item complete and proceed to Phase 2. If the PG-1 VERDICT is FAIL, write the file `.dev/tasks/to-do/TASK-RF-20260518-cliEval-P1-pty-isolation-gates/phase-outputs/plans/PG-1-fix-plan.md` containing (a) the cycle number (start at 1), (b) the verbatim list of FAIL findings extracted from the rf-qa report, (c) the per-finding remediation action (which discovery file to update, what to change), then re-execute the affected discovery items (only the items that PG-1 flagged), then re-spawn the rf-qa subagent for a fresh PG-1 verification using the exact same prompt as Step PG-1.1 but writing to `phase-outputs/reviews/PG-1-rf-qa-report-cycle-2.md`. Apply the **Retry Monotonicity Protocol** per rf-task-builder Critical Rule 14: BEFORE the second cycle's verdict is acted on, compare the cycle-2 PASS set against cycle-1's PASS set — if any previously-PASS item is now FAIL, HALT and emit the byte-exact halt-message `Regression detected on Item X.Y — previously PASS at cycle N, now FAIL. Halt overrides monotonicity check.` to `phase-outputs/plans/PG-1-fix-plan.md` and surface the regression in the Open Questions section. Then, if no regression, compare `|F_2|` to `|F_1|` — if `|F_2| >= |F_1|`, HALT and emit the byte-exact halt-message `[HALT-MONOTONICITY] |F|=<n>` to the same file. If neither halt fires AND cycle-2 verdict is FAIL, run cycle-3 (max 3 cycles total per task-integrity gate type). After cycle-3 FAIL or any halt, surface in Open Questions and proceed to Phase 2 only if the user explicitly authorizes (otherwise mark the task BLOCKED). Each gate keeps its OWN monotonicity history per the protocol — PG-1's F_n is independent from PG-2's F_n. Once done, mark this item as complete.

---

### Phase 2: Vendor ptytest Fork — `cli/eval/pty/` Implementation

**Context:** This phase implements the 6 files under `src/superclaude/cli/eval/pty/`. Each item is a B2 self-contained step. The PROVENANCE.md and LICENSE files MUST come before the code files so license compliance is in place before any vendored code lands. Per D-1, the fork posture is "fork-and-own": vendored, frozen at SHA, with PROVENANCE.md documenting deltas.

**Step 2.1:** Clone upstream ptytest and capture working SHA (L1 Discovery)

- [ ] Run the command `git clone --depth=1 https://github.com/brandon-fryslie/ptytest.git /tmp/cliEval-P1-ptytest-upstream && cd /tmp/cliEval-P1-ptytest-upstream && git rev-parse HEAD && git log -1 --format='%ci' && ls -la` from a Bash tool call with reasonable timeout, capturing the SHA from `git rev-parse HEAD` and the commit date from `git log -1 --format='%ci'` and the file listing from `ls -la`, then append the captured SHA, commit date, and file listing to `.dev/tasks/to-do/TASK-RF-20260518-cliEval-P1-pty-isolation-gates/phase-outputs/discovery/04-ptytest-license-and-sha.md` under a new `## Phase-2 Clone Resolution` subsection (overwriting any `FORK_SHA_TBD_VIA_GIT_CLONE_IN_PHASE_2` placeholder from Step 1.7), ensuring the clone is at depth=1 (we vendor source, not history). If the clone fails due to network unavailability, log the specific blocker in `### Phase 2 Findings` and mark this task BLOCKED until network is available (we cannot vendor without source). Once done, mark this item as complete.

**Step 2.2:** Create `src/superclaude/cli/eval/__init__.py` (L2 Build-from-Discovery)

- [ ] Create the file `src/superclaude/cli/eval/__init__.py` mirroring the pattern from `src/superclaude/cli/prd/__init__.py` (read it first if not already read in Phase 1) — the file MUST contain a module docstring describing the cliEval CLI sub-package, then exactly two import lines `from .commands import eval_group` and `# Note: HomeIsolation, capability_gates land in P1; other components in P2/P3`, then `__all__ = ["eval_group"]`. The file MUST be ≤15 lines total. Ensure no functions or runtime code beyond imports + __all__, no fabricated exports, and the docstring exactly mentions Phase 1 scope ("Phase 1: vendored pty/, HomeIsolation, capability gates, eval doctor subcommand. Phase 2/3/4 add loader, models, expect, runner, orchestrator, reporter."). If unable to create the file due to filesystem issues, log the specific blocker using the templated format in the `### Phase 2 Findings` section of the `## Task Log / Notes`, then mark this item complete. Once done, mark this item as complete.

**Step 2.3:** Create `src/superclaude/cli/eval/pty/__init__.py` (L2 Build-from-Discovery)

- [ ] Create the file `src/superclaude/cli/eval/pty/__init__.py` containing a module docstring describing the vendored ptytest fork (one sentence: "Vendored fork of brandon-fryslie/ptytest. See PROVENANCE.md for fork SHA and diff list."), then `from .driver import PtyDriver` and `from .stream import strip_ansi, line_buffer`, then `__all__ = ["PtyDriver", "strip_ansi", "line_buffer"]`. The file MUST be ≤10 lines total. Ensure no runtime code beyond imports + __all__, and no fabricated symbol names — `strip_ansi` and `line_buffer` are exports from `stream.py` written in Step 2.5. If unable to create the file, log the specific blocker in `### Phase 2 Findings`, then mark this item complete. Once done, mark this item as complete.

**Step 2.4:** Create `src/superclaude/cli/eval/pty/driver.py` — `PtyDriver` class (L2 Build-from-Discovery)

- [ ] Read the upstream `/tmp/cliEval-P1-ptytest-upstream/ptytest/__init__.py` (or the `PtySession` class wherever upstream places it; use `grep -rn "class PtySession" /tmp/cliEval-P1-ptytest-upstream` to find it) and adapt it into the new file `src/superclaude/cli/eval/pty/driver.py` exporting the `PtyDriver` class (renamed from upstream `PtySession`), preserving the core `pexpect.spawn` mechanics intact, REMOVING any pytest-fixture autoloader / `@pytest.fixture` decorator / `conftest.py`-integration code, ADDING two new methods `expect_prompt_ready(self, timeout: int = 30) -> bool` (uses the primary regex heuristic + fallback idle-timeout decided in Phase 1 Step 1.8 — encode both heuristics; return True if matched within timeout, False on timeout) and `inject_prompt(self, text: str) -> None` (writes `text + "\r\n"` to stdin and flushes), TIGHTENING the pexpect dependency assumption to `>=4.9` (add an `import pexpect; assert pexpect.__version__ >= "4.9"` guard at module import or at PtyDriver.__init__), and APPLYING aggressive ANSI strip via the `strip_ansi` helper from `stream.py` (Step 2.5) on all bytes read from the child. The class MUST expose at minimum: `spawn(self, cmd: str, env: dict[str, str]) -> "PtyDriver"`, `read_until(self, pattern: str | re.Pattern, timeout: int) -> str`, `terminate(self) -> int` (return exit code), plus the two new methods above and `expect_prompt_ready`/`inject_prompt`. Total file ≤200 LOC (per design-spec §17 "~150 LOC adapted" budget plus ~50 LOC overhead for the new methods). Ensure every method has a docstring, no fabricated upstream code is preserved beyond what `/tmp/cliEval-P1-ptytest-upstream` actually contains, and the file ends with a comment `# Provenance: see PROVENANCE.md for fork SHA and full diff list.`. If the upstream source cannot be located in `/tmp/cliEval-P1-ptytest-upstream`, log the blocker in `### Phase 2 Findings`. Once done, mark this item as complete.

**Step 2.5:** Create `src/superclaude/cli/eval/pty/stream.py` — ANSI strip + line buffering (L2 Build-from-Discovery)

- [ ] Read the upstream `/tmp/cliEval-P1-ptytest-upstream/ptytest/_stream.py` (or equivalent stream module; use `grep -rn "def.*ansi\|def.*strip" /tmp/cliEval-P1-ptytest-upstream` to locate) and adapt it into the new file `src/superclaude/cli/eval/pty/stream.py` exporting two top-level functions `strip_ansi(text: str | bytes) -> str` (aggressive ANSI escape sequence stripping using a comprehensive regex covering CSI/OSC/single-character escapes — be more aggressive than upstream because Claude Code emits rich ANSI) and `line_buffer(stream_iter: Iterable[bytes]) -> Iterator[str]` (yields complete lines from a byte iterator, handling partial-line buffering across reads), preserving upstream semantics where it overlaps but tightening the ANSI regex per design-spec §13's "Apply ANSI-strip aggressively" delta. Total file ≤100 LOC. Each function must have a docstring with at least one example input/output. Ensure no fabricated upstream behavior, no imports beyond stdlib (`re`, `typing`), and the file ends with `# Provenance: see PROVENANCE.md for fork SHA and full diff list.`. If unable to locate the upstream stream module, log the blocker in `### Phase 2 Findings` and write a from-scratch minimal implementation that satisfies the two function signatures and document the from-scratch divergence in PROVENANCE.md Step 2.6. Once done, mark this item as complete.

**Step 2.6:** Create `src/superclaude/cli/eval/pty/LICENSE` — upstream MIT verbatim (L2 Build-from-Discovery)

- [ ] Copy the upstream LICENSE text byte-for-byte from `/tmp/cliEval-P1-ptytest-upstream/LICENSE` (or from the WebFetch capture in `phase-outputs/discovery/04-ptytest-license-and-sha.md` if the clone is unavailable) into the new file `src/superclaude/cli/eval/pty/LICENSE`, ensuring (a) the file content is identical to upstream (no IronClaude additions, no reformatting, no whitespace changes — verify with `diff /tmp/cliEval-P1-ptytest-upstream/LICENSE src/superclaude/cli/eval/pty/LICENSE` and confirm zero diff output), (b) the SPDX identifier is MIT (matching Phase 1 Step 1.7 decision), (c) the copyright holder line names the upstream author (brandon-fryslie or equivalent — do NOT alter). This file is the license-compliance artifact; license compliance MUST be in place BEFORE the vendored code in driver.py and stream.py lands per upstream MIT license terms. If upstream LICENSE is not available, log the blocker in `### Phase 2 Findings` and mark the task BLOCKED — we cannot legally vendor without the LICENSE. Once done, mark this item as complete.

**Step 2.7:** Create `src/superclaude/cli/eval/pty/PROVENANCE.md` (L2 Build-from-Discovery — AC-P1.5)

- [ ] Create the file `src/superclaude/cli/eval/pty/PROVENANCE.md` containing (a) section `## Upstream` with the URL `https://github.com/brandon-fryslie/ptytest`, the verbatim fork SHA from Phase 2 Step 2.1 (or Phase 1 Step 1.7 if Step 2.1 was deferred), the commit date, and the SPDX MIT identifier, (b) section `## What we changed` with a bulleted list documenting ALL SIX deltas per BUILD_REQUEST AC-P1.5: (1) "Renamed `PtySession` → `PtyDriver` to avoid pytest-fixture connotation and clarify non-pytest usage", (2) "Removed pytest-plugin entry-point and any `@pytest.fixture`/conftest autoloader code (we don't need fixture autoloading)", (3) "Added `expect_prompt_ready(timeout=)` method using the primary regex `[PRIMARY_REGEX_FROM_STEP_1.8]` with fallback idle-timeout heuristic per Phase 1 prompt-ready decision", (4) "Added `inject_prompt(text)` method that wraps stdin writes with CR-LF + flush for Claude Code idioms", (5) "Tightened dependency requirement to `pexpect>=4.9` (upstream did not pin tightly)", (6) "Applied aggressive ANSI strip in `stream.strip_ansi` — Claude Code emits rich ANSI; eval assertions need plain text", (c) section `## What we did NOT change` listing: "Core pexpect.spawn mechanics", "Docker-isolation mode (kept available, unused)", "Original test suite (vendored as `tests/cli/test_eval/test_pty_vendor.py`)", (d) section `## Resync policy` documenting: "Frozen at SHA `[SHA]`; quarterly review of upstream pexpect releases; on resync: pull upstream, three-way merge our deltas, re-run vendored tests", (e) section `## License compliance` documenting that `cli/eval/pty/LICENSE` reproduces upstream MIT verbatim and that this satisfies MIT redistribution terms. Total file ≤80 lines. Verify by re-reading the file and confirming all SIX deltas from AC-P1.5 are present and named. If unable to write the file or the SHA from Step 2.1 is missing, log the blocker in `### Phase 2 Findings`, then mark this item complete. Once done, mark this item as complete.

---

#### PG-2: Phase-Gate QA — Vendored ptytest Verification

**Context:** Verifies Phase 2 produced a legally-clean, structurally-correct vendored fork before any test suite or downstream code depends on it. Applies the full Retry Monotonicity Protocol from rf-task-builder Critical Rule 14 (independent PG-2 F_n history; regression check FIRST then monotonicity halt).

**Step PG-2.1:** Spawn rf-qa to verify Phase 2 vendoring outputs

- [ ] Spawn the rf-qa subagent in a single Agent tool call (subagent_type: "rf-qa", mode: "bypassPermissions") with the prompt below; the subagent MUST verify the 6 files written in Phase 2 Steps 2.2 through 2.7, and write its report to `phase-outputs/reviews/PG-2-rf-qa-report.md`. The prompt is:

> ```
> QA_MODE: task-integrity
> fix_authorization: false
>
> **ADVERSARIAL STANCE:** Assume the work contains errors. Your job is to find what was missed, not confirm everything is fine. Verify every claim exhaustively. A verdict of 0 issues requires evidence you thoroughly checked.
>
> TASK FILE: .dev/tasks/to-do/TASK-RF-20260518-cliEval-P1-pty-isolation-gates/TASK-RF-20260518-cliEval-P1-pty-isolation-gates.md
> SCOPE: Phase 2 (Vendor ptytest Fork) ONLY — Steps 2.1 through 2.7.
> INPUTS TO VERIFY (read each with Read tool — do not trust the task file's prose):
>   - src/superclaude/cli/eval/__init__.py
>   - src/superclaude/cli/eval/pty/__init__.py
>   - src/superclaude/cli/eval/pty/driver.py
>   - src/superclaude/cli/eval/pty/stream.py
>   - src/superclaude/cli/eval/pty/LICENSE
>   - src/superclaude/cli/eval/pty/PROVENANCE.md
>
> ESCALATION — CRITICAL OVERRIDE: You have NO team context. Do NOT use SendMessage. Return your verdict and report file path as your final output.
>
> Checklist (ALL findings must be resolved per zero-trust QA):
> 1. LICENSE: byte-for-byte verbatim from upstream? Run `diff` if /tmp/cliEval-P1-ptytest-upstream/LICENSE is reachable, else compare against discovery file 04.
> 2. PROVENANCE.md: Does it document ALL SIX deltas from BUILD_REQUEST AC-P1.5? (PtySession→PtyDriver rename, pytest-fixture removed, expect_prompt_ready added, inject_prompt added, pexpect>=4.9 tightened, aggressive ANSI strip applied)
> 3. driver.py: Does PtyDriver expose spawn(), expect_prompt_ready(), inject_prompt(), read_until(), terminate()? Does it implement the prompt-ready heuristic per Phase 1 Step 1.8 decision?
> 4. stream.py: Does it export strip_ansi() and line_buffer()? Is the ANSI regex more aggressive than a minimal CSI-only stripper?
> 5. __init__.py files: Do they export only the documented symbols? No fabricated exports?
> 6. driver.py and stream.py: Total LOC within budget (driver.py ≤200, stream.py ≤100)?
>
> OUTPUT FILE: phase-outputs/reviews/PG-2-rf-qa-report.md
> Write the file IMMEDIATELY with a header, then append findings incrementally.
>
> Conclude with: VERDICT: PASS or FAIL with severity-rated issues.
> ```

After the subagent returns, read `phase-outputs/reviews/PG-2-rf-qa-report.md` and check the final VERDICT. If PASS, proceed to Phase 3. If FAIL, proceed to Step PG-2.2 fix cycle. Once done, mark this item as complete.

**Step PG-2.2:** Conditional fix cycle for PG-2 (L5 Conditional-Action)

- [ ] If PG-2 VERDICT is PASS, write a single-line file `phase-outputs/plans/PG-2-fix-plan.md` containing only `PG-2: PASS on first attempt — no fix cycle needed.` and proceed to Phase 3. If PG-2 VERDICT is FAIL, write `phase-outputs/plans/PG-2-fix-plan.md` with (a) the cycle number, (b) the verbatim FAIL findings, (c) per-finding remediation actions naming the specific Phase 2 file to update and the exact change required, then re-execute the affected Phase 2 items only, then re-spawn rf-qa with the same Step PG-2.1 prompt writing to `phase-outputs/reviews/PG-2-rf-qa-report-cycle-2.md`. Apply the **Retry Monotonicity Protocol** (PG-2's F_n history is independent from PG-1's): BEFORE the cycle-2 verdict is acted on, run the regression check FIRST — if any previously-PASS item from cycle-1 is now FAIL, HALT and emit `Regression detected on Item X.Y — previously PASS at cycle N, now FAIL. Halt overrides monotonicity check.` to the fix-plan file and surface in Open Questions. If no regression, run the monotonicity check — if `|F_2| >= |F_1|`, HALT and emit `[HALT-MONOTONICITY] |F|=<n>` to the fix-plan file. Max 3 cycles total; after cycle-3 FAIL or any halt, mark the task BLOCKED. Once done, mark this item as complete.

---

### Phase 3: HomeIsolation Implementation — `cli/eval/isolation.py`

**Context:** This phase implements `HomeIsolation` per D-3 (compose `IsolationLayers`, do not extend) and design-spec §7. Each item is B2 self-contained.

**Step 3.1:** Create `src/superclaude/cli/eval/config.py` — `EvalConfig` dataclass (L2 Build-from-Discovery)

- [ ] Create the file `src/superclaude/cli/eval/config.py` containing a `@dataclass` named `EvalConfig` exposing the following fields per design-spec §3 and §7: `eval_runs_root: Path` (default `Path(".dev/eval-runs")`), `home_root_template: str` (default `"eval-runs/{iso_date}/{run_id}"`), `default_parallel: int` (default `8`), `max_parallel: int` (default `15`), `per_eval_timeout_sec: int` (default `120`), `default_capture_tty: bool` (default `True`), `default_keep_home_on_success: bool` (default `False`), `claude_binary: str` (default `"claude"`), `xdg_overrides: tuple[str, ...]` (default `("XDG_CONFIG_HOME", "XDG_DATA_HOME", "XDG_CACHE_HOME", "XDG_STATE_HOME")`), `env_passthrough: tuple[str, ...]` (default `("PATH", "USER", "TERM", "LANG", "CI")` per design-spec §7 env() return contract). The dataclass MUST be `@dataclass(frozen=True)` and have a docstring describing each field. Total file ≤80 LOC. Ensure all default values are sourced from design-spec §7 (env passthrough) and §11 (binary names) — no fabricated defaults. If a default does not appear in the design-spec, mark it with an inline comment `# Default chosen per orchestrator discretion — not specified in design-spec`. If unable to create the file, log the blocker in `### Phase 3 Findings`. Once done, mark this item as complete.

**Step 3.2:** Create `src/superclaude/cli/eval/isolation.py` — `HomeIsolation` class skeleton + hard guard (L2 Build-from-Discovery — AC-P1.6)

- [ ] Read `phase-outputs/discovery/01-isolation-layers-api.md` to confirm the IsolationLayers composition target's verified-current line range and field names, then read `phase-outputs/discovery/02-install-hooks-contract.md` to confirm the install_hooks function signature and the deployed-script count, then create the file `src/superclaude/cli/eval/isolation.py` containing the `HomeIsolation` class per design-spec §7 interface signature. The class signature MUST be `@dataclass(frozen=True) class HomeIsolation` with fields: `eval_id: str`, `home_root: Path`, `session_id: str`, `time_offset_sec: int = 0`, `isolation_layers: "IsolationLayers"` (composed reference; constructor argument). The class MUST expose methods: `setup(self) -> None` (creates HOME/.claude/{hooks,state,logs}; deploys hook scripts via install_hooks; writes settings.json; seeds state files), `env(self) -> dict[str, str]` (returns env overlay: HOME, XDG_*, CLAUDE_SESSION_ID, CLAUDE_FAKE_TIME_OFFSET if non-zero, plus passthrough of PATH/USER/TERM/LANG/CI, plus IsolationLayers.env_vars merged in), `teardown(self, keep: bool) -> None` (rm-rf home_root unless keep=True), `state_path(self, suffix: str) -> Path` (resolves {session_id}/{project_key} template placeholders). The `setup()` method MUST start with the **HARD GUARD** per AC-P1.6: `if not (str(self.home_root).startswith("/tmp/eval-runs/") or str(self.home_root).startswith(".dev/eval-runs/") or "/eval-runs/" in str(self.home_root.resolve())): raise RuntimeError(f"HomeIsolation refuses to operate on home_root={self.home_root} — must be under /tmp/eval-runs/ or .dev/eval-runs/ (foot-gun guard per AC-P1.6)")`. The guard MUST run BEFORE any filesystem operation. The class file MUST include a module docstring cross-referencing `src/superclaude/cli/sprint/executor.py:107-182` `IsolationLayers` as the composition target per D-3. Total file ≤150 LOC (design-spec §17 budget is ~120 LOC; +30 LOC for guard + docstrings). Ensure no fabricated method names, no inheritance from IsolationLayers (composition only), and no modification to sprint/executor.py. If unable to create the file, log the blocker in `### Phase 3 Findings`. Once done, mark this item as complete.

**Step 3.3:** Implement `HomeIsolation.setup()` body — hook deployment + state seeding (L2 Build-from-Discovery — AC-P1.2)

- [ ] Edit `src/superclaude/cli/eval/isolation.py` to implement the `setup()` method body: AFTER the hard guard, the method MUST (1) create `self.home_root / ".claude" / "hooks"`, `self.home_root / ".claude" / "state"`, `self.home_root / ".claude" / "logs"` with `Path.mkdir(parents=True, exist_ok=True)`, (2) call `install_hooks(target_path=self.home_root / ".claude", force=True)` (imported via `from superclaude.cli.install_hooks import install_hooks`) — this deploys all hook scripts per `phase-outputs/discovery/02-install-hooks-contract.md`, writes `~/.claude/settings.json`, and copies seed files, (3) seed any state files passed in via a (deferred) `seed_state` parameter — for Phase 1, this is a no-op stub with a `# TODO(P2): wire seed_state from EvalSpec` comment; Phase 2 will wire it. The setup() method MUST be idempotent — calling it twice on the same home_root must not error (the hard guard runs both times; `mkdir(exist_ok=True)` is idempotent; `install_hooks(force=True)` is idempotent per its design contract). Ensure all paths use `pathlib.Path`, no f-string path concatenation beyond joins, and no hardcoded `/tmp/` or `/home/` paths outside the guard. If install_hooks raises an exception, propagate it (do NOT silently swallow — failed setup is a failed eval). Once done, mark this item as complete.

**Step 3.4:** Implement `HomeIsolation.env()` and `teardown()` bodies (L2 Build-from-Discovery — AC-P1.2)

- [ ] Edit `src/superclaude/cli/eval/isolation.py` to implement the `env()` method body: build and return a dict with HOME=str(self.home_root), XDG_CONFIG_HOME=str(self.home_root/'.config'), XDG_DATA_HOME=str(self.home_root/'.local/share'), XDG_CACHE_HOME=str(self.home_root/'.cache'), XDG_STATE_HOME=str(self.home_root/'.local/state'), CLAUDE_SESSION_ID=self.session_id, plus CLAUDE_FAKE_TIME_OFFSET=str(self.time_offset_sec) ONLY if self.time_offset_sec != 0, plus passthrough copies of os.environ for keys PATH, USER, TERM, LANG, CI (skip if absent in parent env), plus the env_vars from self.isolation_layers merged in (the merged dict CANNOT overwrite the HOME or XDG_* keys we just set — design-spec §7 mandates HOME isolation is the 5th layer that wins). Also implement the `teardown(self, keep: bool) -> None` method body: if keep is True, return without touching the filesystem; if keep is False, run `shutil.rmtree(self.home_root, ignore_errors=False)` per design-spec §7 key correctness invariant 3 ("Teardown is best-effort; failure to rm -rf is logged but does not affect eval result") — wrap in try/except, log a warning to stderr on failure, but never raise. Also implement `state_path(self, suffix: str) -> Path`: replace `{session_id}` and `{project_key}` placeholders in suffix using self.session_id and a derived project_key (use a stable hash of eval_id for project_key), then return `self.home_root / ".claude" / suffix.format(session_id=self.session_id, project_key=stable_hash)`. Ensure no fabricated env-var names beyond design-spec §7 contract, the passthrough list matches Step 3.1's `env_passthrough` default, and the merged isolation_layers env_vars do not overwrite HOME. Once done, mark this item as complete.

---

#### PG-3: Phase-Gate QA — HomeIsolation Verification

**Step PG-3.1:** Spawn rf-qa to verify Phase 3 HomeIsolation implementation

- [ ] Spawn the rf-qa subagent in a single Agent tool call (subagent_type: "rf-qa", mode: "bypassPermissions") with the prompt below; the subagent MUST verify the 2 files written in Phase 3 Steps 3.1 through 3.4, and write its report to `phase-outputs/reviews/PG-3-rf-qa-report.md`. The prompt is:

> ```
> QA_MODE: task-integrity
> fix_authorization: false
>
> **ADVERSARIAL STANCE:** Assume the work contains errors. Your job is to find what was missed. Verify every claim exhaustively.
>
> TASK FILE: .dev/tasks/to-do/TASK-RF-20260518-cliEval-P1-pty-isolation-gates/TASK-RF-20260518-cliEval-P1-pty-isolation-gates.md
> SCOPE: Phase 3 (HomeIsolation) ONLY — Steps 3.1 through 3.4.
> INPUTS TO VERIFY (read each with Read tool):
>   - src/superclaude/cli/eval/config.py
>   - src/superclaude/cli/eval/isolation.py
>   - src/superclaude/cli/sprint/executor.py:100-185 (verify NOT MODIFIED — diff against git HEAD)
>
> ESCALATION — CRITICAL OVERRIDE: You have NO team context. Do NOT use SendMessage.
>
> Checklist (ALL findings resolved per zero-trust QA):
> 1. AC-P1.6 hard guard: Does HomeIsolation.setup() raise RuntimeError when home_root is outside /tmp/eval-runs/ or .dev/eval-runs/? Run `git diff src/superclaude/cli/sprint/executor.py` to verify zero changes (D-3 composition mandate).
> 2. AC-P1.2 contract: Does env() return dict with HOME, XDG_*, CLAUDE_SESSION_ID, plus passthrough of PATH/USER/TERM/LANG/CI? Does setup() deploy hooks via install_hooks? Does teardown(keep=False) rm-rf?
> 3. Composition: Does HomeIsolation take an IsolationLayers as constructor argument (composition, not inheritance)? Does env() MERGE isolation_layers.env_vars WITHOUT overwriting HOME?
> 4. Idempotence: Would calling setup() twice on the same home_root succeed without error? (Read mkdir/install_hooks usage — they must be idempotent.)
> 5. Frozen dataclass: Is HomeIsolation `@dataclass(frozen=True)` per design-spec §7?
> 6. LOC budgets: isolation.py ≤150 LOC, config.py ≤80 LOC?
>
> OUTPUT FILE: phase-outputs/reviews/PG-3-rf-qa-report.md
> Write incrementally with header first, then findings.
> Conclude with: VERDICT: PASS or FAIL with severity-rated issues.
> ```

After the subagent returns, read the report and check VERDICT. PASS → Phase 4. FAIL → PG-3.2. Once done, mark this item as complete.

**Step PG-3.2:** Conditional fix cycle for PG-3 (L5 Conditional-Action)

- [ ] If PG-3 VERDICT is PASS, write `phase-outputs/plans/PG-3-fix-plan.md` containing only `PG-3: PASS on first attempt — no fix cycle needed.` and proceed to Phase 4. If PG-3 VERDICT is FAIL, write the fix plan with cycle number + verbatim FAIL findings + remediation actions, then re-execute the affected Phase 3 items only, then re-spawn rf-qa with the same Step PG-3.1 prompt writing to `phase-outputs/reviews/PG-3-rf-qa-report-cycle-2.md`. Apply the **Retry Monotonicity Protocol** (PG-3 independent F_n history): regression check FIRST (HALT message `Regression detected on Item X.Y — previously PASS at cycle N, now FAIL. Halt overrides monotonicity check.`), then monotonicity check (HALT message `[HALT-MONOTONICITY] |F|=<n>` when `|F_2| >= |F_1|`). Max 3 cycles; after cycle-3 FAIL or halt, mark BLOCKED. Once done, mark this item as complete.

---

### Phase 4: Capability Gates + `eval doctor` Click Subcommand

**Context:** This phase implements `capability_gates.py` and `commands.py` (doctor-only). All other subcommands (`eval run`, `eval list`, `eval describe`) are deferred to P2/P3 per BUILD_REQUEST "Out of scope". Each item is B2 self-contained.

**Step 4.1:** Create `src/superclaude/cli/eval/capability_gates.py` — `Capability` dataclass + registry (L2 Build-from-Discovery — AC-P1.1)

- [ ] Create the file `src/superclaude/cli/eval/capability_gates.py` containing (a) a `@dataclass` `Capability` with fields `name: str`, `check: Callable[[], bool]`, `failure_mode: Literal["hard", "skip", "xfail"]`, `skip_flag: Optional[str] = None`, `description: str = ""` per design-spec §11 interface signature, (b) helper `shutil.which`-based binary checks `_which_check(binary: str) -> Callable[[], bool]` that returns a closure `lambda: shutil.which(binary) is not None`, (c) helper `_mcp_server_reachable(server: str) -> Callable[[], bool]` that returns a closure attempting to import a placeholder MCP probe (for Phase 1, this is a STUB that returns False unless `os.environ.get(f"MCP_{server.upper().replace('-', '_')}_AVAILABLE") == "1"` — this lets tests parameterize without spinning up real servers; a `# TODO(P3): wire to real MCP stdio probe` comment is required), (d) the `CAPABILITIES` registry list containing exactly the 7 entries per design-spec §11: `Capability("binary.claude", _which_check("claude"), "hard")`, `Capability("binary.make", _which_check("make"), "hard")`, `Capability("binary.jq", _which_check("jq"), "hard")`, `Capability("binary.git", _which_check("git"), "hard")`, `Capability("mcp_server.auggie", _mcp_server_reachable("auggie"), "skip", "--no-mcp")`, `Capability("mcp_server.auggie-mcp", _mcp_server_reachable("auggie-mcp"), "skip", "--no-mcp")`, `Capability("mcp_server.airis-mcp-gateway", _mcp_server_reachable("airis-mcp-gateway"), "skip", "--no-mcp")`, (e) a `@dataclass` `CapabilityReport` with `entries: list[tuple[Capability, bool]]`, `hard_failed: list[str]`, `skipped: list[str]`, and methods `is_ready(self) -> bool` (returns True iff hard_failed is empty), `to_text(self) -> str` (renders the green-checklist format per design-spec §11 "eval doctor output" example), (f) the function `check_all(skip_flags: set[str] | None = None) -> CapabilityReport` that iterates CAPABILITIES, runs each check, classifies hard failures vs skips, returns the populated CapabilityReport. Total file ≤120 LOC (design-spec §17 budget is ~80 LOC + 40 LOC for the report rendering). Ensure no fabricated binary names beyond the 4 + 3 from design-spec, the rendering format matches design-spec §11 "eval doctor output" with checkmark/cross/yellow-circle Unicode chars (✅ for PASS, ❌ for FAIL, ⚠️ for SKIP). If unable to create the file, log the blocker in `### Phase 4 Findings`. Once done, mark this item as complete.

**Step 4.2:** Create `src/superclaude/cli/eval/commands.py` — Click group + `doctor` subcommand only (L2 Build-from-Discovery — AC-P1.1)

- [ ] Create the file `src/superclaude/cli/eval/commands.py` containing (a) a Click group `@click.group() def eval_group(): pass` with help text `"Real-world eval harness for IronClaude hooks. Phase 1: doctor only. Phase 2/3 add list/describe/run."`, (b) a Click command `@eval_group.command("doctor") @click.option("--no-mcp", is_flag=True, default=False, help="Skip MCP server capability checks") def doctor(no_mcp: bool)` that invokes `capability_gates.check_all(skip_flags={"--no-mcp"} if no_mcp else set())`, prints the rendered `report.to_text()` to stdout via click.echo, then exits with code 0 if `report.is_ready()` is True, exit code 2 if any hard requirement failed (per design-spec §4 exit codes and AC-P1.1). The file MUST import only stdlib + click + `from .capability_gates import check_all`. The file MUST NOT define any other subcommand stubs (no `eval_group.command("run")`, no `list`, no `describe`) — those land in P2/P3 per BUILD_REQUEST "Out of scope for THIS task". The file MUST end with a comment `# Phase 1: doctor only. Subcommands list/describe/run land in P2; run lands in P3.`. Total file ≤80 LOC (design-spec §17 budget is ~50 LOC + 30 LOC for click decorator overhead). Ensure no fabricated subcommand stubs, exit codes match AC-P1.1 (0 on ready, 2 on hard fail), and click is imported (a known existing project dependency per pyproject.toml — verify via Read of pyproject.toml if uncertain). If unable to create the file, log the blocker in `### Phase 4 Findings`. Once done, mark this item as complete.

**Step 4.3:** Smoke-test `superclaude eval doctor` invocation (L3 Test/Execute — AC-P1.1)

- [ ] Run the command `uv run superclaude eval doctor 2>&1; echo "EXIT_CODE=$?"` from the repository root using Bash tool and capture stdout/stderr/exit_code, but note that this requires `eval_group` to be wired into `cli/main.py` — which is EXPLICITLY out-of-scope per BUILD_REQUEST "Out of scope for THIS task: Wiring into `cli/main.py` (P4 only)". Therefore, INSTEAD run a localized invocation that does NOT require main.py wiring: use Bash to run `cd /config/workspace/IronClaude && uv run python -c "from superclaude.cli.eval.commands import eval_group; from click.testing import CliRunner; r = CliRunner().invoke(eval_group, ['doctor']); print(r.output); print(f'EXIT_CODE={r.exit_code}')"` and capture the output to `phase-outputs/test-results/01-doctor-smoke-test.txt` with a header line `# eval doctor smoke test (P4 main.py wiring deferred — using Click CliRunner directly)\n# Date: [today]\n---\n`. Verify the captured output contains (a) at least one ✅ or ❌ glyph (the rendering is alive), (b) one of the 4 binary names from CAPABILITIES (claude, make, jq, git) (the registry is loaded), (c) an EXIT_CODE line at the bottom showing 0 or 2 (per AC-P1.1). If EXIT_CODE is non-0 AND non-2, append a FAILURE finding to `### Phase 4 Findings`. If the import fails (e.g., due to a typo in capability_gates.py or commands.py), capture the full traceback and log the blocker. Once done, mark this item as complete.

---

#### PG-4: Phase-Gate QA — Capability Gates + `eval doctor` Verification

**Step PG-4.1:** Spawn rf-qa to verify Phase 4 outputs

- [ ] Spawn the rf-qa subagent in a single Agent tool call (subagent_type: "rf-qa", mode: "bypassPermissions") with the prompt below; the subagent MUST verify the 2 source files written in Phase 4 plus the smoke-test capture, and write its report to `phase-outputs/reviews/PG-4-rf-qa-report.md`. The prompt is:

> ```
> QA_MODE: task-integrity
> fix_authorization: false
>
> **ADVERSARIAL STANCE:** Assume the work contains errors. Verify every claim exhaustively.
>
> TASK FILE: .dev/tasks/to-do/TASK-RF-20260518-cliEval-P1-pty-isolation-gates/TASK-RF-20260518-cliEval-P1-pty-isolation-gates.md
> SCOPE: Phase 4 (Capability Gates + eval doctor) ONLY — Steps 4.1 through 4.3.
> INPUTS TO VERIFY (read each):
>   - src/superclaude/cli/eval/capability_gates.py
>   - src/superclaude/cli/eval/commands.py
>   - phase-outputs/test-results/01-doctor-smoke-test.txt
>
> ESCALATION — CRITICAL OVERRIDE: You have NO team context. Do NOT use SendMessage.
>
> Checklist (ALL findings resolved):
> 1. AC-P1.1 registry: Does CAPABILITIES contain exactly 7 entries — 4 hard (claude/make/jq/git) + 3 skip (3 MCP servers)? Are failure_modes correct ("hard" vs "skip")?
> 2. AC-P1.1 exit codes: Does doctor() exit 0 on ready and exit 2 on hard fail? Verify by reading commands.py code, not just claims.
> 3. Scope boundary: Does commands.py contain ONLY the doctor subcommand? NO eval_group.command("run"/"list"/"describe") stubs per BUILD_REQUEST out-of-scope?
> 4. Smoke test: Did the Click CliRunner smoke test produce non-empty output with at least one glyph and an EXIT_CODE line?
> 5. MCP probe stub: Is the _mcp_server_reachable function a stub with a TODO(P3) comment? It should NOT attempt real MCP probing in Phase 1.
> 6. LOC budgets: capability_gates.py ≤120 LOC, commands.py ≤80 LOC?
>
> OUTPUT FILE: phase-outputs/reviews/PG-4-rf-qa-report.md
> Write incrementally with header first.
> Conclude with: VERDICT: PASS or FAIL.
> ```

After the subagent returns, read the report and check VERDICT. PASS → Phase 5. FAIL → PG-4.2. Once done, mark this item as complete.

**Step PG-4.2:** Conditional fix cycle for PG-4 (L5 Conditional-Action)

- [ ] If PG-4 VERDICT is PASS, write `phase-outputs/plans/PG-4-fix-plan.md` containing only `PG-4: PASS on first attempt — no fix cycle needed.` and proceed to Phase 5. If PG-4 VERDICT is FAIL, write the fix plan with cycle number + verbatim FAIL findings + remediation actions, then re-execute the affected Phase 4 items only, then re-spawn rf-qa with the same Step PG-4.1 prompt writing to `phase-outputs/reviews/PG-4-rf-qa-report-cycle-2.md`. Apply the **Retry Monotonicity Protocol** (PG-4 independent F_n history): regression check FIRST (HALT message `Regression detected on Item X.Y — previously PASS at cycle N, now FAIL. Halt overrides monotonicity check.`), then monotonicity check (HALT message `[HALT-MONOTONICITY] |F|=<n>` when `|F_2| >= |F_1|`). Max 3 cycles; after cycle-3 FAIL or halt, mark BLOCKED. Once done, mark this item as complete.

---

### Phase 5: Test Authoring — 3 pytest Test Files

**Context:** This phase authors three independent pytest test files per BUILD_REQUEST "Files to create" items 11-14. Each test file is a separate B2 self-contained step. Tests use UV per CLAUDE.md absolute rule (`uv run pytest`, never bare `pytest`).

**Step 5.1:** Create `tests/cli/test_eval/__init__.py` + `tests/cli/test_eval/test_isolation.py` (L3 Test/Execute — AC-P1.2, AC-P1.6, AC-P1.8)

- [ ] Create the empty file `tests/cli/test_eval/__init__.py` (single blank line; required so pytest discovers the package per the existing `tests/cli/` convention — verify with `ls tests/cli/` that adjacent `test_*/__init__.py` files exist as empty/blank), then create the file `tests/cli/test_eval/test_isolation.py` containing pytest test functions covering: (a) `test_setup_creates_home_root(tmp_path)` — asserts HomeIsolation(eval_id="P1-smoke", home_root=tmp_path/"eval-runs"/"test", session_id="sid", isolation_layers=IsolationLayers(...)) creates `.claude/{hooks,state,logs}` under home_root after setup() — use monkeypatch to redirect install_hooks to a no-op if real hook deployment is too slow for unit tests, (b) `test_env_returns_expected_keys(tmp_path)` — asserts env() dict contains HOME, XDG_CONFIG_HOME, XDG_DATA_HOME, XDG_CACHE_HOME, XDG_STATE_HOME, CLAUDE_SESSION_ID, and the 5 passthrough keys PATH/USER/TERM/LANG/CI (skip passthrough assertion for keys absent from os.environ), (c) `test_teardown_removes_home_root(tmp_path)` — asserts teardown(keep=False) rmtree's home_root, (d) `test_teardown_keep_preserves_home_root(tmp_path)` — asserts teardown(keep=True) leaves home_root intact, (e) `test_setup_idempotent(tmp_path)` — asserts setup() called twice does not raise, (f) `test_hard_guard_refuses_unsafe_home_root(tmp_path)` (AC-P1.6) — asserts HomeIsolation(home_root=Path("/")).setup() raises RuntimeError with the BUILD_REQUEST AC-P1.6 message substring "must be under /tmp/eval-runs/ or .dev/eval-runs/" — also test with home_root=Path("/home/user/.claude") to confirm the guard blocks real-HOME paths, (g) `test_env_does_not_overwrite_HOME_from_isolation_layers(tmp_path)` — asserts that even if isolation_layers.env_vars contained HOME (it doesn't, but defensively), env() returns HOME=home_root not the isolation_layers value. Each test MUST use pytest's `tmp_path` fixture (which yields a tmpdir under `/tmp/pytest-of-<user>/.../` — this satisfies the hard guard's `/eval-runs/` requirement ONLY if we construct `tmp_path / "eval-runs" / "test"` as home_root). The tests MUST be runnable as `uv run pytest tests/cli/test_eval/test_isolation.py -v` per AC-P1.8. Total file ≤200 LOC. Ensure each assertion has a descriptive `assert ..., "message"` failure message, no flaky time-dependent assertions, and no real network or real claude binary invocation. If unable to create the file, log the blocker in `### Phase 5 Findings`. Once done, mark this item as complete.

**Step 5.2:** Create `tests/cli/test_eval/test_capability_gates.py` (L3 Test/Execute — AC-P1.1, AC-P1.8)

- [ ] Create the file `tests/cli/test_eval/test_capability_gates.py` containing pytest test functions covering: (a) `test_capabilities_registry_count()` — asserts `len(CAPABILITIES) == 7` (4 hard + 3 skip per design-spec §11), (b) `test_capabilities_registry_names()` — asserts the registry contains exactly the 7 expected names: `binary.claude`, `binary.make`, `binary.jq`, `binary.git`, `mcp_server.auggie`, `mcp_server.auggie-mcp`, `mcp_server.airis-mcp-gateway`, (c) `test_check_all_reports_ready_when_all_hard_pass(monkeypatch)` — monkeypatch `shutil.which` to return a non-None value for the 4 hard binaries, monkeypatch `os.environ` to set MCP_AUGGIE_AVAILABLE=1 etc., assert `check_all().is_ready() == True` and `hard_failed == []`, (d) `test_check_all_reports_hard_failed_when_binary_missing(monkeypatch)` (AC-P1.1 exit 2 path) — monkeypatch `shutil.which` to return None for `make`, assert `check_all().is_ready() == False` and `"binary.make" in hard_failed`, (e) `test_check_all_marks_mcp_as_skipped_with_no_mcp_flag(monkeypatch)` — pass `skip_flags={"--no-mcp"}` and assert MCP servers appear in `skipped`, not in `hard_failed`, (f) `test_doctor_exits_0_when_ready(monkeypatch)` — use Click's CliRunner to invoke `eval_group` with `["doctor"]`, monkeypatching capability checks to all-pass, assert `result.exit_code == 0`, (g) `test_doctor_exits_2_when_hard_requirement_missing(monkeypatch)` — same but monkeypatch a hard binary to missing, assert `result.exit_code == 2` (AC-P1.1 exit 2 path), (h) `test_doctor_output_contains_glyphs(monkeypatch)` — assert the rendered output contains ✅ or ❌ glyphs. The tests MUST be runnable as `uv run pytest tests/cli/test_eval/test_capability_gates.py -v` per AC-P1.8. Total file ≤200 LOC. Ensure each missing-binary failure mode from AC-P1.1 is tested with a dedicated test, no real subprocess invocation, and the Click CliRunner pattern matches the existing convention (search for `CliRunner` in `tests/cli/` to find a reference test). If unable to create the file, log the blocker in `### Phase 5 Findings`. Once done, mark this item as complete.

**Step 5.3:** Create `tests/cli/test_eval/test_pty_vendor.py` (L3 Test/Execute — AC-P1.4, AC-P1.8)

- [ ] Locate the upstream ptytest test suite in `/tmp/cliEval-P1-ptytest-upstream/tests/` (or wherever upstream places it — use `find /tmp/cliEval-P1-ptytest-upstream -name "test_*.py" -o -name "*_test.py"` to locate), then create the file `tests/cli/test_eval/test_pty_vendor.py` that EITHER (option A) imports and re-runs the upstream test suite by copying it as a module into the test file with imports re-pointed from `ptytest.PtySession` to `superclaude.cli.eval.pty.PtyDriver` (using the PtySession→PtyDriver rename per AC-P1.5), OR (option B) embeds the upstream tests verbatim as top-level pytest functions with the same import rename, OR (option C) if upstream has no test suite at all, write a minimal test that exercises PtyDriver's core surface — `test_spawn_and_terminate_echo()` (spawn `echo hello`, read_until completion, assert exit code 0 from terminate), `test_inject_prompt_writes_crlf()` (spawn `cat -`, inject_prompt("hello"), read_until("hello\r\n"), terminate), `test_strip_ansi_removes_escapes()` (call strip_ansi directly with `"\x1b[31mred\x1b[0m"` and assert returns `"red"`), `test_line_buffer_yields_complete_lines()` (feed partial-byte iterator, assert complete lines emerge). The file MUST start with a docstring documenting which option (A/B/C) was chosen and why, citing the discovery file at `phase-outputs/discovery/04-ptytest-license-and-sha.md`. Pick option A if upstream tests exist and import cleanly; option B if they require minor adaptation; option C if no upstream tests exist. The tests MUST be runnable as `uv run pytest tests/cli/test_eval/test_pty_vendor.py -v` per AC-P1.4 + AC-P1.8. Each test that spawns a real subprocess MUST have a `@pytest.mark.timeout(30)` decorator (use the pytest-timeout plugin if present; otherwise wrap with `signal.alarm`). Total file ≤300 LOC (test suite vendoring can be larger than other test files). If upstream tests are not locatable AND option C minimal tests cannot exercise the renamed PtyDriver surface, log the blocker in `### Phase 5 Findings`. Once done, mark this item as complete.

---

#### PG-5: Phase-Gate QA — Test File Authoring Verification

**Step PG-5.1:** Spawn rf-qa to verify Phase 5 test file authoring

- [ ] Spawn the rf-qa subagent in a single Agent tool call (subagent_type: "rf-qa", mode: "bypassPermissions") with the prompt below; the subagent MUST verify the 4 files written in Phase 5 Steps 5.1 through 5.3 (including the `__init__.py`), and write its report to `phase-outputs/reviews/PG-5-rf-qa-report.md`. The prompt is:

> ```
> QA_MODE: task-integrity
> fix_authorization: false
>
> **ADVERSARIAL STANCE:** Assume the work contains errors. Verify every claim.
>
> TASK FILE: .dev/tasks/to-do/TASK-RF-20260518-cliEval-P1-pty-isolation-gates/TASK-RF-20260518-cliEval-P1-pty-isolation-gates.md
> SCOPE: Phase 5 (Test Authoring) ONLY — Steps 5.1 through 5.3.
> INPUTS TO VERIFY (read each):
>   - tests/cli/test_eval/__init__.py
>   - tests/cli/test_eval/test_isolation.py
>   - tests/cli/test_eval/test_capability_gates.py
>   - tests/cli/test_eval/test_pty_vendor.py
>
> ESCALATION — CRITICAL OVERRIDE: You have NO team context. Do NOT use SendMessage.
>
> Checklist (ALL findings resolved):
> 1. AC-P1.2 coverage in test_isolation.py: Are setup/env/teardown all covered? Is the AC-P1.6 hard guard tested with /, /home/user/.claude, and a valid /tmp/eval-runs/ path?
> 2. AC-P1.1 coverage in test_capability_gates.py: Are all 7 capabilities tested? Are exit codes 0 and 2 both covered? Are missing-binary failure modes tested per AC-P1.1?
> 3. AC-P1.4 coverage in test_pty_vendor.py: Does the file declare which option (A/B/C) was chosen and exercise PtyDriver's core surface (spawn, expect_prompt_ready, inject_prompt, terminate)?
> 4. UV invocation: Do test commands use `uv run pytest` (NOT bare `pytest` or `python -m pytest`)?
> 5. Real network / real claude binary: Are tests free of real network calls and real `claude` invocation (mocked / Click CliRunner)?
> 6. LOC budgets within reason (test_isolation ≤200, test_capability_gates ≤200, test_pty_vendor ≤300)?
>
> OUTPUT FILE: phase-outputs/reviews/PG-5-rf-qa-report.md
> Write incrementally with header first.
> Conclude with: VERDICT: PASS or FAIL with severity-rated issues.
> ```

After the subagent returns, read the report and check VERDICT. PASS → Phase 6. FAIL → PG-5.2. Once done, mark this item as complete.

**Step PG-5.2:** Conditional fix cycle for PG-5 (L5 Conditional-Action)

- [ ] If PG-5 VERDICT is PASS, write `phase-outputs/plans/PG-5-fix-plan.md` containing only `PG-5: PASS on first attempt — no fix cycle needed.` and proceed to Phase 6. If PG-5 VERDICT is FAIL, write the fix plan with cycle number + verbatim FAIL findings + remediation actions, then re-execute the affected Phase 5 items only, then re-spawn rf-qa with the same Step PG-5.1 prompt writing to `phase-outputs/reviews/PG-5-rf-qa-report-cycle-2.md`. Apply the **Retry Monotonicity Protocol** (PG-5 independent F_n history): regression check FIRST, then monotonicity check, with byte-exact halt-messages per the protocol. Max 3 cycles; after cycle-3 FAIL or halt, mark BLOCKED. Once done, mark this item as complete.

---

### Phase 6: Test Execution — Run All Tests Per AC-P1.8

**Context:** This phase executes the 3 test files authored in Phase 5 and captures results to `phase-outputs/test-results/`. Each test execution is a B2 self-contained step. The pass criterion per AC-P1.8 is that ALL three test files return 0 with all tests PASS under `uv run pytest`.

**Step 6.1:** Run `test_isolation.py` (L3 Test/Execute — AC-P1.2, AC-P1.8)

- [ ] Run the command `uv run pytest tests/cli/test_eval/test_isolation.py -v 2>&1; echo "EXIT_CODE=$?"` from the repository root using Bash tool and capture the full output to `.dev/tasks/to-do/TASK-RF-20260518-cliEval-P1-pty-isolation-gates/phase-outputs/test-results/02-test-isolation.txt` with a leading header `# uv run pytest tests/cli/test_eval/test_isolation.py -v\n# Date: [today]\n# Expected: EXIT_CODE=0, all tests PASS\n---\n`, ensuring the EXIT_CODE line is captured. Verify: (a) EXIT_CODE is 0, (b) the output contains `passed` and no `failed` or `error`, (c) all 7 tests authored in Step 5.1 appear in the output (count them). If EXIT_CODE is non-0 OR any test FAILED, append a `## Failure Triage` subsection to the capture file with the failing test names, then proceed to Phase 7 fix cycle — DO NOT silently continue (AC-P1.8 requires ALL tests pass). Once done, mark this item as complete.

**Step 6.2:** Run `test_pty_vendor.py` (L3 Test/Execute — AC-P1.4, AC-P1.8)

- [ ] Run the command `uv run pytest tests/cli/test_eval/test_pty_vendor.py -v 2>&1; echo "EXIT_CODE=$?"` from the repository root using Bash tool and capture the full output to `.dev/tasks/to-do/TASK-RF-20260518-cliEval-P1-pty-isolation-gates/phase-outputs/test-results/03-test-pty-vendor.txt` with a leading header `# uv run pytest tests/cli/test_eval/test_pty_vendor.py -v\n# Date: [today]\n# Expected: EXIT_CODE=0, all tests PASS (AC-P1.4 + AC-P1.8)\n---\n`. Verify: (a) EXIT_CODE is 0, (b) the test count matches the option (A/B/C) chosen in Step 5.3 (record the number; if option C minimal tests, expect at least 4), (c) the output contains `passed` and no `failed` or `error`, (d) AC-P1.3 surface methods (spawn, expect_prompt_ready, inject_prompt, terminate) appear in at least one test name OR are exercised by an upstream test. If a test times out (the @pytest.mark.timeout(30) decorator fired), record the timeout duration and decide whether it indicates a real PtyDriver bug or just a slow CI environment. If EXIT_CODE is non-0, append `## Failure Triage` and proceed to Phase 7 fix cycle. Once done, mark this item as complete.

**Step 6.3:** Run `test_capability_gates.py` (L3 Test/Execute — AC-P1.1, AC-P1.8)

- [ ] Run the command `uv run pytest tests/cli/test_eval/test_capability_gates.py -v 2>&1; echo "EXIT_CODE=$?"` from the repository root using Bash tool and capture the full output to `.dev/tasks/to-do/TASK-RF-20260518-cliEval-P1-pty-isolation-gates/phase-outputs/test-results/04-test-capability-gates.txt` with a leading header `# uv run pytest tests/cli/test_eval/test_capability_gates.py -v\n# Date: [today]\n# Expected: EXIT_CODE=0, all 8 tests PASS (AC-P1.1 + AC-P1.8)\n---\n`. Verify: (a) EXIT_CODE is 0, (b) all 8 tests from Step 5.2 appear in the output (count them), (c) the output contains `passed` and no `failed`. If EXIT_CODE is non-0, append `## Failure Triage` and proceed to Phase 7 fix cycle. Once done, mark this item as complete.

**Step 6.4:** Aggregate test results (L6 Aggregation)

- [ ] Read the 3 test-result files `phase-outputs/test-results/02-test-isolation.txt`, `phase-outputs/test-results/03-test-pty-vendor.txt`, `phase-outputs/test-results/04-test-capability-gates.txt` and write the aggregated summary to `.dev/tasks/to-do/TASK-RF-20260518-cliEval-P1-pty-isolation-gates/phase-outputs/reports/test-summary.md` containing (a) header with date and overall verdict (PASS if all 3 EXIT_CODE=0, FAIL otherwise), (b) a per-test-file table with columns: file path, exit code, tests-passed count, tests-failed count, duration (extract from pytest output `===== N passed in X.YYs =====` footer), (c) a `## AC Coverage` subsection mapping AC-P1.1, AC-P1.2, AC-P1.3, AC-P1.4, AC-P1.6, AC-P1.8 to specific test names that exercised them with PASS/FAIL verdict per AC, (d) a `## Issues` subsection listing any FAILED tests with their full traceback excerpts. If the overall verdict is FAIL, do NOT proceed to Phase 7 verify-sync — instead, return to Phase 5 to fix the failing tests (or the source files they exercise) and re-run only the affected test file in Phase 6. The test-failure-fix-loop is bounded by the same max-3-cycles rule as the PG fix cycles; surface persistent failures in Open Questions. Once done, mark this item as complete.

---

### Phase 7: Post-Implementation Validation — `make verify-sync` POST-state (AC-P1.7)

**Context:** This phase verifies no regression to `make verify-sync` after all P1 source files have landed. AC-P1.7 requires `make verify-sync` to still EXIT=0 after this phase lands.

**Step 7.1:** Capture POST-state `make verify-sync` exit code (AC-P1.7)

- [ ] Run `make verify-sync 2>&1; echo "EXIT_CODE=$?"` from the repository root using Bash tool and capture both stdout/stderr and the exit code to `.dev/tasks/to-do/TASK-RF-20260518-cliEval-P1-pty-isolation-gates/phase-outputs/test-results/05-verify-sync-POST.txt` with a leading header `# POST-state make verify-sync — after all cliEval-P1 files have landed\n# Date: [today]\n# Expected: EXIT_CODE=0 (AC-P1.7 no regression)\n---\n`, ensuring the EXIT_CODE line is captured. Verify the POST-state exit code MATCHES the PRE-state exit code captured in Step 1.5 (both should be 0). If POST-state exit is non-0 while PRE-state was 0, this is a REGRESSION — append a `## Regression Triage` subsection with the diff between PRE and POST captures and (a) check whether any new files under `src/superclaude/cli/eval/` need to be mirrored to `.claude/` (run `make sync-dev` first then re-run verify-sync), (b) check whether any new file should be excluded from sync-verification (unlikely for `src/superclaude/cli/` paths which are Python source not skill/agent/command source). If POST-state still fails after running `make sync-dev`, mark this an AC-P1.7 FAIL and surface in Open Questions. Once done, mark this item as complete.

**Step 7.2:** Run `make sync-dev` if needed (L5 Conditional-Action)

- [ ] If Step 7.1's POST-state exit code is 0, write `phase-outputs/plans/PG-7-sync-status.md` containing only `verify-sync POST-state: EXIT_CODE=0 on first attempt — no sync-dev needed.` and proceed to Phase 8. If POST-state exit was non-0 due to a sync-dev mismatch, run `make sync-dev 2>&1` and capture the output to `phase-outputs/test-results/06-sync-dev-output.txt`, then re-run Step 7.1's verify-sync capture into `phase-outputs/test-results/05-verify-sync-POST-after-sync.txt`. Verify the re-run produces EXIT_CODE=0. If it does, write `phase-outputs/plans/PG-7-sync-status.md` documenting the sync-dev was run and the verify-sync passed on second attempt. If it still fails, surface the persistent regression as an AC-P1.7 BLOCKER and mark the task BLOCKED. The `src/superclaude/cli/` tree contains pure Python source, NOT skills/agents/commands — verify-sync typically targets `.claude/{skills,agents,commands}/` so the expected POST result is EXIT=0 unchanged; if make verify-sync flags `src/superclaude/cli/eval/` for sync, this is a verify-sync rule misconfiguration not a P1 regression — document the rule misconfiguration in `phase-outputs/plans/PG-7-sync-status.md` and propose either a verify-sync rule update OR a sync-dev rule update as a follow-up task (do NOT modify the Makefile in this task — out of scope). Once done, mark this item as complete.

---

### Phase 8: Aggregation, AC Verification Matrix, and Task Completion

**Context:** This final phase produces the per-AC verification matrix proving all 8 acceptance criteria (AC-P1.1 through AC-P1.8) pass with evidence, then marks the task complete by updating frontmatter.

**Step 8.1:** Final integration QA — composite verification (L4 Review/QA)

- [ ] Spawn the rf-qa subagent in a single Agent tool call (subagent_type: "rf-qa", mode: "bypassPermissions") with the prompt below; the subagent MUST perform composite verification across ALL Phase 1-7 outputs (it is the final structural QA gate), and write its report to `phase-outputs/reviews/PG-FINAL-rf-qa-composite-report.md`. The prompt is:

> ```
> QA_MODE: task-integrity
> fix_authorization: true
>
> **ADVERSARIAL STANCE:** Assume the work contains errors. Verify every claim exhaustively. A verdict of 0 issues requires evidence you thoroughly checked.
>
> TASK FILE: .dev/tasks/to-do/TASK-RF-20260518-cliEval-P1-pty-isolation-gates/TASK-RF-20260518-cliEval-P1-pty-isolation-gates.md
> SCOPE: COMPOSITE — verify all 14 files listed in BUILD_REQUEST "Files to create" + all 8 acceptance criteria (AC-P1.1 through AC-P1.8).
>
> EXPECTED FILE LIST (verify each exists by Glob/Read):
>   1. src/superclaude/cli/eval/__init__.py
>   2. src/superclaude/cli/eval/config.py
>   3. src/superclaude/cli/eval/pty/__init__.py
>   4. src/superclaude/cli/eval/pty/driver.py
>   5. src/superclaude/cli/eval/pty/stream.py
>   6. src/superclaude/cli/eval/pty/LICENSE
>   7. src/superclaude/cli/eval/pty/PROVENANCE.md
>   8. src/superclaude/cli/eval/isolation.py
>   9. src/superclaude/cli/eval/capability_gates.py
>   10. src/superclaude/cli/eval/commands.py
>   11. tests/cli/test_eval/__init__.py
>   12. tests/cli/test_eval/test_isolation.py
>   13. tests/cli/test_eval/test_capability_gates.py
>   14. tests/cli/test_eval/test_pty_vendor.py
>
> AC VERIFICATION — verify each by reading the named evidence file:
>   - AC-P1.1: phase-outputs/test-results/01-doctor-smoke-test.txt + 04-test-capability-gates.txt — green-checklist rendering + exit 0/2
>   - AC-P1.2: phase-outputs/test-results/02-test-isolation.txt — setup/env/teardown contract tests pass
>   - AC-P1.3: phase-outputs/test-results/03-test-pty-vendor.txt — PtyDriver surface tests pass
>   - AC-P1.4: phase-outputs/test-results/03-test-pty-vendor.txt — upstream test suite (or option C minimal) PASS
>   - AC-P1.5: src/superclaude/cli/eval/pty/PROVENANCE.md — 6 documented diffs present
>   - AC-P1.6: phase-outputs/test-results/02-test-isolation.txt — hard guard test passes + isolation.py guard code present
>   - AC-P1.7: phase-outputs/test-results/00-verify-sync-PRE.txt + 05-verify-sync-POST.txt — both EXIT_CODE=0
>   - AC-P1.8: phase-outputs/test-results/02-test-isolation.txt + 03-test-pty-vendor.txt + 04-test-capability-gates.txt — all three EXIT_CODE=0
>
> ESCALATION — CRITICAL OVERRIDE: You have NO team context. Do NOT use SendMessage. Return your verdict and report file path as your final output.
>
> fix_authorization is TRUE for this final pass — you MAY fix small structural issues in the task file or source files IN-PLACE via Edit, then document what you fixed in the report. Do NOT fix substantial design issues — those require user review (flag as Open Question instead).
>
> Apply the rf-task-builder TB-Add-1 through TB-Add-8 structural gate checks against the task file:
>   - TB-Add-1: No TBD/TODO/FIXME tokens in task file checklist items (TODOs inside source files are acceptable per Step 3.3 P2 wiring marker)
>   - TB-Add-2: Item count within bounds (track ≥3 and ≤40; this single-track task should fall in that range)
>   - TB-Add-3: Each blocked item references its blocking Open Question by index in Context (N/A unless blocks exist)
>   - TB-Add-4: Item-to-item dependencies form a DAG (no cycles)
>   - TB-Add-5: XL/multi-file items either split or carry justifying comment
>   - TB-Add-6: Uniform `Verify: ...` prefix and consistent Acceptance Criteria form
>   - TB-Add-7: Source areas in task header reappear in items (this task file does not emit an Execution Context block — TB-Add-7 INACTIVE)
>   - TB-Add-8: Per-item Context evidence binding — each item's referenced file paths cite a stable path (file:line not required since this is an authoring task, not a code-modification task — informational)
>
> OUTPUT FILE: phase-outputs/reviews/PG-FINAL-rf-qa-composite-report.md
> Write incrementally with header first.
> Conclude with: VERDICT: PASS or FAIL with per-AC status table (8 rows, one per AC).
> ```

After the subagent returns, read `phase-outputs/reviews/PG-FINAL-rf-qa-composite-report.md` and check the per-AC status table. If ALL 8 ACs are PASS, proceed to Step 8.2. If any AC is FAIL, surface in Open Questions section at the bottom of this task file and proceed to Step 8.2 ONLY IF the user explicitly authorizes proceeding with known AC failures (otherwise mark task BLOCKED). Once done, mark this item as complete.

**Step 8.2:** Materialize per-AC verification matrix (L6 Aggregation — all 8 ACs)

- [ ] Read `phase-outputs/reviews/PG-FINAL-rf-qa-composite-report.md` and write the final per-AC verification matrix to `.dev/tasks/to-do/TASK-RF-20260518-cliEval-P1-pty-isolation-gates/phase-outputs/reports/per-ac-verification-matrix.md` containing a markdown table with columns `AC-ID | Brief | Verdict (PASS/FAIL) | Evidence File(s) | Checklist Items` with one row per AC (AC-P1.1 through AC-P1.8), populated from the rf-qa composite report's per-AC table. The table MUST list the specific checklist items (per the "Acceptance Criteria Mapping" section at the top of this task file) and the specific evidence files in `phase-outputs/test-results/` and `phase-outputs/reviews/` that prove each verdict. Append a `## Summary` section with the overall verdict (PASS only if all 8 rows are PASS) and a `## Open Questions Carried Forward` section listing any ACs that were FAIL or that surfaced unresolved issues during the task. The matrix is the canonical evidence trail consumed by the maintainer when reviewing the PR `feat(eval): cliEval P1 — vendor ptytest + HomeIsolation + capability gates + eval doctor`. Once done, mark this item as complete.

**Step 8.3:** Update Open Questions section based on final outcomes

- [ ] Read the rf-qa composite report from Step 8.1 and the per-AC matrix from Step 8.2, and update the `## Open Questions` section at the bottom of this task file (NOT the frontmatter — the section near the end of the file) by appending any unresolved questions from the rf-qa report, any AC-failures surfaced in the per-AC matrix, and the disposition (resolved-in-Phase-1, deferred-to-P2, BLOCKED) for each of the 3 original BUILD_REQUEST open questions (Q1: pexpect>=4.9, Q2: ptytest MIT license, Q3: prompt-ready heuristic). Each Open Question entry MUST follow the OQ disposition pattern from rf-task-builder methodology: `**OQ-N:** [question verbatim from BUILD_REQUEST or surfaced during execution]. **Disposition:** [RESOLVED-IN-PHASE-N / DEFERRED-TO-P2 / BLOCKED / SURFACED-FOR-USER]. **Evidence:** [path to discovery / test-result / review file that supports the disposition].`. Once done, mark this item as complete.

**Step 8.4:** Mark task complete — frontmatter update

- [ ] Update the `status` field in the frontmatter at the top of this task file from "🟠 Doing" to "🟢 Done", update the `completion_date` field to today's date (from the session-context envelope), and update `updated_date` to today's date, then add a final timestamped entry to the `### Execution Log` in the `## Task Log / Notes` section using the format `**[YYYY-MM-DD HH:MM]** - Task completed: Updated status to "🟢 Done" and completion_date. Per-AC verification matrix at phase-outputs/reports/per-ac-verification-matrix.md shows [N]/8 ACs PASS.`. If the per-AC matrix from Step 8.2 shows any AC FAIL, do NOT mark the task Done — instead set status to "⚪ Blocked" with `blocker_reason` populated with the failing AC IDs and a one-line summary of why each failed. Verify the frontmatter change by re-reading lines 1-55 of this task file and confirming the status field reads exactly `"🟢 Done"` (or `"⚪ Blocked"` if blocked). If unable to edit the frontmatter due to file access issues, log the specific blocker using the templated format in the `### Phase 8 Findings` section of the `## Task Log / Notes`, then mark this item complete. Once done, mark this item as complete.

---

## Open Questions

This section documents unresolved ambiguities surfaced by the BUILD_REQUEST and by execution. Each entry follows the OQ disposition pattern. Entries are appended during Phase 1 (Steps 1.6, 1.7, 1.8) for the BUILD_REQUEST's original 3 Qs, and during Phase 8 (Step 8.3) for any unresolved gate failures.

**OQ-1:** _BUILD_REQUEST Q1 verbatim — "Confirm `pexpect>=4.9` is acceptable as a new runtime dep (it's transitively pulled by some existing packages but not directly required). If not, the vendored ptytest needs to vendor pexpect too."_

- **Disposition:** [TO-BE-FILLED in Phase 1 Step 1.6 — one of ACCEPTABLE / CONDITIONAL / DEFERRED-TO-VENDOR based on `uv pip list` and pyproject.toml inspection]
- **Evidence:** `phase-outputs/discovery/03-pexpect-acceptability.md`

**OQ-2:** _BUILD_REQUEST Q2 verbatim — "Verify upstream ptytest's MIT license and ensure NOTICE/LICENSE handling matches IronClaude's existing conventions."_

- **Disposition:** [TO-BE-FILLED in Phase 1 Step 1.7 — confirm MIT identifier and verify NOTICE requirement]
- **Evidence:** `phase-outputs/discovery/04-ptytest-license-and-sha.md`

**OQ-3:** _BUILD_REQUEST Q3 verbatim — "Verify Claude Code's TTY behavior on Linux (the target platform) — specifically, does it emit a deterministic prompt-ready signal that `expect_prompt_ready` can match? If not, document the heuristic chosen (e.g., regex for `^> $` or `^\$ $` or idle-stdout-for-N-seconds)."_

- **Disposition:** [TO-BE-FILLED in Phase 1 Step 1.8 — primary regex + fallback idle-timeout chosen; surfaced for verification during AC-P1.3 testing]
- **Evidence:** `phase-outputs/discovery/05-prompt-ready-heuristic.md`

[Additional OQ-N entries appended by Phase 8 Step 8.3 as surfaced during execution]

---

## Task Log / Notes

### Execution Log

[Timestamped entries appended during execution — format `**[YYYY-MM-DD HH:MM]** - <event>`]

### Phase 1 Findings

[Per-step finding entries — format below]

```
**Phase 1 Step X.Y — [PASS|FAIL|BLOCKER]:** <observation>
- Discovery file: <path>
- Evidence: <citation>
- Blocker (if any): <specific issue + remediation suggestion>
```

### Phase 2 Findings

[Same template as Phase 1 Findings]

### Phase 3 Findings

[Same template]

### Phase 4 Findings

[Same template]

### Phase 5 Findings

[Same template]

### Phase 6 Findings

[Same template]

### Phase 7 Findings

[Same template]

### Phase 8 Findings

[Same template]

### Follow-Up Items

[Items discovered during execution that need separate tasks — e.g., a verify-sync rule update if Step 7.2 surfaces one, the P2 wiring of seed_state in HomeIsolation.setup per Step 3.3 TODO marker]
