# Round 1 — Advocate for Variant 2

## Position summary

Variant 2's strongest finding survives: the entry check demands a post-window statement from a summary whose producing task explicitly puts the window afterward (P4:37; S3:158,162). I defend its cap-check and coverage-accounting observations as minor, but withdraw its generation-order claim as a blocking content defect; V1's mapping-test discovery deserves a qualified verification finding, not a certain future red test (V2:25-27; Request:3; P4:20,36; S3:122).

Citation key: paths are relative to `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel`; `alias:line` means the following file at that line.

- **P4** = `.dev/tasks/to-do/TASK-WF-blockerStage4-20261116-030206/TASK-WF-blockerStage4-20261116-030206.md`.
- **Request** = `.dev/tasks/to-do/TASK-WF-blockerStage4-20261116-030206/source.md`.
- **S1** = `.dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md`.
- **S3** = `.dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/TASK-WF-blockerStage3-20261116-030158.md`.
- **OLD** = `.dev/tasks/to-do/TASK-WF-loosenBlockerRev-20261115-210254/TASK-WF-loosenBlockerRev-20261115-210254.md`.
- **Ledger** = `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/stage-requests/README.md`.
- **Matrix** = `.dev/reflect/pre-TASK-WF-blockerStage4-20261116-030206-20261116030426/artifacts/coverage-matrix.yaml`.
- **ADV** = `.dev/reflect/pre-TASK-WF-blockerStage4-20261116-030206-20261116030426/adversarial/adversarial`; **V1**, **V2**, **V3** mean its `variant-1-original.md`, `variant-2-original.md`, `variant-3-original.md` respectively.
- **Mapping** = `tests/skills/test_review_severity_mapping.py`; **Panel** = `src/superclaude/commands/spec-panel.md`; **Brief** = `tests/skills/test_review_brief_placement.py`; **RuleTest** = `tests/skills/test_review_severity_rule.py`.

## Steelman

### Variant 1

Its strongest case is not stylistic: the existing mapping test explicitly requires the very phrase Task 5 removes, and it tests both spec-panel surfaces; this is a concrete dependency a plan review should inspect (V1:11; Mapping:24-27,50-76; P4:89). Its audit-summary mismatch also identifies a real unmet check, independently of whether generation was authorized (V1:9; P4:37; S3:158,162). The limitation is that a present-day pin is not automatically the stage-4-entry pin: stage 3 explicitly migrates the Medium/cadence assertions to the canonical references, so a certain future failure needs evidence of which pins remain (S3:122,125,127).

### Variant 3

Its strongest case is the ordered state walk: the registry and allow-list are updated before copying, any later registry edit triggers another copy, and tests run only after those operations; transient missing files between the first two operations are not a failing task result (V3:20-27; P4:99-102). It also correctly distinguishes tracked-tree coverage from parity coverage and recognizes the registry's logical-path/surfaces model (V3:11,13; S1:96,209). Its limitation is certainty: the second-row representation is ambiguous before the registry implementation exists, and the hypothetical insertion of a consumer line inside a digest is not an instruction the plan actually gives (S1:96; P4:70,99; V3:15).

## Strengths claimed

- **D2 / C-001 is the central blocking defect.** A compliant stage 3 summary says the window runs afterward and its triggers cannot yet be judged; P4 separately requires that same file to attest the window has passed. An executor cannot produce the required evidence by following the stated producing and consuming tasks alone (S3:158,162; P4:37).
- **D3 / C-011 identifies a narrow checking omission, not a cap change.** The request specifically preserves cap sentences by content, while Task 2's acceptance checks name digests, pointers, zero-findings and no-minimum wording without quoting the protected cap; the global prohibition still governs (Request:12,20; P4:22,53-55).
- **D4 / C-012 separates accounting from implementation.** The matrix's INF-002 quote omits the package-id instruction, which the actual plan includes; this calls for a matrix correction, not a new implementation task (Matrix:10-14; Request:7; P4:19).
- **The base comparison prevents reopening resolved scope problems.** OLD requires five digest templates; P4 instead assigns four digests and analysis-only merge text with an 11-row invariant. OLD copies before registration; P4 expressly registers and allow-lists before copying, and repeats the copy after a registry change (OLD:490,493,546; P4:33,38-39,99; Request:11,14).

