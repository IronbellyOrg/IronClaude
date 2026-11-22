# Position OURS (Q04): a typed go per push class, bound to the head sha

Notation: "WC:nnn" is a line of `src/superclaude/core/WORKER-CONTRACT.md` and "D:nnn" a line of `docs/designs/orchestrator.md`, both in the read-only export `/home/coder/.cache/ic-snap-20261120/master` (origin/master 61ac2c2e6). "SPEC:nnn" is a line of `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/spec/SPEC.md`.

## Claim

A push publishes commits the person has not seen. The person's typed go is therefore needed for each push class, and the go is bound to the exact sha being published, so a go for one state of the branch cannot release another state. Merge keeps its own go (SEC-01). The only built exception the owner has accepted is the Full Submit per-issue go (R25), and it stays narrow: that issue's push and PR only.

## Mechanism

1. A push go is a typed line in the person's own session that names repo, branch and the sha to be pushed (the same shape as the merge go, SEC-01 at SPEC:288).
2. Each push class gets its own go: first push and PR; each fix-round push; a push after a revert; a push after a rebase (a force push, refused unless the go names old and new sha); a merge (its own go, never covered by a push go).
3. A go is consumed by the push it names and is void when the branch head moves to a sha it did not name.
4. The Full Submit field value (Pipeline = Full Submit plus the `Approved` field) is the one owner-recorded standing go, for that issue's first push and PR only (R25).

## Cited facts

1. WC:245: "Before any push that would publish worker commits the person has not seen, the coordinator shows them to the person and pushes only on the person's go; no earlier pre-authorization waives this. A commit grant covers one Task and ends at that Task's `worker_done`." The rule is per publication, and it names pre-authorization as not enough.
2. WC:244 and WC:23: PRs go only through `/sc:pr-submit --monitor 3` in an ordinary top-level session, never as a worker; `/sc:pr-submit` is on the never-as-worker list (owner decision D3, recorded in `/home/coder/workspaces/IronClaude/.dev/orca-command-refactor/decisions/APPROVED.md:10-13`, per D06 VERDICT).
3. The owner's rule in the spec: SPEC:124 and SPEC:467 both say "a person's typed go precedes every push and merge". The spec panel graded the rule as holding for merge and only "two unreconciled cases" for push (spec panel report, finding F4, `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/spec/panel/review-1/spec-panel-report.md`, line 26 and the rule table row 2).
4. Master IronClaude is unprotected, there is no ruleset and the acting user holds `maintain` (D:118; risk K12, D:1234). Nothing on GitHub stops a push, so the person's go is the only brake (D06 VERDICT, strongest point 2; Clay's advocate agreed in D06 round 2).
5. Workers run with no L1 guard and no L2 pre-push hook, and a worker's own script can still push a feature branch (D:117 DQ7; SPEC:300 SEC-13; D05 VERDICT item 4: the guard "narrows honest drift on master and main", not a script run). A go that lasts "until merge" would make every such push look authorized.
6. A real miss by an unattended push: on 2026-11-04 the owner squash-merged PR 368 mid-cycle, GitHub deleted the branch, and the skill's round-2 push re-created the deleted branch with an unmerged fix (commit 2306437c; memory `pr-submit-check-pr-open-before-push`, 15 days old, not re-verified). A go that outlives the PR's state is how that happens.
7. `/sc:pr-submit` itself treats the push as separately gated: ordinal gates G-arm, G-edit, G-push (`src/superclaude/commands/pr-submit.md:46`), L2 halts before the push (`SKILL.md:307`), and the merge push is allowed only with exact parents (`pr-submit.md:121`). The push is a named, separately granted capability, not a by-product.
8. Q01 recommendation 5 and D06 item 1 already give the merge go an end (action done, head moves, owner revokes) and a head sha. Extending head-sha binding to push uses the same record and the same check (Q01 VERDICT item 5).
9. Full Submit is already scoped narrowly in the owner's own text: "that setting is the person's go for that issue's push and pull request, and nothing else is pushed" (requirements.md R25 row; D06 item 7 amendment of WC:245).

## What it costs

- A person is asked once per push class instead of once per PR. For a normal PR that is the first push (their own `/sc:pr-submit` line) and a merge.
- The strict per-fix-push reading would cost one prompt per review round, up to 5 rounds (`--max-rounds` hard cap 5, `pr-submit.md:47`). That is real friction and it makes `--monitor 3` behave like `--monitor 2` in practice.
- A go record and a sha check must be built (not built today; D06 notes the gate and verb are design only).

## What it risks

- Taken literally (a fresh go per fix-round push inside one `/sc:pr-submit` run), it contradicts the project's own mandatory PR path: `CLAUDE.md` says `/sc:pr-submit --monitor 3` "fixes the confirmed findings ... pushes the fixes without asking". OURS must say plainly that the typed `/sc:pr-submit --monitor 3` line is the person's go for that run, or the rule cannot be followed.
- A go bound to a head sha cannot be given in advance for a fix commit that does not exist yet, so a per-push sha-bound go is impossible inside an unattended fix loop. This is the strongest point against the strictest form.
- D06 and Q01 bind the head sha to the merge go, not to the push go; no verdict says the push go carries a sha (WC:245 names none). The strict reading as stated in the topic (sha-bound per push) is OURS extended, not OURS recorded.

## What it gets right

- It keeps the one rule that protects an unprotected `master`: nothing publishes unseen commits without a person.
- It separates push from merge, so a push go can never release a merge and a merge go can never release a push (SEC-01, SEC-12).
- It gives every class that changes the commit set (revert, rebase, re-run) its own go, which is where the PR 368 incident and `push_range_mismatch` show the risk lives.
