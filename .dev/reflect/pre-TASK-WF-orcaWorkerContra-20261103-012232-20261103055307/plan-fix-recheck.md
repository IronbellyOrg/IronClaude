# Plan fix recheck: TASK-WF-orcaWorkerContra-20261103-012232 (version 2)

Reviewed 2026-11-03, read-only. Plan = `.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md` (TL:N, working tree), diff taken against the index copy. Spec = `source.md` in the same package (SRC:N).

## Verdict

**FAIL**, with 1 blocking finding (N-01). All 12 approved fixes are applied. But the new wording of the D-001 fix (TL:21) makes an "only file" claim that the plan breaks itself: Tasks 5 and 6 must create `tests/skills/test_worker_contract.py`, which is a file under a directory named `skills`. This is the same halt path as D-001: a quotable Constraint that no repair can satisfy. Fixing it takes one phrase. Everything else is a note.

## Fix-by-fix status

| Deviation | Status | TL line(s) | Check |
|---|---|---|---|
| D-001 (M-01) | fixed as the report recommends, but the new wording causes N-01 | TL:21 | Says "no command file, no `SKILL.md` and no agent file" and names the one sc-recommend refs copy, which matches R-001 word for word. The exhaustive "only file ... under a skills directory" clause is the new defect. |
| D-002 (M-02) | fixed | TL:23, TL:65 | Adds the installed-paths Constraint. It names `CAPS:`, `INV-` and `EVIDENCE.md:` and forbids `src/superclaude/...` and other repo-path citations. Task 1 has a matching AC (TL:65). Task 2 has none, but the Constraint covers it. |
| D-003 (M-03) | fixed | TL:147-156 | Five categories with one-line reasons. Entries are keyed by path, verb and stripped line text, not by line number, and the regex is one module constant. See N-02 on the word-boundary claim. |
| D-004 (M-04) | fixed | TL:22 | Adds a brief-template exception for the section 3.1 "Brief must pass" flags and the section 6 phase markers, with `--report-dir` marked "from P1". |
| D-005 (M-05) | fixed | TL:73, TL:132, TL:55, TL:77 | Uses the spec's own words, "maximum of 10 inputs" and "at least 2 inputs are admitted" (both verbatim at SRC:122). "(as written in section 2.3)" is gone. Tasks 1 and 2 now record phrases. |
| D-006 (M-06) | fixed | TL:178-183, TL:191 | Saves AC-0.1, AC-0.2, AC-0.3, AC-C1 and AC-C2 as `./artifacts/<id>.txt`. The AC lists every evidence file. See N-05 on the unnamed AC-C5 record. |
| D-007 (M-07) | fixed | TL:135 | A conditional byte-identity assertion that follows the `test_plugin_mirror_matches_src` pattern (it exists at `tests/commands/test_workflow_command.py:93`). |
| D-008 (M-08) | fixed | TL:110 | ASCII only. A new top-level `##` section after `<!-- /routing-table -->`, outside all three marker pairs. |
| D-016 (M-16) | fixed | TL:38-48, TL:63, TL:115 | Lists the 8 failing tests as the accepted baseline. `t1-accepted-failures.md` and `t4-wider-compare.md` are cited, not the raw logs. See N-04. |
| D-017 (M-17) | fixed | TL:36, TL:115 | Uses `--ignore=tests/cli/eval/test_perf_home_setup.py`, an equivalent of the recommended `--deselect`, on both the baseline run and the Task 4 run. `git status --short` is checked after each run. |
| D-018 (M-18) | fixed | TL:147 | A post is a `gh api` call whose method is not GET. `--method GET` or `-X GET` with `-f` or `-F` counts as a read. Ships together with D-003. |
| D-019 (M-19) | fixed | TL:22, TL:55, TL:124 | Exempts the worker-session duties from verbatim copying and names phrases for WC-12, WC-13 and heartbeats. Task 5 asserts the recorded phrases, copied into the test as data. See N-03. |

