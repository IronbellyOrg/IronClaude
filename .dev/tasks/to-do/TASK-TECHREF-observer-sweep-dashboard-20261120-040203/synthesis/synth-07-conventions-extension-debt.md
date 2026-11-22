# Synthesis 07: Sections 12-16 and Appendix text (observer, sweep, agent-work-report, dashboard design)

> Basis: code at origin/master 61ac2c2e6 (read-only export `/home/coder/.cache/ic-snap-20261120/master`); design package at docs-branch commit 495eb96d1. Paths below are relative to the repo root at 61ac2c2e6 unless stated. Sources: research files 01-06, gap-fills GF-1 to GF-5, `gaps-and-questions.md` (134 rows), Gate 1 minor findings M-1 to M-17. Where a gap-fill supersedes a research file, the gap-fill is used (C8 labels: GF-1; extension contracts: GF-4). No unification is recommended anywhere in this file. Nothing was executed; test counts are counts of definitions.
> Line budget: the brief asked for about 160 lines; the Section 14 duty to carry every contradiction, stale item and UNVERIFIED item makes this file longer.

---

## 12. Conventions & Patterns

### 12.1 Code Conventions

| Convention | Description | Evidence |
|---|---|---|
| Read-only by construction, observer | Exactly three Orca argv shapes (`skills list --json`; `orchestration worker-list --json --limit 100 [--run][--cursor]`; one 8-token `orchestration check --all --types question --run <id> --json`). `assert_allowed` runs inside both argv builders. 13 forbidden prefixes (check, --ack, --wait, --retry-request, --peek, dispatch, inbox, run-use, run-create, send, ask, reply, reset); `check` is legal only inside the 8-token shape. No shell; own process group; kill on timeout or overflow. | `observe/adapter.py:29-50, 135-170`; guard tests: forbidden set may grow, not shrink (`tests/observe/test_adapter.py:178-192`); no module except `adapter.py` imports `subprocess` (`tests/observe/test_commands.py:585-601`) |
| Read-only by construction, sweep | `probes.py` is the only module that starts a process. Orca: 10 token-for-token templates (`ALLOWED_ORCA`), `--include-remote` rejected in any position, check runs before any process. Git: 4 fixed shapes, always `--no-optional-locks`, `-c core.fsmonitor=false`, `GIT_OPTIONAL_LOCKS=0`; filter pre-check refuses `git status` when a filter driver with a command applies. Only write: one report file via temp file + `os.link` (never overwrites). | `sweep/probes.py:49-62, 226-244, 331-340`; `commands.py:153-208`; four pin layers: allowlist tests, `ast` scan for write verbs (`test_probes_allowlist.py:475-498`), recorded-argv tests (:609-638), file-snapshot diff (`test_readonly.py:376`); real-git hole tests `test_git_config_hole.py` |
| Not read-only, agent-work-report | All subprocess calls go through `common.run_cmd` (list args, no shell) except the page server `Popen` (`page.py:318`) and `git remote get-url` (`sessions.py:119`). `gh` use is read only. The skill does write: a ClickUp DM, an Orca unread mark, text typed into the coordinator terminal, an Orca browser tab, a detached `http.server`, files under `.dev/coordinator/`; the model makes the Step 14 git commit. The guard is test fakes (`fake_gh` fails any command but `issue view`). | `common.py:103-113`; research 05 s27; `tests/skills/test_agent_work_report.py:2941-2959` |
| Unknown is never zero, never all-clear | Observer: dedicated `UNKNOWN` singleton, never None/0/False/"" (`parse.py:43`); only `export.py` turns it into the string "UNKNOWN"; `observedOpen` is "UNKNOWN", never 0; screen gap notice `Human questions: source UNVERIFIED, 0 rows interpreted, not "no questions"`. Sweep: every failure maps to `unscanned` or None, never to clean; `NO_RECORDS = "No matching records. This is not an all-clear."`; "Missing proof never becomes False" (SPEC:232); unknown-age group when no wait time. | `parse.py:25-43`; `view.py:45-48`; `probes.py:923-934`; `report.py:29`; `test_snapshot_schema.py:501-512` |
| Phase limits are printed in the output | The sweep report prints its own limits: `SP24_LINE` (stalled and fenced not observed; a zero count does not mean none occurred), `SAFE_TO_CLOSE_LINE`, `Messages coverage: partial`, "creator not observable in Phase 1", "This brief is not an assurance of completeness". | `report.py:42-49, 199, 302` |
| Layering | Observer: adapter -> parse -> collector -> view (pure `build_view`) -> render / export. Collector never decides STALE; `export.py` imports none of render, parse, adapter, collector; `render(view, policy, message)` takes no other input. Sweep: probes (I/O) -> classify (pure; no file, process or clock; time only from `ctx.now` / `ctx.window_start`) -> report (pure; imports `re`, `unicodedata`, `models`) -> commands (publish). AWR: scripts write run-folder files; the model writes only judgement parts; a sha256 chain gates delivery. | `collector.py:1-6, 39`; `export.py:1-7`; `classify.py:3-5`; `report.py:1-7`; `run.py:204-368` |
| Single construction points | `View` is built only in `build_view`; `Classification` only through `_classification`; every observer display literal is a module constant (`view.py:44-134`, "every literal is defined here once"). | `view.py:968-1156`; `classify.py:130-143` |
| Closed, additive-only schemas | Observer snapshot: Draft-07, `additionalProperties: false` on root and nested objects, `schemaVersion` const 1; new optional field by reviewed edit, remove/rename/retype needs version 2. Sweep JSON v1: every key always present, `JSON_SCHEMA_VERSION = 1`. | `snapshot.schema.json:3-9`; `report.py:613-616`; `models.py:18` |
| Gate constants True only with a cited record | `QUESTION_GATE_PASSED` and `QUESTION_LINK_PASSED` are `True` and tests require a cited, existing record (these two tests cannot pass on the snapshot, which omits `.dev/`). | `observe/commands.py:67, 70`; `test_commands.py:754-779` |
| Recorded captures drive fixtures | Goldens are redacted recordings (no path, handle, token, credential, URL or escape byte); sweep fixtures `tests/sweep/fixtures/captured-*.json` come from dated captures; only rule 5 has a captured-fixture proof. | `test_golden_contract.py:205-213`; `tests/sweep/fixtures/SOURCES.md` |

### 12.2 Architectural Patterns

| Pattern | Where Used | Description |
|---|---|---|
| First-match-wins rule table | Sweep `RULES` (9 `Rule(name, match)`) | `match(row, ctx)` returns `Classification` or None (decline). Rule 9 `fallback` always returns, so every row gets one class. Post-steps can force `could not determine` (unreadable transcript, ambiguous join, 256 KiB tail limit). `classify.py:345-386` |
| Strict envelope, lenient rows | Observer `parse_page` | Envelope shape error raises `ShapeError` (cycle FAILED); a bad row is counted and skipped; 31 keys read, other keys counted and dropped; missing value = UNKNOWN. `parse.py:365-407` |
| Single-flight polling, immutable result | Observer `Collector` | One daemon thread, one cycle at a time, 15 s interval, backoff 15/30/60 s only when the first page fails; one frozen `CycleResult` replaced under a lock. `collector.py:28-34, 155-184, 304-321` |
| Panel as typed dataclass plus builder returning None | Observer `QuestionsPanel`, `DeskView` | Typed frozen dataclass, builder returns None when off, defaulted field on `View`, set by keyword in `build_view`. `view.py:253-298, 368-370, 1104-1156` |
| Atomic publish | Sweep `_publish`; observer `write_atomic` | Sweep: temp `O_EXCL`, fsync, `os.link` to first free name `<stem>.md` .. `-99.md`, unlink temp. Observer: `mkstemp` in the same dir, fsync, `os.replace`, mode 0600. `commands.py:153-208`; `export.py:257-274` |
| Budgeted reads | Sweep `Budget`; observer caps | Sweep 50 `worker-show`, 90 s total, 10 s per call, 8 MiB output. Observer 5 calls per cycle (4 worker-list + 1 question), 10 s, 8 MiB, 2 KiB stderr. `probes.py:85-89, 124-208`; `adapter.py:57-63` |
| Hardened reading of local files | Sweep disk reads; AWR `entry_files` | Every sweep read is checked with `_inside` (symlinks resolved); AWR refuses a symlinked entry folder or file, skips unparseable JSON, drops `javascript:`/`data:` urls. `probes.py` s1.5; `common.py:183-209` |
| Run-folder sha256 chain | AWR gate | `check.py` writes `overview sha256` into `script-checks.md`; `page.py` writes `overview-sha256` into `report.html`; `build_summary` regenerates `summary.md`; `gate` recomputes all three. `run.py:204-368` |

