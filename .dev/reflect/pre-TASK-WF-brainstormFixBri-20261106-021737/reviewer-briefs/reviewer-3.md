# Reviewer brief 3 (pre-execution plan audit, read-only)

## T1 card excerpt

Verbatim contents of .dev/reflect/pre-TASK-WF-brainstormFixBri-20261106-021737/reflection-card.yaml:

```yaml
card_version: "1.0"
mode: pre
subject: "Plan TASK-WF-brainstormFixBri-20261106-021737 (7 tasks, 4 phases), the regenerated plan that applies 17 review corrections, checked against its source brief (source.md, Parts 1 to 5)"
claim: >
  The plan covers the five original brief items and applies all 17 corrections (F-1 to F-17) with the
  replacement wording copied verbatim. Its anchors match the files on disk. It is ready for /sc:implement,
  with the P2 notes below.
self_reported_confidence: 0.88
blind_calibration: {calibrated_confidence: PENDING}
tier_routing: "Forced to Tier 2: strict Pass 1 finds no labelled ID (F-n and INV-n do not match ID_REGEX), 28 inferred rows, so the parse-density guard (coverage_degraded: parsed-sparse) forbids the Tier 1 stop."
coverage:
  parsed_rows: 0
  inferred_rows: 28
  matched_by_containment_rule: 23
  coverage_pct: null
  coverage_pct_union: 0.8214
  s_dev_density: 0.1786
  manual_review_of_the_5_unmatched_rows: "INF-002 (brief item 2, covered by Tasks 4 and 5), INF-007 (F-1, covered by Task 6), INF-009 (F-3, covered by Tasks 1 to 5), INF-018 (F-12, covered by the shared phrases in Tasks 1 to 5) are covered in different words; INF-022 (F-16) is a deliberate narrowing, see F-1 below."
  artifact: artifacts/coverage-matrix.yaml
grounded_checks_passed:
  - "SKILL.md line 195 tail, line 196 blank, line 197 'Quality-tier tracking' heading (artifacts/grounding.txt:9-13)"
  - "handoff-routing.md anchors: Tier 1 line 16, quality_tier line 22, Tier 2 line 24, Activation line 31, Final fallback line 33 (artifacts/grounding.txt:1-8)"
  - "brainstorm.md line 157 ends 'so a nested directory is never reused.' (artifacts/grounding.txt:14-15)"
  - "spec line 62 ends with the sentence Task 6 appends to; spec line 286 is the 7.2 step 4 line ending 'At P0, AC-0.4 replaces this step.' (artifacts/grounding.txt:16-20)"
  - "No test file reads the spec, so the two spec edits cannot break a test (artifacts/grounding.txt:21)"
  - "HEAD copies of the three primitives contain none of the new pins, so the 'fails on pre-change text' claims hold (artifacts/grounding.txt:22-25)"
  - "All five test files named by Task 7 exist; make targets exist (artifacts/grounding.txt:26-46)"
  - "The package passes the workflow quality gate (7 tasks, 4 phases, contiguous, acceptance bullets in every task, no checkbox or numbered lines)"
findings:
  - id: F-1
    priority: P2
    claim: "The plan's Constraints line for correction F-16 says the edits reach the next live plan 'only after they are committed to a branch the live-check worktree is built from'. The brief's correction F-16 asks for 'only after the owner commits and merges them'. The narrowing is deliberate (the earlier review's evidence check found 'merges' unsupported by spec line 282), but the plan does not record the departure."
    evidence: "plan Constraints (line 28); source.md:199; spec:282"
  - id: F-2
    priority: P2
    claim: "Task 7 says 'it writes only the logs and the status snapshot under ./artifacts/'. The brief's correction F-13 gives the sentence 'it writes only the logs under ./artifacts/'. The extension is needed because correction F-2 adds the status-after snapshot, but the departure is not recorded."
    evidence: "plan Task 7 body; source.md:169"
  - id: F-3
    priority: P2
    claim: "Task 7's third acceptance bullet passes only if no new line appears in git status outside the six files and the package folder. If /sc:implement or its final reviewer writes anywhere else under .dev/ (for example a new .dev/reflect or .dev/implement folder), the bullet fails on a correct run. Not verified either way."
    evidence: "plan Task 7 acceptance bullet 3; source.md:53"
  - id: F-4
    priority: P2
    claim: "Task 6 describes the step 4 line as one that 'begins Check the contract (PyYAML ...'; the line actually begins '4. Check the contract'. The anchor is still findable."
    evidence: "plan Task 6 body; artifacts/grounding.txt:19"
risk_surface:
  blast_radius: "Documentation and test text only: six files, no runtime code. A wrong pin turns a test red; a wrong sentence misleads a live-plan author."
  interaction_effects: "Task 4 and Task 5 pins depend on the exact text written by Tasks 1 to 3 (order declared by Depends on). The skill uses the form 'write', the ref and command use 'writes'; the shared phrase 'no nested directory and no nested contract' is a substring of both."
  residual_risks_recorded_in_plan: "Four false-PASS risks of the live-check sentence are listed in Task 6, including the inferred tool names Skill, Agent and Task."
  open_conflict_recorded_in_plan: "Research enrichment from P2 is not covered (Constraints)."
recommendations:
  - id: R-1
    priority: P2
    file: "TASK-WF-brainstormFixBri-20261106-021737.md (Constraints, Task 7 body)"
    change: "Add one sentence to the Constraints saying the F-16 line and the Task 7 'writes only' sentence are deliberately narrower or wider than the brief's, and why."
    verifier: "The Constraints block names both departures."
  - id: R-2
    priority: P2
    file: "TASK-WF-brainstormFixBri-20261106-021737.md (Task 7, third acceptance bullet)"
    change: "State that new lines under .dev/reflect/ or .dev/implement/ created by the executor itself are also allowed, or run a dry check of what the executor writes."
    verifier: "The bullet names every folder the executor is known to write to."
unverified:
  - "make lint-architecture baseline and the two extra test files were not run; the planned text was read against them, not executed"
  - "How /sc:implement and its final reviewer change git status (finding F-3)"
  - "The tool names Skill, Agent and Task in the Task 6 live-check sentence (recorded as a residual risk in the plan)"
```

