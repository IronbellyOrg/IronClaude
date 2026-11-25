# Review safety-scan (`superclaude review safety-scan`)

Read from origin/master, 2026-11-17. Footer token: graph:stale.

## 1. What it is
A small command that reads a text file, one row per line, and prints any row containing a destructive or secret-related word (delete, overwrite, force, token, secret, password, chmod, credential, wipe). It exists because the framework is being changed to treat fewer review findings as "blocking" (issue 552, a program to loosen blocker classification), and the one rule that must not loosen is "a safety risk is never downgraded". A model may grade a dangerous row as minor, so plain code scans the minor rows and shows hits to a person. "Print-only" means the command and its skill wiring only print lines: they ask nothing, store nothing, file no issue, and change no verdict, review result or archive outcome.

- PR: #581, merged 2026-11-17 00:30 UTC (commit dated 2026-11-16 19:30 -0500). Title "feat(review): safety-scan command and print-only follow-up paragraph (issue 552 stage 0 and 1)". It also carries stage 0 evidence (inventory freeze, a regrade with a control test, spec errata), the shadow-model-combos data folder (other agent), and unrelated `sc-reflect-protocol` shadow-mode fixes.
- Entry points: `superclaude review safety-scan <file> [--unattended]`; `src/superclaude/cli/review/safety_cmd.py`, `safety_route.py`, registration in `__init__.py`; skill paragraph "Follow-up print (record and print only)" in `src/superclaude/skills/sc-implement-protocol/SKILL.md` and `refs/managed-workspace.md` (plus byte-equal plugin twins); tests `tests/review/test_review_safety_cmd.py`, `test_review_safety_route.py`.
- Brief correction: the PR did not add a safety-scan paragraph to `sc-reflect-protocol`. Its edits there (SKILL.md, refs/reviewer-spec.md) pin the shadow card model, write `merged-verdict.yaml` and count first-parse findings-block compliance. A grep for "safety-scan" under that skill on origin/master finds nothing.

## 2. How it works
Why it exists. Issue 552 says review gates call too many findings "blocking" and force fix cycles (`.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/00-issue-description.md`). The program spec (`02-brainstorm/merged-requirements.md`, rows GR1 and GR12 at lines 650 and 661; "GR" = guardrail) keeps one hard guard: GR1 "Safety is never downgraded", backed by a code scan of every Medium and Note finding for destructive and secret vocabulary kept in one list. GR12 says a hit is never written as a plain follow-up: attended, show it to the person; unattended, mark the run partial. Stage 0 measured the old rule; stage 1 first planned a classifier, ledger codec and skill folder (16 tasks). A cuts debate (Revision 4 in `.dev/tasks/archive/to-do/TASK-WF-blockerStage1-20261116-030154/source.md`) cut that to two tasks: this scan and the print paragraph.

Data flow (one file in, text out):
1. Skill (or a person) runs `superclaude review safety-scan <notes file>`.
2. `scan_file` (`safety_route.py:87-102`) reads bytes and decodes UTF-8. Missing file, directory, OS error or bad UTF-8 returns an `Unreadable` object, not a zero.
3. `scan_text` (`:63-84`) walks lines. Blank lines are not rows. A row beginning `superseded ` is counted as skipped, never scanned (`:37`, `:72`). Other rows are matched by a regex built from `VOCABULARY` (`:19-34`): case-insensitive, match at word start, so "deleted" and "tokens" hit and "reinforce" does not. First match per row wins.
4. `safety_cmd.py:30-40` prints `SAFETY HIT line N (word), graded blocking: <row>` per hit, then `safety-scan: R rows read, S skipped, H hits` (or `file is empty, 0 rows read`).
5. Attended with hits: prints the prompt "Show these rows to the person before they are treated as follow-ups." (`:13`, `:44`). With `--unattended`: no prompt, last line `safety-scan signal: partial` or `none` (`:41-42`).
6. Exit 0 for any readable input (a hit is information). Unreadable input prints `safety-scan: cannot read <path>: <reason>`, exits 2, and prints no hit count (`:27-29`), so a missing file cannot look like a clean scan.

`raise_outcome(graded, has_hit)` (`safety_route.py:105-114`) is the GR12 raise-only rule: outcomes ordered Note, Medium, Blocking; a hit returns Blocking, no hit returns the graded value, nothing is ever lowered, unknown outcome raises ValueError. The command does not call it: it only prints the words "graded blocking".

