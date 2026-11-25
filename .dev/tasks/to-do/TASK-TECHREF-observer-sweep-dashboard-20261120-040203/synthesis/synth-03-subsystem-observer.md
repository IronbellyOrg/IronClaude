# Synthesis 03: Observer subsystem (template Sections 5.1 and 5.2)

> **Sources:** `research/01-observe-data-contract.md` (R01), `research/02-observe-interaction-gates-docs.md` (R02), `research/gapfill-c1-GF1-c8-reconciliation.md` (GF1), `research/gapfill-c1-GF4-public-entry-points.md` (GF4), `gaps-and-questions.md`, `qa/qa-research-consolidated-findings.md`, all under `/home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-observer-sweep-dashboard-20261120-040203/`. Template read first: `/home/coder/workspaces/IronClaude/.claude/templates/documents/technical_reference_template.md`.
> **Paths:** code paths are relative to the repo root at origin/master 61ac2c2e6; observer code lives in `src/superclaude/cli/observe/` (written `.../`). Nothing was run; facts come from the research files only.
> **Tags:** [CODE-VERIFIED] read in code or pinned by a test; [UNVERIFIED] not settled by code, tests or fixtures; doc-sourced claims are marked "(doc)". GF1 and GF4 supersede R01/R02 where they differ. Counts use the corrected values (QA M-4, M-7): tests/observe has 36 entries of which 26 are `test_*.py`; `test_session.py` has 27 tests.

---

### 5.1 Observer data contract (what it reads from Orca, what it emits)

**Purpose:** `superclaude observe` reads Orca's worker list (and, for one named Run, its question messages) through one read-only edge and keeps a ledger in memory. It emits a plain-text record and a closed JSON snapshot (schema version 1, "PROPOSED, not an Orca contract"). This subsection covers what is read, how it is validated and merged, and what is written.

**Key Files:**

| File | Purpose |
|------|---------|
| `.../adapter.py` | Only observer module that imports `subprocess` (pinned, tests/observe/test_commands.py:585-601); three argv templates, forbidden prefixes, caps, `LiveSource` paging, kill and reap |
| `.../parse.py` | `UNKNOWN` sentinel (parse.py:43), the 31-key `_FIELDS`, `parse_page`, `parse_questions`, `merge`, fixture loader |
| `.../collector.py` | `Collector` (single-flight poll thread, backoff), `CycleResult`, `FixtureSource` |
| `.../questions.py` | `merge_questions` (retention bound 1,000), `window_is_full` (100) |
| `.../view.py` (data part) | `STALE_SECONDS = 45.0`, `source_state`, `_meta` -> `SnapshotMeta` (the bridge to export) |
| `.../export.py` | `snapshot_dict`, `snapshot_json`, `record_text`, `write_atomic`, `state_dir` |
| `.../snapshot.schema.json` | Draft-07 closed schema, `schemaVersion` const 1 |
| `.../fixtures/` | 19 JSON files: 10 synthetic variants, 8 golden (4 worker-list, 4 question), `question-cap-100` |
| `src/superclaude/cli/install_user_setup.py:247-270` | `_find_orca`, the discovery probe the observer borrows |
| `tests/observe/test_{adapter,parse,collector,questions,export,snapshot_schema,golden_contract}.py` | Pin this contract |

**How It Works:**

```
orca skills list --json            (discovery, once per LiveSource; _find_orca)
  -> LiveSource.read_pages         (worker-list, 100 per page, <=5 calls; <=4 when questions are on)
  [+ LiveSource.read_questions     (one: check --all --types question --run <id> --json)]
  -> parse_page / parse_questions  (strict envelope, lenient rows, sanitized text)
  -> merge / merge_questions       (rows kept across cycles; questions kept to 1,000)
  -> Collector publishes one immutable CycleResult
  -> build_view (adds STALE, order, display text) -> screen | record_text | snapshot_json
```

*Allowed argv (after the binary).* Argv is a list, no shell; `assert_allowed` runs inside both builders and refuses anything else.