## Grounding hunks

codegraph run state: index_state=unchecked checked_at=2026-11-06T02:24Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P1 projectPath=/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P1 (codegraph not used in this run; audit with Read/Grep/Glob only)

### src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:195-197

```markdown
   **Under `--unattended`**: the two research rows are skipped, also for an explicit `--research light` or `--research deep` (recorded in `enrichment_used` with `quality_tier: skipped`). The codebase row invokes `/sc:analyze` with `--unattended --report-dir <report-dir>/nested/analyze-<n>/` (`<n>` starts at 1); the `mcp__auggie__codebase-retrieval` alternative is unchanged and writes no nested contract. The nested contract is listed in `artifacts`.

2. **Quality-tier tracking** (mandatory per enrichment source):
```

### src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md:16-35

```markdown
**Tier 1 (primary)**: `mcp__auggie__codebase-retrieval`

- Two parallel queries (per existing brainstorm v1 pattern):
  - Query 1: `"{topic} - find relevant code, existing implementations, related components, and integration points"`
  - Query 2: `"Project architecture, structure, patterns, and conventions related to {topic_domain_area}"`
- Output budget: ~800-1200 tokens summary per query
- quality_tier: `primary`

**Tier 2 (fallback_1)**: codegraph, then native Glob/Grep

- codegraph first (Codegraph usage rules: read `~/.claude/CODEGRAPH.md` (in a dev checkout without an install, the labelled fallback is `src/superclaude/core/CODEGRAPH.md`)): run the guide's readiness check once; only when `index_state` is `fresh` and the tools are listed, call `codegraph_files {format: "grouped", maxDepth: 2, path: <relevant dir>, projectPath}` on the relevant directories and `codegraph_search {query: <entity>, limit: 10, projectPath}` for each entity name the topic names. Graph rows are leads (Read before quoting); record any `graph:*` token in the seed-brief Note section. When codegraph is unusable or returns nothing, the native steps below run unchanged.
- Glob for files matching topic keywords
- Grep for symbol/entity names mentioned in topic (for a named function or class, Grep for `def name|class name|function name`, then Read the range)
- Output budget: ~300-500 tokens (raw file list + grep hits)
- quality_tier: `fallback_1`
- Activation: if Tier 1 returns error OR empty result

**Final fallback**: skip enrichment, set quality_tier: `skipped`, log to seed-brief Note section.

### Research enrichment (light)
```

### src/superclaude/commands/brainstorm.md:157-157

```markdown
- **Nested invocations.** The `/sc:analyze` codebase enrichment receives `--unattended --report-dir <report-dir>/nested/analyze-<n>/`, and the Wave 3 adversarial call receives `--unattended --output <report-dir>/nested/adversarial-<n>/` in place of `<output>/adversarial/`. `adversarial_artifacts_dir` and the nested contracts are listed in `artifacts`. `<n>` starts at 1 for each nested command, and the one retry of a nested call (the adversarial `F1` retry) uses the next number, so a nested directory is never reused.
```

### src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:183-203

