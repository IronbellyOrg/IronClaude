# Reflect Reviewer: Deviation Findings

**Reviewer persona**: analyzer (root cause and correctness of production logic)
**Grounding root**: `/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher`
**Diff scope**: `e8db2fe6...26f551f4` (single commit, parent equals base)
**Timestamp**: 2026-11-08
**Total deviations**: 12 rows below, 0 HIGH, 1 MEDIUM, 11 LOW

Headline: I found no path to a second launch for one issue, no issue text reaching the prompt, audit or store, and no GitHub write or shell use. The only MEDIUM item is the exit-code and reason-table drift (rows 1 and 2).

I read these in full: `cycle.py`, `record.py`, `predicates.py`, `github.py`, `launch.py`, `runner.py`, `audit.py` and `cli.py`. I also read design sections 4.3, 6, 7.3-7.6, 8.2-8.5 and 9.

## Deviations

| # | Category | Location | What diverged | Evidence (file:line) | Severity |
|---|----------|----------|---------------|----------------------|----------|
| 1 | Necessary deviation | `audit.py:57,64`; `cycle.py:1134-1137`; `cli.py:35,123-129` | `cycle_complete` (exit 0) and `cycle_crashed` (exit 1) were added. A closed reason table has no name for a normal cycle line or a crash, so some name was unavoidable. I confirm the card's category. | `audit.py:55-64` and `cli.py:35,124-129` carry `[PROPOSAL]` comments. `cli.py:127-129` prints only the exception class name, so no issue text leaks. Design 4.3 lists no exit 1 for `once` (brief D:114). | MEDIUM |
| 2 | Drift | `docs/designs/issue-watcher.md` section 4.3; spec reason list (52 names) | The names were never added to the design or the spec. Spec has 52 names, code has 59, the runbook documents 59 (setup.md:318,331,344), and the design is silent. `once` can now exit 1, which section 4.3 does not list. Literal AC-17 ("exit codes match section 4") is arguably contradicted for exit 1. No owner decision authorizes it. | `cli.py:35,127-129`; `audit.py:55-64`; brief row C4b | MEDIUM |
| 3 | Drift | `cycle.py:635-641` (`_issue_line`), `audit.py:94` | The `re-approved` note branch is unreachable. `_approve` only runs for entries that are None, `failed`, or an attempts-exhausted tombstone, and none of these carries an approval event id. OQ-49 says "adds no code for it", so the omission is authorized but the dead branch is not. | `cycle.py:635-641`; `cycle.py:859-875` (`_approve`); brief C4c (OQ-49 text not read by me) | LOW |
| 4 | Drift | `cli.py:319` (via `cycle.format_utc`) | `cli` reaches `predicates.format_utc` through the `cycle` namespace. Design section 5.3 gives `cli` no predicates import. The AST boundary test only sees import statements. The task log discloses it as a "judgment call" but does not authorize it. | `cli.py:26,319`; brief C2 | LOW |
| 5 | Drift | `predicates.py:20,54`; `launch.py:30,90`; `audit.py:203,236`; `record.py:132` | The 999_999_999 issue-number bound is encoded in three named copies plus digit-count patterns. Only the audit copy is pinned by a test. The login regex is duplicated (`cycle.py:468`, `github.py:134`) with no parity test. I confirmed the two OPERATION_ID copies agree today (`predicates.py:57`). | brief C3b (re-read in part) | LOW |
| 6 | Drift (alternative reading: NFR-014 regression, behaviour-neutral) | `audit.py:381-404` (`stderr_fallback` reads the wall clock when `ts` is None); `runner.py` monotonic reads | NFR-014 says every time read goes through the Clock. These reads feed a stamp and a duration, not a decision. `cli.py:79,127,219` call the fallback without a `ts`. `cli.py` could pass `cycle.SystemClock().now()`, as `reset` already does at `cli.py:317-319`. | `audit.py:381-404`; `cli.py:79,127,219,266`; brief C6 | LOW |
| 7 | Necessary deviation | `predicates.py:57` and `launch.py:36` | `OPERATION_ID_PATTERN` exists twice because `record` may import only predicates and `launch` may import only runner. `LaunchOutcome.__post_init__` re-checks the id (`launch.py:251-259`). Fail-closed in both directions. | `predicates.py:57`; `launch.py:272,332` | LOW |
| 8 | Authorized expansion | `record.py:23-29` | `record` imports three predicate functions where design section 5.3 says "types only". The task list (Step 4.1a, PRE-11) records and permits it. The design text was never amended. | brief C1a (TL:332, TL:998) | LOW |
| 9 | Necessary deviation | `record.py:183,585,607`; `predicates.py:57-67` | A fourth predicate function, `valid_operation_id`, was added. The status command prints the stored id inside a shell command line, so the store must validate it. B-10 calls this "within design 5.3", which is wrong for a function import. | brief C1b; `launch.py:332` | LOW |
| 10 | Authorized expansion | `audit.py:81,82,98,99,101` | Five reason names beyond the spec's 52. DF-02, DF-03, DF-22 and DF-57 authorize them. | brief C4a (decision register not read by me) | LOW |
| 11 | Authorized expansion | `cycle.py:1010-1016`, `cycle.py:644-649,738-742`, `cycle.py:814-815`; `launch.py:119-132,343-355`; `runner.py:70-72` | Seven departures, each with an anchor: dry-run skips the re-read and the Orca probe (D:362); Retry-After is honoured only on the user call (DF-51, D:598-602); full retry argv (DF-50); any launch-step outcome halts the cycle (D:386-388); the launch runs with `cwd=worktree` and `run` gained a `cwd` argument (DF-01). I read the code for each and it matches the anchors. I did not read DF-xx text itself. | `cycle.py:814-815` is the halt flag I traced; `launch.py:311-334` | LOW |
| 12 | Necessary deviation | `test_cli.py:967,1070`, `test_record.py:739`, `test_cycle.py:735,4694` | Tests use skip or skipif although the plan forbids SKIP. Disclosed in the task log. I did not read the tests. | brief C5 | LOW |

