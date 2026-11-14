# Round 2 rebuttal, Variant 1 advocate (analyzer card, reviewer 1)

Notation: TL = `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md`. DESIGN = `docs/designs/orchestrator-mode.md`. A = the adversarial folder. Calibrated verdicts (CAL) outrank card self-scores. Every TL and DESIGN line cited below was Read by me this round.

## Response to Criticisms

**From V2 (Round 1, "Weaknesses Identified")**

1. *"V1 establishes delivery more often than verification soundness; NFR-013 `covered` does not ask whether 8.9 can show the guard works."* Concede. My NFR-013 row (card line 52) judges that 8.8 builds the guard and 10.4 snapshots no live launch. It never tests the 8.9 Verification. R2-G8 (CAL MEDIUM, holds yes) is the narrower point I did not cover. C-008 goes to V2.
2. *"V1's M2 claim and remedy overreach (7.17 inherits DESIGN behaviour; DESIGN open item 3 already routes a JSON need to the owner; recommendation names item 2)."* Concede on the remedy and the severity. TL:1265 says STILL UNVERIFIED rows follow "the DESIGN 'behaviour until closed' applies", and DESIGN:971 (open item 3) reads "a `--json` need goes to the owner as an allowlist change". What I keep, and nothing in the debate has removed: `M2` has 0 hits in TL (I re-ran the count: no matches). DESIGN:971 routes a need for `--json`; it does not say what happens when plain `run-current` output simply fails to parse. So the residue is "no named item records the M2 question", which is LOW. I do not claim a missing owner route.
3. *R1-G6 / X-006.* Concede in full. TL:2488 says `pipx run --spec` builds a wheel and installs runtime dependencies, so "installs nothing" is false. Only the "count of 168 can hide a swap" point stands, at LOW.

**From V3 (Round 1, "Weaknesses Identified")**

4. *"V1 misses all three execution-blocking defects."* Concede (C-001, C-002, C-007). I read TL:1258 and recorded only that `worker-list` runs before the "before" reads. I did not hold the Verification at TL:1260 against the Action, and I did not read the Branch logic of 6.2 at TL:989. No HIGH finding exists in V1.
5. *"Factual errors: 2.16 (X-003), pipx (X-006), item number (X-005)."* Concede all three. TL:347 reads "QA r3-b1, agent 9 of 9: rf-qa, SPEC-fidelity domain lens (report-only)", so 2.16 is not an edit. My conclusion (2.16 is not delivery for NFR-003) survives; my description does not.
6. *"Weakest calibration: 0.68, 4 citation failures, deviation clarity 0.25."* Concede. These are on the record and cannot be argued away. I note only that 0.25 is partly a calibrator-specific penalty for an omission all three cards share (S-008).
7. *"FR-010 `covered` without reading the edit wording (X-002)."* Concede in part. My row verdict rested on the 10.2 fixtures and the D9 gate at 8.4, and I never read research/04:90 or :148. The calibrated reading (V3 CAL: "wording ambiguity, not a lost rule", LOW) sits between my plain `covered` and V3's card. A fairer verdict for my row would have been `covered-in-substance` with a LOW note. I now give X-002 and C-003 to V3.
8. *"R8 marked covered without noticing 13.6 exceeds the row (C-013)."* Concede that I did not flag it. The row verdict itself ("one item per R1 to R8") is true; the over-scope bullet is a separate defect that only V3 found. C-013 to V3.

**From V2's and V3's shared assumption answers**

9. V2 rejects A-007 and implies my guard was assumed. I partly agree. I cited TL:2508 as the guard. That was weak: TL:2508 is the Context of lens 14.11, which uses `base-commit.txt` only to build a diff for the final review. It is not a pre-Phase-13 anchor check. The real guard is TL:224 (item 1.3): it records `git rev-parse HEAD` and says "If the HEAD sha does not start with `5dc29d23`, record the actual sha and add a note to `### Phase 1 Findings` that every research anchor must be re-checked against the new base". TL:1414 adds heading-based relocation for DESIGN line numbers. So the plan has a real, early guard, but it is a note, not a HALT, and it covers research anchors, not the `WORKER-CONTRACT.md:110` or `test_worker_contract.py` pins named in A-007. I stay at QUALIFY (below).

## Updated Assessment (V2 and V3)

