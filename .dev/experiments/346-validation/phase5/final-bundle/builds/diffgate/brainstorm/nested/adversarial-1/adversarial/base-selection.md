# Base Selection Report

- Generated: 2026-11-08T15:36:46Z (Step 3 of the adversarial pipeline, depth standard)
- Variants: A = `variant-1-opus-architect.md` (opus:architect), B = `variant-2-sonnet-refactorer.md` (sonnet:refactorer), C = `variant-3-haiku-qa.md` (haiku:qa)
- Inputs: `diff-analysis.md` (including its Fact check), `debate-transcript.md` (Metadata, Scoring Matrix, Convergence Assessment), `debate/round2-A.md`, `debate/round2-B.md`, `debate/round2-C.md`, `debate/evidence-flg-r1.md`, `invariant-probe.md`, source `../../../seed-brief.md`
- Debate status: 99% convergence, gate BLOCKED_BY_INVARIANTS (7 HIGH UNADDRESSED). Per the transcript, the base is force-selected by score and Step 4 adopts each invariant Resolution.

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant A (opus:architect) | Variant B (sonnet:refactorer) | Variant C (haiku:qa) |
|--------|--------|-------------------|-------------------|-------------------|
| requirement_coverage | 0.30 | 1.000 (10 of 10) | 1.000 (10 of 10) | 1.000 (10 of 10) |
| internal_consistency | 0.25 | 0.991 (1 - 2/230) | 0.991 (1 - 2/231) | 0.990 (1 - 2/196) |
| specificity_ratio | 0.15 | 0.995 (199/200) | 0.995 (203/204) | 0.992 (132/133) |
| dependency_completeness | 0.15 | 1.000 (64/64) | 0.976 (81/83) | 1.000 (4/4) |
| section_coverage | 0.15 | 0.929 (13/14) | 0.857 (12/14) | 1.000 (14/14) |
| **quant_score** | | **0.986** | **0.972** | **0.996** |

### Computation details

All counts were taken from the variant text with one read-only Python pass (stdlib `re`, run through `uv run --no-project python -I` from standard input; no file written). Headings and lines inside fenced code blocks were excluded, because several variants show `##` lines inside fences (A lines 138, 237, 262-269; B lines 110-123, 233, 304, 390-394).

**Requirement Coverage (RC).** The seed brief has no formal requirement ids, so section-level topic matching applies (scoring protocol, RC edge case). The requirement list is the brief's 6 Constraints (K1 to K6) and 4 Success Criteria (S1 to S4). A requirement counts as referenced when every keyword pattern of its topic occurs in the variant:

| Id | Requirement (seed brief) | Patterns (all must match, case-insensitive) | A | B | C |
|---|---|---|---|---|---|
| K1 | Additive variant `spec-panel-diffgate`; `/sc:spec-panel` untouched | `spec-panel-diffgate`; `additive\|untouched\|not touched\|not edited\|unchanged` | yes | yes | yes |
| K2 | Mechanical over prose; every remaining prose rule named with its residual risk | `residual\|remaining`; `prose` | yes | yes | yes (via "remaining cost", "Still prose") |
| K3 | Builds on 427 text, keeps the 7 bullets' literals | `427`; `literal\|bullet` | yes | yes | yes |
| K4 | No new dependency; stdlib `difflib` via `uv run`; installed path | `difflib`; `uv run`; `~/.claude/skills` | yes | yes | yes |
| K5 | 3-review cap unchanged | `3 reviews\|CAP_REVIEWS\|MAX_ROUNDS` | yes | yes | yes |
| K6 | Honest cost accounting | `tool call`; `session`; `wall time\|minutes` | yes | yes | yes |
| S1 | R3 critical+major 3 or fewer in both replicates or clean PASS; growth 44.4% or less | `44\.4`; `3 or fewer\|<=3` | yes | yes | yes |
| S2 | Unanchored finding handled by a script | `neither\|no valid\|anchor=none`; `deferred\|reject` | yes | yes | yes |
| S3 | Line changed by fix k reviewable in k+1 only | `k\+1\|N\+1\|next review\|immediate next review\|one look` | yes | yes | yes |
| S4 | Pre-existing defects in a deferred list shown once | `deferred`; `once` | yes | yes | yes |

The first K2 pattern used only `residual`, which C does not contain; the topic in the brief is "remaining prose rule ... residual risk", so the pattern was widened to `residual|remaining` before scoring, for all three variants. RC measures reference, not correctness. Whether a variant actually satisfies K4 (A and B copy a `src/superclaude` path into an installed primitive) is scored under Correctness.