Skill wiring. `sc-implement-protocol/SKILL.md` lines 194-200 (Done section) say: at the final review step print every non-superseded minor line of each task's `<retries>/T<id>/notes.md`, run the scan on each notes file, print hits first, print "no notes file for T<id>" when a file is missing (a clean task writes none), ask nothing, make no offer (the offer belongs to the top-level session), change no verdict, add no stop code; a missing `superclaude` command or non-zero exit is one printed line and the run continues. `refs/managed-workspace.md` (lines about step 5 to 6) runs it only when the final review returned `FINAL: pass`, before the helper moves the package, so each run prints once.

Safety limits. No network, no subprocess, no classifier or ledger import: test `test_module_imports_no_unrelated_reader_and_makes_no_call_out` parses the module imports and rejects names matching classif, codec, ledger, follow_up, subprocess, requests, httpx, socket. Registration in `__init__.py:19-38` loads each subcommand module through importlib and skips only a missing module of that exact name, so parallel branches adding subcommands do not conflict.

Tests: `tests/review/test_review_safety_route.py` (each word hits, case and word-start rule, superseded skip, blank lines, empty input, raise-only property, unreadable input as its own result, import ban) and `test_review_safety_cmd.py` (exact output lines, empty file, unattended `partial` and `none`, exit 2 for missing, directory and non-UTF-8). The stage 1 package kept a smoke log (`.dev/tasks/done/TASK-WF-stage1Request-20261116-221852/artifacts/print-smoke.txt`).

## 3. Where it could be integrated in future
- Any review or QA gate that grades findings and then loosens or batches the low ones (reflect, tasklist and roadmap validators, spec panels, PR-review monitors). Why: the scan is the cheap, model-free backstop for "a risky row was labelled minor".
- Pre-filing checks for follow-up issues. Before a minor row is turned into a GitHub issue or backlog item, a hit says "show a person first".
- Worker and unattended pipelines (Orca workers, sprint, sweep). The `--unattended` signal line (`partial` or `none`) is machine-readable, so a coordinator can mark a worker partial without parsing prose.
- CI or pre-commit lint of plan and task files that hold shell recipes (destructive-word check on `.dev/tasks/` plans).
- A future classifier or judge model, as the "never downgrade" floor under it. The spec already plans this (GR12 applies "in every stage including shadow").

## 4. Integration guide
Best route: call the CLI from a skill, as `sc-implement-protocol` does. It keeps skills free of Python imports and works from any project (installed primitives must not point at `src/superclaude/` paths).

1. Produce a plain text file with one finding per line, only the non-blocking rows (Medium and Note). Rows that are history start with `superseded ` and are skipped.
2. Run `superclaude review safety-scan <file>` (add `--unattended` in worker mode).
3. Read the result: exit 2 means the input could not be read (report it, do not treat as clean); exit 0 with `H hits` greater than 0 means show the printed `SAFETY HIT` rows first. Unattended: last line `safety-scan signal: partial` means set the worker status to partial and name the rows in the report line; `none` means nothing to do.
4. Never convert a hit row into a plain follow-up. If your flow has grades, apply the rule "raise only": a hit makes the row Blocking (`raise_outcome`), nothing lowers a grade.
5. Tolerate a missing command: print one line and continue, as the implement paragraph does.
6. If you edit a skill under `src/superclaude/skills/`, run `make sync-dev` and keep the plugin twin byte-equal (`tests/skills/test_review_severity_rule.py::test_h_implement_protocol_plugin_twins_byte_equal` pins the implement one).

Reuse: `safety_route.scan_text` and `scan_file` for Python callers (they return frozen dataclasses `ScanResult` and `Unreadable`); keep `VOCABULARY` as the only word list. Do not copy the list into prompts.

Pitfalls: the match is by word start only, so "forced" and "tokenize" hit (false positives likely, for example "token" in a parser discussion) and misspellings, synonyms ("remove", "rm", "drop", "truncate", "key") do not hit. It reads one row per line, so a row wrapped over two lines is scanned per line. Only the first matching word is reported per row. Exit 0 on hits means a caller that checks only the exit code sees success.

