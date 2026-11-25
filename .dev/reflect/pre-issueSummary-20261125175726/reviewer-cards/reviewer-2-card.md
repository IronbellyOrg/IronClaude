<!-- Reviewer 2: reflect-reviewer, model class opus (alias claude-gw-tier1a), persona qa. Persisted verbatim by the orchestrator from the agent's return (HTML entities decoded). -->
# Reflect Reviewer — Deviation Findings
**Reviewer persona**: qa (coverage and acceptance-criteria lens); **Total deviations**: 13

Path key: PLAN = `/home/coder/workspaces/worktrees/IronClaude/issue-765/.dev/tasks/to-do/TASK-WF-issueSummary-20261125-175231/TASK-WF-issueSummary-20261125-175231.md`, SPEC = `/home/coder/workspaces/worktrees/IronClaude/issue-765/.dev/tasks/to-do/TASK-WF-issueSummary-20261125-175231/source.md`. Every other path is under `/home/coder/workspaces/worktrees/IronClaude/issue-765/`. I re-read every line number cited below.

## Deviations

| # | Category | Location | What diverged | Evidence (file:line) | Severity |
|---|---|---|---|---|---|
| 1 | Drift | PLAN:76-77, PLAN:89 | **Blocking (Missing):** The spec requires "the required broader regression/lint/format gates" (requirement INF-041). No task runs them. The plan runs only the three named test files, Ruff on the two changed test files, and `make verify-sync`. It never runs `make test` (which is `uv run pytest`) or `make lint`. **Affected action:** the final check in Tasks 4 and 5. **Consequence:** 16 test files mention ccsession and only 3 are run. One of the others, `tests/core/test_orca_session_launch_guidance.py`, pins the README's "### Orca session launches" text, requires the paragraph after line 418 to start with "Every Orca worktree gets an agent", and requires that paragraph to match `core/CLAUDE.md` exactly. Task 5 adds a sentence to that same Orca section (PLAN:85). If the sentence lands there, every plan check still passes while the full suite fails. The card's F1 is correct. | SPEC:32; `/home/coder/workspaces/worktrees/IronClaude/issue-765/.dev/issues/765/analysis/analyze-ccsession.md:25` ("then the required broader pytest/Ruff checks"); `/home/coder/workspaces/worktrees/IronClaude/issue-765/Makefile:13-15`, `:48-50`; `/home/coder/workspaces/worktrees/IronClaude/issue-765/tests/core/test_orca_session_launch_guidance.py:8-9`, `:15-16`, `:40-62`; `/home/coder/workspaces/worktrees/IronClaude/issue-765/src/superclaude/skills/ccsession-tag/README.md:409-426` | HIGH |
| 2 | Drift | PLAN:98, PLAN:22 | **Blocking (Missing):** Task 6 checks a live process "started through ccsession after the change", but no step puts the changed launcher where live launches find it. The installer links `~/.local/bin/ccsession` (and `ccsession-orca`) to the installed copy at `~/.claude/skills/ccsession-tag/`. `ccsession-orca` runs the `ccsession` that sits next to its own resolved path. `make sync-dev` writes only the repo's own `.claude/` folder. Constraint PLAN:22 also says "`wire_ccsession` copies the launcher unchanged". It does not copy anything; it only creates links. **Affected action:** Task 6's live environment check and its criterion PLAN:101. **Consequence:** an Orca-launched coordinator still runs the old installed launcher, so the switch line cannot appear. The executor would then either fail the check or run a global install from an unmerged branch, which changes every ccsession launch on the host. The plan must decide this. The card's F2 is correct. | `/home/coder/workspaces/worktrees/IronClaude/issue-765/src/superclaude/cli/install_ccsession.py:13-16`, `:61-71`; `/home/coder/workspaces/worktrees/IronClaude/issue-765/src/superclaude/skills/ccsession-tag/ccsession-orca:46-54`; `/home/coder/workspaces/worktrees/IronClaude/issue-765/Makefile:109-111`; PLAN:85 | HIGH |
| 3 | Drift | PLAN:98, PLAN:101 | **Blocking (Decision):** The environment check in Task 6 can be met by any Claude process started through ccsession "in an existing terminal". The spec requires the coordinator's own process to be checked: "the new coordinator process starts with the switch set" and "Live coordinator Claude PID ... `/proc/<pid>/environ`". The linked analysis says to inspect the switch "in its actual PID's initial environment and require `=1`". PLAN:102 gives the message check a "not run, partial" fallback, but there is no such fallback for the coordinator's environment. **Affected action:** criterion PLAN:101. **Consequence:** two terminal launches, even run straight from `src/`, pass the check while the real coordinator (for example one whose Orca command is plain `claude`) lacks the switch. That contradicts the plan's own Goal at PLAN:15. | SPEC:7, SPEC:31; `/home/coder/workspaces/worktrees/IronClaude/issue-765/.dev/issues/765/analysis/analyze-ccsession.md:25`; PLAN:15 | HIGH |
| 4 | Drift | PLAN:46, PLAN:51 | **Medium:** Task 2 adds a header line "near lines 143-154 ... so `ccsession --help` readers see it". `show_help` prints the header from line 2 and stops at the line `# The wrapper always runs`, which is line 143. Anything placed in 143-154 never appears in `--help`, so the stated reason is false. The only related check (`--help` exits 0) cannot detect this. Nothing the spec requires depends on this line. The card's F3 is correct. | `/home/coder/workspaces/worktrees/IronClaude/issue-765/src/superclaude/skills/ccsession-tag/ccsession:143`, `:2270-2271` | MEDIUM |
| 5 | Drift | PLAN:60, PLAN:66, PLAN:26 | **Medium:** Task 3 says to build the wrapper test on `_orca_env`, with "the fake Claude record extended by the one variable". That fake already records `env_names: sorted(os.environ)` plus the values of `base_url`, `topic` and `origin`. Criterion PLAN:66 ("only the one named variable is captured") is therefore false for the test the plan prescribes. The executor must either break that criterion or write a separate fake. No secret values are captured (names only), so this is not a safety issue. | `/home/coder/workspaces/worktrees/IronClaude/issue-765/tests/unit/test_ccsession_tag.py:1833-1839`; SPEC:25 | MEDIUM |
| 6 | Drift | PLAN:85, PLAN:33 | **Medium:** The documented "session-wide effect" stops at "every background command in that Claude process". The switch is exported, so any process started from inside a protected session inherits it, including a nested `claude -p`, a pipeline Claude child, or a nested ccsession. ccsession's own comment notes that "a claude started inside it inherits this variable". The README and the scope record therefore understate the effect. Their statement that "bare `claude`" is not covered is also wrong for a bare `claude` started from inside a protected session. Whether Claude Code removes the variable from its children was not checked. | `/home/coder/workspaces/worktrees/IronClaude/issue-765/src/superclaude/skills/ccsession-tag/ccsession:2406-2408`, `:2412-2415`; SPEC:11 | MEDIUM |
| 7 | Drift | PLAN:89 | **Note:** "`git status --short` shows no path under `.claude/`" cannot fail. `.gitignore` ignores `.claude/*` except `settings.json`, so mirror files never show up. The real guard is `make verify-sync` in the same criterion. The card's F5 is correct. | `/home/coder/workspaces/worktrees/IronClaude/issue-765/.gitignore:127-128` | LOW |
| 8 | Drift | coverage matrix (brief), SPEC:25 | **Note:** One requirement in the spec has no row in the matrix: "fake-Claude harnesses ... can capture only the named non-secret switch". INF-030 covers isolation from the developer's environment (SPEC:26), and INF-037 covers the live `/proc` check (SPEC:31); neither is this. The plan does own it (PLAN:26, PLAN:66), but see row 5. | SPEC:25; PLAN:26, PLAN:66 | LOW |
| 9 | Drift | coverage matrix (brief) | **Note:** Several matrix rows marked "covered" name the wrong owning task. INF-002, INF-004 and INF-026 point to Task 5; the live proof is Task 6. INF-006 points to Task 1; the launcher change is Task 2. INF-003 points to Task 2; the tests are Tasks 3 and 4. INF-033 points to Task 6; the rule is Constraint PLAN:22. In every case a real owner exists. | PLAN:22, PLAN:46, PLAN:60, PLAN:72, PLAN:98 | LOW |
| 10 | Drift | card excerpt (brief, Coverage paragraph) | **Note:** The card's arithmetic is wrong. Its own list has 15 rows covered in meaning plus 6 effort-estimate rows (INF-001, INF-018 to INF-022), which is 21 that are not gaps, plus 1 real gap (INF-041). That makes 22. The card says "19 ... Three are real gaps", but it admits F2 and F3 are not source rows. | SPEC:6, SPEC:15, SPEC:32 | LOW |
| 11 | Drift | PLAN:33 | **Note:** The route trace names only `ccsession-orca` lines 261 and 263. It leaves out the tab-reopen execs at lines 186 and 189, which Orca uses when it relaunches a coordinator's tab after a restart. Both still go through ccsession, so protection holds. Neither the scope record nor any test names them. | `/home/coder/workspaces/worktrees/IronClaude/issue-765/src/superclaude/skills/ccsession-tag/ccsession-orca:164-190` | LOW |
| 12 | Drift | PLAN:60, PLAN:63 | **Note:** Task 3 says "Add one test", while PLAN:63 expects "two wrapper cases", so the counts disagree. Also, with no terminal and no arguments, `ccsession-orca` gives the session an automatic name and takes the named exec at line 261. The untagged exec at line 263 runs only with `-p`, a resume flag, or `CCSESSION_AUTOSTART=0`. The plan names none of these and no check asserts which exec ran, so a test meant for line 263 can quietly exercise line 261. Protection is unaffected because it lives in ccsession. | `/home/coder/workspaces/worktrees/IronClaude/issue-765/src/superclaude/skills/ccsession-tag/ccsession-orca:227-236`, `:259-263`; `/home/coder/workspaces/worktrees/IronClaude/issue-765/tests/unit/test_ccsession_tag.py:1844-1860` | LOW |
| 13 | Drift | PLAN:60 | **Note:** The spec asks to cover "untagged/raw-resume". The untagged test cases use only `-p x`; no case uses a raw `--resume <id>`. Both forms run the same exec lines (2448 and 2450), so line coverage is unchanged. | SPEC:21; `/home/coder/workspaces/worktrees/IronClaude/issue-765/tests/unit/test_ccsession_tag.py:1465-1472`; `/home/coder/workspaces/worktrees/IronClaude/issue-765/src/superclaude/skills/ccsession-tag/ccsession:2447-2451` | LOW |

