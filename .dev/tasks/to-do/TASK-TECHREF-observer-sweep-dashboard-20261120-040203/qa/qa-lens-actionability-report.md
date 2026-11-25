# QA Report - Tech Reference Actionability Lens (tech-ref-qualitative)

**Status:** Complete
**Topic:** Observer, Sweep and Dashboard technical reference (actionability lens)
**Date:** 2026-11-20
**Phase:** tech-ref-qualitative (actionability lens, Gate 3)
**Fix cycle:** N/A (fix_authorization: false; document not modified)
**Document:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/techref/OBSERVER-SWEEP-DASHBOARD-TECHNICAL-REFERENCE.md
**Snapshot:** /home/coder/.cache/ic-snap-20261120/master (origin/master 61ac2c2e6)

---

Method: read the whole document (1,698 lines), then read the cited snapshot files and test files for each Section 13.1 scenario, Section 9 and Section 13.2. Nothing was run. Document line cites are as printed in the document; "snapshot" below means /home/coder/.cache/ic-snap-20261120/master.

## Scenario A: add a sweep class or rule

| Step | Specific (yes/no) | Verified against code (yes/no) | Evidence |
|---|---|---|---|
| 1 Add class string to `CLASSES`; add a 9th name to the unpack | yes: `sweep/models.py:50-59` and `sweep/classify.py:42-51` | yes | models.py:50-59 is the 8-tuple `CLASSES`; classify.py:42-51 is `(C_WAITING, ..., C_UNKNOWN) = CLASSES`, so a 9th entry gives a ValueError at import (Python semantics). The constant name is left to the reader (skeleton uses `C_EXAMPLE`); acceptable |
| 2 Write rule, register `Rule(name, fn)` in `RULES` at the precedence position | yes: `classify.py:345-355` | yes | `RULES` is a tuple of 9 `Rule(...)` at classify.py:345-355; `Rule` is a dataclass with `name` and `match` (classify.py:156-158); `_classification(class_name, rule, evidence, waiting_kind=None, notes=())` at classify.py:130-136 matches the skeleton comment |
| 3 Add `NEXT_INSPECTION[rule]` | yes: `report.py:54-68` | yes | `NEXT_INSPECTION` dict keyed by rule name at report.py:54-68; `.get(c.rule, _NEXT_DEFAULT)` at report.py:439 confirms the "missing key falls back" claim |
| 4 Edit report sections only if the class needs its own section (default: only `Sessions` table and `summary.counts`) | yes: `report.py:545-558` | yes | report.py:407 lists every row except `_IDLE` in Sessions; report.py:687 builds `counts` over `CLASSES`; classify.py:974 builds `counts` over `CLASSES`. Claim holds |
| 5 Update the test tables | yes (names `_rule_cases`, `RULE_NAMES`, `RULE_CLASS`, line numbers) | yes | test_classify.py:277 `_rule_cases`, :351 `RULE_NAMES`, :371-375 `reached == set(CLASSES)`, :378-379 rule-order pin; test_report.py:1091 `RULE_CLASS`, :1105-1127 coverage test (`set(RULE_CLASS) == names`, `set(report.NEXT_INSPECTION) == names`, `BANNED_WORD` at :1102) |
| Pitfall: `report.py:26-27` index `CLASSES[5]`, `CLASSES[7]` | yes | yes | report.py:26-27 verified verbatim |
| Pitfall: `class_name` not in `CLASSES` raises KeyError at `classify.py:976` | yes | yes | classify.py:974-976: `counts = {name: 0 for name in CLASSES}` then `counts[c.classification.class_name] += 1` |
| Pitfall: `idle` / `person_active` suffix tuple at `classify.py:958` | yes | yes | classify.py:958 `if cls.rule in ("idle", "person_active"):` adds `last_activity from <source>` |
| Prose touch points `docs/designs/orchestrator-mode.md:474`, `commands/sweep.md:14` | yes | yes | orchestrator-mode.md:474 lists the eight `CLASSES`; sweep.md:14 says "one of eight classes" |
| Tests `test_cli_contract.py:956, 1032, 1077` named as files to touch | yes | yes, but no edit is needed | All three derive from `CLASSES` (`{name: int for name in CLASSES}` at :956, `list(CLASSES)` at :1032 and :1077), so a new class passes them without edits; they are verification points, not edit points (minor, F-M1) |

Scenario A result: every named file, constant, function, registration point and test exists and the steps would work.

## Scenario B: add a sweep probe or allowlist entry

