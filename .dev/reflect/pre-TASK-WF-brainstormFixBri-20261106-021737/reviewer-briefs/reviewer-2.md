# Reviewer brief 2 (pre-execution plan audit, read-only)

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

### .dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-021737/source.md (spec body, whole file)

```markdown
Regenerate the implementation plan for the /sc:brainstorm nested-analyze wording fix, applying the review corrections in Parts 3 and 4. Plan only: do not implement, commit, push or open a PR.

## Part 1: the original brief (still binding)

Fix the /sc:brainstorm codebase-enrichment wording so that the nested analyze folder is only required when /sc:analyze was the scan that ran.

Background: the P1 live check lc10 (archived at .dev/tasks/done/TASK-WF-p1LivePlanBrief-20261105-164506/, see artifacts/lc10-result.md and artifacts/p1-owner-decisions-20261105.md) recorded a FAIL because the codebase-enrichment wave ran on quality_tier fallback_1 (codegraph search, Grep and Read, since the auggie MCP tool was not available in the worker session) and so no nested/analyze-1/ directory was written, while the live plan's extra expected one. The owner decided on 2026-11-05 that the check wording was wrong, not the worker: the nested analyze folder applies only when /sc:analyze was used, and the skill must say that the auggie tier and the fallback_1 tier (codegraph/Grep) write no nested folder.

Work to plan:
1. In src/superclaude/skills/sc-brainstorm-protocol/SKILL.md, the Wave 2A text at line 195 (Under --unattended) says the codebase row invokes /sc:analyze with --report-dir <report-dir>/nested/analyze-<n>/ and that the mcp__auggie__codebase-retrieval alternative writes no nested contract. Add the missing statement that the fallback_1 tier (codegraph, then native Glob/Grep, refs/handoff-routing.md Tier 2) also writes no nested folder and lists no nested contract in artifacts. Check src/superclaude/commands/brainstorm.md (its Unattended mode section near line 157) and refs/handoff-routing.md for the same gap, keeping them consistent.
2. Find every test that pins this wording (tests/skills/test_brainstorm_protocol.py line 44 and tests/skills/test_worker_contract.py near lines 292 and 711 reference nested/analyze-) and update or extend tests so the new sentence is pinned.
3. Run make sync-dev and make verify-sync (src/superclaude is the source of truth; never stage .claude/ paths) and check whether a plugins/superclaude mirror needs the same change.
4. Record the corrected live-check wording for future live plans: a step-4 extra for brainstorm must say that for the codebase-enrichment wave the directory nested/analyze-<n>/ exists only when /sc:analyze ran, and that a fallback_1 or auggie primary scan is recorded as the tier used with no nested folder. Put this where the P2 live plan author will find it, for example the live-check section of .dev/orca-command-refactor/specs/orca-worker-contract-spec.md if that is where per-command extras are defined, otherwise as a note in the P1 section of the same spec.
5. Run the affected tests with uv run pytest and make lint.

Constraints: no commit, push or PR; UV only; edits only in the files the plan names; the archived P1 packages under .dev/tasks/done/ stay untouched.

## Part 2: baseline plan and path aliases

A first plan was generated from the Part 1 brief and then reviewed by an independent Tier 2 review (three reviewers, a three-advocate debate, an evidence check). The review found it not ready to run. That plan is the baseline: `.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-001016/TASK-WF-brainstormFixBri-20261106-001016.md`. Read it, keep its structure (7 tasks in 4 phases: skill/command/routing wording, tests, spec note, sync and checks) and its constraints, and write a new plan that applies every correction below. The baseline plan file itself is read-only and is not edited.

The correction texts below use these short names for paths:

- `plan`: .dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-001016/TASK-WF-brainstormFixBri-20261106-001016.md (the baseline plan; line numbers refer to it)
- `src`: the Part 1 brief (line numbers refer to the brief as it appears in the baseline package's source.md)
- `spec`: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md
- `SKILL`: src/superclaude/skills/sc-brainstorm-protocol/SKILL.md
- `routing`: src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md
- `cmd`: src/superclaude/commands/brainstorm.md
- `diagnostics.txt`: .dev/reflect/pre-TASK-WF-brainstormFixBri-20261106-001016/artifacts/diagnostics.txt

## Part 3: corrections the new plan must apply

Apply all of them. The three P1 corrections come first in the plan's reasoning; the P2 ones follow. For each, the task acceptance criteria of the new plan must contain a check equivalent to its verifier.

### F-1 (P1): Task 6 live-check sentence decides the nested folder by quality_tier

Problem in the baseline plan: Task 6's live-check sentence ("a `primary` or `fallback_1` scan is recorded as the tier used, with no nested folder") decides the folder by `quality_tier`. Tier does not decide it: a clean `/sc:analyze` run is also `primary` (SKILL:187,198), and no field of `enrichment_used` names the tool (SKILL:372). A checker following it fails a correct analyze run, which is lc10 in reverse.

Where: .dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-001016/TASK-WF-brainstormFixBri-20261106-001016.md (Task 6, line 81)

Required change: Replace plan:81's second sentence with the exact sentence in "Replacement wording" (live-check sentence), and its first sentence with the companion sentence there. Record in the plan that both depart from src:9's sketch on purpose (Necessary deviation).
(In this card: replacement_wording.task6_live_check_sentence and replacement_wording.task6_companion_sentence.)

Verifier: The revised Task 6 no longer contains "a `primary` or `fallback_1` scan is recorded as the tier used"; it carries the live-check sentence and the companion sentence byte for byte as in replacement_wording; and the plan records the Necessary deviation from source.md:9.

### F-2 (P1): Task 7 bullet 3 cannot pass on today's tree

Problem in the baseline plan: Task 7 bullet 3 cannot pass: its first clause ("lists, among tracked paths, only the six files ... plus this package") fails on today's tree under any reading (950 staged `A` and 3 `R` under the archived P1 package; `git ls-files` = 953), and this package is untracked, so "plus this package" misdescribes it. The `.dev/tasks/done/` clause is reading-dependent. An infeasible AC reaches `E-HALT-QA`.

Where: .dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-001016/TASK-WF-brainstormFixBri-20261106-001016.md (Task 1 first step; Task 7, lines 93-98)

Required change: Task 1 gains a first step: before any edit, save `git status --porcelain` to `./artifacts/status-before.txt`. Task 7 saves `./artifacts/status-after.txt` and its bullet 3 becomes: "Every line that is in `./artifacts/status-after.txt` and not in `./artifacts/status-before.txt` names one of the six files in Constraints or a path under this package's folder; no such line names a path under `.claude/` or `plugins/`; and every line of `./artifacts/status-before.txt` that names a path under `.dev/tasks/done/` is unchanged in `./artifacts/status-after.txt`." The package-path exemption covers the `??` to `A` flip that `/sc:implement`'s `git add .dev/tasks` causes (INV-001).

Verifier: Task 1's first step writes ./artifacts/status-before.txt before any edit; Task 7 writes ./artifacts/status-after.txt; Task 7 bullet 3 reads exactly the quoted text; the "among tracked paths" clause of plan:98 is gone.

### F-3 (P1): Neither half of the owner rule is pinned in the three primitives

Problem in the baseline plan: The owner rule has two halves (src:6: the fallback tier "writes no nested folder and lists no nested contract in artifacts"). No planned pin covers the contract half, and the conditional "exists only when `/sc:analyze` ran" is pinned only in the spec. An implementer can drop either from the three primitives and every planned check stays green.

Where: .dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-001016/TASK-WF-brainstormFixBri-20261106-001016.md (Tasks 1-5)

Required change: Write Tasks 1-3 by the wording rule in "Replacement wording" and pin the shared phrases `no nested directory and no nested contract` and `` only by a `/sc:analyze` call `` in all three primitives (Task 4 for the skill and routing ref, Task 5 for the command file), as listed there.
Applied text (exact; copied from refactor-plan.md "Replacement wording"; also in replacement_wording.tasks_1_to_3_applied_text):
- **Task 1** (SKILL:195): replace everything after "(`<n>` starts at 1)" with: "; the `mcp__auggie__codebase-retrieval` alternative and the `fallback_1` tier (codegraph, then native Glob and Grep, `refs/handoff-routing.md` Tier 2) are unchanged and write no nested directory and no nested contract, so `nested/analyze-<n>/` is written only by a `/sc:analyze` call, and `enrichment_used` does not show whether it exists. The nested contract is listed in `artifacts`, also when the call failed." Task 1 AC: the paragraph contains `fallback_1`, `write no nested directory`, `nested/analyze-`, `skipped` and `` only by a `/sc:analyze` call ``; one line replaced.
- **Task 2** (routing): add one bullet as the last bullet of each codebase tier list (after routing:22 and after routing:31): "- Under `--unattended` this tier writes no nested directory and no nested contract; `nested/analyze-<n>/` is written only by a `/sc:analyze` call (the skill's other codebase action), and the scan is recorded in `enrichment_used` with this tier's `quality_tier`." `grep -c 'writes no nested directory'` still prints 2; two lines added, none deleted.
- **Task 3** (cmd:157): append to the `**Nested invocations.**` bullet: "A codebase scan through `mcp__auggie__codebase-retrieval` or through the `fallback_1` tier (codegraph, then Glob and Grep) is not a nested command and writes no nested directory and no nested contract, so `nested/analyze-<n>/` is written only by a `/sc:analyze` call; `enrichment_used` records the scan's tier, which does not show whether that directory exists." Leave "`adversarial_artifacts_dir` and the nested contracts are listed in `artifacts`" unchanged.
- **Task 4 pins**: in the paragraph slice (F-4): `fallback_1`, `write no nested directory and no nested contract`, `` only by a `/sc:analyze` call ``, and `Quality-tier tracking` absent; in each routing tier slice (F-5): `writes no nested directory and no nested contract` and `` only by a `/sc:analyze` call ``.
- **Task 5 pins**: add `writes no nested directory and no nested contract` and `` only by a `/sc:analyze` call `` to `UNATTENDED_EXPECT["brainstorm"]["phrases"]` (two new removed-token cases, F-8).

Verifier: Tasks 1-3 carry the applied text byte for byte; Task 4 and Task 5 list the two shared pins (in the file's own write/writes form); no applied text says "only for a command that ran" or states a tier for any /sc:analyze outcome.

### F-4 (P2): Task 4's section-wide fallback_1 assertion is vacuous; Task 1's paragraph clause is unpinned

Problem in the baseline plan: Task 4's new `fallback_1` assertion over the whole Wave 2A section passes on the old text (SKILL:199 holds `fallback_1` inside Wave 2A), contradicting plan:65. Task 1's paragraph clause is not vacuous (SKILL:195 lacks `fallback_1`) but is pinned by nothing.

Where: .dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-001016/TASK-WF-brainstormFixBri-20261106-001016.md (Task 4, lines 60-65)

Required change: Task 4 slices the paragraph that starts with the bold lead-in "Under `--unattended`" (up to the next blank line) and asserts `fallback_1`, `write no nested directory and no nested contract` and `` only by a `/sc:analyze` call `` in that slice, plus `"Quality-tier tracking" not in` the slice, so a slicer that returns the whole section fails (INV-005). Correct plan:65 to name the assertions that fail on the old text.

Verifier: Task 4 names the paragraph slice, the three pinned strings and the "Quality-tier tracking" absence check; plan:65 names which assertions fail on the old text.

### F-5 (P2): Routing-ref checks are file-wide, not one per codebase tier

Problem in the baseline plan: The routing-ref checks are file-wide: `grep -c ... prints 2` (plan:42) and "at least twice" (plan:60) pass with both copies in one tier or in the research tiers.

Where: .dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-001016/TASK-WF-brainstormFixBri-20261106-001016.md (Task 4, line 60; Task 2 AC, line 42)

Required change: Task 4 asserts each pinned phrase once in the Tier 1 slice (from the first `**Tier 1 (primary)**` to `**Tier 2 (fallback_1)**: codegraph`) and once in the Tier 2 slice (from there to `**Final fallback`), using the slicing pattern of `tests/skills/test_codegraph_adoption.py:56-59`. Keep the `grep -c` check as a smoke test (it still prints 2, INV-009).

Verifier: Task 4 names both tier slices with these anchors and the `_section` pattern; Task 2's `grep -c` AC is kept.

### F-6 (P2): Task 7 omits two tests that read the edited files

Problem in the baseline plan: Task 7's test set omits `tests/skills/test_codegraph_adoption.py` (reads SKILL, routing, both `brainstorm.md` copies; its Tier 2 slice test spans the Task 2 edit) and `tests/skills/test_tier2_tavily_consistency.py` (reads SKILL). The one extra file it runs, `tests/commands/test_routing_plugin_parity.py`, reads none of the edited files. The planned text breaks neither omitted test (read, not run), so this is a coverage gap, not a missed break.

Where: .dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-001016/TASK-WF-brainstormFixBri-20261106-001016.md (Task 7, lines 93 and 97)

Required change: Add both files to Task 7's pytest command and to its AC bullet 2.

Verifier: Task 7's pytest command and AC bullet 2 both name tests/skills/test_codegraph_adoption.py and tests/skills/test_tier2_tavily_consistency.py.

### F-7 (P2): Task 6 placement is not evaluated against the brief's rule

Problem in the baseline plan: Task 6 puts a brainstorm-specific live-check instruction inside the general 2.1 bullet, and the plan never records that it evaluated src:9's placement rule. Spec 7.2 and 7.3 define no per-command extras (spec:281-327).

Where: .dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-001016/TASK-WF-brainstormFixBri-20261106-001016.md (Task 6, lines 81-85)

Required change: Keep the general (companion) sentence in the 2.1 bullet (spec:62), ending with a pointer "brainstorm's live-check extra for this is in 7.2 step 4". Append the live-check sentence to 7.2 step 4 (spec:286, after "At P0, AC-0.4 replaces this step."). Replace Task 6's AC with: the 2.1 bullet contains `only for a nested command that actually ran` and `7.2 step 4`; the 7.2 step 4 line contains `lc10`, `` a `source: codebase` entry `` and `` neither `quality_tier` nor `source` records ``; `git diff --stat` on the spec shows two lines changed. Do not pin `session file` (the spec already holds it many times, INV-017(a)). Record the departure from src:9's literal second branch as a Necessary deviation, reason: 7.2 step 4 is where every later live plan attaches its step-4 extras (INV-021).

Verifier: Task 6 names both spec targets (2.1 bullet, 7.2 step 4), its AC lists exactly these pins and "two lines changed", does not pin `session file`, and records the Necessary deviation with the INV-021 reason.

### F-8 (P2): Task 5's collect-only check has no recorded baseline

Problem in the baseline plan: Task 5's "lists more cases than before the edit" has no recorded baseline.

Where: .dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-001016/TASK-WF-brainstormFixBri-20261106-001016.md (Task 5, line 75)

Required change: Task 5 first saves the `--collect-only -q -k brainstorm` output to `./artifacts/t5-collect-before.txt`; AC: the count after the edit equals the before-count plus the number of phrases added (2 under F-3). 17 is today's value (`diagnostics.txt:11`), not a constant; no AC hard-codes 18 or 19 (INV-008).

Verifier: Task 5 saves ./artifacts/t5-collect-before.txt before the edit and its AC states before-count plus 2; no AC in the plan contains a fixed 18 or 19.

### F-9 (P2): Task 2 misdescribes where the Tier 2 list ends

Problem in the baseline plan: Task 2 says each codebase tier list "ends with its `quality_tier` line"; the Tier 2 list ends with the Activation bullet (routing:31).

Where: .dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-001016/TASK-WF-brainstormFixBri-20261106-001016.md (Task 2, line 39)

Required change: Task 2 places the Tier 1 bullet after routing:22 and the Tier 2 bullet after the Activation bullet (routing:31), both before `**Final fallback` (routing:33), so the Tier 2 bullet stays inside the slice `test_codegraph_adoption.py:75-82` reads.

Verifier: Task 2 names both insertion points (after the Tier 1 quality_tier line, after the Tier 2 Activation bullet) and no longer says each list "ends with its quality_tier line".

### F-10 (P2): Stale line offsets in Tasks 4 and 5

Problem in the baseline plan: Stale offsets: Task 4 says the test is at line 37 (it is at 39); Task 5 says the phrase list is at line 286 (the entry starts at 286, the list at 288). The brief's line-711 reference is a synthetic-section mutation and needs no change.

Where: .dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-001016/TASK-WF-brainstormFixBri-20261106-001016.md (Task 4, line 60; Task 5, line 71)

Required change: Correct both numbers; add one line to Task 5 saying line 711 needs no change.

Verifier: Task 4 says line 39, Task 5 says the phrase list is at line 288, and Task 5 states that line 711 needs no change.

### F-11 (P2): Task 6 names the wrong spec section for line 142

Problem in the baseline plan: Task 6 calls spec line 142 "the `brainstorm` row of the section 6 table"; line 142 is in the section 3.1 table (spec:136-153), and section 6 starts at spec:215 (its brainstorm text is the P2 row, spec:222).

Where: .dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-001016/TASK-WF-brainstormFixBri-20261106-001016.md (Task 6, line 81)

Required change: Say "the `brainstorm` row of the section 3.1 table (line 142)".

Verifier: Task 6 says "section 3.1 table (line 142)" and no longer says "section 6 table".

### F-12 (P2): Verb forms write/writes are pinned separately per file

Problem in the baseline plan: `write no nested directory` (skill) is not a substring of `writes no nested directory` (routing, cmd), so each file is held to its own verb form.

Where: .dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-001016/TASK-WF-brainstormFixBri-20261106-001016.md (Tasks 1-5)

Required change: Covered by F-3: the shared pinned phrase `no nested directory and no nested contract` is a substring of both forms.

Verifier: Every pin added under F-3 contains `no nested directory and no nested contract`.

### F-13 (P2): Task 7 says it edits no file but writes logs

Problem in the baseline plan: Task 7 says "Do not edit any file in this task" but writes three logs under `./artifacts/`.

Where: .dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-001016/TASK-WF-brainstormFixBri-20261106-001016.md (Task 7, line 93)

Required change: Say "Do not edit any source file in this task; it writes only the logs under `./artifacts/`."

Verifier: Task 7 contains the quoted sentence and no longer says "Do not edit any file in this task".

### F-14 (P2): Task 1's 'listed only for a nested command that ran' can unlist a failed call's contract

Problem in the baseline plan: plan:30's new clause "a nested contract is listed in `artifacts` only for a nested command that ran" can be read as "succeeded" and would unlist a failed call's contract, which WC-4 writes on every outcome; cmd:157's unconditional "the nested contracts are listed in `artifacts`" is right.

Where: .dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-001016/TASK-WF-brainstormFixBri-20261106-001016.md (Task 1, line 30)

Required change: Drop the clause; keep the skill's unconditional sentence, extended to "The nested contract is listed in `artifacts`, also when the call failed." (Tasks 1-3 rule).

Verifier: Task 1 no longer contains "only for a nested command that ran" and its applied text ends with "The nested contract is listed in `artifacts`, also when the call failed."

### F-15 (P2): After Task 2 the routing ref implies codebase enrichment never nests

Problem in the baseline plan: After Task 2 both codebase tiers in the routing ref say "writes no nested directory" and the ref never names `/sc:analyze` (Tier 1 is auggie only), while Wave 2A loads only that ref section. A reader of the ref concludes codebase enrichment never nests.

Where: .dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-001016/TASK-WF-brainstormFixBri-20261106-001016.md (Task 2, line 39)

Required change: Task 2's bullet text is the one in "Replacement wording" (it names `/sc:analyze` as the only writer of `nested/analyze-<n>/`).

Verifier: Task 2's bullet text contains "is written only by a `/sc:analyze` call (the skill's other codebase action)".

### F-16 (P2): Uncommitted edits do not reach the next live plan

Problem in the baseline plan: The plan claims future live plans will see the fix, but it forbids commits (plan:24) and 7.2 builds each live-check worktree from a committed branch (spec:282). Until the owner commits and merges these edits, a P2 author on another branch sees neither the spec sentence nor the new skill text.

Where: .dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-001016/TASK-WF-brainstormFixBri-20261106-001016.md (Constraints, lines 17-24)

Required change: Add one line to Constraints: "The edits reach the next live plan only after the owner commits and merges them; this plan does not commit."

Verifier: Constraints contains the quoted line.

### F-17 (P2): Plugin-mirror decision is not recorded as the resolution of spec open item 8

Problem in the baseline plan: spec:443 (open item 8) says each phase's plan must resolve how the plugin command copies are kept in step before editing; plan:21 decides "not edited by this plan" but does not say it resolves item 8 for this change.

Where: .dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-001016/TASK-WF-brainstormFixBri-20261106-001016.md (Constraints, line 21)

Required change: Add to plan:21: "This is this plan's resolution of spec open item 8 for `brainstorm.md`."

Verifier: plan:21 contains the quoted sentence.

## Part 4: replacement wording (copy exactly, do not paraphrase)

### Task 6 live-check sentence (goes into the spec, section 7.2 step 4)

A live-check extra for brainstorm's codebase-enrichment wave reads: "when the brief passes `--codebase`, or the contract's `domain` is `code`, `architecture` or `incident` and the brief does not pass `--no-codebase`, `enrichment_used` holds a `source: codebase` entry; every `nested/analyze-` path listed in `artifacts` exists and holds its own `return-contract.yaml`, and every `nested/analyze-<n>/` directory that holds a `return-contract.yaml` is listed in `artifacts`; such a directory is required only when a `Skill`, `Agent` or `Task` tool call in the worker's session file or in one of its subagent files (7.2 step 5) passes `--report-dir <report directory>/nested/analyze-<n>/` with a number for `<n>`, the `codebase` entry is not `skipped` (the per-source enrichment timeout records `skipped` and can stop `/sc:analyze` before it writes) and `/sc:analyze` did not refuse that directory, because neither `quality_tier` nor `source` records whether `/sc:analyze` ran; when the session file is not verifiable, this last clause is recorded `not verifiable`, never PASS" (P1 check lc10 is the origin of this rule).

### Task 6 companion sentence (goes into the section 2.1 nested propagation rule bullet)

A nested directory `nested/<command>-<n>/` exists only for a nested command that actually ran, a run that failed included; a command that does the same work through a tool or a native-search fallback (brainstorm's codebase scan through `mcp__auggie__codebase-retrieval`, or through codegraph, then Glob and Grep) writes no nested directory and records the tier it used in its own contract, and brainstorm's live-check extra for this is in 7.2 step 4.

### Wording rule for Tasks 1 to 3

**Rule:** every "no nested directory" statement names its writer (the `mcp__auggie__codebase-retrieval` scan, the `fallback_1` tier of codegraph then native Glob and Grep), never a recorded `quality_tier` or a run; it says that `nested/analyze-<n>/` is written only by a `/sc:analyze` call and that `enrichment_used` does not show whether that directory exists; it states no tier for any `/sc:analyze` outcome and no step from a failed `/sc:analyze` to `fallback_1`; it uses the shared phrase `no nested directory and no nested contract`; and it keeps the nested contract listed in `artifacts` unconditionally, a failed call's included, never "only for a command that ran".

### Applied text and test pins for Tasks 1 to 5

- **Task 1** (SKILL:195): replace everything after "(`<n>` starts at 1)" with: "; the `mcp__auggie__codebase-retrieval` alternative and the `fallback_1` tier (codegraph, then native Glob and Grep, `refs/handoff-routing.md` Tier 2) are unchanged and write no nested directory and no nested contract, so `nested/analyze-<n>/` is written only by a `/sc:analyze` call, and `enrichment_used` does not show whether it exists. The nested contract is listed in `artifacts`, also when the call failed." Task 1 AC: the paragraph contains `fallback_1`, `write no nested directory`, `nested/analyze-`, `skipped` and `` only by a `/sc:analyze` call ``; one line replaced.
- **Task 2** (routing): add one bullet as the last bullet of each codebase tier list (after routing:22 and after routing:31): "- Under `--unattended` this tier writes no nested directory and no nested contract; `nested/analyze-<n>/` is written only by a `/sc:analyze` call (the skill's other codebase action), and the scan is recorded in `enrichment_used` with this tier's `quality_tier`." `grep -c 'writes no nested directory'` still prints 2; two lines added, none deleted.
- **Task 3** (cmd:157): append to the `**Nested invocations.**` bullet: "A codebase scan through `mcp__auggie__codebase-retrieval` or through the `fallback_1` tier (codegraph, then Glob and Grep) is not a nested command and writes no nested directory and no nested contract, so `nested/analyze-<n>/` is written only by a `/sc:analyze` call; `enrichment_used` records the scan's tier, which does not show whether that directory exists." Leave "`adversarial_artifacts_dir` and the nested contracts are listed in `artifacts`" unchanged.
- **Task 4 pins**: in the paragraph slice (F-4): `fallback_1`, `write no nested directory and no nested contract`, `` only by a `/sc:analyze` call ``, and `Quality-tier tracking` absent; in each routing tier slice (F-5): `writes no nested directory and no nested contract` and `` only by a `/sc:analyze` call ``.
- **Task 5 pins**: add `writes no nested directory and no nested contract` and `` only by a `/sc:analyze` call `` to `UNATTENDED_EXPECT["brainstorm"]["phrases"]` (two new removed-token cases, F-8).

### Residual risks of this wording (record them in the plan's notes, do not try to remove them)

No single sentence survives the probe with zero residual risk. This is the sentence with the smallest remaining risk: it has no known false FAIL on a correct run. Its exact residual risks, all in the false-PASS direction:
1. A `/sc:analyze` call made without the nested `--report-dir` (a broken propagation, itself a defect) is not seen, so its missing folder passes. Related: INV-022 (no live check can force the analyze route).
2. The call names `Skill`, `Agent` and `Task` are INFERRED from Claude Code's session format (spec:302 says only "`tool_use` blocks with a `name`"); a call through another tool name is missed and its missing folder passes.
3. The `skipped` carve-out also exempts an invoked `/sc:analyze` that wrote nothing and was recorded `skipped` for a reason other than the timeout.
4. The required-folder clause depends on the session file; when it is missing or ambiguous the clause is `not verifiable`, and spec:300 then blocks a PASS until the owner accepts the gap in writing (accepted by design, INV-023).

## Part 5: extra constraints for the new plan

- Out of scope, open conflict: from phase P2 brainstorm's research enrichment also passes a nested report directory, and the research-deep fallback is itself a nested command. The corrected wording covers only the codebase-enrichment wave. Plan no change for the research wave. Add one line to the plan's Constraints stating this as an open conflict for the owner and the P2 live-plan author.
- The working tree already holds uncommitted edits to `src/superclaude/cli/install_core.py` and `tests/cli/test_how_we_work_install.py` that are not part of this work, and a staged archive of the earlier live plan under `.dev/tasks/done/`. The status check in Task 7 must compare a snapshot taken before Task 1 with one taken after, as correction F-2 says, so these baseline changes do not count.
- Edit only the six files named in the baseline plan's Constraints; the plugin copy `plugins/superclaude/commands/brainstorm.md` is not edited.
- Do not name a `src/superclaude/` path or an Orca command in any text that goes into an installed file (the skill, its refs, the command file).
- UV for every Python command: `uv run pytest ...` with `-p no:cacheprovider` and `PYTHONDONTWRITEBYTECODE=1`. No `superclaude install`. No git commit, push, merge or PR.
```

