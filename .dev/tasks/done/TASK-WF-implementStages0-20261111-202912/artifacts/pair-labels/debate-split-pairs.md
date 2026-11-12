# Split-pair debate: P01, P09, P12, P38 (minority advocate)

Sheet: `.dev/tasks/to-do/TASK-WF-implementStages0-20261111-202912/artifacts/cluster-pairs-50.csv`. Labels: `pair-labels/labeler-{A,B,C}.csv`. Definition used by all labelers: same defect = fixing one flaw in the reviewed document would resolve both findings.

## Sources and version check

Each reviewed document was checked against the sha256 in the run's `artifacts/input-snapshot.yaml`, so the lines quoted below are the lines the reviewers saw, except where stated.

| Pair | Run (`.dev/reflect/...`) | Reviewed document as quoted here | Matches the review snapshot? |
|---|---|---|---|
| P01 | `pre-TASK-WF-brainstormFixBri-20261106-001016` | plan at `git show cb8f2f81a:.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-001016/TASK-WF-brainstormFixBri-20261106-001016.md` (deleted from the tree later); `src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md` at `cb8f2f81a^` (before the fix landed) | plan: yes (sha256 55b0c353...). `handoff-routing.md`: not in that snapshot; the pre-fix version is used |
| P09 | `pre-TASK-WF-scIssueCommand-20261104-064713-20261104070955` | `tests/core/test_how_we_work_routing_table.py` at `6542ca72b^`; plan only at `.dev/tasks/done/TASK-WF-scIssueCommand-20261104-064713/TASK-WF-scIssueCommand-20261104-064713.md` | test file: yes (dbf96c05...). Plan: NO. The reviewed plan (eb19aa0f...) is in no git commit; the done plan is the post-fix version, so plan lines are quoted only to show how the defects were fixed |
| P12 | `pre-TASK-WF-writeTheP1Static-20261105-033458-20261105034258` | spec `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` at `f3c1ef062` (the last spec commit before the review); `src/superclaude/skills/sc-init-lite-protocol/SKILL.md` at `f3c1ef062` | the report names the spec as the `spec:N` target (`REPORT.md:24`); the spec is not in the two-file snapshot, so the version is chosen by date |
| P38 | `pre-workflowSource-20261102234109` | `.dev/releases/current/v5.0.0/post-release/CONSOLIDATED-PLAN.md` and `.dev/tasks/to-do/TASK-WF-workflowSource-20261102-233731/TASK-WF-workflowSource-20261102-233731.md`, both on disk now | yes (2ef75e86... and b21a115b...) |

I also re-ran `cluster_v2` on each run's cards (through `scripts/reflect_cluster_pairs.py`'s converter) to see why it merged each pair or kept it apart. The results are quoted where they matter.

## P01 (minority: no)

Findings (`.dev/reflect/pre-TASK-WF-brainstormFixBri-20261106-001016/reviewer-cards/`):

- `reviewer-1-card.yaml:55` R1-10: "Task 7 says 'do not edit any file' but saves logs under ./artifacts/ (say 'no source edits'). Task 2 says tier lists 'end with' the quality_tier line; the Tier 2 list ends with the Activation bullet (confirms F-2)."
- `reviewer-2-card.yaml:35` R2-6: "Confirms F-2: the Tier 2 list ends with the Activation bullet (line 31) after quality_tier at line 30; the grep -c criterion cannot detect a bullet placed in the wrong list."

Document lines:

- plan:39 (Task 2): "each with a bullet list that ends with its `quality_tier` line. Add one bullet to each tier's list".
- plan:42 (Task 2 criterion): "`grep -c 'writes no nested directory' ... handoff-routing.md` prints 2, one in the Tier 1 list and one in the Tier 2 list".
- plan:93 (Task 7): "Save the command outputs to `./artifacts/t7-sync.log`, `./artifacts/t7-pytest.log` and `./artifacts/t7-lint.log`. Do not edit any file in this task."
- `handoff-routing.md:30-31` (pre-fix): "- quality_tier: `fallback_1`" then "- Activation: if Tier 1 returns error OR empty result".

