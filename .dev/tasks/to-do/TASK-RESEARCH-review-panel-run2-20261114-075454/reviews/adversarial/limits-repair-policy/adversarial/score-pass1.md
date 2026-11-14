# Score Pass 1: slot C-06 limits-repair-policy (Step 3, hybrid scoring)

Scorer: neutral, pass 1 (input order: Variant A, then Variant B).
Variant A = `variant-1-original.md` (Proposal A, normalise before the parser). Variant B = `variant-2-original.md` (Proposal B, never edit reviewer text).
Scored: the two ORIGINAL proposals, not the debate outcome. Debate files were used only as pointers to defects; every defect used below was re-checked against the variant text or the code at HEAD (read-only).
Reproducibility: `uv run python quant-score.py` run twice gave identical stdout and an identical `quant-score-output.json` (sha256 `47a1bca452d1e5d86b7263ceefbb214afe69d884d99ff62c6572341542d8456a`).

## Part 1. Quantitative layer (deterministic)

### 1.1 Results

| Metric | Weight | Variant A | Variant B |
|---|---|---|---|
| RC requirement coverage | 0.30 | 1.0000 (14 of 14 stem sets matched) | 1.0000 (14 of 14) |
| IC internal consistency | 0.25 | 0.9725 (3 contradictions / 109 claims) | 0.9792 (3 contradictions / 144 claims) |
| SR specificity ratio | 0.15 | 1.0000 (60 concrete lines, 0 vague phrases) | 1.0000 (120 concrete lines, 0 vague phrases) |
| DC dependency completeness | 0.15 | 1.0000 (6 of 6 internal refs resolve) | 1.0000 (13 of 13) |
| SC section coverage | 0.15 | 0.7778 (7 H2 / max 9) | 1.0000 (9 H2 / max 9) |
| **quant_score** | | **0.9598** | **0.9948** |

### 1.2 Choices as defined in the script (also printed under `definitions` in the JSON)

- RC: the 14 requirements R01 to R14 with the exact stem sets from the task brief; matched when at least 3 stems are present (case-insensitive substring; `a|b` = either).
- IC: claims are prose sentences and table rows (one unit per row) that contain a digit, a file:line cite or a `[CODE-VERIFIED]`/`[UNVERIFIED]`/`[CODE-CONTRADICTED]`/`[RECOMPUTED]` tag. Headings, blank lines and table separator rows are not units. A: 160 units, 109 claims. B: 197 units, 144 claims. Contradictions come from the scorer's reading (1.3).
- SR: body = every line after the first 6 lines, minus headings, blank lines and table separators (A 66 body lines, B 135 body lines). Concrete = line with a digit, a file:line cite, or a backticked identifier. Vague = occurrences of `appropriate`, `as needed`, `properly`, `adequate`, `should consider`, `might`, `various`, `etc.`, `best practices`, `industry standard` (word-bounded, case-insensitive). Both variants have 0 occurrences of every phrase.
- DC: references are `section N` / `Section N.N` patterns. A: 6 internal refs, all resolve to a numbered heading; 2 refs excluded as external (both directly after a `research/...` token: `research/08` section 5 and `research/web-02` section 3). B: 13 internal refs, all resolve; 1 excluded as external (`research/08 section 7 point 9`).
- SC: A has H2 headings 1 to 7; B has H2 headings 1 to 9.

### 1.3 Intra-variant contradictions (the IC input, each with both sides quoted)

Variant A (3):

| Id | Side 1 | Side 2 | Why it is a contradiction |
|---|---|---|---|
| A-X1 | Section 1: "It touches no field the limits do not name." | Section 5, "Reference tokens survive the cut": "The step therefore copies any reference token found only in the cut text into `refs` while it has room (cap 8), and records `refs_lost` otherwise." A adds that this "is not in E2 R-02". | The step writes to `refs`, which none of the named limits (anchor, anchor2, quote, claim) covers. |
| A-X2 | Line 5: "Truncate `anchor` and `anchor2` to 200 and `claim` to 300 as an exact prefix" | Section 2 item 7: "claim to 297 characters plus `...` ... Position A takes that exact rule as the claim cut" | 297 characters plus a marker is not an exact prefix of the first 300; item 7 itself limits "exact prefixes" to anchor, anchor2 and quote. |
| A-X3 | Section 1: the step "removes 88 of the 92 measured drops, so ... the expensive, unmeasured step (re-ask) is left with at most 4 lines" (repeated in 3.4: "at most 4 lines") | Section 3.1: "88 of 92 ... [derived upper bound, not measured]"; section 5 M1: "a lower number means a second violation on the same line" | An upper bound on what the cut can fix is a lower bound on the residual; "at most 4" does not follow, and A's own M1 allows more. |

