# QA Report: Command-contract lens for `sweep.md` (T245)

**Date:** 2026-11-12
**Phase:** code gate, command-contract lens
**fix_authorization:** false (report is the only file written)
**Target:** `src/superclaude/commands/sweep.md`

**Authority used:** `docs/designs/orchestrator-mode.md` section 7.6 (lines 649-666) and section 9 row R5 (line 719) as revised; the appended addendum paragraph (line 1051 area) and `revisions/chat-output-exception-20261109-133150/design-addendum.md`; OQ-2, OQ-5 and OQ-6 records under `phase-outputs/plans/`; house patterns `graph.md` and `issue.md`; option defaults from `src/superclaude/cli/sweep/commands.py`.

**Method note:** every cited line was read from disk in this session (reads of at most 150 lines). Frontmatter literals were also compared with `grep -Fx`. Six mutations of `sweep.md` were made only in private copies under `/tmp` (deleted afterwards, `CLEANED` printed); no repository file other than this report was written.

## Findings

| id | severity | evidence | what is wrong | smallest fix |
|---|---|---|---|---|
| F1 | MINOR | `src/superclaude/commands/sweep.md:16` says `/sc:sweep` "is on the never-as-worker list in `~/.claude/WORKER-CONTRACT.md`". `src/superclaude/core/WORKER-CONTRACT.md:23` lists `/sc:agent`, `/sc:git`, `/sc:help`, `/sc:issue`, `/sc:pm`, `/sc:spawn` and `/sc:swarm-wizard` only; `grep -n sweep ~/.claude/WORKER-CONTRACT.md` hits only lines 110, 127, 151 (the master "The sweep." text). The task file lists the edit as open item 12.2 (`TASK-RF-sweep-phase1-20261108-072653.md:2117`, unchecked). | The sentence is a forward reference: today it is false on disk. DESIGN 7.6 line 657 itself prescribes it and step 1.18 (section 8) makes it true, so it is sequencing, not a wording defect. | None now. The phase-12 contract gate must confirm line 23 names `/sc:sweep` before the PR; if item 12.2 does not land, this becomes BLOCKING. |
| F2 | MINOR | `sweep.md:20` "the coordinator runs `/sc:sweep` on every wake". DESIGN WC-16 text (`orchestrator-mode.md:679`) and routing row R2 (`:716`) say "on every coordinator wake, at most once every 5 minutes"; the DESIGN section 8 paragraph (`:674`) records that R4 dropped the unbounded "It sweeps on every wake". | The Triggers sentence omits the 5-minute cap that R4 deliberately added, so a reader of the command alone could run it on every wake. DESIGN 7.6 pins only "Triggers: explicit only", which the sentence satisfies, so this is not a 7.6 bullet departure. | Reword to "the coordinator runs `/sc:sweep` on a wake, at most once every 5 minutes (WC-16), or a person types it". |
| F3 | MINOR | `sweep.md:47` "Do NOT proceed using only this command file." versus `graph.md:46` and `issue.md:103` "Do NOT proceed with protocol execution using only this command file." (`recommend.md:62` uses the short form). | Wording differs from the `graph.md` form DESIGN 7.6 names; the MANDATORY line, the `> Skill sc:sweep-protocol` invocation and the do-not-proceed prohibition are all present, so behaviour is the same. | Optional: use the `graph.md` sentence verbatim. |
| F4 | MINOR | `tests/commands/test_sweep_command.py` lines 106-168 (the DESIGN 7.6 test group) never read `name`, `argument-hint`, the `> Skill sc:sweep-protocol` line, the option defaults or the "Do NOT proceed" sentence. Experiment (check C19): five mutations of a `/tmp` copy of `sweep.md` all still gave `110 passed`. | The DESIGN 7.6 test bullet (`:666`) does not require these pins, so the test meets the design; but the contract this lens checks (argument-hint, invoked skill name, 6h default) can drift unseen. | Optional: add three pins (frontmatter `name`/`argument-hint` literals, the `> Skill sc:sweep-protocol` line inside `## Activation`, `6h` in the `--window` row). The test-coverage lens (item 11.8) owns this. |

No BLOCKING or MAJOR finding.

## Check evidence

