# Verdict D13: Closeout, worktree cleanup, PR log versus issue 339 duties

## Question
Clay's `/sc:closeout` (PR 683, merged), worktree cleanup (PR 687, open) and daily PR log (PR 670, merged) versus issue 339's duties (`sc:close`, worktree and branch cleanup, hourly sweep). Are they complementary (keep and adopt as coordinator steps) or duplicates (retire one)?

Correction found while reading: 687 is an issue (Clay's request for a daily worktree cleanup, open, author `clayphi`), not a pull request. `gh pr view 687` does not resolve it and `gh issue view 687` does. Nothing is built for it yet.

## Winner
HYBRID: the three pieces are complementary and none is retired, but the coordinator, not a free-standing script, is the accountable owner of the close chain, which is the owner's wording in issue 339 (the owner's issue: one orchestrator manages all sessions).

## Winning recommendation
The unified spec must say all of the following.

1. **No duplicates, nothing retired.** The duty map is:

   | Issue 339 duty | Tool that covers it | State |
   |---|---|---|
   | Hourly sweep of sessions | `/sc:sweep` (PR 539, merged; `WORKER-CONTRACT.md` line 289, rule WC-16, runs it on every coordinator wake) | Built, read-only |
   | `sc:close`, first half: settle a merged PR, its issue, its work-report entry and its worker's Orca task | `/sc:closeout` (PR 683) | Built |
   | `sc:close`, second half: worktree and branch removal with strict validation | Issue 687's `scripts/worktree_cleanup.py` (nine rules) | Not built |
   | Close or resume an idle session, in-chat status report | none | Not built; stays in issue 339 |
   | Daily log of merged PRs per person | PR 670 | Built; no 339 duty; stays outside the coordinator |