Variant B (3):

| Id | Side 1 | Side 2 | Why it is a contradiction |
|---|---|---|---|
| B-X1 | Section 4.4 totals and 4.6: "all 5 re-asked blocks recorded valid afterwards" / "5 of 5 re-asked blocks recorded valid" | Section 4.4 table, row E3: "reviewer 3 fully fixed; reviewer 2 still had two bad citations; '3 of 3 (to be confirmed by `review cluster`)'" | B's own table shows a re-asked block still invalid and one outcome unconfirmed. |
| B-X2 | Section 4.2: the refusal fires "on none of the 42 merges where a blocking row survived" | Section 4.2 table: "49 rows ... in 44 distinct triples and 42 distinct (row, package) merges" and "4 rows in 3 merges" with no blocking row left | The 42 merges are all merges with a dropped blocking line and include the 3 with no survivor; merges with a surviving blocking row number 39. |
| B-X3 | Sections 3.5 and 5 (INV-C, B-raise): "rewrites four boundary assertions" | Section 3.1 and section 2 INV-010 row: `card_convert.py` (`MAX_CLAIM = 300`) "must import the same constants under either policy"; its pin `tests/review/test_review_card_convert.py:500` asserts `len(f["claim"]) == 300` (read at HEAD) | If card_convert imports the raised claim constant, a fifth pin fails; B's four omits it. |

Considered and not counted (omissions or qualified statements, not stated opposites): A item 8 (compliance computed from a `repair=False` parse) against item 2 (`cluster_cmd` passes `repair=True`), because A never says where first-parse state is carried; A item 6 ("`--resume` ... documented nowhere") against 3.3 (S2 spike passed), documented versus tested; B 3.2 (re-ask only for blocking true or unknown drops) against its C-02 row (any over-limit line leaves `block_ok` False until the re-ask), a gap for reviewers whose only drops say `blocking: false`; B 4.5 bullet 4 against its last bullet, which B qualifies itself.

### 1.4 Reading note on RC

RC is 1.0 for both because the prescribed stem sets are loose: A contains the stems for R04 and R05 incidentally ("fail", "refus", "raise", "limit", "constants" occur in unrelated sentences), although A decides not to address the fail-closed rule (section 4.1: "Silent on ... not part of A") and never evaluates raising the limits. The qualitative layer (Completeness 1) carries that difference; the quant layer cannot see it.

## Part 2. Qualitative layer, pass 1

Order: Variant A evaluated first, then Variant B, per criterion. No partial credit. A MET verdict needs a quote or section reference.

### Completeness

**C1. Covers all explicit requirements from source input (R01 to R14)**
- A. CLAIM: not met in Variant A. EVIDENCE: R04 (fail-closed handling of a dropped blocking line) is declined: section 4.1, "Silent on: whether a residual dropped blocking line should make the merge fail closed? ... it is not part of A". R05 (raise-the-limits option) is not evaluated anywhere; searched sections 1 to 7 (section 6 says only "A PR or rf-qa module that wants a different limit declares it in its profile"). R01-R03, R06-R14 are present. VERDICT: NOT MET.
- B. CLAIM: met in Variant B. EVIDENCE: R04 section 3.3 ("New refusal reason `dropped-blocking`"); R05 section 3.5 ("The raise-the-limits lever (B-raise)"); R06-R08 section 5 (INV-C, INV-I, INV-G rows); R09 section 6; R10 section 7; R11 section 8; R12 section 2 table; R13 section 4.1 ("The loss unit is one finding in the v1 ledger and one reviewer in v2 clustering"); R14 section 4.2 (92 reasons, 49 blocking). VERDICT: MET.

**C2. Addresses edge cases and failure scenarios**
- A. EVIDENCE: section 3.2, a non-verbatim anchor "fails to locate cut or uncut ... kept with `anchor_status: missing`"; section 7 point 4, a shorter prefix "more likely to match twice"; section 5 M3, re-ask recovery "near zero" and the prompt "rewrites unlisted lines". VERDICT: MET.
- B. EVIDENCE: section 3.2, "A transport without the capability gets itemise-only plus the fail-closed rule of 3.3, never a truncation"; section 3.3, the acknowledgement exit "so that it cannot deadlock when a re-ask is impossible or fails"; section 4.4 rows A2, E3 (re-ask that could not be recorded; reviewer still invalid). VERDICT: MET.