| id | check | evidence (read from disk now) |
|---|---|---|
| C1 | Frontmatter `name: sweep` | `grep -Fxn 'name: sweep'` gives `sweep.md:2`. |
| C2 | Frontmatter `allowed-tools: Skill` exactly | `grep -Fxn 'allowed-tools: Skill'` gives `sweep.md:9`; no other tool is listed (graph.md:9 adds Bash entries, sweep correctly does not). |
| C3 | `argument-hint` byte-exact | `grep -Fxn` of the DESIGN 7.6 literal `argument-hint: "[--run <id>]... [--window <N>h\|<N>d] [--root <dir>] [--output <dir>]"` (the quotes are YAML quoting, as in graph.md:8) gives `sweep.md:8`; exactly one `argument-hint:` line; frontmatter delimiters at lines 1 and 10; no CR characters. Value text equals `orchestrator-mode.md:655`. |
| C4 | One-line description, no stop/retry/release/merge/removal words | `sweep.md:3` is a single line; `sed -n 3p ... \| grep -ciE 'stop\|retry\|release\|merge\|remov'` printed 0 (DESIGN section 9 rule at `:728` and step-1.14-checks.md agree). |
| C5 | Headings in the `issue.md` order (title, Triggers, Usage, Options) | `sweep.md` headings: 12 title, 18 Triggers, 22 Usage, 31 Options, 42 Activation, 57 Boundaries. `issue.md`: 12 title, 23 Triggers, 27 Usage, 34 Options, then STOP rules, Examples, Outputs, Boundaries 82, Activation 98. `graph.md` puts Activation (41) before Boundaries (70), as sweep does. The four DESIGN-named headings are in the issue.md order. |
| C6 | `## Activation` block in the `graph.md` form, invoking `Skill sc:sweep-protocol` | `sweep.md:42-55`: "**MANDATORY**: Before executing any protocol steps, invoke:", then `> Skill sc:sweep-protocol` (line 45), "Pass the user's flags unchanged", the do-not-proceed sentence. Same skeleton as `graph.md:41-46`. Skill frontmatter `name: sc:sweep-protocol` (`SKILL.md:2`) matches the invoked name. Wording note F3. |
| C7 | Both skill surfaces named, installed first | `sweep.md:49` `~/.claude/skills/sc-sweep-protocol/SKILL.md`; `:53` `.claude/skills/sc-sweep-protocol/SKILL.md`; `:55` "Skills read `~/.claude/skills/` first." Matches DESIGN 7.6 line 656 and the CLAUDE.md dual-surface rule. |
| C8 | Option defaults equal `commands.py` | `commands.py:27` `DEFAULT_WINDOW = "6h"` and `:228` `default=DEFAULT_WINDOW`; `:234` `--root default=None` (found by `_find_root`, walks up to `.git`, `:64-70`); `:239` `--output default=None` (base `<root>/.dev/sweeps`, `:101-102`); `:221-223` `--run` multiple, empty means `probes.bind_run` (`:264-266`). `sweep.md:35-38` states the same four defaults. |
| C9 | OQ-2 and OQ-5 records honoured | OQ-2 Chosen `<root>/.dev/sweeps/` (record line 34): `sweep.md:38` and `.gitignore:256` `.dev/sweeps/` agree. OQ-5 Chosen `6h`, activity only (record line 34): `sweep.md:36` default `6h`. OQ-6 chosen (b): `sweep.md` contains no chat-format rule, correct because the exception lives in the style and skill (addendum line 29 allocates only the skill, not the command). |
| C10 | Constraint statements in the Options table are true | Window `<N>` 1-9999, max 720h/30d: regex `[1-9][0-9]{0,3}[hd]` and `MAX_WINDOW_HOURS = 720` (`commands.py:45-49`). Run id `run_` plus 12 lowercase hex: `probes.py:44` `RUN_ID_RE = r"run_[0-9a-f]{12}"`. Duplicates read once: `commands.py:92` `dict.fromkeys`. Root must hold `.git`: `_check_root` `:73-84`. Output below `<root>/.dev/sweeps/` and not overlapping read folders: `:99-123`. No Run bound: `probes.py:358` "no Run bound: pass --run <id>" with exit 2 (`commands.py:279-281`), matching `sweep.md:35`. |
| C11 | No `## Unattended mode` heading and no `--unattended` | `grep -n -i 'unattended\|src/superclaude\|--caller\|worker mode' sweep.md` hit only line 40, "There is no worker mode and no flag for one." (no `unattended` token). Heading list has no such heading. |
| C12 | No `src/superclaude/` path in the command | Same grep: no hit. Core doc is named by installed path `~/.claude/WORKER-CONTRACT.md`. |
| C13 | Triggers explicit only and consistent with WC-16 cadence | `sweep.md:18-20` "Explicit only ... Nothing starts it automatically." satisfies DESIGN 7.6 `:657`. Cadence cap missing: see F2. |
| C14 | The never-as-worker claim is true on disk | False today (see F1); pending item 12.2. |
| C15 | Command text agrees with what the skill and CLI do | Command `:55` says the skill runs `superclaude sweep run`, reads the report, prints counts and path, adds no recommendation: `SKILL.md:15, 23-27, 59` say the same. Usage examples `:26-27` use ids that match the Run id regex (`run_0123456789ab`, `run_fedcba987654`), `2d` is valid, and `--output .../.dev/sweeps/archive` is below the base folder. |
| C16 | Intro and report claims match the code | `models.py:31-40` `CLASSES` has eight entries including every class named at `sweep.md:14` (working, waiting on a person, idle, finished, stalled (proved), could not determine). `report.py:209` has an "Unscanned" column and `report.py:491` lists sessions waiting on a person, matching "lists what waits on a person and why, and every source it could not read". |
| C17 | Boundaries match DESIGN 7.6 | `sweep.md:57-68`: runs `superclaude sweep run`, reads the report; will not change Orca, git or a worktree, add advice, or run as a worker. DESIGN lines 662-663 agree. |
| C18 | Tests and lint green | `uv run pytest tests/commands tests/recommend -q`: `628 passed`; with the two severity modules the recorded `phase11-validation.md:62` says `718 passed` (628 + 90, consistent). `uv run ruff check` and `uv run ruff format --check` on `tests/commands/test_sweep_command.py` and `tests/recommend/test_routing_refresh.py`: all passed, 2 files formatted. |
| C19 | Do the tests pin the command contract? | Private-copy experiment (copies deleted, `CLEANED`): unmutated copy `110 passed`; M1 argument-hint minus `[--output <dir>]`, M2 `name: sweepx`, M3 `> Skill sc:other-protocol`, M4 default `6h` changed to `72h`, M5 do-not-proceed sentence removed: each `110 passed`. See F4. |
| C20 | Routing row R5 | `git diff -- tests/recommend/test_routing_refresh.py`: one line, `_POST_REFRESH_ADDITIONS = {"graph", "impact", "issue"}` becomes `{"graph", "impact", "issue", "sweep"}`, equal to DESIGN `:719`. `test_routing_refresh.py` is 100% green inside the 628 passed. |
| C21 | Recorded evidence agrees with disk | `step-1.14-checks.md:35-39` section lines 18/22/31/42/57 equal the headings I read; its line 49 and 53 equal `sweep.md:49,53`. `test-sweep-command.txt` shows `collected 110 items ... 110 passed`, exit 0, equal to the summary's 14 + 70 + 14 + 12 = 110 and to my run. `r5-routing-refresh.txt` shows `collected 248 items`. |
| C22 | Style anchor after item 7.10 | `git diff -U0 -- src/superclaude/output-styles/pragmatic.md`: line 22 changed from "No exceptions." to "The only exception is the sweep chat-summary exception defined in the four sub-bullets below."; four sub-bullets at lines 23-26; six `Except for the sweep chat-summary exception above,` qualifiers (lines 57, 62, 64, 73, 84, 94, as in `step-7.10-style-exception.md:36`). The exception is bounded to the loaded `sc-sweep-protocol` skill for an actual `/sc:sweep` run and the command file does not contradict it (the command prescribes no reply format). |

