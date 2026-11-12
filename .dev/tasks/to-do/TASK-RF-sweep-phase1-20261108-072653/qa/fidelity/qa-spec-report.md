# QA Report: SPEC fidelity lens (T341)

Reviewer: rf-qa (adversarial), fix_authorization: false
Date: 2026-11-13
Scope: every FR, NFR and INV in merged-requirements.md traced to delivered code or test (file:line) or a DESIGN deferral.

Paths: `$R` = `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode`. Code is `$R/src/superclaude/cli/sweep/<module>.py` (cited `probes.py:N` etc.), tests are `$R/tests/sweep/<file>` (cited `test_x.py:N`). SPEC = `.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md` (653 lines, read in full, 5 chunks). DESIGN = `docs/designs/orchestrator-mode.md` (1052 lines, read in full) plus `design-addendum.md` (45 lines).

## 1. What was read and run

- SPEC lines 1-653; DESIGN lines 1-1052; addendum 1-45; the three FINAL-GATE records and the owner decision files OQ-1, OQ-2, OQ-3 (+ addendum), OQ-5, OQ-7, OQ-8, OQ-10, OQ-17; `phase-outputs/discovery/final-inventory.md` and `1.0a-facts.md`.
- Code read: `commands.py` 1-288 (all), `probes.py` 1-600, 860-1362 (the rest located by grep), `classify.py` 1-60, 156-500, 853-992, `report.py` 1-120, 155-215, 556-695, `models.py` 60-160, `__init__.py` (all), `SKILL.md`, `sweep.md`, `pragmatic.md` diff.
- Run: `uv run pytest tests/sweep tests/commands tests/core tests/skills tests/recommend -q` = 3245 passed, 0 failed. `uv run ruff check .` = All checks passed. `uv run pytest tests/sweep tests/commands/test_sweep_command.py -rs` = 719 passed, no skip lines. `cmp` of HOW-WE-WORK.md against the plugin copy = identical; `cmp` of `sweep.md` and `SKILL.md` against the `.claude/` dev copies = identical; no `.claude/` path is staged. The WC-16 paragraph at `WORKER-CONTRACT.md:277` equals DESIGN `:680` byte for byte (1825 bytes each).
- Not run (not on the allowed list): `make sync-dev`, `make verify-sync`, `make lint`, `ruff format --check`. NFR-012 for those is RELIANCE on `phase-outputs/test-results/phase14-sync.md` and `phase14-lint.md`, and is marked so below.
- No code, test or document was edited. No live Orca, ccsession or Claude command was run.

## 2. Owner records that change what the SPEC means now

| Record | What it authorizes | Where I checked it |
|---|---|---|
| `FINAL-GATE-halt-resolution-decision.md` (2026-11-12) | (1) FIN-F7 skill edit reverted, its three tests and two constants removed, step-3 pin back to `success-parse-takes-only-report-path-and-summary`; (2) DESIGN `:491` and `:760` say Rule 5 is inert and `working` is not reached; (3) stale comments fixed, unused model fields marked reserved | SKILL.md:25 (step 3 takes only `report_path` and `summary`); `test_sweep_command.py:436` (pin text); DESIGN `:491`, `:760`, `:997`; `classify.py:251-257`, `:229`; `models.py:78`, `:90`; `probes.py:432-434`; grep for `_OUTAGE_SENTENCE` and `_EXEMPT_ALONE_SENTENCE` in `test_sweep_command.py` returns nothing |
| `FINAL-GATE-cycle2-scope-decision.md` (2026-11-12) | FIN-F5 only: DESIGN `:614-615` has two banners; `report.py`, `test_report.py`, `test_cli_contract.py` move with it | `report.py:33-39`, `:169-176`; `test_report.py:642-695`; `test_cli_contract.py:429-446` |
| `FINAL-GATE-FIN-F7-ruling.md` (2026-11-12) | FIN-F7 (the exempt chat reply prints counts and path alone, so an Orca outage is not visible in that reply) is a documented limitation of Phase 1, in the follow-up issue | SKILL.md:35-43 and `pragmatic.md:23` still print counts and path only; see finding F5 (MINOR) |
| `OQ-1-agent-wait-decision.md` (owner confirmed in person 2026-11-12) | `worktree ps --agent-wait` with and without `--json` is allowed: 10 templates, 7 verbs | DESIGN D10 `:838`; `probes.py:49-60`; `test_probes_allowlist.py:56-67`, `:340-385` |
| `OQ-3-GQ-11-rule-id-decision.md` and `OQ-3-addendum-wc16-wait-timeout-decision.md` | New rule id WC-16 (WC-14 and WC-15 are taken on master); "wake or wait timeout" wording | DESIGN D6 `:834`; `WORKER-CONTRACT.md:275-277`; `test_worker_contract.py:173` |
| `OQ-7-D9-signoff-decision.md` (2026-11-11) | D9 as written, including its two residual path-B cases | DESIGN D9 `:837`; `classify.py:40` (`JOIN_PATH = "B"`) |
| `OQ-17-cursor-template-decision.md` (2026-11-11) | No cursor template; a full 100-row page is truncated with a lower-bound total | `probes.py:49-60` (10 templates), `:1046-1047`; `report.py:32`, `:209-210` |
| `OQ-5-GQ-61-window-decision.md`, `OQ-2-GQ-10-report-location-decision.md` | 6h default; `<root>/.dev/sweeps/` and `<YYYYMMDD-HHMMSS>-sweep.md` | `commands.py:27`, `:99-123`, `:155` |