**C3. Includes dependencies and prerequisites**
- A. EVIDENCE: section 4.1, "**Dependency:** if 'called from inside both parsers' is read as unconditional (no keyword), `test_review_findings.py:113,117` and `test_review_findings_v2.py:200,241` must be rewritten"; C-02 and C-03 rows "consistent and dependent". VERDICT: MET.
- B. EVIDENCE: section 2, "Where B is conditional on one: C-03's refusal object (without it B's fail-closed rule has no vehicle and falls back to a warning), and C-02's `block_ok` filter on clearing". VERDICT: MET.

**C4. Defines success and completion criteria**
- A. EVIDENCE: section 5 M1, "Position A is wrong on its central claim if fewer than 75 percent of the 48 blocking length lines come out located and unambiguous"; M2 and M3 each name a failure condition. VERDICT: MET.
- B. EVIDENCE: section 6 table, M1 "the `dropped-blocking` refusal fires on exactly the 3 merges of 4.2 and on none of the other 261"; T-B1 to T-B5 with "holds / any counterexample". VERDICT: MET.

**C5. Specifies what is explicitly out of scope**
- A. EVIDENCE: section 4.1, "Silent on: whether a residual dropped blocking line should make the merge fail closed ... it is not part of A"; section 5 M3 "the case for the truncation half" is separable from the re-ask half. VERDICT: MET.
- B. EVIDENCE: section 3.6 "What B does not do: No truncation step, no normaliser in front of the parser ... no change to a reviewer's `blocking`, `severity` or any other field"; section 9 lists facts it does not settle. VERDICT: MET.

### Correctness

**K1. No factual errors or hallucinated claims**
- A. CLAIM: not met. EVIDENCE: section 2 item 5 says `record_attempt` "raises only when the earlier attempt `complete`d" and that the re-ask "is therefore recorded as attempt 2". `src/superclaude/cli/review/manifest.py` (read at HEAD) also raises `OutOfOrder` when `stage in m["stages"]` (stage already committed), before the `complete` test; E1 run A2 notes record "Re-ask attempt could not be recorded in the manifest (stage 'collected' already committed; OutOfOrder refused)". Also section 1 states the cut "removes 88 of the 92" as fact while 3.1 labels it an upper bound (A-X3). VERDICT: NOT MET.
- B. CLAIM: not met. EVIDENCE: section 4.4 and 4.6 state "5 of 5 re-asked blocks recorded valid" while the E3 row in the same table shows "reviewer 2 still had two bad citations" and an unconfirmed "3 of 3" (B-X1); section 4.2 says "none of the 42 merges where a blocking row survived" although 3 of the 42 have no survivor (B-X2); "four boundary assertions" omits `test_review_card_convert.py:500` (B-X3). VERDICT: NOT MET.

**K2. Technical approaches are feasible with stated constraints**
- A. EVIDENCE: section 2 item 2, `parse_block(text, *, repair=False)` with the three production call sites passing `repair=True` keeps four direct pins unmodified; section 3.2 reports an executed check at HEAD (335-character anchor cut to 200 locates, repaired line passes `findings.parse_block`). The manifest recording claim is a separate factual error already scored in K1. VERDICT: MET.
- B. EVIDENCE: section 3.1 and 4.1, the classifier plus additive `dropped` key leaves accepted and rejected line sets identical; section 4.3 replay executed against HEAD parsers; section 3.3 states the C-03 refusal object as a dependency. VERDICT: MET.

**K3. Terminology used consistently and accurately**
- A. CLAIM: not met. EVIDENCE: the one step is called "normalise" (title and line 5), "truncate", "cut" and "repair" (`repair_line`, `repair=`); "exact prefix" is applied to `claim` on line 5 although item 7 says the claim is "297 characters plus `...`". VERDICT: NOT MET.
- B. EVIDENCE: section 3.1 defines `blocking_state` as `true`, `false` or `unknown`; "dropped", "itemise", "refusal reason `dropped-blocking`", "B-core" and "B-raise" are used with one meaning throughout (sections 1, 3.3, 3.5, 5). VERDICT: MET.

