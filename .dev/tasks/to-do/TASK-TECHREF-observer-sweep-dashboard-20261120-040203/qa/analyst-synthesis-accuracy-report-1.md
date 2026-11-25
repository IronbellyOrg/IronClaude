# Synthesis Accuracy and Source-Tracing Review (Partition A)

**Status:** Complete (verdict FAIL, 1 blocking finding)
**Analysis type:** synthesis-quality
**Date:** 2026-11-20
**Assigned files:** synth-01-overview-architecture.md, synth-02-directory-dataflow.md, synth-03-subsystem-observer.md, synth-04-subsystem-sweep.md
**Fix authorization:** false (report only; no synthesis file was modified)

## Method

Paths: TD = `/home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-observer-sweep-dashboard-20261120-040203`, SNAP = `/home/coder/.cache/ic-snap-20261120/master` (origin/master 61ac2c2e6), PKG = `/home/coder/workspaces/IronClaude/.dev/design/orca-observer-20261106`. Research cites are `R01`..`R06` (`TD/research/0N-*.md`), `GF1`..`GF5` (`TD/research/gapfill-c1-GFn-*.md`), `gaps` (`TD/gaps-and-questions.md`) with the line number in that file.

Every assigned file was read in full. Tracing used Grep over `TD/research`, `TD/gaps-and-questions.md` and `TD/qa/qa-research-consolidated-findings.md`; a hit counts as "traced" only when the matched line states the same fact. Citations were checked by reading the cited snapshot lines (batched read-only `sed`/`awk`/`grep`/`wc`, plus read-only `git show origin/master:<path>` for `.dev/` files that exist only on origin/master, and one read-only `gh issue view 590 --repo IronbellyOrg/IronClaude`). Nothing was run or modified. Where a synthesis statement rests on the snapshot rather than on a research line, the "Source" cell says "snapshot recount".

## Traced-claims table

Result key: T = traced to a research line that states the same fact; T+ = traced and also confirmed against the snapshot; MISMATCH = the snapshot contradicts the synthesis.

### synth-01-overview-architecture.md (38 claims)

| # | Claim in synth-01 | Source | Result |
|---|---|---|---|
| 1 | Package says "not a production integration"; 20 synthetic designs | R06:60 | T |
| 2 | 406 files (412 with 6 `.pyc`) | R06:16; PKG recount 406 / 412 / 6 | T+ |
| 3 | 360 exports, 2 galleries, 2 PDFs, 18 scenarios + base | R06:18, 30; PKG: 60 files per width per batch, 18 scenario files, 2 PDFs | T+ |
| 4 | `Pillow==13.0.0`, `wcwidth==0.9.4` | R06:23; PKG `requirements.txt:1-2` | T+ |
| 5 | `ARCHITECTURE-SPINE.md:172` code-reuse ban | R06:45; `git show` line 172 of `.dev/issues/409/bmad/spec-orca-observer/ARCHITECTURE-SPINE.md` | T+ (directory not named, see N-9) |
| 6 | `stack.md:3` stack CONFIRMED 2026-11-08 | R06:201; `git show` line 3 | T+ |
| 7 | `owner-decisions-20261108.md:5-9` "Stage it" | R06:72; `git show` lines 5-9 | T+ |
| 8 | DIRECTION-SELECTED passed 2026-11-16 | R06:290; `release-gates.md:10` | T+ |
| 9 | Issue #590: 263 of 264 rows `could not determine` | R03:277; `gh issue view 590` body | T+ |
| 10 | 2026-11-12 live run: 180 of 180 rows `could not determine` | R03:276 | T |
| 11 | Observer inherits 9 of 9 fixture names, 0 of 10 fixture contents; 3 of 20 designs have a counterpart | R06:48, 100 | T |
| 12 | `SKILL.md:194` "never starts or messages agents" broader than `waker.py` (G-20) | gaps G-20; snapshot `SKILL.md:194` | T+ |
| 13 | `orchestrator-mode.md:27` "does not exist yet" (SD-06) | gaps SD-06; snapshot line 27 | T+ |
| 14 | Page server serves the whole `.dev/coordinator/` folder | R05:591; gaps G-22 | T |
| 15 | FR-9: 8 states, mapping not stated | GF3:94 | T |
| 16 | About 30 verb forms; 4 equal a sweep template token for token; none an observer template | GF3:84 | T |
| 17 | 15-step pipeline | R05:464 | T |
| 18 | PR #684 merged 2026-11-20 | R05:363; GF3:202 | T |
| 19 | PR #681 (1,412 lines), D #682, C #684 merged; A #686, P #690 open; B none | GF3:189, 199; R05:366 | T |
| 20 | PR #539 merged 2026-11-14 | R06:199; GF3:196 | T |
| 21 | U-40 no owner for "source mapping" | gaps U-40 | T |
| 22 | C8 identifiers C8-6 (writer), C8-7 (`orchestrator_repo`), C8-9 (D-1) | gaps headings C8-1..C8-9 (lines 168-231 and after) | T |
| 23 | 28 drift guards in `tests/commands/test_sweep_command.py` | R04:162; snapshot recount 28 | T+ |
| 24 | 20 of 31 row attributes exported | R01:212; `parse.py:58-90` holds 31 entries | T+ |
| 25 | HELP says "It never writes to Orca" | R01:156 | T |
| 26 | Observer uses `rich.live.Live(screen=True)` | R02:59 | T |
| 27 | Package/live body still name Bubble Tea (SD-25) | R06:201; gaps SD-25 | T |
| 28 | No code reads a published sweep report (G-17) | gaps G-17; R04:297 | T |
| 29 | Owner accepted the non-owner-read gap on 2026-11-12 | R01:343 | T |
| 30 | 6 of 8 sweep classes can print on live data | R03:80 | T |
| 31 | 13 forbidden prefixes | R01:27; `adapter.py:34-50` holds 13 | T+ |
| 32 | `QA.md` verdict FAIL for pre-correction snapshots, no later verdict | R06:66; PKG `QA.md:19` | T+ |
| 33 | Sweep binary: `$ORCA_CLI_COMMAND` else `orca-ide` | R04:17; `probes.py` | T+ |
| 34 | No code links observer, sweep and report skill | GF3:165; R02:207 | T (composite of two greps) |
| 35 | "Observer reads the sweep JSON" is only an undecided proposal | R06:219-221 | T |
| 36 | STALE at 45 s on the monotonic clock | R01:241; `view.py:33-35, 456-463` | T+ |
| 37 | `projection.attention` present, not parsed | GF3:101; no `attention` in `parse.py` | T+ |
| 38 | File and line totals (13 `.py` 6,011 lines + 158; sweep 3,759; AWR 5,777; AWR test 4,005 lines / 142 defs; observer tests 26 files / 565 defs; sweep tests 7 files / 323 defs; 7 templates; 16 scripts) | snapshot recount (`wc -l`, `grep -c '^def test_'`) | T+ (all match) |

