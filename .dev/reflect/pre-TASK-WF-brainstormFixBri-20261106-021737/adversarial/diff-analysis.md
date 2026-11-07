# Diff Analysis: reviewer-card comparison (plan audit of TASK-WF-brainstormFixBri-20261106-021737)

## Metadata

- Generated: 2026-11-06T03:41Z
- Variants compared: 3 (V1 = reviewer-1 analyzer/sonnet, V2 = reviewer-2 qa/haiku slot, V3 = reviewer-3 refactorer/opus)
- Variant files: `variant-1-original.md`, `variant-2-original.md`, `variant-3-original.md` (this folder)
- Subject of all three cards: the 7-task plan `.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-021737/TASK-WF-brainstormFixBri-20261106-021737.md` against its brief `source.md` (same folder). The plan regenerates an earlier, reviewed plan and applies 17 corrections (brief Part 3) with replacement wording (Part 4).
- Blind calibrated confidence per card: V1 0.73; V2 and V3 pending when this file was written.
- Total differences found: 26 scored points (structural 2, content 14, contradictions 5, shared assumptions 5) plus 6 unique items
- Categories: structural (2), content (14), contradictions (5), unique (6), shared assumptions (5)
- Taxonomy levels: L1 surface wording, L2 structural, L3 state and guard mechanics (Level column)

