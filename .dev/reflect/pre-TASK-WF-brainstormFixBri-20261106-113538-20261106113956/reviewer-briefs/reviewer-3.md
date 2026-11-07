# Reviewer brief 3 (refactorer lens, opus slot; pre-execution plan audit, read-only)

You audit the plan `.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/TASK-WF-brainstormFixBri-20261106-113538.md` against its brief `.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/source.md` (mode pre, UC-1). You are read-only: no edits, no shell, no git. Audit the hunks below and anything you Read, Grep or Glob in the repository. Persona focus: Structure and maintainability: are the six edits minimal, consistent across the three primitives and the spec, and free of drift between the plan, the brief and the files on disk? Look for wording that a later reader or test could misread, and for checks that are vacuous or brittle.

Return findings as YAML: a list of items with id, priority (P1 blocks /sc:implement or reproduces the lc10 false FAIL; P2 a defect a reviewer or test would catch; P3 cosmetic or an owner note), claim, evidence (file:line for every claim, or tag the claim [INFERRED]), exact_change and verifier; then self_reported_confidence (0-1) and a short list of what you checked and found clean. A zero-finding answer needs a self-audit naming what you checked.

## T1 card excerpt

Verbatim contents of reflection-card.yaml:

```yaml
card_version: "1.0"
mode: pre
subject: "Plan TASK-WF-brainstormFixBri-20261106-113538 (7 tasks, 4 phases), regenerated from the owner-amended brief (source.md, Parts 1 to 5, Part 4 amended 2026-11-06), checked against that brief"
claim: >
  The plan covers the five original brief items, applies all 17 corrections (F-1 to F-17) and carries the
  amended Part 4 texts byte for byte: the live-check sentence now requires the nested analyze folder only
  after an actual Skill call that invokes sc:analyze, and the five residual risks are recorded. Every
  correction's verifier string checks out against the plan, and every anchor the plan cites matches the
  files on disk today. No P1 or P2 defect was found; the remaining items are P3 notes and owner items
  carried over from the previous review.
self_reported_confidence: 0.90
blind_calibration: {calibrated_confidence: PENDING}
tier_routing: "Forced to Tier 2: strict Pass 1 finds no labelled ID (F-n and INV-n do not match ID_REGEX) and Pass 2 yields 45 inferred rows, so the parse-density guard (coverage_degraded: parsed-sparse) forbids the Tier 1 stop."
coverage:
  parsed_rows: 0
  inferred_rows: 45
  matched_by_containment_rule: 39
  coverage_pct: null
  coverage_pct_union: 0.8667
  s_dev_density: 0.1333
  rows_added_since_the_previous_review: "Part 2 (source.md:20), the Part 3 preamble (source.md:34) and every Part 4 text (source.md:215-244) are now rows, closing the previous review's note M-15."
  manual_review_of_the_6_unmatched_rows: "INF-002 (source.md:11, tests pin the wording) is covered by Tasks 4 and 5 together; INF-007 (source.md:20, keep 7 tasks in 4 phases) holds structurally; INF-008 (source.md:34, every AC carries its verifier) is checked row by row below; INF-020 (source.md:159, F-12) is covered by the shared pins in Tasks 4 and 5; INF-026 (source.md:215, the amendment note) is reflected in Constraints line 20; INF-035 (source.md:239, 'no known false FAIL') is stated in Task 6 (plan:133)."
  artifact: artifacts/coverage-matrix.yaml
grounded_checks_passed:
  - "Part 4 live-check sentence: plan:128 equals source.md:219 byte for byte; companion sentence plan:122 equals source.md:223 (grep -xF on the plan, both found)."
  - "Plan contains no 'a `Skill`, `Agent` or `Task` tool call' outside the Task 6 negative AC; 'invokes `sc:analyze`' appears in plan:128, plan:131, plan:135, plan:144."
  - "F-2: Task 7 bullet 3 (plan:158) equals the quoted text of source.md:53 (grep -cF = 1); 'among tracked paths', 'section 6 table' and 'Do not edit any file in this task' are absent (grep -c = 0)."
  - "F-13: plan:153 contains 'Do not edit any source file in this task; it writes only the logs under `./artifacts/`.' verbatim; F-16: plan:25 equals source.md:199's quoted line."
  - "F-8: no acceptance bullet contains 18 or 19; collect-only -k brainstorm reports 17/394 today (run 2026-11-06)."
  - "Anchors: SKILL.md:195 tail, :196 blank, :197 'Quality-tier tracking'; handoff-routing.md:16, 22, 24, 31, 33; brainstorm.md:157 ends 'so a nested directory is never reused.'; spec:62 and spec:286 ('4. Check the contract ... At P0, AC-0.4 replaces this step.') (artifacts/grounding.txt)."
  - "HEAD copies of SKILL.md, handoff-routing.md and brainstorm.md contain neither new pin (git show HEAD: ... | grep -c = 0 for both phrases), so the 'fails on pre-change text' ACs hold."
  - "/sc:implement keeps every write inside the package (sc-implement-protocol refs/managed-workspace.md:33-34), so Task 7 bullet 3 is not tripped by the executor."
findings:
  - id: F-1
    priority: P3
    claim: "Task 6's second AC adds a negative check ('does not contain a `Skill`, `Agent` or `Task` tool call') to the pins F-7 lists, and F-7's verifier asks that the AC list 'exactly these pins'. The extra check is useful (it tells the old sentence from the new one) but the departure is not recorded."
    evidence: "plan:144; source.md:109; source.md:111"
  - id: F-2
    priority: P3
    claim: "Task 7 still runs no format check on the two edited test files, while CI runs ruff format --check (carried over from the previous review, M-09)."
    evidence: "plan:153; plan:157; .github/workflows/test.yml:99"
  - id: F-3
    priority: P3
    claim: "Task 1's first AC still checks status-before.txt only for existence and order, with no checkable guard that it was taken before the first edit (carried over, M-11)."
    evidence: "plan:44"
  - id: F-4
    priority: P3
    claim: "Owner items carried over unchanged from the brief: research enrichment from P2 (Constraints, plan:26); no pointer for the P2 author to the new 7.2 step 4 sentence (INV-020); the routing bullet's 'with this tier's quality_tier' versus a timeout's 'skipped' (M-14); the 2.1 companion sentence states a rule for every command and its installed twin is not edited (M-13)."
    evidence: "plan:26; plan:54; plan:122; source.md:232; source.md:248"
risk_surface:
  blast_radius: "Documentation and test text only: six files, no runtime code. A wrong pin turns a test red; a wrong spec sentence misleads a live-plan author."
  interaction_effects: "Tasks 4 and 5 pin text written by Tasks 1 to 3 (Depends on lines). The shared phrase 'no nested directory and no nested contract' is a substring of both the skill's 'write' form and the ref and command's 'writes' form."
  amended_sentence_probe: "Checked by hand against the cases that broke the previous wording: a Task prompt that names /sc:analyze followed by an auggie or fallback_1 scan now requires no folder (no Skill call to sc:analyze); a Skill call to sc:analyze that fails after the directory is usable still requires the folder and its contract (analyze.md:98), which is the brief's 'a run that failed included' rule; a timed-out (skipped) or refused call requires none."
  residual_risks_recorded_in_plan: "Five false-PASS risks in Task 6 (plan:134-138), including the inferred session-file encoding of a Skill call."
recommendations:
  - id: R-1
    priority: P3
    file: "TASK-WF-brainstormFixBri-20261106-113538.md (Task 6 body, near plan:131)"
    change: "Add one clause recording that Task 6's AC adds a negative check beyond F-7's pin list, because the positive pins alone are shared by the old and new sentences."
    verifier: "Task 6 names the extra check and its reason."
  - id: R-2
    priority: P3
    file: "TASK-WF-brainstormFixBri-20261106-113538.md (Task 7 body and second AC)"
    change: "Add `uv run ruff format --check tests/skills/test_brainstorm_protocol.py tests/skills/test_worker_contract.py` to the commands logged in ./artifacts/t7-lint.log and to the second AC."
    verifier: "Task 7 body and its second AC both name ruff format --check."
unverified:
  - "How the session file records a Skill call's input (skill name and args) and a tool error (recorded as residual risk 2 in the plan)."
  - "make lint and the five test files were not run against the planned text; the text was read against them."
```

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-06T11:40:10Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P1 projectPath=/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P1 (the inputs are Markdown and test text; use Read/Grep/Glob for them)

