# OPEN DECISIONS: issue 463 research task

**Written:** 2026-11-15. **Read `HANDOFF.md` first** (same folder) for what this task is and where it stands. This file lists only what a person with authority over the task must answer before work can continue, plus items deliberately deferred.

**Context in two lines:** the task researches whether a model-plus-effort router is feasible for `ccsession` (issue #463, research only, nothing gets built). It is stopped at Phase 1 item 1.3 because its own halt rule fired: the independent check of the work-splitting plan failed in two rounds without shrinking. No actual research has been done yet.

**Who decides:** the issue/task owner (the user who started `/task`). An agent may apply the answer; an agent may not pick for the owner.

## Ledger

| ID | Question | Status | Blocking? |
|---|---|---|---|
| D1 | How to proceed after the allocation-gate halt | **OPEN** | Yes: nothing else can run |
| D2 | Ratify the executor launching workers itself | **OPEN** | No (work already done this way) |
| D3 | Rule on a conflicting field-name contract in the QA role vs the template | DEFERRED | Only if a later gate trips on it |

---

## D1. How to proceed after the allocation-gate halt  (OPEN, blocking)

**Situation.** Item 1.3 requires an independent PASS on the plan that splits 16,719 lines of source and tests into 42 worker assignments of at most 1000 lines each. Round 1: 4 of 5 topic checks failed (one could not launch). I fixed the plan (v2). Round 2: all 5 failed, 14 blocking findings (13 in round 1). The task's rule `[HALT-MONOTONICITY] |F|=5` requires a stop and an owner ruling. The cap itself would allow one more fix and one more review (1 of 2 fix cycles, 2 of 3 reviews used).

**What the findings are.** Mechanical plan defects: cut points that land in the middle of a test or function while the plan claims whole-test edges; context budgets estimated instead of measured; a few relevant call sites or fixtures assigned to no worker (the full register is in `qa/local-allocation-acceptance.md`). The verifiers confirmed the line-range unions are complete. None is a disagreement about what to research.

**Cost fact you should have.** After this gate: about 42 source workers plus 42 independent coverage checkers, merge/reconciliation passes, five canonical findings files, then a 10-plus-reviewer local gate, three external-research workers, four synthesis files with a gate, report assembly with parallel lens reviews, source fidelity and anti-omission passes, and a final independent post-check. 120 checklist items are still open. So far the allocation gate has used 11 worker launches (6 in round 1 including one accidental duplicate, 5 in round 2), on top of 7 for the item 1.1 preparation.

**Options**

1. **Authorize one more correction (v3) built mechanically, then one final review round. (Recommended)**
   - Method: first generate one index of every function and test start line in the 18 files (a single batched grep run), snap every cut to the nearest earlier index line instead of hand-picking numbers, and replace estimated context with counted line totals. Fold in the 14 register findings. Re-run the five checks (new cycle-3 items).
   - Why: every finding is a hand-picked-number error that an index removes; the unions already pass.
   - Risk: if v3 fails, the 3-review cap is spent and you must pick option 2, 3 or 4 anyway. Roughly 5 more verifier launches plus the correction.
2. **Relax the allocation contract** (for example allow cuts inside tests when a one-line overlap and edge note is declared, or raise or drop the per-slice coverage checkers). Fewer failures likely, but this edits the task's own rules (task file lines 140-161 and the Phase 1 items), which agents are forbidden to do; the owner must make or approve that edit explicitly.
3. **Set this task aside and commission proportionate research instead** (for example `/tech-research` scoped to the four acceptance boxes in the issue: compare the public router and alternatives, resolve who "Jev" is, map the session/proxy integration points, give a recommendation). All artifacts here stay as evidence. You lose the task's independent-gate and anti-omission guarantees.
4. **Stop.** Leave issue #463 open and unresearched.

**Recommendation:** option 1. Reason: lowest cost to keep the full evidence guarantees, and the failure mode is removable by method, not by luck. If you would rather not spend more on process, option 3 is the honest alternative; option 2 is the one I would avoid because it changes the rules mid-run.

**What happens on your answer.** Option 1: the executor resumes `/task <task file>`, rewrites `qa/local-source-allocation.md` as v3, emits cycle-3 check items, dispatches five verifiers, and fills `qa/local-allocation-acceptance.md`. Option 2: you edit the rules first; then as option 1. Options 3 and 4: executor records the ruling in the Execution Log and stops.

**Answer:** _(not yet given)_

---

## D2. Ratify the executor launching workers itself  (OPEN, not blocking)

**Situation.** The task names coordinator terminal `term_4db4c124-3b58-4b9e-be54-c53aed3ceac8` as the only way to launch workers. It no longer exists. The live issue-463 session I asked to take over (`issue-463-1109-021326-50bc`) refused: it is a settled worker with no live pane and runs a different model tier. So the person-opened `/task` session created Orca Run `run_c974cafd0eb6` and launched all workers itself with `worker-start --model claude-gw-tier1b`, verifying the backend model each time (HANDOFF.md section 5). The task text still names the dead terminal; I did not edit it, because rewriting items is prohibited.

**Options:** (a) ratify: record that executor-launched Tier1b workers satisfy the worker contract; (b) require a fresh coordinator session to launch workers from here on (more setup, same workers).

**Recommendation:** (a). It is already how everything on disk was produced, and each launch was verified.

**Answer:** _(not yet given)_

---

## D3. Conflicting field names between the QA role and the task template  (DEFERRED)

**Situation.** Recorded in `qa/qa-research-entry-disposition-ctx5f6c.md` (2026-11-09, check 5): the installed `rf-qa` role requires frontmatter fields `created`/`template`/`tracks`, while the governing Template 02 and the `/task` skill use `created_date`. Both versions are preserved; no compatibility was invented. It has not blocked anything yet.

**Decide only if** a later phase-gate QA fails on this mismatch. Then the owner picks which contract wins. **Recommendation:** defer until it actually trips.

**Answer:** _not needed yet_

---

## Not decisions, but things the next person must do

- Settle or verify the six Orca workers left in `unverifiable` state (HANDOFF.md section 6, item 6). Do not release on absence alone.
- `.dev/issues/463/` is untracked and intentionally not committed.
- Task constraint (task file, Key Constraints item 2) still binds: every session and helper uses coordinator-verified `claude-gw-tier1b`; no Opus or Tier1a, no fallback models, no nested workers.
