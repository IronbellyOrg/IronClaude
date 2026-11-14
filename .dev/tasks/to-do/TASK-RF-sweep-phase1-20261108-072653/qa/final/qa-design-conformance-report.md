# QA Report - Final gate, design-conformance lens

**Task:** TASK-RF-sweep-phase1-20261108-072653 (T316)
**Date:** 2026-11-12
**Phase:** final gate, design-conformance lens
**Fix authorization:** false (report only)

## Scope and method

Lens: design conformance. Source of truth: `docs/designs/orchestrator-mode.md` as revised (read: sections 3, 6, 7.1 to 7.6, 8, 9, 10, 11, 17/18 tail and the scoped addendum pointer at lines 1049-1051) plus `revisions/chat-output-exception-20261109-133150/design-addendum.md`. Code and docs read from disk now, in chunks of at most 150 lines. Experiments ran only on private copies under `/tmp` (deleted by an exit trap; I confirmed my directory is gone). I ran no live Orca, ccsession or Claude command, and did not run `make sync-dev`.

Commands I ran and what they returned (this session):

| Command | Result |
|---|---|
| `uv run pytest tests/sweep tests/commands/test_sweep_command.py tests/core tests/recommend tests/commands/test_routing_plugin_parity.py -q -p no:cacheprovider` | 1123 passed |
| `uv run pytest tests/skills -q -p no:cacheprovider` | 1896 passed |
| `uv run ruff check` and `ruff format --check` on `src/superclaude/cli/sweep`, `main.py`, `tests/sweep`, `tests/commands/test_sweep_command.py` | All checks passed; 17 files already formatted |
| `make verify-sync` | All components in sync |
| `cmp src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` | identical |
| WC-16 paragraph in `WORKER-CONTRACT.md:277` against DESIGN `orchestrator-mode.md:679` (`cmp`) | byte identical |
| Mutation batch on a private copy of `sweep.md`, `SKILL.md`, `pragmatic.md` and `test_sweep_command.py` (9 cases) | base 121 passed; 8 of 9 mutations caught by a named test; mutation m9 (argument-hint shortened) was not caught (finding F8, MINOR) |

Departure rule applied: a departure is a place where the code or text contradicts a name, signature, constant, field list, order or sentence the DESIGN states. Items the code adds without contradicting any stated name are graded by the severity rule (wrong behaviour, false claim, missing deliverable, security or data-loss risk is blocking). Where this grading is a judgment call I say so in the finding.

## What conforms (evidence)