| # | Argv | Defined / checked | Notes |
|---|------|-------------------|-------|
| 1 | `skills list --json` | `DISCOVERY_TEMPLATE` adapter.py:30; exact match :148-149 | Run only by `_find_orca`; `LiveSource` never builds it |
| 2 | `orchestration worker-list --json --limit 100 [--run <id>] [--cursor <c>]` | `build_argv` adapter.py:173-183 | Pairs in that order, each at most once; `--limit 100` fixed |
| 3 | `orchestration check --all --types question --run <id> --json` (exactly 8 tokens) | `build_question_argv` :186-190; `_is_question_shape` :111-118 | Run id mandatory; only `read_questions` builds it |

Free values: run id must match `^[A-Za-z0-9_][A-Za-z0-9_.:-]{0,127}$` and a cursor must be a non-empty str with no leading `-`, no NUL, at most 2048 UTF-8 bytes; both limits are commented PROPOSED, not Orca formats (adapter.py:52-55, 92-108) [UNVERIFIED against Orca].

*Forbidden tokens.* `FORBIDDEN_PREFIXES` (adapter.py:34-50) holds 13 prefixes: `check`, `--ack`, `--wait`, `--retry-request`, `--peek`, `dispatch`, `inbox`, `run-use`, `run-create`, `send`, `ask`, `reply`, `reset`. They match by `startswith` at every verb and flag position, never against run or cursor values. In the question shape token indexes 1, 4, 6 (`check`, `question`, run id) are exempt, so `check` is legal only there, and `--wait/--ack/--peek/--retry-request` fail even there. The set may grow but not shrink: test_adapter.py:178-192 asserts a superset of the 13 [CODE-VERIFIED].

*Limits.*

| Limit | Value | Where |
|-------|-------|-------|
| Per-call timeout | 10.0 s; comment "UNVERIFIED until the first permitted live read measures it" (possibly stale, SD-02) | adapter.py:60-62 |
| stdout / stderr / kill | 8 MiB, process group SIGKILLed on overflow; first 2 KiB of stderr kept; 2 s kill grace | adapter.py:58-63, 196-209 |
| Calls per cycle | 5 worker-list (a default argument of `read_pages`, so a caller can override it); 4 + 1 question call when questions are on. Derived, not in code (R01 s12): 500 / 400 rows per cycle; the live sample total was 428, so a questions-on cycle ends PARTIAL | adapter.py:57; collector.py:32-34, 273 |
| Interval, budget, backoff | 15 s wait between cycles, 15 s cycle budget; failed first page doubles the wait 15 -> 30 -> 60 s, any parsed page resets it; 5 s join on stop | collector.py:28-34, 306, 321 |
| Questions | 100-row read window (exactly 100 = "window full"); 1,000 retained, oldest by created time evicted | questions.py:21-22, 125-129 |
| STALE | 45 s on the monotonic clock, computed in `view.py`, never stored by the collector | view.py:33-35, 456-463 |

