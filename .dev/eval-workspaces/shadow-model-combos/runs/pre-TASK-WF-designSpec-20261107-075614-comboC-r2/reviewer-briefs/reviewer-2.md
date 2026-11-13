# Reviewer 2 brief (persona: qa)

Task: audit the PLAN against its driving SPEC before any execution (UC-1 pre-execution reflection). Find where the plan contradicts the spec, omits a spec requirement, or carries an acceptance criterion that cannot fail or cannot pass. Audit only the evidence supplied here plus what you can Read, Grep or Glob. Return your card as text; do not edit anything.

Plan: .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md
Spec: .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md

## T1 card excerpt

Orchestrator Tier 1 card (verbatim lines, persona slice). Full card: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/eval-workspaces/shadow-model-combos/runs/pre-TASK-WF-designSpec-20261107-075614-comboC-r2/t1-card.md

# Tier 1 reflection card (UC-1, pre-execution)

Spec: `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md` (378 lines, design spec v3 for the pr-submit merge guard).
Plan: `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md` (200 lines, 13 tasks, 5 phases).

## Coverage (Step 1B)
Pass 1 (ID regex) found 0 parsed ids in either file (the spec labels requirements FR-n, F-n, G-n, O-n, which the regex does not match). Pass 2 inferred 86 quote-pinned rows, 2 dropped at emission for a non-verbatim quote, 84 kept. Deterministic containment match: 70 of 84 mapped (`coverage_pct_union` 0.8333), 14 unmapped. `coverage_degraded: parsed-sparse` (inferred 84 > parsed 0), so no Tier 1 stop is allowed. Most of the 14 unmapped rows are lexical misses (the plan carries the idea in other words), see the matrix `artifacts/coverage-matrix.json`. `S_dev_density` = 14/84 = 0.1667.
- **T1-F2 (MAJOR, missing-requirement).** The FR-16 retry (spec line 315: "one retry, `already_in_state` counts as confirmed, `release_pending`") has no decision-table row, no fold rule and no acceptance criterion. Task 8 puts "one retry" into the ref prose (plan line 124), and Task 11 only names `test_guard_release_failure_retries_once_and_reports` (plan line 169).
- **T1-F3 (MAJOR, missing-requirement).** No criterion checks that the guard, the push triad and `rereview_requested` share one `cycle_id` (spec line 251). Task 11's trace asserts event order only (plan line 170) and Task 8 only requires the ref to name the minting place (plan line 127).
- **T1-F4 (MAJOR, unpassable-check).** Task 7's criteria check that `--read` prints the keys, not their values (plan line 111). Spec line 230 shows `"autoMergeRequest":false` and a `transitions` count made with `wc -l`, while `gh pr view --json autoMergeRequest` returns an object or null, so the boolean needs a conversion that no criterion tests.
- **T1-F7 (MINOR, other).** Task 11's first criterion passes once the 12 test names exist (plan line 169). The case list has no moved-head scenario although the test name says "moved_head" (spec line 319).

End your card with a ## Findings block holding one fenced findings-v2 block: JSON lines, one object per line, never a table. Fields: id (F1, F2, ...), severity (CRITICAL, MAJOR or MINOR), blocking (true or false; a MINOR finding is never blocking), category (one of contradiction, data-loss, missing-requirement, other, safety, unpassable-check), lens "reflect-pre", claim (one line, at most 300 characters), refs (requirement ids, may be empty) and citations (1 to 8 objects, each with role plan or spec, a repo-relative path, line_start, line_end and an optional quote). Example line: {"id":"F1","severity":"MAJOR","blocking":false,"category":"contradiction","lens":"reflect-pre","claim":"Task 3 says X but task 5 says Y.","refs":["R-1"],"citations":[{"role":"plan","path":"plan.md","line_start":10,"line_end":12}]}. After the block add a reviewer_model_self_report line stating the model you are running as in one line.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-13T04:06:00Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

Audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding.

### .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:1-378

```markdown
# Design Spec: pr-submit merge guard (issue #375)

- Type: component design, format spec
- Input requirements: `.dev/brainstorms/20261107-062111-pr-submit-draft-guard/merged-requirements.md` (FR-1..FR-23, decisions D1..D7)
- Issue: https://github.com/IronbellyOrg/IronClaude/issues/375
- Owner decisions (accepted 2026-11-07, relayed by the coordinator): draft not label; engage at the first verified Medium-or-higher finding routed to a fix; default on at `--monitor 3` via `--merge-guard {draft,off}`; release when the fix push is confirmed on the PR head, before replies and the re-trigger; an unreadable timeline or an exit with unpublished fixes keeps the PR draft and reports.
- Status: design only. No source file is changed by this document.
- Revision: v2 (2026-11-07), after the advisory review of the first plan built from v1 (three reviewers, all not-ready). Changes: Wave 0 resume and `off` hooks; fold rows for `not_applied` and a retried draft; `guard_status` mapping; resume row 2 precedence and the three `RECONCILE` reasons; per-cycle `applied_edits`; `refs/loop-guard.md` enumeration; sync cadence; owner decision on the release gate; section 10 plan authoring notes. The v1 text is preserved in the superseded plan package's `source.md`.
- Revision: v3 (2026-11-07), after the advisory review of the second plan (three reviewers, all not-ready; reflect report `.dev/reflect/pre-designSpec-20261107074409/REPORT.md`). Changes: the pinned write-verb classification table (F12, section 4.7); the L2 report line moves into the always-loaded SKILL.md output table; resume recognises a normal completed push (`published`, `held_cycle_published`) and uses the real recovery branch strings (F13); the fold returns a settled `not_applied` request of either direction to the phase before the request; plan authoring notes for the low-severity items. The v2 text is preserved in the second superseded plan package's `source.md`.

## 1. Facts this design rests on

Read from the repository on 2026-11-07 (master `e8db2fe6`), or from the named documentation.

| # | Fact | Source |
|---|---|---|
| F1 | `EventType` is a closed enum of exactly 43 members; `RunLog.append` rejects anything else. | `pr_submit/models.py:24`, `run_log.py:117-125` |
| F2 | `rebuild_state()` folds the JSONL; new keys are seeded in the `state` dict (`open_conflict_cycle: None` idiom) and a test pins the exact key set. | `run_log.py:205-224`, `tests/pr_submit/test_run_log.py:312,403-404` |
| F3 | Crash matching is push-only: `detect_crash_window` pairs `push_initiated` with `push_completed` or `push_aborted_or_not_landed` by `idempotency_key`. | `recovery.py:69-92` |
| F4 | The only minted cycle ids are conflict ids (`sync-<n>`, `conflict-<n>`, prefixes reserved in `CONFLICT_CYCLE_PREFIXES`). Nothing in code or protocol text mints a fix-cycle or CI-cycle id; the text only says it never starts with `sync-` or `conflict-`. | `conflicts.py:46,1208-1244`, `refs/loop-guard.md:119-120` |
| F5 | `--conflict-max-tier` is the one enum flag of this parser (`choices=`); `parse_args` builds `SkillArgs` only. `RunConfig` has no flag mapping and models seams, not flags. | `fsm.py:103-109,132-146,900-943` |
| F6 | The core-purity test rejects the whole words `gh` and `git` on any line of each core file. | `tests/pr_submit/test_static_grep.py:134-146` |
| F7 | Every `gh` line in a protocol script or ref must be repo-scoped (`--repo`, or a `gh api repos/...` path). | `test_static_grep.py:105-123` |
| F8 | `gh pr ready <N> --repo R --undo` converts to draft "if supported by your plan"; the docs do not say what happens if the PR is already in the target state. `gh pr view --json` offers `isDraft`, `state`, `headRefOid`, `autoMergeRequest` (gh 2.103.3 here). | `gh pr ready --help`, `gh pr view --json`, cli.github.com manual |
| F9 | GitHub documents timeline event types `convert_to_draft` and `ready_for_review`, each with `actor` and `created_at`. Pagination of the timeline endpoint is not stated in the pages read; `gh api --paginate` covers it. | docs.github.com issue-event-types |
| F10 | Wave 3 turns unverified findings into REPORT_ONLY; Wave 4 diagnoses; edits start only in Wave 4 at L2+; Wave 6 (L3) commits, runs the pre-push head guard, then the push triad, then reply, resolve and the S5a re-trigger. | `SKILL.md:279-282` |
| F11 | One GitHub login (`ironbelly`) is used by the human and the agent, so no actor-based test can tell them apart. | `gh auth status` in this session |
| F12 | `tests/skills/test_worker_contract.py` scans every file under `src/superclaude/{skills,commands,agents}` (scripts included) for `gh pr`, `gh api` and the git write verbs (`WRITE_VERB_RE`); every hit must be a key of `WRITE_VERB_CLASSIFICATION`, keyed by the exact path, the verb text and the exact stripped line, with a category and a one-line reason. `test_every_write_verb_hit_is_classified` fails on an unclassified hit and `test_classification_table_has_no_stale_entries` fails when a classified line no longer exists, so editing a classified line breaks the table. The existing pr-submit entries use category `never-worker` with the standard reason text. | `test_worker_contract.py`: `AUDIT_ROOTS`, `WRITE_VERB_RE`, `WRITE_VERB_CLASSIFICATION`, `test_every_write_verb_hit_is_classified`, `test_classification_table_has_no_stale_entries` |
| F13 | Crash recovery returns the strings `landed`, `not_landed` and `ambiguous` (`BRANCH_A_LANDED`, `BRANCH_B_NOT_LANDED`, `BRANCH_C_AMBIGUOUS`). `detect_crash_window` returns only a `push_initiated` with no later `push_completed`, so after a normal `push_completed` it returns `None` and no branch is produced. `recovery.py` imports `run_log`, which will import `merge_guard`, so `merge_guard.py` cannot import `recovery`. | `recovery.py`: `BRANCH_*` constants, `detect_crash_window`, `resolve_crash_window` |

Corrections to the merged requirements, found while grounding them: (a) the flag needs no `RunConfig` field (F5); (b) the cycle key `(kind, round_counter, ci_attempt)` does not exist in code, so section 4.6 defines it (F4); (c) `recovery.py` cannot be reused for the guard's pairs, so section 4.2 adds a guard matcher (F3).

## 2. Component overview

```text
 SKILL.md waves (impure, orchestrates)            pure core (no gh/git words)
 ---------------------------------------          --------------------------------
 Wave 3 end ──► refs/merge-guard.md §Engage ──┐    merge_guard.py
 Wave 6 ───────► §Pre-push + §Release ────────┤      GuardMode, Phase, Direction
 Wave 8 CI push ► §Release ───────────────────┤      GuardAction, GuardRead, GuardDecision
 every exit ───► §Report ─────────────────────┤      fix_cycle_id, next_cycle_number
 --resume ─────► §Resume ─────────────────────┘      fold_draft_guard, pending_requests
        │  1 read   2 decide   3 request(fsync)       classify_toggles
        │  4 mutate 5 settle                          engage_/release_/resume_decision
        ▼                                             guard_status
 scripts/set-draft-state.sh  (all GitHub I/O)       models.py  +2 EventType members (45)
   --read | --to draft|ready                         run_log.py rebuild_state()["draft_guard"]
                                                      fsm.py     --merge-guard, SkillArgs.merge_guard