| Step | Specific (yes/no) | Verified against code (yes/no) | Evidence |
|---|---|---|---|
| 1 Add one token tuple to `ALLOWED_ORCA`; `<run>` and `<dispatch>` are the only placeholders; ids matched with `re.fullmatch` | yes | yes | probes.py:49-60 `ALLOWED_ORCA`; probes.py:91 `_PLACEHOLDERS = {"<run>": RUN_ID_RE, "<dispatch>": DISPATCH_ID_RE}`; probes.py:219-223 `_token_matches` uses `re.fullmatch`. The step does not say what to do if the new verb needs a third placeholder (extend `_PLACEHOLDERS` and pin the regex in `test_other_allowlist_constants_are_pinned`, test_probes_allowlist.py:391-401); minor gap (F-M2) |
| 2 Add one call site shaped like worker-list at `probes.py:1150` | yes | yes | probes.py:1150 is `_call(budget, "orchestration", "worker-list", "--run", run, "--json")`; `_call` is at probes.py:369; `record(...)` helper at :1131 writes the `SourceCoverage` row |
| 3 Add the field to `OrcaObservation` (or `SweepInput`) and set it in `parse_worker_show` | partly: `parse_worker_show` only applies to a worker-show field; for a non-show probe the setting point is `collect` (probes.py:1383-1396), which is in the file list but not named in the step | yes | models.py:84 `OrcaObservation`, :237 `SweepInput`; probes.py:471 `parse_worker_show`; probes.py:1322-1396 `collect` builds `SweepInput` |
| 4 Add a `SourceCoverage` row for every read and failure | yes | yes | models.py:229 `SourceCoverage(name, coverage, age_seconds, unscanned)`; probes.py:1136-1138 and :1338-1357 show the read / unscanned pair |
| 5 Update the allowlist tests; for git add a shape to `ALLOWED_GIT` | yes | yes | test_probes_allowlist.py:370 (`..._exactly_the_ten_templates`), :375 (`..._names_seven_verbs`), :391 constants pin, :404-406 every-template accepted, :423-462 negatives (24 named entries, matches "24 named negative argv" in 13.2), :489-498 `ast` scan, :609-638 recorded-argv and zero-argv tests; test_readonly.py:448 asserts `set(orca_calls) == {WORKER_LIST, TASKS_READY, TASKS_ALL, WORKTREE_PS}` |
| Pitfall: "10 templates, 7 verbs (NFR-014)" comment at `:60` | yes | yes | probes.py:60 comment verbatim |
| Pitfall: full sweep recording 1 + 2 + 5 + 1 = 9 argv | yes | yes | test_probes_allowlist.py:619 `assert len(orca_argv) == 1 + 2 + 5 + 1` |
| Pitfall: four pinned templates tested as zero argv | yes | yes | test_probes_allowlist.py:624-638 (`NOT_CALLED` parametrisation plus the `worktree list|current` and `--agent-wait` assertions) |
| Pitfall: `parse_worker_show` never raises; failure maps to unscanned or None | yes | not re-traced beyond the signature (probes.py:471) and the `record`/`unscanned` pattern; consistent with the code read | |
| Pitfall: git call keeps `--no-optional-locks`, `core.fsmonitor=false`, filter pre-check | yes | yes | probes.py:64-81 comment and `ALLOWED_GIT`; test_readonly.py:40-84 recorder asserts the lock-free argv |

Scenario B result: the steps work; two small gaps (steps 1 and 3) are minor.

(Pitfall "`parse_worker_show` never raises" was re-checked afterwards: probes.py:476 docstring "Never raises", built only from `_get` / `_text` / `_first` which return None on any non-dict. Verified.)

## Scenario C: add a snapshot field