```markdown
1. **Enrichment routing matrix** (apply in parallel via `Task` agents):

   | Condition | Action | Output |
   |-----------|--------|--------|
   | `domain ∈ {code, architecture, incident}` AND NOT `--no-codebase` | Invoke `/sc:analyze <relevant-paths> --focus quality --depth quick` OR `mcp__auggie__codebase-retrieval` for quick scan | `enrichment/codebase-context.md` |
   | `--codebase` (forced) | Same as above regardless of domain | Same |
   | `--research light` OR (auto: topic mentions framework/library names not in project) | Invoke `Skill sc-research-protocol` with `--depth quick` (or `/sc:research` if standalone) | `enrichment/research-light.md` |
   | `--research deep` OR (auto: `--strategy enterprise` + novel topic) | Invoke `Skill tech-research` with topic | `enrichment/research-deep.md` |
   | Otherwise | Skip enrichment | — |

   Research depth/params are owned by `/sc:research` and `tech-research` — see RESEARCH_CONFIG.md; brainstorm selects the route only.

   **Under `--unattended`**: the two research rows are skipped, also for an explicit `--research light` or `--research deep` (recorded in `enrichment_used` with `quality_tier: skipped`). The codebase row invokes `/sc:analyze` with `--unattended --report-dir <report-dir>/nested/analyze-<n>/` (`<n>` starts at 1); the `mcp__auggie__codebase-retrieval` alternative is unchanged and writes no nested contract. The nested contract is listed in `artifacts`.

2. **Quality-tier tracking** (mandatory per enrichment source):
   - `primary` — first-choice source ran cleanly
   - `fallback_1` — primary failed, used codegraph and native Glob/Grep (codebase) or WebSearch (research)
   - `skipped` — enrichment not invoked
   - Record as `enrichment_used: [{source, quality_tier}, ...]` in state.

3. **Token budget for enrichment**: ~30000 tokens total cap. Priority order if exceeded: codebase > research-light > research-deep. Truncate by priority.
```

### src/superclaude/commands/brainstorm.md:148-160

```markdown
## Unattended mode

The shared rules are in `~/.claude/WORKER-CONTRACT.md`; read it first. This section lists only what `/sc:brainstorm` resolves itself. `<report-dir>` below is the one report directory the caller passes.

- **Switch.** It applies only when `--unattended` is a standalone argument token outside any quoted argument (the topic is a quoted argument); otherwise nothing here applies and no worker contract is written.
- **Report directory.** Exactly one of `--output <dir>` (short form `-o`) or `--report-dir <dir>`; both, or neither, is refused before any work. A directory the caller passes is used exactly as passed, never with the usual `-N` suffix. One that already holds a `return-contract.yaml`, one inside `.git/` or `.codegraph/`, one under the distributable skill, agent or command folders of a `.claude/` folder, or one that cannot be created or written, is refused before any work as no usable report directory (printed in chat only), so no earlier contract is overwritten.
- **Contract.** With `--output` the worker fields are added to the command's own `<output>/return-contract.yaml` beside every existing field, its own `status` included. With `--report-dir` the worker contract is a separate `<report-dir>/return-contract.yaml` that lists the own contract in `artifacts`. It is written on every other outcome, including each stop of Wave 0 of the skill (the stop text goes to `reason`). `report_path` is `merged-requirements.md` (null when the merge was not reached, and on `--dry-run`). The own status values success, partial, failed and dry-run map to succeeded, partial, failed and succeeded.
- **Person-mode flags.** `--interactive` and its short form `-i` are refused before any work (contract `worker_status: failed`, the flag in `reason`). The Socratic dialogue proceeds on the best available context, and there is no other gate.
- **Research.** Under `--unattended`, research enrichment is off: the automatic route and an explicit `--research light` or `--research deep` are skipped, each recorded in `enrichment_used` with `quality_tier: skipped`.
- **Nested invocations.** The `/sc:analyze` codebase enrichment receives `--unattended --report-dir <report-dir>/nested/analyze-<n>/`, and the Wave 3 adversarial call receives `--unattended --output <report-dir>/nested/adversarial-<n>/` in place of `<output>/adversarial/`. `adversarial_artifacts_dir` and the nested contracts are listed in `artifacts`. `<n>` starts at 1 for each nested command, and the one retry of a nested call (the adversarial `F1` retry) uses the next number, so a nested directory is never reused.
- **Handoffs.** The `tasklist` and `task` handoffs are skipped and recorded: `status: partial` with one line in `unresolved_conflicts` (their skills do not accept the flag at this phase), and the Wave 0 check that their skills are installed is skipped too. The `design` and `none` handoffs are unchanged.
- **Outward actions.** It pushes, commits and stages nothing.

```