**V2.** After reading its defense my view of V2 is higher than in Round 1, with one new reservation.
- R2-G7 is stronger than the card says. TL:989 Branch 1 fires on "`status` is PENDING **or** `Chosen:` is empty", so it still fires when `Chosen:` is filled but `status` is PENDING. Nothing in 6.2 writes `Chosen:`, `Decided by:` or `Decision source:` after the owner speaks (6.1 at TL:982 only creates them empty). The HALT rule at TL:192 ("set `status` to Blocked ... STOP, and do not tick the item") has no resume clause. So there are two missing links, not one: no step records the answer, and Branch 1 shadows Branch 2. TL:1165 (7.4) repeats Branch 1 and Branch 2 nearly word for word. HIGH holds.
- R2-G5 is stronger than the card says. DESIGN:466 makes `SweepResult.rows` a `tuple[ClassifiedRow, ...]`. So in a correct `models.py`, `ClassifiedRow` appears at least twice (its class line and the `rows` field), and `SessionRow` appears at least twice (its class line and `ClassifiedRow.row: SessionRow`, TL:1431). The check at TL:1434 ("every class and constant name in DESIGN section 7.2 appears once (`grep -c` per name)") cannot pass for a correct file. HIGH holds, and the defect is wider than one name.
- New reservation on R2-G3. TL:1258 step (6) tells the executor to run `echo "${XDG_STATE_HOME:-$HOME/.local/state}/ccsession/orca-tabs/"` and `ls -la <printed path>`. TL:1260 accepts "one of the eight templates or a file read". `echo` is not a template and not a file read, so the contradiction is real. But `ls -la` on a folder can be read as a file-system read, and the grep clause ("finds only the forbidden-list sentence") returns zero lines when nobody writes that sentence, which a lenient reader would count as "no forbidden token". So R2-G3 is the softest of the three HIGHs under a recovery-aware reading. I keep V2 as the winner on C-001 (nobody else found it) but with lower confidence than on C-002 and C-007.
- V2's self-inflicted problems are real and I stated them in Round 1: severity inflation (7 self HIGH, 3 calibrated), `gate-bypass` on G2 contradicted by its CAL, and rows that disagree with findings (X-007). V2 conceded all of them in Round 1. None changes the three HIGH findings.

**V3.** My view is unchanged on its strengths and slightly lower on its framing.
- Strengths that hold: R3-G4 (owner is asked the rule id, not the revised text, CAL MEDIUM), R3-G5 (11.1 "on every wake" without the bound that master carries at `WORKER-CONTRACT.md:110`), R3-G6 (13.6 extra scope), R3-G3 (dead `:545` greps, the only vacuous-pass finding), and the reuse checks. V3 is the only card on the Phase 2 to 6 design fixes, and without it those phases have no reviewer.
- V3 conceded R3-G10 (the gate that "HALTs rather than defaulting" never resumes), the generous grade 4, G9 and G10 as non-findings, and G7. With those concessions the card is a sound complement to V2, not a rival to it.
- Remaining weakness: V3 marks D6 `covered` on the 12.1 byte-for-byte copy and stops there, with only a pointer ("See R3-G4"). That is the same row-verdict-versus-finding gap it blames on V2, only smaller.

## New Evidence

1. **R2-G5 is broader than any card says** (settled by reading TL:1431, TL:1434 and DESIGN:466): `ClassifiedRow` and `SessionRow` each appear at least twice in a correct `models.py`. See Updated Assessment.
2. **6.2 and 7.4 have two missing links** (TL:982, TL:989, TL:1165, TL:192): no step writes the owner's answer into the decision file, and Branch 1 fires on PENDING before Branch 2 can set RESOLVED. The HALT rule has no resume clause.
3. **The A-007 guard is TL:224, not TL:2508.** Item 1.3 records the base sha and a re-check note; it does not HALT, and it does not cover the master pins (`WORKER-CONTRACT.md:110`, `test_worker_contract.py:25`). TL:2508 is only an input to a final review lens, so my Round 1 citation was wrong.
4. **R1-G3 is confirmed against DESIGN as well as TL.** TL:2509 says "find the test function in tests/sweep/ or tests/commands/test_sweep_command.py ... A missing or hollow test is BLOCKING". DESIGN:777 sends FR-023 to `tests/skills/test_worker_contract.py` and DESIGN:778 sends FR-024 to `tests/recommend/`, `tests/core/` and `tests/commands/test_routing_plugin_parity.py`. The lens prompt ranges over "every row of the section 12 trace", so these rows fall into its scope and it names no folder that holds their tests. Nobody disputes it (V2 and V3 both agree).
5. **X-004 reading.** DESIGN:216 reads: "which the NFR-004 import test enforces by forbidding `os` and `shutil`". So the tasklist follows the design's own stated enforcement. One residue that supports V2 modestly: TL:1432 tells `models.py` to import `pathlib`, and `pathlib.Path` has `stat` and `open`, which an `os` and `shutil` ban does not stop. That is a design question, not a tasklist gap, so it stays LOW and X-004 stays with V1.
6. **Row count.** The brief says my Round 1 table had 38 rows. Counting S-001 to S-009 (9), C-001 to C-015 (15), X-001 to X-012 (12) and A-001, A-002, A-007 (3) gives 39 in Round 1 as well. What Round 1 lacked was a real winner on X-006 and X-012, which I left as "none (internal)". Round 2 names a winner for both, so the table below has 39 rows, each with a winner.