**Internal Consistency (IC).** Scorable claims = substantive lines outside fences (non-blank, not headings, not table separator rows): A 230, B 231, C 196. Contradictions counted are the intra-variant ones in `diff-analysis.md` plus one found in this step:

| Variant | Contradictions | Source |
|---|---|---|
| A | 2 | X-015 (byte copy versus "the string `src/superclaude` is absent", 8.1 and 8.5); deferred-list order: section 2 "End" row and section 6 say `final` output is appended to the report, while bullet 9 (8.1) says "above the verdict line" and bullet 3 says the verdict is the last line (also INV-027) |
| B | 2 | X-016 (byte-identical copy and drift guard versus "no `src/superclaude` string anywhere"); X-018 (replay "would have allowed 13" versus its own F1 rule giving 14) |
| C | 2 | X-017 (new `## Unattended mode` section versus "Do not edit ... worker contract" while 13 P1 expects `tests/skills/test_worker_contract.py` to pass); X-008 intra part (bar row "Open CRITICAL+MAJOR proxy" versus "the independent recorder retains the original severity proxy counting rule" versus deferred findings "excluded from the scoped blocker metric") |

X-012 (B and C omit or forbid the `tests/recommend/test_routing_refresh.py` edit) conflicts with the repository, not with another claim in the same variant, so it is scored under Correctness criterion 1, not here.

**Specificity Ratio (SR).** A substantive line is concrete when it contains a digit, a backtick, or a named entity (`difflib`, `SequenceMatcher`, `Orca`, `SHA-256`, `JSON`, `UTF-8`, `Python`, `pytest`, `argparse`). Vague count = occurrences of the protocol's vague indicators (`appropriate`, `as needed`, `properly`, `adequate`, `should consider`, `might`, `various`, `etc.`, `best practice`, `industry standard`, `as appropriate`, plus `reasonable`, `some`). Matches: A line 23 "some" (quantity), B line 15 "some" (quantity), C line 287 "as appropriate". SR = concrete / (concrete + vague).

**Dependency Completeness (DC).** References counted: "section N" or "section N.M" (excluding references to other documents such as "design doc section 12"), parenthesised `(N.M)` refs, rule ids (A: C1 to C13, V1 to V5, "open question 3"; B: C1 to C13, C2b, F1 to F4, R1 to R12, "cause N"). A: 20 section refs plus 44 rule-id occurrences, all defined. B: 27 section refs (the "5.1" ref resolves to the bold label "**5.1 Reviewed once, by construction**"), 53 rule-id occurrences, and 3 "cause N" refs; the two "cause 3" refs (5.2 "This removes cause 3 of section 1" and 5.5 "It lowers the number of fixes (cause 3)") point to row 3 of the section 1 table, which is "Severity drift", while the text means row 2 ("Revisers add work"): 2 unresolved, 81/83. C: 4 section refs ("section 10", "section 13", "sections 2-6"), all defined.

**Section Coverage (SC).** H2 headings outside fences: A 13 (sections 0 to 12), B 12 (1 to 12), C 14 (1 to 14). Max 14.

**Formula.** quant = 0.30 RC + 0.25 IC + 0.15 SR + 0.15 DC + 0.15 SC.

- A: 0.300 + 0.2478 + 0.1493 + 0.1500 + 0.1393 = **0.9864**
- B: 0.300 + 0.2478 + 0.1493 + 0.1464 + 0.1286 = **0.9721**
- C: 0.300 + 0.2474 + 0.1489 + 0.1500 + 0.1500 = **0.9963**

The quantitative layer barely separates the variants (spread 0.024); the qualitative layer decides.

## Qualitative Scoring (50% weight) - Additive Binary Rubric

Claim-Evidence-Verdict (CEV) format: for every cell the CLAIM is "criterion N is met in Variant X"; the Evidence column quotes or cites the variant (or records "no evidence found" with the sections searched); the Verdict column is MET (1) or NOT MET (0). No MET is given without a cited quote or section. Verdicts below are the final ones after the two position-bias passes and re-evaluation (see Position-Bias Mitigation).