```

Rule: the core DECIDES and the SKILL performs, the same split as the push triad and the re-trigger (NFR-6). No new `MonitorState`.

## 3. Behaviour in one table

| Moment | Guard action |
|---|---|
| Ordinal < 3, `--merge-guard off`, or a conflict-merge cycle | Nothing mutates. A held guard found in the log is reported with the clear command. |
| `--resume` at any ordinal and in either mode, or a run log that already holds guard events | Wave 0 loads the ref (Resume and Exit report) before Wave 1: unsettled requests are reconciled before any edit, release or re-trigger; a held guard is reported with the clear command. |
| `--merge-guard off` at L3 | Wave 0 prints once: "Remediation is unprotected: --merge-guard off." No draft call is made. |
| A fresh `--monitor 2` run (no `--resume`, no guard events) that applies fixes and halts before the push | The final report prints "PR #N is still mergeable; this run's fixes are local only." The line is written in the SKILL.md output table, which every run loads, not only in the guard ref. |
| End of Wave 3 at L3: at least one verified, Medium-or-higher finding routed to a fix (review-fix cycle, or CI-fix cycle from Wave 8) | Read, decide, request, `--to draft`, settle. Print the clear command once. |
| First engage of the run finds the PR already draft | Settle `skipped/already_draft`, phase `disabled`, never mutate. |
| Diagnosis ends with no edit (`applied_edits == 0`) | Release, cause `no_edits`. |
| Pre-push head guard (Wave 6) | Script `--read` must show `state == OPEN`; otherwise halt `pr_not_open`, push nothing. |
| After `push_completed`, head equals `target_sha` | Release, cause `pushed`, before reply, resolve and the S5a re-trigger. |
| Foreign toggle seen at a checkpoint | Settle `skipped/user_override`, phase `disabled`, no more draft calls, keep pushing, report. |
| Timeline unreadable at a checkpoint after engage | Do not release; report `held (timeline unreadable)`; keep pushing. |
| Engage fails, or timeline unreadable at engage | Halt before any edit: `terminal_halted`, reason `draft_guard_unavailable`. |
| Any exit after engage with no confirmed push and no zero-edit proof | PR stays draft; report `held` with the clear command. |

## 4. Component specifications

### 4.1 `src/superclaude/pr_submit/merge_guard.py` (new, pure)

No `gh` or `git` word on any line, comments included (F6). Imports only `enum`, `dataclasses`, `re`, `.conflicts.is_conflict_cycle`.

```python
class GuardMode(str, Enum):   DRAFT = "draft"; OFF = "off"      # extension point for later modes
class Direction(str, Enum):   DRAFT = "draft"; READY = "ready"
class Phase(str, Enum):       ENGAGE_PENDING; HELD; RELEASE_PENDING; RELEASED; DISABLED

class GuardAction(str, Enum):
    NOOP; ENGAGE; RELEASE; RETRY_RELEASE; HOLD; REPORT_HELD
    SKIP_ALREADY_DRAFT; SKIP_USER_OVERRIDE; RECONCILE
    HALT_PR_NOT_OPEN; HALT_UNAVAILABLE

@dataclass(frozen=True)
class GuardRead:              # parsed output of `--read`
    ok: bool; state: str | None; is_draft: bool | None; head_sha: str | None
    auto_merge_armed: bool; transitions: int | None; complete: bool

@dataclass(frozen=True)
class GuardDecision:
    action: GuardAction; reason: str; cause: str | None = None; notes: tuple[str, ...] = ()
