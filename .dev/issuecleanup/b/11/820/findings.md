# Round 2 findings: issue 820 (W12, seven-day service-level review after the first live enable, FU-10)

Item: sub-issue of the watcher umbrella #717. Checked 2026-11-24 against master `f2894fc44` (this worktree equals `origin/master`). "REQ" means `.dev/releases/backlog/issue-watcher-zero-setup/requirements.md`. "UNIFY" means `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/`. Live state read read-only from `~/.local/state/superclaude/issue-watch/IronClaude/audit.jsonl`.

## Alignment with architectural decisions

- **R38 (REQ:64): aligned.** FU-10 is a follow-up of the merged design: "SLO review with `cycle.slo_numbers` (section 10.5) ... After 7 days live" (`docs/designs/issue-watcher-setup.md:677`; `docs/designs/issue-watcher.md:869`), with the owner-run snippet at `docs/designs/issue-watcher-setup.md` section 10.5 (lines 448-471). The plan ids in the item (S11-F19, S12-F33, TECHREF:1954) belong to the unification plan, but the requirement itself is the merged design's, so R38 does not drop it.
- **Code (`src/superclaude/cli/issue_watch/cycle.py:1477-1544`): aligned.** `SloNumbers` and `slo_numbers` exist, are pure, and have only test callers (codegraph callers: `tests/issue_watch/test_slo_helper.py` only). No production caller and no CLI verb, as the item says.
- **Approval basis (REQ:61 R35, `src/superclaude/cli/issue_watch/first_run.py`): aligned.** The p95 "approval-to-launch" number reads `approved_at` on the `launched` decision (`cycle.py:1520-1525`), which matches the `Approved` field as approval. The item's watch-out that the number "assumes the approval step the plan keeps" is therefore fine.
- **R26 and the unknown outcome (REQ:52): partly aligned.** An unknown launch outcome counts as the sweep's launch. `slo_numbers` ignores such lines for the two launch-based numbers, which is the cause of the empty numbers below.
- **Owner-decision rule (`src/superclaude/core/WORKER-CONTRACT.md:57`): aligned.** "Decides whether to keep it on" is an owner decision given in chat and recorded by the agent with the quoted words and the date; the item's "written review" fits only if the owner's answer is recorded that way.
- **#450 closure (closed completed 2026-11-24):** replaced the manual shadow run, lock test and restart test by the automatic first-run check. It does not mention the seven-day review, so FU-10 stays open and is not superseded.
- **DECISIONS.md, SPEC.md, FOLLOW-UPS.md and every `debates/*/VERDICT.md` in UNIFY: none apply.** Searched case-insensitively for "SLO", "slo_", "FU-10", "seven", "7 days", "7-day" in those files; the only "seven" hits are unrelated (`DECISIONS.md:278, 309, 311, 593, 1017-1039, 1078`). The only sources for the review are the merged design docs and the technical reference (`UNIFY/techref/ISSUE-TO-WORK-PIPELINE-TECHNICAL-REFERENCE.md:885, 1954, 1990`), which describe the gap and do not decide anything.
- **Not a conflict but a fact:** the "created at switch-on" part of the done-when cannot be met any more. The first real cycle was 2026-11-23T21:56:04Z (first line of `audit.jsonl`), so seven days end 2026-11-30T21:56Z.

## Complementary issues

- **#819 (W11, unknown launch outcome):** the data supplier. The live audit has no decision with reason `launched` (the two real launches are `launch_unknown`, then `claimed`), so `approval_to_launch_p95_s` and `claimed_within_lease_share` come out `None` today. Interface: a `launched` decision line, produced once the launch reply is parsed, or a change to `slo_numbers` to count an unknown entry that later becomes `claimed`.
- **#816 (W8, alert after three bad cycles):** both want an audit-log reader behind `issue-watch status` (`status` does not read the audit log today, per #816 body). Interface: one reader, not two.
- **#814 (W6, every cycle ends with exit 0 or a named reason):** its script over `audit.jsonl` computes the same raw material as the `cycle_exit0_share` number.
- **#821 (W13, dispatch store size bound):** reads the same store and uses the same stale rule (`STALE_AGE_S = 86400`, `cycle.py:46`); independent.
- **#823 (W15, runbook):** the review result is a dated entry the runbook should point to.
- **#777 (map the manual pieces and decide what to automate) and #757 (coordinator sweep outside the session):** a scheduled review could become one of the automated pieces. No duplicate.

## Closest overlap

- **#816, "Issue watcher W8: Alert after three bad cycles (FU-4)".** Shared: the audit log as input and `issue-watch status` as the place a reader would live (the item's optional "status field"). Share of W12's done-when it covers: about 10%. It does not produce the written review or the dated entry.
- **Next two closest:** #814 (about 10%: the exit-0 share number only) and #819 (0% of the done-when text, but without it two of the four numbers cannot exist).

## Standalone or merge

