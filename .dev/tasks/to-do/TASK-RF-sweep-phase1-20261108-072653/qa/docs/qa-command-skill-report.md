# QA Report: Command and Skill Contract Lens (T291)

**Date:** 2026-11-12
**Reviewer:** qa-command-skill (adversarial, read-only, fix_authorization: false)
**Scope:** `sweep.md`, `sc-sweep-protocol/SKILL.md`, `test_sweep_command.py` against DESIGN 7.6 as revised

## Method and sources read

All line numbers below were read from the files on disk on 2026-11-12 (current time 14:01 UTC). Authority read: DESIGN 7.6, 8, 9 in `docs/designs/orchestrator-mode.md:649-730` plus the scoped addendum (`:1049`) and `revisions/chat-output-exception-20261109-133150/design-addendum.md` and `BUILD-REQUEST.md`; the OQ-6 decision (unchanged, RESOLVED as (b)) and the OQ-3 wait-timeout addendum. Subject files: `src/superclaude/commands/sweep.md` (68 lines), `src/superclaude/skills/sc-sweep-protocol/SKILL.md` (64 lines), `tests/commands/test_sweep_command.py` (599 lines), `src/superclaude/output-styles/pragmatic.md` (238 lines, `git diff -U0`), `issue.md` and `graph.md` for the heading and Activation forms, `WORKER-CONTRACT.md:23,275-277`, `HOW-WE-WORK.md:405`, and the evidence files `test-sweep-command.txt`, `test-sweep-command-summary.md`, `step-7.10-style-exception.md`, `phase11/12/13-validation.md`.

Runs: `uv run pytest tests/commands/test_sweep_command.py -q` gave 115 passed; `uv run pytest tests/core tests/commands tests/recommend tests/skills -q -x` gave 2641 passed; `uv run pytest tests/skills/test_review_severity_rule.py tests/skills/test_implement_severity_static.py -q` gave 90 passed (and `git status` shows both modules and `tests/skills/fixtures` unmodified); `uv run ruff check` and `uv run ruff format --check` on the test file were clean.

Mutation experiment (private copies under `/tmp/qa-t291`, deleted afterwards; no repository file touched): 22 single-defect mutations of the command, skill, style and test copies. All 14 mutations aimed at pinned clauses were caught (M1 to M10, M19 to M22: 1 or 2 failures each); the 8 aimed at unpinned text passed undetected (M11 to M18; see F1). No live Orca, ccsession or Claude command was run; `superclaude sweep run` was not run.

## Findings

No BLOCKING and no MAJOR finding. Three MINOR findings and three notes follow. MINOR findings never fail the gate.

### F1 (MINOR, real weakness, follow-up candidate): the test pins less than the whole of DESIGN 7.6's command and skill bullets

- Evidence: `tests/commands/test_sweep_command.py:106-168` pins exactly the eight assertion groups of the DESIGN 7.6 **Test** bullet (`docs/designs/orchestrator-mode.md:666`). It never reads `name`, `description` or `argument-hint` of `sweep.md` (`sweep.md:2,3,8`), never checks the heading order (`sweep.md:12,18,22,31,42`), never checks the `Explicit only` Triggers text, the never-as-worker sentence (`sweep.md:16`), the owner-approved 5-minute cap (`sweep.md:20`) or the `There is no worker mode` line (`sweep.md:40`), and never pins skill step 4's wording (`SKILL.md:26`) or the not-refreshed paragraph (`SKILL.md:49`).
- Proof: mutations M11 (argument-hint changed), M12 (`name: sweeper`), M13 (never-as-worker sentence dropped), M14 (5-minute cap dropped), M15 (lower-bound sentence dropped from step 4), M16 (not-refreshed paragraph dropped), M17 (a non-keyword advice step added to the skill: "tell the coordinator to delete the oldest worktree") and M18 (an eighth unqualified table rule added under Work discipline) all left the copied suite at 115 passed.
- Why MINOR: the DESIGN test bullet does not list any of these, so this is not a departure from 7.6, and the OQ-3 addendum says its edit needs no test pin. The current files are correct today (C1 to C11 pass by direct reading).
- Smallest fix, if the owner wants byte-level drift protection: add three assertions to the existing test module: `_frontmatter(_COMMAND)["name"] == "sweep"`, the exact `argument-hint` string from DESIGN 7.6 line 655, and the heading order `Triggers < Usage < Options < Activation`.