| Step | Specific (yes/no) | Verified against code (yes/no) | Evidence |
|---|---|---|---|
| 1 Row field: add to `_FIELDS` and `Row`, populated by `parse_page` | yes (`observe/parse.py:58-90, 110-157, 365`) | yes | parse.py:58-90 `_FIELDS` (31 entries); parse.py:110-157 `Row` frozen dataclass with `= UNKNOWN` defaults; `_parse_row` (parse.py:325-354) loops `_FIELDS` and is called from `parse_page` (:365). `_KNOWN` (:106) is derived from `_FIELDS`, so no third edit is needed |
| 2 Export: add `("<jsonKey>", "<row_attr>")` to `_TEXT_FIELDS` (dotted key nests) or `_ANY_FIELDS`, or write a conditional key | yes (`observe/export.py:20, 25-47, 141-216`) | yes | export.py:25-45 `_TEXT_FIELDS`, :46 `_ANY_FIELDS`, :134-138 `_set` splits dotted keys, :141-155 `_row_dict` shows the conditional-key pattern (`orderUnknown`, `notReobserved`, `absentFields`) |
| 3 Top-level value: carry on `SnapshotMeta`, set in `_meta`, write in `snapshot_dict` | yes (`view.py:203-223, 664`) | yes | view.py:203-223 `SnapshotMeta`; view.py:664-695 `_meta`; export.py:183-216 `snapshot_dict` |
| 4 Edit `snapshot.schema.json` under `definitions.row.properties`; `required` only if emitted on every row | yes (`:106-155`) | yes | schema lines 103-155: `required` list at 106-109, `properties` at 110-155, `additionalProperties: false` at 105. A `_TEXT_FIELDS` entry is emitted on every row (export.py:144-145), so it belongs in `required`; consistent with the step |
| 5 Tests | yes (`test_snapshot_schema.py:25, 59-91, 296-326, 404-465`, `test_export.py`, `test_render.py:655-695`) | yes | test_snapshot_schema.py:25 `VALIDATOR`, :59-73 closed-schema pin, :79-91 every variant validates, :296-326 privacy test, :404-465 ordering and questions group; test_export.py has 20 tests; test_render.py:655-695 holds the two golden byte pins |
| Pitfall: closed schema rejects an unlisted key | yes | yes | schema `additionalProperties: false` on root (line 6), row (105), stage, liveness, evidence |
| Pitfall: unconditional row key changes `snapshot_json` bytes of the five questions-off variants pinned by `golden_release1_records.json` | yes | yes | test_render.py:677-695 compares `record_text` and `snapshot_json` of every variant to `golden_release1_records.json` and states "never regenerated"; the surface test at :655-671 says "five questions-off variants" |
| Pitfall: privacy test key list and `WITHHELD_QUESTION_KEYS` | yes | yes | test_snapshot_schema.py:262-282 `FORBIDDEN_KEYS` (the doc quotes 8 of 19 names with "..."), :424 `WITHHELD_QUESTION_KEYS`. See F-M9: `FORBIDDEN_WORDS` (:283-293) is a substring check on the whole JSON text and is not mentioned |
| Pitfall: 11 parsed attributes not exported, 6 with no stated reason | yes | yes | parse.py `_FIELDS` minus export.py `_TEXT_FIELDS`/`_ANY_FIELDS` leaves exactly resource.* (7), workspace.id/kind (2), stage.activity/detail (2) = 11; the privacy test pins 5 of them |
| Pitfall: additive-only policy | yes | yes, as a stated policy | schema `description` (line 4): "Additive-only ... removing, renaming or retyping a field needs schemaVersion 2"; nothing enforces it mechanically; the document says so (5.1) |

Scenario C result: every named file, constant, function, registration point and test exists and the steps would work.

## Scenario D: add an observer view, panel or key

