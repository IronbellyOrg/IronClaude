# Round 2 findings: issue 819 (W11, one retry of an unknown launch outcome, FU-8, owner question Q2)

Item: sub-issue of the watcher umbrella #717. Checked 2026-11-24 against master `f2894fc44` (this worktree equals `origin/master`). "REQ" means `.dev/releases/backlog/issue-watcher-zero-setup/requirements.md`. "UNIFY" means `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/`. Live state read read-only from `~/.local/state/superclaude/issue-watch/IronClaude/`.

## Alignment with architectural decisions

- **R38 (REQ:64): partly aligned.** FU-8 belongs to the merged design (`docs/designs/issue-watcher-setup.md:675`, `docs/designs/issue-watcher.md:867`), so the need stands. The item's ids "S11-F18", "S11-F24" and "TECHREF:1963 (D-12)" come from the unification plan, whose adopted-Clay rows R38 withdraws. The "Q2" at `issue-watcher.md:873` is the merged design's own question ("accept the full-argv retry form (C20) in place of FR-015's short form"). It is not the "Q2" at `issue-watcher.md:41`, which is a different decision (D2 option 3).
- **AC-9 / FR-015 / FR-021 (`docs/designs/issue-watcher.md:889`, "No automatic retry; `status` lists the full retry argv"; pinned by `tests/issue_watch/test_cli.py` status-retry tests, found with codegraph callers of `retry_argv`): in conflict if the retry becomes automatic.** The item asks for "one retry", which changes AC-9 unless the owner chooses a manual-only form. The code today prints the full argv and never runs it (`src/superclaude/cli/issue_watch/cycle.py:1446-1458`, `launch.py:160-173`; the only production caller of `retry_argv` is `status_report`).
- **D9 of the claim design (`docs/designs/sc-issue-claim-pipeline-flag.md:387`, "No automatic retry of a launch and no `--retry-launch` in version 1; a silent second launch is not predictable"): in conflict in principle.** It governs the `/sc:issue` claim's own launch, but states the same rule, so W11 needs an explicit owner reversal for the watcher path.
- **R26 (REQ:52): partly aligned.** An unknown outcome already counts as the sweep's one launch and the dispatcher stops on it. A retry in a later sweep is a second launch call, so the item must say whether it counts against the one-launch-per-sweep rule and the six-per-repo-per-day cap (`DAY_CAP = 6` at `cycle.py:36`, checked by `_day_cap_reached`, `cycle.py:924-933`).
- **FR-21 (`UNIFY/spec/SPEC.md:211`, "an unknown launch receipt never relaunches"): aligned as a principle, but the SPEC is the unification plan, not the adopted design.** The same principle lives in AC-9. Whether Orca's `--retry-launch` can never create a second session is UNVERIFIED (`launch.py:67-76` marks the operation-id paths and `agent_session_operation_unknown` as `[PROPOSAL, UNVERIFIED]`).
- **D10 (`UNIFY/debates/D10/VERDICT.md:21, 52`, one Orca verb with a receipt and operation id): does not govern.** D10 is the wake transport, which R38(C) drops. The claim launch already uses the one verb (`launch.py:136-157`).
- **R33 (REQ:59, `launch.py:48`): aligned.** With the ship gate closed only Pipeline None launches, so a wrongly built retry would start at most a second claim session, not a governed worker.
- **WORKER-CONTRACT WC-6 (`src/superclaude/core/WORKER-CONTRACT.md:73-75`, every retry is a new Task, never `worker-start --retry-of`): none apply to this code path.** It concerns coordinator Tasks. It is the same discipline #788 applies to `worker-start`, which is why the owner decision should be shared (see Closest overlap).
- **Q2 owner answer:** the owner's own record R38 and the #717 closing review ("W11 requires ... the current owner's recorded retry choice, not the alternative design's historical answer") confirm the retry form is still undecided. I found no recorded answer in REQ, `UNIFY/QUESTIONS.md` or the decisions (searched "Q2", "retry"). UNVERIFIED whether it was given in chat.

## Complementary issues

- **#820 (W12, seven-day service review):** depends on this item. `slo_numbers` builds two of its four numbers only from `launched` decisions (`cycle.py:1520-1527`); the two real launches on 2026-11-23 were `launch_unknown` then `claimed`, so those numbers are empty until the launch reply is parsed correctly. Interface: a `launched` decision in `audit.jsonl`.
- **#823 (W15, runbook with real captured steps):** the capture of Orca's real launch reply is also a runbook step. Interface: one of W11 or W15 must own capturing the reply and replacing the 20 `_assumed_shape` fixtures (`tests/issue_watch/fixtures/_assumed_shape/`, per #450's closing comment), the other documents it.
- **#788 (Coordinator C7, unknown-outcome handling for `worker-start`, open):** same rule for a different verb ("asks Orca whether that request took effect once, retries only with the same request id, escalates on the second failure"). Interface: one owner decision on whether Orca's request-id retry is idempotent serves both.
- **#774 (docs refresh):** lists replacing the assumed fixtures as work "carried by #717"; no code overlap.
- **#812 (W4 backoff) and #817 (W9 conditional reads):** also wait for the same live capture; independent.
- **#770 (watcher hands claims to the coordinator):** starts after `claimed`; no overlap.

## Closest overlap

- **#788, "Coordinator C7: Worker start ... unknown-outcome handling".** Shared: the same safety rule (retry only through the same request or operation id, never a fresh start) and the same unknown fact (Orca's idempotency). Share of W11's done-when it covers: about 15%. It covers the decision and the principle, none of W11's code, its live lost-reply test, or the `launched`-parse fix.
- **Next two closest:** #823 (about 10%: captures the real launch reply in the runbook but does not change `outcome_of`) and #820 (0% of the done-when, but the consumer of the fix).

