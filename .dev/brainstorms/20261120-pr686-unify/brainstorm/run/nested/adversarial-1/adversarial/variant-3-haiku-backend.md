# Unified issue flow: operations and failure first

## 1. Summary (10 lines)

1. RECOMMENDATION only: one local timer checks projects; it never writes to GitHub and nothing here enables it.
2. Keep the owner's start approval, content-change check, allowed Project Status and manual-claim duplicate check.
3. Decision 1: the poll keeps launching the claim at `--pipeline none`; a durable wake tells the project coordinator about the claim, not to claim again.
4. Decision 2: write the per-issue state before acknowledging a wake; recover undelivered wakes without repeating an uncertain claim launch.
5. Decision 3: bind each supervised worker at Full, abbreviated F: implementation allowed, commit, push and pull request creation refused.
6. Decision 4: one five-minute cron entry calls one dispatcher; project JSON replaces the separate registry repository and its YAML list.
7. Decision 5: a merge needs one person's fresh, head-specific chat go and a repeated gate; a passing check never means permission.
8. Start with one issue in flight per coordinator and separate worker worktrees; increase the cap only after isolation and completion tests pass.
9. The sweep supplies session facts, the observer displays them, and the work report supplies plain-English issue progress without inventing session state.
10. Land the owner's zero-setup branch before adapted PR 686; all new runtime paths stay off until crash tests, live probes and owner rulings pass.

Verdicts are settled recommendations, not consents. Digest: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/brainstorm/run/seed-brief.md:53-108`. D15 integrity conditions: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D15/VERDICT.md:139-144`. D16 has no supplied verdict, only an owner-action proposal. New contracts/tests are proposed, NOT BUILT unless stated.

## 2. Target architecture

```text
One host cron, every five minutes
  -> non-waiting host lock -> one run-all dispatcher -> discover local projects
       -> each project's once cycle, under its own store lock
          -> open + assignment + plan + approval + unchanged body + allowed Status
          -> reserve claim attempt durably -> claim session, pipeline none
          -> observe claim marker -> publish durable, id-only adoption wake
                                      |
                      optional mailbox or safe idle-terminal nudge
                                      v
Project coordinator COORD-<RepoName>, working tree Coordinator
  -> pull wakes on every bounded wait return -> create issue state -> acknowledge
  -> adopt existing claim -> plan approval -> guard preflight -> pending nonce
  -> ONE supervised F worker, separate worktree -> worker_done -> local review
  -> coordinator commits -> person authorizes push and top-level PR submission
  -> final-head reviewer hold -> show merge gate -> person's exact chat go
  -> repeat gate -> head-pinned merge -> audit -> authorized closeout -> cleanup list

Sweep JSON v1 + session_id + worktree_path -> observer, one read-only screen
                            \-> work report + GitHub/ClickUp + unfinished transcripts
Watcher status JSON + audit ----------------> observer's watcher panel
Coordinator report-entry -------------------> work report and observer item text
```

This is a local, at-least-once system: it may deliver the same wake repeatedly, but processing one issue round twice must have no second effect. A claim launch with a lost receipt is uncertain, not a retry instruction. A failed read is unknown, not empty. The system has no cross-host claim guarantee; a second host remains unsupported until a shared lease design is approved and tested.

### Issue watcher

**STAYS (ours).** Read-only GitHub, budgets, origin check, atomic store, kill switch and strict claim builder. Start requires open, solely assigned to watcher, plan present, no backlog hold, current allowed approval, unchanged body and Status Research/Spec/Plan/Debug. Keep trigger; read Approved and Status, not Pipeline. Repeat all gates before claim and worker start; preserve manual-claim exclusion. D01 MR-1/MR-2: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D01/VERDICT.md:12-18`.

**ADOPTED from Clay.** Pure plan check, local holds, bounded wake delivery, cap/restart and audit vocabulary with approval reasons restored. No label writes; body stays in memory. Plan-hold label ignored; backlog is person-set; init alone creates labels.

**REWRITTEN.** One scheduled run-all discovers Orca repos and calls child once. Five-field `*/5 * * * *`, absolute paths, `flock -n`, log `/home/coder/.aidev/logs/issue-watch.log`. Poll saves attempt before claiming, observes marker, then wakes adoption. Unknown receipt never blindly relaunches. Built save-before-launch: `/home/coder/.cache/ic-snap-20261120/master/src/superclaude/cli/issue_watch/cycle.py:1080-1112`. Cron image remains unproved; D02 automation fallback needs its 1-24 hour experiment.

**INTERFACES.** Config/approval/Status/marker in; dispatch/holds/audit/wake/status out. Child lock reserves one active issue per coordinator, one launch per dispatcher pass. Until claim worktrees split, standing Coordinator stays read-only while its claim session runs; marker alone is not completion. No checkout/collision skips. Reapproval wakes a new round, never reclaims.

### Coordinator

**STAYS (ours).** COORD-<RepoName>, Coordinator worktree, separate coordinators records branch, restored plan approval, one supervised worker and chat-only authority. Flag-less call creates no grants. Script start needs owner-approved depth-0 amendment; prompt authorization is self-attestation. D06: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D06/VERDICT.md:14-23`.