### .dev/orca-command-refactor/specs/orca-worker-contract-spec.md:60-63

```markdown
- **Brief guard** (worker session, from P1): it applies only in a session whose current prompt carries a live Orca preamble with Task and Dispatch IDs (see "Worker run"). Before invoking anything, the worker checks every `Command:` line of its brief (section 2.3, "Brief layout"), and only those lines. It decides case 3 from the command name alone. For the other cases it reads, as plain files, every existing copy of the command file: the project `.claude/commands/sc/<name>.md` in its worktree and `~/.claude/commands/sc/<name>.md`. It refuses, runs nothing, writes no contract, and sends `worker_done --outcome failed` with no `--report-path` and a body starting `guard refused:` when: (case 1) every existing copy has an `## Unattended mode` section and the line lacks a standalone `--unattended` (`guard refused: brief lacks --unattended`); (case 2) no existing copy has the section and the line has the flag (`guard refused: loaded command has no Unattended mode section (not converted at this phase, or the loaded copy is stale)`); the copies disagree (`guard refused: command copies disagree (stale copy): <paths>`); (case 3) the command is on the never-as-worker list. A command invoked by another command, through the Skill tool or the Agent tool, is never checked; the nested propagation rule governs it. The guard checks once, before the first run: a WC-3 re-invocation keeps every token of the brief's `Command:` line, `--unattended` included, and only adds the answer.
- **Never-as-worker list**: `/sc:agent`, `/sc:git`, `/sc:help`, `/sc:pm`, `/sc:spawn` and `/sc:swarm-wizard` (section 4), plus `/sc:pr-submit` while the answer to D3 keeps it off workers. The list changes only when section 4 or D3 changes, never per phase. If D3 adds a worker route for pr-submit, D3 also states how that route passes the brief guard.
- **Nested propagation rule**: under `--unattended`, a command that invokes another `/sc:` command or protocol skill, through the Skill tool or the Agent tool, passes `--unattended` when the invoked command accepts it at this phase, together with its own report directory `<caller report-dir>/nested/<command>-<n>/` (WC-4, WC-11). The caller lists the nested contract in its `artifacts`; only the top-level contract drives WC-5. When the invoked command does not accept the flag yet, that step must be gate-free per its section 3 row, or the caller skips it under `--unattended` and records the skip in its contract. Each command's `## Unattended mode` section names its nested invocations.

```

### .dev/orca-command-refactor/specs/orca-worker-contract-spec.md:281-304

```markdown
### 7.2 Live worker check (used by P0-P4)
For each command under test, the coordinator runs the steps below with one worker in a fresh disposable worktree that holds the phase's edits, so step 6 can attribute every change to the worker under test (WC-11 allows sharing a worktree in normal use; the check does not). Orca creates worktrees from a git base, and the phase's edits are uncommitted until the user asks (`CLAUDE.md:37`), so before the check the phase's edits are committed to the feature branch or a scratch branch with the user's authorization (a decision point each phase). The disposable worktree is created by Orca at Orca's default path from that branch, never under `.dev/worktrees/`. `make sync-dev` is run inside it before dispatch unless Orca's `--setup run` is confirmed to do it (UNVERIFIED item 27). Before the phase's live checks, the coordinator asks the owner for approval, then installs that phase into `~/.claude` by running `superclaude install --force` from the phase branch, as `uv run superclaude install --force` inside a checkout of that branch, because the installer copies from the running package's own location (`src/superclaude/cli/install_core.py:117-122`), so a separately installed `superclaude` would install its own files, not the branch's. One approval per phase, asked before every phase's install. If a phase is abandoned, the coordinator reinstalls from master (`superclaude install --force` from master). Both installs pass `--force` because without it the installer skips every file that already exists (`src/superclaude/cli/install_commands.py:55-57`), so the phase would never reach `~/.claude`; `update.sh:8` runs the same `superclaude install --force`. After step 7 the worktree is removed with `orca worktree rm`, because orchestration verbs never delete worktrees (`CAPS:115`).
1. `ORCA orchestration task-create --spec "<brief per section 2.3>" --json`. Then either `ORCA orchestration worker-start --task <task_id> --worktree new-top-level --base-branch <branch> --setup run --agent claude --json`, when the setup is confirmed to run `make sync-dev`; or create the worktree first with `ORCA worktree create` from `<branch>`, run `make sync-dev` inside it, and start the worker with `--worktree path:<worktree>`. For a command that accepts `--unattended` at this phase, confirm before dispatch that every existing copy of its file (`<worktree>/.claude/commands/sc/<name>.md` and `~/.claude/commands/sc/<name>.md`) has its `## Unattended mode` section. **Pass:** exit 0 and `state: ready` (`CAPS:46`).
2. While it runs, `ORCA orchestration worker-show --dispatch <dispatch_id> --json` at least once per 5 minutes. **Pass:** `observation.agentWait` is never non-null (a non-null value means the worker is parked on a prompt only a person can answer, `CAPS:129`). Sampling can only find a wait, not prove there was none; step 3 adds the positive proof.
3. `ORCA orchestration check --wait --types "worker_done,escalation,question" --timeout-ms 900000 --json` until `worker_done` arrives. If the wait ends without one, read `ORCA orchestration worker-read --dispatch <dispatch_id> --source transcript --json`: a final agent turn that sent no `worker_done` is Orca's positive proof of a stall (`CAPS:126`), and the check fails; a transcript still growing means keep waiting. **Pass:** exactly one `worker_done`; its `--outcome` matches the contract's `worker_status` under WC-5; its report path is the WC-4 contract path. At P0, before the contract exists, AC-0.4 replaces the last two conditions.
4. Check the contract (PyYAML is a declared dependency, `pyproject.toml:38`). **Pass:** both commands exit 0. At P0, AC-0.4 replaces this step.
   ```sh
   test -s <contract>
   uv run python -c "import sys, yaml; d = yaml.safe_load(open(sys.argv[1])); assert d['worker_contract_version'] == '1'; assert d['worker_status'] in {'succeeded','partial','failed','blocked'}; assert d['command']; assert d['worker_status'] != 'blocked' or d.get('blocked_question')" <contract>
   ```
