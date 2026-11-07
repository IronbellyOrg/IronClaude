# Refactoring Plan

## Overview

- Base variant: Variant 3 (`variant-3-original.md`, reviewer-3-card, opus/refactorer). Combined score 0.8113 (`base-selection.md`).
- Incorporated from: Variant 1 (`variant-1-original.md`), Variant 2 (`variant-2-original.md`) and the Round 2.5 invariant probe (`invariant-probe.md`).
- Planned changes: 8. Changes not being made: 6.
- Overall risk: Low. Every change either refines a verifier or corrects an anchor. None changes the verdict.
- Output: `merged-review.md`, a merged reviewer card in markdown. It has the verdict PASS, zero blocking findings and minor notes only.

Ground truth for anchors: the plan (`TASK-WF-fixIssue412SVeri-20261106-215543.md`, 53 lines), `source.md:1` and `src/superclaude/cli/install_user_setup.py` (ius). The orchestrator re-read all three.

## Planned Changes

### Change #1: Merge V1's empty-output case and INV-005/INV-006 into the R3-2 verifier

- **Source**:
  - V1, `variant-1-original.md:16`: "test empty-output success separately".
  - `invariant-probe.md`: INV-005 and INV-006.
- **Target**: base R3-2 verifier (`variant-3-original.md:18-21`).
- **Rationale**:
  - C-001 was agreed 3/3: Variant 3 wins, with V1's empty-output case merged in (debate-transcript.md, Scoring Matrix).
  - The Round 2.5 probe found two MEDIUM verifier gaps: a skip reported only on stderr, and an empty-output case with no stated expectation.
- **Integration**: the merged verifier has three fixtures, each with exit 0 and all three SKILL.md files present.
  - (a) Skip named on stdout. Assert the skip text is visible and no refresh-success claim is made.
  - (b) Skip named only on stderr. Same assertions.
  - (c) Empty stdout and stderr. A presence-only success line is acceptable; "refreshed" or "updated" wording is not.
  - Anchors stay ius:230-263 and plan:45-51, with plan:24 added.
- **Risk**: Low (additive).

### Change #2: Add R1-3 + X-001 as a minor note on Task 1's terminal-surface wording

- **Source**: V1 R1-3 (`variant-1-original.md:20-22`); X-001 and C-003, both won by V1 at 3/3.
- **Target**: new minor note in the merged findings, placed after R3-2.
- **Rationale**:
  - Plan:35 says "explicitly distinguish".
  - `source.md:1` says "use Claude (CLI), never New Terminal".
  - The prohibition reaches Task 1 only through its Inputs at plan:30.
  - Variant 3 is silent here and has conceded the point.
- **Integration**:
  - plan_ref plan:30, plan:35.
  - Evidence `source.md:1` and `orca-discovery.md:12-16`.
  - Verifier: "shell routes are prohibited for ccsession sessions". INV-018 refinement: align the AC wording with the source.
- **Risk**: Low.

### Change #3: Trim R3-1 to its verified reader and attach plan:52

- **Source**: V3's Round 2 partial defense (`rounds/round-2-variant-3.md`, (b) and (c)); INV-016, INV-017 and INV-019.
- **Target**: base R3-1 (`variant-3-original.md:8-16`).
- **Rationale**: C-004 was agreed 3/3 with its scope narrowed. Only `tests/core/test_codegraph_guide.py:137-174` is a verified reader of core CLAUDE.md, and plan:52 does not list it.
- **Integration**:
  - Evidence: `tests/core/test_codegraph_guide.py:137-174`, citing the placement-sensitive assertions at lines 149, 155, 162-166 and 173. plan_ref: plan:52.
  - Per INV-019, also recommend adding `tests/cli/test_update_command.py` and `tests/core/test_how_we_work_routing_table.py` to the wider regression run.
  - The routing-table file is a run-it recommendation (INV-017). It is not a verified defect.
- **Risk**: Low.

### Change #4: Add INV-009 (forced-path deadline spend) as a minor note

- **Source**: `invariant-probe.md`, INV-009 (MEDIUM).
- **Target**: new minor note.
- **Rationale**:
  - After the fix, every forced run probes and installs Orca, using up to `_ORCA_TIMEOUT = 25` (ius:39) of `_NETWORK_BUDGET = 30` (ius:40, ius:436).
  - `install_plugins` reports "(time limit)" when less than 2 s remains (ius:397-399).
  - `update` always forces (`main.py:404`).
  - No card weighed this cost.