| Step | Specific (yes/no) | Verified against code (yes/no) | Evidence |
|---|---|---|---|
| 1 New data: add a defaulted field to `CycleResult` | partly: names the class (`collector.py:37-68`) but not where the field is filled | class yes; "step works" no | collector.py:37-68 `CycleResult` (defaulted question fields at :55-68, matches "defaulted"). The field stays at its default unless `Collector.run_once` (collector.py, builds the `CycleResult`) sets it; the step does not say so (part of F-1) |
| 2 Typed frozen dataclass and a builder returning None when off | yes (`view.py:253-298, 334-378`) | yes | view.py:253-298 `DeskView`, `QuestionsPanel` (frozen dataclasses); `_questions_panel(result, clock, selected_question=None) -> QuestionsPanel | None` at view.py:709-715 returns None when `question_state == "OFF"` |
| 3 Defaulted `View` field, set by keyword in `build_view` | yes (`view.py:968-1156`) | yes | view.py:335-378 `View` with `questions: ... = None`, `desk: ... = None`; view.py:1104-1156 `View(...)` call sets `questions=panel`, `desk=_desk(...)` by keyword |
| 4 Literals as constants in `view.py` | yes (`view.py:44-134`) | yes | view.py:44-134 block "literals defined once" (`GAP_NOTICE`, `LEDGER_TITLE`, `KEYS_LINE` ...) |
| 5 Place it in `_compose`'s height budget and each width class | yes (`render.py:1258-1446`, `_columns` 480-568) | yes | render.py:1258 `_compose`, :1302-1314 footer-height budget; terminal.py:21-24 and :82-89 define the four width classes; render.py:480 `_columns` |
| 6 New key: `apply_key` (and `KEY_NAMES` if non-text) | partly | step would not work for a non-text key: **F-1** | view.py:30 `KEY_NAMES`, :1246-1300 `apply_key`. A `Key` is built only in `keys.py` (:165, 186, 188, 190, 194, 214, 227, 233, 235) and `Key.__post_init__` (view.py:144-148) rejects any name outside `KEY_NAMES`; `keys.py` `_take` (:176) and `_take_escape` (:217) emit only enter, backspace, ctrl_c, text, escape, and up/down from CSI/SS3 finals `A` and `B`. A new non-text key reaches `apply_key` only after an edit in `keys.py`, which no step names |
| 7 Fixture variant if needed (`parse.py:750-761`) | yes | yes | parse.py:750-761 `VARIANTS` (10 names); `load_fixture` (:801) reads `fixtures/<variant>.json`; `--fixture` validated through `load_fixture` (commands.py:427-435); every `VARIANTS` entry is parametrised in test_snapshot_schema.py:79 |
| Pitfall: three width classes full >=160, line 116-159, short 80-115 | yes | yes | terminal.py:21-24, 82-89 |
| Pitfall: "below 80 columns or 8 rows only a refusal line prints" | yes | no: F-M3 | render.py:1263-1272: below 80 columns it prints the refusal plus `counts_line_objects(view.counts_tokens)` plus `view.gap_notice`; below 8 rows the refusal plus `view.collected_text` plus the gap notice. Section 5.2 (line 584) says "each with counts and the gap notice" |
| Pitfall: "no key can reach the adapter or collector" is a test | yes | yes | test_session.py:359 `test_no_key_can_reach_the_adapter_or_collector`; it also pins EXPORT to `e` and QUIT to `q`/ctrl_c over `string.printable` (:389-393), and `test_unknown_keys_do_nothing_and_there_is_no_refresh_key` (:339-353) pins `r`, `x`, `Z`, `1`, space as no-ops; the document does not mention the second test (part of F-1) |
| Pitfall: new colour role must exist in `theme.py` (registration rule UNVERIFIED, U-33) | no, left open | the rule is readable: F-M4 | theme.py:16 `ROLES`, :36 `_PALETTE_OF`, :111-125 `style_for` raises `KeyError("unknown role")` for a role not in `_PALETTE_OF`; test_theme.py:31 loops `ROLES` |
| Pitfall: help line chosen at `view.py:1139-1141` | yes | yes | view.py:1139-1141; the three constants are view.py:91-118 `QUESTIONS_KEYS_LINE`, `QUESTIONS_LINK_KEYS_LINE`, `KEYS_LINE` (a new key must be added to these to be shown; not stated) |
| Pitfall: a new always-on element changes the surface pinned by `golden_release1_surface.json` | yes | yes | test_render.py:655-671 compares `surface()` to `golden_release1_surface.json` |

Scenario D result: steps 2 to 5 and 7 are exact and work; steps 1 and 6 stop before the edit that makes the new data or key arrive (F-1, blocking); the scenario names no test to add (see F-M5).

## Scenario E: add an agent-work-report source

| Step | Specific (yes/no) | Verified against code (yes/no) | Evidence |
|---|---|---|---|
| 1 New script `scripts/<name>.py` with `main(run)`: read the run folder, write `<run>/<name>.json` | yes (shape of `exclude.py`, `sessions.py`) | yes | exclude.py:59-109 is `main(run)` reading `run / ...json` and writing `excluded.json`, with `if __name__ == "__main__": if len(sys.argv) != 2: sys.exit(__doc__)`; `main(run)` also exists in activity.py:178, classify.py:113, collect.py:223, match.py:109, page.py:226, render.py:392, sessions.py:278. The `usage:` docstring and the argv check are not stated but follow from the cited model |
| 2 Subprocess only via `common.run_cmd` | yes | yes | common.py:103-113 `run_cmd(args, timeout=120)` list args, no shell; `gh_json` at :116 |
| 3 Add the step to the SKILL.md step list and artifact table | yes (`SKILL.md:56-72, 76-95`) | yes | SKILL.md:56-72 is the artifact table, :76-95 the 15-step table |
| 4 Join it in `match.py` / `classify.py`; present it in `render.py` and templates | files only, no function or constant named | files exist; functions not named: F-M5 | match.py has `task_facts` (:39), `session_facts` (:62), `session_item` (:80), `main` (:109); classify.py has `priority` (:31), `rule` (:67), `classify` (:86), `main` (:113); render.py `main` (:392) |
| 5 A new gate check means `REQUIRED_CHECKS` and `check.main` | yes (`run.py:204-212`) | yes | run.py:204-212 `REQUIRED_CHECKS` (7 names); run.py:219-242 `passed()` reads `| <name> | PASS |` rows; check.py:168 `main(run, links=False)` |
| 6 A new `run.py` subcommand needs an exact-argv-length branch (`run.py:868-887`) | yes | yes | run.py:868-887: each branch tests `a[:1] == [...] and len(a) == n`, else `sys.exit(__doc__)` |
| Pitfall: `SKILL.md:38` Orca's own session state is never read | yes | yes | SKILL.md:38 verbatim in substance ("What Orca says about a session's state is never used") |
| Pitfall: a run without `--links` cannot pass the gate | yes | yes | run.py:204-212 lists `links`; run.py:231 requires every name PASS |
| Pitfall: artifact table omits `abandoned.json` and `refresh.lock` | yes | yes | SKILL.md:56-72 has neither |
| Pitfall: entry readers refuse symlinks; tests patch `gh_json`, `run_cmd`, ClickUp `call`; no real `orca`, `gh` or ClickUp call | yes | yes | common.py:183-209 `entry_files`; test_agent_work_report.py:304, 1249, 2953, 2958 patch `gh_json`/`run_cmd`; :105-120 `root` fixture replaces `orca_term.orca` with a raising stub |

