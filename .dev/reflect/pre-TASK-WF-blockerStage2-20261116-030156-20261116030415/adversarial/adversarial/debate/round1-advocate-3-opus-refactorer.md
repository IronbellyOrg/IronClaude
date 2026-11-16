# Round 1: Advocate for Variant 3 (reviewer-3, refactorer, opus class)

Persisted by the orchestrator from the advocate's returned message.

**Position summary.** V3 is the only card that finds all three gaps where the skills have no command or judge to use (R3-1, R3-2, R3-3) and gives a fix an executor can carry out. It is weaker on coverage: it misses the safety-miss count (C-003) and the capture-failure wording (C-005), and its grade for R3-4 does not hold.

**Steelman of V1.** V1 covers the most ground. It raises the unattended gap (R1-2), the safety-miss count (R1-3), how the judge agents are kept blind (R1-5) and the earlier findings F6 to F8. R1-3 is correct: S0:130 defines a miss as one that "a later review or the owner confirms", and nothing the plan reads (PLAN:110) holds that confirmation. V1 grades the judge gap (R1-4) minor on the defensible ground that the run still finishes.

**Steelman of V2.** V2 asks of every finding whether a literal executor would still be correct, and grades cautiously. It is right that X-003 is wording only: PLAN:50 says outright that GR12 is live. It also finds R2-1, which V3 missed.

**Strengths claimed**
1. R3-1 is the only fix that works. `cli/review/__init__.py:19-29` has no subcommand for follow-ups, the sweep or the safety route, and `ledger_cmd.py:31-126` handles the old review ledger, not `follow-ups.md`. The stage 1 plan adds only `classify` (S1:171), and CLAUDE.md:95 says installed primitives reach package code only through the CLI. V1's fix names writer and safety-route commands that no task creates.
2. R3-3 is backed by the skill text and the spec. `task/SKILL.md:53-55` lists the points that stop under `--unattended`, and the new offer is not one of them. The offer waits for an answer (PSPEC:417), while an unattended run must record only and print "recorded only, no issue created" (PSPEC:434, 441).
3. R3-2 is backed by S1:136 (the only non-test judge is `ReviewerJudge`), S1:176 (no judge gives `classifier=unavailable`) and PSPEC:946 (stage 2 exits on "shadow agreement reported").
4. R3-6 cites real pinning tests. `test_review_prompt_overrides.py:274-283` pins both edited skills, and `test_worker_contract.py:1715-1731` pins the unattended paragraph that R3-3 edits.
5. R3-8 is unique. The tech-research halt at `tech-research/SKILL.md:490` and `:555` sits in a task-file item that `/task` runs (`:614`).

**Weaknesses in V1 and V2**
1. V1's fix for R1-1 cannot be carried out, as strength 1 explains.
2. V1 grades the judge gap (R1-4) minor, yet a live run can only report "unavailable" or an agreement fixed at 100% by construction (S1:136, PSPEC:586). Either way the stage 2 exit figure is missing or wrong.
3. V1 cites PSPEC:169 for the unattended rule; the rule is at PSPEC:434-441.
4. V2 misses C-001 and C-002, the two most severe points.

**Concessions about V3**
- R3-4 (X-002) does not hold as blocking. PLAN:19 makes the executor read the stage 0 package, which names the master table and the consensus file (S0:69, 82). PLAN:104 already requires unsupplied inputs to be recorded as UNSET, so the counts come out honest, only lower. It is minor.
- V3 missed C-003 and C-005, and never examined Task 5.
- "Every point that waits" in R3-3 overstates `SKILL.md:53-55`, which lists specific points. The finding stands, because the offer is not on that list.
- "Selects nothing" in R3-6 overstates: the accurate claim is that `-k tech_research` does not select `test_review_prompt_overrides.py`, because its test ids spell "tech-research" with a hyphen (line 276).
- The X-003 part of R3-3 is wording only.

**Verdicts per diff point**

| Point | Winner | Conf. | Reason |
|---|---|---|---|
| C-001 | V3 | 85% | Only V3's fix names commands that a task creates |
| C-002 | V1 and V3 | 90% | SKILL.md:53-55 and PSPEC:434-441 |
| C-003 | V1 and V2 | 85% | No confirmation source for a miss (S0:130, PLAN:110) |
| C-004 | V1 | 70% | PSPEC:586: results from different judges are not compared |
| C-005 | V1 and V2 | 90% | PSPEC:947 requires "no capture failure" |
| C-006 | V3 | 80% | Adds the worker-contract pin and the no-edit diff check |
| C-007 | V1 and V3 | 75% | V3 adds the halt ordered by a task-file item |
| C-008 | V3 | 60% | Minor; created files are new, nothing is lost |
| C-009 | V3 | 60% | Minor; Task 2 must match an undefined signature |
| C-010 | all | 70% | Each card names part of the gap |
| X-001 | V3 (blocking) | 65% | A required stage 2 exit figure is empty or always 100% |
| X-002 | V1 and V2 (minor) | 60% | See the concession |
| X-003 | V2 (minor) | 80% | PLAN:50 makes GR12 explicit |

**Shared assumptions**
- A-001: QUALIFY. The acceptance checks are greps (PLAN:53-58); a blocking grade should rest on what the task body leads an executor to build, not only on a weak check. C-001 and C-002 meet that bar.
- A-002: QUALIFY. The stage 1 plan has not been built. R3-1 and R3-2 hold only if stage 1 is built as written; PLAN:37 checks only that modules exist. The safety-miss definition is marked "proposed" (S0:130).
- A-003: QUALIFY. PLAN:79 asks a test to assert that an unattended run asks no question, but a contract-text test can check only the contract's wording, not the skill (ties to C-002). Task 5 was examined by no card, and I did not verify it.
- A-004: QUALIFY. A real gap: PLAN:50 asks for `rests_on` on Medium and Note findings, but the old rule produces only blocking and minor. PSPEC:592 points to the scale map (spec section 9.3). Minor if that map has a row taking minor to Medium, blocking if it does not. I did not check the map.
