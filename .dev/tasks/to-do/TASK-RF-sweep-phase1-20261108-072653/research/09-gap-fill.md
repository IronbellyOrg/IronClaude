# Research: Gap fill (research gate round 1)

**Status:** Complete
**Date:** 2026-11-08

---

Short names: GAPS = `.dev/tasks/to-do/TASK-RESEARCH-orchestrator-supervision-20261107-073942/gaps-and-questions.md`; REPORT = the `RESEARCH-REPORT-orchestrator-mode.md` in the same folder; NOTES = `research/research-notes.md` in the same folder; DESIGN = `docs/designs/orchestrator-mode.md`; SPEC = `.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md`; APPROVED = `.dev/orca-command-refactor/decisions/APPROVED.md` (read at `5dc29d23`, 90 lines). All line numbers were read on 2026-11-08.

## Gap 1. Owner decisions at step 1.0b

What step 1.0b asks (DESIGN:907): "Owner decisions GQ-10, GQ-11, GQ-35, GQ-61, GQ-63, and sign-off on the D9 narrowing of SP-29 (section 13); read `.dev/orca-command-refactor/decisions/APPROVED.md`; record in `.dev/tasks/<pkg>/artifacts/owner-decisions.md`". Gate effect (DESIGN:926, :988): steps 1.17 to 1.19 do not start until these are answered; GQ-11 is a hard gate (REPORT:1238 says "working default accepted" counts only when the owner says it). REPORT:1238 also maps each decision to the steps it blocks; that mapping is quoted per row below.

| GQ | Question (quoted) | Options | Recommended or working default | Blocks (REPORT:1238) |
|---|---|---|---|---|
| GQ-10 | "G7 / AMBIGUITY 3: where the sweep report is written" (GAPS:33; status "open (owner decision)", "No source fixes a location.") | NOTES:305: "under `.dev/tasks/` (always staged by rule) or another `.dev/` folder; dated file name format." | DESIGN and SPEC already commit to `<root>/.dev/sweeps/` as the default (DESIGN:13, :914; SPEC:60), gitignored (SPEC:119 FR-025, DESIGN:63 GQ-106). REPORT:1249 calls it the "working default, GQ-10, S9 row 8". File name `<YYYYMMDD-HHMMSS>-sweep.md` (REPORT:1248). REPORT:554 notes WC-11 (`WORKER-CONTRACT.md:46` at research time) is cited only for the timestamped-name rule. | `--output` default of step 1.6 |
| GQ-11 | "Rule ID: new WC-14 versus amending WC-1 (AMBIGUITY 4)" (GAPS:34; "open (owner decision)", "WC-14 is the working name.") | NOTES:306: "new coordinator-loop rule as WC-14 (next free) or reuse the unused WC-1." REPORT:48: "Rules WC-2 to WC-13 exist and WC-1 is unused, so WC-14 is the next free ID." | WC-14 (REPORT:1549 S9 row 9: "WC-14 is the working default"; SPEC:400 "WC-14 is the next free ID"). Hard gate before 1.17 to 1.19. | steps 1.17 to 1.19 |
| GQ-35 | "#409 version pinning (`495eb96d`, unmerged) (AMBIGUITY 9)" (GAPS:58; "#409 is not on master; the layout is read from `git show 495eb96d`.") | NOTES:311: "copy the layout into this repo or cite commit 495eb96d (unmerged); which sort tie-break to use; what approval label the reused design carries." | Pin `495eb96d` as working default (REPORT:1368, :1570 S9 row 30). DESIGN:594 already copies the layout "from #409 at `495eb96d` because #409 is unmerged". Checked 2026-11-08: `495eb96d` is NOT an ancestor of `origin/master`; it lives only on `origin/docs/409-orca-dashboard-designs`; #409 is an OPEN issue, not a PR (`gh pr view 409` fails, `gh issue view 409` = OPEN). So the pin is still needed. | step 1.5 skeleton |
| GQ-61 | "Default window 6 h versus 72 h (AMBIGUITY 2, F11)" (GAPS:84; "The window should bound activity only, not open Tasks or unread reports (N-41).") | NOTES:304: "6 h (issue) vs 72 h (`sc-crash-recovery/SKILL.md:26`)". | 6 h, bounding activity only; open Tasks, questions and unread reports always listed (REPORT:425, :579, :1592 S9 row 51). DESIGN:59 GQ-103(2): no module holds a window constant "except the CLI default `"6h"`". | `--window` default of 1.6; window rules of 1.5 and 1.12 |
| GQ-63 | "`pragmatic` DONE/NEXT rule has \"No exceptions\" and no exception mechanism (AMBIGUITY 6, F10)" (GAPS:86) | NOTES:308: "whether to add an orchestrator exception to the mandatory DONE / NEXT table". Evidence: `src/superclaude/output-styles/pragmatic.md:22` "EVERY response includes a DONE / NEXT table. No exceptions." and `:53` "CRITICAL: Lead every wrap-up with a plain-language DONE / NEXT summary". `07-gate-gap-fill.md:21`: no exception mechanism exists; adding one means editing `:22`. | NO recommendation exists anywhere. REPORT:580 and :1594 say only "Owner decision". DESIGN has no DONE/NEXT text at all (grep for `DONE / NEXT`, `DONE/NEXT`, `pragmatic` in DESIGN: only :907 and :988). Note for the builder: the sweep report file is written by Python (`report.py`), not by a chat reply, so the output style does not govern the file; the decision only affects the skill's chat reply after the run. A safe default to offer the owner: no exception; the skill's reply carries the DONE / NEXT table and points to the report path. | step 1.5 report format |
| D9 sign-off | DESIGN:907 and :990 item 22: sign-off on the D9 narrowing of SP-29 (DESIGN:815: a worker is a transcript joined to a scoped Dispatch row; an unjoined tab-map entry gives `person_started` None with note `Orca pane session, not in scoped Runs`) | sign off D9, or name a stricter rule | D9 as written (DESIGN:815, :853) | the classify step (DESIGN:990: "the classify step does not start until the owner signs off D9 or names a stricter rule") |