- **Module surface (C1, C2).** Every name in DESIGN 7.1 exists in the module the DESIGN gives. `probes.py`: `Budget` (`:108-185`, defaults 50, 90.0, 10.0, `time.monotonic`), `OrcaResult` (`:96-102`), `BindingError` (`:88`), `GitCallFailed` (`:84`), `orca_binary` (`:191`), `check_orca_argv` (`:203`), `check_git_args` (`:218`), `_orca` (`:243`), `_git` (`:289`), `bind_run` (`:352`), `parse_time` (`:368`), `parse_worker_show` (`:413`), `collect` (`:1240`), `read_worktree` (`:978`), `parse_status` (`:491`), `read_packages` (`:677`), `read_ledger` (`:603`), `read_contract` (`:767`), `read_transcript_tail` (`:849`), `read_tab_map` (`:882`), `read_orca_version` (`:887`). `classify.py`: `Rule` (`:154-157`, frozen), `RULES` (`:337`), `classify` (`:361`), `policy_of` (`:381`), `package_state` (`:415`), `mark_shared_packages` (`:424`), `safe_to_close` (`:471`), `removable` (`:447`), `classify_all` (`:867`). `report.py`: `CHECKED_ORCA_VERSION = "1.4.245"` (`:23`), `CELL_MAX = 200` (`:24`), `SECTIONS` (`:523`), `sanitize` (`:547`), `cell` (`:580`), `render` (`:586`), `to_json` (`:591`). `commands.py`: `sweep_group` (`:214-216`), `run(run_ids, window, root, output)` (`:242`), `_parse_window` (`:43`), `_find_root` (`:64`), `_check_output` (`:99`), `_check_run_ids` (`:87`), `_publish(text, output_dir, now) -> Path` (`:153`). Nothing named in 7.1 is missing or renamed.
- **Frozen dataclasses (C3, C4).** All 15 types in `models.py` are `@dataclass(frozen=True)`; `SweepInput` fields are in the DESIGN's order (`models.py:215-227`); `TranscriptTail` carries `first_record_ts` and `tail_complete` (`:114-116`); `OrcaObservation` carries `session_join`, `dispatch_started`, `dispatch_ended`, `dispatch_status` (`:69-74`); `WorktreeState` carries `upstream_note`, `removable`, `removable_reason` (`:184-187`); `ClassifiedRow` is `row, classification, policy, safe` (`:232-236`, builder decision OQ-14). `JSON_SCHEMA_VERSION = 1`, `CLASSES` (8 names, DESIGN order), `PACKAGE_STATES` (6, precedence order), `SAFE_VALUES` (`models.py:17, 31-52`).
- **Rule table (C5).** `RULES` has the 9 names in DESIGN order (`classify.py:337-347`). Rule 5 holds the four conditions one per line (`:250-258`). Rule 1 notes (`:160-187`), rule 2 note (`:190-207`), SP-26 future-timestamp note (`:373-374`) and the join-outcome override that replaces rules 1 to 8 with `fallback` (`:350-358`, `:947-948`) match 7.2.
- **Allowlist (C6).** `ALLOWED_ORCA` has exactly the 10 templates in the DESIGN order (`probes.py:47-58`), `FORBIDDEN_TOKENS` (`:60`), `ALLOWED_GIT` (`:63-65`), `ORCA_VERSION_FILE` (`:67`), `OUTPUT_LIMIT`, `CONTRACT_LIMIT = LEDGER_LIMIT`, `LEDGER_SPLIT`, `TRANSCRIPT_TAIL`, `WORKER_LIST_PAGE` (`:69-73`) have the DESIGN values. `_git` prepends `git --no-optional-locks -C <cwd>` and sets `GIT_OPTIONAL_LOCKS=0` (`:296-297`). No write verb appears as a string in the package (grep for the FR-021 verbs as quoted tokens: only JSON key lookups `"dispatch"` match).
- **JSON v1 and report layout (C7, C8).** `to_json` builds the DESIGN 7.4 key set at every level (`report.py:597-673`); the saved live-check JSON has exactly the 12 top-level keys. `SECTIONS` is 12 functions in the DESIGN order (`report.py:523-536`); the header lines, Sessions columns (ten dimensions, then Class, Rule, Evidence, Safe to close, Notes, Next inspection, `:396-405`), `Report complete` footer (`:518-520`) match 7.5.
- **Impure shell and boundaries (C9, C10).** `_publish` follows DESIGN 3.2 step for step (`commands.py:153-208`: stem, `makedirs`, escape check, `O_EXCL` temp, write plus `fsync`, `os.link` loop to `-99`, post-commit unlink failure exits 1 with `could not remove temp file`). `sys.exit` appears only at `commands.py:281, 285, 288`, all inside `run`. `subprocess` is imported only in `probes.py:15`. File writes and `os.link`/`os.unlink`/`os.makedirs` appear only in `commands.py`.
- **Lazy `__getattr__` (C11).** `__init__.py:4-9` returns `sweep_group` from a lazy `from .commands import ...`; `tests/sweep/test_cli_registration.py:48-69` drops the package and `commands` from `sys.modules`, imports the package, asserts `commands` is absent, then reads `sweep_group` and asserts it is present.
- **Registration (C12).** `main.py:567-569` adds the deferred import and `main.add_command(sweep_group, name="sweep")` after the `issue-watch` pair (`:563-565`) and before `if __name__ == "__main__":` (`:572`), with the same `# noqa: E402,I001 # intentional: deferred subcommand registration` comment as its neighbours.