5. Check the worker's behaviour over the whole run. The primary source is the worker's own session file; `worker-read` is the cross-check for the end of the run (P0 found that `worker-read` returns only the last 40 to 50 messages of a long run and its cursor never ends, so it cannot show the start of a run; UNVERIFIED items 28-33).
   - **Source file.** For a Claude worker started on this machine the file is `~/.claude/projects/<dir>/<session id>.jsonl`, where `<dir>` is the worker's worktree path with each `/` replaced by `-`; each subagent's own file is under `~/.claude/projects/<dir>/<session id>/subagents/`. The disposable worktree is fresh, so `<dir>` must hold exactly one top-level `.jsonl` file; none or several make the source ambiguous. Run the analysis after step 3 and before step 7, with Python under `uv run`. Record the file's path, byte length and sha256 in the phase evidence; the file keeps growing after `worker_done`, so a later re-check uses the first recorded byte length. Do not copy the file into the repo (it holds full prompts and tool output); keep the analysis only. The P0 analysis scripts are `.dev/tasks/done/TASK-WF-writeTheP0LivePl-20261103-215902/artifacts/session-analysis.py` (arguments: the `<dir>` folder, the top-level session file; prints the tool tally, the Skill-call timing, the Orca commands, the heartbeat times and the WC-13 scan) and `session-hbcover.py` (argument: the top-level session file; prints the heartbeat gaps with subagent time removed), each run as `uv run --no-project python -I <script> <arguments>`.
   - **Cross-check.** `ORCA orchestration worker-read --dispatch <dispatch_id> --source transcript --json`, page 1, then once more with the returned `cursor`. Record `contentComplete`, the time window page 1 covers, and whether the second page is empty. It must show the same final `check` call and the same `worker_done` as the session file, and tool calls by name (AC-0.6). If the two sources disagree, step 5 fails.
   - **Pass conditions, all read from the session file:**
     1. No `AskUserQuestion` call, in the top-level session or in any subagent session (WC-2).
     2. The command was run in the worker's top-level session, not inside an Agent-tool call (WC-7): the Skill or command call is a top-level message, not a subagent message.
     3. A `check` call appears after the command finished and before `worker_done` (WC-12).
     4. Heartbeats (WC-10), against the cadence in the worker's own dispatch preamble (5 minutes in Orca 1.4.237). Measure the time between consecutive heartbeats, from the brief to the first heartbeat, and from the last heartbeat to `worker_done`. Both limits must hold: (a) after removing the time during which any subagent of the worker was running or the worker was blocked in `ask` or `check --wait`, at most the cadence; (b) with nothing removed, at most 20 minutes. A subagent's running time is the interval from the first to the last timestamp in that subagent's own session file. Limit (a) removes legitimate waiting on a command's fan-out, during which the worker cannot heartbeat (WC-10); limit (b) bounds a hung subagent.
     5. No `worker-start`, `dispatch` or `task-create` call and no `worktree create --agent` or `agent launch` call (WC-13), searching every Bash command of the top-level and all subagent sessions under any Orca binary name. Read-only calls through the Orca binary (for example `orca-ide skills get ...`, `orca-ide --version`, `orca-ide orchestration worker-list --json`) are not these calls and are listed in the evidence.
   - **Not verifiable.** If the session file is missing, ambiguous, unreadable or contains no tool calls (it is Claude Code's format, not Orca's), conditions 1, 2, 4 and 5 are recorded `not verifiable`. Step 5 is then not passed, the live check is not recorded as passed, and the phase report lists the gap; the phase is not reported PASS until the owner accepts the gap in writing in the phase report. Condition 3 may be judged from the `worker-read` page when that page covers the end of the run. A condition that was not checked is never recorded as PASS. For an agent other than Claude no source file is defined here, so step 5 is `not verifiable` until one is specified.
   - A run shorter than the cadence passes condition 4 vacuously, so each phase report names at least one checked run that lasted longer than the cadence.
   - AC-0.6 (P0) confirmed that tool calls appear by name in `worker-read`; the session file records them as `tool_use` blocks with a `name`.