Status vocabularies in use (five over overlapping Orca data; the words `working` and `stalled` appear in more than one):

| Vocabulary | Values | Defined at |
|---|---|---|
| Observer cycle / source / coverage | cycle NOT_POLLED, NOT_AVAILABLE, OK, FAILED, PARTIAL; view adds STALE (45 s monotonic); snapshot `source.status` OK, STALE, ERROR, UNKNOWN; coverage COMPLETE, PARTIAL, MISMATCH; panel PENDING, OK, STALE, FAILED | `collector.py:44`; `view.py:33-35, 456-463, 664-695`; `parse.py:214-218` |
| Sweep classes | 8: waiting on a person (kind a or b), stalled (proved), fenced, working, finished, idle, person session (active), could not determine; `SAFE_VALUES` yes / no / could not determine; `PACKAGE_STATES` | `models.py:50-71, 62-69` |
| AWR session statuses | 6: working, progressed, waiting on you, stuck, stalled, done (plus 9 `STATES`, 4 `LEVELS`) | `common.py:240-247, 375-399` |
| FR-9 follow-up states | 8: working, question, gated, delivered, claimed-missing, stalled, failed, not-started; design only; field-to-state mapping lives in a spec not in the snapshot (UNVERIFIED) | `docs/designs/orchestrator.md:648, 572` |
| Worker-contract liveness | S0-S11 with rungs L0-L5 | `core/WORKER-CONTRACT.md:116-155` |

### 12.3 Anti-Patterns (Things to Avoid)

| Anti-Pattern | Why It's Wrong | Do This Instead |
|---|---|---|
| Standing in None, 0, False or "" for a value the source did not give | Breaks "unknown is never zero"; the schema, tests and counts rely on UNKNOWN | Use UNKNOWN (observer), `unscanned`/None (sweep), unknown-age group; convert only in `export.py` |
| Adding an Orca argv outside the allowlist, or `--ack` / `--wait` / `--peek` to the observer | The observer's non-consuming read is the property the owner accepted on 2026-11-12 (UNVERIFIED for a non-owner reader) | Add a template deliberately with its tests (13.1 B); never shrink the forbidden set |
| Writing a new snapshot key on every row | Changes the questions-off bytes pinned by `golden_release1_records.json` ("never regenerated") | Conditional key (like `orderUnknown`, `questions`, `collection`) or a reviewed golden change |
| A ninth `CLASSES` entry without extending the unpack | `classify.py:42-51` unpacks eight names; a ninth entry fails at import (from Python semantics, not run) | Edit `CLASSES`, the unpack, `RULES`, `NEXT_INSPECTION` and the test tables together |
| Describing a capability in the present tense while its producer is absent | The documented route fails: `SKILL.md:14-16` (entry files), `CHANGELOG.md:170` (`working` never produced) | State the limit and the deciding line, as the sweep report does with `SP24_LINE` |
| Parsing worker text as markup, or showing it unsanitized | Terminal escape and markup injection | Build `rich.text.Text` from data; sanitize at the parse edge (observer) or `sanitize`/`cell` (sweep) |
| Using `dispatchId` as a question identity | Question identity is `(Run, message.id)`; a dispatch id is never one | Keep `merge_questions` keyed by Run and message id (`parse.py:416-418`) |
| Advice words in `NEXT_INSPECTION` | The report recommends nothing; `BANNED_WORD` forbids stop, retry, release, merge, remov* | Name only what to read (`report.py:54-68`; `test_report.py:1102-1130`) |
| Bare `orca` in the sweep | Sweep default binary is `orca-ide` or `$ORCA_CLI_COMMAND`, "never bare orca" (INV-017); AWR does use bare `orca` (fact, two code paths) | Go through `probes.orca_binary()` |
| Importing `subprocess` outside `adapter.py` / `probes.py` | Tests pin the single process seam | Add the call to the existing seam |

## 13. Extension Guide

Signatures below are from GF-4 (read, not run). Each scenario lists registration points; skeletons are minimal and use only verified signatures.

### 13.1 Common Extension Tasks

| Task | Steps | Files to Touch | Pitfalls |
|---|---|---|---|
| A. Add a sweep class or rule | 1 Add the class string to `CLASSES`; add a 9th name to the unpack. 2 Write the rule and register `Rule(name, fn)` in `RULES` at the precedence position. 3 Add `NEXT_INSPECTION[rule]`. 4 Edit report sections only if the class needs its own section (default: it shows only in the `Sessions` table and `summary.counts`). 5 Update the test tables. | `sweep/models.py:50-59`; `sweep/classify.py:42-51, 345-355`; `sweep/report.py:26-27, 54-68, 545-558`; tests `test_classify.py:277, 351-361, 371-379`, `test_report.py:1091-1127`, `test_cli_contract.py:956, 1032, 1077`; prose `docs/designs/orchestrator-mode.md:474`, `commands/sweep.md:14` | `report.py:26-27` index `CLASSES[5]`, `CLASSES[7]` (shifts if you insert before them). `class_name` not in `CLASSES` raises KeyError at `classify.py:976`. `classify_all` tests the rule names `idle` and `person_active` once, at `classify.py:958` (adds the `last_activity from <source>` suffix); a new rule whose evidence needs that suffix must be added to that tuple. `NEXT_INSPECTION` is keyed by rule name, not class name; a missing key falls back to `_NEXT_DEFAULT`. Rule 2 and rule 3 are the only producers of stalled and fenced; a new class that needs a new Orca field also needs scenario B. Whether a new JSON key needs `JSON_SCHEMA_VERSION` bumped is not stated in code (U-30) |
| B. Add a sweep probe or allowlist entry | 1 Add one token tuple to `ALLOWED_ORCA` (`<run>` and `<dispatch>` are the only placeholders; ids matched with `re.fullmatch`). 2 Add one call site shaped like the existing ones (worker-list at `probes.py:1150`). 3 Add the field to `OrcaObservation` (or `SweepInput`) and set it in `parse_worker_show`. 4 Add a `SourceCoverage` row for every read and failure. 5 Update the allowlist tests. For git: add a shape to `ALLOWED_GIT`. | `sweep/probes.py:49-62, 226-244, 266-312, 369-394, 458-515, 1143-1192, 1322-1396`; `sweep/models.py:83-112, 236-249`; tests `test_probes_allowlist.py:370, 375, 391, 405, 423-462, 475-498, 609-638`, `test_readonly.py:52-72, 448`, `test_git_config_hole.py` | `test_allowed_orca_is_exactly_the_ten_templates` and `..._names_seven_verbs` fail by design; the "10 templates, 7 verbs (NFR-014)" comment (:60) and the full-sweep recording (1 worker-list + 2 task-list + 5 worker-show + 1 `worktree ps` = 9 argv) change. Four pinned templates are tested as "zero argv"; the first call of one changes that test. `parse_worker_show` never raises. Failure maps to unscanned or None, never clean. A new git call must keep `--no-optional-locks`, `core.fsmonitor=false` and the filter pre-check (git config can start programs, issue 547) |
| C. Add a snapshot field | 1 Row field: add to `_FIELDS` and `Row`, populated by `parse_page`. 2 Export: add `("<jsonKey>", "<row_attr>")` to `_TEXT_FIELDS` (dotted key nests) or `_ANY_FIELDS`, or write a conditional key. 3 Top-level value: carry it on `SnapshotMeta`, set it in `_meta`, write it in `snapshot_dict`. 4 Edit `snapshot.schema.json`: add under `definitions.row.properties`; list in `required` only if emitted on every row. 5 Tests. | `observe/parse.py:58-90, 110-157, 365`; `observe/export.py:20, 25-47, 141-216`; `observe/view.py:203-223, 664`; `observe/snapshot.schema.json:106-155`; tests `test_snapshot_schema.py:25, 59-91, 296-326, 404-465`, `test_export.py`, `test_render.py:655-695` | Closed schema rejects an unlisted key. An unconditional row key changes the `snapshot_json` bytes of the five questions-off variants pinned by `golden_release1_records.json`; the conditional route leaves them unchanged. Privacy test lists keys that must never appear (`detail, activity, worktreeId, ownershipState, releaseState, warnings, nextCursor, body, token ...`); `WITHHELD_QUESTION_KEYS` forbids question text. 11 parsed attributes are not exported, with no stated reason for 6 of them (G-05). `counts` values are scalars in the schema but nested JSON to depth 6 in the parser (untested, G-03) |
| D. Add an observer view, panel or key | 1 New data? add a defaulted field to `CycleResult`. 2 Typed frozen dataclass and a builder returning None when off. 3 Defaulted `View` field, set by keyword in `build_view`. 4 Literals as constants in `view.py`. 5 Place it in `_compose`'s height budget and in each width class. 6 New key: `apply_key` (and `KEY_NAMES` if non-text). 7 Fixture variant if needed. | `observe/collector.py:37-68`; `observe/view.py:30, 44-134, 253-298, 334-378, 968-1156, 1246-1299`; `observe/render.py:480-568, 915-942, 1058-1111, 1258-1446, 1328-1376`; `observe/keys.py`; `observe/theme.py`; fixtures `parse.py:750-761` | Three width classes: full >=160, line 116-159, short 80-115 (below 80 columns or 8 rows only a refusal line prints). Ledger columns differ per class (`_columns`); question panel layouts A/B/C at 160 and 116, C only at 80; Decision Desk side by side, split, stacked. Keys change `Session` only; "no key can reach the adapter or collector" is a test. A new colour role must exist in `theme.py` (registration rule UNVERIFIED, U-33). Help line chosen at `view.py:1139-1141`. A new always-on element changes the surface pinned by `golden_release1_surface.json` |
| E. Add an agent-work-report source | 1 New script `scripts/<name>.py` with `main(run)`: read the run folder, write `<run>/<name>.json`. 2 Subprocess only via `common.run_cmd`. 3 Add the step to the SKILL.md step list and artifact table. 4 Join it in `match.py` / `classify.py`; present it in `render.py` and templates. 5 A new gate check means `REQUIRED_CHECKS` and `check.main`. 6 A new `run.py` subcommand needs an exact-argv-length branch. | `skills/agent-work-report/scripts/{common,run,match,classify,render,check,exclude}.py`; `SKILL.md:56-72, 76-95`; `run.py:204-212, 868-887`; `common.py:103-113, 133-151` | `run.py` has no option parser: any argv shape not matched falls to `sys.exit(__doc__)` (exit 1). `SKILL.md:38`: Orca's own session state is never read. A run without `--links` cannot pass the gate. The artifact table already omits `abandoned.json` and `refresh.lock`. Entry-file readers refuse symlinks. Tests patch `gh_json`, `run_cmd` and the ClickUp `call`; no test runs a real `orca`, `gh` or ClickUp call |