**K4. No internal contradictions (cross-validated with IC)**
- A. EVIDENCE: A-X1, A-X2, A-X3 (Part 1.3); IC 0.9725. VERDICT: NOT MET.
- B. EVIDENCE: B-X1, B-X2, B-X3 (Part 1.3); IC 0.9792. VERDICT: NOT MET.

**K5. Claims supported by evidence or rationale within the document**
- A. EVIDENCE: section 3.1 table gives each figure a source and a tag (`R02:99 ... [RECOMPUTED]`); section 3.2 lists the executed check and its result. VERDICT: MET.
- B. EVIDENCE: sections 4.1 to 4.3 tables with tags and the replay method ("1,222 unique report blobs ... 5,270 lines"); section 4.4 run-by-run table. VERDICT: MET.

### Structure

**S1. Logical section ordering**
- A. EVIDENCE: 1 position, 2 design consequence, 3 evidence, 4 invariants, 5 test or measurement, 6 effect on PR review and rf-qa, 7 strongest objection and answer; the objection comes last, after the material it attacks. VERDICT: MET.
- B. EVIDENCE: 1 position, 2 relation to C-01 to C-03, 3 design, 4 evidence, 5 invariants, 6 tests, 7 effect, 8 objection, 9 open facts. VERDICT: MET.

**S2. Consistent hierarchy depth (no orphaned subsections)**
- A. EVIDENCE: H2 sections 1 to 7; H3 only under 3 (3.1 to 3.4) and 4 (4.1); no H4. VERDICT: MET.
- B. EVIDENCE: H2 sections 1 to 9; H3 under 3 (3.1 to 3.6) and 4 (4.1 to 4.6); no H4. VERDICT: MET.

**S3. Clear separation of concerns between sections**
- A. EVIDENCE: evidence (3), invariants (4), tests (5), downstream effect (6) and objection (7) are separate sections. VERDICT: MET.
- B. EVIDENCE: slot relations (2), design (3), evidence (4), invariants (5), tests (6), effect (7), objection (8), open facts (9). VERDICT: MET.

**S4. Navigation aids present**
- A. EVIDENCE: header legend "`R02` = `research/02-finding-contract.md`, `S05` ... `S06` ..."; internal cross-references such as "See section 7." (item 7) and "(section 5)"; DC 6 of 6 resolve. VERDICT: MET.
- B. EVIDENCE: cross-references "(section 4.3)", "(section 3.3)", "Section 7"; DC 13 of 13 resolve; the INV-A..INV-N source named at the head of section 5. VERDICT: MET.

**S5. Follows conventions of the artifact type**
- A. EVIDENCE: "Status: Complete", a code-state line, tag legend, then position, design, evidence, invariants, test, downstream effect and objection, the structure the slot brief requires. VERDICT: MET.
- B. EVIDENCE: "Status: Complete" at lines 3 and 224, code-state line, tag legend, same required structure plus section 9. VERDICT: MET.

### Clarity

**L1. Unambiguous language (no "should consider", "might", "as appropriate")**
- A. EVIDENCE: SR scan of the body found 0 occurrences of all ten hedge phrases. VERDICT: MET.
- B. EVIDENCE: same scan, 0 occurrences. VERDICT: MET.

**L2. Concrete rather than abstract**
- A. EVIDENCE: item 1 gives the function signature "`repair_line(obj) -> (obj', repairs)` ... runs after `json.loads` and before `_check_finding` (`findings.py:188`)"; 60 concrete body lines. VERDICT: MET.
- B. EVIDENCE: section 3.1 table fixes the record shape "`{line, id, rule, field, actual, limit, blocking_state}`"; section 3.3 names the refusal reason, exit code and acknowledgement fields; 120 concrete body lines. VERDICT: MET.

**L3. Each section has a clear purpose or can be summarised in one sentence**
- A. EVIDENCE: section 1 is titled "The position in one paragraph"; sections 3 to 7 are named by function (Evidence, Invariants, test, effect, objection). VERDICT: MET.
- B. EVIDENCE: section 1 "The position in one paragraph"; sections 2 to 9 named by function; section 9 "Open facts this proposal does not settle". VERDICT: MET.

