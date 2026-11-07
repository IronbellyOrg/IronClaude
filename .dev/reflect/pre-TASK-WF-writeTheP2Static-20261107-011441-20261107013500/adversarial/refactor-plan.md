# Refactoring Plan: Merge into Base (Variant 3)

## Overview

- **Base**: Variant 3 (opus, refactorer), combined score 0.844 (`base-selection.md`)
- **Incorporating from**: Variant 2 (0.725), Variant 1 (0.671), the Round 2 new finding, the Round 2.5 invariant probe
- **Planned changes**: 16 (C1-C16), plus 7 base corrections (B1-B7)
- **Risk level**: Medium. Most changes are appends; three replace base text (C1, C6, C7).
- **Gate**: the debate converged at 100%, but the run is BLOCKED_BY_INVARIANTS on INV-001 and INV-002. C14 and C15 carry them into the merged findings as P1 blocking items.

Merged output rules:

- Every finding carries one of the four classes (Authorized expansion, Necessary deviation, Drift, Regression), assigned per finding (C-008).
- Evidence uses V2's repo-relative file:line form (S-003).
- Each merged finding records its provenance (source variant and finding id).

## Base Corrections (base weaknesses with fixes)

All three advocates accepted these.

### B1. R3-F1 harm wording

- **Target**: R3-F1 (replace the harm sentence; keep P1).
- **Fix**: drop "push" (in sc-task "push" is only a task type, and Stage 9 passes a checklist). State the harm as: (a) attended prompts in a worker; (b) a conditional commit: a TFEP inside the nested `sc:task` keeps the committed-report default (`sc-task-protocol/SKILL.md:61,266`) because Stage 9 passes no `--unattended` (`sc-tasklist-protocol/SKILL.md:1539-1542`), breaking WC-9 (spec:77); (c) the impact path: at STRICT compliance the `sc:impact-protocol` call (`sc-task-protocol/SKILL.md:94`) writes `.dev/impact/task-<slug>` outside the report dir (WC-4, WC-11, spec:72,79).
- **Fix also requires**: Task 16 depends on Task 12; both test literals change (`UNATTENDED_EXPECT` tasklist entry to nested `reflect` and `task`, and the Task 20 `EXPECTED_NESTING` literal, plan:79, plan:290); the nested call passes `--report-dir` and keeps `--compliance strict` (INV-009).
- **Rationale**: Round 1 concessions by all; Round 2 advocate 3 s1 and s3 items 2-3.
- **Risk**: Low.

### B2. R3-F13 example

- **Target**: R3-F13 (delete the `.dev/reflect` dirty-folder example).
- **Rationale**: the equality check queries only `src tests plugins` (plan:372). Round 2 advocate 3 s1; C-005.
- **Risk**: Low.

### B3. R3-F6 narrowed

- **Target**: R3-F6. Applies only to the tasklist handoff; the task handoff calls `task-builder`, not `/sc:task` (`sc-brainstorm-protocol/SKILL.md:349-352`).
- **Risk**: Low.

### B4. R3-F7 narrowed

- **Target**: R3-F7. Covers only the Safety Threshold clause in improve (plan:46).
- **Risk**: Low.

### B5. R3-F2 scope narrowed

- **Target**: R3-F2. Remove the FR-G5 and `--no-pty` parts; plan:248 settles both. The remaining content is replaced by C1.
- **Risk**: Low.

### B6. R3-F12 second half dropped

- **Target**: R3-F12. The second half is already covered by D-P2-1.
- **Risk**: Low.

### B7. verified_ok bounded

- **Target**: `verified_ok` section (replace wording). Each item becomes a bounded claim: "listed edges exist (12->11, 13->5, 16->15, 17->15, 18->4)", never "dependency chains correct" or "all required edges present". Note that B1 adds edge 16->12.
- **Rationale**: Round 2 advocate 2 and advocate 3 s1 (`variant-3-original.md:25-27,184`).
- **Risk**: Low.

## Planned Changes

### C1. cli-eval missing safety block (C-001, X-001)

- **Source**: V2 R2-F1; V3 R3-F2 (after B5)
- **Target**: replace R3-F2
- **Approach**: P1 Drift. Spec:164 requires `--suite` and the safety flags in the brief, else blocked; plan:248 blocks only on a missing `--suite`. Add V2's split assertions (block on missing suite; block on missing safety flags). The flag subset is nameable from `sc-cli-eval-protocol/SKILL.md:128-153`, with the eval-docs-loader digest authoritative (SKILL.md:30-33,46-58). Do not state that `run` "launches with no safety inputs" (the brief may pass them, plan:330).
- **Rationale**: Scoring Matrix C-001 (90), X-001 (100), A-001 (90); Round 2 all advocates.
- **Risk**: Medium. The subset choice is an owner decision (see C14).

### C2. Gate phrases are labels, not resolutions (C-004)

