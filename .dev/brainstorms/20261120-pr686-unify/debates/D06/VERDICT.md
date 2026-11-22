# Verdict D06: Authority: merging, script-started coordinators, reviewer hold

## Question
CLAY lets the orchestrator merge (DQ8, D:118), lets a script start the coordinator and a worker run `/sc:pr-submit` (ADD1, D:135), and holds a PR when a reviewer shows no activity (ADD4, D:138). OURS: WORKER-CONTRACT lines 23, 70, 239-246 (coordinator opened by a person, acts only on the person's named go, never merges on its own, `/sc:pr-submit` never as a worker), `/sc:pr-submit` skip rule for a silent reviewer, and the owner rule that approvals are given in chat. Which authority model should the unified design use, and what safe subset of CLAY's automation (merge on explicit go, typed answers) can be adopted?

## Winner
HYBRID. The authority model is OURS (a person's typed go for every merge, `/sc:pr-submit` never an Orca worker, no standing merge grant); the separable, evidenced parts of CLAY (read-only merge gate, merge-time reviewer hold, typed-answer validator, refusal of unlisted GitHub writes, depth-0 script start) are adopted on top of it.

Notation: "D:nnn" is a line of `docs/designs/orchestrator.md` (the design merged by PR 681, Clay's design PR) in the read-only export `/home/coder/.cache/ic-snap-20261120/master` (origin/master 61ac2c2e6). "WC:nnn" is a line of `src/superclaude/core/WORKER-CONTRACT.md` in the same export. "INV-nnn" is a finding of the invariant probe (see Debate artifacts).

## Winning recommendation
The unified design's authority section must say the following. Each item is written so a test or a reviewer can check it. The full text is in `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D06/adversarial/merged-output.md`.

1. **Merge.** No merge without a person's typed go for that PR. The go names repo, PR number, the full 40-character head sha, the merge method (checked against the repo's `merge_method` or `release_merge_method`), the word "merge" and the gate output it refers to. It is typed in live chat after the gate output, recorded as an entry (repo, PR, sha, time), is one-shot (never a standing grant), expires (number is an Owner DECISION, no source gives one) and is void on a head change or any new gate reason. A passing gate never triggers a merge. Test: a merge command without a matching go entry is refused by the merge verb.
2. **Gate.** The `merge-gate` verb (13 closed reasons, D:582) is a read-only check shown to the person before the go and run again immediately before `gh pr merge <N> --repo <R> --<method> --match-head-commit <sha>`, which never carries `--auto`, `--admin` or `--delete-branch` (D:118). The merge is refused if any reason, open thread, review state, base branch or draft state differs from what the person saw (INV-001: the sha pin alone does not cover those). After a restart the PR state is read first (D:591). A fail-closed file list (D:597) and the `changes_requested` and `merge_safety` holds (D:583, D:593) are kept. The gate is design only today (not in master, PR 686, or branch `issue-655-pr-p`), so the spec calls it a requirement and "not shown to pass".
3. **What a go may override.** Never: `head_moved`, `draft`, `not_mergeable`, `snapshot_incomplete`, `changes_requested`, `review_stalled`, `review_none_present`, `checks_pending`, `review_pending`, `threads_open`, `worker_not_done`. Only with that reason's own question key: `checks_failing`, `merge_safety` (INV-004). Owner DECISION: confirm that `changes_requested` is a hard refusal (recommended).
4. **Silent reviewer.** `/sc:pr-submit` is unchanged and keeps its skip rule inside the fix loop (SKILL.md:29-32, table :363-364; project CLAUDE.md:58). A separate merge-time hold is added: the owner sets a per-repo `reviewers` list (`none` allowed, write-protected on the owner's recorded word), a review of the final head is requested from each listed reviewer (the loop never re-triggers an absent reviewer, SKILL.md:364; INV-009), then the gate waits up to a default of 60 minutes from the final head's checks finishing (UNVERIFIED default, Owner DECISION), then escalates to the person. Neither `review_stalled` nor `review_none_present` is overridable by a go. The reason: the loop's absent state is sticky and clock-based, and one done plus one absent reads clean (`src/superclaude/pr_submit/reviewers.py:390-391, :414-419`).
5. **Worker and `/sc:pr-submit`.** `/sc:pr-submit` is never run by an Orca `worker-start` worker (WC:23, WC:244; owner decision D3). Clay's "Orchestrated issue flow" (ADD1, D:135) is not adopted. The automated route to a PR is the ordinary top-level launch of Full Submit (`/sc:issue --claim <N> --pipeline full --submit`, requirement R25), which pushes a feature branch, runs `/sc:pr-submit --monitor 3` and never merges.
6. **Script-started coordinator.** Allowed at depth 0 (a terminal plus `ccsession`, never `worker-start`, D:112) when its launch prompt cites an authorization the owner gave in chat and an agent recorded, and lists only the duties that record names (requirements R9 and R17). The spec states that a launch-prompt authorization is self-attested (the script writes the prompt; INV-010) and must not call it verified.
7. **Contract amendments (owner chat approval first, none in force).** WC:70: "an Orca coordinator session the person opened, or one started at depth 0 by the owner's installed watcher under a standing authorization the owner recorded in chat." WC:245: "A push of a feature branch for an issue the owner set to Full Submit and approved with the approval label counts as the person's go for that issue's push and pull request only, and never covers a merge, a force push, a branch deletion or any other push." WC:23 and WC:244 stay unchanged.
8. **Standing lists.** The verb refusal `E-NO-GRANT` (D:696) is kept; the list holds only duties the owner recorded in chat and never `pr.merge` or `issue.close` (Clay's `grants` names both at D:116 and D:291). The merge must go through one verb that demands the go entry, because `E-NO-GRANT` does not see a raw `gh pr merge` (INV-011).
9. **Typed answers.** `answer-check` (D:694) is adopted as a validator of entry, question key, head sha and freshness only. The spec states it cannot tell a person from a script (the same terminal accepts `orca terminal send`, D:112; a script knows the sha) and lists spoofed typing as a residual risk (INV-003).
10. **Wording rule.** Every gate is described as "narrows" a risk, not "closes" it, until a named check exists (INV-012, INV-013).
11. **Nine-row "what reaches the person" list (D:664-696).** Adopted only as an inventory of reasons for non-outward decisions, as an Owner DECISION; every outward action still waits for the person's go.

## Strongest points

**OURS**
1. The rules are the owner's recorded decisions, and ADD1 reverses them: `/home/coder/workspaces/IronClaude/.dev/orca-command-refactor/decisions/APPROVED.md:10-13` records D3, D4, D5 and the GIT row (approved 2026-11-02, "Nothing here is reopened for debate", :3); ADD1 itself says ruling R10's autonomous merge "contradict[s] all of this" (D:135).
2. With `master` unprotected, no ruleset, and the acting user holding `maintain` (D:118, risk K12 at D:1234), a person's go is the only brake on a merge into the default branch. Clay's advocate agreed (debate-transcript.md Round 2).
3. The worker-runs-`/sc:pr-submit` route lacks its own preconditions: D3's AC-4.3 live check was never run (`.dev/tasks/done/TASK-WF-orcaWorkerContra-20261103-012232/source.md:224, :328`), and ADD1 admits `/sc:pr-submit` "has no unattended mode" (D:135).

**CLAY**
1. A mechanical gate turns "the person's go" into something testable: 13 closed reasons, head-pinned merge, fail-closed file list, restart reads state first (D:578-591, D:597); a rename out of `.github/workflows/` is invisible in `gh pr diff --name-only` but visible to the gate (D:597).
2. The reviewer skip rule loses a late reviewer: absence is declared on a clock or a settled peer (`reviewers.py:390-391`), is sticky for the run (SKILL.md:29-32), and one done plus one absent reads clean (`reviewers.py:414-419`); the owner's own memory records a Codex security review landing after a clean result (memory `pr-submit-check-pr-open-before-push`, 15 days old).
3. `answer-check` binds an answer to one question key and one head sha (D:694), `E-NO-GRANT` refuses unlisted writes (D:696), and a terminal plus `ccsession` start is depth 0 (D:112), which narrows D5's depth reason (`.dev/orca-command-refactor/decisions/D5/RECOMMENDATION.md:9`) to `worker-start` starts only.

## Clay strengths to adopt
- **Read-only merge gate (D:578-591, D:597).** Why: the owner's rules are prose; no hook binds the coordinator (`docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:318`). How: adopt as a check the person reads before the go; override the design so a passing gate never merges; add the second gate run (INV-001).
- **Merge-time reviewer hold (ADD4, D:138).** Why: it fills a verified gap in the skip rule (`reviewers.py:390-391, :414-419`) and is separable because it lives at the merge decision, not in the loop. How: keep the skip rule in `/sc:pr-submit`; override ADD4's sentence that a silent reviewer "is no longer skipped"; add the final-head re-trigger (INV-009), an owner-set `reviewers` list and write protection (INV-005).
- **`answer-check` as a validator (D:694).** Why: it stops a stale or mismatched answer standing for another PR or head. How: adopt with the stated limit (cannot prove a person typed it).
- **`E-NO-GRANT` (D:696).** Why: the only mechanical bind either side has on GitHub writes made through the verbs. How: keep the refusal, remove `pr.merge` and `issue.close` from the grants (D:116, D:291), route the merge through a verb that needs the go entry.
- **Depth-0 script start (D:112, `waker.py:144-169`).** Why: the depth argument in D5 covers `worker-start` only. How: adopt together with the owner-recorded authorization requirement (R9, R17) and the WC:70 amendment.
- **Per-repo `merge_method` and `release_merge_method` (D:118).** Why: the squash merge of release 6.1.0 (#658, a release pull request) was reverted by #662 (a revert pull request). How: the go names the method and the gate checks it. PR 686's `repos.py` already parses these keys (lines 47-84).
- **`changes_requested` hard refusal and `merge_safety` hold (D:583, D:593).** Why: stricter than OURS and fail-closed. How: adopt; `changes_requested` stays an Owner DECISION to confirm.
- **Post-merge audit (AU4a, AU7; D:812, D:601).** Why: it can find a merge the gate did not make, including a raw `gh pr merge`. How: keep after a go as well.
- **Nine-row reasons list (D:664-696).** Why: modest and separable, benefit not shown in use. How: inventory only, Owner DECISION.

## Our strengths that must be kept
- The person's named go for every merge and the live-conversation rule (WC:241, WC:108); no standing merge or close grant.
- `/sc:pr-submit` never an Orca worker (WC:23, WC:244); one ordinary session per PR (owner decision D3).
- Outward actions kept out of workers (owner decision D4), so a worker that ignores its prompt cannot push or merge.
- Push only on the person's go, with the Full Submit per-issue go (R25) as the single owner-recorded exception, after the WC:245 amendment (WC:245).
- Approvals in chat, never in files or relayed text (owner order 2026-11-17); only the person gives a Ruling (D2).
- The `/sc:pr-submit` skip rule inside the fix loop (SKILL.md:29-32; CLAUDE.md:58).
- The coordinator started by script only under an owner-recorded authorization (R9, R17).

## Actions
| Action | Type | Target | Order or dependency |
|--------|------|--------|---------------------|
| Ask the owner, in chat, to decide the open items: go expiry number, `changes_requested` hard refusal, 60-minute default, nine-row list, and whether a repo admin enables branch protection or required review on IronClaude `master` | DECISION | owner chat; items listed in `adversarial/merged-output.md` | First; everything below that changes a rule waits for it |
| Ask the owner, in chat, to approve R25 (Full Submit as a per-issue go) and R17/R9 (launch-prompt authorization) as amendments, because they are in a local unpushed plan and amend WC:245 | DECISION | `claim-handoff-planb` requirements rows R25, R17, R9 (branch `ironbelly/issue-watcher-zero-setup-plan`) | After the first row; before any WC edit |
| Amend WORKER-CONTRACT.md at WC:70 and WC:245 with the two sentences of the recommendation; leave WC:23 and WC:244; update `tests/skills/test_worker_contract.py` and the plugin mirror | LOCAL CHANGE | `src/superclaude/core/WORKER-CONTRACT.md` (then `make sync-dev`) | After owner approval of the amendments |
| Replace the authority parts of the unified design with `merged-output.md`; rewrite DQ8, ADD1, ADD4, OD1, OD3, OD4, risk K7 and K12, and the sentence "merging when every condition holds" in 5.6 | DOC | `docs/designs/orchestrator.md` (or the unified design chosen in D14) | With the WC edit |
| Do not open the orchestrator-skill PR (PR B, not yet opened) with the "Orchestrated issue flow" section of ADD1; its wave 7 asks for a go instead of merging | PR CLOSE (of the plan, nothing to close on GitHub) | design ADD1; PR B plan | Before PR B is opened |
| Keep PR 686's parsing of `merge_method`, `release_merge_method`, `merge_safety_files`, `reviewers` and `grants`; add write protection for `reviewers` and refuse `pr.merge` and `issue.close` as grant names | PR KEEP-ADAPT | PR 686 (rewrite of the watcher), `issue_watch/repos.py` lines 47-84, 227-238, 295-299 | D14 decides the PR; this is the authority rider |
| Build the merge verb and `merge-gate` with the second gate run, the go entry, the reasons table and expiry, and tests for INV-001, INV-002, INV-004, INV-009, INV-011 | LOCAL CHANGE (later build) | new code under the orchestrator package | After the DOC and WC changes |
| Leave `/sc:pr-submit` and its skip rule unchanged | PR KEEP | `src/superclaude/skills/sc-pr-submit-protocol/` | None |
| Record the residual risks (spoofed typing, self-attested launch prompt, unprotected `master`) in the unified design's risk register | DOC | unified design risk section | With the DOC change |

## Implications
- **Watcher and poll.** No change to what the poll does for authority. The poll's `grants` key must not carry merge or close.
- **Coordinator or orchestrator.** It prepares, checks and waits; it never merges on its own. Wave 7 of Clay's design becomes "show the gate output and wait for the go". Clay's throughput gain (fewer interruptions of the person) is given up; no measured figure for it exists, per Clay's advocate.
- **Claim pipeline.** Full Submit launch is the route to an automated push and PR; it never merges. R25 and R17 do not count until the owner approves them in chat and WC:245 and WC:70 are amended.
- **Dashboard and sweep.** A PR waiting for a go and a gate output awaiting the person are facts the observer and sweep can show; D11 should decide where that data lives.
- **What breaks.** Clay's wave 7 autonomous merge, ADD1's worker flow, K7's "merge when every condition holds", and PR B's planned contract section. Design text OD1, OD3, OD4 must be rewritten.
- **What the owner must know.** None of the adopted gates is built; seven HIGH-severity invariants stay open until built (INV-001, -004, -009, -010, -011, -012, -013); the person's typed go cannot be told from script-typed text; Clay's design was approved by Clay only, and no `ironbelly` approval of PR 681 is on GitHub per FULL-REPORT.md section 4 (not re-checked here).

## Confidence
About 85% that the authority model should be OURS with the CLAY gate and hold adopted as a hybrid (both advocates reached it and Clay's advocate conceded the authority-transfer parts; both had been given the weighting rule, which lowers the weight of that agreement). About 60% on the specific numbers (go expiry, 60 minutes) and on which gate reasons a go may override, because no source fixes them. What would change it: the owner choosing a narrow autonomous merge for a stated class of PR, or enabling branch protection with required review (which lowers the stakes of "who merges"); evidence that Codex reviews on push; evidence that the harness marks sent text differently from typed text.

## Unverified
- Whether the owner approved or saw PR 681 outside GitHub (FULL-REPORT.md section 4 is taken as read, not re-checked).
- Whether Codex reviews automatically on push or only on request (decides the dead-wait risk of the merge-time hold).
- The 60-minute default and the go expiry number (no source).
- Whether the harness marks text sent with `orca terminal send` differently from typed text.
- Whether R25's row status "built" means it is in master (it is a local, unpushed plan row).
- That a terminal plus `ccsession` start is depth 0 in Orca: D5 presumes it and design U3 (D:1261) lists it as a live test; not run.
- That `merge-gate` and `answer-check` exist nowhere (searched `src/` in the three exports only).
- The "go may override" choices per gate reason are this verdict's recommendation, not a source rule.
- Both advocates were given the owner's weighting rule, so their agreement is partly shaped by it; the invariant probe is the independent check.
- The memory note on PR 368 and the late Codex security review is 15 days old and was not re-verified.

## Debate artifacts
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D06/position-OURS.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D06/position-CLAY.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D06/adversarial/merged-output.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D06/adversarial/return-contract.yaml`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D06/adversarial/adversarial/diff-analysis.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D06/adversarial/adversarial/debate-transcript.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D06/adversarial/adversarial/invariant-probe.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D06/adversarial/adversarial/base-selection.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D06/adversarial/adversarial/refactor-plan.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D06/adversarial/adversarial/merge-log.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D06/adversarial/adversarial/return-contract.yaml`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D06/adversarial/adversarial/variant-1-original.md` and `variant-2-original.md` (same folder)
- Skill status: the adversarial skill ran in full at depth standard (two advocates, two rounds, invariant probe, dual-pass scoring, merge-executor). Its convergence gate ended BLOCKED_BY_INVARIANTS (seven HIGH items), so its own status is partial.