Unclear for the builder: REPORT:1238 says all decisions except GQ-11 "keep the working default and stay in S9" if unanswered, but DESIGN:988 says "Steps 1.17 to 1.19 do not start" for the whole set, and DESIGN:990 makes D9 gate classify (step 1.3). The task file must state which rule wins; DESIGN:902 says "this design wins".

### APPROVED.md: decisions that answer or constrain this work

None of APPROVED's rows answers GQ-10, GQ-11, GQ-35, GQ-61 or GQ-63 (no row names a report location, a WC number, #409, a window or the output style). These rows constrain `/sc:sweep` or the WC rules:

| ID | APPROVED line | Constraint on Phase 1 |
|---|---|---|
| D3 | :10 "`/sc:pr-submit` is never an Orca worker" | The step 1.18 never-as-worker sentence keeps "plus `/sc:pr-submit` while the answer to decision D3 keeps it off workers" (REPORT:1277). |
| D4 | :11 "no worker acts outward; the coordinator performs every push, PR, comment, install and paid run, on `IronbellyOrg/IronClaude` only" | Step 1.29 needs an install of the branch into pipx (see Gap 3); that is an install, so the coordinator does it, never a worker. The sweep never posts its report (WC-14 G7). |
| D5 | :12 "keep nesting depth 1 ... WC-13" | The sweep reports a non-null `parent` as a WC-13 violation for review (GQ-40, GAPS:63; REPORT:1246). |
| GIT | :13 "coordinator owns push, PR, review replies, comments, merges and worktree removal" | The sweep only recommends worktree removal; it never performs it (REPORT:1276 closing sentence; DESIGN:638). |
| L3 | :20 "`.dev/tasks` staging ... is left to the coordinator, which stages `.dev/tasks` at every commit" | The 1.0a, 1.0b, 1.4, 1.16a and 1.29 artifacts under `.dev/tasks/<pkg>/artifacts/` are staged by the coordinator. |
| CR-01, PATHS | :25, :29 "Orca's default paths (never `.dev/worktrees/`), no Orca issue/PR linking" | Worktree discovery uses `worktree ps --json`, never a `.dev/worktrees/` scan; the sweep passes no Orca link flags. |
| UPSTREAM | :30 | Step 1.16a's `gh` call must carry `--repo IronbellyOrg/IronClaude` (DESIGN:925 already does). |
| B1, B1-N1 | :35, :36 "Before a phase's live tests (7.2), the coordinator asks the owner for approval, then installs ... `superclaude install --force`" | Scoped to the orca-command-refactor phases, not to #339. By analogy, any install the 1.29 check needs gets the owner's approval first. |
| S4 | :47 "`/sc:implement` may not prompt the user outside its halt paths" | Applies to `/sc:implement` plans, not to `/task`; but the same issue exists: steps 1.0a, 1.0b and 1.29 need the person, so the task file must put them where its executor is allowed to ask (a pre-phase the coordinator runs, or a blocking item). |
| G1 | :71 "The owner's own instruction ... in the session in any plain wording, is the quoted grant ... No separate grant file is created" | `owner-decisions.md` (1.0b) should record the owner's words as given; do not invent an extra grant file. |
| F1 | :90 WC-4 `artifacts` excludes paths git ignores | `.dev/sweeps/` is gitignored (FR-025). The sweep writes no contract (never-as-worker), so no effect, but a future worker contract must not list a sweep report in `artifacts`. |