## 3. Functional requirements FR-001 to FR-026

Result column: DELIVERED = code and a passing test both found; DELIVERED (note) = delivered with a MINOR note in section 7; DEFERRED = the DESIGN section and owner record that defer it are named.

| ID | Code | Test | Result |
|---|---|---|---|
| FR-001 | `commands.py:214-242` (`sweep_group`, `run`); `main.py` import and `add_command` after the `issue-watch` pair (git diff hunk `@@ -566`); lazy export `__init__.py:3-9` | `test_cli_registration.py:32-45` (`sweep --help`, `sweep run --help` exit 0) | DELIVERED |
| FR-002 | `commands.py:87-92` (`_check_run_ids`: regex before any `_orca`, dedupe in first-seen order); `probes.py:361-371` (`bind_run`, exit-2 messages with the D3 reason); `probes.py:1031-1038` (first call per Run is `worker-list`); `probes.py:333-358` (`_call`: nonzero or invalid on the first call is `unavailable`) | `test_cli_contract.py:260-332` (empty, `r;x`, duplicates, one bad id, unknown Run then R2); `:375-426` (tests 1, 2, 3); `:478` (test 4, fixture `captured-run-current.json`, runs, not skipped) | DELIVERED. The unknown-Run shape is the captured exit 0 empty list, not the SPEC's guessed nonzero shape: DESIGN `:245`, `:995` (open item 4), D3 `:831` |
| FR-003 | `commands.py:43-52` (`[1-9][0-9]{0,3}[hd]`, at most 720h) | `test_cli_contract.py:500-587` (all SPEC cases incl. `٦h`, `999999999d`, `721h`, `31d`) | DELIVERED |
| FR-004 | `commands.py:55-84` (root walk with `os.stat` only, explicit `--root` checks), `:99-123` (containment on the resolved path, overlap with input folders) | `test_cli_contract.py:595-789` (default, below `.dev/sweeps/`, outside, `.dev/`, `.dev/tasks/`, `.dev/other/`, symlink escape, overlap, file root, no `.git`, walk to filesystem root, no git call) | DELIVERED |
| FR-005 | `classify.py:957-973` (`visible`, `historical`, `total`, `total_is_lower_bound`), `probes.py:1206-1280` | `test_cli_contract.py:847-880`; `test_classify.py:1685` | DELIVERED |
| FR-006 | `classify.py:333-343` (9 rules), `:357` (`classify`) | `test_classify.py:365-380` | DELIVERED (note F1): `working` is never reached, Rule 5 is inert. DEFERRED by DESIGN `:491`, `:760`, `:997` and `FINAL-GATE-halt-resolution-decision.md` change 2 |
| FR-007 | `models.py` `SweepContext` (frozen, `now`, `window`, `window_start`, `root`, `runs`); `classify.py:283-299` (`_rule_idle`) | `test_classify.py:462-503` (5 h row idle only under 5 h; record timestamp older than mtime wins and is named) | DELIVERED |
| FR-008 | `classify.py:318` (`_rule_fallback`) | `test_classify.py:543` (four inputs never `stalled (proved)`) | DELIVERED |
| FR-009 | `classify.py:191-208` (`_exit_proof`: matches only exited, `worker_done_seen False`, `fenced_evidence absent`; otherwise declines with the exact note) | `test_classify.py:549-607` (case 1: `guard refused:` body is finished with the note; case 2: fallback with the note) | DELIVERED |
| FR-010 | `classify.py:678-770` (`_origin_unknown`, `_guard`, `_person_origin`), `:597-672` (joins) | `test_classify.py:918-1000` (control, outage, full page, `call_failed`, plus three non-SPEC list-incomplete fixtures and the note-order fixture); `:1082-1101` (exemptions, SP-29 two-Run); `:1131-1225`, `:1271-1533` (D9 and path-B fixtures) | DELIVERED. The three FR-010 fixtures named in the brief (outage `:932`, full page `:941`, `call_failed` `:953`) exist and assert exactly one `origin unknown:` note, `person_started None`, not Historical. SPEC's `worker of Run <id>, outside scope` False path does not occur: DESIGN `:503`, `:845`. SP-29 narrowed by D9 `:837`, signed off in OQ-7 |
| FR-011 | `report.py:232-282` (Waiting (a) table, oldest first, unknown-age group), `:283-326` (Waiting (b), Ready Tasks sub-heading and count) | `test_report.py:543` (heading order), `:708` (sort with 3 ages plus one unknown, tie by ID), `:774` (b has no question text) | DELIVERED (note F2) |
| FR-012 | `classify.py:467-492` (`safe_to_close`), `:443-464` (`removable`, never `yes`) | `test_classify.py:1586`; `test_cli_contract.py:1038` | DELIVERED |
| FR-013 | `classify.py:443-464`; `probes.py:870-914` | `test_classify.py:1640-1659` (one fixture per condition) | DELIVERED |
| FR-014 | `classify.py:396-417` (`package_state`, precedence order); `probes.py:605-660` | `test_classify.py:1733-1767` (every state incl. `conflict`, `FINAL:` only at line start) | DELIVERED |
| FR-015 | `classify.py:420-440` (`mark_shared_packages`); `probes.py:910-914` (`_package_active`); `ALLOWED_GIT` `probes.py:65-67` | `test_classify.py:1784-1812` (44 committed folders in 3 worktrees: no flag; one modified folder in 3: one line naming all 3; one `??` path marks active) | DELIVERED |
| FR-016 | `report.py:562-605` (`sanitize`, `cell`) | `test_report.py:828-935` (pipe, ANSI, bidi, `<script>`, Markdown link; column count kept) | DELIVERED |
| FR-017 | `commands.py:153-208` (`_publish`), `:277-278` (JSON after publication); `report.py:613-695` (`to_json`, every key present) | `test_cli_contract.py:992-1085` (golden key set and types, zero counts, ID-only `waiting`); `:1123-1184` (dated name, two files for one `now`, earlier file byte-identical); `:1249-1480` (failed-write cases print no success JSON) | DELIVERED |
| FR-018 | `commands.py:279-288` (exit 2 for `UsageError` and `BindingError`, exit 1 with `[sweep <stage>]`) | `test_cli_contract.py:1184-1248` (one test per code; internal error in each pure stage) | DELIVERED |
| FR-019 | `probes.py:1002-1078` (`skip()` writes `unscanned: orca unavailable`), `report.py:169-176` (banner) | `test_cli_contract.py:411-426`, `:449-468` (disk-only continuation); `test_probes_allowlist.py:895` | DELIVERED |
| FR-020 | `probes.py:110-194` (`Budget`), `:333-340`, `:1073`, `:1149-1174`, `:1329-1361`; `classify.py:853-862`, `:962` (`bound_reached`) | `test_probes_allowlist.py:961-1150` (60, 50 and 2x40 rows, 20 s left, full-timeout fakes under 120 s), `:1282-1442` (limit minus 1, at, plus 1 for each byte limit); `test_report.py:1016` (cap line only when `bound_reached` >= 1) | DELIVERED (note F3) |
| FR-021 | `probes.py:49-60` holds no write verb; the forbidden list is in the test | `test_probes_allowlist.py:439-490` (list absent from every template, each refused; source holds no write verb even as a string) | DELIVERED |
| FR-022 | `sweep.md:9` (`allowed-tools: Skill`), `:44-55` (Activation, installed path `:51`, project path `:55`); `SKILL.md:4` (literal), `:23-24` (PATH first, fallback only on "command not found", 120000 ms, `--frozen --no-sync`) | `test_sweep_command.py:106-167` | DELIVERED |
| FR-023 | `WORKER-CONTRACT.md:23` (list), `:275-277` (WC-16) | `test_worker_contract.py:89`, `:173`, `:400`, `:922`, `:1333` (9-entry list, rename, `sweep` not in `UNATTENDED_COMMANDS`) | DELIVERED as WC-16, not WC-14. DEFERRED rename by DESIGN D6 `:834`, `:671` and `OQ-3-GQ-11-rule-id-decision.md` (WC-14 and WC-15 are taken on master `5dc29d23`) |
| FR-024 | `HOW-WE-WORK.md:334` (R1), `:405` (R2); plugin copy `cmp`-identical; `docs/user-guide/commands.md:116`; developer guide `:991`; `CHANGELOG.md` `### sweep:` block | `test_routing_refresh.py` `_POST_REFRESH_ADDITIONS` and `test_how_we_work_routing_table.py` `_OTHER_COMMANDS` (git diff); full `tests/core tests/recommend tests/commands` run = pass | DELIVERED |
| FR-025 | `.gitignore:255-256` (`git check-ignore -v .dev/sweeps/x.md` hits line 256) | `test_readonly.py:471-528` (the one real-git test: ignore, not-ignore, status unchanged) | DELIVERED |
| FR-026 | `probes.py:240-295` (`_orca`: unavailable causes, anchored marker, `call_failed`), `:287-288` | `test_probes_allowlist.py:713-760` (parametrized causes, quoted marker stays `ok`, empty body, captured no-binding fixture), `:814-930` | DELIVERED |

