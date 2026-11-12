# Round 2 rebuttal: Variant 1 (reviewer 1 card plus calibration)

- Protocol: sc-adversarial-protocol, Round 2 (sequential rebuttals, V1 goes first)
- Advocate persona: analyzer (evidence quality, logical consistency)
- Model: sonnet
- Focus: correctness, coverage, deviation-classification
- Inputs read: debate/round1-v1.md, round1-v2.md, round1-v3.md, diff-analysis.md
- Evidence re-read for this round (2026-11-08, before citing): tasklist lines 163, 194, 989, 1140-1142, 1244-1246, 1259-1277, 987-1005, 1436, 1478-1485, 1790-1796, 2256, 2467-2474; design lines 66, 181, 196, 219-221, 532, 552, 738, 868, 873, 875, 884, 971-973; coverage-matrix.yaml and the three reviewer-card row_coverage lists (union check)
- Paths: "tasklist" is `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md`; "design" is `docs/designs/orchestrator-mode.md`

## Response to criticisms

Each criticism of Variant 1 from Round 1 is answered below. "Concede" means I accept it and ask the merge to apply it. "Counter" means I give evidence against it.

### 1. Citation reliability (V2 and V3: 41 of 78 citations failed, four findings with empty evidence lists)

Concede the defect, counter the reach.