*Parsing and merging.*
- **Strict envelope:** `ShapeError` (cycle FAILED `shape`) unless `result` is an object, `result.workers` a list, `result.page` an object and `result.page.hasMore` a real bool (parse.py:365-407). **Lenient rows:** a non-object worker entry is counted (`malformed_rows`) and skipped; missing or odd fields become `UNKNOWN` and are listed in `absent_fields`.
- **31 keys read** (`_FIELDS` parse.py:58-90). Any other key is counted in `unrecognised_keys` and its name and value are dropped.
- **`UNKNOWN`** is one singleton, distinct from None/0/False/"" and surviving copy and pickle; JSON null and an absent key both give it. Only export.py turns it into the string "UNKNOWN".
- **Identity** is `(namespace, dispatchId)`; the namespace is `os.path.realpath` of the Orca binary (observer-derived, adapter.py:378-381); a blank `dispatchId` makes an anonymous row (flag `identity unknown`); there is no cross-namespace merge.
- **Merge** (pure, parse.py:654-744): same identity inside a cycle is deduplicated (newer timestamp wins on like fields, else first kept with flag `order unknown`); across cycles an older timestamp never overwrites a newer one (flag `conflict (time went back)`); a row missing from a cycle stays with `reobserved=False`. Rows are never deleted for absence and the kept set has no cap (derived: memory only grows, untested, G-04).
- **STALE:** `source_state` passes `NOT_AVAILABLE`, `NOT_POLLED`, `FAILED` through; `OK` or `PARTIAL` becomes `STALE` at 45 s or with no success, else `OK`. So a `PARTIAL` cycle shows as `OK` and a `FAILED` one never shows STALE. Snapshot `source.status`: OK, STALE, FAILED -> ERROR, anything else -> UNKNOWN (view.py:667).
- **Collector:** `run_once` holds one cycle lock; one daemon thread `observe-collector`; it ends for good only when no Orca was validated. A failed first page keeps the last good rows; a question-read failure never touches backoff or rows.
- **Questions:** keyed `(Run, message.id)`, nothing is ever closed (no closure source). A question missing from a later good read stays, marked `no longer in source window`. Documented limit (questions.py:9-12): `check --all` rows carry no read/acknowledged marker, so a handled question is listed as open while Orca still returns it.

*Error and source codes.*

| Code | Raised when | Effect on the cycle |
|------|-------------|---------------------|
| `not-found` | `_find_orca` validated no Orca (adapter.py:403, 479; collector.py:261) | `NOT_AVAILABLE`; polling thread ends |
| `timeout` | 10 s call limit, or process lingers after stdout closes (adapter.py:296-305, 422-430) | FAILED on page 1, PARTIAL after |
| `overrun` | 15 s cycle budget spent or source cancelled (adapter.py:409-411; collector.py:213) | same; questions: FAILED |
| `output-cap`, `spawn-error`, `exit:<n>` | stdout over 8 MiB; binary cannot start; non-zero exit | same |
| `json` | stdout not decodable (deep nesting included), or `ok:false` with an unlisted error code | same; default code |
| `shape` | strict envelope check fails (parse.py:369-380, 528-533) | FAILED on page 1, PARTIAL later |
| `cursor-rejected`, `cursor-stalled`, `empty-page` | cursor refused (the only `ArgvRejected` that becomes a cycle code) or not a string; `hasMore` with missing, empty or reused cursor; zero workers while `page.total` > 0 | PARTIAL |
| `consumer-fenced`, `no-active-terminal` | Orca envelope errors `consumer_fenced`, `no_active_terminal` on the question read (adapter.py:66-69, 506-507) | question source FAILED; ledger unchanged, questions kept, no backoff |
| `no-question-fixture` | `--fixture` source has no messages (collector.py:129) | question source FAILED |

*Snapshot schema versus code.*
- **Match:** every key `snapshot_dict`, `_row_dict` and `_questions_dict` write is declared in the schema, which is closed (`additionalProperties: false`) on root, producer, source, page, collection, questions, items, row, stage, liveness, evidence; the code adds nothing [CODE-VERIFIED]. "Additive-only" is a stated policy in the schema description, not enforced by the file. `SCHEMA_VERSION = 1` (export.py:20).
- **Dropped (collected, absent from the JSON):** 11 of the 31 source attributes: all 7 `resource.*` (id, ownershipState, releaseState, worktreeId, ownerDispatchId, originDispatchId, recoveryAttemptCount), `workspace.id`/`.kind`, `stage.activity`/`.detail`. 20 are exported (19 text fields plus `evidence.durable` as given). Also dropped: row bookkeeping and every flag except `order unknown`, page `warnings`, coverage counters, `mode`, `fixture_variant`, `diagnostic`; for questions `subject`, handles, `priority`, `thread_id`, `ask`, `dispatch_id`, `link`; `body`, `to_handle`, `payload` are never kept at all. Tests pin only some drops as privacy exclusions (stage detail and activity, worktreeId, ownershipState, releaseState, warnings, nextCursor); the reason for the other drops is not stated [UNVERIFIED, G-05].
- **Row shape:** flattened (`nextAction.kind` -> `nextAction`, `provider.id` -> `provider`, `host.kind/id` -> `hostKind/hostId`); numbers and booleans become strings via `json.dumps` except `evidence.durable`; optional `orderUnknown`, `notReobserved`, `absentFields`; rows newest first by `liveness.observedAt`, untimed last; every collected row is listed, historical included.
- **Questions group:** ids, `createdAt`, `ageSeconds`, `inWindow` and counts; `closureEvidence` is always "unavailable". The plain-text record differs: it also carries each question's subject (view.py:811; export.py:103-111), never the payload text.
- **Risk:** the schema limits `counts` values to scalars (schema line 50) but the parser keeps nested JSON to depth 6 (parse.py:277-290); no test feeds nested counts [UNVERIFIED].

