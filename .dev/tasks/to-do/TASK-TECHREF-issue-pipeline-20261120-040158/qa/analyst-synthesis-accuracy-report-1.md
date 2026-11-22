# Synthesis Accuracy and Source-Tracing Report (Partition 1 of 2)

**Analysis type:** synthesis-accuracy + source-tracing
**Partition:** 1 (synth-01, synth-02, synth-03)
**Date:** 2026-11-20
**Status:** Complete (see the final line)

[PARTITION NOTE: Cross-file checks limited to assigned subset. Full cross-file analysis requires merging all partition reports.]

Source root used: /home/coder/.cache/ic-snap-20261120/master (read only). Removed code read only through `git -C /home/coder/workspaces/IronClaude show 01e7a9e23^:<path>`. Research erratum sections (Gap-fill c1/c2) were applied as superseding.

## Claim-tracing table

| ID | Synth file and location | Claim | Research support | MATCH/DRIFT/UNTRACEABLE |
|----|-------------------------|-------|------------------|-------------------------|
| C01 | synth-01 s1 stats | Watcher package 8 modules, 4,795 lines (cycle 1,406; github 960; record 865; audit 404; launch 370; cli 348; predicates 312; runner 130), empty `__init__.py` | research 01-03 per-file counts; live `wc -l` gives the same figures | MATCH |
| C02 | synth-01 s1 stats | 59 reason words | research 01 summary line 656; live `REASON_TABLE` awk count 59; group counts in synth-03 5.1.6 (4/7/5/2/2/5/1/1/17/9/1/4/1 = 59) re-derived from audit.py:26-102 | MATCH |
| C03 | synth-01 s1 stats; synth-03 5.1.2 | per-cycle call cap 35 (32 + 3 reserved); G1/G2 shared and never refused, at most 37 calls | research 01:656 "37 calls worst case, 2 idle"; github.py:46-49, 437-463 re-read | MATCH |
| C04 | synth-01 s1; synth-03 5.1.3 | launch argv of exactly 12 elements, `ORCA_AGENT=claude`, prompt `/sc:issue --claim <N> --pipeline none` | research 02:448; launch.py:33, 84-116 re-read (12 list items) | MATCH |
| C05 | synth-01 s1; synth-03 5.1.3 | `dispatch.json` 7 top-level keys, 17-field entries, 6 states | research 02:234; record.py:34-36, 69-88, 120-130 re-read | MATCH |
| C06 | synth-01 s1; synth-03 5.1.4 | exit codes 0,1,2,3,4,5,6,7,75 and their word groups | research 02:399-401; audit.py REASON_TABLE; cli.py:34-38 | MATCH |
| C07 | synth-01 s1; synth-03 5.1.7 | 14 constants at cycle.py:34-47, 13 read, `MAX_LAUNCHES_PER_CYCLE` dead (erratum c1 B-1 applied) | research 01:658-687 ERRATUM; live grep: only definition at cycle.py:35 | MATCH |
| C08 | synth-01 s1 stats | worker agents 35 lines each (erratum c1 B-2 applied), model on line 6 tier1b/tier2/tier2b | research 04:498-510 ERRATUM; live `wc -l` 35 x3, line 6 values | MATCH |
| C09 | synth-01 s1 stats | `issue.md` 117, `SKILL.md` 197, `orca_worktree.py` 1,906, `origin_repo.py` 195, `clickup_claim.py` 270, 15 templates, `refs/claim.md` 150 | research 04:518-535; live `wc -l` and `ls` | MATCH |
| C10 | synth-01 s1 stats | Guard: `launch-level-guard.sh` 808, `launch-job-identity.sh` 582, pre-push 208, `hooks.json` 192, 18 block words | research 05:75, 318 (16 classes + LL-NOBIND + LL-BROKEN); live guard grid at :783-803 | MATCH |
| C11 | synth-01 s1 stats | Guard tests: 17 files, 24,388 lines, 921 plain (920 strict) | research 05:539 sums re-added (21115 + 3273 = 24388; 785 + 136 = 921) | MATCH (mixed 162 strict with 921 plain, see M5) |
| C12 | synth-01 s1 stats | `WORKER-CONTRACT.md` 339 lines, WC-2..WC-16, no WC-1, no WC-17; 3,220 lines and 59 tests in test_worker_contract.py | research 06; live `grep -o WC-N` gives WC-2..WC-16; `wc -l` 3220; `def test_` count 59 | MATCH |
| C13 | synth-01 s1 stats; synth-01 row 8 | Removed package: 10 files, 1,597 lines, 10 verbs, 116 tests in 10 test files plus 1 registration test | research 06; `git show 01e7a9e23^` per-file wc sums to 1597, 116 `def test_`, 10 `.command(` verbs | MATCH |
| C14 | synth-01 row 8; synth-02 s3 | Removal commit 01e7a9e23, PR #682, 2026-11-19 18:02 -0600 (= 2026-11-20 00:02 UTC); message says nothing ran this code | research 06; `git show -s 01e7a9e23` | MATCH |
| C15 | synth-01 s1 | Tests: 867 test functions, 19,801 lines, 19 `_assumed_shape` fixtures | research 01-03; live `cat | wc -l` 19801; `def test_` grep 867; fixture count 19 and test_github.py:575-583 `len(files) == 19` | MATCH (file count wording, see M1) |
| C16 | synth-01 ledger row 1 and 14; synth-03 status table | `enabled` default False at cycle.py:228; `not_enabled` exit 0 at 685-686; no scheduler artefact; SET:288 "This work does not install or enable the entry" | research 03 F.2; live cycle.py:226-230, 685-686; SET:288 quote verified | MATCH |
| C17 | synth-01 ledger row 12; synth-02 4.3 and 4.4 | IR-7 refusal off by constant `IR7_REFUSE = False` at orca_worktree.py:822, used at 1757-1758; not the `enabled` key | research 04 summary line 496; live grep 822 and cmd_launch read | MATCH |
| C18 | synth-01 ledger row 13; synth-02 4.6 | OB-H/OB-CTX observations: 12 parametrised tests all skip (test_launch_level_observations.py:79-84) | research 05; live `_PENDING` = 9 + 3 = 12, `pytest.skip` | MATCH |
| C19 | synth-01 ledger row 9; synth-02 s4.3 | Guard rule 1 / `release-worker` removed; old TAMPER case at guard :441-444 @01e7a9e23^; zero hits for `release-worker` in src/tests/plugins | research 06; `git show 01e7a9e23^:...launch-level-guard.sh` lines 441-444 contain the case; live grep empty | MATCH |
| C20 | synth-01 ledger row 18 | only marker generator was `brief.build` @01e7a9e23^ (brief.py:71-73) | research 06; `git show` brief.py:66-74 | MATCH |
| C21 | synth-01 ledger row 15; synth-02 4.4; synth-03 status table | `COORD-` has 0 hits outside .git/.dev; dispatcher/zero-setup install "not found in snapshot"; "grant row" only as prose (WORKER-CONTRACT.md:57, fu1.md:24,26) | research 03 F.2/F.3, 06; live `grep -rIl COORD-` empty; line 57 contains "grant row"; fu1.md:24,26 read | MATCH |
| C22 | synth-01 ledger row 10; synth-02 4.3 and 4.4 | `orca_worktree.py pending` verb at :1515-1523, :1886-1893; no production caller | research 04, 05; live cmd_pending at 1515; grep `worker-start` in src py empty | MATCH |
| C23 | synth-02 4.1 steps 0-14 | step order: enabled, validate_setup, lock, DISABLED, load, G1, origin, sweep, G2, order, candidates, re-read, launch, commit, conclude, with line cites (685-686, 688, 695, 712-713, 739-750, 752-775, 716-722, 777-792, 794-808, 725-737, 979-1016, 1026-1112, 1116-1144, 1176-1211) | research 01 steps 1-19; live cycle.py 680-830, 979-1112, 1128-1211 re-read | MATCH |
| C24 | synth-03 5.1.1 | exit resolution precedence 2,6,7,5,3,4; 75 only when sole condition; cycle never produces exit 1 | research 01:656; cycle.py:462-482; cli.py:123-129 | MATCH |
| C25 | synth-03 5.1.1.1 | gates E1-E15 order, words, GitHub reads per gate (G4 then G3 then G5 then G6), considered stamp except `budget_exhausted` (831-832) | research 01:94-110; cycle.py:915-961, 828-834 | MATCH |
| C26 | synth-03 5.1.1.2; synth-02 step 12 | launch step order: probe, prompt, `_revalidate` (G7, G3', G6'), day cap, DISABLED, cut-off 120 s, origin, pending save then launch; edits not re-read (1006) | research 01; cycle.py:1026-1112, 979-1016 | MATCH |
| C27 | synth-03 5.1.2; synth-02 4.5 | seven argv G1-G7 exact strings (`gh api user --include`; `gh issue list ... -L 100`; REST `--method GET ... -F per_page=100 -F page=<P> --jq`; two `graphql` calls; G7) | research 02; github.py:175-262 | MATCH |
| C28 | synth-03 5.1.2; synth-02 4.5 | watcher writes no GitHub state; five `"gh"` literals in github.py (177,183,204,231,255); cycle.py has no gh/git/orca/subprocess literal; only runner.py imports subprocess | research 02, 01; live grep `"gh"` lines 177/183/204/231/255; cycle.py grep shows docstring mentions only; `import subprocess` only runner.py:10 | MATCH |
| C29 | synth-03 5.1.3 | transitions T-1..T-13 with function line spans (fail 503-525, backoff_elapsed 528-535, sweep 627-651, mark_claimed 654-686, reset_entry 706-720), MAX_ATTEMPTS 3, backoff 10 min, lease 60 min | research 02:190-203; live record.py def lines and constants 434-443 | MATCH |
| C30 | synth-03 5.1.3 | crash points C1-C5 pinned by test_crash_injection.py, five more cycles, launcher at most once across six runs | research 02:220; test docstring lines 1-10 and test names C1-C5 | MATCH |
| C31 | synth-03 5.1.4 | verbs, options, platform-check column (status = no), `status` returns 1 unhealthy; `reset --rate-limit --forfeit-guarantee` ignores second flag (cli.py:309-313) | research 03; cli.py 111-348 read in full | MATCH |
| C32 | synth-03 5.1.4 config table | 8 allowed keys, defaults, `PVT_[A-Za-z0-9_-]{1,64}`, labels 1-50 chars, state_dir default | research 03 + erratum F-1; cycle.py:58-69, 187-192, 195-283 | MATCH |
| C33 | synth-03 5.1.5 | approval rules in `approval_of` (User actor, id in approvers, strictly after trigger and store creation, unlabel voids, same-second = `events_incomplete`) | research 01; predicates.py:185-234 | MATCH |
| C34 | synth-03 5.1.8 row 8 | agent-work-report reads `orchestrator_repo` from issue-watch.json; `load_config` rejects it, so `once` exits 2 | research 03; common.py:22-40 and cycle.py:58-69, 216-220 | MATCH |
| C35 | synth-02 4.3 contradictions | claim.md:125 says "as the worktree's pre-push hook" and IR-4 "before anything else"; code installs into the shared git-common-dir hooks and runs record/already-launched/stale-prompt checks first (1700-1724) | research 04 stale-passage list; claim.md:125 text and orca_worktree.py:1360-1445 read | MATCH |
| C36 | synth-02 4.3 contradictions | launch-prompt.md:23 names `/sc:task` as a releasing first line, guard regex at :347 accepts only `/sc:implement` and `/task` | research 04, 05; launch-prompt.md:23; guard :345-360 | MATCH |
| C37 | synth-02 4.6 level grid | IMPL/TURN blocked at W only; COMMIT/PUSH/SUBMIT/SKILL below FS; REPO, PUSHFORM, PROTECTED, MERGE, GHWRITE, UNKNOWN, MCP, ESCAPE, TAMPER, BIG at every level | research 05:75, 318; guard :783-803 | MATCH |
| C38 | synth-02 4.6 and synth-01 row 4 | L2: refuses only refs/heads/main and master; `L2-PROTECTED`/`L2-UNKNOWN` exit 1, `L2-MALFORMED` exit 2 | research 05; pre-push.sh :17, 185-208 | MATCH |
| C39 | synth-02 s3 | docs/designs line counts 942, 706, 509, 470, 627, 51, 57, 119; plugin mirror hooks.json 154 lines; three launch scripts byte-identical | research 03-05; live `wc -l`, `cmp` | MATCH |
| C40 | synth-02 s6 | state store modes (dir 0700, files 0600, audit rotation at 5 MiB keeping four), `DISABLED` via `os.path.lexists` | research 02; record.py:377, 777-792, 421-423; audit.py:106 | MATCH |
| C41 | synth-01 s1 (i) | exactly one sentence about PR 686 / rewrite design | grep of three synth files for `686|rewrite|PR 68`: only synth-01:44; other hits are line numbers (685-686, 654-686, 669-686) and the word "Rewrites" for job identity | MATCH |
| C42 | synth-01/02/03 (j) | memory-note terms (zero-setup watcher, COORD-, dispatcher, grant rows) not stated as facts | grep of all hits: every occurrence is "not found in snapshot" or "prose only" | MATCH |