Skeletons (not full interfaces):

```python
# A. classify.py (rule contract: Classification = rule applies; None = decline, next rule tried)
def _rule_example(row: SessionRow, ctx: SweepContext) -> Classification | None:
    if not (...):                                   # only row fields and ctx.now / ctx.window_start
        return None
    return _classification(C_EXAMPLE, "example", "evidence text")   # (class_name, rule, evidence, waiting_kind=None, notes=())
# RULES += Rule("example", _rule_example)   models.CLASSES += "example"   report.NEXT_INSPECTION["example"] = "read ..."

# B. probes.py:49-60 (one tuple; compared token for token)
ALLOWED_ORCA = (..., ("orchestration", "<verb>", "--run", "<run>", "--json"),)

# C. export.py:25-45 and snapshot.schema.json definitions.row.properties
("<jsonKey>", "<row_attr>"),

# D. view.py: View gains `example: ExamplePanel | None = None`; build_view(...) passes example=_example_panel(result, clock)
def _example_panel(result: Any, clock: Any) -> ExamplePanel | None: ...   # None when the source is off

# E. scripts/<name>.py, shaped like exclude.py and sessions.py
def main(run) -> None: ...   # reads the run folder, writes <run>/<name>.json, exit 1 on failure like check.py
```

**Unification touch points (facts only; no recommendation).** Only rows that no other section carries are listed; the sweep and observer outputs, WC-16, `orchestrator_repo`, the entry-file contract, sanitizers, joins, Orca wrappers and "waits on a person" are in 2.5, 8.1 and 8.2.

| Touch point | Fact | Evidence |
|---|---|---|
| Run scoping and mailbox | observer `--questions` reads one named Run from the terminal that holds it (`consumer_fenced`, `no_active_terminal` otherwise); the same Run mailbox is what the design's wave 5 consumes with `check --wait`; the observer form carries no `--ack` or `--wait` | `adapter.py:34-50, 496-507`; GF-3 s10 |
| Extension seams in code | observer `CycleSource` Protocol, `Runner` / `Discover` aliases (`adapter.py:24-27`), `Deps` (`commands.py:132-147`); sweep `RULES`, `ALLOWED_ORCA`, `SECTIONS`; AWR `run.py` dispatch; package fixture schema is "explicitly not an Orca API" and shares no data with observer fixtures (all ten same-named files differ by `cmp`) | research 06 s2; GF-4 |

### 13.2 Testing Requirements for Changes

| Change Type | Required Tests | Test Location |
|---|---|---|
| Sweep class or rule | one case per rule (`_rule_cases`), `reached == set(CLASSES)`, rule-order pin `RULE_NAMES`, `RULE_CLASS` and `NEXT_INSPECTION` coverage, counts keys equal `list(CLASSES)`, report determinism and sections | `tests/sweep/test_classify.py:277-379`; `test_report.py:549, 937, 1091-1130`; `test_cli_contract.py:956, 1032, 1070` |
| Sweep probe, allowlist, git | exact templates, 24 named negative argv, write-verb `ast` scan, recorded-argv full sweep, zero argv for not-called templates, budgets, byte limits, symlink escapes, stable-read, real-git hole routes with a positive control | `tests/sweep/test_probes_allowlist.py`, `test_readonly.py`, `test_git_config_hole.py` |
| Sweep CLI, publish, JSON | exit codes 0/1/2, publish failure modes, JSON key set and types, lazy registration | `tests/sweep/test_cli_contract.py:260-1505`, `test_cli_registration.py` |
| Sweep prose (command, skill, style) | 28 static drift guards on `commands/sweep.md`, `sc-sweep-protocol/SKILL.md`, `output-styles/pragmatic.md`; WC-16 heading and sentences; routing row | `tests/commands/test_sweep_command.py`; `tests/skills/test_worker_contract.py:167-170, 212-215`; `tests/core/test_how_we_work_routing_table.py:33` |
| Observer adapter or argv | exact argv per path, forbidden set (superset floor), 22 + 17 rejected shapes, cursor and run-id checks, paging, caps, real-process kill tests | `tests/observe/test_adapter.py` |
| Observer parse, merge, collector | strict envelope, UNKNOWN, identity, newer-wins merge, backoff `[30,60,60,60]`, STALE at exactly 45 s, single flight | `test_parse.py`, `test_collector.py`, `test_golden_contract.py` |
| Observer snapshot or export | schema validity after every cycle for every variant, closed nodes, privacy keys, 0600 atomic write, byte pin of questions-off records | `test_snapshot_schema.py`, `test_export.py`, `test_render.py:655-695` |
| Observer view, render, keys | session transitions, view build, 135 render tests, height budget over widths and heights, real pty tests (colour depth, `NO_COLOR`, alternate screen), key decoder | `test_session.py`, `test_view.py`, `test_render.py`, `test_height_budget.py`, `test_live_screen_pty.py`, `test_keys_spike.py` |
| Observer CLI and gates | options, exit codes, `--once`, gate constants cite an existing record, registration | `test_commands.py`, `test_registration.py` |
| Agent-work-report | run lock, gate, summary, page, exclude, refresh, symlink and url safety, entry-file reader | `tests/skills/test_agent_work_report.py` (142 definitions; living-report tests at 2979-3983) |

