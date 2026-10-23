# QA Report (Cycle 3): Spec Conformance + Factual Accuracy

**Spec:** `.dev/specs/pr-submit-default-monitor-3.md`
**Date:** 2026-10-23
**Lens:** spec conformance + factual accuracy
**Fix authorization:** false (report-only)

## Verdict

**FAIL.** 3 findings (2 IMPORTANT, 1 MINOR). None falls under section 4 (out of scope).

- F1, F2: removing the Revision-1 `--yes` rows also deleted the blank line after the Options table in `pr-submit.md` and the Required Input table in `SKILL.md`. The paragraph after each table is now rendered as a table row (the `**STOP**` rule in SKILL.md included). Unspecified hunks; the `--yes` revert is not clean.
- F3: `HOW-WE-WORK.md:205` (both copies) says level 3 fixes "any failing CI checks"; the code fixes CI failures only in some cases.

Everything else in the effective spec (C1''-C30) is present and accurate. Tests and ruff pass.

## Per-item table

Effective spec = section 2.6 over 2.5 over the section 2 tables. Evidence comes from `git diff origin/master` (read-only) and the working files.

| Item (latest revision) | Status | Evidence |
|---|---|---|
| C1'' `CLAUDE.md` mandatory paragraph + ` ```text ` block, fallback `gh pr create --repo IronbellyOrg/IronClaude` labelled | PASS | Diff hunk `@@ -43,7 +43,13 @@`: says `gh repo view` target, Medium or higher fixed (lower only reported), failing CI checks, "pushes the fixes without asking", replies to and resolves the comments it fixed, "slash command, not a shell command"; ` ```text ` block; fallback stays in ` ```bash `. NEVER list, checks 2-3, exceptions and rationale unchanged. No `--yes` / "asks once". |
| C22 pre-PR check 1 `gh repo view` / `gh repo set-default` | PASS | `CLAUDE.md:60`. |
| C2 `HOW-WE-WORK.md:204` `--monitor 3` | PASS | Diff line 204; rest of line unchanged. |
| C3'' 3.11 step 6 text + `--monitor 2` sentence | PASS with F3 | `HOW-WE-WORK.md:205` has all required facts and the exact `--monitor 2` sentence; the extra word "any" is F3. |
| C4''/C4 section 5 `/sc:pr-submit` row | PASS | `HOW-WE-WORK.md:254`: default 3, Medium or higher, failing CI, pushes without asking, replies/resolves the comments it fixed; "What to do" = C4 text. 4 pipes, same as neighbours 252-255. |
| C5 routing row `6: --monitor 3` | PASS | `HOW-WE-WORK.md:323`; 9 pipes, same as rows 322 and 324. |
| C23' section 4 push rule exception | PASS | `HOW-WE-WORK.md:229`. |
| C6' plugin copy byte-identical | PASS | `cmp` exit 0. |
| C7 + C30 test rename | PASS | `tests/core/test_how_we_work_routing_table.py:333-344`: comment says "required flag", `_MANDATORY_FLAGS`, `test_named_mandatory_flags_are_on_their_steps`, `"--monitor 3"`. |
| C8''/C9'' release guides | PASS | `prd-skill-release-guide.md:535,538` and `tdd-skill-release-guide.md:557,560`: `--monitor 3`, and the C8'' sentence word for word. |
| C10 `commands.md:363` | PASS | "With no `--monitor` it runs level 3." added after the first sentence. |
| C11 `DEFAULT_MONITOR = 3` | PASS | `fsm.py:30`; read at `:53`, `:76` (argparse default), `:758`; nothing else changed. |
| C12 `test_skill_parse.py` | PASS | Lines 4, 57, 58, 60 updated as specified. |
| C13 `pr-submit.md:19` | PASS | Clause removed. |
| C14 `pr-submit.md:47` default `3` | PASS | But see F1 (blank line after the table removed). |
| C15 `SKILL.md:135` "defaults to 3" | PASS | But see F2 (blank line after the table removed). |
| C16 then C28 `state-machine.md` §5.3 | PASS | Lines 156-159: no interactive confirmation, Wave 6 has no confirm step, `--yes` has no effect, `push_decision` + `--monitor 3` (typed or default) is the authorization, `--monitor 2` stops before any push. |
| C17/C18 next command `--monitor 3{pr_arg}` | PASS | `diagnosis.py:380`, `commands.py:200`. |
| C19/C20 tests | PASS | `test_contract_setup_diagnosis.py:11,290,311`; `test_detection_contract.py:98,99,106`. |
| C24'/C25' `--yes` removed; net change none | FAIL (F1, F2) | No `--yes` row or argument-hint text remains (`git diff origin/master` with `grep -E '^[+-]' \| grep -- --yes` shows only the `state-machine.md` and `CHANGELOG.md` lines). But removing the row also removed the blank line after each table, so both files still differ from origin/master at that spot and the tables are broken. |
| C26 three reflect files "next command to run" | PASS | `src/superclaude/commands/reflect.md:82`, `plugins/superclaude/commands/reflect.md:73`, `sc-reflect-protocol/SKILL.md:67`. |
| C27' `contributing-code.md` | PASS | `git push` in ` ```bash `; "Then, in Claude Code:" plus ` ```text ` block with `/sc:pr-submit --monitor 3 ...`; workflow 3.11 link and fallback present. Fences balanced (28). |
| C29 PR template | PASS | `.github/PULL_REQUEST_TEMPLATE.md:21,23` match the spec text exactly. |
| C30 "required flags" | PASS | `CLAUDE.md:330`, `docs/user-guide/how-we-work.md:3`, both `help.md:91`; help copies `cmp` exit 0. The historical CHANGELOG line 24 is left as written (allowed). |
| C21'' CHANGELOG | PASS | New `[Unreleased]` subsection: default 3, accurate L3 behaviour, `--monitor 2` / `--monitor 0`, file list including `contributing-code.md`, `commands.md` "now states the level-3 default", `gh repo view` check, push-rule exception, C28, C29, C30 bullets, contract-status bullet. No `--yes` documentation or "asks once". The `2165ae25` reference is real (`git show`: 2026-10-22, "Default monitor changed from 2 to 3", only `pr-submit.md`). |
| Superseded wording absent from added lines | PASS | `git diff origin/master \| grep '^+'` for "asks once", "asks you once", "unless you add `--yes`", "on its own", "each review comment", "origin's `owner/repo`", "next safe command", "safe flag": only hit is the C30 rename bullet in `CHANGELOG.md`, which is not one of the C30 files. |
| No extra hunks / AC8 file list | FAIL (F1, F2) | All 25 changed files are named by the spec; no `.claude/` path. The two blank-line deletions are unspecified hunks. |
| `git diff origin/master --check` | PASS | Exit 0, no output. |
| Code fences | PASS | Even fence-line count in every changed `.md` file. |
| Table cell counts | FAIL (F1, F2) | HOW-WE-WORK rows are consistent; `pr-submit.md` and `SKILL.md` tables now swallow the next paragraph as a row. |
| AC2 `--monitor 1` grep | PASS | Hits: `CHANGELOG.md:12` (allowed C21 entry), `docs/user-guide/commands.md:363` (allowed), `pr-submit.md:37` (allowed level-1 example), `tests/pr_submit/test_monitor_arm.py:3,27` (allowed). |
| AC3 default-2 grep | PASS | Hits: `reflect-cli-tools-guide.md:65` (`--max-fix-iterations`), `SKILL.md:137` (`--max-rounds`), `refs/loop-guard.md:18` (max rounds). None about `--monitor`. |
| AC4 / help copies `cmp` | PASS | Both `cmp` exit 0. |
| AC6 tests | PASS | `uv run pytest tests/pr_submit tests/core tests/cli/reflect tests/skills -q -p no:cacheprovider` → `1315 passed, 1 xpassed, 5 warnings in 34.03s`. |
| AC7 ruff | PASS | `uvx ruff check` on the 3 changed source files + 4 changed test files → `All checks passed!`. |
| AC9 Medium or higher fixed / Low-Nit report-only | PASS | `severity_router.py:56-58,202-215` (Medium → `--fix`, High/Critical → deep fix, Low/Nit → `report-only`); SKILL.md Wave 2 (line 190), Wave 3 unverified → REPORT_ONLY (line 191). |
| AC9 L3 fixes and pushes failing CI checks | PASS with F3 | SKILL.md Wave 8 (line 197) runs Waves 3-5 on CI log findings and describes "an L3 CI push"; limits in `ci.py:60-66` make "any" (F3) wrong. |
| AC9 pushes with no confirmation step | PASS | Wave 6 (SKILL.md:194) has no confirm; its loaded refs (`thread-reply.md`, `review-retrigger.md`), plus Wave 6b/7/8 refs, have no confirm prompt (grep for `confirm\|--yes\|y/n`: only thread-identity "confirm" lines). The only "y/n" prompt is the L1 propose in Wave 4. |
| AC9 `--yes` parsed but unused | PASS | `fsm.py:64,97,130` only; no other reader in `src/superclaude/pr_submit/`. |
| AC9 `--monitor 2` fixes locally and stops before pushing | PASS | `pr-submit.md:38`; SKILL.md Wave 5 (line 193); `fsm.py:144-146` (G-edit >= 2), `:188` (G-push needs >= 3), `:1037-1039` and `:899-900` (`S4_HALT_BEFORE_PUSH` when ordinal < 3). |
| AC9 replies/resolves only fixed threads | PASS | `refs/thread-reply.md:3` ("for a remediated finding"), `:18-20` (zero-edit cycle never says resolved). |
| AC9 target from `gh repo view`, which prefers `upstream` | PASS | SKILL.md Wave 0 (line 188); gh source `context/remote.go` `remoteNameSortScore`: upstream 3, github 2, origin 1 (fetched via tavily_extract). |

## Findings

| # | Severity | Location | What is wrong | What it should be |
|---|---|---|---|---|
| F1 | IMPORTANT | `src/superclaude/commands/pr-submit.md:56-57` | The diff deletes the blank line that separated the Options table from the `` `status` enum: ... `` paragraph (diff hunk `@@ -54,7 +54,6 @@`, a bare `-` blank line). This is residue from removing the Revision-1 `--yes` row: the row is gone but the blank line went with it. The paragraph is now parsed as an extra table row: rendering with markdown-it-py (`commonmark` + `table`) puts `<td><code>status</code> enum` inside the table. Not required by any spec item; breaks the table, and the file is not byte-identical to origin/master around the removed `--yes` row. | Restore the blank line between line 56 (`\| --resume <jsonl> \| ... \|`) and the `` `status` enum `` line, exactly as on origin/master (origin lines 56-58). |
| F2 | IMPORTANT | `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:141-142` | Same defect: the diff deletes the blank line between the Required Input table's last row (`\| --resume <abs-run-log-path> \| ... \|`) and the `**STOP** if --monitor >= 1 ...` paragraph (hunk `@@ -132,14 +132,13 @@`). The STOP paragraph is now rendered as a table row (`<td><strong>STOP</strong> if` present in markdown-it-py output). That hides a HALT rule inside a table cell, and is a change beyond the spec. | Restore the blank line after the `--resume` row, as on origin/master (origin line 142). |
| F3 | MINOR | `src/superclaude/core/HOW-WE-WORK.md:205` (and byte-identical `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md:205`) | Step 6 says it fixes "... and **any** failing CI checks". That overstates level 3 (AC9) and adds a word C1''/C3'' do not contain ("failing CI checks"). The code fixes CI failures only in some cases: `ci.ci_wait_autofix()` (`src/superclaude/pr_submit/ci.py:60-66`) allows it only after Augment `TERMINAL_CLEAN`/`REPORT_ONLY` (not after `HALT_MAX_ROUNDS` or a silent Augment review); SKILL.md Wave 8 (line 197) makes CI wait-only once `round_counter >= max_rounds`, routes human-gate checks (`is_human_gate`) to HALT, and sends a log with no file:line findings to `REPORT_ONLY`. | Drop "any": "... and failing CI checks ...", the same wording as `CLAUDE.md`, the section 4 rule, the section 5 row and the release guides. Re-copy to the plugin mirror. |

## Self-Audit

- Read the whole spec and applied the precedence 2.6 over 2.5 over section 2. Did not use earlier QA reports as evidence.
- Read the full `git diff origin/master` for all 25 files, line by line, against each C-item.
- Found F1/F2 by reading the bare `-` blank-line removals in the `pr-submit.md` and `SKILL.md` hunks. Confirmed them by printing origin/master lines (`git show origin/master:...`) and rendering both files with markdown-it-py (`commonmark` + `table`): `<td><code>status</code> enum` and `<td><strong>STOP</strong> if` appear inside tables. The test suite passes anyway, so it does not cover this.
- Found F3 by checking each AC9 claim against code: `ci.py:49-66`, SKILL.md Wave 8.
- Superseded-wording grep over added lines; `--yes` grep over added and removed lines; leftover-contradiction grep (`--yes`, `one-time`, `first push`, `interactive confirm`, `without changing your code`, `defaults to 2`, `safe flag`) over the pr-submit skill, command, core, docs, plugins and `CLAUDE.md`: no stale pr-submit text.
- AC2/AC3 greps run verbatim; every hit classified above.
- `cmp` of both mirrored pairs; `git diff --check`; fence-line parity; pipe counts on the changed HOW-WE-WORK rows.
- External claim (gh remote priority) checked against gh source via `tavily_extract`.
- Confidence: Verified 41/41 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%. AC5 (`make verify-sync`) is not in this cycle's task list and was not run (spec marks it BLOCKED here).
- Tool engagement: Read: 3 | Grep: 0 (grep done in Bash) | Glob: 0 | Bash: 11 | tavily_search: 1 | tavily_extract: 1 | web_search_fallback: 0 | web_fetch_fallback: 0.
