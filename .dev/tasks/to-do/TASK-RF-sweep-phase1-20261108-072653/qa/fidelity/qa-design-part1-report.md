# QA Report: DESIGN part 1 fidelity lens (sections 1 to 8)

**Gate folder:** .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/qa/fidelity/
**Date:** 2026-11-12
**fix_authorization:** false
**Status:** matrix and findings complete; checks and verdict below

Paths are relative to the repository root. `D:<n>` is `docs/designs/orchestrator-mode.md` line n as it stands today (revised). `C` = `src/superclaude/cli/sweep/commands.py`, `P` = `probes.py`, `K` = `classify.py`, `R` = `report.py`, `M` = `models.py` (same folder). `SK` = `src/superclaude/skills/sc-sweep-protocol/SKILL.md`, `CM` = `src/superclaude/commands/sweep.md`, `ST` = `src/superclaude/output-styles/pragmatic.md`, `TC` = `tests/commands/test_sweep_command.py`, `WC` = `src/superclaude/core/WORKER-CONTRACT.md`, `TW` = `tests/skills/test_worker_contract.py`. Evidence run by this reviewer: `uv run pytest tests/sweep tests/commands tests/core tests/skills tests/recommend -q` gave 3245 passed; `uv run ruff check .` gave "All checks passed!"; an end-to-end `superclaude sweep run` in a private /tmp repository (missing Orca binary, private HOME) gave the exit codes and messages listed under C8 and C16 (the repository was not touched; the temp folder was deleted).

Decision records read and applied as authority: `phase-outputs/plans/FINAL-GATE-halt-resolution-decision.md` (D:491 and D:760 edited by the owner; Rule 5 inert), `FINAL-GATE-cycle2-scope-decision.md` (D:614-615 header banner), `FINAL-GATE-FIN-F7-ruling.md` (FIN-F7 is a documented limitation), plus OQ-1 (`--agent-wait` allowed), OQ-2 (`.dev/sweeps/`), OQ-3 and its 2026-11-12 addendum ("wake or wait timeout"), OQ-4, OQ-5 (6h), OQ-6 (b), OQ-7 (D9 as written), OQ-17 (no cursor template).

## Requirement-to-delivery matrix

### Section 1 (status, scope, facts)

| Requirement (D:line) | Delivered at | Result |
|---|---|---|
| One read-only command `superclaude sweep run`, a thin `/sc:sweep` command and `sc-sweep-protocol` skill, the WC-16 text, routing and doc rows (D:11) | `C:214-288`, `CM:1-70`, `SK:1-66`, `WC:277`, `src/superclaude/core/HOW-WE-WORK.md:334,405`, `docs/user-guide/commands.md:116`, `CHANGELOG.md:7-16` | Delivered |
| Only filesystem change is one dated report under `<root>/.dev/sweeps/` (plus the folder when new); dot-prefixed temp only during publication (D:13) | `C:153-208`; no other writer: grep of the package for `.write(`, `write_text`, `mkdir`, `shutil`, `rename` hits only `C:140,149,203`; end-to-end run left exactly one `*-sweep.md` | Delivered |
| `main.py` registers the deferred subcommand after `issue-watch` (D:28) | `src/superclaude/cli/main.py:567-569` | Delivered |
| ccsession tab map: one file per pane, `:` written as `+`, 3 lines, dot-files ignored (D:32) | `P:820-845` (skips names starting with `.`, needs 3 non-empty lines) | Delivered |
| Transcript record keys `timestamp` and `sessionId` (D:33) | `P:736-766` | Delivered |
| Out of scope: write verb, `/sc:close`, `gh`, scheduler, retention, remote hosts (D:35) | Grep of the package: no `gh`, no `stash`, no verb string from the forbidden list; `P:1265` records `remote hosts unknown` | Delivered |
| Review items R3-B1, R3-B2, R3-B3 closed (D:7-11) | time fields `M:72-74,115-117`; several-rows rule `K:597-640`; the three SPEC FR-010 incomplete cases `K:678-708` | Delivered |

### Section 2 (GQ resolutions)