### synth-02-directory-dataflow.md (34 claims)

| # | Claim in synth-02 | Source | Result |
|---|---|---|---|
| 1 | Package content on master is identical (diff empty) | R06:55 | T |
| 2 | `.dev/research/orca-dashboard-20261105/` local-only, untracked | R06:3 | T |
| 3 | Fixtures: base + 9 variants, 4 golden, 4 golden-question, `question-cap-100` (19 JSON) | R06:35; snapshot listing | T+ |
| 4 | State path `$AWR_ROOT` else `orchestrator_repo` of the poll config, needs `repos.yaml` | R05:28; `common.py:29-48` | T+ |
| 5 | CC-02: master poll rejects `orchestrator_repo` | GF1:131; gaps CC-02; `cycle.py:216-220` (`_TOP_KEYS`), 0 hits for the key in `cycle.py` | T+ |
| 6 | Run folder `%Y%m%dT%H%M%SZ-<kind>` with `-n` suffix | R05:67 | T |
| 7 | Observer state dir and record names | R02:178; `export.py:236-244` | T+ |
| 8 | Package export suffixes incl. `.mono.png` | GF5:71 | T |
| 9 | Observer backoff 15 s to 60 s, interval 15 s | R01:116; `collector.py:28-34, 306, 321` | T+ |
| 10 | Orchestrator poll `*/5`, outside repo, UNVERIFIED; waves | GF3:13, 147 | T |
| 11 | `config.json` has 14 keys | gaps G-48 | T |
| 12 | Package pipeline: `exports(batch)` writes fixtures first; 160-wide PNGs feed sheet and PDF | GF5:26, 71, 181; PKG `render.py:41-74` | T+ |
| 13 | U-01, U-03, U-25, U-27, U-35 stay UNVERIFIED | gaps lines 22, 44, 54 | T |
| 14 | G-04 unbounded row retention | gaps G-04; `parse.py:654` | T+ |
| 15 | `JOIN_PATH = "B"` affects the guard only | R03 s4; `classify.py:40, 745` | T+ |
| 16 | Strict envelope `ShapeError` | R01:75; `parse.py:369-380` | T+ |
| 17 | `report_path` is the one unsanitized JSON string | R04:283; `report.py:82` comment | T+ |
| 18 | Sanitizer locations (observer, sweep, AWR x2, package) | R06; snapshot `sanitize.py:27-48`, `report.py:569-605`, `common.py:74-82`, `activity.py:40-54`, PKG `canvas.py:10-29` | T+ |
| 19 | Gate: sha256 chain; `close` enforces checks + sha only (CC-04) | R05:81; `run.py:204-368` | T+ |
| 20 | D-1 refusal (`--questions` with `--fixture`) | R06:229; gaps DC-02; `commands.py:77-78, 183-188` | T+ |
| 21 | Counts: 36 entries, 26 `test_*.py`, 19 fixture JSON; AWR 5,777 lines | snapshot recount | T+ |
| 22 | ClickUp: GET only plus one DM POST | R05; `clickup.py:39, 58-105` | T+ |
| 23 | Package `canvas.py`: sanitize then clip by display width | PKG `canvas.py:10-29, 38-55` | T+ |
| 24 | Package fixtures: no Orca adapter, environment or network | PKG `fixtures.py:1` docstring | T+ |
| 25 | Font path fixed in `render.py:16-18`, read at import | PKG `render.py:16-18` | T+ |
| 26 | `ALLOWED_ORCA` 49-60 (6 called, 4 pinned), `ALLOWED_GIT` 68-81 | R04; `probes.py:49-81` | T+ |
| 27 | Report exclude / match / classify / compare / entry-card line ranges | snapshot `exclude.py:59-103`, `match.py:119-247`, `classify.py:67-128`, `compare.py:84-186`, `render.py:194-303` (function boundaries read) | T+ |
| 28 | Question merge retention 1,000, key `(Run, message.id)` | R01; `questions.py:105-129` | T+ |
| 29 | Decision Desk join exact on `dispatch_id` | R02:139; `view.py:888-948` | T+ |
| 30 | Snapshot export 20 of 31, `export.py:141-216` | R01:212; snapshot | T+ |
| 31 | Sweep contract join, transcript join, `safe_to_close`/`removable` ranges | R03; `classify.py:570-591, 609-683, 455-504` | T+ |
| 32 | Sweep publish `commands.py:153-208` (temp file, `os.link`) | R04; snapshot boundaries | T+ (the `-99` limit not re-read) |
| 33 | Contradiction (3): only `CHANGELOG.md:170` gives the capture-gap reason | GF2; GF1 3.6; snapshot `CHANGELOG.md:170`, `commands.md:619-620` | T+ |
| 34 | Entry writer DESIGNED (PR B, no PR); `exclude.py` excludes nothing today | GF1 3.7; R05:351, 366 | T |