- **Integration**: note it as nonfatal and honestly reported. Recommend the Task 2 evidence record the plugin outcome on a forced run, and name the update path (INV-010).
- **Risk**: Low. This is a verification note, not a plan defect.

### Change #5: Add LOW notes on force passed by keyword and on message accuracy

- **Source**:
  - INV-011 (A-004, QUALIFY 3/3).
  - INV-014 and INV-015.
  - INV-007 refinement.
- **Target**: one combined minor note, LOW.
- **Rationale**:
  - The stub in `tests/cli/test_update_command.py:47-51` is `lambda **kwargs`.
  - The messages at ius:252-256 and 258-262 can mislead when the guides already exist.
- **Integration**:
  - `force` follows `deadline`, defaults to False, and is passed by keyword at ius:441.
  - Assert `"--force" not in command` on the forced path.
  - Pin the wording of the failure messages when the guides exist.
- **Risk**: Low.

### Change #6: Carry V2's preservation checklist and the mocked/live separation as self-audit context

- **Source**: V2 U-003 (`variant-2-original.md:12-14`).
- **Target**: base self-audit (`variant-3-original.md:23-27`).
- **Rationale**: all three advocates rated it unique and of medium value. Anchored to plan:45 and plan:52.
- **Integration**: append to the self-audit as context. It is not a finding.
- **Risk**: Low.

### Change #7: Keep R1-1 as an optional ordering note

- **Source**: V1 R1-1 (`variant-1-original.md:9-12`).
- **Target**: an optional note at the end of the minors.
- **Rationale**: C-002 went to V3 at 3/3. Sync is part of Task 2 (plan:47), so running the routing checks earlier is optional.
- **Integration**: one line, labelled optional.
- **Risk**: Low.

### Change #8: Report coverage both ways, kept separate

- **Source**:
  - V2's 21/21 (`variant-2-original.md:9`).
  - `diff-analysis.md`: lexical 13/21 = 0.6190.
- **Target**: the merged coverage and limitations section.
- **Rationale**: C-005 is a tie between V1 and V3. The 21/21 figure is reviewer judgment; only the lexical figure is measured.
- **Integration**:
  - "Lexical coverage 13/21 = 0.6190 (shared Constraints outside the matcher)."
  - "Reviewer-judgment semantic coverage 21/21 (V2, not independently checked)."
- **Risk**: Low.

## Changes NOT Being Made

| Diff Point | Non-base Approach | Rationale |
|---|---|---|
| S-002 | V1's `original_source_ref` `install_user_setup.py:113-119` | Pathology. It lies inside `install_rules`, not the helper at ius:230-263. V1 conceded. It is excluded from the merged output. |
| S-002 | V3's brief-local "plan lines 81-82" | Pathology. The plan has 53 lines. V3 conceded. It is excluded from the merged output, including the limitations. |
| C-004 | R3-1 leads `tests/cli/test_bash_inspection_policy.py:32` and `tests/cli/test_issue_body_templates.py:18` | Unverified leads. V3 dropped them in Round 2. |
| C-005 | V2's 21/21 as a coverage figure | Not measured. Carried only as labelled reviewer judgment (Change #8). |
| X-002 | V1's "not precisely defined" | Overstated: plan:24, plan:45 and plan:51 define the requirement. V1 conceded. |
| Verdict | Any blocking finding | All three cards and all three advocates agree on PASS. No invariant is HIGH UNADDRESSED. |

## Risk Summary

| Change | Risk | Impact | Rollback |
|---|---|---|---|
| #1 | Low | Verifier gains two fixtures | Drop fixtures (b) and (c) |
| #2 | Low | New minor note on Task 1 | Remove the note |
| #3 | Low | Narrows R3-1 and adds a plan anchor | Restore the base text |
| #4 | Low | New minor note | Remove the note |
| #5 | Low | New LOW note | Remove the note |
| #6 | Low | Self-audit context only | Remove the lines |
| #7 | Low | Optional line | Remove the line |
| #8 | Low | Labelling only | Restore the base limitations |

## Review Status

- Approval: auto-approved (non-interactive)
- Timestamp: 2026-11-06T22:30:00Z
