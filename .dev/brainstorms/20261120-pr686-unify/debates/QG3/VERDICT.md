# Verdict QG3: Authority and config (OD-6, OD-10, OD-11, OD-12)

Terms. D:nnn is a line of `docs/designs/orchestrator.md` in the master snapshot `/home/coder/.cache/ic-snap-20261120/master` (Clay's merged design, PR 681, the merged design document). pr-a is Clay's open PR 686 (rewrite of the issue watcher) head, `/home/coder/.cache/ic-snap-20261120/pr-a`. D04, D06, D13, D15, Q01, Q03 are the earlier verdicts under `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/`. A "go" is the owner's typed approval in chat, which the agent records (Q01). "N6" is the design's rule about tagging or publishing a release (D:763). "`answer-check`" is the design's check of a typed answer (D:694). "Grants" is the per-repo list of GitHub writes the coordinator may make (D:116, D:696). "PB" is the unbuilt coordinator verb group that D15 calls PB.

## Question
QG3 Authority and config: OD-6 (coordinator never tags or publishes), OD-10 (authority for the post-merge issue close), OD-11 (default grants of a fresh install: empty, or the standing entries), OD-12 (protecting the per-repo config from the coordinator)

## Winner
HYBRID: the owner's line wins OD-6, OD-10 and OD-11 (both advocates conceded all three), and OD-12 is a hybrid in which Clay's verb refusal becomes one of the owner's two protection layers.

## Winning recommendation
The adversarial skill ran at depth quick: two advocates, one round, one merge-executor, 17 diff points, 88.2 percent aligned (threshold 80). The invariant probe did not run at this depth. Each line below is an answer, its reason and its source.

1. **OD-6: Yes. The coordinator never tags or publishes a release.** N6 is an unconditional refusal with no `--answer-ref` pass path. It refuses `git tag`, `git push --tags`, `git push origin <tag>`, `gh release create`, `gh release edit`, `gh release delete`, `uv publish`, `twine upload` and `npm publish`, with one denylist test per command and a test that an `--answer-ref` does not change the result. Merging a release pull request stays allowed on the per-PR go. Reason: Clay's own table calls release "something that cannot be undone" (D:676), and the pass path rests on `answer-check`, which cannot tell a person from a script and is open in Clay's own register as U57 (D:694, D:1315). Source: D:676, D:751, D:763, D:1315; confidence 89 percent.
2. **OD-10: One per-PR go, bound to the head sha, covers the merge and the close of that PR's issue; no standing `issue.close`.** The go is worded "merge PR N at sha X, then close issue M if closeout's verdict is done" and ends when both are done, the head moves, or the owner revokes it in chat. A `Fixes` line in the PR body still closes the issue at merge with no coordinator write. Reason: `E-NO-GRANT` covers only writes made through the orchestrator's own verbs (D:696) and closeout writes the close through `scripts/settle.sh` (`/home/coder/.cache/ic-snap-20261120/master/src/superclaude/skills/sc-closeout-protocol/SKILL.md:51`; my inference that the verbs do not see it), so a standing entry would be a permission and not a control; `WORKER-CONTRACT.md:241` allows an outward action "only when the user's instruction names that action". Source: D:696, D:799 (f), `WORKER-CONTRACT.md:241`, Q01 item 5, D04; confidence 77 percent.
3. **OD-11: A fresh install has an empty `grants` list; the owner grants the three standing entries once in chat and the agent records it.** The three are `issue.assign`, `issue.comment` and `issue.body.append_plan_sections` (D15 after Q03 removed `issue.hold`). The refusal text names the missing entry and the sentence the owner can say, and the first run lists the three entries once so one chat answer grants them. The record holds the owner's quoted words, the date, the scope and who recorded it (Q01 item 3). Reason: Clay's own parser reads a missing `grants` key as an empty list (`/home/coder/.cache/ic-snap-20261120/pr-a/src/superclaude/cli/issue_watch/repos.py:295-299`); the six-entry list is an example (D:116, D:291); a fresh install holding `pr.merge` is a standing merge on an unprotected `master` (D:117). Source: `repos.py:295-299`, D:116, D:291, Q01 items 3 and 6; confidence 71 percent.
4. **OD-12: Both layers, and both only narrow the gap.** Layer 1: the `repos` verbs refuse to write `reach_daily_max`, `grants`, `merge_safety_files` and `reviewers` without an accepted answer record, with tests, plus a hook on Write and Edit of the config path. Layer 2: the controls fail closed on values that weaken them (`merge_safety_files: []`, `reviewers: none`, a bad `reach_daily_max`) unless an accepted answer record names the value. Reason: the coordinator runs as the same OS user, so the file cannot be put out of its reach, and the parser accepts every weakening value today (`repos.py:230-231`, `:243`, `:247-252`, `:262-269`); Clay's design says the file is "inside" the orchestrator's reach and guarded "by the verb and by a test" (D:688). Source: D:688, D:758, D:765, `repos.py`; confidence 69 percent. Adding `reviewers` to the guarded keys is this debate's recommendation, not Clay's text (D:688 names three keys).

## Strongest points
**OURS**
1. A release has no undo, and the only brake Clay offers on it is the unproved `answer-check` (D:676, D:694, D:1315 U57). Both advocates agreed (OURS 89 to 90 percent).
2. A standing `pr.merge` or `issue.close` contradicts the contract line "only when the user's instruction names that action" (`/home/coder/.cache/ic-snap-20261120/master/src/superclaude/core/WORKER-CONTRACT.md:241`), and `E-NO-GRANT` does not see closeout's write (D:696; `SKILL.md:51`).
3. The parser accepts the weakening values with line numbers (`pr-a/.../repos.py:243`, `:230-231`, `:262-269`), and Clay's own parser defaults `grants` to empty (`repos.py:295`). Clay states the file is inside the orchestrator's reach (D:688).

**CLAY**
1. A named, tested mechanism for the three sensitive keys: the `repos` verbs refuse them without an accepted `--answer-ref` (D:688, D:758, D:765). The owner's "out of reach or a hook" had nothing named (CLAY advocate, accepted by the OURS advocate as a HYBRID).
2. Closing is reversible and closeout never closes an issue a person reopened after its note (`SKILL.md:114`, checked by both advocates), which lowers the cost of a go that names the close.
3. N6 as an enumerated list of commands with a test for each (D:763 last column), and the parser's shape checks (`repos.py:227-259`) already reject malformed values.

## Clay strengths to adopt
- **Enumerated N6 command list with one test per command (D:763).** Why: a closed, testable list is better than prose. How: adopt the list and the per-command tests, but make the refusal unconditional (no `--answer-ref` pass). Three entries (`git push --tags`, `gh release edit`, `gh release delete`) came from the refactor plan and were not individually checked against D:763 (UNVERIFIED).
- **The `repos` verb refusal of the sensitive keys (D:688, D:758, D:765).** Why: the only named, testable mechanism for protecting the file through the tool path. How: layer 1; add `reviewers` to the guarded keys; word it "narrows".
- **Strict parser shape checks (`repos.py:227-259`).** Why: they already reject malformed values, so the remaining gap is values of the right shape that weaken a control. How: keep the parser; add the fail-closed rule for weakening values.
- **The reopen guard (`SKILL.md:114`).** Why: a lower cost for naming the close in the go. How: the go says "close if closeout's verdict is done". Do not use reversibility as a reason for a standing close.
- **One visible place for the grant list (D:291).** Why: Clay's point that a standing list works at once and is reviewable. How: the first run prints the three entries once; no standing authority.

## Our strengths that must be kept
- Release is a person's act; no pass path (D:676, U57).
- No standing `pr.merge` or `issue.close`; a per-PR go bound to the head sha (D04, D06, Q01 item 5, `WORKER-CONTRACT.md:241`).
- Empty default `grants`; fail closed with no recorded go (Q01 item 6; `repos.py:295`).
- The owner's rule that approvals are given in chat and recorded by the agent, never written by the owner (memory `approvals-through-chat-never-files`; Q01).
- The "narrows, never closes" wording on every control (D15 section 1).

## Actions
| Action | Type | Target | Order or dependency |
|---|---|---|---|
| Owner says in chat: OD-6 yes (never tags or publishes); the agent records it | DECISION | Owner `ironbelly`; D15 section 7 OD-6 | First |
| Owner says in chat: the per-PR go covers the close (OD-10) and the go wording above | DECISION | Owner; D15 OD-10; closes C-INV-4 | First |
| Owner says in chat which of the three standing entries to grant on a host (OD-11); the agent records it with quoted words, date, scope, recorder | DECISION | Owner; D15 OD-11; Q01 item 3 | After the `repos` verb exists; first-run listing needs it |
| Owner says in chat: both protection layers (OD-12), including `reviewers` as a guarded key | DECISION | Owner; D15 OD-12; closes C-INV-3 | First |
| Rewrite the design rows that say the opposite: DQ6 and the six-entry `grants` example (D:116, D:291), 5.6 "closing the issue after the merge" (D:666), N6 (D:751, D:763), the three guarded keys (D:688) | DOC | `docs/designs/orchestrator.md` inside the unified spec (D14) | After the four chat answers |
| Build the N6 refusal as an unconditional, enumerated list with one test per command and a test that an `--answer-ref` changes nothing | LOCAL CHANGE | PB verb group, `refuse(argv)` (D15 row D8) | O4 (substrate) |
| Build the `repos` verb refusal, the answer record, the fail-closed value checks and the `E-NO-GRANT` refusal text that names the missing entry | LOCAL CHANGE | PB; per-repo config of planb (D14: PR 686's `repos.py` supplies key names only) | O5 |
| Remove `pr.merge`, `issue.close` and (Q03) `issue.hold` from the reference config and fixtures; refuse `pr.merge` and `issue.close` as grant names | PR KEEP-ADAPT | PR 686 `repos.py` key names and `tests/issue_watch/conftest.py` (D06, Q03 item 6) | With D14's adaptation, O3 |
| Decide and build the hook on Write and Edit of the config path (optional, narrows only) | LOCAL CHANGE | `src/superclaude/hooks/` | O5; owner choice |
| Change wave 8 so closeout runs only under a go that names the close | DOC | D:795 to D:799 (f) in the unified spec | With the design rewrite |

No PR is reverted or closed by this topic.

## Implications
- **OD-6 (release).** The coordinator never runs a tag or publish command. Impact on the claim pipeline: none. A person or the release flow tags. What breaks: N6's pass path and the release rows of Clay's test T13 and the argv tests (D:763 last column); `refuse(argv)` sees only commands the verbs run (D:769), so a tag run in the coordinator's own shell stays unseen (UNVERIFIED how to cover it).
- **OD-10 (close).** Every merge go must name the close, or the close has no go. A restart between merge and closeout must read the recorded go. The dashboard or sweep showing open goes is not decided (Q01, UNVERIFIED). A close by a `Fixes` line still happens at merge without any coordinator write.
- **OD-11 (grants).** A fresh install refuses the plan call's body write and every assign and comment write until the owner says the one chat answer. The watcher is unaffected (the poll writes nothing). What breaks: Clay's six-entry example and any fixture that lists `pr.merge`, `issue.close` or `issue.hold`. A host where the owner never answers works in a degraded way and the refusal must say why.
- **OD-12 (config).** Neither layer prevents a write by the coordinator's shell (D:769, U42). The merge gate's controls (merge safety files, reviewers, the daily notice cap) are only as strong as the accepted answer record. `merge_safety_files: []` is a valid choice for a repo that wants no hold, so it needs an owner-recorded value to count as deliberate.
- **What the owner must know.** All four answers are recommendations until the owner says them in chat. Every control here narrows and none closes: `master` stays unprotected until an admin sets a rule (D15).

## Confidence
76 percent overall: OD-6 89 percent, OD-10 77 percent, OD-11 71 percent, OD-12 69 percent. It would drop if the owner says a standing close or a release pass is acceptable, if U57 is shown to work (an answer record that tells the owner's chat words from a session's), or if the owner counts the one chat answer as manual setup under the zero-setup rule. It would rise if the live checks show the verb refusal and the hook do what the design says.

## Unverified
- U57 (D:1315): that the recorded OK for a release, or any recorded go, can be told from a session's words. This paper does not claim the Q01 record fields close that gap.
- Whether the `repos` verb refusal and its tests (D:688, D:758, D:765) are built in pr-a. D15 records the verbs as design text only.
- That no other check stops closeout's close (the `E-NO-GRANT` inference rests on D:696 and `SKILL.md:51`).
- Whether `git push --tags`, `gh release edit` and `gh release delete` match D:763 exactly.
- The zero-setup memory body (`zero-setup-watcher-decisions`): only its index line was visible to me; the CLAY advocate could not read it.
- Which planb file holds the per-repo keys (D15 R-3).
- The workflow search (no tag or publish step in master workflows) was run by me and was not re-run by either advocate.
- Debate limits: quick depth, one round, no rebuttals; both advocates and the scoring evaluator are the same model family, one evaluator scored both papers (estimates, not measurements); the invariant probe was skipped.
- The sums of the diff points (17) and the 88.2 percent are my count from the advocates' verdict tables; the two open points (C-006, X-003) were both resolved as HYBRID in the merge.

## Debate artifacts
All under `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/QG3/`:
- `position-OURS.md`, `position-CLAY.md`
- `adversarial/merged-qg3-position.md`, `adversarial/return-contract.yaml` (worker contract)
- `adversarial/adversarial/diff-analysis.md`, `debate-transcript.md`, `base-selection.md`, `refactor-plan.md`, `merge-log.md`, `return-contract.yaml`, `variant-1-original.md`, `variant-2-original.md`
- `adversarial/adversarial/rounds/` (empty: the advocate texts are in `debate-transcript.md`)