### .dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-021737/TASK-WF-brainstormFixBri-20261106-021737.md (plan, whole file)

```markdown
---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-brainstormFixBri-20261106-021737
version: "1"
priority: Medium
created_date: "2026-11-06"
---

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
- `git show HEAD:src/superclaude/skills/sc-brainstorm-protocol/SKILL.md | grep -c 'write no nested directory and no nested contract'` and the same command for `refs/handoff-routing.md` with `writes no nested directory and no nested contract` both print 0, which shows the pins fail on the pre-change text.

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

### .dev/reflect/pre-TASK-WF-brainstormFixBri-20261106-021737/artifacts/coverage-matrix.yaml (whole file)

```text
# Pass 2 coverage matrix (deterministic containment rule, threshold 0.6; targets: Task 1..7 bodies plus the Constraints block as a pseudo-item)
parsed_rows: 0   # strict ID_REGEX (R-, REQ-, SPEC-, T-) finds no labelled ID; F-n and INV-n do not match
inferred_rows: 28
matched: 23
coverage_pct: null
coverage_pct_union: 0.8214
s_dev_density: 0.1786
rows:
  - {id: INF-001, line: 10, best_item: 'Task 1', ratio: 0.947, method: containment}
  - {id: INF-002, line: 11, best_item: 'Task 4', ratio: 0.588, method: none}
  - {id: INF-003, line: 12, best_item: 'Constraints', ratio: 0.684, method: containment}
  - {id: INF-004, line: 13, best_item: 'Task 6', ratio: 0.789, method: containment}
  - {id: INF-005, line: 14, best_item: 'Task 7', ratio: 1.0, method: containment}
  - {id: INF-006, line: 16, best_item: 'Constraints', ratio: 0.667, method: containment}
  - {id: INF-007, line: 42, best_item: 'Task 6', ratio: 0.562, method: none}
  - {id: INF-008, line: 53, best_item: 'Task 1', ratio: 0.667, method: containment}
  - {id: INF-009, line: 63, best_item: 'Task 4', ratio: 0.588, method: none}
  - {id: INF-010, line: 79, best_item: 'Task 4', ratio: 1.0, method: containment}
  - {id: INF-011, line: 89, best_item: 'Task 4', ratio: 0.867, method: containment}
  - {id: INF-012, line: 99, best_item: 'Task 6', ratio: 0.833, method: containment}
  - {id: INF-013, line: 109, best_item: 'Task 6', ratio: 0.6, method: containment}
  - {id: INF-014, line: 119, best_item: 'Task 5', ratio: 0.789, method: containment}
  - {id: INF-015, line: 129, best_item: 'Task 2', ratio: 0.769, method: containment}
  - {id: INF-016, line: 139, best_item: 'Task 5', ratio: 0.625, method: containment}
  - {id: INF-017, line: 149, best_item: 'Task 6', ratio: 0.833, method: containment}
  - {id: INF-018, line: 159, best_item: 'Constraints', ratio: 0.444, method: none}
  - {id: INF-019, line: 169, best_item: 'Task 7', ratio: 0.889, method: containment}
  - {id: INF-020, line: 179, best_item: 'Task 6', ratio: 0.667, method: containment}
  - {id: INF-021, line: 189, best_item: 'Task 1', ratio: 0.778, method: containment}
  - {id: INF-022, line: 199, best_item: 'Constraints', ratio: 0.571, method: none}
  - {id: INF-023, line: 209, best_item: 'Constraints', ratio: 0.857, method: containment}
  - {id: INF-024, line: 245, best_item: 'Constraints', ratio: 0.895, method: containment}
  - {id: INF-025, line: 246, best_item: 'Constraints', ratio: 1.0, method: containment}
  - {id: INF-026, line: 247, best_item: 'Constraints', ratio: 0.714, method: containment}
  - {id: INF-027, line: 248, best_item: 'Constraints', ratio: 0.917, method: containment}
  - {id: INF-028, line: 249, best_item: 'Constraints', ratio: 1.0, method: containment}
```

## Coverage slice

See the coverage-matrix hunk above (28 inferred rows, 23 matched by the containment rule, 5 below threshold). Audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding.
