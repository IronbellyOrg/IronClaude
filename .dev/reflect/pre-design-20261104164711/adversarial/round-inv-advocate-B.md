# Round INV — Advocate B (qa card)

## 1. Element verdicts

**E1 (A/B set + 5→4a + 9→4b): ACCEPT.** P:106 ("Depends on: Task 4") and P:171 ("Task 5, Task 6") are unchanged in the plan and both A/B R2 tables — INV-001 is real; C called it first. With the two edges, every edge points backward in the E2 order (acyclic), and Task 9's closure {5, 4a, 3, 2, 6, 4b, 7} covers every S:741-749 name, including 4b's `conflict_resume_plan`/`crash_resume_plan` (P:92) — INV-002's ImportError becomes impossible. Condition: the set must include my Task 8 re-point (P:155 → 4b); name it in the fix text.

**E2 (4b between Task 7 and Task 8): ACCEPT.** IMPL:97 runs "default sequential in source order"; IMPL:79 ignores `depends-on`; grep of P for `independent|parallel` finds nothing — document order is execution order, so placement is load-bearing. At that slot, 4b's edges (4a, 5, 7) and consumers (8, 9) sit correctly; no other task moves.

**E3 (split P:95-100 ACs; t4a/t4b logs): ACCEPT.** Also closes INV-012: P:99 mixes 4b's `conflict_resume_plan` with 4a's `prior_conflict_cycles`; P:100 names one log.

**E4 (Task 3 Depends on: Task 1, Task 2): ACCEPT.** P:66 lists Task 2 only; Task 1 has no Depends-on line; both edit `test_static_grep.py` (P:40, P:75). Closes INV-007; Task 18 stays ordered via 18→17→1.

**E5 (INV-006; lower CF-01/02/03/04/17/22 M→L): QUALIFY — concede.** My Mediums rested on A-003 (graph-ordered or parallel execution); IMPL:79 + IMPL:97 refute that premise for this executor, and INV-003 shows each edge is already satisfied by document order. I accept Low and keeping the fixes, provided INV-006's wording scopes the regrade to document-order execution, so a future graph-order executor re-opens the cards.

## 2. Invariant coverage

- **INV-001: fully addressed** (E1 rewrites P:106; cycle and missing path closed).
- **INV-002: fully addressed** (E1 adds 9→4b; E2 places 4b before 9 in execution order).
- **INV-005: fully addressed** (E2 fixes 4b's document position; no other task moves).

Also closed: INV-012 (E3), INV-007 (E4). Remaining open: INV-014 only (Low, C-specific, moot here).

**Verdict: ACCEPT R-INV; all three HIGH blockers resolved; the gate can pass.**