P1-C5 (:83, the Skill-call rule for WC-7) and H1 to H3 (:54 to :56, heartbeat reading) apply to workers only; `/sc:sweep` is never a worker, so they do not apply.

## Gap 2. The ten #409 SessionRow dimensions

Source of the list: REPORT:1245 (step 1.2) names them as `str` fields defaulting to `UNKNOWN`, "the ten #409 dimensions of `data-dictionary.md:19-28`". That file exists only at `495eb96d`: `git show 495eb96d:.dev/design/orca-observer-20261106/data-dictionary.md`, lines 19-28 (read 2026-11-08). Meanings below are quoted from that file; the sweep's source per column is REPORT:1248 (step 1.5, "Column sources per `scope-04:336-351`").

| # | Field (REPORT:1245) | Values | Meaning (data-dictionary.md at 495eb96d) | Sweep source and fallback (REPORT:1248) |
|---|---|---|---|---|
| 1 | `lifecycle` | running / settled / unknown | :19 "Settlement does not admit a result." | `projection.outcome` and `stage.detail`; `settled` -> settled, else running (unknown) |
| 2 | `phase` | work / review / queue / dependency | :20 "Phase is not health or percentage complete." | no input (not observed) |
| 3 | `health` | no issue observed / failed result / unknown | :21 "Stale is handled separately." | contract `worker_status: failed` -> failed result; liveness `unverifiable` -> unknown (unknown) |
| 4 | `approval` | none observed / human decision observed | :22 "A dependency wait does not imply approval." | candidate `gate-list` mapping [UNVERIFIED] (not observed). DESIGN:66 GQ-109 removes `gate-list` from the allowlist, so this is always "not observed" in Phase 1. |
| 5 | `freshness` (plus `freshness_age_s: int \| None`) | fresh / stale, with age in seconds | :23 "A stale pass cannot establish current readiness." | `evidence.liveStatus` and `observedAt`; transcript mtime for a person-started session (unknown) |
| 6 | `result` | succeeded / partial / failed / null | :24 "These are report outcomes, not transport events." | contract `worker_status`; `blocked` prints null (not observed) |
| 7 | `admission` | admitted / not admitted | :25 "Defined by an explicit fixture record, never inferred from settlement, packet completeness or passing tests." | none (not observed) |
| 8 | `evidence_packet` | complete packet / partial packet | :26 "Completeness means inspectable, not accepted." Renamed from #409's `evidence` "so it does not clash with the derived `evidence`" (REPORT:1245) | DERIVED: contract `report_path` and every `artifacts` path exist -> complete, else partial (not observed) |
| 9 | `policy` | frozen / not frozen | :27 "Frozen work remains inert; the gallery cannot lift it." | freeze test at `WORKER-CONTRACT.md` (contract + ledger) (not observed) |
| 10 | `tests_review: str \| None` | null = unavailable | :28 "Tests are tied to check_revision and must match current revision to count as current evidence." | none (null (unavailable)) |

### What DESIGN section 7.2 covers

- DESIGN:459 `SessionRow` lists `id`, `person_started`, `orca`, `contract`, `transcript_path`, `transcript_readable`, `last_activity`, `gate_policy`, `row_id`, and then only the words "the ten #409 dimensions". SPEC:235 says the same ("the ten #409 dimensions defaulting to `unknown` (REPORT step 1.2)"). Neither names a single dimension field. So the design covers all ten by reference only; the names, the `freshness_age_s` extra field and the `evidence_packet` rename exist only in REPORT:1245.
- DESIGN:634 puts "the ten #409 dimensions" as the first columns of the Sessions table, again unnamed.
- Conflict to settle in the task file: the design's `policy_of(row) -> str | None # "frozen" or None` (DESIGN:413) and the JSON row key `policy: str|null` (DESIGN:570) overlap with dimension 9 `policy` on `SessionRow`. The task file should say whether dimension 9 is filled from `policy_of` or is a separate field.
- Second difference: REPORT:1249 put the ten dimension fields in each JSON row; DESIGN:567-573 (JSON v1 rows) does not list them, and DESIGN:590 pins the v1 row key set without them. The design wins (DESIGN:902), so the dimensions appear in the Markdown report only, not in the JSON. The task file should state this so no builder adds them to the JSON.

### `ClassifiedRow`

Not defined anywhere. A repo-wide search for `ClassifiedRow` finds only DESIGN:466 (`SweepResult.rows: tuple[ClassifiedRow, ...]` "(row plus `Classification`, policy and `SafeToClose`)") and the task's own research and QA files (`research/01-file-inventory.md:44`, `qa/qa-research-depth-report.md:92` finding M-1). No SPEC or REPORT entry. Proposed fields, derived only from the DESIGN:466 wording and the JSON row keys at DESIGN:568-572: `row: SessionRow`, `classification: Classification`, `policy: str | None` (from `policy_of`), `safe: SafeToClose`. The task item must name these as a builder decision, not as a design fact.

