# Scope 6: Coordinator duties text (current) and removed issue_pipeline package
**Scope:** WORKER-CONTRACT.md coordinator text (snapshot 61ac2c2e6); removed package src/superclaude/cli/issue_pipeline/ + WC-17 (commit 01e7a9e23, PR 682)
**Status:** Complete
**Date:** 2026-11-20
---

Paths: SNAP = /home/coder/.cache/ic-snap-20261120/master (read-only). OLD = `git -C /home/coder/workspaces/IronClaude show 01e7a9e23^:<path>`.

## 1. Current coordinator text (SNAP/src/superclaude/core/WORKER-CONTRACT.md, 339 lines)

Headline finding [CODE-VERIFIED by grep + full read]: the snapshot has NO sentence about the issue pipeline, the issue watcher, an issue-claim hand-off, plan approval, `COORD-` naming, or an adoption row. `grep -i 'WC-17|watcher|COORD-|issue.pipeline|plan.approv|approval record'` returns only lines 23 and 57. Rules present: WC-2..WC-16 (no WC-1 heading, no WC-17). Structure: s1 Terms (l.9), s2 Command-side rules (l.27), s3 Worker-session duties (l.49), s4 Coordinator rules (l.68), s5 Brief template (l.299).

Only issue-related hits (the whole current tie between the contract and the pipeline):

| Where | Text (gist) |
|---|---|
| l.23 "Never-as-worker list" | `/sc:issue` (the claim command) is never dispatched as a worker and gets no `--unattended`; same for /sc:agent, closeout, git, help, pm, sweep, swarm-wizard; /sc:pr-submit while decision D3 holds. |
| l.57 (WC-3, 4th sub-bullet) | Ruling halts (`E-HALT-QA`, `E-NO-RULING`) are never asked of the coordinator; person gives Ruling in chat (decision D2, amended 2026-11-17: person never writes a Ruling line into a file); "other owner records, such as a grant row or a pass record, are still written by the owner". Only mention of "grant row"; names no store or verb. |
| l.241-245 (Git and GitHub ownership) | Coordinator does every GitHub outward action only when the user's instruction names it; targets only IronbellyOrg/IronClaude; "Progress posts (issue comments, project fields)" are coordinator actions made from read contracts; PRs only via `/sc:pr-submit --monitor 3` in a top-level session (D3). |
| l.66 | "Messages carry no `--to`" bullet (kept from WC-17 by PR 682; see s5). |

Coordinator rules (all coordinator-general, none issue-specific):

| Rule | Line | Gist |
|---|---|---|
| WC-6 Every retry is a new Task | 72 | Never `worker-start --retry-of`; retry = new `task-create --spec`, own report dir; 3-failed-starts cap; settle crashed attempt first. |
| "What the coordinator owes each worker" | 82-91 | Brief carries Command: line, report dir, blocked-gate policy, local-commit authorization, worktree placement. |
| Liveness supervision (wait, sweep, S0-S11, ladder L0-L5, acks A1-A4, resume note) | 95-200 | `orca orchestration check --wait --types ...`; 5-min sweep; restart only on Orca stall proof or person's recorded stop. |
| Brief layout / two-copy preflight | 202-228 | Guard line, Chain line, Command: lines; `--unattended` decided by `## Unattended mode` in both command copies. |
| Feature worktree and child worktrees | 230-237 | Orca-default-location worktrees; `--setup skip`; merge child back; never auto-resolve conflicts. |
| Git and GitHub ownership | 239-247 | see table above. |
| Reading a result | 249-258 | succeeded/partial/failed/blocked admission; coordinator starts only Tasks it created (l.258). |
| After an /sc:implement stop (D2) | 260-281 | Freeze/lift; Ruling check conditions (1)-(7); resume Task in halted worktree. |
| Fan-in rule | 283-285 | N<=10 inputs; merge Task only with >=2 admitted. |
| WC-16 Coordinator loop | 287-289 | Coordinator never stops watching its Run; re-arms Orca waits; each wake runs "The sweep" plus `/sc:sweep` (read-only, report never posted, recommends nothing); lists escalations to person; "Phase 1 adds this duty, not a scheduler." No issue/claim wording. |
| Worked example | 291-297 | Troubleshoot gate hit -> blocked -> answer -> T2. |