```

Functions (all total, no I/O):

| Function | Contract |
|---|---|
| `fix_cycle_id(kind, n)` | `"fix-<n>"` for kind `fix`, `"ci-<n>"` for kind `ci`; `ValueError` otherwise or when `n < 1`. Never collides with `CONFLICT_CYCLE_PREFIXES`. |
| `next_cycle_number(events, kind)` | 1 + the highest `<kind>-<n>` seen in any event's `cycle_id`; 1 when none. |
| `fold_draft_guard(events)` | Section 4.2. Returns `None` when the log holds no guard record. |
| `pending_requests(events)` | Guard requests with no matching settle, matched by `idempotency_key` (the guard's own crash window; `recovery.py` stays push-only). |
| `classify_toggles(guard, read)` | `"ok"`, `"foreign"` or `"unreadable"`; rule below. |
| `engage_decision(*, mode, ordinal, cycle_id, guard, read)` | Table below. |
| `release_decision(*, mode, ordinal, cycle_id, guard, read, applied_edits, target_sha, push_completed)` | Table below. `applied_edits` is THIS cycle's count of applied edits; it is not the run-wide `applied_edits` output field (which counts the whole run), so a zero-edit cycle after a fixing cycle still releases with `no_edits`. |
| `held_cycle_published(events, guard)` | `True` when `guard` is not `None` and the log holds a `push_completed` event whose `cycle_id` equals `guard.cycle_id`, whether written by the push triad or synthesized by recovery (`recovered: true`); `False` otherwise. The SKILL passes the result as `published`. It is the only way resume learns that a held cycle's push completed normally (F13). |
| `resume_decision(*, mode, ordinal, guard, read, pending, dangling_branch, published)` | Table below. `dangling_branch` is `None` or one of the module constants `BRANCH_LANDED = "landed"`, `BRANCH_NOT_LANDED = "not_landed"`, `BRANCH_AMBIGUOUS = "ambiguous"`, which equal the `recovery.py` strings (F13); a test imports both modules and asserts equality, because the core cannot import `recovery`. `published` is the output of `held_cycle_published`. |
| `guard_status(guard, mode, ordinal)` | `"off"`, `"released"`, `"held"`, `"user_override"`, `"unavailable"` for the output field `merge_guard`. |

`guard_status(guard, mode, ordinal)` maps, first match wins: `mode == OFF` or `ordinal < 3` with no guard record gives `off`; no guard record gives `released`; phase `HELD` gives `held`; phase `ENGAGE_PENDING` or `RELEASE_PENDING` gives `held` when `owned_draft` is true, else `unavailable`; phase `DISABLED` with cause `user_override` gives `user_override`; phase `DISABLED` with cause `already_draft` gives `off` (the PR was a draft before the run, nothing is guarded); phase `RELEASED` gives `released`. A halt with reason `draft_guard_unavailable` reports `unavailable`.

`classify_toggles(guard, read)` (the only foreign-toggle test; no actor identity, F11):

```text
if not read.ok or not read.complete or read.transitions is None:        -> "unreadable"
observed = read.transitions - guard.baseline
slack    = guard.unsettled + guard.failed_mutations
if observed < guard.run_toggles:                                        -> "unreadable"   # events missing
if observed > guard.run_toggles + slack:                                -> "foreign"
expected = {HELD: True, RELEASED: False}.get(guard.phase)               # pending phases accept either
if expected is not None and read.is_draft != expected:                  -> "foreign"
else                                                                    -> "ok"
```

`failed_mutations` keeps a call that failed on the client but landed on the server from being read as a user action (a retry then finds the PR already in the target state and settles `confirmed, changed: false`).

`engage_decision`, first matching row wins:

| # | Condition | Decision |
|---|---|---|
| 1 | `mode == OFF`, or `ordinal < 3`, or `is_conflict_cycle(cycle_id)` | `NOOP` (reason `mode_off`, `ordinal`, `conflict_cycle`) |
| 2 | `guard.phase == DISABLED` | `NOOP(disabled)` |
| 3 | `not read.ok` | `HALT_UNAVAILABLE(read_failed)` |
| 4 | `read.state != "OPEN"` | `HALT_PR_NOT_OPEN` |
| 5 | `guard.phase == RELEASE_PENDING` and `guard.owned_draft` | `RETRY_RELEASE` (release first, then re-decide) |
| 6 | `guard.phase == RELEASE_PENDING` and not `owned_draft` | `HOLD(ownership_unproven)` |
| 7 | `guard.phase == HELD` | `NOOP(already_held)` |
| 8 | `not read.complete` or `read.transitions is None` | `HALT_UNAVAILABLE(timeline_unreadable)` |
| 9 | `guard` exists and `classify_toggles == "foreign"` | `SKIP_USER_OVERRIDE` |
| 10 | `guard is None` and `read.is_draft` | `SKIP_ALREADY_DRAFT` |
| 11 | otherwise | `ENGAGE`; `notes` carries `auto_merge_armed` when set |

`release_decision`, first matching row wins:

| # | Condition | Decision |
|---|---|---|
| 1 | `mode == OFF`, `ordinal < 3`, or conflict cycle | `NOOP` |
| 2 | `guard is None` or `guard.phase not in (HELD, RELEASE_PENDING)` | `NOOP(not_held)` |
| 3 | `not read.ok` | `HOLD(read_failed)` |
| 4 | `read.state != "OPEN"` | `HALT_PR_NOT_OPEN` |
| 5 | `classify_toggles == "unreadable"` | `HOLD(timeline_unreadable)` |
| 6 | `classify_toggles == "foreign"` | `SKIP_USER_OVERRIDE` |
| 7 | `applied_edits == 0` | `RELEASE(cause=no_edits)` |
| 8 | `push_completed` and `read.head_sha == target_sha` | `RELEASE(cause=pushed)` |
| 9 | otherwise | `HOLD(head_mismatch or push_not_completed)` |

`resume_decision`, first matching row wins:

| # | Condition | Decision |
|---|---|---|
| 1 | `guard is None` | `NOOP` |
| 2 | `(ordinal < 3 or mode == OFF)` and phase not in (`RELEASED`, `DISABLED`) | `REPORT_HELD` (no mutation; prints the clear command) |
| 3 | `pending` non-empty | `RECONCILE`, with `reason` one of `resume_reconciled`, `not_applied`, `ambiguous`: live draft state and `classify_toggles` decide; live state matching the request's direction and `observed == run_toggles + 1` settles `confirmed, changed: true, cause: resume_reconciled`; live state not matching settles `skipped, cause: not_applied`; anything else is `ambiguous` and holds. Each reason has its own test. |
| 4 | phase `HELD` and (`dangling_branch == "landed"` or `published`) | re-enter `release_decision` with `push_completed=True` (`landed` is a push recovery just completed; `published` is a push that completed normally before the crash) |
| 5 | `dangling_branch == "not_landed"` and phase `HELD` | `NOOP(held_through_redrive)` |
| 6 | `dangling_branch == "ambiguous"` | `HOLD(ambiguous_remote_tip)` |
| 7 | phase `RELEASE_PENDING` and `owned_draft` | `RETRY_RELEASE` |
| 8 | phase `RELEASE_PENDING` and not `owned_draft`, live draft | `HOLD(ownership_unproven)` |
| 9 | otherwise | `NOOP` |

### 4.2 Events and the folded key

Add to `EventType` in `models.py` (43 to 45, update the docstring and the `models.py:3,24` count, and the 43 text at `run_log.py:117`):

```text
DRAFT_GUARD_REQUESTED = "draft_guard_requested"   # appended and fsynced BEFORE the draft/ready call
DRAFT_GUARD_SETTLED   = "draft_guard_settled"     # appended AFTER the call, or alone for a skip
```

| Event | Fields |
|---|---|
| `draft_guard_requested` | `run_id`, `cycle_id`, `to` (`draft` or `ready`), `timeline_baseline` (int, set on the first request only), `original_is_draft` (bool, first request only), `idempotency_key` = `guard:<run_id>:<cycle_id>:<to>:a<k>` (`k` = 1 + prior requests with the same cycle and direction), `timestamp` |
| `draft_guard_settled` | `run_id`, `cycle_id`, `to`, `idempotency_key`, `outcome` (`confirmed`, `failed`, `skipped`), `changed` (bool), `cause`, `original_is_draft` (carried by a skip that has no request) |

`fold_draft_guard(events)` returns `None` or this dict, and `run_log.rebuild_state()` stores it as `state["draft_guard"]` (default `None`, added to `_NEW_KEY_DEFAULTS`):

```text
phase, phase_before_request, cycle_id, original_is_draft, baseline, run_toggles,
unsettled, failed_mutations, owned_draft, disabled_cause
```

| Event | Effect |
|---|---|
| `requested(to=draft)` | `phase = ENGAGE_PENDING`; remember the key as pending; first request sets `baseline` and `original_is_draft` |
| `requested(to=ready)` | `phase = RELEASE_PENDING`; remember the key |
| `settled(draft, confirmed, changed)` | `phase = HELD`, `owned_draft = True`, `run_toggles += 1` |
| `settled(draft, failed)` | `phase = RELEASE_PENDING`, `failed_mutations += 1`, `owned_draft` unchanged |
| `settled(draft, skipped, already_draft)` | `phase = DISABLED`, `disabled_cause = already_draft`; a first skip also sets `original_is_draft` |
| `settled(any direction, skipped, not_applied)` | the pending key is cleared and the phase returns to `phase_before_request`; `owned_draft` and the toggle counters are unchanged. For a draft request that was the first guard record, the whole record is erased (the fold returns `None`, including `baseline` and `original_is_draft`), so the next request is a first request again and takes a fresh baseline and a fresh `original_is_draft`; this is safe because `not_applied` means no toggle landed. For a ready request the phase returns to `HELD` (or `RELEASE_PENDING` when a failed release preceded it), and the next `release_decision` re-checks publication before a new request is made. It is NOT `DISABLED`, so a crash before the call does not leave later cycles unguarded. |
| `settled(draft, confirmed, not changed)` | `phase = HELD`, `owned_draft = True`, no toggle (a retry that finds the PR already draft after a call that failed on the client but landed) |
| `settled(ready, confirmed, changed)` | `phase = RELEASED`, `owned_draft = False`, `run_toggles += 1` |
| `settled(ready, confirmed, not changed)` | `phase = RELEASED`, `owned_draft = False`, no toggle |
| `settled(ready, failed)` | `phase = RELEASE_PENDING`, `failed_mutations += 1` |
| `settled(any, skipped, user_override)` | `phase = DISABLED`, `owned_draft = False` |

`unsettled` is the count of remembered keys with no settle. A corrupt line still raises, as it does today. `original_is_draft` is never read from GitHub after the first record, so a resumed run cannot mistake its own draft for an original one.

The matcher `pending_requests` uses the same key pairing as `detect_crash_window`, but over the two guard event types, so push recovery and guard recovery stay independent.

### 4.3 `fsm.py`: the flag

- `DEFAULT_MERGE_GUARD = "draft"`; `build_arg_parser` adds `--merge-guard` with `dest="merge_guard"`, `choices=["draft", "off"]` (same shape as `--conflict-max-tier`, F5).
- `SkillArgs.merge_guard: str = DEFAULT_MERGE_GUARD`; `parse_args` passes `ns.merge_guard`.
- Effective only at `--monitor 3`; accepted and inert below. `off` makes the skill print one line: "Remediation is unprotected: --merge-guard off."
- `RunConfig` and `run_skill` do not change (F5): the guard is SKILL-orchestrated.

### 4.4 `scripts/set-draft-state.sh` (new; all GitHub I/O)

Modelled on `scripts/retrigger-review.sh`: `set -euo pipefail`, same `die`, same `--repo` resolution from the origin remote, numeric `--pr` check, exit 127 when `gh` or `jq` is missing.

```text
set-draft-state.sh --pr <N> [--repo <owner/repo>] --read
set-draft-state.sh --pr <N> [--repo <owner/repo>] --to draft|ready
```

| Mode | Calls (every one repo-scoped, F7) | Output (one JSON line) |
|---|---|---|
| `--read` | `gh pr view "$PR" --repo "$REPO" --json state,isDraft,headRefOid,autoMergeRequest`; `gh api --paginate "repos/${REPO}/issues/${PR}/timeline" --jq '.[] \| select(.event=="convert_to_draft" or .event=="ready_for_review") \| .event'` counted with `wc -l` | `{"ok":true,"state":"OPEN","isDraft":false,"headRefOid":"<sha>","autoMergeRequest":false,"transitions":3,"complete":true,"error":null}`; when the timeline call fails: `"transitions":null,"complete":false` |
| `--to draft` | re-read `state,isDraft`; if not `OPEN`, emit `ok:false,error:"not_open"`; if already draft, `changed:false`; else `gh pr ready "$PR" --repo "$REPO" --undo`; re-read to verify | `{"ok":true,"state":"OPEN","isDraft":true,"headRefOid":"<sha>","changed":true,"error":null}` |
| `--to ready` | same with `gh pr ready "$PR" --repo "$REPO"` | same shape |

Exit codes: 0 success; 1 `gh` failure or failed verification (the JSON line is still printed with `ok:false`); 2 usage; 127 missing dependency. `--to` is idempotent, so a retry or a resume re-issue is safe. A verification mismatch after a mutation is `ok:false, error:"verify_failed"`, and the SKILL settles it `failed`.

### 4.5 Protocol and docs

| File | Change |
|---|---|
| `skills/sc-pr-submit-protocol/refs/merge-guard.md` (new) | The procedure of sections 3 and 4.1 to 4.4 as protocol steps (read, decide, request, mutate, settle) for Engage, Pre-push, Release, Exit report and Resume. Loaded lazily at L3 Wave 3, Wave 6 and Wave 8. Uses `scripts/...` and `superclaude.pr_submit.merge_guard` names only. |
| `SKILL.md` | One short bullet under each of Wave 0, Wave 3, Wave 6 and Wave 8, written as new sentences after, never inside, the pinned sentences. The Wave 0 bullet applies at every ordinal and in both modes: on `--resume`, or when the run log holds guard events, it loads the ref (Resume and Exit report) before Wave 1 and before any edit, release or re-trigger; at L3 with `--merge-guard off` it prints the unprotected line once. The Wave 3, Wave 6 and Wave 8 bullets load the ref only at L3 with `draft`: the Wave 3 bullet states that engage happens at the end of Wave 3 only when at least one verified finding of Medium severity or higher is routed to a fix, and once per cycle id (it must not contain the words `evidence-validator` or `conflict-intent.md`, which a line-content test allows only on lines that also say "Tier 2"); the Wave 6 bullet states that Pre-push runs at the pre-push head guard step before `push_decision` and Release runs after `push_completed` before reply, resolve and the re-trigger; the Wave 8 bullet states that a CI-fix cycle engages with kind `ci` and releases after `push_completed` before the CI re-poll. Also one `--merge-guard {draft,off}` row in the Required Input flag table beside `--conflict-max-tier`; one row `merge_guard` in the output table, which also carries the literal L2 line "PR #N is still mergeable; this run's fixes are local only." so that a fresh L2 run prints it without loading the ref; one line in the wave structure list. The Wave 0 bullet is a flat line placed before the Wave 1 bullet and contains no L3 or `draft` condition (the Wave bullets are flat lines, not headings, so the test checks position and wording). No new python fence (the one-fence tests, `test_cosmos_protocol.py:34-44`, `test_codex_reviews.py:685-697`). |
| `refs/loop-guard.md` | Its event-type enumeration says the enum has 43 members; update it to 45 and name `draft_guard_requested` and `draft_guard_settled`, without the words `gh` or `git` (the file is in `CORE_PURE_FILES`). |
| `refs/state-machine.md` | Overlay note: the guard phases are fold values, not `MonitorState` members. Respect the wait-only sentences pinned at `test_static_grep.py:791`. |
| `commands/pr-submit.md` | `--merge-guard {draft,off}` in the argument-hint and the Options table; a short "Merge guard" section next to "Merge-conflict handling". |
| `docs/user-guide/commands.md`, `docs/user-guide/flags.md` | Flag row and a paragraph: what it does, the clear command, `held` meaning, default on. |

Output field `merge_guard`: `off`, `released`, `held`, `user_override`, `unavailable`. A `held` report always carries the reason and `gh pr ready <N> --repo <REPO>` (formatted by the SKILL, never by the core, because the core cannot contain `gh`). At L2 the final report adds: "PR #N is still mergeable; this run's fixes are local only." (the literal line lives in the SKILL.md output table; the ref's Exit report section refers to it and does not carry its own copy).

### 4.6 Cycle identity

`fix_cycle_id` gives guard-enabled cycles an explicit id: `fix-<n>` for review-fix cycles and `ci-<n>` for CI-fix cycles, `n` from `next_cycle_number`. The SKILL mints it at the end of Wave 3 and uses the same id as the `cycle_id` of the push triad (`push_idempotency_key`) and of `rereview_requested`, so the guard, the push and the re-trigger of one cycle share a key. With `--merge-guard off` nothing changes. The build must first confirm where the SKILL assigns a fix cycle's id today and keep exactly one source for it (open item O1).

### 4.7 Pinned write-verb classification (F12)

Every new line under `src/superclaude/skills/`, `src/superclaude/commands/` or `src/superclaude/agents/` that contains `gh pr`, `gh api` or a git write verb is a hit of `WRITE_VERB_RE` and needs one entry in `WRITE_VERB_CLASSIFICATION` in `tests/skills/test_worker_contract.py`: the key is the repo-relative path, the verb text (`gh pr`, `gh api`) and the exact stripped line; the value is category `never-worker` with the standard pr-submit reason text used by the neighbouring entries (the pr-submit monitor is on the never-as-worker list). The entries are added after the text of each file is final, as the last step of the task that writes the file, because a later edit of a classified line makes the entry stale and fails `test_classification_table_has_no_stale_entries`. The new files that carry hits are `scripts/set-draft-state.sh`, `refs/merge-guard.md`, `src/superclaude/commands/pr-submit.md` and any new `SKILL.md` line; a new line that does not need the words `gh pr` (for example "print the clear command from the ref") avoids an entry. The `read-only` category is not used for these calls (a `gh pr ready` mutation is never read-only). `docs/user-guide/` is outside the scanned roots.

## 5. Sequences

Happy path, ordinal 3:

```text
W3 end : read -> engage_decision=ENGAGE -> requested(draft) fsync -> to draft -> settled(confirmed)
W4/W5  : diagnose, edit, validate               (PR is draft; clear command already printed)
W6     : fix commit -> pre-push guard (+ read.state == OPEN) -> push_decision -> push_initiated(fsync)
         -> push -> push_completed
         -> read -> release_decision=RELEASE(pushed) -> requested(ready) fsync -> to ready -> settled(confirmed)
         -> reply -> resolve -> S5a re-trigger (reviewers see a ready PR)