*Where it writes.* State dir is `$XDG_STATE_HOME/superclaude/observe` when absolute, else `~/.local/state/superclaude/observe` (export.py:236-244). `snapshot.json` has a fixed name; `observe-<generatedAt, ':' -> '-'>.txt` records are written only by the `e` key. `write_atomic`: `mkdir` leaf mode 0700 (umask applies, unrun), `mkstemp` in the same dir (0600), write, fsync, `os.replace`, temp unlinked on failure [CODE-VERIFIED]. The snapshot is overwritten each cycle with no history: one write per published cycle, failed cycles included, when live or `--snapshot` is given; `--once` writes only with `--snapshot`; fixture runs write nothing without it. Records accumulate (no pruning; two exports in one second share a name).

*Is the question read non-acknowledging? [UNVERIFIED].* Code, tests and fixtures are consistent with it but cannot prove it: argv never carries `--ack/--wait/--peek/--retry-request`, only the `--all` form; every recorded reply has `result.acknowledged: null` and rows `delivered_at: null`, and the parser reads neither. Design records (doc, not re-run): RESEARCH-REPORT-phase2-gate.md 2.2 tested it as the owner of a probe Run only; release-gates.md says non-owner non-consumption is UNVERIFIED; the owner accepted that on 2026-11-12. A non-owner read is fenced today anyway. **Contradiction:** R02 section 6.2 says the gate record "resolves" the `check`-without-`--peek` question; R01 section 10 keeps UNVERIFIED because the evidence covers the owner-bound reader on a probe Run only. R01 has the stronger evidence, so UNVERIFIED stands. Orca's `check --all` source and `--help` were not read.

*Discovery.* `_find_orca` tries `orca-ide` then `orca` via `shutil.which`, runs `skills list --json` (timeout 10 s) and accepts exit 0 with a topic named `orca-cli` (install_user_setup.py:247-270) [CODE-VERIFIED]. The `any(...)` over `topics` sits outside the `try`, `LiveSource.discover` has no handler and `_loop` has none, so an odd `topics` shape would end the polling thread silently [UNVERIFIED: read, not run; no covering observer test found].

**Public Interface** (key signatures only):
- `LiveSource.read_pages(clock, budget_deadline, run_id=None, max_calls=MAX_CALLS_PER_CYCLE) -> SourceResult` (adapter.py:395); `read_questions(clock, budget_deadline, run_id) -> SourceResult` (:469); `SourceResult(state, pages, code, diagnostic, capped, calls)`.
- `build_argv(orca, run_id=None, cursor=None)`, `build_question_argv(orca, run_id)`, `assert_allowed(argv)` (raises `ArgvRejected`), `check_run_id`, `check_cursor`; `parse_page`, `parse_questions`, `merge(previous, pages, stopped_by_cap, stopped_by_error) -> Snapshot`, `merge_questions(...)`.
- `Collector(source, clock, interval=15.0, budget=15.0, max_backoff=60.0, run_id=None, questions=False, link=False)` with `run_once() -> CycleResult`, `latest()`, `start()`, `stop()` (collector.py:135-145); `CycleSource` protocol (`mode`, `variant`, `available`, `namespace`, `read_pages`, `read_questions`).
- `snapshot_dict(view)`, `snapshot_json(view)`, `record_text(view)`, `write_atomic(path, text)`, `state_dir()`.

