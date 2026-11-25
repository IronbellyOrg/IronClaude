# Variant 1 (architect): one target architecture for the watcher, coordinator, dashboard and claim pipeline

Status: RECOMMENDATION only. Nothing here was built, pushed, merged, reverted or commented. Lens: start from the end state, then derive stages from the gap to `origin/master` 61ac2c2e6 (snapshot `/home/coder/.cache/ic-snap-20261120/master`). Short names: "Dnn" and "Qnn" are the verdict files `debates/<id>/VERDICT.md` under `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/`; "planb" is the owner's unpushed branch `ironbelly/issue-watcher-zero-setup-plan` (worktree `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb`); "pr-a" and "pr-p" are the snapshots of PR 686 and PR 690. D16 has no VERDICT.md, so it is left out.

## 1. Summary

The end state is one flow per project. A cron line runs one dispatcher every five minutes; the dispatcher runs a read-only poll for each project; when an issue is approved and has a plan, the poll writes a small wake file and nudges that project's coordinator; the coordinator (a Claude session named `COORD-<RepoName>` in the project's `Coordinator` worktree) claims the issue at level none, starts one supervised worker that may edit but not commit, commits the work itself, and pushes, opens a PR and merges only on a person's typed go. Closeout and a dry-run cleanup list follow each merge. The sweep, the observer screen and the work report read one JSON document.

The five decisions that matter most:
1. The coordinator claims, not the poll (K1). The built "poll launches a claim session" path stays as the only mode until the coordinator passes its live tests, then becomes a fallback.
2. Workers are bound to guard level F (implement, no commit, no push); the coordinator commits and pushes only on a person's go (K2). This uses the guard grid as built instead of inventing a commit-only level.
3. All machine state (wake, acknowledgment, per-issue state, in-flight count, go entries, use log) lives in one per-repo state folder outside any git checkout; `.dev/coordinators/` holds only human-readable records (K5).
4. One config contract: per-repo JSON in `~/.config/superclaude/issue-watch.d/`, schema version 2, with Clay's key names, safe defaults when absent, and one poll command `run-all` (K4).
5. The sweep JSON is the one document the screen reads: it gains `session_id`, `worktree_path` and a `watcher` block filled from `issue-watch status --all --json` (K10).

## 2. Target architecture

End state (nothing below the cron line runs today in this shape; see section 6 for what is built).

```
 OWNER'S CHAT --- approvals, goes, grants, rulings (an agent records each one) ---------+
                                                                                        |
 GITHUB (the poll only reads)                                                           |
   issue: assigned to the watcher login, Approved field set, Status in allow-list,      |
   plan sections filled, no hold:backlog label, body unchanged since approval           |
        | seven read-only gh calls                                                      |
        v                                                                               |
 cron */5 -- flock -n -- superclaude issue-watch run-all     (ONE dispatcher)           |
                 | orca repo list  ->  one child cycle per project                      |
                 v                                                                      |
   issue-watch once --config ~/.config/superclaude/issue-watch.d/<repo>.json            |
   start rule -> plan check -> cap -> write  ===>  PER-REPO STATE FOLDER                |
                 |                                  dispatch.json, audit.jsonl, holds,  |
                 |                                  wakes/<id>.json, issues/<N>.json,   |
                 |                                  goes/, grants use log               |
                 | nudge: mailbox or typed line, carrying the wake id only              |
                 v                                                                      |
   COORD-<Repo> session in <worktrees>/<repo>/Coordinator  <----------------------------+
     /sc:coordinator --wake <id>  (also pulls wakes/ at each return of check --wait)
     1 write issues/<N>.json   2 write wakes/<id>.ack.json   (ack only after 1)
     3 /sc:issue --claim <N> --pipeline none          (posts the claim marker)
     4 orca_worktree.py pending --level full ; worker-start with
       [sc-launch:v1:<nonce>] in the first prompt ; check pending/<nonce> is gone
     5 worker at guard level F: edits, tests, worker_done (no commit, no push)
     6 coordinator commits; shows the commits; on a go: push + /sc:pr-submit
     7 merge-gate -> person's typed go -> merge-gate again ->
       gh pr merge <N> --repo <R> --<method> --match-head-commit <sha>
     8 /sc:closeout <PR> ; cleanup list (dry run) ; post-merge audit
                 |
                 v
   superclaude sweep  (read-only: Orca, transcripts, issue-watch status --all --json)
     sweep JSON v1 + session_id, worktree_path, watcher block  (saved beside report)
          |                                   |
          v                                   v
   superclaude observe                 work report skill
   (the one screen, read-only)         (plain English per issue: GitHub, ClickUp,
                                        entry files; session facts from the sweep)
```

### 2.1 Issue watcher