Scenario E result: the named files, constants and line ranges exist and the steps are directionally right; step 4 names no function, and no test step is given in the scenario (F-M5).

## Section 9 configuration check

| Item in Section 9 | Document says | Code says | Match |
|---|---|---|---|
| Observer flags (9.3, 5.2) | `--once`, `--width {160,116,80}`, `--ascii`, `--fixture <name>`, `--snapshot <file>`, `--run <id>`, `--questions` | observe/commands.py:449-496: exactly these options; `WIDTHS = ("160","116","80")` (:61) | yes |
| `--questions` rules and exit codes | needs `--run` and a live source (exit 2); gate False exits 1 with no Orca call | commands.py:183-197 `_question_refusal` (fixture, no run, bad run id give 2; gate False gives 1), :414 runs it before any Orca call | yes |
| Gate constants | `QUESTION_GATE_PASSED`, `QUESTION_LINK_PASSED` at commands.py:67, 70, both True | commands.py:67, 70 | yes |
| Fixture runs write no snapshot without `--snapshot` | yes | commands.py:264 (`--once`), :408 `write_snapshots=live or bool(options.snapshot)` | yes |
| Sweep flags | `run --run` (repeatable), `--window` default `6h` (`[1-9][0-9]{0,3}[hd]`, max 720h or 30d), `--root`, `--output` default `<root>/.dev/sweeps/` | sweep/commands.py:219-241 and :43-52, :27-29 | yes |
| `ORCA_CLI_COMMAND` default `orca-ide`, unvalidated | probes.py:214-216 | yes | yes |
| `XDG_STATE_HOME` | observer `<it>/superclaude/observe` when absolute; sweep `<it or ~/.local/state>/ccsession/orca-tabs` (probes.py:871) | export.py:236-244; probes.py:870-871, :1369-1371; sweep/commands.py:253 | yes |
| `NO_COLOR`, `COLORTERM`, `TERM` | non-empty `NO_COLOR` disables colour; truecolor/24bit, `*256color`, else standard; dumb gives none | terminal.py:92-116 (`TERM` "dumb" and "unknown" both give none; trivial) | yes |
| Design `--show` and `NO_COLOR` | presence only (render.py:129) | `"NO_COLOR" in os.environ` at render.py:129 | yes |
| `AWR_ROOT`, `orchestrator_repo` | `common.py:28-51` | common.py:28-51; AWR side reads the key and works on master (test_agent_work_report.py:2979-3002) | yes, with F-M7 on the wording "only `$AWR_ROOT` works" |
| `AWR_HOOK_FILE`, `AWR_PROJECTS` and defaults | `~/.config/orca/agent-hooks/last-status.json`, `~/.claude/projects` | sessions.py:44-47 | yes |
| `CLICKUP_API_TOKEN` (required), `CLICKUP_WORKSPACE_ID` (optional) | yes | clickup.py:60-63, 132; SKILL.md:37 | yes |
| `ORCA_TERMINAL_HANDLE`, `CLAUDE_TOPIC` | orca_term.py:34-58 | orca_term.py:35, 56-57 | yes |
| `GIT_OPTIONAL_LOCKS=0` set by the sweep | probes.py:331-340 | probes.py:340 `env = {**os.environ, "GIT_OPTIONAL_LOCKS": "0"}` | yes |
| `config.json` 14 keys and recorded values | person `clayphi`, orgs two, timezone America/Chicago, `daily_run_local` 07, `missed_run_dm_local` 09, budgets 120/10, prefix `coordinator-` | config.json: 14 keys; values match except the two time strings are `"07:00"` and `"09:00"`; waker.py:56, 61 read only the first two characters | yes, with F-M6 |
| `session_tag` read at waker.py:175, 273, 362; `person_name` at classify.py:35, 62; no read of `clickup_email` / `clickup_user_id` | yes | same lines; no `CONFIG["clickup_*"]` in any script (clickup.py:559 reads settings.json, not CONFIG) | yes |
| `settings.json` / `priorities.json` writers | clickup.py:558-563, 610-612; prefs.py:35-47 | same lines | yes |
| `JOIN_PATH = "B"`, `CHECKED_ORCA_VERSION = "1.4.245"`, `JSON_SCHEMA_VERSION = 1` | classify.py:40, report.py:23, models.py:18 | all three at those lines | yes |
| `.gitignore:255-256` | `.dev/sweeps/` | .gitignore:256 `.dev/sweeps/` | yes |
| Design `render.py --batch {1,2}`, `--show`, `--width N`, defaults 1, none, 116 | render.py:127-130 | render.py:127: `--batch` int choices (1,2) default 1; `--show`; `--width` int default 116 | yes |
| Design font path and requirements | render.py:16-18 | render.py:16-17 | yes |
| `issue-watch.json` `_TOP_KEYS` rejects extra keys | cycle.py:58-69, 216-220 | exactly; `orchestrator_repo` absent from `_TOP_KEYS` | yes |