## Gap 3. Step procedures the research skipped

### 1.0a, the live read-only capture

What the design says (DESIGN:866-896):

- Who and what Run: "a manual, pre-implementation capture run by the person or the coordinator, never by a test" (:868). "It runs against an existing Run that the person names. It creates no Run, Task or Dispatch; the REPORT's throwaway Run is dropped." (:872). Gate: "An existing Run named by the person" (:906).
- Exact commands: "only the eight `ALLOWED_ORCA` templates of section 7.3, with the binary `orca-ide` or `$ORCA_CLI_COMMAND`" (:873). The eight templates (DESIGN:521-530), with the binary prefixed:
  1. `orca-ide orchestration run-current`
  2. `orca-ide orchestration worker-list --run <run> --json`
  3. `orca-ide orchestration worker-show --dispatch <dispatch> --json`
  4. `orca-ide orchestration task-list --ready --run <run> --json`
  5. `orca-ide orchestration task-list --run <run> --json`
  6. `orca-ide worktree ps --json`
  7. `orca-ide worktree list --json`
  8. `orca-ide worktree current --json`
  Forbidden in the capture (:873): `worker-read` in any form, `gate-list`, `check`, `inbox`, `--include-remote`, `--agent-wait`, any `git stash`. `run-current --json` is not run (:874).
- Order: `worker-show` and `task-list` once before and once after all other reads; outputs must match apart from timestamps; "A difference stops the build and goes to the owner." (:875).
- Non-Orca reads in the item list: item 12 reads `/opt/Orca/resources/app.asar.unpacked/out/package.json` (:893); item 13 reads the `orca-tabs/` files only (:894); item 8 is template 2 with an unknown id (:889); item 9 is recorded only if Orca is already down, "never induced" (:890).
- Where outputs go: `.dev/tasks/<pkg>/artifacts/readonly-probe.md` (:876); sanitized samples become fixtures under `tests/sweep/fixtures/` "with their source named" (:876, and DESIGN:733: hand-made fixtures carry `synthetic` in the name until 1.0a replaces them).
- Host facts checked 2026-11-08: `orca-ide` is on PATH at `/home/coder/.local/bin/orca-ide`; `ORCA_CLI_COMMAND` is unset.

What is unclear:

- `<pkg>` is not named. For this task it should be `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/readonly-probe.md`.
- How the person supplies the Run: the design says only "named by the person". The task item should ask for one Run id with at least one Dispatch (better one live and one settled worker, so items 4 and 13 can be captured), and should note that template 1 (`run-current`) shows the bound Run if the person has none in mind. Which Dispatch ids to `worker-show` is also not said: the natural reading is every Dispatch id from the item 3 `worker-list` output.
- What unknown Run id to use for item 8 is not said (any well-formed id that `run-list` would not return; but `run-list` is not allowed, so pick an obviously fake id of the same shape as the item 10 samples).
- "Sanitized" is not defined for the fixtures (which fields to scrub: paths, session ids, user names). The task item should define it.
- Interaction with step 1.4: the 1.4 live check needs a Run too; the design does not say it is the same Run. Using the same Run is the simplest reading.

### 1.4, the "Live" note

DESIGN:912: "Live check saved to `.dev/tasks/<pkg>/artifacts/sweep-live-check-1.4.json`; no `--include-remote` timing". The design gives no pass rule. The only pass rule is REPORT:1247 (step 1.4 "Acceptance, live check"): record each worker's state from `orca-ide orchestration worker-list --run <id> --json`, then run `superclaude sweep run --run <id>` once through Bash with timeout 120000 ms; "Pass = exit 0, the probe calls finish inside the 90 s budget, every row carries a class, each recorded worker gets the class its recorded state maps to under step 1.3 (could not determine where step 1.3 says so), and no row is could not determine because of a probe error or timeout." The REPORT's second part, timing `worker-list --include-remote` into `artifacts/include-remote-cost.txt`, is dropped by the design ("no `--include-remote` timing"), because `--include-remote` is a forbidden token (DESIGN:532). The 90 s figure still holds in the design (`Budget` "50 shows, 90 s", DESIGN:221).

Unclear: (a) the run uses the dev checkout, so the command form is `uv run superclaude sweep run --run <id>` (the pipx `superclaude` on PATH is a master install from `git+https://github.com/IronbellyOrg/IronClaude` and has no `sweep` until reinstalled; see 1.29); (b) the run writes one real report under `<root>/.dev/sweeps/`, which is gitignored and allowed, but the task item should say so; (c) whether the pass rule is the REPORT's (design silent). Recommendation: take the REPORT pass rule minus the include-remote timing.

