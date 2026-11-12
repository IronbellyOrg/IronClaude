# QA Report - T249 Reader-clarity lens (cmd-skill gate)

**Date:** 2026-11-12
**Phase:** code gate, reader-clarity lens (rf-qa-qualitative)
**fix_authorization:** false (report is the only file written)

Method: every cited line was read from disk on 2026-11-12 (both primitives are under 150 lines and were read whole; the style, DESIGN, addendum, CLI source and tests were read in chunks of at most 150 lines). Ran `uv run pytest tests/commands/test_sweep_command.py tests/recommend/test_routing_refresh.py -q` (358 passed), `uv run ruff check` and `ruff format --check` on both test files (clean), and plain greps. One experiment on a private /tmp copy (deleted afterwards; repository files unchanged, confirmed with `git status --short`).

## Findings

### F1 (MAJOR) SKILL.md:27 step 5 contradicts SKILL.md:47 on what an exit 1 or 2 reply contains
- Evidence: `SKILL.md:27` "On exit 1 or 2, print the standard error line exactly as it came and end the run. Nothing else is printed as a result." `SKILL.md:47` "The exception does not cover ... failures ... Non-exempt replies keep the ordinary table and its placement." `pragmatic.md:25` says the same ("Keep stderr visible for exit 1 or 2 ... Non-exempt replies keep the ordinary table"). Addendum line 19: "Preserve visible stderr for exit 1 or 2 ... Non-exempt replies retain the ordinary table and its placement."
- What is wrong: a failure is non-exempt, so line 47 and the style say the reply keeps the DONE / NEXT table. Step 5 read literally says nothing else is printed, which removes the table. A coordinator new to the project cannot tell which applies on an error reply, and line 47's own sentence puts "ordinary formatting" only on "other failures", not on exit 1 or 2.
- Smallest fix: keep the pinned sentence "On exit 1 or 2, print the standard error line exactly as it came and end the run." and replace "Nothing else is printed as a result." with "The reply keeps the ordinary formatting, and no summary and no report path are printed." Verified on a private copy: all 110 tests in `tests/commands/test_sweep_command.py` still pass and no forbidden word (stop, retry, release, merge, removal) appears. Rewording the pinned sentence itself fails `test_skill_states_clause[exit-1-or-2-prints-stderr-and-ends-run]`, so do not touch that sentence.

### F2 (MAJOR) SKILL.md:33 and :43 do not separate canonical style text from the installed style, and the two disagree on this machine
- Evidence: `SKILL.md:33` "It is the same rule as the sweep chat-summary exception in the output style `pragmatic` (installed as `~/.claude/output-styles/pragmatic.md`)". Installed file read now: `~/.claude/output-styles/pragmatic.md:22` still says "EVERY response includes a DONE / NEXT table. No exceptions."; `grep -c 'sweep chat-summary exception'` on it prints 0. The canonical `src/superclaude/output-styles/pragmatic.md:22-26` carries the exception. `src/superclaude/cli/install_user_setup.py:74-76` (`_copy_tree`) skips an existing target unless `force`, so an upgraded install keeps the old style. `step-7.10-style-exception.md` check C10 and addendum line 39 record that the HOME copy is not refreshed by this work.
- What is wrong: the skill tells the reader the installed style carries the same rule. For an existing install it does not, and the skill gives no tie-breaker. Also `SKILL.md:43` lists the precedence it takes over (lead sentence, recommended action, gloss) but not the table rule that `SKILL.md:35` omits, so against a stale style ("No exceptions") the skill never claims to override the table rule. The reader cannot tell canonical text from installed activation.
- Smallest fix (a wording choice for the authority, safe default shown): add one sentence to "Final reply", for example "If the output style text loaded in this session has no sweep chat-summary exception (an installed copy that was not refreshed), nothing here is exempt and every reply keeps the ordinary formatting." Verified on a private copy: 110 tests pass with that sentence added before "**Scope.**". No HOME change is needed.

