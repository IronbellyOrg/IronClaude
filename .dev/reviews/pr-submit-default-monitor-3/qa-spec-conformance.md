# QA Report — Spec Conformance: pr-submit-default-monitor-3

**Spec:** `.dev/specs/pr-submit-default-monitor-3.md`
**Date:** 2026-10-23
**Phase:** spec-conformance (report-only, fix_authorization = false)
**Fix cycle:** N/A

---

## Verdict: FAIL

All 21 changes (C1-C21) match the spec exactly, with nothing extra changed. AC2, AC3, AC4, AC6, AC7 and AC8 all pass. The verdict is FAIL because of 4 MINOR factual-accuracy findings:

- F1 and F2 are wording the implementer wrote into CHANGELOG.md and CLAUDE.md.
- F3 and F4 come from the spec's own required text, so the spec must be fixed first.

## Per-item table

Base check: every "Old" line number in the spec was confirmed on `origin/master` with `git grep -n ... origin/master -- <files>` (all 30 cited lines matched exactly: CLAUDE.md:46, HOW-WE-WORK.md:204/205/254/323, test_how_we_work_routing_table.py:338, prd guide :535/:538, tdd guide :557/:560, commands.md:363, fsm.py:30, test_skill_parse.py:4/57/58/60, pr-submit.md:19/47, SKILL.md:135, state-machine.md:158, diagnosis.py:380, reflect/commands.py:200, test_contract_setup_diagnosis.py:11/290/311, test_detection_contract.py:98/99/106). The full `git diff origin/master` has 17 files, 47+/33-, and every hunk maps to one C-item below; no extra hunk. `git diff origin/master --check` reports no whitespace errors.

