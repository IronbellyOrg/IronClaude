# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

Independent fault-finder agent (not an advocate), run 2026-11-08 after Round 2 against the Round 2 consensus. No `branch-trace.md` exists; sufficiency entries carry inline source enumerations. Orchestrator spot-checks: INV-005 confirmed (`cmp` of `src/superclaude/templates/documents/release-spec-template.md` vs `src/superclaude/examples/release-spec-template.md`: differ at byte 401, line 8); INV-007 confirmed (`spec-panel.md:259`, Review Loop bullet 2: "CRITICAL and FR-8/FR-9 findings are blocking").

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | state_variables | `verdict` can always find R2's blocking ids and labels in `D/state.json` | UNADDRESSED | HIGH | not-triggered writes only the audit state and "change[s] nothing else" (plan:50); skip guard "writes `audit: skipped(ids not citable)` ... and stops" (plan:57); `verdict` takes no R2 argument (plan:101; src.md:210 reads only `D/*` and R3) yet `prior_open` and the owner count need R2 grades and labels (plan:101, 104-106; src.md:131); an empty-diff or skipped audit still reaches review 3 and the verdict step (src.md:32, 200); the plan leaves verdict with no grades on those paths (crash, or a fail-closed FAIL on R2-minor rows T09 lists) |
| INV-002 | state_variables | every failed step records `audit: skipped(<reason>)` | UNADDRESSED | MEDIUM | APPLY_STOP prints and exits 1 but writes nothing to `state.json` (plan:87) while the shipped Fix Audit text says a failed step records `audit: skipped(<reason>)` (src.md:199, 45); `final-verdict.md` prints `audit: <state>` (plan:109) and T08a reports `state.json` (plan:205) |
| INV-003 | interaction_effects | "the script never turns a FAIL into a PASS" agrees with the any-severity rule | UNADDRESSED | HIGH | any-severity prints the report line only as `t09-verdict:`, not cross-checked (plan:101; src.md:129); final line is PASS when "open is empty and no DISAGREE" (plan:109); AC plan:114 "a report whose own line is FAIL never yields a final PASS" has no mode qualifier; in S1 (recorder template, plan:202) T09 fails on any finding, so the two rules give opposite final lines when only minor findings remain; spec carries the same conflict (src.md:129 vs 134; src.md:270 intends the computed 427 pass as the clean-pass readout) |
| INV-004 | guard_conditions | the verdict tests prove PASS is reachable | UNADDRESSED | MEDIUM | every case in AC plan:114-116 expects FAIL or a printed line; none expects `verdict: PASS`; "review 3 has no new findings" (empty or absent table) is undefined and, if treated as unparseable, exits 2 with FAIL (plan:101) |
| INV-005 | sufficiency_challenge | C-001's "owner picks" fix has a clean option | ADDRESSED | MEDIUM | option (b), enumerating line 220 as a difference, can only point at `~/.claude/templates/documents/release-spec-template.md`, whose source differs from `src/superclaude/examples/release-spec-template.md`, so the variant would behave differently on TDD input (against src.md:194 and plan:16 "full copy"); option (a), scoping the pin, ships a new primitive referencing `src/superclaude/examples`, against the project CLAUDE.md rule and plan:29; the merged finding must state both costs |
| INV-006 | interaction_effects | the literal `## Fix Audit` text stays true after the Unattended deviation and the C-002 fix | UNADDRESSED | LOW | plan:134 copies src.md:194 verbatim ("Without `--fix-audit` this command behaves exactly as `/sc:spec-panel`"); plan:26 removes `## Unattended mode` and C-002 drops two Usage tokens, so the sentence is false and Task 8 (plan:147) does not catch it |
| INV-007 | sufficiency_challenge | adding an FR-8/FR-9 tag alone fixes C-005 | UNADDRESSED | MEDIUM | K4 compares `claimed` with "the grade read from R" (plan:74; src.md:216); a new tag changes that string and, unless K4 is pinned to the `fix-list.md` grade cell verbatim, every row fails K4; cheaper fix: Review Loop bullet 2 (spec-panel.md:259) already makes FR-8/FR-9 blocking, so the parser can set the blocking flag (stricter than src.md:131 literal; say so); a parser reading `MAJOR (FR-8 GAP)` as unknown already protects it (plan:55), so blocking holds only for a prefix-matching parser |
| INV-008 | count_divergence | C-004 is minor because both ACs can pass | ADDRESSED | MEDIUM | both ACs pass with a `skipped(ids not citable)` fixture (no `check.log`), but with `skipped(check failed)` or APPLY_STOP the held set (plan:104) takes DOWNGRADE ids from a rejected audit and raises the registered owner count (plan:202) though the spec is byte-identical to the unaudited copy (src.md:267-272): wrong behaviour on a reachable path; fix: count DOWNGRADE ids only when state is `applied(...)`, which needs INV-002 first |
| INV-009 | count_divergence | the owner count fails closed like `new_blocking` | UNADDRESSED | LOW | `new_blocking` counts unknown grades as blocking (plan:101); "new critical+major" counts only labelled CRITICAL or MAJOR (plan:105), so an unknown-label finding is left out of the registered number, against plan:21 |
| INV-010 | collection_boundaries | "unattributed" means "added text that cites no id" | UNADDRESSED | LOW | a pure-deletion hunk has no current lines, cites no id, is unattributed (plan:54, 56; src.md:37, 39) and counts toward the skip guard (plan:57); safe (nothing edited) but untested |
| INV-011 | sufficiency_challenge | adding "recovery" resolves C-010 | ADDRESSED | LOW | the fix must either restore S from `current-before-audit.md` with `skipped(apply failed)` or write the logs before `os.replace` (plan:87; K1 at src.md:213); minor is right: I/O fault only |
| INV-012 | collection_boundaries | reverting a hunk restores the exact baseline bytes | UNADDRESSED | LOW | hunks ignore whitespace-only lines (plan:52), so reverting an insert hunk leaves the blank lines the fix added, which the AC "exact baseline bytes" (plan:92) and src.md:125 do not allow for |

## Summary

- **Total findings**: 12
- **ADDRESSED**: 3 (MEDIUM 2: INV-005, INV-008; LOW 1: INV-011)
- **UNADDRESSED**: 9
  - HIGH: 2 (INV-001, INV-003)
  - MEDIUM: 3 (INV-002, INV-004, INV-007)
  - LOW: 4 (INV-006, INV-009, INV-010, INV-012)

## Gate result

CONVERGENCE BLOCKED: 2 HIGH-severity UNADDRESSED invariant(s) detected
Blocking items: INV-001, INV-003
These invariant violations must be resolved before convergence can be declared.
Action: `--depth standard` allows no Round 3, so they are neither debated nor accepted as risk here; they are carried into the merged output as probe-raised blocking candidates (raised by no card) and into `unaddressed_invariants` of the return contract for the caller to resolve.

WARNING: 3 MEDIUM-severity UNADDRESSED invariant(s) detected
Items: INV-002, INV-004, INV-007
These items do not block convergence but should be reviewed (INV-007 is attached to the C-005 fix; INV-002 and INV-004 are carried as probe-raised minors).