### 1.16a, the PR #422 check

DESIGN:925: "`gh pr view 422 --repo IronbellyOrg/IronClaude --json state,files` and the #409 diff check; results to `.dev/tasks/<pkg>/artifacts/`"; "must finish before 1.17". REPORT:1275 gives the branches: if #422 is open, wait or move 1.17 to 1.19 to a follow-up PR; "if it is merged, rebase onto `origin/master` first"; if #409 has merged, diff its layout files against `495eb96d`.

Checked 2026-11-08: `gh pr view 422 --repo IronbellyOrg/IronClaude --json state,mergedAt,mergeCommit` returns `"state":"MERGED"`, `"mergedAt":"2026-11-07T14:15:58Z"`, merge commit `2327fbd3...`, which is on `origin/master` ("feat(orca): convert the 15 P2 commands to --unattended with report directories (#422)"). That commit changes `src/superclaude/core/WORKER-CONTRACT.md` (17 lines) and `tests/skills/test_worker_contract.py` (765 lines). The branch is at `5dc29d23` = `origin/master`, so the rebase is already done. #409 is still unmerged (`495eb96d` is not an ancestor of `origin/master`).

What the step should become: a record-only step. Write `artifacts/pr422-409-check.md` with (1) the `gh pr view 422` state line (MERGED, merge commit `2327fbd3`), (2) `git merge-base --is-ancestor 2327fbd3 HEAD` succeeding, (3) `git merge-base --is-ancestor 495eb96d origin/master` failing, so the `495eb96d` pin stands and no layout diff is needed, and (4) a note that every WORKER-CONTRACT.md and test_worker_contract.py line cited by 1.17 to 1.19 must be re-read at HEAD (the re-anchoring is being done by other agents). The "wait or split the PR" branch no longer applies. The step's gate on 1.17 stays, but it is satisfied as soon as the record is written.

### 1.28, the primitive-path grep

DESIGN:939: "`grep -rn 'src/superclaude' src/superclaude/{commands,skills,agents,core,hooks}`, every hit justified". REPORT:1299 scopes it to the new files: "justify or remove every new hit".

Checked 2026-11-08 at `5dc29d23`: the full command returns **168** hits (commands 18, skills 132, agents 9, core 0, hooks 9). Justifying all 168 is out of scope for Phase 1. The new files do not exist yet (`src/superclaude/commands/sweep.md`, `src/superclaude/skills/sc-sweep-protocol/`).

How to scope it to Phase 1's files: run
`grep -rn 'src/superclaude' src/superclaude/commands/sweep.md src/superclaude/skills/sc-sweep-protocol/ src/superclaude/core/WORKER-CONTRACT.md src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`
Pass = no output (grep exit 1). The two core files and the plugin copy are included because Phase 1 edits them and the CLAUDE.md rule covers `core` and the `plugins/superclaude/` mirror; all three have 0 hits today. As a second check, record the full-tree count before and after (168 today); pass = the count is unchanged. A changed count means a Phase 1 edit added a hit somewhere else.

### 1.29, the manual pipx check

DESIGN:940: "`superclaude sweep --help` under a pipx install; output saved to `.dev/tasks/<pkg>/artifacts/sweep-help-pipx.txt`". REPORT:1300: run once "from a directory that is not a uv project, time limit 30 s"; "Pass = exit 0 and the help text lists the `run` subcommand; save the output and exit code".

Checked 2026-11-08: `superclaude` on PATH resolves to `/home/coder/.local/share/pipx/venvs/superclaude/bin/superclaude`; `pipx list --short` shows `superclaude 5.0.0`; its `pipx_metadata.json` has `"package_or_url": "git+https://github.com/IronbellyOrg/IronClaude"` (a master install, not editable). So the installed copy has no `sweep` until the branch code is installed into a pipx environment.

What is unclear and how to run it:

- The design does not say how the branch code reaches pipx. Option A (no change to the installed tool): from a non-uv directory such as `/tmp`, run `pipx run --spec <worktree path> superclaude sweep --help` (`pipx run --help` documents `--spec SPEC` as "The package name or specific installation source to install the app from"). It builds a temporary environment and leaves the installed `superclaude` alone. This command was read from help text only and not run; that a local path works as `--spec` is UNVERIFIED. Option B: `pipx install --force <worktree path>` (`--force` is in `pipx install --help`), then reinstall from master afterwards. Option B changes the person's installed tool, which is an install under D4 (APPROVED:11), so it needs the owner's approval and is done by the coordinator. Recommend option A, with option B only if the owner wants the real PATH form tested.
- Who runs it: it is "Manual" (DESIGN:940), so the person or the coordinator, never a test.
- The REPORT's 30 s limit and pass rule should be copied into the task item, since the design gives neither.

