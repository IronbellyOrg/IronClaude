# Round 1: Advocate for Variant 2 (haiku class, qa)

## Position summary
Variant 2 correctly identifies the missing ledger mapping and the two conflicting acceptance checks. Its strongest feature is separating required results from tests that can pass without them; it nevertheless misses variant 1’s genuine allow-list defect.

## Steelman
**Variant 1:** Its strongest contribution is following the scale-map allow-list into its named consumer, the stage 3 scan. The unchanged severity-code phrases really would fail that scan. Its wider dependency and synchronization concerns are sensible checks, but not all survive the plan’s global constraints.

**Variant 3:** It strengthens the installed-only finding by connecting it to T4 and the unresolved owner decision. Its doctor-parser and sketch-location concerns identify plausible implementation traps, but neither implementation choice is required by this plan.

## Strengths claimed
1. **Missing mapping is substantive.** SPEC:404 explicitly leaves “A mapping rule from its rows to `review-ledger/1` rows” to this plan. PLAN:110 commissions a reuse audit and codec, not that mapping. PLAN:113 narrows its test claim to “covers each T7 failure condition above”; those conditions do not test the mapping. SPEC:945 also requires stage 1 “ledger adapters.”
2. **The grep check rejects correct reuse.** PLAN:115 begins “Two readers of this ledger do not exist,” then requires matches in “only the new module and its command wiring.” Reusing the reader as PLAN:148 requires does not create two readers, but its ordinary import adds a forbidden match. The stated check therefore conflicts with the required implementation; PLAN:24 expressly requires an endpoint.
3. **The scale-map check has no installed-only exemption.** PLAN:62 requires each family to name “a defining file that exists in the repository”; PLAN:209 repeats the existing-file-and-label check. Source, plugin and project-copy searches found no stoprule/grader definition. The registry’s separate installed-only category does not exempt scale-map rows.

## Weaknesses identified in the other variants
1. **Variant 1 understates the mapping omission.** SPEC:404 assigns an actual mapping rule, not merely an optional reuse investigation. Calling its absence minor permits a required result to remain missing.
2. **Variant 1’s synchronization blocker overlooks PLAN:25:** “Edit there, then run `make sync-dev`.” Following that standing instruction keeps PLAN:40 true after later edits.
3. **Variant 3 substitutes possible implementations for necessary failures.** PLAN:197 requires version comparison, not a contiguous fence-opener literal in doctor code. PLAN:139 requires agreement with the sketch, not a permanent test import from its current task-folder location.

## Concessions
Variant 2 missed C-003: `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/src/superclaude/cli/pipeline/fmea_classifier.py:304` contains “highest severity,” also at :323. PLAN:59 supplies the later scan’s allow-list but omits this unchanged file; SPEC:920 makes that a failing result. The defect is inherited from the request, not invented by this plan.

## Per-point positions
S-001 | winner: tie | verdict: N/A | Finding count is not correctness evidence.
S-002 | winner: tie | verdict: N/A | Absolute versus relative citations changes no result.
C-001 | winner: variant 2 | verdict: BLOCKING-REAL | PLAN:115’s match restriction conflicts with PLAN:148 reuse.
C-002 | winner: tie | verdict: BLOCKING-REAL | PLAN:62 requires a repository definition; no applicable exemption.
C-003 | winner: variant 1 | verdict: BLOCKING-REAL | PLAN:59 omits unchanged phrase-bearing code consumed by SPEC:920.
C-004 | winner: variant 2 | verdict: BLOCKING-REAL | SPEC:404 mapping remains unassigned by PLAN:110.
C-005 | winner: variant 1 | verdict: REAL-NOT-BLOCKING | PLAN:136/171 need the map; its executable interface remains unspecified.
C-006 | winner: none | verdict: NOT-A-DEFECT | PLAN:72 requires the location rule, not verbatim copying of its explanatory path.
C-007 | winner: variant 1 | verdict: REAL-NOT-BLOCKING | PLAN:146 omits Task 7’s edge, but numbered execution supplies it first.
C-008 | winner: none | verdict: NOT-A-DEFECT | PLAN:197 does not require the literal that would trigger PLAN:209.
C-009 | winner: none | verdict: NOT-A-DEFECT | PLAN:139 mandates comparison, not a durable task-folder import.
C-010 | winner: variant 2 | verdict: NOT-A-DEFECT | PLAN:25 already requires synchronization after edits.
X-001 | winner: variant 2 | verdict: BLOCKING-REAL | Missing mapping violates SPEC:404 despite green codec tests.
X-002 | winner: tie | verdict: BLOCKING-REAL | Cheap repair does not make PLAN:115’s explicit check pass.
A-001 | winner: tie | verdict: N/A | Repository boundary holds; “tracked” adds an unstated qualification.
A-003 | winner: tie | verdict: N/A | Genuine acceptance failure is independent of repair cost.

## Shared assumptions
A-001: QUALIFY — installed copies cannot satisfy repository existence, and experimental paths violate PLAN:87; “tracked” is not expressly required by PLAN:62.
A-002: ACCEPT — PLAN:24 expressly governs acceptance lines falsified by later tasks.
A-003: ACCEPT — a genuine final acceptance failure blocks regardless of fix cost; failure must first be established.