- The failure is real and narrow. I re-read the card: all 41 failed citations are the second `evidence` entry on the 26 FR rows and 15 NFR rows (a `grep -c 'orchestrator-mode.md:4[4-8][0-9]'` on the card prints 41). Design lines 444 to 472 are exit-mapping and rule-table prose, not requirement rows, so these numbers are very likely SPEC line numbers written under the design path. The first entry on the same rows (design lines 755 and up) is a different range and is not the failing one.
- So no row depends on a failed citation alone. Each FR and NFR row also names its delivering tasklist items (for example FR-002 lists items 8.10, 9.1, 10.7). The calibrator did not fail those. The rows stay usable as item-level verdicts; the second citation should be discarded.
- Concede that the tag `Grounded` on every row carried no signal (V3's point). It was applied without distinguishing a row whose second ref failed. The merge should treat the V1 row verdicts as "item-checked, second ref unreliable".
- Concede the four findings with empty evidence lists (R1-G5, R1-G6, R1-G7, R1-G9). R1-G5 and R1-G6 are nevertheless confirmed against tasklist lines 1260, 1262 and 1276, which I re-read this round; the evidence lived in the `location` and `claim` fields instead of the `evidence` list. That is a format fault, not a truth fault. R1-G7 is refuted and withdrawn (below).

### 2. R1-G7 refuted (V2, V3)

Concede in full. Item 9.3 reads the OQ-8 record and halts at tasklist 1640 to 1643. R1-G7 carries no weight. I do not defend U-010.

### 3. R1-G3, R1-G8, R1-G9 weakened (V2, V3)

- R1-G3: concede further than in Round 1. Tasklist line 1260 says "Compare before and after outputs with timestamps removed" and line 1262 says "apart from timestamps". The plan therefore does state a strip rule. What it lacks is a definition of which fields count as timestamps. The claim in my card ("no timestamp-strip rule") was overstated; the survivor is a LOW wording gap. I withdraw MEDIUM.
- R1-G8: concede, and go further than Round 1. I re-read line 163: "The Orca allowlist has ten read templates (eight called in Phase 1 plus the two R5 `worktree ps --agent-wait` forms); step 1.0a uses only templates 1 to 8". The eight called in Phase 1 are templates 1 to 8, which both the capture (items 7.16) and the Phase 1 code use. The sentence is accurate, so R1-G8 and V3's R3-G3 are not even wording defects. I withdraw both; see C-010 and A-003.
- R1-G9: concede the mechanism. Line 2471 recounts at the recorded base and tells the executor to replace each hit with the installed path. Severity LOW stands only as a fidelity note.

### 4. V1 missed R2-G1 and V3's whole R5 record thread (V3, V2)

Concede both.

- R2-G1 is a deterministic false rejection (tasklist 1436 "appears once (`grep -c` per name)" against `ClassifiedRow` fields at 1433 that repeat `SessionRow`, `Classification` and `SafeToClose`). I missed it, and I rank it first in the merge.
- The R5 record thread (C-017 to C-021) is also missed. Worse, my card listed the R5 decision as a strength. I re-verified three V3 claims this round and they hold (see New evidence).
- Consequence for my own Round 1 claim of "severity discipline": V3 and V2 are right that having zero HIGH is not discipline when the one real HIGH was missed. I withdraw that strength (see X-004).

### 5. Classification clarity 0.60, no four-category vocabulary (V2, V3)

Concede the score. A UC-1 card has no completed deviation to put in Drift or Regression, but the calibrator also found that R1-G3 and R1-G9 were mis-classed, and it scored V3's separation of design-fix from unsound-check at 0.85. I accept that V3's vocabulary was the clearer of the three (S-007).

### 6. R1-G1: `gate-bypass` label, and "dead end, not silent" (my own Round 1 concession, challenged by V3 on A-001d)

V3 said a QA fix cycle could "fix" the count by dropping a template. I conceded too much in Round 1. New evidence, from lines I re-read this round:

- Tasklist 8.10 Context (line 1482) says "From the 1.0a facts: ... the cursor field". Its Verification (line 1485) says the `ALLOWED_ORCA` count is 10. The item tells the executor to use a cursor field and to ship exactly ten templates, with no template that carries the cursor. The conflict is inside one item.
- 8.10 Verification has no stop clause. Compare 8.3 (line 1436), which says to stop before marking complete. The HALT rule at line 194 applies only where an item names it.
- Item 10.3 (line 1796) says "A test that exposes a code bug is fixed in the code". A failed ten-template pin routes to code, which means removing the extra template. The route is toward silent loss of the cursor, not toward the owner.
- Design 884 lists the cursor field as a step 1.0a item and design 552 says the template is "added only after step 1.0a captures the cursor field". The 7.17 Branch (line 1267) fires only if a live field name "differs from the name DESIGN section 7.2 or 7.3 uses". The design names no cursor field in 7.2 or 7.3 (grep for `cursor` in the design finds only lines 552, 884 and 973), so the Branch cannot fire for a cursor.

So the Round 1 phrase "loud, not silent" was wrong, and my retreat from `gate-bypass` should be partly reversed. I still keep MEDIUM, not HIGH, because a ten-template build with lower-bound totals is the design's own fallback (973), so correct delivery can satisfy the checks.

### 7. V2's A-001d: "generic QA may halt safely"

Counter. The shared QA Gate Protocol (line 188 onward) covers gate items; it does not attach to 8.10. And a gate reviewer checks code against the task text, which pins ten. A reviewer following the plan would pass the ten-template build. Nothing in the plan makes the failure loud.

### 8. V2: "V1's late-decision claim must be dropped; live-state objection must be narrowed"

Concede both (see items 2 and 3).

### 9. V3: "R1-G6's second sentence is unsupported"

Concede. Line 1259 says the agent-wait flag is not run in step 1.0a.

## Updated assessment of V2 and V3 after their defenses

### V2

- R2-G1 stays the top finding, and V2's defense adds a point I had not weighed: the HIGH is justified by a bar stated in words ("correct delivery cannot satisfy the check"). V2 also conceded all five downgrades cleanly (R2-G2 to R2-G5 to MEDIUM, R2-G7 to LOW), which makes its calibrated profile (one HIGH, five MEDIUM, three LOW) trustworthy.
- V2 withdrew the unconditional INF-019 "covered in substance" reading and agrees the CLOSED path has no explicit branch. That moves V2 onto my side on X-001 and X-005, so the remaining disagreement on those is small.
- V2 is right that R2-G6, R2-G8 and R2-G7 prove missing traceability and not a delivery failure. I accept those as LOW to MEDIUM traceability findings.
- One thing V2 did not address: its steelman of my R1-G1 treats it as an "execution-path completeness" finding, but its own A-001d answer ("generic QA may halt safely") contradicts that. See item 7 above.
- Not conceded: V2's claim that A-004c needs an "explicit disposition". Line 2471 already says "replace it with the installed path", which is a disposition for each hit. V2 and I agree on LOW.

### V3

- V3 is now the strongest card on the R5 and design-text thread. Three of its claims I re-verified directly:
  1. C-020 holds. Design line 221 reads "a new template in `ALLOWED_ORCA` (only after a capture, and never a write verb)". The string `agent-wait` does not appear on line 221, and the 6.3 step (5) discovery grep (`grep -n 'agent-wait' docs/designs/orchestrator-mode.md`) lists hits only at lines 66, 532, 738 and 873. No step of 6.3 can reach line 221.
  2. C-021 (15.1 half) holds, and more firmly than V3 argued. The only `agent-wait` text in design 15.1 is the forbidden-list entry on line 873. Step (4) of 6.3 removes it. Step (5) rewords "every other sentence that says `worktree ps` never carries `--agent-wait`", but after step (4) line 873 no longer says that. So the 6.4 pass rule ("the hits in ... 15.1 allow it", tasklist 1005) has no hit to find. The executor can follow 6.3 exactly and fail 6.4.
  3. C-018 holds. Design line 181 is `ALLOWED_ORCA (8)` and line 196 is `8 read templates`. The 6.3 grep is `'eight\|8 templates'`. "(8)" and "8 read templates" match neither string.
- V3's weakness that I raised (21 of 32 rows inferred, no HIGH, missed R2-G1) is real and V3 concedes all of it. I withdraw my R1 criticism that V3 offers "no view" on blast radius as a reason to rank it lower on the R5 thread; it only applies to Phase 8 to 10.
- V3's R3-G8 is correctly closed as superseded by item 5.4. I agree.
- Not conceded: V3's reading that the D10 half of R3-G6 is "overstated" and the 15.1 half "holds" is right, but its A-001d answer ("a QA fix cycle could drop a template") is better evidenced than V3 itself shows; my item 6 above supplies the missing lines (1482, 1485, 1796).

## New evidence

1. Coverage union check (settles A-006 and A-006a). I read the ids from `coverage-matrix.yaml` and the `row_coverage` lists of the three reviewer cards with a throwaway script (deleted afterwards). The matrix has 152 ids. The three card slices (V1 76, V2 44, V3 32) are disjoint, their union is 152, and there are no missing and no extra ids. The "missing rows" worry in A-006a is therefore not supported, and I change my answer from QUALIFY to ACCEPT. What remains is the A-006 point that each card's own verdicts have different reliability (V1 second refs, V3 21 of 32 inferred), which is a per-row weighting matter, not a coverage gap.
2. 8.10 internal conflict (tasklist 1482 against 1485). Context says use the cursor field from the 1.0a facts. Verification pins a count of 10 for `ALLOWED_ORCA` and has no stop clause. This is the new fact behind the A-001d reversal in the Response section, item 6.
3. Design 221 is out of reach of 6.3 (C-020). Line 221 holds the extension rule ("a new template in `ALLOWED_ORCA` (only after a capture, and never a write verb)") and contains no `agent-wait` string. The 6.3 discovery grep finds only lines 66, 532, 738 and 873.
4. 15.1 allowing hit disappears after step (4) (C-021, 15.1 half). Line 873 is the only `agent-wait` text in 15.1, and step (4) removes it. The 6.4 pass rule at tasklist 1005 then has no allowing hit to find.
5. Stale counts (C-018). Design 181 `ALLOWED_ORCA (8)` and 196 `8 read templates` match neither alternative of the 6.3 grep `eight\|8 templates`.
6. Line 163 is accurate. "ten read templates (eight called in Phase 1 plus the two R5 forms); step 1.0a uses only templates 1 to 8". This closes R1-G8 and R3-G3 for good (C-010, A-003).
7. 7.17 Branch is unreachable for the cursor. The Branch triggers on a live field name that differs from the name design 7.2 or 7.3 uses. Those sections name no cursor field. The `cursor` word occurs in the design only at 552, 884 and 973.
8. Possible extra gap for C-007, marked [INFERRED] because I did not open the file. `SOURCES.md` names the sanitize rules and sits in the fixtures folder that item 7.18 greps with `/home/coder\|coder`. A bare `coder` term could match prose in that file. Whether it does needs one grep; I did not run it.
9. 8.3 shows the plan can write a stop clause (1436 says stop before marking complete). Its absence from 8.10 is therefore an omission, not a style choice. This supports the A-001d reversal.
10. `core/CLAUDE.md` is stated untouched (tasklist 2256: the level table is not touched). That removes the concealment path V3 used for X-003 and C-011. See the table.
11. C-019 is accepted on V3's re-read. I did not re-verify it myself.

## Updated per-point positions

"Changed?" compares with my Round 1 position. "none" means no variant is superior or the point should not be decided for any variant. Unmarked entries repeat Round 1.

### Structure (S)

| id | superior | changed? | reason |
|---|---|---|---|
| S-001 | none | yes | V1's 76-row coverage table has no better evidence than the other two, given 41 failed second refs. V2's compact table and V3's inferred tagging each have their own cost. Equal. |
| S-002 | V3 | yes | V3 separates design-fix from unsound-check, and the calibrator scored its separation 0.85 against my 0.60. |
| S-003 | V2 | no | V2 puts the HIGH first, gives a stated bar and a remediation path per finding. |
| S-004 | V2 | no | V2's findings carry a clear what-fails-and-why shape. |
| S-005 | V2 | no | V2 has the best severity statement because it states the bar in words. |
| S-006 | none | no | Appendix layout does not change the verdicts. |
| S-007 | V3 | yes | Classification vocabulary. V1 has none, V3 is clearest. |
| S-008 | none | no | Evidence-list presentation is a style matter. |
| S-009 | none | no | Ordering of unique contributions does not decide anything. |
| S-010 | V3 | yes | V3's [INFERRED] tag is honest about 21 of 32 rows, which my blanket `Grounded` tag was not. |

### Content (C)

| id | superior | changed? | reason |
|---|---|---|---|
| C-001 | V1 | no | Coverage of the tasklist versus FR/NFR rows is widest in V1 (76 rows) and nothing in the defenses undid it. |
| C-002 | V1 | no | Same basis as C-001 for the design step rows. |
| C-003 | V1 | no | Row-level verdicts exist for all of the slice, though the second refs are unreliable. |
| C-004 | V1 | no | Kept, but at LOW only. R1-G3 survives as a wording gap about which fields count as timestamps. |
| C-005 | none | no | No variant has the better treatment. |
| C-006 | V2 | no | V2's traceability findings (R2-G6, R2-G8) hold up as missing-trace points. |
| C-007 | V1 | no | The live capture and sanitize thread in V1 (R1-G5, R1-G6) is confirmed at 1260, 1262 and 1276. The SOURCES.md point in New evidence 8 is a possible extension, [INFERRED]. |
| C-008 | V1 | no | R1-G5 and R1-G6 survive. |
| C-009 | none | yes | Round 1 gave V1 the edge on stale-count wording. Line 163 is accurate, so R1-G8 and R3-G3 both fail. |
| C-010 | none | yes | Same reason as C-009. No variant found a real defect in line 163. |
| C-011 | none | yes | Both mechanisms are overstated. `core/CLAUDE.md` is stated untouched at 2256, so no known concealment path exists. |
| C-012 | V2 | no | R2-G1 is the one finding that holds as HIGH. |
| C-013 | V2 | no | R2-G2 to R2-G5 at calibrated MEDIUM. |
| C-014 | V2 | no | Same. |
| C-015 | V2 | no | Same. |
| C-016 | V2 | no | Same. |
| C-017 | V3 | no | The R5 record thread is V3's. |
| C-018 | V3 | no | Verified: design 181 and 196 match neither alternative of the 6.3 grep. |
| C-019 | V3 | no | Accepted from V3's re-read, not re-verified by me. |
| C-020 | V3 | no | Verified: design 221 is unreachable by the 6.3 step (5) grep. |
| C-021 | V3 | no | Verified for the 15.1 half. The D10 half is overstated, as V3 itself says. |
| C-022 | none | no | No variant made the case. |
| C-023 | V3 | no | R3-G8 closed as superseded by item 5.4. V3's handling is right. |
| C-024 | V3 | no | Same thread. |
| C-025 | V3 | no | Same thread. |

### Contradictions between variants (X)

| id | superior | changed? | reason |
|---|---|---|---|
| X-001 | V1 | no | V2 has now withdrawn the unconditional "covered in substance" reading. The CLOSED path has no explicit branch. |
| X-002 | V1 | no | Unchanged. |
| X-003 | none | yes | Both mechanisms are overstated and `core/CLAUDE.md` is untouched at 2256. |
| X-004 | none | yes | V2's bar for HIGH is right but was applied unevenly, and V1 and V3 stated no bar. I withdraw "severity discipline" as a V1 strength because V1 missed the only HIGH. |
| X-005 | V1 | no | Follows X-001. |
| X-006 | V3 | no | Unchanged. |

### Adversarial points (A)

| id | superior | changed? | reason |
|---|---|---|---|
| A-001 | none | no | Overall R1-G1 severity is MEDIUM with no clear winner. |
| A-001a | none | no | Unchanged. |
| A-001b | none | no | Unchanged. |
| A-001c | none | no | Unchanged. |
| A-001d | V3 | yes | Reversed from "loud failure, dead end" to "silent omission". See Response item 6 and New evidence 2, 7 and 9. V3's QUALIFY answer was closer to right. |
| A-002 | none | no | Unchanged. |
| A-002a | none | no | Unchanged. |
| A-002b | none | no | Unchanged. |
| A-003 | none | yes | Line 163 is accurate, so neither side's reading wins. |
| A-003a | none | yes | Same. |
| A-004 | none | yes | R1-G9 is LOW only. Line 2471 already gives a disposition per hit. |
| A-004a | none | yes | Same. |
| A-004b | none | no | Unproven by anyone. |
| A-004c | none | no | V2 asks for an explicit disposition, but 2471 already says to replace with the installed path. LOW either way. |
| A-005 | V3 | no | R5 record thread. |
| A-005a | none | no | Unchanged. |
| A-005b | V3 | no | Verified on C-020 and C-021. |
| A-005c | none | no | Unchanged. |
| A-006 | none | yes | Response changed to ACCEPT after the union check. The remaining point is per-card reliability, not coverage. |
| A-006a | none | yes | QUALIFY becomes ACCEPT: 152 of 152 ids covered, disjoint, none missing or extra. |
| A-006b | none | no | Unchanged. |
| A-007 | none | no | Unchanged. |
| A-007a | none | no | Unchanged. |
| A-007b | none | no | Unchanged. |
| A-008 | none | no | Unchanged. |
| A-008a | none | no | Unchanged. |
| A-009 | V2 | no | V2 partly, on traceability. |
| A-009a | none | no | Unchanged. |