## Adherence summary

- Spec units audited: 38 (FR-001 to FR-029, plus 9 safety-property groups). This is an estimate: I did not map each row to a single FR id.
- Fully adherent: about 30 (estimate, same caveat)
- Authorized expansion: 3 | Necessary deviation: 4 | Drift: 5 | Regression: 0

## Notes

- **Tier-1 claims in my area**
  - I confirm C1a, C1b, C2, C3a, C3b, C4a, C4b, C4c, C6, C8a-g and the A-series items below, with the line numbers I read.
  - I did not verify C5 and C7 (they depend on tests and the task file), C9, C10, A11 or A12.
- **At-most-once launch**
  - `mark_pending` at `cycle.py:335` and `_save()` at `cycle.py:336` run before `launcher.launch` at `cycle.py:337`.
  - A failed save raises `_Stop` before the spawn.
  - Sweep, `abandoned`-with-`pending_at`, lease expiry and `unknown` all route through the marker check. None of them relaunches.
- **Prompt and issue text**
  - `launch_argv` guards with `PROMPT_PATTERN.fullmatch` and has 12 elements.
  - The body is reduced to a jq boolean, and audit lines use the closed schema.
- **Windows**
  - Day cap (now-24h, now], backoff 10 min, lease 60 min and marker window (at or after pending_at minus 300 s, else strictly after approved_at) match design 7.5.
  - `_in_window` and `day_cap_count` are half-open as specified.
- **Not read, so unverifiable by me**
  - spec-final.md.
  - The decision register `06-gap-fill-decisions.md`, so DF-01, DF-02, DF-03, DF-22, DF-50, DF-51 and DF-57 rest on the card's citations.
  - Tasklist OQ-1..OQ-51 text.
  - The tests, and the setup runbook beyond the card's line numbers.
  - `__init__.py`, `main.py` and `swarm/atomic.py`.
  - Design sections not listed in the header.
- `rg` returned EACCES during this pass, so I used codegraph and the other read tools instead.

## Correctness gaps (advisory, non-gating)

