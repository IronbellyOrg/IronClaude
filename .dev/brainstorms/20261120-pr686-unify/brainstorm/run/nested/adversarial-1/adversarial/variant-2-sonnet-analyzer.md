# Unified architecture and staged migration (variant 2: evidence-and-sequence-first)

Status: RECOMMENDATION only. Nothing here is pushed, merged, reverted or commented. Lens: start from what is built and from the D14 lanes; every stage is one small, independently shippable change with a mechanical merge check.

## 1. Summary

Reading guide. "Poll" means one run of the issue watcher for one repo. "Coordinator" is the long-running Claude session of one project (D08). "Owner" is `ironbelly`; "Clay" is `clayphi`. "Dnn" and "Qnn" are the settled verdicts under `.../debates/`. "O0..O7" are D15's build-order codes; "S0..S20" are this spec's stages. "UNVERIFIED" means no source proves it.

The end state is one project-local flow, built from the smallest steps that master can carry. Cron runs one dispatcher; the dispatcher runs one read-only poll per repo; the poll starts a claim session at level none exactly as master does today (`launch.py:33`); when the claim marker shows, the poll writes an ids-only wake file; the project coordinator pulls it, acknowledges it only after its own state file exists, and starts ONE supervised worker bound to the launch guard; a person's typed go is needed for every push and every merge; closeout and a cleanup dry run follow; the sweep, the observer and the work report read the same session facts. Nothing is switched on until a live shadow run passes (`enabled` stays false, `cycle.py:228`).

The five decisions that matter most:
1. The poll claims, the wake follows (K1). It keeps the built claim path and MR-2 (`marker_in_window`), and the wake means "claimed, take over", never "please claim".
2. The worker is bound at guard level F, not FS (K2). F is the only built level that blocks commit, push and PR while allowing implement (`launch-level-guard.sh:787-790`); the coordinator commits after `worker_done` and pushes only on the person's go.
3. Order is fixed by evidence: hold (H0), lane 1 (PR 693, PR 690, rule C1), revert dry run, revert, amendments, planb as a draft, small additive watcher PRs, PR 686 adapted to a wake-only change, then the coordinator. PR 686 never merges as it stands (D14).
4. One poll command and one config (K4): cron runs `issue-watch run-all`, which runs `issue-watch once --config <per-repo JSON>`. No registry, no `repos.yaml`. Grants default to empty, three standing entries at most, and `max_in_flight` starts at 1 (K6, K9).
5. One plan-check definition lives in `plan_body.py`; the package holds a copy tied to it by a parity test (K8). The poll writes nothing to GitHub (NG-2, D09). The observer's one watcher feed is `issue-watch status --json` (K10).

What cannot be proven yet: a bound `worker-start` worker (never observed), the mailbox from outside a Run (U5), Orca `tui-idle`, cron in the image (Coder 515), and a chat go on one shared login. Section 8 names the test for each.

## 2. Target architecture

### 2.0 Diagram

Tags in square brackets say what exists today: [B] built on master, [P] built only in the owner's unpushed branch "planb" (`ironbelly/issue-watcher-zero-setup-plan`), [C] open Clay PR, [N] not built, [D] design text only.

```
 cron  */5 * * * *  under flock -n, absolute paths                      [N] (Coder 515)
   |
   v
 dispatcher  `issue-watch run-all`  (one loop over `orca repo list`)    [P]
   |   one child per repo, own lock/state/kill file, 270 s total cap
   v
 POLL = `issue-watch once --config ~/.config/superclaude/issue-watch.d/<owner>__<repo>.json`   [B]
   |  READS only (7 gh calls + plan check + hold:backlog). Writes NOTHING to GitHub (NG-2).
   |  Start rule: open + assigned only to watcher + approval unchanged + Status in
   |  {Research,Spec,Plan,Debug} + no hold:backlog + plan check ok.     (D01)
   |  Caps: max_in_flight 1, one launch per sweep, DISABLED kill file, enabled=false default
   v
 CLAIM SESSION  `/sc:issue --claim <N> --pipeline none`   (integer-only prompt, D3)   [B]
   |  claim writes assignee + claim marker comment (the claim does the GitHub writes, not the poll)
   v
 poll sees marker (marker_in_window) -> state `claimed` -> writes WAKE FILE (ids only)  [C, to adapt]
   |      <project>/.dev/coordinators/wakes/<wake_id>.json   (+ optional nudges: mailbox, typed line)
   v
 COORDINATOR  session COORD-<Repo>, worktree/branch `Coordinator`   [N / D]
   |  pulls wakes at every return of `check --wait`; creates per-issue state file; THEN writes ack
   |  starts ONE worker with `worker-start`, first prompt carries [sc-launch:v1:<nonce>],
   |  bound at level F (implement; no commit, no push, no PR)             [N: caller missing]
   |  worker_done -> coordinator commits -> shows commits -> person's go -> push
   |  PR: /sc:pr-submit --monitor 3 in a top-level session (never a worker)
   |  merge: person's typed go -> merge-gate -> gh pr merge --match-head-commit -> merge-gate run again first
   |  wave 8: /sc:sweep -> /sc:closeout <PR> -> cleanup `list` (dry run)  [closeout B; cleanup N]
   v
 OBSERVABILITY (read-only)
   sweep JSON v1 (+session_id, worktree_path), saved beside the sweep report   [B; new fields N]
   observer = the one screen: sweep JSON + `issue-watch status --json`        [B; wiring N]
   work report = plain-English per-issue layer; entry files written by `report-entry`  [B; writer N]
```

Gates that stay manual: the approval (an issue field or label set by a person), the typed go for each push and each merge, the chat go for `--apply`, a server-side ruleset on `master` (does not exist today: `protected:false`, D01).

### 2.1 Issue watcher

What it is: the cron-driven, read-only poll that decides which approved issue starts, starts its claim, and tells the coordinator. Master today has the single-repo poll (`once`, `status`, `check-config`, `init-state`, `reset`; `cli.py:111-348` per the techref ledger row 1b), switched off by default (`cycle.py:228`).

**STAYS (ours).**
- The start rule and its code: `approval_of`, `unchanged_since`, the Status allow-list (R22), `is_intended_owner`, `eligibility_order`, the evidence classes, `_revalidate` at the moment of start (MR-1, `cycle.py:979`), and `marker_in_window` (MR-2, `predicates.py:279`). Assignment alone never starts work (D01).
- The integer-only claim prompt (`launch.py:33`), seven read-only `gh` calls, `enabled` absent means off, the `DISABLED` file, `dispatch.json` (`record.py:281`), `status --json` (`cli.py:165`).
- From planb (unpushed): `run-all`, per-repo JSON under `issue-watch.d/`, `generate.py`, `repo_init.py`, `GOVERNED_LEVELS_ALLOWED = False` (`launch.py:48` in the planb worktree).

**ADOPTED from Clay.**
- `plan_check` as a read-only skip reason `held_incomplete`, run before the approval read, with the "`<...>` placeholder counts as empty" rule (D01, D09, D15 A1); `hold:backlog` as a person-set veto read as `held_backlog` (D15 A3).
- The wake file with acknowledgment, 3 deliveries 10 minutes apart, unread mark, exit 7 (D10); the id-only rule widened to prompt, typed line, mailbox subject and argv (D10 item 6).
- `max_in_flight` with `coordinator_full`, guarded restart, exclusive-create per-issue state file, `owner/name` keys with `name_collision` (D07, D15 C1, C2, C4); the closed reasons table (`audit.py:39`) and Clay's per-repo key names (D15 R-3).

**REWRITTEN.**
- Wake path project-local, names say coordinator, ids only (K5, D08, D10 item 5). Ack only after the per-issue state file exists (M1); an abandoned wake is re-targeted by the poll with a new wake id (M2; the poll already owns the retry loop, so no second writer).
- State machine merges both lines: master's `pending, launched, unknown, failed, abandoned, claimed` (`record.py:34-35`) plus `woken, acked`. `claimed` stays so MR-2 survives (K1).
- Stripped: label writer, `_hold_write_ok`, `hand_removed` (D09, Q03); registry, PR 686's `repos.py`, `wrong_target` never land (D07). Reasons table rewritten (S11, MC-10).

**INTERFACES.** Exposes cron line, `run-all`, per-repo JSON contract, wake and ack files, `dispatch.json`, `audit.jsonl`, `status --json` (plus `last_sweep_at`, `recent_skips`, K10). Consumes `orca repo list`, `gh` reads, the claim marker, the ack and state files, the plan check. Rows 1-8, 11-13, 20, 24-25 of section 4.

### 2.2 Coordinator

What it is: one standing, project-local Claude session (`COORD-<RepoName>`, working branch and worktree `Coordinator`, records under `.dev/coordinators/`) that takes a claimed issue, runs one supervised worker, and carries the issue to a person-approved merge. Nothing of it is built: no skill, no command, no verb group (techref ledger rows 7, 15, 17). Today only the contract text exists (`WORKER-CONTRACT.md`) and the design text `docs/designs/orchestrator.md`.