Tests to add when integrating: a fixture file with one hit, one superseded hit and one clean row through the new caller; unreadable input path (exit 2 must not be read as clean); unattended `partial` mapping; a test that the caller never lowers a grade; vocabulary-extension test if the list grows (route test pins the nine words as one list).

## 5. IronClaude fit
Ranked. Verified from origin/master: `sc-pr-submit-protocol/SKILL.md:20` (re-grades each finding's severity; the project rule is that findings below Medium are only reported, not fixed), `cli/review/findings_v2.py:46` (a `safety` category exists), and the `cli/review/` command set (`fixcheck`, `ledger`, `panel`, `manifest`, `cluster`).

1. PR-review monitor, `src/superclaude/skills/sc-pr-submit-protocol/` (refs/severity-routing.md, Wave 2) and `src/superclaude/pr_submit/`.
   - Change: after `remap_severity`, write the below-Medium findings to a temp file and run the scan; a hit raises the finding to Medium so it is fixed, or is reported as a safety row.
   - Value: high. Today a Low finding about a secret or `rm` is only reported, which is exactly the downgrade GR1 forbids.
   - Effort: low to medium (a skill paragraph, a small row-writer, one test). Risk: low; false positives only add a fix or a report line. Check the exact routing file first (not read here, UNVERIFIED).
2. Reflect and review loop, `src/superclaude/skills/sc-reflect-protocol/` and `src/superclaude/cli/review/` (`findings_v2.py`, `ledger.py`, `fixcheck.py`).
   - Change: a new subcommand or flag that scans the claim text of non-blocking findings-v2 rows and ledger rows, and tags hits. Wire into the Tier 2 merge step as a print, then later as the raise-only rule (`raise_outcome`, currently unused in production).
   - Value: medium to high, it is the intended next stage of issue 552 (stages 2 to 4 are in the program folder). Effort: medium. Risk: medium, because it touches review-loop carriers and the program says a person approves each stage in chat.
3. Other print-and-continue final reviews: `sc-troubleshoot-protocol` (Tier 3 remediation notes), `sc-tasklist-protocol` and `sc-workflow-protocol` reviews, `/sc:task`.
   - Change: copy the sc-implement paragraph (print, ask nothing). Value: medium. Effort: low per skill, but each needs its plugin twin and sync. Risk: low.
4. Task and plan files that contain shell recipes (`.dev/tasks/*` plans checked by `sc-implement-protocol`): a pre-execution scan of recipe lines. Value: low to medium, noisy because plans legitimately say "delete". Effort low. Risk low.

Not a good fit: anything needing meaning ("is this delete safe?"). The scan is words only; that judgement stays with a reviewer or person.

## 6. Limits, open questions, UNVERIFIED
Limits
- Word list of nine, word-start match, first hit per row only, English only. False positives (token, force) and false negatives (remove, drop, rm, key, truncate) are both expected.
- Prints only. Nothing enforces that a skill acts on a hit; the agent following the skill text must show it. The `raise_outcome` rule exists but nothing in production calls it (grep of src and tests on origin/master: only tests).
- Exit 0 on hits, so scripts must read the output or the `--unattended` signal line, not the exit code.
- Only `sc-implement-protocol` calls it. Hits are not stored anywhere, so there is no audit trail beyond the printed text.
- The cut stage 1 left out the classifier, the follow-up ledger, the skill folder `sc-review-severity` work and the owner summary. Whether stages 3 and 4 will add them is open; the request file says stage 2 is withdrawn into this package.
- `tests/skills/test_review_severity_rule.py` has the plugin twin test; whether the test ran green in CI for #581 was not checked.

Open questions
- Should the vocabulary grow (rm, drop, truncate, key)? Spec says "and similar" (merged-requirements.md line 650).
- Who owns the "offer to file" step? The skill text says the top-level session; that flow is not built.

UNVERIFIED
- Exact line numbers in `refs/managed-workspace.md` (paragraph located by text, not by number).
- `sc-pr-submit-protocol/refs/severity-routing.md` contents and where a scan would hook in.
- Whether other skills on origin/master call `safety-scan` (grep of `src/superclaude/skills` found only the two sc-implement files).
- The shadow-model-combos data in the PR, covered by another agent.
- Codegraph facts (index does not cover origin/master).

---
graph:stale (codegraph not used; all facts from `git show origin/master:<path>`).