### Completeness (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence | Variant C | Evidence |
|-----------|-----------|----------|-----------|----------|-----------|----------|
| 1. Covers all explicit requirements | MET | All 10 seed requirements referenced (RC 10/10): additive variant (8, "`/sc:spec-panel` (both copies) ... are not edited"), cap constant `CAP_REVIEWS = 3` (3.6), deferred list (6), S1 bar (9), costs (10). | MET | RC 10/10: "Additive variant command `spec-panel-diffgate`" (header), cap "`begin` enforces it" (5.4), deferred list (6), bar "3 or fewer in both replicates" (9), costs table (10). | MET | RC 10/10: "Ship an additive critique-mode command" (1), canonical cap retained (2), deferred (6), bar table (9), "Cost envelope" (10). |
| 2. Addresses edge cases and failures | MET | Section 2 "What happens when an actor skips its step" table; 4.3 "On reject"; 16 test cases (8.4) incl. "A pure deletion yields a hunk with an empty changed span". | MET | Section 2 "Where a model could skip a step, and what then happens"; tests "pure deletion gives before and after lines", "ledger corrupt exits 6" (8.3). | MET | Section 13 P0 cases "Empty diff", "Delete-only", "Empty file, invalid UTF-8, BOM, CRLF and no final newline". |
| 3. Includes dependencies and prerequisites | MET | 3.2 "Python 3.10 stdlib only"; "A script reaches `~/.claude/skills/` only inside a folder that has a `SKILL.md`"; open question 6 on `uv run` permission. | MET | Open question 1 "Worker permissions (UNVERIFIED, blocks the experiment) ... A one-worker smoke run of `status` settles it before any replicate"; 3 "needs a `SKILL.md` for `install_skills.py`". | MET | 8 install note "install only the new command ... and its complete new skill directory"; "Restart/discover the newly installed name before starting measured runs". |
| 4. Defines success or completion criteria | MET | 9 "What would mean the idea failed" (five conditions) and the bar row "3 or fewer in both". | MET | 9 "Only F1 to F4 absent together and both replicates at 3 or fewer count as success." | MET | 14 "Acceptance criteria" (15 items), "Implementation acceptance is separate from experimental success." |
| 5. Specifies out-of-scope items | MET | 1 "Causes this proposal leaves in place"; 8.8 "Not changed, and why". | MET | 1 "What stays unfixed (said up front)"; 5.5 "Not claimed"; Stage C "Not specified here" (8). | MET | 1 "Non-goals. No automatic repair, new reviewer ensemble, generic workflow engine ...". |
| **Subtotal** | **5/5** | | **5/5** | | **5/5** | |

### Correctness (5 criteria)

Repository errors from the `diff-analysis.md` Fact check and Contradictions: X-012 (`tests/recommend/test_routing_refresh.py` line 648 needs `spec-panel-diffgate` in `_POST_REFRESH_ADDITIONS`; B omits the edit, C forbids it), X-015 (A copies `src/superclaude/commands/spec-panel.md:220`, which reads `src/superclaude/examples/release-spec-template.md`, into an installed primitive), X-016 (B does the same), X-017 (C adds a `## Unattended mode` section but forbids the `tests/skills/test_worker_contract.py` edit that line 837 requires). Predictions withdrawn in Round 2: A withdrew "about 60% that both replicates meet the proxy bar" and its N5/F22 story (`round2-A.md`, B-5: "A's 60% and its 'N5 would never have existed' story do not generalise"); C withdrew "1 and 2, mean 1.5" (`round2-C.md`: "This is enough to withdraw C's 1 and 2 forecast"); B's forecast stood with a small revision (0.25 to 0.2, `round2-B.md`).

