# Design Spec: pr-submit merge guard (issue #375)

- Type: component design, format spec
- Input requirements: `.dev/brainstorms/20261107-062111-pr-submit-draft-guard/merged-requirements.md` (FR-1..FR-23, decisions D1..D7)
- Issue: https://github.com/IronbellyOrg/IronClaude/issues/375
- Owner decisions (accepted 2026-11-07, relayed by the coordinator): draft not label; engage at the first verified Medium-or-higher finding routed to a fix; default on at `--monitor 3` via `--merge-guard {draft,off}`; release when the fix push is confirmed on the PR head, before replies and the re-trigger; an unreadable timeline or an exit with unpublished fixes keeps the PR draft and reports.
- Status: design only. No source file is changed by this document.

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
| `release_decision(*, mode, ordinal, cycle_id, guard, read, applied_edits, target_sha, push_completed)` | Table below. |
| `resume_decision(*, mode, ordinal, guard, read, pending, dangling_branch)` | Table below. |
| `guard_status(guard, mode, ordinal)` | `"off"`, `"released"`, `"held"`, `"user_override"`, `"unavailable"` for the output field `merge_guard`. |

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
| 2 | `ordinal < 3` or `mode == OFF` and guard not released or disabled | `REPORT_HELD` (no mutation; prints the clear command) |
| 3 | `pending` non-empty | `RECONCILE`: live draft state and `classify_toggles` decide; live state matching the request's direction and `observed == run_toggles + 1` settles `confirmed, changed: true, cause: resume_reconciled`; live state not matching settles `skipped, cause: not_applied`; anything else `HOLD(ambiguous)` |
| 4 | `dangling_branch == "A"` (push landed) and phase `HELD` | re-enter `release_decision` with `push_completed=True` |
| 5 | `dangling_branch == "B"` (not landed) and phase `HELD` | `NOOP(held_through_redrive)` |
| 6 | `dangling_branch == "C"` | `HOLD(ambiguous_remote_tip)` |
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
phase, cycle_id, original_is_draft, baseline, run_toggles, unsettled,
failed_mutations, owned_draft, disabled_cause
```

| Event | Effect |
|---|---|
| `requested(to=draft)` | `phase = ENGAGE_PENDING`; remember the key as pending; first request sets `baseline` and `original_is_draft` |
| `requested(to=ready)` | `phase = RELEASE_PENDING`; remember the key |
| `settled(draft, confirmed, changed)` | `phase = HELD`, `owned_draft = True`, `run_toggles += 1` |
| `settled(draft, failed)` | `phase = RELEASE_PENDING`, `failed_mutations += 1`, `owned_draft` unchanged |
| `settled(draft, skipped)` | `phase = DISABLED`, `disabled_cause = cause`; a first skip also sets `original_is_draft` |
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
| `SKILL.md` | One short bullet under each of Wave 3, Wave 6 and Wave 8 pointing at the ref (new sentences; the pinned Wave 0/4/6/8 sentences are not edited); one row `merge_guard` in the output table; one line in the wave structure list. No new python fence (the one-fence tests, `test_cosmos_protocol.py:34-44`, `test_codex_reviews.py:685-697`). |
| `refs/state-machine.md` | Overlay note: the guard phases are fold values, not `MonitorState` members. Respect the wait-only sentences pinned at `test_static_grep.py:791`. |
| `commands/pr-submit.md` | `--merge-guard {draft,off}` in the argument-hint and the Options table; a short "Merge guard" section next to "Merge-conflict handling". |
| `docs/user-guide/commands.md`, `docs/user-guide/flags.md` | Flag row and a paragraph: what it does, the clear command, `held` meaning, default on. |

Output field `merge_guard`: `off`, `released`, `held`, `user_override`, `unavailable`. A `held` report always carries the reason and `gh pr ready <N> --repo <REPO>` (formatted by the SKILL, never by the core, because the core cannot contain `gh`). At L2 the final report adds: "PR #N is still mergeable; this run's fixes are local only."

### 4.6 Cycle identity

`fix_cycle_id` gives guard-enabled cycles an explicit id: `fix-<n>` for review-fix cycles and `ci-<n>` for CI-fix cycles, `n` from `next_cycle_number`. The SKILL mints it at the end of Wave 3 and uses the same id as the `cycle_id` of the push triad (`push_idempotency_key`) and of `rereview_requested`, so the guard, the push and the re-trigger of one cycle share a key. With `--merge-guard off` nothing changes. The build must first confirm where the SKILL assigns a fix cycle's id today and keep exactly one source for it (open item O1).

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
| Crash between request and settle | `--resume`: `pending_requests` non-empty -> `RECONCILE` with a live read. |
| Crash after `push_completed`, before release | Branch A: `resume_decision` row 4 releases first, then the S5a logic of `refs/review-retrigger.md` runs. |
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
| `.../SKILL.md`, `.../refs/state-machine.md` | edit | additive only |
| `src/superclaude/commands/pr-submit.md` | edit | flag and section |
| `docs/user-guide/commands.md`, `docs/user-guide/flags.md` | edit | flag and paragraph |
| `tests/pr_submit/test_merge_guard.py`, `test_set_draft_state.py` | new | section 7 |
| `tests/pr_submit/test_run_log.py`, `test_codex_reviews.py`, `test_static_grep.py`, `test_skill_parse.py` | edit | count 43 to 45 at `test_run_log.py:171-175` and `test_codex_reviews.py:441`; `"draft_guard": None` at `test_run_log.py:312`; `merge_guard.py` into the zero-token file set; script lists only after checking each list's purpose; flag default and choices test mirroring `--conflict-max-tier` |

After editing under `src/superclaude/`: `make sync-dev`, then `make verify-sync`. Never stage `.claude/`. Unchanged and must still pass: `test_idempotency.py:89` (7 sets), the one-python-fence tests, `test_conflict_sync_protocol.py:576` (no `src/superclaude` text in skill or command files).

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
| `test_guard_crash_boundaries_and_push_recovery_abc` | crash before and after each request and settle; Branch A, B, C; engage, crash, resume with live draft true stays `held`, never `disabled` (FR-7, FR-21) |
| `test_guard_closed_merged_or_moved_head_forbids_mutation` | `pr_not_open`, moved head, nothing pushed (FR-10) |
| `test_guard_script_contract_scoping_and_legacy_fold` | fake `gh` on PATH, exit codes 0/1/2/127, `--repo` on every call, an old log folds to `draft_guard: None` |

Unit tables for `engage_decision`, `release_decision`, `resume_decision` and `classify_toggles` cover every row of section 4.1. Add the acceptance trace of section 5 as a fixture over `RunLog`. A static test asserts `merge_guard.py` has no `gh` or `git` word.

## 8. Pre-build gate (FR-23) and open items

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
- **O3** Exact-text pins on `pr-submit.md` (argument-hint, Options table) and `SKILL.md` that the additive edits must not break; grep before editing.
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
