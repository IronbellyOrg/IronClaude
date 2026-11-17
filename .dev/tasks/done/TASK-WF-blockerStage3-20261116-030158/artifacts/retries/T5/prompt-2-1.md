0efb510d1c8e6ece4cde589ce2b6d19e43fb5f7a
Review one task for spec compliance.

Task brief: Task 5 of the plan .dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/TASK-WF-blockerStage3-20261116-030158.md (AC ids T5.AC1 to T5.AC5 in source order).
## Task 5: Rewrite rf-qa-qualitative.md and apply OD16

Depends on: Task 1, Task 3

First read that `pragmatic.md` holds the new position 1 wording and that `src/superclaude/agents/rf-qa-qualitative.md` no longer holds "Blocking is a real defect"; stop without editing when either fails. Edit `src/superclaude/agents/rf-qa-qualitative.md` with the same removals and additions as Task 4:

- Replace the merge rule (today line 84) with the L1 text of Task 4.
- Add the L2 pre-handback step (with the same missing-command clause) to its fix-cycle text and the L3 three choices with the one-offer sentence beside each cap sentence "After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings" (today at lines 809 and 994; line 994 is rule 10 inside the `## Critical Rules` block whose hash Task 8 re-pins), written as new sentences directly after the final period of the cap sentence, which stays word for word.
- Rewrite or keep as named mechanical gates, recorded in `./artifacts/kept-mechanical-gates.md` (format of the Constraints), the eight verdict pairs that fail a review on "Any CRITICAL or IMPORTANT issue exists" (the FAIL bullet today at lines 240, 291, 362, 429, 500, 567, 746 and 784, each with its PASS bullet one line above; the list is in the stage 0 package's `./artifacts/stage0-inventory-freeze.md`, read by package id), and treat every other hit the frozen inventory lists for this file the same way, except a hit that is only an example of one check's own result (for example the `"System should be fast" = FAIL` example of the testable-user-stories check), which stays and is listed in the same artifact with that reason.
- Rewrite Rule 6 ("Contradictions are always IMPORTANT or CRITICAL ... that's never minor", today line 990) per OD16 option (b): a contradiction nothing rests on is a follow-up, and a contradiction that touches a decision basis, a quoted number or a required deliverable stays Blocking under the Decision condition. The new Rule 6 keeps the form `6. **<heading>** ...` because stage 4 reads the bold words of that line; the bold heading is copied into the first line of `./artifacts/kept-mechanical-gates.md` for stage 4. The new Rule 6 text avoids the softening tokens that `tests/audit/test_severity_floor_unweakened.py` rejects (for example "typically", "may be minor", "could be minor", "should be IMPORTANT").
- Reword the three relay lines that carry the old Rule 6 floor and the label as the grade: the line near 611 ("Severity floor: IMPORTANT (cf. Critical Rule #6)"), the one near 616 (">= IMPORTANT") and the verdict message near 918 ("Must resolve ALL CRITICAL and IMPORTANT issues before proceeding"), so each states the grade by the rule and names no label as the grade. They lie outside the `## Critical Rules` block and its hashed window.
- Rewrite principle 8 "NO LENIENCY" (today line 99, ending "an unverified or 'probably fine' claim is blocking") and Critical Rule 9 "Report honestly" (today line 993, ending "When in doubt, fail it and explain why."; it sits inside the `## Critical Rules` block) with the Task 4 consequence wording. The rewritten Rule 9 keeps its first sentence about a false PASS and the "stays open for verification" and "Unknown is not no" wording, and avoids the softening tokens above. The Confidence Gate lines that treat an UNCHECKED item as blocking a PASS (today lines 936 to 952) are not edited, for the reason given in Task 4. The slice that `test_severity_floor_unweakened.py` hashes by window (three lines above the `## Critical Rules` header to six below) is not touched.

Run `make sync-dev` afterwards.

Acceptance criteria:
- `grep -c "Any CRITICAL or IMPORTANT issue exists" src/superclaude/agents/rf-qa-qualitative.md` prints 0, or each remaining line is listed in `./artifacts/kept-mechanical-gates.md` with its reason; every other hit line of the stage 0 frozen inventory for this file is changed or listed there.
- `grep -n "that's never minor" src/superclaude/agents/rf-qa-qualitative.md` prints nothing, the new Rule 6 line begins `6. **` and names the decision-basis exception, and `grep -c -F "Severity floor: IMPORTANT"` and `grep -c -F ">= IMPORTANT"` and `grep -c -F "Must resolve ALL CRITICAL and IMPORTANT issues"` over the file each print 0 (today the first two print 1 each: the phrase wraps across two lines near 611 and 616, so a pattern that includes the wrapped parenthesis prints 0 today and proves nothing; the two short patterns do not wrap).
- The file has no `more severe rating` text; `grep -c -F "claim is blocking"`, `grep -c -F "it FAILS. Grade what you find"` and `grep -c -F "When in doubt, fail it"` each print 0; the lines holding "NO LENIENCY" and "Report honestly" contain "stays open for verification" and the Rule 9 line contains "consumer-unknown".
- The cap sentence "After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings" still prints a `grep -c -F` of 2, each with the three choices and the one-offer sentence, the L2 step naming `superclaude review fixcheck` is present, and each `new` string of the rows that name `agents/rf-qa-qualitative.md` in `tests/skills/fixtures/review_severity_cap_edits.yaml` is still found in the agent file with `grep -F`.
- `uv run pytest tests/skills/test_review_severity_rule.py` passes. `tests/audit/test_severity_floor_unweakened.py` is red from this task until Task 8 re-pins the `## Critical Rules` block hash in the same change set.

Global constraints:
## Constraints

- Spec and cuts: the merged spec `02-brainstorm/merged-requirements.md` inside the program folder `BLOCKER-CLASSIFICATION-PROGRAM-20261115` (found by that folder name under the repository's task folder). This plan calls that folder PF and the spec file the spec. Section numbers, requirement ids (REQ-nn), loop changes (L1 to L6), guardrails (GR1 to GR12), revert triggers (RT1 to RT8) and owner decisions (OD1 to OD17) refer to the spec. The cuts that shaped this plan are in `cuts-debate/final-cuts.md` in PF (rows C1 to C14, the S3 table of its section (b), the cross-package facts of its section (c)); where that file and the spec disagree about scope, the cuts file wins. Evidence of earlier stages is read from their packages by package id (the ids are in the stage ledger `stage-requests/README.md` in PF), found by that folder name in the to-do or done subfolder of the repository task folder. The stage 0 package is `TASK-WF-blockerStage0-20261116-021044` and the stage 1 package `TASK-WF-blockerStage1-20261116-030154`. The stage 2 package is withdrawn: its one survivor, the `/sc:implement` print, is task 2 of the stage 1 package.
- One package, one stage. This is stage 3 of the packages that remain (stage 0, stage 1, this one, stage 4). It changes the live review rule. Entry check, read from files and not from memory: the stage 0 package's `./artifacts/stage0c-regrade.md` exists; the stage 1 package is done (it is in the done subfolder of the repository task folder, or it is in the to-do subfolder with a `complete` line for every task in its `progress.md` and a latest `FINAL:` line that reads `FINAL: pass`); the stage 0 errata task has reworded the spec's RT1 row to read "any real blocker found in a Medium list" (`grep -c -F "any real blocker found in a Medium list"` over the spec prints 1 or more; Task 10 quotes it); the stage 3 row of `stage-requests/README.md` in PF holds the owner's go with a date (the go is a chat message recorded there by the session that received it; no hash and no line ruling are part of it). Task 1 runs this check before it creates any file under `src/` or `tests/`, and Task 2 runs it again before the first rule-file edit. A failed check stops the task before any edit and halts the run for the owner. While the check fails, no fix pass, repair, retry or adviser step edits a file under `src/`, `tests/` or `plugins/`, and the acceptance lines of that task that describe the edit do not apply. No task edits the ledger row. Stage 4 starts only after the owner has read the first five runs' Medium lists after the switch and RT1 did not trip (the stage 3 note says how), and the owner's go in chat.
- Limit of what this package shows. The stage 0 regrade is a lower bound: it regrades findings that were already supplied and cannot measure whether a reviewer would have found a defect. The stage 0 result, as its control test supports it, is only that the new text does not change grades on a table already filed as blocking (310 of 318 stay blocking under both texts, 82 of 82 panel blockers kept); both arms carried the old rule through the same hook, so no task here and no sentence of the Task 10 note cites that regrade as evidence that the new text works. No seeded-defect experiment is run here (the earlier one was confounded: both arms carried the old output style through the SubagentStart hook). What covers discovery is RT1 (spec section 13.2) read by the owner on the first five runs' Medium lists and one small planted-defect check run as part of the live RT1 audit after the switch; both go into the Task 10 note and neither is a build task.
- Owner decisions use the spec's recommendations unless the owner changes them, and none of them is converted into an owner answer here: OD1 no new skill folder, the S1 to S5 bullets of `pragmatic.md` are the one source; OD2 the Medium offer once per run plus at any escalation halt; OD9 reviewer-named consumer; OD11 replace label-max merging, staged (this stage the three agents; the rest is stage 4); OD14 a finding with an unknown consumer keeps the reviewer's label (no deferral); OD16 option (b) for Rule 6 of `rf-qa-qualitative.md`. OD3 (finding text leaving the machine) is open and no task depends on its answer; OD4 stands (no classifier in version 1).
- Retired carriers are not edited. The owner is retiring `/sc:task` and the task-builder: no task here edits `src/superclaude/skills/task/`, `src/superclaude/skills/task-builder/` or `src/superclaude/agents/rf-task-builder.md`. Tests that exist only to pin those files are not re-pinned here; where one test pins both a retired and an active carrier, only the active carrier's part is re-pinned.
- Follow-up list. The list of minors is the reviewers' own `follow-up candidates` section plus each task's `notes.md`; no list file, codec, sweep or registry is built. The stage 1 package prints that list at the end of `/sc:implement` (one paragraph titled "Follow-up print (record and print only).", command `superclaude review safety-scan`). This package edits no `sc-implement-protocol` file, no plugin file and no `refs/qa.md`. The once-per-run offer question stays with the top-level session through the output style (the Medium rule of `pragmatic.md`, changed from per loop to per run in Task 2), so no command gains a question.
- Plugin surface. IronClaude is installed from the Coder template or from a clone plus `superclaude install`, not as a plugin, so this package edits nothing under `plugins/` and creates no plugin mirror, parity test or plugin registry row. `src/superclaude/commands/spec-panel.md` and its plugin twin keep their "once per loop" wording, pinned by `tests/skills/test_review_severity_mapping.py`, `tests/skills/test_review_loop_extension.py` and `tests/skills/test_spec_panel_review_loop.py`; that wording moves in stage 4.
- Not built here: no classifier (`superclaude review classify` does not exist), no follow-up list file or `follow-ups` command group, no `sc-review-severity` skill folder, scale map, carrier registry, doctor check or registry drift test, no seeded-recall run, hash-bound owner ruling, shadow stage or baseline file, no Jev or other external judge call, no change to `src/superclaude/skills/sc-implement-protocol/refs/qa.md` (it keeps its own scale), to `src/superclaude/cli/review/ledger.py` or `review-ledger/1`, to the own-scale primitives of spec section 9.3, to code-assigned severity in `src/superclaude/cli/**/*.py`, to the cap of 2 fix cycles, or to the 35 percent target. Stage 4 edits the doubt wording and the merge text of the templates and rule prompts; this package only copies the S1 to S3 and S5 bullets into the ten tuple files (Task 3).
- Pins are by content. An acceptance check that must survive a task's own edit quotes the sentence it protects; it does not name a line number, because the edit moves the line. Line numbers in a task body are where the text sits today and are re-read before editing. An acceptance line that a later task of this package makes false carries its end point ("until Task N").
- `src/superclaude/` is the source of truth. Edit there, then run `make sync-dev` (it copies skills, agents, commands, hooks and templates; it does not copy `output-styles/`, `core/` or `rules/`). The installed `~/.claude/output-styles/pragmatic.md` therefore changes only at a refresh (Task 10 says how). Staging anything under the project `.claude/` folder is forbidden (only `.claude/settings.json` is tracked). Installed primitives name installed paths (`~/.claude/...`) first and project `.claude/...` second, never a `src/superclaude/` path.
- Kept mechanical gates (fixed FAIL triggers that stay as named gates) are recorded in the editing task's own `./artifacts/kept-mechanical-gates.md`, one bullet per gate: path relative to `src/superclaude/`, the gate's quoted words, the condition it maps to (the Missing condition of the digest), the reason. No `refs/scale-map.md` exists and none is created.
- Python work uses UV only: `uv run pytest ...`, never `python -m` or bare `pip`.
- Task-owned evidence and generated outputs go under `./artifacts/` in this package. `.dev/tasks/` is always staged (`git add .dev/tasks`), packages and their `./artifacts/` included, and no document a task writes says it is left out of staging. Staging is not committing.

Start sha: 0efb510d1c8e6ece4cde589ce2b6d19e43fb5f7a

Diff against the start snapshot:
```diff
diff --git a/src/superclaude/agents/rf-qa-qualitative.md b/src/superclaude/agents/rf-qa-qualitative.md
index 7e2eea0eb..d467a7c9e 100644
--- a/src/superclaude/agents/rf-qa-qualitative.md
+++ b/src/superclaude/agents/rf-qa-qualitative.md
@@ -81,7 +81,7 @@ The orchestrator (skill session or team lead) is responsible for:
 - Deciding when to partition (based on file count — typically >6 files warrants partitioning)
 - Dividing files into balanced subsets
 - Spawning multiple rf-qa instances in parallel, each with its `assigned_files` list
-- Merging partition reports after all instances complete (union of findings, take the more severe rating for shared items)
+- Merging partition reports after all instances complete (union of findings; the consolidator grades each by the review severity rule and keeps every reviewer's own grade visible; a blocking grade that names a consumer the code check does not disprove stands; a blocking grade that names no consumer goes back to the reviewer once with the `reasked` flag, and if it still names none the reviewer's label stands, the row is tagged `consumer-unknown` and is listed first, never demoted for missing grounding)
 - **DNSP Synthetic Finding emission (PR-03).** If a partition rf-qa instance fails after the single retry AND exhausts its escalation ladder, the orchestrator MUST emit a synthetic finding conforming to the **7-field DM-003 contract**: `severity: HIGH` (non-overridable), `source: "synthetic-dnsp"` (literal sentinel), `affected_range: <assigned_files / assigned_phases slice verbatim>`, `evidence: <spawn log path or evidence-absence stub: never blank>`, `recommendation: "Manual review required — partition agent failed twice"` (fixed string, byte-exact), `dedup_key: ["<assigned_files_range>", "<escalation_ladder_exhaust_point>"]` (2-tuple YAML list; `escalation_ladder_exhaust_point` ∈ closed vocabulary `{retry-1, retry-2, gap-fill-round-1, gap-fill-round-2, gap-fill-round-3}`), and `found_n_times: 1` (int, default `1`; increments by `1` on each within-cycle dedup-key collapse). The orchestrator continues with the remaining N-1 partitions rather than aborting. All-agents-fail still escalates normally (no DNSP). Repeated synthetics for the same dedup key collapse into one finding with `found_n_times` incremented (INV-012 composition with PR-02 monotonicity). **Fixed-field emitter rejection (R-113 + R-114).** The `severity` and `source` fields are non-overridable fixed-value invariants: the emitter MUST reject any synthetic emission whose `severity` field is not the literal `HIGH` (case-sensitive) OR whose `source` field is not the literal `synthetic-dnsp` (case-sensitive). Such rejections surface as `DM-003-fixed-field-invariant-violation` errors; the literal `synthetic-dnsp` sentinel is what allows downstream operator inspection and the `HIGH` pin is what prevents merge-time severity downgrade. **Dynamic-field emitter rejection (R-115 + R-116).** The `affected_range` field MUST be the partition's spawn-prompt `assigned_files / assigned_phases` slice copied verbatim -- byte-for-byte, with no normalization, canonicalization, ordering changes, or whitespace edits. The `evidence` field MUST NEVER be blank: the canonical wire value is the spawn-log path `${TASK_DIR}qa/spawn-log-<agent_role>-<partition_id>.txt`; when that log is unavailable the emitter MUST substitute the stub `<!-- evidence-absence: no-spawn-log: <reason> -->` explicitly citing the absence (e.g., `no-spawn-log: tmpfs-cleared`). The emitter MUST reject any synthetic emission whose `affected_range` does not byte-match the spawn-prompt `assigned_files / assigned_phases` slice OR whose `evidence` field is empty/whitespace-only. Such rejections surface as `DM-003-dynamic-field-invariant-violation` errors and MUST NOT be silently coerced. **Fixed-value + tuple-shape + counter emitter rejection (R-117 + R-118 + R-119).** The `recommendation` field is a fixed-value invariant: the emitter MUST reject any synthetic emission whose `recommendation` field is not the literal byte-exact string `Manual review required — partition agent failed twice` (case-sensitive; no leading/trailing whitespace; no suffix). The `dedup_key` field MUST be emitted as a 2-element YAML list of the shape `["<assigned_files_range>", "<escalation_ladder_exhaust_point>"]`; the emitter MUST reject any synthetic emission whose `dedup_key` is not a 2-element list OR whose second element falls outside the closed vocabulary `{retry-1, retry-2, gap-fill-round-1, gap-fill-round-2, gap-fill-round-3}`. The `found_n_times` field defaults to the integer `1` on first emission and increments by exactly `1` on each within-cycle dedup-key collapse; the emitter MUST reject any synthetic emission whose `found_n_times` is not a positive integer >=1 OR whose first emission carries a value other than `1`. Such rejections surface as `DM-003-recommendation-invariant-violation`, `DM-003-dedup-key-shape-violation`, and `DM-003-found-n-times-invariant-violation` errors respectively, and MUST NOT be silently coerced. **API-003-M6 emission wire-shape (R-120 + R-121).** The synthetic-dnsp finding MUST be emitted as a structured Markdown block written into the partition agent's **normal output stream** -- the same stdout/report channel that real findings use -- with no separate signalling channel, sideband API, structured-result frame, or out-of-band metadata transport. The block is consumed downstream by the task-builder skill's merge step at `SKILL.md` §A.8 (Research Quality Gate merge) and §A.10 (Task File Validation merge), where it is treated as a real blocking finding (severity HIGH) under the review severity rule (explicit pick-up wiring lands at T06.11 / R-127 + R-128). The `escalation_ladder_exhaust_point` value (second element of `dedup_key`) MUST be drawn from the closed vocabulary `{retry-1, retry-2, gap-fill-round-1, gap-fill-round-2, gap-fill-round-3}`; the emitter MUST reject any synthetic-dnsp emission whose `escalation_ladder_exhaust_point` falls outside this vocabulary OR whose value is a free-form description, paraphrase, or natural-language summary of the exhaust point (e.g., "second retry", "after WebSearch exhaustion"). Such rejections surface as `API-003-exhaust-point-vocabulary-violation` errors (cross-bound with `DM-003-dedup-key-shape-violation` from T06.05 -- the same vocabulary violation can fire at either check) and MUST NOT be silently coerced. **All-agents-fail guard precedence (R-122).** The synthetic-dnsp emitter MUST gate on the partition-cohort success count BEFORE any per-partition emission attempt, routing the cohort outcome down exactly one of three mutually-exclusive paths: **Path A (zero-partitions-succeeded -> existing rf-team-lead's Fix Cycles rule fix-cycle escalation; NO synthetic emits)** fires when the success count is `0` and the orchestrator MUST activate the byte-stable `rf-team-lead's Fix Cycles rule` fix-cycle escalation (max-2-cycles HALT-and-ask-user contract) without emitting any synthetic-dnsp block -- a HIGH synthetic for every partition is informationally equivalent to escalation and adds noise; **Path B (>=1-success AND >=1-exhaust -> synthetic-dnsp emits ALONGSIDE real findings)** fires when at least one partition succeeded AND at least one partition exhausted its escalation ladder, and the orchestrator MUST emit one synthetic-dnsp block per exhausted partition into the normal output stream alongside the real findings from the successful partitions (the synthetic-dnsp adds to, never replaces, real findings -- preserving the cohort's real-finding count and the parallel-research invariant); **Path C (all-partitions-succeeded -> no synthetic; normal merge)** fires when every partition succeeded and is the baseline no-DNSP path. The three paths are mutually exclusive (a single partition-cohort outcome MUST traverse exactly one path; the guard MUST reject any cohort outcome that satisfies more than one path's precondition or none -- e.g., a cohort with zero successes AND zero exhausts is a contract violation because every partition must terminate in success-or-exhaust). Such guard-precedence violations surface as `R-122-guard-precedence-violation` errors (named symbol distinct from `API-003-exhaust-point-vocabulary-violation` and `DM-003-dedup-key-shape-violation` because the path-selection gate is upstream of the per-emission wire-shape gate -- the symbol scopes the cohort-level path-selection failure, not a per-emission field-shape failure) and MUST NOT be silently coerced into a default path. The `rf-team-lead's Fix Cycles rule` line MUST be byte-stable across the M6 landing (COMP-006-M6 preservation gate; sha256 frozen at `c1c4ae4d8fa874df75b1ab4ca17891c01635ca522df6383cbfcb6fbfa480b4ee`); the all-agents-fail Path A activation MUST NOT replace, short-circuit, or modify the existing fix-cycle escalation, only route control to it. **Within-cycle + cross-cycle dedup composition (INV-012, R-123 + R-124).** The synthetic-dnsp emitter MUST apply two distinct dedup-collapse rules at orthogonal scopes that together compose with PR-02 Retry Monotonicity (FR-CONV.5 / M5) per the operational rule subsection at `~/.claude/skills/task-builder/SKILL.md` § "Within-cycle + cross-cycle dedup composition" (T05.07 INV-012 cross-cycle dedup composition; subsection sha256 pin OMITTED as bridge-stage). **Within-cycle collapse (R-123).** Two synthetic-dnsp findings emitted within the SAME retry cycle for the SAME `(assigned_files_range, escalation_ladder_exhaust_point)` 2-tuple MUST collapse to a single record with `found_n_times` incremented by exactly `1` from its current value (default `1` on first emission -> `2` after the first within-cycle collision -> `3` after the second, etc.); the emitter MUST NOT emit two cardinality-2 records and MUST NOT skip the increment. The within-cycle collapse happens BEFORE the merge step picks up the synthetic block at SKILL.md §A.8 / §A.10. **Cross-cycle composition (R-124, INV-012 non-regression).** A synthetic-dnsp finding with an identical `dedup_key` re-emitted on cycle `n+1` AFTER appearing on cycle `n` is a DEDUP case, NOT a regression -- its prior-cycle verdict was already FAIL, not PASS -- and it contributes `1` (not `2`) to `|F_{n+1}|` (the failure-set cardinality after the cycle-`n+1` fix attempt, per SKILL.md L1064). The cross-cycle collapse runs BEFORE the PR-02 monotonicity comparison `|F_{n+1}| >= |F_n|` at Step 2 of the 4-step ordering rule (SKILL.md L1071). The cross-cycle synthetic-dnsp persistence MUST NOT trip Step 1 (regression detection at SKILL.md L1070) because `dedup_key in FAIL_n` implies `dedup_key not in PASS_n`, so the Step 1 predicate `dedup_key in PASS_n ∩ FAIL_{n+1}` is FALSE by construction; persistence trips Step 2 (monotonicity) **if and only if** `|F_{n+1}| >= |F_n|` after the dedup-collapse step -- the intended halt when the partition agent is stuck. Violations of the within-cycle collapse rule surface as `INV-012-within-cycle-collapse-violation` errors; violations of the cross-cycle composition rule surface as `INV-012-cross-cycle-composition-violation` errors. Both symbols are distinct from `DM-003-found-n-times-invariant-violation` (T06.05 -- per-emission counter-shape failures), `R-122-guard-precedence-violation` (T06.08 -- cohort-level path-selection failures), and `API-003-exhaust-point-vocabulary-violation` (T06.07 -- per-emission wire-shape failures), because the dedup-composition gate is the cross-emission compositional layer between the per-emission field-shape gates and the cohort-level path-selection gate. Both rejections MUST NOT be silently coerced. **INV-021 N-1 cohort concurrency + R-126 HIGH severity non-overridable across merge step (R-125 + R-126).** The synthetic-dnsp emitter MUST preserve two cohort-level invariants spanning the partition-agent execution lattice and the merge-step output stream. **INV-021 N-1 cohort concurrency (R-125).** When one partition's escalation ladder exhausts, the orchestrator MUST allow the remaining N-1 sibling partitions to continue executing concurrently to their own success-or-exhaust terminal state BEFORE the exhausted partition's synthetic-dnsp emission is composed AND BEFORE the merge step at SKILL.md §A.8 / §A.10 runs. The exhausted partition's synthesis MUST NOT block, pause, serialize, or reduce the parallelism of the sibling cohort; spawn-log timestamps MUST evidence the N-1 partitions completing concurrently with (overlapping in wall-clock time with) the exhausted partition's synthesis step. This is the per-cohort instantiation of NFR-CONV.10 parallel-research invariant. **R-126 HIGH severity non-overridable across merge step + real findings preserved alongside synthetic.** The synthetic-dnsp `severity: HIGH` value MUST be non-overridable at every downstream layer: the per-emission `DM-003-fixed-field-invariant-violation` gate from T06.03 enforces non-override at the emission boundary, and T06.10 extends the invariant transitively across the cohort-level merge step at SKILL.md §A.8 / §A.10 (no merge-time normalization, severity-downgrade transform, severity-coalesce rule, or operator-overridable severity flag is permitted to lower the synthetic-dnsp severity below HIGH). The synthetic-dnsp block MUST be merged ALONGSIDE the real findings from the successful partitions (Path B from T06.08), never IN PLACE OF them: the cohort's real-finding count post-merge MUST equal the cohort's real-finding count pre-merge plus the synthetic count (strictly additive -- not replacement, coalesce, or filter); any merge logic that drops real findings to make room for synthetic findings, that coalesces real findings into synthetic ones, or that filters real findings on the basis of severity-bucket collisions with synthetic findings is a contract violation. Violations of the N-1 concurrency invariant surface as `INV-021-cohort-serialization-violation` errors. Violations of the real-findings-preservation invariant surface as `R-126-real-findings-replacement-violation` errors. Violations of the merge-step HIGH-severity non-overridable invariant surface as `R-126-severity-override-violation` errors (distinct from `DM-003-fixed-field-invariant-violation` from T06.03 -- the DM-003 symbol scopes per-emission boundary failures, the R-126 symbol scopes merge-step / cohort-layer override failures across the emission lifecycle; both layers are needed because the wire format is preserved post-emission but merge logic could still apply transforms). All three new symbols are distinct from `INV-012-within-cycle-collapse-violation` + `INV-012-cross-cycle-composition-violation` (T06.09), `R-122-guard-precedence-violation` (T06.08), `API-003-exhaust-point-vocabulary-violation` (T06.07), `DM-003-found-n-times-invariant-violation` (T06.05), and `DM-003-fixed-field-invariant-violation` (T06.03), because the INV-021 + R-126 gates scope the **execution-layer + merge-step layer** spanning cohort-wide parallelism and post-emission severity / count preservation across the merge boundary. All three rejections MUST NOT be silently coerced.
 
 ---
@@ -96,7 +96,7 @@ The orchestrator (skill session or team lead) is responsible for:
 5. **No red flags**: Unrealistic targets, missing dependencies, contradictory requirements, scope that doesn't match timeline, risks without real mitigations — these are the issues that bite teams months later.
 6. **Actionable feedback**: Provide specific fixes for failures — not "this needs work" but "S5.1 contains a KPI table that duplicates S19 — replace with business justification prose and a forward reference to S19."
 7. **Context matters**: A feature PRD and a platform PRD have different standards. Apply the right lens for the document type.
-8. **NO LENIENCY**: Do not give the document the benefit of the doubt. If something is "close enough" or "probably fine" — it FAILS. Grade what you find by the review severity rule: an unverified or 'probably fine' claim is blocking; a cosmetic or wording finding is minor.
+8. **NO LENIENCY**: Do not give the document the benefit of the doubt; verify before you accept. Grade an unverified claim by the review severity rule: a claim a named decision, number, acceptance check or required deliverable rests on is blocking, an unverified safety claim stays open for verification, an unverified claim nothing named rests on is Medium, and a cosmetic or wording finding is a Note. No item fails a review for being close enough or probably fine.
 9. **Ban N/A**: NO CHECK MAY BE MARKED N/A. Every check must be adapted to the document type. If the literal check doesn't apply, reinterpret it for the context and document what the adapted check verified.
 10. **Exhaustive verification**: Verify EVERY factual claim against actual source code using tools. No sampling, no spot-checking, no representative checks. Use Grep, Read, Glob to verify file existence, function names, config values, port numbers, test counts — everything.
 11. **Self-audit**: Before writing your verdict, ask: 'If I told the user I found 0 issues, would they believe me? What evidence can I show that I actually checked?' If you cannot point to specific verification steps, go back and check harder.
@@ -236,8 +236,8 @@ Before issuing your verdict, answer these questions in your report:
 
 ### Verdict
 
-- **PASS** — No CRITICAL or IMPORTANT issues; any MINOR issues are listed as notes.
-- **FAIL** — Any CRITICAL or IMPORTANT issue exists. List each with specific remediation. All blocking issues must be resolved before proceeding; MINOR issues never fail the review.
+- **PASS** — No blocking issue exists; any Medium or Note issues are listed as notes.
+- **FAIL** — Any blocking issue exists. List each with specific remediation. All blocking issues must be resolved before proceeding; Medium and Note issues never fail the review.
 
 ---
 
@@ -287,8 +287,8 @@ Before issuing your verdict, answer these questions in your report:
 
 ### Verdict (report-qualitative)
 
-- **PASS** — No CRITICAL or IMPORTANT issues; any MINOR issues are listed as notes.
-- **FAIL** — Any CRITICAL or IMPORTANT issue exists. List each with specific remediation. All blocking issues must be resolved before proceeding; MINOR issues never fail the review.
+- **PASS** — No blocking issue exists; any Medium or Note issues are listed as notes.
+- **FAIL** — Any blocking issue exists. List each with specific remediation. All blocking issues must be resolved before proceeding; Medium and Note issues never fail the review.
 
 ---
 
@@ -358,8 +358,8 @@ Before issuing your verdict, answer these questions in your report:
 
 ### Verdict (tdd-qualitative)
 
-- **PASS** — No CRITICAL or IMPORTANT issues; any MINOR issues are listed as notes.
-- **FAIL** — Any CRITICAL or IMPORTANT issue exists. List each with specific remediation. All blocking issues must be resolved before proceeding; MINOR issues never fail the review.
+- **PASS** — No blocking issue exists; any Medium or Note issues are listed as notes.
+- **FAIL** — Any blocking issue exists. List each with specific remediation. All blocking issues must be resolved before proceeding; Medium and Note issues never fail the review.
 
 ---
 
@@ -425,8 +425,8 @@ Before issuing your verdict, answer these questions in your report:
 
 ### Verdict (tech-ref-qualitative)
 
-- **PASS** — No CRITICAL or IMPORTANT issues; any MINOR issues are listed as notes.
-- **FAIL** — Any CRITICAL or IMPORTANT issue exists. List each with specific remediation. All blocking issues must be resolved before proceeding; MINOR issues never fail the review.
+- **PASS** — No blocking issue exists; any Medium or Note issues are listed as notes.
+- **FAIL** — Any blocking issue exists. List each with specific remediation. All blocking issues must be resolved before proceeding; Medium and Note issues never fail the review.
 
 ---
 
@@ -496,8 +496,8 @@ Before issuing your verdict, answer these questions in your report:
 
 ### Verdict (ops-guide-qualitative)
 
-- **PASS** — No CRITICAL or IMPORTANT issues; any MINOR issues are listed as notes.
-- **FAIL** — Any CRITICAL or IMPORTANT issue exists. List each with specific remediation. All blocking issues must be resolved before proceeding; MINOR issues never fail the review.
+- **PASS** — No blocking issue exists; any Medium or Note issues are listed as notes.
+- **FAIL** — Any blocking issue exists. List each with specific remediation. All blocking issues must be resolved before proceeding; Medium and Note issues never fail the review.
 
 ---
 
@@ -563,8 +563,8 @@ Before issuing your verdict, answer these questions in your report:
 
 ### Verdict (readme-qualitative)
 
-- **PASS** — No CRITICAL or IMPORTANT issues; any MINOR issues are listed as notes.
-- **FAIL** — Any CRITICAL or IMPORTANT issue exists. List each with specific remediation. All blocking issues must be resolved before proceeding; MINOR issues never fail the review.
+- **PASS** — No blocking issue exists; any Medium or Note issues are listed as notes.
+- **FAIL** — Any blocking issue exists. List each with specific remediation. All blocking issues must be resolved before proceeding; Medium and Note issues never fail the review.
 
 ---
 
@@ -590,7 +590,7 @@ Read the **entire task file** end to end. Then for each checklist item that modi
 
 #### Five Adversarial Axes (PR-07 -- applied as a sharpening overlay across all 15 checks below)
 
-These axes are NOT new checks -- they are adversarial lenses that sharpen the existing 15-item checklist. For every finding you record, annotate which axis fired in the Items Reviewed table (`axis: drift | contradictions | omissions | weakened-criteria | invented-content`). Pick the most-specific axis; record multiple only when each is independently load-bearing. Contradictions remain IMPORTANT or CRITICAL by default (cf. Critical Rule #6 below).
+These axes are NOT new checks -- they are adversarial lenses that sharpen the existing 15-item checklist. For every finding you record, annotate which axis fired in the Items Reviewed table (`axis: drift | contradictions | omissions | weakened-criteria | invented-content`). Pick the most-specific axis; record multiple only when each is independently load-bearing. Contradictions are graded by the review severity rule (cf. Critical Rule #6 below).
 
 - **AX-1 Drift** (kebab alias: `drift`) -- Has the task content drifted from BUILD_REQUEST.GOAL
   through paraphrasing, OR has a cited fact (file path, line number, signature, count, config value)
@@ -608,12 +608,12 @@ These axes are NOT new checks -- they are adversarial lenses that sharpen the ex
 - **AX-2 Contradictions** (kebab alias: `contradictions`) -- Do two items in the task (or two
   artifacts, or two sections of one artifact) assert mutually incompatible facts about the same
   subject? One says "use A", another implies "must not use A"? Do frontmatter fields contradict
-  body content? Do Acceptance Criteria contradict Open Questions? Severity floor: IMPORTANT
+  body content? Do Acceptance Criteria contradict Open Questions? Graded by the review severity rule
   (cf. Critical Rule #6). **Finding example (return-type mismatch pattern):** Section A states
   `build_axis_overlay()` returns `dict[str, Axis]`, while Section B's call site unpacks the same
   function's return value as `list[Axis]` (`for ax in build_axis_overlay(): ...`). Two artifacts
-  assert incompatible return types for the same callable. Annotate `axis: AX-2` with severity
-  >= IMPORTANT.
+  assert incompatible return types for the same callable. Annotate `axis: AX-2` with the grade
+  the review severity rule gives.
 - **AX-3 Omissions** (kebab alias: `omissions`) -- Are any BUILD_REQUEST `QA_GATE_REQUIREMENTS`,
   `VALIDATION_REQUIREMENTS`, or `TESTING_REQUIREMENTS` (SKILL.md rules #16/#17/#18) missing from
   the task as checklist items? Are any rf-qa FAIL items from the Inherited Structural Verdict left
@@ -742,8 +742,8 @@ Before issuing your verdict, answer these questions in your report:
 
 ### Verdict (task-qualitative)
 
-- **PASS** — No CRITICAL or IMPORTANT issues; any MINOR issues are listed as notes.
-- **FAIL** — Any CRITICAL or IMPORTANT issue exists. List each with specific remediation. All blocking issues must be resolved before proceeding; MINOR issues never fail the review.
+- **PASS** — No blocking issue exists; any Medium or Note issues are listed as notes.
+- **FAIL** — Any blocking issue exists. List each with specific remediation. All blocking issues must be resolved before proceeding; Medium and Note issues never fail the review.
 
 ### Parallel Partitioning for Large Task Files
 
@@ -780,8 +780,8 @@ Before issuing your verdict, answer these questions in your report:
 
 ### Verdict (doc-qualitative)
 
-- **PASS** — No CRITICAL or IMPORTANT issues; any MINOR issues are listed as notes.
-- **FAIL** — Any CRITICAL or IMPORTANT issue exists. List each with specific remediation. All blocking issues must be resolved before proceeding; MINOR issues never fail the review.
+- **PASS** — No blocking issue exists; any Medium or Note issues are listed as notes.
+- **FAIL** — Any blocking issue exists. List each with specific remediation. All blocking issues must be resolved before proceeding; Medium and Note issues never fail the review.
 
 ---
 
@@ -793,7 +793,7 @@ Before issuing your verdict, answer these questions in your report:
 ### Process
 
 1. Read the previous qualitative QA report (path provided in prompt)
-2. For each blocking (CRITICAL or IMPORTANT) issue flagged in the previous report:
+2. For each blocking issue flagged in the previous report:
    - Verify the fix was applied
    - Verify the fix is correct (not just present)
    - If the fix introduced new issues, flag them and grade them by the review severity rule
@@ -804,9 +804,11 @@ Before issuing your verdict, answer these questions in your report:
    - New issues introduced by fixes (new minor issues are notes)
 5. Updated verdict: PASS / FAIL (FAIL only when a blocking finding is open)
 
+**Pre-handback step for the fix agent (L2).** Before handing back, the fix agent runs `superclaude review fixcheck --file <edited file> (--base <copy saved before the fix> | --lines <start-end>)` over the lines it edited (repeat `--file` for several files) and writes every result, passes included, into the fix log. When that command is missing in the project or exits non-zero, the agent writes one line saying so in the fix log and carries on. A defect a verifier finds on those lines carries `origin: fix-induced` and is graded by the same review severity rule.
+
 ### Rules
 
-- Maximum 2 fix cycles. After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings. Do NOT convert unfixed findings to Open Questions. All blocking findings must be resolved; minor findings are recorded as notes.
+- Maximum 2 fix cycles. After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings. The user then chooses one of three: fix by hand, accept and file each open blocking finding as an `accepted-blocker` follow-up, or stop. The halt message carries the top-level session's once-per-run offer, which this agent does not make, so a halt shows one offer. Do NOT convert unfixed findings to Open Questions. All blocking findings must be resolved; minor findings are recorded as notes.
 - Each cycle should have fewer issues than the previous one. If issue count increases, flag this as a systemic problem.
 - **Tavily-first for any external lookup** -- When verifying a claim that requires fetching from the open web (a vendor doc page, an external standard, a third-party API surface, an external link in the document under review), you MUST attempt `mcp__litellm__Tavily-tavily_search` (else `mcp__tavily__tavily_search`) / `mcp__litellm__Tavily-tavily_extract` (else `mcp__tavily__tavily_extract`) before falling back to `WebSearch` / `WebFetch`. Silent fallback is a process violation; the fallback condition and reason MUST appear in your QA report.
 
@@ -915,7 +917,7 @@ After writing your QA report:
    SendMessage:
      type: "message"
      recipient: "team-lead"
-     content: "Qualitative QA [phase] complete. Verdict: [PASS/FAIL]. [count] checks passed, [count] failed. Issues: CRITICAL: [n], IMPORTANT: [n], MINOR: [n]. [If FAIL: 'Must resolve ALL CRITICAL and IMPORTANT issues before proceeding.' If PASS: 'Green light to proceed.'] Report: [path]."
+     content: "Qualitative QA [phase] complete. Verdict: [PASS/FAIL]. [count] checks passed, [count] failed. Issues: blocking: [n], Medium: [n], Note: [n]. [If FAIL: 'Must resolve ALL blocking issues before proceeding.' If PASS: 'Green light to proceed.'] Report: [path]."
      summary: "Qualitative QA [phase] complete — [PASS/FAIL]"
    ```
 
@@ -987,11 +989,11 @@ For qualitative checks that involve judgment calls (e.g., "is the audience appro
 3. **Think like a stakeholder** — Would a PM approve this? Would an engineer be able to build from this? Would a VP present this to investors? If any answer is "no," that's a finding.
 4. **Evidence for every verdict** — Never say "this seems fine" without explaining what you checked. Never say "this is wrong" without explaining what it should be.
 5. **Fix then verify** — If authorized to fix, always verify the fix worked. A fix that doesn't verify = still failed.
-6. **Contradictions are always IMPORTANT or CRITICAL** — If two sections say different things about the same topic, that's never minor. Always surface contradictions.
+6. **A contradiction a decision rests on stays Blocking** — If two sections say different things about the same topic, always surface it. A contradiction nothing rests on is a follow-up; a contradiction that touches a decision basis, a quoted number or a required deliverable stays Blocking under the Decision condition.
 7. **Be specific about fixes** — "This section needs work" is useless. "S5.1 contains a KPI table with 11 metrics that duplicates S19 — replace with business justification prose and a forward reference to S19" is useful.
 8. **Scope is the #1 issue** — The most common qualitative failure is content at the wrong scope level (platform content in feature PRDs, feature content in platform PRDs). Check this first and thoroughly.
-9. **Report honestly** — A false PASS that lets a bad PRD reach stakeholders is worse than a false FAIL that triggers one more review cycle. When in doubt, fail it and explain why.
-10. **Maximum 2 fix cycles** — After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings. All blocking findings must be resolved; minor findings are recorded as notes.
+9. **Report honestly** — A false PASS that lets a bad PRD reach stakeholders is worse than a false FAIL that triggers one more review cycle. Unknown is not no: when in doubt whether a finding is blocking, keep your own grade, tag the row `consumer-unknown` and explain why; an unresolved doubt about a safety claim stays open for verification.
+10. **Maximum 2 fix cycles** — After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings. The user then chooses one of three: fix by hand, accept and file each open blocking finding as an `accepted-blocker` follow-up, or stop. The halt message carries the top-level session's once-per-run offer, which this agent does not make, so a halt shows one offer. All blocking findings must be resolved; minor findings are recorded as notes.
 11. **You complement rf-qa, not replace it** — rf-qa checks structural correctness (section
     numbers, cross-references, evidence citations, template conformance, the TB-Add-*
     structural-gate additions). You check whether the content makes sense. Don't re-verify what
diff --git a/.dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/artifacts/kept-mechanical-gates.md b/.dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/artifacts/kept-mechanical-gates.md
new file mode 100644
index 000000000..c1155a792
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/artifacts/kept-mechanical-gates.md
@@ -0,0 +1,28 @@
+Rule 6 bold heading of `agents/rf-qa-qualitative.md` for stage 4: **A contradiction a decision rests on stays Blocking**
+
+# Kept mechanical gates (stage 3)
+
+Format: path relative to `src/superclaude/`, the gate's quoted words, the condition it maps to, the reason.
+
+## agents/rf-qa.md (Task 4)
+
+Frozen inventory source: `.dev/tasks/done/TASK-WF-blockerStage0-20261116-021044/artifacts/stage0-inventory-freeze.md` rows for `src/superclaude/agents/rf-qa.md`.
+
+- `agents/rf-qa.md`: "Generic steps like "create a service" = FAIL" | Missing (a required step named by the task is absent in substance when it is only generic) | kept: it is a mechanical check of one item's own result, an example of what makes that check fail, and the label does not decide the grade.
+- `agents/rf-qa.md`: "Missing fields = FAIL" (frontmatter schema check) | Missing (a required field is absent) | kept: a fixed mechanical check of required fields; absent required content is the Missing condition itself.
+- `agents/rf-qa.md`: "that's a FAIL" for a phase header whose claimed item count differs from the actual count (phase header accuracy check) | Decision (a quoted number the deliverable rests on is wrong) | kept: a recomputed count either matches or does not, so no judgment is involved.
+- `agents/rf-qa.md`: "that's a FAIL" for an overview whose quantitative claim differs from the checklist (prose count accuracy check) | Decision (a quoted number the deliverable rests on is wrong) | kept: same reason, a recomputed count.
+
+Rewritten, not kept (no longer fail by label): "Any incomplete file = FAIL", "Any untagged doc claim = FAIL" (both now graded by the review severity rule as Missing), the gap-severity bullets and the "Any CRITICAL or IMPORTANT gap = overall FAIL" line, the PASS and FAIL bullets of the research gate (now "blocking gap"), "Flag exact duplicates as IMPORTANT" (now a Note unless a condition holds), "For each blocking (CRITICAL or IMPORTANT) issue", and the summary-message counts.
+
+## agents/rf-qa-qualitative.md (Task 5)
+
+Frozen inventory source: `.dev/tasks/done/TASK-WF-blockerStage0-20261116-021044/artifacts/stage0-inventory-freeze.md`, rows for `src/superclaude/agents/rf-qa-qualitative.md` (lines 84, 108 to 111, 184, 240, 291, 332, 362, 429, 500, 567, 746, 784, 809, 858, 990, 994).
+
+All eight verdict pairs (the FAIL bullets at the old lines 240, 291, 362, 429, 500, 567, 746 and 784, each with its PASS bullet one line above) were rewritten to "Any blocking issue exists" and none is kept as a named gate. The merge rule (84), principle 8, Rules 6, 9 and 10, the two cap sentences (809, 994), the relay lines and the summary message were rewritten. Lines 108 to 111 were changed by Task 3.
+
+Kept, not rewritten, with the reason:
+
+- `agents/rf-qa-qualitative.md`: line 184 `"System should be fast" = FAIL` | the testable-user-stories check's own example | an example of one check's own result, not a grade of a finding.
+- `agents/rf-qa-qualitative.md`: line 332 `"Handle errors gracefully" = FAIL` | the error-handling check's own example | an example of one check's own result, not a grade of a finding.
+- `agents/rf-qa-qualitative.md`: line 858 "Failing checks (Result = FAIL) MUST carry one of `AX-1..AX-5`" | the Result column of the check table | it names a check result, and the grade of a finding still comes from the review severity rule.
diff --git a/.dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/artifacts/t5-pytest.log b/.dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/artifacts/t5-pytest.log
new file mode 100644
index 000000000..00f3022ed
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/artifacts/t5-pytest.log
@@ -0,0 +1,7 @@
+## test_review_severity_rule
+
+============================== 62 passed in 3.47s ==============================
+## tests/audit red files (plan allows these until Task 8)
+      3 FAILED tests/audit/test_invariant_preservation_NFR_6_through_10.py
+      5 FAILED tests/audit/test_nfr_conv_9_zero_trust.py
+      4 FAILED tests/audit/test_severity_floor_unweakened.py
```

Codegraph context
index_state: fresh
checked_at: 2026-11-17T00:49:50Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel
projectPath: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel
call codegraph only when index_state: fresh, never to widen scope
Q2b dependents not in the diff: none for code; rf-qa-qualitative.md is a markdown agent read by tests/skills/test_review_severity_rule.py and tests/audit/test_severity_floor_unweakened.py; the plan says the audit tests are re-pinned in Task 8 (observed red files are in t5-pytest.log).

Delta diff from the previous reviewed tree (empty on the first review): 
```diff
diff --git a/src/superclaude/agents/rf-qa-qualitative.md b/src/superclaude/agents/rf-qa-qualitative.md
index 1f152f5cc..d467a7c9e 100644
--- a/src/superclaude/agents/rf-qa-qualitative.md
+++ b/src/superclaude/agents/rf-qa-qualitative.md
@@ -590,7 +590,7 @@ Read the **entire task file** end to end. Then for each checklist item that modi
 
 #### Five Adversarial Axes (PR-07 -- applied as a sharpening overlay across all 15 checks below)
 
-These axes are NOT new checks -- they are adversarial lenses that sharpen the existing 15-item checklist. For every finding you record, annotate which axis fired in the Items Reviewed table (`axis: drift | contradictions | omissions | weakened-criteria | invented-content`). Pick the most-specific axis; record multiple only when each is independently load-bearing. Contradictions remain IMPORTANT or CRITICAL by default (cf. Critical Rule #6 below).
+These axes are NOT new checks -- they are adversarial lenses that sharpen the existing 15-item checklist. For every finding you record, annotate which axis fired in the Items Reviewed table (`axis: drift | contradictions | omissions | weakened-criteria | invented-content`). Pick the most-specific axis; record multiple only when each is independently load-bearing. Contradictions are graded by the review severity rule (cf. Critical Rule #6 below).
 
 - **AX-1 Drift** (kebab alias: `drift`) -- Has the task content drifted from BUILD_REQUEST.GOAL
   through paraphrasing, OR has a cited fact (file path, line number, signature, count, config value)
@@ -793,7 +793,7 @@ Before issuing your verdict, answer these questions in your report:
 ### Process
 
 1. Read the previous qualitative QA report (path provided in prompt)
-2. For each blocking (CRITICAL or IMPORTANT) issue flagged in the previous report:
+2. For each blocking issue flagged in the previous report:
    - Verify the fix was applied
    - Verify the fix is correct (not just present)
    - If the fix introduced new issues, flag them and grade them by the review severity rule
```

Earlier blocking findings of this start (empty on the first review): 
F1.2 sev=blocking trigger=B4 ac=scope at=src/superclaude/agents/rf-qa-qualitative.md:111 anchor=src/superclaude/agents/rf-qa-qualitative.md:796 chk=n,y,n,n family=label-as-grade fix=reword line 796 to "For each blocking issue flagged in the previous report" covers="so each states the grade by the rule and names no label as the grade" first=start origin=inherited: line 796 reads "For each blocking (CRITICAL or IMPORTANT) issue flagged in the previous report" and defines blocking by label

Saved-probe re-check hit locations (may be empty): src/superclaude/agents/rf-qa-qualitative.md lines (none)

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
