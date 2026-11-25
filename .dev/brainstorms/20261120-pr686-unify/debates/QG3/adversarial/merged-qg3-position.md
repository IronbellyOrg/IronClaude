<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 1 (OURS, QG3 position paper) -->
<!-- Merge date: 2026-11-20T09:10:21Z -->

# Position OURS (QG3): authority and config, OD-6, OD-10, OD-11, OD-12

<!-- Source: Base (original) -->
Terms: D:nnn is a line of `docs/designs/orchestrator.md` in the master snapshot `/home/coder/.cache/ic-snap-20261120/master` (Clay's merged design, PR 681). pr-a is Clay's open PR 686 (rewrite of the watcher) head in `/home/coder/.cache/ic-snap-20261120/pr-a`. D04, D06, D13, D15, Q01 are the earlier verdicts under `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/`.

## Claim (one line per sub-question)
<!-- Source: Base (original, modified) - OD-6 appended per Change #3 (argv list and tests from Variant 2, Cited fact 1, D:763) -->
- **OD-6:** Yes. The coordinator never tags or publishes a release. N6 is an unconditional refusal with no `--answer-ref` pass path. N6 refuses `git tag`, `git push --tags`, `git push origin <tag>`, `gh release create`, `gh release edit`, `gh release delete`, `uv publish`, `twine upload` and `npm publish`, with one denylist test per argv and a test that an `--answer-ref` does not change the result (D:763). Merging a release pull request stays allowed on the per-PR go (D:763, D:118). UNVERIFIED: the entries `git push --tags`, `gh release edit` and `gh release delete` come from the refactor plan, not from Variant 2's text, and were not checked against D:763.
<!-- Source: Base (original, modified) - OD-10 appended per Change #2 (go names the close, from Variant 2) -->
- **OD-10:** A person's per-PR go, bound to the head sha, covers the merge and the post-merge close of that PR's issue. No standing `issue.close`. A `Fixes` line still closes at merge. The go reads "merge PR N at sha X, then close issue M if closeout's verdict is done" and ends when both are done, the head moves, or the owner revokes it in chat.
<!-- Source: Base (original, modified) - OD-11 appended per Change #4 (refusal text and first-run listing, from Variant 2 and the refactor plan) -->
- **OD-11:** A fresh install has an empty `grants` list. The owner says once in chat which of the three standing entries to grant and the agent records it. The `E-NO-GRANT` refusal names the missing entry and the sentence the owner can say in chat, and the first run lists the three standing entries (`issue.assign`, `issue.comment`, `issue.body.append_plan_sections`, as named from D15 in the refactor plan) once, so one chat answer grants them. The agent records that answer with its quoted words, date, scope and recorder (Q01 item 3).
<!-- Source: Base (original, modified) - OD-12 restructured per Change #1 (layer 1 reworded "narrows", verb refusal named, from Variant 2 Claim OD-12, D:688) -->
- **OD-12:** Both layers, and both only narrow the gap. Layer 1: the `repos` verbs refuse to write `reach_daily_max`, `grants`, `merge_safety_files` and `reviewers` without an accepted answer record (D:688, D:758, D:765), with a protective hook on Write and Edit of the config path. Layer 2: the controls fail closed on values that weaken them (`merge_safety_files: []`, `reviewers: none`, a bad `reach_daily_max`) unless an accepted answer record names the value. `reviewers` is added to the guarded keys as a recommendation of the refactor plan; D:688 guards the other three keys only.

## Mechanism
<!-- Source: Base (original) -->
- Release is the one action row 5 of Clay's own table calls "something that cannot be undone" (D:676). The control that cannot be spoofed is to give the coordinator no path to it. Merge is different: a merge has a head-pinned command (`gh pr merge --match-head-commit`, D:118) and a go bound to `merge_safety:<PR>:<head sha>` (D:598, D:694).
<!-- Source: Base (original, modified) - appended per Change #2; the reopen guard (SKILL.md:114) and D:799 (f) come from Variant 2 -->
- Close follows the merge of the same PR, so one recorded go that names both actions needs no second approval and no standing authority. Q01 item 5 says a go ends when the named action is done, so the go record must name the close, or the close has no go. The go ends when both actions are done, the head moves, or the owner revokes it in chat. Reversibility lowers the cost of naming the close: closeout never closes an issue a person reopened after its note (`/home/coder/.cache/ic-snap-20261120/master/src/superclaude/skills/sc-closeout-protocol/SKILL.md:114`). Reversibility is not offered as a reason for a standing close: a reopen needs a person to notice, and the `done` verdict is a model decision (`SKILL.md:20`). Clay's design names `issue.close` as the grant under which closeout's close writes fall (D:799 (f)); the per-PR go is the authorization record used here in its place, because `E-NO-GRANT` does not bind closeout's write (fact 5).
<!-- Source: Base (original) -->
- The standing list is the owner's consent to a write. No record is not a default consent. Fail closed (Q01 item 6) means no recorded grant, no write.
<!-- Source: Base (original, modified) - restructured per Change #1; the verb refusal and its tests (D:688, D:758, D:765) come from Variant 2, Mechanism bullet 4 and Cited fact 6 -->
- The per-repo config holds the keys that decide whether the merge gate holds (`merge_safety_files`, `reviewers`, `grants`, `reach_daily_max`). The coordinator can edit its own file with a plain shell write, and `refuse(argv)` sees only commands the verbs run (D:769, K22, U42 open). So the file needs two lines of defence, and neither closes the gap.
  - Layer 1 narrows who writes the file through the tool path: the `repos` verbs refuse the guarded keys without an accepted answer record, and tests pin the refusal (N1 and N8 rows, D:758, D:765). A hook on Write and Edit adds to it. Neither sees a Bash-written file (D:769, U42).
  - Layer 2 is values that fail closed: `merge_safety_files: []`, `reviewers: none` and a bad `reach_daily_max` read as a refusal, not as "no hold", "no reviewer" or "no cap", unless an accepted answer record names the value.

## Cited facts
<!-- Source: Base (original) -->
1. Clay's design lists "publishing or tagging a release" under "something that cannot be undone" (D:676, row 5), and its own N6 lets the coordinator tag with a recorded OK (D:751, D:763). The check the design relies on is `answer-check` (D:694), which cannot tell a person from a script (D15 wording rule, INV-015) and hardwires Clay's terminal and ClickUp id (D:694).
2. The design's own open item U57 says words typed into the issue "cannot be told from the orchestrator's own text because there is one login", so the proof of a "recorded OK" for a release is unverified in Clay's own register (D:1315).
3. No workflow in master tags or publishes: a search of `/home/coder/.cache/ic-snap-20261120/master/.github/workflows` for `gh release create`, `git tag` and `tags:` found only a `workflow_dispatch` trigger in `test.yml:8`. A release is a person's act today, and N6 with a pass path would give the coordinator a new irreversible capability.
4. Master `WORKER-CONTRACT.md:241` says the coordinator performs every git and GitHub outward action "only when the user's instruction names that action". A standing `pr.merge` or `issue.close` contradicts it, and the D04 and D06 verdicts reject both as standing grants.
5. `E-NO-GRANT` refuses a GitHub write "that the orchestrator makes through its own verbs" (D:696). `/sc:closeout` writes the close through `scripts/settle.sh` (`/home/coder/.cache/ic-snap-20261120/master/src/superclaude/skills/sc-closeout-protocol/SKILL.md:51`), a path the verbs do not see (my inference from D:696 and SKILL.md:51). So a standing `issue.close` entry would be a permission, not a mechanical control.
6. Closeout closes only after a `done` verdict and a checked merge (`SKILL.md:20`; STOP `E-NOT-MERGED` at line 82), so tying the close to the merge go loses nothing: the skill that proves the merge proves the close is due.
7. PR 686's parser reads a missing `grants` key as an empty list (`/home/coder/.cache/ic-snap-20261120/pr-a/src/superclaude/cli/issue_watch/repos.py:295-299`). Clay's own code is fail closed on `grants`; the six standing entries appear in a design example (D:116, D:291), not as the parser default.
8. The parser accepts the weakening values: `merge_safety_files: []` is "valid: no hold" (`repos.py:243`, `:247-252`), `reviewers: "none"` returns an empty tuple (`repos.py:230-231`), and a bad `reach_daily_max` is read as 0, meaning no cap (`repos.py:262-269`). Clay says the file is "inside" the orchestrator's reach and guarded "by the verb and by a test" (D:688). No hook in master mentions the poll config (a search of `src/superclaude/hooks` for `issue-watch` found nothing).
9. The owner's rule of 2026-11-17 (memory `approvals-through-chat-never-files`) and Q01 settle who records a grant: the owner says it in chat, the agent records it. D15 R-4 and Q01 items 1, 6, 7 give the empty default.
<!-- Source: Variant 2 (CLAY), Cited fact 7 - merged per Change #1; shape checks kept so the gap is stated as weakening values of the right shape (debate point C-008) -->
10. The same parser checks shape strictly: `reviewers` must be `none` or a non-empty list of `augment` and `codex` with no repeats (`repos.py:227-239`), `merge_safety_files` must be a list of non-empty strings and a null is invalid (finding F45 of issue 675, `repos.py:242-252`), `max_in_flight` is checked to 1 to 10 (`repos.py:255-259`), and a `grants` value that is not a list of strings is rejected (`repos.py:295-299`). The gap in fact 8 is values of the right shape that weaken a control, not malformed values.

## What it costs
<!-- Source: Base (original) -->
- OD-6: a release stays a human step. Release PRs can still be merged on a person's go (D:763 "Merging a release pull request is allowed"; D:118 `release_merge_method`).
- OD-10: one go must name two actions, and a restart between merge and closeout must read the go record. Cost: a slightly longer go sentence.
<!-- Source: Base (original, modified) - appended per Change #4; the zero-setup point is from Variant 2, What it gets right bullet 4 -->
- OD-11: one extra chat message on a new host. Until it is said, the plan call's body write and the assign and comment writes are refused. The refusal text and the first-run listing of the three entries have to be built (whether `E-NO-GRANT` already names the missing entry: UNVERIFIED). A standing list would work at once and sit in one visible place (D:291); the first-run listing gives the same visibility without a standing authority. Variant 2 counts a fresh install that works at once as the owner's zero-setup aim, citing memory `zero-setup-watcher-decisions` that its advocate could not read (UNVERIFIED), "unless the one chat message is counted as setup".
<!-- Source: Base (original, modified) - reworded per Change #1 -->
- OD-12: a hook, the verb refusals and a set of fail-closed checks are real work. The hook and the fail-closed checks do not exist today; whether the `repos` verb refusal and its tests (D:688, D:758, D:765) are built in pr-a is UNVERIFIED. The verb refusal and the hook cannot see a Bash-written file (D:769, U42).

## What it risks
<!-- Source: Base (original, modified) - reworded per Change #1; the shell-write gap of the verb path is from Variant 2, What it costs bullet OD-12 -->
- A hook that blocks `Write` and `Edit` on the config path does not stop `sed -i` or a Python write in the coordinator's shell, and the `repos` verb refusal does not see a direct edit either (D:688 names the gap). Layer 1 must be worded "narrows", never "out of reach".
<!-- Source: Base (original) -->
- Fail-closed rules on `merge_safety_files: []` also block a repo whose owner really wants no hold. They need an owner-recorded value to count as deliberate.
<!-- Source: Base (original, modified) - mitigation added per Change #4 -->
- An empty default on a host where the owner never says the one chat message works in a degraded way; the refusal names the missing entry and the sentence to say, or it looks like a bug.
<!-- Source: Refactor plan, Risk Summary row for Change #3 -->
- The N6 argv list can be incomplete: a publish route that is not on the list passes `refuse(argv)`. The fix is to add the entry and its denylist test.

## Conditions and limits
<!-- Source: Refactor plan Change #5 (diff-analysis.md A-001 and A-002, both UNSTATED in both papers; both advocates answered in Round 1 of debate-transcript.md) -->
- **A-001, the controls are design text, not built code.** Both advocates QUALIFY this. It weighs more against Clay's release path, whose pass needs `answer-check`, than against the unconditional refusal of N6, which needs no new verb (debate-transcript.md, Round 1). The verb refusals, the hook, the fail-closed checks and the refusal text are all work to build.
- **A-002, the config is writable by the coordinator's shell.** Both advocates ACCEPT this: the coordinator runs as the same OS user, and Clay says the file is "inside" the orchestrator's reach (D:688). A file cannot be put out of that reach, so layer 1 only narrows and the value checks of layer 2 carry the weight.
- **Wording rule:** every control narrows and never closes. For the config (OD-12) no sentence of this paper says a hook, a verb refusal or a value check prevents a write to the file. Whether N6's argv refusal sees a tag run outside the verbs is not settled here, because `refuse(argv)` sees only commands the verbs run (D:769): UNVERIFIED.
- **Accepted answer record:** layers 1 and 2 both rest on an accepted answer record. Whether the verbs' `--answer-ref` check (D:688, D:694) can tell the owner's chat words from a session's is open in Clay's register (U57, D:1315). UNVERIFIED: that the record fields of Q01 item 3 (quoted words, date, scope, recorder) close that gap. This paper does not claim they do.

## What it gets right
<!-- Source: Base (original) -->
- Each irreversible action sits behind a person's typed words, and no standing authority goes to the one party that could be wrong without noticing (D04, D06).
- It never relies on a check that cannot tell a person from a script as the only brake on a release.
<!-- Source: Base (original, modified) - list extended per Changes #1, #2 and #3 -->
- It keeps Clay's useful pieces: the head-pinned merge, the question key, the log of each grant used, the `grants` fail-closed reading, the `repos` verb refusal and its tests, the reopen guard of closeout and the enumerated N6 argv list with one test per entry.

## Result of the debate
<!-- Source: Refactor plan Change #6 (debate-transcript.md Scoring Matrix; the "Not adopted" column carries Variant 2 positions and citations as recorded in the refactor plan and Variant 2) -->
Confidence is the debate's score for the diff point named in the second column, an estimate and not a measurement. Quick depth: one round, 17 diff points, 88.2 percent aligned; the invariant probe was not run (debate-transcript.md).

| Sub-question | Winner (diff point) | Confidence | Answer | Adopted from CLAY | Not adopted from CLAY |
|---|---|---|---|---|---|
| OD-6 | OURS (C-001) | 89% | A release stays a person's act; N6 is an unconditional refusal | The enumerated argv list with one refusal test per entry (D:763) | N6 pass with an `--answer-ref` (D:751, D:763); the recorded OK rests on `answer-check`, open as U57 (D:1315), while row 5 sends release to a person (D:676) |
| OD-10 | OURS (C-002); C-006 resolved as HYBRID | 77%; C-006 61% | One per-PR go, bound to the head sha, names the merge and the close; no standing `issue.close` | The reopen guard (`SKILL.md:114`) as the reason the go may name the close | Standing `issue.close` (R10 at D:82, ruling 13 at D:682, D:799 (f)); `E-NO-GRANT` does not bind closeout (D:696, `SKILL.md:51`) |
| OD-11 | OURS (C-003) | 71% | Empty `grants` on a fresh install; the owner grants the three entries once in chat | The refusal text names the missing grant (D:116 gives the "no person at each step" reason for a standing list) | Six standing entries at install (D:291, D:866); a fresh install holding `pr.merge` is a standing merge on `protected: false` (D:117) |
| OD-12 | HYBRID (C-004); X-003 resolved as HYBRID | 69%; X-003 58% | Two layers that narrow: verb refusal plus hook, and fail-closed values | The `repos` verb refusal with its tests (D:688, D:758, D:765); the strict parser shape checks (`repos.py:227-259`) | Guard "by the verb and by a test" alone (D:688): it leaves `merge_safety_files: []`, `reviewers: none` and a shell write open |

Points that stay open: C-006 (OURS 62 against HYBRID 60 by the two advocates) and X-003 (CLAY 55 by the OURS advocate against HYBRID 60), both compatible with the HYBRID wording used above. Base selection: Variant 1 scored 0.857 against 0.822 for Variant 2, a margin of 3.5 points, below the 5 percent threshold, so the debate tiebreaker applied (base-selection.md; one evaluator scored both variants, so the scores are estimates).
