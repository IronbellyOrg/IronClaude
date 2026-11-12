# QA Report - Read-only-claims lens (T248)

**Date:** 2026-11-12
**Phase:** cmd-skill gate, read-only-claims lens
**fix_authorization:** false

Files judged from disk on 2026-11-12: `src/superclaude/commands/sweep.md` (68 lines), `src/superclaude/skills/sc-sweep-protocol/SKILL.md` (62 lines), `src/superclaude/output-styles/pragmatic.md` (238 lines), `src/superclaude/cli/sweep/commands.py` (288 lines), `probes.py` and `report.py` (read-only claims), `tests/commands/test_sweep_command.py` (572 lines), `tests/recommend/test_routing_refresh.py`, `docs/designs/orchestrator-mode.md` 7.5 to 9, OQ-2, OQ-5 and OQ-6 records, the revision BUILD-REQUEST and design-addendum, and the six result files named in the prompt. No earlier QA report was used as evidence.

## Findings

No BLOCKING and no MAJOR finding. Six MINOR notes (they never fail the gate).

### F1 (MINOR) "the one file it adds" omits the transient temp file and created folders

- Evidence: `sweep.md:14` ("the report is the one file it adds") and `sweep.md:66` ("write any file except the one report"). `commands.py:158` (`os.makedirs(output_dir, exist_ok=True)`), `commands.py:168-170` (a hidden `.<stem>.<pid>.tmp` is created in the report folder), `commands.py:142` and `commands.py:205-207` (a temp file can be left behind; in the last case the complete report also stays and there is no success JSON), `commands.py:159` comment ("folders it made may remain").
- What is wrong: on exit 0 the sentence is true (the temp file is unlinked before `_publish` returns, `commands.py:202-208`). On an exit 1 publish failure a stray `.tmp` file (and, in one case, a report plus the temp file) can remain. The text states an absolute that the code only guarantees on success.
- Smallest fix: add "(while it publishes it makes a hidden temp file in the same folder and removes it; a publish error line says if one is left)" after the sentence at `sweep.md:14`.

### F2 (MINOR) exempt reply says "counts and path alone"; the lower-bound statement is only in step 4 and no test pins it

- Evidence: `SKILL.md:26` (step 4: "say that the total is a lower bound when `total_is_lower_bound` is true"), `SKILL.md:35` ("only the summary counts and the report path are printed"), `pragmatic.md:23` (reply "contains the summary counts and the report path"). `grep -n 'lower bound' tests/commands/test_sweep_command.py` finds nothing. Mutation M4 (private /tmp copy, clause removed from step 4): 110 passed, so the clause can disappear unnoticed.
- What is wrong: read literally, the exempt reply could drop the caveat that the total is a lower bound, which would present a partial count as complete. Mitigated by `SKILL.md:49` and `pragmatic.md:26` (truthfulness rules stay in force) and by step 4 itself, so this is an ambiguity, not a proven defect.
- Smallest fix: in the exempt bullet (`SKILL.md:35` and `pragmatic.md:23`) say "the summary counts (with the lower-bound statement when `total_is_lower_bound` is true) and the report path", and add one pin for it.

### F3 (MINOR) step 5 says "the standard error line" (one line); the command can print several

- Evidence: `SKILL.md:27` ("print the standard error line exactly as it came"); `commands.py:35-37` (`_PublishError(*lines)`), `commands.py:181` and `commands.py:192-194` (a second line such as `[sweep publish] left temp file ...` is added), `commands.py:282-285` (every line is echoed to stderr).
- What is wrong: a literal reading prints only the first line and hides the "left temp file" line, which is the one signal that a stray file remains. `SKILL.md:47` ("Standard error stays visible") partly covers it.
- Smallest fix: "print the standard error text exactly as it came".

### F4 (MINOR) never-as-worker claim is true only after plan step 1.18 lands

