# Q14: what "#339 is complete" means for #423's start gate

## Question (verbatim from the spec row)

merged-requirements.md section 3, row Q14: "What \"#339 is complete\" means for #423's gate; and does the gate mean the capture is recorded, or the sweep's `working` class is restored in code? (second part widened by this debate, X-009)"

ADJ Part 7 wording (alignment-findings-adjudicated.md:784): "What does \"#339 is complete\" mean for #423's gate: PR #539 merged only, or also `/sc:close`, resume and the trust layer?"

## Spec's recommended answer

"PR #539 merged plus the #534 live capture (ADJ); other phases only if v2 relays to agents" (merged-requirements.md:541). ADJ Part 2.6 (alignment-findings-adjudicated.md:294) words it: "PR #539 merged plus the #534 live capture that restores the sweep's `working` class; `/sc:close`, resume and the trust layer are not prerequisites unless the brainstorm decides that v2 relays to agents and not only to a person."

## Default if unanswered

"PLAN INFERENCE: ADJ's recommended gate, read as \"capture recorded\" and labelled \"default\" in V2-01 and V2-02; SW-14 is then not needed" (merged-requirements.md:541).

## What it gates

- V2-01: the rewrite of issue #423 (Orchestrator v2, the planned knowledge layer), whose sequencing clause is set "per Q14" (merged-requirements.md:398).
- V2-02: the dated check that the v2 start gate is met; it passes "only if every part of the owner's Q14 answer is met" (merged-requirements.md:399).
- SW-12: the deferred "manages work" phases of #339 (`/sc:close`, resume, trust layer, orchestrator of orchestrators); they feed V2-04 "only if v2 relays to agents, Q14" (merged-requirements.md:201).
- V2-04: the deferred v2 first release (merged-requirements.md:401).
- SW-14: a conditional sweep change that restores the `working` class from the shared capture; "Needed only if the owner's Q14 answer means \"`working` class restored\", not \"capture recorded\"" (merged-requirements.md:203).
- Wave W3.

## Facts the question depends on

1. #423's gate reads "after #339 is complete", which "has two readings and cannot be applied as written"; "v2" has at least three meanings (the #339 summary's signed grants plus orchestrator of orchestrators; the research report's phases 2 to 6; #423's knowledge layer) (ADJ Part 2.6, line 294; E-13 at line 139).
2. The `working` class is one of the sweep's eight classes (docs/designs/orchestrator-mode.md:472). Its rule (Rule 5) is inert in Phase 1: `_rule_working` returns None because the live names of `agentWait`, `live` and `in_progress` "were never captured", so such a row falls to the fallback (src/superclaude/cli/sweep/classify.py:251-257, re-read 2026-11-14; design open item 6 at orchestrator-mode.md:997).
3. The shared capture (work item XC-03) is a read-only record of live Orca values; ADJ row A-013 says it "unblocks" the `working` class (ADJ line 335). Weak point W5 of the spec: "The gate as worded conflates a record with a code change" (merged-requirements.md:415). That is debate point X-009.
4. ADJ's proposed #423 sequencing text: "This starts only after PR #539 (#339 Phase 1, the read-only sweep) is merged and the #534 live capture that restores the sweep's `working` class is recorded. The other #339 phases ... are not prerequisites, unless the brainstorm decides that v2 relays to agents and not only to the person" (ADJ line 699).
5. v2 per ADJ: advisory, a separate command or skill, delivers to the person or the coordinator only, LLM-derived entries marked inferred (ADJ line 294). V2-04 requires that v2 reads only what named collectors publish (merged-requirements.md:401). Q15 decides whether v2 ever delivers to non-worker sessions.
6. The dedicated v2 research pass (V2-05) is ungated (merged-requirements.md:400, item 2). V2-03, the v2 brainstorm, waits on V2-02 for its implementation-facing parts.
7. Nothing of v2 exists. PR #539 is open; the capture (XC-03) has not run; the Orca app was not reachable on 2026-11-13 per the spec's ORCA-AVAILABLE note (merged-requirements.md:604), and the spec does not claim that is still current.
8. Sweep rows that would be `working` today show the fallback class, which the design lists as `could not determine` among the classes (orchestrator-mode.md:472; classify.py:251-257 comment).