```

Acceptance trace (must appear in this order in the run log): `draft_guard_requested(draft)`, `draft_guard_settled(confirmed)`, `fix_applied`, `push_completed`, `draft_guard_requested(ready)`, `draft_guard_settled(confirmed)`, `rereview_requested`.

| Case | Trace |
|---|---|
| Engage fails | `requested(draft)` -> `--to draft` fails -> `settled(failed)` -> `terminal_halted(draft_guard_unavailable)`, no edit. Message names `--merge-guard off` and prints the clear command. |
| Validation fails after engage | `terminal_halted` or `VALIDATION_FAIL`; phase stays `HELD`; report `merge_guard: held` plus the clear command. |
| Zero-edit cycle | engage at W3 end, no edit, W6 blocks the push (INV-016 predicate 5), `release_decision=RELEASE(no_edits)`. |
| Foreign toggle | at release `classify_toggles == foreign` -> `settled(skipped, user_override)` -> phase `DISABLED`; the push and reply continue; report `user_override`. |
| Crash between request and settle | `--resume`: Wave 0 loads the ref, `pending_requests` is non-empty, `RECONCILE` runs with a live read before any edit. If the live PR is not draft, the request settles `skipped/not_applied`, the phase returns to `phase_before_request`, and the next cycle engages normally. |
| Crash after `push_initiated`, before `push_completed`, push landed | `detect_crash_window` finds the dangling push; recovery returns `landed` and synthesizes `push_completed`; `resume_decision` row 4 (`dangling_branch == "landed"`) releases first, then the S5a logic of `refs/review-retrigger.md` runs. `not_landed` keeps the PR draft (row 5); `ambiguous` holds (row 6). |
| Crash after a normal `push_completed`, before release | No dangling window (`detect_crash_window` returns `None`), so there is no branch. The SKILL passes `published = held_cycle_published(events, guard)`, which is true; row 4 releases first, then the S5a logic runs. Without `published` no row would match and the PR would stay draft. |
| PR merged while held | next checkpoint: `state != OPEN` -> halt `pr_not_open`, nothing pushed, report the local commit `<target_sha>`. |

## 6. Files to change

| File | Kind | Notes |
|---|---|---|
| `src/superclaude/pr_submit/merge_guard.py` | new | section 4.1 |
| `src/superclaude/pr_submit/models.py` | edit | 2 members, docstring and count |
| `src/superclaude/pr_submit/run_log.py` | edit | `rebuild_state` key, append docstring count |
| `src/superclaude/pr_submit/fsm.py` | edit | flag, `SkillArgs`, `parse_args` |
| `src/superclaude/pr_submit/__init__.py` | edit | export the public guard names |
| `src/superclaude/skills/sc-pr-submit-protocol/scripts/set-draft-state.sh` | new | section 4.4 |
| `.../refs/merge-guard.md` | new | section 4.5 |
| `.../SKILL.md`, `.../refs/state-machine.md`, `.../refs/loop-guard.md` | edit | additive only (loop-guard: the 43 to 45 enumeration text) |
| `src/superclaude/commands/pr-submit.md` | edit | flag and section |
| `docs/user-guide/commands.md`, `docs/user-guide/flags.md` | edit | flag and paragraph |
| `tests/pr_submit/test_merge_guard.py`, `test_set_draft_state.py` | new | section 7 |
| `tests/skills/test_worker_contract.py` | edit | one `WRITE_VERB_CLASSIFICATION` entry per new hit line (section 4.7); added last in each task that writes a file with hits |
| `tests/pr_submit/test_run_log.py`, `test_codex_reviews.py`, `test_static_grep.py`, `test_skill_parse.py` | edit | count 43 to 45 at `test_run_log.py:171-175` and `test_codex_reviews.py:441`; `"draft_guard": None` at `test_run_log.py:312`; `merge_guard.py` into the zero-token file set; script lists only after checking each list's purpose; flag default and choices test mirroring `--conflict-max-tier` |

After editing under `src/superclaude/`: `make sync-dev`, then `make verify-sync`. Run `make sync-dev` at the end of every task that edits a file under `src/superclaude/skills/` or `src/superclaude/commands/`, because `tests/cli/test_verify_sync_hooks.py` runs `make verify-sync` inside the full suite; the final task also runs `uv run pytest tests/cli/test_verify_sync_hooks.py tests/unit/test_cli_install.py -q`. A repo-wide pin (F12) escaped two reviews because only `tests/pr_submit` was run, so the final task runs the FULL suite (`uv run pytest -q tests`) and compares its failures with the base-commit record. Record `make lint`, `uv run ruff format --check src/ tests/` and the full-suite result (`uv run pytest -q tests`: pass count and every failing test id) on the base commit before the first code edit (pre-existing failures are not this feature's). Never stage `.claude/`. Unchanged and must still pass: `test_idempotency.py:89` (7 sets), the one-python-fence tests, `test_conflict_sync_protocol.py:576` (no `src/superclaude` text in skill or command files).

## 7. Test design

The twelve minimum tests of the requirements, mapped to what they assert:

| Test | Asserts (FR) |
|---|---|
| `test_guard_modes_ordinals_and_resume_authority` | no call or event at ordinals 0-2 or `off`; held guard reported on resume (FR-1, FR-2) |
| `test_attach_and_create_preserve_preexisting_draft` | `skipped/already_draft`, never `--to ready` (FR-6) |
| `test_guard_engages_at_routed_finding_once_per_cycle` | engage at the end of Wave 3, once per cycle id, not for conflict cycles (FR-3, FR-5, FR-20) |
| `test_guard_releases_only_after_publication_or_zero_edit_proof` | head equals `target_sha`, or `applied_edits == 0`; release before reply and re-trigger (FR-8, FR-9) |
| `test_guard_holds_on_unpublished_or_uncertain_exits` | each exit of D7 reports `held` and the clear command (FR-17) |
| `test_guard_engage_failure_blocks_edits` | `draft_guard_unavailable` before any edit (FR-15) |
| `test_guard_release_failure_retries_once_and_reports` | one retry, `already_in_state` counts as confirmed, `release_pending` (FR-16) |
| `test_guard_external_toggle_and_roundtrip_disable` | ledger test: observed above `run_toggles + slack`; ready-then-draft round trip (FR-12, FR-13) |
| `test_guard_missing_timeline_or_ambiguous_intent_never_readies` | unreadable, incomplete or short timeline holds (FR-14) |
| `test_guard_crash_boundaries_and_push_recovery_abc` | crash before and after each request and settle; the `landed`, `not_landed` and `ambiguous` branches produced by the real `detect_crash_window` and `resolve_crash_window` over a real `RunLog` (never injected strings); a crash after a normal `push_completed` (no dangling window, `published` true) releases before the re-trigger; engage, crash, resume with live draft true stays `held`, never `disabled` (FR-7, FR-21) |
| `test_guard_closed_merged_or_moved_head_forbids_mutation` | `pr_not_open`, moved head, nothing pushed (FR-10) |
| `test_guard_script_contract_scoping_and_legacy_fold` | fake `gh` on PATH, exit codes 0/1/2/127, `--repo` on every call, an old log folds to `draft_guard: None` |

Unit tables for `engage_decision`, `release_decision`, `resume_decision`, `classify_toggles` and `guard_status` (every phase and cause) cover every row of section 4.1, including the three `RECONCILE` reasons and the case of a zero-edit cycle after a fixing cycle. Two further cases: crash, resume with `not_applied`, then re-engage; and the protocol assertions that the Wave 0 bullet names `--resume`, is not gated on L3 or `draft`, and prints the literal `off` line. Add the acceptance trace of section 5 as a fixture over `RunLog`. A static test asserts `merge_guard.py` has no `gh` or `git` word. Further cases required by v3: a fold test for `settled(ready, skipped, not_applied)` (key cleared, phase back to `HELD`, `unsettled == 0`) and for request, `not_applied`, request on a first record (fresh `baseline` and `original_is_draft` on the second request); a `held_cycle_published` test (true for a normal and for a recovered `push_completed` of the guard's `cycle_id`, false for another cycle's); a test that `BRANCH_LANDED`, `BRANCH_NOT_LANDED` and `BRANCH_AMBIGUOUS` equal the `recovery.py` constants; protocol assertions that the literal L2 line is in `SKILL.md` and that the Wave 3 bullet names the Medium-or-higher routed-finding trigger and "once per cycle"; the script test for a missing `jq` (exit 127); `test_every_write_verb_hit_is_classified` and `test_classification_table_has_no_stale_entries` pass after the new files exist.

## 8. Pre-build gate (FR-23) and open items

Owner decision (2026-11-07, relayed by the coordinator): the build proceeds now with no GitHub calls (tests use a fake `gh`). Gates G1 (live token and plan check), G2 (live ordering and pagination), G4, G5 and G6 are a RELEASE gate, not a build gate: the owner runs them on a disposable fork PR before the feature is merged or turned on by default. The user guide states that draft behaviour is unverified until then, and the PR body states the gate plainly. No task makes a live PR call, and the run that opens the PR must not enable the feature (`--merge-guard off`).

| # | Check | Status |
|---|---|---|
| G1 | `gh pr ready --undo` exists | Confirmed in `gh` 2.103.3 and the manual; "subject to plan support": confirm on a disposable fork PR |
| G2 | Timeline names `convert_to_draft`, `ready_for_review` | Confirmed in GitHub documentation; confirm live ordering and pagination on a disposable PR |
| G3 | `gh pr view --json autoMergeRequest,isDraft,state,headRefOid` | Confirmed locally (field list) |
| G4 | A draft blocks merge via UI, API, auto-merge, merge queue; converting disarms an armed auto-merge | NOT verified; disposable PR |
| G5 | Augment, Codex and the three `pull_request` workflows on draft and ready transitions | NOT verified; `contract3-generator-constraint-lint.yml` lacks `ready_for_review` |
| G6 | `gh pr ready` when already in the requested state (error or no-op) | NOT verified; the script checks first, so the answer only affects the error text |

Open items for the plan (do not guess; resolve with a read of the code first):

- **O1** Where the SKILL assigns a fix or CI cycle's `cycle_id` today, and whether any test pins that value.
- **O2** How scripts are granted and invoked in the SKILL front matter and in `test_conflict_sync_protocol.py:587`, so the new script follows the same path.
- **O3** Exact-text pins on `pr-submit.md` (argument-hint, Options table) and `SKILL.md` that the additive edits must not break, and the line-content rules (`test_intent_and_validator_lines_say_tier_2`, `test_skill_forbids_force_push`) that constrain which words a new line may contain; grep before editing.
- **O4** The extra `retrigger` guard: the S5a text must stay unchanged; release is placed before it by a new sentence, not by editing the pinned one.

## 9. Traceability

| Requirement | Section |
|---|---|
| FR-1, FR-2 | 3, 4.1 (row 1), 4.3 |
| FR-3, FR-5, FR-20 | 4.1 engage rows 1, 5-7, 4.6 |
| FR-4, FR-6, FR-7 | 4.1 row 10, 4.2 (first record, never a live read) |
| FR-8, FR-9 | 4.1 release rows 7-8, 5 |
| FR-10, FR-11 | 4.1 engage row 4, release row 4, 4.4 (`state`, `autoMergeRequest`) |
| FR-12, FR-13, FR-14 | 4.1 `classify_toggles`, release rows 5-6 |
| FR-15, FR-16, FR-17, FR-18, FR-19 | 4.1 engage rows 3 and 8, 4.5 (clear command, L2 line), 5 |
| FR-21 | 4.1 `resume_decision`, 4.2 `pending_requests` |
| FR-22, FR-23 | 7, 8 |

## 10. Plan authoring notes (for the workflow that builds the plan from this design)

These come from a review of the first plan built from this design; they are requirements on the plan, not on the code.

- Cite tests and constants by symbol name (for example `_NEW_KEY_DEFAULTS`, `_RESOLUTION_SCRIPTS`, the test that asserts the event count), never by bare line number: earlier tasks edit the same files and line numbers drift.
- Declare dependencies completely, one `Depends on:` line per dependency: a task depends on every earlier task whose output it imports or consumes (the run-log wiring task and the scenario-test task both need the decision functions; the protocol tasks need the pre-build record).
- The protocol wiring covers the Wave 0 resume and `off` hook as well as Waves 3, 6 and 8 (section 4.5), with a test for each bullet.
- Run `make sync-dev` at the end of each task that edits `src/superclaude/skills/` or `src/superclaude/commands/`, and run the sync-hook tests named in section 6 in the final task.
- The fold, `guard_status`, resume-reason and per-cycle `applied_edits` rules of sections 3 and 4.1 each get an acceptance criterion that a wrong implementation would fail.
- The pre-build record task states the release-gate decision of section 8 and records the base-commit lint result.
- Update the 43-member enumeration in `refs/loop-guard.md` in the event-enum task.
- Protocol prose written by the plan never carries `file:NNN` pointers and never contains the words `evidence-validator` or `conflict-intent.md` on a new SKILL.md line.

Added in v3 (from the review of the second plan):

- Classification entries (section 4.7): the task that writes `scripts/set-draft-state.sh`, the task that writes `refs/merge-guard.md`, the task that edits `src/superclaude/commands/pr-submit.md` and any task that adds a `SKILL.md` line with `gh pr` or `gh api` each ends with adding its `WRITE_VERB_CLASSIFICATION` entries (exact stripped line, category `never-worker`) and runs `uv run pytest tests/skills/test_worker_contract.py -q`. The final task runs the full suite and compares it with the base-commit record.
- The L2 line is written into the SKILL.md output table; its acceptance criterion is a test that the literal line is in `SKILL.md`, and a fresh L2 run must not depend on loading the ref.
- Resume: the plan passes `published` and the recovery branch strings of F13; the crash scenario tests derive branches from a real `RunLog` through `detect_crash_window` and `resolve_crash_window`, never by injecting `"A"`, `"B"` or `"C"`.
- Fold: the plan states that a settled `not_applied` of either direction returns to `phase_before_request` and that a first record erased by it makes the next request a first request again; the acceptance criteria test both directions and the fresh baseline.
- Test hygiene: scenario tests import only helpers and fixtures from `test_set_draft_state.py`, never `test_*` functions (pytest would collect them twice); "no push after a `pr_not_open` halt" is asserted on `RunLog.read_events()` (no `push_initiated` or `push_completed` after the halt), because the fake `gh` log cannot see a `git push`; the byte-identical checks for the pinned S5a and Wave 6 pre-push sentences compare against literal string constants taken from the existing pins, not against `git show HEAD:`; the repo-pin proof for the new script is the recorded fake-`gh` argument log plus a static scan inside `test_set_draft_state.py` that every `gh` line carries `--repo` or a `repos/` path (the `test_t105_runtime_repo_pin` test covers only the poll script).
- The Wave 3 and Wave 0 bullet acceptance criteria assert wording and position, not headings: the Wave 3 bullet names the routed-finding trigger and "once per cycle"; the Wave 0 bullet sits before the Wave 1 bullet and has no L3 or `draft` condition.
```