| Requirement (D:line) | Delivered at | Result |
|---|---|---|
| 2.1 `_git` is the only git starter; argv `["git","--no-optional-locks","-C",cwd,*args]`; env `GIT_OPTIONAL_LOCKS=0`; args must equal the one `ALLOWED_GIT` template else `ValueError` before any process (D:41-47) | `P:298-322` (argv `:305`, env `:306`, check `:304`, `:227-230`) | Delivered |
| GQ-101 shared package = active in 2+ worktrees by one `git status` path prefix `.dev/tasks/{to-do,done}/<id>/`; one Retained problems line naming every worktree (D:57) | `P:910-914`, `K:420-440`, `R:368-372` | Delivered |
| GQ-102 `conflict` first (D:58) | `M:43-50`, `K:396-417` | Delivered |
| GQ-103(2) window is data; no window constant but CLI default `6h` (D:59) | `M:55-61`, `C:27,267`; OQ-5 | Delivered |
| GQ-103(3) model carries every rule field (D:60) | `M:64-91,95-127` | Delivered |
| GQ-104 no `run-list`; no binding exits 2 `no Run bound: pass --run <id>`; unavailable first call exits 2 with `Orca unavailable (<reason>); ...` (D:61) | `P:361-371`, `P:49-60` (no `run-list`), `C:279-281` | Delivered |
| GQ-105 `archive-blocked` = `FINAL:` line after optional whitespace; ledger over 1 MiB split read (D:62) | `P:557-569`, `K:399` | Delivered (see M5) |
| GQ-106 `.dev/sweeps/` in `.gitignore` (D:63) | `.gitignore:255-256` | Delivered |
| GQ-107 `sanitize()` escapes `|` (D:64) | `R:569-599` (`:593`) | Delivered |
| GQ-108 two join paths; both Orca-side fields were UNVERIFIED until 1.0a (D:65) | `K:38-40` `JOIN_PATH = "B"` closed by `phase-outputs/discovery/1.0a-facts.md` rows 1 and 22; `P:438` `session_join = dispatch.assigneeHandle` | Delivered |
| GQ-109 `gate-list`, `worker-read`, `git stash` absent; only `--include-remote` forbidden; `--agent-wait` allowed (D:66) | `P:49-62` | Delivered |
| GQ-110 exactly one `git status` per worktree (D:67) | `P:917-941`, `P:1246-1249` | Delivered |
| M7 `unpushed` bool or None; `no upstream` still makes `removable: no` (D:71-72) | `P:492-509`, `P:885-892`, `K:449-450` | Delivered |
| 2.3 GQ-111 to GQ-113 carried, REPORT not edited (D:76-80) | `git status` shows the REPORT file staged `A ` with no later modification | Delivered |

### Section 3 (publication, G-1 with SP-20)

| Requirement (D:line) | Delivered at | Result |
|---|---|---|
| Single write path is private `commands._publish(text, output_dir, now) -> Path`; `report.py` has no `write_report` (D:88) | `C:153`; `R` has no writer (imports `re`, `unicodedata`, `.models` only, `R:11-21`) | Delivered |
| Seven steps: stem, makedirs plus re-resolve and escape check, `O_EXCL` temp `0o666`, full write plus `fsync` plus close, `os.link` to `stem.md` then `stem-2.md` to `stem-99.md`, exhaustion exit 1, unlink after commit (D:103-111) | `C:155-208` (stem `:155`, makedirs `:158`, escape check `:161-164`, temp `:168-170`, write `:177-179`, link loop `:182-196`, exhaustion `:197-201`, unlink `:202-207`) | Delivered (see M10) |
| Error table: makedirs, temp exists, write/fsync/close, link non-EEXIST, unlink failure on exit-1 path (second stderr line), unlink failure after commit (no JSON, exit 1), print failure after commit (exit 1) (D:121-129) | `C:159-160`, `:171-172`, `:180-181`, `:191-194`, `:137-143`, `:202-207`, `:275-278`, `:276,286-288` | Delivered |
| Crash table and never-reused rule (D:133-147) | temp name has pid and second; `O_EXCL`; `collect` never reads `.dev/sweeps/` (`P:1206-1280` reads none) | Delivered |
| 3.4 exit-1 rule: no file at a report name before the commit point; exit 2 writes nothing (D:151-153) | publish is called after every exit-2 check and after `render` (`C:246-275`); end-to-end exit-2 runs left no new file | Delivered |

### Sections 4 to 6 (boundaries, sequence, counts)