**ADOPTED from Clay.** One runner/lock, permitted-command list, refuse(argv), merge-gate, answer-check, grant-use log, final-head reviewer hold, audit AU1-AU8, hand-back and nine-category notice table. AU means audit check. These narrow risk, not raw-shell bypass. No interrupt, permission-prompt answer, release tag or publication; unanswered means wait.

**REWRITTEN.** Save issue/round state before ack; poll verifies matching state. Retarget abandoned wake with linked new id, never re-claim. Pull on bounded wait return within five minutes. Three deliveries ten minutes apart end unread/exit 7; three failed restarts require a person. Run guard preflight separately: pending only writes, as `/home/coder/.cache/ic-snap-20261120/master/src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:1515-1523` shows. Restored brief binds F; verify consumed pending plus session record within proposed 60 seconds, UNVERIFIED. Coordinator commits after worker_done, person authorizes top-level push/PR. Merge uses one-shot go, two gates and head pin; uncertain result reconciles before reuse. Changed head/reviews/base/threads/draft/reason voids go. Only checks_failing and merge_safety have keyed overrides; changes_requested refuses. Live role overrides can_merge. Close requires named authority.

Merge argv is exactly `gh pr merge <N> --repo <R> --<method> --match-head-commit <40-char-sha>`: never --auto, --admin or --delete-branch. Go records full 40-character head, owner quote/date/recorder, question key and gate snapshot; answer must follow the latest entry edit in the owner's own session. Fresh gate precedes both chat go and merge.

**INTERFACES.** Command flags and twelve DESIGN ONLY verbs are in section 4. Config authority cannot weaken without an accepted owner answer. Restart never restores consumed consent; runtime and protected authority records remain separate.

### TUI dashboard and observability

**STAYS (ours).** TUI means terminal user interface. Sweep alone classifies sessions; observer alone displays them, read-only, no Options/Recommendation. Add session_id/worktree_path, empty if unknown. Existing rows lack both: `/home/coder/.cache/ic-snap-20261120/master/src/superclaude/cli/sweep/report.py:642-661`.