Minor items D-009 to D-015 were left out, as decided. They are not counted here.

## New findings

### N-01 (blocking): TL:21's "only file under a skills directory" is false for this plan's own test file
- **TL line:** TL:21 against TL:120 and TL:124 (Task 5 creates `tests/skills/test_worker_contract.py`), TL:147 (Task 6 extends it), and TL:188 (Task 8 lists it for the commit).
- **Problem:** TL:21 says "The only file this plan writes under a skills directory is the byte-for-byte copy of `HOW-WE-WORK.md` at `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` that Task 4 makes." `tests/skills/` is a directory named `skills`, and Tasks 5 and 6 must write a file there. The text is byte-present in the Constraints, so under qa.md:52 and qa.md:61 a reviewer who reads it literally gets a mechanically confirmed B4 blocker. The managed FINAL also returns `issues` on a violated Constraint (qa.md:310). No repair satisfies both rules, because the spec fixes the test path (SRC:220, P0 row). This is the same "no repair satisfies both" mechanism that made D-001 blocking. `make sync-dev` (TL:24, TL:110) also writes all of `.claude/skills/`. Today that directory is missing in this worktree: `make verify-sync` reports `MISSING in .claude/skills/` for every skill. `.claude/` is gitignored, so it should not appear in the reviewed diff, but it is a second literal breach of the same sentence.
- **Fix:** Narrow the clause to skill packages. For example: "The only file this plan writes inside a skill package (`src/superclaude/skills/` or `plugins/superclaude/skills/`) is the byte-for-byte copy ... that Task 4 makes; `tests/skills/test_worker_contract.py` is a test file, and the `.claude/` copies `make sync-dev` writes are sync output." Alternatively, drop the "only file" sentence and keep just the SKILL.md ban.

### N-02 (note): "word boundaries, so `git merge-base` is not `git merge`" is technically false
- **TL line:** TL:147.
- **Problem:** A regex word boundary sits between `e` and `-`, so `\bgit merge\b` matches `git merge-base`. Checked with `uv run python`: the result is `True`. The scan roots hold 6 `git merge-base` lines. An implementer who uses `\b` gets those 6 hits. The `read-only` category (TL:154) still lets the test pass, but the delivered regex then contradicts the quoted instruction. That costs a QA attempt, though a regex repair closes it, so it does not halt.
- **Fix:** "Match each verb as whole words, not followed by a word character or `-` (for example `(?![\w-])`), so `git merge-base` is not `git merge`."

### N-03 (note): phrase-count wording conflicts with the named WC-12 phrases
- **TL line:** TL:55 and TL:64 against TL:22.
- **Problem:** TL:55 asks for "one short phrase" per rule but names two phrases for WC-12. TL:64 says "names one phrase per rule". TL:22 says the duties are "not copied verbatim", while TL:55 copies the WC-12 title verbatim. None of this is Orca verb syntax, and all phrases are present in the spec, so the no-copy rule is not broken. Only the counting is inconsistent.
- **Fix:** Say "at least one phrase per rule" in TL:55 and TL:64. In TL:22, say "not copied in full".

### N-04 (note): residual risk that a raw baseline log is cited on a `complete` line
- **TL line:** TL:48 and TL:63.
- **Problem:** TL:63's first AC is that the raw logs exist. The natural evidence for that AC is the raw `t1-baseline-wider.txt`, whose outcome line shows `8 failed`. qa.md:310 turns a cited log that shows a failure into `issues`, which ends in `E-ARCHIVE-BLOCKED`. TL:48's "Cite that file, not the raw logs" steers away from this but does not change the AC. There is also a label drift: TL:48 marks failures as "in the list above or new" and then calls them "pre-existing", while TL:63 says "accepted ... or pre-existing".
- **Fix:** Reword the AC as "`t1-accepted-failures.md` records that both baseline files exist and lists every failing test", and use the labels `accepted` and `pre-existing` consistently.
- **Context:** `test_V1_clean_tree_exits_zero`, `test_V2_...` and `test_V7_...` fail today because `.claude/` is unsynced in this worktree (`make verify-sync` exits 2 with MISSING lines). They should pass after Task 4's `make sync-dev`. AC-C2 is still checked on its own (TL:116, TL:183), so accepting V1 hides nothing.