Configuration result: no wrong flag, variable or default. Two precision notes (F-M6, F-M7).

## Other checks in this lens

| Check | Result | Evidence |
|---|---|---|
| Pitfalls reflect real constraints (additive-only schema; exact-template allowlist) | PASS | Additive-only is the schema's stated policy (snapshot.schema.json line 4) and the document says it is not enforced by the file; the allowlist is token-for-token (probes.py:226-238 `check_orca_argv`), pinned by `test_allowed_orca_is_exactly_the_ten_templates` (:370) |
| Is every how-to followable without reading other documents? | PASS with notes | Steps cite code and test locations in the snapshot; ids such as U-30, U-33, G-03, G-05 are defined in Section 14.4 B and C, so they resolve inside the document. Gaps are those in F-1, F-M5 |
| Criteria testable (pass/fail), not aspirational | PASS | Section 13.2 lists tests by file; Section 15.2 gives five concrete spot-checks; no criterion uses aspirational wording |
| "Unification touch points" are facts with paths, not a recommendation | PASS | Heading and rows say "facts only; no recommendation"; whole-document grep for recommend/unif* finds only negations ("recommends no unification", "recommends nothing"). Row 1 evidence `adapter.py:34-50, 496-507` verified (FORBIDDEN_PREFIXES; `_ERROR_CODES` handling in `read_questions`); row 2 `adapter.py:24-27` (`Runner`, `Discover`), `commands.py:132-147` (`Deps`) and `CycleSource` (collector.py:71) verified. Weak point: sweep and AWR seams have no path or line and the evidence column cites research ids (F-M8) |
| Section 13.2 names real test files and locations | PASS | All files exist in the snapshot: tests/sweep/{test_classify,test_report,test_cli_contract,test_probes_allowlist,test_readonly,test_git_config_hole,test_cli_registration}.py; tests/commands/test_sweep_command.py (28 tests); tests/skills/test_worker_contract.py (WC-16 at :167-170, sentence at :212-215); tests/core/test_how_we_work_routing_table.py:33; tests/observe/{test_adapter,test_parse,test_collector,test_golden_contract,test_snapshot_schema,test_export,test_render (135 tests),test_session,test_view,test_height_budget,test_live_screen_pty,test_keys_spike,test_commands,test_registration}.py; tests/skills/test_agent_work_report.py. Counts checked: 24 named negative argv (test_probes_allowlist.py:423-453), 22 + 17 rejected observer shapes (test_adapter.py:244-267 and :651-679), backoff `[30.0, 60.0, 60.0, 60.0]` (test_collector.py:149), STALE at 45 s (test_golden_contract.py:121-122) |