- **Source**: V2 R2-F2; V1 R1-F10
- **Target**: append
- **Approach**: relationship-level negative tests (reversal negatives) plus V1's per-gate phrase inventory for Tasks 5, 13 and 16. Note V2's `_check_unattended_section` evidence: presence only (test:509-512).
- **Rationale**: C-004 (95); Round 2 advocate 2 new evidence.
- **Risk**: Low.

### C3. task-builder CLI-mode gate (U-004)

- **Source**: V1 R1-F3, corrected
- **Target**: append
- **Approach**: the `git add -A` half of task-builder:2237 is refused by spec:77 (WC-9). The `reflect run --fix --promote` half is a conditional integration question partly covered by the plan's `--no-promote` brief row (plan:276), not an outward action. Output location at task-builder:2239. Class: Drift.
- **Rationale**: Round 2 advocates 2 and 3 corrected V1's "outward" claim.
- **Risk**: Low. Whole-run vs staging-only scope is INV-018 (C16).

### C4. spec-panel socratic (U-005)

- **Source**: V1 R1-F4
- **Target**: append
- **Rationale**: kept by all advocates (Round 2 advocate 3 s5).
- **Risk**: Low.

### C5. "left out (WC-4)" across all 15 commands (C-003)

- **Source**: V2 R2-F3 merged into V3 R3-F11
- **Target**: replace R3-F11 body (keep its parametrized-test shape)
- **Approach**: only plan:97 and plan:110 pin the phrase; the matrix overstates the pinned count (real count 2). One parametrized test over all 15 commands.
- **Rationale**: C-003 (95).
- **Risk**: Low.

### C6. Task 21 path list (C-005)

- **Source**: V2 R2-F4
- **Target**: replace R3-F13 (after B2)
- **Approach**: P3. Compare the full commit manifest including the package; Task 21's list omits `.dev/tasks`.
- **Rationale**: C-005 (95).
- **Risk**: Low.

### C7. workflow.md:72 stale artifacts clause (C-002, X-002)

- **Source**: V3 R3-F3 spine; V1 R1-F1
- **Target**: replace R3-F3 remedy
- **Approach**: Drift (X-002). Add `refs/return-contract.md` to the coherence check. Remove the claim that the test pin at 837-844 must change (it pins tokens, not the path). The fix must reach the line `_artifacts_clause` reads (first matching line, test:770-775): Task 17 replaces only line 75 (plan:303) and ADDITIVE allows one deleted line (plan:41), so an added correcting line is invisible. Either widen the exemption to two lines or scope the clause check (INV-017).
- **Rationale**: C-002 (90), X-002 (95), A-002 (90); Round 2 advocate 3 s3 item 4.
- **Risk**: Medium. The fix form is an owner decision.

### C8. HALTs and depth-map.yaml (U-006)

- **Source**: V1 R1-F6, narrowed
- **Target**: append
- **Approach**: keep only the depth-map.yaml part; drop the D-P2-13 reading (see Changes NOT Made).
- **Risk**: Low.

### C9. reflect-pre readers grep AC (U-007)

- **Source**: V1 R1-F7
- **Target**: append, bounded to a grep acceptance criterion
- **Risk**: Low.

### C10. Matrix gap: two source.md:14 spans (U-009)

- **Source**: V2 R2-F5
- **Target**: append as a coverage-matrix note, not a Drift finding
- **Rationale**: V2 conceded in Round 1 that it is not drift.
- **Risk**: Low.

### C11. Instruction/check collisions (C-007)

- **Source**: V1 R1-F8 wording; V3 R3-F8
- **Target**: insert beside R3-F8
- **Approach**: Task 12 "add new lines" vs ADDITIVE and WRITE_VERB_CLASSIFICATION; Task 17 vs the one-line budget; task.md:44 flag-list line edit vs ADDITIVE.
- **Rationale**: C-007 (95).
- **Risk**: Low.

### C12. Per-finding reclassification (C-008)

- **Source**: all variants
- **Target**: restructure the class field on every merged finding
- **Approach**: replace V3's uniform "drift", V2's uniform "Drift" and V1's "none"/"authorized" with one of the four classes per finding, on the record (for example C-002 Drift, R2-F5 matrix note, R1-F5 Necessary deviation as an alternative, not a requirement).
- **Rationale**: C-008 (95).
- **Risk**: Medium. Every finding is touched.

### C13. NEW: troubleshoot `--diagnosability-handoff` nests `sc:workflow-protocol`

- **Source**: Round 2 advocate 3 s3 item 1; orchestrator evidence E-1
- **Target**: append, P1 Drift
- **Approach**: the flag (parsed at `troubleshoot.md:148`) calls `Skill sc:workflow-protocol` (`src/superclaude/skills/sc-troubleshoot-protocol/refs/diagnosability-audit.md:245,250`; `SKILL.md:645`). Task 11 nests only `adversarial` (plan:220); "diagnosability" appears 0 times in the plan. Unflagged, the nested workflow runs `git add .dev/tasks` (`sc-workflow-protocol/SKILL.md:28`), which WC-9 forbids (spec:77). Fix: Task 11 adds `workflow` to its nested list and to `EXPECTED_NESTING` and changes the return-contract read path (INV-003), or the section refuses `--diagnosability-handoff` under `--unattended`.
- **Risk**: Medium. Either fix also changes the Task 20 literal (INV-004).