- STAYS (ours): D01's start rule (assigned only to the watcher login, `approval_of` plus `unchanged_since`, Status allow-list R22, `marker_in_window` at master `predicates.py:279`, start-time re-check `_revalidate`); NG-2, the poll writes nothing to GitHub (seven read-only calls); off by default (`enabled` absent means off, master `cycle.py:228`; kill file `DISABLED`; `GOVERNED_LEVELS_ALLOWED = False`, planb `launch.py:48`); `dispatch.json`, `audit.jsonl`, `status --json`; the D3 prompt rule widened by D10 item 6 (only pattern-checked values reach a prompt, typed line, mailbox subject or argv); planb's `run-all`, `generate.py`, `repo_init.py`; the trigger label for now.
- ADOPTED from Clay: read-only plan check with skip `held_incomplete`, run before the approval read, where a `<...>`-only section counts as empty, and `hold:backlog` read with skip `held_backlog` (D09, D15 A1, A3); wake file plus acknowledgment with M1 and M2 (D10); `max_in_flight` with `coordinator_full`, guarded restart, `owner/name` keys with `name_collision` (D07); the closed reasons table with its pin recomputed (14 approval reasons back; add `coordinator_full`, `name_collision`, `no_checkout`, `coordinator_absent`; drop `registry_invalid`, `repo_not_listed` and four label reasons; pr-a `tests/issue_watch/test_audit.py:86-98`); `would_hold` and a local `holds` entry with no write (Q03).
- REWRITTEN: per-repo key `start_mode`, `claim` (today's built launch, the default) or `wake` (write a wake and nudge), flipped per repo after S14 (K1); one store-state union `pending, woken, acked, claimed, unknown, failed, abandoned, waiting_reapproval`, keeping `claimed` so MR-2 holds in both modes (K15); wake folder moved to the per-repo state folder (K5); coordinator names (D08: `coordinator-wake/1`, `coordinator-wake-ack/1`, mailbox kind `coordinator-wake`, line `/sc:coordinator --wake <id>`; today orchestrator names at pr-a `wake.py:46-47`, `:823`); plan check as a package copy of `plan_body.py check` (K8).
- INTERFACES: consumes GitHub reads, `orca repo list`, the defaults file and per-repo config, acknowledgment files, the claim marker `<!-- sc:issue:claim -->` (master `predicates.py:14`). Exposes wake files, nudges, `issue-watch status --all --json` (the only public read of watcher state) and `audit.jsonl`; `dispatch.json` stays private.

### 2.2 Coordinator

- STAYS (ours): a person's typed go for every merge, no standing `pr.merge` or `issue.close` (D04, D06); `/sc:pr-submit` never an Orca worker; a flag-less `/sc:coordinator` is person-opened and creates no grant and no merge (D08); WC-9 no outward action from a worker (master `WORKER-CONTRACT.md:41`) and push of worker commits only on the person's go (`:245`); the restored `issue_pipeline` package in planb's stage-aware form (`brief.py` with the marker line, `complete.py`, `release-worker`, WC-17) and G2 rule 1 (K3); project-local topology (`COORD-<RepoName>`, `Coordinator` worktree and branch, `coordinators` records branch; D07, D08); the guard required for every worker it starts (D05).
- ADOPTED from Clay: one verb group `superclaude coordinator <verb>` with one JSON contract, one state lock and one `refuse(argv)` closed list (D15 O4); verbs per D15 R-7: `wake-check`, `wake-ack`, `state`, `plan-check`, `repos`, `merge`, `merge-gate` (13 closed reasons, read-only), `answer-check`, `audit` (AU1 to AU8), `report-entry`, `escalate` (no interrupt), `handback`; `E-NO-GRANT` with a use log, fail closed on missing or malformed `grants` (D04, Q01); head-pinned merge, reviewer hold, post-merge audit (D05, D06); hand-back with `/sc:issue --remaining`, escalation table, restart and cap (D07, D15).
- REWRITTEN: workers bound at level F, not FS; the coordinator commits after `worker_done` and, on the person's go, pushes and runs `/sc:pr-submit --monitor 3` from its own top-level session (K2); the worker's first prompt comes from the restored `brief.py`, so no second `handoff-prompt.md` (K3); grants default empty with at most three standing entries (K6); started or restarted by the dispatcher only under a recorded per-repo authorization (K11); the close after merge rides on the merge go entry (K12).
- INTERFACES: consumes wake files (pull and nudge), per-repo config (read only), grants, go entries, `plan-check`, Orca `worker-start`, `check --wait`, mailbox. Exposes acknowledgments, `issues/<N>.json`, go entries, audit rows, report entry files, escalations, the claim marker (through `/sc:issue`) and the launch marker (through `brief.py`).

### 2.3 TUI dashboard and observability

- STAYS (ours): the sweep (`/sc:sweep`, PR 539) as the one stateless, read-only source of session facts with no GitHub call; the observer `superclaude observe` as the one screen (no Options, no Recommendation, no write; entry text through `observe/sanitize.py`; three distinct empty states) (D11); the issue 409 package stays a prototype.
- ADOPTED from Clay: the living work report (PR 684; per-user state path; entry files store only `session_id`), the nine-row "what reaches the person" table as the notice step, silent-loss rules and the `check.py` gate; the cap of 5 notices a day stays a proposal, default 0 (D11, D15 D17).
- REWRITTEN: sweep rows gain `session_id` and `worktree_path` (today hidden inside `row_id`; the models already hold both, master `sweep/models.py:103`, `:131`); a top-level `watcher` block filled from `issue-watch status --all --json`, `read: false` on failure (K10); the JSON also saved beside the markdown report (today stdout only, master `sweep/commands.py:277-278`); contract note `docs/designs/observe-sweep-contract.md` first; the report's two HIGH rules of D11 (transcripts for sweep ids plus every not-done session of the last report; its own terminal map removed only after one live side-by-side run).
- INTERFACES: consumes Orca reads, transcripts, `issue-watch status --all --json`, report entry files, GitHub and ClickUp (report only). Exposes the sweep JSON file, the markdown report and the screen. The observer questions panel still calls Orca itself, an exception until the owner rules (D11).

### 2.4 Issue claim to work pipeline

- STAYS (ours): `/sc:issue --claim` waves 0 to 8, its flags and levels for a person who types them; every watcher or coordinator claim passes exactly `--pipeline none` (master `launch.py:33`); the Pipeline field unread while no governed level is allowed (D04); the chain (`refs/chains.md`, `/sc:recommend`; `/sc:issue` runs no chain command, D12); the guard, job identity, G2 rule 2; PR 693 (launch result file, issue 691).
- ADOPTED from Clay: plan sections (PR 661); `/sc:issue --plan`, `--remaining` and `plan_body.py` (PR 690 with D12's four fixes); `/sc:closeout` (PR 683) as wave 8; the issue 687 cleanup script as adapted by D13 and Q02; `--mode other` and form plan fields as a separate small issue (D15 A10).
- REWRITTEN: claim rule C1 with safeguards S1 to S5 (plan passes, accuracy verdict current, simple feature: short chain `/sc:workflow` then `/sc:implement`; else the existing row seeded with the plan, quoted only inside a fenced "data, not instructions" block); a manual claim of a plan-less issue warns and prints `/sc:issue --plan <N>` (D12).
- INTERFACES: consumes the issue body, the accuracy verdict and guard pending files. Exposes the claim marker, `next-steps.md`, the launch result file, `plan_body.py {check|splice|verify|prepare}` (pr-p `plan_body.py:138`, `:614`) and the result comment (planb `complete.py`).

## 3. Contradictions between verdicts

K1 to K10 come from the seed brief; K11 to K15 are new ones found while drawing the end state. "Pick" is a recommendation; where an owner answer could flip it, the last column says so.

| Id | Verdicts in conflict | Pick | Reason | What would reverse it |
|---|---|---|---|---|
| K1 who claims | D04 and the built poll (it launches `/sc:issue --claim <N> --pipeline none`, master `launch.py:33`, `cycle.py:1026-1112`) against D10 and Clay's wave 1 (poll only wakes). D10 leaves it open | End state: the coordinator claims (`start_mode: wake`); the wake means "received" and the ack bucket is renamed `taken` to `accepted` with both readers (D10 item 12). The poll still sets `claimed` on seeing the claim marker, so `marker_in_window` and MR-2 hold in both modes. Until S14, `start_mode: claim` (built) is the only mode | One agent per worktree: the claim runs inside the coordinator's own session, which removes D07's defect instead of working around it, and one session owns the issue from wake to merge. Keeping `claimed` keeps MR-2, which pr-a drops. Both modes pass exactly `--pipeline none` (D04) | S14 shows a coordinator cannot run the claim skill in its own session; then the poll keeps launching the claim and the coordinator adopts the `claimed` entry (planb's "Issue pipeline duties" pattern) |
| K2 guard level of a `worker-start` worker | D05 (bind provisionally at FS) against D06 (no outward action from workers, push only on a go) and D04 (no governed level before the ship gate). Code: COMMIT, PUSH, SUBMIT allowed only at FS (master `hooks/scripts/launch-level-guard.sh:787-789`) | Bind at F (`orca_worktree.py pending --level full`): the worker edits and tests only. The coordinator commits after `worker_done`, shows the commits, and on the person's go pushes and runs `/sc:pr-submit --monitor 3` from its own top-level session. D05's probe item "a `/sc:pr-submit` cycle at FS" becomes "a cycle run by the coordinator after an F worker" | F is the only built level that fits D06 and WC-9 (`WORKER-CONTRACT.md:41`); WC:245 already makes the coordinator the pusher. FS lets a worker push; a new level is a guard change needing independent review | Owner opens FS in chat after issue 442's 12 live observations pass and D04's gate-open design is reviewed |
| K3 PR 682 revert against D05 | D03 and D14 (revert restores `brief.py` with the marker slot, `release-worker`, WC-17, G2 rule 1) against D05 (assumes PR 682 stands: marker line in a new template, rule 1 stays removed) | The restored `brief.py` (planb's stage-aware version) is the one builder of the worker's first prompt; no `templates/handoff-prompt.md`. G2 rule 1 returns. D05's other binding steps stay unchanged | D05 item 6 itself requires a TAMPER class back if approval or release verbs return, which the revert does. One prompt builder, not two | OA-1 answered "only the start gate": PR 682 stands (D03 item 7) and D05 applies as written |
| K4 config file and poll command | D07 and planb (no registry, per-repo files, `run-all`) against D04, D06, D09, D11 (cite pr-a `repos.yaml` keys) and master/pr-a (`once` plus `repos.yaml`) | Cron runs `superclaude issue-watch run-all`, which runs `issue-watch once --config <file>` per repo. One config: `~/.config/superclaude/issue-watch.d/<repo>.json`, schema version 2, adding Clay's keys with safe absent values: `grants` (empty), `max_in_flight` (1), `reach_daily_max` (0), `start_mode` (`claim`), `coordinator_autostart` (false), `plan_tier`, `worker_tier`, `coordinator_tier`, optional `merge` block (`merge_method`, `release_head`, `release_merge_method`, `can_merge`, `reviewers`, `merge_safety_files`) | D07 and D15 R-3 chose the home; key names come from pr-a `repos.py:47-84`, `:295-299`. Safe absent values let a version-1 file run and grant nothing | OA-3 answered "`once` plus `repos.yaml`": D07 overruled, registry returns |
| K5 wake file location | D10 (`<orchestrator-repo>/.orchestrator/wakes/`) against D07 (no separate repo; records under `.dev/coordinators/` in each project) | All machine state (wakes, acks, per-issue state, go entries, grant use log) in the per-repo state folder `~/.local/state/superclaude/issue-watch/<owner>__<name>/`. `.dev/coordinators/` in the `Coordinator` worktree holds only human-readable records, carried on the `coordinators` branch | Machine state in a git worktree invites accidental commits and a `.gitignore` edit per project; the state folder already holds `dispatch.json` and `audit.jsonl`; only `wake.py` and `cycle.py` change. D10's path assumed the repo D07 removed | Poll and coordinator on different hosts; then a git-ignored `.dev/coordinators/wakes/` |
| K6 standing grants | D04 and Q01 (four standing incl. `issue.hold`) against Q03 (no label write) | Default empty; at most three standing: `issue.assign`, `issue.comment`, `issue.body.append_plan_sections`; `issue.hold` dormant. Recorded by the agent with `coordinator repos grant` (D15 R-4) | A grant for a write the poll never makes is a trap (Q03) | The deferred label-write PR lands after its 24-hour shadow run |
| K7 Project reads | D04 (no Project read while no governed level) against D01 (start rule needs Status R22 and `Approved` R35) | Read Status and `Approved` every cycle and at the start-time re-check; never read Pipeline while `GOVERNED_LEVELS_ALLOWED = False` | D04 defers approval and Status to D01; its concern is Pipeline, which picks a governed level | Owner opens a governed level |
| K8 one plan check | D12 and D15 R-2 (`plan_body.py check` imported by `hold.py`) against D01 and D09 (`hold.py plan_check`). Code: no package module imports a skill script; the two differ on commented-out headings | `plan_body.py check` is the reference; the package keeps a copy `issue_watch/plan_check.py` used by `hold.py`; a parity test loads the script by path and drives one shared case table through both (pattern of `tests/issue_watch/test_origin_parity.py`). Align comment stripping and the `<...>` rule first | The package cannot rely on an installed skill folder, and the skill's interpreter cannot rely on the package. Copy plus parity is the repo's only precedent | A small library both can import, or the skill calling `superclaude coordinator plan-check`; then the copy goes |
| K9 sessions in flight per coordinator | D07 (`max_in_flight` default 3; claim agents share the `Coordinator` worktree) against D10 ("one launch per sweep") | Absent key reads as 1. Raise to 3 only when each worker is seen running in its own worktree and the closing writer and expiry exist (C-INV-1). Keep one launch per sweep | With K1, claims run inside the coordinator; only workers need worktrees, and that is unobserved | Live proof that `worker-start` always makes its own worktree |
| K10 watcher state on the screen | D09 and Q03 (held issues show only in `issue-watch status` and the audit log) against D11 (sweep makes no GitHub call; one source) | One data path: `superclaude issue-watch status --all --json` (watcher owns the format; read-only, no `gh`, master `cycle.py:1279`). The sweep copies it into a `watcher` block; observer and report read only the sweep JSON | Keeps one screen, one document, and a sweep free of GitHub calls | Sweep run time grows too much; then a direct observer panel as a second named exception |
| K11 who starts a coordinator session (new) | D10 item 8 (poll starts one if none is live) and D07 item 4 (restart) against D06 (script start only at depth 0 under a recorded authorization) | The dispatcher starts or restarts `COORD-<Repo>` only when `coordinator_autostart` is true, set by the agent from a recorded owner go; otherwise it marks the workspace unread and records `coordinator_absent`. An unreadable process table starts nothing | D06 is the stricter authority rule; D10's start is transport, not authority | Owner allows automatic start everywhere |
| K12 close after merge (new) | D13 (closeout needs `issue.close`) against D04 and D06 (no standing close); D15 R-5 left open (C-INV-4) | The merge go entry names the PR and its linked issue; one go covers the merge and that close. A `Fixes` line still closes at merge: stated as a limit | One answer per PR, and no standing close | Owner wants a separate close go or a recorded closeout grant |
| K13 when the cron line exists (new) | D02 and D14 lane 3 (fix the cron line early) against D14 lane 2 (`run-all` lands with planb, after the revert) | Lane 3 fixes text only; no stage installs a cron entry before S14 | A cron line on `once` plus `repos.yaml` would be a third contract | None expected |
| K14 restart target before Coder 516 (new) | D07 item 4 (duty holder `ORCH-IronClaude` until 516) against D08 (`COORD-<RepoName>`) | No restart of any session until 516 creates `COORD-<RepoName>`; never restart an `ORCH-*` name | Restarting a retired name bakes it into the store | Coder 516 lands |
| K15 hand-back round 2 (new) | D01 item 5 and D15 R-6 (a re-plan voids approval) against pr-a `cycle.py:993-994` (an acked entry is never woken again) and the D07 cap (C-INV-1, C-INV-2) | New state `waiting_reapproval`: outside the cap, re-checked by the poll each cycle, given a NEW wake id when the start rule passes again, expiring to `stopped` after the owner's limit | The poll already owns the start rule; a coordinator copy would duplicate it | OA-14 answered "carry the remaining list": no re-approval |

## 4. Interface table

"State folder" below means the per-repo state folder of K5, `~/.local/state/superclaude/issue-watch/<owner>__<name>/` (the exact subfolder naming in planb is UNVERIFIED; the key on `owner/name` is D07 item 7). "Built" refers to `origin/master` 61ac2c2e6 unless a branch or PR is named.

| Name | Format or path | Writer | Reader | Owner piece | Built today? |
|---|---|---|---|---|---|
| Per-repo config | `~/.config/superclaude/issue-watch.d/<repo>.json`, `schema_version` 2 (keys in K4) | Init (`generate.py`) once; then only the agent via `coordinator repos` on a recorded go; a hook refuses other coordinator writes (C-INV-3) | Poll (watch keys, `max_in_flight`, `start_mode`); coordinator (`merge`, `grants`, tiers) | Watcher | v1 planb only (`generate.py:195`, `:252`); v2 NOT BUILT; Clay's keys only in pr-a's `repos.yaml` parser |
| Defaults file | `~/.config/superclaude/issue-watch-defaults.json` | Install or init | Poll | Watcher | Planb only |
| Old single config | `~/.config/superclaude/issue-watch.json` | Person | Master poll; report skill (`orchestrator_repo`, `agent-work-report/scripts/common.py:22-25`) | Watcher | BUILT; retired in S7; report re-pointed in S10 |
| Poll command | `superclaude issue-watch run-all`, running `once --config <file>` per repo under `run-all.lock` | Cron | Dispatcher | Watcher | `once` BUILT; `run-all` planb only (`cli.py:432`, `dispatch.py:57`) |
| Cron line | `*/5 * * * *`, `flock -n`, absolute paths, log `~/.aidev/logs/issue-watch.log` | Install (Coder 515) | cron | Watcher | NOT BUILT in the image; hand-installed on this host |
| Dispatch store | `<state folder>/dispatch.json`, state union of section 2.1, restart counter | Poll only | Poll; `status` | Watcher (private) | BUILT with `pending, launched, unknown, failed, abandoned, claimed` (master `record.py:34-35`); union NOT BUILT |
| Kill file, audit log | `<state folder>/DISABLED`; `<state folder>/audit.jsonl` with the closed reasons table | Person or agent; poll | Poll; `status`, report | Watcher | BUILT (master `record.py:283`, `audit.py:124-128`); recomputed reasons NOT BUILT |
| Wake file | `<state folder>/wakes/<wake_id>.json`, `coordinator-wake/1`: wake id, target, attempt 1 to 3, items of `repo`, `number`, `url` only; temp plus rename, 0600, at most 64 KiB | Poll | Coordinator (`wake-check`; pull at each `check --wait` return) | Watcher | pr-a only, `.orchestrator/wakes`, `orchestrator-wake/1` (pr-a `wake.py:46`, `:69`) |
| Acknowledgment | `<wake_id>.ack.json`, `coordinator-wake-ack/1`, bucket `accepted`, only after `issues/<N>.json` exists (M1) | Coordinator (`wake-ack`) | Poll | Coordinator | pr-a only (bucket `taken`, `wake.py:47`, `:553`); M1 NOT BUILT |
| Nudge | Mailbox kind `coordinator-wake`, payload `{"kind","wake_id"}`; typed line `/sc:coordinator --wake <id>` only to an idle or just-started session after a screen-tail check | Poll | Coordinator session | Watcher | pr-a only, orchestrator names (`wake.py:823-827`); U5 UNVERIFIED |
| Per-issue state | `<state folder>/issues/<N>.json`, exclusive create: phase, wake id, worker id, nonce, PR, head sha, round | Coordinator (`state`) | Coordinator; `status --all` (counts) | Coordinator | NOT BUILT |
| Human records | `<Coordinator worktree>/.dev/coordinators/<N>/summary.md`, `audit/<date>.md`, on the `coordinators` branch | Coordinator | People, report | Coordinator | NOT BUILT |
| Claim prompt | `/sc:issue --claim <N> --pipeline none` | Poll (`claim` mode) or coordinator (`wake` mode) | `/sc:issue` | Claim pipeline | BUILT for the poll (master `launch.py:33`) |
| Claim marker | Comment with `<!-- sc:issue:claim -->` | `/sc:issue --claim` | Poll (`marker_in_window`, `claimed`) | Claim pipeline | BUILT (master `predicates.py:14`; `cycle.py:899`) |
| Launch marker, pending file | `[sc-launch:v1:<32 hex>]` in the worker's first prompt; `~/.claude/state/launch-level/pending/<nonce>` (level word, 0600) | Coordinator runs `orca_worktree.py pending --level full`; restored `brief.py` adds the marker | Guard L1 (`launch-level-guard.sh:318-319`); coordinator's gone-check | Claim pipeline | Guard and `pending` BUILT (`orca_worktree.py:1515`, levels at `:1891`); preflight NOT BUILT; `brief.py` slot REMOVED by PR 682 |
| Result comment | `<!-- sc:issue:result issue=<N> run=<id> -->` | `complete.py` | Poll, report | Claim pipeline | Planb only |
| Launch result file | Claim launch result (issue 691) | `/sc:issue` | Coordinator, report | Claim pipeline | PR 693 OPEN; path UNVERIFIED |
| Merge go entry | `<state folder>/goes/<PR>-<sha12>.json`: repo, PR, 40-char head sha, method, the word merge, linked issue, gate output, quoted words, date, recorder, question key, used flag; one-shot | Agent, after `answer-check` passes on the typed answer | `coordinator merge` | Coordinator | NOT BUILT |
| Grants, use log | `grants` in the per-repo config (default empty); `<state folder>/grants-use.jsonl` | Agent via `repos grant` on a recorded go; verbs append uses | `refuse(argv)`, `E-NO-GRANT`, audit | Coordinator | NOT BUILT (pr-a only reads `issue.hold`, `cycle.py:1024`) |
| Merge gate | `coordinator merge-gate --repo <R> --pr <N> --json`: `ok` plus reasons from a closed list of 13 | Coordinator | Person before the go; `merge` again before `gh pr merge` | Coordinator | NOT BUILT |
| Watcher status | `issue-watch status --all --json`: per repo enabled, disabled, last sweep time (INV-008), counts by state, holds with reason; typed scalars | Watcher (read-only) | Sweep (`watcher` block) | Watcher | One-config `status --json` BUILT, no reader (master `cli.py:165`); `--all` NOT BUILT |
| Sweep JSON | v1 (PR 539) plus row `session_id`, `worktree_path`, top-level `watcher {read, repos[]}`; stdout and a file beside the report | Sweep | Observer, report, coordinator | Dashboard | v1 BUILT (stdout only); additions NOT BUILT |
| Report entry files | Per-user state path; `session_id` and issue id only | Coordinator (`report-entry`) | Report skill | Dashboard | Writer NOT BUILT |
| Plan check | `plan_body.py check` (reference; states absent, repeated, empty, placeholder, ok) plus package copy `issue_watch/plan_check.py`; one parity table | Claim pipeline; watcher (copy) | `--plan`, rule C1, poll, `coordinator plan-check` | Claim pipeline | PR 690 OPEN (pr-p `plan_body.py:138`); pr-a `hold.py:122` differs; copy NOT BUILT |
| Coordinator command | `/sc:coordinator [--wake <id>] [--hourly] [--resume] [--take <owner/repo#N>] [--sub]`, skill `sc-coordinator-protocol` | Person, or dispatcher when `coordinator_autostart` is recorded | Claude Code | Coordinator | DESIGN ONLY |
| Escalation | `coordinator escalate --kind <k> --issue <N>`: one notice via the nine-row table, no interrupt | Coordinator | Person, report | Coordinator | NOT BUILT |

## 5. Staged migration

The mechanical merge checks of D14, named once and reused below:
- MC-1 `uv run superclaude --help` exits 0.
- MC-2 every package under `src/superclaude/cli/` imports (`uv run python -c "import superclaude.cli.<pkg>"` per package, or one pytest that walks them).
- MC-3 names check: every name the restored `issue_pipeline` package imports from `issue_watch` exists (35 names; 9 missing on the pr-a head, including `EVENTS_JQ`, `argv_edits`, `github.edits`, `github.events`).
- MC-4 a test that removing the approval between wake (or launch) and start refuses.
- MC-5 a test that the global `enabled` key absent means off.
- MC-6 Rule B: an acknowledgment with no per-issue state file leaves the wake entry in place.
- MC-7 `make verify-sync`, plus `grep -rn 'src/superclaude' src/superclaude/{commands,skills,agents,core,hooks}` with every hit justified.

Every stage is one PR or one owner action. The watcher stays `enabled: false` and the `DISABLED` kill file works through every stage up to S14, so no stage changes live behaviour by itself. "Lane" and "O" codes are D14's lanes and D15's order codes.

**S0 Hold and first answers** (H0, O0). Scope: ask Clay to mark PRs 686 and 690 drafts; recommend a ruleset on `master` and `integration` requiring a non-author review; owner answers OA-1 to OA-6 in chat. No files, tests or rollback. Preconditions: none.

**S1 Merge PR 693** (lane 1, O1). Tests: its suite, its `/sc:pr-submit --monitor 3` loop, MC-1, MC-7. Rollback: revert. Preconditions: S0 sent.

**S2 Adapt and merge PR 690** (lane 1, O1). Scope: rebase on master plus 693; D12's four fixes; add the `<...>`-only rule and pr-a's comment stripping to `plan_body.py check` (prepares K8). Tests: new cases for a heading inside a code fence, a `<...>`-only section, a commented-out heading; MC-1, MC-7. Rollback: revert (PR 683's `--plan` reference dangles again, as today). Preconditions: S1; OA-2.

**S3 Claim rule C1** (lane 1, O1/O3). Scope: `sc-issue-protocol` `refs/claim.md`, `refs/chains.md`, `templates/next-steps.md`; S1 to S5; the plan-less warning. Tests: `tests/skills/test_issue_protocol.py` chain pins in the same PR; MC-7. Rollback: revert. Preconditions: S2.

**S4 Text only** (lane 3, O1). Scope: `HOW-WE-WORK.md` glossary line (D08) with its plugin copy and the `core/CLAUDE.md` level-table copy; banner on `docs/designs/orchestrator.md`; `docs/designs/observe-sweep-contract.md` (D11); five-field cron line and real reasons in `docs/designs/issue-watcher-setup.md` (D02, K13). Tests: HOW-WE-WORK copy tests, MC-7. Rollback: revert by file. Preconditions: S0.

**S5 Revert PR 682** (lane 2, O2). Scope: `git revert 01e7a9e23` as one new PR; the "ask and send carry no `--to`" bullet and assertions re-applied by hand; same-PR correction of the three "gate retired" design statements; G2 rule 1 back (K3). Tests: dry run first in a clean checkout bound to a recorded master head sha (repeat if master moves); the 117 restored tests; guard tests for rule 1 and rule 2; MC-1, MC-2, MC-3, MC-7. Rollback: revert the revert. Preconditions: OA-1 "both gates stay", the dry-run record.

**S6 Contract and guard amendment** (lane 2, O2). Scope: `WORKER-CONTRACT.md` lines 57 (grant rows recorded by the agent, Q01), 70 (script-started coordinator under a recorded authorization), 245, 298, 300; guard comment 441-443; `core/CLAUDE.md:58`; one sentence binding coordinator-started workers at F (K2). Tests: `tests/skills/test_worker_contract.py`, guard suite, MC-7. Rollback: revert. Preconditions: S5; OA-7.

**S7 Land planb** (lane 2, O2). Scope: commit, push as a draft, rebase onto post-revert master (expect modify/delete conflicts on `issue_pipeline/`; do not resume its half-finished `/sc:implement` ledger across the rebase), re-point WC-17 references, land. Brings `run-all`, `dispatch.py`, `generate.py`, `repo_init.py`, `defaults.py`, config version 1, stage-aware `brief.py`, `complete.py`, `GOVERNED_LEVELS_ALLOWED = False`, the start-time re-check and claim-marker test. Tests: `tests/issue_watch/test_dispatch.py` (loop, rotation, 270 s cap), planb's suite, MC-1 to MC-5, MC-7. Rollback: revert; master returns to the single-config poll, still off. Preconditions: S5, S6; OA-4.

**S8 Design amendment** (lane 2, O2). Scope: rewrite the contested rows of `docs/designs/orchestrator.md` to this architecture (K picks, verb list, "narrows" wording, C-INV-1 to C-INV-4), or a new `docs/designs/coordinator.md` with the old file bannered. Tests: a doc grep that finds `orchestrators.json` and `repos.yaml` only in the "rejected" table (D07 item 2) and no "closes K12" (D05 item 4). Rollback: revert by file. Preconditions: S7; owner review in chat. Gate: S11 and later wait for S8 (D14, D15).

**S9 Adapted PR 686** (lane 2, O3). Scope, as a draft in place: keep every D01 symbol and MC-3's names; drop pr-a `repos.py`, registry parts of `route.py`, and the label writer (Q03 list; save the removed hunk as a patch); add `issue_watch/plan_check.py` with parity (K8), `held_incomplete`, `held_backlog`, `would_hold`, local `holds`; `wake.py` with the state-folder path and coordinator names; store-state union; `start_mode`; config version 2 with safe absent values; reasons pin recomputed. Tests: MC-1 to MC-7; `tests/issue_watch/test_hold.py`; new `test_plan_check_parity.py` (loads `plan_body.py` by path); `test_audit.py` pin; `test_security_invariants.py` zero-write test restored; renamed `test_wake.py`; new: absent `start_mode` means `claim`, absent `max_in_flight` means 1, absent `grants` means empty, `waiting_reapproval` outside the cap. Rollback: revert; absent `start_mode` keeps the built claim path anyway. Preconditions: S2, S5, S7, S8; OA-2; D08 names.

**S10 Dashboard** (lane 3, beside S9, after S7). Scope: sweep rows gain `session_id`, `worktree_path`; `watcher` block; JSON saved beside the report; `issue-watch status --all --json` with last-sweep time (INV-008) and holds; PR 684 follow-up (D08 wording at `SKILL.md:12`; config path re-pointed from `issue-watch.json`). Tests: reviewed sweep golden-test edit; `status --all` with three repos, one store unreadable (`read: false` for it only); observer's three empty states; entry files carry only `session_id`. Rollback: revert; readers ignore unknown keys (pinned in the contract note). Preconditions: S4, S7; OA-9.

**S11 Coordinator substrate, person-opened only** (O4). Scope: `/sc:coordinator` and skill `sc-coordinator-protocol` (installed paths only); package verb group `superclaude coordinator` with state lock, JSON contract, `refuse(argv)`, path map, verbs `state`, `wake-check`, `wake-ack` (M1), `plan-check`, `repos` (read; `grant` on a recorded go), `audit`, `escalate`, `report-entry`; worker start bound at F (`pending --level full`, marker through `brief.py`, preflight, gone-check on a stated timeout, stop and escalate); constant `BOUND_WORKERS_PROVEN = False` keeps real issues "unbound and flagged" (the person sees it and gives a go) until S14's probe (D05 item 3); a hook refusing writes to `issue-watch.d/` from a coordinator session (C-INV-3). No merge verb. Tests: new `tests/coordinator/test_refuse_argv.py`, `test_state_lock.py`, `test_wake_ack_m1.py` (MC-6), `test_binding.py` (no marker leaves `pending/<nonce>` and triggers the stop; missing `jq` refuses, D05 item 2), the hook test, `tests/skills/test_primitive_dual_surface_lookup.py` extended; MC-1, MC-2, MC-7. Rollback: revert; nothing calls the verbs while repos run `start_mode: claim`. Preconditions: S8, S9.

**S12 Merge path as one unit** (O5). Scope: `merge` verb, go entry, `merge-gate` run twice, `answer-check` (Q01's four tests, "narrows"), `E-NO-GRANT` with use log, fail closed on weakening config values (empty `reviewers`, `merge_safety_files: []`, bad `reach_daily_max`), reviewer hold, audit AU1 to AU8, the linked-issue close under the go (K12). Tests: Clay's T13 as `tests/coordinator/test_merge_path.py`: gate pass without a go does not merge; go void after a head move; a go for one PR refused for another; `--auto`, `--admin`, `--delete-branch` refused; `checks_failing` override only with its own question key; `changes_requested` refused. Rollback: revert; merges are typed by hand again. Preconditions: S11; OA-12, OA-13.

**S13 Transport, cap, restart, hand-back, cleanup** (O6; may be three PRs). Scope: restart (K11, K14); `max_in_flight` closing writer and expiry; `handback` with `waiting_reapproval` (K15); one shared Orca terminal helper with parity against the report waker's `orca_term.py` fixtures (D10 item 9); M2 (abandoned wakes listed by `status --all`); issue 687 cleanup (`list` each cycle, `--apply` on a recorded go, Q02 refusals before removal, first week report-only). Tests: D07's three cap tests; restart bounded at 3 and nothing restarted on an unreadable terminal list; round 2 needs the start rule; helper parity; cleanup refuses master, main, integration, the default branch, a branch with an open PR, a foreign head owner. Rollback: revert per PR. Preconditions: S11; OA-14, OA-15; Coder 516 for restart.

**S14 Live tests, then switch on per repo** (O7). Scope, in order: D10 live gate (U5 mailbox outside a Run, `tui-idle`, U25 tag spike, screen-tail check); U28, U3, U8, U54; guard probe on a throwaway issue (receipt, `send` and `ask` without `--to`, an F worker refused on `git commit`, bare `git push` and `git add && git commit` refused, a scripted push to `master` on a throwaway repo); the D02 1-24 hour shadow test only if the precheck fallback is wanted; a 24-hour dry-run poll on cron. Then per repo, each on a recorded go: `enabled: true` with `start_mode: claim`; later `wake`; later `BOUND_WORKERS_PROVEN = True` by a reviewed commit. Rollback: `DISABLED`, `enabled: false`, `start_mode: claim`. Preconditions: S9 to S13; Coder 515 and 516; a per-host diff before `superclaude install --force`; the `Approved` field in each Project.

## 6. Built today versus not built

States: BUILT-ON (on master and in use), BUILT-OFF (on master, switched off or never run live), NOT BUILT (no code on master; a branch or open PR may hold a version, named in the "where" column), REMOVED (was on master, deleted), DESIGN ONLY (text, no code anywhere). Consistent with the seed brief's table and the two technical references.

| Item | State | Where today | Target stage |
|---|---|---|---|
| Issue watcher poll (`issue-watch once`, start rule, seven read-only calls, claim launch at level none) | BUILT-OFF | master `src/superclaude/cli/issue_watch/`, `enabled` default false (`cycle.py:228`); never run live; reply fixtures assumed | stays; S7, S9 extend |
| `issue-watch status --json` | BUILT-OFF (no reader) | master `cli.py:165` | S10 adds `--all` |
| Dispatcher `run-all`, per-repo config, `generate.py`, `repo_init.py` | NOT BUILT | planb only (unpushed) | S7 |
| Cron entry | NOT BUILT | hand-installed on this host 2026-11-18; Coder 515 and 516 open | S14 |
| `GOVERNED_LEVELS_ALLOWED = False` (R33) | NOT BUILT | planb `launch.py:48` | S7 |
| `/sc:issue --claim`, waves 0 to 8, levels | BUILT-ON | master `sc-issue-protocol` (a person types it) | stays; S3 adds C1 |
| Launch guard L1, L2, job identity, G2 rule 2 | BUILT-ON | master `hooks/scripts/launch-level-guard.sh`; live observations of issue 442 not passed | S6 text, S14 probe |
| G2 rule 1 and `issue_pipeline` package, WC-17 | REMOVED | PR 682 (commit `01e7a9e23`); present at `01e7a9e23^` and in planb | S5 |
| Claim launch result file | NOT BUILT | PR 693 open | S1 |
| `/sc:issue --plan`, `--remaining`, `plan_body.py` | NOT BUILT | PR 690 open, CI green | S2 |
| Plan sections in issue templates | BUILT-ON | PR 661 merged | stays |
| Claim rule C1 | DESIGN ONLY | D12 | S3 |
| Watcher rewrite: `hold.py`, `wake.py`, `route.py`, label writer, registry | NOT BUILT | PR 686 open, `enabled:false`; nothing on master reads its wake files | S9 adapts; registry and label writer dropped |
| Package plan-check copy and parity test | DESIGN ONLY | this spec (K8) | S9 |
| Wake file and acknowledgment with M1, M2, state-folder path, coordinator names | DESIGN ONLY | pr-a has the orchestrator-named version without M1 and M2 | S9, S11, S13 |
| `/sc:coordinator`, `sc-coordinator-protocol`, `superclaude coordinator` verbs | DESIGN ONLY | `docs/designs/orchestrator.md` (PR 681); PR B and PR E have no PR or branch | S11 to S13 |
| Merge gate, `answer-check`, `E-NO-GRANT`, go entry, audit AU1 to AU8, reviewer hold | DESIGN ONLY | design text only; not in master, pr-a or pr-p (D15 strongest points OURS 3) | S12 |
| `max_in_flight`, guarded restart | DESIGN ONLY on master | pr-a `route.py` `in_flight` (registry-bound) | S13 |
| `/sc:closeout` | BUILT-ON | PR 683 merged | stays; coordinator calls it in S12/S13 |
| Worktree cleanup script | DESIGN ONLY | issue 687 (an issue, not a PR) | S13 |
| Issue 689 items | DESIGN ONLY | an issue | split; deferred |
| Sweep (`/sc:sweep`, JSON v1 to stdout, markdown report) | BUILT-ON | PR 539; master `sweep/` | S10 extends |
| Observer `superclaude observe` | BUILT-ON (read-only) | master `observe/`; questions panel calls Orca itself | S10 |
| Work-report skill | BUILT-ON | PR 684 merged | S10 follow-up |
| Report entry-file writer | NOT BUILT | none | S11 (`report-entry`) |
| Sweep `session_id`, `worktree_path`, `watcher` block, saved JSON | NOT BUILT | rows lack the keys (enrichment K10) | S10 |
| TUI dashboard design package (issue 409) | DESIGN ONLY (prototype on synthetic fixtures) | `docs/` package, "not a production integration" | stays a prototype |
| Branch protection or ruleset on `master` | NOT BUILT | `protected: false`; one login `ironbelly` for owner and sessions | S0 recommendation; owner admin action |

## 7. Open owner actions

Every answer is given in the owner's chat and recorded by an agent (quoted words, date, exact scope, who recorded). The owner never writes a file. Ordered by the stage that first needs the answer.

**Needed at S0**
- OA-1 Do both gates stay (start approval, and plan approval after the claim)? (D03, D14 Q1)
  - Yes: S5 reverts PR 682; K3 pick applies (restored `brief.py`, G2 rule 1 back).
  - No, only the start gate: PR 682 stands under D03's three conditions; S5 is dropped; D05 applies as written (new marker line in a handoff template); planb must be rebased onto a tree without `issue_pipeline`.
- OA-2 Who adapts PR 686 and PR 690? (D14 Q2)
  - Clay, in place: review history and credit kept; the owner reviews each push.
  - An owner session on a new draft: faster control; D14's "adapt in place" is set aside and the old PRs are closed by their author.
- OA-3 Which poll command does cron run? (D02, D14 Q3)
  - `run-all` (recommended): K4 pick stands.
  - `once` plus `repos.yaml`: D07 is overruled; a registry returns and S7 and S9 change shape.
- OA-4 Order of planb and the revert. (D14 Q4)
  - Revert first, planb after (recommended): S5 then S7.
  - Planb first: planb lands on the PR 682 tree; the later revert then conflicts with planb's `issue_pipeline` edits.
- OA-5 Server-side ruleset on `master` and `integration`.
  - Yes (admin sets it): K12 is re-graded; a worker push to `master` is refused by GitHub.
  - No: the person's go stays the only brake; the guard only narrows honest drift.
- OA-6 Who counts as "the owner" for typed answers on the shared login `ironbelly`.
  - Name one session kind (for example a person-opened terminal tagged by the owner): `answer-check` test 1 gets a concrete meaning.
  - Leave it unnamed: `answer-check` cannot pass, so S12 ships but every merge stays typed by hand.

**Needed at S2 to S6**
- OA-7 Wording of WORKER-CONTRACT lines 57, 70, 245 (Q01, D06).
  - Approve: S6 lands; a script-started coordinator becomes possible under a recorded authorization.
  - Approve line 57 only: S6 lands without 70 and 245; `coordinator_autostart` can never be set.
- OA-8 Keep the trigger label? (D01)
  - Keep for now (verdict default): no change.
  - Drop: start rule loses one predicate; labels created by init shrink by one.
- OA-9 Where the sweep JSON lives. (D11)
  - Beside the report (recommended): one file all readers share; S10 adds the write.
  - Each reader runs its own sweep: no file; readers may disagree within a minute.
- OA-10 Branch names: `Coordinator` working branch and `coordinators` records branch as two things (D08).
  - Accept: layout as in section 4.
  - One name: the records move onto the working branch; `.dev/coordinators/` commits mix with work commits.

**Needed at S11 to S13**
- OA-11 Which of the three standing grants (`issue.assign`, `issue.comment`, `issue.body.append_plan_sections`). (K6)
  - Any subset: the agent records it with `coordinator repos grant`; the rest fail closed with `E-NO-GRANT`.
  - None: every such write asks the person each time.
- OA-12 Close authority after merge. (K12, C-INV-4)
  - Go entry covers the linked issue (recommended): one answer per PR.
  - Separate close go: two answers per PR.
  - Standing closeout grant: closes without asking; the only standing write beyond the three.
- OA-13 Go expiry and reviewer hold.
  - A number of hours for the go: a stale go dies even if the head did not move.
  - No expiry: a go lives until used, the head moves, or it is revoked (Q01).
  - Reviewer hold 60 minutes (UNVERIFIED default), another value, or none.
- OA-14 Hand-back: re-approve after a re-plan (default) or keep the body and carry the remaining list (OD-2); and the expiry of `waiting_reapproval` (OD-13).
  - Re-approve: K15 pick; expiry value sets when an issue drops to `stopped`.
  - Remaining list: no re-approval; `waiting_reapproval` is not needed.
- OA-15 Local `git branch -d` in cleanup. (Q02)
  - Yes: with the Q02 refusals, first week report-only.
  - No: cleanup removes worktrees only; branches stay.
- OA-16 Cap of 5 notices a day. (D11, D15 D17)
  - Accept: `reach_daily_max` 5 recorded per repo.
  - Keep 0: no notices; the report and screen are the only signals.
- OA-17 May the observer show entry text, and does the questions panel exception stay? (D11)
  - Yes: shown through `sanitize.py`; panel keeps its own Orca call.
  - No: titles only; the panel is removed or fed from the sweep.

**Needed at S14**
- OA-18 Per repo: `coordinator_autostart` true or false. (K11)
  - True: the dispatcher may start or restart `COORD-<Repo>` at depth 0.
  - False: a missing coordinator is reported as `coordinator_absent`; a person opens it.
- OA-19 Per repo, switch on: `enabled: true` with `start_mode: claim`; later `start_mode: wake`.
  - Each "yes" is one recorded config change; each "no" leaves the repo off.
- OA-20 Flip `BOUND_WORKERS_PROVEN` after the probe; later, open level FS for workers (K2).
  - Flip: real issues get bound workers without the "unbound" go.
  - Open FS: workers push feature branches; the coordinator only merges.

**Not blocking any stage**
- OA-21 Confirm the eight removal PRs (620, 622, 627, 629, 631, 632, 650, 656) (D14): blocks only a host install.
- OA-22 Answer Clay on issue 450; ask Clay to drop "replaces #450" from issue 655 (D14).

## 8. Risks and unverified items

Severity: H high, M medium, L low. Every control below "narrows" a risk; none "closes" one (D06 item 10, D15 wording rule).

| Id | Risk | Sev | What is unproven | Test that would prove it |
|---|---|---|---|---|
| RK-1 | A `worker-start` worker cannot be bound by the guard (marker not seen, or `pending/<nonce>` never consumed) | H | No code builds a worker prompt with the marker on master; binding a `worker-start` worker was never observed (enrichment K2) | S14 guard probe on a throwaway issue: receipt recorded, `pending/<nonce>` gone within the stated timeout, `git commit` refused at F |
| RK-2 | Unprotected `master`: a worker or script pushes or merges outside every gate (K12) | H | Nothing in the repo blocks it; the guard narrows plain pushes to `master` and `main` by bound sessions only (D05 item 4) | Owner sets a ruleset (OA-5); then a scripted `git push origin master` from a throwaway session is refused by GitHub |
| RK-3 | Owner identity on the shared login: `answer-check` cannot tell a person from a script | H | Q01's test 1 ("typed by a person in own session") has no mechanical proof | None fully proves it. OA-6 names the session kind; a test shows an answer typed in any other session is refused |
| RK-4 | Planb does not rebase cleanly onto post-revert master | H | Modify/delete conflict on `issue_pipeline/` paths, never tried (seed Q6) | S7 trial rebase in a throwaway checkout, then MC-1 to MC-5 on the result |
| RK-5 | Cron is not in the Coder image; the Coordinator worktree is not created | H for zero setup | Coder 515 and 516 open; until 516, planb `dispatch.py` returns `worktree_invalid` for every repo (D07 item 9) | A fresh workspace from the new template shows `crontab -l` with the five-field line and `<worktrees>/<repo>/Coordinator` present; one `run-all --dry-run` lists every repo without `worktree_invalid` |
| RK-6 | Revert and PR 686 merged in the wrong order break `superclaude --help` | H | Known (D03: 29 test modules fail at collection); guarded only by order and checks | MC-1, MC-2, MC-3 required on S5 and S9 |
| RK-7 | The coordinator cannot run the claim skill inside its own session (K1 end state) | M | Never tried; context size, Skill tool access and the claim's worktree check are untested | S14: coordinator runs `/sc:issue --claim <N> --pipeline none` on a throwaway issue; the claim marker appears; the poll moves the entry to `claimed` |
| RK-8 | Orca transport unknowns: `tui-idle` may not mean "idle at the prompt"; mailbox from outside a Run (U5) may fail; `orca agent launch` may not carry the ccsession tag (U25), so a lookup misses the session and starts a duplicate | M (U5 costs latency only, thanks to the pull) | All three are Orca behaviour never observed here | D10's live gate in S14, run before the start route changes |
| RK-9 | An F-bound worker is blocked by a skill that commits on its own (for example a ledger step) | M | WORKER-CONTRACT line 44 says such skills defer staging under `--unattended`; not observed bound | S14: an F worker runs `/sc:implement --unattended` on a throwaway task; the only guard refusals are the intended commit and push |
| RK-10 | A coordinator weakens its own controls by editing the per-repo config (C-INV-3) | M | A hook catches Edit and Write tools, not every shell write | Hook test in S11; fail-closed tests in S12 for empty `reviewers`, `merge_safety_files: []`, bad `reach_daily_max` |
| RK-11 | Two agents in one worktree if a worker shares the `Coordinator` worktree (K9) | M | Whether `worker-start` always makes its own worktree | S14 observation; `max_in_flight` stays 1 until proven |
| RK-12 | An abandoned wake is never woken again (M2) | M | pr-a `cycle.py:994` behaviour; recovery path new | S13 test: an abandoned entry shows in `status --all`; a new coordinator picks it up with a new wake id |
| RK-13 | Crash between acknowledgment and state file loses the issue (M1) | M | Order not enforced in pr-a (`cycle.py:777-810`) | MC-6 and `test_wake_ack_m1.py` in S11 |
| RK-14 | `orca worktree rm` deletes the branch itself, so cleanup refusals come too late (Q02) | M | UNVERIFIED Orca behaviour | Throwaway worktree removed with `orca worktree rm`; check whether the branch survives |
| RK-15 | Plan check copy drifts from `plan_body.py` | L | Two copies by design (K8) | Parity test in S9 on one shared case table |
| RK-16 | The `Approved` field or the Status allow-list is missing in a project, so every issue is skipped silently | L | Per-project setup (D02) | `status --all` shows the skip reason per repo; init refuses to enable a repo without the field |
| RK-17 | Low-severity design limits: `status --all` inside every sweep may slow it (time 20 sweeps before and after S10); a wake folder outside git cannot reach a coordinator on another host (K5 reverse; none needed while both share a host) | L | Not measured | As stated in the risk cell |

UNVERIFIED items carried as stated by their sources: U28 model picker id, U30 effort levels, U8 info stream replies, U3 depth-0 script start, U54, the 60-minute reviewer default, `HANDBACK_MAX = 3`, the exact per-repo state subfolder name in planb, the path of PR 693's result file, which restored `issue_pipeline` verb emits the worker brief, and whether a coordinator session can run the claim skill (RK-7).