### N-05 (note): the AC-C5 evidence file has no name
- **TL line:** TL:185 and TL:191.
- **Problem:** TL:191 requires that each evidence file "exists", but it lists "the AC-C5 record" without a file name, and TL:185 does not say where the record goes.
- **Fix:** Name it `./artifacts/ac-c5.txt` (recorded as run with an empty edit set).

### N-06 (note): the installed-paths Constraint needs rewording in Task 2
- **TL line:** TL:23 against TL:73.
- **Problem:** Section 2.3's seven-condition check cites `ledger.md:71` and `refs/retry.md:498` (SRC:114, SRC:116). The contract cannot copy these citations as they stand. They are satisfiable with installed paths (`~/.claude/skills/sc-implement-protocol/refs/...`). Rule-content paths such as `.dev/tasks` and `.dev/worktrees/` are not citations. This is achievable, so it is not a conflict.
- **Fix (optional):** Add "rewrite skill citations as `~/.claude/skills/<name>/refs/...` paths" to TL:23.

Checked with no conflict found:
- `--ignore` against AC-C3: AC-C3 runs `tests/skills/` only, and the perf test is under `tests/cli/eval`.
- The 8 accepted failures against AC-C3: all 8 are in `tests/cli`.
- The baseline and the Task 4 comparison both use the same `--ignore`.
- The five Task 6 categories against SRC:305: every category is "an explicit allowlist with a reason", and `wc9-allowed` matches "allowed by WC-9".
- Task 8's evidence files are each produced by a named task: AC-0.7 and AC-C6 by Task 7, AC-0.9 and AC-C3 by Task 6, and the rest by Task 8.

## Self-audit

Factual claims the edit added, all checked true in the repo:
- The 8 test ids exist as test functions:
  - `test_ban_import_rule.py:79`, `:99` and `:137`;
  - `test_claude_process_adapter.py:417` and `:463`;
  - `test_verify_sync_hooks.py:124`, `:146` and `:197`.
- `test_plugin_mirror_matches_src` is at `tests/commands/test_workflow_command.py:93`.
- `tests/cli/eval/test_perf_home_setup.py` writes `TASKLIST_ROOT/evidence/T02.15/perf.json`, where `TASKLIST_ROOT` is `.dev/releases/current/cliEval` (lines 105-117 and 264), and that `perf.json` is tracked.
- `HOW-WE-WORK.md`'s last line is `<!-- /routing-table -->` (line 393), followed by a trailing newline, so appending deletes no line (AC-0.3 is safe). No routing test assumes end of file.
- The WC-12 phrases are in source.md: "Coordinator follow-ups are pulled, not pushed" and "at natural checkpoints" at SRC:80, "No Orca fan-out from the worker session" at SRC:81, and "at the cadence its preamble sets" at SRC:78.
- The fan-in phrases are at SRC:122.

Format gate (quality-gates.md:26-36):
- There are no checkbox or numbered lines.
- Tasks 1-8 are contiguous.
- All 8 tasks have `Acceptance criteria:`.
- Every `Depends on` names a lower task.
- `version: "2"` is a positive integer, and the plan is ASCII only.
- The gate passes.

Also read:
- the diff;
- merged-verdict M-01 to M-19;
- REPORT D-001 to D-019 and R-001 to R-019;
- qa.md:35-99 and qa.md:270-310;
- source.md sections 2.1-2.3, 6, 7.1 and 7.3;
- the Makefile `sync-dev` and `verify-sync` targets.