### .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md:29-56

```markdown
## Phase 1: Contracts and pure core

## Task 1: Write the pre-build record `./artifacts/pre-build-gate.md`

Create `./artifacts/pre-build-gate.md` in this package from ./source.md sections 6, 8 and 10. First record the base-commit state: run `make lint`, `uv run ruff format --check src/ tests/` and the full suite `uv run pytest -q tests` before any code edit and write each exit code, the pass count and every failing test id (or "clean") into the file, so later failures can be told apart from this feature's. Then record the release-gate decision of ./source.md section 8 in the owner's words: the build proceeds with no GitHub calls (fake `gh` in tests); gates G1 (live part), G2 (live part), G4, G5 and G6 are a release gate that the owner runs on a disposable fork PR before the feature is merged or turned on by default; the user guide states that draft behaviour is unverified until then; the PR body states the gate plainly; the run that opens the PR must pass `--merge-guard off`. Then close the open items by reading the code: O1, where `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md` (Wave 3 to Wave 6 and Wave 8 text) and `refs/loop-guard.md` assign a fix or CI cycle's `cycle_id` today and whether any test under `tests/pr_submit/` pins a value; O2, how scripts are granted and invoked in the SKILL front matter and what `test_allowed_tools_cover_every_program` in `tests/pr_submit/test_conflict_sync_protocol.py` and the `_RESOLUTION_SCRIPTS` tests in `tests/pr_submit/test_static_grep.py` require of a new script; O3, every exact-text pin and line-content rule (for example `test_intent_and_validator_lines_say_tier_2`, `test_skill_forbids_force_push`, the wait-only sentences pinned for `refs/state-machine.md`, and the `WRITE_VERB_CLASSIFICATION` table with its stale-entry test in `tests/skills/test_worker_contract.py`) on `SKILL.md`, `refs/state-machine.md`, `refs/loop-guard.md` and `src/superclaude/commands/pr-submit.md` that the later additive edits must avoid; O4, that the S5a re-trigger sentence in `SKILL.md` stays unchanged and where the new release sentence goes relative to it; and the literal start text of the S5a sentence and of the Wave 6 pre-push sentence as the existing pins write them, so later tests can compare against string constants.

Acceptance criteria:
- `./artifacts/pre-build-gate.md` has the base-commit record (three commands, exit codes, the full-suite pass count and failing test ids, or "clean") and one row each for G1 to G6: G1 to G3 `CONFIRMED` for the locally verifiable part with the evidence named in ./source.md, G1 and G2 live parts, G4, G5 and G6 `OPEN` as a release gate with the owner decision quoted.
- O1 to O4 each carry the finding with the file and symbol read in this task (no bare line numbers); O1 names one single place where the guard-enabled cycle id is minted so the push triad and `rereview_requested` use the same id, or states that no id is minted today and which sentence will mint it.
- The file lists every exact-text pin and line-content rule found for O3, including the classification table rule (exact line key, category, stale-entry test), and the literal start text of the two pinned sentences of O4, so Tasks 7 to 13 can avoid or reuse them; no GitHub or network call is made.

## Task 2: Add the two guard events to the closed event enum and the enumeration texts

Depends on: Task 1

Edit `src/superclaude/pr_submit/models.py`: add `DRAFT_GUARD_REQUESTED = "draft_guard_requested"` and `DRAFT_GUARD_SETTLED = "draft_guard_settled"` to `EventType` (a comment block like the conflict-cycle one), and change the module docstring and the `EventType` class docstring from "exactly 43 members" to 45, naming the new events. Edit the `RunLog.append` docstring in `src/superclaude/pr_submit/run_log.py` that says "43 closed" to 45. Edit `src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md`: its heading "The 43 event types" and the sentence that says the enum has EXACTLY 43 members become 45 and name `draft_guard_requested` and `draft_guard_settled`, without the whole words `gh` or `git` (the file is in `CORE_PURE_FILES`). Update `tests/pr_submit/test_run_log.py` (the test `test_eventtype_is_43_members_with_silence_reviewer_and_conflict_events`: rename it to describe 45 members, assert both lengths are 45 and both new values are present) and the `len(EventType)` assertion in `tests/pr_submit/test_codex_reviews.py` to 45. Leave `tests/pr_submit/test_idempotency.py` (7 sets) unchanged. Run `make sync-dev`.

Acceptance criteria:
- `uv run pytest tests/pr_submit/test_run_log.py tests/pr_submit/test_codex_reviews.py tests/pr_submit/test_idempotency.py tests/pr_submit/test_static_grep.py -q` passes with `len(EventType) == 45` and the two new values asserted.
- `RunLog.append` accepts an event with `event_type: "draft_guard_requested"` and still rejects an unknown type, with the updated count in the error message.
- `grep -rn "43" src/superclaude/pr_submit/models.py src/superclaude/pr_submit/run_log.py src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md` shows no remaining claim that the enum has 43 members, and `refs/loop-guard.md` names both new event values.
- `make verify-sync` exits 0 after the sync.

## Task 3: Create `merge_guard.py` types, cycle ids, fold, pending matcher, published check and status mapping

Depends on: Task 2

Create `src/superclaude/pr_submit/merge_guard.py` following ./source.md sections 4.1, 4.2 and 4.6: `GuardMode`, `Direction`, `Phase`, `GuardAction`, `GuardRead`, `GuardDecision`; the string constants `BRANCH_LANDED = "landed"`, `BRANCH_NOT_LANDED = "not_landed"`, `BRANCH_AMBIGUOUS = "ambiguous"`; `fix_cycle_id(kind, n)` and `next_cycle_number(events, kind)` (never colliding with `CONFLICT_CYCLE_PREFIXES` from `src/superclaude/pr_submit/conflicts.py`); `fold_draft_guard(events)` implementing every row of the section 4.2 effect table (fields `phase, phase_before_request, cycle_id, original_is_draft, baseline, run_toggles, unsettled, failed_mutations, owned_draft, disabled_cause`; `None` when no guard record exists; `original_is_draft` taken only from the first guard record or a first skip, never from a later read); `pending_requests(events)` matching requests to settles by `idempotency_key`; `held_cycle_published(events, guard)` (true when a `push_completed` event, normal or recovered, carries the guard's `cycle_id`); `guard_status(guard, mode, ordinal)` implementing the first-match mapping of section 4.1 (`off`, `released`, `held`, `user_override`, `unavailable`). The module imports only `enum`, `dataclasses`, `re` and `is_conflict_cycle` from `.conflicts`, and contains no `gh` or `git` word on any line. Create `tests/pr_submit/test_merge_guard.py` with table tests for these functions.
```

