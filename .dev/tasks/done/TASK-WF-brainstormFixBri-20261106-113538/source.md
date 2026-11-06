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

Required change: Keep the general (companion) sentence in the 2.1 bullet (spec:62), ending with a pointer "brainstorm's live-check extra for this is in 7.2 step 4". Append the live-check sentence to 7.2 step 4 (spec:286, after "At P0, AC-0.4 replaces this step."). Replace Task 6's AC with: the 2.1 bullet contains `only for a nested command that actually ran` and `7.2 step 4`; the 7.2 step 4 line contains `lc10`, `` a `source: codebase` entry ``, `` neither `quality_tier` nor `source` records `` and `` invokes `sc:analyze` ``; `git diff --stat` on the spec shows two lines changed. Do not pin `session file` (the spec already holds it many times, INV-017(a)). Record the departure from src:9's literal second branch as a Necessary deviation, reason: 7.2 step 4 is where every later live plan attaches its step-4 extras (INV-021).

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

Owner amendment, 2026-11-06: the live-check sentence, residual risks 2 and 3, the new residual risk 5 and the F-7 pin `` invokes `sc:analyze` `` were amended after the review of the plan generated from the previous version of this brief (`.dev/reflect/pre-TASK-WF-brainstormFixBri-20261106-021737/REPORT.md`, findings M-01 to M-05). The texts below are the amended ones.

### Task 6 live-check sentence (goes into the spec, section 7.2 step 4)

A live-check extra for brainstorm's codebase-enrichment wave reads: "when the brief passes `--codebase`, or the contract's `domain` is `code`, `architecture` or `incident` and the brief does not pass `--no-codebase`, `enrichment_used` holds a `source: codebase` entry; every `nested/analyze-<n>/return-contract.yaml` that exists is listed in `artifacts`; a `nested/analyze-<n>/` directory is required, and must then hold its own `return-contract.yaml` with every `artifacts` entry under it existing, only when a `Skill` tool call (not a `Task` or `Agent` call whose prompt only names `/sc:analyze`) in the worker's session file or in one of its subagent files (7.2 step 5) invokes `sc:analyze` with `--report-dir <report directory>/nested/analyze-<n>/` and a number for `<n>` and returns no tool error, the `codebase` entry is not `skipped` (the per-source enrichment timeout records `skipped` and can stop `/sc:analyze` before it writes) and `/sc:analyze` did not refuse that directory, because neither `quality_tier` nor `source` records whether `/sc:analyze` ran; when the session file is not verifiable, this last clause is recorded `not verifiable`, never PASS" (P1 check lc10 is the origin of this rule).

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
2. The required-directory clause sees only a `Skill` tool call that invokes `sc:analyze`. The spec's nested propagation rule (spec:62) names the Skill tool, but how the session file records the invoked command, its arguments and a tool error is INFERRED from Claude Code's session format (spec:302 says only "`tool_use` blocks with a `name`"); a `/sc:analyze` run made another way, or recorded under another name, is missed and its missing folder passes.
3. The `skipped` carve-out also exempts an invoked `/sc:analyze` that wrote nothing and was recorded `skipped` for a reason other than the timeout, and, because `enrichment_used` holds one `codebase` entry, it exempts every `nested/analyze-<n>/` call of the run at once.
4. The required-folder clause depends on the session file; when it is missing or ambiguous the clause is `not verifiable`, and spec:300 then blocks a PASS until the owner accepts the gap in writing (accepted by design, INV-023).
5. An `artifacts` entry under a directory that is not required (a `skipped`, refused or tool-error call) is not checked for existence; Task 1's "also when the call failed" produces exactly this case.

## Part 5: extra constraints for the new plan

- Out of scope, open conflict: from phase P2 brainstorm's research enrichment also passes a nested report directory, and the research-deep fallback is itself a nested command. The corrected wording covers only the codebase-enrichment wave. Plan no change for the research wave. Add one line to the plan's Constraints stating this as an open conflict for the owner and the P2 live-plan author.
- The working tree already holds uncommitted edits to `src/superclaude/cli/install_core.py` and `tests/cli/test_how_we_work_install.py` that are not part of this work, and a staged archive of the earlier live plan under `.dev/tasks/done/`. The status check in Task 7 must compare a snapshot taken before Task 1 with one taken after, as correction F-2 says, so these baseline changes do not count.
- Edit only the six files named in the baseline plan's Constraints; the plugin copy `plugins/superclaude/commands/brainstorm.md` is not edited.
- Do not name a `src/superclaude/` path or an Orca command in any text that goes into an installed file (the skill, its refs, the command file).
- UV for every Python command: `uv run pytest ...` with `-p no:cacheprovider` and `PYTHONDONTWRITEBYTECODE=1`. No `superclaude install`. No git commit, push, merge or PR.