## Gap 4. R3-B1 to R3-B3 fixtures for DESIGN sections 11 and 12

Source: `research/04-design-fixes-r3.md` (232 lines). Checked 2026-11-08: none of the fixes is in DESIGN yet (grep for `first_record_ts`, `dispatch_started`, `origin unknown`, `conflict: one pane` finds nothing; "the four incomplete cases" is still in the `test_classify.py` row at DESIGN:739). The QA gates the fixtures must satisfy are at 04:221-224.

### Section 11 (test plan), by file

`tests/sweep/test_probes_allowlist.py` row (DESIGN:738), R3-B1 reader and parser cases (04:99-108), 6 fixtures:

1. `test_read_transcript_tail_sets_first_and_last_record_ts`
2. `test_read_transcript_tail_first_record_ts_is_minimum`
3. `test_read_transcript_tail_first_record_ts_over_256k`
4. `test_worker_show_dispatch_times_sqlite_form`
5. `test_worker_show_dispatch_times_iso_z_form`
6. `test_worker_show_dispatch_times_missing_or_bad`

`tests/sweep/test_classify.py` row (DESIGN:739), 15 fixtures:

- R3-B1 path-B window (04:110-117), 4: `test_path_b_window_open_row_joins`, `test_path_b_window_inclusive_bounds`, `test_path_b_terminal_row_without_end_has_no_window`, `test_path_b_row_without_start_has_no_window`.
- R3-B2 several rows on one pane (04:154-164), 7: `test_path_b_pane_reused_joins_later_row_only`, `test_path_b_two_windows_hold_session_is_conflict`, `test_path_b_shared_boundary_second_is_conflict`, `test_path_b_no_matching_window_holds`, `test_path_b_multi_row_result_ignores_row_order`, `test_path_b_entry_failing_window_note_order`, `test_path_b_rows_share_terminal_handle`. Placement (04:149): after "a row with no observable start time never joins by path B;".
- R3-B3 SPEC incomplete cases (04:191-200), 4: `test_fr010_outage_older_transcript_unknown_not_historical`, `test_fr010_full_page_uncaptured_continuation`, `test_fr010_call_failed_incomplete_list`, `test_fr010_incomplete_notes_order`. Text edit (04:186): replace "the four incomplete cases" with "the three SPEC incomplete cases (an older transcript during an Orca outage, an older unjoined transcript after a full page with uncaptured continuation, an incomplete list after `call_failed`; each stays visible with `person_started` None and its `origin unknown:` note, never idle or Historical)", keeping the four guard-case fixtures listed later in the same cell. Keep the existing FR-010 complete-negative-join control beside them (04:202).

Total: 21 new fixtures (6 + 15).

### Section 12 (traceability)

- FR-010 row (DESIGN:764), R3-B2 edit (04:150): after "with a path-B join also needing the Dispatch row's time window" add ", and one rule for several rows matching one pane session (join only the one row whose window holds it; `conflict:` when two or more do)".
- FR-010 row, R3-B3 edit (04:188): design column, after "completeness guard" add "with its three list-incomplete cases (outage, full page, `call_failed`) and"; test column, add "the three SPEC incomplete-case fixtures" to the `sweep/test_classify.py` parenthesis.
- R3-B1: 04 gives NO section 12 edit (its nine edits, 04:87-95, touch 7.1, 7.2, 2.2, 15.1, 17 and 18 only), and its gate (04:221) does not grep section 12. Recommendation, not from 04: add `sweep/test_probes_allowlist.py` (the six reader and parser fixtures) to the FR-010 row's test column, and FR-010 to that file's Covers cell in section 11, so the six R3-B1 parser fixtures trace to a requirement.
- D9 (DESIGN:815) and SP-29 (DESIGN:853) are sections 13 and 14, not 12, but the R3-B2 gate (04:222: "D9, SP-29 and FR-010 rows agree") needs the 04:151 edit there too: add "and, when several rows match one pane session, exactly one window holding it".

### What each gate checks (04:221-224), and which fixture satisfies it

