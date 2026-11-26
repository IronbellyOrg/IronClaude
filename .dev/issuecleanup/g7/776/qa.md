VERDICT: PASS

## Blocking defects

None.

## What I checked (all against the worktree HEAD and the live issue)

- Live issue 776: OPEN, label `enhancement`, created 2026-11-24T18:29:53Z, 0 comments. Matches findings.md. `gh pr list --search 776 --state all` returns none, so there is no closing PR.
- worker-brief.txt:12 is the `Plan approval: ... follow rule WC-17` line, in the shared head.
- brief.py:19 is `STAGES = ("research", "spec", "plan", "debug")`.
- stage_predicates.py:45 is `STAGE = "plan"`. The key `(issue, STAGE, marker.plan_hash)` is at :294.
- cli.py command decorators are at the cited lines: plan-hash 62, check-approval 77, init 97, adopt-create 109, adopt-mark 118, record-create 135, record-show 162, record-mark 180, release-worker 201, complete 226, stage-status 409. There is no `approve` verb.
- tests/issue_pipeline/test_brief.py:279 is `test_brief_points_at_the_plan_approval_rule_of_the_contract`, and it loops over every stage row.
- WORKER-CONTRACT.md:57 is the owner-says-in-chat text (Ruling halt). :59 is WC-17. :300 is the coordinator Plan approval duty.
- No skill with "approv" in its name on HEAD or on origin/master (ls and git ls-tree). The only `approve`-like code is `cycle.py::_approve`, which only reads the approval. The `Approved` field is only read (`predicates.py`, `github.py`, `repo_init.py`). Nothing sets the claim approval.
- Issue states: #698, #722, #727, #716, #733, #761 and #571 are all OPEN. PR #707 is MERGED at 2026-11-20T22:09:24Z.
- origin/master is f2894fc44. Only afb3ccf29 touched the watched paths, and only under `skills/sc-swarm-wizard-protocol/refs`. Nothing changed in `issue_pipeline` or `WORKER-CONTRACT.md`.
- Headings are exactly Verdict, Complexity and size, Priority, Concrete next steps, Dependencies, Related issues, Related PRs, in that order. No template placeholders.
- The verdict (still-relevant), complexity and size (medium, M), priority (P2), the five next steps and the dependencies (owner answers, #722 for claim approval) follow from this evidence. The findings leave the two things I could not check marked UNVERIFIED, which is correct.

## Notes (non-blocking)

1. The `docs/designs/issue-watcher-status-pipelines.md:5` citation supports "the approval is the `Approved` field set to Yes" only loosely. It is a design note, not code. The code claim itself holds.
2. SEC-08 / the draft SPEC.md is not on this checkout (`.dev/brainstorms/20261120-pr686-unify/spec/SPEC.md` is absent). findings.md correctly labels it UNVERIFIED. I did not check the other branch.
3. The `claim.md` line numbers (55 to 92) were not re-read. findings.md already marks them approximate, and they are quoted from the issue.
4. The "Lookup matches" issues (#379, #699, and so on) were not re-checked. They are listed only as unconfirmed matches.
