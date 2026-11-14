# Round 1 advocate statement: Variant 3 (proposal C, combination), persona qa

## Position summary

Variant 3 is the only shape whose acceptance test catches both ways the fix can fail: a configured program still runs, or a worktree's git state is silently wrong and presented as a normal scan (variant-3-original.md, "What happens next" step 2). Its weak point is that its trigger, "could change the answer", is harder to decide than variant 1's "could run", and on filters the two shapes give nearly the same result.

## Steelman

**Variant 1 (F2, fail closed).** It has one behaviour, and a worktree is either scanned unchanged or reported `unscanned` with a reason. No result can be distorted, because nothing is changed (variant-1-original.md, "What it unlocks": "Status results are never altered"). It is also the only variant that turns the two host facts into a counting rule: the system git-lfs filter "counts only in a worktree whose attributes select it" (step 3). That answers the over-refusal risk in question.md line 17. It also notes that a hit in the inherited environment affects the whole run, not one worktree (U-004). For QA this is the easiest shape to test: two outcomes and no third, "scanned but altered", state.

**Variant 2 (the author picks).** The fix design "belongs to the #539 author and the owner" (ADJ line 206, quoted in question.md line 60). Implementation details that only appear in the code, for example how git-lfs behaves under each shape (question.md line 18, UNVERIFIED), are best judged by the person reading that code. It also matches the spec's own recommended answer, "F1 or F2" (question.md line 31). It is the only variant that does not claim to cover channels nobody listed. It says the ruling must name any channel it leaves out, which can be audited.

## Strengths claimed

1. **Two-sided regression test (U-003, C-005).** The test fails if any in-scope program runs, and it also fails if "a worktree whose result would be altered is reported as scanned" (variant-3-original.md step 2). Neither other variant pins the second failure. Under variant 2, a pure F1 choice in an LFS repository could report LFS files as changed (question.md line 18) and still pass a test that only checks "covers every in-scope channel" (variant-2-original.md step 2). That is a silent wrong answer that passes CI.
2. **It handles both of the host's failure edges.** Pure F1 risks wrong results in LFS repositories (question.md line 18). F2 written too broadly refuses every worktree, because `/etc/gitconfig` defines `filter.lfs.*` for all of them (question.md lines 15, 17). Variant 3 states both edges as constraints the ruling must respect (step 3).
3. **It keeps information where disabling is harmless.** A worktree that only configures `core.fsmonitor`, a speed-up, stays scanned with its git facts instead of becoming `unscanned` (variant-3-original.md "What it unlocks"). That fsmonitor's absence never changes `status` output is UNVERIFIED on git 2.47.3.
4. **The owner decides now.** The coordinator-visible result (scanned or `unscanned`) is settled at W0 (question.md line 42) and not discovered inside a 1003-file PR.

## Weaknesses identified in other variants

- **Variant 1, X-001.** "The sweep never runs a configured program, including through a channel nobody listed" overclaims. Its refusal fires only on what its check detects, and an unlisted channel is by definition not tested. The claim cannot be verified, so it should be dropped from the ruling text.
- **Variant 1, information loss.** Every worktree that configures fsmonitor or included config is `unscanned`, even where nothing about the answer would change. How many of the 29 worktrees that affects is UNVERIFIED (variant-1-original.md "Costs").
- **Variant 1, whole-run refusal.** By its own account an inherited-environment hit refuses the whole run (U-004). The session already carries `GIT_CONFIG_COUNT=2` (question.md line 19). The "could run" rule has to classify those credential keys correctly, or no sweep runs at all. Variant 1 does not state how the environment channel is counted, only how the lfs filter is.
- **Variant 2, untestable deferral.** The owner gives up the decision that most affects what the coordinator sees (variant-2-original.md "Costs"), and its regression test has no criterion against altered results. Whichever shape the author picks, the test does not fail on the F1 failure mode.
- **Variant 2, extra review step.** The shape is reviewed only at SW-05. A shape the owner rejects then sends the work back after implementation, on the critical path for XC-04 and the v2 start gate (question.md line 41).