| Requirement (D:line) | Delivered at | Result |
|---|---|---|
| Module boundaries B1 to B5: `classify` and `report` import only `models` plus the standard library, no `os`, `subprocess`, `click`, `shutil`; `probes` imports `models` and no `classify`/`report`/`click`; `commands` imports all (D:206-219) | imports at `K:10-36`, `R:11-21`, `M:10-15`, `C:13-25`, `P:12-39` | Delivered (see M8) |
| `__init__` lazy `__getattr__` for `sweep_group` (D:208, NFR-006) | `src/superclaude/cli/sweep/__init__.py:4-9` | Delivered |
| Sequence: validate then now then bind then collect then classify then render then publish then JSON; every exit-2 check before any Orca call or write (D:229-280) | `C:246-278`; end-to-end: exit 2 for `--output /tmp/x`, `--window 721h`, `--run 'r;x'`, and for no binding with the binary missing | Delivered |
| Explicit `--run` or established binding plus later unavailable: continue, publish, exit 0; budget-cut timeout is `call_failed` (D:286-287) | `P:333-358` (`:349-354`), `P:1002-1078`; end-to-end run 1 exit 0 with `orca_available: false` | Delivered |
| Counts: Orca argv at most `1+3R+1+50`, `worker-show` `min(D,50)` shared across Runs, git argv exactly W, `N = D+U`, `total = visible+historical` (D:335-349) | `P:131-155` (share with `wanted`), `P:1002-1078`, `P:1244-1249`, `K:957-967` | Delivered |
| `total_is_lower_bound` true when any list truncated or unscanned (D:346) | `K:969-972` sets it always True | Delivered with a stated shortcut (M1) |

### Section 7.1 to 7.4 (signatures, model, constants, JSON)

| Requirement (D:line) | Delivered at | Result |
|---|---|---|
| Signatures of `Budget`, `OrcaResult`, `BindingError`, `orca_binary`, `check_orca_argv`, `check_git_args`, `_orca`, `_git`, `GitCallFailed`, `bind_run`, `parse_time`, `parse_worker_show`, `collect`, readers (D:366-401) | `P:110-194,98-104,90,200,212,227,252,298,86,361,377,422,1206,944,468,589,731,815,848,853` (`share_shows` has one extra optional `wanted` argument, `P:131-133`) | Delivered |
| `classify` signatures and `Rule`, `RULES` (9), `policy_of`, `package_state`, `mark_shared_packages`, `safe_to_close`, `removable`, `classify_all` (D:408-420) | `K:155-158,333-343,357,377,411,420,467,443,863` | Delivered |
| `report` signatures: `CHECKED_ORCA_VERSION="1.4.245"`, `CELL_MAX=200`, `SECTIONS`, `sanitize`, `cell`, `render`, `to_json` (D:426-432) | `R:23-24,545-558,569,602,608,613` | Delivered |
| `commands` signatures and exit mapping (D:438-447) | `C:214-288`; mapping `C:279-288` | Delivered |
| Data model: every type and field of the table, all aware-UTC times, constants `CLASSES`, `PACKAGE_STATES`, `SAFE_VALUES`, `JSON_SCHEMA_VERSION=1` (D:453-472) | `M:17-257` (`SessionRow` carries nine dimension fields; the tenth, policy, is printed from `ClassifiedRow.policy`, `M:141-142`, `R:400`) | Delivered |
| Time parsing: SQLite form read as UTC, ISO with `Z` or offset, unparseable gives None, never raises (D:470) | `P:377-401` | Delivered |
| Rule table order and names (D:476-486) | `K:333-343` | Delivered |
| Rule 1 notes (D:490) | `K:161-188` (`NOTE_ASK_COORDINATOR`, `NOTE_ORCA_NOT_OBSERVED` at `K:79-80`) | Delivered |
| Rule 5 as revised: four conditions kept as the text to restore; inert, returns None, rows fall to the fallback; names not yet captured (D:491, owner edit) | `K:251-257` (`return None`, the four conditions in the comment); `P:432-434` | Delivered; authorized by `FINAL-GATE-halt-resolution-decision.md` |
| Age rule: future timestamp is unknown age, note `timestamp in the future`, never idle (D:492) | `K:232-233,283-299,369-370` | Delivered |
| Joins: row ids, path A and B, whole-second window with both ends included, open window to `collected_start` only for `pending`/`dispatched`, tail-only, several rows, duplicate merge first, join outcome replaces rules 1 to 8 with rule `fallback` keeping evidence (D:496-498) | `K:500-546,597-671,346-354,891-896,943-944` | Delivered |
| No-entry transcripts and the five list-incomplete cases and four guard cases, with their notes and order (D:499-503) | `K:678-762` (origin notes in order `:683-707`; guard `:724-740`; `_person_origin` `:743-762`); `R:327-350` prints the SP-16 line | Delivered |
| Observation rules: WC-13 note plus Retained problems, show wins, unknown schema, duplicate Dispatch, input changed (`_stable`), path escapes, worktree removed, unreadable transcript/contract, rule 6 wording, `FINAL:` start of line, remote hosts (D:507-517) | `K:367-368`, `R:373-375`; `P:422-465`; `P:1091-1146`, `K:500-533`; `P:540-554`; `P:522-532,1298`; `P:917-954`; `P:736-812`; grep shows no `admitted`/`accepted` in the package; `P:557-569`; `P:1265`, `R:194-196,532` | Delivered |
| 7.3 constants: `ORCA_BINARY_DEFAULT`, ten `ALLOWED_ORCA` templates, `FORBIDDEN_TOKENS={"--include-remote"}`, one `ALLOWED_GIT`, `ORCA_VERSION_FILE`, byte limits, `WORKER_LIST_PAGE=100`; token-for-token matching; no cursor template (D:523-559) | `P:43-75,205-224` | Delivered (OQ-1, OQ-17) |
| 7.3 forbidden verb list lives only in the test, so the package holds no write verb as a string (D:553) | grep of the package for every verb in the list as a quoted string: only `dispatch` as a JSON key inside `parse_worker_show` (`P:431-443`) | Delivered |
| 7.4 JSON v1: every key always present, `collected`, `waiting_kind`, `policy`, `person_started`, `summary.counts` with zeros, `class`, values sanitized never cut, `unpushed` bool or null, `safe_to_close.worktree` never `yes` (D:565-599) | `R:613-695`; end-to-end run 1 printed the full key set | Delivered |
| Per-Run source rows `orca worker-list <run>` and `orca task-list <run>`; `unscanned` reasons; `truncated` on a full page (D:597) | `P:1031-1078` | Delivered |

