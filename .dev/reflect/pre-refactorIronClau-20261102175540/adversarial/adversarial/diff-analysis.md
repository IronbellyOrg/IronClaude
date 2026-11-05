# Diff Analysis: reflect reviewer-card comparison

## Metadata
- Generated: 2026-11-02T18:30:00Z
- Variants compared: 3
  - Variant 1: reviewer-1 card (sonnet, analyzer lens), 6 findings, blind-calibrated C 0.80
  - Variant 2: reviewer-2 card (haiku slot = glm-5.3, qa lens), 4 findings, blind-calibrated C 0.76
  - Variant 3: reviewer-3 card (opus, refactorer lens), 6 findings, blind-calibrated C 0.83
- Subject under review by all three: the plan `.dev/tasks/to-do/TASK-WF-refactorIronClau-20261102-162730/TASK-WF-refactorIronClau-20261102-162730.md` against its spec `source.md`
- Focus areas: correctness, coverage, deviation-classification
- Total differences found: 20
- Categories: structural (3), content (5), contradictions (2), unique (7), shared assumptions (3)

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Variant 3 | Severity | Level |
|---|------|-----------|-----------|-----------|----------|-------|
| S-001 | Top-level sections | findings, t1_findings_disputed, inferred_claims | adds `missing_requirements` with a one-line justification | findings, t1_findings_disputed, inferred_claims | Low | L1 |
| S-002 | Classification spread | drift x2, necessary x2, authorized x1, drift x1 (mixed) | drift x3, necessary x1 | drift x6 (single label for all findings) | Low | L1 |
| S-003 | T1-card dispute coverage | disputes F1, F2, F3, F4 | disputes F1, F2, F3, S2 | disputes S1, S4 only | Medium | L2 |

## Content Differences

| # | Topic | Variant 1 Approach | Variant 2 Approach | Variant 3 Approach | Severity | Level |
|---|-------|--------------------|--------------------|--------------------|----------|-------|
| C-001 | Pre-PR checks vs the new no-interaction rule (CLAUDE.md:64, :66) | R1-1 (medium): checks 1 AND 3 contradict; fix check 1 with `git remote get-url origin` + `gh repo view IronbellyOrg/IronClaude`; fix check 3 to stop and report instead of closing an upstream PR; AC: `grep -n 'close it immediately'` empty | not raised | R3-F2 (medium): check 1 only; fix with `gh repo set-default IronbellyOrg/IronClaude` then `gh repo set-default --view`; AC: no bare `gh repo view` | Medium | L2 |
| C-002 | Upstream #419 doc link at CLAUDE.md:251 | R1-5 (low): narrow wording to tool calls and link flags; plan must decide keep or de-link | R2-F1 (low): strip URL to plain text or keep with an "inert historical reference" note | R3-F6 (low): unlink/remove, or narrow plan line 73 to "link flags" | Low | L1 |
| C-003 | Third class "Historical record" for POST-REFLECT-TASK.md | R1-2 (necessary, low): keep; add that the file is Blocked and stale paths are intentional; report the class first in the summary | R2-F2 (necessary, low): keep as-is; record as a deviation; surface at completion; do not gate | not raised | Low | L2 |
| C-004 | Proof that internal checkouts "keep working without Orca" | R1-4 (drift, low): add pytest run of 3 internal-checkout test files to Task 7 | R2-F3 (drift, low): same 3 files in Task 6 or 7 | not raised as a finding | Low | L3 |
| C-005 | Reading "interacted with" as also banning fetch/pull and Orca link flags | R1-6: authorized addition (memory entry + literal source) | dispute of T1 F3: not a deviation at all | silent | Low | L1 |

## Contradictions

| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Variant 3 Position | Impact | Level |
|---|-------------------|--------------------|--------------------|--------------------|--------|-------|
| X-001 | Does plan line 73 ("no tool call or link (gh, git or Orca) that resolves to it") already forbid the static #419 doc link? | Ambiguous: "A static markdown link is not a tool call, but the plan neither removes it nor says it is allowed" | Yes: "Task 3's new 'no link that resolves to upstream' rule is contradicted by the untouched #419 upstream issue link" | Yes: "The tightened rule bans links that resolve to upstream" | Medium | L2 |
| X-002 | Is the plan's hit set complete for the spec's "every tracked file that encodes ... git worktree add"? | Complete: "matched 108 hits in 17 files with the same per-file counts as the plan" | Complete: `missing_requirements: []`; "Hit set independently reproduced" | Incomplete: scripts/eval_runner.py:143 runs `["git", "worktree", "add", ...]` (list arguments) that the grep cannot match; persistent sibling worktree, never removed | Medium | L3 |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | 3 | R3-F1: scripts/eval_runner.py creates a never-removed sibling worktree via list-argument `git worktree add`; invisible to the spec's grep; fits none of the four internal-checkout exceptions | High |
| U-002 | 3 | R3-F3: Orca flags `--json`, `--issue`, `--pr` written into CLAUDE.md are absent from the plan's confirmed-command list | Low |
| U-003 | 3 | R3-F4: tests/skills/test_sc_recommend_routing_contract.py reads all three Task 5 files but Task 6 does not run it | Medium |
| U-004 | 3 | R3-F5: the /sc:post-release tag checkout (SKILL.md:91) names no location and no removal, so it does not meet the plan's "creates and removes itself" exception | Medium |
| U-005 | 1 | R1-3: Task 1 labels the .gitignore row "rewrite to Orca's default location" while Task 4 keeps the `.dev/worktrees/` entry | Low |
| U-006 | 2 | R2-F4: the "only .claude/settings.json" staging constraint conflicts with tracked .claude/cache files (blind calibration: weak; misquotes .gitignore:129) | Low |
| U-007 | 1 | Inferred claim: src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:267 uses a bare `gh repo view --json nameWithOwner` fallback, in tension with the tightened rule but outside the hit set | Medium |

## Shared Assumptions

| # | Agreement Source | Assumption | Classification | Promoted |
|---|------------------|------------|----------------|----------|
| A-001 | No variant raises any finding against Task 2's or Task 3's rewrite of CLAUDE.md text | No test, hook, or installed primitive reads the root CLAUDE.md worktree subsection or the fork-rule wording, so rewriting them breaks nothing | UNSTATED | Yes |
| A-002 | All three accept Task 2/Task 4's "Orca creates project worktrees outside the repository" | Orca's default worktree location lies outside the main checkout on every host this repo is used on, so `.gitignore` needs no new entry | UNSTATED | Yes |
| A-003 | Variants 1 and 2 recommend the same three test files as proof of "keeps working" | Those three test files actually execute (are not skipped) in a normal checkout, so a pass is evidence | UNSTATED | Yes |
| (A-x) | Variants 1 and 2 treat the spec's git grep output as the full scope | The grep pattern defines the full scope of "every tracked file" | CONTRADICTED by Variant 3 (see X-002) | No (flagged for debate) |

### Promoted [SHARED-ASSUMPTION] diff points

| # | Assumption | Impact | Status |
|---|------------|--------|--------|
| A-001 | Root CLAUDE.md worktree and fork-rule text is not pinned by any test, hook or primitive | If false, Tasks 2-3 break a test the plan never runs | Open |
| A-002 | Orca's default location is outside the main checkout | If false, Task 4's "retired, outside the repository" comment is wrong and nested checkouts could be staged | Open |
| A-003 | The three internal-checkout test files run (not skip) in a normal checkout | If false, the added acceptance line passes vacuously | Open |

## Summary
- Total structural differences: 3
- Total content differences: 5
- Total contradictions: 2
- Total unique contributions: 7
- Total shared assumptions surfaced: 4 (UNSTATED: 3, STATED: 0, CONTRADICTED: 1)
- Highest-severity items: U-001 (High value); C-001, X-001, X-002, S-003 (Medium)
- Convergence denominator (S + C + X + A): 3 + 5 + 2 + 3 = 13
- Taxonomy coverage: L1 = S-001, S-002, C-002, C-005; L2 = S-003, C-001, C-003, X-001, A-001; L3 = C-004, X-002, A-002, A-003
- Similarity check: 20 differences across 16 findings; variants are not substantially identical; debate proceeds