**ADOPTED from Clay.** Living issue report, done/remaining text, transcript increments and silent-loss delivery gate. Read transcripts for sweep ids PLUS prior not-done sessions. Keep old map until LIVE side-by-side parity. Entries reference ids, never copied classes. Cap remains 0, not proposed 5. D11: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D11/VERDICT.md:17-37`.

**REWRITTEN.** Recommend atomic saved sweep JSON beside report, timestamps visible; screen refresh is not collection. Owner chooses saved snapshot or each reader's sweep. Questions panel remains labelled direct-Orca exception. Watcher status supplies holds/delivery without adding GitHub reads to sweep.

**INTERFACES.** Sweep owns session facts, report entries narrative, watcher status holds/audit summary. Empty folder, zero rows and failed read differ; Orca down means read:false, never ended. Sanitize entry text. Contract note precedes integration.

### Issue claim to work pipeline

**STAYS (ours).** Claim waves/flags, explicit none and duplicate marker, not consent: `/home/coder/.cache/ic-snap-20261120/master/src/superclaude/skills/sc-issue-protocol/templates/claim-comment.md:23`. Restore plan gate and G2.1 if owner keeps both; G2.2 retains plain ask/send without --to. Restored brief alone owns handoff marker.

**ADOPTED from Clay.** Templates, adapted --plan/--remaining, closeout and guarded cleanup design. C1 short chain is workflow then implement only for current accuracy, passing plan and simple feature; otherwise existing chain seeded with plan. This changes next-step text, never runs chain commands. Plan is fenced data. Plan-less manual claims warn with --plan, never refuse.

**REWRITTEN.** Canonical pure checker in proposed `/home/coder/workspaces/IronClaude/src/superclaude/cli/issue_watch/plan_check.py`; standalone installed script copy is parity-tested against it, never imported by package code. Reject headings in fences/comments and absent, repeated, empty or placeholder-only sections, including `<...>`, TBD and Not known yet. Presence is not quality. PR 690 currently counts exact lines without fence state: `/home/coder/.cache/ic-snap-20261120/pr-p/src/superclaude/skills/sc-issue-protocol/scripts/plan_body.py:101-139`. Hand-back creates a new round after final worker completion. Body edits void approval; the poll must recheck waiting rounds despite old acknowledgments. Waiting reapproval consumes no slot. Proposed round cap 3 is unmeasured. Closeout needs explicit close authority; cleanup starts report-only for one week, apply needs its own chat go, and any refusal keeps the entire worktree.

**INTERFACES.** Claim artifacts and claim marker flow to coordinator adoption. The guard nonce flows from pending record through the restored brief to the first prompt. Worker completion flows through `worker_done`, not a guessed idle screen. `--remaining` feeds hand-back; `left_open` from closeout feeds a report entry and, only under fresh approval, another round. Issue 689's creation redesign stays deferred; only its separable mode and form fields get a small later issue.

## 3. Contradictions between verdicts

The K numbers below name contradictions, not risk scores. A pick resolves the implementation recommendation; it does not answer an owner-only consent question. D15's later summary governs its own stale action rows. In particular, its order-code definition at `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D15/VERDICT.md:18` agrees with D14, whereas its section 6 moves PR 690 later. Use the definition and D14's lanes.

| id | Verdicts in conflict | The pick | The reason | What would reverse it |
|---|---|---|---|---|
| K1 | D04 poll claim; D10/Clay wave 1 coordinator claim | Poll claims none; coordinator adopts marker; ack means received | One claim owner, existing duplicate guard | Owner selects coordinator claim after parity tests |
| K2 | D05 FS; D06 no outward worker writes; D04 closed claim gate | F worker, coordinator commit, person-gated top-level push/PR | FS permits push; no commit-only level exists | Reviewed new level or owner-opened governed route |
| K3 | D03/D14 restore; D05 assumes removed G2.1/brief | Restore G2.1 and brief marker; retain G2.2 no-to | One template, two-gate flow | Owner keeps only start gate and approves replacement |
| K4 | D07 JSON/run-all; D02 once; D04/D06 YAML keys | run-all calls once; per-repo JSON holds keys | No registry; planb first | Discovery fails, owner approves new contract |
| K5 | D10 registry wake path; D07 local; D08 rename | Project-local coordinators wake directory | Same project owns recovery | Owner approves cross-project service |
| K6 | D04/Q01 four grants; Q03/D15 three | Three eligible, empty defaults | No poll label writer | Separate tested label PR and consent |
| K7 | D04 no Status read; D01 Status/Approved | Read Status/Approved; Pipeline dormant | Start safety is not execution level | Explicit owner start-rule change |
| K8 | D12/D15 import script; package isolation | Package pure copy and standalone script, parity pinned | No installed-skill runtime dependency | Shared standalone-safe distributable module |
| K9 | D07 cap 3/shared worktree; D10 one launch | Cap 1; separate worker tree; claim ends before coordinator writes | Prevent shared writes | Isolated claims, closing/expiry tests, owner raises cap |
| K10 | D09/Q03 no label; D11 no GitHub sweep | Observer reads watcher status, not GitHub | One watcher reducer, no label API | Reviewed local-status sweep extension |
| K11 | D15 hand-back; old ack never re-woken | Poll scans waiting round, rechecks approval, new wake | Old claim must not strand new round | Tested coordinator approval-event reader |
| K12 | D15 cap versus waiting rounds | Waiting excluded; unknown active counts | Avoid deadlock without hiding work | Measured owner-set stopped expiry |
| K13 | D06 no standing close; D13 closeout | Explicit close in merge go or separate close go | No implicit permission; Fixes remains limit | Owner requires only separate close consent |
| K14 | D11 single source; direct question reader | Label exception pending owner ruling | Do not claim unbuilt question integration | Owner accepts exception or shared schema |
| K15 | D14/O definition; stale D15 action order | 693 then 690 at O1; restore/planb O2; 686 O3 | Independent work need not wait | Verified dependency amends sequence |
| K16 | D05 bound workers; D04 closed governed claims | Separate constants; one staged F worker probe | Worker binding is not governed claim permission | Owner rejects distinction; automation stays off |

Code basis for K2: `/home/coder/.cache/ic-snap-20261120/master/src/superclaude/hooks/scripts/launch-level-guard.sh:785-799` allows COMMIT/PUSH/SUBMIT at FS only. Code basis for K11: `/home/coder/.cache/ic-snap-20261120/pr-a/src/superclaude/cli/issue_watch/cycle.py:992-994` excludes every non-failed prior entry. D10 expressly does not choose who claims, at `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D10/VERDICT.md:28`. K1 therefore changes no settled D10 ruling.

## 4. Interface table

Paths illustrate this host only: derive home and Orca roots at install time. `<repo-key>` reversibly encodes validated owner/name as owner__name, rejecting collisions. Coordinator is the worktree; coordinators is the records branch. Runtime state is local and ignored, never synchronized by committing locks. Evidence retention grants no commit/push authority. Singular report coordinator and plural project coordinators remain distinct.

| Name | Format or path | Writer | Reader | Owner piece | Built today or not |
|---|---|---|---|---|---|
| Timer | Five fields, `*/5 * * * *`, absolute argv, `flock -n`; log `/home/coder/.aidev/logs/issue-watch.log` | Installer after host consent | Cron, operator | Watcher | NOT BUILT on master |
| Dispatcher | `superclaude issue-watch run-all`; `orca repo list`; child `issue-watch once --config <absolute file>` | Installer/config generator | Host timer | Watcher | Local planb only |
| Per-repo config | `/home/coder/.config/superclaude/issue-watch.d/<repo-key>.json`, schema_version 1 | Guarded init and `coordinator repos`, owner answer required for authority changes | Poll, coordinator, report config reader | Watcher | Local shape exists, adapted keys NOT BUILT |
| Config keys | enabled false, repo, checkout/worktree, project/approver identity, labels; merge block: merge_method, release_head, release_merge_method, can_merge, reviewers, merge_safety_files; grants []; max_in_flight 1; reach_daily_max 0; coordinator_tier, worker_tier, plan_depth | Same guarded writer | Poll, merge and report verbs | Watcher with coordinator authority validation | Combined contract DESIGN ONLY |
| Host lock | `/home/coder/.local/state/superclaude/issue-watch/run-all.lock` | Dispatcher | Other dispatcher invocation | Watcher | Planb only |
| Dispatch store | `/home/coder/.local/state/superclaude/issue-watch/<repo-key>/dispatch.json`, versioned JSON, issue+round+attempt identity | Child cycle under store lock | Recovery, status, coordinator adoption check | Watcher | Store built; proposed round/outbox fields not built |
| Kill switch | `/home/coder/.local/state/superclaude/issue-watch/<repo-key>/DISABLED`; presence blocks outward launch | Operator/installer with consent | Poll before launch and wake delivery | Watcher | Built mechanism |
| Local holds and audit | Same dispatch store holds; `/home/coder/.local/state/superclaude/issue-watch/<repo-key>/audit.jsonl`, closed reasons, rotated | Poll only | Status reducer and operator | Watcher | Audit built; held/read reducer not integrated |
| Project runtime layout | `/home/coder/workspaces/worktrees/<project>/Coordinator/.dev/coordinators/runtime/` with issues, asks, grant-use log, locks | Coordinator verbs | Coordinator recovery and report-entry writer | Coordinator | DESIGN ONLY |
| Project records | `/home/coder/workspaces/worktrees/<project>/Coordinator/.dev/coordinators/records/`, quoted chat rulings and retained evidence | Agent records consent | Reviewers, operator | Coordinator | DESIGN ONLY |
| Wake | `/home/coder/workspaces/worktrees/<project>/Coordinator/.dev/coordinators/wakes/<wake_id>.json`; `coordinator-wake/1`, immutable id envelope, target generation, poll evidence ids, attempt; issue items repo/number/url only | Poll, temp+rename, 0600, max 64 KiB | `wake-check` and bounded coordinator loop | Watcher | PR 686 has old path/schema only |
| Acknowledgment | Wake directory above, `<wake_id>.ack.json`; coordinator-wake-ack/1, accepted/skipped/rejected, matching issue-state revision | wake-ack after durable state | Poll/recovery | Coordinator | Paired new schema NOT BUILT |
| Nudge/start | Mailbox coordinator wake id; typed `/sc:coordinator --wake <id>`; fixed agent-launch builder after U25 | Poll | Target session | Watcher | Adapted path NOT BUILT |
| Report runtime | Configurable per-user report_state_dir, default `/home/coder/.local/state/superclaude/work-report/`; no registry lookup | Report runner | Report/observer adapters | Observability | Rehome NOT BUILT |
| Issue state | `/home/coder/workspaces/worktrees/<project>/Coordinator/.dev/coordinators/runtime/issues/<repo-key>__<N>.json`; schema, round, revision, wake_id, claim evidence, phase, worker id, approval binding, terminal outcome | `state`, serialized under coordinator lock | Ack validator, cap, restart, audit, handback | Coordinator | DESIGN ONLY |
| Claim marker | Exact HTML comment `<!-- sc:issue:claim -->` on claim comment | Top-level claim skill | Poll `marker_in_window`, adoption validator | Claim pipeline | BUILT-ON manually; timer path off |
| Launch marker | `[sc-launch:v1:<32 lowercase hex nonce>]` in first worker prompt; pending word `full` in `/home/coder/.claude/state/launch-level/pending/<nonce>` | Pending verb and restored brief | Guard binds to `/home/coder/.claude/state/launch-level/sessions/<session_id>` | Claim pipeline/guard | Pending and guard built; worker caller NOT BUILT |
| Grant record | Protected config plus immutable quoted owner answer, date, exact scope, recorder and source session; names assign/comment/append_plan_sections only | Agent via accepted answer and guarded repos verb | `E-NO-GRANT`, use log | Coordinator | DESIGN ONLY; empty default |
| Merge go | `/home/coder/workspaces/worktrees/<project>/Coordinator/.dev/coordinators/runtime/asks/<question-key>.json`; repo, PR, head, method, merge word, gate hash, quote, times, recorder, consumed state | Agent records own-session chat; merge verb consumes | answer-check, merge, audit | Coordinator | DESIGN ONLY |
| Coordinator command | /sc:coordinator, skill sc-coordinator-protocol; --wake, --hourly, --resume, --take owner/repo#N, evaluation --sub | Person/authorized watcher | Coordinator | Coordinator | DESIGN ONLY |
| Coordinator verbs | `superclaude coordinator wake-check/wake-ack/state/plan-check/repos/merge/merge-gate/answer-check/audit/report-entry/escalate/handback`; JSON | Runner | Skill/tests/report | Coordinator | NOT BUILT |
| Plan approval | Restored issue-pipeline plan-hash/check-approval/stage-status/release-worker; approval record and session .ok | Coordinator under plan consent | Guard/worker start | Claim pipeline | REMOVED, restoration pending |
| Watcher status | `superclaude issue-watch status --json`; typed scalars and counts, proposed schema version, held issues, delivery/ack states, last_completed_at, read errors | Status reducer, no write | Observer and operator | Watcher | Built verb; extensions NOT BUILT |
| Sweep JSON | Schema v1, existing keys plus row session_id and worktree_path, empty strings allowed; proposed saved sibling of dated report in `/home/coder/workspaces/<project>/.dev/sweeps/` | Sweep publisher | Observer, work report, coordinator | Observability | JSON built stdout only; new fields/file NOT BUILT |
| Report entry | `/home/coder/workspaces/worktrees/<project>/Coordinator/.dev/coordinator/orchestrated/<repo-key>__<N>.json`; issue narrative, links and session references, no copied session class | `report-entry` only, close transition coordinated with report reader | Report refresh/exclude, observer | Coordinator writes, observability owns read contract | Readers built, entry writer NOT BUILT |
| Plan check | `plan_body.py check` installed script under `/home/coder/.claude/skills/sc-issue-protocol/scripts/plan_body.py`; equivalent package `coordinator plan-check`, states absent/repeated/empty/placeholder/ok | Pure checker, stdin body, stdout JSON | Claim, plan mode, read-only hold adapter | Claim pipeline | PR 690 only; parity and package API NOT BUILT |
| Worker completion | Run mailbox worker_done with worker id and outcome, handled once per message id | Supervised worker | Coordinator state transition | Coordinator | General route exists; issue wiring NOT BUILT |
| Cleanup boundary | Top-level closeout result left_open; cleanup list table names worktree, branch action, PR head and keep reason | Closeout/list script | Coordinator and owner chat | Claim pipeline | Closeout built; cleanup NOT BUILT |

### Integrity rules shared by these interfaces

Each write carries one stable action id. Use exclusive creation for a new issue state, temp file plus rename for replacement, flush file and parent directory before acknowledging. Reject symlinks, over-size JSON, unsupported schema and mismatched repository, issue, target or round. A duplicate wake returns the existing state and acknowledgment; it cannot overwrite a newer round. Lock contention returns a named busy result and does no outward work. Never acquire watcher and coordinator locks in opposite orders: release the producer lock before delivery; consumer commits its state before publishing ack. The poll verifies the referenced issue state exists and matches wake/round before accepting accepted. Missing state leaves the wake in place, the Rule B merge check.

Separate claim attempt from adoption delivery. Outbox replay keeps the wake id; retarget links a new id/generation. Failed moves remain replayable. Startup reconciles outbox, wakes, states and consumed goes before new work. Nudges carry wake id only. Type only to idle person-opened or just-started session: empty draft, 60 seconds quiet, main prompt visible, never busy/check-wait. Unreadable process list means unknown, no start. No listener.

The existing PR 686 writer already has size checking, exclusive temp creation, fsync and rename at `/home/coder/.cache/ic-snap-20261120/pr-a/src/superclaude/cli/issue_watch/wake.py:269-299`; its ack parser expects `taken`, not accepted, at `/home/coder/.cache/ic-snap-20261120/pr-a/src/superclaude/cli/issue_watch/wake.py:545-581`. Rename the schema and both readers together, with a pinned pair test. Never accept an old-schema empty acknowledgment as success. Shared terminal behavior gets one package helper and a parity fixture test, not another copy of the report helper.

## 5. Staged migration

Each stage is a separate reviewable PR or consented host operation. Stages do not enable subsequent stages implicitly. D14's hold H0 and three lanes are at `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D14/VERDICT.md:34-40`; D15's O codes mean order groups, not commands. S1 can proceed independently of S2-S4. All proposed tests below are acceptance requirements, not reported passing tests.

**Merge gate M for every watcher/restoration PR:** `uv run superclaude --help` exits 0; every CLI package imports; names match restored imports; approval removed between wake/start refuses; absent global enabled means off; Rule B retains wake if ack lacks state; `make verify-sync` passes. Run affected suites via UV, sync but never stage generated mirrors. Green 686 alone does not prove the combined tree.

| Stage / mapping | Scope and carrier | Tests and checks | Preconditions | Rollback |
|---|---|---|---|---|
| S0: H0/O0 | Hold 686/690 drafts; both-gate ruling; master/integration ruleset | Throwaway PR proves non-author/stale-head block | Owner consent/admin | Stop rollout, disabled |
| S1: Lane 1/O1 | 693 then adapted 690 then C1, keep 661 | Plan fence/comment/placeholder parity, chain pins, none names plan, warning/splice/693 compatibility | Reviewed heads, merge goes | Revert C1 then 690 |
| S2: Lane 2/O2 | Exact-master clean revert trial; restore 682 with no-to/banner/three corrections | M, pipeline/guard suites, CLI registration; repeat if master moves | BOTH gates consent/H0 | Revert restoration, retain evidence |
| S3: Lane 2/O2 | Contract/guard amendment then draft planb landed before 686; new ledger after rebase | M, R33 before field launch, F denies outward actions, both G2 rules, preflight/host diff | S2, wording consent, resolved conflicts | Revert independently, stores retained, timer off |
| S4: Lanes 2/3/O1-O2 | Amend 681/glossary, sweep contract note, 685, cron rationale | Text/installed-path tests, schema golden; runbook not probe proof | Rulings reflected; no B/E builder yet | Revert docs, no contested build |
| S5: Lane 2/O3 | Adapt draft 686 atop planb/690, retain symbols, remove registry/label/copied helper | M, zero-write, parity/reason pin, ack-state/retarget/unknown/helper tests | S1-S4, named editor, paired ack readers | Revert 686 only, preserve delivery files |
| S6: O4 | Runner/JSON/lock/path map/refuse/config guard | test_state_exclusive_create, test_state_revision_conflict, test_config_weakening_refused; symlink/size/schema/refusal cases | Amended design, empty grants, authority protection | Disable verbs, retain records |
| S7: O5 | Merge/go/gates/answer/grant/reviewer/head pin as ONE unit | T13 changes head/gate/review/base/thread/draft; no-go, duplicate/uncertain merge | S6, expiry/reviewer/close choices, live role | Disable merge, retain consumed go |
| S8: O6 | Wake/cap/restart/F binding/audit/handback/report-entry; 684/observer | Rule B, outbox/new-round/concurrent-cap/binding/sanitizer/missing-worktree tests | S5-S7, paired schema, isolated worker, old map kept | Disable consumers, retain files/map |
| S9: Lane 3/O7 | Throwaway live, shadow, enable; Coder 515/516/consented install | U5 mailbox, U25 tag/idle/screen, U28 effective model, U3 depth 0, optional U8, U54, guard probe; twelve observations separate | Host diff/removal consent, image proof, live fixtures, push/merge go | enabled false + DISABLED, stop timer, retain ledger |
| S10: O6/post-O7 | Adapt 687/list then apply; small 689 split | Nine rules plus protected/default, OPEN PR, foreign owner/head, saved evidence BEFORE Orca removal; prove branch effect | Design/branch consent, week one list-only | Disable apply, no recovery promise |

Cleanup never uses --force, -D or rm; remote branch deletion is human-only. Git refusal means kept, not failure.

Go/no-go evidence must identify code head, host, installed primitive hashes, fixture captures and failed as well as passed probes. A shadow timer does not launch agents or write GitHub. Only S9's explicit enable changes that. Increasing concurrency, activating Pipeline-field governed launches, adding label writes or polling a second host are separate future changes, not completion criteria hidden inside S9.

## 6. Built today versus not built

Baseline is the supplied master snapshot, not the stale main checkout. BUILT-ON means wired code exists, not proof this host ran it; BUILT-OFF means present behind a disabled switch. Open-PR/local code is not shipped. Source ledgers: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/techref/ISSUE-TO-WORK-PIPELINE-TECHNICAL-REFERENCE.md:317-343` and `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/techref/OBSERVER-SWEEP-DASHBOARD-TECHNICAL-REFERENCE.md:242-249`.