### Section 7.5 (report layout)

| Requirement (D:line) | Delivered at | Result |
|---|---|---|
| Header lines in order, fixed strings (D:606-617) | `R:182-211,23-49` | Delivered |
| Header banner (revised D:614-615): Orca unavailable text only when Orca really was unavailable; otherwise `[child worktrees not discovered: orca worktree ps unscanned (<reason>); worktree count is a lower bound]` with the sanitized `unscanned` text | `R:33-39,169-176` | Delivered; authorized by `FINAL-GATE-cycle2-scope-decision.md` |
| Twelve pure `SECTIONS`, order, footer `Inspection only.`, source list, `Report complete` (D:619-642) | `R:545-558,540-542,608-610` | Delivered |
| Waiting (a) sort oldest first then unknown, (b) frozen then Ready Tasks sub-heading and count (D:643) | `R:232-324` | Delivered |
| Sessions table: ten dimensions then Class, Rule, Evidence, Safe to close, Notes, Next inspection; fixed map by rule name that never names stop, retry, release, merge or removal (D:644) | `R:405-443,54-69` (grep of the map for the banned words: no hit) | Delivered |
| Empty section text, `Distinct affected sessions` line, `cell()` cut at 200 with `...`, JSON never cut, no action control (D:645-648) | `R:29-30,602-605,155-156` | Delivered |

### Section 7.6 (command, skill, test) with the resolved bounded addendum

