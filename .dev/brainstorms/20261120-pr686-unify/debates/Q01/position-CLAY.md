# Position CLAY (Q01): who writes a per-issue grant row

Abbreviations: "master" = `/home/coder/.cache/ic-snap-20261120/master`; "D:nnn" = `docs/designs/orchestrator.md` line nnn in master (Clay's design from PR 681, the design document); "pr-a" = `/home/coder/.cache/ic-snap-20261120/pr-a` (Clay's PR 686 head, the poll rewrite).

## Claim

No grant is a row that any person writes, and no per-issue row exists. Low-stakes writes sit on a standing `grants` list. Everything that needs a person's word (change the list, release a merge, tag a release, clear a hold) is a typed answer in the orchestrator's own terminal, checked by a script (`answer-check`) before anything is acted on. Nobody writes a file; the script refuses answers that are relayed, stale, for another entry or for another question.

## Mechanism

1. Standing list: `grants: [issue.assign, issue.comment, issue.body.append_plan_sections, issue.hold, pr.merge, issue.close]` in `repos.yaml` (D:291, D:872; DQ6 at D:116).
2. `superclaude orchestrator` refuses with `E-NO-GRANT` any GitHub write made through its own verbs that is not on the list, and logs the grant used (D:696).
3. A change to `grants`, `reach_daily_max` or `merge_safety_files` passes only with `--answer-ref` of an `answer-check` that accepted the answer (D:688).
4. `answer-check --entry <id> --source <session|clickup-dm> --answered-at <UTC> [--question-key <key>]` passes only if (1) the source is the person's own typed input in the orchestrator's terminal or a ClickUp reply from their id, never another agent, (2) it names the right entry, (3) it is newer than the entry's last edit (D:694). The merge-safety key is `merge_safety:<PR>:<head sha>` (D:598).

## Cited facts

1. D:116 (DQ6): the missing-plan agent's write grant is "a standing grant, the `grants` list of `repos.yaml`"; the design says the old per-issue grant row retires (H-design681-map.md, row "2 DQ6", in `/home/coder/workspaces/IronClaude/.dev/analyze/pr686-20261120/`).
2. D:688 and D:694: `repos` verbs refuse to change `grants` without an accepted answer; `answer-check` rejects relayed answers, wrong entries, stale answers.
3. D:696: `E-NO-GRANT` refusal plus a log of each use.
4. `src/superclaude/cli/issue_watch/repos.py:295` in pr-a reads a missing `grants` key as an empty list (fail closed), as recorded in the D04 verdict.
5. PR 682 (Clay's deletion of the issue-pipeline package, merged 2026-11-20 00:02 UTC, commit `01e7a9e23`) removed the per-issue grant-row machinery (`src/superclaude/cli/issue_pipeline/`, rule WC-17 and old contract line 300), so master has no per-issue row writer or checker (E-pr682.md in the same analysis folder).
6. The owner's rule of 2026-11-17 (memory `approvals-through-chat-never-files`) forbids asking the owner to write a record; D:694 is built for exactly an answer given in a terminal.
7. The merged text of the contract (`WORKER-CONTRACT.md:57`, master) still says a grant row is "written by the owner"; Clay's design has no such step, so it cannot trap an owner into writing one.
8. D13 verdict (owner chat go for `--apply` and for the cleanup design) and D04 verdict (per-PR chat go for merge and close) both need an accepted-answer check that the old row design lacked.

## What it costs

- `answer-check`, `E-NO-GRANT` and the `repos` verbs are all PR B and are not built (the design's own PR B file list, D:1020). Until then there is no check at all.
- A standing `pr.merge` and `issue.close` removes a person from every merge and close. D04 rejected that part (contract lines 241 and 245).

## What it risks

- D:694 names Clay as the source of an accepted answer (Clay's terminal or Clay's ClickUp id, per the D04 verdict). It is hardwired to the wrong person for this repository (D04 verdict, "parameterise the owner identity").
- `E-NO-GRANT` covers only the orchestrator's own verbs. Assignment and claim comments come from `/sc:issue`, `pr.merge` is a raw `gh pr merge` and `issue.close` comes from `/sc:closeout` (D04 verdict item 6), so the refusal covers at most two of the six entries.
- The "source is the person" test cannot tell the owner from another session on the same host: any agent with the Orca CLI can type into a terminal (design unknown U37, D:1295, accepted as a v1 risk).
- Master's `grants` file lies inside the orchestrator's own write reach, guarded only by a verb and a test (D:688).

## What it gets right

- It is the only design with a check on a typed chat answer. Today a row an agent writes from chat has none.
- It fits the owner's chat-only rule better than an owner-written row: the person types once, in chat, and nothing is hand-written.
- Fail closed on a missing list; every grant use is logged.

