# Ruling: should B's finding M6 (tie-cut) be Blocking?

The debate's answer below is advice. The owner decides.

Source: /sc:adversarial, compare mode, standard depth, over the three position papers. Artifacts: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/throwaway-medium-runs-20261117/severity-debate/adversarial/ (merged-output.md; process files and return-contract.yaml in its inner adversarial/ folder).

## (a) Answer on M6

**Yes, Blocking (Decision test), confidence 62%.** One grade, no conditional. Paper 3 started at Medium and moved to Blocking in round 2.

Winning reasons:
1. Fixing M6 changes a named acceptance check: plan lines 14-15 (task T2) gain "the top n of the fully sorted list" and the T5 test gains a tie-at-the-cut case. Today a wrong program (prints `zed` instead of `and` on `zed sat the the the cat cat and`, N=3) passes every planned check.
2. The plan names the consumers (T2; T5 is "one test per acceptance line"). The card itself says (line 175) M6 "still let[s] wrong programs pass the planned checks".
3. "The gap starts in the spec" is not a test in the rule. Paper 3 dropped its "restoring versus making a decision" separator, because the B3 line it relied on is equally a parenthesis.
4. Medium is never rechecked, so a Medium lets the loop end PASS with a wrong program still passing (a consequence of the rule, not a cost argument).

Strongest losing argument (paper 3): both programs satisfy every normative spec line on a tied boundary; only the parenthesis at spec line 38 picks `and`, so the fix adds a rule instead of changing one. Weakened, not refuted: the probe found spec line 22 sits under "Tie rules" and line 38 under "Example", so they are not equally weighty. That open point is why the answer is 62%, not higher.

## (b) Disputed items

B = Blocking, M = Medium, N = Note. P1/P2/P3 = the papers' starting grades.

| Item | P1 | P2 | P3 | Debate | Reason |
|---|---|---|---|---|---|
| M6 tie cut | B | B | M | **B** | Section (a) |
| B2 no `wordcount` command | B | B | M | B (Missing) | Spec and plan:20 name it; no task builds it. P3 conceded |
| B1 `tokenize.py` shadows stdlib | B | B | B | B | Fails only under some pytest invocations: a caveat |
| A: directory / BOM as FILE | N | M | N | N | Spec says "unreadable". P2 conceded |
| A: output encoding | N | M | N | N | No stated text contradicted. P2 conceded |
| B r3 M1: T3, T4 order | N | M | N | N | T1 to T5 order works. P2 conceded |
| B's 8 Note bullets | N | not graded | N | N | Label or naming only |
| B raw cards r1 M2, r1 M3, r3 M3 | folded | B | omitted | no own grade | Inputs to B2, B3; not counted twice |
| A: "letters" (L1) | M | M | M | M | No concrete wrong outcome named |
| A `FILE` placeholder vs B M1 | M | M | M | M, same defect | A test can assert the printed string |
| C F1.1 ASCII pattern | M | M | M | M, same as A's L1 | Own-scale "minor" is vocabulary |
| M5 run from repo root | M | M | M | M, contested | Plan:4 names `code/`; see INV-009 |
| M7 stdout / no words | M | M | M | M, contested | Other plan lines pin both; see INV-009 |
| M8 coverage matrix | M | M | M | M, follow-up | Review-tool defect, outside the plan verdict |

Totals: B has 4 Blocking (B1, B2, B3, M6) and 7 Medium; A and C have none. B's verdict stays FAIL.

## (c) Convergence and what the skill reports

- convergence_score **0.9423** (49 of 52 points; threshold 0.80).
- Status **BLOCKED_BY_INVARIANTS**: not converged. Blocked by INV-009 (HIGH, unaddressed): M6 = Blocking with M5 and M7 = Medium has no agreed rule wording. Unresolved points: S-002, S-007, C-016.
- Contract status **partial** (invariant gate failed; the merge re-scan found one stale count in merged-output.md summary item 8).
- base_variant: "variant 1 (position paper 1, "the rule as written, literally"); no model or persona recorded". The skill has **no judge or model field** and no artifact records one, so none is given.

## (d) Smallest wording change (observation; not agreed, 50%)

The debate's leading option is paper 2's addition at the end of the Decision paragraph (pragmatic.md line 229, copy at rf-qa.md line 108): "A defect also meets this test when the text lets a result pass the item's own checks that the source text (spec, task or criterion) rules out; where the gap first appeared does not change the grade. A choice the source text leaves open is Medium until someone decides it." It still turns on whether spec line 38 "rules out" cut-then-sort, so it moves the dispute rather than ending it. Test first: B3 and M6 stay B, M5 and M7 stay M.

## (e) UNVERIFIED

1. INV-009: no wording holds M6 Blocking with M5 and M7 Medium. A third round would address it; standard depth runs none.
2. Whether spec line 38 states a tie rule at the cut or only explains the example (58%): the hinge of the 62%.
3. Owner rulings not given: "any tie-break at the cut is fine" (flips M6 to Medium in all three papers) or "line 38 is normative".
4. INV-001 and INV-012 (Medium, unaddressed): line 22 versus 38 weight; the "rules out" wording.
5. The papers cite M6 at card lines 86-92; the debate agents report 96-104 (form only). I did not re-check it.
6. B1 reproduces under `uv run --with pytest pytest`, not `python -m pytest`.
7. Advocates and scorers were subagents of this session; no model identity is recorded, so panel diversity is UNVERIFIED.
8. merged-output.md summary item 8 says "two are overstated"; its section 4 supports one (form only).