6. `git status --porcelain` in the disposable worktree. **Pass:** every path it prints that the phase did not edit is under the brief's output or report directory or is a documented artifact of the command. Ignored paths (tool caches, `.venv/`) are not checked.
7. `ORCA orchestration worker-release` for the settled worker, then `ORCA orchestration worker-list --run <run_id> --terminal-state reclaimable --json` returns no rows (`CAPS:107-113`).
```

### .dev/orca-command-refactor/specs/orca-worker-contract-spec.md:136-143

```markdown
### 3.1 Ready with brief constraints (12)
These run as workers now only if the brief uses the stated flags and avoids the inputs that trigger a gate; the worker reports the named file until Phase 1 adds the contract. Four of them (reflect, release-split, tdd, troubleshoot) still have a gate that Phase 2 converts: until then the brief must keep away from it (no `--remediate` for reflect; spec-shaped input and the default `--r1-scope` for release-split; a precise component prompt for tdd; no `--depth deep` and no `--fix` for troubleshoot), and an input that hits the gate stalls the worker. The only command changes are the small fixes in the last column.

| Command | Brief must pass | Report today | Resume (WC-6) | Small fix (phase) | Evidence |
|---|---|---|---|---|---|
| adversarial | `--output <dir>`; never `--interactive` | contract, but filename not fixed | `--pipeline-resume` (pipeline mode only); else fresh dir | Fix its own contract filename to `<output>/adversarial/return-contract.yaml` (P1); the worker contract is `<output>/return-contract.yaml` and lists that file in `artifacts` (WC-4) | `sk/sc-adversarial-protocol/SKILL.md:427-429,605,1908,2806-2833`; `INV-A:35,60-61` |
| brainstorm | `--output <dir>`; never `--interactive` | `<output>/return-contract.yaml` | `--resume-from <seed-brief>` | Under `--unattended`, automatic research enrichment (`sk/sc-brainstorm-protocol/SKILL.md:185`) is off (P1); from P2 it passes `--unattended` and a nested report directory (P2) | `sk/sc-brainstorm-protocol/SKILL.md:134,335`; `cmd/brainstorm.md:59-63`; `INV-A:39` |
| cleanup-audit | `--pass <N>` (single pass); `--report-dir <dir>` | `.claude-audit/pass<N>-summary.md` | `progress.json` checkpoint | Name the `--pass all` final report; the audit output dir is fixed (`cmd/cleanup-audit.md:112`), so the contract goes to `--report-dir` and only one audit runs per worktree at a time (WC-11); under `--unattended`, amend its `.claude-audit/`-only write scope (`cmd/cleanup-audit.md:112`; `sk/sc-cleanup-audit-protocol/SKILL.md:92`) to allow that contract (P1) | `sk/sc-cleanup-audit-protocol/SKILL.md:76,113`; `cmd/cleanup-audit.md:112-117`; `INV-A:42` |
```

### .dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-021737/TASK-WF-brainstormFixBri-20261106-021737.md:12-36

```markdown
# Brainstorm: nested analyze folder only when /sc:analyze ran (corrected plan)

Source: ./source.md
Goal: `/sc:brainstorm` under `--unattended` says, in its skill, its command file and its routing ref, that the nested `analyze` directory is written only by a `/sc:analyze` call, and that the auggie scan and the `fallback_1` scan (codegraph, then Glob and Grep) write no nested directory and no nested contract. Tests pin both halves of that rule, and the worker-contract spec carries a live-check sentence that does not decide the folder by `quality_tier`.

## Constraints