## Checks

A FAIL on a check whose only findings are MINOR does not fail the gate (severity rule).

| id | Result | Gate impact |
|---|---|---|
| C1 | PASS | none |
| C2 | PASS | none |
| C3 | PASS | none |
| C4 | PASS | none |
| C5 | PASS | none |
| C6 | PASS | none (MINOR F3 noted) |
| C7 | PASS | none |
| C8 | PASS | none |
| C9 | PASS | none |
| C10 | PASS | none |
| C11 | PASS | none |
| C12 | PASS | none |
| C13 | FAIL | none, MINOR F2 only |
| C14 | FAIL | none, MINOR F1 only (forward reference to item 12.2) |
| C15 | PASS | none |
| C16 | PASS | none |
| C17 | PASS | none |
| C18 | PASS | none |
| C19 | FAIL | none, MINOR F4 only (design does not require these pins) |
| C20 | PASS | none |
| C21 | PASS | none |
| C22 | PASS | none |

## Summary

- Checks: 22 run, 19 PASS, 3 FAIL (all three MINOR only).
- BLOCKING: 0. MAJOR: 0. MINOR: 4 (F1 to F4).
- Confidence: Verified: 22/22 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- Tool engagement (approximate counts, above the 22-check minimum): Read: about 30 | Grep: about 14 | Glob: 2 | Bash: about 12 (one Bash call was the /tmp mutation batch, 7 variants); tavily and web: none used.
- Not done by design: no live Orca, ccsession or Claude command; no `superclaude sweep run` against a real Orca; `tests/core` and `tests/skills/test_worker_contract.py` were not run (outside the permitted commands). Whether a live model follows the style exception is not tested here, and the installed `~/.claude/output-styles/pragmatic.md` was not compared (static text review only).

Verdict: PASS
Blocking count: 0