| Criterion | Variant A | Evidence | Variant B | Evidence | Variant C | Evidence |
|-----------|-----------|----------|-----------|----------|-----------|----------|
| 1. No factual errors or hallucinated claims | NOT MET | X-015: 8.1 "A byte copy of `src/superclaude/commands/spec-panel.md` with these changes only" ships line 220's `src/superclaude/examples/...` read into an installed primitive. Also overstated: 8.6 "must equal P1 plus P2 with exactly 31 entries (line 1564)" (Fact check: line 1564 only checks 31 entries). | NOT MET | X-012: 8.3 lists existing tests that "must keep passing without edit" and omits `test_routing_refresh.py`, which fails. X-016: 8.1 "Every other line is byte-identical". Fact check: "Title line 11" (it is line 10); plugin copy "drifts ... by one word at line 219" (it lacks more). | NOT MET | X-012 and X-017: 8 "Do not edit ... worker contract, severity rule, routing table or installer", while both tests fail on the new file. Fact check: "unrelated one-word drift" of the plugin copy is understated. |
| 2. Technical approaches feasible with stated constraints | NOT MET | INV-001: 4.3 step 4 "the coordinator re-dispatches the reviewer", but 3.3 `open` accepts only "no ledger" or state `reviewed`, and the ledger stays `reviewing`, so the re-dispatch exits 2; the specified recovery path cannot run. | NOT MET | INV-005: rule C10 "A `PRIOR ... resolved` whose anchor line no fix hunk touched ... is set to `open`" makes an FR-8/FR-9 gap finding that is fixed by inserting text elsewhere unresolvable, forcing FAIL at the cap although 427 grading keeps FR-8/FR-9 blocking. | MET | Each mechanism has a defined, executable path including its costly cases: "Adjacent legitimate fixes may fail the map and force manual replanning; do not silently assign multiple owners" (10); deletion fixes use "a current insertion boundary" (3); stdlib only (8 "Script outline"). |
| 3. Terminology consistent and accurate | MET | One vocabulary throughout: `hunk`, `surface`, `ledger`, `DG`/`DG-STATUS`, `deferred: pre-existing` and `deferred: unanchored` (3.3, 4.1, 4.3, 6) with step ids `R1.a`/`F1.a` distinct from rule ids `C1`/`V1`. | NOT MET | The label F1 names two different things: 5.2 "F1. Every fix hunk is claimed by exactly one id" (fix-map rule) and 9 "F1, wrong lever" (failure condition); `round` and `review` alternate for the same counter (2 "Open review 2", ledger "rounds"). | NOT MET | "Proxy" has three meanings: 9 table "Open CRITICAL+MAJOR proxy at R3", 9 "the independent recorder retains the original severity proxy counting rule", and "excluded from the scoped blocker metric" (X-008). |
| 4. No internal contradictions (cross-checked with IC) | NOT MET | IC found 2: X-015 and the deferred-list order (section 2 "End" row "appends its output to the report" versus bullet 9 "above the verdict line"). | NOT MET | IC found 2: X-016 and X-018 ("the gate would have allowed 13" versus 14 under its own F1). | NOT MET | IC found 2: X-017 and the X-008 intra part. |
| 5. Claims supported by evidence or rationale | NOT MET | The section 9 forecast ("1 to 3", "about 60% that both replicates meet the proxy bar") rested on the flg-r2 N5/F22 story, which A withdrew in Round 2 against `debate/evidence-flg-r1.md` (4 blockers from 4 blocking fixes). | MET | 9 prediction "3.5 mean (replicates about 5 and 2)" and "about 0.25" with a reasoning column built on a replay of recorded data (1, "Retrofit evidence ... 5 to 2, blocking 1 to 1"), flagged "flg-r1 composition is UNVERIFIED"; Round 2 kept it (0.2) after flg-r1 was read. | NOT MET | 9 "1 and 2, mean 1.5", withdrawn in Round 2; the spread-check arithmetic "Forecast reduction 4.5 exceeds the historical control spread 4" depends on that withdrawn forecast. |
| **Subtotal** | **1/5** | | **1/5** | | **1/5** | |

### Structure (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence | Variant C | Evidence |
|-----------|-----------|----------|-----------|----------|-----------|----------|
| 1. Logical section ordering | MET | Summary (0), problem (1), mechanism (2), script (3), checker (4), convergence (5), deferred (6), comparison (7), changes (8), measurement (9), risks (10), adopters (11), questions (12). | MET | Problem (1), loop (2), script (3), checker (4), convergence (5), deferred (6), comparison (7), changes (8), measurement (9), risks (10), adopters (11), questions (12). | MET | Same order 1 to 12, then "13. Test plan" and "14. Acceptance criteria" after the changes they test. |
| 2. Consistent hierarchy depth | MET | Numbered H3 subsections under 3, 4 and 8 only (3.1 to 3.6, 4.1 to 4.4, 8.1 to 8.9); no orphan or skipped level. | NOT MET | Section 5 numbers its subsections as bold text ("**5.1 Reviewed once, by construction**" to "**5.5 Not claimed.**") while section 8 uses H3 headings ("### 8.1 New: ..."); same depth, two mechanisms. | MET | Unnumbered H3 subsections used the same way under 3, 8, 10 and 13 ("### Surface definition", "### P0: eligibility and checker unit cases"). |
| 3. Clear separation of concerns | NOT MET | Tests sit inside "Exact changes" (8.4 to 8.6) and there are no implementation acceptance criteria apart from the S1 plan (`diff-analysis.md` S-002, S-003). | NOT MET | Tests are one table row in 8.3; "None separate; staged transformation path (Stage A, B, C) instead" (S-003). | MET | 13 "Test plan" and 14 "Acceptance criteria", with "Implementation acceptance is separate from experimental success." Debate S-001 to S-003: C at 95%. |
| 4. Navigation aids present | MET | 20 internal section cross-references, e.g. "(section 4)", "(3.5)", "section 9 measures it". | MET | 27 internal cross-references, e.g. "(section 5)", "Section 9 states which result would say so", "(section 10, R9)". | MET | Cross-references present: "with its semantic risk recorded in section 10", "tests in section 13", "from sections 2-6". Fewer than A and B, but the criterion asks for presence. |
| 5. Follows conventions of the artifact type | MET | Has every part the seed brief's "Done?" line asks for: script outline (8.3), checker (4), measurement plan with predicted numbers (9), falsification condition (9). | MET | Script outline (8.2), checker (4), predictions table (9), "What result would mean the idea failed" (9). | MET | "Script outline" (8), checker (4), forecast table (9), "Failure and validity rules fixed before running" (9). |
| **Subtotal** | **4/5** | | **3/5** | | **5/5** | |