### synth-03-subsystem-observer.md (37 claims)

| # | Claim in synth-03 | Source | Result |
|---|---|---|---|
| 1 | PR #577: 11 cuts, 684 observe tests per body | R02:261 | T |
| 2 | PR #592: 762 observe tests per body; link guard; keys n/p/Esc | R02:262 | T |
| 3 | PR #514: `QUESTION_GATE_PASSED = False` at merge, retention 1,000 | R02:260 | T |
| 4 | File lists truncated at 100; #503 545 files, #673 2,831 files | R02:266; R06:56, 94; gaps G-10 | T |
| 5 | 13 forbidden prefixes, set may grow not shrink | R01:27; `test_adapter.py:178-192` asserts a 13-name superset | T+ |
| 6 | Three argv templates; question shape exactly 8 tokens | R01:369; `adapter.py:29-32, 111-118, 186-190` | T+ |
| 7 | 31 keys in `_FIELDS` | R01; `parse.py:58-90` recount 31 | T+ |
| 8 | 20 of 31 exported; 11 dropped (7 `resource.*`, 2 `workspace.*`, 2 `stage.*`) | R01:212, 354 | T |
| 9 | Limits: 10 s, 8 MiB, 2 KiB stderr, 2 s kill grace | R01; `adapter.py:58-63` | T+ |
| 10 | Question retention 1,000, window 100 | R01; `questions.py:21-22, 125-129` | T+ |
| 11 | STALE 45 s, `PARTIAL` shows as OK, `FAILED` never STALE | R01:148, 241; `view.py:456-463` | T+ |
| 12 | `write_atomic`: mkdir 0700, mkstemp, fsync, `os.replace`, temp unlinked | R02:178; `export.py:258-270` | T+ |
| 13 | Non-acknowledging read is UNVERIFIED; owner accepted 2026-11-12 | R01:343; gaps U-01 | T |
| 14 | Both gate constants True; tests pin them with a cited record | R02:162; `commands.py:67, 70`; `test_commands.py:756` | T+ |
| 15 | D-1 facts (refusal, `no-question-fixture`, only test hit `test_collector.py:675`) | GF1 3.8; `commands.py:77-78, 183-188`; `collector.py:125-129` | T+ |
| 16 | Exit codes 0/1/2 and their lines | R02:28-52; `commands.py:195-196, 264-268, 364-369, 377-387` | T+ |
| 17 | SIGTERM/SIGHUP give 143/129 | R02:77, 303; `keys.py:115-125` | T+ |
| 18 | Key map (j/k, d/u, /, h, e, m, n/p) | R02; `view.py:1257-1270` | T+ |
| 19 | Layouts A/B/C, minimum 3 question rows | R02:133; `render.py:939-942` | T+ |
| 20 | Desk text cut at 400 chars, 4 lines | R02; `parse.py:475` (`ASK_CAP = 400`), `view.py:111` (`DESK_TEXT_LINES = 4`) | T+ |
| 21 | Widths 160/116/80, min 80 columns and 8 rows | R02:113; `terminal.py:21-24, 82-89` | T+ |
| 22 | `_find_orca` order, 10 s probe, `orca-cli` topic; odd `topics` shape unhandled | gaps U-03; `install_user_setup.py:247-270` | T+ |
| 23 | SD-02 stale "UNVERIFIED until first live read" comment | gaps SD-02; `adapter.py:60-62` | T+ |
| 24 | SD-05 `test_keys_spike.py:3` docstring stale | gaps SD-05 | T |
| 25 | G-05 drops with no stated reason | gaps G-05; R01:354 | T |
| 26 | G-07 two gate tests need origin/master-only files | gaps G-07 | T |
| 27 | G-08 record names `run_93bfa00cae2b`, code accepts any valid id | gaps G-08; R02:243 | T |
| 28 | U-06 four-kinds rule, U-08 version placement | gaps U-06, U-08 | T |
| 29 | CC-01 "no option maps to an Orca call" loose | gaps CC-01; snapshot `cli-groups.md:42` | T+ |
| 30 | Post-release report counts "13 source files" | R02:223 | T |
| 31 | `release-gates.md:58` QUESTION-LINK status line recorded by agent on owner's chat "yes" | R02:251; `git show` line 58 | T+ |
| 32 | `golden_release1_records.json` "never regenerated" | R02:202; `test_render.py:658-683` | T+ |
| 33 | Fixtures: 19 JSON = 10 variants + 8 golden + `question-cap-100` | R06:35; snapshot listing | T+ |
| 34 | `tests/observe/` 36 entries, 26 `test_*.py`, `test_session.py` 27 tests | gaps; QA M-7; snapshot recount | T+ |
| 35 | Schema limits `counts` values to scalars, parser keeps nested JSON to depth 6 | R01:177; schema lines 46-52; `parse.py:279` | T+ |
| 36 | `SPEC.md:32` CAP-1 and `acceptance-tests.md:25` T7 | R06:231; GF1 3.8; `git show` lines | T+ |
| 37 | Consumers: `tests/observe` validate snapshots with `Draft7Validator` in `test_commands.py`, `test_snapshot_schema.py`, `test_export.py` | R02:210 | **MISMATCH** (finding B-1) |