- R3-B1 gate: the four new field names appear in 7.1, 7.2, 2.2, 11, 15.1, 17 and 18. In section 11 only the fixtures carry them, so at least one fixture text in the rows must name `first_record_ts` and the `dispatch_*` fields (fixtures 1 to 6 and the four path-B window fixtures do).
- R3-B2 gate: "each outcome has a fixture in section 11": one window holds (`..._pane_reused_joins_later_row_only`), two or more hold (`..._two_windows_hold_session_is_conflict`, `..._shared_boundary_second_is_conflict`), none holds (`..._no_matching_window_holds`).
- R3-B3 gate: "outage" and "uncaptured continuation" in section 11 (the replacement text and fixture names carry them); the three `origin unknown:` notes in 7.2 and section 11 (the fixture rows must quote the three literals, not only the names); "four incomplete cases" absent from section 11.
- All three: em-dash count 0, no `TODO` or `TBD`, deviation total still 9, open-item total still 23.

## Gap 5. Gate sizing for `QA_INTENSITY: full`

Source: `~/.claude/templates/workflow/02_mdtm_template_complex_task.md` (1519 lines). I22:808 says full intensity is "Per I19 tables (5+ intermediate, 6-12+ final) | Per I19 tables + all domain lenses | Per I21 (2-8 agents) | Per I16 (2 per gate) | 2" (verification agents), and I22:839 "All current I19, I20, I21 rules apply without modification."

| Item | Exact count at full | Source |
|---|---|---|
| Final-document gate (M3) | By output size, BEFORE domain lenses: <500 lines 3 rf-qa + 3 rf-qa-qualitative = 6; 500-1500 lines 4 + 4 = 8; 1500-3000 lines 5 + 5 = 10; >3000 lines 6 + 6 = 12. Plus "all domain lenses" on top (I22:808; I19:717). | I19:710-715 |
| Code-modifying task gate | "M3 lens-based (minimum 6 agents per I19)" | :1056 |
| Intermediate gate | 5 per gate: research gate 2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative; synthesis gate 2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative; task-integrity 2 rf-qa + 2 rf-qa-qualitative + 1 rf-analyst | I19:737-741; :1057 |
| Intermediate partitioning | Counts are "per-lens-per-partition"; "if research files >6, each agent type gets partitioned (e.g., 10 research files -> 4 rf-analyst + 4 rf-qa + 2 rf-qa-qualitative = 10 agents at research gate)" | I19:743-745 |
| Fidelity gate (M4) | Minimum 2; "If source docs exceed 1000 lines total, partition across 3-4 agents"; I22 range 2-8 | I21:788; I22:808 |
| Fix agent | ONE rf-qa with `fix_authorization: true` per fix cycle, only when blocking findings exist | I20:755 |
| Verification round | Minimum 2 (1 rf-qa + 1 rf-qa-qualitative) per round | I20:756; I22:808 |
| Fix cycles | 2 per gate (3 reviews), then HALT and escalate with the open blocking findings; every gate type in the I16 table is 2 | I16:657, :664-671; I20:757 |

Applied to this task, as worked numbers the builder can use:

- DESIGN is 1013 lines, so a gate whose target is the design (the R3-B1 to R3-B3 design-fix gates) is the 500-1500 row: 8 agents (4 + 4) plus domain lenses, then 1 fix agent and 2 verifiers per cycle, at most 2 cycles.
- Fidelity sources: DESIGN 1013 lines plus SPEC 653 lines is over 1000 lines, so 3 to 4 fidelity agents, not 2.
- Research gate: this task has 9 files under `research/` (01 to 09), which is over 6, so partitioning applies. The template's only worked example is 10 files -> 10 agents; it gives no exact formula for 9. Recommendation: use the 10-agent split (4 rf-analyst + 4 rf-qa + 2 rf-qa-qualitative).

## Gap 6. POST reflect diff scope

Findings in `~/.claude/skills/sc-reflect-protocol/`:

- `SKILL.md:80`: "`--diff <ref-or-path>` [dash] git ref (e.g., `HEAD~1..HEAD`, branch name) or path to a diff file (required for UC-2)". So both a single ref and a diff file path are accepted.
- `refs/remediation-handoff.md:104`: "A single ref (not `A..B`) diffs against the working tree, so `--diff <baseline_ref>` captures uncommitted `/sc:implement` edits to tracked files; `git diff` omits untracked files, so `--task-log` (the package's sibling `progress.md` ledger) lets reflect see files the run created." The skill's own post gate uses this form (`SKILL.md:344`: `--diff <baseline_ref> --task-log <resolved-pkg>/progress.md`).
- `SKILL.md:249-250` (the `--isolate-reviewers` snapshot) STOPs on a dirty tree, but that gate belongs to the `superclaude reflect run --isolate-reviewers` wrapper, is off by default and "is not a `/sc:reflect` flag" (`SKILL.md:256`). It does not affect `/sc:reflect`.
- `SKILL.md:204`: the `--diff` file must not lie inside the reflect output root (STOP `output_input_overlap`).

