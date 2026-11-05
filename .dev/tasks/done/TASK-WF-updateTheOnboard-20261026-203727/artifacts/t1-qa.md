# T1 QA (fresh reflect-reviewer subagent, sonnet, 2026-10-26T21:35Z)
Verdict: compliant
- T1.AC1 met: deck:317 intro (guide line 9 meaning, no "unsure"/"heavier"); deck:318, :341, :343 no spec-driven/large/rare; rung names deck:325, :327, :329, :331, :337, :339 match guide 15-20.
- T1.AC2 met: deck:325 rung 6 reads `/prd → /tdd`; deck:344 gives /sc:workflow then /sc:implement, /roadmap only explicit or exceptional.
- T1.AC3 met: artifacts/t1-baseline.log:2 HEAD, :3-12 git status.
- T1.AC4 met: deck:318 slide; deck:333-335 D3 rung area; desc deck:323; figcaption deck:341.
- T1.AC5 met: six rung rects; hard-limit line deck:332 between levels 2 and 3; class-only colors; title deck:322, desc deck:323; viewBox 426 deck:321.
extra_scope: none. misunderstood: none.
Note (not a failure): rung 6 shows only /prd → /tdd; the planning clause is on the slide (deck:344).
Extras: test pass (tests/docs/test_onboarding_deck.py, 3 passed); lint/typecheck skip (HTML only).