### .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md:104-114

```markdown
## Task 7: Create the GitHub I/O script `set-draft-state.sh`

Depends on: Task 1

Create `src/superclaude/skills/sc-pr-submit-protocol/scripts/set-draft-state.sh` following ./source.md section 4.4 and modelled on `scripts/retrigger-review.sh` (same `die`, `--repo` resolution from the origin remote, numeric `--pr` check, exit 127 when `gh` or `jq` is missing, executable bit). Modes `--read` and `--to draft|ready` with the exact calls, the one-line JSON shapes and the exit codes 0, 1, 2, 127 of section 4.4; every `gh` call carries `--repo "$REPO"` or a `repos/${REPO}/...` path; the timeline count uses `gh api --paginate` with a `jq` filter on `convert_to_draft` and `ready_for_review` piped to `wc -l`; `--to` re-reads state first (non-`OPEN` gives `error:"not_open"`), is idempotent (`changed:false` when already in the target state) and verifies after the mutation (`verify_failed`). Create `tests/pr_submit/test_set_draft_state.py` using a fake `gh` on `PATH` that logs its arguments (the fake-executable approach of `tests/pr_submit/test_conflict_scripts.py`), exposing the fake as a helper or fixture that other test files may import. Add the script to `_RESOLUTION_SCRIPTS` in `tests/pr_submit/test_static_grep.py` only after reading the purpose of that list (Task 1 O2), and to any script list that Task 1 O2 shows is required for a new script. As the last step, once the script text is final, add one `WRITE_VERB_CLASSIFICATION` entry in `tests/skills/test_worker_contract.py` for every line of the script that matches `gh pr` or `gh api` (exact stripped line, category `never-worker`, the standard pr-submit reason). Run `make sync-dev`.

Acceptance criteria:
- Fake-`gh` tests assert: `--read` prints one JSON line with `ok`, `state`, `isDraft`, `headRefOid`, `autoMergeRequest`, `transitions`, `complete`; a failing timeline call prints `transitions: null` and `complete: false`; `--to draft` on a draft PR makes no `pr ready` call and prints `changed:false`; `--to ready` on a merged PR prints `ok:false` with `error:"not_open"`; a mismatch after the mutation prints `ok:false` with `error:"verify_failed"`.
- Exit codes are asserted: 0 on success, 1 on a failing `gh` (JSON still printed with `ok:false`), 2 for a missing or non-numeric `--pr` and for an unknown argument, 127 with `gh` absent from `PATH` and a separate case with `jq` absent from `PATH`.
- The recorded fake-`gh` argument log shows `--repo` or a `repos/` path on every call, and `test_set_draft_state.py` also statically scans the script and asserts every `gh` line carries `--repo` or a `repos/` path (the existing `test_t105_runtime_repo_pin` covers only the poll script and is not the proof); the script passes the `_RESOLUTION_SCRIPTS` origin-URL resolution tests.
- `uv run pytest tests/pr_submit/test_set_draft_state.py tests/pr_submit/test_static_grep.py tests/pr_submit/test_conflict_sync_protocol.py tests/skills/test_worker_contract.py -q` passes (the classification and stale-entry tests included) and `make verify-sync` exits 0.
```