2. **The coordinator owns the chain.** Each coordinator cycle: run `/sc:sweep`; call `/sc:closeout <PR>` for every merged PR (wave 8 of the design of PR 681); run the cleanup script's `list` (dry run) and report its table. The `--apply` step runs only under a grant row or a user instruction that names that action (`WORKER-CONTRACT.md` line 241). `/sc:closeout` stays on the never-as-worker list (line 23).
3. **Nobody removes by judgment.** A removal is decided only by the nine rules of issue 687 (PR merged, nothing added after, issue closed, nothing using it, idle 7 days, `.dev/` files saved and verified first, and the rest of spec section 6). The script never uses `--force`, `git branch -D` or `rm`. The sentence "never run by the orchestrator" in issue 687 and the "not done by the orchestrator" in `docs/designs/orchestrator.md` line 628 are narrowed to: no session decides a removal by its own judgment; line 628 stays true for wave 9's issue worktree only.
4. **Branches.** Remote branch deletion stays human-only (rule 1 as quoted at `orchestrator.md` line 139). A local `git branch -d` inside the script needs the owner's decision (Actions, row 7); this verdict recommends yes because `-d` refuses an unmerged branch and the owner asked for branch cleanup on 2026-11-05.
5. **Testable checks.** (a) The design or `HOW-WE-WORK.md` carries the duty map above. (b) No sentence in the design says the orchestrator or coordinator never removes a worktree without the scope in item 3. (c) Issue 687's acceptance list gains: `--apply` is refused without a grant, and a test records that no `--force`, `-D` or `rm` is ever run. (d) The words orchestrator (issue 339), orchestrator (design of PR 681) and coordinator (contract) are mapped to one role in a written glossary.
6. **Issue 339 stays open** as the umbrella until the "close or resume an idle session" and in-chat report items are built or dropped (the owner's status review of 2026-11-17 says exactly this for `sc:close`).

## Strongest points

**OURS**
1. The owner's comment on issue 339 (2026-11-05 13:43Z) puts worktree and branch cleanup in the orchestrator role "with extra rigid and strict validation" and has it keep polling until sessions are finished, cleaned up and closed. Source: `gh issue view 339`.
2. Closeout is not `sc:close`: its Will Not Do list says it never deletes a branch or a worktree (`src/superclaude/skills/sc-closeout-protocol/SKILL.md` line 110), and the design drops Jay Wedgeworth's "Retire the lane" step (`docs/designs/sc-closeout.md` line 106). The owner's 2026-11-17 status review says `sc:close` is not built.
3. Clay's blanket "never removes" is wider than its sources: `orchestrator.md` line 628 is in wave 9 and covers the issue worktree only, line 139 is the `gh pr merge --delete-branch` ban, and `WORKER-CONTRACT.md` lines 236 and 237 already let the coordinator remove a child worktree and delete its branch after merge-back, with keep conditions. Verified in the master snapshot.

**CLAY**
1. Closeout is built and tested: PR 683 reports 22864 passed and 2 environment failures (a PR body claim), and wave 8 of the merged design already calls it (`orchestrator.md` line 603).
2. Issue 687 turns "rigid and strict validation" into nine mechanical rules with a dry run, an evidence-repo save first, and the lesson of 2026-11-20 (git knew 53 worktrees, Orca 26; sixteen removed by hand, two for open issues #354 and #419). Source: issue 687 body.
3. One truth check serves both: issue 687 reuses closeout's `branch-landed.sh` (three-dot diff, never commit ancestry; `SKILL.md` line 62 stops on anything but `MERGED`). The PR log (PR 670, merged by `ironbelly`) is independent and overlaps no duty.

## Clay strengths to adopt
1. **`/sc:closeout` as the coordinator's post-merge step.** Why: it is the only built path to part of `sc:close`, and it is already wave 8. Merge: adopt as is. Override: its writes (close issue, note, Orca task) need a named grant row (`WORKER-CONTRACT.md` line 241); the close authority itself is for the debate on merge and close rights, not this one.
2. **The nine-rule removal script of issue 687.** Why: it supplies the strict validation the owner asked for and removes model judgment from an irreversible act. Merge: adopt with change: the coordinator runs `list` each cycle and `--apply` only under a grant; narrow the "never run by the orchestrator" sentence (item 3 above).
3. **Shared landed check.** Why: one truth check, not two. Merge: adopt as is; note that issue 687 itself lists "how the check is reached once installed" as unproved.
4. **Evidence-repo save before removal** (`.dev/` files verified in `IronbellyOrg/run-evidence`). Why: workflow files are untracked and die with the worktree. Merge: adopt with 687; its proofs (push with the environment token, Orca removal without `--force`) stay open items.
5. **PR log (PR 670).** Why: complementary reporting. Merge: keep as is, as an opt-in daily automation, not a coordinator step.

## Our strengths that must be kept
- The owner's duty text in issue 339 (hourly sweep, `sc:close`, polling until cleaned up and closed) as the governing definition; issue 339 stays open as umbrella.
- `/sc:sweep` run on every coordinator wake (WC-16) and its read-only, recommends-nothing rule.
- The coordinator's existing bounded removal duty for child worktrees (`WORKER-CONTRACT.md` lines 236 and 237, with its keep conditions) and the rule that outward actions need a user instruction naming them (line 241).
- Closeout never as a worker (line 23), and no session removing a worktree by its own judgment.
- Remote branch deletion human-only.

## Actions
| Action | Type | Target | Order or dependency |
|---|---|---|---|
| Keep closeout and its three never-as-worker pins as merged | PR KEEP | PR 683 (`/sc:closeout`) | None; its dangling `/sc:issue --plan` reference depends on PR 690 (the plan flag), see Implications |
| Keep the PR log unchanged and outside the coordinator | PR KEEP | PR 670 (daily merged-PR log) | None |
| Adapt the cleanup issue before anything is built: replace "never run by the orchestrator" with the coordinator-runs-under-grant rule; add the `--apply` grant acceptance check and the test that records no `--force`, `-D`, `rm` | PR KEEP-ADAPT | Issue 687 (it is an issue; nothing is built) | After decisions in rows 6 and 7; before any build |
| Narrow the blanket removal sentences to the scope in recommendation item 3 | DOC | `docs/designs/orchestrator.md` line 628 and the rule 1 reading at line 139 (inside the unified rewrite, not a direct edit of master) | With the D14 disposition of PR 686 and the merged design |
| Add the duty map and the three-name glossary (orchestrator in issue 339, orchestrator in the PR 681 design, coordinator in the contract) | DOC | The unified spec; `HOW-WE-WORK.md` | First: other verdicts use the names |
| Record the owner's approval of the cleanup design, in chat | DECISION | Issue 687 | Before any build; the agent records it, the owner writes no file |
| Decide whether the script may run local `git branch -d` (recommended: yes, local only, remote stays human-only) | DECISION | Issue 687 section on removal; line 139 reading | Before row 3 |
| Keep issue 339 open as umbrella; remaining items are "close or resume an idle session" and the in-chat report | DECISION | Issue 339 | After the cleanup build or an explicit drop |
| Make the wave 8 closeout call depend on a grant row | LOCAL CHANGE | The unified spec, closeout step | With the verdict on merge and close authority (another topic) |

## Implications
- **Coordinator and orchestrator.** The cycle gains three steps (sweep, closeout, cleanup list). The coordinator needs a grant row for closeout's writes and for `--apply`; without it the steps stop at read-only. This lines up with the existing rule on grant rows.
- **Watcher and claim pipeline.** No direct effect. Closeout's `left_open` hand-back feeds the hand-back loop of the PR 681 design (another topic). PR 683's command names `/sc:issue --plan <N>` in its Related Commands table and hand-back sentence, but that flag lands in PR 690 (the plan flag, open); if PR 690 is closed or rewritten, those two references dangle until updated.
- **Dashboard and observer.** The cleanup `list` table could feed the observer report (issue 409); whether it should is UNVERIFIED and not decided here.
- **What breaks.** Nothing is lost by keeping the three. A reading in which the coordinator may delete on its own judgment would be unsafe (issue 687's incident); this verdict rejects it. If the PR 681 design is rewritten or removed, wave 8 loses its caller of closeout, but closeout still works from a person's prompt and escalates the work-report entry when `superclaude orchestrator report-entry` is absent (`SKILL.md` line 21 and error table).
- **Owner must know.** On GitHub there is no `ironbelly` comment on 668, 681 to 684, 686 or 687 (FULL-REPORT.md). Closeout's spec says the owner approved it; the cleanup design has no recorded approval, so the owner's chat decision is needed before a build.

## Confidence
80%. It would drop if the owner says the coordinator must never run `--apply` (then recommendation item 2 becomes "report only"), if the owner rules local branch deletion human-only, or if the verdict on merge and close authority removes the coordinator's right to close issues (then closeout runs only on a person's instruction).

## Unverified
- PR 683's test counts (22864 passed, 2 failed) come from its body; not re-run.
- Issue 687's numbers (53 worktrees, 49.4 GB, Orca 26, 13 removable, 16 removed by hand) come from its body; not re-run.
- Whether "orchestrator" in issue 339, in the PR 681 design and "coordinator" in the contract are one role (open item 1; both advocates answered QUALIFY).
- Issue 687's own "proved first" items: Orca removal without `--force`, how the landed check is reached once installed, a push with only the environment token, the `/proc` process check.
- Advocate 1's references to `orchestrator.md` lines 82 (R10) and 912 (C14) were not checked by me beyond a grep showing line 912 text.
- Whether an owner approval of 687 or of the wave 8 chain exists in chat or calls (GitHub shows none).
- The debate's agents were same-family agents run by one orchestrating session; the two rubric passes were independent runs but not different models. The quantitative layer of the scoring was estimated by hand.
- Whether the observer report should include the cleanup table.

## Debate artifacts
Adversarial skill ran (depth quick, one round, two advocates, two scoring passes, merge-executor). All under `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D13/`:
- `position-OURS.md`, `position-CLAY.md`
- `adversarial/return-contract.yaml` (worker contract)
- `adversarial/merged-hybrid-position.md`
- `adversarial/adversarial/diff-analysis.md`
- `adversarial/adversarial/debate-transcript.md`
- `adversarial/adversarial/base-selection.md`
- `adversarial/adversarial/refactor-plan.md`
- `adversarial/adversarial/merge-log.md`
- `adversarial/adversarial/return-contract.yaml`
- `adversarial/adversarial/variant-1-original.md`, `variant-2-original.md`