- Background: the P1 live check lc10 failed because the codebase-enrichment wave ran on `quality_tier: fallback_1` (the auggie tool was not available in the worker session) and wrote no `nested/analyze-1/` directory, while the live plan expected one. The owner decided on 2026-11-05 that the check wording was wrong, not the worker. The archived record is in `.dev/tasks/done/TASK-WF-p1LivePlanBrief-20261105-164506/` (`artifacts/lc10-result.md`, `artifacts/p1-owner-decisions-20261105.md`); those files are read, never edited.
- This plan replaces an earlier plan for the same work (package `TASK-WF-brainstormFixBri-20261106-001016`) that an independent review found not ready to run: its Task 6 wording decided the nested folder by `quality_tier`, its Task 7 status check could not pass on the current tree, and the owner rule was not fully pinned. This plan applies those corrections. The earlier package is left as it is.
- Edit only these six files: `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md`, `src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md`, `src/superclaude/commands/brainstorm.md`, `tests/skills/test_brainstorm_protocol.py`, `tests/skills/test_worker_contract.py` and `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. `make sync-dev` also rewrites the gitignored copies under `.claude/`; those are output, not edits, and are never staged.
- `src/superclaude/` is the source of truth. `plugins/superclaude/commands/brainstorm.md` is a copy that already differs from the `src` file, and no test requires the two to match (`tests/commands/test_routing_plugin_parity.py` covers only the `sc-recommend` skill). It is not edited. This is this plan's resolution of spec open item 8 for `brainstorm.md`. Task 7 confirms nothing under `plugins/` changed.
- No new text in the installed files (the skill, its refs, the command file) may name a `src/superclaude/` path or an Orca command; `tests/skills/test_worker_contract.py` (`_check_unattended_section`) fails on both.
- UV for every Python command: `uv run pytest ...`, `uv run python ...`. Test runs use `-p no:cacheprovider` and `PYTHONDONTWRITEBYTECODE=1`. No `superclaude install` (the owner updates the installed copies under `~/.claude/` later). No git commit, push, merge or PR.
- The edits reach the next live plan only after they are committed to a branch the live-check worktree is built from; this plan does not commit.
- Open conflict, no change planned here: from phase P2 brainstorm's research enrichment also passes a nested report directory, and the research-deep fallback is itself a nested command. The corrected wording covers only the codebase-enrichment wave. This is an open conflict for the owner and the P2 live-plan author.
- Starting state: the working tree already holds uncommitted edits to `src/superclaude/cli/install_core.py` and `tests/cli/test_how_we_work_install.py` that are not part of this work, and a staged archive of the earlier live plan under `.dev/tasks/done/`. Task 1 records this state before any edit and Task 7 compares against it.

## Phase 1: Say it in the installed primitives

## Task 1: State in the skill that the auggie scan and the fallback tier write no nested directory

First, before any edit, save the output of `git status --porcelain` to `./artifacts/status-before.txt`. Task 7 compares against that file.

In `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md`, the Wave 2A paragraph whose bold lead-in is "Under `--unattended`" (line 195) currently ends: "The codebase row invokes `/sc:analyze` with `--unattended --report-dir <report-dir>/nested/analyze-<n>/` (`<n>` starts at 1); the `mcp__auggie__codebase-retrieval` alternative is unchanged and writes no nested contract. The nested contract is listed in `artifacts`." Replace everything after "(`<n>` starts at 1)" with this exact text, copied character for character:

```

### .dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-021737/TASK-WF-brainstormFixBri-20261106-021737.md:121-200