### .dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/TASK-WF-brainstormFixBri-20261106-113538.md:1-158

````markdown
---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-brainstormFixBri-20261106-113538
version: "1"
priority: Medium
created_date: "2026-11-06"
---

# Brainstorm: nested analyze folder only when /sc:analyze ran (plan from the amended brief)

Source: ./source.md
Goal: `/sc:brainstorm` under `--unattended` says, in its skill, its command file and its routing ref, that the nested `analyze` directory is written only by a `/sc:analyze` call, and that the auggie scan and the `fallback_1` scan (codegraph, then Glob and Grep) write no nested directory and no nested contract. Tests pin both halves of that rule, and the worker-contract spec carries a live-check sentence that requires the folder only after an actual `Skill` call to `sc:analyze`, never by `quality_tier`.

## Constraints

- Background: the P1 live check lc10 failed because the codebase-enrichment wave ran on `quality_tier: fallback_1` (the auggie tool was not available in the worker session) and wrote no `nested/analyze-1/` directory, while the live plan expected one. The owner decided on 2026-11-05 that the check wording was wrong, not the worker. The archived record is in `.dev/tasks/done/TASK-WF-p1LivePlanBrief-20261105-164506/` (`artifacts/lc10-result.md`, `artifacts/p1-owner-decisions-20261105.md`); those files are read, never edited.
- This plan replaces two earlier plans for the same work, packages `TASK-WF-brainstormFixBri-20261106-001016` and `TASK-WF-brainstormFixBri-20261106-021737`. An independent review found the first not ready to run (its Task 6 wording decided the nested folder by `quality_tier`, its Task 7 status check could not pass on the current tree, and the owner rule was not fully pinned). A second review found that the second plan's live-check sentence required the folder whenever any `Skill`, `Agent` or `Task` call passed the flag text, so a `Task` prompt followed by an auggie or `fallback_1` scan would fail a correct run; the owner amended the brief's Part 4 on 2026-11-06 and this plan carries the amended text. Both earlier packages are left as they are.
- Edit only these six files: `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md`, `src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md`, `src/superclaude/commands/brainstorm.md`, `tests/skills/test_brainstorm_protocol.py`, `tests/skills/test_worker_contract.py` and `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. `make sync-dev` also rewrites the gitignored copies under `.claude/`; those are output, not edits, and are never staged.
- `src/superclaude/` is the source of truth. `plugins/superclaude/commands/brainstorm.md` is a copy that already differs from the `src` file, and no test requires the two to match (`tests/commands/test_routing_plugin_parity.py` covers only the `sc-recommend` skill). It is not edited. This is this plan's resolution of spec open item 8 for `brainstorm.md`. Task 7 confirms nothing under `plugins/` changed.
- No new text in the installed files (the skill, its refs, the command file) may name a `src/superclaude/` path or an Orca command; `tests/skills/test_worker_contract.py` (`_check_unattended_section`) fails on both.
- UV for every Python command: `uv run pytest ...`, `uv run python ...`. Test runs use `-p no:cacheprovider` and `PYTHONDONTWRITEBYTECODE=1`. No `superclaude install` (the owner updates the installed copies under `~/.claude/` later). No git commit, push, merge or PR.
- The edits reach the next live plan only after the owner commits and merges them; this plan does not commit.
- Open conflict, no change planned here: from phase P2 brainstorm's research enrichment also passes a nested report directory, and the research-deep fallback is itself a nested command. The corrected wording covers only the codebase-enrichment wave. This is an open conflict for the owner and the P2 live-plan author.
- Starting state: the working tree already holds uncommitted edits to `src/superclaude/cli/install_core.py` and `tests/cli/test_how_we_work_install.py` that are not part of this work, and a staged archive of the earlier live plan under `.dev/tasks/done/`. Task 1 records this state before any edit and Task 7 compares against it.

## Phase 1: Say it in the installed primitives

## Task 1: State in the skill that the auggie scan and the fallback tier write no nested directory

First, before any edit, save the output of `git status --porcelain` to `./artifacts/status-before.txt`. Task 7 compares against that file.

In `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md`, the Wave 2A paragraph whose bold lead-in is "Under `--unattended`" (line 195) currently ends: "The codebase row invokes `/sc:analyze` with `--unattended --report-dir <report-dir>/nested/analyze-<n>/` (`<n>` starts at 1); the `mcp__auggie__codebase-retrieval` alternative is unchanged and writes no nested contract. The nested contract is listed in `artifacts`." Replace everything after "(`<n>` starts at 1)" with this exact text, copied character for character:

```text
; the `mcp__auggie__codebase-retrieval` alternative and the `fallback_1` tier (codegraph, then native Glob and Grep, `refs/handoff-routing.md` Tier 2) are unchanged and write no nested directory and no nested contract, so `nested/analyze-<n>/` is written only by a `/sc:analyze` call, and `enrichment_used` does not show whether it exists. The nested contract is listed in `artifacts`, also when the call failed.
```

The wording names the writer (a tool or a tier), never a recorded `quality_tier` or a run. A clean `/sc:analyze` run is also `primary`, and `enrichment_used` records `source` and `quality_tier` as separate fields that do not name the tool, so a statement that depended on the tier would be wrong for an analyze run. It states no tier for any `/sc:analyze` outcome and keeps the nested contract listed unconditionally, a failed call's included. Change nothing else in the file.

Acceptance criteria:
- `./artifacts/status-before.txt` exists and was written before the first edit of this plan.
- The paragraph with the bold lead-in "Under `--unattended`" in the Wave 2A section of `SKILL.md` contains `fallback_1`, `write no nested directory and no nested contract`, ``only by a `/sc:analyze` call``, `nested/analyze-` and `skipped`, ends with "The nested contract is listed in `artifacts`, also when the call failed.", and does not contain "only for a nested command that ran".
- `git diff --stat -- src/superclaude/skills/sc-brainstorm-protocol/SKILL.md` shows one line changed (one insertion, one deletion).
- `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/skills/test_brainstorm_protocol.py -q -p no:cacheprovider` still passes before Task 4 changes the tests.

## Task 2: State the same rule in the routing ref for both codebase tiers

In `src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md`, the "Codebase enrichment" section has two tier lists. The list under `**Tier 1 (primary)**` (line 16) ends with the line `- quality_tier: ` followed by `primary` in backticks (line 22). The list under `**Tier 2 (fallback_1)**: codegraph, then native Glob/Grep` (line 24) ends with the line `- Activation: if Tier 1 returns error OR empty result` (line 31), and the line `**Final fallback**` (line 33) follows it. Add the bullet below, identical text, as the last bullet of each of the two lists: once after the Tier 1 `quality_tier` line, and once after the Tier 2 `Activation` line, both before the next `**Final fallback**` or `**Tier 2` anchor. The Tier 2 bullet must stay inside the span that `tests/skills/test_codegraph_adoption.py` reads in `test_brainstorm_tier2_names_codegraph_files_and_search` (from `**Tier 2 (fallback_1)**: codegraph` to the line starting `**Final fallback`).

```text
- Under `--unattended` this tier writes no nested directory and no nested contract; `nested/analyze-<n>/` is written only by a `/sc:analyze` call (the skill's other codebase action), and the scan is recorded in `enrichment_used` with this tier's `quality_tier`.
```

The bullet names `/sc:analyze` as the only writer so that a reader of this ref alone does not conclude that codebase enrichment never nests. Do not touch the research tiers (line 35 onward) or the `nested/adversarial-` text.

Acceptance criteria:
- `grep -c 'writes no nested directory' src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md` prints 2 (kept as a smoke check; Task 4 pins each tier separately).
- `git diff --stat -- src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md` shows two lines added and none deleted; one added bullet follows the Tier 1 `quality_tier` line and the other follows the Tier 2 `Activation` line.
- `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/skills/test_codegraph_adoption.py -q -p no:cacheprovider` passes with the edit in place.

## Task 3: State the same rule in the command file's Unattended mode section

In `src/superclaude/commands/brainstorm.md`, the `## Unattended mode` section has a bullet `**Nested invocations.**` (line 157) that says the `/sc:analyze` codebase enrichment receives `--unattended --report-dir <report-dir>/nested/analyze-<n>/`. Append this text to the end of that bullet, after "so a nested directory is never reused.", copied character for character:

```text
A codebase scan through `mcp__auggie__codebase-retrieval` or through the `fallback_1` tier (codegraph, then Glob and Grep) is not a nested command and writes no nested directory and no nested contract, so `nested/analyze-<n>/` is written only by a `/sc:analyze` call; `enrichment_used` records the scan's tier, which does not show whether that directory exists.
```

Leave the existing sentence "`adversarial_artifacts_dir` and the nested contracts are listed in `artifacts`" unchanged. Do not edit `plugins/superclaude/commands/brainstorm.md`.

Acceptance criteria:
- The `**Nested invocations.**` bullet of `src/superclaude/commands/brainstorm.md` contains `writes no nested directory and no nested contract` and ``only by a `/sc:analyze` call``, and still contains `nested/analyze-`, `nested/adversarial-` and "`adversarial_artifacts_dir` and the nested contracts are listed in `artifacts`".
- `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/skills/test_worker_contract.py -q -p no:cacheprovider` passes with the edit in place.
- `git diff --stat -- plugins` prints nothing.

## Phase 2: Pin the wording with tests

## Task 4: Pin the skill and routing-ref wording in test_brainstorm_protocol.py

Depends on: Task 1, Task 2

In `tests/skills/test_brainstorm_protocol.py`, the test `test_brainstorm_unattended_nested_directories_are_named` starts at line 39. It asserts `nested/analyze-` and `skipped` in the Wave 2A section (`_wave2a_section()`, line 44) and `nested/adversarial-` in `refs/handoff-routing.md` (line 47). Keep every existing assertion unchanged. Add a sibling test next to it, using the file's own helpers (`_wave2a_section`, `_BRAINSTORM`) and, for the routing ref, the slicing pattern of the `_section(text, start, end_pattern)` helper in `tests/skills/test_codegraph_adoption.py` (it splits the text at `start`, then splits the rest at `end_pattern` with `re.M` and keeps the first part). The new test asserts:

- Paragraph slice: take `_wave2a_section()`, split at the bold lead-in ``**Under `--unattended`**``, and keep the text up to the next blank line. The slice contains `fallback_1`, `write no nested directory and no nested contract` and ``only by a `/sc:analyze` call``, and the text `Quality-tier tracking` is not in it, so a slicer that returns the whole section fails.
- Tier slices of `refs/handoff-routing.md` (the file next to the SKILL file): the Tier 1 slice runs from the first `**Tier 1 (primary)**` to the line starting `**Tier 2 (fallback_1)**: codegraph`; the Tier 2 slice runs from there to the line starting `**Final fallback`. Each slice contains `writes no nested directory and no nested contract` exactly once and ``only by a `/sc:analyze` call`` exactly once.

All pins are exact substring checks. On the pre-change text every paragraph-slice pin and every tier-slice pin fails; only the `Quality-tier tracking` absence check passes there, because it guards the slice boundary and not the new wording.

Acceptance criteria:
- `tests/skills/test_brainstorm_protocol.py` contains the new sibling test with the paragraph-slice pins and both tier-slice pins above, and every earlier assertion of `test_brainstorm_unattended_nested_directories_are_named` is unchanged.
- `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/skills/test_brainstorm_protocol.py -q -p no:cacheprovider` passes.
- `git show HEAD:src/superclaude/skills/sc-brainstorm-protocol/SKILL.md | grep -c 'write no nested directory and no nested contract'` and `git show HEAD:src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md | grep -c 'writes no nested directory and no nested contract'` both print 0, and `git cat-file -e` exits 0 for both `HEAD:` paths, which shows the pins fail on the pre-change text.

## Task 5: Pin the command-file wording in test_worker_contract.py

Depends on: Task 3

In `tests/skills/test_worker_contract.py`, `UNATTENDED_EXPECT["brainstorm"]` is the entry that starts at line 286; its `phrases` list opens at line 288 and holds `research enrichment is off`, `exactly as passed`, `never reused`, `nested/analyze-`, `nested/adversarial-` and `dry-run`.

First, before editing, save the output of `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/skills/test_worker_contract.py -p no:cacheprovider --collect-only -q -k brainstorm` to `./artifacts/t5-collect-before.txt`. Today the summary line reports 17 collected cases, but that number is not a constant; the saved file is the baseline.

Then add the two phrases `writes no nested directory and no nested contract` and ``only by a `/sc:analyze` call`` to that `phrases` list. The removed-token tests (`_removals`, built from `UNATTENDED_EXPECT`) pick up both phrases and add one case for each; do not add a separate mutation by hand. The mutation list near line 711 (lines 704 to 724) rewrites a made-up section and does not read the real brainstorm text, so it needs no change.

Acceptance criteria:
- `UNATTENDED_EXPECT["brainstorm"]["phrases"]` in `tests/skills/test_worker_contract.py` contains `writes no nested directory and no nested contract` and ``only by a `/sc:analyze` call``.
- The collect-only command above, run again after the edit, reports a collected count equal to the count in `./artifacts/t5-collect-before.txt` plus 2; the plan does not hard-code that number.
- `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/skills/test_worker_contract.py -q -p no:cacheprovider` passes.
- `git show HEAD:src/superclaude/commands/brainstorm.md | grep -c 'writes no nested directory and no nested contract'` prints 0, which shows the new phrase fails on the pre-change command file.

## Phase 3: Record the corrected live-check wording

## Task 6: Add the corrected wording to the worker-contract spec in two places

In `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` make two edits, each on one existing line.

First, the section 2.1 bullet `**Nested propagation rule**` (line 62) ends with "Each command's `## Unattended mode` section names its nested invocations." Append this sentence to that line, copied character for character:

```text
A nested directory `nested/<command>-<n>/` exists only for a nested command that actually ran, a run that failed included; a command that does the same work through a tool or a native-search fallback (brainstorm's codebase scan through `mcp__auggie__codebase-retrieval`, or through codegraph, then Glob and Grep) writes no nested directory and records the tier it used in its own contract, and brainstorm's live-check extra for this is in 7.2 step 4.
```

Second, section 7.2 step 4 is the line that begins "4. Check the contract (PyYAML is a declared dependency" (line 286) and ends "At P0, AC-0.4 replaces this step." The fenced shell block for that step follows on the next lines and is not edited. Append this sentence to the end of the step 4 line, copied character for character:

```text
A live-check extra for brainstorm's codebase-enrichment wave reads: "when the brief passes `--codebase`, or the contract's `domain` is `code`, `architecture` or `incident` and the brief does not pass `--no-codebase`, `enrichment_used` holds a `source: codebase` entry; every `nested/analyze-<n>/return-contract.yaml` that exists is listed in `artifacts`; a `nested/analyze-<n>/` directory is required, and must then hold its own `return-contract.yaml` with every `artifacts` entry under it existing, only when a `Skill` tool call (not a `Task` or `Agent` call whose prompt only names `/sc:analyze`) in the worker's session file or in one of its subagent files (7.2 step 5) invokes `sc:analyze` with `--report-dir <report directory>/nested/analyze-<n>/` and a number for `<n>` and returns no tool error, the `codebase` entry is not `skipped` (the per-source enrichment timeout records `skipped` and can stop `/sc:analyze` before it writes) and `/sc:analyze` did not refuse that directory, because neither `quality_tier` nor `source` records whether `/sc:analyze` ran; when the session file is not verifiable, this last clause is recorded `not verifiable`, never PASS" (P1 check lc10 is the origin of this rule).
```

Placement and wording are a Necessary deviation from the brief, recorded here. The brief allows either the live-check section or a note in the P1 rows, and sketches the wording as "a fallback_1 or auggie primary scan is recorded as the tier used with no nested folder". This plan puts the live-check sentence in 7.2 step 4 because every later live plan attaches its step-4 extras there, and sections 7.2 and 7.3 hold no per-command extras list of their own, so the P2 live-plan author reads 7.2 step 4. The wording departs from the sketch because tier does not decide whether the folder must exist: a clean `/sc:analyze` run is also `primary`, and neither `quality_tier` nor `source` names the tool. The trigger is an actual `Skill` call that invokes `sc:analyze`, because a `Task` or `Agent` prompt that only names the command can be followed by an auggie or `fallback_1` scan that writes no folder.

Residual risks of the live-check sentence are left in place on purpose; all are in the false-PASS direction, and the sentence has no known false FAIL on a correct run:
- A `/sc:analyze` call made without the nested `--report-dir` (a broken propagation, itself a defect) is not seen, so its missing folder passes; no live check can force the analyze route.
- The required-directory clause sees only a `Skill` tool call that invokes `sc:analyze`; the spec's nested propagation rule names the Skill tool, but how the session file records the invoked command, its arguments and a tool error is inferred from Claude Code's session format (the spec says only that the session file records `tool_use` blocks with a `name`); a `/sc:analyze` run made another way, or recorded under another name, is missed and its missing folder passes.
- The `skipped` carve-out also exempts an invoked `/sc:analyze` that wrote nothing and was recorded `skipped` for a reason other than the timeout, and, because `enrichment_used` holds one `codebase` entry, it exempts every `nested/analyze-<n>/` call of the run at once.
- The required-folder clause depends on the session file; when it is missing or ambiguous the clause is `not verifiable`, and the spec then blocks a PASS until the owner accepts the gap in writing (accepted by design).
- An `artifacts` entry under a directory that is not required (a `skipped`, refused or tool-error call) is not checked for existence; Task 1's "also when the call failed" produces exactly this case.

Leave the `brainstorm` row of the section 3.1 table (line 142) and everything else in the spec as it is.

Acceptance criteria:
- The `**Nested propagation rule**` bullet in section 2.1 contains `only for a nested command that actually ran` and `7.2 step 4`.
- The section 7.2 step 4 line contains `lc10`, ``a `source: codebase` entry``, ``neither `quality_tier` nor `source` records`` and ``invokes `sc:analyze` ``, and does not contain ``a `Skill`, `Agent` or `Task` tool call``.
- `git diff --stat -- .dev/orca-command-refactor/specs/orca-worker-contract-spec.md` shows two lines changed (two insertions, two deletions), and `git diff -U0` on that file shows hunks only at the section 2.1 bullet and the section 7.2 step 4 line.

## Phase 4: Dev copies and final checks

## Task 7: Sync the dev copies, run the affected tests and lint, and compare the tree against its starting state

Depends on: Task 1, Task 2, Task 3, Task 4, Task 5, Task 6

Run `make sync-dev` and then `make verify-sync` from the repository root so the gitignored copies under `.claude/` match `src/superclaude/`. Then run `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/skills/test_brainstorm_protocol.py tests/skills/test_worker_contract.py tests/skills/test_codegraph_adoption.py tests/skills/test_tier2_tavily_consistency.py tests/commands/test_routing_plugin_parity.py -q -p no:cacheprovider` and `make lint` (which runs `lint-architecture` and then `uv run ruff check .`). Save the outputs to `./artifacts/t7-sync.log`, `./artifacts/t7-pytest.log` and `./artifacts/t7-lint.log`, and save the output of `git status --porcelain` to `./artifacts/status-after.txt`. Do not edit any source file in this task; it writes only the logs under `./artifacts/`. The status snapshot `./artifacts/status-after.txt` is the one non-log file it writes there, and `make sync-dev` rewrites the gitignored copies under `.claude/` (output, not edits).

Acceptance criteria:
- `./artifacts/t7-sync.log` shows `make sync-dev` and `make verify-sync` both exiting 0.
- `./artifacts/t7-pytest.log` shows the five test files passing with no failure, including `tests/skills/test_codegraph_adoption.py` and `tests/skills/test_tier2_tavily_consistency.py`, and `./artifacts/t7-lint.log` shows `make lint` exiting 0 with no new ruff finding in the two edited test files.
- Every line that is in `./artifacts/status-after.txt` and not in `./artifacts/status-before.txt` names one of the six files in Constraints or a path under this package's folder; no such line names a path under `.claude/` or `plugins/`; and every line of `./artifacts/status-before.txt` that names a path under `.dev/tasks/done/` is unchanged in `./artifacts/status-after.txt`.
````

### src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:181-200

```markdown
**Behavioral Instructions**:

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
```

### src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:368-390

````markdown
adversarial_artifacts_dir: <path> | null
domain: code | architecture | product | process | incident | research
proposal_count: <int>
enrichment_used:
  - source: codebase | research-light | research-deep
    quality_tier: primary | fallback_1 | skipped
handoff_action: none | design | tasklist | task
handoff_output_path: <path> | null
unresolved_conflicts: [<list of strings>]
```

### Worker fields (only with `--unattended`)

Added beside the fields above in `<output>/return-contract.yaml` (with `--report-dir`: written to `<report-dir>/return-contract.yaml`, which lists the own contract in `artifacts`), on every outcome:

```yaml
worker_contract_version: "1"
worker_status: succeeded | partial | failed
command: <the exact command line>
report_path: <output>/merged-requirements.md | null   # null when the merge was not reached, and on dry-run
artifacts: [<every other file written, adversarial_artifacts_dir, the nested contracts>]
reason: <the STOP or refused flag>                     # only when failed
```
````

### src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md:12-35

```markdown

- `domain ∈ {code, architecture, incident}` AND NOT `--no-codebase`, OR
- `--codebase` (forced) regardless of domain

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

### src/superclaude/commands/brainstorm.md:150-159

```markdown
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

### .dev/orca-command-refactor/specs/orca-worker-contract-spec.md:58-63

```markdown
- **Report directory**: the directory that holds the worker contract (WC-4). Under `--unattended` the brief passes exactly one: either the command's own existing directory-valued output flag (`--output <dir>` or `--output-dir <dir>`), or the new flag `--report-dir <dir>` (for a command without such a flag, or a brief that does not pass it). An output flag a section 3 row adds is file-valued, so those commands always take `--report-dir`. Passing neither, or both, is refused before any work (WC-4, last sentences).
- **Contract file**: one shared document, proposed as `src/superclaude/core/WORKER-CONTRACT.md`, installed to `~/.claude/WORKER-CONTRACT.md`. Core `.md` files install to `~/.claude/`: the installer copies every `*.md` in `core/` (`src/superclaude/cli/install_core.py:36,56,65-70`; `CLAUDE.md:83,408`). The new name is also added to `KNOWN_CORE_FILES` (`src/superclaude/cli/install_core.py:13-27`), which only controls which installed files `list_installed_core_files` reports (`install_core.py:12,155`); installation itself is checked by AC-0.1. The file holds the command-side rules (WC-2, WC-4, WC-8 to WC-11, the flag parse rule, the person-mode refusal above and the nested propagation rule below), the worker session's brief guard and the never-as-worker list below, and the coordinator's rules (WC-6 and section 2.3, including its brief template and the template's guard line). For the worker-session duties (WC-3, WC-5, WC-7, WC-12, WC-13 and heartbeats) it states only the IronClaude-specific rule (outcome mapping from `worker_status`, including WC-5's P0 brief override, top-level only, ask only when the brief allows it) and points to the dispatch preamble as the authority for Orca verb syntax and heartbeat cadence; it never copies them, because the preamble is issued per dispatch by the running Orca version (`CAPS:130`). Each changed command adds a short `## Unattended mode` section that lists only its own gate resolutions and report file and points to the installed contract path, so the shared rules are written once.
- **Brief guard** (worker session, from P1): it applies only in a session whose current prompt carries a live Orca preamble with Task and Dispatch IDs (see "Worker run"). Before invoking anything, the worker checks every `Command:` line of its brief (section 2.3, "Brief layout"), and only those lines. It decides case 3 from the command name alone. For the other cases it reads, as plain files, every existing copy of the command file: the project `.claude/commands/sc/<name>.md` in its worktree and `~/.claude/commands/sc/<name>.md`. It refuses, runs nothing, writes no contract, and sends `worker_done --outcome failed` with no `--report-path` and a body starting `guard refused:` when: (case 1) every existing copy has an `## Unattended mode` section and the line lacks a standalone `--unattended` (`guard refused: brief lacks --unattended`); (case 2) no existing copy has the section and the line has the flag (`guard refused: loaded command has no Unattended mode section (not converted at this phase, or the loaded copy is stale)`); the copies disagree (`guard refused: command copies disagree (stale copy): <paths>`); (case 3) the command is on the never-as-worker list. A command invoked by another command, through the Skill tool or the Agent tool, is never checked; the nested propagation rule governs it. The guard checks once, before the first run: a WC-3 re-invocation keeps every token of the brief's `Command:` line, `--unattended` included, and only adds the answer.
- **Never-as-worker list**: `/sc:agent`, `/sc:git`, `/sc:help`, `/sc:pm`, `/sc:spawn` and `/sc:swarm-wizard` (section 4), plus `/sc:pr-submit` while the answer to D3 keeps it off workers. The list changes only when section 4 or D3 changes, never per phase. If D3 adds a worker route for pr-submit, D3 also states how that route passes the brief guard.
- **Nested propagation rule**: under `--unattended`, a command that invokes another `/sc:` command or protocol skill, through the Skill tool or the Agent tool, passes `--unattended` when the invoked command accepts it at this phase, together with its own report directory `<caller report-dir>/nested/<command>-<n>/` (WC-4, WC-11). The caller lists the nested contract in its `artifacts`; only the top-level contract drives WC-5. When the invoked command does not accept the flag yet, that step must be gate-free per its section 3 row, or the caller skips it under `--unattended` and records the skip in its contract. Each command's `## Unattended mode` section names its nested invocations.

```

### .dev/orca-command-refactor/specs/orca-worker-contract-spec.md:281-304

````markdown
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
````

### .dev/tasks/done/TASK-WF-p1LivePlanBrief-20261105-164506/artifacts/lc10-result.md:1-17

```markdown
# lc10 result: /sc:brainstorm

- Worktree setup: PASS (`lc10-worktree.json`, `lc10-branch.txt` = ironbelly/p1-live-brainstorm, `lc10-sync-dev.txt`, `lc10-status-before.txt`; worktree HEAD equals `branch-tip.txt`)
- Section check: PASS (`lc10-unattended-check.txt`: brainstorm.md:1 brainstorm.md:1)
- Step 1: PASS (`lc10-step1.txt`: state ready, 38.505 s)
- Step 2: PASS (`lc10-step2-samples.txt`: 4 sample(s), all agentWait=null)
- Step 3: PASS (`lc10-step3.json`: 1 worker_done, outcome `succeeded` vs contract worker_status `partial`; report path `.dev/p1-live/brainstorm/return-contract.yaml` vs `.dev/p1-live/brainstorm/return-contract.yaml`; acknowledged in `lc10-step3-ack.json`)
- Step 4: PASS (`lc10-step4.txt`). Extra: FAIL. Extra as written FAILS in part. Holds: the contract keeps the command's own fields beside the worker fields (`contract_version`, `status: partial`, `seed_brief_path`, `merged_output_path`, `convergence_score`, `enrichment_used`, ...); research enrichment is recorded as skipped (`research-light` and `research-deep`, `quality_tier: skipped`); the adversarial wave ran and `nested/adversarial-1/` exists with its own `return-contract.yaml` and is listed in `artifacts`. Does not hold: the codebase-enrichment wave ran (`enrichment_used`: `codebase`, `quality_tier: fallback_1`, output `enrichment/codebase-context.md`) but no `nested/analyze-1/` directory exists, because the worker did not call `/sc:analyze`: the contract says the auggie retrieval tool was not available and codegraph search, Grep and Read were used. The skill (`sc-brainstorm-protocol/SKILL.md:195`) says the auggie alternative "writes no nested contract" and does not say what the fallback tier writes, so the plan's wording and the skill differ here; recorded as a finding for the phase report.
- Step 5: PASS (`lc10-step5.md`)
- Step 6: PASS (`lc10-step6.md`, `lc10-status-after.txt`, `lc10-index-after.txt`)
- Step 7: PASS (`lc10-step7.txt`)
- Remove: PASS (`lc10-remove.json`, `lc10-worktree-list-after.json`, `lc10-head-after.txt`, `lc10-branch-after.txt`)
- Step 5 condition 2 also covers the nested calls: the session file holds two top-level Skill calls (`sc:brainstorm-protocol` at 19:53:39.9 and, made by the command, `sc:adversarial-protocol` at 19:55:18.0), both with sidechain False; no nested `/sc:analyze` call was made. The run lasted 13.9 min (longer than the 5-minute heartbeat cadence); it is a checked run longer than the cadence for owner decision H1.

Overall verdict: FAIL

Recording status: complete (verdict recorded, not a task failure)
```

### tests/skills/test_brainstorm_protocol.py:1-48

```python
"""Drift guard for the sc:brainstorm protocol (Cluster C4).

The Wave-2A enrichment matrix must ROUTE to the research engine only — it must not
duplicate Tavily params or name the map/crawl tools (X5/X6). CI-safe.
"""

import re
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
_BRAINSTORM = (
    _REPO / "src" / "superclaude" / "skills" / "sc-brainstorm-protocol" / "SKILL.md"
)

_FORBIDDEN = [
    "search_depth:",
    "extract_depth:",
    "max_results:",
    "tavily-map",
    "tavily-crawl",
]


def _wave2a_section() -> str:
    text = _BRAINSTORM.read_text(encoding="utf-8")
    parts = re.split(r"###\s*Wave 2A", text, maxsplit=1)
    assert len(parts) == 2, "brainstorm SKILL missing the 'Wave 2A' section"
    # Up to the next '### Wave ' heading.
    return re.split(r"\n###\s*Wave ", parts[1], maxsplit=1)[0]


def _wave_section(n: str) -> str:
    text = _BRAINSTORM.read_text(encoding="utf-8")
    parts = re.split(rf"###\s*Wave {n}\b", text, maxsplit=1)
    assert len(parts) == 2, f"brainstorm SKILL missing the 'Wave {n}' section"
    return re.split(r"\n###\s*Wave ", parts[1], maxsplit=1)[0]


def test_brainstorm_unattended_nested_directories_are_named():
    """Under --unattended the nested calls get their own directories (P1 worker contract)."""
    wave3 = _wave_section("3")
    assert "--unattended" in wave3 and "nested/adversarial-" in wave3
    wave2a = _wave2a_section()
    assert "nested/analyze-" in wave2a and "skipped" in wave2a
    assert "exactly as passed" in _wave_section("0")
    refs = _BRAINSTORM.parent / "refs" / "handoff-routing.md"
    assert "nested/adversarial-" in refs.read_text(encoding="utf-8")

```

### tests/skills/test_worker_contract.py:284-297

```python
        "nested": [],
    },
    "brainstorm": {
        "flags": ["--output", "-o", "--interactive", "-i"],
        "phrases": [
            "research enrichment is off",
            "exactly as passed",
            "never reused",
            "nested/analyze-",
            "nested/adversarial-",
            "dry-run",
        ],
        "nested": ["analyze", "adversarial"],
    },