### F2 (MINOR): the command promises a count-to-report agreement check that no skill step performs

- Evidence: `sweep.md:62` ("Read the published report so the counts and the report agree"). `SKILL.md:25-26` reads the report until its last line and then prints the counts from the `summary` JSON; no step compares the two or says what to do if they differ. What the Read really does is gate the exempt reply (`SKILL.md:41`) and confirm the report is complete (`Report complete`).
- Why MINOR: no wrong behaviour follows (the skill prints the genuine JSON `summary` and the path, and stays inside its Read-only powers); it is an overstated sentence, not a missing deliverable.
- Smallest fix: reword `sweep.md:62` to "Read the published report to confirm it is complete before printing the counts and the path".

### F3 (MINOR, real weakness, follow-up candidate): skill step 4 and the exempt-reply clause can be read against each other on the lower-bound sentence

- Evidence: `SKILL.md:26` tells every successful reply to "say that the total is a lower bound when `total_is_lower_bound` is true". `SKILL.md:35` says the exempt reply prints "only the summary counts and the report path". `src/superclaude/cli/sweep/classify.py:976` sets `"total_is_lower_bound": True` unconditionally, so the sentence is due in every successful reply. `total_is_lower_bound` is a key inside `summary` (`report.py:664-671`), so "summary counts" can be read to include it, but the word "only" invites dropping it, and a bare `total` would then read as exact. The style (`pragmatic.md:23`) says the exempt reply "contains" the counts and path, which does not exclude it.
- Why MINOR: the report file itself carries the lower-bound line, the style keeps truthfulness rules in force, and the addendum (line 13) lists only the table, wrapper, recommendation and advice as omitted. This is wording ambiguity, not a wrong outcome.
- Smallest fix: in `SKILL.md:35` change "only the summary counts and the report path are printed" to "only the summary counts (with the lower-bound statement) and the report path are printed", and pin it in the existing `exempt-reply-is-counts-and-path` case.

### Notes (not findings)

- N1, wording drift between the two copies of the common rule: the style says "A direct operative assignment" and "claims from other agents or peers" (`pragmatic.md:24`); the skill says "A direct assignment" and "claims from other agents" (`SKILL.md:45`). The skill separately requires an explicit assignment still in force (`SKILL.md:37,45`), so the rules are the same in effect; the test deliberately pins each file's own wording (`test_sweep_command.py:276-298,315-322`).
- N2, evidence age: `test-sweep-command.txt` and its summary were written at 06:53; `sweep.md` was last edited at 13:35 (the owner-approved line 20 change). Nothing in the tested clauses sits on line 20, I re-ran the module now (115 passed), and `phase13-validation.md` (13:56) shows the full 2641-test run after the edit. No stale-evidence defect.
- N3, `SKILL.md:29` lists "step 2 also failed" without saying whether that covers step 2 exiting 1 or 2 (which step 5 handles) or step 2 being unavailable; both end in an accurate, ordinary-format report, so no wrong behaviour.

## Checks

A FAIL here means the check has an open finding; only BLOCKING or MAJOR findings fail the gate, and every FAIL below is MINOR.