**Dependencies:**

| Depends On | Type | Description |
|------------|------|-------------|
| Orca CLI (`orca-ide`, then `orca`) | Subprocess | Only through adapter.py, three argv shapes |
| `_find_orca` | Import | Discovery; the observer allow-list is not applied to this probe (it builds its own argv) |
| `view.py` `source_state`, `_meta`, `SnapshotMeta` | Import | export reads only `view.meta`, `view.all_rows`, `view.questions` |

**Consumers:**

| Used By | How |
|---------|-----|
| `.../commands.py` (`run_once`, `run_loop`) | Builds the `Collector`, writes snapshot and record files |
| `tests/observe` | Validate snapshots against the schema (Draft7Validator in test_commands.py and test_snapshot_schema.py; shared validator set up in `conftest.py:17, 32`) |
| Anything else | None found: no module outside `observe/` imports it except the main.py registration; no agent, command or skill names it. `snapshot.json` in `agent-work-report` is another producer, other schema, other directory |

**Conventions & Patterns:**
- Add an Orca call only by changing the template constants, `assert_allowed` and the pinned tests; add forbidden prefixes freely, never remove one (the test is a floor). Keep `subprocess` imports in adapter.py only.
- Missing values are `UNKNOWN`, never None, 0, False or "". STALE is derived in `view.py` from the injected clock; the collector stores no STALE flag.
- Exporting a new worker-row field is a four-place edit: `Row` and `_FIELDS` in parse.py, `_TEXT_FIELDS` or `_ANY_FIELDS` in export.py, `definitions.row.properties` in the schema, tests (GF4 5.3). An unconditional row key changes the questions-off bytes pinned by `golden_release1_records.json` ("never regenerated", test_render.py:677-695); a conditional key does not while its condition is false.
- Treat questions as "seen, not resolved"; never present `open` as unhandled.

<!-- END 5.1 -->

---

### 5.2 Observer interaction layer, exit codes and release gates

**Purpose:** Describes how a person runs and drives the observer (one click group, seven flags, a key map, three width layouts, the Decision Desk), what it returns to the shell, which constants gate the live question features, and which release stage is built. It is read-only toward Orca: no key and no option writes to it.

**Key Files:**

| File | Purpose |
|------|---------|
| `.../commands.py` | Click group `observe`, `Options`, `Deps`, `execute`, `run_once`, `run_interactive`, `run_loop`, gate constants (:67, :70) |
| `.../view.py` | `build_view`, `apply_cycle`, `apply_key` (what each key means, :1246-1300), `Session`, `View` |
| `.../keys.py` | POSIX key decoder (termios, cbreak) and signal handlers; imported lazily |
| `.../terminal.py`, `.../render.py`, `.../theme.py`, `.../sanitize.py` | Width classes, colour and ASCII policy, the only Rich `Console`; layouts, questions panel, Decision Desk; seven exact state words coloured (not a health verdict); escape stripping |
| `src/superclaude/cli/main.py:590-592` | Registers `observe_group` as `observe` |
| `docs/user-guide/cli-groups.md:40-54`, `README.md:35,136` | The only user documentation |
| `.dev/issues/409/owner-pass-record-20261112.md`, `.dev/issues/409/bmad/spec-orca-observer/release-gates.md` | Gate records; on origin/master only, not in the docs-branch checkout |

**How It Works:**

*Command surface.* `superclaude observe` is a click group with no subcommands; with no flag it starts the interactive loop (commands.py:449-521).