Totals: 42 claims traced, 42 MATCH, 0 DRIFT, 0 UNTRACEABLE. Each file has at least 8 sampled claims (synth-01: C01-C22; synth-02: C14, C17-C19, C21-C23, C27-C28, C35-C40; synth-03: C02-C07, C16, C21, C24-C34); several claims span two files.

## Findings

| ID | Severity | Synth location | Problem | Evidence (research or source path:line) | Required fix |
|----|----------|----------------|---------|------------------------------------------|--------------|
| M1 | MINOR | synth-01 s1 "Watcher tests" row | "20 files in `tests/issue_watch/` (19 test modules plus `conftest.py`)" leaves out the empty `__init__.py`; the directory holds 21 `.py` files plus a `fixtures/` folder. The line total (19,801) does include `__init__.py` (0 bytes), and the parenthetical states the composition, so no reader is misled about the tests. | live `ls tests/issue_watch/*.py` = 21; `wc -c __init__.py` = 0 | Say "21 `.py` files (19 test modules, `conftest.py`, an empty `__init__.py`)" or leave as is |
| M2 | MINOR | synth-02 s3 tree line 16 and synth-03 key-files note ("nine modules") vs synth-01 s1 ("8 modules ... plus an empty `__init__.py`") | The same package is called nine modules in two files and eight in a third. Nine counts the empty `__init__.py` (the boundary test's `RULES` includes `__init__`), eight does not. Neither file says which way it counts. | tests/issue_watch/test_module_boundaries.py:51, 221, 240-246 (`RULES` incl. `__init__`) | Pick one convention or add "nine files counting the empty `__init__.py`" |
| M3 | MINOR | synth-01 s2.3 intro to the ledger | Says "rows 1b, 7b and 9 to 18 are additional rows" but row 12b (IR-4 enforcement preflight) is also an additional row and is not named. | synth-01 ledger rows 12 and 12b | Add 12b to the list |
| M4 | MINOR | synth-01 s2.1 diagram line 105 and s2.4 row 6; synth-02 s6 | G2 rule 2 is summarised as "allowed only with no `--to`". The guard code also refuses `--run`, `--environment`, `--pairing-code`, any name that could be read as `--to` or `--run`, any bare word, more than 64 arguments or more than 8,192 bytes. The summary is a true necessary condition but narrower than the code. | launch-level-guard.sh:496-537 | Optionally add "and no `--run`, `--environment` or `--pairing-code`" |
| M5 | MINOR | synth-01 s1 "Guard tests" row | Mixes two counting methods: "921 test functions by plain `def test_` grep (920 strict)" and "the main file ... 162 tests". 162 is the strict count; the plain count for that file is 163 (research 05:539). | research 05:328 (162) vs 05:539 (163 plain) | Write "163 (162 strict)" or drop the per-file figure |
| M6 | MINOR | synth-01 ledger row 7 | "issue-related lines only at `:23, 57, 66, 242-243`" is a judgement of relevance: the contract also mentions grants at :41-44 (WC-9 local commit grant) and the coordinator push rule at :245. None of these is an issue-pipeline duty, so the NOT BUILT status stands. | WORKER-CONTRACT.md grep for issue/grant/watcher/COORD-/adopt | Optionally rename to "lines that mention issues or the guard rule" |
| M7 | MINOR | synth-02 s4.2 intro | Cites `SK/SKILL.md:35` for "only the three helper scripts are code"; line 35 is one row of the script table and the sentence is a summary of the table, not a single-line fact. | SKILL.md:35 | Cite the table range |

| M8 | MINOR | synth-03 5.1.8 | The table of doc-vs-code contradictions lists 9 rows and does not repeat research 03's items DES:75 (platform check omits `reset`), DES 4.1 exit lists (omit 1 and 2), DES:137 and DES:154-155 (label and approvers rules incomplete), the `_ORCA_CLIS` line number, and the missing live-test file as contradictions. They are not lost: synth-06 rows X-10 to X-13 carry them and the live-test file is NOT BUILT in synth-03 5.1 status table. synth-03 does not say it defers them. | research 03 Gaps 5-10 (lines 440-460); synth-06:195-198 | Add one sentence "other doc-vs-code items: see the Section 14 or appendix table X-10..X-13" |

| M9 | MINOR | synth-03 5.1.7, rows "`LaunchOutcome.detail` (8 words), `launch_login`, `launch_account_id`, `record.disabled_present`" and "`prompt_invalid` for discovered issues" | The Status column holds "dead or write-only" and "practically unreachable", which are not one of the four allowed status words. The rows describe unused fields and an unreachable branch, not pipeline capabilities, so none of the four words fits cleanly, and the facts are true (launch.py:58-70 detail never read; record.py `launch_login`/`launch_account_id` have no reader; github.py:827-828 rejects bad numbers first). | launch.py:58-70, 264-270; record.py:69-88, 748; test_cycle.py:3348 | Use "NOT BUILT (dead field)" and "NOT BUILT (unreachable branch)" or move the two rows to a plain notes list |

No BLOCKING finding. Nothing was fabricated, no constant, argv, exit code, count or status word was found wrong, no doc-only claim is presented as current, every research `[CODE-CONTRADICTED]` item that belongs to Sections 1 to 6 is surfaced (or deferred to Section 14), and the single PR 686 sentence rule holds.

## Checks performed

| Check | Result | Evidence |
|-------|--------|----------|
| (a) no fabrication beyond research | PASS | 42 claims traced, all MATCH; every number re-derived from the snapshot or `git show 01e7a9e23^` |
| (b) paths and path:line evidence | PASS | about 60 line citations re-read live (cycle.py, github.py, record.py, launch.py, cli.py, audit.py, predicates.py, guard, pre-push, job identity, orca_worktree.py, claim.md, templates, main.py, install_hooks.py, designs); all point at the stated content; only drift is a few one-line offsets inside ranges (not graded) |
| (c) architecture backed by code-traced evidence | PASS | Section 2 diagram and ledger rows cite code lines; doc-only items carry `[UNVERIFIED - doc-only, no code confirmation]` (hand-off prose, PRs #447/#448, OB gate) |
| (d) no doc-only claim as current in Sections 2 or 8 style content | PASS | hand-off after a `--pipeline none` claim is NOT BUILT, not stated as working |
| (e) research `[CODE-CONTRADICTED]` / `[STALE DOC]` items surfaced | PASS with note M8 | synth-03 5.1.8 rows 1-9, synth-02 4.1 and 4.3 and 6; remaining research 03 items are in synth-06 X-10..X-13 |
| (f) CODE-CONTRADICTED corrected to code behaviour; UNVERIFIED flagged | PASS | e.g. skew row (erratum F-1 withdrew the contradiction and synth-03 row 1 says so), MAX_LAUNCHES dead constant (erratum B-1), agent files 35 lines (erratum B-2) |
| (g) cross-references consistent | PASS | Section 14 pointers, O-1..O-9 list, ledger rows 7/10/13-18; only the module-count wording differs (M2) |
| (h) status words only BUILT-ON / BUILT-OFF (enabled:false) / NOT BUILT / REMOVED | PASS with note M9 | every pipeline piece, hand-off and trigger row uses one of the four words (qualifiers such as "BUILT-ON as a verb, no production caller" keep the word); two cells of synth-03 5.1.7 use "dead or write-only" and "practically unreachable" (M9) |
| (i) exactly one PR 686 / rewrite sentence | PASS | synth-01:44 only |
| (j) no memory-note facts as facts | PASS | every occurrence of zero-setup, COORD-, dispatcher, grant row is "not found in snapshot" or "prose only" |

Counts: 3 synth files read completely; 6 research files consulted (01, 02, 03 fully for the cited parts; 04, 05, 06 for the cited parts); 42 claims traced (42 MATCH, 0 DRIFT, 0 UNTRACEABLE); 9 findings (0 BLOCKING, 9 MINOR); about 60 live line citations spot-read; 4 git-show reads of removed code; 0 writes outside this report.

## Verdict: PASS

BLOCKING findings: 0. MINOR findings: 9 (M1-M9).

Status: Complete