So `--diff {BASE}..HEAD` audits committed work only and would show nothing for an uncommitted Phase 1. The single-ref form `--diff {BASE}` covers uncommitted edits to tracked files, but Phase 1 is mostly NEW files (the `src/superclaude/cli/sweep/` package, `tests/sweep/`, `commands/sweep.md`, the `sc-sweep-protocol` skill), and `git diff` leaves untracked files out.

Recommendation, to audit all uncommitted Phase 1 work with no commit:

1. Record `BASE` at task start with `git rev-parse HEAD` (today `5dc29d23`).
2. Before the POST reflect item, write one diff file into the task package, outside the reflect output root: `git diff --binary {BASE} -- . ':(exclude).dev'` for edited tracked files, then, for each path from `git ls-files --others --exclude-standard -- src tests docs plugins`, append `git diff --no-index -- /dev/null <path>` (exit 1 means "files differ", which is the expected result). Save as `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/phase1-working-tree.diff`. These are read-only git calls; the only write is the diff file in the task package. The `.dev` exclusion keeps the task's own staged artifacts out of the diff.
3. Run `/sc:reflect --mode post --spec docs/designs/orchestrator-mode.md --tasklist <task file> --diff .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/phase1-working-tree.diff --task-log <task file>`.

Simpler fallback, the skill's own documented form: `--diff {BASE} --task-log <task file>`. It needs no extra file, but the reviewers then see the new files only through the task log, not as diff content. For a phase that is mostly new files, the diff-file form gives fuller coverage, so it is the recommended one. Neither form needs a commit, `git add -N` or any index change.

---

## Summary

- Gap 1: all five owner decisions are still open; none is answered by APPROVED.md. Working defaults: GQ-10 `<root>/.dev/sweeps/` (already in DESIGN and SPEC), GQ-11 WC-14 (hard gate), GQ-35 pin `495eb96d` (still needed: #409 is an open issue and `495eb96d` is not on master), GQ-61 6 h for activity only. GQ-63 has no recommendation anywhere; a safe offer is "no exception", because the report file is written by Python and the output style governs only the skill's chat reply. D9 sign-off also sits at 1.0b and gates the classify step. APPROVED rows D3, D4, D5, GIT, L3, CR-01/PATHS, UPSTREAM, S4, G1 and F1 constrain the work.
- Gap 2: the ten dimensions are lifecycle, phase, health, approval, freshness (plus `freshness_age_s`), result, admission, evidence_packet, policy and tests_review (REPORT:1245; meanings from `data-dictionary.md:19-28` at `495eb96d`). DESIGN 7.2 names none of them, only "the ten #409 dimensions"; the dimension fields are not in the JSON v1 row keys; `policy` overlaps `policy_of`. `ClassifiedRow` is defined nowhere; proposed fields `row`, `classification`, `policy`, `safe`, as a builder decision.
- Gap 3: 1.0a uses the eight `ALLOWED_ORCA` templates against a Run the person names, output to `artifacts/readonly-probe.md`; `<pkg>`, Dispatch choice, the unknown-id sample and "sanitized" are unclear. 1.4 has no design pass rule; use REPORT:1247's rule without the include-remote timing. #422 is MERGED (`2327fbd3`, on master; it changed WORKER-CONTRACT.md and test_worker_contract.py), so 1.16a becomes a record-only check. 1.28's full grep gives 168 hits today; scope it to the new and edited primitive files (0 hits expected) plus an unchanged full-tree count. 1.29: pipx `superclaude` is a master install with no `sweep`; recommend `pipx run --spec <worktree>` from `/tmp` (UNVERIFIED, help text only), with a `pipx install --force` only on owner approval under D4.
- Gap 4: 21 new fixtures in section 11 (6 in `test_probes_allowlist.py` for R3-B1; in `test_classify.py` 4 for R3-B1, 7 for R3-B2 and 4 for R3-B3), plus replacing "the four incomplete cases". Section 12 gets the R3-B2 and R3-B3 FR-010 edits; R3-B1 has no section 12 edit in 04 (adding the parser file to the FR-010 test column is recommended). D9 and SP-29 also need the R3-B2 edit for its gate.
- Gap 5: full intensity is final gate 6/8/10/12 by size (8 for the 1013-line design) plus domain lenses, at least 6 for a code gate, 5 per intermediate gate (partitioned when over 6 research files, 10 at 10 files), fidelity 2 minimum and 3 to 4 when sources pass 1000 lines, 1 fix agent and 2 verifiers per cycle, 2 fix cycles per gate.
- Gap 6: `sc-reflect-protocol` accepts a single ref (diffs against the working tree, tracked files only) or a diff file path. Recommend a diff file built from `git diff --binary {BASE}` plus `git diff --no-index /dev/null <new file>` for untracked files, passed as `--diff <path>` with `--task-log`; no commit needed.