## Adherence summary
- Spec units audited: 42 (the 41 matrix rows plus the missing SPEC:25 requirement). The 7 effort-estimate rows (INF-001, INF-017 to INF-022) describe the issue and place no requirement on the plan. I counted them as adherent.
- Fully adherent: 37.
- Not adherent: 5.
  - Blocking: 3 units. INF-041 (row 1); INF-002 and INF-004 (rows 2 and 3, the live proof of the coordinator's switch).
  - Medium: 2 units. INF-008 (row 6) and SPEC:25 (row 5).
- By category: Authorized expansion 0 | Necessary deviation 0 | Drift 13 rows (3 Blocking, 3 Medium, 7 Note) | Regression 0.

## Notes
Verdict: FAIL (rows 1, 2 and 3 are Blocking).

Self-confidence: 0.85.

**Confirmed correct.** These plan references match the live files:
- The six `exec "$CLAUDE_BIN"` lines (2448, 2450, 2509, 2511, 2516, 2518).
- The user env file being sourced at lines 1082-1086, after the add-on profiles.
- `CCSESSION_ORIGIN` at lines 2428-2438, and the insertion point between lines 2438 and 2440.
- `ccsession-orca` lines 261 and 263.
- `ic` lines 128 and 130.
- The `WORKER-CONTRACT.md` wait command, which matches line 102 exactly.
- The README anchors (lines 392, 409, 592-613).
- The test-helper line ranges (lines 63-85, 1333-1373, 1465-1472 and 1820/1977 in the tag tests; lines 368-386, 389-453, 430-436 and 592 in the tier tests).
- `_LAUNCH_CASES` reaches all six exec lines (the profile `claude` sets a model).
- No existing test name contains "reap", so `-k reap` will select only the new tests.
- The switch is absent from the repo outside `.dev/`.
- The test commands are valid as written.

**Requirements owned and checkable.** INF-010, 011, 014, 015, 025, 032, 035, 036 and 040 are owned by Constraints PLAN:19-27. Tasks 2-4 own the switch-forcing tests and they can fail: PLAN:64 asks for a check that the new tests fail when the export is removed. One exception: if the switch is moved before the env file is sourced, only the env-file test case catches it.

**Read in full:**
- the brief;
- the plan;
- the relevant parts of `ccsession` (lines 1-170, 1040-1139, 2268-2297, 2340-2520);
- all of `ccsession-orca`;
- `install_ccsession.py`;
- the tag and tier test helpers;
- README lines 385-434;
- the relevant Makefile targets;
- `tests/core/test_orca_session_launch_guidance.py`;
- `.dev/issues/765/analysis/analyze-ccsession.md`;
- `ic` lines 120-131;
- `WORKER-CONTRACT.md` lines 98-105.

**Not checked:**
- whether any file under `.claude/` other than `settings.json` is tracked by git (I had no git access);
- whether Claude Code removes the switch from the environment of its child processes (row 6);
- the real Claude Code runtime switch itself;
- the other 13 test files that mention ccsession, beyond the guidance test cited in row 1.

reviewer_model_self_report: claude-gw-tier1a[1m]