## 4. Non-functional requirements NFR-001 to NFR-015

| ID | Code | Test | Result |
|---|---|---|---|
| NFR-001 | `commands.py:153-208` (one write: temp file, `os.link`, unlink) | `test_readonly.py:187-292` (snapshot of path, size, mtime_ns, sha256 under root, HOME, XDG), `:368` (exactly one added file), `:393` (no temp file or second name after exit 0), `:407` (a stray write is caught) | DELIVERED |
| NFR-002 | `probes.py:298-322` (`_git`: `git --no-optional-locks -C <cwd>` built inside the seam, `GIT_OPTIONAL_LOCKS=0` in `env`); `ALLOWED_GIT` `:65-67` | `test_readonly.py:73` (argv index 1 and env), `:94`, `:130`, `:144` (one git argv per worktree), `:471-528` (the single real-git test: control, ignore, not-ignore, status unchanged; control only warns when inconclusive) | DELIVERED |
| NFR-003 | `probes.py:212-230` (`check_orca_argv`, token for token, `ValueError` before any process), `:227-230` (`check_git_args`), `:200-202` (`orca_binary`) | `test_probes_allowlist.py:369-440`, `:489-584` (argv[0] `orca-ide` or `ORCA_CLI_COMMAND`; zero argv for the 4 not-called templates; git negatives `rev-parse`, `log`, `branch`, `--version`) | DELIVERED. The SPEC negative `worktree ps --agent-wait` is replaced by a positive case under R5 and D10 (DESIGN `:838`, `OQ-1`). See finding F4 for the missing literal `worker-list --include-remote` case |
| NFR-004 | `classify.py:10-36` and `report.py:11-21` import only stdlib `re`, `dataclasses`, `datetime`, `pathlib`, `unicodedata` and `.models` | `test_classify.py:1905-1913` (AST scan of `classify.py`, `report.py`, `probes.py`) | DELIVERED |
| NFR-005 | `report.py:608-610` (`render` reads no clock); `probes.py:1210`, `:1279` (`collected_start`, `collected_end`) | `test_report.py:937` (render twice: equal bytes, equal JSON apart from `report_path`) | DELIVERED |
| NFR-006 | `__init__.py:3-9` (lazy `__getattr__`) | `test_cli_registration.py:48-69` (import records no seam call; `commands` loads only when `sweep_group` is read) | DELIVERED |
| NFR-007 | `probes.py:110-194` (`Budget` 90 s), `SKILL.md:23-24` (timeout 120000 ms on both runs) | `test_probes_allowlist.py:1116` (full-timeout fakes finish under 120 s and publish), `:1150`; `test_sweep_command.py:151` | DELIVERED |
| NFR-008 | `probes.py:1016-1026`, `:1157-1171` (`unscanned` source rows); `classify.py:343-356` (`_force_unknown`) | `test_report.py:956` (source loss gives could not determine with the `unscanned:` reason) | DELIVERED |
| NFR-009 | `report.py:613-695`; `models.py:17` (`JSON_SCHEMA_VERSION = 1`) | `test_cli_contract.py:992-1070` (golden key set and types at every level; the type check rejects a wrong key set) | DELIVERED |
| NFR-010 | `classify.py:333-343` | `test_classify.py:379` (`[r.name for r in RULES]` equals the 9 names) | DELIVERED |
| NFR-011 | no `src/superclaude` string in `sweep.md` or `SKILL.md`: `grep -rn 'src/superclaude'` over both returns no match (exit 1) | `test_sweep_command.py:163` | DELIVERED |
| NFR-012 | `.claude/` copies of command and skill are `cmp`-identical to `src/`; nothing under `.claude/` is staged; `ruff check .` clean (run here) | `phase14-sync.md` (RELIANCE: `make sync-dev`, `make verify-sync`), `phase14-lint.md` (RELIANCE: `make lint` exit 0) | DELIVERED (note F6): `uv run ruff format --check src/ tests/` exits 1 on 12 Markdown files that exist unchanged at base `5dc29d23` (`git diff --quiet` run here for all 12); `ruff format --check` on every file this task created or edited (20 Python files) is clean |
| NFR-013 | `tests/sweep/conftest.py:30-41` (autouse guard patches `subprocess.run`, `Popen`, `os.system`; only the `integration` real-git test steps aside) | `test_readonly.py:434-460` | DELIVERED |
| NFR-014 | `probes.py:49-62` (10 templates, 7 verbs, `FORBIDDEN_TOKENS = {--include-remote}`) | `test_probes_allowlist.py:56-67` (independent literal of the 10 templates), `:340-366` (exact-set pin, 7-verb pin, constants), `:374-385` (`worktree ps --agent-wait`, both forms, accepted), `:388-436` (negatives incl. `--include-remote` in three positions) | DELIVERED. The exact allowlist is still pinned. `--agent-wait` is allowed under R5 (owner "Allow it, no conditions needed", confirmed in person 2026-11-12 in `OQ-1-agent-wait-decision.md`) and recorded as D10 (DESIGN `:838`); the SPEC wording "eight templates, never `--agent-wait`" is superseded for that line only |
| NFR-015 | `report.py:23`, `:159-166` (`_version_line`: text before the first `-` equals `1.4.245` gives `unlikely`, else `UNVERIFIED ... observed <v or unknown>`); `probes.py:853-864` (`read_orca_version`) | `test_report.py:1009` (`1.4.245-aidev02...` matches; `1.4.246` and a missing file give `UNVERIFIED`) | DELIVERED |