**L4. Acronyms and domain terms defined on first use**
- A. CLAIM: not met. EVIDENCE: "GQ-017" (section 3.2 heading), "CO-8 is decided" (item 7), "DR-006" (M1), "FX-1" (section 6), "E1" and "E2" (section 3.3) appear with no definition; only R02, S05 and S06 are defined in the header. VERDICT: NOT MET.
- B. CLAIM: not met. EVIDENCE: "INV-C" is used in section 2 (INV-003 row) before section 5 names the source of INV-A..INV-N; "C-08", "C-10", "C-11", "GQ-017" (4.3) and "debate N-B3" (section 2 row 1) are undefined; E1 and E2 are used without a definition. VERDICT: NOT MET.

**L5. Actionable next steps or decision points clearly identified**
- A. EVIDENCE: section 7 point 1, "if the owner reads the sentence as covering code, Position A is wrong as written and the sentence has to be amended ... or the policy changes to B"; M1 "75 percent figure is my proposal, to be fixed before the run; the owner may change it". VERDICT: MET.
- B. EVIDENCE: section 3.5 and 9, "Whether the owner accepts a widening of the findings-v1 grammar (B-raise); that is an owner decision"; section 6 "Rules for each measurement are written to a file before the first run". VERDICT: MET.

### Risk Coverage

**R1. At least 3 risks with probability and impact assessment**
- A. CLAIM: not met. EVIDENCE: only the re-ask exposure is bounded (section 7 point 5, "at most 4 of 92 lines (1 of 49 blocking) depend on re-ask recovery"). Wrong occurrence (point 4) gives a qualitative likelihood only ("more likely to match twice ... the one I cannot close from code"); false-blocker rows (M2) have a stated impact (rejected row "stays `open` and only `defer` clears it") but no likelihood. Searched sections 3.4, 5, 7. VERDICT: NOT MET.
- B. EVIDENCE: section 8 point 1, refusal exposure "3 of 264 merges" and re-ask volume "44 reviewer runs, not 80"; section 4.3, claim cut "34 claims ... 3 to 135 characters, median 37.5, 9 cut more than 60"; section 8 point 5, repeat-violation risk with the stated consequence "B's cost becomes refusals" (luna 27 of 30 drops are anchors, M2). VERDICT: MET.

**R2. Mitigation strategy for each identified risk**
- A. CLAIM: not met. EVIDENCE: most risks have one (copy-to-`refs` for lost tokens; "keep the line but mark `anchor_ambiguous`" for ambiguity; stateless prompt for the dispatch paths), but the false-blocker risk in section 5 M2 ("this is a real cost to count, not assume") has only a measurement and a kill line, no mitigation. VERDICT: NOT MET.
- B. EVIDENCE: stall exposure, the acknowledgement option (3.3); no re-ask transport, "degrades to itemise plus refusal-on-PASS-by-loss" (section 8 point 4); headless path, "B excludes that path until isolation exists" (INV-G row); repeat offenders, B-raise and the brief change (section 8 point 5). VERDICT: MET.

**R3. Failure modes and recovery procedures**
- A. EVIDENCE: section 7 point 4 (on many ambiguous anchors keep the line, mark `anchor_ambiguous`, refuse to let the row clear on a `prior resolved` alone); section 5 M3 (if re-ask recovery is near zero "the position reduces to truncation plus itemised drops"). VERDICT: MET.
- B. EVIDENCE: section 3.3 (refusal when the round has no blocking row and a true or unknown line was dropped; acknowledgement as the human exit); section 3.2 (transport without the capability). VERDICT: MET.

**R4. External dependencies and their failure scenarios**
- A. EVIDENCE: section 4.1 C-02 and C-03 rows; INV-I row "if those slots decide otherwise the block stays `block_ok` False with its repaired findings kept"; item 6, "`--resume` for gateway model ids is documented nowhere ... the stateless form does not depend on it". VERDICT: MET.
- B. EVIDENCE: section 2 ("without it B's fail-closed rule has no vehicle and falls back to a warning"); section 3.2 (the record shape "belongs to slot C-08", E1 run A2 refusal); `--resume` "[UNVERIFIED] for other gateway ids". VERDICT: MET.

**R5. Monitoring or validation mechanism for risk detection**
- A. EVIDENCE: section 5 M4, "Track `repaired_lines_rate` per model next to first-parse compliance. A rising repair rate means the brief is failing to state the limits"; M1 to M3 replays. VERDICT: MET.
- B. EVIDENCE: section 3.1 `dropped` record and the conservation property ("every non-blank line ... is exactly one of kept finding, prior line, or dropped record"); section 6 M1 to M3 and T-B1 to T-B5. VERDICT: MET.