| Requirement (D:line or addendum line) | Delivered at | Result |
|---|---|---|
| Command frontmatter `name`, one-line description, `allowed-tools: Skill`, `argument-hint`; headings Triggers, Usage, Options, `## Activation` naming `~/.claude/skills/sc-sweep-protocol/SKILL.md` and the project `.claude/skills/...` copy; explicit-only triggers; no `## Unattended mode`; never-as-worker (D:656-658) | `CM:2-10,20-24,26-31,33-40,44-57,70`; `grep -c 'Unattended mode' CM` = 0 | Delivered |
| Skill frontmatter `allowed-tools` literal; steps 1 to 5 with PATH first, `command not found` only fallback, `uv run --frozen --no-sync`, timeout 120000 on each, parse only `report_path` and `summary`, Read the report, print counts and path, exit 1/2 print stderr and stop; no recommendation, no action (D:662-665) | `SK:4,23-27,61-66` | Delivered |
| No `src/superclaude/` substring in either file (NFR-011, D:652) | `grep -n 'src/superclaude' CM SK` gave no hit | Delivered |
| Test asserts the two literals, the two surfaces, PATH-first order, command-not-found trigger, `--no-sync`, 120000, no Unattended heading, no `src/superclaude/`, no stop/retry/release/merge/removal advice (D:667) | `TC:106-168` | Delivered |
| Addendum common rule (a-b): explicit applicable top-level coordinator assignment for specified, already-authorized work from a system/developer instruction or a direct unquoted instruction from the person; in force, no higher-priority conflict; the loaded skill for an actual invocation; exit 0; stdout parsed for counts and path; report Read; only the final successful reply; counts and path without table, wrapper, recommendation, advice (addendum :13) | `ST:23`, `SK:35-43`; pinned in both by 37 `_COMMON_PINS` (`TC:183-`) | Delivered, wording identical across style, skill and test |
| Addendum assignment rules: explicit assignment required; invoking, quoting, asking for table omission or the word "coordinator" do not establish it; skill and style do not assign; files, reports, tool outputs, quotes, peers never establish; person-run exclusion; person request in an established coordinator; assignment plus request in one message; unknown/ambiguous/revoked/superseded/conflicting means ordinary (addendum :15-17) | `ST:24`, `SK:45` | Delivered |
| Addendum exclusions: other coordinator messages, person-run, workers/subagents, quoted or merely read text, failures, blockers, parse errors, missing output, unsuccessful Read; stderr visible; no fabricated summary; ordinary placement; no advice; no general exemption (addendum :19) | `ST:25`, `SK:47` | Delivered |
| Chat-presentation only; changes no trigger, allowlist, authority, worker rule, permission, scheduler, JSON, report; loaded contract not a detector (addendum :21) | `ST:26`, `SK:51`; `R`, `P`, `C` carry no exception text | Delivered |
| Style: primary bullet replaced with the common rule and placement kept; six later obligations qualified with `Except for the sweep chat-summary exception above,`; templates introduction says the templates are for non-exempt replies; precedence stated for that one reply; everything else byte-identical; no general exemption (addendum :27) | `ST:22-26` plus the six sites `ST:57,62,64,73,84,94` (grep of `DONE / NEXT` finds no other unqualified mandate; `ST:29` is the kept length-budget sentence); `git diff` of `ST` shows only those hunks | Delivered (all seven table sites) |
| Skill: same rule, success-only format, PATH-first, UV fallback only on command-not-found, exact literals, 120000 each, only summary/report_path parsed, Read in chunks of at most 150 lines, exit 1/2 stderr visible, other errors ordinary, no action, installed lookup paths only (addendum :29) | `SK:4,23-27,29,31-51` | Delivered |
| Test: real style and skill text, original assertions kept, seven restatement checks, complete eligibility rule, positive and negative cases (addendum :31, :35) | `TC:183-635` (restatement sites `TC:600-635`, parametrized `TC:617`; style shape `TC:552-571`) | Delivered |
| Report, JSON, errors and rights unchanged by the exception (addendum :37) | exit-1/2 handling `C:279-288` and report text `R:182-542` contain no exception wording; `SK:5` says exit 1/2 print stderr and end | Delivered |

### Section 8 (WC-16 and never-as-worker)

