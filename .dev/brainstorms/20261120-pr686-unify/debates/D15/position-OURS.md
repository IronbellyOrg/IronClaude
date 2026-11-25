# D15 position paper: OURS (the owner's line)

Topic: Clay strengths bundle, what to adopt and how. This paper argues the owner's side: adopt Clay's elements one at a time, each only where a cited verdict shows a clear benefit, each re-homed under the owner's rules.

## Claim

Adopt Clay's elements as separable parts, each one tested against the weighting rule (a clear, cited benefit, or OURS wins). Most adopted elements must change on the way in: a new name, a new home for its settings, a narrower authority, or a repaired defect. Adopting the whole stack "as built" would also import Clay's contested rules (assignment-only trigger, standing merge grant, no launch guard, label writes by the poll). So: a per-element table, not a package.

## Mechanism

Each element gets one of three outcomes: adopt as is (no contested rule inside it), adopt with change (a benefit separable from a contested rule), reject or defer (no cited benefit, or it needs an owner ruling first). Order of work follows the owner's chain: rules and doc fixes first, then the code Clay already built and tested, then the unbuilt verbs, then live tests.

## Cited facts

1. The owner order in the brief: OURS wins unless CLAY shows a clear, evidenced benefit; a tie goes to OURS (`debates/BRIEF-COMMON.md`, weighting rule).
2. Thirteen verdicts (D01 to D13) each adopted a few Clay parts. Most carry a change; only a few are as is (closeout, PR 661, the landed check, the PR log, the report's silent-loss rules) (`debates/D01..D13/VERDICT.md`, section "Clay strengths to adopt").
3. The 62-reason audit table is pinned by a test that says none of 14 old approval reasons may survive (`pr-a/tests/issue_watch/test_audit.py:78-98`; table at `pr-a/src/superclaude/cli/issue_watch/audit.py:39`). If approval stays the gate (D01), that test and 14 reasons must come back, so the table is not adoptable as is.
4. The nine-row escalation table, the cap of 5, `escalate`, `asks.json`, `answer-check`, `merge-gate`, `refuse(argv)` and the audit are design text only: no `escalate` verb, no `orchestrator` command group and no `asks.json` exist in master, pr-a or pr-p (D11 verdict, "Strongest points" OURS 3; D06 verdict, "Unverified": `merge-gate` and `answer-check` exist nowhere).
5. `answer-check` is hardwired to Clay's terminal or ClickUp id (`docs/designs/orchestrator.md:694`) and cannot tell a person from a script that types into the same terminal (D06 verdict, item 9, INV-003).
6. Two defects sit in Clay's wake code today: an acknowledgment can arrive before the issue's state file exists, and an abandoned wake can never be recovered (D10 verdict, mandatory conditions M1 and M2; `pr-a/.../cycle.py:777-810`, `:994`).
7. The tier settings reach a worker through `worker-start --model <picker id>`, which the design itself marks UNVERIFIED (`orchestrator.md:726`, U28); the hand-back cap `HANDBACK_MAX` = 3 is "this design's value, not measured" (`orchestrator.md:612`).
8. `plan_check` has a gap: only HTML comments are stripped, so the unfilled issue template with `<...>` placeholders passes (D09 verdict item 6; `pr-a/.../hold.py:69-70`, `:140`). `plan_body.py` passes any non-empty text except "Not known yet" (D12 verdict, "Implications").
9. Clay's design keeps its settings in a separate registry repo and `repos.yaml`, which D07 removes; the settings must be re-homed in the per-repo config (D07 verdict items 2 and 5).

## What it costs

A per-element table is longer than "merge the stack", and every adopted row needs a rename (D08 action 8) and a re-home (D07). Clay's throughput gains from standing grants and autonomous merge are given up (D06 verdict, Implications).

## What it risks

Cherry-picking can leave pieces that lean on a part we rejected (for example `E-NO-GRANT` listing `pr.merge`). The table must say, per row, which neighbours it needs.

## What it gets right

It keeps the owner's gates (approval, level none, guard required, person's go for merge) while taking every cited Clay benefit: plan check, hold:backlog, wake file and ack, cap, restart, merge gate, reviewer hold, answer-check, refusal list, audit, closeout, cleanup rules, living report.