### F3 (MINOR) sweep.md:16 states a list entry that is not on disk yet, and overstates what the list does
- Evidence: `sweep.md:16` "It is on the never-as-worker list in `~/.claude/WORKER-CONTRACT.md`, so a dispatched worker never runs it." `src/superclaude/core/WORKER-CONTRACT.md:23` and `~/.claude/WORKER-CONTRACT.md:23` list agent, git, help, issue, pm, spawn, swarm-wizard only. Task item 12.2 (step 1.18, add the entry) is still `[ ]`. `WORKER-CONTRACT.md:16,20,22` show the list works through the brief guard on a brief's `Command:` line only; commands invoked inside another command are never checked.
- Why minor: DESIGN 7.6 (line 657) and section 8 plan this exact claim and the entry lands at item 12.2; the sentence is true after that. "So a dispatched worker never runs it" is stronger than a dispatch-time guard. Carry forward: the final and source-fidelity gates must confirm `WORKER-CONTRACT.md:23` names `/sc:sweep` before merge.

### F4 (MINOR) sweep.md:20 "on every wake" is undefined and drops the cadence cap
- Evidence: `sweep.md:20` "the coordinator runs `/sc:sweep` on every wake". DESIGN section 9 R2 and the WC-16 text (lines 679, 716) say "on every wake, at most once every 5 minutes". "Wake" is contract jargon (`WORKER-CONTRACT.md:110`) not defined in either primitive. "Explicit only" next to "every wake" can read as a schedule.
- Fix: "the coordinator runs `/sc:sweep` on a wake, at most once every 5 minutes, or a person types it" (no WC-16 citation until it lands).

### F5 (MINOR) SKILL.md:26 vs :35 "alone" and "only" versus the lower-bound statement
- Evidence: step 4 (`SKILL.md:26`) says to say the total is a lower bound when `total_is_lower_bound` is true; `src/superclaude/cli/sweep/classify.py:976` sets it to `True` always in Phase 1. `SKILL.md:35` says "only the summary counts and the report path are printed". Step 4 also says the format "depends on who runs the skill", but the five conditions at :37-:41 are mostly success state, not who.
- Fix: say that the lower-bound wording is part of the counts, and replace "who runs the skill" with "whether every condition under Final reply holds".

### F6 (MINOR) "Read successfully" is undefined; sweep.md:62 promises a check the skill does not make
- Evidence: `SKILL.md:25` Reads "until its last line, `Report complete`" (`report.py:520`); `SKILL.md:29` lists only "fails or is denied"; `SKILL.md:41` "was Read successfully". `sweep.md:62` "Read the published report so the counts and the report agree" but no step compares them or says what happens on a mismatch or a missing footer.
- Fix: define success as reaching `Report complete` without a tool error, and reword `sweep.md:62` to "Read the published report to its last line".

### F7 (MINOR) SKILL.md:26 prints labels it never defines
- Evidence: `visible`, `historical`, `bound_reached` appear with no meaning in either file; code gives `historical` = idle sessions and `visible` = total minus idle (`classify.py:964-971`), `bound_reached` = Orca reads cut by the budget (`classify.py:966`). A non-exempt reply must gloss labels (`pragmatic.md:39`) but the skill gives nothing to gloss from. Fix: one clause per label, or print only `total` and the per-class counts.

### F8 (MINOR) SKILL.md:45 person request inside an assigned coordinator is a double negative
- Evidence: "neither removes that assignment nor, by the request alone, creates one." The outcome (the exempt reply can still apply if every other condition holds) is only implied. "Person-run exclusion" is used at :45 before :47 introduces the matching "ordinary person-run invocations". Fix: add "In that case the assignment still counts, and the exempt reply applies only if every other condition holds."

### F9 (MINOR) non-exempt success reply: required RECOMMENDED ACTION versus "recommends nothing"
- Evidence: `pragmatic.md:21` requires a RECOMMENDED ACTION and a NEXT row; `SKILL.md:59` and `:47` forbid advice. `:47` ("Formatting never gives permission for advice this skill does not give") resolves it by precedence but never says what the lines hold. Fix: say they state that no action comes from this skill.