| # | Correctness gap | Location | Sibling disagreement | Evidence (file:line) |
|---|-----------------|----------|----------------------|----------------------|
| 1 | Day cap fails open after a backward clock step. `consumed_at` later than `now` is not counted, so the cap of 6 can be exceeded. This is design-conformant (D:500,505) and only warns (`cycle.py:755-756`). Backoff, lease and next-permitted all fail closed on skew. Possibly MEDIUM in impact (inferred). | `record.py:689-703` | Other time windows fail closed | `record.py:689-703`; `cycle.py:755-756` |
| 2 | `disabled()` treats a dangling-symlink DISABLED as present, but `disabled_since()` uses `os.stat`, which follows the link. The kill switch stops cycles while `status` prints "disabled since: no". Any OSError other than FileNotFoundError escapes `status_report`. | `record.py:423,425-431`; `cycle.py:1255` | `disabled` and `disabled_since` disagree | `record.py:423` vs `425-431` |
| 3 | DISABLED is checked once at `cycle.py:308`, then the origin git call (up to 10 s) and a durable pending write run before the spawn. A `touch DISABLED` in that window is not honoured, and a re-check before `mark_pending` would leave no pending entry. The design order (D:355) allows it. | `cycle.py:308,335-337` | Kill switch vs origin call | `cycle.py:308,335` |
| 4 | Any exception other than `_Stop` after the spawn skips `_commit`. `_locked_body` catches only `_Stop`. The entry stays `pending` and is swept to `pending_orphan`. The operation id and retry hint are lost, and no audit line is written. At-most-once still holds. | `cycle.py:685-690`; `cli.py:121-129` | `_locked_body` vs `once` crash path | `cycle.py:685-690`; `cli.py:123-129` |
| 5 | A process holding the pipes after the Orca launch exits would block `communicate()` until the 120 s timeout. Every successful launch would then become `unknown`. A PATH stub exits at once, so tests cannot show it. Inferred, not verified. | `runner.py:91-101,125-126` | Stubs vs real Orca | `runner.py:15,126`; `launch.py:320-321` |
| 6 | Dead code: `MAX_LAUNCHES_PER_CYCLE` (never used), `record.disabled_present`, `status_report`'s unused audit argument, `CommandResult.duration_s`. | `cycle.py:35`; `record.py:748`; `cycle.py:1235,1244`; `cli.py:173`; `runner.py:35` | Declared but unused | same |
| 7 | `mark_pending` checks state only, not `launches == 0`. The spec (S:272) says a fresh launch requires `launches == 0`. It is safe today because `validate` rejects `failed` with `launches` 1 (`record.py:208`). | `record.py:538-568` | `mark_pending` vs `validate` | `record.py:208,538-568` |
| 8 | Same-second trigger and approval label events are detected across the whole label history. An issue where a human sets both in one `gh issue edit` stays `events_incomplete` forever, and re-applying the label does not clear it. The spec words it that way (S:92) but the documented re-arm (S:94) does not rescue this case. | `predicates.py:205-209` | Rule vs re-arm | `predicates.py:205-209` |
| 9 | Any `OSError` after the spawn is classified by `outcome_of` as `spawn_error` (no id, `launches` stays 0 on the failed branch), even though a real process may have started. The spec distinguishes this only by `spawn_error is not None`, so I flag it for triage only. | `launch.py:318-319`; `runner.py` (OSError and ValueError mapping) | Spawn-error vs started | `launch.py:318-319` |
| 10 | An exit-0 reply that carries `error.operation_id` is accepted as `launched`, because `_first_hit` looks at error paths too. | `launch.py:326-334` | `_first_hit` vs exit code | `launch.py:326-334` |
| 11 | The stored id pattern `^[A-Za-z0-9._:-]{1,128}$` allows a leading `-`. The status command prints the id into a shell command line, so a leading dash could be read as an option. | `predicates.py:57` | Id pattern vs shell use | `predicates.py:57` |
| 12 | Stderr is capped at 500 bytes, but the `agent_session_operation_unknown` text is searched in both streams at `launch.py:322`. A long stderr could push the marker past the cap and turn an `unknown` into `launched`. Stdout is uncapped. Inferred, not verified. | `runner.py:15,58-63`; `launch.py:322` | Cap vs search | `runner.py:15,63`; `launch.py:322` |
| 13 | The approvers file is the allow-list. `lstat` checks owner and mode, then `open` uses `O_NOFOLLOW` with no `fstat` on the descriptor. The parent directory mode is not checked. Exploiting it needs write access to the parent directory. Card finding; I read the surrounding code but did not confirm the `fstat` gap line by line. | `cycle.py:307-324` | `lstat` vs `open` | brief A7 |

## Blind calibration (attached by the orchestrator; full report: reviewer-1-calibration.md)

- Reviewer model class: sonnet (persona analyzer). Calibrator class: opus (calibrator_diversity degraded: no class disjoint from the three reviewers exists in this environment).
- Calibrated confidence C = 0.70 (citation grounding 0.72, coverage completeness 0.68, deviation-classification clarity 0.75, risk surface 0.85, recommendation actionability 0.50). C < 0.85.
- Citation spot-check: 27 of 29 groups match. Two do not: the at-most-once note cites cycle.py:335-337 but mark_pending, _save and launch are at cycle.py:1060-1062; correctness gap 3 cites cycle.py:308 and "checked once" but DISABLED is checked at cycle.py:693 and again at 1033-1034, the unprotected window is 1033 to 1060 (second origin git call 1041-1045). The header count "1 MEDIUM, 11 LOW" contradicts the table (rows 1 and 2 are both MEDIUM).
- The card has no recommendations section.