| Capability | Status | Consequence |
|---|---|---|
| Real watcher once cycle and fixed none launch | BUILT-OFF | Default enabled false; no live shape proof |
| Watcher status, dry-run and configuration verbs | BUILT-ON | Status integration and audit reducer still absent |
| Manual claim; L1/L2 guard; job identity; G2 rule 2 | BUILT-ON | Guard only covers bound sessions and tested local surface |
| IR7 missing-L2 refusal | BUILT-OFF | Constant false, warning is not enforcement |
| Issue pipeline, WC-17, G2 rule 1 | REMOVED | Revert recommendation is conditional, not built restoration |
| Dispatcher, cron provisioning, COORD worktree setup | NOT BUILT on master | Dispatcher/config code is local planb only; Coder image rollout unproved |
| Worker pending verb | BUILT-ON | Production worker binding caller NOT BUILT |
| Coordinator command, verbs, grants/merge/answer checks | DESIGN ONLY | No current mechanical merge-go path |
| PR 686 wake/hold/route implementation | BUILT-OFF in open PR only | Wrong baseline semantics and names; no master wake consumer |
| Plan mode and remaining, PR 690 | NOT BUILT on master | Open PR, needs adaptation |
| Template plan sections; closeout | BUILT-ON | Closeout wiring and close consent still need design |
| Sweep, observer, daily report and living-report readers | BUILT-ON | Separate sources today, no unified integration |
| Report entry writer; new sweep ids/saved JSON; observer watcher panel | NOT BUILT | Reader-side code does not establish these producers |
| Issue 409 dashboard package | DESIGN ONLY | Synthetic prototype, not production integration |
| Cleanup issue 687; creation redesign issue 689 | NOT BUILT | Issues are requests, not executable features |
| Twelve guard observations and host/runtime probes | NOT BUILT as completed proof | Runbook or fixtures are not live evidence |
| Branch ruleset protecting this flow | NOT BUILT in supplied evidence | Shared login remains a residual risk even after a ruleset |

