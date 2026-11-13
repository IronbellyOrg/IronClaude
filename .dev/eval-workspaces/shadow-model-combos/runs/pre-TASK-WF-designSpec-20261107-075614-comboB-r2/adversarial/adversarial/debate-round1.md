# Round 1: advocate statements (condensed record; each advocate ran as its own agent, parallel)

Abbreviations: S = spec source.md, P = plan TASK-WF-designSpec-20261107-075614.md.

## Variant 1 advocate (analyzer card, sonnet class)
- Position: most complete audit of the plan's own acceptance criteria; confirms T1 F1 to F7; F1 and F2 blocking.
- Steelman of V2: disciplined premises; its F5 (producer payload) is the only finding on the event producer; blocking C-003 is defensible. Steelman of V3: F8 is a real hazard (S:139 engage row 7 NOOPs on a held guard; S:186-206 no row sets cycle_id; S:108 held_cycle_published keys on guard.cycle_id); F10 useful.
- Claims: F1 (P:108,113 vs test_static_grep.py:545-550, `_repo_scoped` :107-132, also `command -v gh`); F2 (S:107-109,166); F5/F6 confirmed against V2's rejection; F8 order of resume row 3 reasons.
- Weaknesses admitted: its F9 is mis-cited (P:175 is Task 11; Task 5's claim is at P:88 and says "including ... the key-set assertions", not three files): WITHDRAWN. Missed U-005, U-003, U-007. F3 non-blocking is open to challenge; F7 MINOR is weaker than V3's point.
- A-001 QUALIFY (base-stable facts such as test helpers are fine; feature-introduced signatures are not); A-002 ACCEPT; A-003 QUALIFY.

## Variant 2 advocate (qa card, haiku class; served model self-reported as an OpenAI assistant)
- Position: best at separating missing acceptance evidence from speculative defects; keeps F2 blocker and producer-payload finding; withdraws categorical dismissal of baseline contamination; softens reporting blocker.
- Steelman of V1: precise resume critique. Steelman of V3: multi-cycle failure sequence is genuine (S:108,139,190-206).
- Claims: U-003 distinct acceptance gap (S:184-185, P:62,170-172; Task 8 omits section 4.2 from its source list P:124); C-002 blocking (S:107-109,166; P:70,77); C-004 settle-fold-status test.
- Weaknesses admitted: X-001 rejection too strong (docs/memory/reflect/deviation-patterns-post-release-v5.0.0.md:7); C-003 blocking overconfident (engage already halts before edits, S:68); C-007 conflict is real but "condition" must not mean any token.
- A-001 REJECT (HEAD equals base is unproved); A-002 ACCEPT; A-003 QUALIFY.

## Variant 3 advocate (refactorer card, opus class)
- Position: only card with a release-safety finding (F8) and the most verifiable repo evidence; one inconsistency: F2 not blocking.
- Steelman of V1: precise shared findings, F9 real over-claim (as V3 saw it). Steelman of V2: producer-payload gap real; push-back on T1 F5/F6 sets a bar. Critique of V2: ignores the one-python-fence limit (P:143) for F6.
- Claims: F8 re-checked (S:139,108,166,190-206; P:62,77); F1 holds at the base (parent of 0b8a5801d has `_repo_scoped` and the resolution test); F10 re-checked (test_worker_contract.py:2019-2021, :2067-2072); F2 confirmed in later code.
- Weaknesses admitted: F2 should be blocking; F7 overstated (the plan:137 test is about "L3 only" or `draft` gate wording, a builder can pass it): MINOR-plus; F10 narrower (plan:22 already names git write verbs; the gap is the per-task wording and key shape); some evidence is hindsight.
- A-001 QUALIFY; A-002 ACCEPT; A-003 QUALIFY.
- Not re-checked: V1 F8, V2 F6.

## Per-point winner votes (V1 / V2 / V3)
C-001 none/V1/V1 | C-002 V1/V2/V1 (blocking) | C-003 V2/V1/V3 (non-blocking by 2 of 3) | C-004 V2/V2/V2 | C-005 V1/V3/V3 (real) | C-006 V1/V2/V1 | C-007 V3/V1/V3 -> severity MINOR-plus by V3's own concession | X-001 V1/V3/V3 | X-002 V1/V2/V1 | X-003 none/V1/none