## Per-Point Positions (Round 2)

| ID | Winner | Confidence | Reason |
|---|---|---|---|
| S-001 | V1 | 85 | Only card on FR, NFR and step rows (76); V2 and V3 cover GQ, D, SP, INF and the R rows. |
| S-002 | tie | 60 | Disjoint item lists reflect different scopes (Phase 7 to 14 delivery versus Phase 2 to 6 design fixes); X-011 shows neither refutes the other. |
| S-003 | V2 | 70 | Line ranges (`:1784-1788`) are the most checkable; all three notations are usable. |
| S-004 | V3 | 70 | Smallest self-to-calibrated gap and one downgrade; V2 had four HIGH cuts; V1 close behind. |
| S-005 | V2 | 85 | Only card with `recommended_action` and `not_checked`. |
| S-006 | V3 | 85 | 40 citations checked, 0 failed; V1 had 4 failed, V2 had 1. |
| S-007 | V2 | 80 | Every V2 finding asks for a change; V1 filed one confirmation (G5), V3 filed two (G9, G10). |
| S-008 | tie | 85 | All three omit the deviation category; only one calibrator penalised it, so scores are not comparable. |
| S-009 | V2 | 65 | Touches F1, F2, F3 and F7 by name; V1 touches F4, F6, F8; V3 touches F5 and F9. |
| C-001 | V2 | 85 | R2-G3: `echo` and `ls` (TL:1258) against "eight templates or a file read" (TL:1260); soft on `ls` and on the grep clause, firm on `echo`; V1 and V3 missed it. |
| C-002 | V2 | 92 | R2-G7 holds at TL:989 and TL:1165, with two missing links (no step records the answer; Branch 1 shadows Branch 2); V3's R3-G4 is a valid second mechanism. |
| C-003 | V3 | 65 | Conceded: V3 read the edit wording (LOW ambiguity); my plain `covered` did not. |
| C-004 | tie | 55 | R1-G2 (ID labels) and R2-G9 (matrix row B2) are both LOW partly and address different things. |
| C-005 | V2 | 90 | R2-G1: the DESIGN:78-80 count-citation rule has no tasklist item; analyst greps found 0 hits; MEDIUM. |
| C-006 | V1 | 95 | R1-G3 verified at TL:2509 and against DESIGN:777-778; CAL MEDIUM; no other card found it. |
| C-007 | V2 | 92 | R2-G5 holds at TL:1431, TL:1434 and DESIGN:466; wider than one name; V3's R3-G3 (vacuous pass) is a LOW addition. |
| C-008 | V2 | 75 | R2-G8 (no negative guard test, MEDIUM) beats my `covered` and V3's design preference (R3-G7). |
| C-009 | V2 | 65 | R2-G10 (SP-28 rationale deliverable, MEDIUM partly) survives; V1's R1-G6 contains a false clause. |
| C-010 | V1 | 55 | Only card that asked for the handoff line; CAL LOW, partly; the plan already documents grouping. |
| C-011 | tie | 60 | Conceded: V1's G5 and V3's G10 ordering parts both confirm without a defect; V3's owner-gate error is already counted under X-001. |
| C-012 | V3 | 70 | Conceded: R3-G5 (TL:1952 lacks the bound at `WORKER-CONTRACT.md:110`) is a real LOW; my row only described current SPEC text. |
| C-013 | V3 | 85 | R3-G6 holds (13.6 exceeds R8); my R8 row verdict was true but silent on over-scope. |
| C-014 | V3 | 80 | Only card that checked reuse against code (G8, G9); both LOW. |
| C-015 | V2 | 65 | Conceded: V2 followed INF-001 into a holding MEDIUM finding; my re-maps fed only a LOW partly (R1-G2). |
| X-001 | V2 | 95 | TL:982 and TL:989 confirm the deadlock; V3 conceded R3-G10. |
| X-002 | V3 | 65 | Calibrated reading is LOW wording ambiguity; V3 read the edit and I did not. |
| X-003 | V3 | 95 | TL:347 names 2.16 a report-only SPEC-fidelity lens. |
| X-004 | V1 | 65 | DESIGN:216 says the NFR-004 import test enforces B2; V2's critique is of the design; the B2 matrix omission is V2's LOW residue. |
| X-005 | tie | 60 | CAL is right on the item number (3, DESIGN:971); I am right that `M2` has 0 hits in TL; both residues are LOW. |
| X-006 | V1 (as calibrated) | 90 | TL:2488 shows `pipx run --spec` installs runtime dependencies, so the card clause loses and the CAL correction wins. |
| X-007 | V3 | 55 | Conceded: its covered-with-defect rows name their finding ids ("See R3-G4"); V1's rows do not contradict findings either, but link less. |
| X-008 | tie | 65 | V1 and V3 each took one downgrade; V2's `gate-bypass` HIGH is contradicted by its own CAL. |
| X-009 | V2 | 60 | Grade 2 fits three calibrated HIGH defects; V1 and V3 grade 4 is too generous (I conceded this in Round 1); no CAL scores grades, so confidence is moderate. |
| X-010 | V2 | 70 | V2 follows false matches to real delivery (INF-005 via 8.3, 8.4, 8.10; INF-014 via 7.2, 7.12); V3 stops at the false match. |
| X-011 | V1 | 60 | For the capture run the executable subject is 7.16 to 7.18; V3 judged the design text (2.4, TL:263); same row ID, different subjects. |
| X-012 | V3 (as calibrated) | 80 | CAL: the reflect precedent also replaces the whole `_git`, so R3-G7 is a design preference; the CAL correction wins. |
| A-001 | V3 | 65 | Only card that tested whether a delegated row survives the Phase 2 to 6 edits (R3-G1). |
| A-002 | V2 | 60 | Applies literal execution most consistently; all three HIGH findings rest on it; R2-G3 is the weakest under a recovery-aware reading. |
| A-007 | V3 | 55 | Only card that checked the master pins; V2's REJECT is too strict because TL:224 and TL:1414 already mitigate. |