- **Command and skill surface, DESIGN 7.6 (C13, C14).** `sweep.md:9` is `allowed-tools: Skill`; `:8` carries the DESIGN `argument-hint`; headings are title, Triggers (`:20`), Usage (`:24`), Options (`:33`), Activation (`:44`); the Activation block names `~/.claude/skills/sc-sweep-protocol/SKILL.md` (`:51`) and the project copy `.claude/skills/sc-sweep-protocol/SKILL.md` (`:55`); no `## Unattended mode`; no `src/superclaude` substring in either file (grep count 0). `SKILL.md:4` is the exact `allowed-tools` literal; steps 1 to 5 (`:23-27`) are PATH-first, `command not found`-only fallback with `--frozen --no-sync`, timeout 120000 ms on both runs, only `report_path` and `summary` taken, Read of the report in chunks of at most 150 lines, exit 1/2 prints stderr and ends. The 12 original 7.6 assertions exist as tests (`tests/commands/test_sweep_command.py:106-170`).
- **Addendum conformance, style (C15).** `git diff <base> -- pragmatic.md` shows five hunks only. The mandatory-table bullet now names the one exception and keeps placement (`pragmatic.md:22`), followed by exactly four sub-bullets (`:23-26`) carrying the eligibility rule (assignment, loaded skill, exit 0, JSON parsed, report Read), what establishes the assignment, what stays ordinary, and scope. "Except for the sweep chat-summary exception above," qualifies exactly the six later obligations (Status and wrap-ups, template introduction, Simple, Normal, Wrap-up, Multi-point); the templates introduction says the templates and examples are for non-exempt replies. Work-discipline and severity text is untouched (the test `test_style_exception_does_not_leak_into_work_discipline` and the diff agree). The exception is a loaded-instruction contract and names no detector.
- **Addendum conformance, skill and test (C15).** `SKILL.md:31-51` states the same eligibility rule, the positive and negative cases (independently assigned coordinator, direct assignment plus separate request, peers and files never assign, unknown or conflicting role means ordinary), final-reply-only scope, and the chat-presentation-only limit. `tests/commands/test_sweep_command.py` pins the clauses in both texts (parametrized `_PIN_PARAMS`, lines 423-429), the six qualified sites (`:617-622`) and the primary rule (`:559-571`). Mutation evidence: dropping `exit 0` from the skill or the style, weakening `top-level session`, removing the peer/file clause, removing a qualifier, changing the timeout, and removing `workers or subagents` each failed a named test.
- **WC-16 and never-as-worker, DESIGN 8 (C16).** WC-16 is at `WORKER-CONTRACT.md:275-277`, byte-identical to the DESIGN fenced block, and carries the owner-approved opening "On every coordinator wake or wait timeout" (decision `OQ-3-addendum-wc16-wait-timeout-decision.md:21`). `sweep.md:22` carries the 5-minute cap with the WC-16 pointer (the owner record calls it "line 20"; the same sentence now sits on line 22 because the file gained lines, and the words match the approved text). The never-as-worker line has `/sc:sweep` in the DESIGN order (`WORKER-CONTRACT.md:23`). The five pins in `tests/skills/test_worker_contract.py` are present: `WC-16` entry after `WC-15` and before `heartbeats`, `/sc:sweep` appended to `NEVER_AS_WORKER`, the rename to `...names_every_listed_command`, `assert "sweep" not in UNATTENDED_COMMANDS`, and the changed `never-as-worker` phrase.
- **Routing and docs, DESIGN 9 and 10 (C17, C18).** R1 row after `/sc:spawn` and R2 bullet in `HOW-WE-WORK.md`, R3 byte copy, R4 `_OTHER_COMMANDS`, R5 `_POST_REFRESH_ADDITIONS`, R6 row after `/sc:issue`, R7 developer-guide list, R8 CHANGELOG topic heading with `#### Added (sweep)`, and the two `.gitignore` lines after `.dev/sprint-state/` are all present with the DESIGN's wording. `git check-ignore` confirms `.dev/sweeps/x.md` is ignored and `.dev/tasks/to-do/x.md` is not. Nothing under `.claude/` is staged.
- **Test plan, DESIGN 11 (C19).** All 29 test functions the DESIGN names (the seven `test_fr010_*`, the fifteen `test_path_b_*`, the three `test_read_transcript_tail_*`, the three `test_worker_show_dispatch_times_*`, `test_collect_worker_list_source_rows_and_truncated`) exist exactly once under `tests/sweep/`. The six test files plus `conftest.py` and `__init__.py` exist (the DESIGN's "seven new files" counts `conftest.py`).
- **Phase 14 evidence and the three full-run failures (C20).** My re-runs match `phase14-sync.md`, `phase14-lint.md` and the scoped pytest records. I checked the argument in `phase14-full-pytest.md` instead of trusting it: `git diff <base> --stat -- tests/cli/eval tests/hooks src/superclaude/hooks src/superclaude/cli/eval` prints nothing, so this change touches none of the three failing areas; `tests/cli/eval/test_claude_process_adapter.py:437` and `:468` launch `sys.executable -m ruff`, which fails when the venv has no `ruff` module (environment cause); the third is a timing test (`test_speed_large_commands[1MB-big]`) in an untouched hook suite. The argument holds. I did not re-run those three tests because the lens allows only the sweep, commands, core, skills and recommend folders.
- **pipx check, owner option (A) (C21).** `OQ-10-pipx-decision.md:20-23` records the owner's "go with A". `artifacts/sweep-help-pipx.txt` shows `pipx run --spec <worktree>` printing the `sweep` group help with exit 0, and the installed tool is unchanged.
- **Saved live check (C23).** `artifacts/sweep-live-check-1.4-rerun-9.14.json`: exit 0, 71 source rows, none unscanned, 12 top-level keys equal to DESIGN 7.4, `total_is_lower_bound` true. All 182 rows are `could not determine` by rule `fallback` (see F6).

## Findings

No BLOCKING or MAJOR finding. Nine MINOR findings follow (notes; they never fail the gate). F1 and F5 are the two where the grade is a judgment call, and I state the reasoning so the lead can overrule it.

### F1 (MINOR): three model fields the DESIGN field tables do not list

- **Evidence:** `src/superclaude/cli/sweep/models.py:103` (`ContractRecord.mtime`), `:90` (`OrcaObservation.agent_wait_since`), `:147` (`SessionRow.freshness_age_s`), and four extra constants `CONTRACT_FILE`, `REPORT_DIR_RE`, `SHOW_CAP_REASON`, `TIME_BUDGET_REASON` at `:21-29`. DESIGN `orchestrator-mode.md:451` says the design "keeps every SPEC field and adds only the items marked (design)"; the 7.2 tables (`:453-468`) and the constants sentence (`:472`) do not list these.
- **What is wrong:** the code adds fields and constants that DESIGN 7.2 does not name, against its own "adds only" sentence. No owner decision or OQ-14 covers `mtime` and `agent_wait_since`. OQ-11 covers the dimension fields (`freshness_age_s` is the Freshness dimension's age).
- **Why MINOR (judgment call):** `mtime` and `agent_wait_since` carry the two inputs of the Waiting (a) age that SPEC line 238 (`merged-requirements.md:238`, SP-15) requires and that DESIGN 7.5 (`:642`) sorts by; a pure `render` cannot sort by age without them, so the DESIGN omitted a needed field rather than the code contradicting one. No stated name, signature or order is changed. If the lead reads "adds only the items marked (design)" strictly, F1 becomes BLOCKING.
- **Smallest fix:** add the three fields and the four constants to DESIGN 7.2 marked (design). No code change.

### F2 (MINOR): extra optional parameters and widened annotations versus DESIGN 7.1

- **Evidence:** `probes.py:129-131` `share_shows(runs, wanted=None)` (DESIGN `:368` shows `(runs)`); `probes.py:603`, `:767`, `:849` add `root: Path | None = None` to the three readers (DESIGN `:398-400` shows `(path)`); `__init__.py:4` has no `-> object` and `:12` adds `__all__` (DESIGN `:360`); `report.py:547` and `:580` take `text: object` (DESIGN `:429-430` says `str`); `report.py:523` has no type annotation (DESIGN `:428`).
- **What is wrong:** signatures differ from the DESIGN text in ways that are backward compatible; the `wanted` parameter is what makes "2 Runs of 40 rows get 25 each" and `min(D, 50)` (DESIGN `:303`, `:341`) work.
- **Smallest fix:** note the extra parameters and the widened types in DESIGN 7.1, or narrow them in code.

### F3 (MINOR): a third per-Run source row

- **Evidence:** `probes.py:1067-1069, 1085-1088` writes `orca task-list --ready <run>` as its own source row; DESIGN `:597` names two rows per Run (`orca worker-list <run>` and `orca task-list <run>`). The call count `1 + 3R + 1 + 50` (DESIGN `:298-301, :340`) already includes the ready call.
- **What is wrong:** the row set is one larger than DESIGN 7.4 says. `classify._origin_unknown` reads only the first two names, so no behaviour changes.
- **Smallest fix:** name the third row in DESIGN 7.4.

### F4 (MINOR): `OrcaResult.data` is the envelope's `result`, not "parsed JSON"

- **Evidence:** `probes.py:99-101` and `:285` (`OrcaResult("ok", parsed["result"], None)`); DESIGN `:377` comment says "parsed JSON for ok".
- **What is wrong:** wording only; the code matches the captured fixtures.
- **Smallest fix:** align the DESIGN comment.

### F5 (MINOR): the skill prints a mark and a lower-bound sentence that the DESIGN and the addendum do not state

- **Evidence:** `SKILL.md:26` (step 4: print `(not observed in Phase 1)` after the stalled and fenced counts and say the total is a lower bound) and `SKILL.md:43` (the exempt reply keeps the mark). DESIGN 7.6 `:662` says "print the counts from `summary` and the report path"; the addendum (`design-addendum.md:13`) says the exempt reply "contains the summary counts and report path"; `pragmatic.md:23` does not mention the mark. The mark came from docs-gate fix DOC-F2 (`TASK-RF-sweep-phase1-20261108-072653.md:3010`, which already lists "style does not mention the mark" as a Medium follow-up).
- **What is wrong:** the skill's exempt reply has two more elements than the style and the addendum describe. It contradicts neither text and adds no advice, so the reply stays inside "counts and path"; but the two normative texts are not identical on what the reply holds.
- **Why MINOR (judgment call):** additive, serves the DESIGN's own D7 footnote purpose (`orchestrator-mode.md:834`), and no sentence of the DESIGN or addendum forbids it. If the lead treats every unlisted element of the exempt reply as a departure, F5 becomes BLOCKING.
- **Smallest fix:** add one clause to `pragmatic.md:23` (and its test pin) saying the counts keep the `(not observed in Phase 1)` mark, or drop the mark from `SKILL.md:26, :43`.

### F6 (MINOR, follow-up candidate): rule 5 cannot match live Orca data, and the report's Phase 1 caution names only stalled and fenced

- **Evidence:** `probes.py:431` and `:433` fill both `dispatch_status` and `status` from `dispatch.status`; `classify.py:250-258` needs `status == "in_progress"`; `1.0a-facts.md:16` records that `status` is `completed` on all rows, that `in_progress` is not one of the dispatch status values, and that `agentWait` is absent from all `worker-show` output. The saved live check classifies 182 of 182 rows `could not determine` (`artifacts/sweep-live-check-1.4-rerun-9.14.json`, `summary.counts`). DESIGN `:629` and `:834` (D7) and `report.py:36-39` say only "Stalled and fenced are not observed in Phase 1".
- **What is wrong:** `working` is as unobservable live as stalled and fenced, but the report and the skill warn only about the other two, so `working: 0` can be misread. The code follows the DESIGN text here (not a departure); the gap is in the DESIGN's D7 wording and is not in `followups.md` (24 lines, no match for `working`, `in_progress` or `rule 5`).
- **Smallest fix:** add `working` to the SP-24 line, or log it in `followups.md` as a follow-up.

### F7 (MINOR): `N = D + U` does not hold when ready Tasks exist

- **Evidence:** `probes.py:1168-1179` turns each ready Task that has no worker row into an `OrcaObservation` and so into a session row `orca:<task id>`; DESIGN `:326, :344` states `N = D + U` with D "distinct Dispatch rows returned by `worker-list`".
- **What is wrong:** the rows-equal-D-plus-U statement is not exact; DESIGN 7.5 (`:642`) and rule 4(b) need ready Tasks as rows to list them in Waiting (b), so the code is right and the count sentence is loose.
- **Smallest fix:** state `N = D + U + ready Tasks` in DESIGN section 6.

### F8 (MINOR): no test pins the command's `argument-hint`

- **Evidence:** `sweep.md:8` carries the DESIGN string (`orchestrator-mode.md:655`); grep for `argument-hint` in `tests/commands/test_sweep_command.py` and `tests/sweep/` finds none; mutation m9 (argument-hint cut to `[--run <id>]`) left all 121 tests passing.
- **What is wrong:** the DESIGN's 7.6 test list (`:666`) does not require this pin, so this is a coverage gap only.
- **Smallest fix:** one equality assertion on `_frontmatter(_COMMAND)["argument-hint"]`.

### F9 (MINOR): the over-limit ledger read touches only the tail

- **Evidence:** `probes.py:573-585` seeks to `size - LEDGER_SPLIT` and reads the tail only; DESIGN `:62` (GQ-105) says "the head 512 KiB and the tail 512 KiB are read and the tail is searched", and `:398` repeats "head 512 KiB + tail 512 KiB".
- **What is wrong:** the head is never read. Because only the tail is searched, the result is identical; the DESIGN sentence describes a read that has no effect.
- **Smallest fix:** reword the DESIGN to "the tail 512 KiB is read and searched".

## Limits of this review

- I read `probes.py` lines 1-460, 450-600 (signatures and parsers), 772-1030, 1030-1240 and 1240-1392, `classify.py` lines 150-505 and 824-996, `report.py` lines 1-75, 120-366 and 364-673, and all of `models.py`, `commands.py` and `__init__.py`. I did not read line by line: `probes.py:600-770` (package, ledger and contract readers), `classify.py:1-150` and `:505-824` (note constants, dispatch merge and the transcript-join logic), and `report.py:75-120`. For those regions I checked names and signatures by grep and relied on the passing tests (1123 plus 1896) for behaviour; join and window behaviour is not this lens's subject.
- I did not run the three failing full-run tests (outside the allowed folders); I checked the diff and the code path that explains them.
- Mutation experiments covered the command, skill and style pins only. I did not mutate `.py` code.
- Wording tests prove the clauses are present in the texts; they do not prove a live model follows them (the addendum says the same, `design-addendum.md:37`).

## Checks

| Check | What it covers | Result |
|---|---|---|
| C1 | DESIGN 7.1 names present in the right modules (probes, classify, report, commands, `__init__`) | PASS |
| C2 | DESIGN 7.1 signatures and defaults (Budget, OrcaResult, seams, readers, classify, report, commands); F2 and F4 are MINOR notes | PASS |
| C3 | DESIGN 7.2 frozen dataclasses, field names and order; OQ-11 and OQ-14 decisions; F1 is a MINOR note | PASS |
| C4 | `models.py` constants and tuples (`JSON_SCHEMA_VERSION`, `CLASSES`, `PACKAGE_STATES`, `SAFE_VALUES`) | PASS |
| C5 | `RULES` order and names, rule 5 four conditions, rule 1 and 2 notes, SP-26, join-outcome override | PASS |
| C6 | DESIGN 7.3 allowlist (10 templates, `FORBIDDEN_TOKENS`, `ALLOWED_GIT`, limits, id regexes, no write verb string) | PASS |
| C7 | DESIGN 7.4 JSON v1 key set at every level; F3 is a MINOR note | PASS |
| C8 | DESIGN 7.5 `SECTIONS` order, header lines, Sessions columns, `cell`, `sanitize`, footer | PASS |
| C9 | `commands.py`: exit mapping, `_publish` against DESIGN 3.2, `sys.exit` only in `run` | PASS |
| C10 | Module boundaries: `subprocess` only in `probes`, writes only in `commands`, `classify` and `report` import purity | PASS |
| C11 | Lazy `__getattr__` and its test | PASS |
| C12 | `main.py` deferred registration after the `issue-watch` pair | PASS |
| C13 | DESIGN 7.6 command and skill surface (frontmatter, headings, Activation, steps, literals) | PASS |
| C14 | DESIGN 7.6 test pins and mutation evidence; F8 is a MINOR note | PASS |
| C15 | Scoped addendum: style edit, skill text, test coverage; F5 is a MINOR note | PASS |
| C16 | DESIGN 8: WC-16 byte identity, owner-approved edits, never-as-worker, five pins | PASS |
| C17 | DESIGN 9: rows R1 to R8, plugin byte copy, parity tests | PASS |
| C18 | DESIGN 10: `.gitignore` lines and ignore behaviour | PASS |
| C19 | DESIGN 11: test files and the 29 named tests exist | PASS |
| C20 | Phase 14 evidence re-run, and the argument for the three full-run failures checked | PASS |
| C21 | OQ-10 pipx option (A) record and `sweep-help-pipx.txt` | PASS |
| C22 | Scan for departures not covered by an owner decision or OQ-11 / OQ-14 (F1 to F9 all graded MINOR; see grading notes on F1 and F5) | PASS |
| C23 | Saved live-check JSON against the DESIGN 7.4 key set (no live run); F6 is a MINOR note | PASS |
| C24 | Caller-liveness of design-stated interfaces: `WorktreeState.frozen` now set by `classify_all` (`classify.py:927-935`), `removable` reads it (`:457`); rule 5 reachability is F6 | PASS |
| C25 | No `.claude/` path staged, `.dev/tasks/` not ignored, private `/tmp` copies removed | PASS |

Confidence: Verified: 25/25 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (over this lens's checklist; the unread regions listed under "Limits of this review" are outside the checklist and are named, not hidden).

Tool engagement: Read: 48 | Grep: 18 | Glob: 3 | Bash: 19 (my own tally; Bash includes the pytest, ruff, verify-sync, mutation, cmp and git diff runs listed above). No web research was performed.

Self-audit: a reader told "no BLOCKING finding" can point to the byte-identical WC-16 `cmp`, the 1123 plus 1896 passing tests, the style diff with exactly five hunks, the nine-case mutation batch (8 caught, 1 reported as F8), the grep that confines `subprocess` and file writes, and the line-level reads cited per check. The two grading judgment calls (F1, F5) are named, and I give the flip condition for each.

Verdict: PASS

Blocking count: 0