```markdown
```text
A nested directory `nested/<command>-<n>/` exists only for a nested command that actually ran, a run that failed included; a command that does the same work through a tool or a native-search fallback (brainstorm's codebase scan through `mcp__auggie__codebase-retrieval`, or through codegraph, then Glob and Grep) writes no nested directory and records the tier it used in its own contract, and brainstorm's live-check extra for this is in 7.2 step 4.
```

Second, section 7.2 step 4 is the line that begins "Check the contract (PyYAML is a declared dependency" (line 286) and ends "At P0, AC-0.4 replaces this step." The fenced shell block for that step follows on the next lines and is not edited. Append this sentence to the end of the step 4 line, copied character for character:

```text
A live-check extra for brainstorm's codebase-enrichment wave reads: "when the brief passes `--codebase`, or the contract's `domain` is `code`, `architecture` or `incident` and the brief does not pass `--no-codebase`, `enrichment_used` holds a `source: codebase` entry; every `nested/analyze-` path listed in `artifacts` exists and holds its own `return-contract.yaml`, and every `nested/analyze-<n>/` directory that holds a `return-contract.yaml` is listed in `artifacts`; such a directory is required only when a `Skill`, `Agent` or `Task` tool call in the worker's session file or in one of its subagent files (7.2 step 5) passes `--report-dir <report directory>/nested/analyze-<n>/` with a number for `<n>`, the `codebase` entry is not `skipped` (the per-source enrichment timeout records `skipped` and can stop `/sc:analyze` before it writes) and `/sc:analyze` did not refuse that directory, because neither `quality_tier` nor `source` records whether `/sc:analyze` ran; when the session file is not verifiable, this last clause is recorded `not verifiable`, never PASS" (P1 check lc10 is the origin of this rule).
```

Placement and wording are a Necessary deviation from the brief, recorded here. The brief allows either the live-check section or a note in the P1 rows, and sketches the wording as "a fallback_1 or auggie primary scan is recorded as the tier used with no nested folder". This plan puts the live-check sentence in 7.2 step 4 because every later live plan attaches its step-4 extras there, and sections 7.2 and 7.3 hold no per-command extras list of their own, so the P2 live-plan author reads 7.2 step 4. The wording departs from the sketch because tier does not decide whether the folder must exist: a clean `/sc:analyze` run is also `primary`, and neither `quality_tier` nor `source` names the tool.

Residual risks of the live-check sentence are left in place on purpose; all are in the false-PASS direction, and the sentence has no known false FAIL on a correct run:
- A `/sc:analyze` call made without the nested `--report-dir` (a broken propagation, itself a defect) is not seen, so its missing folder passes; no live check can force the analyze route.
- The call names `Skill`, `Agent` and `Task` are inferred from Claude Code's session format (the spec says only that the session file records `tool_use` blocks with a `name`); a call through another tool name is missed and its missing folder passes.
- The `skipped` carve-out also exempts an invoked `/sc:analyze` that wrote nothing and was recorded `skipped` for a reason other than the timeout.
- The required-folder clause depends on the session file; when it is missing or ambiguous the clause is `not verifiable`, and the spec then blocks a PASS until the owner accepts the gap in writing (accepted by design).

Leave the `brainstorm` row of the section 3.1 table (line 142) and everything else in the spec as it is.

Acceptance criteria:
- The `**Nested propagation rule**` bullet in section 2.1 contains `only for a nested command that actually ran` and `7.2 step 4`.
- The section 7.2 step 4 line contains `lc10`, ``a `source: codebase` entry`` and ``neither `quality_tier` nor `source` records``.
- `git diff --stat -- .dev/orca-command-refactor/specs/orca-worker-contract-spec.md` shows two lines changed (two insertions, two deletions), and `git diff -U0` on that file shows hunks only at the section 2.1 bullet and the section 7.2 step 4 line.

## Phase 4: Dev copies and final checks

## Task 7: Sync the dev copies, run the affected tests and lint, and compare the tree against its starting state

Depends on: Task 1, Task 2, Task 3, Task 4, Task 5, Task 6

Run `make sync-dev` and then `make verify-sync` from the repository root so the gitignored copies under `.claude/` match `src/superclaude/`. Then run `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/skills/test_brainstorm_protocol.py tests/skills/test_worker_contract.py tests/skills/test_codegraph_adoption.py tests/skills/test_tier2_tavily_consistency.py tests/commands/test_routing_plugin_parity.py -q -p no:cacheprovider` and `make lint` (which runs `lint-architecture` and then `uv run ruff check .`). Save the outputs to `./artifacts/t7-sync.log`, `./artifacts/t7-pytest.log` and `./artifacts/t7-lint.log`, and save the output of `git status --porcelain` to `./artifacts/status-after.txt`. Do not edit any source file in this task; it writes only the logs and the status snapshot under `./artifacts/`.

Acceptance criteria:
- `./artifacts/t7-sync.log` shows `make sync-dev` and `make verify-sync` both exiting 0.
- `./artifacts/t7-pytest.log` shows the five test files passing with no failure, including `tests/skills/test_codegraph_adoption.py` and `tests/skills/test_tier2_tavily_consistency.py`, and `./artifacts/t7-lint.log` shows `make lint` exiting 0 with no new ruff finding in the two edited test files.
- Every line that is in `./artifacts/status-after.txt` and not in `./artifacts/status-before.txt` names one of the six files in Constraints or a path under this package's folder; no such line names a path under `.claude/` or `plugins/`; and every line of `./artifacts/status-before.txt` that names a path under `.dev/tasks/done/` is unchanged in `./artifacts/status-after.txt`.
```

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|---|---|---|---|
| Corrections F-1, F-7, F-11, F-14, F-15 (wording and placement) | Tasks 1, 2, 3, 6 | matched | plan Tasks 1 to 3 and 6 |
| Corrections F-16, F-17 and the open conflict (Constraints) | Constraints | matched, F-16 narrowed | plan Constraints |
