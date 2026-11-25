# Verdict Q04: Does one typed go cover the fix-round pushes?

Notation: "WC:nnn" is a line of `src/superclaude/core/WORKER-CONTRACT.md`, "D:nnn" a line of `docs/designs/orchestrator.md` (Clay's merged design from PR 681, the design PR), both in `/home/coder/.cache/ic-snap-20261120/master` (origin/master 61ac2c2e6). "SPEC:nnn" is a line of `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/spec/SPEC.md`. D06 is the debate on who may merge, Q01 the debate on who writes a go record, OAG1 the debate on how long a go lasts, D04 the debate on standing grants, D05 the debate on the launch guard (verdicts in the sibling folders under `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/`).

## Question

Spec panel finding F4 (spec/panel/review-1/spec-panel-report.md): the spec rule "a person's typed go precedes every push and every merge" (SEC rules, D06, Q01) is not reconciled with (a) the fix-round pushes that `/sc:pr-submit --monitor 3` makes after review findings and (b) the Full Submit per-issue go (SEC-15 in /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/spec/SPEC.md) that lets a launched worker commit, push a feature branch and run `/sc:pr-submit`. Decide for each push class whether a new typed go is needed: the first push and PR, each fix-round push by the same session on the same PR, a push after a revert or rebase, and a merge. OURS = the strict reading (a go per push, bound to the head sha, per D06 and Q01); CLAY = one go per issue or per PR covers every push of that PR's feature branch until merge (D:135 ADD1 and the Full Submit design). Read D04, D05, D06, Q01 and OAG1 verdicts and WORKER-CONTRACT.md lines about "pushes only on the person's go". The verdict must give one rule in a sentence that a test can check, and name the SEC/FR rows to change.

## Winner

HYBRID. The owner's per-publication rule stays for every push class except one: the person's own typed `/sc:pr-submit --monitor 3` line (or the Full Submit field) is the go for that one run's fix-round pushes, which is a separable, evidenced Clay benefit, while Clay's "until merge" scope and worker route are rejected.

## Winning recommendation

**The rule (one sentence, testable).** A push to a PR's feature branch needs a person's typed go, except that the person's typed `/sc:pr-submit --monitor 3` line (or the Full Submit field for that issue) is itself that go for the first push, the PR and the fix-round fast-forward pushes of that one run, ending when the run ends, when the PR is merged or closed, or when the branch head moves outside the run; a push after a revert or rebase (the go names the old and new sha), a push by any other actor or in a new run, and every merge each need their own new typed go, and a merge go is bound to the 40-character head sha.

**Per push class.**

| Push class | New typed go? | Why |
|---|---|---|
| First push and PR | No, if it is made by the person's typed `/sc:pr-submit --monitor 3` line or by the Full Submit field. Yes for a manual or coordinator push made without `/sc:pr-submit`. | The typed line is the go; WC:245 and WC:244 |
| Each fix-round push, same session, same PR, same run | No, while the tool's fence holds: one fix commit per cycle, a halt on `push_range_mismatch`, fast-forward only, no force push, no push to the default or protected branch, `push_count <= max_rounds + 1` (hard cap 5) | `SKILL.md:262, 342-348`; `pr-submit.md:47, 121`; a go cannot name a sha for a commit not yet written |
| Push after a revert | Yes | The commit set differs from what the person saw; outside the run |
| Push after a rebase | Yes, the go names the old and new sha (a force push; the tool never rebases or force-pushes) | `pr-submit.md:121`, `SKILL.md:343` |
| New `/sc:pr-submit` run on the same PR | Yes (the person types the new line) | A go ends with its run |
| Merge | Yes, always its own go, bound to the 40-character head sha; a push go never covers a merge and a merge go never covers a push | SEC-01 (SPEC:288), D06 item 1 |

**What the spec must also say.**
1. A go ends: with its run, when the PR is merged or closed, or when the branch head moves to a sha the run did not make. After that the next push needs a new typed go. (This answers the 2026-11-04 miss on PR 368, an owner-merged PR whose deleted branch a later round-2 push re-created; memory `pr-submit-check-pr-open-before-push`, not re-verified.)
2. The run line covers only pushes the tool itself makes. A worker's own script push, or any push by another actor, is covered by no go (SEC-13, D:117 DQ7).
3. The Full Submit field is a go given before the commits exist, so WC:245 ("no earlier pre-authorization waives this") would refuse it. It is therefore the one named exception, valid only after the owner approves R25 in chat and WC:245 is amended to name it. The amendment must say so, and must not claim the field is "given in the live session at the time of the run". Only the typed run line is live. (This corrects one clause in the debate's merged text, merge-log tension 2.)
4. The Full Submit go covers that issue's first push, the PR and the loop pushes of the one `/sc:pr-submit --monitor 3` run it starts, in a top-level session, and never a merge, force push, branch deletion or any other push. R25's current words "nothing else is pushed" must be amended to say the run's loop pushes are included.
5. A worker never runs `/sc:pr-submit` (WC:23, WC:244). ADD1 (D:135, the Clay design addition that lets a handoff worker run it) stays rejected, as D06 item 5 decided.
6. The coordinator's own push of worker commits (FR-32) stays strict: it shows the commits to the person and pushes only on the person's typed go (WC:245). The run line covers the tool's fix commits only, not worker commits the person has not seen.

**Tests that check it.** A push with no typed run line, Full Submit field or go record is refused. A second `/sc:pr-submit` run on the same PR needs a new line. A push after the PR is merged or closed, or after the head moved outside the run, is refused. A fix-round push count above `max_rounds + 1` cannot happen. A merge command carrying only a push go is refused. A push after a rebase without a go naming old and new sha is refused.

**Rows to change in SPEC.md.**
- SPEC:124 (the flow sentence) and SPEC:467 (the stage rules): "a person's typed go precedes every push and merge" becomes the rule's first clause plus "except the run line of `/sc:pr-submit --monitor 3` or the Full Submit field (SEC-15, SEC-22)".
- FR-32 (SPEC:233): restate the push clause as the rule; keep "only on a typed go in a person-opened session" for the coordinator's push of worker commits.
- SEC-15 (SPEC:302): amend the WC:245 text as in items 3 and 4 above; WC:23 and WC:244 stay.
- SEC-01 (SPEC:288): add "a push go never covers a merge, and a merge go never covers a push".
- New row SEC-22: the end of a run go (run end, PR merged or closed, head moved outside the run), with the tests above. The highest existing row is SEC-21 (SPEC:284 list).
- Section 13.2 guard probe row (SPEC:699): keep "a full `/sc:pr-submit --monitor 3` cycle only if level FS is ever opened", add that the probe records the end-of-go checks.
- L-07 (SPEC:357): the WC:245 edit waits on the owner's chat approval of R25, as already written.

## Strongest points

**OURS**
1. WC:245: "Before any push that would publish worker commits the person has not seen, the coordinator shows them to the person and pushes only on the person's go; no earlier pre-authorization waives this." A go that lasts until merge is exactly that pre-authorization (Clay's advocate conceded it, `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/Q04/adversarial/adversarial/debate-transcript.md`, Round 1).
2. Master is unprotected and the acting user holds `maintain` (D:118, risk K12 at D:1234), so a person's go is the only brake; the PR 368 miss shows a go that outlives PR state is how an unattended push goes wrong (memory `pr-submit-check-pr-open-before-push`).
3. `/sc:pr-submit` is never an Orca worker (WC:23, WC:244; D06 item 5 rejected ADD1), and a revert or rebase changes the commit set the person approved, while the tool never rebases or force-pushes (`pr-submit.md:121`, `SKILL.md:343`).

**CLAY**
1. A per-push go is impossible for a fix commit that does not exist yet, and a fresh go per round turns `--monitor 3` into `--monitor 2` (up to 5 prompts at the hard cap; `pr-submit.md:38, 47`). The project `CLAUDE.md` says the mandatory path "pushes the fixes without asking". OURS' own Risks section conceded the point (X-001).
2. The tool fences its own pushes mechanically: one fix commit per cycle, `push_range_mismatch` halt, fast-forward only, no default-branch push, `push_count <= max_rounds + 1` (`pr-submit.md:121`, `SKILL.md:262, 342-348`), so a run-level go is bounded and testable.
3. The owner's own R25 is already a go that stands for a push and its PR without a typed line per step (requirements.md R25 row in `claim-handoff-planb`; D06 item 7), so one go can cover a bounded unit of work.

## Clay strengths to adopt

- **A run-level go for fix-round pushes.** Why: a sha-bound go per fix push cannot exist (the sha is not known until the commit is made), and OURS' strict reading would contradict the mandatory `/sc:pr-submit --monitor 3` path (`CLAUDE.md`; `pr-submit.md:38`). How: the typed run line is the go for that run's first push, PR and fix-round pushes, limited by the tool's fence; override Clay's "until merge" with the end events above.
- **The tool's push fence as the stated condition of the run go.** Why: it makes the go testable (`SKILL.md:262, 342-348`). How: list each fence item as a test; the go is void if any item fails.
- **Merge-time controls as the catch for a bad fix push.** Why: a person sees the final head only at the merge go (D06 items 1, 2, 4: the 13-reason gate, `--match-head-commit`, reviewer hold). How: keep the merge go sha-bound and run the gate twice, as D06 says.

## Our strengths that must be kept

- A typed go for every class that changes the commit set: revert, rebase, new run, manual or coordinator push.
- Merge as its own sha-bound go; push go and merge go never cover each other (SEC-01, SEC-12).
- WC:245's "no earlier pre-authorization", with Full Submit as the single named, owner-approved exception.
- `/sc:pr-submit` never as a worker (WC:23, WC:244; ADD1 rejected).
- A go that has an end, so it cannot outlive PR state (PR 368).
- The honesty note: D06 and Q01 bind the head sha to the merge go only. A sha-bound fix-round push was "OURS extended", not owner text, so it is dropped.

## Actions

| Action | Type | Target (file, PR or issue number) | Order or dependency |
|---|---|---|---|
| Owner approves in chat: the typed `/sc:pr-submit --monitor 3` line is the go for that run's fix-round pushes; the Full Submit field is a named exception to WC:245 (R25 and its amendment) | DECISION | owner chat; `claim-handoff-planb` requirements R25; WC:245 | First; nothing below that edits the contract waits on it |
| Rewrite the push clause of the spec rule in the places listed under "Rows to change" | DOC | SPEC.md lines 124, 467, FR-32 (233), SEC-15 (302), SEC-01 (288), 13.2 row (699) | After the first row for SEC-15; the rest may go with the spec |
| Add SEC-22 (end of a run go) with its tests | DOC | SPEC.md section 4.5 | With the rewrite |
| Amend WC:245 to name the run line and the Full Submit field, leave WC:23 and WC:244, update the contract test | LOCAL CHANGE | `src/superclaude/core/WORKER-CONTRACT.md` line 245 and `tests/skills/test_worker_contract.py` (then `make sync-dev`) | After the owner's chat approval (row 1); this is spec stage S8 |
| Reject ADD1 in the unified design text (worker runs `/sc:pr-submit`) | DOC | `docs/designs/orchestrator.md` D:135 (in the unified rewrite) | With D06's design rewrite |
| Leave `/sc:pr-submit` and its fence unchanged | PR KEEP | `src/superclaude/skills/sc-pr-submit-protocol/` | None |
| Build the run-go record and the end-of-go checks | LOCAL CHANGE (later build) | new coordinator code (merge path unit, spec S14) | After the DOC and contract rows |

## Implications

- **Watcher.** No change. The poll writes nothing to GitHub and pushes nothing.
- **Coordinator or orchestrator.** It still shows worker commits to the person and pushes only on a typed go (WC:245, FR-32). It never types the run line itself. The run line is typed by the person in a person-opened session.
- **Claim pipeline.** Full Submit (R25) stays the only automated route to a push and PR. It needs the owner's chat approval and the WC:245 amendment before it counts, and its go ends with its run.
- **Dashboard and sweep.** A PR waiting for a new go after a rebase or revert, and a run whose go ended, are facts the observer can show; nothing is decided for the dashboard.
- **What breaks.** Any spec text that says "every push" without the exception; R25's "nothing else is pushed" as written; Clay's ADD1 worker route. The fix-round pushes made today by `/sc:pr-submit --monitor 3` are not a new risk, they were always the run line's.
- **What the owner must know.** The run go is only as strong as "a person typed it": a script in the same terminal can type the line (D06 INV-003, residual risk). The end-of-go checks and the record are design only, not built. A Full Submit field set days earlier is a pre-authorization in the plain sense, so the amendment has to name it as an exception and not call it live.

## Confidence

About 80 percent on the rule, because both advocates reached the same hybrid on the central points and the sources (WC:245, `SKILL.md:262, 342-348`) agree with it. It would change if the owner wants a typed go for each fix-round push despite the cost (that is a decision, and the rule would then say `--monitor 2` is the ceiling), or if `push_range_mismatch` and the fast-forward-only fence are found not to work as the protocol text says (they were read from the text, not run), or if the owner rules that a Full Submit field cannot be a pre-authorization at all.

## Unverified

- That `push_range_mismatch`, `push_parent_ok` and the fast-forward-only push behave as `SKILL.md` and `pr-submit.md` describe (read from the text; not run).
- That R25 is "built": it is a row of an unpushed local plan (`claim-handoff-planb`); the owner has not approved the WC:245 amendment (D06 verdict action).
- The PR 368 incident (memory note, 15 days old, not re-verified).
- Whether a Full Submit launch really runs `/sc:pr-submit` in an ordinary top-level session rather than as a worker (A-003; D04, D06 assume it; the live guard probe row at SPEC:699 is the test).
- Whether the harness can tell typed text from script-typed text (D06 INV-003).
- Whether WC:245 strictly applies to the tool's own fix commits (the advocates split on A-004; the drafting answer is the same: say so in the amendment).
- Whether another actor's push of the feature branch between rounds is stopped by the tool's guard (A-005; the advocates split).
- Scores were estimated by hand; the second scoring pass was run by the same evaluator, and the two advocates are same-family agents under the weighting rule, which shapes their agreement.
- Quick depth skipped Round 2, the invariant probe and Round 3, so no fault-finder checked the consensus.

## Debate artifacts

- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/Q04/position-OURS.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/Q04/position-CLAY.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/Q04/adversarial/merged-output.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/Q04/adversarial/return-contract.yaml`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/Q04/adversarial/adversarial/return-contract.yaml`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/Q04/adversarial/adversarial/diff-analysis.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/Q04/adversarial/adversarial/debate-transcript.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/Q04/adversarial/adversarial/base-selection.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/Q04/adversarial/adversarial/refactor-plan.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/Q04/adversarial/adversarial/merge-log.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/Q04/adversarial/adversarial/variant-1-original.md` and `variant-2-original.md` (same folder)
- Skill status: the adversarial skill ran at depth quick with two real advocate agents and a merge-executor agent; its own status is partial (two unresolved points, same-evaluator second scoring pass).