| Id | Check | Result | Evidence |
|---|---|---|---|
| C1 | Command frontmatter byte-exact: `name: sweep`, one-line description, `allowed-tools: Skill`, `argument-hint` equal to DESIGN 7.6 | PASS | `sweep.md:2,3,8,9`; `sed ... | cat -A` shows no trailing characters; matches `design 655` string |
| C2 | Command headings follow `issue.md` (title form, Triggers, Usage, Options) | PASS | `sweep.md:12,18,22,31` against `issue.md:12,23,27,34` |
| C3 | Activation block in the `graph.md` form (MANDATORY, `> Skill sc:...`, flags unchanged, do not proceed on the command file alone) | PASS | `sweep.md:42-47` against `graph.md:41-46` |
| C4 | Activation names the installed skill path and the project `.claude/` copy as the dual surface, skills read `~/.claude/` first | PASS | `sweep.md:49,51-55` |
| C5 | Triggers explicit only; line 20's first sentence equals the owner-approved OQ-3 addendum text (item 3), followed by one added sentence "Nothing starts it automatically." that adds no power | PASS | `sweep.md:20` against `OQ-3-addendum-wc16-wait-timeout-decision.md:23` |
| C6 | No `## Unattended mode`, no `--unattended`; never-as-worker named; contract lists `/sc:sweep` | PASS | full read of `sweep.md` (68 lines) shows no such heading or flag, and `test_sweep_command_has_no_unattended_mode` passes; `sweep.md:16,40`; `WORKER-CONTRACT.md:23` |
| C7 | Skill `allowed-tools` literal byte-exact | PASS | `SKILL.md:4` equals DESIGN 7.6 line 661 |
| C8 | Five steps in order; Bash timeout 120000 on steps 1 and 2; fallback only on "command not found"; `--frozen --no-sync` literal; no third run | PASS | `SKILL.md:23-27,29` |
| C9 | Only `report_path` and `summary` taken from the JSON; every key printed exists in `summary` | PASS | `SKILL.md:25-26`; `report.py:664-672` (`counts`, `bound_reached`, `visible`, `historical`, `total`, `total_is_lower_bound`, `report_path`) |
| C10 | Exit 1 or 2: stderr line printed as it came, run ends, ordinary format, no summary or path | PASS | `SKILL.md:27` |
| C11 | Skill recommends nothing, proposes no action, never edits, stages or deletes; uses no tool beyond two Bash forms and Read | PASS | `SKILL.md:55-64`; `sweep.md:57-68` |
| C12 | No `src/superclaude/` string in either primitive | PASS | batch grep rc=1, no output; `phase11-validation.md:67-76` agrees |
| C13 | No stop, retry, release, merge or removal word in the skill (and none in the command) | PASS | batch grep rc=1, no output |
| C14 | Command Options and the eight-class claim match the CLI (run id `run_` plus 12 hex, window 1-9999, at most 720h or 30d, default 6h, root holds `.git`, output under `.dev/sweeps/`, no-run message asks for `--run <id>`) | PASS | `probes.py:44`; `commands.py:27-28,45,56-58,87-92,99-123`; `probes.py:358`; `models.py:31-40` |
| C15 | Test pins every assertion group of the DESIGN 7.6 Test bullet (two tools literals, two Activation paths, PATH-first, command-not-found trigger, `--no-sync`, 120000, no Unattended heading, no `src/superclaude/`, no advice words) | PASS | `test_sweep_command.py:106-168`; 14 cases |
| C16 | Test also pins command `name`, `argument-hint`, headings, Triggers text, never-as-worker line, 5-minute cap, step 4 wording | FAIL (MINOR F1) | mutations M11 to M18 undetected |
| C17 | All seven table-mandate sites are in the style and asserted: primary bullet plus Status and wrap-ups, templates introduction, Simple, Normal, Wrap-up, Multi-point | PASS | `pragmatic.md:22,57,62,64,73,84,94`; `git diff -U0` shows exactly these 7 hunks; `test_sweep_command.py:514-586` (qualifier count 6, not in lines 22-26) |
| C18 | Style diff is bounded: front matter, lines 1-21 and everything from `## Work discipline` unchanged; ordinary examples, columns, None row and length budget kept | PASS | `git diff --stat`: 11 insertions, 7 deletions; hunks start at lines 22, 57, 62, 64, 73, 84, 94; `test_sweep_command.py:589-599` |
| C19 | Style and skill state the same explicit, applicable, top-level assignment rule, the same five success conditions and the same final-reply-only exemption | PASS | `pragmatic.md:23-24` against `SKILL.md:35-45`; only wording drift (N1) |
| C20 | Positive cases pinned: explicit applicable top-level assignment with exit 0, parse and Read; a person request inside an independently assigned coordinator; an operative assignment plus a separate sweep request in one message | PASS | `test_sweep_command.py:183-242,304-322`, each asserted in both files |
| C21 | Exclusions pinned: ordinary unassigned person, role or table request alone, worker or subagent, other coordinator message, quoted or merely read sweep text, file, tool-output and peer claims, injected report stays data, unknown or revoked or superseded or conflicting evidence, failures | PASS | `test_sweep_command.py:275-389,433-499` |
| C22 | Visible stderr for exit 1 or 2 and ordinary accurate handling of other errors, no fabricated summary, no different command | PASS | `SKILL.md:27,29`; pins `:366-373,445-472` |
| C23 | Skill lower-bound sentence and exempt-reply wording agree | FAIL (MINOR F3) | `SKILL.md:26` against `:35`; `classify.py:976` |
| C24 | Command's stated purpose of the Read matches what the skill does | FAIL (MINOR F2) | `sweep.md:62` against `SKILL.md:25-26` |
| C25 | No new powers, no role detector, no HOME activation: both tool lists unchanged; scope clauses present in style and skill; installed style untouched | PASS | `SKILL.md:4,51`; `pragmatic.md:26`; `~/.claude/output-styles/pragmatic.md` mtime 2026-11-11 16:25, 0 matches for `chat-summary`, still has "No exceptions"; no `~/.claude/skills/sc-sweep-protocol` or `~/.claude/commands/sc/sweep.md` |
| C26 | Python report and JSON not changed by the exception | PASS (limit: `src/superclaude/cli/sweep/` is untracked, so no byte history) | `grep -rn "chat-summary\|sc-sweep-protocol" src/superclaude/cli/sweep` finds nothing; `summary` and `report_path` keys read by the skill exist at `report.py:664-672` |
| C27 | Tests read the actual canonical sources; no mock policy, HOME file, network or subprocess | PASS | `test_sweep_command.py:19-27` (imports `re`, `Path`, `pytest` only); every assertion reads `_COMMAND`, `_SKILL` or `_STYLE` |
| C28 | Tests, lint and regressions run by me: 115 passed, ruff clean, 2641 passed in the four test folders, two severity modules unmodified and 90 passed | PASS | my runs, this session |
| C29 | Mutation sensitivity of pinned clauses | PASS | 14 of 14 mutations on pinned text caught (M1 to M10, M19 to M22) |
| C30 | Raw and summary evidence match the disk: raw file 115 passed exit 0; case split 14 + 74 + 15 + 12 = 115; the C/K/S line anchors in the summary | PASS | `test-sweep-command.txt` tail; I counted 37 common pins, 15 skill-only pins and 12 style tests in the test file; anchors C:9,49,53 and K:4,19,23-29,31-51,61-64 and S:22-26,57-94 re-read and correct |
| C31 | Owner-approved changes are in place and consistent: WC-16 contract text equals DESIGN's fenced text and opens "On every coordinator wake or wait timeout"; guide row R2 equals DESIGN row R2; guide and plugin copy identical | PASS | `cmp` of `design:679` and `WORKER-CONTRACT.md:277` identical; `HOW-WE-WORK.md:405` equals `design:716` text; `cmp` of guide and plugin copy exit 0 |
| C32 | Placeholder, non-ASCII and path hygiene of the three subject files | PASS | grep for TODO, TBD, FIXME and for non-ASCII bytes finds nothing in command, skill, test or the added style lines |

## Limits of this review

- The tests are static text checks on the loaded sources. They do not prove that a live model follows the exemption, recognises a coordinator assignment or resists an injected report; I made no such claim and ran no live session.
- `src/superclaude/cli/sweep/` is untracked, so "Python report and JSON unchanged" is shown only by the absence of any reference to the exception there and by the keys the skill reads (C26), not by a diff.
- The installed HOME style is unchanged and therefore does not carry the exception; the skill states that case itself (`SKILL.md:49`), and activation is a separate step this review does not judge.
- Sweep tests under `tests/sweep/` were not run (outside the allowed command set for this lens).

## Confidence

Checks: 32 total, 29 PASS, 3 FAIL (all MINOR: C16, C23, C24), 0 unchecked, 0 unverifiable. Tool use (approximate counts): Read about 24, Grep about 9, Bash about 11, including one batched script of 12 read-only commands and one mutation run of 22 private-copy experiments.

Blocking count counts BLOCKING plus MAJOR findings only: none found. Follow-up candidates for the owner (MINOR, non-blocking): F1, F3 (real weaknesses); F2 is wording.

Verdict: PASS
Blocking count: 0