### Invariant & Edge Case Coverage

**E1. Boundary conditions for collections (empty, single-element, maximum size)**
- A. EVIDENCE: section 5 Boundary, "200 and 300 characters pass both with and without repair; 201 and 301 fail with `repair=False`"; section 5 refs copy "while it has room (cap 8)" and `refs_lost` when full; a 205-character raw anchor that flattens to 190 is not repaired. VERDICT: MET.
- B. EVIDENCE: section 6 T-B3, "one reviewer with only dropped blocking lines (today's refusal at `ledger.py:150-157` stays); two reviewers, one with a dropped blocking line and one with an empty valid block"; section 4.2 total-loss merges "6 of 6 and 8 of 8 lines". VERDICT: MET.

**E2. State variable interactions across component boundaries**
- A. EVIDENCE: INV-I row, "`block_ok` becomes True for a reviewer whose only fault was length, so that reviewer counts for clearing and quorum. That is a C-02 and C-03 policy over `block_ok`"; item 8, the compliance metric from a `repair=False` parse. VERDICT: MET.
- B. EVIDENCE: section 2 C-02 row, "an over-limit finding line makes the reviewer `block_ok` False, so its `prior` lines do not count until the re-ask returns a valid block"; section 3.3 `block_ok` and `complete` for quorum. VERDICT: MET.

**E3. Guard condition gaps (missing validation, unguarded type assumptions)**
- A. EVIDENCE: item 3, "`finding_id` and `blocking` are read from the raw object when it is a dict"; section 4.1, the step "never creates `anchor`, `quote` or `citations`"; section 5 idempotence and non-invention tests. VERDICT: MET.
- B. EVIDENCE: section 3.1, `blocking_state` is "`true`, `false` or `unknown` (absent or non-boolean `blocking`)"; section 2 C-02 row, "a `prior` line with a bad status is itemised too (`findings.py:175-186`)". VERDICT: MET.

**E4. Count divergence (off-by-one, inclusive/exclusive ranges, unit mismatches)**
- A. EVIDENCE: section 3.1, "80 reviewer-runs with `block ok false` (a count of runs, not findings)" and the unit mismatch with 92; "the '4' of `COMBO-REPORT.md:292` is not reproduced"; section 5, limit measured after `flat()`. VERDICT: MET.
- B. EVIDENCE: section 4.2 distinguishes 92 lines, 49 blocking rows, 44 triples, 42 merges, 80 runs; "Four verdicts flipped ... [CODE-CONTRADICTED] as '4'"; section 4.1, "Length is counted after whitespace flattening, in characters". VERDICT: MET.

**E5. Interaction effects when features or components combine**
- A. EVIDENCE: section 5, a cut can remove `AC-0.4` found only in the tail and "change `fp` and `same_defect`" (`refs_norm`); section 3.2 and 7 point 4, a shorter prefix with `locate` taking the first match; repair combined with C-02 clearing and C-03 quorum (4.1). VERDICT: MET.
- B. EVIDENCE: section 3.5, "together they leave about 4 lines in 124 for the re-ask" (B-core with B-raise); section 2, the `dropped-blocking` refusal combined with C-02 `block_ok` filter and C-03 refusal object and exit 12. VERDICT: MET.

### Qualitative summary

| Dimension | Variant A | Variant B |
|---|---|---|
| Completeness | 4 / 5 | 5 / 5 |
| Correctness | 2 / 5 | 3 / 5 |
| Structure | 5 / 5 | 5 / 5 |
| Clarity | 4 / 5 | 4 / 5 |
| Risk Coverage | 3 / 5 | 5 / 5 |
| Invariant & Edge Case Coverage | 5 / 5 | 5 / 5 |
| **Total met** | **23 / 30** | **27 / 30** |
| **qual_score** | **0.7667** | **0.9000** |

### Edge Case Floor Check (Invariant & Edge Case Coverage, floor 1 of 5)

| Variant | Score | Eligible as base |
|---|---|---|
| A | 5 / 5 | Yes |
| B | 5 / 5 | Yes |

The floor is not suspended (neither variant scores 0 of 5).

### Pass 1 provisional combined score (before pass 2 and any re-evaluation)

