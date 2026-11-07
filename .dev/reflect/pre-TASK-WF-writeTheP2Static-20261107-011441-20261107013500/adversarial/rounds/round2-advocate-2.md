# Round 2 — Variant 2 advocate (QA)

## Citation key and scope

Repository root: `/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P2`.

- `plan` = `.dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/TASK-WF-writeTheP2Static-20261107-011441.md`.
- `source` = the same package's `source.md`.
- `spec` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`.
- `matrix` = `.dev/reflect/pre-TASK-WF-writeTheP2Static-20261107-011441-20261107013500/artifacts/coverage-matrix.yaml`.
- `D` = `.dev/reflect/pre-TASK-WF-writeTheP2Static-20261107-011441-20261107013500/adversarial`.
- Other file paths below are repository-relative. A citation such as `plan:248` resolves to the exact file above, not a variant's paraphrase.

Read all three original cards, all three Round 1 statements, and `D/rounds/round2-advocate-1.md`. Re-read the underlying plan, brief, relevant specification sections, and the source excerpts used below. This is a read-only rebuttal, apart from this output file; no plan execution, tests or live operations were performed.

## 1. Response to criticisms of Variant 2

### Steelman before rebuttal

V1's strongest criticism is that precision is not completeness: V2 misses the nested-call class and the stale workflow contract. V3 demonstrates that omission with actual Skill invocations, not hypothetical paths. V1 also correctly distinguishes a report-manifest defect from a runtime safety defect. These are good reasons not to use V2 alone as the complete audit. They do not displace V2's condition/outcome tests, F1 coverage finding, or missing cli-eval block.

### Criticism-by-criticism disposition

| Criticism | Concede or counter | Evidence and updated position |
|---|---|---|
| V2 omitted nested-call coverage and the stale workflow clause (V1 Round 1:27-28; V3 Round 1:27; V1 Round 2:39). | **Concede the omissions.** | Tasklist Stage 9 invokes `sc:task` and repeats the call on loop-back (`src/superclaude/skills/sc-tasklist-protocol/SKILL.md:1539-1557,1607`), whereas Task 16 covers reflect only (`plan:290`). Release-split allows analyze (`src/superclaude/skills/sc-release-split-protocol/SKILL.md:324`); reflect lists optional tech-research (`src/superclaude/skills/sc-reflect-protocol/SKILL.md:632`). Workflow's old directory remains explicit (`src/superclaude/commands/workflow.md:72`; `src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md:52`), while Task 17 changes the nested destination (`plan:303`). Add these findings. |
| V2 “never opened the skill bodies” (V1 Round 2:39). | **Counter the unsupported process claim; concede inadequate coverage.** | V2's card reports inspection of helpers, nesting tests and classifications, but does not establish a complete skill-body sweep (`D/variant-2-original.md:98-104`). Its omissions prove that the sweep was insufficient, not which files were never opened. I cannot reconstruct the original review's tool history from its card. The measurable defect is missing call coverage. |
| Self-confidence 0.94 was excessive; every finding was labelled Drift (V1 Round 1:29,33; V3 Round 1:27). | **Concede.** | Those values are explicit in `D/variant-2-original.md:16,36,57,76,93,97`. In particular, R2-F5 concerns the review matrix, while both underlying duties already appear in `plan:27`. Separate plan defects, owner-policy questions and review-process observations; do not manufacture a deviation class for a note. |
| R2-F3 conflated prose and executable coverage; the true explicit phrase-list count is two. | **Clarify, not withdraw.** | Cleanup and improve list `left out (WC-4)` as expected phrases (`plan:97,110`); research, cli-eval and tdd describe exclusions without that phrase in their entries (`plan:123,248,261`). `matrix:14` claims five commands are test-pinned. The distinction is the substance of R2-F3, not a claim that five are correctly pinned. Keep the plan-test gap and correct the separate matrix overstatement. |
| R2-F4 should be P3 because the package is already staged (V1 Round 1:31; Round 2:40). | **Concede P3; counter dismissal of the clean-tree mismatch.** | `plan:367` stages the package and defines the report's five source/test/plugin groups; `plan:371` separately checks staged package paths. Neither adds them to the report list whose equality test explicitly queries only `src tests plugins` (`plan:372`). `source:16` requests the exact paths for the owner-approved commit. “Clean-tree reproduction” means this inconsistency needs no unrelated dirty files, not that staging or runtime necessarily fails. Include plan-produced task-package paths in the manifest and its comparison, without absorbing unrelated pre-existing paths. |
| R2-F5 is not plan drift (all advocates). | **Concede and retain only as a review-process observation.** | `matrix:25-36` has no separate rows for clause placement and pre-change failure, while `source:14` requires them and `plan:27` already states both. Correct the matrix, not a supposedly absent plan requirement. |
| A static plan cannot prescribe safety-input identification from a fresh digest; it must name a fixed flag set (V1 Round 1:32,75). | **Counter the categorical claim; concede the missing policy.** | The existing protocol requires the fresh load before either pipeline and makes its digest the only authority for later flags/fields (`src/superclaude/skills/sc-cli-eval-protocol/SKILL.md:46-58`). A static plan can prescribe that runtime validation procedure. What a digest alone cannot supply is the owner's policy for which values must be explicit and which defaults count as sufficient. Require that policy plus separate missing-suite and missing-safety-input assertions; do not freeze an invented mandatory list. |
| V2 lacks the concrete missing-phrase inventory supplied by V1. | **Concede and merge.** | Task 5 pins a filename instead of an Improve condition/outcome phrase (`plan:136`); Task 13 has no safety-input resolution (`plan:248`); Task 16 has one generic `blocked_question` for multiple HALTs (`plan:290`). Add that inventory to V2's relationship-level test requirement. |

### Severity correction without a new exaggeration

I continue to support **P1 for X-001**: the specification explicitly requires a pre-launch block that Task 13 omits (`spec:164`; `plan:248`). This is a plan-level safety-contract omission pending an owner-approved input/default policy. It is **not evidence of an observed unsafe run**, and not proof that every invocation has “no safety inputs.” V1 Round 2:86 goes too far on that last point: Task 13 expressly permits flags supplied in the brief. The defect is accepting an invocation without checking its required completeness.

## 2. Updated assessment of V1 and V3 after their defenses

### V1

**Steelman.** V1's complete-gate question remains valuable: Task 14 disables only staging, while the conditional CLI-mode action couples staging with a wrapper invocation (`plan:261`; `src/superclaude/skills/task-builder/SKILL.md:2235-2240`). V1 also adds the return-contract reference to the stale workflow finding and supplies specific Tasks 5/13/16 for the gate-test merge. Its Round 2 concessions on X-002, the recorded HALTs and the duplicated decision table improve the proposed merge.

**Remaining correction.** V1 Round 2:24 says local `--fix` edits and `--promote` moves are themselves outward actions prohibited under unattended mode. That is not established by WC-9. The specification names outward defaults and git writes, not a blanket prohibition on local edits or folder moves (`spec:77`); its reflect row makes `--no-promote` conditional on coordinator ownership (`spec:148`). The plan likewise leaves Wave 7 promotion unchanged with that conditional flag (`plan:276`). Keep U-004 as an unresolved conditional wrapper-integration rule, not as proof that every local mutation is forbidden. The spec's citation of the same staging line proves staging must be refused; it does not automatically ban every other operation on that line.

V1's Round 2 “new evidence” about Task 12 dependency and the Task 20 literal is useful integration guidance, but was already in V3's original suggested fix (`D/variant-3-original.md:25-27`). Do not count it as an independent new discovery.

### V3

**Steelman.** V3 still supplies the best base: actual nested-call coverage across three missed branches and a separate negative-evidence section. Stage 9's initial and repeat invocations make U-001 concrete. The general rule is stated in `spec:62`, not invented from an expansive reading of a command row. V3's Round 1 concessions also correctly narrow the claimed workflow test pin: the existing test checks tokens, not the old path (`tests/skills/test_worker_contract.py:837-844`).

**Remaining correction.** Do not carry `verified_ok` as a blanket certificate. The original card calls dependency chains correct while its own R3-F1 asks for a missing Task 12 dependency (`D/variant-3-original.md:25-27,184`). “Listed edges exist” is weaker than “all required edges are present.” Likewise, agreement between nesting tables does not establish call-site completeness: Task 20 currently hardcodes tasklist's reflect-only list (`plan:345`). Preserve each bounded check and its scope, not the broad completeness wording.

Drop R3-F13's `.dev/reflect` counterexample: that root is excluded by `plan:372`. Narrow R3-F6 to the tasklist handoff, because the task handoff invokes `task-builder`, not the converted `/sc:task` command (`src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:349-352`). These corrections do not erase V3's coverage advantage.

## 3. New evidence and implications

These additions rely on source details not used as evidence in the supplied earlier arguments, rather than renaming an existing contribution.

1. **The runtime digest is explicitly authoritative, not merely available.** The core objective forbids stale or hardcoded eval contracts, and Wave 0 requires reloading any flag/field absent from the digest (`src/superclaude/skills/sc-cli-eval-protocol/SKILL.md:30-33,46-58`). This strengthens the counter to a mandatory frozen flag inventory in the static plan. The merge should distinguish a stable owner-approved safety policy from the current CLI facts used to validate it.

2. **A workflow override added on a later line is invisible to the current artifacts extractor.** `_artifacts_clause` chooses the first matching line and returns only the suffix after its first key; it does not collect later explanatory lines (`tests/skills/test_worker_contract.py:770-775`). Task 17 explicitly proposes an added reference-file line while preserving the old clause (`plan:303`). Therefore an additive scoped override can fix prose, but the path-coherence test must deliberately read that override or the relevant section too. Adding another token assertion against `_artifacts_clause` alone does not prove the override and old clause agree. This strengthens C-002 without reviving V3's false claim that an old-path pin already exists.

3. **The inherited section helper really checks presence, not relationships.** `_check_unattended_section` asserts each expected phrase occurs somewhere in the section (`tests/skills/test_worker_contract.py:509-512`); `_remove` strips tokens/phrases (`:533-534`). Task 20 proposes deriving gate phrases from the earlier entries and removal negatives (`plan:345`). This is direct evidence for C-004's testing risk, beyond inspecting the plan's example vocabulary. It is not a claim that the future dedicated gate helper is already implemented incorrectly. Require complete condition/outcome phrases and reversal negatives to prevent that implementation.

4. **The CLI-mode gate's emitted output location is another integration question, not proof of an outward-action violation.** Its verification text locates wrapper artifacts under the task directory's `reflect/post/<short-sha>/` unless an explicit output is passed (`src/superclaude/skills/task-builder/SKILL.md:2239`), while the emitted invocation on `:2237` passes no output directory. If the unattended branch retains this conditional gate, settle output/contract ownership and propagation as well as staging and HALT handling. Whether the tdd path actually selects that CLI arm is not proven here; do not claim every tdd run reaches it. This is a more precise reason to retain U-004 than categorically forbidding local edits and moves.

## 4. Final per-point position table

“Merge” means combine complementary contributions after the stated corrections, not retain every original claim.

| Point | Winner | Final position |
|---|---|---|
| S-001 | merge | Keep V3's `verified_ok` section, with individually bounded claims rather than a complete dependency/nesting certificate. |
| S-002 | merge | Use V3's coverage as the spine; add V2's verification depth and V1's conditional wrapper gate. Finding count alone is not quality. |
| S-003 | V2 | Explicit repository paths and line numbers; retain inference labels and define aliases where used. |
| C-001 | merge | V2's separate missing-suite/missing-safety-input cases, with an owner-approved required-input/default policy and digest-grounded validation. Do not require all example flags. |
| C-002 | merge | V1's command/ref coherence, V3's drift diagnosis, and an explicit path-coherence check. Existing token pins do not assert the old path; later-line overrides need section-aware verification. |
| C-003 | merge | V2's all-fifteen clause scope, conditional report sentence and matrix correction; V3's single parametrized-test shape. |
| C-004 | merge | V2's condition/outcome phrases and reversal negatives, plus V1's concrete Tasks 5/13/16 inventory (`plan:136,248,290,345`). |
| C-005 | V2 | Keep the clean-tree manifest omission, **P3**, not a runtime failure. Compare the complete plan-produced commit manifest, including the task package; reject V3's out-of-scope dirty-folder example. |
| C-006 | merge | Keep V3's light-arm output-consumption ambiguity (`src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:189`; `src/superclaude/commands/research.md:103`). V1's deep reroute is optional: the brief expressly allows recorded skipping (`source:12`). |
| C-007 | merge | Task 12's flag-list instruction conflicts with new-lines-only (`plan:233`; `src/superclaude/commands/task.md:44-48`). V1's classified-line issue is wording ambiguity constrained by `plan:42`, not an inevitable audit break. |
| C-008 | merge | Classify actual departures by the four-category taxonomy. Keep observations outside the deviation list; do not rename “none” into a false deviation or treat pending owner approval as authorization. |
| X-001 | V2 | **P1 supported.** Missing required pre-launch block (`spec:164`; `plan:248`), with the mandatory-input/default policy still unresolved. No observed unsafe launch is claimed. |
| X-002 | V3 | **Drift.** Stale output guidance is an overlooked inconsistency, not a necessary departure forced by the spec. |
| A-001 | merge | **Qualify/correct premise.** W3 labels the candidates safety flags (`src/superclaude/skills/sc-cli-eval-protocol/SKILL.md:137-146`); a mandatory-explicit subset is not defined. Preserve runtime digest authority and obtain the policy. |
| A-002 | merge | **Qualify.** The cap is the plan's binding execution constraint (`plan:41`), not an immutable spec allowance (`spec:211`). Use scoped additive clarification or obtain a justified revised exemption; an advocate cannot authorize widening. |
| A-003 | V3 | **Accept; STATED.** `spec:60,62` expressly covers nested command/protocol calls; individual section 3 rows are not exhaustive call inventories. Preserve ordinary command-owned fan-out under WC-7 (`spec:75`). |

## 5. Updated unique-contribution disposition

| ID | Disposition | Treatment in the merged result |
|---|---|---|
| U-001 | **correct** | Keep P1 for unattended prompt/stall exposure; drop automatic commit/push harm. Propagate to initial and loop-back task calls, add Task 12 dependency, update Task 16 entry and Task 20 literal (`src/superclaude/skills/sc-tasklist-protocol/SKILL.md:1539-1557,1607`; `plan:233,286,290,345`). |
| U-002 | **keep** | Resolve the optional Part 4 analyze call as explicitly inline verification or nested analyze (`src/superclaude/skills/sc-release-split-protocol/SKILL.md:324`; `plan:179`; `spec:62`). |
| U-003 | **keep** | Explicitly settle optional deep tech-research by the general gate-free/recorded-skip rule (`src/superclaude/skills/sc-reflect-protocol/SKILL.md:632`; `plan:26,276`). |
| U-004 | **correct** | Keep the conditional full-gate integration question. Staging is prohibited; local fix/promotion is not automatically an outward action. If retained, settle wrapper arguments, output ownership and HALTs (`spec:77,148`; `plan:261,276`; `src/superclaude/skills/task-builder/SKILL.md:2235-2240`). |
| U-005 | **keep** | Record the socratic non-waiting decision or refuse the mode; do not infer its behavior solely from business-panel's precedent (`plan:55,136`; `spec:162,180`). |
| U-006 | **correct** | Drop the claim that D-P2-13 omits HALT mappings: `plan:58` records both. Keep only the depth-map ownership/location clarification; relocation is not automatically required (`src/superclaude/skills/sc-tasklist-protocol/SKILL.md:1641`). |
| U-007 | **correct** | Keep a bounded repository-reader check/AC suggestion, not proof that external/generated consumers do not exist. The cited test is documentation/invariant checking, not a filesystem reader (`tests/tasklist/test_tasklist_cli.py:568-580`). This round did not repeat a full consumer search. |
| U-008 | **drop** | The decision list and owner-approval report duty already exist (`plan:45-62,367`). A compact table is optional presentation, not a missing requirement. |
| U-009 | **correct** | Retain two missing review-matrix rows as review-process observations; both underlying obligations already exist in the plan (`source:14`; `plan:27`; `matrix:25-36`). |
| U-010 | **correct** | The handoff-skip rationale becomes stale for tasklist, not for the task handoff's task-builder route (`src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:349-352`; `plan:290`). |
| U-011 | **correct** | Improve's own anchors are already named (`plan:110`); narrow to inheriting cleanup's Safety Threshold instruction where improve has no corresponding section (`src/superclaude/commands/cleanup.md:123-127`; `src/superclaude/commands/improve.md:108-129`). |
| U-012 | **correct** | Preserve a tool-list consistency observation, not a mandatory spec deviation. Both lists omit a Write bullet; explain alone has the explicit section 3 requirement and dedicated test (`src/superclaude/commands/cleanup.md:46-51`; `src/superclaude/commands/improve.md:46-51`; `spec:168`; `tests/skills/test_worker_contract.py:847-851`). |
| U-013 | **keep** | Include the recommend routing test in the format baseline, since Task 6 edits it and Task 21 compares edited test files (`plan:73,149,364`). |
| U-014 | **keep** | Remove the nonexistent equality-only P2-key case instruction: current negatives cover missing/extra/repeated names and an unknown `extra` key (`plan:78`; `tests/skills/test_worker_contract.py:1001-1012`). |
| U-015 | **correct** | Keep bounded negative evidence with its actual checked scope. Do not carry a complete dependency/nesting claim: the same V3 card asks to add a missing dependency and nesting edge (`D/variant-3-original.md:25-27,184-189`; `plan:286,345`). No fresh full parity or eleven-entry recount was performed in this rebuttal. |

## 6. Recommended merge base

**Use Variant 3 as the base, corrected as above.** It contributes the three missed nested branches and a place for bounded negative evidence. V2's narrower card should supply the verification standard, not the whole coverage inventory.

Graft V2's cli-eval missing-block finding, relationship-level negative tests, complete F1 coverage and P3 commit-manifest omission onto that base. Add V1's conditional wrapper gate, unrecorded socratic decision, return-contract-reference coherence and specific per-gate inventory. Drop duplicate decision-recording findings and false path-pin/dirty-folder claims. Present the safety-input/default boundary as an owner decision; no advocate's proposed policy counts as approval.

No action on the plan or implementation was taken. The only deliverable changed by this rebuttal is this file; tests, live behavior and full mirror/consumer sweeps remain unverified here.
