# Synthesis 04: Technical Reference sections 5.3 and 5.4 (sweep)

Inputs: `research/03-sweep-classifier-joins.md`, `research/04-sweep-readside-wc16.md`, `research/gapfill-c1-GF1` to `GF4` (GF5 concerns the design package, not the sweep), `gaps-and-questions.md`, `qa/qa-research-consolidated-findings.md`. Nothing was re-run; no source was re-read except wc -l counts and two line checks on the snapshot.
Paths are relative to origin/master 61ac2c2e6 (`/home/coder/.cache/ic-snap-20261120/master`) unless stated. `SPEC` = origin/master `.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md`; `DESIGN` = `docs/designs/orchestrator-mode.md`.
Authority: GF-1 (rule R-C8) supersedes file 04's DEFECT-CANDIDATE labels (file 03 read the SPEC; file 04 did not, so 03's evidence is stronger). Line counts below are `wc -l` values (file 04's 1478, 289 and 696 are one too high). Facts only; no unification recommendation.

---

### 5.3 Sweep Classifier and Joins

**Purpose:** Turn each Orca Dispatch row and each un-joined session transcript into one `SessionRow` with exactly one of 8 classes, using 9 ordered pure rules, then qualify it with join, transcript and source evidence. It never recommends an action; "could not determine" is the default for anything it cannot prove.

**Key Files:**

| File | Purpose |
|------|---------|
| `src/superclaude/cli/sweep/classify.py` (1009 lines) | `RULES` (345-355), `classify` (369), `classify_all` (880), joins (`_join_path_b` 609, `_guard` 728, `_person_origin` 760), `_contract_for` (570; docstring :575), `safe_to_close` (479), `removable` (455), `package_state` (423) |
| `src/superclaude/cli/sweep/models.py` (278) | `CLASSES` (50-59), `PACKAGE_STATES` (62-69), `SAFE_VALUES` (71), `OrcaObservation`, `SessionRow`, `Classification` (212) |
| `tests/sweep/test_classify.py` (1978) | In-memory builders `orca()`, `contract()`, `row()` (143-169); `RULE_NAMES` pin (378-379) |
| `tests/sweep/test_cli_contract.py`, `test_probes_allowlist.py` | The only readers of captured fixtures (rule 5 proof) |
| `tests/sweep/fixtures/` (21 entries) | 20 `captured-*.json` plus `SOURCES.md`; 5 exited workers captured 2026-11-11, `captured-worker-show-running.json` 2026-11-16 |

**How It Works:**

```
SweepInput -> classify_all: merge rows sharing a Dispatch id -> join each transcript (path A, else path B)
  -> _guard flags -> one SessionRow per Orca row + one per un-joined transcript (person_started via _person_origin)
  -> classify(row, ctx): RULES 1..9, first match wins -> note harvest -> unreadable transcript forces unknown
  -> classify_all: join/source flags force unknown -> lifecycle/health/result/freshness, counts, waiting_a/b
```

Terms: settled = `orca.outcome` in succeeded/partial/failed; STOP code = `E-...` token in contract `reason` plus `blocked_question`; Ruling halt = `E-HALT-QA` or `E-NO-RULING`; freeze code = any STOP code except `E-RESUME-NEEDED`.

| # | Rule | Class (kind) | Exact firing condition | Proving test | Fixture |
|---|------|--------------|------------------------|--------------|---------|
| 1 | `blocked_contract` | waiting on a person (a) | contract `blocked` and transcript not unreadable; then no Orca row needs a Ruling halt; Orca row settled, or `gate_policy == "report blocked"`, or Ruling halt matches; else declines (note "may be re-running" if live and policy is ask/None) | `test_classify.py:288-295, 728-760`; `test_cli_contract.py:1085-1115` | inline |
| 2 | `orca_exit_proof` | stalled (proved) | Orca row, `liveness_verdict == "exited"`, transcript not unreadable, `worker_done_seen is False`, `fenced_evidence == "absent"` | `:296-307, 581-624, 763-777` | inline only |
| 3 | `fenced` | fenced | Orca row and `fenced_evidence == "present"` | `:308`; `test_report.py:353` | inline only |
| 4 | `waiting_signal` | waiting (a) or (b) | (a) Orca `agent_wait` not None; (b) contract `failed` with a freeze code; (b) Orca `status == "ready"` Task row | `:309-319, 382-417, 476-485` | inline; `captured-task-list-ready.json` is an empty list |
| 5 | `working` | working | Orca row, `liveness_verdict == "live"`, `outcome == "in_progress"`, `agent_wait_present is True`, `agent_wait is None`; `dispatch.status` not tested | `:320, 444-485`; `test_cli_contract.py:1133-1169`; `test_probes_allowlist.py:1639-1651` | `captured-worker-show-running.json` (positive), `captured-worker-show-1.json` (exited, negative) |
| 6 | `finished` | finished | `orca.body_text` first line starts `guard refused:`, or Orca settled and a parsed contract with settled `worker_status`; note "partial: usable not yet judged" | `:321-328, 627-654, 785-806` | inline |
| 7 | `idle` | idle | `person_started True`, no Orca row, transcript readable, `last_activity <= now` and `< window_start` | `:329-337, 493-540, 957-968` | inline |
| 8 | `person_active` | person session (active) | `person_started True`, transcript readable, `last_activity >= window_start` (no check on Orca row or `<= now`) | `:338-346, 1734-1756` | inline |
| 9 | `fallback` | could not determine | always; evidence "no rule 1 to 8 matched (...)"; note "no contract read for this row" for a settled row without a contract | `:347, 581-654, 672-673` | inline |

Only rule 5 has a captured-fixture proof; the 5 captured tab-map files are read by no test (path-B tests use synthetic `entry()` objects). Rules 1 and 2 are called a second time by `classify` (378) only to harvest decline notes.

| Class (`models.CLASSES`) | Produced by | Prints in a live run today |
|--------------------------|-------------|----------------------------|
| waiting on a person | rules 1, 4 | Yes for contract and Task data; rule 4(a) needs a non-null `agentWait`, never captured |
| stalled (proved) | rule 2 only | No (no producer) |
| fenced | rule 3 only | No (no producer) |
| working | rule 5 only | Yes, since the 2026-11-16 capture |
| finished | rule 6 only | Yes, only when a contract was found for the row |
| idle | rule 7 only | Rarely: needs `person_started True` (below); counted as `historical`, `visible = total - historical` |
| person session (active) | rule 8 only | Same condition as idle |
| could not determine | rule 9 plus forcing | Yes: the common outcome |

**Could-not-determine forcing** (`_force_unknown`, 358-366; replaces the matched class, keeps its evidence): (B) `transcript_readable is False`, any rule; (C) a non-empty `forced` tuple from `classify_all`: path-A several-rows, path-B notes, duplicate Dispatch ids that disagree (`_merge_group` 512-525), or an `unscanned` source named `contract <dispatch>` or `transcript <path>` or containing "inconsistent"; (D) rule 9. The notes cell is the only place the three meanings (nothing proved, input unreadable, join ambiguous) differ. A transcript over 256 KiB joined by path B forces unknown ("session start not observable: transcript tail only", `test_classify.py:1405-1412`); a terminal Dispatch row without `completedAt` has no window (`:1385-1391`).

**Joins** (`classify_all` 880-1009):

| Step | Fact |
|------|------|
| Path A | `session_join == transcript session id`; one row joins, several rows give a forcing note. Tried first and independent of `JOIN_PATH`. Production `session_join` is `dispatch.assigneeHandle` (`term_<uuid>` captured); a production path-A join is UNVERIFIED |
| Path B (`JOIN_PATH = "B"`, 40) | tab-map keys (`file_name`, `terminal_handle`) of entries with the transcript's session id; needs a Dispatch window (`_window` 548-558), a transcript read from byte 0, and exactly one row whose window holds the first record (bounds inclusive) |
| `JOIN_PATH` | read in one place, `_guard` (745) |
| `_guard` | excludes `ready` Task rows; flags `origin` (5 list-incomplete notes), `unobservable`, `no_join`, `unmatched` and `earlier_pane` (path B: any considered row exists) |
| `person_started` (`_person_origin`) | True only if no origin note, no guard flag and no tab-map entry. Under path B, True needs a sweep with no non-ready Dispatch rows, a readable tab map and a complete worker list; with any Dispatch row present every un-joined transcript is None and prints could not determine. No live row of idle or person-active was found (UNVERIFIED) |
| `_contract_for` (570-591) | a contract attaches to an Orca row only if a report folder (`--report-dir/--output-dir/--output`) or a path named in the Task text identifies exactly one contract, or it is the only contract under the only row using that worktree; else None (so no rule 1, no finished, no frozen) |

**Safe to close, Removable, package states:**

| Item | Rule (all in `classify.py`) | Values it can print |
|------|-----------------------------|---------------------|
| `safe_to_close` (479-504) | terminal: no Orca row or unobserved gives could not determine; `retained` gives no; `reclaimable` + `release` gives could not determine ("result read not observable"); other gives no. Worktree part is `removable()` | no or could not determine; no branch returns `yes` |
| `removable` (455-476) | first of: uncommitted, unpushed or no upstream, `.dev/tasks` unsaved, frozen plan, a package in unfinished/archive-blocked/interrupted-archive/conflict, shared active package; then unreadable worktree; else could not determine ("report read, open PR and unmerged commits not observable") | no or could not determine; never `yes` |
| `package_state` (423-429) | `conflict` (id in to-do and done), `interrupted-archive` (marker), `archive-blocked` (to-do with `FINAL:` line), `unfinished` (to-do, no `FINAL:`), `archived` (done), `unknown`; first four block removal | proofs `test_classify.py:1770-1817`; shared packages `:1833-1871` |

**Phase 1 limits (facts, each with its cited on-record text; label KNOWN LIMIT (cited) per GF-1 rule R-C8):**

| Limit | Code fact | Cited scope text | Residual owner facts |
|-------|-----------|------------------|----------------------|
| `stalled (proved)` cannot fire | whole-snapshot grep for `worker_done_seen` and `fenced_evidence`: defaults `None` and `"unreadable"` (`models.py:108-109`), readers in `classify.py`, constructor arguments in tests only; `parse_worker_show` (`probes.py:471-515`) never sets them. Live exited rows get the note "Orca: exited; fenced evidence not readable" | SPEC:232 "stays fixture-only until a source mapping exists", SPEC:231, SPEC:103; DESIGN:493, :636, :841 (D7), :877 | No work item owns the "source mapping" (one `gh search`, not a scan); text is attributed to review inputs, not a dated owner ruling. Remediation task not created (read-only brief); flagged for the owner |
| `fenced` cannot fire | same missing producer; rule needs `"present"` | SPEC:251 "synthetic fixtures only in Phase 1", SPEC:231; DESIGN:493, :841 | No "until" condition named; WC-16 names the stalled behaviour, not `fenced`. Remediation task not created (read-only brief); flagged for the owner |
| `agent_wait_since` never set | `models.py:111-112`, `probes.py:481`; pinned `is None` (`test_probes_allowlist.py:1651, 1687`); a waiting row from `agentWait` alone has unknown age | SPEC:238 (UNVERIFIED field, "no `t`" gives unknown-age group); DESIGN:493, :494, :1003 | Non-null `agentWait` never captured (UNVERIFIED). Remediation task not created (read-only brief); flagged for the owner |
| `Safe to close` never `yes` | no branch returns `yes` | SPEC:106 (FR-012), :111, :167, :274; DESIGN:794 | Only the report footnote, CHANGELOG:171 and commands.md:621 say "never yes"; `commands/sweep.md:16` and `SKILL.md:66` do not. No tracked owner for an "until" condition: remediation task not created (read-only brief); flagged for the owner |
| `Removable` never `yes` | same | SPEC:106, :274, :338; DESIGN:795 | Missing sources (open PR, unmerged commits) named in SPEC:338; no later work named. Remediation task not created (read-only brief); flagged for the owner |

**Public Interface:**

```python
classify(row: SessionRow, ctx: SweepContext) -> Classification          # classify.py:369
classify_all(inp: SweepInput, ctx: SweepContext) -> SweepResult          # classify.py:880
Rule(name: str, match: Callable[[SessionRow, SweepContext], Classification | None])   # RULES: 9 entries
_classification(class_name, rule, evidence, waiting_kind=None, notes=()) -> Classification  # :130 (private)
safe_to_close(row, worktree: WorktreeState | None) -> SafeToClose; removable(worktree) -> tuple[str, str]
```

**Dependencies:**

| Depends On | Type | Description |
|------------|------|-------------|
| `probes.collect` output (`SweepInput`) | Data | Orca rows, contracts, transcript tails, tab map, worktrees, source rows |
| `SweepContext` (`now`, `window`, `window_start`) | Data | Only time source; rules do no file, process or clock access |
| `models.py` frozen dataclasses | Import | `CLASSES`, `SessionRow`, `Classification`, `PackageRecord` |

**Consumers:**

| Used By | How |
|---------|-----|
| `commands.py:269-271` | `probes.collect` then `classify_all` |
| `report.py` | Sections chosen by `waiting_kind`, `CLASSES[5]` (idle) and `CLASSES[7]` (unknown); `NEXT_INSPECTION` keyed by rule name |

**Conventions & Patterns:**

- Keep rules pure and first-match-wins; a rule returns `Classification` or None (rule 9 always returns).
- Missing proof never becomes False or "absent" (SPEC:232): set `worker_done_seen` or `fenced_evidence` only from a named live source.
- A new class needs `models.CLASSES`, the positional unpack at `classify.py:42-51` (a ninth entry breaks it; UNVERIFIED by execution), a `Rule` in `RULES`, a `NEXT_INSPECTION` row (a read only, no stop/retry/release/merge/remove wording), and the tables `RULE_NAMES` (`test_classify.py:351`), `_rule_cases` (`:277`) and `RULE_CLASS` (`test_report.py:1091`).
- A `finished` row never says admitted or accepted (`test_classify.py:791-800`).
- Prove a rule with a captured fixture and a `SOURCES.md` entry; in-memory builders alone prove only the code path.

<!-- END 5.3 -->

---

### 5.4 Sweep Read Side, Safety, Publish and the WC-16 Binding

**Purpose:** Collect read-only facts (Orca, git, disk), render one dated Markdown report plus a JSON v1 object, publish the report atomically under `.dev/sweeps/`, and bind a coordinator (by contract text only) to run it. Every failed read is reported as `unscanned`, never as clean.

**Key Files:**

| File | Purpose |
|------|---------|
| `src/superclaude/cli/sweep/probes.py` (1477 lines) | The only module that starts a subprocess: `ALLOWED_ORCA` (49-60), `ALLOWED_GIT` (68-81), `_orca` (266), `_git` (315), `Budget` (124), `collect` (1322) |
| `src/superclaude/cli/sweep/commands.py` (288) | `sweep run`, `_check_output` (99), `_publish` (153), exit codes |
| `src/superclaude/cli/sweep/report.py` (695) | `render` (608), `to_json` (613), `sanitize` (569), `SECTIONS` (545-558) |
| `src/superclaude/cli/main.py:581-583`, `cli/sweep/__init__.py` | Registration `sweep`; lazy import of `sweep_group` |
| `commands/sweep.md`, `skills/sc-sweep-protocol/SKILL.md`, `output-styles/pragmatic.md:22-25` | Command, skill (steps 1-4) and chat-summary exception |
| `core/WORKER-CONTRACT.md:20, 23, 46, 110, 287-289`, `core/HOW-WE-WORK.md:298, 359`, `.gitignore:255-256` | WC-16 and its routing and ignore rule |
| Tests | `test_probes_allowlist.py` (2397; 100 tests), `test_readonly.py` (536), `test_git_config_hole.py` (276; 10, real git), `test_cli_contract.py` (1534; 61), `test_cli_registration.py` (69; 3), `test_report.py` (1465; 43), `tests/commands/test_sweep_command.py` (637; 28 functions, prose pins only) |

**How It Works:**

```
coordinator (WC-16 prose duty) or person -> /sc:sweep -> Skill sc:sweep-protocol -> superclaude sweep run
  bind_run (only without --run) -> collect: Orca allowlist + git allowlist + disk reads, under Budget
  -> classify_all (pure) -> render (pure) -> _publish: temp file, os.link, unlink -> JSON on stdout
  -> .dev/sweeps/<UTC>-sweep.md (gitignored; read by the skill's step 3 and by a person)
```

Orca allowlist (10 templates, 7 verbs; `check_orca_argv` needs a token-for-token match, `<run>` = `run_[0-9a-f]{12}`, `<dispatch>` = `ctx_[0-9a-f]{12}`, `--include-remote` rejected in any position, refusal before any process starts). Binary: `$ORCA_CLI_COMMAND` if set (not validated) else `orca-ide`, never bare `orca`; only the arguments are allowlisted.

| # | Template | Status (`probes.py`) |
|---|----------|----------------------|
| 1 | `orchestration run-current` | called only when no `--run`; plain-text reply (399) |
| 2 | `orchestration worker-list --run <run> --json` | called once per Run (1150) |
| 3 | `orchestration worker-show --dispatch <dispatch> --json` | called, capped at 50 per sweep (1281) |
| 4 | `orchestration task-list --ready --run <run> --json` | called once per Run (1165) |
| 5 | `orchestration task-list --run <run> --json` | called once per Run (1178) |
| 6 | `worktree ps --json` | called once per sweep while Orca is available (1335) |
| 7, 8 | `worktree list --json`, `worktree current --json` | pinned, not called (56-57) |
| 9, 10 | `worktree ps --agent-wait` (with and without `--json`) | allowed by R5 (owner 2026-11-08), not called (58-59) |

Rows 7-10 are pinned by a zero-argv test (`test_probes_allowlist.py:624-638`). Result kinds: `ok`, `no_binding`, `unavailable` (timeout, binary missing, `runtime_unavailable`), `call_failed` (over 8 MiB, non-zero exit, invalid reply). After `unavailable` every later Orca read becomes an `unscanned` source row; the sweep still exits 0 (only a failed binding without `--run` exits 2).

Git: four exact argv shapes (`status --porcelain=v1 -z --branch --untracked-files=all --ignore-submodules=all`, `config --show-origin --list -z`, `ls-files -z`, `check-attr --stdin -z filter`). The seam always prepends `git --no-optional-locks -C <cwd> -c core.fsmonitor=false` and sets `GIT_OPTIONAL_LOCKS=0`. "4 fixed calls per worktree" is a maximum: `config` runs first; with no filter driver having a non-empty `clean` or `process` command, `status` runs after 2 calls. Filter holes (issue 547): when a tracked path selects such a driver, `status` is not run and the source row is `unscanned: git filter could run a program`. Real-git tests plant a marker-writing command and assert it never runs, with a positive control: routes 1 (shared `core.fsmonitor`), 4 (`include.path`), 5 (per-worktree config), 6 and 6b (`GIT_CONFIG_*` env), 2 and 3 (filter `clean`, `process`), 8 and 9 (submodule config). Route 7 was not found (UNVERIFIED); routes 8 and 9 pass because of `--ignore-submodules=all`, not the pre-check; a defined-but-unselected driver is still read.

| Disk read | Bound |
|-----------|-------|
| Packages: `<worktree>/.dev/tasks/{to-do,done}`, `progress.md` `FINAL:` line, `.archiving` marker | real path must stay inside the worktree; over 1 MiB only the last 512 KiB is searched |
| Contracts (`yaml.safe_load`) | candidates named by Task text or report folders, inside an observed worktree; 1 MiB |
| Transcripts `~/.claude/projects/<key>/*.jsonl` | key = worktree path with non-alphanumerics replaced by `-`; last 256 KiB |
| ccsession tab map `$XDG_STATE_HOME/ccsession/orca-tabs/*` | missing folder is readable and empty |
| Orca version `/opt/Orca/resources/app.asar.unpacked/out/package.json` | fixed Linux path; elsewhere the lock line prints UNVERIFIED |
| Remote hosts | never read; coverage fixed `unknown` |

Budgets: 50 shows (shared evenly across Runs), 90 s total, 10 s per call, 8 MiB output, 1 MiB contract and ledger, 256 KiB transcript tail, worker-list page 100. The four byte limits are marked "proposed (DESIGN 17 open item 19)"; a recorded decision for 50/90/10 is UNVERIFIED. Stable-read check re-reads once if (size, mtime) changed, then `conflict: inconsistent observation`.

Publish and exit codes: stem `YYYYMMDD-HHMMSS-sweep` (UTC); `_check_output` requires the folder inside `<root>/.dev/sweeps` (symlinked base fails) and not overlapping `.dev/tasks`, `~/.claude/projects` or the tab-map folder. Temp `.<stem>.<pid>.tmp` (`O_EXCL`, fsync), commit point `os.link` to `<stem>.md`, `-2` to `-99` (never overwrites), then unlink. JSON is printed after publication; a print failure leaves one complete report.

| Exit | Cause |
|------|-------|
| 0 | report published, one JSON object on stdout |
| 1 | publish error or any other exception (`[sweep <stage>] <sanitized message>`), including an allowlist `ValueError` |
| 2 | usage error or binding error (no Run bound, Orca unavailable while binding) |

JSON v1 (12 top-level keys, all always present): `schema_version`, `observed_at`, `collected`, `scope`, `window`, `orca_available`, `sources`, `rows`, `worktrees`, `waiting`, `summary` (counts for every class, `bound_reached`, `visible`, `historical`, `total`, `total_is_lower_bound`), `report_path` (the one unsanitized string). `orca_binary`, `orca_version`, the ten dimensions and Next inspection are Markdown only.

Report sections (`SECTIONS`, 12, joined by blank lines; header and footer have no `##`): header (READ ONLY line, scope, `Messages coverage: partial`, lock-risk line); Source coverage; Waiting on a person (a); Waiting on a person (b) with Ready Tasks "creator not observable in Phase 1"; Could not determine; Retained problems; Sessions (10 dimension columns, `SP24_LINE`, `SAFE_TO_CLOSE_LINE`); Worktrees; Historical sessions; Shift Brief; What I could not determine; footer ending "Report complete".

Sanitizer (`sanitize`): strips ESC sequences, drops control, format, surrogate and private-use characters, turns line breaks into a space, then escapes `\ | < > [ ]`; `cell` cuts to 200 characters; empty cell prints `none`.

Command and skill: `commands/sweep.md` has `allowed-tools: Skill`, no worker mode and no `## Unattended mode`, and says "Nothing starts it automatically" (:22). The skill runs `superclaude sweep run` (PATH first; `uv run --frozen --no-sync` only on "command not found"; Bash timeout 120000), Reads the report in chunks of at most 150 lines to `Report complete`, then prints counts and the path; exit 1 or 2 prints stderr and ends. Chat exempt reply: the final successful reply may skip the DONE / NEXT table only if there is an explicit top-level coordinator assignment (system/developer or direct person instruction, in force), the loaded skill is executing a real `/sc:sweep`, exit 0, stdout parsed, report Read; workers, subagents, failures and quoted text stay ordinary. `SKILL.md:51` calls it "a rule the loaded text states, not a runtime detector"; 37 shared clauses plus 15 skill-only pins are tested as text.

**WC-16 binding:**

| Element | Text (location) | What code does |
|---------|-----------------|----------------|
| WC-16 | `WORKER-CONTRACT.md:287-289`: on every coordinator wake or wait timeout, at most once every 5 minutes, run "The sweep." unchanged and in the same pass `/sc:sweep`, read its report before acting; an added read, not a second pass, no heartbeat update, no `worktree ps --agent-wait`, not an L1 probe; "Phase 1 adds this duty, not a scheduler" | No caller exists: hop 1 is prose for an LLM session; hops 2-4 (command, skill, `main.py` registration) are intact |
| "The sweep." | `:110`: one `worker-list`, one `worktree ps --agent-wait`, one `stat` per contract path, heartbeat records updated | Sweep issues its own `worker-list`, never calls `worktree ps --agent-wait`, reads `agentWait` from `worker-show`, allowlists no message verb; heartbeats, deadlines and the L0-L5 ladder stay the coordinator's |
| WC-10 stall proofs | `:46, :157`; WC-16: "only Orca's stall proofs make a worker stalled" | Only rule 2, with no producer for two inputs; the transcript proof "final turn sent no `worker_done`" has no reader (transcript tail keeps timestamps and session id); fallback is could not determine |
| Never-as-worker | `:23` lists `/sc:sweep`; brief guard case 3 (`:20`); `commands/sweep.md:18, 42, 70` | Pinned in `tests/skills/test_worker_contract.py` and `test_sweep_command.py:155-159` |
| HOW-WE-WORK | row 298 (read-only snapshot, "Coordinator or person only, never a worker"), row 359 (every wake, at most once per 5 min, beside "The sweep."); `commands/closeout.md:99` | Row required by `tests/core/test_how_we_work_routing_table.py:33` |
| Cadence and "read before acting" | WC-16 | No throttle in `cli/sweep` (grep found none); only the sentence is pinned (`test_worker_contract.py:212-215`) |
| Never posted, recommends nothing | WC-16, `.gitignore:255-256` | No send or post verb; `NEXT_INSPECTION` names a read only; `test_report.py:1439-1459` |

**Public Interface:**

```python
sweep run [--run RUN]... [--window 6h] [--root PATH] [--output PATH]          # commands.py:220-241; window <N>h|<N>d, max 720h
collect(ctx: SweepContext, runs: tuple[str, ...], root: Path, budget: Budget) -> SweepInput   # probes.py:1322
Budget(shows=50, total_s=90.0, per_call_s=10.0, clock=time.monotonic); bind_run(budget) -> str
check_orca_argv(args) / check_git_args(args) -> None   # raise ValueError
render(result: SweepResult, ctx: SweepContext) -> str; to_json(result, ctx, report_path: str) -> dict
_publish(text: str, output_dir: Path, now: datetime) -> Path                    # private, only writer
```

**Dependencies:**

| Depends On | Type | Description |
|------------|------|-------------|
| `orca-ide` or `$ORCA_CLI_COMMAND` | Subprocess | 6 read templates; `runtime_unavailable` shape never induced (design item 9) |
| `git` | Subprocess | 4 exact argv shapes, lock-free |
| Claude project transcripts, ccsession tab map, `.dev/tasks` | File read | bounded as above |
| `yaml`, `click` | Import | contract parsing; CLI group |

**Consumers:**

| Used By | How |
|---------|-----|
| Coordinator or person via `/sc:sweep` | runs the skill, Reads the report; WC-16 asks for it, no code enforces it |
| Tests | the four pinning layers: allowlist shapes plus an `ast` scan of `probes.py` for write verbs, recorded-argv full sweeps, a before/after file-snapshot diff, real-git hole tests |

**Conventions & Patterns:**

- Add an Orca or git call only by extending `ALLOWED_ORCA` or `ALLOWED_GIT` and the pinned tests; the argv must match exactly.
- Map every failure to an `unscanned` source row or None; never to an empty or clean value.
- Write only through `_publish`; the report folder must stay inside `<root>/.dev/sweeps`.
- Pass every string into a report or JSON through `sanitize` (`cell` in tables); `report_path` is the one raw string, by design.
- A new report section is a function added to `SECTIONS`; a breaking JSON change bumps `JSON_SCHEMA_VERSION` (the bump policy is UNVERIFIED).
- Design section 17 (23 open items, no status column) is a historical list; item statuses stay UNVERIFIED unless code shows closure.
- Keep UNVERIFIED items marked: non-null `agentWait` meaning, source for stall and fence proofs, route 7, Budget decision, orchestrator binding.
