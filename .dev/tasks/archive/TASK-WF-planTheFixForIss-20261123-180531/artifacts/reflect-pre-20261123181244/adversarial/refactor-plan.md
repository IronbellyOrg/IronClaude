# Refactoring Plan: Merge into Base (Variant 3)

## Overview
- Base: Variant 3 (reviewer-3 card, persona refactorer, requested model opus; actual identity unverified)
- Incorporating strengths from: Variant 1 (reviewer-1 card), Variant 2 (reviewer-2 card), debate-transcript.md Round 2 consensus, invariant-probe.md
- Planned changes: 9
- Risk level: Medium (overall): the merge rewrites the base's blocking-finding fix, which is the decision-bearing part
- Output: `<OUTPUT>/merged-review.md`, where OUTPUT = this run's reflect-pre directory. The merged artifact is a review of the plan only; it carries no repair acceptance and authorizes no plan or product edit.

### Stable finding IDs for the merged review

| ID | Grade | Finding | Sources |
|---|---|---|---|
| MR-B1 | Blocking (Decision + Missing) | Task 4 omits active matching documentation; plan:81 "No changes to installed skill or command definitions are required" and plan:84 "all four known stale occurrences" are false | V3 row 1; X-001; C-001; C-006; Round 2 all advocates |
| MR-M1 | Medium | plan:60 gives no rule separating the bundled default from a caller template | V1 row 1; V3 row 3; X-003; A-008; INV-001; INV-003 |
| MR-M2 | Medium | plan:62 names no quoting form for the comma list | V3 row 4; X-004; INV-004; INV-005 |
| MR-M3 | Medium | docs/swarm/wizard-guide.md:216 lists refactor-find's stale hand-off as `/code-review` | V1 row 2; V3 row 2; C-002 |
| MR-M4 | Medium | The MR-B1 fix conflicts with plan:20 and the "three" wording at plan:75 and plan:84 unless those are widened too | INV-007 |
| MR-L1 | Low | "Successful usable reports" (plan:62) is not defined in code; a success with an empty body can count toward the two-report guard | INV-008 |
| MR-L2 | Low | Resumed runs give an empty suggestion; Task 4 documents only the too-few-reports reason | INV-009; X-002 |
| MR-L3 | Low | A spec scaffolded before the fix keeps the stale command as caller-owned input; document only | V1/V2/V3 Round 2 |
| MR-N1 | Note | Goal text "Find small safe cleanups I could apply" (interview.md:15, wizard-guide.md:63) should be recorded as a deliberate keep | INV-010 |
| MR-N2 | Note | sc-bare-review/SKILL.md:21 names `/sc:code-review` as a bare-review caller; out of scope, record in documentation-check.txt | V1 Round 2; INV-006 |
| MR-N3 | Note | Existing real-dispatch test calls the subcommand directly; plan:34 requires the public `swarm_group` | V2 U-005 |
| MR-D1 | Dropped | V1 row 3: resume renders literal `{compare_files}` | Refuted: commands.py:2578-2586 passes no template; reduce.py:553 default ""; reduce.py:460-461 returns "" (r1:16; X-002, 100%) |

Merged verdict: FAIL (1 Blocking: MR-B1).

## Planned Changes

