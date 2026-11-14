# QA Report: Task Integrity, Lens B2 Self-Containment (Partition 2 of 2: Phases 8 to 14)

**Topic:** Issue #339 Phase 1, sweep CLI task file
**Date:** 2026-11-08
**Phase:** task-integrity
**Lens:** b2-self-containment
**Fix cycle:** N/A
**fix_authorization:** false (report only; task file not edited)
**Task file:** /home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md

[PARTITION NOTE: Cross-file checks limited to Phases 8 to 14 (lines 1265 to 2479) plus the frontmatter (1-69) and Execution Context (117-202). Full cross-file verification requires merging with the Phase 1 to 7 partition report.]

## Overall Verdict: FAIL

9 blocking (IMPORTANT) findings, 0 CRITICAL, 10 MINOR notes.

## Progress log

- Read frontmatter (1-69) and Execution Context (117-202). The shared QA Gate Protocol (186-192) holds the report-only, fix and verifier preambles; it tells the executor to "embed verbatim in every report-only agent spawn", but the text lives only in the header.
- Read Phases 8 to 14 in chunks of at most 150 lines (1265-2479).
- Grepped item 2.17, 2.21, 2.25 (lines 354, 382, 410) to confirm the procedures later gates point to live only there.
- Grepped DESIGN for `[sweep publish]` messages (6 distinct, lines 106, 110, 123, 124, 126, 128).
- Diffed the item 14.44 runner prompt (lines 2364-2372) against `~/.claude/skills/task-builder/SKILL.md:2223-2231` after filling the placeholders: IDENTICAL.
- Read `~/.claude/skills/sc-reflect-protocol/SKILL.md:80` (accepts a diff-file path for `--diff`) and :200-206 (`output_input_overlap`).

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Every item has Context, Action, Output, Verification, Completion gate | FAIL | All items carry the five labels. But 8.11 edits `tests/sweep/conftest.py` with no Output line and no verification for that edit (line 1341-1343). |
| 2 | No item leans on an earlier item without restating context | FAIL | 15 gate items point to Phase 2 procedures ("as in item 2.17", "Apply the item 2.21/2.25 procedure"); many say "Same inputs and gate folder as N". See I2, M1. |
| 3 | Agent-spawning items carry fully embedded prompts; POST runner verbatim | FAIL (partial) | POST runner prompt is verbatim (diff IDENTICAL after placeholder fill; `--diff` path fill is documented in OQ-12 and accepted by reflect SKILL.md:80). But every QA spawn says "with the report-only / fix agent / verifier preamble" without the text. See I3. |
| 4 | File paths specific | FAIL | Shell commands embed `${TASK_DIR}`, which is a notation, not a set shell variable (I1). 10.1 writes `tests/sweep/fixtures/synthetic-*` with no names (I8). 13.9 "the developer guide" (M7). |
| 5 | Verification measurable, commands named | FAIL | 9.1 claims five `[sweep publish]` messages, lists three, DESIGN has six (I5). 11.1 and 11.3 dual-surface check cannot tell the two surfaces apart (I7). Several unmeasurable or incomplete commands (M2 to M6). |
| 6 | One item per file, no batch items | FAIL | 10.1 extends conftest.py and creates an open set of fixture files plus SOURCES.md rows in one item (I8). 12.3 is five edits but one file (note only). |
| 7 | No item rests on [CODE-CONTRADICTED] or [UNVERIFIED] findings | PASS | UNVERIFIED items are fenced: 1.0a facts (OQ-13) keep DESIGN behaviour until closed (8.3, 8.10); `pipx run --spec <path>` (UNVERIFIED) runs only after the owner picks it and HALTs on failure (14.6-14.8); OQ-9 keeps the DESIGN form. |
| 8 | No commit, push, merge, `.claude/` staging, or Orca/ccsession/Claude launch in a test | PASS | Only staging is `git add .dev/tasks` (14.45, allowed). 14.1 only unstages. Live Orca read in 9.3 is a task step, not a test, and limited to the allowlisted `worker-list` template. Tests use seam fakes and a subprocess guard (8.8); the one real subprocess test runs `git` in `tmp_path` (8.9). |

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| I1 | IMPORTANT | Items 8.1 (line 1271), 14.4 (2084), 14.5 (2091), 14.8 (2110), 14.9 (2117), 14.10 (2123), 14.43 (2355) | Bash commands use `${TASK_DIR}` as if it were a shell variable. Execution Context line 169 defines it only as a notation; nothing exports it, and Bash shell state does not persist. Run as written, 14.43 does `cat artifacts/base-commit.txt` (fails, BASE empty) and `mkdir -p reflect/post` at the repository root; 14.8 writes `$WT/artifacts/sweep-help-pipx.txt`, the project-root `artifacts/` folder that CLAUDE.md says is never staged, while its Verification reads the task-package path. | Write the literal path `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/` in every shell command, or start each command with `TASK_DIR=.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/;`. |
| I2 | IMPORTANT | Items 8.21, 8.25, 8.29; 9.12, 9.16, 9.20; 10.16, 10.20, 10.24; 13.17, 13.21, 13.25; 14.20, 14.24, 14.28; 14.33, 14.37, 14.41 | Consolidation and decision items say "Merge ... as in item 2.17" and "Apply the item 2.21 / 2.25 procedure". The dedup rule (same `file:line` and defect), keep-highest-severity rule, ordering, and how `F_1` is computed live only in items 2.17, 2.21 and 2.25 (lines 354-412), six to twelve phases back. The decision items restate the halt strings but not the procedure. | Move the consolidation and decision procedures into the Execution Context "QA Gate Protocol" block and cite that block by name, or restate the rules in each item. |
| I3 | IMPORTANT | Every QA spawn item in Phases 8, 9, 10, 13, 14 (for example 8.14 line 1362, 8.22 line 1418, 8.23 line 1425) | The items say "with the report-only preamble", "with the fix agent preamble", "with the verifier preamble" but do not include the text. The prompt the agent receives is assembled from lines 188-190 of the header. B2 check 3 needs the full prompt in the item. The lens prompts are embedded; the preambles, which carry `fix_authorization`, the severity scale and the `Verdict:` / `Blocking count:` format the Verification greps for, are not. | Embed the preamble text in each spawn item, or reduce the risk by stating in each item "prepend the exact text of Execution Context lines 188/189/190" and have Verification check the report shows the preamble's required lines. |
| I4 | IMPORTANT | Item 8.11 (lines 1339-1344) | Action edits `tests/sweep/conftest.py` (removes `raising=False` from `patch_orca`), but Output lists only the pytest log and nothing verifies the edit. | Add `tests/sweep/conftest.py` to Output and a check such as `grep -n 'raising=False' tests/sweep/conftest.py` prints nothing. |
| I5 | IMPORTANT | Item 9.1 Verification (line 1480) | "each of the five `[sweep publish]` messages of section 3.2 appears byte-exact" but Context quotes only three, and DESIGN lines 106-128 hold six (`output dir escaped`, `report name space exhausted`, `<error>`, `temp file exists`, `cannot link report`, `could not remove temp file`). The count is wrong and the check is not runnable from the item. | List all six message templates in the item and grep each. |
| I6 | IMPORTANT | Item 9.3 Action (line 1492) | The live Orca read on the person's real Run is "Run the `worker-list` template ... exactly as `ALLOWED_ORCA` in probes.py holds it". The item gives neither the binary (`$ORCA_CLI_COMMAND` or `orca-ide`) nor the argv, so the executor composes a live command from code. | Write the literal command with the Run-id placeholder, copied from DESIGN 7.3 / the 1.0a facts, and add a check that the executed argv equals the `ALLOWED_ORCA` entry. |
| I7 | IMPORTANT | Items 11.1 Verification (line 1800) and 11.3 Action (line 1812) | The dual-surface check greps for `~/.claude/skills/sc-sweep-protocol/SKILL.md` and then `.claude/skills/sc-sweep-protocol/SKILL.md`. The second string is a substring of the first, so both pass when only the installed path is present. The durable test in 11.3 has the same flaw. That leaves the CLAUDE.md dual-surface rule unpinned. | Match the project copy separately, for example a regex that requires `.claude/skills/...` not preceded by `~/`, in both the grep and the test. |
| I8 | IMPORTANT | Item 10.1 (lines 1622-1627) | One item extends `conftest.py`, creates "any hand-made fixture files" under `tests/sweep/fixtures/synthetic-*` and adds `SOURCES.md` rows. The fixture file names and count are not given, so Output is a glob and the item batches an open set of files. | Name each synthetic fixture the DESIGN 11/12 cases need (or split one item per fixture file), and list them in Output. |
| I9 | IMPORTANT | Item 8.1 Context and Action (lines 1270-1271) | The gate grep `grep -L 'status: RESOLVED' .../OQ-*-decision.md` passes when a decision file is missing, because `grep -L` only lists files that exist. "OQ-1 ... to the OQ-8 record" does not name the eight files, so the pre-flight that blocks all code can pass vacuously. | List the eight decision file paths and check that each exists and holds `status: RESOLVED`. |
| M1 | MINOR | 8.15-8.20, 8.23, 8.24, 8.27, 8.28 and the same pattern in Phases 9, 10, 13, 14 | "Same inputs and gate folder as N" / "the item N inputs" points to an adjacent sibling in the same phase. Low risk, still a B2 lean. | Optional: restate the input list once per item. |
| M2 | MINOR | 8.12 Verification (line 1350) | Greps import lines for `datetime.now`, which never sits on an import line. The `stop|retry|...` grep is judged "not user-facing text", a judgment. | Grep the whole file for `datetime.now(`; give a fixed allowlist of the hits. |
| M3 | MINOR | 8.9 Verification (line 1329) | "the saved output shows no test reaching a real subprocess except the marked one" cannot be read from `pytest -v` output. | Drop it (the guard already fails such tests) or make it measurable. |
| M4 | MINOR | 8.4 (line 1294), 8.10 (line 1336) | "every note string ... (`grep -F`)" and "`grep -c` finds each DESIGN 7.1 probes name" with no list of strings or names. | List them. |
| M5 | MINOR | 9.1 Verification (line 1480) | `grep -c 'sys.exit'` gives a count, not "only inside `run`". | Use `grep -n` and compare line numbers with the `run` body. |
| M6 | MINOR | 11.2 (line 1807), 12.3 (line 1855), 13.1 (line 1882), 13.6 (line 1917) | Commands with `...` in place of the path, or `grep -c 'WC-14' ` with no file ("on the new line"). | Write full commands. |
| M7 | MINOR | 13.9 Context (line 1935), 14.19 (line 2186) | "the developer guide" without its path (`docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`, given only in 12.4). | Name the path. |
| M8 | MINOR | Agent-failure lines in every QA spawn item (for example 8.14 line 1364) | "log the blocker ... and stop" skips the HALT rule of line 192 (status Blocked, `blocker_reason`). | Say "apply the HALT rule". |
| M9 | MINOR | 8.10 (lines 1332-1337) | About 30 names added in one item; past atomicity size, no own unit test until Phase 10. | Optional split. |
| M10 | MINOR | 14.12 Action (line 2138) | A report-only agent is told to re-run `make verify-sync` and pytest; pytest writes caches, which conflicts with the preamble "must not edit any file except your own report". | Say cache writes are allowed or have the executor re-run them. |

## Summary

- Checks passed: 2 / 8 (checks 7 and 8)
- Checks failed: 6 / 8 (checks 1 to 6)
- Critical issues: 0
- Important (blocking) issues: 9 (I1 to I9)
- Minor notes: 10 (M1 to M10)
- Issues fixed in-place: 0 (fix_authorization: false)

## Actions Taken

None. Report only.

## Recommendations

- Fix I1 first: it sends the POST diff file and the pipx output to the wrong folders.
- Fix I2 and I3 together by moving the consolidation and decision procedures into the QA Gate Protocol block and having each item cite that block, or by embedding the text.
- Fix I5, I6 and I7: each is a check that cannot prove what it claims.

## Confidence Gate

- **Confidence:** Verified: 8/8 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 14 | Grep: 4 | Glob: 0 | Bash: 2
- No UNCHECKED items. No UNVERIFIABLE items.

## QA Complete

VERDICT: FAIL