## 7. Open owner actions

Every answer is given in the owner's chat; an agent records the quote, date, scope and recorder. Never ask the owner to write a grant file. Until answered, affected writes stay off. These are choices, not approvals inferred from this spec.

**1. Hold, gates, editor, order**
- Hold 686/690: drafts stay.
- No hold: no protected rollout assumption.
- Both gates: S2 restoration.
- Start only: 682 stands, redesign release.
- Neither: stop rollout.
- Clay edits: same draft PR.
- Another editor: bounded assignment, no parallel rewrite.
- Post-revert planb first: S2-S5.
- Different order: compatibility trial first.

**2. Names, trigger, typed wake**
- Accept names/run-all: this contract.
- Alternatives: amend paired readers/tests.
- Keep trigger: preserve ordering.
- Drop trigger: review replacement ordering.
- Permit typed wake: live screen proof first.
- Refuse typed wake: file pull/mailbox only.

**3. Identity, contract and standing duty**
- Own-session chat: validator with spoof limit.
- Stronger identity required: writes wait.
- Approve R9/R17 depth-0 start: amend contract.
- Decline R9/R17: person-opened only.
- Approve R25: design later Full Submit gate, not enable now.
- Decline R25: manual push only.
- Authorize standing duty: provision watcher.
- Decline standing duty: manual operation.