**STAYS (ours).**
- Authority: a person opens the session, or a script starts it at depth 0 under an authorization the owner recorded in chat (self-attested, stated so); no merge without a person's typed go; `/sc:pr-submit` never runs as a worker (WC:23, WC:244); `/sc:closeout` never a worker (WC:23). Contract amendments WC:70 and WC:245 are not in force until the owner approves in chat (D06 item 7).
- The restored `issue_pipeline` package, WC-17, "Issue pipeline duties", G2 rule 1 (after the revert, D03, D14), and G2 rule 2 (built; `launch-level-guard.sh:485-537`).
- Every approval, go and ruling is given in the owner's chat and recorded by the agent (Q01).

**ADOPTED from Clay.**
- `merge-gate` (13 closed reasons) run twice, head-pinned `gh pr merge --match-head-commit`, never `--auto`, `--admin`, `--delete-branch`; `changes_requested` hard refusal; merge-time reviewer hold (60 minutes, UNVERIFIED) (D06).
- `answer-check` as a validator only, `E-NO-GRANT` with a use log, `refuse(argv)` with a closed "may do" list (D04, D15 table rows D4, D5, D8: "row D4" means D15's table, not debate D04).
- Audit AU1-AU8, hand-back loop (`HANDBACK_MAX` 3), `escalate`, `report-entry`, the nine-row notice table, one verb group with one JSON contract and one state lock, test plan T1-T13, flags `--wake`, `--hourly`, `--resume`, `--take`, `--sub` (D08, D15).

**REWRITTEN.**
- Worker bound at level F with a marker from the restored `brief.build` (K2, K3); the coordinator commits after `worker_done` (WC:245-246 already make it the committer).
- Grants: default empty, at most three standing entries (K6); no standing `pr.merge` or `issue.close` (K11). Merge only through one verb that refuses without a go entry, because `E-NO-GRANT` does not see a raw `gh pr merge` (D06 item 8). Owner identity is a parameter, never Clay (Q01).
- The first skill ships without the merge path and stops at "PR ready, person merges by hand" (S15); the merge path then arrives as ONE tested unit (S16, D15 O5).

**INTERFACES.** Consumes the wake file, the per-repo JSON (`grants`, `merge` block, `reviewers`, `max_in_flight`), `gh` reads, the person's typed answers. Exposes ack and state files, the handoff prompt with `[sc-launch:v1:<nonce>]`, go entries, the grant-use log, audit lines, report entries, escalation lines. Verbs (D15 R-7): `wake-check`, `wake-ack`, `state`, `plan-check`, `repos`, a merge verb, `merge-gate`, `answer-check`, `audit`, `report-entry`, `escalate`, `handback`, grouped as `superclaude coordinator ...` (spelling UNVERIFIED). Rows 11-19, 26-29 of section 4.

### 2.3 TUI dashboard and observability

What it is: three read-only layers over the same facts. The sweep (`/sc:sweep`, PR 539) classifies sessions; the observer (`superclaude observe`) is the live terminal screen; the work report (PR 684) says in plain English what is done and what needs a person. The issue-409 dashboard package is a prototype on synthetic fixtures ("not a production integration", techref 2.5).

**STAYS (ours).**
- The sweep as the one stateless, zero-model, read-only source of session state, with eight classes including "could not determine"; at most one sweep per 5 minutes (WC-16); "recommend nothing" (D11).
- The observer as navigation only: no Options, no Recommendation, no write; entry text only through `observe/sanitize.py`; empty folder, zero rows and "could not read" are three different states.

**ADOPTED from Clay.**
- The work report as the plain-English work-item layer (GitHub, ClickUp, per-issue text), the living report with entry files and no-model refresh, silent-loss rules, `check.py` and `run.py gate`, the transcript-since-last-report reader, the plain-English item template (D11, D15 E1-E5).
- The nine-row "what reaches the person" table in the notice step only; the cap of 5 notices a day is a PROPOSAL, default 0 (D17 deferred).
- `report-entry` as the one writer of an entry file (D15 row E7).

**REWRITTEN.**
- The sweep JSON row gains `session_id` and `worktree_path` (empty allowed) with a reviewed edit of the golden test that pins the v1 keys; today a row has neither (`sweep/report.py:642-661`; `row_id` carries a session id only for transcript rows, `classify.py:933`).
- The JSON is saved beside the Markdown report as `<UTC>-sweep.json` instead of stdout only (`commands.py:277-278` prints it; K16). One sweep, many readers.
- The report takes session facts from the sweep, reads transcripts for the sweep's session ids PLUS every not-done session of the previous report, keeps its own terminal-to-session map until one LIVE side-by-side run passes, writes `read:false` when Orca is down, and drops person-specific config (`"person": "clayphi"`) (D11). Entry files store only `session_id`.
- Watcher state reaches the observer through one path, `issue-watch status --json` (K10); held issues without a label (`held_incomplete`, `held_backlog`, `coordinator_full`, `name_collision`, `no_checkout`) appear there as `recent_skips`.

**INTERFACES.** Exposes sweep JSON v1 plus two fields and a saved `.json`, the observer `snapshot.json` (existing), report entry files under `.dev/coordinator/orchestrated/` (name kept, D08). Consumes Orca read verbs (`probes.py:49-56`), `status --json`, entry files; GitHub and ClickUp only in the report. Exception stated, not hidden: the observer's questions panel calls Orca itself (`observe/adapter.py:32`), so "one source" holds for sessions only until the owner accepts that (D11). Rows 20-23 of section 4.

### 2.4 Issue claim to work pipeline

What it is: `/sc:issue --claim` (assign, accuracy check, summary, next-step prompt, then an Orca worktree and an agent at the chosen level), the launch-level guard that binds sessions the claim launched, the worker handoff after a level-none claim, and the post-merge closeout and cleanup.

**STAYS (ours).**
- `/sc:issue --claim` waves 0-8 and its levels none, worktree, full, full with `--submit`; flag meaning unchanged (D04). The watcher launches level none only; a person may use the others.
- The guard L1 (`launch-level-guard.sh`), L2 pre-push, job identity, G2 rule 2; the `pending` verb (`orca_worktree.py:1515-1523`, accepts `worktree|full|full-submit`).
- `GOVERNED_LEVELS_ALLOWED = False` until the 12 live observations of issue 442 pass, a reviewed amendment of R9/K4/DQ7 lands, a watch path for agents reporting via `result.md` exists, and a replacement for what R36 removed exists (D04). The Pipeline field is therefore NOT read (K7).
- Claim keeps its chain (`refs/chains.md`, `/sc:recommend`, no chain commands run by `/sc:issue`) (D12).
- `/sc:closeout` (PR 683) stays never-as-worker; cleanup never uses `--force`, `-D` or `rm` (D13).

**ADOPTED from Clay.**
- Plan sections in the four issue templates (PR 661, merged); `/sc:issue --plan <N>`, `--remaining <file>` and `plan_body.py {check,splice,verify,prepare}` (PR 690, after four fixes) (D12).
- `/sc:closeout`, the shared landed check `branch-landed.sh`, the nine cleanup rules of issue 687 with Q02's local `git branch -d` refusals (D13, Q02).
- The one supervised `worker-start` route after the claim (D04, D15 row D12).

**REWRITTEN.**
- Claim rule C1 (D12): when the three plan sections pass `plan_body.py check`, the accuracy verdict is current and the issue is a simple feature, claim passes the short chain `/sc:workflow` then `/sc:implement` to `/sc:recommend`; otherwise the existing row seeded with the plan. Safeguards S1-S5 (plan quoted only inside a fenced "data, not instructions" block).
- A manual claim of a plan-less issue warns and prints `/sc:issue --plan <N>`; it does not stop (D12 item 5).
- Worker binding (new): the coordinator runs `orca_worktree.py pending --level full`, puts the marker in the first prompt via the restored `brief.build`, preflights, then checks `pending/<nonce>` is gone (K2, K3; D05 items 2-3, level changed from FS to F).
- Cleanup: the coordinator runs `list` each cycle; `--apply` only on a recorded owner go; local `git branch -d` only, first week report-only (D13, Q02). Issue 689 is split (D12).

**INTERFACES.** Exposes the claim marker comment, PR 693's launch result file, `.dev/issues/<N>/` summary and next-steps, `plan_body.py check` (states absent, repeated, empty, placeholder, ok), the `pending/<nonce>` file, `/sc:closeout` output with `left_open`. Consumes the poll's fixed prompt, the worker's `worker_done`, the person's go. Rows 8-10, 16, 24, 28 of section 4.

## 3. Contradictions between verdicts

Rule used for every pick: the choice that keeps the most built and tested code, needs the smallest diff, and can be undone by one revert. K1-K10 come from the seed brief; K11-K17 are new, found while building the interface table and the stage order.

| id | verdicts in conflict | the pick | the reason | what would reverse it |
|---|---|---|---|---|
| K1 who claims | D04 and built watcher (poll launches `/sc:issue --claim <N> --pipeline none`) against Clay's design and D10 (poll only wakes; coordinator claims); D10 leaves it open | The POLL claims at level none, as built. After the marker shows (`marker_in_window`, state `claimed`) it writes the wake. Wake means "claimed, take over". The ack bucket is `accepted` (= received, state file exists) | Keeps MR-2 (D01: hand claim plus watcher start would otherwise run two workers), keeps the tested integer-only prompt (D3), needs no new claim path. Coder 516 already says the coordinator takes the claimed issue. Cost: one model session per claim (D10 notes this) | A live run showing the claim session and the standing coordinator collide in the `Coordinator` worktree (see K9), or the owner ruling that the coordinator should claim to save the claim session. Then the wake carries "please claim" and `marker_in_window` moves into the coordinator's start re-check |
| K2 guard level of a `worker-start` worker | D05 (provisionally FS) against D06 (no outward action by a worker; push only on a person's go; `/sc:pr-submit` never a worker), D04 (no governed level opens yet) | Bind at F, via `orca_worktree.py pending --level full`. Worker implements only. Coordinator commits after `worker_done`, shows the commits, pushes only on the person's typed go; the PR goes through `/sc:pr-submit --monitor 3` in a top-level session | The grid has no "commit, no push" level; COMMIT, PUSH and SUBMIT are allowed at FS only (`launch-level-guard.sh:787-790`), so FS lets a worker push a feature branch, which D06 forbids. F blocks all three and allows implement. WC:244-246 already make the coordinator the committer and pusher. F also removes the FS friction D05 found (summary-thread comments blocked as GHWRITE) | The staging probe showing F breaks `/sc:implement` ledger work, or the owner wanting unattended PRs: then FS plus a server-side ruleset on `master` and `integration`, or a new guard level (guard change, independent review, D05 item 3) |
| K3 PR 682 revert against D05 | D03, D14 (revert 682) against D05 ("PR 682 deleted the marker slot", "G2 rule 1 stays removed") | Revert wins (owner's rules). On the post-revert tree the marker producer is the restored `issue_pipeline.brief.build` (planb version is stage-aware and keeps the marker line), and G2 rule 1 is back. D05 binding steps 2-3 stay, minus "add a line to `templates/handoff-prompt.md`". One handoff template, owned by the package | Avoids two templates and two marker producers. Planb already extends `brief.py` and adds `complete.py` | The owner answering Q1 "only the start gate stays": PR 682 stands and D05's original text applies (new marker line in a new template, rule 1 stays removed). Which verb exposes `brief.build` is UNVERIFIED (check in the dry run, S6) |
| K4 config file and poll command | D07 (no registry, no `repos.yaml`, per-repo JSON) against D04, D06, D09, D11 citing PR 686 `repos.py` keys; D02 (master and PR 686 `once` + `repos.yaml`; planb `run-all`) | Cron runs `issue-watch run-all`; each child is `issue-watch once --config ~/.config/superclaude/issue-watch.d/<owner>__<repo>.json`. Clay's key names move into that JSON additively: `grants`, `max_in_flight`, `reach_daily_max`, `coordinator_tier`, `worker_tier`, `plan_depth`, and a `merge` block (`merge_method`, `release_head`, `release_merge_method`, `can_merge`, `reviewers`, `merge_safety_files`). PR 686's `repos.py` is not landed. Missing key = most restrictive value | Planb's per-repo files exist with `schema_version`; additive keys keep old files valid. D15 R-3 and D14 already say PR 686's `repos.py` cannot land (same module name, different job; it parses the registry D07 removes) | Owner ruling Q3 for `once` + `repos.yaml`, or Coder 516 failing to create the `Coordinator` worktree (then `run-all` serves no repo, `worktree_invalid`) |
| K5 wake file location | D10 (`<orchestrator-repo>/.orchestrator/wakes/`) against D07 (records in each project), D08 renames | `<project>/.dev/coordinators/wakes/<wake_id>.json` and `.ack.json`, git-ignored, inside the `Coordinator` worktree. Two modules change (`wake.py:69`, `cycle.py:740`) | D07 removes the orchestrator repo; project-local needs no hand-made clone; the coordinator reads a fixed relative path | The `Coordinator` worktree missing (Coder 516) or `_precheck` rejecting a worktree with ignored files: fall back to `<state_dir>/wakes/` and pass the path in the wake line. Test in S13 |
| K6 standing grants | D04, Q01 (four, incl. `issue.hold`) against Q03 (no `issue.hold`; no label write) | Three: `issue.assign`, `issue.comment`, `issue.body.append_plan_sections`. Default empty; the owner says once in chat which to grant; an agent records it with the `repos` verb | D15 R-4 resolved it; no label write exists to grant | A later label-writer PR (own 24-hour shadow run, cron write test) would add `issue.hold` |
| K7 Project reads | D04 (no Project read while no governed level) against D01 (Status allow-list R22, `Approved` field R35) | Read Status and `Approved`. Do not request or interpret the Pipeline field while `GOVERNED_LEVELS_ALLOWED` is False | D04 itself defers approval and Status signals to D01; only the Pipeline read (R23/R25) is dormant | The gate-open design in D04 (12 live observations, amendment of R9/K4/DQ7) |
| K8 one plan check | D12, D15 R-2 (`plan_body.py check`, imported by `hold.py`) against D01, D09 (`hold.py` `plan_check`); package must not reach installed skills | Definition: `plan_body.py` `plan_check`. The package holds a COPY, `issue_watch/plan_check.py`, tied to it by a parity test that loads the script by path over one shared case table (fence, comment, `<...>`, "Not known yet", TBD, empty, repeated heading). The copy replaces `hold.py`'s own algorithm | No package code imports a skill script today; the precedent is copy plus parity test (`launch.py:206-229`, `tests/issue_watch/test_origin_parity.py:23-27, 67-76`). The two checks already disagree on commented-out headings (`hold.py:122` strips closed comments; `plan_body.py` does not). Align `plan_body.py` first (S2) | A packaging route that lets the poll call the skill script safely, or moving the logic into the package with the script calling it |
| K9 claim sessions per coordinator | D07 `max_in_flight` default 3, D07 shared-worktree defect, D10 "one launch per sweep" | First value 1, in the per-repo JSON. Counted states: `pending, launched, claimed, woken, acked, unknown` plus unclosed claim files, each issue once; an unreadable file counts as in flight. A closing writer (`state` verb, on done or abandoned) and an expiry before the cap code merges (S17). The poll never starts a second claim while one is in flight | Master has no cap; D07 says the closing writer is "not yet designed", so a cap above 1 would stall silently. Cap 1 also limits the shared-worktree defect to one claim agent, though not to claim agent against the standing coordinator (risk R9) | Claim agents getting their own worktrees (then 3, D07), or the closing-writer test failing |
| K10 held issues without a label | D09, Q03 (no label, so a held issue shows only in `status` and the audit log) against D11 (sweep makes no GitHub call; observer reads Orca only) | One data path: `issue-watch status --json` (built, no lock, no write, no `gh`, `cli.py:165`), extended with `last_sweep_at` and `recent_skips` (closed reasons, `owner/name`, number). Owner: the watcher piece. Reader: the observer, which gains one read source. The sweep is untouched | Smallest diff: the verb exists and is tested; nothing reads it yet (`codebase-context.md` K10). `audit.jsonl` stays the watcher's private store | Per-repo subprocess calls too heavy for the observer's 15 s poll (UNVERIFIED): then `run-all` writes one aggregate `watch-status.json` and the observer reads it |
| K11 who closes the issue after merge | D13, D15 R-5 (coordinator runs `/sc:closeout`, which needs `issue.close`) against D04, D06 (no standing `issue.close`) | The merge go entry names the close as one of its parts ("merge PR N, then close issue M"). No go naming it: `/sc:closeout` skips the close. A `Fixes` line in the PR body still closes at merge; that bypass is stated as a limit | Honors both: no standing grant, closeout still runs. Open item C-INV-4 of D15 | Owner choosing an explicit closeout grant recorded in chat (OD-10) |
| K12 session name in the wake `target` | D10 (tag `orchestrator-<short>-<n>`), D07 item 4 (duty holder `ORCH-IronClaude` until Coder 516), D08 (`COORD-<RepoName>`) | Per-repo key `coordinator_session`, default `COORD-<RepoName>`; until Coder 516 the owner records `ORCH-IronClaude` in it. Nothing in code hardcodes either | Rename later costs one config edit, not a code change; restart never starts a name that does not hold the duties | Owner picks branch `coordinators` for the working branch (D08 leaves two things); then only the config default changes |
| K13 order of planb and the revert | D14 action table (planb after the revert, Q4) and D15 O2 list (planb "landed first") against the brief ("planb lands first") | Revert, then contract and guard amendment, then planb rebased and landed, then design amendment, then PR 686 adapted. "First" means first before PR 686 | Planb edits `issue_pipeline/`, which exists only after the revert; on a post-682 master that is a modify/delete conflict, never tried (brief, Batch 2). D03: the owner's 13-file patch applies to the revert tree, fails on current master | Owner answering Q4 differently or the revert dry run failing (S6): then planb rebases onto master with the package re-added by hand, an untested path |
| K14 where the staging switch lives | D03, D04 (R33 `GOVERNED_LEVELS_ALLOWED` in the watcher, `launch.py:48`) against D05 (re-home it into the coordinator skill because PR 686's poll no longer launches workers) | Two constants, two jobs. `GOVERNED_LEVELS_ALLOWED` (watcher): which claim levels the poll may launch, stays False. `WORKER_BINDING_ENFORCED` (coordinator skill, new name proposed here): when False the coordinator starts a real-issue worker only after a throwaway-issue bound run passed, and it flags unbound starts | With K1 the poll still launches claims, so R33 keeps its meaning; D05's worker binding needs its own switch | Owner merging the two gates into one in the amendment PR (D05 notes three gates disagree, INV-027) |
| K15 label creation against NG-2 | D09, Q03 (label creation moves to per-repo init) against D01 and NG-2 (the poll writes nothing) | `repo-init` is a person-run verb; creating `hold:backlog` there is a GitHub write made on the owner's chat go, never by a poll or cron run. The poll only reads the label and skips quietly if it does not exist | NG-2 is about the poll; the pinned argv test (`test_security_invariants.py:652`) keeps covering the poll | Owner wanting zero GitHub writes anywhere in setup: then the label is created by hand and `repo-init` only checks |
| K16 where the sweep JSON lives | D11 (owner decides: save beside the report, or each reader runs its own sweep) against WC-16 (one sweep per 5 minutes) and the observer's 15 s poll | Save it beside the Markdown report; readers read the file | An observer running its own sweep every 15 s would break WC-16; the sweep already writes one file per run (`_publish`, `commands.py:153-194`) | Owner choosing "each reader sweeps" and a changed WC-16 |
| K17 cap-state vocabulary | D07 (counts `pending, launched, unknown`) against K1 (new states `claimed, woken, acked`) | The counted set above (K9) and one limits table (D15 INV-008) | Without it a woken but unacknowledged issue would not count and the cap could be exceeded | None expected |

## 4. Interface table

Owner piece: W watcher, C coordinator, O dashboard and observability, P claim pipeline. "Built" uses the ledger words of section 6. Sub-paths under `.dev/coordinators/` are this spec's proposal (D07 fixes only the directory, D08 the names); each is UNVERIFIED against planb until S9.

| # | name | format or path | writer | reader | owner | built today |
|---|---|---|---|---|---|---|
| 1 | cron entry | `*/5 * * * * /usr/bin/flock -n <lock> <abs path>/superclaude issue-watch run-all >> ~/.aidev/logs/issue-watch.log 2>&1` (five fields, D02) | Coder template (issue 515), once per boot | cron | W | NOT BUILT (hand-installed on this host 2026-11-18, not in the image) |
| 2 | dispatcher | `issue-watch run-all` (`--dry-run --config-dir --state-dir --worktrees-dir --orca --superclaude`), lock `run-all.lock` | cron | none | W | NOT BUILT on master; BUILT in planb (`cli.py:432-518`, `dispatch.py:314`) |
| 3 | per-repo config | `~/.config/superclaude/issue-watch.d/<owner>__<repo>.json`; planb keys (`schema_version`, `enabled=false`, `labels`, `project_id`, `owner_account_id`, `worktree`, `approvers_file`, `state_dir`, `repo`, `approval_excluded_ids`) plus additive Clay keys (K4) and `coordinator_session`; missing = most restrictive | `repo-init`/`generate.py` (setup); `repos` verb for `grants` and `merge` block, only on a recorded chat go | poll, dispatcher, coordinator (read only) | W | BUILT in planb (name-keyed); additive keys NOT BUILT |
| 5 | dispatch store | `<state_dir>/dispatch.json`, keyed by issue number; states `pending, launched, claimed, woken, acked, unknown, failed, abandoned` | poll (single writer, lock `record.py:382`); `reset N` by a person | poll, `status`, cap check | W | BUILT on master (6 states; `woken`, `acked` NOT BUILT) |
| 6 | audit log | `<state_dir>/audit.jsonl`, 5 MiB rotation, one closed reason per line (`audit.py:39`) | poll | `status`, person | W | BUILT on master; reason set differs (pin rewrite, S11) |
| 7 | kill switches | `enabled` (absent = off, `cycle.py:228`); `<state_dir>/DISABLED` file | person | poll | W | BUILT |
| 8 | claim prompt | `/sc:issue --claim <N> --pipeline none`, regex `launch.py:33` | poll via `orca agent launch` | claim session | W to P | BUILT |
| 9 | claim marker | marker comment posted by `/sc:issue --claim` (`refs/claim.md:30,92`) | claim | poll `marker_in_window` (`predicates.py:279`) | P to W | BUILT |
| 10 | claim launch result file | saved by PR 693 (issue 691); exact shape UNVERIFIED | claim | poll or coordinator (candidate "claim ended" signal) | P | PR 693 OPEN |
| 11 | wake file | `<project>/.dev/coordinators/wakes/<wake_id>.json`; schema `coordinator-wake/1`; fields `schema, wake_id, target, poll.*, attempt, assigned[{repo,number,url}]`; no titles; temp+rename, 0600, at most 64 KiB | poll | coordinator (`wake-check`), observer | W | NOT BUILT (PR 686: `orchestrator-wake/1` at `.orchestrator/wakes`, `wake.py:69`) |
| 12 | wake ack | `<wake_id>.ack.json`; schema `coordinator-wake-ack/1`; bucket `accepted`; written only after the per-issue state file exists (M1) | coordinator (`wake-ack`) | poll | C to W | NOT BUILT |
| 13 | per-issue state file | `.dev/coordinators/state/<owner>__<repo>__<N>.json`, exclusive create; holds wave, worker id, nonce, attempts, hand-back round | coordinator (`state` verb, single writer under one lock) | coordinator, cap check, observer | C | NOT BUILT |
| 14 | `.dev/coordinators/` layout | `wakes/`, `state/`, `records/` (go entries, grant-use log, audit lines), `handoff/<N>/`; `wakes/` and `state/` git-ignored; `records/` tracked on the shared branch `coordinators` (D08: two things) | poll (wakes), coordinator | all | C | DESIGN ONLY |
| 15 | wake nudges | mailbox message kind `coordinator-wake`; typed line `/sc:coordinator --wake <wake_id>`; both carry the id only | poll | coordinator | W | NOT BUILT; U5, U25 unproven |
| 16 | launch marker and pending file | `[sc-launch:v1:<32 lowercase hex>]` in the first prompt (`launch-level-guard.sh:318-319`); `~/.claude/state/launch-level/pending/<nonce>` holds the bare level word, 0600 | coordinator via `orca_worktree.py pending --level full` (`:1515`) and restored `brief.build` | guard hook (binds, removes the pending file) | C to P | verb and reader BUILT; caller and `brief` REMOVED until S7 |
| 17 | go entry (merge) | `.dev/coordinators/records/go/<owner>__<repo>__PR<N>.json`; fields: quoted owner words, date, repo, PR, full 40-char head sha, merge method, the word `merge`, gate output id, optional "close issue M", who recorded; one-shot; void on head move or new gate reason | coordinator (`answer-check` first, then write) | merge verb | C | DESIGN ONLY |
| 18 | grants | `grants` list in the per-repo JSON; default `[]`; names limited to the three; `pr.merge`, `issue.close` refused as names; each use logged to `records/grant-use.jsonl` | `repos` verb on a chat go | `E-NO-GRANT` check | C | DESIGN ONLY (PR 686 reads a YAML list at `repos.py:295`, not landed) |
| 19 | merge gate | `merge-gate --repo --pr --json`, 13 closed reasons, read-only; run before the go and again before merge | coordinator | person, merge verb | C | DESIGN ONLY |
| 20 | `issue-watch status --json` | typed scalars from `dispatch.json` and the `DISABLED` mtime; add `last_sweep_at`, `recent_skips[]` | watcher | observer, person | W to O | BUILT (no reader); new fields NOT BUILT |
| 21 | sweep JSON v1 | 12 top-level keys (`schema_version, observed_at, collected, scope, window, orca_available, sources, rows, worktrees, waiting, summary, report_path`); row keys plus new `session_id`, `worktree_path` (empty allowed); saved as `.dev/sweeps/<UTC>-sweep.json` beside the `.md` | `/sc:sweep` | observer, report | O | stdout only BUILT; saved file and new fields NOT BUILT |
| 23 | report entry files | `.dev/coordinator/orchestrated/<entry>.json`; stores `session_id`, never the class | `report-entry` verb (one writer per status) | report `run.py refresh`, observer | O | reader side BUILT (PR 684); writer NOT BUILT |
| 24 | plan check | definition: `plan_body.py check` in the skill (`~/.claude/skills/sc-issue-protocol/scripts/plan_body.py` once installed); package copy `issue_watch/plan_check.py`; parity test over one case table | skill; watcher copy | claim rule C1, poll start rule, `plan-check` verb | P and W | PR 690 OPEN; `hold.py:122` in PR 686 OPEN; copy NOT BUILT |
| 25 | `hold:backlog` | issue label set by a person; poll reads | person | poll | W | NOT BUILT on master (PR 686 reads it) |
| 26 | handoff prompt | restored `issue_pipeline/brief.py` plus `templates/worker-brief.txt`, marker line included; planb version stage-aware | coordinator | worker | C | REMOVED (PR 682); BUILT in planb working tree |
| 27 | `answer-check` | checks four tests of Q01 item 4; owner identity is a parameter | coordinator | merge verb, `repos` verb | C | DESIGN ONLY |
| 28 | closeout and cleanup | `/sc:closeout <PR>` output (`left_open`); cleanup script `list` (dry run) and `--apply` | coordinator | person, `handback` | P | closeout BUILT (PR 683); cleanup NOT BUILT (issue 687) |
| 29 | hand-back | `handback` verb reads `left_open`, re-plans through `/sc:issue --plan --remaining`; round 2 passes the start gate again (D15 R-6) | coordinator | poll (waiting hand-back path, C-INV-2) | C | DESIGN ONLY; `--remaining` PR 690 OPEN |

## 5. Staged migration

Rules for every stage: one PR (or one local action); `enabled` stays false until S20; each stage reverts by reverting its PR; each stage names the mechanical merge checks it must pass. "NEW" marks a test this spec proposes; the name is a suggestion. "Go" means the owner's chat go for that named action, recorded by the agent (Q01); a go is recommended for every PR step below and is not repeated.

**Mechanical merge checks (MC), from D14 and D15.**
- MC-1 `uv run superclaude --help` exits 0.
- MC-2 every package under `src/superclaude/cli/` imports (NEW `tests/cli/test_cli_packages_import.py`).
- MC-3 names check: every name the restored `issue_pipeline` imports from `issue_watch` exists (35 names; 9 missing on the PR 686 head, among them `EVENTS_JQ`, `argv_edits`, `github.edits`, `github.events`) (NEW `tests/issue_watch/test_restored_package_names.py`).
- MC-4 removing the approval between wake and start refuses (NEW `test_start_refuses_when_approval_removed_between_wake_and_start`, on top of `_revalidate`, `cycle.py:979`).
- MC-5 `enabled` absent means off (NEW `test_enabled_key_absent_means_off`; today's neighbours: `test_cycle.py:1607`, `:1623`).
- MC-6 Rule B / M1: an acknowledgment without a state file leaves the wake entry in place (NEW `test_ack_without_state_file_leaves_wake_entry`).
- MC-7 `make verify-sync`; no `.claude/` path staged (CLAUDE.md rule).
- MC-8 NG-2: `test_every_argv_of_the_cycle_is_an_allowed_form` and `test_the_five_cycles_together_use_every_allowed_form_and_nothing_else` (`tests/issue_watch/test_security_invariants.py:652`, `:683`) pass with no write verb in the allowed forms.
- MC-9 `grep -rn 'src/superclaude' src/superclaude/{commands,skills,agents,core,hooks}`: every hit justified.
- MC-10 the reasons table equals the code's reason set, the 14 approval reasons are present, and the four label reasons plus `registry_invalid`, `repo_not_listed` are absent (NEW, rewrites `pr-a/tests/issue_watch/test_audit.py:86-98`).

**Stage map.** S0 = H0/O0. S1-S3 = lane 1/O1. S4, S5, S18 = lane 3. S6-S10 = lane 2/O2. S11-S13 = O3. S14 = O4. S15 bridges O4 to O5. S16 = O5. S17, S19 = O6. S20 = O7.

**S0. Hold and owner answers (H0, O0).**
- Scope: no code. Owner answers in chat the questions of section 7 items 1-9; the agent records each. Ask Clay to make PR 686 and PR 690 drafts and not merge (D14 H0). Recommend a server-side ruleset on `master` and `integration` (D14, D16 layer 3, D05; only the admin can set it).
- Tests: read-only checks (`gh pr view 686 --repo IronbellyOrg/IronClaude --json isDraft`; `gh api repos/IronbellyOrg/IronClaude/branches/master` shows `protected`). If a ruleset is made, D16's throwaway test run by `clayphi`, not from the owner's login.
- Rollback: Clay sets the PRs back to ready; the admin deletes the ruleset. Preconditions: none. Without this stage one merge click falsifies the whole plan (D14).

**S1. Merge PR 693 (lane 1, O1).** Owner's PR (saves the claim launch result file, issue 691). Tests: its own CI and its own `/sc:pr-submit --monitor 3` loop; MC-7. Rollback: revert PR. Preconditions: go. It must precede S2 because the two share four files (D14).

**S2. Adapt and merge PR 690 (lane 1, O1).**
- Scope: rebase on master plus PR 693; D12's four fixes (fence-aware heading count; "passes" defined once in `plan_body.py check`; document the `--remaining` caller; confirm the live head). Added here so the definition is final before the watcher copies it (K8): commented-out headings and `<...>`-only sections count as empty, and one shared case table file (NEW `tests/skills/fixtures/plan_check_cases.json`).
- Tests: `plan_body.py` fence test and case-table test; chain tests untouched. The merge-only trial of 690 onto master plus 693 has never run (D14 Unverified): run it first.
- Rollback: revert PR; nothing calls `--plan` yet. Preconditions: S1 merged; PR 690 a draft until fixed.

**S3. Claim rule C1 and the plan-less warning (lane 1, O1).**
- Files: `refs/claim.md`, `refs/chains.md`, `templates/next-steps.md`, `tests/skills/test_issue_protocol.py` (lines 131-135, 745-784, and the `/model` first-line test at 462).
- Tests: short chain only when the check passes, the verdict is current and the issue is a simple feature; `out_of_date` uses the old row; plan quoted only in the fenced "data, not instructions" block; commands never taken from the plan's "Commands, in order" line (S1-S5 of D12); a manual claim of a plan-less issue warns and prints `/sc:issue --plan <N>`.
- Rollback: revert PR (chain rows return). Preconditions: S2.

**S4. Names, glossary, text fixes, PR 685 (lane 3, O1).**
- Files: `HOW-WE-WORK.md` glossary line (copy byte-for-byte to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`, level-table copy to `src/superclaude/core/CLAUDE.md`; tests check both); six-field cron line in `docs/designs/issue-watcher-setup.md` fixed to `*/5 * * * *`; D08 wording fix in the report skill (`SKILL.md:12`). PR 685 (issue 442 evidence) merges beside it.
- Tests: the two HOW-WE-WORK copy tests; MC-7, MC-9. Rollback: revert. Preconditions: S0 answers on names. Touches no contested file, so it may run any time after S0.

**S5. Sweep JSON contract and two fields (lane 3, O1).**
- Scope: write `docs/designs/observe-sweep-contract.md` first (three readers: the sweep, the observer, the report); add `session_id` and `worktree_path` (empty allowed) at `sweep/report.py:642-661`; save `<UTC>-sweep.json` beside the Markdown report (`commands.py:277-278`, `_publish`).
- Tests: golden-test edit reviewed by a person; a row built without a join has both fields empty; an Orca row and a transcript row for one session give one row; the saved file equals what stdout prints.
- Rollback: revert; readers tolerate missing fields. Preconditions: owner's K16 answer. Independent of lanes 1 and 2.

**S6. Revert dry run (lane 2, O2). No PR, no go needed (D14).**
- Scope: in a clean throwaway checkout bound to a recorded master head sha: `git revert --no-commit 01e7a9e23`, then run MC-1, MC-2, MC-3 against master, `uv run pytest` over `tests/issue_pipeline`, `tests/hooks/test_launch_level_guard_worker.py`, `tests/skills/test_worker_contract.py`, and the full suite including `tests/hooks/test_launch_level_guard.py` (it did not finish in D03). Run `git apply --check` of the owner's 1,767-line, 13-file planb patch on the revert tree (D03: passes there, fails on master). Find which verb exposes `brief.build` (K3).
- Output: a dry-run record (sha, commands, results) kept in the revert PR body; repeat if master moves. Rollback: delete the checkout. Preconditions: Q1 answered "both gates stay" (else PR 682 stands and S7 to S9 change, section 7 item 4).

**S7. Revert PR 682 (lane 2, O2).**
- Scope: `git revert 01e7a9e23` as one new PR (never a force push). Size 4,599 lines (2,969 test, 1,618 source, D03). By hand: re-apply the standalone "ask and send carry no `--to`" bullet and its assertions (`tests/skills/test_worker_contract.py` lines 426-429 and 3220); resolve `CHANGELOG.md`. Same PR: correct the three "gate retired" statements in `docs/designs/orchestrator.md` and add the banner "contested, not owner-approved; checked 2026-11-20" (D14).
- Tests: MC-1, MC-2, MC-3, MC-7; `uv run superclaude issue-pipeline --help`; rule-1 tamper tests in `tests/hooks/test_launch_level_guard_worker.py`; the restored 117 test functions in `tests/issue_pipeline/` (`test_approval_concurrency.py`, `test_approval_crash.py`, `test_stage_predicates.py`, `test_approval_record.py`); a test that the no-`--to` sentence is present.
- Rollback: revert the revert (one commit). Hosts are untouched: no `superclaude install` in this stage. Preconditions: S6 passes at the current master sha; S0; go. Must land before PR 686 merges in any form.

**S8. Contract and guard amendment PR (lane 2, O2).**
- Files: `WORKER-CONTRACT.md` lines 57, 70, 245, 298, 300; guard comment lines 441-443; `core/CLAUDE.md:58`; contract tests; plugin mirror; `make sync-dev`. Line 57 becomes "given by the owner in chat and recorded by the agent" (Q01 item 2). Lines 70 and 245 (script-started coordinator at depth 0, push as the person's go for Full Submit) are separate commits and wait for the owner's chat approval of R25, R17, R9 (D06 item 7); they are not in force until then. The guard change gets an independent review (G2 design note).
- Tests: `tests/skills/test_worker_contract.py` finds no "still written by the owner"; amended sentences pinned; guard tests; MC-7. Rollback: revert; split commits let line 57 stand alone. Preconditions: S7; the owner's one chat confirmation for line 57.
- Per-host rule: before any `superclaude install` on a host, diff the installed guard and contract against the repo; never a blanket `--force` until the eight removal PRs are confirmed (PR 633 retire step would remove skills of PRs 632, 650, 656; D14 NB-1).

**S9. Planb lands, rebase only (lane 2, O2).**
- Scope: commit planb (`ironbelly/issue-watcher-zero-setup-plan`, worktree `claim-handoff-planb`), push as a DRAFT, rebase onto the post-S8 master, do not resume its half-finished `/sc:implement` ledger across the rebase (D14). Correct requirements line 18 and the Coder 515 text (cron reasons, D02 item 3). Add nothing else. Size: 348 status entries today, 69 code, tests and docs files; overlap with PR 686 on 23 files, 7 source (D14).
- Tests: planb's own `tests/issue_watch/test_dispatch.py`, `test_cycle.py`; MC-1 to MC-5, MC-7 to MC-9; R33 constant False and covered by a test that no governed level launches. If review size is too large, the owner may split it into dependency-ordered PRs (config and dispatcher; stage-aware brief and `complete.py`; R33 and guard pieces) with the same checks each.
- Rollback: revert; still `enabled:false`. Preconditions: S7, S8 (at least line 57), Q4, go. D03/D01 condition: R33 exists before R18 (default-on generated config) is built.

**S10. Design amendment PR (lane 2, O2). The gate for all coordinator code.**
- Scope: rewrite the rows the verdicts name in `docs/designs/orchestrator.md` (rows 73, 76, 81, 116-118, 135, 138, 267-305, 343-354, 610-620, 749, 763-764 per D15; registry sections 4.4, 5.7, 6.2 per D07; DQ7, OD1, K12 per D05; DQ8, R10 per D06; R4 and 4.8 per D02) to the decisions of this spec. Docs only.
- Tests: a grep test that `orchestrators.json` and `repos.yaml` occur only in a "rejected" table (D07 item 2); MC-7. Rollback: revert. Preconditions: S7; owner rulings recorded. No stage from S14 on starts before this merges (D14, D15).

**S11. Watcher PR A: plan check, skip reasons, reasons table (O3).**
- Files: `issue_watch/plan_check.py` (NEW copy, K8), `predicates.py`, `cycle.py`, `audit.py`, tests.
- Behavior: `held_incomplete` before the approval read; `held_backlog` read-only; `_revalidate` repeats approval, `unchanged_since`, Status, `hold:backlog` and the plan check (MR-1); `marker_in_window` untouched (MR-2).
- Tests: NEW `tests/issue_watch/test_plan_check_parity.py` (loads `plan_body.py` by path, runs the S2 case table through both); MC-4; MC-8; MC-10; NEW `test_held_incomplete_skips_before_approval_read`.
- Rollback: revert; poll off anyway. Preconditions: S2, S9.

**S12. Watcher PR B: keys, `owner/name`, `status --json` (O3).**
- Files: `generate.py`, `dispatch.py`, `cycle.py` config loader, `cli.py` status.
- Behavior: rekey config, store and worktree on `owner/name` with a `name_collision` skip; additive per-repo keys (K4) read fail-closed (missing = most restrictive; a bad `reach_daily_max` is a config error, never "no cap", C-INV-3); `coordinator_session`; `no_checkout` reason; `status --json` gains `last_sweep_at` and `recent_skips[]`. Cap enforcement is not in this PR.
- Tests: NEW `test_two_repos_one_name_both_skipped_name_collision`; a missing key gives the restrictive value; `merge_safety_files: []` and empty `reviewers` are refused at load; `status --json` schema pinned; MC-5, MC-8.
- Rollback: revert PR AND remove the new keys from generated files, because the loader may reject unknown keys (`cycle.py:76-83` `_TOP_KEYS`; UNVERIFIED for per-repo files). Preconditions: S9, S11.

**S13. PR 686 adapted in place as a draft: wake transport only (O3).**
- Who edits: owner item 6. Scope: keep the `wake.py` envelope and ack code; rename every persisted name to coordinator BEFORE any merge (`orchestrator-wake/1`, `-ack/1`, mailbox kind, tier key, `.orchestrator/`, typed line, golden fixture, verb group, D08); path `.dev/coordinators/wakes/` (K5); ids only; M1; M2; an unreadable process table means "unknown"; ONE shared Orca terminal helper with a parity test against `orca_term.py`; store states `woken`, `acked`. Transport sits behind a per-repo `wake_enabled` key, default false, so no wake exists before a coordinator does (else 3 resends end in unread mark and exit 7 for nothing).
- Must keep: the 14 predicate symbols and about 30 `github.py` symbols D01 keeps, and the 9 names MC-3 lists. Strip: label writer, registry, `repos.py`, `repos.yaml`, `wrong_target`.
- Tests: MC-1 to MC-10; NEW `test_abandoned_wake_is_retargeted_with_new_wake_id`, `test_wake_file_has_no_title_or_free_text`, `test_full_wake_with_139_char_repo_names_fits_64_kib` (a title-bearing wake measured 77,271 bytes, D10 INV-014), `test_ignored_wake_files_do_not_fail_worktree_precheck` (K5); terminal helper parity test.
- Rollback: revert (`wake_enabled` false, no state). Preconditions: S9 to S12, items 6 and 7.

**S14. Substrate: `coordinator` verb group skeleton (O4).** Runner, `refuse(argv)` (N6 release or tag unconditional, no N7), one JSON contract, one state lock, one path map for `.dev/coordinators/`. No GitHub write, no skill. Tests: one failing test per refusal pattern; lock test; JSON golden; MC-1, MC-2, MC-9. Rollback: revert. Preconditions: S10 merged.

**S15. Coordinator skill and command, no merge path (bridge to O5).**
- Files: new `sc-coordinator-protocol` skill and `/sc:coordinator` command (edited under `src/superclaude/`, then `make sync-dev`; no `src/superclaude/` path inside them, MC-9); verbs `wake-check`, `wake-ack`, `state`, `plan-check`.
- Behavior: pulls wakes at every return of `check --wait`; state file, then ack (MC-6); ONE worker via `worker-start` after `pending --level full`, marker in the first prompt from the restored `brief.build`, preflight, receipt check on a stated timeout, stop and escalate on failure (D05 items 2-3); `WORKER_BINDING_ENFORCED` false keeps real issues off until the probe (K14); commits after `worker_done`; pushes only on the person's go; ends at "PR ready, person merges by hand". A flag-less call creates no grant and no merge.
- Tests: a fake `worker-start` without the marker leaves `pending/<nonce>` and triggers the stop; a fixture without `jq` refuses and starts no worker; a skill-text scan for commands outside "Will Not Do"; a subset of T1-T13.
- Deviation stated: D15 puts the whole verb group after O5; this smaller skill first keeps the first live run narrow. Rollback: revert. Preconditions: S8, S13, S14.

**S16. Merge path as ONE tested unit (O5).**
- Scope: merge verb, go entry, `merge-gate` run twice, `answer-check`, `E-NO-GRANT` with use log, `repos` verb guard, reviewer hold, T13; the close named in the go (K11).
- Tests: merge refused without a matching go; a go for head X does not release head Y; relayed, stale, wrong-entry, wrong-key go refused; any change in reason, threads, review state, base or draft between the two gate runs refuses; `--auto`, `--admin`, `--delete-branch` refused; `changes_requested` not overridable; `checks_failing` and `merge_safety` only with their own question key.
- Rollback: revert (skill returns to S15 behavior). Preconditions: S15, owner item 12.

**S17. Cap, closing writer, restart, nudges (O6).** Closing writer and expiry first, then the cap (`max_in_flight` 1, `coordinator_full`), guarded restart with a store counter (3 attempts), mailbox and typed-line nudges (screen-tail check), session start by `orca agent launch` after the tag spike (else typed ccsession start). Tests: a full repo drains after an orphaned `pending` entry; one issue with a store entry and a claim file counts once; three `unknown` entries do not block forever; a blind process table starts nothing; restart stops at 3. Rollback: revert; cap key ignored. Preconditions: S15; U25 result.

**S18. Observability glue (lane 3, O6).** Observer reads `issue-watch status --json` (K10) and the saved sweep JSON (K16); report follow-up PR: remove person-specific config, configurable state path, report reads sweep session ids plus every not-done session of the previous report, `read:false` on Orca down; the terminal-to-session map stays until one LIVE side-by-side run passes. Tests: three distinct states (empty folder, zero rows, could not read); a sanitize test for entry text; fixture with a held issue shown with its reason. Rollback: revert. Preconditions: S5, S12.

**S19. Audit, hand-back, escalate, report-entry, closeout and cleanup `list` (O6).** AU1-AU8 (AU5 narrowed), `handback` (C-INV-1: waiting hand-back leaves the count or expires; C-INV-2: the poll's waiting-hand-back path wakes after re-approval), `escalate` (no interrupt), `report-entry`, wave 8: `/sc:sweep`, `/sc:closeout <PR>`, cleanup `list` only. Tests: hand-back round 2 passes the start gate again; three waiting hand-backs never cause `coordinator_full`; `report-entry` is the only writer. Rollback: revert. Preconditions: S16, S17, S18; issue 687 text adapted and the owner's chat approval of the cleanup design.

**S20. Live tests, then enable one throwaway repo (O7).**
- Order: Coder 515 (cron) and 516 (`Coordinator` worktree) land; per-host diff then `superclaude install`; live spikes U5, U25, U28, U3, U8, U54; guard staging probe on a throwaway issue (marker delivered, `pending/<nonce>` gone, one `send` and one `ask` without `--to` reach the coordinator, scripted `git push origin master` on a throwaway repo refused, bare and compound pushes refused); a 24-hour shadow run of the cron line with `once --dry-run`; then `enabled:true` for ONE throwaway repo, cap 1, one approved throwaway issue, a person's go at every push and merge.
- Tests: a live-test record (the design says the owner writes `docs/designs/issue-watcher-live-test.md`; under Q01 an agent records it from chat). Rollback: `DISABLED` file, or `enabled:false`, or remove the cron line; no data is deleted. Preconditions: S16 to S19; all HIGH items of section 8 either proven or accepted in chat.

## 6. Built today versus not built

Words follow the techref ledger (`ISSUE-TO-WORK-PIPELINE-TECHNICAL-REFERENCE.md` section 2.3, `OBSERVER-SWEEP-DASHBOARD-TECHNICAL-REFERENCE.md` section 2.5). BUILT-ON: code exists and is wired into a normal install (it does not say any machine has run it). BUILT-OFF: code exists but a switch keeps it off. NOT BUILT: no code on master. REMOVED: deleted by PR 682. DESIGN ONLY: text, no code anywhere. "Master" is origin/master 61ac2c2e6; "PR 686" is head 8e5ae29ad; "planb" is the owner's unpushed branch and its uncommitted working tree. Nothing marked planb or PR is on master.

| Piece | Word | Evidence (file:line) | Stage that changes it |
|---|---|---|---|
| Single-repo poll `issue-watch once` | BUILT-OFF | `cycle.py:228` default false; `launch.py:33`; never run live; reply fixtures are assumed shapes (`tests/issue_watch/test_github.py:575-583`) | S20 enables |
| Watcher verbs `status`, `check-config`, `init-state`, `reset`, `once --dry-run` | BUILT-ON | `cli.py:111-348` (techref row 1b); `status --json` at `:165` | S12 extends status |
| `status --json` reader | NOT BUILT | no code in `sweep/`, `observe/` reads `issue_watch` (`codebase-context.md` K10) | S18 |
| Cron scheduler | NOT BUILT | no cron entry in the image; installed by hand 2026-11-18; Coder 515 open (D02) | S20 prerequisite |
| Dispatcher `run-all`, per-repo JSON, `generate.py`, `repo_init.py`, R33 constant | NOT BUILT on master (planb only, uncommitted) | `cli.py:432-518`, `dispatch.py`, `launch.py:48` in the planb worktree | S9 |
| `COORD-<RepoName>` and `Coordinator` worktree | NOT BUILT | Coder 516 open; until then `dispatch.py` returns `worktree_invalid` for every repo (D07) | S20 prerequisite |
| `/sc:issue --claim` waves 0-8, levels none, worktree, full, full submit | BUILT-ON | `commands/issue.md:104-110`; `refs/claim.md:48, 91-92` | S3 (rule C1) |
| Watcher claim launch at level none | BUILT-OFF | `launch.py:33`, `cycle.py:1026-1112` | none |
| Launch guard L1, L2 pre-push, job identity, G2 rule 2 | BUILT-ON | `launch-level-guard.sh:785-803`, `launch-level-pre-push.sh`, `launch-job-identity.sh`; governs only sessions a claim launch bound | none |
| Live observations OB-H1..3, OB-CTX, ship gate | NOT BUILT | `tests/hooks/test_launch_level_observations.py:79-84` skips; gate is prose | S20 |
| `pending` verb | BUILT-ON | `orca_worktree.py:1515-1523` | none |
| Caller of `pending` and binding of a worker-start worker | NOT BUILT | techref rows 10, 18 | S15 |
| `issue_pipeline` package, WC-17, "Issue pipeline duties", G2 rule 1, `release-worker` | REMOVED | PR 682 commit `01e7a9e23`; present at `01e7a9e23^`; zero hits in `src` on master | S7 restores |
| Coordinator skill, `/sc:coordinator`, verb group, wake handling | NOT BUILT (design text `docs/designs/orchestrator.md`) | no `commands/coordinator`, no skill on master | S14, S15 |
| `merge-gate`, `answer-check`, `E-NO-GRANT`, `refuse(argv)`, audit AU1-AU8, hand-back, `escalate`, `asks.json` | DESIGN ONLY | in none of master, pr-a, pr-p (D06, D11) | S14, S16, S19 |
| Wake file, ack file, `route.py` counting and restart | NOT BUILT on master; PR 686 OPEN (CI green, `enabled:false`) | `pr-a wake.py:69` | S13 |
| Plan check in the poll | NOT BUILT on master; `hold.py:122` in PR 686 OPEN | `pr-a hold.py:122` | S11 |
| Label writer of PR 686 | NOT BUILT on master; to be stripped | D09, Q03 | S13 strips |
| `/sc:issue --plan`, `--remaining`, `plan_body.py` | NOT BUILT on master; PR 690 OPEN | `skills/sc-issue-protocol/scripts/plan_body.py` in pr-p | S2 |
| Plan sections in issue templates | BUILT-ON | PR 661 merged | none |
| Claim launch result file | NOT BUILT on master; PR 693 OPEN | D14 | S1 |
| `/sc:closeout` | BUILT-ON | PR 683 | S19 wires it |
| Cleanup script, nine rules | NOT BUILT | issue 687 (an issue, nothing built) | after S19, owner go |
| Issue 689 items | NOT BUILT | issue; split by D12 | later |
| Sweep (`/sc:sweep`) | BUILT-ON | PR 539; `commands.py:277-278` prints JSON | S5 |
| Sweep `session_id`, `worktree_path`, saved JSON | NOT BUILT | `report.py:642-661` | S5 |
| Observer (`superclaude observe`) | BUILT-ON | R0 to R3 (`commands.py:67,70`); questions panel calls Orca itself (`adapter.py:32`) | S18 |
| Work report skill and living-report reader | BUILT-ON | PR 684 | S18 follow-up |
| Entry-file writer (`report-entry`) | NOT BUILT | techref 2.5 | S19 |
| Dashboard design package (issue 409) | DESIGN ONLY (prototype on synthetic fixtures) | "not a production integration" | none |
| Branch protection on `master` | NOT BUILT (`protected:false`, no ruleset) | D01, D14 | S0 recommendation |

Consistency note: where D05 and D14 say "built" for the guard, this table says BUILT-ON only for sessions a claim launch bound; no worker-start worker has ever been bound.

## 7. Open owner actions

Every item is a decision only the owner (`ironbelly`) can give, in this order. The owner answers in chat; the agent records the quoted words, date, exact scope and who recorded it (Q01). The owner never writes a file. Silence is not a yes. Items 1-5 gate S0 to S9; items 6-9 gate S13 to S15; the rest gate S16 to S20.

1. **Hold PRs 686 and 690?** Yes: Clay is asked to make both drafts and not merge; S0 holds (D14 H0). No: only temporary code-owner lines can catch 686 (through `issue_watch/`) and 690 (through `sc-issue-protocol/`), and one merge click can break `superclaude --help` (D03).
2. **Server-side ruleset on `master` and `integration`?** Yes with admin bypass: the owner's own PRs and reverts do not wait, and the gate binds `clayphi` only (D16 decision 3). Yes symmetric: owner PRs need a second code owner. No: K12 (a worker or any session on the shared login can push `master`) stays Medium likelihood, High impact (D05); the typed go is the only brake. Also answer whether `integration` is in or out (D16 decision 4).
3. **Q1: do BOTH gates stay (start approval and plan approval after the claim)?** Both stay: S6 to S9 run as written (revert, planb on `issue_pipeline`). Only the start gate stays: PR 682 stands under D03's three conditions (PR B tests exist first, R33 built before R18, a written owner ruling), S6 to S9 change, K3 flips to D05's text.
4. **Who is "the owner" for typed answers and grant changes on one shared login?** Chat only, stated as a limit: `answer-check` cannot tell a person from a script (D06 item 9). A separate GitHub login for agents: lets GitHub-side checks prove who acted, costs setup (UNVERIFIED how Coder provisions it). A named second person: needs their own agreement first (D16 never names `IB-JonathanB` before that).
5. **Q4: order of planb and the revert.** Revert first (recommended, K13): planb rebases cleanly onto the restored package. Planb first: planb must carry the package re-add by hand, an untested path.
6. **Who edits PR 686 (Q2)?** Clay on the PR: keeps review history and credit, owner reviews each push. A new draft by the owner's side: faster to control, loses history. Either way S13 keeps the same checks.
7. **Poll command contract (Q3).** `run-all` over `orca repo list` with per-repo JSON (recommended, K4). `once` plus `repos.yaml`: needs the registry D07 removed and reopens D07.
8. **Who claims (K1).** The poll, wake after the marker (recommended). The coordinator: one fewer model session per claim, but MR-2 moves into the coordinator and `claimed` leaves the store.
9. **Guard level for a worker-start worker (K2).** F (recommended): worker never commits, pushes or opens a PR. FS: worker can push a feature branch, PR flow simpler, relies on a ruleset for `master`. New guard level "commit only": a guard change needing independent review.
10. **Contract amendments.** Line 57 ("given by the owner in chat and recorded by the agent"): Yes ships in S8; No keeps the sentence the owner never worded (Q01). Lines 70 and 245 (script-started coordinator at depth 0; push for Full Submit as the person's go): approve R25, R17, R9 and they ship as separate commits; No leaves a person-opened coordinator only.
11. **Standing grants.** Name which of `issue.assign`, `issue.comment`, `issue.body.append_plan_sections` to grant, if any; the agent records it with the `repos` verb. None: every write needs a per-action chat go (safest, slowest). `pr.merge` and `issue.close` are never standing.
12. **Merge details.** Go expiry (no source gives a number; recommend 24 hours, UNVERIFIED); reviewer hold (default 60 minutes, UNVERIFIED); keep `changes_requested` a hard refusal (recommended, D06); post-merge close (K11): the go names the close (recommended) or a separate closeout grant is recorded.
13. **Cleanup.** Approve the issue 687 design in chat: Yes lets S19 wire `list` only; `--apply` still needs a go each time. Local `git branch -d` (Q02): Yes with the refusals, first week report-only; No: worktree removal only.
14. **Observability.** Sweep JSON saved beside the report (recommended, K16) or each reader sweeps. May the observer show entry text (through `observe/sanitize.py`)? Cap of 5 notices a day: default stays 0 until ruled. Is a typed wake line to an idle person-opened session acceptable at all (D10)? No: only file and mailbox remain.
15. **Names.** Working branch `Coordinator` or `coordinators` (D08 keeps two things, one working, one shared records); one `COORD-<RepoName>` per project or per scope; until Coder 516, `ORCH-IronClaude` in `coordinator_session` (K12).
16. **Cap and hand-back.** `max_in_flight` first value 1 (recommended) or 3 once claim agents have their own worktrees; in-flight expiry hours (no source; recommend 24, UNVERIFIED, OD-13); hand-back round 2 re-approves after the re-plan (default) or carries the remaining list in the handoff (OD-2); default `plan_depth` (OD-1).
17. **Confirmations.** The eight removal PRs (620, 622, 627, 629, 631, 632, 650, 656): confirming blocks only host install. Issue 450 stays open and Clay's 2026-11-18 comment gets an answer. Issue 655 is rescoped by its assignee (drop "replaces #450"). Issue 689's B2 question (who runs brainstorm and design at filing time): until answered its items 1, 2, 4 are not built.
18. **Coder issues 515 and 516** are owner-run and gate S20; cron by hand on this host does not count as the image.

## 8. Risks and unverified items

Severity is H (could lose work, merge unreviewed code, or break the install), M, or L. Every row says what no source proves and the test that would prove it. A control is described as narrowing a risk, never closing it (D06 item 10).

| id | sev | what is unproven | test that would prove it |
|---|---|---|---|
| R1 | H | A `worker-start` worker can be bound: the first prompt fires `UserPromptSubmit` with the marker intact; `cmd_pending` has no preflight; `pending/<nonce>` is consumed. Never observed (D05; G2 facts 1-4 UNVERIFIED) | S20 staging probe on a throwaway issue: marker delivered, `pending/<nonce>` gone, `send` and `ask` without `--to`, scripted `git push origin master` refused. Until it passes real issues stay off (`WORKER_BINDING_ENFORCED`, K14) |
| R2 | M | The mailbox send works from outside a Run (U5) | One live send in S20; if refused the transport is file only plus the pull at `check --wait` |
| R3 | M | Orca `tui-idle` means "at the main input prompt"; the screen-tail check is new | Live capture of an idle and a busy session in S20 before any typed line (S17) |
| R4 | H | Cron exists in the image after boot (Coder 515); the `Coordinator` worktree exists (Coder 516) | After two workspace restarts `crontab -l` shows the line once and `pgrep -x cron` finds one daemon (D02); `run-all --dry-run` no longer returns `worktree_invalid` |
| R5 | H | A chat go is provable on one shared login; `answer-check` cannot tell a person from a script; the coordinator's own shell can run `gh pr merge` | Not provable by code. Narrowed by: one merge verb, go entry with head sha, gate run twice, post-merge audit AU1-AU8. Server-side ruleset (S0) is the only control that closes it (D05, D14) |
| R6 | H | The revert tree passes the full suite and `tests/hooks/test_launch_level_guard.py` (did not finish in D03); revert plus PR 686 breaks `superclaude --help` | S6 dry run at a recorded master sha; MC-1, MC-2, MC-3 on every later PR touching `issue_watch/` |
| R7 | M | Planb rebases onto post-revert master (never tried); 23 files overlap PR 686 | S9 rebase in a throwaway checkout first; MC-1 to MC-5 |
| R8 | M | PR 690 merges onto master plus PR 693 (share four files; trial never run) | S2 merge-only trial before review |
| R9 | M | A claim agent and the standing coordinator in one `Coordinator` worktree break "one worktree, one live agent" even at cap 1 (`launch.py:136-157`) | S20: first live run with the coordinator started only after the claim result file exists; later give claim agents their own worktrees. Test: NEW `test_wake_written_only_after_claim_ended` (needs PR 693's file shape, UNVERIFIED) |
| R10 | H | `master` is unprotected (`protected:false`); the guard narrows honest drift on `master` and `main` only; `integration` is open at every level | Owner item 2; a ruleset plus D16's throwaway test |
| R11 | M | All GitHub and Orca reply fixtures are assumed shapes (`test_github.py:575-583`); no live record exists | S20 shadow run records real replies; replace fixtures before enabling |
| R12 | M | The package copy of the plan check stays equal to `plan_body.py` | NEW parity test over the shared case table (S11), run in CI on every change to either file |
| R14 | H | The per-repo config is not tamper-protected (`launch.py:48-53`); a coordinator could weaken `merge_safety_files`, `reviewers`, `reach_daily_max` (C-INV-3) | S12 refuses weakening values at load; `repos` verb writes only on a recorded go; test: empty `reviewers` and `merge_safety_files: []` are refused. A hook on the config dir is not built (UNVERIFIED need) |
| R15 | M | "In flight" has a closing writer and expiry; at cap 1 a stuck `unknown` entry stalls the repo (only `reset N` frees it, `record.py:448, 706-720`) | S17 tests: drain after orphaned `pending`; three `unknown` do not block forever |
| R17 | M | `orca worktree rm` may delete the branch itself (UNVERIFIED), so Q02's refusals must run first | Prove `orca worktree rm` behavior on a throwaway worktree before any cleanup build; first week report-only |
| R18 | H | A blanket `superclaude install --force` on a host removes skills of PRs 632, 650, 656 (NB-1) | Per-host diff of installed guard and contract before any install (S8 rule, S20) |
| R19 | M | F-level binding lets `/sc:implement` run to the end without commit (the ledger needs `.dev/tasks` staged by the coordinator, WC:246) | S20 probe runs one real `/sc:implement` at F |
| R20 | M | Hand-back loops: a waiting issue holds a slot (C-INV-1); nothing wakes after re-approval (C-INV-2, `pr-a cycle.py:993-994`) | S19 tests for both; `HANDBACK_MAX` 3 is "not measured" |
| R22 | M | Session detection by name or tag (U25); `orca agent launch` carries the tag; `worker-start --model` picker id (U28) | S20 spikes; unreadable process table means "unknown, start nothing" |
| R23 | M | Reviewer hold default of 60 minutes and go expiry number have no source | Owner ruling plus one measured late-review case; label UNVERIFIED in the spec until then |
| R24 | M | The merge path is only as safe as its parts together: `E-NO-GRANT` does not see a raw `gh pr merge` | S16 tests as ONE unit (T13); `refuse(argv)` pattern tests |
| R25 | M | PR 686's own tests pin the old reasons table (`test_audit.py:86-98` forbids the 14 approval reasons) | MC-10 rewrite in S11 before S13 |

**Not shown by any source and so UNVERIFIED in this spec:** which verb exposes the restored `brief.build`; the shape of PR 693's launch result file; whether per-repo config loaders reject unknown keys; whether an agent-recorded go survives a coordinator restart; the proposed `.dev/coordinators/` sub-paths; the D16 package (it has no VERDICT.md yet, only a merged text; its ruleset test is not run); the word "simple feature" in rule C1 (D12 gives no measurable test).

**Where this spec leaves a verdict unfinished on purpose.** D10 M2 allows two answers; this spec picks "the poll re-targets", which is a recommendation, not a verdict. D15's four HIGH conditions (C-INV-1 to C-INV-4) are carried into S12, S16 and S19 as tests, not as proofs.