Case for "no":

1. R1-10 holds two defects in two different tasks: the Task 7 contradiction at plan:93 and the Task 2 placement error at plan:39. No single edit to the plan fixes both. Rewording plan:39 leaves "Do not edit any file" at plan:93 contradicting the three log writes on the same line, so R1-10 is still open after the fix that closes R2-6. Under the definition as written ("would resolve both findings"), that is a no.
2. R2-6 is itself two claims: the placement error (F-2) and a second one, that the plan:42 criterion "cannot detect a bullet placed in the wrong list". Fixing the wording at plan:39 does not change what `grep -c` can detect. The run's own merge treated the detection gap as a separate defect with its own remedy: `adversarial/refactor-plan.md:108` reads "R2-6 diagnoses the file-wide count but gives no fix | ... | V1 (R1-3, `_section` helper) | Change 4". So the one shared flaw (F-2) resolves neither finding completely.
3. The run's debaters called R1-10 two findings: "R1-10 bundles two unrelated nits (the 'do not edit any file' wording and the 'ends with' wording)" (`adversarial/debate-transcript.md:59`). The merge split it: "Change 9 ... Source: V1, R1-10 first half ... The second half of R1-10 is already base R2-6 (C-009)" (`adversarial/refactor-plan.md:72-75`). The merge needed a split before anything could match. `cluster_v2` cannot split a finding, so a "yes" credits it for a judgement it never made.

## P09 (minority: no)

Findings (`.dev/reflect/pre-TASK-WF-scIssueCommand-20261104-064713-20261104070955/reviewer-cards/`):

- `reviewer-1-card.yaml:27` A-4: "Task 2 no_token check does not unset CLICKUP_API_TOKEN; Task 11 git diff --stat check fails on a tree holding other tasks' changes; Task 10 does not say the new row must be ASCII." Recommendation (`:29`): "Task 2 runs with env -u CLICKUP_API_TOKEN; Task 11 checks git diff -- <that file>; Task 10 states the row is ASCII-only."
- `reviewer-3-card.yaml:39` S-6: "Task 10 does not say the new Other-commands row must be ASCII and must not backtick a non-existent /command (test_guide_is_ascii_except_the_ruling_example, test_other_commands_membership_and_live_references)."

Document lines:

- `tests/core/test_how_we_work_routing_table.py:341-346` (snapshot-matched): `def test_guide_is_ascii_except_the_ruling_example(): ... if not line.isascii(): assert "Ruling:" in line`.
- The reviewed plan is not recoverable (see the version table). The post-fix plan shows the three parts of A-4 fixed in three separate tasks: `.dev/tasks/done/TASK-WF-scIssueCommand-20261104-064713/TASK-WF-scIssueCommand-20261104-064713.md:50` (Task 2 now runs `env -u CLICKUP_API_TOKEN -u CLICKUP_WORKSPACE_ID ...`), `:170` (Task 10 now says "The row is ASCII only ... and backticks no `/...` token other than `/sc:issue`"), and `:189` (Task 11's criterion is now `git diff -U0 -- docs/developer-guide/...`, not `--stat`).

Case for "no":

1. A-4 covers three tasks, three plan lines (plan:49, plan:178 and the Task 10 text) and three separate fixes, as its own three-part recommendation shows. Fixing Task 10 resolves one third of A-4. The other two thirds stay open, so one fix does not resolve both findings.
2. S-6 also says more than A-4: the "must not backtick a non-existent /command" rule (`test_other_commands_membership_and_live_references`) is in S-6 and missing from A-4. The overlap is one clause of each finding, not either finding as a whole.
3. The run's merge split A-4 into three findings with different classes: F-06 `non-observable-ac` (with S-3), F-07 `other` (with S-6), F-08 `unexecutable` (A-4 alone) (`adversarial/merged-verdict.yaml:101-140`). The debater for A-4's own card conceded: "A-4 bundled three unrelated items: conceded. I split it" (`adversarial/adversarial/debate-transcript.md:320`). The refactor plan records "V1 A-4 bundle | three nits in one finding | Split into F-06, F-07 and F-08" (`adversarial/adversarial/refactor-plan.md:165`).
4. A "yes" here hides a real cluster error. Re-running `cluster_v2` on this run puts A-4, S-3 and S-6 in one cluster, C3, which is not flagged as chained. S-3 (the Task 11 `git diff --stat` defect) and S-6 (the Task 10 ASCII defect) are different defects that the merge kept apart as F-06 and F-07. They match directly because S-3 cites plan:159, Task 10's line, as context. The sampler skips same-reviewer pairs (`scripts/reflect_cluster_pairs.py`, `if r1 == r2 ... continue`), so S-3/S-6 was never drawn. A bundled finding such as A-4 binds both defects into one cluster, and calling A-4/S-6 correct endorses that cluster.

## P12 (minority: yes)

Findings (`.dev/reflect/pre-TASK-WF-writeTheP1Static-20261105-033458-20261105034258/reviewer-cards/`):

- `reviewer-1-card.yaml:111-125` R1-06 (t1_ref F-002, stance downgrade, "fix: None."): "Spec 2.1 is general; adversarial and analyze both accept the flag after P1. D-P1-4 is a faithful reading, not creep. Disclosure as D-P1-4 and in the Task 15 report is enough."
- `reviewer-2-card.yaml:92-106` R2-06 (stance new): "The spec's small fix names Safety Invariant 3; Task 8 amends 2 and 3 because the contract is required on --dry-run. The extension is necessary but is a spec delta decided inside a task body, not in the D-P1 list." Fix: "Add the invariant-2 extension to the D-P1 decision list (D-P1-11)."

Document lines (spec at `f3c1ef062`):

- spec:62: "a command that invokes another `/sc:` command ... passes `--unattended` when the invoked command accepts it at this phase, together with its own report directory `<caller report-dir>/nested/<command>-<n>/`".
- spec:142 (brainstorm row): "Under `--unattended`, automatic research enrichment ... is off (P1); from P2 it passes `--unattended` and a nested report directory (P2)".
- spec:147 (init-lite row): "Under `--unattended`, amend Safety Invariant 3 ('the only write is the marked report', `sk/sc-init-lite-protocol/SKILL.md:63`) to allow the contract (P1)".
- `sc-init-lite-protocol/SKILL.md:62-63`: "2. **Dry-run writes nothing** ..." and "3. **Default = report only** -- the only write is the marked report at `output`."
- T1 finding F-002 (`t1-card.md:30-39`), which R1-06 downgrades: "Brainstorm's nested-call behaviour goes beyond the spec's P1 row ... The plan records this as decision D-P1-4, so it is disclosed".

Case for "yes":

1. Both findings name one plan-level flaw: the plan departs from a spec section 6 row (spec:142 for brainstorm, spec:147 for init-lite) and has to make each departure an owner-visible D-P1 decision. R2-06's fix ("add ... to the D-P1 decision list") is the same remedy R1-06 says is already enough for its case ("Disclosure as D-P1-4 and in the Task 15 report is enough"). One plan rule, "every departure from a section 6 row is a D-P1 decision reported in Task 15", would close R2-06 and is the rule R1-06 checks against.
2. Both cite the same spec table (rows 142 and 147, five lines apart) for the same kind of issue (a P1 row's scope extended inside a task body), and both carry `severity: minor`. A labeler who groups by "kind of plan flaw" gets one defect: undisclosed or under-disclosed spec deltas.
3. R1-06 is a stance on a real finding (F-002, "goes beyond the spec's P1 row"), not a statement that nothing is wrong. Its claim keeps the disclosure requirement, so it still points at the D-P1 disclosure flaw that R2-06 names.

Mechanical note (fact, not argument): `cluster_v2` merged this pair on equal fingerprints, not on citations. Both findings have `refs_norm == ['P1']`, because `_REF_TOKEN` (`src/superclaude/cli/review/findings.py:29`, `\bP[0-9]\b`) picks up the phase tag inside "D-P1-4" and "D-P1 list". Their primary citations share role `spec` and the same path. The fingerprint carries no line numbers, so the line-span test (142 versus 147 is more than `SPAN_TOLERANCE = 3` apart) never ran. The converter also resolved `spec:N` to `.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/source.md`, an 11-line brief, instead of the spec the report names. Lines 62, 142 and 147 of that file do not exist, yet the sheet marks them "resolved".

## P38 (minority: yes)

Findings (`.dev/reflect/pre-workflowSource-20261102234109/reviewer-cards/`):

- `reviewer-1-card.yaml:49-53` R1-F8: "Dependency declarations do not enforce ordering for Tasks 37, 47, 66 and Task 1's upgrading.md link; fine only under sequential execution." Citation "tasklist:342-346, :422-430, :581-589; CONSOLIDATED-PLAN.md:481". Recommendation: "Add Depends-on lines: 47 on 3,17,43-46; 66 on 48-65; 37 on 43-46."
- `reviewer-3-card.yaml:25-29` R3-F4: "Task 37 omits B-W12 #6 (link four new notes) and runs before Tasks 43-46 with no dependency; AC checks in-file anchors only." Citation "CONSOLIDATED-PLAN.md:481; tasklist:340-346". Recommendation: "Do the four-note links after Task 46 (fold into Task 47) with a target-exists AC."

Document lines:

- `.dev/releases/current/v5.0.0/post-release/CONSOLIDATED-PLAN.md:475` "**B-W12 `docs/developer-guide/README.md` (update)**", and `:481` "6. Link the four new notes (B-W19..B-W22)."
- tasklist `.dev/tasks/to-do/TASK-WF-workflowSource-20261102-233731/TASK-WF-workflowSource-20261102-233731.md:340-346`: "## Task 37: Update docs/developer-guide/README.md (item B-W12)" with no "Depends on" line; its criteria check only `SuperClaude-Org` and "every in-file anchor resolves".
- tasklist:19: "The item text for every task lives in ... CONSOLIDATED-PLAN.md ... Read the named item before editing." So the executor of Task 37 reads B-W12 #6.
- tasklist:390-414: Tasks 43-46 create the four notes; tasklist:424: Task 47 "Depends on: Task 46".

Case for "yes":

1. Both findings cite the same line, `CONSOLIDATED-PLAN.md:481`, B-W12 item 6. R1-F8 has only one reason to want "37 on 43-46": Task 37 must link notes that Tasks 43-46 create. That is item 6. The Task 37 part of R1-F8 and R3-F4 therefore describe one flaw: B-W12 #6 sits in Task 37, which runs before the notes exist. Because tasklist:19 makes the executor read item 6, "omits" (R3-F4) and "not ordered after 43-46" (R1-F8) describe the same defect from two sides.
2. One fix closes both. R3-F4's remedy (move the four-note links into Task 47, which already depends on Task 46) resolves R3-F4 and removes the need for R1-F8's "37 on 43-46" line. The run's merge did exactly this: it split R1-F8 and filed the Task 37 part with R3-F4 as R1-F8b, `source_variants: [V1 R1-F8, V3 R3-F4, V2 R2-F4]`, claim "Task 37 omits B-W12 #6 ... and runs before Tasks 43-46" (`adversarial/merged-verdict.yaml:158-166`). The debate record says "R1-F8 conflates omission with ordering" (`adversarial/debate-transcript.md:38`).
3. This pair has the same structure as P01 and P09: a bundled finding (R1-F8: Tasks 37, 47, 66 and 1) one part of which is exactly the other finding's defect, and a run merge that split the bundle and matched that part. Labeler A voted yes on P01 and P09 for that reason and no here. Labeler A's stated difference ("B is mainly that Task 37 omits the B-W12 item 6 links") is the same defect, as point 1 shows. Applying one rule to all three pairs makes P38 yes.
4. `cluster_v2` kept the pair apart for a mechanical reason, not a semantic one. On the sheet each finding's only converted citation is `source CONSOLIDATED-PLAN.md:481 (unresolved)`. The bare file name does not match the snapshot path, and the `tasklist:` citations (340-346 versus 342-346, which overlap) were not converted, so no resolved citation was left to compare.

## Honest verdicts

The facts in P01, P09 and P38 are not in dispute. All three labelers describe the same overlap, and their votes split only over how to count a bundle, so for those pairs the label follows from the rule chosen below, not from more evidence.

| Pair | Evidence favours | Confidence | Why |
|---|---|---|---|
| P01 | yes (majority), under the recommended rule | medium (0.7) | R1-10's second half and R2-6's first half are one flaw at plan:39 against `handoff-routing.md:30-31`, and the run's merge says so ("The second half of R1-10 is already base R2-6", `refactor-plan.md:75`). The "no" case only wins on a whole-finding reading of the definition, and it proves too much: R2-6 also carries the separate `grep -c` gap, so under that reading R2-6 could not match even a perfect copy of itself with that gap left out. |
| P09 | yes (majority), under the recommended rule | medium (0.7) | The Task 10 ASCII clause is shared word for word and the run merged it as F-07 with `source_cards: [reviewer-3, reviewer-1]` (`merged-verdict.yaml:116-126`). The C3 cluster problem (S-3 with S-6) is real, but it is a same-reviewer pair this sheet never samples; it should be reported, not counted against this pair. |
| P12 | no (majority) | high (0.9) | Different commands (brainstorm against init-lite), different spec rows (142 against 147), different source files, and opposite verdicts: R1-06 says there is no defect ("fix: None."), R2-06 asks for a new D-P1-11. No single edit resolves R2-06 and also changes anything R1-06 asks for. The "same kind of flaw" argument groups by category, not by defect. The merge is an artifact of the `P1` token and the line-blind fingerprint. |
| P38 | yes (minority), under the recommended rule | medium-low (0.6) | R1-F8's Task 37 part and R3-F4 are one flaw (B-W12 #6 at `CONSOLIDATED-PLAN.md:481`, placed in Task 37 before Tasks 43-46), and the run merged them as R1-F8b. The weaker point: R1-F8 states it only as a missing dependency line, so a labeler who reads the claim text alone and not its citation can fairly see a different defect. If the panel adopts the whole-finding rule, P38 is no along with P01 and P09. |

Two `cluster_v2` problems found on the way, outside these four labels: (1) fingerprint merges ignore line numbers and treat phase tags such as `P1` as references (`findings.py:29`; P12 shows the result); (2) the converter resolves `spec:N` to the brief `source.md` and leaves bare `CONSOLIDATED-PLAN.md` and `tasklist:` citations unresolved or unconverted (P12, P38).

## Recommended rule for bundled findings

Rule: a pair counts as the same defect when one flaw in the reviewed document, fixed by one edit, fully resolves at least one separable part of each finding, and for a finding with no separable parts, the whole finding. Parts of either finding about other flaws do not change the label. A part is separable when it names a different task, line or fix (as A-4's three-part recommendation does). Extra detail about the same flaw, such as a second missing test file in the same test list (P03), is not a separate part.

Why this rule: `cluster_v2` exists to count which reviewers found each defect (support and agreement in `src/superclaude/cli/review/cluster.py`). The runs' own adversarial merges credited the bundling reviewer for the shared part in all three bundle cases (P01 `refactor-plan.md:75`, P09 F-07 `source_cards`, P38 R1-F8b `source_variants`). A whole-finding rule would score as wrong the very merges the human-supervised pipeline made, and the cause is the card author's writing style, which `cluster_v2` cannot see.

Effect on measured precision (majority labels, 25 merged and 25 apart pairs): today the labels give 21 true merges and 4 false (P12, P14, P17, P18), so precision is 21/25 = 0.84 and recall is 21/21 = 1.00. Under this rule P01 and P09 stay yes and precision stays 0.84. P38 becomes a missed merge, so recall drops to 21/22, about 0.95. Under the whole-finding rule, P01 and P09 become false merges and precision falls to 19/25 = 0.76, with recall unchanged at 1.00. Caveat: these figures count only the four split pairs. Labelers A and C may have applied a whole-finding rule to other apart pairs without a split vote; that was not re-checked, so recall under the recommended rule is an upper bound.
