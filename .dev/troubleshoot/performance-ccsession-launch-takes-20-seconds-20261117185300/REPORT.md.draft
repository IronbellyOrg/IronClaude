# Troubleshoot Report

**Target**: ccsession launch takes 20 seconds and 5-10% of the CPU when session list is large (GitHub issue IronbellyOrg/IronClaude#607)
**Type**: performance
**Tier reached**: 2
**Confidence**: 0.83
**Status**: partial <!-- merged: failed > blocked > partial > success. partial because the Wave 4 self-review returned FAIL with one blocking finding (F1) that was corrected in the text only and not re-reviewed, and the diagnosability verdict is partial -->
**Escalation reason**: forced_by_depth_deep
**Test is wrong**: false
**Behavior is documented**: false
**Doc context card**: .dev/troubleshoot/performance-ccsession-launch-takes-20-seconds-20261117185300/doc-context.md
**Duration**: 2473 seconds
**Date**: 2026-11-17T19:27:04Z

---

> ⚠ **Diagnosability Caveat**: Your hypothesis depth was constrained by insufficient evidence. See
> Diagnosability Context and pending evidence in Next Steps below. Execution remains subject to
> capability, authorization, transport and round-cap restrictions.

## Summary

The saved-session list that `ccsession --ask` builds before every new plain Claude tab takes 22.5 to 27.1 s with 477 saved names (measured here, reproducing the reported 20 s), and nothing is printed until it ends. The cause is measured, not guessed: the list code runs about 13 external processes plus a transcript scan for every saved name, and the `LC_ALL=C` meant to speed up the transcript scan never reaches `grep` (a `local` variable is not exported), which costs about 7 s of a 23.6 s listing. Status is partial: the independent review of the merged remediation found one blocking mistake (per-row caches built inside `$(...)` subshells are lost), which is corrected in the text below but not re-reviewed, and the reported 5-10% CPU was not reproduced (about 2.5% of this 28-core machine).

## Documentation Context

- **Relevant refs**: /home/coder/workspaces/IronClaude/src/superclaude/skills/ccsession-tag/README.md, /home/coder/workspaces/IronClaude/docs/testing/v5.0.0/user/D08-ccsession.md, .dev/releases/current/v5.0.0/post-release/scan/DE2-claude-surface.md
- **Documented behavior**: `--list`, `--here` and `--ask` have a pinned output and exit-code contract and a 30 s question limit inside Orca's 60 s readiness window; no document sets a speed or CPU target.
- **Restrictions honored**: read only the start and end of a transcript, GNU-first stat, bash 3.2, "Listing never writes any file" (README:190), pinned row formats and exit codes.
- **Restrictions overridden**: None
- **Card path**: .dev/troubleshoot/performance-ccsession-launch-takes-20-seconds-20261117185300/doc-context.md

## Diagnosability Context

**Verdict**: partial
**Complexity classification**: non-trivial
**Captured-bytes (failing run)**: n/a (audit-time only)

The launcher has no timing, debug or trace output on the listing path (no `CCSESSION_DEBUG`, no verbose or timing switch, every error path silenced). That gap would have halted hypothesis work (static verdict insufficient), but an external `bash -x` trace with timestamps captured at the invocation site before the audit supplied the missing where-and-why, so the verdict was recomputed to partial and no hard-stop fired (a reading of the recompute-after-observation clause by the orchestrator, not an automatic result).

(Full card: /home/coder/workspaces/IronClaude/.dev/troubleshoot/performance-ccsession-launch-takes-20-seconds-20261117185300/diagnosability-context.md)
(Tasklist (informational): /home/coder/workspaces/IronClaude/.dev/troubleshoot/performance-ccsession-launch-takes-20-seconds-20261117185300/diagnosability-tasklist.md)

## Diagnosis

**Root cause**: `list_sessions` (installed ccsession I:1554-1663) runs about 13 external processes plus a head/tail/grep/awk transcript scan for each of 477 saved names, and `local ... LC_ALL=C` at I:1383 and I:1403 never reaches `grep`, so the scan runs in the UTF-8 locale and takes about twice as long; `ccsession --ask` runs this whole list before the 30 s question.

**Cause class**: Performance/resource (N+1 process spawning, plus an environment variable that never reaches the child process)

**Detailed explanation**: Per-function self time of the 27.08 s trace: session_home 12.16 s, loop body 5.12 s, format_epoch 2.68 s, session_transcript 2.03 s, session_place 1.95 s, get_btime and get_mtime 2.42 s. Reading the two ends of the 439 transcripts takes 1.442 s; the full pipeline takes 13.227 s in the shell's UTF-8 locale and 6.460 s with `LC_ALL=C`, and alternating end-to-end runs show 22.5-24.7 s plain against 16.2-16.7 s with `LC_ALL=C` exported (median gap 6.99 s). A one-process prototype of the same index and scan took 0.75 s. Three independent specialist cards and the Tier 1 card agree on this diagnosis (calibrated 0.83, 0.83, 0.83, 0.83; the performance-engineer card 0.50 after a structural cap, see Grounding Gaps). The 5-10% CPU figure is not explained: 19.4 s CPU over 27.1 s wall is about 0.7 of one core, about 2.5% of this machine.

## Evidence

1. `/home/coder/.claude/skills/ccsession-tag/ccsession:1383` — `local store want cwd first="" LC_ALL=C` (and `:1403` — `local b LC_ALL=C`); a bash probe `bash -c 'f() { local x LC_ALL=C; env | grep -c "^LC_ALL="; }; f'` printed 0, so the value is not exported to `grep`.
2. `/home/coder/.claude/skills/ccsession-tag/ccsession:1396` — `done < <({ head -c 262144 "$1"; echo; tail -c 1048576 "$1"; } 2>/dev/null |` and `:1397` — `grep -oE '"cwd":"([^"\\]|\\.)*"' | awk '!seen[$0]++')`: one pipeline per session.
3. `/home/coder/.claude/skills/ccsession-tag/ccsession:1482` — `ls -t "$PROJECTS_DIR"/*/"$1".jsonl 2>/dev/null | head -n 1 || true`, called per row from `:1599` — `jsonl=$(session_transcript "$uuid")`.
4. `/home/coder/.claude/skills/ccsession-tag/ccsession:1535` — `date -r "$epoch" '+%Y-%m-%d %H:%M' 2>/dev/null \` and `:1536` — `|| date -d "@$epoch" '+%Y-%m-%d %H:%M' 2>/dev/null`; GNU `date -r 1794941650 '+%Y-%m-%d %H:%M'` printed `date: 1794941650: No such file or directory`, exit 1 (tier1-observation.md, "Primitive behaviour observed in this run").
5. `/home/coder/.claude/skills/ccsession-tag/ccsession:1610` — `start_ts=$(get_btime "$jsonl")` and `:1611` — `last_ts=$(get_mtime "$jsonl")`, `:1616` — `start_str=$(format_epoch "$start_ts")`, `:1617` — `last_str=$(format_epoch "$last_ts")`: per-row command substitutions (subshells).
6. `/home/coder/.claude/skills/ccsession-tag/ccsession:1718` — `sessions=$(LIST_NAME_ON="$accent" LIST_DETAIL_ON="$dim" LIST_OFF="$reset" \`: the list is captured whole, nothing prints until it is built.
7. `/home/coder/.claude/skills/ccsession-tag/ccsession-orca:204` — `answer=$("$CCSESSION" --ask "$hint") || rc=$?`: the launch route into the list.
8. `/home/coder/.claude/skills/ccsession-tag/ccsession:1733` — `# Every question gives up after CCSESSION_ASK_TIMEOUT seconds (default 30;` with `:1735` — `# within 60 seconds, and an unanswered question must not outlast that.`
9. Command: `time ccsession --here` → real 27.069 s, user 5.823 s, sys 13.566 s, 405 output lines; `time ccsession --list` → real 14.473 s (tier1-observation.md, "Wall-clock").
10. Command: `PS4='+T ${EPOCHREALTIME} ${FUNCNAME[0]:-main} ' bash -x ~/.local/bin/ccsession --here` → self time session_home 12.16 s, list_sessions loop 5.12 s, format_epoch 2.68 s, session_transcript 2.03 s, session_place 1.95 s, get_btime 1.22 s, get_mtime 1.20 s; 1756 `date`, 972 `head`, 936 `dirname`, 936 `basename`, 878 `stat`, 477 `ls`, 448 `grep` (tier1-observation.md, "bash -x trace of `ccsession --here`"; the full command, with its `>/dev/null 2>/tmp/ccs-xtrace.log` redirection, is Task 1 of diagnosability-tasklist.md).
11. Command: the head/tail-only loop, the C-locale pipeline and the shell-locale pipeline over the 439 transcripts → 1.442 s, 6.460 s, 13.227 s (tier1-observation.md, "Falsification probe run by the parent").
12. Command: six alternating runs of `ccsession --here` plain vs `env LC_ALL=C` → plain 23.586, 24.663, 22.471 s; `LC_ALL=C` 16.657, 16.244, 16.597 s; median gap 6.99 s (locale-probe.txt, tier1-observation.md "End-to-end locale probe").
13. Command: one-process prototype of the uuid index plus head 256 KiB and tail 1 MiB scan → 0.75 s total for 439 sessions, 554 MB read (tier1-observation.md, "Prototype").

## Proposed Fix

The full corrected remediation (stages, tests, success measure, gates, risks) is in `/home/coder/workspaces/IronClaude/.dev/troubleshoot/performance-ccsession-launch-takes-20-seconds-20261117185300/remediation-plan.md` and is posted into issue #607. In short:

**Files to change**:
- `src/superclaude/skills/ccsession-tag/ccsession` — Stage 1: `LC_ALL=C` prefix on grep and awk in session_home and session_branch; build the transcript index, the `date` flavour probe and caches in the parent shell before the row loop, not inside `$(...)`; one `stat -c '%W %Y'` per row; parameter expansion instead of basename, dirname and `head -n 1`; `date -d` first on GNU; Stage 2: call a python3 helper once per list with Stage 1 as the fallback
- `src/superclaude/skills/ccsession-tag/scan_sessions.py` (new, Stage 2) — one-pass index and head/tail cwd scan, one record per uuid in input order
- `tests/unit/test_ccsession_tag.py` — spawn-count, locale-shim, parity, date-probe, `set -e` and boundary fixtures through the real entry points

**Test to verify**:
- all existing `_listed` tests and tests at 4474, 4522, 4551, 4585, 3465, 2740 pass unchanged
- add new tests: spawn count does not grow with N=10 vs N=60; `grep` sees `LC_ALL=C`; helper vs python3-hidden parity is byte-identical; no file written while listing

**Apply with**: `/sc:workflow` on the remediation section of issue #607, then `/sc:implement <printed plan path>` (a written plan is required: more than one source file changes); the Tier 3 offer of this run was replaced by the issue edit the user asked for.

## Alternative Fixes Considered

- **Fix 1 — one python3 batch helper with a locale-fixed bash fallback, shipped as one change** (from the Tier 1 card and the root-cause-analyst card)
  - Rejected because: lost on staging (a helper defect would block the already measured locale win) and was judged by the debate to have a thinner helper specification; its helper design is kept as Stage 2.
- **Fix 2 — bash only: real C locale and builtins, no helper** (from the performance-engineer card)
  - Rejected because: the per-file `head | tail | grep | awk` scan keeps 6.46 s (Arm 2) against the helper's 0.75 s; it also proposed `printf '%(...)T'` (unavailable on bash 3.2) and a `-nt` glob whose tie-break against `ls -t` is unverified. Its two-file Stage 1 shape and the invalid-UTF-8 note were kept.
- **Bound the list to the N newest rows; disk cache; parallel jobs** (considered by the specialists)
  - Rejected because: they change the output contract or break "Listing never writes any file" (README:190).

## Risk + Rollback

- **Likelihood of regression**: medium in the cwd/here-gone-other classification if the Stage 2 helper drifts from the pinned rule; low for Stage 1.
- **Test coverage of the changed code**: partial today (the pinned-format tests exist; no test counts process spawns or runs under bash 3.2); the plan adds the missing tests.
- **Rollback**: Stage 1 and Stage 2 are separate changes; `git revert` of either restores the previous behaviour, and Stage 2 falls back to Stage 1 when python3 or the helper fails.

## Follow-up tasks

- Printing rows as they are built, or starting the 30 s question clock earlier, would change the `show_saved` contract (`Suggested type`: `refactor`; evidence: `ccsession:1718`).
- A hook that records each session's start folder at session start would remove the transcript scan (`Suggested type`: `refactor`; needs a migration for existing sessions).
- `src/superclaude/agents/troubleshoot-analyst.md` lacks the `mcp__litellm__augment_code-augment_code_search` tool that the installed protocol lists in its closed roster (`Suggested type`: `bug`).
- Ask the reporter for core count and store size to explain the 5-10% CPU (`Suggested type`: `observability`).

## Grounding Gaps

- The reported 5-10% CPU is not reproduced (measured about 2.5% of a 28-core machine); whether the reporter's locale and store size match this machine is unverified (gate A-001).
- All timings and the 0.75 s prototype ran warm; cold-cache cost is not measured (gate A-002). The per-spawn proxy for dirname, basename and head is not measured (gate A-004).
- Wave 4 self-review verdict FAIL: one blocking finding (F1, caches in `$(...)` subshells are lost) is corrected in remediation-plan.md, which was not independently re-reviewed; seven non-blocking findings (F2-F8) are folded into the same text.
- The performance-engineer card was calibrated 0.50 because the calibrator fired a structural cap (C7) for environment mentions without a 2x2 row; the two other Tier 2 calibrators did not fire it for similar mentions; the value was kept as returned and its card is the outlier in weighting.
- The analyst profile in the project `.claude/agents/troubleshoot-analyst.md` declares a strict subset of the protocol's closed roster (no litellm augment tool); it was used with that recorded deviation, and the parent ran the augment search itself.
- The checkout (`docs/409-orca-dashboard-designs`) holds an older ccsession (1902 lines) than origin/master (2072 lines); all line citations use the installed copy, which was verified byte-identical to origin/master 10f6ec670 (ccsession unchanged through e3e9d636a).
- The diagnosability hard-stop was not applied because an external trace supplied the evidence; that is the orchestrator's reading of the recompute-after-observation clause.
- Not read: the Coder New Terminal hook, `ensure_names_migrated` before line 505, the plugins/superclaude mirror, the bodies of most pinned tests; no test or run was made under bash 3.2 or macOS.
- The first computed DC metric for the staged proposal (0.400) came from a definition-detection rule that was corrected and re-run once; both values are in base-selection.md and the selection is unchanged.

## Next Steps

- Pending tasklist rows (diagnosability-tasklist.md): Task 2 (optional) `strace -f -c -o /tmp/ccs-strace.txt ~/.local/bin/ccsession --here` to corroborate the process-creation share (sys time was 13.6 s of 19.4 s CPU); Task 3 re-measure with the Task 1 trace and `time ccsession --here` / `--list` after the fix and compare with 27.069 s and 14.473 s.
- Apply the remediation through `/sc:workflow` on issue #607 (Stage 1 first, then Stage 2), read its plan and pre-execution review, then `/sc:implement <printed plan path>`; run `/sc:reflect --mode post` before committing.
- Because the Wave 4 review failed on a blocking point, let `/sc:workflow`'s own `/sc:reflect --mode pre` re-review the corrected plan before any code is written.

## Audit

- **Hypothesis cards**: /home/coder/workspaces/IronClaude/.dev/troubleshoot/performance-ccsession-launch-takes-20-seconds-20261117185300/tier1-hypothesis.md, tier2-performance-engineer-hypothesis.md, tier2-root-cause-analyst-hypothesis.md, tier2-system-architect-hypothesis.md (same folder)
- **Adversarial artifacts** (Tier 2 only): /home/coder/workspaces/IronClaude/.dev/troubleshoot/performance-ccsession-launch-takes-20-seconds-20261117185300/adversarial/adversarial (merged plan: ../merged-output.md; convergence 94.7%, base Variant 3)
- **Self-review** (Tier 2 only): FAIL, one blocking finding (F1), seven non-blocking (F2-F8): /home/coder/workspaces/IronClaude/.dev/troubleshoot/performance-ccsession-launch-takes-20-seconds-20261117185300/self-review.md
- **Task file** (Tier 3 only): not built (the user asked for the remediation to be posted into the issue; Tier 3 was redirected, not run)
- **Audit log**: /home/coder/workspaces/IronClaude/.dev/troubleshoot/performance-ccsession-launch-takes-20-seconds-20261117185300/audit.log

## Pipeline Hardening Closure

Pipeline hardening not applicable: the diagnosed defect is wall time inside one process's list building, not a pipeline escape. Boundary scan (HC0), typed rows:

| boundary_type | producer / transformers / consumer | evidence_source | risk | decision | rationale |
|---|---|---|---|---|---|
| CLI/subprocess | `ccsession --ask` stdout and exit code / `show_saved` / `ccsession-orca` (`ccsession-orca:204`) | ccsession-orca:204; ccsession:1715-1735 | the fix adds a python3 subprocess in Stage 2 | not_applicable | the diagnosed defect is speed, the stdout/stderr and exit-code contract is unchanged and pinned by existing tests, and no proof substitution is possible; the remediation requires its tests to run through `ccsession --here`, `--list` and `--ask`, not the helper alone |
| gate-status-enum, generated-artifact-parser, persisted-state, review-selector, sibling-pipeline, duplicate-evaluator, prior-escape-unmask, file-stdin-prompt | none in the data path of the symptom | listing code ccsession:1554-1663 | none | not_applicable | no gate or severity enum, no parsed generated artifact, no persisted or resumed state, no review selector, no sibling pipeline and no earlier escape is involved |

**Applicable**: false (see note below)
**Closure verdict**: not_applicable
**Waiver status**: none
**Backtest status**: not_run
**Off-path review**: not_required

Note: the protocol's first bullet sets applicable=true when an issue touches any trigger boundary, including CLI/subprocess; this run decided `not_applicable` on the rationale above because the issue is not an escape, and it records that reading here.