- Evidence: `sweep.md:16` ("It is on the never-as-worker list in `~/.claude/WORKER-CONTRACT.md`"). A search of `src/superclaude/core/` for `sc:sweep` and `WC-16` finds no match; `src/superclaude/core/WORKER-CONTRACT.md:23` lists `/sc:agent`, `/sc:git`, `/sc:help`, `/sc:issue`, `/sc:pm`, `/sc:spawn` and `/sc:swarm-wizard` only. DESIGN 8 (`docs/designs/orchestrator-mode.md:668-707`) schedules the entry (steps 1.17 to 1.19, gated on GQ-11), and the task plan carries it as a later item.
- What is wrong: a forward reference, false on disk today. It restricts (grants no right), so it is not a read-only claim defect.
- Smallest fix: no edit now; the final gate must confirm `/sc:sweep` is on that line before the PR, or reword to "is to be added".

### F5 (MINOR) the no-advice and no-new-right tests cover the skill only

- Evidence: `test_sweep_command.py:167-168` applies `_FORBIDDEN_ADVICE` to `_SKILL` only. Private /tmp mutations, all other tests untouched: M2 (a "Merge the branch once the report is clean" bullet added to `sweep.md`) gave 110 passed; M6 (the style Scope sub-bullet extended with "a coordinator in that state may also close idle sessions") gave 110 passed. Controls: M1 (command tools widened), M3 (skill `Write` added) and M5 (a "Retry" bullet in the skill) each failed exactly one test.
- What is wrong: DESIGN 7.6 (`orchestrator-mode.md:666`) only requires the skill check, so this is a hardening gap, not a deviation. The current text is clean: `grep -niwE 'stop|retry|release|merge|removal'` finds nothing in `sweep.md`, `SKILL.md` or `pragmatic.md` lines 22-26.
- Smallest fix: run `_FORBIDDEN_ADVICE` over `sweep.md` and over `_style_rule()` as well.

### F6 (MINOR) two small wording gaps

- `sweep.md:20` ("the coordinator runs `/sc:sweep` on every wake") drops the cadence cap in DESIGN 8 WC-16 and R2 ("at most once every 5 minutes"). The plan's own item text uses the same short form, so this follows the plan. Add "at most once every 5 minutes" if the final gate wants the cap in the command.
- `tests/recommend/test_routing_refresh.py:29-32` comment lists #323 and #302 as the reasons for `_POST_REFRESH_ADDITIONS` but not the new `sweep` entry (issue #339). The git diff is exactly the one added string at line 33.

## Method notes

- Mutation experiments ran only on a private copy under `/tmp/t248-copy.*` (copy deleted afterwards, `ls` shows none left). Baseline copy: 110 passed. M1 to M6 results are in F2 and F5.
- Repository run: `uv run pytest tests/commands tests/recommend -q` gave 628 passed; `uv run ruff check` on the test files and `src/superclaude/cli/sweep` passed; `uv run ruff format --check` on the two test files passed. Result files agree: `test-sweep-command.txt` 110 passed exit 0, `r5-routing-refresh.txt` 248 passed, `phase11-validation.md` 718 passed (includes the two severity modules, which I did not rerun).
- Style diff against HEAD: seven hunks (`@@ -22 +22,5`, `-53 +57`, `-58 +62`, `-60 +64`, `-69 +73`, `-80 +84`, `-90 +94`), lines 1-21 and everything from `## Work discipline` identical to HEAD, no non-ASCII character in added lines. `git show HEAD:...pragmatic.md` line 22 is the old "No exceptions." mandate, so the pre-7.10 anchor is correct.
- Limits: static text and code reads only. No live Orca, ccsession or Claude command was run, and nothing here proves a live model follows the exception.

## Checks