Facts: tests were not run here; `test_commands.py:754-779` cannot pass on the snapshot because it omits `.dev/`; `tests/sweep/fixtures/captured-tab-map-*.json` are read by no test. All `tests/observe` paths above are under `tests/observe/`.

## 14. Known Limitations & Technical Debt

Labels follow rule R-C8 of GF-1 (14.5). Item ids (U-, CC-, SD-, DC-, G-, C8-) are the ids of `gaps-and-questions.md`. "None recorded" means no research file names a plan.

### 14.1 Current Limitations

| Limitation | Impact | Workaround | Planned Fix |
|---|---|---|---|
| Sweep `stalled (proved)` and `fenced` cannot fire on live data: `worker_done_seen` stays None and `fenced_evidence` stays `unreadable` because `parse_worker_show` never sets them (C8-1, C8-2, KNOWN LIMIT) | An exited worker prints `could not determine` with the note `Orca: exited; fenced evidence not readable`; a zero count means nothing | The report prints the limit (`SP24_LINE`); counts carry `(not observed in Phase 1)` | "until a source mapping exists" (SPEC:232); no work item owns the mapping (U-40); `fenced` has no "until" condition |
| Waiting (a) from `agentWait` alone has unknown age: `agent_wait_since` is never set (C8-3) | Row sits in the unknown-age group | A blocked contract gives an age from its mtime | None recorded; a non-null `agentWait` was never captured (U-11) |
| `Safe to close` and `Removable` never say `yes` (C8-4, C8-5) | Every cell reads `no` or `could not determine` with a reason | Read the reason text | Phase 2 `/sc:close` acts on these rows after the person confirms (SPEC:75, 208); no `yes` source is named |
| Sweep coverage gaps: remote hosts not scanned (lower bound), `Messages coverage: partial`, Ready-Task creator not observable, `worktree ps --agent-wait` never called | Totals are a lower bound; pending questions cannot be read | None | Out of Phase 1 on record (design s1 line 35) |
| Sweep show cap 50, no contract read, 256 KiB transcript tail, join path B | Live runs print mostly `could not determine` (issue #590: 264 sessions, 263 undetermined, causes not measured; recorded, not re-run [UNVERIFIED]) | Read the Evidence and Notes cells and the sources marked unscanned | Owner decision 2026-11-17 to page past the cap (issue #534 comment, wording UNVERIFIED) |
| Observer questions: one named Run, only from the terminal that holds it; 100-row window; nothing is ever closed ("seen is not resolved"); retention 1,000 | Bursts over 100 rows between reads may be lost; a handled question is listed again while Orca returns it | Run from the Run-holding terminal; export for newer questions | Recorded limit accepted in the owner pass record (2026-11-12) |
| Observer reads at most 500 worker rows per cycle (5 pages x 100; 400 with questions on); recorded live total was 428 | With questions on a full traversal never completes (always PARTIAL); oldest rows are the ones cut. Derived arithmetic, not stress-tested | Questions off | None recorded |
| Observer is POSIX only, needs a terminal of at least 80 columns and 8 rows, has no refresh key, and a polling thread ends if no Orca CLI is found | Windows prints POSIX-only text; narrow terminals print a refusal line | `--once` prints a plain record | None recorded |
| Observer snapshot v1 has no in-repo consumer; JSON drops 11 parsed attributes; the text record lists question subjects while the JSON does not | A second consumer would parse the file itself | None | None recorded |
| Question ledger and Decision Desk cannot be replayed from fixtures through `superclaude observe` (D-1, DEFECT-CANDIDATE, 14.5) | `--questions --fixture` exits 2 | Fake-runner tests exercise views B and C | Flagged for the owner |
| Living report: the entry writer `superclaude orchestrator report-entry` does not exist (C8-6) | `exclude.py` excludes nothing; `run.py refresh` renders no "Held by the orchestrator" block; closeout prints `ENTRY escalated why=surface_absent` | Entry files written by hand work (tests do this) | PR B (no PR); design states no interim behaviour (G-37) |
| `orchestrator_repo` key route to the state folder fails on master (C8-7) | Only `$AWR_ROOT` works | Set `$AWR_ROOT` | PR A (#686, open) |
| A "Needs you" entry for a session cannot be answered by `prefs.py answer ... <session url>` (C8-8, DEFECT-CANDIDATE) | The entry stays until answered | None found | Flagged for the owner |
| Coordinator cadence ("at most once every 5 minutes") and "read before acting" are text duties; nothing schedules or enforces them | A sweep runs only when a session runs it | None | WC-16 says Phase 1 "adds this duty, not a scheduler" |
| `ORCA_VERSION_FILE` is a fixed Linux path | On other installs the lock line always prints UNVERIFIED | None | None recorded |

### 14.2 Technical Debt

No research file rates severity or effort, so those template columns are not invented; the research label is shown instead.

| Item | Research label | Description | Evidence |
|---|---|---|---|
| `Window.more_text` | dead code | Field with no reader; spec says there is no "+N more" row | `view.py:331, 402`; `test_render.py:99-118` |
| `counts` schema/parser mismatch | untested risk | Schema allows scalars; parser keeps nested JSON to depth 6 | `snapshot.schema.json:50`; `parse.py:277-290` |
| In-memory row set only grows | untested | `merge` keeps absent rows with `reobserved=False`, no cap or expiry | `parse.py:654-744` |
| `_find_orca` iterates `topics` outside its `try` | UNVERIFIED (U-03) | A bad reply would end the observer's polling thread; not executed | `install_user_setup.py:265-268`; `launch.py:148-152` |
| `PER_CALL_TIMEOUT` comment | possibly stale (SD-02) | "UNVERIFIED until the first permitted live read measures it" while live reads exist | `adapter.py:60-62` |
| Constants labelled PROPOSED | UNVERIFIED (U-02) | `RUN_ID_PATTERN`, `CURSOR_MAX_BYTES`, ms heuristic, schema | `adapter.py:52-55`; `parse.py:247` |
| `RowView.liveness` | unread by ledger columns (U-32) | Read by `export._row_line`; other readers not traced | `view.py:190`; `export.py:62` |
| Sweep Budget defaults and four byte limits | no recorded decision (U-14) | Only the byte limits carry a "proposed" marker | `probes.py:85-89, 127-133` |
| AWR entry fields `kind`, `group`, `follow_up_state` | never read | In the contract comment or fixtures only | research 05 s26 |
| AWR `waker.py` hourly mode, `templates/qa-report-template.md` | leftover, unreferenced | No hourly automation exists; nothing reads a QA verdict | `waker.py:8-9, 216-220`; SD-16 |
| AWR page server and template | fact | Serves the whole `.dev/coordinator/` on 127.0.0.1:8765; template loads Google Fonts | `page.py:326-327`; `report-template.html:8-10` |

### 14.3 Future Considerations

| Item | Deferred Because | Revisit When |
|---|---|---|
| Sweep `stalled (proved)`, `fenced` live | no named live source for the absence of `worker_done` (SPEC:232) | a source mapping exists; none is tracked |
| Phase 2 `/sc:close` acting on Safe-to-close rows | Phase 1 is read-only (SPEC:75, 208) | Phase 2 |
| Sweep report retention (SP-22, person deletes by hand) | out of Phase 1 (design s1 line 35) | not stated |
| Observer write-back actions (reply, ack, resolve) | package contract is navigation only; recorded as a future stage that "never R1" and needs a boundary change on issue 409 | owner changes the boundary |
| Remote fleet rows (`--include-remote`) | R4 "Not established" (`release-gates.md:14`); backlog issue #604 | not stated |
| Admission, revision-pinned verification, cost, deep links, persisted "last look", rotation set | not established or left out on record (`release-gates.md:17, 53`; `rendering-rules.md:97`) | not stated |
| A Go/TUI reader of the JSON snapshot | deferred (`ARCHITECTURE-SPINE.md:287, 306, 318`) | not stated |
| Live issue 409 alignment items 1-10 (observer reads sweep JSON, recommendation text, PR/issue link sources) | all "None is decided" (body lines 108-121) | owner decision |
| Orchestrator pieces: PR B (skill, verbs, "Orchestrated issue flow"), PR A (#686), PR P (#690) | sequencing D, A, P, B on record (DESIGN:1011-1046; ruling 37) | per the design order |
| Rasterised PNG visual-parity comparison | PNG route failed; gate scored on the text and ANSI tier | owner requirement (G-27) |

### 14.4 Contradictions, stale documentation and UNVERIFIED items

Where research files disagree, the stronger evidence wins: code and tests over docs; gap-fills over files 01-06. Nine STALE DOC rows below are also [CODE-CONTRADICTED] in their source (SD-01, SD-06, SD-07, SD-21 to SD-24, SD-26, SD-27). Each row cites its research source in `gaps-and-questions.md`.

**A. Contradicted or stale documentation, grouped by subject** (document statement versus reality)

| Subject | ID and tag | Statement versus reality | Evidence |
|---|---|---|---|
| Sweep: design | SD-06 CODE-CONTRADICTED | `docs/designs/orchestrator-mode.md:27` says `src/superclaude/cli/sweep/` does not exist yet; the package exists (6 `.py` files). A dated fact (checked 2026-11-08) | Glob of `cli/sweep/` |
| Sweep: CHANGELOG | SD-07 CODE-CONTRADICTED | `CHANGELOG.md:170` (under `[6.0.0] - 2026-11-18`, "Known limits (sweep, Phase 1)") says `working` is never produced and healthy workers read `could not determine`; rule 5 is active since 2026-11-16 | `classify.py:251-269`; `test_cli_contract.py:1133-1140`; DESIGN:493, 841 |
| Sweep: CHANGELOG | SD-08 STALE DOC | Same line gives "the live `agentWait` names were never captured (design open item 6)" as the reason for stalled and fenced: the only public line that does. SPEC:232 gives a different reason; open item 6 is resolved 2026-11-16 (`orchestrator-mode.md:1003`) | CHANGELOG:170; SPEC:232 |
| Sweep: user guide | SD-09 STALE DOC | `docs/user-guide/commands.md:620` first clause (`working` never produced, healthy workers read `could not determine`) is stale; its clause "a waiting-on-a-person row from an agent wait cannot match on live data" is UNVERIFIED, not contradicted. `commands.md:619` is current and gives no reason | commands.md:619-621 |
| Sweep: issue and PR text | SD-10, SD-11 STALE DOC | Issue #534 body item 2 says rule 5 is inert (its own comment says PR #579 restored it; comment-level check only); PR #539 body lists "the working rule is inert and the agent-wait rule is dark" | `gh` read; `test_cli_contract.py:1133-1160` |
| Sweep: design status | SD-12 STALE DOC | Design section 17 still reads "Total: 23 open items" with no status column although item 6 is resolved and items 2, 3, 8 are implemented; treat as a historical list | `orchestrator-mode.md:992-1022` |
| Sweep: repo | SD-14 STALE DOC | The stale checkout `.gitignore` lacks the `.dev/sweeps/` rule that origin/master has at lines 255-256 | checkout vs master |
| Sweep: line cites (resolved) | SD-13, SD-15 (resolved by GF-1, GF-4) | D7 is at `orchestrator-mode.md:841` (also :636, :877); `design-base.md:813` is the task-package copy. `_classification` is at `classify.py:130-143`; :222 is inside `_rule_fenced` | GF-1 s1.2; GF-4 |
| Observer docs | SD-01 CODE-CONTRADICTED | `release-gates.md` R0 row says no recorded `worker-list` sample exists and `base` stands in; four golden samples exist and are tested | `fixtures/golden-*.json`; `test_golden_contract.py:22-199` |
| Observer docs | SD-02, SD-03 STALE DOC | `adapter.py:60-62` "UNVERIFIED until the first permitted live read" (live reads since 2026-11-17; possibly stale); RESEARCH-REPORT rotation set vs code (no contradiction found, tabled only) | `release-gates.md` lines 40-42 |
| Observer docs | SD-04, SD-05 STALE DOC | `post-release-report.md:56, 173` "No technical doc for `superclaude observe`" is still open at 61ac2c2e6 ("13 source files" vs 14 `.py` by Glob); `test_keys_spike.py:3` "only test module that uses a real pty" is older than `test_live_screen_pty.py:34` | docs/testing/v6.0.0 |
| Observer docs | CC-01 CODE-CONTRADICTED (minor) | "no key and no option maps to an Orca call" (`cli-groups.md:42`, HELP): true for keys and writes; `--run` and `--questions` select which read argv is built | `adapter.py:173-179, 469-512` |
| Report skill and entry files | CC-02 CODE-CONTRADICTED | `SKILL.md:14` and `common.py:25` name `orchestrator_repo` in `issue-watch.json`; the master poll rejects the key, so only `$AWR_ROOT` works. KNOWN LIMIT sequenced to PR A; the tag stands until PR A merges | `cycle.py:216-220`; ORCH:372, 374 |
| Report skill and entry files | CC-03 CODE-CONTRADICTED | `SKILL.md:14-16, 115-116` describe entry files and `exclude.py` in the present tense; the writer verb does not exist (design places it in PR B) | `refs/settle.md:99`; ORCH:510, 791 |
| Report skill and entry files | CC-04 CODE-CONTRADICTED (in part) | `SKILL.md:183` says the gate is enforced again by `clickup.py dm` and `run.py close`; `dm` enforces `deliverable`, `close` enforces only `passed()` | `clickup.py:619`; `run.py:376-379` |
| Report skill and entry files | CC-05 CODE-CONTRADICTED | Design DQ13 puts information entries under "Watching"; code uses "Other work in progress" and no "Watching" string exists | ORCH:123; `run.py:788-793` |
| Report skill and entry files | SD-16 to SD-20 STALE DOC | `qa-report-template.md` describes a verdict `run.py gate` reads (unreferenced; nothing reads it); `sc-closeout.md:361` says the skill is in IronFlow (moved by PR #684; the `report-entry` half is still true); `SKILL.md:56-72` omits `abandoned.json` and `refresh.lock`; design line cites into the IronFlow copy (render.py:194-303 etc., an expected shift); DQ12 "183 lines, 15 scripts" vs 194 and 16 | research 05 Stale |
| Issue 409 and design package | SD-21 to SD-24 CODE-CONTRADICTED | Live body says "No observer code exists yet" (lines 19, 36, 105), "No direction chosen" (25), PR #539 open (27, 28, 204: merged 2026-11-14), and the package is unmerged (`orchestrator-mode.md:609`: true only of commit 495eb96d1; the identical 406-file content is on master via PR #503). The body banner (line 13) says the observer is on master; the correction pass waits on an owner grant | `main.py:590-592`; PR #503, #539 |
| Issue 409 and design package | SD-25 to SD-29 STALE DOC | Package README and body prefer Bubble Tea / Lip Gloss; shipped observer is Python + Rich by owner decision 2026-11-08 (`stack.md:3`). `rendering-rules.md:3` says fixture mode uses the package's fixtures (different schema; only names shared). Local `issue-body.md:23` and `posted-body.md:23` say 405 files / 14,435,766 bytes (live: 406 / 14,438,526). `concepts.md:43-49` top three differ from the owner's staged three. Scope file `scope/04` cites wrong line numbers | research 06 s7 |
| Orchestrator design vs shipped | SD-30 to SD-35 STALE DOC | DESIGN:116, 135 cite WC-9 at :44-47 (now :41-45) and a `:300` line removed by PR #682; DESIGN:991, 1017 describe PR D as future work (merged 2026-11-20); guard comment at :500 is at `launch-level-guard.sh:496`; DESIGN:122 treats `refresh` and `exclude.py` as UNVERIFIED though the code exists; `closeout.md:97` names `/sc:issue --plan` (PR #690 open); ADD6 verb list omits `report-entry` and `plan-check` while the 5.1 row lists both | GF-3 Stale |

**B. UNVERIFIED items (all stay UNVERIFIED; M-17)**

| Subject | IDs | Statement | Evidence |
|---|---|---|---|
| Orca question read | U-01, U-04, U-05 | `orchestration check --all --types question` is not shown to be non-acknowledging: recorded probes show non-consumption for the owner-bound reader on probe Runs only; owner accepted the remainder 2026-11-12. Live message rate, `run-use` effect on a live coordinator, several concurrent observers, `message.id` on other Runs, fencing, the 100-row window, `--peek` order, latency and load figures are recorded probe results, re-verified only as encoded in code and fixtures | `adapter.py:34-50`; `release-gates.md:42, 48, 63`; `question-cap-100.json` |
| Observer constants, tests, versions | U-02, U-03, U-06, U-07, U-08, U-09 | `RUN_ID_PATTERN`, `CURSOR_MAX_BYTES`, ms heuristic (`> 1e11`) and the schema are PROPOSED; `_find_orca` robustness; four-kinds data-gate rule for messages (stale and contradictory samples); `tests/observe` golden and surface files not read; which tag first held R2 and R3 (no CHANGELOG entry); the two records cited by `commands.py:67, 70`; the Orca error-code names `consumer_fenced` and `no_active_terminal` (envelope `error.code`) are not shown to be verified against a live Orca (`adapter.py:65-69, 496-507`) | research 01 (line 52), 02 |
| Sweep inputs | U-10, U-11, U-12, U-13, U-15 | Whether Orca exposes a source for the absence of `worker_done` or fencing; the shape and meaning of a non-null `agentWait` (rule 4(a) unproven on live data; sweep reads `worker-show`, coordinator reads `worktree ps --agent-wait`); how often real transcripts exceed 256 KiB; whether path A ever matches in production; the definition of "route 7" in the git hole list | `models.py:98-112`; `probes.py:458-481`; `classify.py:40` |
| Sweep policy | U-14, U-16, U-30, U-31, U-39, U-40 | Budget defaults (50, 90 s, 10 s) have no recorded decision; design open items 17, 18, 21 not checked with `gh`; no stated rule for bumping `JSON_SCHEMA_VERSION`; a ninth `CLASSES` entry breaking the unpack (read from semantics, not run); how a live orchestrator or report session is classified (`could not determine` under path B per `classify.py:760-779`); no work item owns the "source mapping" (search, not scan) | `probes.py:127-133`; `models.py:18` |
| Observer internals | U-26, U-32, U-33 | `projection.attention` and `projection.parent` (present, redacted, not parsed) as attention or dependency signals; who reads `RowView.liveness`; `theme.py` role registration | `view.py:566-584`; `render.py:571, 1457` |
| Report skill and orchestrator environment | U-17 to U-23 | Who sets `orchestrator_repo` and writes `issue-watch.json`; Orca automations `coordinator-morning-wake`, `coordinator-missed-check` and their VERIFIED dates; the Orca automation `orchestrator-poll` (`*/5 * * * *`), the repo `IronbellyOrg/IronOrchestrator` and the `waker.py` triggers are outside the repo and not checked (research 05:571-572; GF-3:185-186; design O1, O3, O4); the spec path at `SKILL.md:12`; how the markdown entry-update template becomes the JSON entry file; design unknowns U17, U27, U38 (code answers partly, not run); ruling on two writers of the closed entry (`sc-closeout.md:374`); AWR test results ("142 tests" counts definitions) | research 05 |
| Orchestrator design | U-34 to U-38 | The eight FR-9 states and their mapping to `worker-list` fields (spec not in snapshot); whether WC-16 binds a script-started orchestrator (design says the orchestrator "is the coordinator", DESIGN:930; WC:70 says "a session the person opened"; open question of scope, flagged for the owner); the reach of PR B's "Orchestrated issue flow" section; typed approvals and the one interrupt against WC:122, 137, 188; `check --wait` types and cadence (design 4 types, 240000 ms; contract 9 types, 300000 ms) | GF-3 |
| Orca wrappers and recorded live result (no register id) | none | Why the observer, sweep and report skill have three separate Orca wrappers is not stated (synth-01 Section 2.5; G-52); the issue #590 live result (264 sessions, 263 `could not determine`) is a recorded report, not re-run | issue #590; `adapter.py:224`; `probes.py:214`; `orca_term.py:17-21` |
| Design package | U-24, U-25, U-27, U-28, U-29 | `QA.md:9` "19 tests passed" and the gallery DOM test not run; `sources.json` E01-E04 against the installed Orca; the DejaVu font path; checked-in artifacts against the current `render.py`; README line 44 "previous prototype files are preserved unchanged" | `.dev/design/orca-observer-20261106/` |

**C. Open gaps and Gate 1 corrections carried into the synthesis** (facts; not tagged UNVERIFIED above)

| Subject | IDs | Fact |
|---|---|---|
| Scope of "no DEFECT-CANDIDATE" | G-01 (resolved by GF-1), M-1 | Files 01 and 02 mean: R2/R3 live path wired. Use: "R2/R3 live path wired; fixture replay of the question ledger and Decision Desk is refused (D-1, DEFECT-CANDIDATE)" |
| Observer limits | G-02 to G-05, G-08, G-09, G-31 | Questions only for the Run its terminal holds (accepted); `counts` schema risk; unbounded row retention; 6 parsed fields exported nowhere with no stated reason; the pass record names one Run id while code accepts any valid id; no in-repo consumer; adapter tail and helpers not traced |
| Evidence limits | G-06, G-07, G-10, G-11, G-14, G-28, G-34 | `adapter-contract.md` and `release-gates.md` exist only on origin/master under `.dev/issues/409/bmad/spec-orca-observer/`; two gate tests cannot pass on the snapshot; PR file lists truncated at 100 (use #503: 545 files, #673: 2,831); 6.0.0 post-release artifacts, sweep internals, render internals and most of the orchestrator design were not read in full |
| Sweep | G-12, G-15 to G-19, G-39 | Stalled and fenced scope text cites review inputs, not a dated owner ruling (if the owner requires one the label reverts, no fact changes); `person_started True` never seen live; four pinned templates never called; cadence and read-before-acting are text duties; JSON omits Markdown-only fields; `report_path` unsanitized; fixed Linux version path; whether `CHANGELOG.md:170` covers three classes or one is a grammar question |
| Report skill | G-20 to G-25, G-32, G-48 to G-51 | `SKILL.md:194` "never ... starts or messages agents" is broader than `waker.py`; entry fields `kind`, `group`, `follow_up_state` never read; page server serves the whole coordinator folder; Google Fonts; hourly mode; `refresh` body and `reconcile_entries` untraced; `config.json` has 14 keys and no `CONFIG[...]` read of `clickup_email` or `clickup_user_id` was found (a fuller grep is needed before calling them unused); AWR join-key fields `tabId`, `leafId`, `handle`, `worktreePath`, `connected`, `lastOutputAt` (`sessions.py:323-330`); sanitizers described only as "control characters removed" |
| Design package | G-26 to G-30, G-33 | PR #673 file count unexplained; PNG parity not recorded; render and non-renderer file authorship not traced; live body alignment items undecided; `_publish` private |
| Count corrections | G-41 to G-47, M-2, M-4, M-7 to M-9, M-12 to M-14 | Use `wc -l` values (adapter 512, commands 524, probes 1477, parse 835, collector 361); `tests/observe` = 36 entries, 26 `test_*.py`, `test_session.py` 27 tests; AWR scripts total 5,777 lines (5,971 with SKILL.md), not 6,321; `_contract_for` docstring at `classify.py:575`; snapshot has 19 JSON fixtures (10 variants, 8 golden, `question-cap-100`); modal "would need" wording dropped; file 05 sections 19-29 lack Key Takeaways lines |
| Orchestrator overlap | G-52, M-3 | Three meanings of "waits on a person", two terminal-to-transcript joins, four sanitizers, three Orca wrappers exist only as scattered facts (assembled in 2.5) |

### 14.5 C8 DEFECT-CANDIDATE analysis

**The single rule (R-C8, GF-1 s2; it supersedes file 04's stricter test, which labelled stalled, fenced and `agent_wait_since` DEFECT-CANDIDATE).** A capability that a spec, design, skill, command or user doc names as shipped, enabled or required, and that has no producer, writer or reachable path at its runtime entrypoint, gets one label:

1. A cited spec-level or design-level text states, for that specific capability, that the shipped build does not deliver it (deferred, fixture-only, not observed, not observable, UNVERIFIED with a stated fallback outcome, or assigned to a named later piece of work): **KNOWN LIMIT (cited)**, citation printed. A report footnote, CHANGELOG line or user-guide line shows the limit is disclosed; by itself it is not the scope decision.
2. No such text: **DEFECT-CANDIDATE**. A text that only records an absence ("not built", "cannot run as written", "UNVERIFIED") does not meet step 1.
3. Either label carries the residual owner facts the citation does not settle; residual facts never change the label.
4. "Remediation task not created (read-only brief); flagged for the owner" is printed on every DEFECT-CANDIDATE and on every KNOWN LIMIT whose cited text names no tracked owner for its "until" condition.

Table of determinations (SPEC = `.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md` on origin/master; DESIGN = `docs/designs/orchestrator-mode.md`; ORCH = `docs/designs/orchestrator.md`):

| ID | Capability | Label | Declaring spec or design line | Code evidence | Cited decision or statement |
|---|---|---|---|---|---|
| C8-1 | Sweep `stalled (proved)` (rule 2 `orca_exit_proof`) | KNOWN LIMIT (cited) | SPEC:103 (FR-009), `commands/sweep.md:14`, WC:289 | `models.py:108-109`; `probes.py:471-515` never sets the inputs; `classify.py:196-200` | SPEC:231-232 ("stays fixture-only until a source mapping exists"); DESIGN:493, 636, 841, 877. Residual: no work item owns the mapping (U-40); review inputs, not a dated owner ruling (G-12). Impact in 14.1. Remediation task not created (read-only brief); flagged for the owner |
| C8-2 | Sweep `fenced` (rule 3) | KNOWN LIMIT (cited) | SPEC:251, `commands/sweep.md:14` | `models.py:109`; `classify.py:219-223` needs `present`; no producer | SPEC:251 "synthetic fixtures only in Phase 1", SPEC:231; DESIGN:493, 636, 841, 877. Residual: no "until" condition. Remediation task not created (read-only brief); flagged for the owner |
| C8-3 | Sweep `agent_wait_since` | KNOWN LIMIT (cited) | SPEC:238 | read at `classify.py:229-235`, `report.py:127-128`; set nowhere (`probes.py:481`) | SPEC:238; DESIGN:493, 494, 649, 1003. Residual: a non-null `agentWait` was never captured (U-11). Remediation task not created (read-only brief); flagged for the owner |
| C8-4 | `Safe to close` never `yes` | KNOWN LIMIT (cited) | SPEC:106 (FR-012) | `classify.py:479-504`: no branch returns `yes` | SPEC:106, 111, 167, 274; DESIGN:794. Only Phase 2 `/sc:close` (SPEC:75, 208) is named later; no `yes` source stated. Flagged for the owner |
| C8-5 | `Removable` never `yes` | KNOWN LIMIT (cited) | SPEC:106 | `classify.py:455-476`; `REASON_NOT_OBSERVABLE` (:88-90) | SPEC:274, 338; DESIGN:795. No later work named. Flagged for the owner |
| C8-6 | Living-report entry writer `superclaude orchestrator report-entry` | KNOWN LIMIT (cited), sequenced to PR B | `SKILL.md:14-16, 115-116`; `common.py:133-137` | no code outside tests writes `orchestrated/*.json`; `superclaude orchestrator` absent from `cli/` and `main.py`; `refs/settle.md:99` | ORCH:3 (owner ruling 37, 2026-11-19), 510, 791, 1020, 1021, 1041; closeout handles absence under D10 (`sc-closeout.md:66, 368`). Residual: skill text [CODE-CONTRADICTED] (CC-03); no interim behaviour stated (G-37); if the owner holds that a PR-sequencing line is not a scope decision the label becomes DEFECT-CANDIDATE with no fact changed (G-35). Remediation task not created (read-only brief); flagged for the owner |
| C8-7 | `orchestrator_repo` route to the state folder | KNOWN LIMIT (cited), sequenced to PR A | `SKILL.md:14`; `common.py:25` | master poll rejects the key (`cycle.py:216-220`) | ORCH:372, 374, 1018; PR A (#686) open. Residual: who sets the key is unverified (U-17); the [CODE-CONTRADICTED] tag stands (CC-02). Flagged for the owner |
| C8-8 | Answering a "Needs you" session entry (`prefs.py answer <run> <session url> session`) | **DEFECT-CANDIDATE** | `SKILL.md:172`; `SKILL.md:22` ("An unanswered 'Needs you' entry stays until Clay answers it") | `prefs.check_url` accepts only GitHub and ClickUp urls (`prefs.py:20, 30-32`), so `orca://session/<id>` exits "not an item URL"; `render.still_waiting` drops an entry only when its url is in `answered_since` (`render.py:339, 347`); also [CODE-CONTRADICTED] | none found. Remediation task not created (read-only brief); flagged for the owner |
| C8-9 | D-1: fixture replay of the question ledger and Decision Desk through `superclaude observe --fixture` | **DEFECT-CANDIDATE** | `SPEC.md:32` (CAP-1), `release-gates.md:9` (R0), `acceptance-tests.md:25` (AC-3, T7) under `.dev/issues/409/bmad/spec-orca-observer/` | `commands.py:77-78, 183-188, 414` refuse `--questions` with `--fixture` (exit 2); `FixtureSource.read_questions` always returns FAILED `no-question-fixture` (`collector.py:125-129`); only test hit `test_collector.py:675` | none found. The only text, `acceptance-tests.md:25` ("T7 cannot run as written"), records an absence and does not state the build is meant not to replay question fixtures; no spec line adopts the refusal; five owner records searched contain nothing on fixtures (G-36). Scope: observer `--fixture` path only; live `--questions` is wired. Question for the owner (fact, not a recommendation): is fixture replay through `superclaude observe --fixture` still wanted, or is the fake-runner test route the accepted substitute? Remediation task not created (read-only brief); flagged for the owner |

Checked and not raised as candidates (GF-1, GF-3, GF-4, GF-5): observer live R2 and R3, snapshot and `--once` are wired (both gate constants True, chain traced from the click option to the Orca read). The orchestrator design is a proposal ("It holds no implementation code", DESIGN:3), so its unbuilt `/sc:orchestrator`, verbs and contract section are not named as shipped. The missing `report-entry` verb is named in `check.py:77` (docstring) and `common.py:136` (comment) and called only by `settle.sh:1037-1042` (probe at :1037, call at :1042, ends `ENTRY escalated why=surface_absent`); that one caller is covered by decision D10. WC-16 versus the orchestrator design is an open question of scope, not a defect (U-35); no on-record decision says the orchestrator is exempt from WC-16 or covered; flagged for the owner; remediation task not created (read-only brief). The design package pipeline has a writing call for every documented output (no candidate); `--width` is ignored in export mode, `test_export_manifest` does not check `.mono.png`, the contact sheet, the gallery or the hash, and batch 2 rewrites the root `fixture.json` and `scenarios/` (facts, not defects). Declared Phase 1 limits with cited text (Ready-Task creator, remote hosts, Orca messages) and package-only designs not adopted by the observer (hold/pause, heartbeat classification, secret redaction, superseded attempts) are not named as shipped in the observer.

### 14.6 Process note (write boundary)

Research file 03 (line 10) records that one scratch copy of the SPEC was written to `/tmp` during reading and deleted again: a breach of the read-only write boundary with no residue (M-11, G-45). It is surfaced here for the owner. GF-1 states it wrote no scratch copy and read the SPEC with `git show ... | cat -n` only.

## 15. Verification & Accuracy

### 15.1 Verification Log

| Date | Verified By | Code Version / Commit | Sections Verified | Issues Found |
|---|---|---|---|---|
| 2026-11-20 | synthesis agent (Doc Analyst role) over research files 01-06, GF-1 to GF-5, `gaps-and-questions.md` | code: origin/master 61ac2c2e6 (read-only export); design package: docs-branch commit 495eb96d1 | 12, 13, 14, 16 and Appendix against the research files; code re-read this pass limited to `sweep/probes.py:40-63`, `sweep/report.py:50-71`, `observe/export.py:22-48` (skeleton literals) | 134 tracked items: 40 UNVERIFIED, 5 CODE-CONTRADICTED, 35 STALE DOC, 2 DEFECT-CANDIDATE, 52 GAP (all in 14.4 and 14.5). No tests, Orca, `gh` or renderer were run; test counts are counts of definitions |

Trust levels: [CODE-VERIFIED] statements come from research files that read the code; everything under UNVERIFIED in 14.4 stays UNVERIFIED. Research files 01-06 each carry their own date (2026-11-20).

### 15.2 Spot-Check Protocol

1. **File existence check:** every path in Sections 12-14 exists at origin/master 61ac2c2e6, for example `src/superclaude/cli/{observe,sweep}/`, `src/superclaude/skills/agent-work-report/scripts/`, `tests/{observe,sweep}/`, `docs/designs/orchestrator-mode.md`, `docs/designs/orchestrator.md`. Paths under `.dev/` exist only on origin/master (`git show origin/master:<path>`), the design package only at 495eb96d1 or via PR #503.
2. **Export verification:** check 3-5 signatures from the Public Interface blocks of Section 5 against the source: `classify` (`classify.py:369`), `collect` (`probes.py:1322`), `build_view` (`view.py:968`), observer `render` (`render.py:1449`), `Collector.__init__` (`collector.py:135`), and the `RULES` tuple of nine `Rule` entries (`classify.py:345-355`).
3. **State shape check:** the document carries no client-state section. If the assembled document adds one, compare it with `Session` (`view.py:151-168`) and `CycleResult` (`collector.py:37-68`).
4. **Component tree check:** if the assembled document carries one, compare it with the width-class layouts of `render.py` (`LAYOUTS`, `_columns`, `_desk_widths`).
5. **Convention check:** verify 2-3 conventions from Section 12 in recent changes, for example: the forbidden-prefix set only grows (`test_adapter.py:178-192`); the rule order pin (`test_classify.py:378-379`); the closed snapshot schema (`snapshot.schema.json:6` and `test_snapshot_schema.py:59-73`).

---

## 16. Glossary

| Term | Definition |
|---|---|
| Observer | `superclaude observe` (`src/superclaude/cli/observe/`): read-only terminal view and record of Orca `worker-list` rows, on master since PR #503 (2026-11-11), registered at `main.py:590-592`. Python with Rich |
| Sweep | `superclaude sweep run` and `/sc:sweep` (`src/superclaude/cli/sweep/`): read-only snapshot of a Run, its worktrees and person-started sessions; writes one dated report under `.dev/sweeps/` and prints JSON v1; recommends nothing |
| WC-16 | Rule "Coordinator loop" at `core/WORKER-CONTRACT.md:287-289`: the coordinator runs `/sc:sweep` on every wake, at most once every 5 minutes, beside "The sweep." (WC:110) |
| WC-10 | Contract rule on stall proofs: restart only on Orca's positive proofs; a missing heartbeat is absence, not death (`WORKER-CONTRACT.md:46, 157`) |
| "The sweep." | The coordinator's own liveness pass (WC:110): one `worker-list`, one `worktree ps --agent-wait`, one `stat` per contract path; distinct from `/sc:sweep` |
| worker-list | Orca `orchestration worker-list`: the observer's source (31 keys read); the sweep's per-Run read |
| Run, Dispatch | Orca orchestration Run (`run_<12 hex>`) and the Dispatch of one worker (`ctx_<12 hex>`, field `dispatchId`) |
| Phase 1 | The first sweep release; its limits are printed in the report (SPEC, DESIGN) |
| R0, R1, R2, R3 | Observer release stages: R0 synthetic fixture renders; R1 live worker-list ledger, `--once` and snapshot (it records the redacted golden samples); R2 question read (`--questions`); R3 link and Decision Desk. R4 (remote fleet) is "Not established" |
| Decision Desk | R3 observer pane for one selected question, built only with `--questions` and the link on; joins the question's verified `dispatch_id` to a collected row; screen only; no key acts on a question |
| Orchestrator | Designed, unbuilt: "a standing-grant coordinator and not a worker" (`docs/designs/orchestrator.md`; DESIGN:799); `/sc:orchestrator` and `superclaude orchestrator` do not exist |
| Coordinator | Contract role: "an Orca coordinator session the person opened" (WC:70) |
| agent-work-report (AWR) | Skill in `src/superclaude/skills/agent-work-report/` (PR #684): 15-step report over GitHub, ClickUp and Orca sessions, plus the living report |
| PR A, B, C, D, P | A #686 poll wakes the orchestrator (open); B orchestrator skill and verbs (no PR); C #684 report skill and living report (merged); D #682 plan-approval retirement (merged); P #690 `/sc:issue --plan` (open) |
| SPEC | `.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md` on origin/master (653 lines) |
| C8 | The brief's rule for capabilities named in scope but not reachable at the runtime entrypoint; applied as R-C8 (14.5) |
| KNOWN LIMIT / DEFECT-CANDIDATE | R-C8 labels: cited text says the build does not deliver the capability / no such text |

---

## Appendix: Document Provenance

This is not a consolidation of the research; it is the provenance of Sections 12-16. All code claims trace to origin/master 61ac2c2e6 as read by the research agents; design-package claims trace to commit 495eb96d1. No unification between the tools is recommended or implied.

| Source | Contribution to this part |
|---|---|
| Scope files `scope/01-observe.md`, `02-sweep.md`, `03-agent-work-report.md`, `04-dashboard-design.md` | Starting map only (verify, do not copy); `scope/04` has two wrong line cites (SD-29) |
| Research 01 `01-observe-data-contract.md`, 02 `02-observe-interaction-gates-docs.md` | Observer: argv guard, parse and merge, collector, STALE, snapshot schema versus export, fixtures, error codes, non-acknowledging read verdict, key map, width classes, theme and sanitizer, R2/R3 wiring, tests, consumers, docs versus code (12, 13.1 C and D, 13.2, 14.1, 14.4) |
| Research 03 `03-sweep-classifier-joins.md`, 04 `04-sweep-readside-wc16.md` | Sweep: nine rules, eight classes, joins, producer search, allowlists, budgets, git guard, publish, report sections, JSON v1, sanitizer, WC-16 chain (12.1, 12.2, 13.1 A and B, 13.2, 14.1, 14.5); 03 records the scratch-copy note (14.6); 04's stalled, fenced and `agent_wait_since` labels are superseded by GF-1 |
| Research 05 `05-agent-work-report-living-report.md`, 06 `06-dashboard-design-vs-observer-gaps.md` | Report skill: scripts, gate, entry-file contract, built-versus-designed table, PR state (12, 13.1 E, 14.1, 14.4); design package, contradictions C1-C8 settled against live sources, D-1 (14.4 A, 14.5) |
| GF-1 `gapfill-c1-GF1-c8-reconciliation.md`, GF-2 `gapfill-c1-GF2-commands-md-claim.md`, GF-3 `gapfill-c1-GF3-orchestrator-design-overlap.md`, GF-4 `gapfill-c1-GF4-public-entry-points.md`, GF-5 `gapfill-c1-GF5-package-pipeline.md` | GF-1: rule R-C8 and every C8 label (authority for 14.5); GF-2: what `CHANGELOG.md:170`, `commands.md:619` and `:620` each say (14.4 A); GF-3: orchestrator design versus the tools, verbs, FR-9, contract edits, PR chain (13.1, 14.4); GF-4: entry-point signatures and extension contracts (13.1); GF-5: design package render pipeline and tests (14.4, 14.5) |
| `gaps-and-questions.md`; Gate 1 `qa/qa-research-consolidated-findings.md` | The 134-row register behind Section 14; blocking findings GF-1 to GF-5 (answered by the gap-fill files) and minor findings M-1 to M-17 (14.4 C) |