| Variant | 0.5 x quant | 0.5 x qual | Combined |
|---|---|---|---|
| A | 0.4799 | 0.3833 | 0.8632 |
| B | 0.4974 | 0.4500 | 0.9474 |

Margin B over A: 0.0842 (above the 0.05 tiebreaker band on pass 1 alone).

### Verdict table

| Criterion | Variant | Pass 1 verdict | Evidence |
|---|---|---|---|
| Completeness 1 | A | NOT MET | R04 declined (4.1 "not part of A"); R05 absent |
| Completeness 1 | B | MET | R04 3.3, R05 3.5, R06-R14 sections 2, 4 to 8 |
| Completeness 2 | A | MET | 3.2 missing anchor status; 7 pt 4; M3 |
| Completeness 2 | B | MET | 3.2 transport; 3.3 deadlock exit |
| Completeness 3 | A | MET | 4.1 Dependency note; C-02/C-03 rows |
| Completeness 3 | B | MET | section 2 conditional on C-03 object and C-02 filter |
| Completeness 4 | A | MET | M1 75 percent kill line |
| Completeness 4 | B | MET | section 6 M1 and T-B1 to T-B5 |
| Completeness 5 | A | MET | 4.1 "Silent on ... not part of A" |
| Completeness 5 | B | MET | 3.6 "What B does not do"; section 9 |
| Correctness 1 | A | NOT MET | manifest.py OutOfOrder at committed stage vs 2 item 5 |
| Correctness 1 | B | NOT MET | 4.4 "5 of 5" vs E3 row; 4.2 "42 merges" |
| Correctness 2 | A | MET | repair keyword; executed check 3.2 |
| Correctness 2 | B | MET | additive classifier; replay 4.3 |
| Correctness 3 | A | NOT MET | "exact prefix" for claim vs 297 plus "..."; four names for one step |
| Correctness 3 | B | MET | blocking_state and dropped terms uniform |
| Correctness 4 | A | NOT MET | A-X1, A-X2, A-X3 |
| Correctness 4 | B | NOT MET | B-X1, B-X2, B-X3 |
| Correctness 5 | A | MET | 3.1 sourced and tagged figures |
| Correctness 5 | B | MET | 4.1 to 4.4 sourced tables and replay method |
| Structure 1 | A | MET | order 1 to 7 |
| Structure 1 | B | MET | order 1 to 9 |
| Structure 2 | A | MET | H2 with H3 only, no orphans |
| Structure 2 | B | MET | H2 with H3 only, no orphans |
| Structure 3 | A | MET | separate evidence, invariants, tests, effect, objection |
| Structure 3 | B | MET | separate sections 2 to 9 |
| Structure 4 | A | MET | legend; "See section 7"; DC 6/6 |
| Structure 4 | B | MET | section cross-refs; DC 13/13 |
| Structure 5 | A | MET | status line, required proposal sections |
| Structure 5 | B | MET | status line, required proposal sections |
| Clarity 1 | A | MET | 0 hedge phrases |
| Clarity 1 | B | MET | 0 hedge phrases |
| Clarity 2 | A | MET | signature and call sites named |
| Clarity 2 | B | MET | record shape, refusal reason, exit code |
| Clarity 3 | A | MET | section 1 one-paragraph purpose |
| Clarity 3 | B | MET | section 1 one-paragraph purpose |
| Clarity 4 | A | NOT MET | GQ-017, CO-8, DR-006, FX-1, E1/E2 undefined |
| Clarity 4 | B | NOT MET | INV-C before definition; C-08, C-10, C-11, N-B3, E1/E2 undefined |
| Clarity 5 | A | MET | 7 pt 1 owner dependency; M1 threshold owner-changeable |
| Clarity 5 | B | MET | 3.5 and 9 owner decision |
| Risk Coverage 1 | A | NOT MET | only re-ask exposure bounded; others no likelihood |
| Risk Coverage 1 | B | MET | 3 of 264; 44 vs 80; 34 claims, 9 over 60 |
| Risk Coverage 2 | A | NOT MET | M2 false-blocker risk has no mitigation |
| Risk Coverage 2 | B | MET | ack exit; degrade path; exclude headless; B-raise |
| Risk Coverage 3 | A | MET | 7 pt 4 fallback; M3 degrade |
| Risk Coverage 3 | B | MET | 3.3 refusal and exit; 3.2 degrade |
| Risk Coverage 4 | A | MET | C-02/C-03 conditions; --resume not required |
| Risk Coverage 4 | B | MET | C-03 object, C-08 record, --resume UNVERIFIED |
| Risk Coverage 5 | A | MET | M4 repaired_lines_rate |
| Risk Coverage 5 | B | MET | dropped record; conservation test; M1 to M3 |
| Invariant & Edge Case 1 | A | MET | 200/201, 300/301, refs cap 8 |
| Invariant & Edge Case 1 | B | MET | T-B3 single reviewer, empty block; total-loss merges |
| Invariant & Edge Case 2 | A | MET | block_ok True after length repair (INV-I row) |
| Invariant & Edge Case 2 | B | MET | block_ok False and priors (C-02 row) |
| Invariant & Edge Case 3 | A | MET | blocking read "when it is a dict"; no invented anchor |
| Invariant & Edge Case 3 | B | MET | blocking_state unknown; bad prior lines itemised |
| Invariant & Edge Case 4 | A | MET | flat() length vs raw; run vs line units |
| Invariant & Edge Case 4 | B | MET | 92/49/44/42/80 units; "4" flipped contradicted |
| Invariant & Edge Case 5 | A | MET | refs_norm, fp, locate first-match interactions |
| Invariant & Edge Case 5 | B | MET | B-core with B-raise; refusal with C-02/C-03 |

