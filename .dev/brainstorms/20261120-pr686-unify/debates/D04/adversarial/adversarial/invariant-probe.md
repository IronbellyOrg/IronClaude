# Invariant Probe Results (D04 claim level and grants)

## Round 2.5 - Fault-Finder Analysis

Fault-finder: independent agent (a86821ec5d4611789), not an advocate. It probed the emerging consensus (none-only live claim, Pipeline read deferred, four standing grants, `pr.merge` and `issue.close` per PR through an `answer-check`-style go, adopt `answer-check`, `refuse(argv)` and mailbox supervision). The orchestrator re-read the evidence for INV-001 (grep of master, pr-a and pr-p snapshots for `GOVERNED_LEVELS_ALLOWED`: no match) and for INV-004 (D:582 lists thirteen merge-gate reasons, `changes_requested` and `merge_safety` among them; D:588 runs a raw `gh pr merge`).

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | state_variables | The constant `GOVERNED_LEVELS_ALLOWED` exists and is False, so a test or spec text can key to it | UNADDRESSED | HIGH | No match in master, pr-a or pr-p snapshots; it exists only in the unpushed worktree `claim-handoff-planb` (`launch.py:48`, R33 `requirements.md:59`). The live gate on master is `PROMPT_PATTERN` pinned to `--pipeline none` (`launch.py:33`) plus the Wave 8 ship-gate text. Round 2 answer (a) of A keyed the spec to a name master does not have |
| INV-002 | state_variables | The standing grants live in `repos.yaml` and change only through `answer-check` | UNADDRESSED | HIGH | D:688: "ours are inside it and are guarded by the verb and by a test"; an agent session can write any file; D:300 lists validated `repos.yaml` fields and gives no rule for an absent or malformed `grants` value |
| INV-003 | guard_conditions | Claiming at none and starting one `worker-start` worker bounds what the worker can do | UNADDRESSED | HIGH | D:117: no L1 guard, no L2 pre-push, `master` not protected, "nothing on GitHub stops a worker that ignores its prompt"; `refuse(argv)` (D:1117) limits the orchestrator, not the worker; ADD1 (D:135) says the contract is still to be rewritten; Q34 and Q38 accepted this for the one test issue only |
| INV-004 | guard_conditions | `E-NO-GRANT` plus `answer-check` gate `pr.merge`; the go is "keyed to the PR and head sha" | UNADDRESSED | HIGH | D:588 raw `gh pr merge`; D:696 limits `E-NO-GRANT` to the orchestrator's own verbs; `merge_safety:<PR>:<head sha>` (D:598) is the key of the merge-safety hold only; the closed set of thirteen gate reasons (D:582) has no "recorded merge go", so `merge_ok: true` can print with no recorded go |
| INV-005 | guard_conditions | An issue reassigned or closed after claim stops being worked | UNADDRESSED | MEDIUM | D:1109 frees the place at the next hourly check (window up to an hour); D:582 reasons include no `unassigned` or `closed`; the "assigned to the user" condition of DQ6 (D:116) is enforced by verbs, which merge does not use |
| INV-006 | count_divergence | How many of the six grant entries `E-NO-GRANT` really covers | UNADDRESSED | MEDIUM | B's Round 2 (iii) says at most 2 of 6; the consensus text implies about 4 are covered; `issue.close` is written by `/sc:closeout` (D:605, D:799), `pr.merge` is raw (D:588); coverage of `issue.comment` (the R24 result comment) is not shown |
| INV-007 | count_divergence | "Three in flight" is a fixed limit | ADDRESSED | LOW | D:93, D:113, D:289, D:300: `max_in_flight`, integer 1 to 10, default 3; 12 observations = 9 + OB-H2 + OB-H3 + OB-CTX |
| INV-008 | collection_boundaries | Empty or missing grants, unlisted repo, no Pipeline value and an empty plan fail safe | ADDRESSED | MEDIUM | D:300 "no grant, no write"; D:112 and D:114 unlisted or disabled repo is information only; R34(2) (`requirements.md:60`) absent Pipeline is None; D:1099, D:445 holds. Residual gap: `grants: []` and its effect on the poll's own `issue.hold` write is not stated |
| INV-009 | interaction_effects | The only brake between claim and merge is `hold:backlog`, which must exist | UNADDRESSED | MEDIUM | D:445: the label is created once per repo by hand (O3, U31); if absent no person can place the brake; it stops the claim wave only; no mid-flight stop is listed (per repo: `enabled`, `max_in_flight`; per PR: the gate reasons) |
| INV-010 | interaction_effects | The gate flips safely later because "Pipeline picks the level" stays as the gate-open design | UNADDRESSED | MEDIUM | D:575 ends waves on `worker_done`; a launched agent reports through `result.md` (R24); R36 (`requirements.md:62`) withdrew the value-time check, so a Pipeline raised after approval is blocked only while the gate is closed; the flip removes that protection with no replacement |
| INV-011 | interaction_effects | Two orchestrators or hosts cannot claim the same issue | ADDRESSED | MEDIUM | D:113 (DQ3): poll routing, `O_EXCL` state files, claim stop, lowest-comment-id lease; same-login re-claim is idempotent (`refs/claim.md:43`) so the lease is the only arbiter; survival of the lease after a state restore is not shown |
| INV-012 | sufficiency_challenge | The consensus alone makes unattended claiming safe | UNADDRESSED | HIGH | Falsifiers: (1) `ironbelly` is "the one login shared by the owner and every session on this host" (`owner-answers.md:162`), and `answer-check` is hardwired to Clay's terminal or Clay's ClickUp id (D:694), so a chat go does not prove the owner gave it; (2) unprotected `master` and no hook (D:117); (3) R10 and ADD1 (D:135) contradict WORKER-CONTRACT lines 239-246, still unrewritten. No evidence for "none" found |

## Summary

- **Total findings**: 12
- **ADDRESSED**: 3 (INV-007, INV-008, INV-011)
- **UNADDRESSED**: 9
  - HIGH: 5 (INV-001, INV-002, INV-003, INV-004, INV-012)
  - MEDIUM: 4 (INV-005, INV-006, INV-009, INV-010)
  - LOW: 0

Gate result: CONVERGENCE BLOCKED: 5 HIGH-severity UNADDRESSED invariants (INV-001, INV-002, INV-003, INV-004, INV-012). MEDIUM items are warnings. The HIGH items are carried into the verdict as spec requirements (none of them is a reason to change the winner; each is a condition the spec must state).
