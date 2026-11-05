# Invariant round — Advocate C (refactorer card)

Sources re-read: P (plan) :35-189 and a grep of every `Depends on` / `Task 4` reference; IMPL = `sc-implement-protocol/SKILL.md` :71, :75, :79 ("Ignore MDTM fields (`depends-on` ...)"; the probe cites it as :77), :97 ("Default sequential in source order"). P has no `independent` or `parallel-ok` marker.

**Concession.** I drop my preferred edge set (5 on 4b). Under IMPL:79/:97 it only holds if Task 7 (P:137) moves above Task 5 (P:104). Nobody proposed that move, and it is stricter than spec step 4 (INV-014). R-INV is my own round-2 fallback (R2-C:20), with the document position added.

| # | Verdict | Evidence |
|---|---|---|
| 1 | ACCEPT | Order 1,2,3,4a,5,6,7,4b,8,9 puts every edge earlier in the order: 4b→4a,5,7; 5→4a; 8→4b,7; 9→5,6,4b. There is no cycle. Task 9's closure now reaches 4b, so the `__init__` exports (S:744) resolve. P:106 "Task 4" becomes "Task 4a". P:155 becomes "Task 4b, Task 7" (B's change). |
| 2 | QUALIFY | Correct and load-bearing (IMPL:97). The 4b heading must read `## Task 4b: ...` with body text (IMPL:71, :75). It sits under "Phase 3: Changes to the existing core modules" (P:102), so the heading text should say it extends `conflicts.py`, or Phase 3 should be renamed. This is cosmetic only. |
| 3 | QUALIFY | P:96-98 go to 4a. P:99 is mixed: its `prior_conflict_cycles(...) == 0` clause is a 4a function (P:91) and must move to 4a, and the rest goes to 4b (INV-012). P:93's test list must be split the same way (Resume cases go to 4b). One residue is outside R-INV: the prose at P:241 says "from Task 4" for `parse_resolution_record`, and it should say Task 4a. |
| 4 | ACCEPT | Task 1 (P:35) has no Depends-on. Task 3 (P:66) depends only on Task 2. Both edit `test_static_grep.py` (P:40, P:75). The new edge points backward, so it creates no cycle. Under document order the problem stays latent, so the severity is Low. |
| 5 | QUALIFY | True for the stated executor: every listed edge points backward in the new order, including 10→4a and 15→4a. A halt STOPs the run (IMPL:97b). Two conditions apply. (a) The lowered severities hold only while P marks no set `independent`/`parallel-ok`; record that as the condition. (b) Only the edge part of CF-03 is lowered. Its header-match grep stays in the fix. |

## INV status under R-INV
- **INV-001: fully addressed.** Element 1 changes P:106 to 4a, which breaks the 4b→5→4b cycle.
- **INV-002: fully addressed.** 9→4b is in the graph, and in document order 4b (after 7) runs before Task 9.
- **INV-005: fully addressed.** Element 2 states 4b's position, and no existing task moves. The element 2 heading qualification is still required.

Gate: unblock, provided the element 3 and element 5 qualifications are written into the fix.