| Check | What was checked | Result |
|---|---|---|
| C1 | Command `allowed-tools: Skill` equals DESIGN 7.6 (`sweep.md:9`, `orchestrator-mode.md:655`) and is no wider than `graph.md:9` | PASS |
| C2 | Skill `allowed-tools` literal equals DESIGN 7.6 exactly (`SKILL.md:4`, `orchestrator-mode.md:661`); no Write, Edit or other tool; body names only the two Bash forms and Read (`SKILL.md:62`) | PASS |
| C3 | Sentences about what the sweep writes or changes (`sweep.md:14`, `:55`, `:66`; `SKILL.md:15`, `:60`) against `commands.py` `_publish`: one report under `<root>/.dev/sweeps/`, JSON on stdout, nothing else (true on success; see F1) | PASS |
| C4 | Option table (run id regex, duplicates, window 1-9999 and 720h/30d, root `.git`, output under `.dev/sweeps/` and non-overlap, no-Run message) against `commands.py:43-123`, `:219-245` and `probes.py:44`, `:352-362` | PASS |
| C5 | OQ-2 location and file name and OQ-5 `6h` default as stated in the primitives (`sweep.md:25,33-38`) against `commands.py:27`, `:101-123`, `:155` | PASS |
| C6 | No stop, retry, release, merge, removal or Orca write verb (and no delete, close, push, commit advice) in `sweep.md`, `SKILL.md` or `pragmatic.md:22-26` | PASS |
| C7 | "changes nothing in Orca, in git or in any worktree" against `probes.py:47-64` (read-only Orca templates, one `git --no-optional-locks status`) and `probes.py:296-297` (`GIT_OPTIONAL_LOCKS=0`) | PASS |
| C8 | Skill steps: PATH-first, fallback only on "command not found", timeout 120000 each, only `report_path` and `summary` parsed, report Read in chunks of 150 lines, no third run (`SKILL.md:23-29`) | PASS |
| C9 | Scoped exception grants no role or action right: assignment must be explicit and for specified work, skill and style do not assign, files, reports and peers never establish it, person-run, worker, subagent and failure cases stay ordinary (`pragmatic.md:23-25`, `SKILL.md:35-47`) | PASS |
| C10 | Exception changes no runtime write, report or JSON: scope clauses (`pragmatic.md:26`, `SKILL.md:49`) and no reference to the exception in `src/superclaude/cli/sweep/` or its registration (`main.py:567-569`) | PASS |
| C11 | Exception does not hide failures: success needs exit 0, parsed stdout, successful Read (`SKILL.md:36-41`); stderr stays visible, no fabricated summary (`SKILL.md:29`, `:47`); see F2 and F3 for wording gaps | PASS |
| C12 | Style edit bounded against HEAD (seven hunks, head and tail identical, ASCII) and six later restatements qualified | PASS |
| C13 | Pre-7.10 anchor: HEAD line 22 held the unqualified mandate; working line 22 holds the scoped exception | PASS |
| C14 | Exception no broader than OQ-6 (b) and the design-addendum (narrower: final successful reply only, top-level coordinator assignment) | PASS |
| C15 | `test_sweep_command.py` reads the real sources (no mock policy), pins both files, and its static-only limit is stated (module docstring lines 13-16); 110 cases reproduced on a copy and 628 in the repository run | PASS |
| C16 | `git diff -- tests/recommend/test_routing_refresh.py` adds only `"sweep"` to `_POST_REFRESH_ADDITIONS` (DESIGN 9 row R5) | PASS |
| C17 | Result files (`step-1.14-checks.md`, `step-1.15-checks.md`, `step-7.10-style-exception.md`, `test-sweep-command-summary.md`, `test-sweep-command.txt`, `r5-routing-refresh.txt`, `phase11-validation.md`) match the files on disk (hunks, counts, cited lines `SKILL.md:29,37-49`) | PASS |
| C18 | House pattern: Activation block and `name: sc:sweep-protocol` as in `graph.md:41-46` and `sc-graph-protocol/SKILL.md:2`, no Unattended mode section, no `src/superclaude/` path | PASS |
| C19 | Role-claim sentence `sweep.md:16` (never-as-worker) is true on disk | PASS (forward reference, F4) |
| C20 | Tests would catch new advice or a new right in the three primitives (mutations M1 to M6) | PASS (gaps for the command and the style are F5, not required by DESIGN 7.6) |

Verdict: PASS
Blocking count: 0