```

### tests/skills/test_worker_contract.py:704-724

```python
@pytest.mark.parametrize(
    "mutate",
    [
        lambda s: s.replace("return-contract.yaml", "the-file"),
        lambda s: s.replace("~/.claude/WORKER-CONTRACT.md", "the-contract"),
        lambda s: s.replace("--report-dir", "--dir"),
        lambda s: s.replace("alpha-gate", "beta"),
        lambda s: s.replace("nested/analyze-", "nested/other-"),
        lambda s: s + "See src/superclaude/skills/x.\n",
        lambda s: s + "Then run orca worktree create.\n",
    ],
    ids=[
        "no-contract-file",
        "no-contract-path",
        "no-report-dir",
        "no-phrase",
        "no-nested-name",
        "src-path",
        "orca-name",
    ],
)
```

### tests/skills/test_codegraph_adoption.py:52-83

```python
def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _section(text: str, start: str, end_pattern: str) -> str:
    after = text.split(start, 1)
    assert len(after) == 2, f"missing anchor {start!r}"
    return re.split(end_pattern, after[1], maxsplit=1, flags=re.M)[0]


def _rel(path: Path) -> str:
    return str(path.relative_to(_REPO))


def test_validate_roadmap_step05_puts_codegraph_above_grep_and_never_skips():
    step = _section(_text(_VR_SKILL), "#### Step 0.5", r"^#### |^### ")
    assert "codegraph_search" in step and "Grep" in step
    assert step.index("codegraph_search") < step.index("call `Grep` for its definition")
    assert "skip" not in step.lower(), (
        "Step 0.5 must never skip where the Grep floor exists"
    )