| Flag | Behavior |
|------|----------|
| `--once` | Read once, print, exit (`run_once`) |
| `--width {160,116,80}` | Binds the layout; with `--once` prints the rendered screen instead of the record |
| `--ascii` | Forces ASCII (also on when the stream encoding is not UTF-8) |
| `--fixture <name>` | Replays a synthetic fixture; unknown name is a click usage error |
| `--run <id>` | One Run; without `--questions` it filters the worker-list call (`--run`) |
| `--snapshot <file>` | JSON snapshot path; interactive default is the state dir |
| `--questions` | Lists coordinator questions of the one `--run` Run; needs a live source; guarded by `QUESTION_GATE_PASSED` |

`execute` first applies `_question_refusal` (before any Orca call, discovery included), then routes to `run_once` or `run_interactive`. Interactive polls every 15 s, repaints when dirty or every 0.5 s, and writes one snapshot per cycle (see 5.1). `--once` prints `record_text` by default (plain, no ESC bytes when piped); a colour screen only when `--width` is given and stdout is a TTY.

*Exit codes.*

| Code | Condition (commands.py unless noted) |
|------|--------------------------------------|
| 0 | `--once` read printed; loop ended by `q`, by Ctrl-C (decoded key) or by SIGINT (keys.py:115-117). A failed Orca read is a view state, not an exit code |
| 1 | `--once` snapshot not writable (:264-268); render failure in the loop ("observe: display failed", :364-369); `--questions` with the gate False (:195-196, unreachable today, constant is True) |
| 2 | `--questions` with `--fixture`, without `--run`, or with a rejected run id (:187-194); interactive on win32 (:377-379) or with no terminal on stdin (:385-387); click usage errors (bad `--width`, `--fixture`, `--run`; click's own code) |
| 143, 129 | SIGTERM, SIGHUP while the key source holds the terminal (keys.py:119-125) |

*Key map* (`apply_key`, view.py:1246-1300; keys change the Session only, "there is no refresh key and none reaches Orca"). The decoder emits up, down, enter, escape, backspace, ctrl_c and text; left, right, Home, End, PgUp, PgDn are swallowed.

| Key | Effect |
|-----|--------|
| Ctrl-C (any focus), `q` (not in filter) | Quit |
| any key in filter focus | Types into the filter; Backspace deletes; Enter or Esc returns to list |
| Up/`k`, Down/`j` (list or inspector); `d` / `u` (inspector) | Move selection; scroll the inspector 3 lines |
| Enter (row selected); Esc (inspector) | Open the inspector; back to list |
| `/`; `h` | Filter (substring over eight cells); toggle historical (`released` or `retained`) rows |
| `e`; `m` | Export plain record to the state dir and show `exported <path>`; set the "changed since" baseline |
| `n` / `p`; Esc | Next / previous question (oldest first) and clear selection; only with link on and a question line present |

*Width layouts* (terminal.py:21-24, 82-89; below 80 columns "terminal too narrow (min 80)", below 8 rows "terminal too small (min 8 rows)", each with counts and the gap notice).

| Class | Ledger columns | Questions panel | Decision Desk |
|-------|----------------|-----------------|---------------|
| full (>=160, `--width 160`) | marker, dispatchId (<=48), run, workerState, status, nextAction.kind, alive, evidence age | layouts A, B, C tried in order | question pane over list on the left, evidence pane 80 wide on the right |
| line (116-159) | marker, kind, dispatchId, alive, status, age | A, B, C tried in order | question pane spans the width; evidence left, list 46 wide right |
| short (80-115) | marker, kind, dispatchId, alive, status, age | C only | three panes stacked |

Layout A = count strip + list + RETAIN CONTEXT pane, B drops RETAIN, C drops the strip; the first that shows at least 3 question rows wins. Questions win over the ledger on a short terminal. When the list is cut the oldest questions stay and the newer are reachable only by export (owner decision 2026-11-12, as the docstring records).

*Decision Desk (R3).* Built only with `--questions` and the link on (`DeskView`, `_desk` view.py:888-948). It needs a selected question; the join is exact: the question's verified payload `dispatch_id` against a collected row's `dispatchId`. Linked fields: dispatch, state, status, outcome, next action, liveness, evidence age, `resource.worktreeId` shown as "this session only". Unlinked: "affected scope unknown" plus the reason. If it does not fit, `decision desk hidden: terminal too short` goes in the list frame. No desk key acts on a question. Question text from the payload is screen-only (cut at 400 characters, at most 4 desk lines); it is never in the JSON snapshot and not in the record's question lines (the record keeps ids, ages and subject).

*Gates.* `QUESTION_GATE_PASSED = True` (commands.py:67, cites `.dev/issues/409/owner-pass-record-20261112.md`) and `QUESTION_LINK_PASSED = True` (:70, cites release-gates.md `QUESTION-LINK`) [CODE-VERIFIED on 61ac2c2e6]. `_questions_on` = option and gate 1; `_link_on` = questions on and gate 2. Tests pin both as True only with a cited, existing record (tests/observe/test_commands.py:754-779); the snapshot export omits `.dev/`, so those two tests read origin/master-only files (G-07). The gate records live in `.dev/issues/409/` on origin/master only. Provenance differs (doc): QUESTION-OBSERVATION has an owner-written record (accepts Q-1 FAIL: reads only from the terminal that holds the Run; non-owner non-consumption unverified; burst loss over 100 rows accepted); QUESTION-LINK is an agent-written status line recording the owner's chat "yes" of 2026-11-17 (release-gates.md:58); the on-screen-only text decision is also a recorded chat decision (PR #598). The record names Run `run_93bfa00cae2b`; the code accepts any valid `--run` (G-08). Whether the "four sample kinds" data-gate rule (release-gates.md:5) was met for messages is [UNVERIFIED] (U-06).

*Release stage* (release-gates.md is doc; "State" is checked against code).

| Stage | Content | State at origin/master 61ac2c2e6 |
|-------|---------|-----------------------------------|
| R0 | `--fixture` replay of 10 synthetic variants | Built; `--questions` with `--fixture` refused (D-1 below) |
| R1 | Live worker ledger, `--once`, snapshot | Built (PR #503); DIRECTION-SELECTED passed 2026-11-16 |
| R2 | `--questions`, one named Run | Built; live read enabled by PR #577 |
| R3 | Question text, link, Decision Desk | Built 2026-11-17 behind QUESTION-LINK (PR #592) |
| R4 and later | Remote fleet (`--include-remote`), closure evidence, history past 100 rows, admission, verification, cost, deep links, write-back | Not built; "Not established" in the gate table; write-back "never R1" |

Closure shows `unavailable (no source)`. What the docs lack: one section in `cli-groups.md` and two README lines; no CHANGELOG entry in [Unreleased], 6.1.0 or 6.0.0; no technical doc (the post-release report counts "13 source files"; Glob finds 14 `.py`, 13 without `fixtures/__init__.py`); no sysop guide (deferred, decision 6.6). Which tag first contained R2 and R3 is [UNVERIFIED] (U-08). `cli-groups.md:42` and the HELP say "no option maps to an Orca call"; `--run` and `--questions` do select which read argv is built (commands.py builds none) [CODE-CONTRADICTED, minor, CC-01].

*The six PRs* (state read with `gh pr view <n> --repo IronbellyOrg/IronClaude`; merge commits are ancestors of origin/master [CODE-VERIFIED via git]).

| PR | Title (short) | State, merged (UTC) | Content |
|----|---------------|---------------------|---------|
| #503 | release 1, `superclaude observe` | MERGED 2026-11-11 | R1 plus the design package; `gh` file list truncated at 100 (545 files per G-10) |
| #514 | release 2, questions for one named Run (live read off) | MERGED 2026-11-12 | `QUESTION_GATE_PASSED = False` at that merge; retention bounded at 1,000 |
| #577 | enable the live questions read, 11 cuts, record owner direction | MERGED 2026-11-17 | Owner pass record, live-test guide, decisions; 684 observe tests passed per body |
| #592 | question text, dispatch link, Decision Desk behind QUESTION-LINK | MERGED 2026-11-17 | collector, commands, export, parse, render, view plus tests; 762 observe tests per body |
| #598 | record: question text stays on screen only | MERGED 2026-11-17 | Docs only (release-gates.md) |
| #673 | visual parity at 160, 116 and 80 columns (#606) | MERGED 2026-11-19 | Rendering and design records; file list truncated (2,831 files per G-10) |

*C8 reachability.* Live R2 (`--questions`), R3 (link, Decision Desk), the snapshot and `--once` are wired from the click option through `Options` -> `_questions_on`/`_link_on` -> `Collector` -> `LiveSource.read_questions` (commands.py:173-180, 247-253, 388-395, 487-496; collector.py:205-245). The "no DEFECT-CANDIDATE" lines in R01 and R02 cover only these paths (GF1 section 4).
- **DEFECT-CANDIDATE D-1 (C8-9), fixture replay of the question ledger and Decision Desk.** `_question_refusal` exits 2 for `--questions --fixture` (commands.py:77-78, 183-188, 414); `FixtureSource.read_questions` always returns FAILED `no-question-fixture` (collector.py:125-129; only test hit test_collector.py:675). No cited scope decision; remediation task not created (read-only brief); flagged for the owner. Declaring lines (SPEC.md:32, release-gates.md:9, acceptance-tests.md:25) and the owner question are in 14.5.
**Public Interface** (key signatures only):
- `observe_group(ctx, once, width, ascii_mode, fixture, run_id, snapshot, questions)`; `Options` (frozen, seven fields); `execute(options, deps=None) -> int`; `run_loop(collector, keys, screen, clock, *, make_policy, directory, snapshot_file, write_snapshots) -> int`.
- `build_view(result, session, clock) -> View` (the only `View` constructor); `apply_cycle(session, result, clock) -> Session`; `apply_key(session, key, view, clock) -> tuple[Session, Effect]` (`Effect` = NONE, EXPORT, QUIT); `render(view, policy, message=None) -> Group`; `screen_lines(view, policy, message=None) -> list[str]`; `KeySource(fd=None)`.

**Dependencies:**

| Depends On | Type | Description |
|------------|------|-------------|
| 5.1 `Collector`, `export` | Import | Data and files |
| `click`, `rich` (`Live`, `Console`) | Import | Command line and screen; `Console` built only in terminal.py |
| `termios`, `tty` (POSIX) | Import, lazy | Only the interactive path; `--once` works with them blocked (test_commands.py:73-100) |

**Consumers:**

| Used By | How |
|---------|-----|
| A person at a terminal | `superclaude observe [flags]` |
| Tests | `tests/observe`: pure view and render, click and loop with fakes, real pty (`test_live_screen_pty.py`, `test_keys_spike.py`); `main.py:590-592` registers it (test_registration.py:59-71) |

**Conventions & Patterns:**
- A new panel: typed frozen dataclass, a builder returning None when off, a defaulted `View` field set by keyword in `build_view`, a literal in view.py (GF4 3.2). New data needs a new `CycleResult` field first.
- A new non-text key needs a name in `KEY_NAMES` (view.py:30) and a branch in `apply_key`; keys must only change the Session.
- Ledger columns come from `_columns` (render.py:480-568); vertical space is budgeted in `_compose`; the renderer takes only `(view, policy, message)`, never parses worker text as markup, and only terminal.py builds a Console.
- Keep the question text out of the record and snapshot; a link-off screen must stay byte-identical to the reference capture (PR #592).
- R02's "41 entries" and "29 tests" are superseded by 36 entries, 26 `test_*.py` files, 27 tests in `test_session.py`; `test_keys_spike.py:3` ("only module with a real pty") predates `test_live_screen_pty.py` (SD-05).

<!-- END 5.2 -->