## Weaknesses identified

- **V2's labels are inconsistent.** D1 and D2 simultaneously say `MAJOR; blocking true` and `Table severity: MEDIUM`; D3 and D4 add a second LOW scale to MINOR. The merged card needs one authoritative grade per row, not two unexplained scales (V2:21-27).
- **V2 overstates C-010.** Request:3 and Ledger:9 require generation after go, and Ledger:20-21 do not record that go. That is evidence of an unmet generation procedure, not proof the future conditional plan is wrong: P4:20 still conditions execution on the predecessors and P4:36 fails closed on a missing go. An empty ledger proves absence of the required record, not what was said in all chat history; retain the provenance concern outside content blockers.
- **V2 missed a real dependency.** Mapping:58,71-76 pins the old list and cadence, while Panel:259-260 contains them and P4:89 removes the list phrase. However, S3:122 explicitly migrates the Medium/cadence pins into the full rule and scale map and S3:127 requires replacement pins; it is possible for compliant stage 3 execution to remove the exact spec-panel literals before stage 4. Therefore C-002 should identify the absent stage-4 re-check/ownership, not assert a guaranteed failing future test (P4:88,102).
- **V2's acceptance-only reassurance is narrower than a suite result.** Its claim about no later task falsifying earlier acceptance does not establish that every connected test remains green; the source/plugin prompt byte-equality test is another dependency worth checking after Task 5 (V2:55; Brief:129-134; P4:84,90).

## Concessions

1. Withdraw D1's blocking grade and drop C-010 from plan-content defects; an execution hold until recorded go is still required, but editing the plan cannot retroactively repair generation history (Request:3; Ledger:9; P4:20,36; V2:21).
2. Keep D2 blocking, and D3/D4 minor; remove the competing MEDIUM/LOW table labels rather than treating the label inconsistency as another execution blocker (V2:21-27; P4:37; S3:158,162).
3. Accept V1's mapping/byte-parity dependency discoveries as useful additions, but not its unconditional red-test prediction without the predecessor's re-pinned test. Separate in-place editing is compatible with byte identity when the same changes are applied, so there is no demonstrated inevitable parity failure (Mapping:58,71-76; S3:122; Brief:134; P4:84,90).
4. Accept the missing final-sentence ordering pin as minor only: the requested audit-window content is present, even though Task 7 also says to list open items afterward (Request:16; P4:111,116; V2:48).

## Shared assumptions

- **A-001 — QUALIFY.** Treat the stage 1/stage 3 plans as the conditional entry contract, not completed implementation evidence. In particular, stage 3 explicitly changes the mapping pins, so today's test cannot be assumed unchanged at stage 4 entry; revisit findings if the predecessor contract changes (P4:20; S3:122,125,127).
- **A-002 — QUALIFY.** Explicit evidence requirements must hold, but a sentence reference is not automatically a case-sensitive shell command. P4:24 calls for content pins and P4:36 explicitly halts on missing go; this supports the substantive audit mismatch, not promotion of every capitalization defect into a blocker (P4:37,64).
- **A-003 — ACCEPT.** P4:37 explicitly makes the summary file the subject of “exists and states”; the preceding ledger-go check is a different acceptance bullet. Reading the ledger as a substitute would repair the requirement rather than satisfy it as written (P4:36-37; S3:158,162).

## Per-point positions

Grades concern defects in the merged review, not how strongly an advocate phrases them. “Drop” removes a standalone finding, not its underlying evidence from the discussion.

