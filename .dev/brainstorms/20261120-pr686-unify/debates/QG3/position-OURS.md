# Position OURS (QG3): authority and config, OD-6, OD-10, OD-11, OD-12

Terms: D:nnn is a line of `docs/designs/orchestrator.md` in the master snapshot `/home/coder/.cache/ic-snap-20261120/master` (Clay's merged design, PR 681). pr-a is Clay's open PR 686 (rewrite of the watcher) head in `/home/coder/.cache/ic-snap-20261120/pr-a`. D04, D06, D13, D15, Q01 are the earlier verdicts under `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/`.

## Claim (one line per sub-question)
- **OD-6:** Yes. The coordinator never tags or publishes a release. N6 is an unconditional refusal with no `--answer-ref` pass path.
- **OD-10:** A person's per-PR go, bound to the head sha, covers the merge and the post-merge close of that PR's issue. No standing `issue.close`. A `Fixes` line still closes at merge.
- **OD-11:** A fresh install has an empty `grants` list. The owner says once in chat which of the three standing entries to grant and the agent records it.
- **OD-12:** Both layers: the per-repo config sits outside the coordinator's write reach (or behind a hook) and the controls fail closed on values that weaken them.

## Mechanism
- Release is the one action row 5 of Clay's own table calls "something that cannot be undone" (D:676). The control that cannot be spoofed is to give the coordinator no path to it. Merge is different: a merge has a head-pinned command (`gh pr merge --match-head-commit`, D:118) and a go bound to `merge_safety:<PR>:<head sha>` (D:598, D:694).
- Close follows the merge of the same PR, so one recorded go that names both actions needs no second approval and no standing authority. Q01 item 5 says a go ends when the named action is done, so the go record must name the close, or the close has no go.
- The standing list is the owner's consent to a write. No record is not a default consent. Fail closed (Q01 item 6) means no recorded grant, no write.
- The per-repo config holds the keys that decide whether the merge gate holds (`merge_safety_files`, `reviewers`, `grants`, `reach_daily_max`). The coordinator can edit its own file with a plain shell write, and `refuse(argv)` sees only commands the verbs run (D:769, K22, U42 open). So the file needs a second line of defence: values that fail closed.

## Cited facts
1. Clay's design lists "publishing or tagging a release" under "something that cannot be undone" (D:676, row 5), and its own N6 lets the coordinator tag with a recorded OK (D:751, D:763). The check the design relies on is `answer-check` (D:694), which cannot tell a person from a script (D15 wording rule, INV-015) and hardwires Clay's terminal and ClickUp id (D:694).
2. The design's own open item U57 says words typed into the issue "cannot be told from the orchestrator's own text because there is one login", so the proof of a "recorded OK" for a release is unverified in Clay's own register (D:1315).
3. No workflow in master tags or publishes: a search of `/home/coder/.cache/ic-snap-20261120/master/.github/workflows` for `gh release create`, `git tag` and `tags:` found only a `workflow_dispatch` trigger in `test.yml:8`. A release is a person's act today, and N6 with a pass path would give the coordinator a new irreversible capability.
4. Master `WORKER-CONTRACT.md:241` says the coordinator performs every git and GitHub outward action "only when the user's instruction names that action". A standing `pr.merge` or `issue.close` contradicts it, and the D04 and D06 verdicts reject both as standing grants.
5. `E-NO-GRANT` refuses a GitHub write "that the orchestrator makes through its own verbs" (D:696). `/sc:closeout` writes the close through `scripts/settle.sh` (`/home/coder/.cache/ic-snap-20261120/master/src/superclaude/skills/sc-closeout-protocol/SKILL.md:51`), a path the verbs do not see (my inference from D:696 and SKILL.md:51). So a standing `issue.close` entry would be a permission, not a mechanical control.
6. Closeout closes only after a `done` verdict and a checked merge (`SKILL.md:20`; STOP `E-NOT-MERGED` at line 82), so tying the close to the merge go loses nothing: the skill that proves the merge proves the close is due.
7. PR 686's parser reads a missing `grants` key as an empty list (`/home/coder/.cache/ic-snap-20261120/pr-a/src/superclaude/cli/issue_watch/repos.py:295-299`). Clay's own code is fail closed on `grants`; the six standing entries appear in a design example (D:116, D:291), not as the parser default.
8. The parser accepts the weakening values: `merge_safety_files: []` is "valid: no hold" (`repos.py:243`, `:247-252`), `reviewers: "none"` returns an empty tuple (`repos.py:230-231`), and a bad `reach_daily_max` is read as 0, meaning no cap (`repos.py:262-269`). Clay says the file is "inside" the orchestrator's reach and guarded "by the verb and by a test" (D:688). No hook in master mentions the poll config (a search of `src/superclaude/hooks` for `issue-watch` found nothing).
9. The owner's rule of 2026-11-17 (memory `approvals-through-chat-never-files`) and Q01 settle who records a grant: the owner says it in chat, the agent records it. D15 R-4 and Q01 items 1, 6, 7 give the empty default.

## What it costs
- OD-6: a release stays a human step. Release PRs can still be merged on a person's go (D:763 "Merging a release pull request is allowed"; D:118 `release_merge_method`).
- OD-10: one go must name two actions, and a restart between merge and closeout must read the go record. Cost: a slightly longer go sentence.
- OD-11: one extra chat message on a new host. Until it is said, the plan call's body write and the assign and comment writes are refused.
- OD-12: a hook or a set of fail-closed checks is real work (nothing exists today), and a hook cannot see a Bash-written file (D:769, U42).

## What it risks
- A hook that blocks `Write` and `Edit` on the config path does not stop `sed -i` or a Python write in the coordinator's shell. "Out of reach" must be worded "narrows".
- Fail-closed rules on `merge_safety_files: []` also block a repo whose owner really wants no hold. They need an owner-recorded value to count as deliberate.
- An empty default on a host where the owner never says the one chat message works in a degraded way; the refusal must say why or it looks like a bug.

## What it gets right
- Each irreversible action sits behind a person's typed words, and no standing authority goes to the one party that could be wrong without noticing (D04, D06).
- It never relies on a check that cannot tell a person from a script as the only brake on a release.
- It keeps Clay's useful pieces: the head-pinned merge, the question key, the log of each grant used and the `grants` fail-closed reading.