## 5. Invariants INV-001 to INV-017

`grep -on 'INV-0[0-9][0-9]'` over the SPEC finds INV-001 to INV-013, INV-015 and INV-017. INV-014 and INV-016 are never named in the SPEC, so there is nothing to trace for them. INV rows live in the Round 3 files the SPEC cites; the SPEC text that states each one is what I traced.

| INV | SPEC place | Code | Test | Result |
|---|---|---|---|---|
| INV-001 outage before and after a binding | FR-002, FR-019, 5.1 | `probes.py:361-371`, `:333-358`; `commands.py:279-281` | `test_cli_contract.py:375-426`, `:449-468` | DELIVERED |
| INV-002 four Orca result classes | FR-026, section 8 | `probes.py:98-107`, `:240-295` | `test_probes_allowlist.py:713-760`, `:814-930` | DELIVERED |
| INV-003 `person_started` True, False or None | FR-010, section 7 | `classify.py:678-770` | `test_classify.py:918-1000`, `:1131-1225` | DELIVERED |
| INV-004 banner when worktree discovery is incomplete | section 9 header | `report.py:33-39`, `:169-176`, `:204-206` | `test_report.py:616-700`; `test_cli_contract.py:429` | DELIVERED (two banners per `FINAL-GATE-cycle2-scope-decision.md`) |
| INV-005 Orca read verbs and optional git locks | section 13, NFR-014, NFR-015 | `probes.py:49-62`; `report.py:159-166` | see NFR-014, NFR-015 | DELIVERED (D10 widens the template set by owner decision R5) |
| INV-006 `worker_done_seen` None on live rows | section 7 | `probes.py:422-465` never sets `worker_done_seen`; `models.py:87` default None | `test_classify.py:557-571` (stalled only from a fixture row) | DELIVERED |
| INV-007 stalled only on Orca's exit proof; unreadable fencing declines with note | FR-009, rule 2 | `classify.py:191-208` | `test_classify.py:549-607` | DELIVERED |
| INV-008 untracked paths named limitation and `--untracked-files=all` | section 9, FR-015, section 14 | `probes.py:65-67`, `:910-914`; `report.py:201-202` | `test_classify.py:1812`; `test_probes_allowlist.py:1933-1941`; `test_report.py:577` | DELIVERED |
| INV-009 full-page lower-bound note with the completeness guard | FR-010, section 8 | `probes.py:1045-1047`; `report.py:32`, `:209-210`; `classify.py:678-712` | `test_report.py:1025`; `test_classify.py:941` | DELIVERED |
| INV-010 budget scope | FR-020, section 8 | `probes.py:110-194`, `:928-939` (git call counts against the 90 s total) | `test_probes_allowlist.py:961-1150` | DELIVERED |
| INV-011 cadence | section 10, OQ-7 | `WORKER-CONTRACT.md:277` ("at most once every 5 minutes", "keeps that pass scheduled while work remains", "Phase 1 adds this duty, not a scheduler") | `test_worker_contract.py:173` | DELIVERED (the SPEC leaves a fixed cadence open; DESIGN D6 takes master's 5-minute cap) |
| INV-012 WC-14 text: heartbeat absence, recommends nothing | section 10 | `WORKER-CONTRACT.md:277` ("A missing heartbeat is absence, never death", "recommends nothing: no stop, retry, release, merge or removal") | `test_worker_contract.py:173` (4 pinned phrases); `test_sweep_command.py:167` | DELIVERED |
| INV-013 PR #422 sequencing, WC rule stays in this PR | section 10, OQ-6 | `WORKER-CONTRACT.md:275-277`; DESIGN `:671`, `:948` (step 1.16a record-only) | `test_worker_contract.py` full file passes | DELIVERED |
| INV-015 determinism | NFR-005 | `report.py:608`; `models.py` `SweepInput` | `test_report.py:937` | DELIVERED |
| INV-017 Orca binary resolution | section 8, section 14 | `probes.py:43`, `:200-202`, `:266-267`; `report.py:197` | `test_probes_allowlist.py:511-521`, `:570`, `:737`; `test_cli_contract.py:375` | DELIVERED |

## 6. SPEC statements that are not an FR, NFR or INV id but bind the delivery

| SPEC place | Where delivered or deferred | Result |
|---|---|---|
| Section 5.3 and G-1 (what an exit-1 run leaves on disk) | DESIGN section 3 `:82-155` (D1, D2): temp file, `fsync`, `os.link` commit point; `commands.py:153-208`; tests `test_cli_contract.py:1249-1480` | DELIVERED |
| Section 6 boundary rules B1 to B5 | `commands.py:22-25` imports; `classify.py`, `report.py`, `probes.py` import tests `test_classify.py:1905-1929` (B5 at `:1922`) | DELIVERED (note F4b: no AST pin for `models.py` importing no sweep module; the code complies, `models.py:10-15`) |
| Section 8 byte limits (1 MiB, 256 KiB, 8 MiB, "proposed") | `probes.py:70-75`; rationale before release is DESIGN open item 19 `:1010` (still open by design) | DELIVERED (note F3) |
| Section 11 failure-mode rows (17 rows) | DESIGN `:505-517` observation rules; tests `test_probes_allowlist.py:1474-1830`, `test_classify.py:780-870`, `test_report.py:1040`, `:1190` | DELIVERED |
| Section 14 open warnings INV-008, INV-011, INV-017 | stay open warnings by design; applied in body as traced in section 5 | DELIVERED |
| Section 15 GQ-101 to GQ-110 resolutions | DESIGN section 2.2 `:55-67`; code and tests as traced in section 3 | DELIVERED |
| Section 17 rollback and 17.1 checklist | DESIGN section 16 `:967-984`; no code deliverable | n/a |
| DESIGN addendum `design-addendum.md` (chat-summary exception), anchor `pragmatic.md:22` | `pragmatic.md:22` now reads "The only exception is the sweep chat-summary exception defined in the four sub-bullets below"; four sub-bullets `:23-26`; the qualifier "Except for the sweep chat-summary exception above" appears 6 times (`grep -c`); `SKILL.md:31-51` states the same rule | DELIVERED; tests `test_sweep_command.py:424-635` (121 cases per `test-sweep-command-summary.md`; I ran the module: part of the 719 passed). Scope is the chat reply of an actual `/sc:sweep` run only, not a general coordinator exemption (`SKILL.md:47`, `pragmatic.md:25`) |

## 7. Findings

No BLOCKING and no MAJOR finding. Six MINOR findings. MINOR findings never fail the gate.

| ID | Severity | Evidence | What is wrong | Smallest fix | Authorizing record |
|---|---|---|---|---|---|
| F1 | MINOR | `classify.py:251-257` (`_rule_working` returns None), `test_classify.py:320`, `:368`, `:372-376`, `:436-454`; DESIGN `:491`, `:760`, `:997` | SPEC FR-006's acceptance criterion "each class name is reached at least once" is narrowed: the class `working` is never produced in Phase 1. Every row that would be `working` prints `could not determine` (the safe direction, NFR-008) | None for this run; follow-up: capture a live worker's `worker-show` (`agentWait`, the `live` and `in_progress` values), then restore the four conditions kept in the comment at `classify.py:252-256` | `FINAL-GATE-halt-resolution-decision.md` change 2 (owner, 2026-11-12), written into DESIGN `:491` and `:760` |
| F2 | MINOR | `probes.py:432-434` (no `agentWait` read), `classify.py:226-236` (Rule 4(a) branch kept), `models.py:78-79`, `:90-91`; DESIGN `:997` (open item 6 "Behaviour until closed" names only Rule 5); `qa/final/fix-log-cycle1.md:33` ("OPEN: that part") | The `agentWait` branch of Rule 4(a) (waiting on a person (a) from Orca's wait entry) is also inert in a live run, for the same reason as Rule 5: no code sets `agent_wait`, and the capture saw no `agentWait` key (`1.0a-facts.md` row 6). SPEC R2 names it as one of two stand-ins for the question read; only the contract `blocked_question` stand-in (Rule 1) is live. A person-wait seen only through Orca prints under `## Could not determine`, which the report places before working rows. DESIGN open item 6 does not say this | Add "and the `agentWait` branch of Rule 4(a)" to DESIGN `:997` (a design edit, outside this gate's authority), or record it in the follow-up issue with FIN-F5 and FIN-F7 | Same cause as F1 (uncaptured live `agentWait` name), so `FINAL-GATE-halt-resolution-decision.md` change 2 covers the behaviour; the wording gap in DESIGN `:997` is not covered by a record |
| F3 | MINOR | `probes.py:257-263` (`_orca`) and `:308-310` (`_git`) call `subprocess.run(..., capture_output=True, timeout=...)`; SPEC `:286` (section 8): "run it with `subprocess.Popen` ... read the output in chunks ... Once the combined output exceeds 8 MiB, reading stops, the process is killed"; no `Popen` in `src/superclaude/cli/sweep/` (grep) | The 8 MiB limit is checked after the child finished (`probes.py:270`, `:315`), so memory is bounded only by the 10 s timeout, and the child is not killed at the limit. The class result (`call_failed`, `output over 8 MiB`; git: unread worktree) and both boundary tests are as the SPEC says. DESIGN section 13 (D1 to D10) does not list this difference | Add a D11 row to DESIGN section 13, or read through `Popen` with a chunk loop as SPEC section 8 says | none (not recorded anywhere) |
| F4 | MINOR | (a) `test_probes_allowlist.py:388-418` has `--include-remote` on `worktree ps` (3 positions) and alone, but no `orchestration worker-list ... --include-remote` case, which SPEC NFR-003 (`:132`) and NFR-014 (`:143`) name; (b) `test_classify.py:1897-1913` pins imports of `classify.py`, `report.py`, `probes.py` only, so SPEC B1 ("an AST import test fails on any other edge") has no pin for `models.py`; (c) `read_orca_version` (`probes.py:853-864`) is replaced by `lambda: None` in all tests (`test_probes_allowlist.py:211`, `test_cli_contract.py:88`, `test_readonly.py:126`), so the file read of the `version` field has no test | The code is correct in all three (a: `FORBIDDEN_TOKENS.intersection` at `probes.py:217` refuses the token in any position; b: `models.py:10-15` imports only stdlib; c: the reader returns None on a missing file, over 1 MiB or a missing field). The tests that the SPEC wording names are missing, so a later change could break the property unseen | Add one parametrized case for (a), a `models.py` banned-imports row for (b), one `tmp_path` package.json test for (c) | none |
| F5 | MINOR | `SKILL.md:35-43` and `pragmatic.md:23`: the exempt reply is the summary counts and the report path alone; `SKILL.md:25` step 3 takes only `report_path` and `summary` | During an Orca outage (exit 0, `orca_available: false`) the exempt chat reply does not say so. The report at the printed path does, and `SKILL.md:25` makes the session Read it to its last line first, and the `total is a lower bound` note still prints | Follow-up listed in the ruling: allow one outage line in the exempt reply (7 sites in `pragmatic.md`, `design-addendum.md:29` and `:37`, DESIGN 7.6 `:662`, skill steps 3 and 4 and their pins) | `FINAL-GATE-FIN-F7-ruling.md` (owner, 2026-11-12: documented limitation of Phase 1) |
| F6 | MINOR | `phase14-lint.md:54-88` (`uv run ruff format --check src/ tests/` exit 1, 12 files); I ran `git diff --quiet 5dc29d23b` on all 12: unchanged; I ran `ruff format --check` on the 20 Python files this task created or edited: "20 files already formatted" | NFR-012 lists `uv run ruff format --check src/ tests/` as a repo gate. Run over the whole tree it exits 1, because 12 Markdown files with embedded Python code that exist unchanged at the base commit are unformatted. The task's own files pass | Format those 12 files in a separate change, or drop Markdown from the format gate | Task item 14.2 (`TASK-RF-sweep-phase1-20261108-072653.md:2455`) allows a failure only in a file this task did not touch; logged in `phase14-lint.md:90-111` |

## 8. Self-audit

If I told the user "no blocking finding", the evidence behind it is: 719 sweep and command tests and 3245 scoped tests run here, all passing with no skip; ruff clean; byte comparisons of the WC-16 text, the routing byte copy and both dev copies; a line-by-line read of the SPEC (all 653 lines) and the DESIGN (all 1052 lines) so that each FR, NFR and INV was matched to a code line and a test name before it was marked delivered; and independent re-derivation of the owner-record claims from the files (grep for the removed FIN-F7 constants, line reads of DESIGN `:491`, `:614-615`, `:760`, `:838`). I looked for undelivered requirements in the places most likely to hide them (the unknown-Run shape, the `agentWait` input, the Popen mechanism, the `models.py` import edge, the version file reader, the `worker-list --include-remote` negative) and found the six notes above, none of which leaves an FR, NFR or INV neither delivered nor deferred.

## Checks

| Check | What it covers | Result |
|---|---|---|
| C1 | SPEC (653 lines) and DESIGN (1052 lines) read in full; addendum, three FINAL-GATE records and owner decision files read | PASS |
| C2 | `uv run pytest tests/sweep tests/commands tests/core tests/skills tests/recommend -q` (3245 passed) and `uv run ruff check .` (clean) run here | PASS |
| C3 | FR-001 to FR-005 each have code and a passing test | PASS |
| C4 | FR-006 to FR-010 each have code and a passing test, or a named deferral (FR-006 `working`: F1) | PASS |
| C5 | FR-011 to FR-016 each have code and a passing test | PASS |
| C6 | FR-017 to FR-021 each have code and a passing test | PASS |
| C7 | FR-022 to FR-026 each have code and a passing test (FR-023 renumbered WC-16 by D6 and OQ-3) | PASS |
| C8 | NFR-001 to NFR-008 each have code and a passing test | PASS |
| C9 | NFR-009, NFR-010, NFR-011 and NFR-013 each have code and a passing test | PASS |
| C10 | NFR-014 still pins the exact allowlist (10 templates, 7 verbs, independent literal in the test), with `worktree ps --agent-wait` allowed by R5 and recorded as D10 | PASS |
| C11 | NFR-015 version-scoped lock line, three observed-version cases tested (the file reader itself is untested: F4c) | PASS |
| C12 | INV-001 to INV-013, INV-015, INV-017 traced; INV-014 and INV-016 are not in the SPEC | PASS |
| C13 | FR-010 fixtures outage (`test_classify.py:932`), full page (`:941`), `call_failed` (`:953`) exist and assert the SPEC outcome | PASS |
| C14 | Halt-resolution changes 1 to 3 are on disk (skill step 3, pin text, removed constants and tests, DESIGN `:491` and `:760`, reserved fields and comments) | PASS |
| C15 | Cycle-2 FIN-F5: DESIGN `:614-615`, `report.py:33-39` and `:169-176`, and the two test pins agree | PASS |
| C16 | FIN-F7 graded against `FINAL-GATE-FIN-F7-ruling.md`: documented limitation, MINOR (F5) | PASS |
| C17 | WC-16 text byte-identical in contract and DESIGN; four pinned phrases present; D6 covers the WC-14 renumbering | PASS |
| C18 | R1 to R8 routing and docs rows present; plugin `HOW-WE-WORK.md` byte copy `cmp`-identical | PASS |
| C19 | SPEC 5.3 and G-1 publication rule delivered through DESIGN section 3 (D1, D2) and `_publish` | PASS |
| C20 | Style anchor `pragmatic.md:22` holds the scoped exception, qualifier appears 6 times, skill states the same rule, scope is not a general exemption | PASS |
| C21 | No `src/superclaude` string in `sweep.md` or `SKILL.md`; dev copies identical; nothing under `.claude/` staged | PASS |
| C22 | Search for an FR, NFR or INV that is neither delivered nor deferred | PASS (none found) |
| C23 | NFR-012 repo gates: `ruff check` and `ruff format --check` on the task files run here; `make sync-dev`, `make verify-sync`, `make lint` not run (not on the allowed list), taken from `phase14-sync.md` and `phase14-lint.md`; whole-tree format gate exits 1 on 12 base-commit files (F6) | PASS (reliance on the `make` targets) |

Confidence: Verified: 22/23 | Unverifiable: 1 (C23, the three `make` targets, blocker: not on the allowed command list; evidence is the two Phase 14 result files) | Unchecked: 0 | Confidence: 100.0% (22 / (23 - 1)).

Tool engagement (approximate, counted from this session): Read: 68 | Grep: 20 | Glob: 0 | Bash: 17. Each Read, Grep and Bash call above maps to a row in sections 2 to 7. No web research was done, so no Tavily or fallback call applies.

Unchecked items: none. Unverifiable items: C23 as stated.

Verdict: PASS
Blocking count: 0