## Summary
- Checks passed: 10 / 11
- Checks failed: 1 (Scenario D)
- Critical issues: 0
- Blocking (IMPORTANT) issues: 1 (F-1)
- Minor notes: 9 (F-M1 to F-M9)
- Issues fixed in-place: 0 (fix_authorization: false; document not modified)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| F-1 | IMPORTANT (blocking) | Section 13.1 row D, steps 1 and 6 (and the matching convention in 5.2, "A new non-text key needs a name in `KEY_NAMES` ... and a branch in `apply_key`") | Step 6 says a new key needs `apply_key` and, if non-text, `KEY_NAMES`. That is not enough: `Key` objects are built only in `observe/keys.py` (`_take` at :176, `_take_escape` at :217; the escape decoder maps only the CSI/SS3 finals `A` and `B`), and `Key.__post_init__` (view.py:144-148) rejects names outside `KEY_NAMES`. A developer who follows step 6 literally for a non-text key (for example PageUp) gets a key that no input produces. Step 1 stops at "add a defaulted field to `CycleResult`" with no step saying `Collector.run_once` must fill it, so the field stays at its default. Step 6 also omits two pinned tests that a new key can break: `test_unknown_keys_do_nothing_and_there_is_no_refresh_key` (test_session.py:339-353; `r`, `x`, `Z`, `1`, space and backspace must do nothing) and `test_no_key_can_reach_the_adapter_or_collector` (:359-393; only `e` exports, only `q`/ctrl_c quit), and the help-line constants a new key must be added to (view.py:91-118). | In row D, step 1 add "and set it in `Collector.run_once` when it builds the `CycleResult`". Replace step 6 with: "New key: add the branch in `apply_key`; for a non-text key also add its name to `KEY_NAMES` (view.py:30) and make `KeySource._take` / `_take_escape` (keys.py:176, 217) return `Key("<name>")`; add the key to `QUESTIONS_KEYS_LINE`, `QUESTIONS_LINK_KEYS_LINE` (view.py:91-93) so it is shown; extend `test_keys_spike.py` (decoder) and `test_session.py`; `r`, `x`, `Z`, `1` and space are pinned as no-ops at test_session.py:339-353". Make the same correction to the 5.2 convention sentence. |
| F-M1 | MINOR | 13.1 row A, "Files to Touch" | `test_cli_contract.py:956, 1032, 1077` are listed as files to touch but all three derive from `CLASSES` and need no edit | Move to a "verify, no edit" note |
| F-M2 | MINOR | 13.1 row B, steps 1 and 3 | Step 1 does not say what to do when the new verb needs a third placeholder (extend `_PLACEHOLDERS`, probes.py:91, and pin its regex in `test_other_allowlist_constants_are_pinned`, test_probes_allowlist.py:391-401). Step 3 names `parse_worker_show` only, but a field from a non-show probe is set in `collect` (probes.py:1383-1396) | Add one clause to each step |
| F-M3 | MINOR | 13.1 row D pitfall "(below 80 columns or 8 rows only a refusal line prints)" | Contradicts Section 5.2 (line 584) and render.py:1263-1272: the refusal screens also print the counts line (or `collected_text`) and `view.gap_notice`, so a new panel's gap-notice text is visible there | Reword to "below 80 columns or 8 rows a refusal line prints, with the counts and the gap notice; layouts are not drawn" |
| F-M4 | MINOR | 13.1 row D pitfall "A new colour role must exist in `theme.py` (registration rule UNVERIFIED, U-33)" | The rule is readable: add the role to `ROLES` (theme.py:16) and `_PALETTE_OF` (theme.py:36), and to `_BOLD` if bold; `style_for` raises `KeyError` otherwise (theme.py:117-118); `test_theme.py:31` loops `ROLES` | State the rule and close U-33 |
| F-M5 | MINOR | 13.1 rows D and E | Neither scenario has a test step or lists a test file under "Files to Touch" (A, B, C do); the only pointers are the change-type rows of 13.2. Row E step 4 names no function: the join lives in `match.main` (with `task_facts`, `session_facts`, `session_item`), grouping in `classify.rule` / `classify.classify`, presentation in `render.main`; the tests chain the scripts by hand in `new_run` (test_agent_work_report.py:123-140), which a new pipeline step must join | Add a test step to D (`test_view.py`, `test_session.py`, `test_height_budget.py`, `test_render.py`) and E (`tests/skills/test_agent_work_report.py`, the `root` fixture at :105 and `new_run` at :123); name the functions in E step 4 |
| F-M6 | MINOR | 9.1 `config.json` row | Prints `daily_run_local 07` and `missed_run_dm_local 09`; the file values are the strings `"07:00"` and `"09:00"` (waker.py:56, 61 read only the first two characters) | Print the literal values |
| F-M7 | MINOR | 9.2 `AWR_ROOT` row, 8.2, 14.1 ("Only `$AWR_ROOT` works") | The AWR side does read `orchestrator_repo` on master (common.py:35-51; test_agent_work_report.py:2979-3002). What fails is the poll: `superclaude issue-watch` rejects a config file holding the key (cycle.py:216-220, `config_invalid`). The actionable pitfall (adding the key to `~/.config/superclaude/issue-watch.json` breaks the poll's config check) is not stated that way | Reword: "AWR reads the key, but master's issue-watch rejects the file while the key is present; use `$AWR_ROOT`" |
| F-M8 | MINOR | Section 13, "Unification touch points", row "Extension seams in code" | Facts are true, but the sweep (`RULES`, `ALLOWED_ORCA`, `SECTIONS`) and AWR (`run.py` dispatch) seams carry no path or line and the evidence column cites "research 06 s2; GF-4" | Add `classify.py:345`, `probes.py:49`, `report.py:545`, `run.py:868` |
| F-M9 | MINOR | 13.1 row C pitfalls | The privacy test also applies `FORBIDDEN_WORDS` (test_snapshot_schema.py:283-293: `prompt`, `credential`, `password`, `secret`, `token`, `worktree`, `terminal handle`, `stage.detail`, `stage.activity`) as a substring check over the whole lowercased snapshot text, so a new key or value containing one of them fails; the document lists only key names | Add one sentence naming `FORBIDDEN_WORDS` |

## Actions Taken
None. fix_authorization was false; the document was not modified. Only this report was written.

## Self-Audit

**(a) Reliance list - rf-qa PASS items skipped for structural re-check:**
- None. The spawn prompt carried no `## Inherited Structural Verdict` section, so standalone behaviour applied and nothing was skipped on the strength of an rf-qa PASS.

**(b) Independent semantic checks (>=1 required, INV-019):**
- Scenario A steps executed against the sweep code: read classify.py:30-60, 340-390, 945-985, models.py:45-75, report.py:20-80, 540-558 and the test tables; confirmed the unpack, KeyError, `CLASSES[5]`/`[7]`, `NEXT_INSPECTION` fallback and `idle`/`person_active` suffix claims.
- Scenario D key step executed against `keys.py` and `view.py:134-148`: found that a non-text key needs a decoder edit the document does not name (F-1).
- Scenario D pitfall tested against `render.py:1263-1272` and `terminal.py:82-89`: found the "only a refusal line prints" statement is incomplete (F-M3).
- Section 9 values compared with `config.json`, `waker.py:56-62`, `common.py:28-51`, `cycle.py:58-69, 216-220` and `test_agent_work_report.py:2979-3002`: found the time-string and `orchestrator_repo` imprecisions (F-M6, F-M7).
- Section 13.2 counts (24 negative argv, 22 + 17 rejected shapes, 135 render tests, backoff list) counted from the test files.

1. Factual claims independently verified against snapshot code: about 120 (every file, function, constant, line range and test name cited in 13.1 rows A to E, the skeletons, the 13.2 table and the Section 9 tables).
2. Files read: sweep/{classify,models,report,probes,commands}.py; observe/{adapter,parse,collector,export,view,render (cited ranges),terminal,theme,keys,commands}.py and snapshot.schema.json; skills/agent-work-report/{SKILL.md,config.json,scripts/{run,exclude,common,clickup,prefs,waker,match,classify}.py}; issue_watch/cycle.py; tests/sweep/{test_classify,test_report,test_cli_contract,test_probes_allowlist,test_readonly}.py; tests/observe/{test_render,test_snapshot_schema,test_session,test_adapter,test_collector,test_golden_contract}.py; tests/skills/test_agent_work_report.py; design package render.py; .gitignore.
3. Findings exist (1 blocking, 9 minor), so the "zero issues" question does not arise; the clean results (scenarios A, B, C, Section 9 flags and defaults, touch-point facts) are backed by the line-level reads above.
4. No web research was performed; Tavily was not needed (all checks were local).

## Confidence Gate

- Items (this lens): 11 = Scenario A, B, C, D, E; pitfalls reflect real constraints; Section 9 configuration exact; how-tos followable without other documents; criteria testable; unification touch points are facts; 13.2 real test files.
- **Confidence:** Verified: 11/11 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (10 items PASS, 1 item FAIL on a verified defect)
- **Tool engagement (approximate counts):** Read: about 85 | Grep: about 42 | Glob: 4 | Bash: 1
- Tool-engagement minimum met (Read + Grep + Glob = about 131, above 11 items).
- Limits: nothing was run; `.dev/`-only files on origin/master (release-gates records) were not needed for this lens and were not read; the design-package renderer was read at the checkout path, not executed.

## Verdict

**Overall Verdict: FAIL** (1 blocking finding, F-1; 9 minor notes). Resolving F-1 is a two-sentence edit to Section 13.1 row D (and the matching 5.2 convention line); the minor notes do not need a fix pass.

## Recommendations
- Fix F-1 before the document is released; it is the only finding that makes a documented extension step fail as written.
- F-M3, F-M4, F-M5 and F-M7 are cheap to fold into the same edit but are optional.

## QA Complete