### Clarity (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence | Variant C | Evidence |
|-----------|-----------|----------|-----------|----------|-----------|----------|
| 1. Unambiguous language | MET | Vague-indicator scan found only "some" in "relabels some MAJOR findings" (line 23), a quantity, not a hedge. | MET | Only "some" in "relabels some MAJOR findings" (line 15), a quantity. | NOT MET | 13 P0 oracle "Exit 3 or stale-state exit 4 as appropriate" (line 287) leaves the expected exit code to judgement, the phrase the criterion names. |
| 2. Concrete rather than abstract | MET | Nine verbatim command bullets (8.1), typed function signatures (8.3), exit-code table (3.3); 199 of 230 substantive lines concrete. | MET | Python skeleton with constants (8.2), surface file example (3), report block example (4); 203 of 231 lines concrete. | NOT MET | The parts an implementer acts on are summaries: "the seven bullet adaptations are described in summary form only" (S-004, e.g. "Grading retains 427 literals, with coordinator confirmation and script-derived blocking"); "Script outline" is prose ("Dispatch the five subcommands to small operations", S-005); 132 of 196 lines concrete. |
| 3. Each section has a clear purpose | MET | Section 0 summary; each section title states its question ("Who computes the diff", "The checker: proving the reviewer stayed inside the surface"). | MET | Opening lens line; sections start with a bold decision ("**Decision: a Python stdlib script ...**", "**Model ...: the reviewer proposes, the script derives.**"). | MET | 1 opens with "**Decision.**"; 5 opens "**Use a one-round delta lease plus checked edit ownership.**"; 14 opens with its purpose sentence. |
| 4. Acronyms and domain terms defined on first use | NOT MET | No evidence found that S1, flg-r2, Arm B or FR-8/FR-9 are defined; searched 0, 1, 9. First use "Measured on S1 (`AB-REPORT.md` ...)" names no scenario. | NOT MET | S1 is first used in 1 "What was measured (S1, 2 replicates per arm" and only described in 9; flg-r1/flg-r2 and FR-8 are never defined. | NOT MET | S1, R3 proxy and FR-8/FR-9 are never defined; searched 1, 9, 13. |
| 5. Actionable next steps or decision points identified | MET | 12 question 9 "The owner should confirm this counting before any run"; 8.9 exact install commands. | MET | 12 question 1 "blocks the experiment ... A one-worker smoke run of `status` settles it before any replicate"; Stage A/B/C (8). | MET | 12 "Defaults above govern the first experiment" with a default per question; 14 checkable criteria. |
| **Subtotal** | **4/5** | | **4/5** | | **2/5** | |

### Risk Coverage (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence | Variant C | Evidence |
|-----------|-----------|----------|-----------|----------|-----------|----------|
| 1. At least 3 risks with probability and impact | NOT MET | Risk table (10) has "How it happens, Mitigation, Residual"; no probability for any risk. Searched 9, 10. | NOT MET | R1 to R12 (10) give limits and residuals; no probability per risk. Searched 9, 10. | NOT MET | "Failure modes and mitigations" (10) has "Guard and remaining cost"; no probability. Searched 9, 10. |
| 2. Mitigation for each identified risk | NOT MET | 10 risk table, "Renumbering noise" row: Mitigation "None in v1". | MET | Every R1 to R12 has a "Limit" or "Limits" clause, e.g. R11 "The loop is sequential in S1". | MET | Every row of the risk table (10) has a guard, e.g. "Deferred flooding ... Exact deduplication and single final disclosure". |
| 3. Failure modes and recovery procedures | MET | 3.3 exit table "Who acts" (exit 3 "reviewer corrects once, then `close --demote`"); 4.3 "On reject". | MET | 3 exit table "Who acts"; 4 "What happens on a reject (one answer, three tiers)". | MET | 4 "One report repair, not another review"; 3 "resume verifies every referenced digest and either completes the identical pending operation or stops". |
| 4. External dependencies and their failure | MET | 10 "Fail-closed stalls: A script error or a permission prompt for `uv run` stops a worker ... UNVERIFIED". | MET | R7 "A bug, a missing `uv`, a worker permission mode that blocks `uv run` ... or a missing skill install stops the loop." | MET | 8 "failure to resolve it is a setup failure, never permission to use the old command"; 12 question 7 "Actual plugin runtime discovery is UNVERIFIED". |
| 5. Monitoring or validation for risk detection | MET | 9 "Blindness audit (out of loop, not counted in the bar)" and "Secondary metrics". | MET | 9 "Blind audit", "Extra recordings", R4 "`coverage:` ... above 50%". | MET | 9 "Keep raw drafts and rejected claims", transcript check (8), spread check (9). |
| **Subtotal** | **3/5** | | **4/5** | | **4/5** | |