## Concessions

- **The trigger is harder to decide (A-001).** Variant 3 must decide both whether a program could run and whether disabling it would change the output. Variant 1 decides only the first. If the second cannot be decided reliably, the combination either leaks a wrong result or refuses, and then it collapses into variant 1.
- **On filters it equals variant 1.** A filter whose attributes select it is exactly where it could run and exactly where disabling changes the answer, so both variants refuse it. The real difference shrinks to fsmonitor-only worktrees, and possibly to included or environment settings that name no output-affecting program. That benefit is unmeasured.
- **Two behaviours cost more** to build, test and review inside a 1003-file PR (variant-3-original.md "Costs"; C-006).
- **Unlisted channels.** "Disabled if safe, otherwise refused" (C-003) has the same detection problem as variant 1's X-001: an unknown channel can be neither disabled nor refused on purpose.
- **Spec wording.** The spec offered F1 or F2, not a combination (variant-3-original.md "Costs"; question.md line 25).

## Shared assumption responses

| Id | Response | Reason |
|---|---|---|
| A-001 | QUALIFY | A conservative over-estimate can be decided from configuration and attributes: treat a program as able to run whenever any attribute source could select it. An exact decision would need every source git reads (attributes from config as well as files), and whether that can be done without git's own machinery is UNVERIFIED. The safe reading pushes both variant 1 and variant 3 toward refusal on doubt. Variant 3's extra question, "would the answer change", is the harder half. |
| A-002 | ACCEPT | Every shape needs it: narrowing the `git status` paths without separating them from the contract allow-list and transcript scans changes the pinned rows (ADJ line 469, INV-039). None of the three variants says so, and the ruling should state it explicitly. |

## Per-point positions

| Point | Superior variant | Confidence | Reason |
|---|---|---|---|
| S-001 | none (identical) | 50 | Same sections and order by design of the brief. |
| C-001 | V1 = V3 (owner now) | 70 | Deciding at W0 avoids a rejected shape coming back after SW-02 on the merge critical path. |
| C-002 | V3 | 60 | It keeps facts for harmless-to-disable worktrees and withholds altered results, but only if A-001 holds. |
| C-003 | V2 | 60 | Naming the channels left out is the only claim that can be audited; V1 and V3 both imply coverage of unknown channels that no test can confirm. |
| C-004 | V1 | 70 | It turns the host facts into a concrete counting rule (the lfs filter counts only where attributes select it), which is the most testable form. |
| C-005 | V3 | 80 | The two-sided test is the only one that fails on a silently wrong scan as well as on a program running. |
| C-006 | V1 | 75 | One behaviour means fewer states to test and review in a 1003-file PR. |
| X-001 | V2 | 70 | V1 overclaims coverage of unlisted channels; V2 does not. |
| X-002 | V1 = V3 (owner) | 60 | ADJ line 206 names "the #539 author and the owner"; the owner fixing the outcome-level shape is consistent with that and removes a review loop. |
| X-003 | V1 | 65 | F2 fails on this host only if its rule is written broadly; V1 writes the rule that avoids it, so V3's "avoids F2's failure" argues against a weaker F2. |
| A-001 | V1 | 60 | "Could run" is the easier question to answer; "could change the answer" adds a semantic judgment. |
| A-002 | none (all omit) | 50 | No variant states it; all need it added to the ruling. |

## Overall

Judged neutrally, I would recommend **variant 1 (F2 with its "could run for this worktree" rule)**, amended with three additions:
- variant 3's two-sided regression test (U-003);
- an explicit rule for counting `GIT_CONFIG_*` keys;
- the A-002 separation stated in the ruling.

Confidence: 60.

Variant 3 is the better choice only if the owner values git facts for fsmonitor-only worktrees enough to pay for a second behaviour and the harder "could change the answer" rule. How many such worktrees exist is UNVERIFIED.