| Item | Status | Evidence |
|---|---|---|
| C1 | PASS (conformance) — see F2 for wording accuracy | CLAUDE.md:46-56. "The mandatory command shape" line is gone; new line 46 makes `/sc:pr-submit --monitor 3` mandatory with one sentence on what level 3 does; code block `/sc:pr-submit --monitor 3 --head <branch> --title "..." --body "..."`; then "**Fallback only, when `/sc:pr-submit` cannot run:**" above the unchanged `gh pr create --repo IronbellyOrg/IronClaude ...` block. Diff hunk `@@ -43,7 +43,13 @@` touches only that line; NEVER list, pre-PR checks, exceptions and rationale are untouched. |
| C2 | PASS | HOW-WE-WORK.md:204 now `/sc:pr-submit --monitor 3 --head feature/invoice-csv-export ...`; rest of line byte-identical to old (diff). |
| C3 | PASS (conformance) — see F3 | HOW-WE-WORK.md:205 now "...checks each of its findings, fixes the ones it confirms, pushes those fixes to your branch, and replies to and resolves each review comment." Augment app / `--monitor 0` tail unchanged. Old "proposes fixes without changing your code" gone. |
| C4 | PASS | HOW-WE-WORK.md:254 both cells match spec text exactly; old "uses `--monitor 2`" and "Always pass `--monitor 1`." gone. Table still 3 columns. |
| C5 | PASS | HOW-WE-WORK.md:323 cell now `4: --no-post-pr; 6: --monitor 3`; column count unchanged; routing-table tests pass. |
| C6 | PASS | `cmp src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` printed nothing, exit 0 (IDENTICAL). Both files have the same blob `9aff68ac` in the diff header. |
| C7 | PASS | tests/core/test_how_we_work_routing_table.py:338 `"/sc:pr-submit": "--monitor 3",`. |
| C8 | PASS | prd-skill-release-guide.md:535 `--monitor 3`; :538 inserts "It fixes the review findings it confirms and pushes those fixes to your branch on its own." directly after "then run `/sc:pr-submit`.". |
| C9 | PASS | tdd-skill-release-guide.md:557/:560, same change as C8 byte-for-byte. |
| C10 | PASS | commands.md:363 "With no `--monitor` it runs level 3." inserted after first sentence ("...reply and resolve."). |
| C11 | PASS | fsm.py:30 `DEFAULT_MONITOR = 3`; lines 53/76/758 still read the constant (git grep). |
| C12 | PASS | test_skill_parse.py:4 "default L3"; :57 `def test_t103_default_monitor_three_armed`; :58 "the default is 3"; :60 `== DEFAULT_MONITOR == 3`. |
| C13 | PASS | pr-submit.md:19 now ends "(the hook NEVER arms a monitor itself)."; "NEVER implies level-3" gone (git grep, no hits). |
| C14 | PASS | pr-submit.md:47 `\| --monitor {0,1,2,3} \| 3 \|`; :26 untouched ("default 3"). |
| C15 | PASS | SKILL.md:135 "No (defaults to 3)". |
| C16 | PASS | state-machine.md:158-159 now "...the `push_decision` record + the / `--monitor 3` arming (typed or the default) stands as the recorded authorization."; "the explicit" gone; blockquote `>` prefixes intact. |
| C17 | PASS | diagnosis.py:380 `return f"/sc:pr-submit --monitor 3{pr_arg}"`. |
| C18 | PASS | reflect/commands.py:200 same. |
| C19 | PASS | test_contract_setup_diagnosis.py:11, :290, :311 all `--monitor 3`. |
| C20 | PASS | test_detection_contract.py:98, :99, :106 all `--monitor 3`. |
| C21 | PASS (conformance) — see F1, F2, F4 | CHANGELOG.md:7-15, new subsection under `## [Unreleased]` above the existing "routing" entry; heading style matches neighbours (`### <area> — ...` / `#### Changed (<area>)`). States: default now 3; PR instructions + routing guide use `--monitor 3`; contract-readiness next command (`superclaude reflect contract-status`) is `--monitor 3`; bare run pushes/replies/resolves without asking; `--monitor 0` to only open. Commit `2165ae25` claim verified (`git show 2165ae25` changed pr-submit.md "default 2" -> "default 3", 2026-10-22). |
| AC2 | PASS | `git grep -n -E -- '--monitor 1' -- ':!.dev'` -> 5 hits: CHANGELOG.md:12 (C21, "instead of `--monitor 1`"), docs/user-guide/commands.md:363 ("at `--monitor 1` or higher"), src/superclaude/commands/pr-submit.md:37 (level-1 example), tests/pr_submit/test_monitor_arm.py:3 and :27 (T-109 level-1 tests). All in the allowed list. |
| AC3 | PASS | 3 hits: docs/guides/reflect-cli-tools-guide.md:65 (`--max-fix-iterations` "(default 2)", unrelated feature), SKILL.md:137 (`--max-rounds`), refs/loop-guard.md:18 (`max_rounds` "Default 2"). None about the `--monitor` default. Extra repo-wide sweep for `defaults to 2`, `\| 2 \| Capability`, `default L2`, `monitor_two`: no hits outside `.dev`. |
| AC4 | PASS | Same as C6. |
| AC6 | PASS | `uv run pytest tests/pr_submit tests/core tests/cli/reflect -q -p no:cacheprovider` -> `906 passed, 1 xpassed, 5 warnings in 15.83s` (warnings are Click `isolated_filesystem` deprecation, pre-existing). |
| AC7 | PASS | `uv run ruff` fails to spawn (ruff not in the venv). Ran `uvx ruff check --no-cache` on all 7 changed `.py` files -> `All checks passed!`. |
| AC8 | PASS | `git diff --name-only origin/master` = the 17 files of spec section 2 exactly. `git status --porcelain --untracked-files=all` adds only `.dev/specs/pr-submit-default-monitor-3.md` and two files in `.dev/reviews/pr-submit-default-monitor-3/` (this report and `qa-orphan-sweep.md`, another reviewer's report in the allowed folder). No `.claude/` path. |
| Item 7 (facts in C1/C21) | FAIL | See F1, F2, F4. The `gh pr create --repo` on origin's `owner/repo` claim is TRUE (SKILL.md:189 Wave 0: `REPO="$(gh repo view --json nameWithOwner ...)"`, then `gh pr create --repo "$REPO" ...`; SKILL.md:216). |

## Findings

Every C-item matches the spec's "New" text. The four findings below are about facts: text that does not match what the code and skill really do. F1 and F2 come from the implementer's own wording. F3 and F4 copy the spec's wording exactly, so the spec has to be fixed first.

| # | Severity | Location | What is wrong | What it should be |
|---|---|---|---|---|
| F1 | MINOR | `CHANGELOG.md:12` | Says `docs/user-guide/commands.md` "now say[s] to open PRs with `/sc:pr-submit --monitor 3` instead of `--monitor 1`". Untrue for that file: on origin/master `commands.md:363` never told anyone to pass `--monitor 1` (it says "at `--monitor 1` or higher, arm..."), and after C10 it only states the default ("With no `--monitor` it runs level 3."). It does not tell the reader to pass `--monitor 3`. | Take `docs/user-guide/commands.md` out of that list and add a separate clause, e.g. "`docs/user-guide/commands.md` now says that with no `--monitor` it runs level 3." |
| F2 | MINOR | `CLAUDE.md:46` (C1 sentence); same claim at `CHANGELOG.md:11` | "fixes the findings it verifies, pushes the fixes, and replies to and resolves each review comment" overstates level 3. SKILL.md:191 sends Low/Nit findings to report-only (`severity_router.py:58` `ROUTE_REPORT_ONLY = "report-only"  # Low / Nit — not dispatched`), so some verified findings are never fixed. SKILL.md:192 sends unverified findings to REPORT_ONLY. `refs/thread-reply.md:3` says the reply and resolve steps are "for a remediated finding". So level 3 does not fix every verified finding and does not reply to or resolve every review comment. CHANGELOG:11 makes the same claim ("fixes the review findings it verifies ... replies to and resolves the review comments"). | CLAUDE.md:46: "...fixes the verified findings of Medium severity or higher, pushes the fixes, and replies to and resolves the review threads it fixed." Change CHANGELOG:11 the same way. |
| F3 | MINOR (wording comes from the spec) | `src/superclaude/core/HOW-WE-WORK.md:205` and its copy `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md:205`; also `HOW-WE-WORK.md:254`, `prd-skill-release-guide.md:538`, `tdd-skill-release-guide.md:560` | The same overstatement as F2: "fixes the ones it confirms ... replies to and resolves each review comment" (C3), and "fixes the review findings it confirms" (C4, C8, C9). These lines copy the spec's C3/C4/C8/C9 text exactly, so they pass the spec check, but the facts are wrong for the same reasons as F2 (Low/Nit and unverified findings are report-only and get no reply or resolve). | Fix spec C3/C4/C8/C9 first, e.g. "fixes the confirmed findings of Medium severity or higher, pushes those fixes, and replies to and resolves the threads it fixed". Then update these lines and run `cmp` again for the plugin copy. |
| F4 | MINOR (wording comes from the spec) | `CHANGELOG.md:11` ("...without asking") versus `src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md:156-158` | The CHANGELOG says a bare `/sc:pr-submit` pushes "without asking". The skill's own reference says "the FIRST push of a run requires `--yes` OR an interactive confirm unless the run is non-interactive". The Python code parses `--yes` (`fsm.py:97`, `fsm.py:130`) but never reads it, so the code does not ask. The agent, however, follows state-machine.md, and in an interactive session it is told to ask before the first push. The spec wants "without asking" (C21) and logs the `--yes` gap as out of scope (§4.2), but the released text now contradicts the shipped skill documentation. | Either (a) word the CHANGELOG to match state-machine.md: "...pushes fixes (after a one-time confirmation of the first push in an interactive run) and replies to and resolves...", or (b) fix the `--yes` gap from §4.2 before release so that "without asking" is true everywhere. Fix spec C21 to match whichever is chosen. |

## Self-Audit

What I checked myself, with tools, and did not take from anyone else's report:

- I read the whole spec, and the whole `git diff origin/master` hunk by hunk. I matched each hunk to exactly one C-item and found no extra hunk. The 17 changed files are exactly the files listed in spec section 2.
- I checked every spec "Old" line number against `origin/master`. All 30 lines matched. I also searched the working tree for each removed phrase; none is left outside `.dev`.
- I compared the plugin copy of HOW-WE-WORK.md with `cmp`: identical.
- I ran the exact AC2 and AC3 `git grep` commands and checked every hit against the allowed list.
- I ran the tests: 906 passed, 1 xpassed. I ran ruff through `uvx` because `uv run ruff` is not installed: clean. `git diff --check` found no whitespace errors.
- I checked the markdown tables in the changed rows (HOW-WE-WORK.md:254 and :323, pr-submit.md:47, SKILL.md:135). Each has the same number of cells as before, and the routing-table tests pass.
- I searched for copies of the pr-submit command or skill outside `src/` (`git ls-files | grep pr-submit`). Apart from `.dev` history, there are none, so no copy still says the default is 2.
- I checked the facts in the C1 and C21 text against SKILL.md:189/191/192/216, `refs/thread-reply.md:3`, `severity_router.py:56-58`, `refs/state-machine.md:156-158`, `fsm.py:97,130`, and `git show 2165ae25`.

Why the verdict is FAIL: the change matches the spec on every item. But the task also asked whether the facts in C1 and C21 are true, and they are not fully true (F1, F2, F4). F3 shows the same wrong wording sits in the spec itself. Under "any issue of any severity = FAIL", the verdict is FAIL.

- **Confidence:** Verified: 28/28 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 4 | Grep: 0 (searches run as `git grep` / `grep` through Bash) | Glob: 0 | Bash: 9. No web research.
- AC5 (`make sync-dev && make verify-sync`) was not in my task list and was not run (the spec records it as blocked because `make` is not installed).

## QA Complete