**4. Server rules and deputy**
- Master/integration rules yes: test blocking.
- Rules no: HIGH risk, person-operated outward actions.
- Admin bypass yes: shared-login bypass remains.
- Bypass no: emergency needs second approver.
- Named deputy: scope recorded, no self-ruling.
- Nobody: owner absence waits.

**5. Grants and config**
- Chosen subset of assign/comment/append_plan_sections: record only those.
- No grants: all refuse; issue.hold unavailable now.
- Protect plus validate: recommended.
- Protect only: prove coverage.
- Validate only: record raw-edit bypass risk.

**6. Merge and close**
- Set expiry: use chosen duration.
- No expiry answer: merge automation off.
- Hard changes_requested yes: refuse.
- Hard refusal no: reviewed redesign, not generic override.
- Reviewer hold 60 minutes: test proposal.
- Other hold: use owner value.
- Reviewers none: record explicit exception.
- Close in merge go: permit named closeout.
- Separate close go: closeout waits.
- Neither: report only.

**7. Hand-back and capacity**
- Re-plan: fresh approval/new-round wake.
- Untouched body: remaining handoff, revalidate approval.
- Exclude waiting: recommended.
- Expiry instead: owner sets duration/proof.
- Cap 1: serialize.
- Higher cap: isolation/closing/concurrency tests first.

