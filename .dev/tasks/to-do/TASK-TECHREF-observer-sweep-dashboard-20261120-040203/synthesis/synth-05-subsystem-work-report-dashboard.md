# Synthesis 05: Technical Reference sections 5.5 and 5.6 (work report and living report; #409 dashboard design package)

Inputs: research/05-agent-work-report-living-report.md, research/06-dashboard-design-vs-observer-gaps.md, gapfill-c1-GF1, GF2, GF3, GF4 (run.py CLI only), GF5, gaps-and-questions.md, qa/qa-research-consolidated-findings.md (M-1 to M-17). Where a gap-fill file supersedes 05 or 06 it is the authority (GF1 writer label, GF3 orchestrator overlap and PR chain, GF5 package pipeline). Code paths are relative to origin/master 61ac2c2e6 (read-only export `/home/coder/.cache/ic-snap-20261120/master`) unless marked "checkout". Nothing was run. UNVERIFIED items stay UNVERIFIED. Facts and overlaps only; no unification recommendation.

### 5.5 Agent-work-report pipeline and the living report

**Purpose:** The `agent-work-report` skill builds one daily report of Clay's open work (both Ironbelly GitHub orgs, Projects boards, ClickUp, Orca agent sessions) with 16 scripts, a model-written judgement layer and a checked delivery gate. Since PR C (#684, merged 2026-11-20T02:01:07Z, d7d645ddd) it also keeps a "living report" page from per-issue entry files that an orchestrator is designed to write. The reader side is built; the writer is not (built-versus-designed table below).