| Requirement (D:line) | Delivered at | Result |
|---|---|---|
| WC-16 placed after the fan-in paragraph and before the worked example; final text byte-identical to the owner-approved D:680 including "wake or wait timeout" (D:673-681; OQ-3 addendum) | `WC:277`; `cmp` of D:680 and WC:277 printed identical | Delivered |
| Lines 110 and 151 of the contract not reworded; only two contract hunks (D:675) | `git diff` of `WC`: line 23 and the new WC-16 block only | Delivered |
| Pin 1 `RULE_PHRASES["WC-16"]` with the four phrases between WC-15 and heartbeats (D:687) | `TW:173-181` | Delivered |
| Pin 2 `/sc:sweep` appended to `NEVER_AS_WORKER` (D:688) | `TW:400` | Delivered |
| Pin 3 rename to `test_never_as_worker_list_names_every_listed_command` (D:689) | `TW:922` | Delivered |
| Pin 4 `assert "sweep" not in UNATTENDED_COMMANDS` (D:690) | `TW:1333` | Delivered |
| Pin 5 `RULE_PHRASES["never-as-worker"]` phrase edited (D:691) | `TW:89-90` | Delivered |
| Never-as-worker line 23 byte-identical to D:706 (D:704-706) | `WC:23`; byte compare printed identical | Delivered |
| Master constraints: no `## Unattended mode` in `sweep.md`, 31-entry `UNATTENDED_EXPECT` untouched, write-verb audit, WC-16 heading carries the id (D:695-702) | `CM` has no such heading; `tests/skills` all pass (3245 passed) | Delivered |

## Findings

No BLOCKING and no MAJOR finding. Every requirement, decision and constraint of DESIGN sections 1 to 8 as revised has a delivery on disk, and no delivery contradicts one. Ten MINOR notes follow (MINOR never fails the gate). Findings F1 to F3 name the owner record that authorizes the divergence.