## Standalone or merge

**Verdict: stand alone, and reframe the first step.**

| Test against #788 | #819 | #788 |
|---|---|---|
| Owner | the watcher side of #717 | the coordinator side (#716) |
| Acceptance test | live lost-reply test: one retry with the same operation id gives exactly one session; entry reaches `claimed` or `failed` | fault-injected unknown `worker-start` never makes two Dispatches; a second failure writes an escalation entry |
| Files touched | `src/superclaude/cli/issue_watch/launch.py`, `cycle.py`, `record.py`, tests | the coordinator skill (not built) and Orca verbs `request-show`, `worker-start --retry-request` |
| Build phase | watcher second part, after the live capture | coordinator phase after C5 |
| Risk if merged | a watcher fix would wait for an unbuilt skill, and a coordinator-skill ticket would carry a cron-side change | same, reversed |

Why it decides: different code, different acceptance test and different build time. The only thing they share is one decision (is Orca's retry idempotent, and is the retry manual or automatic), and that is a chat decision the owner records once, not a reason to join two work items.

Merging would be right only if the owner turns it into one "Orca unknown-outcome rule" issue that both consumers follow; I do not recommend it because the decision costs one chat answer.

## Closed issues and merged PRs checked

- **#450 (rollout, closed completed 2026-11-24):** its closing comment names 2 `launch_unknown` cycles and says the 20 assumed fixtures and the live-test record were not done; it assigns the capture to #717's W4, W10, W11 and W15 and says "I did not re-check that claim". The capture has no single owner today.
- **#813 (W5, closed not planned 2026-11-24, 22:10Z):** the live firing tests were replaced by the automatic first-run check, so the manual live gate that would also have captured Orca's reply was dropped. Makes the capture duty heavier on W11 or W15.
- **#809 (W1, merged into #716):** precedent of the owner folding W-items.
- **PR 447 (poller with `retry_argv`, `status`, `slo_numbers`) and PR 448:** built the print-only retry argv and the unknown-entry state. Not W11, which is the retry itself.
- **PR 759 (retry of first-run setup for a failed first run, #751):** not W11; the #717 review says the same.
- **PR 707 (zero-setup watcher):** adds R26 and the ship gate; no retry.
- **#655 (closed not planned) and PR 729 (R38):** source and baseline; put S-ids out of scope.
- **#394 / PR 432, #390 / PR 403:** unrelated to launch retry.
- **Live record (read-only):** `dispatch.json` holds #597 and #751 both `claimed`, `launches: 1`, `operation_id: null`; `audit.jsonl` shows `launch_unknown` for 597 (2026-11-23T22:12:11Z) and 751 (22:13:13Z), then `claimed` at 22:28:06Z and 22:19:10Z; no decision with reason `launched`. Both sessions had in fact started, and the claim marker healed each entry (`cycle.py:983-994`).

## Updated recommendation

- **Suggested action: keep open with changes.** (1) Lead with the finding that both real launches ended `unknown` with a null id and healed on their own, so the first step is to capture Orca's real launch reply and fix `outcome_of` (`launch.py:372-395`: any exit-0 reply without a recognised id is `unknown`). UNVERIFIED that the cause is the assumed reply shape; Orca's real reply was not captured. (2) Say that the manual retry through `status` exists and works only when an id was parsed. (3) Make the retry a later step, gated on proof that Orca's retry makes at most one session, and one chat decision (manual only, or one automatic retry) that also serves #788. (4) Amend AC-9 only if the automatic retry is chosen. (5) Rename the S-ids to FU-8. (6) Settle with #823 which of the two owns the reply capture; I suggest W11, because the fix is in `launch.py`, with W15 only documenting it.
- **Priority: P2** for the reframed step (it affects every launch and the numbers of #820); the automatic retry on its own stays P3. Round 1 said "P3 as written; P2 if reframed", so this is the reframed reading, chosen because the live record shows 2 of 2 launches were `unknown`.
- **Complexity and size: medium, M.** Unchanged from round 1.
- **What changed from round 1:** closest overlap and standalone test added; priority resolved to P2 with the reframe; #813's closure added as a new fact that removes the manual live gate.

## Scan record

- Lists read in full: open-issues.tsv 134 rows, closed-issues.tsv 157 rows, merged-prs.tsv 508 rows.
- Search terms: retry, unknown, launch, operation id, `--retry-launch`, FU-8, Q2, fixture, `_assumed_shape`, request-show, idempotent, watcher, claim, dispatch.
- Opened and read: open issues #717 (body and closing review), #788, #820, #823, #816, #814, #821, #822, #753, #442, #698, #722; closed issues #450, #331, #655, #813, #809; PRs #447, #448, #707, #729, #759, #584. #716, #774, #770, #812, #817 were searched by keyword (their bodies were not read end to end).
- Source: `launch.py:48, 67-76, 136-173, 372-395`, `cycle.py:983-994, 1195-1204, 1400-1458, 1497-1544`, `docs/designs/issue-watcher.md:41, 867, 873, 889`, `docs/designs/issue-watcher-setup.md:675`, `docs/designs/sc-issue-claim-pipeline-flag.md:387`.
- Command run: `/sc:analyze src/superclaude/cli/issue_watch --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/b/11/analyze` (shared by the three items).
- UNVERIFIED: Orca's real launch reply; whether `--retry-launch` is idempotent; whether the owner answered Q2 in chat.
