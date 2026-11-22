# D15 position paper: CLAY (Clay's line)

Topic: Clay strengths bundle, what to adopt and how. This paper argues Clay's side: Clay's controls are one interlocked set, so the unified design should adopt the set and its test plan as built, and take the owner's rules as amendments to it.

## Claim

Clay's controls are one interlocked set. The grant list, `E-NO-GRANT`, `answer-check`, `escalate`, the merge gate, `refuse(argv)`, the audit and the hand-back loop each lean on the others. Taking them piece by piece, each with its own rewrite, costs more and leaves gaps between pieces. The unified design should adopt the set and its test plan (tests T1 to T13, the UNVERIFIED list, the 62-reason table) as the base, and apply the owner's rules as amendments to it.

## Mechanism

The design makes the fixed-result steps verbs of one group (`wake-check`, `wake-ack`, `state`, `merge-gate`, `lease`, `repos`, `escalate`, `answer-check`, `audit`, `handback`) so the model runs them and reads JSON (`docs/designs/orchestrator.md:140`, ADD6). The verbs share one refusal function `refuse(argv)` and one grant list (`orchestrator.md:767`, `:696`). Adopting the verbs together means one set of tests and one JSON contract.

## Cited facts

1. The stack is already half on master: `/sc:closeout` (PR 683), the report skill (PR 684), the plan sections in templates (PR 661) and the design text (PR 681) are merged; PR 686 passes 6 of 6 checks and is mergeable (`inventory/clay-prs.md`, section 2A).
2. PR 690 (`--plan`, `--remaining`) has three review rounds and 23,043 tests passing on its first head (D12 verdict, "Strongest points" CLAY 2).
3. The design carries a complete test plan: tests T1 to T13, an UNVERIFIED register (U1 onward) and a risk register (K11, K12, K14, K16) so a live test can be planned (`orchestrator.md:957-961`; D10 verdict "Clay strengths to adopt", last item).
4. The 62-reason audit table is pinned by one test and gives every skip and failure a visible reason (`pr-a/tests/issue_watch/test_audit.py:78-83`).
5. The owner's line lacks these capabilities, each verified by a verdict: an in-flight cap (D07, grep zero), restart of a dead coordinator (D07), a merge gate and head-pinned merge (D06), a post-merge audit (D05, D06), a typed-answer check (D04, D06), a closed refusal list (D04, D05), a hand-back for work a PR did not finish (`orchestrator.md:610-616`), a nine-row reasons list (D11).
6. Every verdict D04 to D11 adopted a Clay control and had to say how to fit it; D06 alone adopts nine (D06 verdict, "Clay strengths to adopt"). The rewrite cost is paid per piece instead of once.
7. The design separates what Clay decided from what is a question (OQ1 to OQ6, the U-list), and the owner can overrule by amending a named row (`orchestrator.md:109-140`, tables with an Owner column).
8. The owner's own `issue_pipeline` (Plan A and Plan B) also never ran live (FULL-REPORT.md, section 3, "The case for the deletion"); "unbuilt" or "never ran" is not a mark that only Clay's verbs carry.

## What it costs

The set carries Clay's contested rules (standing `pr.merge` grant, assignment-only trigger, no launch guard, label writes, registry repo). Each needs an owner override, and the amendments touch many rows (`orchestrator.md` lines 73, 76, 81, 116, 117, 118, 135, 138, 267-305).

## What it risks

Importing the set whole risks landing a contested rule by accident, because the code and tests encode it (for example the NG-2 test pinning three label calls, `pr-a/tests/issue_watch/test_security_invariants.py:12`).

## What it gets right

It treats the control verbs as one tested unit with one contract, it keeps a complete register of what is unproven, and it gives the owner a single place (`orchestrator.md` tables with an Owner column) to rule on each contested row.