**8. Observability and notice**
- Save sweep JSON: shared snapshot.
- Per-reader sweep: cadence/timestamps enforced.
- Entry text yes: sanitize/display.
- Entry text no: links only.
- Questions exception yes: label source.
- Exception no: shared questions block first.
- Cap 5: cap notices, never entries.
- Another cap: owner number, never drop entries.
- Cap 0: uncapped.
- Nine-category notice yes: wire it.
- Notice table no: durable entries only.
- Audit entry plus notice: notify.
- Audit entry only: no extra notification.

**9. Other D15 choices**
- plan_depth quick: shallow planner.
- standard: middle depth.
- deep: full depth.
- Naming own writers: narrow scan.
- All surfaces: broader reviewed rule, attribution unchanged until authorized.
- No naming rule: no scan.
- Naming failure fail-open: deliver safety escalation.
- Fail-closed: visible local unread, never silent loss.
- Never tag/publish: keep refusal.
- Exception: reviewed authority contract first.
- No interrupts: current pick.
- Allow interrupts: contract exception/receipt proof first.
- Lease deferred: single host only.
- Lease required: stale-lease design before second host.
- could_assign off: current pick.
- could_assign on: U8 capture first.

**10. Cleanup, installation and final actions**
- Cleanup design yes: build list.
- Cleanup no: no apply path.
- Local branch -d yes: guarded deletion.
- Branch deletion no: keep worktree if Orca cannot preserve branch.
- Specific apply go: named action only.
- No apply go: list only; first week always report-only.
- Confirm 620/622/627/629/631/632/650/656: reviewed host install.
- Do not confirm: block blanket install only.
- Answer 450/rescope 655 yes: record coexistence.
- No: communication pending.
- Small 689 split yes: mode/forms only.
- No split: defer.
- B2 creation redesign yes: separate design.
- B2 no: deferred.
- Live probes/Coder provisioning yes: gather evidence.
- No: disabled.
- Final enable after proof yes: S9.
- No/missing proof: disabled.
- D16 wording/ledger yes: reviewed follow-up.
- D16 no: no implied process change.

