# Round 1: Advocate for Variant 3 (opus class, refactorer)

## Position summary
Variant 3 is right that C-001 and C-002 both block the plan, and it adds the strongest evidence for each: source.md:17 for C-001 and the undecided OD10 for C-002. But Variant 3 missed C-003, C-004 and C-005. Variant 1 makes the more complete case on C-002, and Variant 2 is right that C-004 blocks.

## Steelman
**V1:** It has the widest coverage. On C-002 it closes the escape route Variant 3 left open: the tracked `.dev/experiments/.../finding-grader.md` copy is in the repository, but Task 5 forbids any `.dev/` string in the skill folder (PLAN:87). I confirmed its C-003 hits: `remediate_parser.py` and `fmea_classifier.py` contain the phrases. It over-grades C-003 and C-010, though.
**V2:** It alone treats C-004 as blocking, and the spec backs it. SPEC:404 says "A mapping rule from its rows to `review-ledger/1` rows is left to the `/sc:workflow` plan", and SPEC:945 lists "ledger adapters" as a stage 1 deliverable. No task in the plan produces either one. Its C-002 argument never deals with the tracked `.dev/` copy.

## Strengths claimed
1. **C-001 rests on the source request, not only on the plan's own rule.** source.md:17 says lines a later task makes false "get an end point (\"until Task N\")". The stage ledger README:33 repeats it, and README:33 also makes acceptance lines standing at the final review. Task 10 says "Reuse the reader of Task 7" (PLAN:148), and Task 7's check says "shows only the new module and its command wiring" (PLAN:115).
2. **The `__pycache__` point holds.** `src/superclaude/cli/review/__pycache__/` exists today. `grep -rn` reads files on disk, not only tracked files, so it will also list compiled `.pyc` files.
3. **The OD10 point holds.** PLAN:21 says OD10 is undecided and "no task depends on a different answer". Yet Task 3 needs a stoprule file in the repository, which SPEC:582 says means "adding it to src or writing a new agent (OD10)". `src/` and `plugins/` contain no stoprule or finding-grader file today.

## Weaknesses identified in the other variants
1. **V1 C-003 is real but does not block stage 1.** Task 3's acceptance line says it "lists" the auggie file and the others; it never says "only". SPEC:845 says both code files are "Not changed", so an executor can add them and still pass every stage 1 line. T5 is also not a stage 1 exit test (SPEC:945 lists "T1 to T4, T6 to T8, T11 to T13 and T17").
2. **V1 C-010 is not a defect.** PLAN:25 is a standing order: "Edit there, then run `make sync-dev`".
3. **V2 F2** does not show why the tracked `.dev/experiments` copy fails the check. Only V1's argument through Task 5 does.

## Concessions
- Variant 3 missed C-003, C-004 and C-005.
- Its F1 wrongly ties "never reads `~/.claude`" to T4. That clause belongs to T3 (PLAN:209).
- Its C-002 case is weaker than V1's, because the `.dev/experiments` copy is tracked (`git ls-files` lists it).
- C-008 is only a latent risk: T2's strict mode is "off in this phase" (PLAN:209), and `doctor.py` can match the fence with a pattern rather than the literal opener.

## Per-point positions
S-001 | winner: tie | verdict: N/A | layout only
S-002 | winner: tie | verdict: N/A | citation format only
C-001 | winner: variant 3 | verdict: BLOCKING-REAL | PLAN:115 vs PLAN:148; source.md:17 and README:33 require an end point
C-002 | winner: variant 1 | verdict: BLOCKING-REAL | no stoprule file in src/ or plugins/; the tracked `.dev/` copy is banned by PLAN:87; OD10 undecided
C-003 | winner: variant 1 | verdict: REAL-NOT-BLOCKING | phrases confirmed in both code files; executor can add them (SPEC:845); T5 is not a stage 1 test
C-004 | winner: variant 2 | verdict: BLOCKING-REAL | SPEC:404, :879 and :945 assign the mapping and "ledger adapters" to this plan; no task builds them
C-005 | winner: variant 1 | verdict: REAL-NOT-BLOCKING | Task 9 depends only on Task 5 (PLAN:134); scale-map layout not fixed; numbered order still runs Task 3 first
C-006 | winner: variant 1 | verdict: REAL-NOT-BLOCKING | REQ-07 table row cites `.dev/pr-monitor/` (SPEC:485); executor can paraphrase
C-007 | winner: variant 1 | verdict: REAL-NOT-BLOCKING | PLAN:146 "Depends on: Task 9" only; numbered order covers it
C-008 | winner: variant 3 | verdict: REAL-NOT-BLOCKING | T2 non-strict in stage 1 (PLAN:209)
C-009 | winner: variant 3 | verdict: REAL-NOT-BLOCKING | the sketch lives under `.dev/tasks/to-do/` and moves on archive; ruff excludes `.dev/` (pyproject:179-180)
C-010 | winner: variant 3 (silent) | verdict: NOT-A-DEFECT | PLAN:25 standing sync-dev order
X-001 | winner: variant 2 | verdict: BLOCKING-REAL | same evidence as C-004
X-002 | winner: tie | verdict: BLOCKING-REAL | the severity rule judges the result, not the cost of the fix
A-001 | winner: variant 1 | verdict: N/A | see below
A-003 | winner: tie | verdict: N/A | see below

## Shared assumptions
- **A-001: QUALIFY.** The `.dev/experiments` copy is tracked, so it literally "exists in the repository". It is ruled out by Task 5's `.dev/` ban and by the meaning of "defining file", not by the words "exists in the repository" alone.
- **A-002: ACCEPT.** README:33 says "a package's final review covers only its own tasks", and PLAN:24 requires end points. Both treat in-package acceptance lines as standing until the final review.
- **A-003: ACCEPT.** The severity rule counts a check that is false at the final review as blocking, whatever it costs to fix. The PLAN:115 grep still has to show something beyond the module and its wiring.