### Invariant and Edge Case Coverage (5 criteria)

| Criterion | Variant A | Evidence | Variant B | Evidence | Variant C | Evidence |
|-----------|-----------|----------|-----------|----------|-----------|----------|
| 1. Boundary conditions for collections (empty, single, maximum) | NOT MET | Empty surface (C8, test 13) and one-word hunk (test 2) are covered, but an empty finding set cannot pass: 4.3 "A missing or empty section can never become PASS" (INV-007), and no maximum size is stated (10 lists only "Disk: three snapshots"). | MET | Empty: "`FINDINGS none` accepted" (8.3), empty surface keeps priors open (bullet 5). Large: "a 320-line input keeps the diff exact (the `autojunk=False` regression)" (8.3). | MET | Empty: "No findings: R1 `findings:[]` ... Accepted PASS". Maximum: "at most 2 MiB per document, 100,000 physical lines and 1,000 finding/status entries" (10). |
| 2. State variable interactions across components | MET | 3.4 ledger states `reviewing`/`reviewed`/`passed`/`capped`; 4.4 replay on `open`; snapshot re-hash. | MET | Ledger `state` (`open`, `checked`, `fixed`, `closed`); "Anyone edits `<spec>` after `fixcheck`: the doc sha differs, `begin` exits 5" (2). | MET | "Use a short exclusive-create lock during each operation, compare ledger generation" (3). |
| 3. Guard condition gaps | MET | C1 to C13 (4.2); "UTF-8 strict, else EXIT_STATE" (8.3). | MET | Hard rules C1 to C9 with error codes (4); "exit 6 on parse error" (8.2). | MET | "Reject duplicate JSON keys and unknown control fields" (3); symlink refusal (10). |
| 4. Count divergence (off-by-one, inclusive or exclusive ranges) | NOT MET | 3.4 `"new_lines": [a, b]` gives no base or inclusivity (INV-018); no test pins a range boundary. Searched 3.4, 3.5, 8.4. | MET | C4 "`at` lies inside the snapshot (1..number of lines)"; test "two edits 2 lines apart merge, 3 apart do not" (8.3). | MET | "Eligibility numbering remains physical and one-based" (13); "Proxy reduction must exceed the larger within-arm spread, not merely equal it" (9). |
| 5. Interaction effects when features combine | MET | 10 "False PASS from demotion" (demotion with one-look closure); "Id gaming by the reviser" (gate with inline ids). | MET | `via` with its cap and deferral (C11); degrade with verdict ("a lazy report can add an `open` prior ... but can never smuggle in an unanchored blocker", 4). | MET | "Two adjacent fixes that merge into one actual edit-group and name two owners fail" (13); whitespace mask with fix-map ownership (3). |
| **Subtotal** | **3/5** | | **5/5** | | **5/5** | |

### Qualitative Summary

| Dimension | Variant A | Variant B | Variant C |
|-----------|-----------|-----------|-----------|
| Completeness | 5/5 | 5/5 | 5/5 |
| Correctness | 1/5 | 1/5 | 1/5 |
| Structure | 4/5 | 3/5 | 5/5 |
| Clarity | 4/5 | 4/5 | 2/5 |
| Risk Coverage | 3/5 | 4/5 | 4/5 |
| Invariant and Edge Case Coverage | 3/5 | 5/5 | 5/5 |
| **qual_score** | **20/30 = 0.667** | **22/30 = 0.733** | **22/30 = 0.733** |