### synth-04-subsystem-sweep.md (36 claims)

| # | Claim in synth-04 | Source | Result |
|---|---|---|---|
| 1 | 9 ordered rules and their names | R03:17; `classify.py:345-355` | T+ |
| 2 | Rule 5 four conditions; `dispatch.status` not tested | R03; `classify.py:251-269` | T+ |
| 3 | No producer for `worker_done_seen` / `fenced_evidence` (whole-snapshot grep) | GF1 1.3; my grep of `src/superclaude` outside `classify.py`/`models.py` found none | T+ |
| 4 | `agent_wait_since` never set | GF1 3.3; `models.py:111-112`; `probes.py:481` | T+ |
| 5 | SPEC:232, :106, :251 text | GF1 1.1; `git show` lines | T+ |
| 6 | DESIGN:493, :636, :841, :1003 | GF1 1.2; snapshot lines read | T+ |
| 7 | `CHANGELOG.md:170-171`, `commands.md:619-621` wording and staleness | GF1 1.4, 3.6; snapshot lines | T+ |
| 8 | DESIGN:27 "does not exist yet" CODE-CONTRADICTED | gaps SD-06; snapshot | T+ |
| 9 | 10 Orca templates, 7 verbs; 6 called, 4 pinned | R04; `probes.py:49-60` | T+ |
| 10 | Four git shapes; `--no-optional-locks`, `core.fsmonitor=false` | R04; `probes.py:65-81, 324` | T+ |
| 11 | Budget 50 shows / 90 s / 10 s | R04; `probes.py:129-131` | T+ |
| 12 | Byte limits proposed (8 MiB, 1 MiB, 512 KiB, 256 KiB) | R04; `probes.py:85-88` | T+ |
| 13 | Result kinds `ok`, `no_binding`, `unavailable`, `call_failed` | R04; `probes.py:114` | T+ |
| 14 | Orca version file path (fixed Linux path) | R04; `probes.py:83` | T+ |
| 15 | Exit codes 0 / 1 / 2 | R04; `commands.py:276-288` | T+ |
| 16 | JSON v1 has 12 top-level keys | R04; `report.py` `to_json` (12 keys counted) | T+ |
| 17 | 12 report sections | R04; `report.py:545-558` | T+ |
| 18 | Sanitizer and 200-char cell cut | R04; `report.py:569-605` | T+ |
| 19 | `_publish`: temp file, `os.link`, unlink | R04; `commands.py:153-208` | T |
| 20 | WC-16 text at `WORKER-CONTRACT.md:287-289` | R04:204; snapshot read | T+ |
| 21 | "The sweep." at `:110`; never-as-worker `:23`; WC-10 `:46` | R04; snapshot read | T+ |
| 22 | `HOW-WE-WORK.md:298, 359`; routing test `:33` | R04; snapshot read | T+ |
| 23 | `pragmatic.md:22-25` exempt reply | R04; snapshot read | T+ |
| 24 | `commands/sweep.md:16, 18, 22, 42, 70`; `SKILL.md:25, 51, 66` | R04; snapshot read | T+ |
| 25 | Test sizes (2397 / 100, 1534 / 61, 69 / 3, 276 / 10, 536, 1465 / 43, 637 / 28) | R04:158-162; snapshot recount | T+ |
| 26 | Real-git routes 1, 4, 5, 6, 6b, 2, 3, 8, 9 | R04:158; `test_git_config_hole.py` docstrings | T+ |
| 27 | 37 shared clauses + 15 skill-only pins | R04:162, 164; `_SKILL_ONLY_PINS` exists | T |
| 28 | Fixtures: 20 `captured-*.json` + `SOURCES.md` = 21 | R03; snapshot recount | T+ |
| 29 | `JOIN_PATH = "B"` at line 40, read once at 745 | R03; `classify.py:40, 745` | T+ |
| 30 | `_force_unknown` 358-366; second call of rules 1-2 at 378 | R03; `classify.py:358-378` | T+ |
| 31 | `safe_to_close` / `removable` never return `yes` | GF1 3.4, 3.5; `classify.py:455-504` | T+ |
| 32 | `report_path` unsanitized | R04:283 | T |
| 33 | Issue #590: 263 of 264 | R03:277 | T+ |
| 34 | Cadence "pinned as text" at `test_worker_contract.py:212-215` | R04:205 | T, but cites the wrong sentence (note N-1) |
| 35 | Overlap facts: 4 token-for-token matches, FR-9 8 states | GF3:84, 94 | T |
| 36 | Rule 6, 7, 8, 9 firing conditions and proving tests | R03 s1 table; `test_classify.py:791-800, 1385-1412` | T+ (sampled) |