### C14. INV-001 (HIGH, blocking)

- **Source**: `invariant-probe.md`
- **Target**: append as P1 blocking finding, linked to C1
- **Approach**: the cli-eval safety-flag subset is undefined, so the P1 block cannot be tested. Either the plan names the subset (from `sc-cli-eval-protocol/SKILL.md:128-153`) or the cli-eval section is carried as blocked-pending-decision.
- **Risk**: High until the owner decides.

### C15. INV-002 (HIGH, blocking)

- **Source**: `invariant-probe.md`
- **Target**: append as P1 blocking finding, linked to B1
- **Approach**: a nested blocked or failed status has no propagation path. sc-task Step 4 has no blocked branch; tasklist Stage 9 gates only on completion. The plan must define how a nested `blocked`/`failed` reaches the outer return contract.
- **Risk**: High until resolved.

### C16. MEDIUM invariants as findings

- **Source**: `invariant-probe.md`
- **Target**: append, one finding each, P2
- INV-003: diagnosability handoff step 3 reads `.dev/tasks/to-do/<id>/return-contract.yaml`; a nested workflow writes elsewhere (linked to C13).
- INV-004: `UNATTENDED_EXPECT` nested lists in Tasks 8, 11 and 16 must equal the Task 20 literal (linked to B1, C13).
- INV-009: nested task needs `--report-dir` plus retained `--compliance strict`; no AC pins it (linked to B1).
- INV-011: cli-eval spec-panel/document are command-only; the technical-writer agent route yields no nested dir.
- INV-016: Task 12 `report_path` undefined for a non-TFEP run.
- INV-017: the C-002 fix must widen the exemption or scope the clause check (linked to C7).
- INV-018: task-builder CLI gate whole-run vs staging-only undecided (linked to C3).
- LOW, as notes only: INV-005 (empty nested list forbids the `nested/` token in skip wording), INV-010 (`--unattended` placement inside a quoted string).
- **Risk**: Low.

## Changes NOT Being Made

| Diff Point | Non-Base Approach | Rationale |
|---|---|---|
| U-008 | V1 R1-F9 owner-approval table | Dropped by all advocates; plan:45 already covers it |
| U-006 | V1 R1-F6 D-P2-13 reading | Misread of plan:58, conceded by V1 in Round 1 |
| C-002 | V3 R3-F3 "update the test pin at 837-844" | The lines pin tokens, not the path (conceded) |
| C-005 | V3 R3-F13 `.dev/reflect` dirty-folder example | Cannot fail a check that queries only `src tests plugins` (plan:372) |
| U-004 | V1 "`--fix --promote` is an outward action" | Not on the spec's outward-action list (spec:77) |
| X-001 | V1 "run launches with no safety inputs" | The brief may pass them (plan:330); the gap is the missing block |
| U-003 | V1 R1-F5 deep-research reroute as a requirement | Kept only as an alternative (Necessary deviation) |
| C-001 | V2 R2-F1 digest-only identification without a policy | Insufficient alone; INV-001 needs a named subset or a blocked status |
| C-008 | V1 "none"/"authorized" labels | Outside the four-class taxonomy (conceded) |
| C-001 | R1-F2 / R3-F2 FR-G5 and `--no-pty` settlement | Already settled at plan:248 |

## Risk Summary

| Change | Risk | Impact if Failed | Rollback |
|---|---|---|---|
| B1-B7 | Low | Overstated or wrong claims stay in the merged findings | Revert to the V3 text |
| C1 | Medium | cli-eval P1 stays untestable | Keep as R3-F2 plus C14 |
| C2-C6, C8-C11 | Low | A unique finding is lost or misworded | Re-append from the source variant |
| C7 | Medium | Stale clause persists behind an invisible added line | Owner picks exemption or scoped check |
| C12 | Medium | Misclassification on individual findings | Per-finding revert to the debate record |
| C13 | Medium | Worker `git add` via nested workflow stays unaddressed | Refuse the flag under `--unattended` |
| C14, C15 | High | P2 ships with untestable P1 gate or silent nested failure | None: blocking until resolved |
| C16 | Low | MEDIUM gaps go untracked | Re-append from `invariant-probe.md` |

## Review Status

- [x] Base selection reviewed against the scoring record
- [x] Every change traced to a debate point or invariant
- [x] Changes NOT made documented
- [ ] Owner decisions pending: INV-001 subset; C-002 fix form (INV-017); C13 nest vs refuse

- **Approved by**: auto-approved (non-interactive run)
- **Approval timestamp**: 2026-11-07T02:10:41Z
