# Round 2: Advocate for Variant 1 (sonnet class, analyzer)

## Response to criticisms
- **C-003 (V2 calls it blocking, V3 and I say it isn't).** I concede V2's facts and keep my grade. `/sc:workflow` source.md:12 prescribes this exact list, which names "the auggie file, `refs/rule.md` and the six stage 4 files". `stage-requests/README.md:27` says "Stage 3's scan test allow-lists only files that exist then". SPEC:845 puts `remediate_parser.py` and `fmea_classifier.py` out of scope and "Not changed". T5 is not among the stage 1 exit tests (SPEC:945). No Task 3 acceptance line says "only". The gap is real but it is a stage 3 problem, and the plan copied it from the request. It is not blocking for stage 1.
- **My own concession (C-006).** I withdraw "real". PLAN:72 asks only for "the location rule (REQ-07)", not for the verbatim `.dev/pr-monitor/` text at SPEC:485. Task 5's grep at PLAN:87 catches any copy, and the fix is a paraphrase. That is a tripwire working as designed, not a wrong result.
- **My own concession (C-009).** I withdraw "real". The sketch comparison at PLAN:139 is a one-off `uv run python -c`. The committed test (PLAN:159, `test_review_classifier.py`) does not import the sketch, so the sketch's path never becomes a standing dependency.
- **C-008.** I keep it as real but not blocking. The doctor check (PLAN:197) must read the fence opener, so a literal in `doctor.py` could trip T2, which is non-strict only for the legacy sentence (PLAN:209). V2 is right that the plan never requires the literal. V3 is right that T2 would show the failure, and the executor repairs it by building the string or adding a registry row.
- **A-003 (V2 and V3 vs my QUALIFY).** The severity rule you gave never counts fix cost. I switch to ACCEPT, with V2's condition that the failure is first established. For C-001 it is established (see New evidence).

## Updated assessment
- **V2** is right on C-001, C-002 and C-006/C-009. Its C-004 blocking grade is the one I still reject.
- **V3** adds the strongest support for C-001: source.md:17 and README:33 require an end point.
- **V3's C-002 argument has a hole.** The `.dev/experiments` copy is tracked, so only PLAN:87's ban on `.dev/` strings removes it. That is my argument.

**C-004/X-001, decided on SPEC:404, 879, 945 and PLAN:110.**
- SPEC:404 and SPEC:879 call the `review-ledger/1` mapping a "plan decision". A decision can be "none in version 1", because SPEC:404 also says version 1 is "a separate, human-readable markdown ledger".
- Nothing in the spec consumes a mapping. The only `ledger.py` mentions are the three items at lines 404, 879 and 1148-1153.
- The stage 1 request and source.md never mention a mapping or adapters. `grep -i "adapter\|mapping\|review-ledger"` over `stage-requests/` and source.md returned nothing.
- "Ledger adapters" at SPEC:945 is undefined. SPEC:731 and SPEC:940 use "adapters" for own-scale primitives, which is a different sense.
- The exit tests listed for stage 1 (T1–T4, T6–T8, T11–T13, T17) have no mapping condition.
- PLAN:110 already covers the half the spec makes mandatory: the `reuse-auditor` runs first and `ledger.py` is named.

An executor following the plan builds no mapping and breaks no stated check. The plan should record its decision in one sentence. I hold REAL-NOT-BLOCKING on the merits, and V2 and V3 have not moved me.

## New evidence
- **Task 12 as a second false match for C-001.** Task 12 (PLAN:167–171) depends on Task 7. It writes the verdict into the ledger row's `classifier` column through the Task 7 writer. So `grep -rn "follow_ups" src/superclaude/cli/review` (PLAN:115) matches Task 10's `classifier_inputs.py` and `classify_cmd.py`, not only the module and its wiring. Task 12 adds a match even if Task 10 avoided the import.
- **C-002 repository check.** `git ls-files` lists the stoprule and `finding-grader` files only under `.dev/experiments/`. `src/superclaude/agents/` has no grader file, and `src/superclaude/skills/` and `commands/` hold no stoprule file. SPEC:582 and SPEC:1038 treat bringing them into `src` as undecided (OD10). SPEC:740 does give the stoprule row an `installed-only` registry kind. PLAN:62's "exists in the repository" and PLAN:209's rule that the test "never reads `~/.claude`" give that row no exemption.

## Final positions
C-001 | winner: variant 3 | verdict: BLOCKING-REAL | changed from round 1: no | PLAN:115 against PLAN:148 and PLAN:171; source.md:17 and README:33 require "until Task N"
C-002 | winner: variant 1 | verdict: BLOCKING-REAL | changed from round 1: no | PLAN:62 against PLAN:87; the only tracked copies are under `.dev/experiments/`; OD10 undecided
C-003 | winner: variant 3 | verdict: REAL-NOT-BLOCKING | changed from round 1: no | PLAN:59 matches source.md:12 and README:27; the T5 gap shows at stage 3 (SPEC:845)
C-004 | winner: variant 1 | verdict: REAL-NOT-BLOCKING | changed from round 1: no | SPEC:404 and 879 call it a plan decision; no requirement or check consumes it
X-001 | winner: variant 1 | verdict: REAL-NOT-BLOCKING | changed from round 1: no | "ledger adapters" (SPEC:945) is undefined and has no exit test
C-006 | winner: variant 2 | verdict: NOT-A-DEFECT | changed from round 1: yes | PLAN:72 needs the rule only; the PLAN:87 grep catches a verbatim copy
C-008 | winner: variant 3 | verdict: REAL-NOT-BLOCKING | changed from round 1: no | PLAN:197 needs a version comparison; a T2 trip would show and be fixed
C-009 | winner: variant 2 | verdict: NOT-A-DEFECT | changed from round 1: yes | the sketch check is one-off (PLAN:139); the committed test (PLAN:159) has no sketch import
A-003 | winner: tie | verdict: N/A | changed from round 1: yes | ACCEPT: the severity rule ignores fix cost once the failure is shown (C-001 shows it)