### .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md:159-173

```markdown
## Task 11: Write the scenario tests over the run log

Depends on: Task 3
Depends on: Task 4
Depends on: Task 5
Depends on: Task 7

Create `tests/pr_submit/test_merge_guard_scenarios.py` with a small test driver that applies the pure decisions of `merge_guard.py`, appends events to a real `RunLog` in a temporary directory and runs `scripts/set-draft-state.sh` against a fake `gh`; it imports only the fake-`gh` helper or fixture from `tests/pr_submit/test_set_draft_state.py`, never a `test_*` function (pytest would collect it twice). Implement the twelve test names of ./source.md section 7 and the acceptance trace of section 5. Cover the cases of the section 5 table: engage failure halts before any edit, validation failure leaves phase `held`, zero-edit cycle releases with `no_edits` (including a zero-edit cycle after a fixing cycle), foreign toggle disables the guard and the run continues, crash between request and settle reconciles on resume (including `not_applied` followed by a normal re-engage, and a ready request settled `not_applied` that stays `HELD` and is released after the publication check), crash after a dangling `push_initiated` with branch strings produced by the real `detect_crash_window` and `resolve_crash_window` (`landed` releases, `not_landed` holds, `ambiguous` holds), crash after a normal `push_completed` (no dangling window, `published` true) releases before the re-trigger, merged PR halts `pr_not_open`, ordinals 0 to 2 and `off` make no call, an originally draft PR is never made ready, an engage, crash, resume with live draft true stays `held` and is released after the push, and a conflict-cycle id never engages.

Acceptance criteria:
- The test file defines `test_guard_modes_ordinals_and_resume_authority`, `test_attach_and_create_preserve_preexisting_draft`, `test_guard_engages_at_routed_finding_once_per_cycle`, `test_guard_releases_only_after_publication_or_zero_edit_proof`, `test_guard_holds_on_unpublished_or_uncertain_exits`, `test_guard_engage_failure_blocks_edits`, `test_guard_release_failure_retries_once_and_reports`, `test_guard_external_toggle_and_roundtrip_disable`, `test_guard_missing_timeline_or_ambiguous_intent_never_readies`, `test_guard_crash_boundaries_and_push_recovery_abc`, `test_guard_closed_merged_or_moved_head_forbids_mutation` and `test_guard_script_contract_scoping_and_legacy_fold` (the last asserts the legacy-log fold and the script scoping through shared helpers, with no imported `test_*` function).
- The acceptance-trace test asserts the exact event order `draft_guard_requested(draft)`, `draft_guard_settled(confirmed)`, `fix_applied`, `push_completed`, `draft_guard_requested(ready)`, `draft_guard_settled(confirmed)`, `rereview_requested` from `RunLog.read_events()` and asserts no `rereview_requested` appears before the release settle.
- The crash tests build the dangling window by appending a real `push_initiated` event and calling `detect_crash_window` and `resolve_crash_window`; none of them passes a hand-written branch string to `resume_decision`, and the normal-`push_completed` test asserts `detect_crash_window` returns `None` and `published` is true.
- Forbidden-call assertions: the fake `gh` log never contains `pr ready` without `--undo` for an originally draft PR and never contains any `pr ready` call at ordinal 2 or with `off`; after a `pr_not_open` halt the test asserts on `RunLog.read_events()` that no `push_initiated` or `push_completed` event follows the halt (the fake `gh` log cannot see a `git push` and is not used for this check).
- `uv run pytest tests/pr_submit -q` passes in full.
```

### .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md:188-200

```markdown
## Task 13: Document the flag in the user guides, sync, and run the final checks

Depends on: Task 2
Depends on: Task 10
Depends on: Task 11
Depends on: Task 12

Edit `docs/user-guide/commands.md`: add `[--merge-guard {draft,off}]` to the `/sc:pr-submit` usage line and a paragraph after the "Merge conflicts" paragraph describing the guard, its default, the `held` state, the clear command `gh pr ready <N> --repo <REPO>` and that draft behaviour is unverified until the owner runs the disposable-PR gate. Edit `docs/user-guide/flags.md`: add a `--merge-guard` row beside the `--conflict-max-tier` row with values `draft` (default) and `off`. Then run `make sync-dev`, `make verify-sync`, `make lint`, `uv run ruff format --check src/ tests/`, the full suite `uv run pytest -q tests`, and `uv run pytest tests/cli/test_verify_sync_hooks.py tests/unit/test_cli_install.py -q`, and write the outputs, the full-suite pass count and every failing test id (compared with the base-commit record of Task 1) to `./artifacts/final-checks.md`.

Acceptance criteria:
- `grep -n "merge-guard" docs/user-guide/commands.md docs/user-guide/flags.md` shows the usage entry, the paragraph and the flags row; the paragraph names the clear command and the unverified-until-release-gate statement.
- `make verify-sync` exits 0, the full suite `uv run pytest -q tests` shows no failing test id that is absent from the base-commit record of Task 1, and `uv run pytest tests/cli/test_verify_sync_hooks.py tests/unit/test_cli_install.py -q` passes; `make lint` and `uv run ruff format --check src/ tests/` exit 0, or every remaining failure is listed in `./artifacts/final-checks.md` as present in the base-commit record of Task 1.
- `git status --short` lists changes only under `src/superclaude/`, `tests/`, `docs/user-guide/`, `.dev/` and gitignored `.claude/` mirrors; no `.claude/` path other than `.claude/settings.json` is staged, and `.dev/tasks` is staged with `git add .dev/tasks`.
```

## Coverage slice

All 84 inferred rows (Pass 1 found 0 parsed ids). Matrix file: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/eval-workspaces/shadow-model-combos/runs/pre-TASK-WF-designSpec-20261107-075614-comboC-r2/artifacts/coverage-matrix.json

