# Invariant round: Variant A advocate

P = plan, IMPL = sc-implement-protocol SKILL.md.

| Element of R-INV | Verdict | Evidence |
|---|---|---|
| Adopt A/B CF-05 set, plus "5 on 4a" and "9 on 4b" | ACCEPT | With 4a on 3, 5 on 4a, 4b on 4a/5/7, 8 on 4b/7, 9 on 5/6/4b, every edge points backward in the proposed document order, so there is no cycle. Task 9's closure is {5, 6, 4b, 4a, 3, 2, 7}. Four text edits are needed: P:106, P:155, P:171, and P:241 ("from Task 4" becomes 4a). R-INV omits P:241. |
| Put 4b between Task 7 and Task 8 | ACCEPT | IMPL:97 runs tasks sequentially in source order. IMPL:79 ignores `depends-on` (INV-005 cites :77, the text is at :79). P has no `independent` or `parallel` marker (grep: no match). IMPL:71 turns `## Task 4b` into `T4b`, which the ledger regex accepts. Resume walks T1..TN in source order (ledger.md:125), so an id that is out of numeric order is harmless. Give 4b a body sentence saying why it sits there. |
| Split P:95-100 into 4a and 4b ACs; logs t4a/t4b | QUALIFY | P:99 mixes `conflict_resume_plan` (4b) with `prior_conflict_cycles` (4a). `crash_resume_plan` (P:92) has no AC at all. The P:93 test bullet must be split too: the Resume cases go to 4b, and everything else (router, gates, branch-literal equality, REPORT/HALT sets) stays in 4a. P:100 must also be renamed. |
| Task 3 on Task 1, 2 | ACCEPT | Task 1 rewrites `test_static_grep.py:654-661` (P:40) and Task 3 edits `CORE_PURE_FILES` in the same file (P:75). S:1416 and S:1418 leave them unordered. The edge is backward and Task 1 has no dependency, so it is acyclic. |
| Record INV-006; lower CF-01/02/03/04/17/22 to Low | QUALIFY | Every one of those edges is already satisfied by document order, so only order is affected (my R2 rule: Low). I accept the downgrade for CF-01/02/04/17/22. CF-03 also carries the header-match grep fix, which stays; its dependency is met because Task 13 comes before Task 16. Condition: state that Low holds only while no `independent` or `parallel-ok` marker is added (IMPL:97). |

## Per-invariant outcome

- **INV-001: fully addressed.** Rewriting P:106 to 4a removes the cycle 4b → 5 → 4b.
- **INV-002: fully addressed.** "9 on 4b" puts `conflict_resume_plan` and `crash_resume_plan` in Task 9's closure before the `__init__` import (S:744).
- **INV-005: fully addressed**, but only once the 4b heading is physically moved. Edges alone do nothing under IMPL:97.