### Machine-readable verdicts

PASS1|Completeness|1|A|NOT MET
PASS1|Completeness|1|B|MET
PASS1|Completeness|2|A|MET
PASS1|Completeness|2|B|MET
PASS1|Completeness|3|A|MET
PASS1|Completeness|3|B|MET
PASS1|Completeness|4|A|MET
PASS1|Completeness|4|B|MET
PASS1|Completeness|5|A|MET
PASS1|Completeness|5|B|MET
PASS1|Correctness|1|A|NOT MET
PASS1|Correctness|1|B|NOT MET
PASS1|Correctness|2|A|MET
PASS1|Correctness|2|B|MET
PASS1|Correctness|3|A|NOT MET
PASS1|Correctness|3|B|MET
PASS1|Correctness|4|A|NOT MET
PASS1|Correctness|4|B|NOT MET
PASS1|Correctness|5|A|MET
PASS1|Correctness|5|B|MET
PASS1|Structure|1|A|MET
PASS1|Structure|1|B|MET
PASS1|Structure|2|A|MET
PASS1|Structure|2|B|MET
PASS1|Structure|3|A|MET
PASS1|Structure|3|B|MET
PASS1|Structure|4|A|MET
PASS1|Structure|4|B|MET
PASS1|Structure|5|A|MET
PASS1|Structure|5|B|MET
PASS1|Clarity|1|A|MET
PASS1|Clarity|1|B|MET
PASS1|Clarity|2|A|MET
PASS1|Clarity|2|B|MET
PASS1|Clarity|3|A|MET
PASS1|Clarity|3|B|MET
PASS1|Clarity|4|A|NOT MET
PASS1|Clarity|4|B|NOT MET
PASS1|Clarity|5|A|MET
PASS1|Clarity|5|B|MET
PASS1|Risk Coverage|1|A|NOT MET
PASS1|Risk Coverage|1|B|MET
PASS1|Risk Coverage|2|A|NOT MET
PASS1|Risk Coverage|2|B|MET
PASS1|Risk Coverage|3|A|MET
PASS1|Risk Coverage|3|B|MET
PASS1|Risk Coverage|4|A|MET
PASS1|Risk Coverage|4|B|MET
PASS1|Risk Coverage|5|A|MET
PASS1|Risk Coverage|5|B|MET
PASS1|Invariant & Edge Case Coverage|1|A|MET
PASS1|Invariant & Edge Case Coverage|1|B|MET
PASS1|Invariant & Edge Case Coverage|2|A|MET
PASS1|Invariant & Edge Case Coverage|2|B|MET
PASS1|Invariant & Edge Case Coverage|3|A|MET
PASS1|Invariant & Edge Case Coverage|3|B|MET
PASS1|Invariant & Edge Case Coverage|4|A|MET
PASS1|Invariant & Edge Case Coverage|4|B|MET
PASS1|Invariant & Edge Case Coverage|5|A|MET
PASS1|Invariant & Edge Case Coverage|5|B|MET

END-OF-SCORE-FILE
