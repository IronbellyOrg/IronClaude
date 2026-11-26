# Findings: issue #776

Issue: "[FEATURE] A skill for the two human approvals (claim and plan), and what Research, Spec and Debug workers do at plan approval". State OPEN, label `enhancement`, created 2026-11-24T18:29:53Z, no comments, no closing PR. Checked at commit a7ae3dd30 (worktree HEAD); origin/master f2894fc44 has no change to `src/superclaude/cli/issue_pipeline`, `src/superclaude/core/WORKER-CONTRACT.md` or `src/superclaude/skills` since (only `afb3ccf29` touched swarm).

## Verdict

**still-relevant.** The issue is a pair of open design questions for the owners (Ryan and Clay). Nothing has answered them and no code has moved.

Evidence:
- No approval skill exists: no `skills/*approv*` on HEAD or on origin/master (git ls-tree).
- No `approve` verb: `src/superclaude/cli/issue_pipeline/cli.py` commands are plan-hash (:62), check-approval (:77), init (:97), adopt-create (:109), adopt-mark (:118), record-create (:135), record-show (:162), record-mark (:180), release-worker (:201), complete (:226), stage-status (:409). Nothing in `issue_pipeline/` sets the claim approval (the `Approved` field is only read; design note `docs/designs/issue-watcher-status-pipelines.md:5`).
- Problem 2 is real in the source: `src/superclaude/cli/issue_pipeline/templates/worker-brief.txt:12` (`Plan approval: ... follow rule WC-17 ...`) sits in the shared `[head]`, so all four stages (`brief.py:19` `STAGES = ("research", "spec", "plan", "debug")`) carry it. The pinning test is `tests/issue_pipeline/test_brief.py:279` (`test_brief_points_at_the_plan_approval_rule_of_the_contract`, loops over every stage row).
- Approval code is plan-only: `stage_predicates.py:45` `STAGE = "plan"`; the key is `(issue, STAGE, marker.plan_hash)` at :294.
- Contract references hold: WC-17 at `src/superclaude/core/WORKER-CONTRACT.md:59`; coordinator plan-approval duty at :300; owner-says-in-chat rule at :57. `claim.md` summary, next steps and marked comments exist near lines 55 to 92 (line numbers approximate; UNVERIFIED to the exact line).
- Code that handles it and is merged: PR #707 (merged 2026-11-20T22:09:24Z).
- UNVERIFIED: what a live Research worker at level none actually does at the approval line (no run or transcript was read). UNVERIFIED: SEC-08 at `.dev/brainstorms/20261120-pr686-unify/spec/SPEC.md:297` on branch `ironbelly/orch-ledger-20261122` (not on this checkout).
- Related issues #698, #722, #727, #716, #733, #761, #571 are all OPEN (gh).

Real state: the shared brief tells every worker to follow WC-17 after "writing the plan"; only the plan row writes one. The approval machinery cannot approve anything but a plan.

## Complexity and size

Complexity: medium. Size: M. Reason: the code change is small once the owners decide (brief row split or a stage parameter, plus contract, design note and tests), but a skill touches the safety rule that a go is typed by the person in their own session, which needs decisions first.

## Priority

P2. Reason: it concerns the watcher's main safety gate, but the gate works for plan stages today, nothing is blocked on it, and the issue itself waits on owner answers (and, for claim approval, on #722).

## Concrete next steps

1. Owners (Ryan, Clay) answer: which approvals a skill may set (claim, plan, neither), and whether claim approval waits for #722.
2. Run the cheapest evidence step: read the transcript of an earlier level-none Research worker, or do one live run, to settle the UNVERIFIED question.
3. Decide for report stages: move the `Plan approval:` line from `[head]` into the plan row only (small change to `worker-brief.txt` and the test at `test_brief.py:279`), or add a stage argument to `stage_predicates.py` / `plan_hash`.
4. Make the brief, contract (`WORKER-CONTRACT.md:59`), design note and tests agree with that choice.
5. If a skill is chosen: write it under `src/superclaude/skills/` with installed paths only (CLAUDE.md rule on `src/superclaude/` paths), reuse `claim.md` summary, route plan approval through `check-approval`, and keep the own-session go.

## Dependencies

Needs: owner answers on this issue; #722 for the claim-approval half. Blocks: nothing found.
Soft links: #698 (approver rule, out of scope), #727 and #716 item C13 (how a decision reaches the person), #571 (future "stage other than plan" test).

## Related issues

#761 (source list of gaps), #698, #722, #727, #716, #733 (out of scope), #571, #707 (the merged watcher's PR). Lookup matches listed in the issue, not confirmed duplicates: #379, #699, #723, #725, #753, #409, #665, #655, #446, #717.

## Related PRs

#707 (merged: zero-setup watcher and coordinator, the code this issue builds on). No open PR targets #776 (gh pr list search "776" returned none).