D15's detailed unresolved alternatives are at `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D15/adversarial/merged-d15-position.md:213-268`. Its stale four-grant alternative loses to its later R-4 resolution and Q03. D16 prevention remains a proposal at `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D16/adversarial/merged-output.md:15-22`, not an implemented protection.

## 8. Risks and unverified items

All live behavior below is UNVERIFIED until the named experiment passes. Proposed test names describe required behavior, not existing test functions. Crash tests kill the process at each persistence boundary and restart with the same store. No live test is run by this document.

| Severity | Failure or unproven behavior | Required test and safe failure |
|---|---|---|
| HIGH | Timer overlaps, clock jumps, stale lock or partial store | `test_overlapping_poll_one_reservation`: two invocations, one launches; killed lock holder releases OS lock; malformed state blocks, never resets |
| HIGH | Claim launch succeeds but receipt/save is lost | `test_unknown_launch_no_second_claim`: inject timeout after success, reconcile marker/operation, no new launch id; operator sees unknown |
| HIGH | Crash after claim marker before wake publication | `test_claimed_outbox_replay`: restart emits adoption wake once, never reclaims |
| HIGH | Ack before state/dispatch save crash | Rule B: missing/mismatched state retains wake; replay adopts once |
| HIGH | Abandoned target | test_abandoned_retarget: linked new wake, no round restart, exhaustion unread |
| HIGH | Blind process lookup | test_unreadable_proc_unknown: no launch; U25 proves tag/idle/draft/screen prompt |
| HIGH | Outside-Run mailbox | U5 plus dropped nudges: bounded file pull still delivers |
| HIGH | Restart storm/false receipt | test_restart_budget_survives_crash: persist three tries; screen proves readiness |
| HIGH | Worker unbound/CLI alias bypass | Live F pending/session proof, deny commit/push/PR/merge; installed aliases/preflight tested; 12 observations separate |
| HIGH | Approval/body/Status changes | test_revoked_between_wake_and_start: no worker; manual marker no duplicate |
| HIGH | Cap race/hand-back deadlock | test_concurrent_cap_one: waits excluded, unknown active counted, reapproval wakes round |
| HIGH | Weakened config | test_config_weakening_refused: raw edit and repos update; malformed cap refuses |
| HIGH | Shared-login spoof/raw merge/unprotected base | Replay narrows stale consent; live ruleset proves server block, not person identity |
| HIGH | Merge uncertainty/state change | T13 changes head/base/review/thread/draft/reason; reconcile exact head, no reused go |
| HIGH | Closeout/Fixes unfinished closure | test_closeout_needs_named_close_go; demonstrate Fixes limit, retain left_open |
| HIGH | Missing-worktree session loss | Live map parity; test_previous_not_done_carried with Orca down read:false |
| HIGH | Cleanup evidence/branch loss | Nine-rule dry run plus protected/default/integration, OPEN PR, foreign owner, dirty/unsaved evidence; prove Orca behavior, week one list only |
| MEDIUM | Plan copies disagree, malicious plan text reaches prompt | Shared fixture parity for fences/comments/placeholders; inject instruction-like plan into fenced data; zero free GitHub text in wake/argv/mailbox/typed line |
| MEDIUM | Coder image lacks cron/coordinator or install retires wanted skills | Rebuild a fresh workspace, inspect single timer and target; compare installed guard/contract before consented install; no manual-host success counted as image proof |
| MEDIUM | Tier/effort, notice cap, binding timeout and hand-back limit assumed | U28/U30 capture requested/effective model; record owner values and measured outcomes. Numbers 60 minutes, 60 seconds and 3 rounds remain proposals |

Limits: verb checks do not cover raw shell; launch authority is self-attested; guard is not a sandbox; audit misses direct pushes. Ledger: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/techref/ISSUE-TO-WORK-PIPELINE-TECHNICAL-REFERENCE.md:1886-1894`. Only this spec was written; no tests or live actions ran.