**Verdict: stand alone. Only the optional `status` field would be right to merge, into #816.**

| Test against #816 | #820 | #816 |
|---|---|---|
| Owner | the owner and the watcher owner (a person decides to keep it on) | the watcher owner |
| Acceptance test | a dated written review of the four numbers exists after the first 7 live days | three scripted failing cycles make `status` exit non-zero; a good cycle clears it |
| Files touched | a ledger or task entry and the review document; possibly `cycle.py` (`slo_numbers`) | `cycle.py` `status_report`, `audit.py`, `cli.py` |
| Build phase | time-bound, due about 2026-11-30 | early, independent, waits on the alert-destination choice |
| Risk if merged | the review deadline would be held up by W8's unchosen alert sink, or W8 would grow a calendar task | the same, reversed |

Why it decides: W12 is a dated review a person signs off; W8 is a code change with a tested behaviour. Different test, different clock. Merging would be right for one piece only: if the owner wants `status` to print the four numbers so no snippet is needed, that field should be built inside #816 to avoid two readers of `audit.jsonl`. The review itself stays here.

## Closed issues and merged PRs checked

- **PR 447 (poller, merged 2026-11-08):** delivered `slo_numbers`, `SloNumbers` and the owner-run snippet. It is the "built" half; the review is the missing half.
- **PR 448:** approvers-file race fix; unrelated.
- **PR 707 (zero-setup watcher, merged):** adds the `launched`/`claimed` decisions and levels the numbers read; does not run the review.
- **PR 759 (retry of first-run setup):** not W12. PR 729 (R38 record): puts plan ids out of scope.
- **#450 (rollout, closed completed 2026-11-24):** records 284 cycles at that time (280 exit 0, 2 `lock_missing`, 2 `launch_unknown`) and says the live-test record was never written. It does not run the seven-day review, so it does not deliver W12.
- **#331 (original watcher request):** no SLO content. **#655 (closed not planned):** source of the item.
- **#813 (W5, closed not planned) and #809 (W1, merged into #716):** the owner folds or closes W-items replaced by automatic checks; W12 has no such replacement because nothing reads the numbers.
- **Live audit at 2026-11-24T22:22Z (read-only):** 1439 cycle lines with exit 0, 2 with exit 6 (`lock_missing`, the first two cycles), 2 with exit 7 (`launch_unknown`); 5299 decision lines; `audit.jsonl` is 1,973,797 bytes (about 1.9 MB a day). It rotates at 5 MiB (`audit.py:108`) and `slo_numbers` reads the file plus four older ones, so the seven-day window will still be on disk by 2026-11-30 (my estimate; I did not test rotation).

## Updated recommendation

- **Suggested action: keep open with changes.** (1) Replace "created at switch-on" with "created now, due about 2026-11-30"; the owner picks the anchor (enabled 21:44Z, first cycle 21:56:04Z, or first exit-0 cycle on 2026-11-23). (2) Say plainly that two of the four numbers are empty until #819 is fixed, and ask the owner for one choice: count an unknown entry that later becomes `claimed` in `slo_numbers` (small code change with tests), or accept two empty numbers and wait for #819. (3) Note that missed cron runs leave no audit line, so `cycle_exit0_share` cannot see them. (4) Keep the optional `status` field as a separate follow-up inside #816. (5) Drop the unification-plan row ids.
- **Priority: P2.** Unchanged from round 1: due in six days, the only service-level check, but nothing breaks if it runs a few days late.
- **Complexity and size: simple, S.** Unchanged from round 1 (the review is a one-off; the code change to `slo_numbers` is the S part).
- **What changed from round 1:** nothing in the action, priority or size; the closest-overlap choice (#816), the standalone test and the confirmation that no decision file in the unification plan governs FU-10 are new. The live counts were refreshed (1439 exit-0 cycles now).

## Scan record

- Lists read in full: open-issues.tsv 134 rows, closed-issues.tsv 157 rows, merged-prs.tsv 508 rows.
- Search terms: SLO, slo_numbers, service level, seven-day, FU-10, audit, status, alert, exit 0, stale, review, cycle, watcher.
- Opened and read: open issues #717 (body and closing review), #816, #814, #819, #821, #822, #823, #753, #442, #698, #788, #722; closed #450, #331, #655, #813, #809; PRs #447, #448, #707, #729, #759. #777, #757, #761, #774, #716 were searched by keyword (not read end to end).
- Source: `cycle.py:36, 46, 1477-1544`, `audit.py:108`, `docs/designs/issue-watcher-setup.md:448-471, 677`, `docs/designs/issue-watcher.md:869`, `UNIFY/techref/...TECHNICAL-REFERENCE.md:885, 1954, 1990`.
- Command run: `/sc:analyze src/superclaude/cli/issue_watch --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/b/11/analyze` (shared by the three items).
- UNVERIFIED: the right anchor date for "seven days live"; whether cron missed runs are visible anywhere; audit rotation behaviour at day 7.
