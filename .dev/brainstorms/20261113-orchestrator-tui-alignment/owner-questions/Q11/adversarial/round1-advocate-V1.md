# Round 1 advocate statement: Variant 1 (both reports, now)

Advocate: Variant 1 (proposal A). Persona: analyzer. Depth: quick, Round 1 only.
Paths below are relative to the worktree root `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode`. "ADJ" is `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/alignment-findings-adjudicated.md`. "V5" is `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/adversarial/variant-5-original.md`. "MR" is `.dev/brainstorms/20261113-orchestrator-tui-alignment/merged-requirements.md`. MR:748 and MR:1032 are taken from question.md and were not re-read by this advocate.

## Position summary

Variant 1 is the only answer that gives #339 what it actually asked for: a static report of all agents, sessions and worktrees modelled on #409, not just a count line and a file path. Both programs it names already exist, the observer's one-shot mode writes no file, so it can sit beside the sweep without breaking any rule, and the decision is recorded-only, so the owner loses little by stating the full intent now.

## Steelman

**Variant 2 (sweep summary only, until the contract note).** Its strongest form: this is the spec's own recommended answer and its default (MR:538), and section 6.7 already says it (MR:1040), so choosing it costs zero edits to the spec, the worker contract, the sweep skill, the output style or the open sweep PR. It keeps one source of truth in chat while the observer and the sweep still use different status words (V5:216 lists the shared word list the contract note must fix: stale, unknown, unavailable, historical and others). It also follows V5's D2 recommendation exactly: "keep the sweep reply as the WC-16 output until D1 is settled; do not name `observe` in WC-16 or the skill's `allowed-tools` yet" (V5:222). It is the lowest-risk, most reversible choice, and it honestly states its own gap: "every 3 minutes" is not met and the reply is narrower than #409.

**Variant 3 (neither yet, park the clause).** Its strongest form: no coordinator loop exists to print anything every 3 to 5 minutes (question.md fact 10), and WC-16 is a cap, not a schedule (ADJ:81; `src/superclaude/core/WORKER-CONTRACT.md:109` "at most once every 5 minutes"). Promising a cadence with nothing to run it is a false promise. The owner's stated preference is that automated status shows outstanding decisions only (MR:1040, quoting SEED Batch 2 item 8). Parking avoids picking a format before the contract note fixes a shared word list. It is the most honest about what exists today.

## Strengths claimed

1. **Fidelity to the issue.** The issue summary says #339 wants "a static report of all agents, sessions and worktrees (modelled on #409) that replaces the usual end-of-message table" (`.dev/issues/339/issue-summary.md:10`), and lists #409 as the design "the static report layout should follow" (same file :26). The sweep's exempt reply prints "only the summary counts and the report path" (`src/superclaude/skills/sc-sweep-protocol/SKILL.md:35`, rule at :31-43). Only the observer text is a fleet picture. Variant 1 is the only variant that meets the literal ask (diff C-005).
2. **No new program.** `observe --once` is built: `run_once` collects once, renders a bound-width screen when `--width` is given, prints it, and writes a snapshot only when `--snapshot` is passed (`src/superclaude/cli/observe/commands.py:215-237`). ADJ E-17 says the same and is marked "verified in Round 1" (ADJ:143): "the #339 'static report in chat' ask does not need a new program".
3. **No conflict with the one-report-per-run rule.** NFR-001 says "a sweep adds exactly one report file" (ADJ:83). Because `observe --once` writes nothing without `--snapshot` (commands.py:232-236), it can run between sweeps without adding files (diff U-001).
4. **It is the only variant that can reach the 3-minute end of "3 to 5 minutes".** The sweep is capped at once every 5 minutes (WORKER-CONTRACT.md:109). The observer carries no such cap in the contract, so a 3-minute report is possible only with the observer (diff C-004).
5. **Honest risk statement.** Variant 1 is the only variant that names the Q-1 gate failure (ADJ:87: "an unbound terminal cannot read another terminal's Run ... failed on 2026-11-11") as an open risk for the coordinator's own terminal, and marks it UNVERIFIED (diff U-002). It also names the unmeasured combined load (INV-032) and the word-list mismatch. An owner choosing it chooses with the risks in view.
6. **A cheap way to retire the main risk exists.** The observer has a `--run <runId>` option (commands.py:435-436), and V5 already proposes the owner run `superclaude observe --once --run <run>` (writes nothing without `--snapshot`) to compare dispatch ids with the sweep rows (V5:217). The same run would show whether a coordinator terminal sees its own Run. Whether `--run` from the coordinator's terminal avoids the Q-1 failure is UNVERIFIED.
7. **The owner's first-PR scope paired sweep with the report.** The issue summary records the owner's first-PR scope as "read-only `/sc:sweep` plus static report" (issue-summary.md:28) and budgets "`/sc:sweep` with the static report about 20" hours (:6). The report is a named deliverable, not an afterthought. Variant 1 keeps the sweep reply as half of it and supplies the other half.

## Weaknesses identified in others

