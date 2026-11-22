# Verdict Q03: Dormant hold:plan label code in PR 686

## Question

D09 recommends the poll keeps writing nothing to GitHub (NG-2), but PR 686 contains the `hold:plan` / `hold:backlog` label writing code (`src/superclaude/cli/issue_watch/hold.py` in snapshot pr-a). Should that code stay in PR 686 dormant (switched off), be stripped out until the owner amends NG-2, or be replaced by a read-only variant now? Read D09 VERDICT.md and the code.

## Winner

HYBRID: replace the label-writing code with a read-only variant now (the owner's rule NG-2, that the poll never writes to GitHub, stays as written), and carry over Clay's read-only plan check, `hold:backlog` stop and `would_hold` dry-run listing, with Clay's narrow label form written down as the deferred design.

## Winning recommendation

Terms. "The poll" is the unattended cron job that watches for newly assigned issues. PR 686 is Clay's open rewrite of that watcher. "The grant" is the entry `issue.hold` in the `grants` list of the repo config file `repos.yaml`; PR 686 writes labels only when it is listed. "pr-a" is the read-only copy of PR 686 at /home/coder/.cache/ic-snap-20261120/pr-a. Line numbers below are in that copy.

The unified spec must say:

1. **PR 686 ships no GitHub write by the poll.** Remove from PR 686: `LabelWriter` (`src/superclaude/cli/issue_watch/github.py:983-1069`), the four label argv builders (`github.py:267-320`), `_hold_write_ok` and `_label_write` (`cycle.py:1021-1044`), the label-driven rows 3 to 5 of `_hold_step` (`cycle.py:1064-1119`) and the `hand_removed` state. Test: the NG-2 test is zero writes again; every argv the runner sees is a read.
2. **Keep, read-only.** `plan_check` (`hold.py:122-143`), the `held_incomplete` skip, `hold:backlog` read from the search row (`cycle.py:1055`), the audit reasons, and the `would_hold` dry-run listing. Per D09, `plan_check` runs before the approval read and a `<...>` placeholder-only section counts as empty.
3. **The local entry is created with no write.** When a failing issue is first seen, the poll writes its local `holds` entry (store file, not GitHub) so the one-hour quiet clock starts. Test: with the grant absent and also with it present, a failing issue gets an entry and `writes == []`.
4. **The wake-time re-check changes too.** `cycle.py:1293-1300` tests `hold:plan` on the re-read (`has_label`); a plan request needs the label there and a normal wake rejects it. In the read-only variant these label tests go, and only the plan check and `hold:backlog` remain. Test: a plan request is not rejected as `revalidation_failed` for lack of a label.
5. **A `hold:plan` label on an issue is ignored.** A person who wants a stop uses `hold:backlog`. A leftover `hold:plan` never blocks a passing issue and the poll never logs a warning for it. This is a stated cost: a hand-placed `hold:plan` no longer holds anything.
6. **The grant `issue.hold` is removed** from the reference config and the test fixtures (`docs/designs/orchestrator.md:291` and the `grants` row at `:872`; `tests/issue_watch/conftest.py:286`; `tests/issue_watch/test_repos.py:24`, `:55`; `tests/issue_watch/test_security_invariants.py:968-972`). Test: a config that still lists it is rejected or ignored with one startup line, not acted on.
7. **The label write is deferred, not rejected.** It comes back as its own PR only when someone shows a reader of the label. That PR restores Clay's narrow form (add and remove one label, no comment call, injected refusal guard, `github.py:983-992`), amends NG-2 to name exactly those calls, and is switched on only after a 24-hour `--dry-run` shadow run and a test that `gh` can add and remove a label under cron's minimal environment (D09 rule 4).
8. **Save the removed code before it goes.** Keep the label-writing hunk as a patch next to the debate record, so restoring it does not depend on PR 686's branch history surviving.
9. **Fallback if the sizing step (action 3) finds the rework too large.** Delete only the write calls and the grant check, keep the six-row table and the entry creation, drop `issue.hold` from the reference config, and restore the zero-write NG-2 test. The owner chooses between full rework and fallback after the count.

## Strongest points

OURS:
1. "Dormant" is not the default. The design's own reference config lists the grant (`docs/designs/orchestrator.md:291`, repeated at `:872`) and so does the default test fixture (`tests/issue_watch/conftest.py:286`); nothing in the code defaults it off (grep of `issue_watch/` outside `repos.py`: no match). A copied config turns the label writes on at the first live cycle. Both advocates accepted this.
2. The dormant form is defective in code. With no grant, a failing issue the poll finds itself gets no `holds` entry because row 4 returns before `record.set_hold` (`cycle.py:1080-1083`); a passing issue with a leftover label is skipped (`cycle.py:1064-1070`); and the poll warns every cycle (`cycle.py:1021-1027`, pinned by `tests/issue_watch/test_hold.py:416-426`). Read from code, not run.
3. The boundary is an owner rule with a test behind it. NG-2 says "no GitHub write" (`/home/coder/.cache/ic-snap-20261120/master/docs/designs/issue-watcher.md:76`), and PR 686 rewrites the NG-2 test to allow three label calls (`tests/issue_watch/test_security_invariants.py:12`, `:634-645`). Nobody showed a reader of the label (D09; conceded by both advocates).

CLAY:
1. The hold is one interlocked design: rows, `holds` entries and the plan-request clock depend on each other (`cycle.py:1046-1149`), and `tests/issue_watch/test_hold.py` is 1,073 lines with 58 test functions (counted here). Cutting rows 3 to 5 is a real rewrite before the unification merge.
2. The write form is narrow and tested: `LabelWriter` "has no comment call here and no way to build one" with an injected refusal guard (`github.py:983-992`), the no-grant test asserts `writes(world) == []` (`test_hold.py:416-426`), and the NG-2 test would fail any write beyond the label.
3. The dry-run lists `would_hold` and `would_release` (`cycle.py:1065-1078`) and D09 makes the 24-hour shadow run the switch-on gate; one grant line plus an NG-2 amendment is cheaper than restoring code later (diff point C-009, Clay's side at 65 percent, only if the label is ever wanted).

## Clay strengths to adopt

- **Read-only plan check, `held_incomplete` skip and `hold:backlog` stop.** Why: OURS has no early check and nothing holds a plan-less issue today (D09). Merge: kept as D09 rules 1 to 6; the placeholder and ordering fixes apply.
- **The narrow label-write form, written down as the deferred design.** Why: the form is already designed and tested; losing the description would make the later PR start from nothing. Merge: spec section "deferred label write" (recommendation 7); the code itself is not shipped.
- **`would_hold` dry-run listing and the shadow run as the switch-on gate.** Why: it is the only way to see holds before any write is enabled. Merge: keep `would_hold`, drop `would_release`, and make the shadow run plus the cron test the gate for any later switch-on.
- **Local `holds` entry and quiet-hour clock.** Why: the plan request after one hour needs it (D09 defers the request itself to the topology decision D07). Merge: keep the entry, but create it with no GitHub write (recommendation 3).
- **The cost ledger Clay priced** (a 58-test module, a second PR to restore, a lost hand-placed `hold:plan`). Why: the owner should choose with these costs in view. Merge: recorded under Implications and in the fallback.

## Our strengths that must be kept

- NG-2 as written and the zero-write NG-2 test, until a label write is enabled by its own PR.
- The per-issue grant row, as against a standing grant list (the standing list is what makes "dormant" unsafe).
- The poll never creates a label and never comments about a hold. The only creation of `hold:backlog` is a once-per-repo step by a person or by init (D09 rule 2). PR 686 creates only `hold:plan` (`github.py:278-291`), so removing the write path also removes that creation.
- GitHub text never reaches a typed line, the audit log or the store: the issue body read for `plan_check` stays in memory (D09 rule 6).

## Actions

| Action | Type | Target | Order or dependency |
|---|---|---|---|
| Write recommendations 1 to 9 into the unified design as the Q03 rules (the poll writes nothing; label write deferred; entry without write; label ignored) | DOC | unified design spec (D14 output) | First |
| Sizing step: count lines and tests touched by `LabelWriter`, the four argv builders, rows 3 to 5, the `hand_removed` state and `cycle.py:1293-1300`; then choose full rework or the fallback | DECISION | owner, with the coordinator's count | Before the strip is requested |
| Decide who makes the edit: ask Clay to change PR 686 before merge, or merge as is and strip in a follow-up (recommended: change PR 686 first, so master never carries the loosened NG-2 test) | DECISION | owner | With the sizing row |
| Strip the label-writing code and the label tests of the wake-time re-check; create the entry with no write; ignore a `hold:plan` label | PR KEEP-ADAPT | PR 686: `github.py`, `cycle.py:1021-1119`, `cycle.py:1293-1300`, `hold.py` (`table_row`), `record.py` (`hand_removed`), `tests/issue_watch/test_hold.py` | After the DOC row and the decisions |
| Restore the zero-write NG-2 test; replace the no-grant warning test by the "no write, no warning, entry created" tests | PR KEEP-ADAPT | `tests/issue_watch/test_security_invariants.py:12`, `:288-296`, `:634-645`; `tests/issue_watch/test_hold.py:416-426` | With the strip |
| Remove `issue.hold` from the reference config, the grant validator tests and the fixtures | PR KEEP-ADAPT | `docs/designs/orchestrator.md:291`, `:872`; `tests/issue_watch/conftest.py:286`; `test_repos.py:24`, `:55`; `test_security_invariants.py:968-972` | With the strip |
| Save the removed label-writing hunk as a patch next to the debate record | LOCAL CHANGE | a patch file under /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/ | Before the strip lands |
| Write the deferred label-write form (add and remove one label, no comment, injected guard, grant gated) into the design as a reserved section | DOC | `docs/designs/orchestrator.md` section 4.11 (unified copy) | With the first DOC row |
| Amend NG-2 to name exactly add and remove of `hold:plan`, and add the 24-hour shadow run and the cron write test | DOC and LOCAL CHANGE | `docs/designs/issue-watcher.md:76`; watcher runbook | Only when a label write is enabled |
| Make held issues visible without the label: sweep and observer read `issue-watch status` or the audit log (`held_incomplete`) | DECISION | topic D11 (sweep and observer) | D11 result |

## Implications

- **Watcher.** The poll stays read-only on GitHub. A failing issue is skipped as `held_incomplete` and logged; the one-hour plan request remains a wake-file item for D07. Because the wake-time re-check today needs the label (`cycle.py:1295-1300`), leaving it unchanged would stop plan requests from ever firing in a read-only variant.
- **Visibility.** With no label a held issue shows only in `issue-watch status` and the audit log (design 4.11 points 8 and 10(a)). The sweep and the observer behind the issue 409 dashboard design (the owner's dashboard proposal) must read those, or a plan-less issue is invisible to everyone but the owner.
- **Claim pipeline and coordinator.** No change: a held issue is never sent to a coordinator and plans come from a person or `/sc:issue --plan`.
- **What breaks.** In PR 686: the NG-2 test (three calls to zero), about 17 lines of `test_hold.py` that mention a label call (grep count, rough), the no-grant warning test, the grant fixtures, and the reference config lines. A hand-placed `hold:plan` stops holding anything.
- **The owner must know.** (a) The "dormant" form is not dormant by default: the design's own config example turns it on. (b) Clay's code has a real defect in its own dormant state (no entry, a stuck leftover label, a warning every cycle) whichever way this is decided; the strip removes it. (c) The poll is `enabled: false` in PR 686, so nothing runs live yet and this choice carries no live risk today; the cost is in review and merge effort. (d) The rework lands on Clay's PR, so the owner decides who edits it.

## Confidence

70 percent. It would rise if the sizing step shows the strip is a deletion of roughly the size counted here, or if a repo config is found that really lists the grant. It would fall if the sizing shows a much larger rework (then the fallback in recommendation 9 applies, not the dormant form), if the owner decides GitHub visibility of a hold is required now (the label write then ships in its narrow form, with the fixes), or if D07 changes who writes the plan request.

## Unverified

- Whether any live repo config lists `issue.hold`, and which file holds it; whether that file is protected from edit (D07 says the config directory "is not tamper-protected", read via D07's verdict, not re-read).
- The size of the rework: "about 75 lines to about 30", "about 140 lines", "about 17 test lines" are rough counts by the two position papers; I counted 58 test functions and 1,073 lines in `test_hold.py` but did not run any test or any rework.
- Row 3, row 4 and warning behaviour with no grant were read from `cycle.py`, not executed.
- The wake-time re-check at `cycle.py:1280-1305` was read in part; the effect on plan requests (needs the label) is from those lines, not from a run.
- Clay's claim that the owner's local branch already writes a label once per repo (`repo_init.py`) was not re-read; D09 reports it from the owner's local worktree.
- The mapping "standing grant list (DQ6) against per-issue grant row" comes from the FULL-REPORT.md section 5 table, not from the design text itself.
- The qualitative scores came from two agent evaluators and the orchestrator's re-evaluation; the advocates were given the orchestrator's diff analysis (including moderator facts M1 to M4), so they are not fully independent. One debate round (depth quick); convergence 71.4 percent, below the 80 percent threshold.

## Debate artifacts

- /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/Q03/position-OURS.md
- /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/Q03/position-CLAY.md
- /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/Q03/adversarial/merged-output.md
- /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/Q03/adversarial/return-contract.yaml
- /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/Q03/adversarial/adversarial/diff-analysis.md
- /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/Q03/adversarial/adversarial/debate-transcript.md
- /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/Q03/adversarial/adversarial/base-selection.md
- /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/Q03/adversarial/adversarial/refactor-plan.md
- /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/Q03/adversarial/adversarial/merge-log.md
- /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/Q03/adversarial/adversarial/return-contract.yaml
- Adversarial status: partial (convergence 0.714 at depth quick; no invariant probe at that depth; post-merge validation PASS).
