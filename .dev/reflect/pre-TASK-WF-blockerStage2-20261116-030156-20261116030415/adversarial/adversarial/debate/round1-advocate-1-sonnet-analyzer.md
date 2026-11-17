# Round 1: Advocate for Variant 1 (reviewer-1, analyzer, sonnet class)

Persisted by the orchestrator from the advocate's returned message (the advocate is read-only).

**Position summary.** V1 is the best-evidenced card. All three of its blocking findings reproduce, and it is the only card to check F6-F8 and to catch the three consolidation points. It has one wrong citation, and its R1-1 fix is incomplete. V3 beats it on breadth for C-001, C-006 and C-008.

**Steelman of V2.** V2 is disciplined. Each finding says whether a literal executor would still be right. It dropped five T1 sub-leads with stated reasons, so it carries no false positives. R2-1 is the same safety-miss blocker as R1-3. R2-4 is real: `test_review_prompt_overrides.py:271-283` pins "no minimum count" in the two skills that Tasks 2 and 3 edit, and no task runs it.

**Steelman of V3.** V3 has the most complete answer to C-001. It names all three missing surfaces (writer, sweep, safety route) and cites the installed-primitive rule at `CLAUDE.md:95`, which I verified. R3-4 is grounded: `stage0-heldout-ids.json` holds ids only (S0:82, 85). R3-6 is correct: no test in `tests/skills` has `tech_research` with an underscore (grep found none), so half of `-k "tech_research or review_severity"` (PLAN:67) selects nothing. R3-8 is real: the tech-research cap sentences sit at `tech-research/SKILL.md:490` and `:555`, as checklist items.

**Strengths claimed (V1)**
1. R1-1 verifies. The `__init__.py:19-29` tuple has 9 subcommands and none covers follow-ups, sweep or safety. S1:167-171 adds only `classify`. `ledger_cmd.py` has no follow-up, sweep or safety hits. PLAN:50 still tells the skill to call all three.
2. R1-2 carries a constraint no other card has. `test_worker_contract.py:1715-1731` pins the paragraph starting "The same applies to the two other" (`task/SKILL.md:55`), so any `--unattended` fix must keep it green. V1 also notes that PLAN:74 edits only `WORKER-CONTRACT.md`, so no task makes `/task` return the three keys.
3. R1-3 shows that PLAN:110 plus S0:130(a) can only print 0 (PLAN:114 ties that 0 to the stage 3 entry). Its fix prints "not computable" instead of a bare 0.
4. R1-8 is verified. The consolidation points are `task/SKILL.md:252`, `:338-340` and `:405`, against the singular "step" at PLAN:50. V1 also found the SRC:19 no-edit list missing from PLAN:22.
5. V1 is the only card with an explicit F6-F8 check (S-002/U-005). It graded R1-4 to R1-7 as minor, with a stated reason for each.

**Weaknesses in V2 and V3**
1. V2 misses C-001, C-002 and X-001. It states "tasks 1, 4, 5 not examined" in its calibration, and never examines Task 2's `--unattended` gap. It treats the S0:130 safety-miss definition as settled, but S0:130 marks it "proposed, for owner acceptance".
2. V3 misses the safety-miss blocker (C-003) entirely. It never mentions PLAN:110's safety-miss count.
3. V3 overgrades R3-2. S1:176 and PSPEC:586 say that when the reviewer's label is the only judge, the row records `classifier=unavailable`. That is not a trivial 100%. GR12 also keeps a judge-free vocabulary trigger (S1:183).
4. V3 overgrades R3-4. PLAN:104 already requires UNSET or NA, "never N", for unsupplied inputs, so the plan pre-handles "answers wrong".

**Concessions about V1**
- PSPEC:169 is a bad cite for R1-2. The real text is at PSPEC:434 and 438 (438 "the row is recorded and the run does not wait"; 441 the final report line).
- R1-1's fix adds only `review sweep`. The writer and safety route also have no command (S1:110, 183), so V3's new-task fix is more complete.
- V1 did not examine Tasks 3 and 5. It missed the `-k` selection problem (C-006), C-008 and C-009.

**Per diff point verdicts**
- C-001: V3, 60%. Both grade it blocking. V3 covers all three surfaces and cites `CLAUDE.md:95`.
- C-002: all, 80%. Blocking. V1 adds the test pin and the return keys. V3 adds the GR12 wait and the PSPEC:441 line.
- C-003: V1 (V2 co-winner), 75%. Blocking, because the result printed is wrong. V3 misses it.
- C-004: V1, 70%. Minor. S1:136 and PSPEC:586 supply the replicate and judge rule.
- C-005: all, 85%. Minor.
- C-006: V3, 70%. Minor. V3 is broadest and its hyphen finding is verified.
- C-007: tie V1 and V3, 60%. Minor. They name different sites, so the fix should cover both (V1: 252, 338-340, 405; V3: 490, 555).
- C-008: V3, 70%. Minor. The files are new, so no data is lost.
- C-009: V3, 60%. Minor. V1's R1-1 command would fix the signature anyway.
- C-010: V1/V3 tie, 55%. Minor.
- X-001: V1's minor is right, 78%. The executor can finish. S1:176 gives an honest `unavailable`. M13 (PSPEC:975) asks for a split by judge id.
- X-002: minor, 60%. Closest call. It flips to blocking only if the held-out consensus has no recorded source. V3's `@E2` point is a coverage gap, not a wrong result, because PLAN:104 already counts UNSET rows.
- X-003: minor, 80%. PSPEC:592 names GR12 as the one exception to "changes nothing". Wording fix.

**Shared assumptions**
- A-001: QUALIFY. Right yardstick, but acceptance greps are weak, so a literal executor passes while delivering nothing runnable (R1-1, R3-1). The final review step in `/sc:implement` only partly compensates.
- A-002: QUALIFY. The S1 file exists and PLAN:37 checks the stage 1 modules at run time. Findings hold only against S1 as written. If S1 gains a follow-ups or sweep command, C-001 shrinks to a wording fix. S0:130's definition is only proposed, but R1-3 survives any confirmation-based definition.
- A-003: REJECT in part. Task 4 edits only the contract and its test (PLAN:74); no task makes anything emit the keys. Task 5's `pragmatic.md:225` pin does resolve.
- A-004: QUALIFY. PLAN:50 asks for `why not blocking` on Medium or Note rows but never names the stage 1 scale map (`refs/scale-map.md`, S1:38) that turns old labels into tiers. S1:110 refuses a Medium row without `why_not_blocking`. Minor if the executor reads S1, could be blocking if it does not.