## Final positions on shared assumptions

**A-001 (delegation counts as coverage): QUALIFY.** Unchanged in direction, tighter in wording. Accept delegation per row, and only when the delegated DESIGN row is read as revised by Phases 2 to 6 (A-004, stated in the 8.3 Context at TL:1431: "as revised by Phases 2 to 6"). R3-G1 shows the risk is real but small (LOW ambiguity). About 32 of my 76 verdicts rest on it, so I would mark them `covered-in-substance` and not `covered`.

**A-002 (judge checks as written): QUALIFY.** Use literal execution to decide whether a check can pass; use recovery awareness to decide how bad a failed check is. R2-G5 (8.3) and R2-G7 (6.2 and 7.4) stay HIGH under both readings, because no text inside the item lets a correct executor recover. R2-G3 (7.16) stays a defect but is softer: an executor can read `ls` as a file read and an empty grep as "no forbidden token". The CAL downgrades on R2-G2, R2-G8, R3-G2 and R1-G1 all follow this split.

**A-007 (master anchors stable until execution): QUALIFY.** Not REJECT and not plain ACCEPT. The plan has two real guards: TL:224 (record the base sha; if it moves, note that every research anchor must be re-checked) and TL:1414 (relocate DESIGN lines by section heading). Gaps: TL:224 is a note and not a HALT, and it names research anchors, not the master pins in A-007. Condition for acceptance: the executor treats a moved base sha as a stop for the master pins (`WORKER-CONTRACT.md:110`, `test_worker_contract.py:25`) before Phase 13.

## Merge guidance (short)

Take V2's three HIGH findings (R2-G7 widened to 7.4 and 14.7, R2-G5 widened beyond one name, R2-G3 flagged as the softest), V3's R3-G4, R3-G5, R3-G6, R3-G3 and reuse checks, and V1's R1-G3 plus the 76-row requirement ledger. Do not carry R1-G1 as a missing owner route, R1-G6's "installs nothing" clause, or V3's G9 and G10 as findings.