def test_brainstorm_tier2_names_codegraph_files_and_search():
    tier2 = _section(
        _text(_BS_ROUTING), "**Tier 2 (fallback_1)**: codegraph", r"^\*\*Final fallback"
    )
    assert "codegraph_files" in tier2 and "codegraph_search" in tier2
    assert "Glob for files matching topic keywords" in tier2, (
        "native Glob/Grep floor must stay"
    )

```

(The full brief is at .dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/source.md; Read it as needed.)


## Coverage slice

Verbatim contents of artifacts/coverage-matrix.yaml (all rows; every reviewer owns the whole plan, each from its own lens):

```yaml
# Pass 2 coverage matrix (deterministic containment rule, threshold 0.6; targets: Task 1..7 bodies plus the Constraints block)
# Quote = first two sentences of the cited source.md line; stopwords stripped, case folded.
parsed_rows: 0   # strict ID_REGEX (R-, REQ-, SPEC-, T-) outside code fences
inferred_rows: 45
matched: 39
coverage_pct: null
coverage_pct_union: 0.8667
s_dev_density: 0.1333
rows:
  - {id: INF-001, line: 10, best_item: 'Task 1', ratio: 0.970, method: containment}
  - {id: INF-002, line: 11, best_item: 'Constraints', ratio: 0.593, method: none}
  - {id: INF-003, line: 12, best_item: 'Constraints', ratio: 0.739, method: containment}
  - {id: INF-004, line: 13, best_item: 'Task 6', ratio: 0.871, method: containment}
  - {id: INF-005, line: 14, best_item: 'Task 7', ratio: 1.000, method: containment}
  - {id: INF-006, line: 16, best_item: 'Constraints', ratio: 0.765, method: containment}
  - {id: INF-007, line: 20, best_item: 'Constraints', ratio: 0.550, method: none}
  - {id: INF-008, line: 34, best_item: 'Constraints', ratio: 0.417, method: none}
  - {id: INF-009, line: 42, best_item: 'Task 6', ratio: 0.654, method: containment}
  - {id: INF-010, line: 53, best_item: 'Task 7', ratio: 0.776, method: containment}
  - {id: INF-011, line: 63, best_item: 'Constraints', ratio: 0.679, method: containment}
  - {id: INF-012, line: 79, best_item: 'Task 4', ratio: 0.778, method: containment}
  - {id: INF-013, line: 89, best_item: 'Task 4', ratio: 0.737, method: containment}
  - {id: INF-014, line: 99, best_item: 'Task 6', ratio: 0.778, method: containment}
  - {id: INF-015, line: 109, best_item: 'Task 6', ratio: 0.750, method: containment}
  - {id: INF-016, line: 119, best_item: 'Task 5', ratio: 0.615, method: containment}
  - {id: INF-017, line: 129, best_item: 'Task 2', ratio: 0.774, method: containment}
  - {id: INF-018, line: 139, best_item: 'Task 5', ratio: 0.667, method: containment}
  - {id: INF-019, line: 149, best_item: 'Task 6', ratio: 0.778, method: containment}
  - {id: INF-020, line: 159, best_item: 'Constraints', ratio: 0.583, method: none}
  - {id: INF-021, line: 169, best_item: 'Constraints', ratio: 0.727, method: containment}
  - {id: INF-022, line: 179, best_item: 'Constraints', ratio: 0.647, method: containment}
  - {id: INF-023, line: 189, best_item: 'Task 1', ratio: 0.769, method: containment}
  - {id: INF-024, line: 199, best_item: 'Constraints', ratio: 0.824, method: containment}
  - {id: INF-025, line: 209, best_item: 'Constraints', ratio: 0.833, method: containment}
  - {id: INF-026, line: 215, best_item: 'Constraints', ratio: 0.595, method: none}
  - {id: INF-027, line: 219, best_item: 'Task 6', ratio: 1.000, method: containment}
  - {id: INF-028, line: 223, best_item: 'Task 6', ratio: 1.000, method: containment}
  - {id: INF-029, line: 227, best_item: 'Task 1', ratio: 0.900, method: containment}
  - {id: INF-030, line: 231, best_item: 'Task 1', ratio: 0.966, method: containment}
  - {id: INF-031, line: 232, best_item: 'Task 2', ratio: 0.979, method: containment}
  - {id: INF-032, line: 233, best_item: 'Task 3', ratio: 0.957, method: containment}
  - {id: INF-033, line: 234, best_item: 'Task 4', ratio: 0.964, method: containment}
  - {id: INF-034, line: 235, best_item: 'Task 5', ratio: 0.944, method: containment}
  - {id: INF-035, line: 239, best_item: 'Task 6', ratio: 0.500, method: none}
  - {id: INF-036, line: 240, best_item: 'Task 6', ratio: 1.000, method: containment}
  - {id: INF-037, line: 241, best_item: 'Task 6', ratio: 1.000, method: containment}
  - {id: INF-038, line: 242, best_item: 'Task 6', ratio: 1.000, method: containment}
  - {id: INF-039, line: 243, best_item: 'Task 6', ratio: 0.870, method: containment}
  - {id: INF-040, line: 244, best_item: 'Task 6', ratio: 1.000, method: containment}
  - {id: INF-041, line: 248, best_item: 'Constraints', ratio: 0.920, method: containment}
  - {id: INF-042, line: 249, best_item: 'Constraints', ratio: 0.775, method: containment}
  - {id: INF-043, line: 250, best_item: 'Constraints', ratio: 0.733, method: containment}
  - {id: INF-044, line: 251, best_item: 'Constraints', ratio: 0.929, method: containment}
  - {id: INF-045, line: 252, best_item: 'Constraints', ratio: 1.000, method: containment}
```