Totals: 145 claims traced across the four files (38 + 34 + 37 + 36). 144 trace to a research line that states the same fact (most also confirmed against the snapshot); 1 is contradicted by the snapshot (synth-03 #37, finding B-1); 1 traced claim cites the wrong sentence (synth-04 #34, note N-1).

## Citation spot-check table

Every row is a `file:line` (or range) cited in the synthesis that I opened myself in SNAP, PKG or `git show origin/master`. "Match" means the cited lines contain what the synthesis says they contain.

### synth-01

| # | Citation | What I read | Result |
|---|---|---|---|
| 1 | `src/superclaude/core/WORKER-CONTRACT.md:287-289` | `### WC-16. Coordinator loop` and its paragraph: wake or timeout, at most every 5 minutes, "The sweep." plus `/sc:sweep`, read report before acting | Match |
| 2 | `WORKER-CONTRACT.md:23` | never-as-worker list names `/sc:sweep` | Match |
| 3 | `src/superclaude/cli/install_user_setup.py:247-270` | `def _find_orca` at 247 through `return None` at 270 | Match |
| 4 | `src/superclaude/cli/main.py:590-592` and `:581-583` | observe and sweep deferred imports + `add_command` | Match |
| 5 | `observe/parse.py:43` | `UNKNOWN: Any = _Unknown()` (the "never None, 0, False or ''" wording is in the docstring above, not on line 43) | Match (sentinel); wording nit |
| 6 | `observe/commands.py:67, 70` | `QUESTION_GATE_PASSED = True`, `QUESTION_LINK_PASSED = True` | Match |
| 7 | `sweep/report.py:23` | `CHECKED_ORCA_VERSION: str = "1.4.245"` | Match |
| 8 | `tests/observe/test_commands.py:585-601` | only `adapter.py` may import `subprocess` | Match |
| 9 | `observe/view.py:566-584` | `RowView(...)` with worker_state, dispatch_status, terminal_state, outcome, next_action, liveness | Match |
| 10 | `.gitignore:255-256` | comment at 255, `.dev/sweeps/` at 256 | Match |
| 11 | `docs/designs/orchestrator.md:930` and `:3` | "the orchestrator is the coordinator they describe"; "holds no implementation code" | Match |
| 12 | PKG `fixtures.py:1` | docstring "No Orca adapter, environment reads or network I/O" | Match |
| 13 | PKG `render.py:16-17` | font paths | Match |
| 14 | `docs/user-guide/cli-groups.md:42` | "no key and no option maps to an Orca call" | Match |
| 15 | `CHANGELOG.md:170` and `docs/user-guide/commands.md:620` | `working` "never produced" | Match |
| 16 | `agent-work-report/scripts/prefs.py:20, 30-32` | `URL` regex (GitHub and ClickUp only), `check_url` | Match |
| 17 | `agent-work-report/scripts/common.py:25` (cited for `orchestrator_repo`) | `POLL_CONFIG = "~/.config/superclaude/issue-watch.json"`; the key itself is named at lines 22, 30, 40 | Near match (note N-4) |
| 18 | `sweep/report.py:569-599` | sanitizer starts at 569; `cell` runs to 605 | Range short by 6 (note N-2) |

### synth-02

| # | Citation | What I read | Result |
|---|---|---|---|
| 1 | `issue_watch/cycle.py:216-220` | `unknown = set(raw) - _TOP_KEYS` then error | Match |
| 2 | `agent-work-report/scripts/common.py:74-82` | `safe_title` | Match |
| 3 | `scripts/activity.py:40-54` | `clean`, quote helper | Match |
| 4 | `scripts/exclude.py:59-103` | `main(run)` | Match |
| 5 | `scripts/match.py:119-247` | join code ends at `items[item["url"]] = item` | Match |
| 6 | `scripts/classify.py:67-128` | `rule(...)` | Match |
| 7 | `scripts/compare.py:84-186` | `lookup_closed` through `write_json(... "snapshot.json" ...)` | Match |
| 8 | `scripts/run.py:204-368` | `REQUIRED_CHECKS` through `sys.exit(0 if ok else 1)` | Match |
| 9 | `scripts/render.py:194-303` | `entry(...)` | Match |
| 10 | `scripts/clickup.py:39, 58-105` | `API = ...`, `call(...)` | Match |
| 11 | `observe/adapter.py:135-190`, `:469-512` | `assert_allowed` .. `build_question_argv`; `read_questions` | Match |
| 12 | `observe/parse.py:654-744`, `:750-835` | `merge`; `VARIANTS` .. `load_fixture` | Match |
| 13 | `observe/questions.py:105-129`, `export.py:141-216`, `sanitize.py:27-48`, `view.py:888-948` | function boundaries | Match |
| 14 | `sweep/commands.py:153-208`; `classify.py:455-504, 570-591, 609-683` | `_publish`; `removable`..`safe_to_close`; `_contract_for`; `_join_path_b` | Match |
| 15 | PKG `render.py:41-74`, `canvas.py:10-29, 38-55` | `exports(batch)` .. print; `sanitize`/`clip`; `text` | Match |
| 16 | `agent-work-report/SKILL.md:14-16`, `:38` | state location, living report text, "Orca's own session state is never read" wording | Match |

### synth-03

| # | Citation | What I read | Result |
|---|---|---|---|
| 1 | `adapter.py:30, 34-50, 111-118, 148-149, 173-183, 186-190` | `DISCOVERY_TEMPLATE`; 13-entry `FORBIDDEN_PREFIXES`; `_is_question_shape`; exact-match return; `build_argv`; `build_question_argv` | Match |
| 2 | `adapter.py:52-55, 92-108, 58-63, 66-69` | run-id pattern, cursor cap, limits, `_ERROR_CODES` | Match |
| 3 | `adapter.py:296-305, 378-381, 395, 403, 409-411, 422-430, 469, 479, 506-507` | timeouts, namespace, `read_pages`, `not-found`, `overrun`, `read_questions`, error codes | Match |
| 4 | `tests/observe/test_adapter.py:178-192` | superset assertion | Match |
| 5 | `collector.py:28-34, 125-129, 135-145, 205-245, 261, 273, 306, 321` | intervals, `no-question-fixture`, `Collector`, question read, `not-found`, `QUESTION_PAGE_CAP`, backoff | Match |
| 6 | `questions.py:9-12, 21-22, 125-129` | docstring limit, `RETENTION_BOUND`, `WINDOW_ROWS`, eviction | Match |
| 7 | `view.py:30, 33-35, 456-463, 667, 811, 888-948, 1246-1300` | `KEY_NAMES`, STALE, `source_state`, status map, subject in record text, `_desk`, `apply_key` | Match |
| 8 | `export.py:20, 103-111, 236-244` and write_atomic at 258-270 | `SCHEMA_VERSION = 1`, question lines, `state_dir`, atomic write | Match |
| 9 | `parse.py:43, 58-90, 277-290, 365-407, 528-533, 654-744` | sentinel, 31 fields, depth 6, strict envelope, merge | Match |
| 10 | `commands.py:67, 70, 77-78, 183-196, 264-268, 364-369, 377-387, 414` | gates, refusal, exit codes | Match |
| 11 | `keys.py:115-117, 119-125` | SIGINT, SIGTERM, SIGHUP | Match |
| 12 | `terminal.py:21-24, 82-89`; `render.py:480-568` | widths, `width_class`, `_columns` | Match |
| 13 | `tests/observe/test_commands.py:754-779`, `test_render.py:677-695`, `test_registration.py:59-71` | gate pins, golden "never regenerated", registration block | Match |
| 14 | `snapshot.schema.json` line 50 | `counts` values limited to scalar types | Match |
| 15 | Consumers table: `Draft7Validator` in `test_export.py` | `test_export.py` has no schema reference at all | **Mismatch** (B-1) |

### synth-04

| # | Citation | What I read | Result |
|---|---|---|---|
| 1 | `classify.py:40, 42-51, 345-355, 358-366, 369-378, 423, 455, 479, 512-525, 548-558, 570, 609, 745, 760, 880` | `JOIN_PATH`, class unpack, `RULES`, `_force_unknown`, `classify`, `package_state`, `removable`, `safe_to_close`, `_merge_group`, `_window`, `_contract_for`, `_join_path_b`, `path_b = JOIN_PATH == "B"`, `_person_origin`, `classify_all` | Match |
| 2 | `classify.py:728` for `_guard` | line 728 is the `@dataclass` of `_Guard`; `def _guard(` is at 741 | Moved by 13 (note N-3) |
| 3 | `classify.py:251-269` | `_rule_working` | Match |
| 4 | `models.py:50-59, 62, 71, 108-112, 212` | `CLASSES`, `PACKAGE_STATES`, `SAFE_VALUES`, the three producer-less fields, `Classification` | Match |
| 5 | `probes.py:49-60, 68-81, 83, 85-88, 124-131, 266, 315, 458-468, 471-515, 481, 1322` | allowlists, version file, limits, `Budget`, `_orca`, `_git`, `_agent_wait`, `parse_worker_show`, `collect` | Match |
| 6 | `sweep/commands.py:99, 153, 220-241, 269-271, 276-288` | `_check_output`, `_publish`, options, collect and classify, exits | Match |
| 7 | `report.py:23, 545-558, 569, 608, 613` | version const, `SECTIONS`, `sanitize`, `render`, `to_json` | Match |
| 8 | `WORKER-CONTRACT.md:20, 23, 46, 110, 157, 287-289` | case 3, never-as-worker, WC-10, "The sweep.", ladder, WC-16 | Match |
| 9 | `HOW-WE-WORK.md:298, 359`; `tests/core/test_how_we_work_routing_table.py:33` | routing row, wake-time rule, `"sc:sweep"` required | Match |
| 10 | `output-styles/pragmatic.md:22-25`; `commands/sweep.md:16, 18, 22, 42, 70`; `sc-sweep-protocol/SKILL.md:25, 51, 66`; `closeout.md:99` | chat exception; command text; skill text | Match |
| 11 | `docs/designs/orchestrator-mode.md:27, 493, 636, 841, 1003` | "does not exist yet", rule 5, footnote, D7 row, open item 6 | Match |
| 12 | `CHANGELOG.md:170-171`; `docs/user-guide/commands.md:619-621` | known-limit lines | Match |
| 13 | `tests/sweep/test_classify.py:351, 378-379, 791-800, 1385-1391, 1405-1412`; `test_report.py:353, 1091, 1439-1441`; `test_cli_contract.py:1133-1140`; `test_probes_allowlist.py:624-638, 1651, 1687` | RULE_NAMES pin, rule 6 test, path-B tests, fenced row, `RULE_CLASS`, no-action-control test, running-worker test, zero-argv test, `agent_wait_since is None` | Match |
| 14 | `tests/skills/test_worker_contract.py:212-215` (cited for the WC-16 cadence) | pins "at most once every 5 minutes, the coordinator runs one sweep" under key `liveness-sweep-and-states`; WC-16's own pins are at 167-175 | Wrong sentence (note N-1) |
| 15 | `tests/commands/test_sweep_command.py:155-159` | no `## Unattended mode` | Match |

Totals: 64 citation rows opened (18 + 16 + 15 + 15; each row groups one or more cited lines, so more than 10 distinct citations per file). 5 rows are not a clean match: 1 false attribution (B-1) and 4 moved or imprecise citations (N-1 to N-4 below). The remaining rows match.

## Synthesis Quality Review Checklist (9 items) and extra checks

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Headers match the template structure | PASS | Sections 1, 2.1-2.4, 3, 3.1, 4.1-4.3 and the 5.x block order (Purpose, Key Files, How It Works, Public Interface, Dependencies, Consumers, Conventions & Patterns) match `technical_reference_template.md` lines 147-324. 2.5 "Family at a glance" is an addition the task prompt (task file line 283) orders. Two cosmetic header edits: 2.2 column "Subsystem (Section 5)", 2.3 column "TDD Divergence (design or docs)" (N-8) |
| 2 | Tables use the template column structure | PASS | 2.4 (Technology, Version, Purpose), 3.1 (Pattern, Convention, Example), 4.2 (Source, Type, Location, Description), 4.3 (Transformation, Input, Output, Location, Description), Key Files, Dependencies, Consumers all match |
| 3 | No fabricated content | FAIL (1 item) | 144 of 145 traced claims have a supporting research line. One claim (synth-03 Consumers table, `Draft7Validator` in `test_export.py`) is false against the snapshot, and the research hedge on it was dropped (B-1) |
| 4 | Findings cite real paths and evidence | PASS | 64 citation rows opened; every cited path exists (including origin/master-only `.dev/` files via `git show`); no vague "the system uses X" statements found |
| 5 | Subsystem sections within depth budget | PASS | 5.1 = 120 lines (synth-03 lines 9-128), 5.2 = 121 (132-252), 5.3 = 117 (synth-04 lines 9-125), 5.4 = 122 (129-250): all inside the 120-200 "complex" band and none above 200. File totals exceed the task prompts' "about N lines" hints (N-7) but that is not a template budget |
| 6 | Architecture backed by code-traced evidence | PASS | Section 2 and 4.1 diagrams rest on code reads; designed-only boxes (orchestrator, entry writer) are marked DESIGNED and kept out of the built flows |
| 7 | Cross-references consistent | PASS | Counts, gate constants, 13 prefixes, 45 s STALE, 6 of 8 classes, the 10 templates (6 called), 12 sections / 12 keys, C8 labels and PR numbers agree across synth-01 to 04. Only difference: sanitizer range 569-599 (synth-01) vs 569-605 (synth-02) (N-2) |
| 8 | No doc-only claims in Architecture or API sections | PASS with note | Doc-sourced owner decisions in synth-01 section 2.3 (QUESTION-LINK status line, stack decision, "Stage it") carry citations but no "(doc)" or [UNVERIFIED - doc-only] tag, while synth-03 does tag them "(doc)"; the code facts beside them are verified (N-5) |
| 9 | Stale-doc discrepancies surfaced or pointed to Section 14 | PASS | SD-06, SD-07, SD-09, SD-21 to SD-23, SD-25, CC-01, CC-02, CC-03, CC-04, G-20 in synth-01/02; `[STALE DOC]`/`[CODE-CONTRADICTED]` for `CHANGELOG.md:170`, `commands.md:620`, `orchestrator-mode.md:27` in synth-04; SD-02, SD-05, CC-01 in synth-03; synth-01 points to Section 14 |
| X1 | Live versus designed accuracy | PASS | Built: observer R0-R3, sweep, daily report, reader side of the living report. Designed only: orchestrator writer (PR B, no PR), R4, package as a product. Items sequenced to an open PR (`orchestrator_repo`, PR A #686) are called failing on master. No designed item is described as built |
| X2 | C8 wording | PASS with note | D-1 and the `prefs.py` "Needs you" session answer stay DEFECT-CANDIDATE (GF1 3.8, 3.7 last paragraph). stalled / fenced / `agent_wait_since` / Safe to close / Removable stay KNOWN LIMIT (cited) with the SPEC and DESIGN lines, as GF1 R-C8 requires. The exact words "remediation task not created (read-only brief); flagged for the owner" appear in synth-03 (D-1), in all five rows of the synth-04 limits table, and once in the synth-01 pointer lead-in; they are absent next to the D-1 and writer pointers in synth-02 (N-6) |
| X3 | Neutrality | PASS | Regex scan of the four files for recommend / should be / unif / consolidat / suggest / prefer / combine: every hit is a file name, the word "consolidated" in a source list, or the sweep's own behaviour ("never recommends an action"). No unification recommendation |

## Findings

### Blocking

**B-1 (blocking). synth-03 states a test file validates snapshots against the schema; the file does not.**
- File and location: `TD/synthesis/synth-03-subsystem-observer.md`, section 5.1 "Consumers" table, row `tests/observe`: "Validate snapshots against the schema (Draft7Validator in test_commands.py, test_snapshot_schema.py, test_export.py)".
- Evidence: in SNAP, `tests/observe/test_export.py` contains no `jsonschema`, `Draft7Validator`, `schema` or `valid` token (searched the whole file; its imports are `export`, `adapter`, `collector`, `render`, `terminal`, `view` and `conftest` helpers). `Draft7Validator` appears in `tests/observe/conftest.py:17, 32`, `test_commands.py` and `test_snapshot_schema.py`. The only research line behind the claim, R02:210, says the schema check is "[CODE-VERIFIED for test_commands.py; the other two named by their file names only]". The synthesis dropped that hedge and stated all three as verified.
- Required fix: name only the files that do validate (`test_commands.py`, `test_snapshot_schema.py`, with the shared `Draft7Validator` set-up in `conftest.py:17, 32`), or drop `test_export.py`. The same sentence should not be carried into the final document with `test_export.py` in it.

### Minor (notes only; none fails the gate)

- **N-1.** synth-04 section 5.4, WC-16 table, row "Cadence and 'read before acting'": "only the sentence is pinned (`test_worker_contract.py:212-215`)". Lines 212-215 pin the Liveness-supervision sentence "at most once every 5 minutes, the coordinator runs one sweep" (key `liveness-sweep-and-states`). WC-16's own pins are at `test_worker_contract.py:167-175` ("WC-16. Coordinator loop", "On every coordinator wake", "it is never posted", "It never stops watching on its own"); WC-16's 5-minute clause and "reads its report before it acts" are not pinned. The claim that no code enforces the cadence is true. R04:205 carries the same citation. Fix: cite 167-175 for WC-16 and 212-215 for "The sweep." separately.
- **N-2.** synth-01 section 2.5 overlaps table cites the sweep sanitizer as `sweep/report.py:569-599`; synth-02 4.3 says `569-605` and `cell` (the 200-character cut) ends at 605. Use 569-605 in both.
- **N-3.** synth-04 section 5.3 Key Files and the join list cite `_guard` at `classify.py:728`; `def _guard(` is at 741 (728 is the `@dataclass` of `_Guard`). Moved line number on a true claim.
- **N-4.** synth-02 section 3 cites `common.py:25` for the `orchestrator_repo` key; line 25 is `POLL_CONFIG = ...`. The key is named at `common.py:22, 30, 40`. Moved line number on a true claim.
- **N-5.** synth-01 section 2.3, "Staged observer release" and "Python + Rich stack" rows: owner-decision text from `.dev/issues/409/...` (QUESTION-LINK "status line recorded by the agent on the owner's chat yes", stack CONFIRMED, "Stage it") is stated in the "What Was Built" or "Rationale" cells without a "(doc)" tag. The code facts in the same cells are verified. Tag them "(doc)" as synth-03 does.
- **N-6.** synth-02 sections 4.1(a) and 4.1(c) mention D-1 / C8-9 and the PR-B writer without the exact sentence "remediation task not created (read-only brief); flagged for the owner"; synth-01's pointer lead-in and synth-03 / synth-04 carry it. Acceptable as pointers; if Section 14 is assembled from these files the sentence must be present there for D-1, the writer and the `prefs.py` item.
- **N-7.** Length against the task prompts' hints: synth-02 is 179 lines (hint "about 90"), synth-03 252 (hint about 180), synth-04 249 (hint about 200), synth-01 117 (hint about 110). Many lines are 600-1,000 characters long. Not a template depth-budget breach.
- **N-8.** Cosmetic header and format deviations: synth-01 2.2 column "Subsystem (Section 5)" and 2.3 column "TDD Divergence (design or docs)"; synth-02 file tree carries "base + 9 variants" and 3.1 carries "(19 JSON files; M-12)" although the prompt says no inline file counts in the trees; synth-03 5.2 has "**Public Interface**" directly after the D-1 bullet with no blank line (line 225-226).
- **N-9.** synth-01 section 2.3 cites `ARCHITECTURE-SPINE.md:172` without a directory; two files of that name exist under `.dev/issues/409/bmad/` on origin/master (`spec-orca-observer/` and `architecture-orca-observer/`). Line 172 read from the `spec-orca-observer/` copy matches.
- **N-10.** synth-01 section 2.3 cites `parse.py:43` for the wording "never None, 0, False or ''"; line 43 is the `UNKNOWN` definition and the wording sits in the docstring above it.

### Zero-finding lenses (what I checked and found clean)

- No designed-only item is presented as built; no unification recommendation; C8 labels equal GF1's determinations in all four files (stalled, fenced, `agent_wait_since`, Safe to close, Removable = KNOWN LIMIT (cited); D-1 and the `prefs.py` session-answer item = DEFECT-CANDIDATE; living-report writer and `orchestrator_repo` = KNOWN LIMIT sequenced to PR B and PR A).
- All counts I recomputed match: 13 observer `.py` files (6,011 lines) plus 158-line schema; per-file line counts in the 2.2 map; sweep 3,759 lines; AWR 16 scripts 5,777 lines; test file counts and `def test_` counts; package 406/412 files, 360 exports, 18 scenarios; 31 `_FIELDS`; 13 forbidden prefixes; 12 report sections; 12 JSON keys.
- Research-to-synthesis supersession was applied correctly: GF1 over R04 for labels, GF2 for the `commands.md` / `CHANGELOG.md` attribution, QA M-4/M-7/M-8/M-12 count corrections.

## VERDICT: FAIL

One blocking finding (B-1: a false test attribution in synth-03 section 5.1 Consumers, with the source hedge dropped) and ten minor notes (N-1 to N-10). Everything else traced: 144 of 145 sampled claims have a supporting research line and 59 of 64 citation rows match the snapshot exactly. Re-run this lens after B-1 is fixed; N-1 to N-10 can be fixed in the same pass but do not gate.

