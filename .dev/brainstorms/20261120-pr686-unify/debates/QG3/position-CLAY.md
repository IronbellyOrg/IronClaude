# Position CLAY (QG3): authority and config, OD-6, OD-10, OD-11, OD-12

Terms: D:nnn is a line of `docs/designs/orchestrator.md` in `/home/coder/.cache/ic-snap-20261120/master` (Clay's merged design, PR 681). pr-a is Clay's open PR 686 (rewrite of the watcher) head in `/home/coder/.cache/ic-snap-20261120/pr-a`. Rulings are the numbered rulings in the design.

## Claim (one line per sub-question)
- **OD-6 (No):** The coordinator may tag and publish a release when a recorded human OK exists: N6 passes with the `--answer-ref` of a passed `answer-check` (D:751, D:763).
- **OD-10 (standing close):** Closing the issue after a merge is the orchestrator's own work and belongs in the standing `grants` list (`issue.close`), because merging and closing are "off the human-only list" (R10, D:82; ruling 13, D:682).
- **OD-11 (standing entries at install):** A fresh install should work at once with the standing entries listed, because "there is no person at each step" of the plan agent's writes (D:116).
- **OD-12 (guard by verb and test):** The per-repo file may live where the orchestrator edits it, guarded by the `repos` verbs refusing the three sensitive keys without an accepted `--answer-ref`, and by a test (D:688).

## Mechanism
- Every action is either on the closed "may do" list with a tested refusal pattern or refused (`refuse(argv)`, D:736 to D:765). Release is on the list only with a recorded OK, so the coordinator can finish a release flow when the person has said yes once in a form `answer-check` accepts (D:694: typed in the orchestrator's own terminal, or a ClickUp DM reply from Clay's own user id).
- The grants list is a standing permission Clay sets (N1, D:758: "`grants` is a standing permission that Clay sets; it is not a grant the orchestrator remembers"). `E-NO-GRANT` refuses a verb's GitHub write that is not in the list and logs the grant used (D:696).
- A merge is pinned to the head sha, so it needs no per-action grant to be safe; the close that follows is bounded by the closeout skill's `done` verdict and merge check.
- The `repos` verbs refuse to write `reach_daily_max`, `grants` and `merge_safety_files` without an accepted answer (D:688), so the file stays editable by the coordinator for the other keys.

## Cited facts
1. N6 is a tested refusal, not a free pass: no `git tag`, `git push origin <tag>`, `gh release create`, `uv publish`, `twine upload` or `npm publish` unless the call carries the `--answer-ref` of an `answer-check` that passed for that release, and the argv denylist test checks both the refusal and the pass (D:763).
2. Row 5 of the escalation table already sends "publishing or tagging a release" to the person (D:676), so Clay's design treats release as person-gated; N6 only lets the coordinator act after that gate. Per-repo `release_merge_method` exists because a squash merge of release 6.1.0 (#658) was reverted by #662 (D:118), so the design already models release PRs as a special case.
3. Ruling 13 puts merging and closing outside the human-only list: "Merging and closing issues are not in the table" (D:682; R10 at D:82). The coordinator closes through `/sc:closeout`, whose writes the design says "fall under its grants `issue.close` and `issue.comment`" (D:799 (f), DQ6 at D:116).
4. The reference config lists six standing entries: `issue.assign, issue.comment, issue.body.append_plan_sections, issue.hold, pr.merge, issue.close` (D:291). Clay's minimum first-use file is `repos.yaml` with `schema_version`, `orgs`, a `repos` list and `grants` (D:866).
5. The reason for a standing list is stated: "there is no person at each step", and "the old per-issue grant row came from the approval flow that this issue retires" (D:116).
6. The guard of the three keys is by verb: `reach_daily_max`, `grants` and `merge_safety_files` are changed only on Clay's recorded word and the verbs refuse without `--answer-ref` (D:688), with tests (N1 and N8 rows, D:758, D:765). The design says plainly that Jay keeps his file out of the agent's reach while "ours are inside it and are guarded by the verb and by a test" (D:688).
7. PR 686's parser validates strictly: `reviewers` must be `none` or a non-empty list of `augment` and `codex` with no repeats (`/home/coder/.cache/ic-snap-20261120/pr-a/src/superclaude/cli/issue_watch/repos.py:227-239`), `merge_safety_files` must be a list of non-empty strings and a null is invalid (finding F45 of issue 675, `repos.py:242-252`), `max_in_flight` is checked to 1 to 10 (`repos.py:255-259`) and `grants` that is not a list of strings is rejected (`repos.py:295-299`).
8. A missing `grants` key reads as empty (`repos.py:295`), so the six-entry default is a choice written in the example (D:291), and a host can set it once in the file.

## What it costs
- OD-6: `answer-check` has to be trusted for the most irreversible action (U57 open, D:1315).
- OD-10: a standing `issue.close` is a permission with no mechanical bind on closeout's own writes (they run through `settle.sh`).
- OD-11: a standing list gives writes without a fresh owner record.
- OD-12: the guard is only as strong as the verb path; a direct edit of the file by the coordinator's shell is not seen.

## What it risks
- `answer-check` cannot tell a person from a script (D:694; one login for the owner and every session on the host, D:1315 U57). A release OK could be produced by a session.
- A standing close lets the coordinator close an issue where a person would have said "leave it open" (the `done` verdict is a model's decision, `/home/coder/.cache/ic-snap-20261120/master/src/superclaude/skills/sc-closeout-protocol/SKILL.md:20`).
- A fresh install that already holds `pr.merge` is a standing merge on an unprotected `master` (`protected: false`, D:117).

## What it gets right
- It frees a person from every step that is bounded and reversible. A closed issue can be reopened by a person, and closeout never closes an issue a person reopened after its note (`SKILL.md:114`).
- It gives a release flow a path other than a hand-run `git tag`, which has no log or check at all today.
- It states the guard honestly as "the verb and a test" and names the gap (D:688), and the six-entry list is in one place (D:291), so there is one list to review.
- A fresh install that works at once fits the owner's zero-setup aim of "nothing manual" (memory `zero-setup-watcher-decisions`), unless the one chat message is counted as setup.

