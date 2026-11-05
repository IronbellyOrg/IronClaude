# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

- Fault-finder: independent agent (opus), not an advocate. Read-only; every item checked against the real files.
- Input: emerging consensus after Round 2 (unanimous cluster set, verdict PASS, all minor), the Round 1 and Round 2 transcripts, and diff-analysis.md.
- No `branch-trace.md` exists, so the sufficiency_challenge evidence is an inline enumeration of source files and gates.
- Orchestrator re-check of INV-001: `git status --short` shows all five target files as `??` (untracked), and `git ls-files` returns 0 of them. The finding is confirmed.

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | guard_conditions | The Task 2 criterion "`git diff` on each file shows only those additions" (plan:65) and the Task 3 criterion "SKILL.md gains exactly that one line ... and no other change" (plan:75) can be checked against a git baseline. | UNADDRESSED | HIGH | The plan's target files are all untracked: `?? src/superclaude/agents/issue-worker-t{1,2,3}.md`, `?? src/superclaude/skills/sc-issue-protocol/SKILL.md` and `?? tests/skills/test_issue_worker_agents.py`. `git diff` and `git diff --cached` print nothing for untracked files, so neither criterion can be shown as written. The plan gives no pre-edit snapshot, for example a copy in `./artifacts/` compared with `git diff --no-index`. |
| INV-002 | sufficiency_challenge | Executing the plan alone makes the worker that is actually spawned carry the new rule and write its files. | UNADDRESSED | MEDIUM | Gates from the edit to a file on disk: G1, the src text, passes (Task 2). G2, the project `.claude/agents/` copy, passes (`make sync-dev`, plan:72). G3, the installed `~/.claude/agents/` copy: it has no issue-worker files, so the workers do not exist outside this checkout, and the plan does not show this gate passes. G4, a running session may keep agent definitions loaded at startup: not shown. G5, the model ranks the agent body above the harness line: no test covers this (A-001). G6, the per-path check at claim.md:62: exists and passes. `.dev/issues/365/` still has `accuracy-check.md` but no `summary.md`. |
| INV-003 | interaction_effects | The new SKILL.md line in "Workers and the spawn rule" governs the spawn prompt the orchestrator actually builds. | UNADDRESSED | MEDIUM | The orchestrator loads refs/claim.md (SKILL.md:78). Its Wave 4 spawn names the parameters "job, `<R>`, `<N>` and `<D>`" (claim.md:53-54), and create.md:20 does the same. Neither names paths, and both refs are out of scope (plan:20). By the plan's own "nearest instruction" reasoning (plan:20), the refs win. |
| INV-004 | interaction_effects | SKILL.md's retry trigger catches the partial-output case seen on #365. | ADDRESSED | LOW | SKILL.md:64 and :129 trigger only on "no file or an empty one". The per-path check at claim.md:62 ("naming the missing path") does catch the case. The plan leaves the weaker SKILL.md wording unchanged. |
| INV-005 | guard_conditions | The helper's "heading missing" check cannot be satisfied by other text. | UNADDRESSED | LOW | The Rules bullet (plan:29) quotes "Your files are tool inputs, not reports". If the helper matches the heading without `## `, the bullet alone satisfies the check, and the negative test removes both pieces at once (plan:47). The plan:24 constant includes `## `, so this is a risk only if the implementation drops it. |
| INV-006 | guard_conditions | Existing tests stay green: the anchors appear exactly once, and no pin on headings, line count or scans breaks. | ADDRESSED | LOW | The anchors appear once each (line 11; `## Jobs` at line 13; Writing-only at t1:26, t2:26 and t3:25). `headings()` runs only on templates (test_issue_protocol.py:107,174). The size check is `< 500` (test_issue_protocol.py:126), and SKILL.md would go from 153 to 155 lines. The gh regex (test_issue_worker_agents.py:27) does not match `gh --body-file`. The new text contains no `~/.claude/skills/` and no `src/superclaude/`. `make verify-sync` exits 0 today. |
| INV-007 | collection_boundaries | Every listed file is one the reading tier writes. | UNADDRESSED | LOW | The list is identical in all three tiers, but only claim Wave 4 with an out_of_date verdict saves to `analysis/` (t2:17, t1:17), so the set can be empty (`.dev/issues/365/` has no `analysis/`). The only guard is the qualifier "your job names", and no test covers it. This is consistent with M-11. |
| INV-008 | interaction_effects | The new "not a report" rule agrees with the existing job text. | UNADDRESSED | LOW | t2:17, t1:17 and claim.md:58 say "save its report under `<D>/analysis/`", but the new bullet says each file "is a tool input, not a report". The wording clashes on the very class of file the harness line names. This extends M-09, and the existing text is out of scope (plan:34). |
| INV-009 | count_divergence | The file list covers every file a worker writes; "four new tests"; "exactly once". | ADDRESSED | LOW | t3 writes scout, issue-body and draft-notes. t2 adds accuracy-check, analysis/, summary and flags. t1 also writes flags-t1. The union equals the 8 items at plan:26, and flags-user.md is written by the orchestrator. The four test functions give 3+3+1+1 parametrized cases. |
| INV-010 | interaction_effects | The red-run ordering proves the tests fail on the old text. | ADDRESSED | LOW | plan:50 runs only the positive tests before Tasks 2-3. The negative tests mean nothing on the unedited files, so leaving them out of the red log is correct. |