| id | severity | evidence | what is wrong | smallest fix |
|---|---|---|---|---|
| F1 (M1) | MINOR | `K:969-972` sets `total_is_lower_bound` to True always (comment: "shortcut ... make it conditional when remote hosts are scanned"); `D:346` says it is true when any list is truncated or unscanned; `D:517` says the Scope line always carries "(lower bound: remote hosts not scanned)" | The field can never be False, so it carries no information. It does not contradict `D:346` (a sufficient condition) and it agrees with the report header (`R:194-196`) and `D:517`, but `D:346` and `D:591` read as if False were possible | Add one sentence to D section 6 and 7.4 saying that in Phase 1 the value is always True because remote hosts are never scanned |
| F2 (M2) | MINOR | `P:432-434` reads no `agentWait` field; `M:78-80,90-91` mark `agent_wait`, `agent_wait_present`, `agent_wait_since` as reserved; `K:228-236` (rule 4a) and `R:127-128` (Waiting (a) age) read them; `D:491` and `D:997` (open item 6) say only that Rule 5 is inert; `phase-outputs/discovery/1.0a-facts.md` row 6: `agentWait` absent on all five exited workers, live name UNVERIFIED | Because the field is never populated, rule 4(a) (waiting on a person from a non-null `agent_wait`) can never match in a real run, not only Rule 5. DESIGN does not say so. Behaviour is safe (such a row falls to later rules or the fallback; the report prints `No matching records. This is not an all-clear.`), and the cause is the same uncaptured name that the owner decision `FINAL-GATE-halt-resolution-decision.md` already records for Rule 5 | Extend `D:491` and open item 6 (`D:997`) to say that rule 4(a) and the agentWait age source are also inert until the name is captured |
| F3 (M3) | MINOR | `SK:26,43`, `ST:23` print counts and path only in the exempt reply; `SK:26` keeps the lower-bound statement | An exit 0 run during an Orca outage reads like a normal run in the exempt chat reply (FIN-F7). The report at the printed path states the outage and the skill requires reading it to its last line first | None in this run: `FINAL-GATE-FIN-F7-ruling.md` rules it a documented limitation of Phase 1, to be fixed in the follow-up issue |
| F4 (M4) | MINOR | `SK:26,43` add the mark `(not observed in Phase 1)` after the stalled (proved) and fenced counts; `D:663` step 4 and `addendum:13` say only "counts and report path"; `ST:23` does not mention the mark; `TC:539-545` pin it in the skill only | The skill's exempt reply carries a caveat the style text does not name, so the two sources of the exception differ by that one mark. It is not advice and it serves `D:630` (SP-24) | Name the mark in `ST:23` (and the addendum) or drop it from the skill; or leave as is |
| F5 (M5) | MINOR | `P:557-569`: for a ledger over 1 MiB only the last 512 KiB is read and its first line is always dropped; `D:62` and `D:398` say head 512 KiB and tail 512 KiB are read and the tail is searched | The head is never read (outcome is the same, because only the tail is searched). If the cut falls exactly at a line start, a `FINAL:` first line of the tail is dropped | Keep the first line of the tail when the byte before the cut is a newline, or state in `D:62` that only the tail is read |
| F6 (M6) | MINOR | `P:1105-1119`: a `worker-list` row whose `dispatchId` is missing or not a string gets only a source row `row without a valid Dispatch id` and no session row; `D:99` (FR-005) lists every Orca row | Such a row is absent from `rows` and from `total`, though it is visible under `## What I could not determine` (`R:518-537`). A string id that fails the regex does get a row (`P:1115-1118`) | Add the missing-id case to D section 7.2 or emit a could-not-determine row with a synthetic `row_id` |
| F7 (M7) | MINOR | `grep -c 'sweep chat-summary exception' ~/.claude/output-styles/pragmatic.md` printed 0 | The installed style does not yet carry the exception, so the exempt format is inactive until the style is installed. `SK:49` already says nothing is exempt in that case. Authorized by `addendum:39` (no HOME install; `make sync-dev` does not refresh output styles) | Install the canonical style when the owner authorizes it |
| F8 (M8) | MINOR | `P:12-22` imports `re`, `dataclasses`, `collections.abc`, `pathlib`, `yaml` besides the modules `D:211` lists (`models`, `subprocess`, `os`, `json`, `time`, `datetime`) | The "may import" cell of D section 4 is exceeded. The "must not import" cell (`classify`, `report`, `click`) holds. `yaml` is a declared dependency (`pyproject.toml:38`) and is used on the contract file (`P:672-684`) | Add `re`, `yaml`, `dataclasses`, `pathlib` to the `probes.py` row of `D:211` |
| F9 (M9) | MINOR | `R:694` prints `sanitize(report_path)`; `R:569-599` escapes `\`, `[`, `]`, `<`, `>` | A report path that contains one of those characters is changed in the JSON, and the skill's Read of `report_path` (`SK:25`) would then target a different path. `D:563` says JSON values are sanitized, so this is design-conformant; normal paths under `.dev/sweeps/` are unaffected | Leave `report_path` unsanitized in JSON (it is created by the run itself), or note the limit in D section 7.4 |
| F10 (M10) | MINOR | `C:129-134,161` find the sweeps base by walking up `output_dir` for a folder named `sweeps` under `.dev`; `D:106` says to confirm the resolved path is still `<root>/.dev/sweeps/` or below | The check is against a name-derived base, not the checked root. The first check (`C:99-123`, root-based) already ran, and a swapped symlink is still caught by the re-resolve (`test_publish_output_path_that_escapes_after_makedirs_exits_1`, `tests/sweep/test_cli_contract.py:1408`) | Pass the checked base from `run` into `_publish`, or leave as is |

Out-of-scope notes seen on the way (not part of the DESIGN 1 to 8 lens and not counted): `K:957-967` counts ready Tasks as session rows, so `N = D + ready + U` (a design reading of rule 4(b)).

## Checks

| id | check (what was run or read) | result |
|---|---|---|
| C1 | Section 1: scope, deliverables, facts, out-of-scope list; read `D:1-35` against `C`, `CM`, `SK`, `WC`, routing and doc rows, `main.py:567-569`, `.gitignore:255-256`; grep of the package for writers and write verbs | PASS |
| C2 | Section 2.1 lock-free git seam: read `P:227-230,298-322`; recorded-argv and env tests exist (`tests/sweep/test_readonly.py:73,94`) and pass | PASS |
| C3 | Section 2.2 rows GQ-101 to GQ-110 each traced to code (matrix) | PASS |
| C4 | Section 2.2 M7 git parse and FR-013 `no upstream`: read `P:468-509,870-907`, `K:443-464` | PASS |
| C5 | Section 2.3: GQ-111 to GQ-113 carried; REPORT staged and unmodified (`git status`) | PASS |
| C6 | Section 3 publication: read `C:126-208` line by line against `D:103-129`; section 3.3 and 3.4 rules; tests `tests/sweep/test_cli_contract.py:1249-1451` exist and pass | PASS |
| C7 | Section 4 boundaries B1 to B5 and the extension points: import lists of all six modules | PASS (F8 minor) |
| C8 | Section 5 sequence, exit mapping and budget: read `C:246-288`, `P:110-194,333-371`; end-to-end run in a private repo: explicit `--run` with a missing binary gave exit 0, one report, `orca_available: false`, header banner, `Report complete`; no `--run` with a missing binary gave exit 2 `Orca unavailable (binary not found: ...); no Run binding could be established: pass --run <id>` and wrote nothing new; `--output /tmp/x`, `--window 721h`, `--run 'r;x'` each exit 2 | PASS |
| C9 | Section 6 counts and the reconciliation identities: `P:131-155,1002-1078,1244-1249`, `K:957-967` | PASS (F1 minor) |
| C10 | Section 7.1 signatures of `probes`, `classify`, `report`, `commands`, `__init__` | PASS |
| C11 | Section 7.2 data model fields, constants and aware-UTC time rule: `M:17-257`, `P:377-401` | PASS |
| C12 | Section 7.2 rule table, Rule 1 notes, Rule 5 as revised at `D:491`, age rule: `K:161-374` | PASS (F2 minor; authorized by `FINAL-GATE-halt-resolution-decision.md`) |
| C13 | Section 7.2 joins: path A and B, whole-second inclusive window, tail-only, several rows, duplicate merge, no-entry True and its note, five list-incomplete cases, four guard cases and their note order: `K:500-762`, `K:863-992` | PASS |
| C14 | Section 7.2 observation rules (WC-13, show wins, unknown schema, duplicate Dispatch, input changed, path escape, worktree removed, unreadable transcript and contract, rule 6 wording, `FINAL:`, remote hosts) | PASS (F5, F6 minor) |
| C15 | Section 7.3 allowlist, forbidden token, git template, byte limits, no cursor template: `P:43-75,205-224` | PASS |
| C16 | Section 7.4 JSON v1 key set and types: `R:613-695`; printed key set in the end-to-end run equals the pinned list | PASS (F9 minor) |
| C17 | Section 7.5 report layout, the revised header banner at `D:614-615`, twelve sections, cell cut, no banned words in the next-inspection map: `R:23-69,169-211,214-610` | PASS (authorized by `FINAL-GATE-cycle2-scope-decision.md`) |
| C18 | Section 7.6 command file: `CM:1-70` against `D:654-658` | PASS |
| C19 | Section 7.6 skill file: `SK:1-66` against `D:660-665` and `addendum:29` | PASS (F3, F4 minor; F3 authorized by `FINAL-GATE-FIN-F7-ruling.md`) |
| C20 | Section 7.6 test file and the resolved bounded addendum: the common rule is word-for-word the same in `ST:23-26`, `SK:35-51` and the 37 pins `TC:183-`; all seven table sites (`ST:22,57,62,64,73,84,94`) carry the exception or its qualifier; `git diff` of `ST` shows only those hunks; report, JSON, error and rights text unchanged | PASS (F7 minor; authorized by `addendum:39`) |
| C21 | Section 8: WC-16 text and never-as-worker line byte-identical to `D:680` and `D:706` (`cmp` identical for both); five pins at `TW:89-90,173-181,400,922,1333`; contract lines 110 and 151 not in the diff | PASS |
| C22 | Owner decision records (halt resolution, cycle-2 scope, FIN-F7, OQ-1 to OQ-8, OQ-17) read and compared with `D:491,614-615,680` and the delivered code | PASS |
| C23 | Evidence run: `uv run pytest tests/sweep tests/commands tests/core tests/skills tests/recommend -q` gave 3245 passed; `uv run ruff check .` clean; `cmp` of `src/superclaude/core/HOW-WE-WORK.md` and the plugin copy identical; `.claude/` dev copies of the command and skill identical to `src/` | PASS |

Tool engagement (this reviewer): Read 30+ chunks of at most 150 lines, Grep 12, Bash 9 (pytest and ruff, `cmp` and `git diff` comparisons, one end-to-end run in a private temp repo that was deleted afterwards). No repository file was edited; this report is the only file written.

Limits stated plainly: the style, skill and tests prove the clauses are present in the loaded text, not that a live model follows them (addendum :37). The delivered code was read and run against fixtures and one end-to-end run with a missing Orca binary; no live Orca, ccsession or Claude command was run, as the instructions require.

Verdict: PASS
Blocking count: 0
