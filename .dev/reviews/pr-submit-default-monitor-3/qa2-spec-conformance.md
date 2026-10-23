# QA Report — Spec Conformance + Factual Accuracy (QA cycle 2)

**Spec:** `.dev/specs/pr-submit-default-monitor-3.md`
**Date:** 2026-10-23
**Phase:** fix-cycle (cycle 2), report-only

## Verdict

**FAIL** — 2 findings (1 IMPORTANT, 1 MINOR). Every spec item C1-C27 (revised text) is present and correct, and tests, ruff, whitespace check, cmp and the grep gates are clean. The FAIL comes from the independent accuracy check (task item 5): the added "asks once before its first push unless `--yes`" claim describes a step that nothing at the push point of the skill tells the agent to perform (F1). There is also a slash command shown inside `bash` code fences (F2).

## Per-item table

Base: `origin/master` = `b0bd8c8b8bbefbd6b9ca36fadc8ec9cba8f244d3` (matches the spec's base). Evidence = `git diff origin/master` unless stated otherwise.

| ID | Status | Evidence |
|---|---|---|
| C1 / C1' | PASS | `CLAUDE.md:46-56`: "The mandatory way to open a PR" paragraph says `gh pr create --repo <repo>` where `<repo>` is what `gh repo view` reports (pre-PR check 1 makes sure that is the fork); Medium+ fixed, lower only reported; pushes; replies to and resolves the comments it fixed; asks once unless `--yes`. Shows `/sc:pr-submit --monitor 3 --head <branch> ...`; `gh pr create --repo IronbellyOrg/IronClaude ...` kept under "Fallback only". NEVER list, checks 2-3, exceptions and rationale unchanged (only 2 hunks in the file). Nowhere does it say the PR targets origin directly. |
| C2 | PASS | `HOW-WE-WORK.md:204`: `--monitor 1` changed to `--monitor 3`; rest of the line is byte-identical in the diff. |
| C3 / C3' | PASS | `HOW-WE-WORK.md:205` matches the C3' text exactly; the Augment app / `--monitor 0` tail is unchanged. |
| C4 / C4' | PASS | `HOW-WE-WORK.md:254`: same facts as C3', with no "on its own" and no "each review comment". The "What to do" cell is exactly the C4 text. The row has 4 pipes, like the other rows in the table (awk count, lines 250-256). |
| C5 | PASS | `HOW-WE-WORK.md:323`: `4: --no-post-pr; 6: --monitor 3`; 9 pipes, matching rows 316-324. |
| C6 / C6' | PASS | `cmp src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` exit 0. |
| C7 | PASS | `tests/core/test_how_we_work_routing_table.py:338` `"/sc:pr-submit": "--monitor 3",`. |
| C8 / C8' | PASS | `prd-skill-release-guide.md:535` `--monitor 3`; `:538` has the exact C8' sentence; no "on its own". |
| C9 / C9' | PASS | `tdd-skill-release-guide.md:557` / `:560`, identical to C8'. |
| C10 | PASS | `docs/user-guide/commands.md:363`: "With no `--monitor` it runs level 3." placed after the first sentence. |
| C11 | PASS | `fsm.py:30` `DEFAULT_MONITOR = 3`; lines 53, 76 and 758 still read the constant (grep). |
| C12 | PASS | `test_skill_parse.py:4` "default L3"; `:57` `test_t103_default_monitor_three_armed`; `:58` "the default is 3"; `:60` `== 3`. |
| C13 | PASS | `pr-submit.md:19` now ends "(the hook NEVER arms a monitor itself)". |
| C14 | PASS | `pr-submit.md:47` Default column `3`; line 26 untouched. |
| C15 | PASS | `SKILL.md:135` "No (defaults to 3)". |
| C16 | PASS | `refs/state-machine.md:158-159` "the `--monitor 3` arming (typed or the default) stands as the recorded authorization." |
| C17 | PASS | `diagnosis.py:380` `/sc:pr-submit --monitor 3{pr_arg}`. |
| C18 | PASS | `cli/reflect/commands.py:200` same. |
| C19 | PASS | `test_contract_setup_diagnosis.py:11, :290, :311` changed to `--monitor 3`. |
| C20 | PASS | `test_detection_contract.py:98, :99, :106` changed to `--monitor 3`. |
| C21 / C21' | PASS | `CHANGELOG.md:7-17` new subsection under `[Unreleased]` covering: default 3; accurate L3 behaviour; `--yes` documented; corrected file list (`contributing-code.md` says to open PRs with `--monitor 3`, `commands.md` "now states the level-3 default"); `gh repo view` pre-PR check; push-rule exception; contract-status `--monitor 3`; `--monitor 0` open-only. No "without asking". (The wording inherits F1.) |
| C22 | PASS | `CLAUDE.md:60` check 1 adds the `gh repo view --json nameWithOwner -q .nameWithOwner` / `gh repo set-default IronbellyOrg/IronClaude` text and "(gh prefers an `upstream` remote over `origin`)". |
| C23 | PASS | `HOW-WE-WORK.md:229` keeps the rule and adds the exception for workflow 3.11 with the lead go-ahead clause. |
| C24 | PASS | `pr-submit.md:8` `argument-hint` ends `[--yes]`; `:57` Options row cites `refs/state-machine.md` §5.3; the table keeps 4 pipes per row. |
| C25 | PASS | `SKILL.md:142` matching `--yes` row; 4 pipes. |
| C26 | PASS | `commands/reflect.md:82`, `plugins/.../reflect.md:73`, `sc-reflect-protocol/SKILL.md:67` say "the next command to run"; `git grep 'next safe command' -- src plugins docs tests` returns no hits. |
| C27 | PASS (see F2) | `contributing-code.md:185-190`: workflow 3.11 link (relative path resolves to `src/superclaude/core/HOW-WE-WORK.md`), push only after approval, `/sc:pr-submit --monitor 3 --head ... --title ... --body ...`, fallback `gh pr create --repo IronbellyOrg/IronClaude`; "# Create PR on GitHub" removed. |
| Superseded wording | PASS | `git grep -E 'on its own\|without asking\|each review comment\|origin.s \`owner/repo\`'`: no hit in any added line. The remaining hits are pre-existing, unrelated text (for example `CHANGELOG.md:30` about RULES.md) or pre-existing pr-submit targeting text (`pr-submit.md:29,:63`, `SKILL.md:18,:144`, `refs/review-retrigger.md:28`, `tests/pr_submit/test_static_grep.py:5`) that the spec defers to §4 item 3(a). |
| Extra hunks | PASS | 21 files, 61+/41-; every hunk maps to a C-item. `git diff origin/master --check` exit 0 (no whitespace damage). Table pipe counts are consistent in every edited table. |
| AC2 | PASS | Hits: `CHANGELOG.md:12` (C21 "previously said `--monitor 1`"), `docs/user-guide/commands.md:363`, `pr-submit.md:37`, `tests/pr_submit/test_monitor_arm.py:3,:27`. All are on the allowed list. |
| AC3 | PASS | Hits: `docs/guides/reflect-cli-tools-guide.md:65` (reflect, unrelated), `SKILL.md:137` (`--max-rounds`), `refs/loop-guard.md:18` (max_rounds). None is about the `--monitor` default. |
| AC4 | PASS | cmp exit 0. |
| AC6 | PASS | `uv run pytest tests/pr_submit tests/core tests/cli/reflect tests/skills -q -p no:cacheprovider` gave `1315 passed, 1 xpassed, 5 warnings in 37.97s` (the warnings are Click `isolated_filesystem` deprecations). |
| AC7 | PASS | `uvx ruff check` on the 7 changed .py files: `All checks passed!`. |
| AC8 | PASS | `git diff --name-only origin/master` lists exactly the 21 section-2/2.5 files. Untracked files are only the spec and the `.dev/reviews/pr-submit-default-monitor-3/` reports. No `.claude/` path. |
| AC9 | PASS against the spec's §2.5 fact list; FAIL on the independent check (F1) | Medium+ fixed and Low/Nit report-only: `severity_router.py:202-222` `route()` (Critical/High deep-fix, Medium `--fix`, otherwise `ROUTE_REPORT_ONLY`), `fsm.py:417`, `SKILL.md` Wave 2 (l.192). Unverified findings are report-only: Wave 3 (l.193). Replies to and resolves fixed threads: `refs/thread-reply.md` §1 (only a cycle with a grounded applied edit may call a thread fixed) and §3-4. Target from `gh repo view`: `SKILL.md:190` Wave 0, with origin parse as fallback. "gh prefers upstream over origin" matches gh's remote ranking (upstream > github > origin). First-push confirm unless `--yes`: stated only in `refs/state-machine.md:156-159` and not reachable at the push step (F1). |

## Findings

| # | Severity | Location | What is wrong | What it should be |
|---|---|---|---|---|
| F1 | IMPORTANT | `CLAUDE.md:46`; `src/superclaude/core/HOW-WE-WORK.md:205, :229, :254` (and the plugin mirror); `docs/guides/prd-skill-release-guide.md:538`; `docs/guides/tdd-skill-release-guide.md:560`; `CHANGELOG.md:11` | Each of these says flatly that `/sc:pr-submit --monitor 3` "asks once before its first push unless you add `--yes`". HOW-WE-WORK section 4 (`:229`) even uses this as the safeguard behind its new exception to "Never push without approval". Nothing that drives the push carries that step out. (a) The only place it is defined is `refs/state-machine.md:156-159`, and `SKILL.md` never tells the agent to load that ref: refs "are LAZY-loaded per wave", and no wave loads `state-machine.md` (it appears only at `SKILL.md:27` and as a "matching §5.2a" note at `:195`). (b) Wave 6 (`SKILL.md:196`), where the push happens, says to push "ONLY when the conjunction holds" and has no confirmation step. Wave 6 loads `thread-reply.md` and `review-retrigger.md`, and neither of those mentions it. (c) `fsm.py` parses `--yes` (`:64, :97, :130`), but no code reads `args.yes` (grep of `src/superclaude/pr_submit/` finds only the assignment at `:130`). (d) §5.3 also exempts non-interactive runs, and the added sentences leave that condition out. The only sign of the confirmation the agent will actually see is the new `--yes` row (`SKILL.md:142`), which describes the flag rather than telling the agent to ask. A user who relies on "it will ask me before pushing" can get a push with no prompt. The spec's §2.5 lists this as a fact and §4 item 2 admits it is not wired in code. | Pick one. (1) Put the confirmation step into `SKILL.md` Wave 6, right before the first `git push` of a run: "unless `--yes`, ask the user once and HALT_BEFORE_PUSH if they decline". Then the claim is backed. (2) Or reword every listed claim so it does not promise a prompt, for example "the skill's state machine requires a one-time confirmation before the first push (`--yes` skips it)", and remove "asking you only once" from the section-4 exception. Either way, record the decision in the spec, because AC9 currently treats this as an established fact. |
| F2 | MINOR | `CLAUDE.md:48-50`; `docs/developer-guide/contributing-code.md:187-190` | `/sc:pr-submit --monitor 3 ...` is a Claude Code slash command but sits in a ```` ```bash ```` fence. In `contributing-code.md` the same `bash` block also holds the shell command `git push origin ...`. Pasting that block into a terminal fails on the second line. An agent reading CLAUDE.md may try to run the line with the Bash tool. The release guides (`prd-skill-release-guide.md:531`) use an unlabelled fence for slash commands, and HOW-WE-WORK uses inline code. | Use an unlabelled fence (or `text`) for the slash-command line. In `contributing-code.md`, split it: keep `git push origin feature/your-feature-name` in the `bash` block and show `/sc:pr-submit --monitor 3 ...` in its own unlabelled block, with "then, in Claude Code:" before it. |

## Self-Audit

What I checked, and how:
- Read the full spec, including §2.5, and applied the revised text (C1', C3', C4', C6', C8'/C9', C21') over the originals.
- Read the full `git diff origin/master` (all 21 files) and matched every hunk to a C-item. There are no extra hunks. `--check` is clean.
- Re-ran the AC2 and AC3 greps and the superseded-wording greps myself. I sorted every hit into "allowed", "pre-existing and deferred by spec §4 item 3(a)", or "unrelated".
- Counted pipes in every edited markdown table row against the neighbouring rows.
- Ran cmp for AC4, pytest with `tests/skills` added (1315 passed, 1 xpassed), and ruff (clean).
- AC9 facts: read `severity_router.py` `route()`, `fsm.py` (`route` and `yes` usage), `SKILL.md` Purpose, Required Input, Waves 0-8 and VAL, `refs/thread-reply.md` (all of it), and `refs/state-machine.md` §5.3. I grepped every ref and script, plus the Python core, for `--yes` and `confirm`; that search produced F1.
- Checked the gh remote-preference claim with one Tavily search (cli/cli issues #9399, #9654, #2300 and the `gh repo set-default` manual). They agree that gh resolves the base repo among several remotes and that `set-default` overrides it. The "upstream ranks above origin" ordering comes from gh's remote ranking, not from a quoted page.

Observations that are not findings (in scope or deferred):
- The pre-existing "origin's `owner/repo`" targeting text in `pr-submit.md:29,:63` and `SKILL.md:18,:144-145` now sits awkwardly beside the new CLAUDE.md line that says the target comes from `gh repo view`. The spec explicitly defers this (§4 item 3a), and no added line repeats it.
- `refs/state-machine.md` §5.3 is headed "INV-016, verbatim", and C16 edits it. The spec requires that edit. The `<!--mc:rev ...-->` section hash at the end of that file (`92ba8752` for §5.3) was not updated. It is tooling metadata with no test, so I note it and do not count it as a finding.
- Level 3 also fixes CI failures and stops at `--max-rounds` (default 2). None of the added sentences mentions either. That is an omission, not a wrong statement, and both are outside the §2.5 fact list.

Confidence: Verified 35/35 table rows | Unverifiable: 0 (AC5 `make` is out of scope for this lens) | Unchecked: 0 | Confidence: 100%.
Tool engagement: Read: 4 | Grep: 0 (searches ran through Bash `git grep`/`grep`) | Glob: 0 | Bash: 10 | tavily_search: 1 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0.

## QA Complete