| Requirement | Spec cite | Status | Best task (ratio) |
|---|---|---|---|
| INF-001: default on at `--monitor 3` via `--merge-guard {draft,off}` | source.md:6 | covered by Task 12 | Task 12 (1.0) |
| INF-002: release when the fix push is confirmed on the PR head, befor | source.md:6 | covered by Task 8 | Task 8 (0.8889) |
| INF-003: an unreadable timeline or an exit with unpublished fixes kee | source.md:6 | covered by Task 8 | Task 8 (0.7778) |
| INF-004: draft not label; engage at the first verified Medium-or-high | source.md:6 | covered by Task 8 | Task 8 (0.8) |
| INF-005: Rule: the core DECIDES and the SKILL performs, the same spli | source.md:51 | unmapped | Task 1 (0.5385) |
| INF-006: Nothing mutates. A held guard found in the log is reported w | source.md:57 | unmapped | Task 8 (0.5556) |
| INF-007: Wave 0 loads the ref (Resume and Exit report) before Wave 1: | source.md:58 | covered by Task 8 | Task 8 (0.6923) |
| INF-008: Wave 0 prints once: "Remediation is unprotected: --merge-gua | source.md:59 | covered by Task 9 | Task 9 (1.0) |
| INF-009: The final report prints "PR #N is still mergeable; this run' | source.md:60 | covered by Task 9 | Task 9 (0.8889) |
| INF-010: Read, decide, request, `--to draft`, settle. Print the clear | source.md:61 | covered by Task 8 | Task 8 (0.6667) |
| INF-011: Settle `skipped/already_draft`, phase `disabled`, never muta | source.md:62 | covered by Task 3 | Task 3 (0.8571) |
| INF-012: Release, cause `no_edits`. | source.md:63 | covered by Task 4 | Task 4 (1.0) |
| INF-013: Script `--read` must show `state == OPEN`; otherwise halt `p | source.md:64 | covered by Task 8 | Task 8 (1.0) |
| INF-014: Release, cause `pushed`, before reply, resolve and the S5a r | source.md:65 | covered by Task 8 | Task 8 (0.75) |
| INF-015: Settle `skipped/user_override`, phase `disabled`, no more dr | source.md:66 | unmapped | Task 3 (0.5455) |
| INF-016: Do not release; report `held (timeline unreadable)`; keep pu | source.md:67 | covered by Task 8 | Task 8 (0.625) |
| INF-017: Halt before any edit: `terminal_halted`, reason `draft_guard | source.md:68 | covered by Task 8 | Task 8 (1.0) |
| INF-018: PR stays draft; report `held` with the clear command. | source.md:69 | covered by Task 8 | Task 8 (0.8571) |
| INF-019: No `gh` or `git` word on any line, comments included (F6). I | source.md:75 | covered by Task 3 | Task 3 (0.7692) |
| INF-020: `ValueError` otherwise or when `n < 1`. Never collides with  | source.md:101 | covered by Task 3 | Task 3 (0.6) |
| INF-021: 1 + the highest `<kind>-<n>` seen in any event's `cycle_id`; | source.md:102 | covered by Task 3 | Task 3 (0.6667) |
| INF-022: Guard requests with no matching settle, matched by `idempote | source.md:104 | covered by Task 3 | Task 3 (0.8333) |
| INF-023: so a zero-edit cycle after a fixing cycle still releases wit | source.md:107 | covered by Task 11 | Task 11 (0.8571) |
| INF-024: whether written by the push triad or synthesized by recovery | source.md:108 | unmapped | Task 1 (0.375) |
| INF-025: a test imports both modules and asserts equality, because th | source.md:109 | unmapped | Task 3 (0.4545) |
| INF-026: phase `DISABLED` with cause `already_draft` gives `off` (the | source.md:112 | covered by Task 3 | Task 3 (0.7273) |
| INF-027: `failed_mutations` keeps a call that failed on the client bu | source.md:127 | covered by Task 4 | Task 4 (0.6) |
| INF-028: `mode == OFF`, or `ordinal < 3`, or `is_conflict_cycle(cycle | source.md:133 | covered by Task 3 | Task 3 (1.0) |
| INF-029: `RETRY_RELEASE` (release first, then re-decide) | source.md:137 | covered by Task 1 | Task 1 (0.6) |
| INF-030: `HALT_UNAVAILABLE(timeline_unreadable)` | source.md:140 | unmapped | null (0.0) |
| INF-031: `ENGAGE`; `notes` carries `auto_merge_armed` when set | source.md:143 | covered by Task 4 | Task 4 (0.8) |
| INF-032: `push_completed` and `read.head_sha == target_sha` | source.md:156 | covered by Task 4 | Task 4 (0.75) |
| INF-033: `HOLD(head_mismatch or push_not_completed)` | source.md:157 | unmapped | Task 4 (0.3333) |
| INF-034: `(ordinal < 3 or mode == OFF)` and phase not in (`RELEASED`, | source.md:164 | covered by Task 3 | Task 3 (1.0) |
| INF-035: `RECONCILE`, with `reason` one of `resume_reconciled`, `not_ | source.md:165 | covered by Task 4 | Task 4 (1.0) |
| INF-036: re-enter `release_decision` with `push_completed=True` | source.md:166 | covered by Task 4 | Task 4 (1.0) |
| INF-037: 43 to 45, update the docstring and the `models.py:3,24` coun | source.md:175 | covered by Task 2 | Task 2 (0.7273) |
| INF-038: appended and fsynced BEFORE the draft/ready call | source.md:178 | covered by Task 7 | Task 7 (0.6) |
| INF-039: `idempotency_key` = `guard:<run_id>:<cycle_id>:<to>:a<k>` | source.md:184 | covered by Task 3 | Task 3 (0.75) |
| INF-040: `run_log.rebuild_state()` stores it as `state["draft_guard"] | source.md:187 | covered by Task 5 | Task 5 (0.7778) |
| INF-041: For a draft request that was the first guard record, the who | source.md:201 | covered by Task 3 | Task 3 (0.8571) |
| INF-042: `original_is_draft` is never read from GitHub after the firs | source.md:208 | covered by Task 3 | Task 3 (0.8333) |
| INF-043: `SkillArgs.merge_guard: str = DEFAULT_MERGE_GUARD` | source.md:215 | covered by Task 6 | Task 6 (1.0) |
| INF-044: Effective only at `--monitor 3`; accepted and inert below. | source.md:216 | unmapped | Task 12 (0.4) |
| INF-045: `RunConfig` and `run_skill` do not change (F5) | source.md:217 | unmapped | Task 6 (0.4) |
| INF-046: `set -euo pipefail`, same `die`, same `--repo` resolution fr | source.md:221 | covered by Task 7 | Task 7 (0.875) |
| INF-047: `gh pr view "$PR" --repo "$REPO" --json state,isDraft,headRe | source.md:230 | covered by Task 7 | Task 7 (0.8889) |
| INF-048: `gh pr ready "$PR" --repo "$REPO" --undo` | source.md:231 | covered by Task 7 | Task 7 (0.8) |
| INF-049: Exit codes: 0 success; 1 `gh` failure or failed verification | source.md:234 | covered by Task 7 | Task 7 (0.7059) |
| INF-050: A verification mismatch after a mutation is `ok:false, error | source.md:234 | covered by Task 7 | Task 7 (0.8571) |
| INF-051: Loaded lazily at L3 Wave 3, Wave 6 and Wave 8. | source.md:240 | covered by Task 8 | Task 8 (0.75) |
| INF-052: The Wave 0 bullet is a flat line placed before the Wave 1 bu | source.md:241 | covered by Task 9 | Task 9 (1.0) |
| INF-053: it must not contain the words `evidence-validator` or `confl | source.md:241 | covered by Task 9 | Task 9 (0.8571) |
| INF-054: No new python fence | source.md:241 | covered by Task 9 | Task 9 (1.0) |
| INF-055: update it to 45 and name `draft_guard_requested` and `draft_ | source.md:242 | covered by Task 2 | Task 2 (1.0) |
| INF-056: Respect the wait-only sentences pinned at `test_static_grep. | source.md:243 | covered by Task 1 | Task 1 (0.7143) |
| INF-057: `--merge-guard {draft,off}` in the argument-hint and the Opt | source.md:244 | covered by Task 12 | Task 12 (1.0) |
| INF-058: A `held` report always carries the reason and `gh pr ready < | source.md:247 | covered by Task 8 | Task 8 (0.8889) |
| INF-059: uses the same id as the `cycle_id` of the push triad (`push_ | source.md:251 | covered by Task 8 | Task 8 (0.8571) |
| INF-060: With `--merge-guard off` nothing changes. | source.md:251 | covered by Task 8 | Task 8 (0.8) |
| INF-062: Acceptance trace (must appear in this order in the run log) | source.md:270 | covered by Task 11 | Task 11 (0.8333) |
| INF-063: Message names `--merge-guard off` and prints the clear comma | source.md:274 | covered by Task 8 | Task 8 (0.875) |
| INF-064: phase stays `HELD`; report `merge_guard: held` plus the clea | source.md:275 | covered by Task 8 | Task 8 (0.625) |
| INF-065: W6 blocks the push (INV-016 predicate 5), `release_decision= | source.md:276 | unmapped | Task 4 (0.3333) |
| INF-066: `classify_toggles == foreign` -> `settled(skipped, user_over | source.md:277 | unmapped | Task 3 (0.4545) |
| INF-067: the request settles `skipped/not_applied`, the phase returns | source.md:278 | covered by Task 3 | Task 3 (0.7273) |
| INF-068: `not_landed` keeps the PR draft (row 5); `ambiguous` holds ( | source.md:279 | covered by Task 4 | Task 4 (0.8571) |
| INF-069: The SKILL passes `published = held_cycle_published(events, g | source.md:280 | covered by Task 3 | Task 3 (0.8) |
| INF-070: `state != OPEN` -> halt `pr_not_open`, nothing pushed, repor | source.md:281 | covered by Task 8 | Task 8 (0.9) |
| INF-071: count 43 to 45 at `test_run_log.py:171-175` and `test_codex_ | source.md:299 | covered by Task 2 | Task 2 (0.6667) |
| INF-072: Record `make lint`, `uv run ruff format --check src/ tests/` | source.md:301 | covered by Task 1 | Task 1 (0.9231) |
| INF-073: Never stage `.claude/`. | source.md:301 | unmapped | Task 3 (0.3333) |
| INF-074: Unchanged and must still pass: `test_idempotency.py:89` (7 s | source.md:301 | covered by Task 2 | Task 2 (0.6364) |
| INF-075: never injected strings | source.md:318 | covered by Task 8 | Task 8 (0.6667) |
| INF-076: A static test asserts `merge_guard.py` has no `gh` or `git`  | source.md:322 | covered by Task 3 | Task 3 (1.0) |
| INF-077: the script test for a missing `jq` (exit 127) | source.md:322 | covered by Task 7 | Task 7 (1.0) |
| INF-078: No task makes a live PR call, and the run that opens the PR  | source.md:326 | covered by Task 1 | Task 1 (0.8333) |
| INF-079: The user guide states that draft behaviour is unverified unt | source.md:326 | covered by Task 1 | Task 1 (1.0) |
| INF-081: one `Depends on:` line per dependency | source.md:363 | covered by Task 7 | Task 7 (0.75) |
| INF-082: The protocol wiring covers the Wave 0 resume and `off` hook  | source.md:364 | unmapped | Task 9 (0.5833) |
| INF-083: Protocol prose written by the plan never carries `file:NNN`  | source.md:369 | unmapped | Task 8 (0.5556) |
| INF-084: scenario tests import only helpers and fixtures from `test_s | source.md:377 | covered by Task 11 | Task 11 (0.7) |
| INF-085: "no push after a `pr_not_open` halt" is asserted on `RunLog. | source.md:377 | covered by Task 11 | Task 11 (0.8333) |
| INF-086: its acceptance criterion is a test that the literal line is  | source.md:374 | covered by Task 1 | Task 1 (0.8571) |
