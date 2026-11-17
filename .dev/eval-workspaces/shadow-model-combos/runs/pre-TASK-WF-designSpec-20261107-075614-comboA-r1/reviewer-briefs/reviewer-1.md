# Reviewer 1 brief — persona: analyzer (root-cause / deviation lens)

Audit target: UC-1 pre-execution. Spec = `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md` (design spec v3, issue #375, pr-submit merge guard). Plan = `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md` (13 tasks, 5 phases).

ATTRIBUTION NOTE (binding): this is a PRE-execution audit of the frozen spec↔plan pair. The spec's facts F1-F13 are pinned at base commit e8db2fe6 (2026-11-07). HEAD has since evolved (the feature landed as commit 0b8a5801d); do NOT file findings that rest on HEAD source text — audit the plan's coherence against the frozen spec only.

Your lens: decision-table fidelity, behavior coverage, internal contradictions, unpassable checks. The spec's section 4.1 defines three first-match decision tables (engage 11 rows, release 9 rows, resume 9 rows), the fold effect table (4.2) and guard_status mapping. Verify Tasks 3, 4, 5, 11 carry every row faithfully and that every AC is mechanically falsifiable.

## T1 card excerpt

Verbatim excerpt from t1-card.md (deviation-relevant slice):

> ## Findings (hypotheses — for Tier 2 review)
>
> - **H1 (wording tension, MINOR candidate).** The Wave 0 SKILL.md bullet must itself carry the L3/`--merge-guard off` print clause ("at L3 with `--merge-guard off` the line 'Remediation is unprotected...' is printed once", source.md:241) while Task 9's AC says the bullet "contains no `L3 only` or `draft` gate wording" (tasklist:137,140). The AC's "gate wording" qualifier makes it implementable (the load-clause carries no gate; the print-clause names L3), but a test author reading only the AC could ban the token `L3` outright and write an unpassable test. Family: pass-gate wording (shadow06/08/10 recurrence class).
> - **H2 (superset dependency, MINOR candidate).** Task 13 (docs/user-guide) declares "Depends on: Task 2" (tasklist:190); nothing in Task 13 consumes the enum change. Harmless over-sequencing, not a coverage gap. [INFERRED]
> - **H3 (verified conformance).** Dependency completeness per source.md:363: every consumer declares its producers (T5←T3,T4; T8←T1,T4,T7; T9←T6,T8; T10←T9; T11←T3,T4,T5,T7; T12←T6,T8; T13←T2,T10,T11,T12). Every file in the spec's files-to-change table (source.md:283-301) has an owning task. The 12 minimum tests of source.md:307-322 all appear by name in Task 11 (tasklist:169). The classification-last discipline (source.md:255, 373) appears in Tasks 7, 8, 9, 10, 12.
> - **H4 (constraint without explicit AC, MINOR candidate).** source.md:208 "A corrupt line still raises, as it does today" — no task AC names corrupt-line fold behavior explicitly (implicitly held by existing RunLog tests; Task 5's legacy-log AC is adjacent but not the same). Family: constraint without matching AC (shadow06/10 recurrence).

End your card with a ## Findings block holding one fenced findings-v2 block: JSON lines, one object per line, never a table. Fields: id (F1, F2, ...), severity (CRITICAL, MAJOR or MINOR), blocking (true or false; a MINOR finding is never blocking), category (one of contradiction, data-loss, missing-requirement, other, safety, unpassable-check), lens "reflect-pre", claim (one line, at most 300 characters), refs (requirement ids, may be empty) and citations (1 to 8 objects, each with role plan or spec, a repo-relative path, line_start, line_end and an optional quote). Example line: {"id":"F1","severity":"MAJOR","blocking":false,"category":"contradiction","lens":"reflect-pre","claim":"Task 3 says X but task 5 says Y.","refs":["R-1"],"citations":[{"role":"plan","path":"plan.md","line_start":10,"line_end":12}]}. After the block add a reviewer_model_self_report line stating the model you are running as in one line.

Cite with repo-relative paths: spec = `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md`, plan = `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md`. Quote ≤200 chars.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-13T03:03:29Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### source.md:129-171 (engage/release/resume decision tables + guard_status)

```text
`engage_decision`, first matching row wins:
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
| 1 | `guard is None` | `NOOP` |
| 2 | `(ordinal < 3 or mode == OFF)` and phase not in (`RELEASED`, `DISABLED`) | `REPORT_HELD` (no mutation; prints the clear command) |
| 3 | `pending` non-empty | `RECONCILE`, with `reason` one of `resume_reconciled`, `not_applied`, `ambiguous` |
| 4 | phase `HELD` and (`dangling_branch == "landed"` or `published`) | re-enter `release_decision` with `push_completed=True` |
| 5 | `dangling_branch == "not_landed"` and phase `HELD` | `NOOP(held_through_redrive)` |
| 6 | `dangling_branch == "ambiguous"` | `HOLD(ambiguous_remote_tip)` |
| 7 | phase `RELEASE_PENDING` and `owned_draft` | `RETRY_RELEASE` |
| 8 | phase `RELEASE_PENDING` and not `owned_draft`, live draft | `HOLD(ownership_unproven)` |
| 9 | otherwise | `NOOP` |
```

### source.md:196-208 (fold effect table, incl. the not_applied row and the corrupt-line claim)

```text
| `settled(any direction, skipped, not_applied)` | the pending key is cleared and the phase returns to `phase_before_request`; `owned_draft` and the toggle counters are unchanged. For a draft request that was the first guard record, the whole record is erased (the fold returns `None` ...) It is NOT `DISABLED`, so a crash before the call does not leave later cycles unguarded. |
| `settled(draft, confirmed, not changed)` | `phase = HELD`, `owned_draft = True`, no toggle (a retry that finds the PR already draft after a call that failed on the client but landed) |
...
`unsettled` is the count of remembered keys with no settle. A corrupt line still raises, as it does today. `original_is_draft` is never read from GitHub after the first record, so a resumed run cannot mistake its own draft for an original one.
```

### TASK-WF-designSpec-20261107-075614.md:66-78 (Tasks 3 and 4: core functions and decision functions)

```text
Task 4: ... `engage_decision(*, mode, ordinal, cycle_id, guard, read)` (all 11 rows, first match wins, `notes` carries `auto_merge_armed`), `release_decision(*, mode, ordinal, cycle_id, guard, read, applied_edits, target_sha, push_completed)` (all 9 rows; `applied_edits` is the count of edits applied in THIS cycle, not the run-wide output field) and `resume_decision(*, mode, ordinal, guard, read, pending, dangling_branch, published)` (all 9 rows, with the row 2 precedence, the three `RECONCILE` reasons `resume_reconciled`, `not_applied`, `ambiguous` of section 4.1, and `dangling_branch` limited to `None` or the `BRANCH_*` constants of Task 3).
```

### TASK-WF-designSpec-20261107-075614.md:137-144 (Task 9 body + ACs — the H1 tension)

```text
Edit `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md` additively ...: one new bullet under Wave 0, written as a flat line before the Wave 1 bullet, that applies at every ordinal and in both modes and carries no L3 or `draft` condition; it states that on `--resume`, or when the run log already holds guard events, the ref `refs/merge-guard.md` (Resume and Exit report) is loaded before Wave 1 and before any edit, release or re-trigger, and that at L3 with `--merge-guard off` the line "Remediation is unprotected: --merge-guard off." is printed once and no draft call is made.
Acceptance criteria:
- The Wave 0 test fails when the bullet is placed after the Wave 1 bullet, when it names an L3 or `draft` condition, or when the literal `off` line is missing, and passes on the real file.
```

### source.md:241 (the SKILL.md row the Task 9 bullet implements)

```text
The Wave 0 bullet applies at every ordinal and in both modes: on `--resume`, or when the run log holds guard events, it loads the ref (Resume and Exit report) before Wave 1 and before any edit, release or re-trigger; at L3 with `--merge-guard off` it prints the unprotected line once.
```

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|--------------------|---------|--------|-----------|
| INF-001 ordinals 0-2/off no call; held reported on resume | H1-family (Task 11) | covered | source.md:348 |
| INF-002 engage end of Wave 3, once per cycle id, not conflict cycles | Task 8/10 | covered | source.md:349 |
| INF-003 first record, never a live read (original_is_draft) | Task 3 | covered | source.md:350 |
| INF-004 release rows 7-8 (pushed / no_edits), release before reply+re-trigger | Task 8 | covered | source.md:351 |
| INF-005 state/autoMergeRequest in script read | Task 7 | covered | source.md:352 |