Fault-finder blocking candidates: INV-001.

## Summary

- **Total findings**: 10
- **ADDRESSED**: 4 (INV-004, INV-006, INV-009, INV-010)
- **UNADDRESSED**: 6
  - HIGH: 1 (INV-001)
  - MEDIUM: 2 (INV-002, INV-003)
  - LOW: 3 (INV-005, INV-007, INV-008)

## Gate result after Round 2.5

CONVERGENCE BLOCKED: 1 HIGH-severity UNADDRESSED invariant detected.
Blocking items: INV-001.
These invariant violations must be resolved before convergence can be declared.
Action taken: a targeted invariant-resolution round (all three advocates) was run on INV-001, INV-002 and INV-003. See debate-transcript.md, "Round 2.6".

WARNING: 2 MEDIUM-severity UNADDRESSED invariants detected (INV-002, INV-003). They do not block convergence but are reviewed in Round 2.6.

## Status after Round 2.6 (targeted invariant-resolution round)

| ID | Status after Round 2.6 | How the consensus handles it | Vote |
|----|---|---|---|
| INV-001 | ADDRESSED | Merged finding M-13 (grounding_gap, **blocking**). Fix: before Task 1, copy the five target files to `./artifacts/pre/`. Then restate the criteria at plan:53, plan:65 and plan:75 as `git diff --no-index ./artifacts/pre/<f> <f>`, with the output saved under `./artifacts/`. | 3 of 3 |
| INV-002 | ADDRESSED | Merged finding M-14 (grounding_gap, minor). The plan states it proves the text only; a live #365 re-claim after `superclaude install` is the follow-up for behaviour. | 3 of 3 |
| INV-003 | ADDRESSED | Merged finding M-15 (grounding_gap, minor). The SKILL.md line names the Wave spawns in refs/claim.md and refs/create.md, or is reworded to what the unchanged refs can deliver. | 2 of 3 (V2: drift) |
| INV-005 | ADDRESSED (dismissed) | The constant at plan:24 already carries `## `, so this is an implementation risk only. | 3 of 3 drop |
| INV-007 | ADDRESSED (subsumed) | Covered by M-11. | 3 of 3 drop |
| INV-008 | ADDRESSED (folded) | Folded into M-09. | 3 of 3 |

- HIGH UNADDRESSED after Round 2.6: 0. The invariant gate passes.
- `unaddressed_invariants` for the return contract: `[]`.