Facts checked on disk by the orchestrator while writing this file (use them as ground truth in the debate):
- `src/superclaude/commands/analyze.md:97-98`: the `/sc:analyze` worker contract `<report-dir>/return-contract.yaml` "is written on every outcome" once it has a usable report directory; an unusable one is refused before any work and "printed in chat only" (no contract).
- Plan line 25 is the Constraints line "The edits reach the next live plan only after they are committed to a branch the live-check worktree is built from; this plan does not commit." (brief correction F-16 asks for "...the owner commits and merges them...").
- Plan line 38 is Task 1's replacement text ending "The nested contract is listed in `artifacts`, also when the call failed."; plan line 128 is Task 6's live-check sentence with "every `nested/analyze-` path listed in `artifacts` exists and holds its own `return-contract.yaml`" and, later, "the `codebase` entry is not `skipped` ... and `/sc:analyze` did not refuse that directory"; plan line 133 says the sentence "has no known false FAIL on a correct run".
- Plan line 125 says the 7.2 step 4 line "begins "Check the contract (PyYAML ..."" but the spec line 286 begins "4. Check the contract".
- Git index today: the earlier package `...001016` is staged (`A`); this package `...021737` is untracked (`??`) until the final workflow step stages it.
- Task 1 is the only task whose body says "before any edit"; Tasks 2, 3 and 6 carry no Depends-on line; Tasks 4, 5, 7 carry correct ones (plan lines 83, 99, 150).

## Structural Differences

| # | Area | V1 | V2 | V3 | Severity |
|---|------|----|----|----|----------|
| S-001 | Findings count and P1 count | 7 findings, 0 P1 | 5 findings, 1 P1 | 8 findings, 2 P1 | Low |
| S-002 | Use of INFERRED tag | 3 findings (A-2, A-3, A-5) | none | 2 findings (R3-2, R3-7) | Low |

## Content Differences

| # | Topic | V1 | V2 | V3 | Severity | Level |
|---|-------|----|----|----|----------|-------|
| C-001 | Task 1's "listed in artifacts, also when the call failed" vs Task 6's "every listed nested/analyze- path exists" | A-2 P2 INFERRED: contradiction; false FAIL possible; not in the residual-risk list | silent | R3-1 P1 Grounded: contradiction; the plan's "no known false FAIL" is false; reword the skill sentence to "listed when it was written" | High | L3 |
| C-002 | F-16 Constraints line: plan substitutes "committed to a branch the live-check worktree is built from" for "owner commits and merges them" | disputes the card: the plan's wording is the correct one (spec line 282); documentation nit | R2-1 P1: verifier literally unsatisfied, departure unrecorded, motivating scenario dropped | silent | Medium | L1 |
| C-003 | Task 7 sentence "it writes only the logs and the status snapshot under ./artifacts/" (F-13) | A-4 P2: false because make sync-dev rewrites `.claude/`; F-13 verifier wants the literal sentence | R2-2 P2: widening forced by F-2, departure unrecorded; also not strictly true because of sync-dev | silent | Low | L1 |
| C-004 | Task 7 bullet 3 (git-status delta check) may fail on a correct run | A-5 P2: not vacuous; earlier package already staged; only other untracked paths under .dev/tasks/ are a risk | R2-3 P2: residual exposure from anything the executor writes under .dev/ outside the package | R3-2 P1 INFERRED: if the earlier package were untracked, git add would break the bullet | Medium | L3 |
| C-005 | `git show HEAD:` checks in Tasks 4 and 5 can pass without testing (short path, no pipefail, grep -c exit 1) | A-1 P2 | silent | silent | Medium | L3 |
| C-006 | Task 7 logs record no exit code; no format check on the edited test files | A-3 P2 INFERRED | silent | silent | Low | L2 |
| C-007 | Live-check sentence reads `domain` and `enrichment_used` from "the contract"; with `--report-dir` they live in brainstorm's own contract, not the worker contract | silent | silent | R3-3 P2 Grounded | Medium | L2 |
| C-008 | Companion sentence in 2.1 is a rule for every command and the installed WORKER-CONTRACT.md twin gets no matching edit | silent | silent | R3-4 P2 | Low | L2 |
| C-009 | New routing bullet says the scan "is recorded in enrichment_used with this tier's quality_tier"; a timed-out source is recorded `skipped` | silent | silent | R3-5 P2 | Low | L1 |
| C-010 | Residual risk 2 calls Skill, Agent and Task all inferred; the spec already names Skill and Agent | silent | silent | R3-6 P2 | Low | L1 |
| C-011 | Task order: Tasks 2, 3, 6 lack "Depends on: Task 1" although Task 1 snapshots "before any edit" | silent | silent | R3-7 P2 INFERRED | Low | L2 |
| C-012 | Coverage matrix never sampled Part 2, the Part 3 preamble and Part 4 of the brief | silent | R2-5 P2 (plan does satisfy them; matrix completeness only) | silent | Low | L2 |
| C-013 | Task 6 anchor says step 4 "begins Check the contract"; the line begins "4. Check the contract" | A-6 P2 | R2-4 P2 | silent | Low | L1 |
| C-014 | Confirmations: pins, slicing, anchors and Part 4 byte-for-byte copy hold | A-7 | anchors confirmed | R3-8 | Low | L2 |

## Contradictions

| # | Point of Conflict | V1 Position | V2 Position | V3 Position | Impact |
|---|-------------------|-------------|-------------|-------------|--------|
| X-001 | Is the listed-contract vs "listed paths exist" conflict a P1 defect with a real false FAIL? | P2, INFERRED | silent | P1, Grounded | High: it decides whether the plan can be called ready; `analyze.md:97-98` supports the edge case (refused directory writes no contract) |
| X-002 | Does Task 7 bullet 3 fail because of the earlier sibling package? | No: already in the index | not specific | Yes if it were untracked (P1 INFERRED) | Medium: index shows the earlier package staged today, so the premise is false today; it would matter only if someone unstages it |
| X-003 | Severity of the F-16 wording departure | P2 or nit; the plan's wording is the correct one | P1 | silent | Medium |
| X-004 | Is the Task 7 "writes only ..." sentence an acceptable necessary deviation or a false statement? | false (sync-dev writes `.claude/`) | necessary deviation but unrecorded and also not strictly true | silent | Low |
| X-005 | Size of the false-FAIL exposure of Task 7 bullet 3 from executor writes elsewhere under .dev/ | small: executor artifacts stay in the package | real but unquantified | via the sibling package only | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | V3 | R3-1: the listed-contract conflict, with the reword | High |
| U-002 | V1 | A-1: git show HEAD check can pass vacuously | Medium |
| U-003 | V3 | R3-3: domain/enrichment_used live in brainstorm's own contract, not the worker contract | Medium |
| U-004 | V1 | A-3: no exit codes recorded, no ruff format check | Low |
| U-005 | V2 | R2-5: matrix completeness gap | Low |
| U-006 | V3 | R3-7: missing Depends-on for the snapshot step | Low |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Classification | Impact | Status |
|-------|------------|------------------|----------------|--------|--------|
| A-001 | `/sc:analyze` (and any nested command) writes its worker contract on every outcome once it has a usable report directory, and writes none when the directory is refused. All three cards lean on this when judging the "listed in artifacts" sentences | C-001, X-001 | UNSTATED | Decides whether the conflict is a real false FAIL; a state/guard (boundary) question | Promoted |
| A-002 | `/sc:implement` judges each acceptance bullet literally, so an unpassable or unrecorded-deviation bullet blocks completion | C-002, C-003, C-004 | UNSTATED | Decides whether C-002 and C-003 are blockers or notes (validation rule) | Promoted |
| A-003 | The tree at execution time equals today's (staged earlier package, uncommitted install_core.py edits, this package staged by then). A state change alters every baseline-dependent check | C-004, X-002, X-005 | UNSTATED | Baseline-dependent checks hold only if this state persists | Promoted |
| A-004 | Exact-substring pins are the right way to pin the wording | C-014 | STATED | All three cards accept it | Not promoted |
| A-005 | When the plan departs from a sentence the brief demands verbatim, the plan itself must record the departure (a reviewer convention, not stated in the brief) | C-002, C-003 | UNSTATED | V2 treats it as an obligation, V1 and V3 do not; decides the priority of C-002 and C-003 | Promoted |

## Summary

- Total structural differences: 2
- Total content differences: 14
- Total contradictions: 5
- Total unique contributions: 6
- Total shared assumptions surfaced: 5 (UNSTATED: 4, STATED: 1, CONTRADICTED: 0)
- Highest-severity items: C-001, X-001
- Scored diff points (denominator for convergence): S 2 + C 14 + X 5 + A 5 = 26