### Change 1: Rewrite the blocking finding's evidence and fix (from debate consensus, X-001)
- **Source**: debate-transcript.md Round 2 (V1, V2, V3 rebuttals); invariant-probe.md INV-006, INV-007
- **Target**: Base deviation row 1 (replace)
- **Rationale**: X-001 agreed at 100%; all advocates conceded the base fix count "four to six" is wrong (eight active mentions) and sync-dev is not required
- **Integration point**: MR-B1 in the merged findings table
- **Risk**: Medium: this is the decision-bearing finding
- **Concrete anchors preserved**: plan:79, plan:81, plan:84; refs/cli-contract.md:44; refs/interview.md:65; src/superclaude/commands/swarm-wizard.md:94; docs/swarm/wizard-guide.md:216; README.md:67; lens-catalog.md:25 and :49; user-guide.md:200; wizard SKILL.md:32-36, 71-73; source.md:1 "Update the matching documentation"
- **Threshold preservation**: count "four" (plan:84) -> replaced by a required search, disposition modified-with-rationale (Round 2: four, six and eight all named; a fixed number is fragile). V3 card count "six" -> dropped-with-rationale (undercount). Eight -> preserved as the currently observed total, not as an acceptance constant.
- **Fix text to carry**: delete the fixed count at plan:84; require a repo-wide search for active refactor-find hand-off mentions excluding refactor_find.py:53, release-notes-v1.md:34, docs/testing/**, and built-in `/code-review` mentions not tied to a lens; give every hit of the search pattern a disposition in ./artifacts/documentation-check.txt (including docs/dev/lens-contribution-policy.md:190, agents/reuse-auditor.md:3,16, reflect/ensemble.py:77, tests/pr_submit fixtures, docs/testing/v6.0.0/post-release-report.md:170 per INV-006, or narrow the pattern); name refs/cli-contract.md, refs/interview.md, swarm-wizard.md and wizard-guide.md in Task 4; remove the plan:81 sentence; no sync-dev step is required for correctness (.claude/skills absent in this worktree); never stage .claude (plan:26).
- **Impact statement to carry**: the wizard presents `recommended_next_command` verbatim after a run (refs/run-monitor-summarize.md:88-89), so after Task 3 the final copy-paste step is correct; the stale tables mislead the pre-run lens explanation and plan and contradict the run output. The blocker rests on the false plan:81 decision and plan:84 number.

### Change 2: Add the plan-constraint widening as MR-M4 (from INV-007)
- **Source**: invariant-probe.md INV-007
- **Target**: new Medium row after MR-M3
- **Rationale**: MEDIUM UNADDRESSED invariant warning; plan:20 and the "three" wording at plan:75/plan:84 would make the MR-B1 fix look like a scope breach
- **Integration point**: findings table, plus a cross-reference from MR-B1's fix
- **Risk**: Low: additive

### Change 3: Refine the default-detection finding (MR-M1) (from V1 row 1, V2/V3 Round 2, INV-001, INV-003)
- **Source**: V1 v1:13; Round 2 V2 rule; INV-001, INV-003
- **Target**: Base row 3 (replace text, keep Medium)
- **Rationale**: X-003 agreed 95%; probe showed an equality-only rule would also match edge-case-hunt (edge_case_hunt.py:53) after Task 2
- **Integration point**: MR-M1
- **Risk**: Low
- **Concrete anchors preserved**: commands.py:929-930, 1178, 1684, 2141-2144, 2152, 3735-3737, 1297-1304; preflight.py:539-543; plan:22, plan:60, plan:64, plan:69
- **Rule to carry**: the refactor-find bundled default applies only when the lens is refactor-find (lens name at commands.py:2152) AND (run is `--lens` mode OR the post-preflight template equals the current refactor-find default) AND no caller compare_files; tests add scaffold-to-stdin, detached `--lens` (child runs as spec-file, commands.py:1297-1304), and edge-case-hunt in spec/stdin mode keeping its prefix.

### Change 4: Refine the quoting finding (MR-M2) (from V3 row 4, Round 2, INV-004, INV-005)
- **Source**: v3:17; V3 Round 2; INV-004, INV-005
- **Target**: Base row 4 (replace text, keep Medium)
- **Rationale**: X-004 agreed 95%; probe showed shlex quoting is not proven against the consumer, which only splits on commas (sc-adversarial-protocol SKILL.md:562-565; adversarial.md:15,39,58)
- **Integration point**: MR-M2
- **Risk**: Low
- **Fix text to carry**: the plan must name one form, show in Task 3 evidence that the consumer's documented comma-split rule accepts it (a shlex.split round-trip only proves producer intent), confine quoting to the refactor-find default branch so siblings are unchanged (plan:69; shared builder commands.py:2141-2144), keep the no-suggestion rule for commas inside paths, or record the form as a known gap.

### Change 5: Replace base row 2 with the correct wizard-guide reading (MR-M3) (from V1 row 2, C-002)
- **Source**: v1:14; C-002 (V1 wins, 95%)
- **Target**: Base row 2 (replace rationale)
- **Rationale**: the line lists "the follow-up each lens hands off to"; no lens template uses built-in `/code-review` (lens files listed in V1 Round 2); the base's "real built-in" reason was conceded wrong
- **Integration point**: MR-M3, remedied inside MR-B1's fix list (drop the entry)
- **Risk**: Low

### Change 6: Add coverage table (from V2)
- **Source**: v2:18-27
- **Target**: new "Coverage" section after the findings
- **Rationale**: S-004 V2 wins 95%; base lacks per-requirement mapping
- **Integration point**: new section; INF004 row corrected to "partially covered: three docs only; see MR-B1"
- **Risk**: Low: additive
- **Concrete anchors preserved**: every plan line range in v2:20-27, verbatim

### Change 7: Add Low and Note rows MR-L1..MR-L3, MR-N1..MR-N3 (from probe, Round 2, V2)
- **Source**: INV-008, INV-009, INV-010, INV-006 note; Round 2 pre-fix scaffold case; v2:34
- **Target**: findings table, after Mediums
- **Rationale**: recorded non-blocking items; they never fail the review or start a fix pass
- **Risk**: Low

### Change 8: Record the dropped finding MR-D1 (from V1 row 3, X-002)
- **Source**: v1:15; r1:16; X-002 (100%)
- **Target**: new "Dropped findings" section
- **Rationale**: minority claim refuted by actual function arguments, not by grep absence or vote
- **Risk**: Low

### Change 9: Preserve verified supporting evidence and limits (from V1, V2, V3)
- **Source**: v1:21-24, v1:27-28; v2:30-36; v3:23-27
- **Target**: "Evidence checked" and "Limits" sections
- **Rationale**: S-006 V1 limits style; C-008/C-009/C-010 evidence; U-007 golden verified
- **Concrete anchors preserved**: _validate.py:417-429; adversarial.md:15,39; reduce.py:672-697; test_commands_run.py:507-542; tests/swarm/fixtures/bare_review_v1/golden/all-success/return-contract.yaml:28; reflect/ensemble.py:404; release-notes-v1.md:34; william.md:50
- **Risk**: Low

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|---|---|---|
| S-001 / C-007 | V1 PASS (with notes), V2 PASS | All three advocates conceded FAIL; X-001 100% |
| X-001 (V2 card) | INF004 covered by three docs / four occurrences | Refuted by refs/cli-contract.md:44, refs/interview.md:65, swarm-wizard.md:94 |
| X-003 (V2 card) | Default/caller distinction not a deviation | V2 advocate conceded; Medium kept |
| X-004 (V2 card) | Quoting covered at plan:62-68 | V2 advocate conceded; plan:62 names no form |
| V1 row 2 disposition | Scope wizard-guide.md:216 out in documentation-check.txt | V1 advocate withdrew it in Round 2 in favour of fixing the entry |
| V1 row 3 | Resume renders literal placeholder | Refuted (MR-D1) |
| V1/V2 recommendations | "Proceed to execution" / "Accept QA PASS" | Contradicted by MR-B1; dropped-with-rationale |
| V3 timestamp line | Reviewer-supplied 2026-11-23T18:30:00Z | Unverified metadata; V3 advocate agreed to drop it |
| Base "sync-dev" step | Required by the fix | Conceded not required; .claude/skills absent |

Omitted anchors from non-base variants: V1 "Bare-review golden ... :28" is preserved (Change 9); V2 relative plan link `../../TASK-...md` (v2:17) omitted as wrong (r2:7), replaced by the absolute plan path; no requirement ID, threshold or acceptance anchor from V1 or V2 is dropped without a row above.

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|---|---|---|---|
| 1 | Medium | Wrong blocker fix would misdirect the plan reviser | Revert to base row 1 text plus Round 2 transcript |
| 2 | Low | Executor treats wizard edits as scope breach | Remove MR-M4 row |
| 3 | Low | Sibling lens rerouted if rule miscopied | Revert to base row 3 |
| 4 | Low | Unproven quoting form adopted | Revert to base row 4 |
| 5 | Low | Wrong rationale kept | Revert to base row 2 |
| 6 | Low | Additive | Remove section |
| 7 | Low | Additive | Remove rows |
| 8 | Low | Additive | Remove section |
| 9 | Low | Additive | Remove sections |

## Review Status
- [x] Auto-approved (default)
- [ ] User-approved (--interactive)
- Approved by: auto
- Approval timestamp: 2026-11-23T18:43:33Z