### F10 (MINOR) small claims wider or narrower than the CLI
- `sweep.md:14` "the worktrees of this checkout": `probes.py:1226-1237` reads the checkout root plus every path from `orca worktree ps`.
- `sweep.md:14` "the one file it adds": `commands.py:158` also creates the report folder and a transient temp file.
- `sweep.md:38` "the folders the sweep reads" is not named (`commands.py:258-260`: `.dev/tasks`, `~/.claude/projects`, ccsession orca-tabs).
- `SKILL.md:27` "the standard error line": `commands.py:283-285` can print several lines.
- `SKILL.md:5` description "changes nothing" versus `SKILL.md:15` "does all the ... writing".

## Checked and found clear
- No new detector or power is implied: `SKILL.md:49` says the rule is not a runtime detector, identity check or flag; `SKILL.md:19` adds no flag, environment variable or worker mode; allowed-tools literals match DESIGN 7.6 and the tests.
- Assignment vs labels and data: `SKILL.md:45` states that invoking, quoting, the word coordinator, the skill, the style, files, reports, tool output, quoted text and agent claims never establish the assignment; ambiguity defaults to ordinary formatting. The style at `pragmatic.md:24` agrees clause for clause (wording differences are pinned in the tests and do not change meaning).
- Success vs failure: the five conditions (:37-:41), "only the final successful reply" (:43) and the failure list (:29, :47) are consistent apart from F1, F5 and F6.
- Options, defaults and limits in `sweep.md:35-38` match `commands.py` (6h, 1 to 9999, 720h or 30d, `run_` plus 12 hex digits, `.git` required, output under `.dev/sweeps/`). No `src/superclaude/` path, no `--unattended`, no stop/retry/release/merge/removal word, no em or en dash in either file (greps).
- DESIGN 7.6 structure and R5 (`_POST_REFRESH_ADDITIONS` now `{"graph","impact","issue","sweep"}`, assertion at test line 648) hold; the diff of `test_routing_refresh.py` is that one line.

## Checks
| Check | Result |
|---|---|
| C1 Real applicable coordinator assignment distinguishable from invocation, role labels and data claims (SKILL.md:37, :45) | PASS |
| C2 Ordinary unassigned person sessions distinguishable from person requests inside an assigned coordinator (SKILL.md:45, :47) | PASS (wording note F8) |
| C3 Successful final reply distinguishable from other messages and errors (SKILL.md:26-29, :35-47) | FAIL (F1; notes F5, F6) |
| C4 Canonical style text distinguishable from installed activation (SKILL.md:33, :43) | FAIL (F2) |
| C5 No undefined detector or new power implied | PASS (notes F3, F7) |
| C6 No contradiction between sweep.md and SKILL.md | PASS (F3, F4 are claims, not contradictions) |
| C7 No contradiction with DESIGN 7.6 and its addendum | FAIL (F1 against addendum line 19) |
| C8 No claim wider than the CLI | PASS with notes (F3, F10) |
| C9 Options table matches `commands.py` defaults and limits | PASS |
| C10 Tests and routing refresh: pytest 358 passed, ruff clean, R5 diff is one line | PASS |
| C11 Earlier reviews not relied on; all judgments from files read now | PASS |

Confidence: 11 of 11 checks verified with tool evidence, 0 unverifiable, 0 unchecked. Tool engagement is approximate: Read about 33, Grep about 17, Bash 7, plus one private-copy experiment that was removed.

Self-audit: I read both primitives, the canonical and installed style, the addendum, DESIGN 7.6 and 9, `commands.py`, `probes.py`, `classify.py`, `report.py`, `install_user_setup.py`, contract lines 12-25 and the whole test file, and re-derived the 110-test count (14 + 70 + 14 + 12). Two blocking findings, not zero: F1 is a literal conflict and F2 is observed on disk. The drift axis does not apply to this lens (no task-qualitative axis table).

Verdict: FAIL
Blocking count: 2