1. **Variant 2 answers a narrower question than #339 asked.** It concedes the reply is "counts plus a path, not a #409-style fleet picture" and that "every 3 minutes" is not met (variant-2-original.md, "What it costs or risks"). So for an undated period (its own words: "'Until the note exists' has no date") the issue's report clause is met only in name. A count line and a path do not usefully "replace the usual end-of-message table"; the person still opens a file.
2. **Variant 2's trigger is outside its control.** It ties the revisit to XC-05, which waits on Q5 and other work (variant-2-original.md). Nothing in Variant 2 makes the reopen happen; it relies on someone adding a line to the contract note.
3. **Variant 3 contradicts the scope the owner already set.** The owner's first-PR scope is "read-only `/sc:sweep` plus static report" (issue-summary.md:28). Parking the report clause drops half of that scope. Variant 3 also says the sweep reply is not the #339 report (diff X-002), which leaves the sweep's chat-summary exception (`src/superclaude/output-styles/pragmatic.md:22-23`) with no stated purpose, a cost Variant 3 itself admits.
4. **Variant 3 adds edits while claiming to wait.** It removes the last sentence of section 6.7 and adds a deferral row to #534 (variant-3-original.md). That is more paperwork than Variant 2 and delivers nothing.
5. **Variant 3 conflates "no loop yet" with "no report yet".** A static report can be printed on demand today (both `/sc:sweep` and `observe --once` exist). The missing loop limits the cadence, not the content. Deciding the content now is still useful so that the loop, when built, is built to it.

## Concessions

1. Variant 1 implies edits that are not scheduled: section 6.7 wording, and later WC-16, the sweep skill's `allowed-tools` and possibly the output style (variant-1-original.md, "What happens next"). Variant 2 implies none. This is real cost.
2. Variant 1 runs against V5's D2 recommendation not to name `observe` in WC-16 or `allowed-tools` before the contract note (V5:222). The analysis behind D2 (two word lists for the same facts, V5:216) is sound, and Variant 1 does not solve it.
3. The Q-1 failure (ADJ:87) is a genuine unknown. If the coordinator's terminal cannot see its own Run through `observe --once`, half of Variant 1 does not work, and the owner would have stated an answer that has to be walked back.
4. Combined load of observer, sweep and watcher was never measured (INV-032; MR:1032 per question.md limits the coordinator to at most one observer instance).
5. Variant 3 is right that no loop exists to print anything every 3 to 5 minutes (question.md fact 10). Variant 1's cadence benefit is future value only.
6. "Now" is the weakest word in Variant 1. The content choice is strong; the timing is not, because the main risk has a cheap check that has not been run.

## Shared assumptions

- **A-001** (no work item behind it, so a wrong answer is cheap to reverse): QUALIFY. The ledger record is cheap to reverse (MR:538 "none scheduled"), but Variant 1's answer implies later edits to WC-16, the sweep skill and the output style, and those would not be cheap to reverse once made.
- **A-002** (the contract note XC-05 will be written, so "until the note" is a real trigger): ACCEPT. XC-05 is a planned item in wave W1 (MR:540, row Q13 names XC-05 and W1), so the trigger is real, though it has no date.

## Per-point verdicts

| Point | Winner | Confidence | Reason |
|---|---|---|---|
| S-001 | Tie (1 = 2 = 3) | 90% | All three use the same five sections; no structural advantage. |
| C-001 | 1 | 55% | Only "both" gives a fleet picture (issue-summary.md:10) while keeping the sweep reply; the Q-1 risk keeps the margin small. |
| C-002 | 2 | 55% | Waiting for the note avoids two word lists in chat (V5:216); "now" is premature while Q-1 is unchecked. |
| C-003 | 2 | 70% | Zero edits; section 6.7 already says it (MR:1040). |
| C-004 | 1 | 65% | Only the observer can reach the 3-minute end; the sweep is capped at 5 minutes (WORKER-CONTRACT.md:109). |
| C-005 | 1 | 80% | #339 asks for a #409-style report of agents, sessions and worktrees (issue-summary.md:10, :26). |
| X-001 | 2 | 55% | Not naming `observe` until the note follows V5:222; Variant 1 defers the naming to the unbuilt loop, so the gap is small. |
| X-002 | 1 | 60% | The owner's first-PR scope pairs the sweep with the static report (issue-summary.md:28), so the sweep reply is part of it, not all of it. |
| X-003 | 2 | 60% | Keeping 6.7 as written is cheapest and already matches the recorded default (MR:538, MR:1040). |
| U-001 | 1 | 75% | `--once` writes nothing without `--snapshot` (commands.py:232-236), so NFR-001 (ADJ:83) holds. |
| U-002 | 1 | 85% | Only Variant 1 surfaces the Q-1 failure (ADJ:87) as a risk; the other two are silent on it. |
| U-003 | 3 | 70% | The loop is unbuilt (question.md fact 10), so no cadence promise can be kept today. |

## Overall ranking and unassigned pick

Ranking (best first): Variant 1, Variant 2, Variant 3. Variant 1 wins on what the report should contain (C-001, C-004, C-005, X-002, U-001, U-002); Variant 2 wins on timing and cost (C-002, C-003, X-001, X-003); Variant 3 contributes U-003 but drops half of the owner's stated first-PR scope.

Unassigned pick: honestly, Variant 2, with one addition from Variant 1. Record "sweep summary only until the contract note", and add the V5:217 check (`superclaude observe --once --run <run>` from the coordinator's terminal) to the contract note's work, so that Q-1 is answered before `observe --once` text joins the chat report. That keeps zero edits now and makes Variant 1's content the planned destination rather than an open question.
