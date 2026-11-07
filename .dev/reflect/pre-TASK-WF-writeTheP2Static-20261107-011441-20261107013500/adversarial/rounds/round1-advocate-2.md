# Round 1 — Variant 2 advocate (QA)

## Position summary

Merge V2's test-quality findings with V3's missed nested calls and V1's unresolved CLI-mode gate. V2 is strongest on whether the prescribed checks can distinguish a correct resolution from its opposite, not on total coverage. Keep R2-F1 as P1, conditional on an explicit required-input policy; keep R2-F2/R2-F3 as P2; retain R2-F4 as a bounded manifest gap; correct R2-F5 to a review-matrix omission, not plan drift.

All citations below refer to files I re-read, not just the cards. Paths without an absolute prefix are relative to `/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P2`.

Citation aliases:
- `plan` = `.dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/TASK-WF-writeTheP2Static-20261107-011441.md`.
- `source` = that package's `source.md`.
- `spec` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`.
- `review` = `.dev/reflect/pre-TASK-WF-writeTheP2Static-20261107-011441-20261107013500`; `matrix` = `review/artifacts/coverage-matrix.yaml`; `calibration` = `review/artifacts/calibration.yaml`.
- Finding IDs refer to the three `review/adversarial/variant-<n>-original.md` cards.

The blind calibration lowers V2 from self-reported 0.94 to 0.78 and specifically corrects R2-F5's classification (`calibration:25-29`). I accept that correction; scores are not substitutes for the source evidence below.

## Steelman (V1, V3)

### V1

V1's strongest contribution is R1-F3: Task 14 suppresses the CLI-mode reflect gate's staging step but leaves the rest of the generated gate unspecified (`plan:261`). The template explicitly couples staging with a wrapper invocation using `--fix --promote` (`src/superclaude/skills/task-builder/SKILL.md:2235-2240`). That is a real conditional integration question which V2 missed. It needs a complete unattended rule when that arm is active, not an assumption that disabling staging resolves the whole gate. The flags' local mutation is not, by itself, proof of forbidden outward action.

V1 also correctly identifies the stale workflow contract description in R1-F1: `.dev/reflect/` remains in the command and return-contract reference, while Task 17 changes the nested location (`src/superclaude/commands/workflow.md:72-75`; `src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md:52`; `plan:303`). R1-F4 correctly asks for the unrecorded socratic-mode decision: Task 5 specifies non-waiting behavior, but D-P2-10 records only target-release and Improve behavior (`plan:55,136`).

### V3

V3's strongest argument is R3-F1. Stage 9 really invokes `sc:task` through Skill and repeats it on loop-back (`src/superclaude/skills/sc-tasklist-protocol/SKILL.md:1535-1557`). Task 16 supplies nested propagation only for reflect (`plan:286-290`), despite Task 12 converting task (`plan:233`). Spec section 2.1 covers nested Skill calls independently of the per-command table (`spec:60-62`). The defensible P1 harm is an unattended run reaching task's person-blocking gates, not an inevitable commit/push operation.

R3-F4 and R3-F5 extend that same reasoning to real optional branches: release-split permits analyze or inline verification, and reflect lists optional deep tech-research (`src/superclaude/skills/sc-release-split-protocol/SKILL.md:318-326`; `src/superclaude/skills/sc-reflect-protocol/SKILL.md:624-636`). V2 did not find these branches. V3's concrete fixes deserve inclusion after calibration.

## Strengths claimed

1. **R2-F1 separates missing-suite and missing-safety-input failures.** Spec row 164 requires both, whereas Task 13 and D-P2-15 explicitly block only a missing suite and otherwise treat the supplied invocation as confirmed (`spec:164`; `plan:60,248`). Two independent negative cases prevent a suite-only assertion from masquerading as full coverage. The required safety-input policy still needs owner clarification; I do not advocate requiring every example flag to be present.

2. **R2-F2 tests the relationship, not the vocabulary.** Task 20 derives gate phrases from earlier entries and only specifies removed-phrase negative cases (`plan:345`). Cleanup supplies separate `Approval Required` and `not applied` phrases; release-split supplies a generic `blocked_question` plus filenames/status language (`plan:97,179`). Those words can remain while the relevant condition's outcome is reversed. Condition-plus-outcome phrases scoped to the rule, with reversal cases preserving the gate label, directly implement the brief's opposite-wording warning (`source:14`). This is a prescribed-test weakness, not an observed failing implementation.

3. **R2-F3 distinguishes prose coverage from executable coverage.** Only cleanup and improve explicitly put `left out (WC-4)` in their expected-phrase lists (`plan:97,110`); research, cli-eval and tdd describe exclusions without pinning that phrase (`plan:123,248,261`). Matrix INF-006 says five commands are test-pinned (`matrix:14`), conflating those two categories. The brief also requires the conditional short local sentence explaining that the report names where excluded files went (`source:7`), which the per-task instructions do not assign. Keep the all-fifteen clause-scoped test and this conditional assignment, rather than checking only for a WC-4 token somewhere in a section.

4. **R2-F4 identifies an omission even on a clean tree.** The requested list is for the owner-approved commit (`source:16`), but its equality criterion only queries `src tests plugins` (`plan:372`), while the same task stages the package, report and evidence (`plan:367,371`). Include plan-produced task-package paths, while distinguishing unrelated pre-existing changes. This does not depend on any actual dirty status in this checkout.

## Weaknesses identified in others

- **V1's decision-recording objections overreach.** R1-F6 says D-P2-13 covers only directories, but it explicitly maps both HALTs to blocked (`plan:58`); the unresolved High/Medium HALT belongs to Stage 10, not 10.5 (`src/superclaude/skills/sc-tasklist-protocol/SKILL.md:1608,1612,1631`). R1-F9's table is not wholly missing: the plan already labels D-P2-1 through D-P2-17 as decisions for approval, and Task 21 repeats that duty (`plan:45-62,367`). Retain genuinely uncovered details, not duplicate recording requirements.
- **V1's R1-F8 is an ambiguity warning, not an instruction to break the audit.** Exact stripped line text is part of the classification key (`tests/skills/test_worker_contract.py:1165-1166`), but the plan already forbids editing classified lines (`plan:42`). Prefer clearer new-line instructions; do not describe the conflict as unavoidable.
- **V3's workflow-test claim is too strong.** R3-F3 says the existing test pins the old path, but it checks reflect, deviation-patterns, runs.jsonl, left-out wording and WC-4, not `.dev/reflect/` itself (`tests/skills/test_worker_contract.py:837-844`). Add path coherence coverage; do not claim an existing path assertion must be changed.
- **V3's dirty-tree example is outside the check's scope.** R3-F13's `.dev/reflect` folders cannot fail the `src tests plugins`-limited equality command (`plan:372`). Baseline handling remains useful for unrelated changes inside those roots, but R2-F4 is the cleaner clean-tree defect.
- **V3's blanket drift labels confuse improvement with deviation.** R3-F9's missing Write bullet is a useful consistency observation (`src/superclaude/commands/cleanup.md:46-51`; `src/superclaude/commands/improve.md:46-51`), but the spec explicitly mandates the explain tool fix, not the same bullet for every command (`spec:168`). Likewise, no test or static check has actually been run by this advocate.

## Concessions

- V2 missed the strongest nested-propagation problem (R3-F1), the two optional nested branches (R3-F4/R3-F5), workflow's stale directory clause and V1's conditional CLI-mode gate question. V2 must not be selected alone as the complete audit.
- R2-F1's suggested identification from a fresh digest does not define which settings must be explicit and which defaults are acceptable. That boundary needs an owner decision, not a reviewer-invented mandatory flag list.
- R2-F4's P2 severity is debatable; it is a report/manifest completeness defect, not demonstrated runtime corruption. P3 is acceptable if the merged card preserves its clean-tree reproduction.
- R2-F5 is not plan drift. The matrix omits the two spans, but `plan:27` already includes both obligations; correct the review evidence rather than presenting missing plan requirements (`source:14`; `matrix:25-36`).
- V2's universal `Drift` label and 0.94 self-confidence were too broad. Separate unmet obligations, under-specified decisions, review-process gaps and non-deviation observations. No regression in executable behavior is demonstrated by reviewing an unexecuted plan.

## Diff-point positions (table)

| Point | Superior handling | Reason |
|---|---|---|
| S-001 | merge | Keep V3's negative-evidence section, but qualify completeness claims against its own missed dependency (R3-F1; `plan:286`). |
| S-002 | merge | V2's five findings are focused but omit real conditional calls shown by V3 and the V1 template concern (R2-F2; R3-F1; R1-F3). |
| S-003 | V2 | Explicit repo-relative paths make V2 evidence directly traceable; retain the other cards' inference labels and define shorthand as above (R2-F1 evidence; `spec:164`, `plan:248`). |
| C-001 | V2 | Separate missing-suite and missing-safety-input assertions capture the actual omitted resolution, subject to a required-input decision (R2-F1; `spec:164`, `plan:248`). |
| C-002 | merge | V1/V3 find the stale clause; preserve additive clarification but correct V3's claim about the existing path pin (R1-F1/R3-F3; `workflow.md:72` under commands; `tests/skills/test_worker_contract.py:837-844`). |
| C-003 | V2 | V2 covers all fifteen clauses, the conditional local sentence and the inflated matrix claim, not only a phrase token (R2-F3; `source:7`, `matrix:14`). |
| C-004 | V2 | Condition/outcome reversal negatives detect semantic breakage that label-deletion tests miss (R2-F2; `plan:97,179,345`). |
| C-005 | V2 | The staged package is absent even on a clean tree; V3's `.dev/reflect` example is excluded by the command (R2-F4; `plan:367,371-372`). |
| C-006 | merge | Keep the concrete light-arm output mismatch; treat deep-arm rerouting as optional, since the brief expressly allows recorded skipping (R3-F12/R1-F5; `source:12`; `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:189-190`; `src/superclaude/commands/research.md:103`). |
| C-007 | merge | Clarify both locations: preserve classification keys and add flag rows/new lines without rewriting the existing flag list (R1-F8/R3-F8; `plan:42,233`; `src/superclaude/commands/task.md:44-48`). |
| C-008 | merge | Use explicit requirement-based classes; V1 differentiates but mislabels workflow, while V2/V3 overuse drift (R1-F1/R2-F5/R3-F9; `plan:27,303`; `spec:168`). |
| X-001 | V2 | P1 is defensible for removing the required pre-launch block; do not assert inevitable unsafe execution before the policy is defined (R2-F1; `spec:164`; `src/superclaude/skills/sc-cli-eval-protocol/SKILL.md:135-150`). |
| X-002 | V3 | Leaving contradictory output-location guidance is drift, not a necessary deviation; an additive scoped override is available (R3-F3; `plan:303`; `src/superclaude/commands/workflow.md:72`). |

For C-002's shortened `workflow.md` citation, the full path is `src/superclaude/commands/workflow.md`.

## Shared assumptions (A-001..A-003)

### A-001 — QUALIFY

There are nameable candidate settings, but no established mandatory-explicit subset. The diff's premise that none is labelled a safety flag is factually wrong: W3 expressly calls the digest options “the safety flags” and lists them (`src/superclaude/skills/sc-cli-eval-protocol/SKILL.md:137-139`). Nevertheless, spec row 164 does not define a required set or omission/default policy, and W3 explicitly permits omitting `--no-pty` for a real run (`spec:164`; the same skill:144-146). Therefore retain the missing-block finding while requiring an owner-approved policy for required inputs/values and accepted defaults. Do not require all listed flags, and do not quietly equate “supplied” with “complete”.

### A-002 — QUALIFY

The one-deleted-line cap is binding for executing this plan as written (`plan:41,303,317`), not an immutable external allowance. SA-4 permits specific defect-fix changes and is still authoritative (`spec:211`). Prefer an explicit additive unattended override resolving the stale workflow/ref wording within the current cap. If a second command-line replacement is chosen, obtain a revised, justified exemption and update its check before execution; an advocate cannot silently authorize that widening. Skill/ref files generally lack this cap, with the named remediation-handoff exception (`plan:41`).

### A-003 — ACCEPT

The general nested rule governs actual command/protocol invocations even when a section 3 row does not enumerate them (`spec:60-62`; `plan:26`). Thus Stage 9 task requires propagation, Part 4 analyze requires propagation if selected (or an explicitly selected inline branch), and reflect's deep tech-research needs a documented gate-free/skip resolution (`src/superclaude/skills/sc-tasklist-protocol/SKILL.md:1539-1557`; `src/superclaude/skills/sc-release-split-protocol/SKILL.md:324`; `src/superclaude/skills/sc-reflect-protocol/SKILL.md:632`). This does not mean passing flags to every ordinary Agent-tool reviewer: command-owned fan-out stays unchanged under WC-7 (`spec:75`).

## Unique contributions (table)

| ID | Disposition | Evidence-backed treatment |
|---|---|---|
| U-001 | correct | Keep R3-F1 as P1 for unattended prompt/stall exposure; propagate through initial and loop-back task calls and add Task 12 dependency; drop inevitable commit/push framing (`src/superclaude/skills/sc-tasklist-protocol/SKILL.md:1539-1557`; `plan:233,286-290`). |
| U-002 | keep | R3-F4 finds an unresolved conditional analyze call; explicitly choose inline verification or nest analyze (`src/superclaude/skills/sc-release-split-protocol/SKILL.md:324`; `plan:179`). |
| U-003 | keep | R3-F5 finds optional deep tech-research; give it an explicit unattended resolution consistent with the general rule (`src/superclaude/skills/sc-reflect-protocol/SKILL.md:632`; `plan:26,276`). |
| U-004 | correct | Keep R1-F3 as a conditional full-gate clarification, not proof that every tdd run invokes the CLI arm or that local `--fix/--promote` is itself forbidden (`plan:261`; `src/superclaude/skills/task-builder/SKILL.md:2235-2240`). |
| U-005 | keep | Record the spec-panel socratic non-waiting decision; do not assume business-panel's refusal automatically applies to this mode (`plan:55,136`; `spec:162,180`; `src/superclaude/commands/spec-panel.md:123-125`). |
| U-006 | correct | D-P2-13 already covers both HALTs; retain only clarification of the depth-map location, which need not move merely because per-phase outputs move (`plan:58,290`; `src/superclaude/skills/sc-tasklist-protocol/SKILL.md:1608,1641`). |
| U-007 | correct | Preserve bounded negative evidence: the src/tests search found only tasklist-skill documentation/instructions and test comments, not a runtime consumer; do not call this proof for generated/external consumers (`tests/tasklist/test_tasklist_cli.py:568-580`; `src/superclaude/skills/sc-tasklist-protocol/SKILL.md:1628,1641`). |
| U-008 | drop | Drop the missing-table defect: decisions are already enumerated for approval and assigned to the report; a compact table is optional presentation (R1-F9; `plan:45-62,367`). |
| U-009 | correct | Retain R2-F5 as two missing review-matrix rows, not plan drift; both duties already exist in the plan (`source:14`; `plan:27`; `matrix:25-36`). |
| U-010 | correct | Narrow R3-F6 to tasklist's now-stale reason; task handoff routes to task-builder, so do not declare both skills converted (`src/superclaude/commands/brainstorm.md:158`; `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:349-352`; `plan:56,290`). |
| U-011 | correct | Task 3 already names improve's Approval Required/Explicitly Will NOT anchors; only the inherited Safety Threshold instruction lacks a counterpart (`plan:110`; `src/superclaude/commands/cleanup.md:123-127`; `src/superclaude/commands/improve.md:117-129`). |
| U-012 | correct | Keep the Write-bullet consistency observation, not a claimed mandatory spec deviation; explain has an explicit requirement (`src/superclaude/commands/cleanup.md:46-51`; `src/superclaude/commands/improve.md:46-51`; `spec:168`; `tests/skills/test_worker_contract.py:847-851`). |
| U-013 | keep | Add the recommend routing test to the format baseline because Task 6 edits it and Task 21 compares edited test files (`plan:73,149,364`). |
| U-014 | keep | Remove the nonexistent equality-only case instruction: current negatives use missing/extra/repeated inputs and unknown `extra`, not an extra P2 key (`plan:78`; `tests/skills/test_worker_contract.py:1001-1012`). |
| U-015 | correct | Keep individually corroborated checks (eleven deferred entries found; actual auggie options exist), but do not endorse the complete dependency/nesting graph: R3-F1 itself disproves completeness (`plan:42,286,345`; `src/superclaude/commands/auggie-review.md:49-57`; deferred-entry search of `tests/skills/test_worker_contract.py`). |

Recommended merge action: preserve the concrete missing resolutions and relationship-level tests, correct the overstatements above, and present the undefined safety-input policy for owner decision. This statement changes no plan or implementation file. Tests, live runs and a full plugin-parity audit were not performed.