Worker-side rules in s3: WC-3 (53-58, ask at most once per Task), WC-5 (59), WC-7 (60), WC-12 (61, ack line `ack <message_id> applied|queued|refused`), WC-13 (62, worker never worker-start/dispatch/task-create), WC-14 (63), WC-15 (64), Heartbeats (65), Messages carry no `--to` (66). s2: WC-2 (31), WC-4 (32), WC-8 (40), WC-9 (41), WC-10 (46), WC-11 (47).

### Other places in SNAP tying coordinators to the issue pipeline
- `src/superclaude/skills/orchestration/` does NOT exist in SNAP (ls error). [UNVERIFIED where the orchestration skill lives; it appears in the session skill list from an installed set.]
- `src/superclaude/agents/`: no issue-pipeline or watcher text (only unrelated "coordinate" wording).
- `tests/skills/test_worker_contract.py`: no WC-17 / issue-pipeline / watcher hits; asserts WC-16 text (l.170-171) etc.
- `src/superclaude/hooks/scripts/launch-level-guard.sh:496` comment: "G2 rule 2 (issue-pipeline-guard-g2.md section 5; the rule 1 text of that design is retired, the commands it classed as TAMPER no longer exist)". Only remaining trace in code.
- Still present (not removed): `src/superclaude/cli/issue_watch/` (launch.py, cycle.py, cli.py, ...), `tests/issue_watch/`, `main.py:579` registering `issue-watch`.
- Docs in SNAP: `docs/user-guide/cli-groups.md:20,25,77`; `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md` l.151,190-192,209,267-268,276,287,377,544,668,1052-1074,1416,1445 (watcher/claim chain; l.268 says the contract's coordinator duties for the hand-off were removed in issue 655 PR D and "until it lands no contract rule says who starts that worker"); design notes `docs/designs/issue-watcher.md`, `issue-watcher-setup.md`, `issue-pipeline-fu1.md`, `issue-pipeline-guard-g2.md`, `issue-pipeline-guard-g2-no-to.md`. `docs/designs/orchestrator.md` l.991-1017 holds a removal inventory (PR D rows) but is a separate design: out of scope.

## 2. Removed package inventory (OLD = 01e7a9e23^, dir src/superclaude/cli/issue_pipeline/; 1,597 lines total incl. template)

Deleted 2026-11-19 18:02 -0600 by commit 01e7a9e23 "refactor: retire the old plan-approval gate (issue 655, PR D) (#682)" (36 files, +35/-4599). Commit message states "Nothing ran this code: the issue watcher has enabled: false and never ran live." Package imported from `superclaude.cli.issue_watch` (never the reverse; boundary pinned by `tests/issue_watch/test_module_boundaries.py`, per `__init__.py` docstring).

| File | Lines | Purpose | Key symbols (line) |
|---|---|---|---|
| `__init__.py` | 5 | Docstring only: "the approval core for a coordinator-started plan-writing worker". | none |
| `approval_line.py` | 62 | The only two accepted approval texts; worker-side `check-approval`. | `SHORT="approved"` (18); `_LONG` regex (19); result words `OK/REFUSED_BARE/REFUSED_MISMATCH/REFUSED_MALFORMED` (23-26); `record_id(issue, plan_hash)` (29) -> `ap-<issue>-plan-<first 12 hex>`; `parse(text)` (33); `check(report_dir, names, line, issue=None)` (43). A bare `approved` is refused by the worker check (comment-channel only). |
| `plan_hash.py` | 90 | One SHA-256 over a named list of plan files. | `PlanHashError` (16); `REASONS` 11 closed words (24); `_checked_names` (39); `_read_plan_file` (57); `compute(report_dir, names)` (77) returns `(sorted names, hex)`. |
| `approval_record.py` | 416 | Locked write-ahead store of adoption rows and approval rows. | consts `LOCK_FILE`, `CHANNELS=("label","comment","reply")`, `ADOPTION_STATES`, `APPROVAL_STATES` (37-46); `ApprovalError` (49); `init_dir` (81); `_Guard`/`_locked` (101-122); `_adoption_path` (126); `_approval_path` (132); `_row_is_valid` (177); `_read_row` (206); `_write_row` (225); `adopt_create` (235); `adopt_mark` (268); `adopt_show` (301); `record_create` (313); `record_show` (374); `record_mark` (389). |
| `stage_predicates.py` | 301 | Pure functions deciding plan-stage status from GitHub evidence. | `STATUS_EVENT`, `STAGE="plan"` (44-45); `PlanMarker` (49); `CommentFact` (57); `ChannelResult` (72); `StageStatus` (81); `latest_plan_reply` (118); `_is_allowed_actor` (130); `_edit_of` (141); `_label_channel` (145); `_comment_channel` (192); `_comment_failure` (227); `evaluate(...)` (247). |
| `reads.py` | 161 | Read-only `gh api` projections that turn comment text into booleans/ids (body never leaves jq). | `COMMENTS_JQ` (44); `argv_comments_projected` (65); `_comment_fact` (78); `comments` (107); `StageEvidence` (124); `read_stage_evidence` (130) (events + comments + edits under one `CallBudget`). Reuses `issue_watch.github` (`argv_events`, `argv_edits`, `CallBudget`, `_rest_read`). |
| `release.py` | 66 | Release a bound worker from the launch-level guard (G2 route A): creates `sessions/<session_id>.ok`. | `default_store()` (30) = `~/.claude/state/launch-level`; `ReleaseError` (22); `release(session_id, store=None)` (38) returns `released` / `already-released`; refuses `bad-session-id`, `no-store`, `not-bound`, `not-worktree-level`. O_EXCL|O_NOFOLLOW, mode 0600. |
| `brief.py` | 74 | Builds the plan-writing worker's brief from a fixed template. | `TYPES`, `COMPLEXITIES` (18-19); `BriefRefused` (22); `_sections` (30); `build(issue, type_, complexity, nonce=None)` (51); refuses `bad-issue`, `bad-type`, `type-not-supported` (bug), `bad-complexity`, `bad-nonce`. NO CLI verb called it; only tests did (grep of old tree: callers = tests/hooks/test_launch_level_guard_worker.py and tests/issue_pipeline/test_brief.py). |
| `templates/worker-brief.txt` | 27 | Sections `[head] [marker] [simple] [medium] [complex]`. Head = the 5 fixed contract lines plus `Plan approval: after writing the plan, follow rule WC-17...`, `Report directory: .dev/issues/{N}/worker-plan`, `Worktree: path:<existing worktree>`. Command rows: simple = brainstorm(quick) -> workflow(quick); medium = brainstorm(--blind) -> design -> workflow(standard); complex = brainstorm(deep, research deep, codebase, blind) -> design -> workflow(deep). All `--unattended`, `--handoff none`; rows stop before /sc:implement and /task. `[marker]` adds `Launch marker: [sc-launch:v1:{NONCE}]`. |
| `cli.py` | 395 | Click group `issue-pipeline`; verbs only sequence calls and print closed result words. | `_run_record` (35); `issue_pipeline_group` (57); verbs listed in s3; `_stage_status` (266); `_row_facts` (245); `_make_runner` (220); `_load_stage_inputs` (225); exit codes 1 refused, 2 config, 75 lock-held (29-32). |
| Registration | n/a | `src/superclaude/cli/main.py:581-583` (old) `main.add_command(issue_pipeline_group, name="issue-pipeline")`; removed in 01e7a9e23 (-4 lines). | |

## 3. Removed behaviour map

**CLI: `superclaude issue-pipeline <verb>` (cli.py)**

| Verb | Line | Effect |
|---|---|---|
| `plan-hash REPORT_DIR NAMES...` | 61 | prints `file: <name>` lines and `plan-sha256: <hex>`; refusal `refused:<reason>` exit 1. Worker verb (guard allowed it). |
| `check-approval REPORT_DIR NAMES... --line <text> [--issue N]` | 76 | prints `ok` or `refused:bare|mismatch|malformed|<plan-hash reason>`; exit 1 on refusal. Worker verb. |
| `init APPROVALS_DIR` | 96 | creates dir 0700 and `lock` file 0600 (`approval_record.init_dir`). |
| `adopt-create APPROVALS_DIR --issue N [--stage plan]` | 108 | reserves (issue, stage); only `created` may start a worker. |
| `adopt-mark ... --state started|uncertain [--dispatch-id]` | 117 | adoption transitions. |
| `record-create ... --issue --stage --plan-hash --channel label|comment|reply --evidence-id --actor` | 134 | create approval row or append evidence. |
| `record-show ...` | 161 | prints row JSON. |
| `record-mark ... --state instructed|acked|revoked` | 179 | forward-only transitions. |
| `release-worker SESSION_ID [--store]` | 200 | `release.release`; prints `released`/`already-released`. Coordinator verb. |
| `stage-status ISSUE [--json] [--config ~/.config/superclaude/issue-watch.json] [--approvals-dir] [--plan-dir] [--plan-file ...]` | 335 | read-only; one JSON object (sorted keys). Keys: issue, state, plan_reason, plan_reply_id, plan_hash, record_id, plan_files_checked, approvals{label,comment}, approved, label_revoked, status_seen, assignee_is_host_login, adoption_state, row_state, row_evidence_count. Reads label and approver ids from the watcher config via `cycle.load_config` and `cycle.validate_approvers`. |

**Approval-record format and store [CODE-VERIFIED approval_record.py]**
- Location: a directory the caller names (`APPROVALS_DIR` positional, no default in code, `init` creates it); "of their own, never inside the watcher's state directory and never touching `dispatch.json`" (docstring l.3-5). No default path found in the old tree or designs [UNVERIFIED in practice; the one use I found is test fixtures, `--approvals-dir` in `.dev/tasks/done/TASK-WF-planDecision6BFo-.../retries/T6/prompt-1-1.md`].
- Files: `adoption-<issue>-<stage>.json` (l.126); `approval-<issue>-<stage>-<64hex plan hash>.json` (l.132); `lock` (flock, via `issue_watch.record.FileStore.lock()`, exclusive non-blocking; second caller gets `lock-held`, exit 75). Writes via `swarm.atomic.write_prepared_bytes` + dir fsync.
- Adoption row keys: kind, issue, stage, state, dispatch_id, created_at, updated_at. States: reserved -> started (needs Dispatch id) | uncertain; uncertain -> started. `uncertain` is never restarted by code (`uncertain-launch` / `already-started` refusals).
- Approval row keys: kind, record_id, issue, stage, plan_hash, state, evidence[], created_at, updated_at; evidence entry keys channel, id, actor, time. States: recorded -> instructed -> acked, `revoked` from any non-revoked. A second approval (label then comment) appends evidence to the same row; a replayed (channel,id) changes nothing; new evidence reopens a revoked row. `record_create` requires an existing adoption row (`no-adoption`). All values pattern-checked (`_STAGE`, `_HASH`, `_ID`, `_TIME`); no GitHub text stored.
- Record id: `ap-<issue>-plan-<first 12 hex of plan hash>`.

**Plan hash [CODE-VERIFIED plan_hash.py:77]**: SHA-256 over files sorted by UTF-8 bytes of name; each contributes 8-byte big-endian length + name bytes + 8-byte length + file bytes. Refuses absolute/`..`/duplicate/backslash/NUL names, symlinks at any component, outside-dir, non-file, missing, unreadable. Never prints file text.

**Accepted approval texts (approval_line.py)**: short `approved` (matched whole, no trim; usable only on the GitHub comment channel; bare is `refused:bare` for the worker) and long `approved ap-<N>-plan-<12hex> plan-sha256=<64hex>`.

**Stage predicates (stage_predicates.py docstring l.1-42, `evaluate` l.247)**: plan reply = latest comment by host login carrying hidden marker `<!-- sc:stage:plan id=<record-id> plan=<64hex> -->`, unedited since posting, plan files still hash to marker value. Label channel: approval label applied after plan reply, still applied, actor type `User` and assignee (by login) or approver (by id from approvers file). Comment channel: whole body `approved` or long form, author assignee/approver and `User`, created after plan reply, never edited, long form carries latest reply's id+hash. Both channels give key (issue, "plan", plan hash). Label removal = revocation; Status move after reply = `status_seen` (never required). Equal timestamps never count as "after". Output `StageStatus.state` in: no-plan-reply | plan-reply-invalid | plan-changed | awaiting-approval | approved | revoked. Flags carried, not hidden: actor equals host login; assignee is host login.

**What it wrote to GitHub: nothing.** Every GitHub touch is a read (`gh.user`, `gh.reread`, events, projected comments, edits GraphQL POST-that-reads). Posting the plan reply (with marker), mirroring the label and Status, and mentioning the assignee were done by the coordinator LLM following WC-17 "Issue pipeline duties" text, not by this package. Local writes: approval rows, and `.ok` file under `~/.claude/state/launch-level/sessions/` (`release`).

**Trigger / caller**: no daemon. Callers were (a) the coordinator session following WC-17 / "Issue pipeline duties" for an issue the watcher claimed with `/sc:issue --claim <N> --pipeline none`, (b) the plan-writing worker running `plan-hash` and `check-approval` per WC-17, (c) tests. Nothing in code invoked `stage-status`, `brief.build` or the `adopt-*` verbs automatically. Upstream trigger = the issue watcher (`superclaude issue-watch once`, off by default, `enabled: false`, never ran live per commit message).

**WC-17 (old WORKER-CONTRACT.md l.59, in s3 worker-session duties)**: heading "**WC-17. Plan approval is the reply to the worker's own ask.**" Gist: a brief carrying a `Plan approval:` line makes the worker, after writing the plan, (1) run `issue-pipeline plan-hash`, (2) ask once (does not consume WC-3's one ask) with plan path, file list, hash, (3) wait/resume same message ID, (4) run `check-approval --line <reply>`, (5) send `ack <id> applied|refused` (WC-12), (6) continue only on `applied`; a bare `approved` or any non-reply text is never approval; mismatch = refused ack, stop, refusal word in `worker_done` body. Its last-but-one sentences (ask/send carry no `--to`; guard blocks any `--to` from a bound worker) were kept as a standalone bullet.

**Old "### Issue pipeline duties" (old WORKER-CONTRACT.md l.291-300, coordinator side)**: six bullets. (1) Adopt from sources that exist after `--pipeline none` claim: watcher store's `claimed` entry in `dispatch.json` (read-only) plus `.dev/issues/<N>/issue-summary.md`, `next-steps.md`; one person-opened coordinator owns every watcher-claimed issue on the host. (2) Reserve before starting: `adopt-create` before `worker-start`; only `created` may start; mark `started` with Dispatch id, `uncertain` otherwise; never start again for `uncertain`. (3) Worktree then worker: run `orca_worktree.py worktree --repo <R> --number <N> --base origin/<B> --source <claim issue folder>`, then `worker-start --worktree path:<path> --agent claude --spec <brief>`. (4) Plan approval: post plan reply with hash and file list, mention assignee, read GitHub through `stage-status` at each gate or wake; `record-create` only when worker `ask` carries the plan hash; on approval write row, `reply approved <record-id> plan-sha256=<hash>`, mirror label and Status, mark `instructed` then `acked`. (5) Route B adds no exception to "never answer a person prompt" (types nothing into worker terminal). (6) Never: pass plan boundary without approval row; act on Status move alone; relaunch a dead worker; "post an issue write without that issue's grant row". `COORD-` naming: NOT in the contract text, old or new (`grep -c COORD-` on the old file = 0; snapshot grep also 0).

## 4. Tests removed (all under OLD tests/issue_pipeline/ unless noted; counts = `def test_` per file)
| File | Lines | Tests | Covers |
|---|---|---|---|
| `test_approval_concurrency.py` | 78 | 2 | two processes never make a second row |
| `test_approval_crash.py` | 88 | 3 | kill at worst moment leaves rows that stop a second start (mirrors `tests/issue_watch/test_crash_injection.py`) |
| `test_approval_line.py` | 135 | 9 | the two accepted texts, closed refusal words |
| `test_approval_record.py` | 424 | 21 | adoption/approval row transitions, validation |
| `test_brief.py` | 224 | 12 | brief build, closed refusals; a test keeps template's five fixed lines equal to contract s5 |
| `test_plan_hash.py` | 116 | 10 | hash framing, name/symlink refusals |
| `test_reads.py` | 295 | 10 | jq projection, read budget |
| `test_release.py` | 89 | 7 | `.ok` creation and refusals |
| `test_stage_predicates.py` | 466 | 29 | label/comment channel rules, revocation |
| `test_stage_status.py` | 476 | 13 | `stage-status` end to end with fake runner |
| `__init__.py`, `fixtures/recorded/{OWNER-INPUT.md,README.md,comments-page1.json,edits-page1.json,events-page1.json}` | 0,1,16,143,42,264 | n/a | Responses recorded 2026-11-16 for owner-named issue 452 of IronbellyOrg/IronClaude (read-only GETs; no label event or plan reply present) |
| `tests/cli/test_issue_pipeline_registered.py` | 15 | 1 | group registered in main |
Total removed `def test_` in tests/issue_pipeline: 116 [computed: 2+3+9+21+12+10+10+7+29+13].
Edited (not deleted) in the same commit: `tests/skills/test_worker_contract.py` (-62/+: dropped RULE_PHRASES entries `issue-pipeline-duties`, `wc17-plan-approval`; dropped adoption-source tests `_adoption_bullet`, `_check_adoption_sources`, `test_adoption_names_only_sources_that_exist_after_pipeline_none`, `test_adoption_check_fails_when_worktree_json_is_named`, `test_issue_pipeline_duties_allow_no_typing_into_a_worker_prompt`; added `messages-carry-no-to` phrases and `test_the_no_to_rule_sits_in_the_worker_session_duties`). `tests/hooks/test_launch_level_guard_worker.py` (-56): dropped `from superclaude.cli.issue_pipeline import release`, the parametrized TAMPER test for pipeline verbs (6 commands) and the plan-hash/check-approval allowed test; release now a typed `/sc:implement` prompt; nonce binding test uses `_marker(nonce)` instead of `brief.build`.

## 5. What changed in WORKER-CONTRACT.md and launch-level-guard.sh (01e7a9e23)
- WORKER-CONTRACT.md (numstat +1/-12): removed WC-17 bullet (old l.59) and the `### Issue pipeline duties` section (old l.291-300); added bullet "**Messages carry no `--to`.**" (now l.66) holding the WC-17 sentence the guard rule relies on (commit message: fixes "missing contract text for the worker side of guard rule 2 (finding F14 of issue 665)"). The brief template (s5) in the old tree had no `Plan approval:` slot; the line existed only in `templates/worker-brief.txt`.
- launch-level-guard.sh (source and plugin copy, byte-identical, `plugins/superclaude/hooks/scripts/...`; numstat +2/-5 each): removed OLD l.441-444 the G2 rule 1 `case $T in *release-worker* | *release_worker* | *issue-pipeline*adopt-* | *issue-pipeline*record-* | *issue_pipeline*release* | *issue_pipeline*approval_record*) LL_CLASSES+='TAMPER ' ;; esac` (plan-hash and check-approval were deliberately left allowed). Kept G2 rule 2 (bound worker may run `orchestration send|ask` only as one plain call with no `--to`) and the guard's own `sessions/<sid>.ok` release path; comment at new l.496 rewritten.
- Also in commit: `main.py` -4 (registration); `docs/user-guide/cli-groups.md` (issue-pipeline rows removed; lines 25 note); `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md` +1 sentence at l.268 (see s1); `CHANGELOG.md` +4 ("Removed: the old plan-approval gate (issue 655)"; says guard "still lets a bound worker run `orchestration send` and `ask` without `--to`, and the person's typed `/sc:implement` still releases it").

## 6. Proposed deep-research assignments (max 2)
1. **Current text.** Trace, for the technical reference, exactly what the snapshot's contract says a coordinator does with an issue claimed by the watcher (answer: nothing issue-specific) by reading SNAP WORKER-CONTRACT.md s4 end to end against `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md` l.190-290 and l.1052-1145, the `/sc:issue --claim --pipeline none` flow in `skills/sc-issue-protocol` and `orca_worktree.py`, and the `sc-orchestration`/`orchestration` skill wherever it is installed. Output: who starts the worker after a claim today, with file:line, and which rules (WC-6, WC-13, WC-16, Git and GitHub ownership l.239-247) bind that coordinator.
2. **Removed code.** Reconstruct the removed approval gate's data flow and security properties end to end from OLD tree: coordinator verbs -> approval rows -> `stage-status` GitHub reads -> `reply approved <id> plan-sha256=<hash>` -> worker `check-approval` -> `release-worker` `.ok` file -> guard release; cross-read OLD `docs/designs/issue-pipeline-guard-g2.md`, `issue-pipeline-fu1.md` and `issue-watcher.md` sections on approvals/approvers/edit-history, and the `.dev/tasks/done/TASK-WF-planDecision6BFo-20261114-174909` plan that built it (Plan B Tasks 3,5,7,9,13,14). Output: removal rationale, what safety properties (plan-hash binding, approver checks, revocation, edit detection, write-ahead adoption) existed and which were reassigned or dropped.

## 7. Gaps
- Approvals store default path: no default in code; real deployment path unknown [UNVERIFIED].
- `COORD-<RepoName>`, "grant row", "zero-setup watcher", "issue pipeline duties accepted": appear only in owner memory notes in the session context, not in any file I read; the snapshot contract has the phrase "grant row" once (l.57) and no definition. I did not search `.dev/` trees or `docs/designs/orchestrator.md` for them.
- The `orchestration` skill is not under SNAP src/superclaude/skills; its coordinator text was not read.
- Old `sc-issue-protocol` skill and `orca_worktree.py` (claim script) were not read for what they said about the pipeline hand-off beyond what the contract and tech reference quote.
- Old `docs/designs/*` (issue-pipeline-guard-g2.md, fu1) were skimmed only (headers, s1-s5 titles), not read in full; `issue-watcher.md` approval/approver sections not read.
- Did not read the unread bodies of `approval_record._row_is_valid`/`_read_row` (l.177-232), `stage_predicates._comment_channel`/`_comment_failure` (l.192-245), `reads._comment_fact` (78-105), `cli.py` verb bodies l.100-199; summaries there come from signatures and docstrings.
- Test counts are a `def test_` grep (parametrized cases not expanded).
