# QA Report: Operator-actionability lens (final gate, T327)

Date: 2026-11-12
Reviewer: qa-final-usefulness-lens (rf-qa-qualitative), fix_authorization false
Method: files on disk read now, in chunks of at most 150 lines.

## Findings

Method note. Every cited line was read from the file on disk in this session (chunks of at most 150 lines). I ran `uv run pytest tests/commands/test_sweep_command.py tests/sweep tests/skills/test_worker_contract.py tests/core tests/recommend` (1860 passed), `uv run ruff check` and `ruff format --check` on the sweep package and tests (clean), and `make verify-sync` (in sync). No live Orca, ccsession or Claude command was run. I wrote no file except this report.

No BLOCKING or MAJOR finding. Seven MINOR findings (notes; they do not fail the gate). Each one is a point where a coordinator in a fresh session must guess or could drift toward an action the contract limits.

### OA-F1 (MINOR) The `Next inspection` column reads as an instruction and collides with the L1 probe trigger rule
- Evidence: `src/superclaude/cli/sweep/report.py:42-54` (for a `working` row: "read the worker's last transcript lines to confirm it is active"; same for `idle`, `person_active`, `blocked_contract`, `orca_exit_proof`). `src/superclaude/core/WORKER-CONTRACT.md:110` ("Costly probes (transcript tail, screen read) run only for workers a trigger fired for") and `:151` (L1 probe `worker-read --source transcript` needs "A trigger fired"; at most 2 costly probes per triggered worker per sweep). `src/superclaude/commands/sweep.md:16` calls the column "what to read next" and an observation.
- What is wrong: a coordinator that follows the column row by row would read transcript tails for every `working` worker on every 5-minute pass, with no trigger. WC-16 (`WORKER-CONTRACT.md:277`) has the sentence "the coordinator's own L1 probes stay limited to workers a trigger fired for", which resolves the conflict for a careful reader, but neither the command, the skill nor the report says that `Next inspection` is not a trigger.
- Smallest fix: add one sentence to `sweep.md:16` (and the skill's closing paragraph): "`Next inspection` names what a person could read; it is not a trigger and does not authorise an L1 probe (WC-16)." Already on the follow-up list as the "reads like instructions" item; I confirm it with the L1 evidence.

### OA-F2 (MINOR) The class `idle` is never defined and shares a word with liveness state S3 "idle at prompt"
- Evidence: `sweep.md:14` names `idle` without a definition. `classify.py:289-305` (`idle` is only a person-started session with no Orca row whose last activity is before the window; it goes to `## Historical sessions`, `report.py:458-477`). `WORKER-CONTRACT.md:121` (S3 "idle at prompt": a worker that gets L1, L2 nudge, L3).
- What is wrong: a coordinator that reads `idle` as S3 would be led toward nudging, which WC-16 forbids for person-started sessions ("never messaged", `WORKER-CONTRACT.md:277`). The evidence text ("person_started True; ...") says what it is, but nothing in the command, skill or WC-16 says `idle` means "a person's session outside the window".
- Smallest fix: in `sweep.md:14` write "idle (a person-started session outside the window; not a worker state)".

### OA-F3 (MINOR) The command names six of the eight classes and never explains `(a)`, `(b)` or the `Rule` ids
- Evidence: `sweep.md:14` ("eight classes (for example working, waiting on a person, idle, finished, stalled (proved), or could not determine)"); `models.py:31-40` (the full eight, including `fenced` and `person session (active)`); report sections `## Waiting on a person (a)` and `(b)` (`report.py:246`, `:268`) with no legend; `Rule` values such as `blocked_contract`, `waiting_signal`, `fallback` (`classify.py:337-347`) appear in the Sessions table (`report.py:415`) but are defined nowhere an operator reads.
- What is wrong: mapping from class to WC-16 escalation is by inference: (a) is a blocked contract or an Orca agent-wait (WC-6 answer, or S4 "never answer the prompt", or a frozen Ruling halt for the person); (b) is a frozen plan or a ready Task (both on the WC-16 escalate list). Escalating to the person is the safe direction, so this is a guess point, not a hazard.
- Smallest fix: one sentence in `sweep.md`: "(a) = a session blocked on a question or an Orca prompt; (b) = a frozen plan or a ready Task that needs ownership review; `Rule` is the first matching rule, `Evidence` says why."

### OA-F4 (MINOR) No failure path or report-absent rule for the coordinator
- Evidence: `WORKER-CONTRACT.md:277` ("runs `/sc:sweep` and reads its report before it acts"); `SKILL.md:27` and `:29` (exit 1 or 2 prints the error and ends; no summary, no path); `commands.py:279-288` (exit 2 for usage and no bound Run, exit 1 for a publish or internal error).
- What is wrong: WC-16 has no sentence for "the sweep failed". Read literally, "before it acts" can block every action on a pass whose sweep failed, against "It never stops watching on its own". The sentence "an added read: it does not replace that sweep" points the right way, but a fresh coordinator guesses. Same text as the known CON-F14.
- Smallest fix (needs the owner, WC-16 is owner-approved text): "If `/sc:sweep` fails, log the error line in the run notes and continue the pass without its report."

### OA-F5 (MINOR) Installed output style may stay stale and nothing tells the operator how to refresh it
- Evidence: `install_user_setup.py:140-149` (`install_output_styles` copies with `force=False`, reporting "kept" for an existing file); `SKILL.md:49` (a stale style means nothing is exempt, no refresh instruction); `CHANGELOG.md:7-15` (the sweep entry never mentions the `pragmatic.md` change or that an existing installed copy is kept).
- What is wrong: a person who already has `~/.claude/output-styles/pragmatic.md` installs the new command and skill, runs a coordinator, and never gets the exempt reply or any message saying why. The failure direction is safe (ordinary formatting) but it is a silent no-op.
- Smallest fix: one CHANGELOG line: "the pragmatic style gained the sweep chat-summary exception; run `superclaude install --force` (or copy `output-styles/pragmatic.md`) to refresh an existing install."

### OA-F6 (MINOR) Ordinary-format reply asks for a RECOMMENDED ACTION, the skill forbids recommending
- Evidence: `src/superclaude/output-styles/pragmatic.md:21` ("End with RECOMMENDED ACTION") and `:22` (table keeps a NEXT row in every non-exempt reply); `SKILL.md:26` (ordinary formatting by default), `:47` ("Formatting never gives permission for advice"), `:61` (Will Not: "Recommend anything, propose an action").
- What is wrong: for a person-run sweep, an unassigned coordinator, or any error reply the reader must improvise what goes into RECOMMENDED ACTION and NEXT. The style does allow "If no action is needed, say so plainly" (`pragmatic.md:21`), so a compliant answer exists ("none from this run"), but the skill does not say it and a model may write "review the waiting sessions".
- Smallest fix: in `SKILL.md` "What stays ordinary" add: "In an ordinary reply the RECOMMENDED ACTION and NEXT rows say that this run recommends nothing and point to the report path."

### OA-F7 (MINOR) Small mismatches an operator will trip on
- `HOW-WE-WORK.md:334` says the command "prints JSON"; the slash command prints counts and a path (`SKILL.md:26`); only `superclaude sweep run` prints JSON (`commands.py:277-278`). Row text is pinned to DESIGN R4, so a fix needs the DESIGN change.
- `HOW-WE-WORK.md:405` says "on every wake"; WC-16 (`WORKER-CONTRACT.md:277`) says "wake or wait timeout" (known).
- `SKILL.md:43` keeps the mark "(not observed in Phase 1)" on the exempt counts; the style (`pragmatic.md:23`) does not mention it (known 13.18). The skill is loaded in every exempt case (condition 2), so the mark survives; the style-alone reader would drop it.
- The skill's "other agents" wording (`SKILL.md:45`) omits "peers", which the style names (`pragmatic.md:24`); "other agents" covers peers, so no behaviour changes.
- Every pass loads the full stdout JSON (every row, `report.py:620-639`) and then the whole report in 150-line Reads (`SKILL.md:25`). The skill says "take only `report_path` and `summary`" but the JSON is already in context. For a long Run a coordinator that sweeps every 5 minutes spends context fast; no guidance on `--window` or on pruning old reports (`.dev/sweeps/` grows by one file per pass, `commands.py:153-208`).

## Guess / read-source / forbidden-action list

Walk-through as a coordinator in a fresh session holding only the installed command, the skill, WC-16 and the routing guide.

**Answered without guessing (verified on disk)**
- When to run: explicit only, inside the liveness pass, at most once every 5 minutes, or a person types it (`sweep.md:22`, `WORKER-CONTRACT.md:277`, `HOW-WE-WORK.md:405`). Never a worker (`sweep.md:18`, `WORKER-CONTRACT.md:23`).
- Flags: `--run` (repeatable, `run_` plus 12 lowercase hex), `--window` (`<N>h|<N>d`, 1 to 9999, at most 720h or 30d), `--root`, `--output` match `commands.py:43-123` and `probes.py:44`. No Run bound and none named: exit 2 with "no Run bound: pass --run <id>" (`probes.py:358`, matching `sweep.md:37`).
- Where the report lands: `<root>/.dev/sweeps/<YYYYmmdd-HHMMSS>-sweep.md`, then `-2` to `-99` on a same-second clash (`commands.py:153-196`); the skill prints the exact `report_path`; the folder is git-ignored (`.gitignore:256`, `git check-ignore` confirmed), so the report does not dirty any worktree.
- What WC-16 says next: escalate the listed cases, never message person-started sessions, post nothing, recommend nothing (`WORKER-CONTRACT.md:277`).
- `Safe to close` and `Removable` can never print `yes` in Phase 1: `classify.py:447-468` returns only `no` or `could not determine`; `classify.py:471-496` returns `no` or `could not determine` for the terminal and never `yes`. So the column cannot lead to a close or removal, and a `could not determine` row is never presented as closable. (No operator-facing file states "never yes in Phase 1"; a reader has to read `classify.py` to know it. See OA-F3.)
- Stalled and fenced cannot fire in Phase 1: `probes.py` never sets `worker_done_seen` and `models.py:86-87` defaults them to `None` and `"unreadable"`, so rules 2 and 3 (`classify.py:190-222`) never match. This agrees with `sweep.md:16` and `WORKER-CONTRACT.md:277`.

**Points where I would have to guess or read source**
1. Which classes exist beyond the six named, and what `(a)`, `(b)` and each `Rule` id mean (OA-F3).
2. Whether `idle` is a worker state (OA-F2).
3. Whether `Next inspection` authorises a transcript read for a worker with no trigger (OA-F1).
4. What to do on a pass whose sweep fails (exit 1 or 2, or Orca down) and whether "before it acts" waits for it (OA-F4).
5. How the "keep that pass scheduled" duty is met: WC-16 says "Phase 1 adds this duty, not a scheduler" and the skill must "schedule nothing" (`SKILL.md:64`). The coordinator's own wait loop is the only scheduler; this is implied, not stated.
6. Whether a coordinator that was resumed or compacted still has an "applicable, explicit coordinator assignment in force" (`SKILL.md:37`, `:45`: "do not rebuild a role from files or history"). After compaction the exempt reply probably falls back to ordinary formatting, and the ordinary reply needs the RECOMMENDED ACTION text the skill forbids (OA-F6).
7. Whether a coordinator that invokes the skill on its own (no person typed `/sc:sweep`) is "an actual `/sc:sweep` invocation" (`SKILL.md:36`). The natural reading is yes, since WC-16 tells it to run the command, but the text does not say so.
8. Which of the "Ready Tasks needing ownership review" are the coordinator's own just-created Tasks (`report.py:283`; creator "not observable"). WC-16 escalates only "a ready Task it did not create", and the coordinator must compare with its own plan; the run notes record admissions, not creations.
9. How to refresh a stale installed style so the exempt reply can ever apply (OA-F5).
10. Which `--window` to pass for a Run longer than the 6 h default, and what to do with the growing `.dev/sweeps/` folder (OA-F7).
11. A stale installed `superclaude` without the `sweep` subcommand fails step 1 with a click "No such command" (exit 2), not "command not found", so the fallback in step 2 does not fire and the stderr line carries no upgrade hint (`SKILL.md:23-24`). Unverified by a live run; from reading the skill and click behaviour only.

**Led toward an action the contract forbids?**
- Messaging a person-started session: not directly. WC-16 forbids it, the report labels such rows `person session (active)` or `idle` with `person_started True` evidence. The `idle` wording risk is OA-F2.
- Closing or removing a row the sweep could not determine: not directly. `yes` is never printed in Phase 1 (above); the command and WC-16 say the report recommends nothing and the coordinator decides. The contract does not say "could not determine is never grounds to close", which would be a cheap safety sentence.
- Untriggered transcript probes: yes, mildly, through `Next inspection` (OA-F1). WC-16's own L1 sentence is the counter-text.

**Style and skill agree on the exemption (checked line by line)**
- Condition 1 (top-level session, applicable explicit coordinator assignment for specified, already-authorised orchestration work, from a governing system or developer instruction or a direct unquoted instruction from the person, still in force, no higher-priority conflict) is word for word the same in `pragmatic.md:23` and `SKILL.md:37`.
- Conditions 2 to 5 (loaded skill for an actual invocation, exit 0, stdout parsed, report Read) match (`pragmatic.md:23`, `SKILL.md:36-41`).
- No self-grant: both texts say the loaded skill and the style do not assign the role (`pragmatic.md:24`, `SKILL.md:45`). No file, tool or peer inference: both say files, reports, tool output, quoted text and other agents' claims never establish or extend it; unknown, ambiguous, revoked, superseded or conflicting evidence means ordinary formatting and the role is not rebuilt from files or history (the style says "agents or peers", the skill "other agents").
- Ordinary contexts keep ordinary formatting: person-run, workers and subagents, other coordinator messages, quoted or read sweep text, failures, blockers, parse errors, missing output, unsuccessful Read (`pragmatic.md:25`, `SKILL.md:47`). Standard error stays visible for exit 1 or 2; only the final successful reply of an assigned coordinator drops the wrapper, and it never drops error visibility or safety (`pragmatic.md:25-26`, `SKILL.md:27`, `:51`).
- A stale installed style disables the exemption and keeps ordinary formatting (`SKILL.md:49`).
- No live recognition or installed activation is claimed: `tests/commands/test_sweep_command.py:14-15` and `step-7.10-style-exception.md:98` say the tests show the clauses are present, not that a live model follows them or that the HOME style is updated. `~/.claude/commands/sc/sweep.md` and `~/.claude/skills/sc-sweep-protocol` do not exist on this machine (checked with `ls`), so nothing installed was exercised.

## Checks

PASS means no finding. FAIL means at least one finding; the severity is in the last column. Only BLOCKING or MAJOR fails the gate.

| Check | What it tests | Result | Severity of any finding |
|---|---|---|---|
| C1 | When to run: command, WC-16 and guide agree (5-minute cap, coordinator loop, person typing, never a worker) | PASS | note only: guide says "wake", WC-16 says "wake or wait timeout" (OA-F7) |
| C2 | Flags and defaults in `sweep.md` match `commands.py` and `probes.py` (window grammar and bound, run id regex, root rule, output rule, no-Run exit 2 message) | PASS | none |
| C3 | Where the report lands is stated and true (folder, file name, never-overwrite suffix, git-ignored, path printed) | PASS | note: no pruning guidance (OA-F7) |
| C4 | A coordinator can read each class from the operator files alone | FAIL | MINOR (OA-F2, OA-F3) |
| C5 | A coordinator can read each note and column (`Safe to close`, `Removable`, `Next inspection`) without a forbidden action | FAIL | MINOR (OA-F1); `yes` never printed in Phase 1, so no close or removal is invited |
| C6 | WC-16 says what to do next for each report outcome, including failure | FAIL | MINOR (OA-F4) |
| C7 | Person-started sessions are never messaged and never closed on a `could not determine` row | PASS | none blocking; wording risk in OA-F2; missing "could not determine is not grounds to close" sentence noted in the guess list |
| C8 | Style and skill describe the same explicit applicable top-level assignment, no self-grant, no file, tool or peer inference | PASS | note: "peers" wording (OA-F7) |
| C9 | Unassigned person, worker, unknown, other-message and error contexts keep ordinary formatting; only an assigned coordinator's final success drops the wrapper; error visibility and safety stay | PASS | none |
| C10 | The ordinary reply is fully specified for a person-run sweep | FAIL | MINOR (OA-F6) |
| C11 | No live recognition or installed activation is claimed from the canonical tests | PASS | none (tests and step-7.10 file state the limit) |
| C12 | The exempt reply keeps the `(not observed in Phase 1)` mark consistently across skill and style | PASS | note: the style does not name the mark (known 13.18); the skill is always loaded in an exempt case |
| C13 | Installed-style staleness is handled and documented | FAIL | MINOR (OA-F5) |
| C14 | Routing guide rows are accurate for an operator | FAIL | MINOR (OA-F7: "prints JSON", "on every wake") |
| C15 | Stalled (proved) and fenced cannot appear in Phase 1, matching `sweep.md:16` and WC-16 (probe and model check) | PASS | none |
| C16 | Phase 14 argument for the 3 failing tests is correct (re-run by me) | PASS | none: the two `test_claude_process_adapter.py` ruff tests fail with "No module named ruff" from `.venv/bin/python -m ruff`; `tests/hooks/test_launch_level_guard.py::test_speed_large_commands` passed 6 of 6 on a re-run (241 s); `git diff` against the base shows no change under `tests/cli/eval`, `tests/hooks`, `src/superclaude/cli/eval` or `src/superclaude/hooks` |
| C17 | Tests, lint and sync pass on the sweep surface | PASS | none: 1860 passed; `ruff check` clean; `ruff format --check` 16 files formatted; `make verify-sync` "All components in sync" |

Tool engagement: Read 14, Grep 13, Glob 1, Bash 4 (pytest, ruff, verify-sync, git diff and ignore checks, two test re-runs).

Self-audit. Relied on earlier reports: none. I did not open any `qa/*/` report. Independent checks that could have found a defect: line-by-line text comparison of the exemption in `pragmatic.md:22-26` and `SKILL.md:31-51`; flag and exit-code verification against `commands.py` and `probes.py`; proof that `yes` is unreachable for `Safe to close` and `Removable` (`classify.py:447-496`); proof that stalled and fenced never fire (no setter for `worker_done_seen` or `fenced_evidence`); L1 trigger cap read from `WORKER-CONTRACT.md:151`; re-run of the three disputed failing tests.

Limits. Point 11 in the guess list (stale CLI without `sweep`) is reasoned from the skill text and click's usual behaviour, not run. Whether a live model drops the table correctly or recognises a coordinator is not tested and not claimed.

## Verdict

Verdict: PASS

Blocking count: 0