`make verify-sync` was run read-only. It exits 2 today because `.claude/skills/` is missing in this worktree. No test suites were run, and no file was changed except this review.

## Recheck after fix pass 1

Read-only. I re-read the plan (TL:17-194) and ran `git diff -- <plan path>` against the index (51 insertions, 17 deletions). No test suites were run.

### Verdict

**PASS.** N-01 to N-06 are all applied, and no new blocking defect was found.

### Status of N-01 to N-06

| Finding | Status | TL line(s) |
|---|---|---|
| N-01 | fixed. The clause is now limited to "inside a skill package (`src/superclaude/skills/` or `plugins/superclaude/skills/`)". It names `tests/skills/test_worker_contract.py` as a test file and the `.claude/` sync copies as sync output. | TL:21 |
| N-02 | fixed. "not followed by a word character or `-` (for example the lookahead `(?![\w-])`)" | TL:147 |
| N-03 | fixed. "at least one phrase" appears in TL:55, TL:64 and TL:80. TL:22 says "not copied in full". | TL:22, TL:55, TL:64, TL:80 |
| N-04 | fixed. `t1-accepted-failures.md` records that both baseline files exist, uses the labels `accepted` and `pre-existing`, and states that no tracked file changed. It is the cited evidence. The raw logs are now only inputs and appear in no AC as evidence. | TL:48, TL:63 |
| N-05 | fixed. `./artifacts/ac-c5.txt` is named in the Task 8 instructions and in its AC list. | TL:185, TL:191 |
| N-06 | fixed. The installed-path rewrite of skill citations is stated, with the `ledger.md:71` and `refs/retry.md:498` example. | TL:23 |

### TL:21 checked against every file Tasks 1-8 write

| Task | Files written | Inside `src/superclaude/skills/` or `plugins/superclaude/skills/`? |
|---|---|---|
| 1 | `src/superclaude/core/WORKER-CONTRACT.md`, `src/superclaude/cli/install_core.py`, and package `./artifacts/` | no |
| 2 | `WORKER-CONTRACT.md` and `./artifacts/t1-rule-phrases.md` | no |
| 3 | an optional `plugins/superclaude/core/WORKER-CONTRACT.md` (under `core/`, not `skills/`) and `./artifacts/t3-plugin-mirror.md` | no |
| 4 | `src/superclaude/core/HOW-WE-WORK.md`, `.claude/` through `make sync-dev` (named as sync output), and `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` (the one named exception) | only the named exception |
| 5 and 6 | `tests/skills/test_worker_contract.py` (named as a test file) and scratch files under `tmp_path` (TL:141 and TL:160 forbid any scratch file under `src/superclaude/`) | no |
| 7 and 8 | `./artifacts/` only, plus `git add .dev/tasks` | no |

`make sync-dev` writes only to `.claude/` (Makefile:109-158). No task instruction or AC now conflicts with TL:21.

### Format gate

Still passes:
- there are no checkbox or numbered lines;
- Tasks 1-8 are contiguous;
- all 8 tasks have `Acceptance criteria:`;
- the plan is ASCII only;
- `version: "2"`.

### Notes (not blocking)

- **R1-01 (note, TL:115):** The Task 4 comparison "names each remaining failure as accepted in `./artifacts/t1-accepted-failures.md`". That file now uses two labels, so a failure labelled `pre-existing` that still fails would be called "accepted" here. This matters only if a failure outside the list of 8 shows up, and a repair can satisfy it either way. Fix: "names each remaining failure by its label (`accepted` or `pre-existing`) in ...".
- **R1-02 (note, TL:21):** A test run can leave `__pycache__/` inside a skill package if a test imports a skill's Python script. `git check-ignore` confirms such paths are ignored, so they never appear in a reviewed diff. This is the same case as the `.claude/` sync output. No change is needed.
- **R1-03 (note, TL:77):** Task 2's instruction still says "Append one phrase per rule", while its AC says "at least one". One phrase meets "at least one", so there is no conflict.