**Key Files** (under `src/superclaude/skills/agent-work-report/`; scripts total 5,777 lines, 5,971 with SKILL.md; research 05's "6,321" is wrong, M-8):

| File | Purpose |
|---|---|
| `SKILL.md` (194 L) | the behavioural spec: 15 steps (76-95), statuses (140), gate (152), boundaries (192-194) |
| `scripts/run.py` (887) | run lock, gate, summary, close, abandon, log, refresh, status |
| `scripts/common.py` (507) | state paths, `repo_root()`, `run_cmd`, entry-file reader and contract comment (133-151), fixed vocabularies |
| `scripts/collect.py`, `clickup.py`, `sessions.py` | GitHub, ClickUp, Orca-terminal-and-transcript collectors |
| `scripts/exclude.py`, `match.py`, `classify.py`, `compare.py` | Steps 4b to 7: leave out held issues, join, group, diff against the previous run |
| `scripts/activity.py`, `render.py`, `check.py` | Steps 8, 9, 11: evidence file, writing sheet, seven script checks |
| `scripts/page.py`, `waker.py`, `orca_term.py`, `prefs.py` | page, server and Orca tab; coordinator wake; Orca terminal verbs; priority and answer log |
| `config.json` (14 keys), `templates/` (7 files) | M-14 key list (`person`, `orgs`, `timezone`, `session_tag`, `automation_prefix`, ...); `qa-report-template.md` is unreferenced and stale |
| `tests/skills/test_agent_work_report.py` (4,005 L, 142 `def test_`) | fakes patch `gh_json`, `run_cmd` and the ClickUp `call`; no live call; results not run (UNVERIFIED) |

**How It Works:**

```
gh (2 orgs) ------> collect.py \
ClickUp GET ------> clickup.py  >-> exclude.py -> match -> classify -> compare -> activity -> render
Orca + transcripts > sessions.py/     ^ orchestrated/*.json (no writer in the snapshot)
model writes overview.md -> check.py --links -> page.py + summary -> run.py gate -> ClickUp DM / Orca tab -> run.py close
```

Pipeline and run-folder artifacts (state `<orchestrator repo>/.dev/coordinator/`, run folder `runs/<%Y%m%dT%H%M%SZ-kind>/`; step numbers and commands match the script usage lines, **[CODE-VERIFIED]**):

| Step | Script | Reads -> writes |
|---|---|---|
| 1 | `run.py open daily` or `on-demand` | lock, `wakes/` -> `run.json` (run, kind, started, previous_completed_run, stuck_run_replaced), `run-log.md`, `wake-records.json`, `automation-runs.json`, `incomplete-runs.json`, `run.lock` |
| 2 | `collect.py` | config orgs -> `github-items.json`, `coverage.json` (repos, boards, source_errors) |
| 3 | `clickup.py` | token, previous run -> `clickup-items/events/gone/status/replies.json`, `settings.json`; model logs DM answers with `prefs.py answer` |
| 4 | `sessions.py` | hook file, transcripts, /proc -> `sessions.json`, `sessions-status.json` |
| 4b | `exclude.py` | `orchestrated/*.json`, `coverage.json` -> `excluded.json`, rewritten items and sessions, two `*-before-exclude.json` copies |
| 5-7 | `match.py`, `classify.py`, `compare.py` | -> `items.json`, `merged-into.json`; `classified.json`; `snapshot.json`, `compare.json` (new, changed, closed, unchanged, carried) |
| 8-9 | `activity.py`, `render.py` | -> `activity.md` (others' text only as `> ` quoted lines); `overview.md` stub, `to-write.json` |
| 10 | model edits `overview.md` | never calls GitHub, ClickUp or Orca (SKILL.md:10) |
| 11 | `check.py --links` | -> `script-checks.md` (table plus `overview sha256: <hex>`); exit 1 on any FAIL |
| 12 | `page.py`; `run.py summary`, `gate`, `refresh --run` | -> `report.html`, `notes.json`, shared `.dev/coordinator/report.html`, `summary.md` |
| 13 | `page.py --open`; model posts `summary.md`; `clickup.py dm`; `run.py log ... delivered` | -> `clickup-dm.json` (sent, detail), `action-log.jsonl` |
| 14 | `run.py close`; model runs `git add .dev/coordinator && git commit` | -> `complete.json`; never push; no script runs `git commit` |
| 15 | `prefs.py priority` or `answer` | -> `priorities.json`, `action-log.jsonl`. Not in SKILL.md's table: `abandoned.json` (`run.py abandon`), state-folder `refresh.lock` |

Six statuses (SKILL.md:140; `common.SESSION_STATUSES`; Orca's own session state is never read, SKILL.md:38). Thresholds appear only in SKILL.md:140; no script computes them; `check.py` enforces only the form `status: <one of six>: <reason>` and the "Needs you" two-way match:

| Status | SKILL.md definition | Inputs the model sees (`activity.md`) |
|---|---|---|
| working | running, active in last 15 min | `Claude running`, N events since previous report, last activity |
| progressed | worked since previous report, now at rest | event count, last 3 prompts, last reply |
| waiting on you | last turn asks Clay, or a tool call waited over 15 min | quoted last reply, "stopped on a <tool> call with no result since <time>"; `ends_on_question` and `pending_tool_call` live in `sessions.json` |
| stuck | same error or step repeating | last 2 errors; `repeated_steps`, `error_count` are in `sessions.json` only, never printed |
| stalled | nothing since previous report, or Claude gone | event count 0; script rule `render.carried_status` for unchanged items |
| done | it reports the work finished | quoted last reply; session kept in `sessions.json` until a report called it done |

Who writes a status: the model for sessions on new or changed items; the script for unchanged items (`carried_status`); the entry file's `session_status` map for a held issue (nobody writes it today). Groups: assigned, owned, opened, inprogress, candidate, other (a session on no item is `inprogress`). Priority: `priorities.json`, then board priority, then `config.json` labels, then the person's own text, else Unset; order by level (Urgent, High, Medium, Low) then state.

**Lock, gate, carry-forward.** `run.lock` is `{run, kind, started}`; a lock younger than `time_budget_minutes` (daily 120, hourly 10) writes `wakes/*-skipped.json` and exits 3; an older one is kept as `stuck` and replaced. Delivery gate (`run.py:204-368`): seven checks PASS (placeholders, template, sessions, carry-forward, needs-you, candidates, links) plus the sha256 chain: `check.py` writes `overview sha256` into `script-checks.md`, `page.py` writes `<meta name="overview-sha256">` into `report.html`, `summary.md` must equal `build_summary` byte for byte, and `gate` recomputes all three. `clickup.py dm` enforces the whole gate and sends only `<run>/summary.md`; `run.py close` enforces only checks plus sha, so SKILL.md:183 is **[CODE-CONTRADICTED]** in part. Carry-forward invariants: every previous-snapshot item is listed, closed, counted quiet or in `excluded.json` (`check.py`); `compare.py` closes an item only on evidence (`gh ... view`; HTTP 404/410 means "no longer visible"; any other error carries it); items of a repo or org that failed to read, and sources not read, are carried unchanged.

**Data sources and exact commands** (all list-argument `run_cmd`, no shell, bare `orca` and `gh`; no `--repo IronbellyOrg/IronClaude` because both orgs are read; no SuperClaude-Org target):

| Source | Commands | Read or write |
|---|---|---|
| GitHub | `gh repo list <org> --limit 1000`; `gh issue list` and `gh pr list --repo <o>/<r> --state open --limit 1000 --json ...`; `gh project list --owner <org>`; `gh project item-list <n> --owner <org>`; `gh search issues --owner <org> --involves <person> --state open [--include-prs]` (collect); `gh api --paginate --slurp repos/<o>/<r>/issues/<n>/timeline`, `gh pr view <url> --json mergeable,isDraft,reviewDecision,statusCheckRollup` (activity); `gh issue or pr view <url> --json state,closedAt` (compare); `--json number` (check); `gh issue view <n> --repo <r> --json state,stateReason,assignees` (run) | read only |
| ClickUp | `urllib` GETs to `api.clickup.com` (`/v2/user`, `/v2/team`, tasks, comments, v3 chat); POST only in `send_dm` (`.../channels/direct_message`, `.../channels/{cid}/messages`); `CLICKUP_API_TOKEN` required, never the connector | read; one write |
| Local | hook file `~/.config/orca/agent-hooks/last-status.json` (version 2), `~/.claude/projects/*/*.jsonl`, `/proc/<pid>/environ` (`ORCA_TERMINAL_HANDLE`, `CLAUDE_TOPIC`), `git -C <path> remote get-url origin`; terminal join fields `tabId`, `leafId`, `handle`, `worktreePath`, `connected`, `lastOutputAt` (sessions.py:323-330) | read |

What it WRITES outside run and state folders (**[CODE-VERIFIED]**): (1) a ClickUp DM to the token owner's own DM channel (`clickup.py dm` after the gate; `waker.notify`); (2) an Orca unread mark and comment on the orchestrator repo workspace (`waker.notify` fallback); (3) text typed into the coordinator's Orca terminal (`/clear`, `Wake (daily report): run /agent-work-report for today's report.`, `ccsession coordinator`) and a new terminal; (4) an Orca browser tab at `http://127.0.0.1:8765/report.html`; (5) a detached `python -m http.server 8765 --bind 127.0.0.1 --directory <.dev/coordinator>`, which serves the whole folder (`settings.json` with ClickUp user and DM channel ids, `action-log.jsonl`, run folders); (6) a git commit in the orchestrator repo, by the model at Step 14. The page loads Google Fonts and makes no other outside request.

**Living report.** Entry-file contract (common.py:133-151), path `.dev/coordinator/orchestrated/<owner>__<repo>__<N>.json` (`closed/`, `info/<kind>__<key>.json`):

| Fields | Read by | Written today by |
|---|---|---|
| `url`, `title`, `priority`, `assignees`, `human_assignee`, `author`, `orchestrator{}`, `worker{}`, `pr_url`, `last_update`, `session_status`, written parts (`state`, `next`, `what`, `state_text`, `done`, `todo`, `happened`, `recommend`, `needs`, `how`), `suggested`, `priority_why` | `exclude.py`, `run.py refresh`, `render.entry(filed=)`, `common.entry_session_ids` | nobody in the snapshot; designed writer `superclaude orchestrator report-entry` (PR B); tests build entries by hand |
| `closed_at`, `close_reason` | `run.py` | this skill: `move_to_closed` (run.py:483), the only entry-file writer in the snapshot |
| `kind`, `group`, `follow_up_state` | no code | nobody (`follow_up_state` only in a test fixture and the design header) |

- `exclude.py`: a candidate is an issue assigned to the person in a repo read without error; it removes the issue url, the entry's `pr_url` and each `orca://session/<id>`; keeps unreduced copies so a rerun is identical; `closed/` and `info/` exclude nothing; no external command. With no entry files it excludes nothing.
- `run.py refresh` (7 stages: lock check, reconcile via `gh issue view`, prune by `info_ttl_days` 14, read base overview, drop held blocks, add entry blocks, build the page with `page.main`): exclusive flock on `refresh.lock`; without `--run` it does nothing while a daily run holds the lock; rewrites only the shared `report.html`; fake-tested, no live run recorded.
- `waker.py morning`, `hourly`, `check-missed`: finds the `coordinator` session by process environment, types `/clear` and the wake line, retries 15 x 120 s (morning only), counts SENT only when a run folder appears; failure becomes `DM_NEEDED` and `notify`; `hourly` is a recorded skip.
- `orca_term.py`: `terminals`, `screen`, `is_idle`, `send` (the only terminal-writing function; waker only), `claude_processes`, `find_session`, `typing_or_fresh` (unsafe if draft text or output under 60 s).

**Built versus designed** (61ac2c2e6; sources research 05 s29, GF1 3.7, GF3 s7 and s8):

| Capability | Status |
|---|---|
| Skill, 15 steps, run lock, sha gate, carry-forward; `exclude.py`, `run.py refresh`, `render.entry(filed=)`, `waker.py` | built (PR #684), fake-tested |
| Design #681, plan-gate retirement #682, `/sc:closeout` #683 | merged |
| `superclaude orchestrator report-entry`, `src/superclaude/cli/orchestrator/`, `/sc:orchestrator`, `sc-orchestrator-protocol` | designed (PR B); absent; no PR. `cli/main.py` has no `orchestrat` match; closeout's `settle.sh:1037-1042` prints `ENTRY escalated key=<k> why=surface_absent` |
| Poll wakes the orchestrator and `orchestrator_repo` key (PR A #686); `/sc:issue --plan` (PR P #690) | open, unmerged; master `_TOP_KEYS` rejects `orchestrator_repo` (cycle.py:216-220) |
| Orca automations `coordinator-morning-wake`, `coordinator-missed-check`, `orchestrator-poll`; orchestrator repo `IronOrchestrator`; spec `SPEC-AGENT-WORK-COORDINATOR-20261027.md` | outside the repo: **[UNVERIFIED]** (triggers of `waker.py` included) |
| Daily report phased out for the living report (owner ruling 1) | designed; code still runs the daily pipeline |

**Wording rule (R-C8).** Living-report writer: KNOWN LIMIT (cited), sequenced to PR B (C8-6); `orchestrator_repo` route: KNOWN LIMIT, sequenced to PR A (C8-7), who sets it is **[UNVERIFIED]**, `$AWR_ROOT` works today; `prefs.py answer <run> <session url> session` (SKILL.md:172, `prefs.py:20`): **DEFECT-CANDIDATE** (C8-8); remediation task not created (read-only brief); flagged for the owner. Declaring lines, evidence and residual facts are in 14.5.

**Public Interface:**

```
run.py open <daily|hourly|on-demand> | gate|summary|close <run> | abandon <run> <reason> | log <run> <action> <item|-> <reason> | refresh [--run <run>] | status   # exit 3 = run active
collect|clickup|sessions|exclude|match|classify|compare|activity|render.py <run>;  check.py <run> [--links];  page.py <run> [--open];  clickup.py dm <run> <message_file>
prefs.py priority <run> <item url> <Urgent|High|Medium|Low|clear>;  prefs.py answer <run> <url|-> <session|clickup-dm>;  waker.py morning|hourly|check-missed
common.repo_root() -> Path   # $AWR_ROOT, else orchestrator_repo in ~/.config/superclaude/issue-watch.json (dir must hold repos.yaml)
```

**Dependencies:**

| Depends On | Type | Description |
|---|---|---|
| `gh`, `orca` (bare binaries), ClickUp REST | CLI / API | collection, terminals, tabs, DM |
| Orca hook file, Claude transcripts, `/proc`; `ccsession`, system `python3` | local files / CLI | session facts; wake typing; page server |
| `<orchestrator repo>/.dev/coordinator/` via `$AWR_ROOT` or `orchestrator_repo` | state folder | all run state; repo outside this checkout |

**Consumers:**

| Used By | How |
|---|---|
| Clay | page at 127.0.0.1:8765, ClickUp DM of `summary.md`, Orca unread mark |
| `sc-closeout-protocol` `settle.sh` `cmd_entry` | calls the absent `report-entry` verb; ends `surface_absent` |
| Orca automations (outside the repo) and the `coordinator` session | start `waker.py`; run `/agent-work-report` |
| designed orchestrator | would write entry files and call `run.py refresh`; no code in the snapshot does either |

**Conventions & Patterns:**

- Run subprocesses only through `common.run_cmd` (list args, no shell; exceptions `page.py:318`, `sessions.py:119`). The model writes only judgement parts, never calls GitHub, ClickUp or Orca; others' text enters as `> ` quoted lines.
- Deliver only after `run.py gate` PASS; send the ClickUp DM only from `<run>/summary.md`; commit `.dev/coordinator` in the orchestrator repo, never push.
- A new session status needs `SESSION_STATUSES` and `check.STATUS_OK` edits; links must be `http(s)://` or `orca://`; symlinked entry files and folders are refused.
- An entry writer must use the `WRITTEN` slot names plus `session_status`, `pr_url`, `orchestrator`, `priority_why`, `suggested`. Treat SKILL.md:14, 172, 183 as corrected above; design DQ13 "Watching" is **[CODE-CONTRADICTED]** (code: "Other work in progress").

### 5.6 Orca dashboard design package (issue 409) and its relationship to the observer

**Purpose:** The #409 package is "a design collaboration branch, not a production integration" (README.md:9): 20 synthetic terminal-dashboard designs (two sets of ten) with a Python/Pillow prototype renderer, drawn only from a synthetic fixture schema that is explicitly not an Orca API. The shipped observer (`superclaude observe`, Python and Rich) implements three of the designs in reduced form and shares no code or fixture data with the package. Provenance: package root (checkout) `/home/coder/workspaces/IronClaude/.dev/design/orca-observer-20261106/` on docs branch `docs/409-orca-dashboard-designs`, commit 495eb96d1, which is not an ancestor of origin/master and has no PR; the same 406 files are on origin/master through PR #503 (merge 9e2608b03, 2026-11-11T19:54:57Z; REST list 545 files, `gh pr view` truncates at 100; #673 lists 2,831). `.dev/research/orca-dashboard-20261105/` is **LOCAL-ONLY, untracked** (0 files in HEAD and origin/master); it is the origin of the R-rules and is cited below only as local-only.

**Key Files** (package paths relative to the package root; counts re-made in research 06 s1: 406 files, 20 designs, 18 scenarios plus base, 360 exports, 2 galleries, 2 PDFs, fixture sha256 `1f17a907...bd42e4`):

| File | Purpose |
|---|---|
| `README.md`, `DESIGN-CONTRACT.md`, `concepts.md`, `data-dictionary.md`, `integration-gaps.md` (28 L), `sources.json`, `QA.md` | self-description, contract (navigation only), provisional picks, schema, six "not established" items, E01-E13 evidence, QA verdict |
| `render.py` (130), `fixtures.py` (122), `canvas.py` (122), `layouts/group_a.py`, `group_b.py`, `agent_focus.py`, `requirements.txt` (Pillow==13.0.0, wcwidth==0.9.4) | renderer, fixture builder, Canvas, layouts: set 1 (signal-bridge, fleet-quilt, time-loom, worktree-atlas, decision-desk, proof-gate, budget-engine, relay-map, delta-deck, watchkeeper), set 2 (leverage-board, attention-ledger, handoff-switchboard, loop-detector, collision-lens, outcome-ledger, revision-drift, mission-pulse, owner-load, shift-brief) |
| `tests/test_designs.py` (19 tests), `tests/test_gallery.cjs` | unittest on fixtures, sanitizing, layouts; Node DOM stub (no browser); count verified, pass result **[UNVERIFIED]** |
| `.dev/issues/409/` (origin/master; checkout copy) | `owner-decisions-20261108.md`, `owner-direction-record-20261116.md`, `bmad/spec-orca-observer/*` (`release-gates.md`, `unverified-register.md`, `rendering-rules.md`), `visual-parity/REDESIGN-SPEC.md` |
| `src/superclaude/cli/observe/` (origin/master) | shipped observer: 13 top-level `.py` files (6,011 L), `snapshot.schema.json` (158 L); registered `cli/main.py:590-592` |

**How It Works:**

```
render.py [--batch 1|2] [--show SLUG] [--width N]     # --width only with --show; export mode renders 160, 116, 80
 -> exports(batch) -> write_fixtures(ROOT)            # fixture.json + scenarios/ (9 variants + 9 scale); both batches rewrite ROOT
 -> designs(batch) -> screen(spec, fixture, width) -> Canvas -> layout fn (c, f, metrics(f))
 -> six files per design and width (.txt .ascii.txt .ansi .svg .png .mono.png) -> contact-sheet.png, portfolio.pdf (160-wide PNGs)
 -> manifest.json (+ fixture sha256) -> gallery.html (19 scenarios x 10 designs x 3 widths, pre-rendered, no fetch)
```

- `--batch 2` swaps only the layout module (`layouts/agent_focus.py`) and the output folder (`agent-focus/`). README commands (README.md:24-28) are documented, not run; the DejaVu font path is read at import and not checked; README.md:44 is **[UNVERIFIED]**. No defect candidate in the pipeline; facts: `--width` is ignored in export mode; `test_export_manifest` skips `.mono.png`, contact sheet, gallery and hash.
- Fixture schema (proposed, not Orca; `data-dictionary.md:3`, `sources.json` E13): top-level keys `synthetic, as_of, variant, sources, orchestrators, sessions, worktrees, requests, edges, events, scope, previous`; five fake sources `demo:*`. A session has no PR, issue, url or session-open field (`fixtures.py:30-43`). Real Orca fields are the 31 worker-list keys the observer parses (`parse.py:58-90`) plus the question message row; `projection.attention`, `parent`, `resource`, `id` are present but redacted and unparsed (meaning **[UNVERIFIED]**); admission, revision, cost, timeline, edges and events have no verified Orca counterpart.
- Reads and writes: the package reads and writes neither GitHub nor ClickUp (`fixtures.py:1`: no adapter, environment or network); neither do the observer or sweep (grep; `sweep/probes.py:1-7`).
- Name parity: all 9 variant names plus base appear verbatim as observer fixtures (`parse.py:750-761`); content parity 0 of 10 (`cmp` differs; observer keys are `variant, description, cycles`). Package-only: 9 `scale-*`; observer-only: 8 `golden-*`, `question-cap-100` (19 files). Code reuse is banned on record (`ARCHITECTURE-SPINE.md:172`, `SPEC.md:76`, `sanitize.py:3-4`); `rendering-rules.md:3` ("the package's synthetic fixtures") is **[STALE DOC]**. Eight palette colors match exactly (`theme.py:59-69` and `canvas.py:7`).

| Design | In the observer | Evidence |
|---|---|---|
| Signal Bridge | partly (view A): worker ledger, counts and freshness strips; no owner or SIGNALS bars | `view.py:48`; `REDESIGN-SPEC.md:75-76` |
| Attention Ledger | partly (view B): `COORDINATOR QUESTIONS` for one named Run | `view.py:54,69-84`; `REDESIGN-SPEC.md:78,82` |
| Decision Desk | partly (view C, minimal): one question, one linked session | `view.py:97-112,888-948` |
| other 17 | none (0 name hits); PR #673 (closed #606) targets exactly three (`REDESIGN-SPEC.md:9`) | spec and code grep |

Rules S1-S11 (package) and R1-R11 (local-only research) are a scope-discovery grouping, not numbers in any source file. Status in the shipped observer (06 s5; where 06's takeaways group S1, S2, S4 loosely as "by absence", its rule table is the stronger evidence):

| Status | Rules |
|---|---|
| ENFORCED | S3, S6, S7, S8 (`commands.py` builds no argv; allow-list in `adapter.py`), S9 (own sanitizer), S11 (labelling), R3 (other wording), R4 (non-consuming reads, `adapter.py:34-50`) |
| BY ABSENCE | S1 (`unavailable (no source)`, `view.py:134`), S2 (no git or overlap data) |
| PARTLY | S5, S10, R1, R2, R6, R7, R8, R9, R10 |
| NOT BUILT | S4 (scope on record: `release-gates.md:17`, `unverified-register.md:69-71`); hold/pause (S10, package-only); R5 (`--types question` instead); superseded attempts (R8); secret redaction (R9) |
| FG-1..14 (R11) | open: 1-7, 10, 12; FG-8 closed for the owner's own Run, **[UNVERIFIED]** for non-owners; 9 avoided; 11 n/a; 13, 14 partly |

| integration-gaps item | Status now |
|---|---|
| 1 non-consuming enumeration beyond 100 rows | partly closed (owner's own Run); still capped at 100, newest first |
| 2 joins across hosts | partly closed for one Run on one host (QUESTION-LINK); cross-host open |
| 3 admission, revision, human owner | open; 4 cost telemetry: open; 5 durable replay: open (source-loss handling built, S7); 6 deep links: open, no click-to-open |

Contradictions between the issue-409 body, the package and the code (stale body lines 19, 36, 27, 28, 204; "unmerged, no PR"; Bubble Tea versus Python and Rich; reply, ack and resolve versus navigation only; 405 versus 406 files; "No direction chosen") are settled in 14.4 A (SD-21 to SD-29) and 14.3.

**QA verdict and direction.** `QA.md:19`: "FAIL for the inspected pre-correction snapshots" (4 blocking findings); corrections were made with "No new independent post-correction verdict" (`QA.md:29`); Playwright check failed (Chrome absent). The package chose no design (`concepts.md:43-49` picks are "not user approval"). The live body says "No direction chosen" (stale); `owner-decisions-20261108.md:5-9` and `owner-direction-record-20261116.md:2-5` record a staged order (worker list, questions, third screen later), mapped by `release-gates.md:3,10` to Signal Bridge, Attention Ledger, Decision Desk (DIRECTION-SELECTED passed 2026-11-16); the owner's record names an order, not designs, and no package-ranked pick was adopted. Parity gate: PASS on the text and ANSI tier (PNG route failed).

**D-1 (C8-9, DEFECT-CANDIDATE).** `--questions` with `--fixture` is refused (exit 2) in `observe/commands.py:77-78, 183-188`, so the question ledger and Decision Desk cannot be replayed from fixtures; live R2/R3 are wired. No cited scope decision; remediation task not created (read-only brief); flagged for the owner. Declaring lines, evidence and the owner question are in 14.5.

**Overlaps (facts).** Reviewer asks of 2026-11-11 (issue links, PR links, plain-English summary, session-open link, step flow; issue comment, 14:47:52Z): live body line 98 says none is built; no observer or package row has a link. The report skill has counterparts, assembled here from 05 and 06 (neither states the mapping): GitHub urls and `linked_issue`/`linked_pr`, `orca://session/<id>` links, model-written "What it is" and "Current state"; no step-flow field (nearest: "Done with evidence", "Still to do"). Sweep layout and dimensions: `orchestrator-mode.md:609` "The layout is SPEC section 9 ... copied from #409 at `495eb96d`"; `sweep/models.py:162-164` "The #409 dimensions, nine fields ... dimension 9 'policy' ... report-only, never JSON keys" (06 cites fragments; wording re-read). "Observer reads the sweep JSON" is an undecided proposal only (body lines 82, 110-112, 204; alignment items 1-10 undecided; no code or design); JSON v1 lacks dimensions, links and step flow.

Orchestrator design overlap (mentions, about 30 Orca verb forms, the five status vocabularies): see 2.5, 8.1, 8.2 and 12.2. PR chain: merged #539, #503, #514, #577, #592, #598, #673, #681-#684; open #686, #690; PR B none.

**Public Interface:**

```
render.py [--batch {1,2}] [--show SLUG] [--width N]    # defaults 1, 116; NO_COLOR present disables ANSI
fixtures.fixture(owners=8, count=80, variant="base"); metrics(f, owner=None); write_fixtures(root)
render.designs(batch=1); render.screen(spec, f, width, ascii_mode=False) -> Canvas   # layout fn (c, f, m)
```

**Dependencies:** Pillow==13.0.0, wcwidth==0.9.4, DejaVu Sans Mono (hard-coded path), Node (gallery test), `uv` (README command). **Consumers:** the observer spec (names, intent, palette, no code); `orchestrator-mode.md:609` (layout pin at `495eb96d`); reviewers (gallery, PDFs). Nothing imports the package.

**Conventions & Patterns:**

- Cite `.dev/research/orca-dashboard-20261105/` only as local-only and untracked; never as repo evidence. Cite package files by checkout path and code by origin/master path.
- Write "20 designs, 3 partly implemented"; never say the package fixture schema feeds the observer, or that the owner picked a package design.
- Keep UNVERIFIED: package test results, `sources.json` E01-E04 against the installed Orca, non-owner non-consumption, `projection.attention` meaning, FR-9 mapping.
- Apply R-C8 to any "required but unwired" capability: a cited decision gives KNOWN LIMIT, none gives DEFECT-CANDIDATE.