All three score 1/5 on Correctness: each carries at least one verified repository error and two internal contradictions. The differences between variants come from Structure (C's separate test and acceptance sections), Clarity (C's summary-only command text and one "as appropriate"), and the edge-case dimension (A's empty-finding gap and unstated range bases).

## Position-Bias Mitigation

Pass 1 read the variants in order A, B, C; Pass 2 in order C, B, A. Both passes applied the same 30 criteria to the same evidence. Totals: Pass 1 A 22, B 23, C 20; Pass 2 A 20, B 22, C 23. Each pass scored the variant read first higher on borderline criteria, which is the bias this step exists to remove. 84 of 90 criterion-variant pairs agreed; the 6 disagreements were re-evaluated by putting both passes' evidence side by side against the literal criterion text.

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|-----------|---------|--------|--------|-----------|-------|
| Invariant 1 (collection boundaries) | A | MET | NOT MET | DISAGREE | NOT MET: Pass 1 credited the empty-surface rule; Pass 2, after C's explicit limits, noticed that an empty finding set can never PASS (4.3, INV-007) and no maximum is stated. Two of three named boundaries are missing or wrong. |
| Risk 2 (mitigation for each risk) | A | MET | NOT MET | DISAGREE | NOT MET: the "Renumbering noise" row literally says "None in v1"; "each" is not satisfied. |
| Correctness 3 (terminology) | B | MET | NOT MET | DISAGREE | NOT MET: F1 names both a fix-map rule (5.2) and a failure condition (9) in the same document. |
| Structure 4 (navigation aids) | C | NOT MET | MET | DISAGREE | MET: Pass 1 compared C's 4 cross-references with A's 20 and B's 27; the criterion asks only whether aids are present, and they are. |
| Correctness 2 (feasibility) | C | NOT MET | MET | DISAGREE | MET: Pass 1 read the single-owner rule as a stall; C specifies the behaviour ("Adjacent legitimate fixes may fail the map and force manual replanning"), so the path is executable at a stated cost. |
| Clarity 2 (concrete) | C | NOT MET | MET | DISAGREE | NOT MET (Pass 1 kept): Pass 2 was swayed by C's concrete test fixtures, but the criterion concerns the instructions an implementer acts on, and C's command bullets and script outline are summaries (S-004, S-005). |

Disagreements re-evaluated: 6
Final verdicts changed from Pass 1: 5 (one re-evaluation kept the Pass 1 verdict)

Limitation: both passes were run by the same evaluator in one session, so order effects are reduced, not eliminated.

## Edge Case Floor Check

| Variant | Invariant and Edge Case Coverage | Floor (at least 1/5) | Eligible as base |
|---|---|---|---|
| A | 3/5 | met | yes |
| B | 5/5 | met | yes |
| C | 5/5 | met | yes |

No variant is excluded by the floor.

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate Tiebreaker |
|---------|---------------|--------------|-----------------|-------------------|
| A (opus:architect) | 0.4932 | 0.3333 | **0.8265** | not applied (not one of the top two) |
| B (sonnet:refactorer) | 0.4860 | 0.3667 | **0.8527** | 36 diff points won (7 sole) |
| C (haiku:qa) | 0.4982 | 0.3667 | **0.8648** | 23 diff points won (6 sole) |

**Margin**: top two are C (0.8648) and B (0.8527); difference 0.0121 (1.2 points), below the 0.05 threshold.
**Tiebreaker applied**: Yes, step 1 of the protocol (debate performance). From the Scoring Matrix of `debate-transcript.md`, counting every diff point whose winner includes the variant (single wins and merges; ties and the unresolved C-008 excluded): A 40, B 36, C 23. Counting single-variant wins only: A 7 (C-002, C-009, C-019, C-020, C-033, X-012, X-017), B 7 (C-013, C-014, C-023, C-029, X-005, X-007, X-010), C 6 (C-027, S-001, S-002, S-003, X-015, X-016). Between the top two, B wins under both counts (36 to 23, 7 to 6), so B is selected. Step 2 (correctness count) is not reached; it would also tie at 1/5.

**Sensitivity, stated plainly.** (1) A is 0.0383 below C, also within 0.05 of the top score. The protocol applies the tiebreaker to the top two only, so A is not considered; under a three-way reading A would win on debate points (40). (2) One criterion flipped for C (for example Clarity 2) would put C 0.0288 ahead of B, still inside the tie band, so B would still be selected. The selection is a tiebreak outcome, not a clear score win, and Step 4 therefore imports a large share of A's and C's material.

## Selected Base: Variant B (sonnet:refactorer)

### Selection Rationale

C has the highest combined score (0.8648) and B is second (0.8527); the 0.0121 gap is inside the 0.05 tie band, and the protocol's first tiebreaker, debate performance, selects B (36 diff points won against C's 23; 7 single wins against 6). Evidence that B is a workable base beyond the tiebreak:

- B holds the positions the debate converged on for the experiment's core question: its forecast and failure test won outright (C-023 and X-007, B at 95%; Round 2 consensus "no mechanism inside the diffgate theme lowers the count of blocking-fix-induced blockers", forecast mean about 3.0 to 3.5), and its F1 "wrong lever" is the primary diagnostic in C-025 (A+B+C, 95%).
- B holds the winning reviser-side design: explicit fix map with `declined` (C-014, B at 95%), quote-checked `via=` (C-013 and X-005, B at 75%), removal of the 427 flags from Usage (C-029 and X-010, B at 95%), and `--expect-round` (kept in C-028).
- B scores 5/5 on edge cases (explicit `FINDINGS none`, one-based `at` range, a tested merge-gap boundary), which A misses on two criteria.
- B's Round 2 statement already concedes most of what it must import (`round2-B.md`: reviewer writes no verdict, `OUTCOME_MIN` and `FIX_BUDGET_BYTES` removed, token-level eligibility, `test_routing_refresh.py` edit, line-220 removal), so the merge has little to argue with in B's own text.

What B lacks is large and is the job of Step 4: A's grammar, naming, id scheme, test integration and audit, and C's test plan, acceptance criteria, cost envelope and portability fix. B is the least structured of the three (Structure 3/5) and carries two verified repository errors (X-012, X-016); both are fixed by planned changes.

### Strengths to Preserve from Base

1. Explicit reviser fix map `fixmap-r<N>.txt` with `H<i> R<N>.<j>` and `declined R<N>.<j> <reason>` lines and rules F1 to F3 (B 5.2).
2. `via=H<i> via_quote=[[...]]` for an unchanged line broken by a changed hunk, quote-checked and capped (B rules C7, C11; 6).
3. `--expect-round N` on `begin` to catch a wrong or fresh state directory (B 2, R9).
4. Fix chains recorded and printed (`R1.5 -> R2.1 -> R3.2`) as a report line, not a stop rule (B 5.3).
5. Primary metric `R3-proxy-all` counting deferred findings by their label, plus the validity gate and extra recordings (B 9).
6. Honest statement of what stays unfixed and what is not claimed (B 1, 5.5), and the retrofit replay on recorded data (B 1).
7. Staged, independently revertible delivery: Stage A inert, Stage B experiment arm, Stage C fold only after the result (B 8).
8. The `FINDINGS none` sentinel and rule C2b (every `R<N>.<j>` token in the prose must be a `FINDING` line) (B 4).
9. Usage line rewritten to `[--diffgate-dir <dir> [--expect-round N]]`, dropping 427's flags (B 8.1 item 2).
10. `autojunk=False` with its reason (B 3, diff step 2) and the reflow filter with `ignored` and `coverage:` counts (B 3, R4).

### Strengths to Incorporate from Non-Base Variants

1. From A: token-level eligibility inside changed lines (A 3.5 steps 3-4; C-008 common core, C-022).
2. From A: skill named `sc-diffgate`, called by path, with the installer analysis (A 3.2; C-002).
3. From A: JSON-string quoted values in the finding lines instead of `[[...]]` (A 4.1; C-006).
4. From A: hunk ids `H<k>.<n>` that never repeat across reviews (A 3.5 step 5; C-009).
5. From A: MAJOR blocking on outcome presence, no length constant (A 4.1; C-019); `resolved by=<hunk>` and pinned severity on carried lines (A C8, V4; C-020).
6. From A: the reviewer writes no verdict; the script prints `verdict_line` (A 4.1, bullet 3; C-018, X-006).
7. From A: ledger replay on `begin` (A 4.4; C-035) and the `PROFILES` seam with `CAP_REVIEWS` as a constant (A 3.6; C-034).
8. From A: both existing-test edits, `_POST_REFRESH_ADDITIONS` and `UNATTENDED_VARIANTS` (A 8.6; X-012, X-017, C-030).
9. From A: mandatory blindness audit classified by ledger history (A 9; C-033); hash of the untouched `spec-panel.md` and "never `--force`" (A 8.9; C-028).
10. From A: verbatim single-line bullets and the 427-bullet-keyed residual-risk table (A 8.1, 7; S-004, S-008).
11. From C: removal of the copied `src/superclaude/examples/release-spec-template.md` read in `## Tool Coordination` (C 8; X-015, X-016, U-016).
12. From C: separate Test plan (tiered P0/P1) and Acceptance criteria sections (C 13, 14; S-001 to S-003).
13. From C: full cost envelope including Read-backs, correction turns and failed attempts (C 10 "Cost envelope"; C-027, S-009).
14. From C: one JSON object on stdout with separate verdict and execution-success fields; a valid FAIL exits 0 (C 3; C-004, C-005).
15. From C: validate every claimed anchor (C 4 step 4; C-010); scoped-PASS sentence (C 6; C-017); exclusive-create lock, size limits and symlink refusal (C 3, 10; C-035).
16. From C: spread check (C 9; C-025), transcript check of the variant call and isolated-HOME install test (C 8, 13 P1; C-028, C-030), a default for every open question (C 12; S-010), PROPOSED labels (C 8; S-007), later-adopter limits (C 11; C-034).