| point | grade | evidence |
|---|---|---|
| S-001 | minor | V2:19-27 uses D-rows/deviation headings; this is a card-format difference, with no demonstrated lost plan result. |
| S-002 | minor | V2:21,23 attaches both MAJOR/blocking and MEDIUM to each row; normalize the unexplained scales without inventing a runtime failure. |
| C-001 | blocking | P4:37 demands a passed-window attestation from the summary; S3:158,162 produces that summary before the window and assigns no later attestation update. |
| C-002 | minor | Mapping:58,71-76 conflicts with P4:89 today, but S3:122,125,127 migrates/replaces those pins before entry; require an explicit stage-4 mapping-test re-check, not an unproven guaranteed red test. |
| C-003 | minor | P4:33,59 calls it the scan test's allow-list; S3:144,149 explicitly stores that list in scale-map.md, so clarify the location rather than claim missing scope. |
| C-004 | minor | P4:64 uses capitalized “After 2 fix cycles”; `src/superclaude/skills/tdd/refs/build-request-template.md:125` uses lowercase “after”; this is wording, not a specified case-sensitive grep failure. |
| C-005 | minor | Panel:332 also contains the forbidden list phrase outside P4:84's named anchors; P4:89 makes replacement necessary, so name FR-8 explicitly to remove the edit-scope ambiguity. |
| C-006 | minor | Brief:134 demands full prompt byte identity and S3:122 preserves digest/cap checks; P4:88,102 does not re-run those tests after the final edits, a verification-instruction gap without a proven failure. |
| C-007 | minor | P4:90 requires the same pointer while P4:84 never explicitly orders adding it to spec-panel; clarify the instruction, and preserve Request:16's final-sentence order in P4:111. |
| C-008 | minor | P4:36-37 places go/evidence checks in acceptance after the edit body at P4:33, but P4:20 already forbids running before the prerequisites; repeat them as an explicit pre-edit check. |
| C-009 | minor | P4:39,73 uses “T1 passes” and “consumer-line instruction” while P4:24 asks for content pins; the task body at P4:70 supplies the intended consumer example, so this is pin wording, not missing functionality. |
| C-010 | drop | Request:3 governs when to generate; P4:20,36 retains the future execution gate. Premature generation is a process/provenance note, not a demonstrated wrong plan-content result. |
| C-011 | minor | Request:12 protects cap content, while P4:53-55 quotes no cap sentence; add the content pin without claiming the global cap prohibition at P4:22 disappeared. |
| C-012 | minor | Matrix:10-14 truncates Request:7 before the package-id instruction; P4:19 already implements it, so repair coverage wording/accounting only. |
| C-013 | minor | S1:209 specifies tracked-tree T2 and P4:99-102 never explicitly tracks the new mirror before scanning; clarify verification wording, since the required T15 parity independently checks mirror content. |
| C-014 | minor | S1:96 uses logical paths plus surfaces, but P4:99 requests an additional canonical row using a repository-path description; clarify its representation rather than predict an unimplemented resolver failure. |
| C-015 | drop | P4:70 never orders insertion inside a digest, and P4:99-102 re-runs registry equality at the end; the damaging placement is speculative, with the earlier re-check wording already covered by C-006. |
| X-001 | drop | V2:55 discusses acceptance endpoints and V3:27 only the three Task-6 tests; neither claims the mapping test is green, so the dependency concern belongs in C-002, not a separate contradiction. |
| X-002 | drop | Brief:134 requires byte identity, but P4:84's separate in-place edits can produce identical rules prompts and P4:90 requires parity; no inevitable inconsistent final state follows, and the missing test reminder is C-006. |
| X-003 | drop | The MAJOR/MEDIUM conflict is visible at V2:21 and already retained as S-002; do not count the same card-format defect twice. |

Verification limit: this statement re-read the cited plan, request, predecessor contracts, existing tests and command text; it did not execute or implement the plans, and claims about future registry/scan behavior remain conditional on those contracts (S1:96,209; S3:122; P4:20).
