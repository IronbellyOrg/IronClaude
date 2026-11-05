# Base Selection Report

Decision D2 (`/sc:implement` Ruling halt inside an Orca worker). Scored objects: the three original position papers, V1 = `variant-1-original.md` (option a), V2 = `variant-2-original.md` (option b), V3 = `variant-3-original.md` (option c). Citation key: `V<n> L<k>` = line k of that variant; `DA` = `diff-analysis.md`; `SC-n` = DA citation spot-check row n; `P1`, `P2` = `scoring/qual-pass-1.md`, `scoring/qual-pass-2.md`; `SPEC:N`, `QA:N`, `LEDGER:N`, `RETRY:N`, `SKILL:N` as in `DA`.

## Quantitative Scoring (50% weight)

| Metric | Weight | V1 (option a) | V2 (option b) | V3 (option c) |
|--------|--------|---------------|---------------|---------------|
| requirement_coverage (RC) | 0.30 | 0.8750 (14/16 topics; misses C-009, C-010) | 0.8750 (14/16; misses C-010, C-011) | 0.9375 (15/16; misses C-011) |
| internal_consistency (IC) | 0.25 | 1.0000 (0 contradictions / 9 claims) | 0.8889 (1 / 9: X-004) | 1.0000 (0 / 10) |
| specificity_ratio (SR) | 0.15 | 1.0000 (32 concrete / 0 vague) | 1.0000 (29 / 0) | 1.0000 (35 / 0) |
| dependency_completeness (DC) | 0.15 | 1.0000 (17/17 references resolve) | 1.0000 (15/15) | 1.0000 (18/18) |
| section_coverage (SC) | 0.15 | 0.8000 (4/5 H2 sections) | 1.0000 (5/5) | 1.0000 (5/5) |
| **quant_score** | | **0.9325** | **0.9347** | **0.9813** |

Computation (deterministic; the counts were taken with `grep` over the variant files in this run):

- **RC.** The source (spec D2, lines 333-337) has no requirement IDs (no `FR-`, `NFR-` or `R-` patterns), so the protocol's edge case applies: section-level topic matching. Topics (16): the four decision requirements (safety/provenance, reliability, day-to-day use, implementation cost) plus the twelve content topics C-001..C-012 in `DA`. Matching rule: a requirement topic is covered when the variant has its H2 section; a C-NNN topic is covered unless the variant's cell in the `DA` Content Differences table begins with "Silent", "n/a" or "Not addressed". The rule reads only the `DA` artifact, so a rerun gives the same counts.

  | Topic | V1 | V2 | V3 |
  |-------|----|----|----|
  | Safety / provenance | yes (`## Safety`, L9) | yes (L12) | yes (L12) |
  | Reliability | yes (L13) | yes (L16) | yes (L16) |
  | Day-to-day use | yes (L17) | yes (L19) | yes (L19) |
  | Implementation cost | yes (L21) | yes (L22) | yes (L23) |
  | C-001 provenance of the Ruling | yes | yes | yes |
  | C-002 who writes the line | yes | yes | yes |
  | C-003 scoped explanation | yes | yes | yes |
  | C-004 plan continuity | yes | yes | yes |
  | C-005 resume mechanics | yes ("Not described beyond…" but cites `LEDGER:149-156`) | yes (addressed, wrongly) | yes |
  | C-006 human wait time | yes | yes | yes |
  | C-007 protocol change cost | yes | yes | yes |
  | C-008 testability | yes | yes | yes |
  | C-009 single writer | **no** ("Not addressed") | yes | yes |
  | C-010 malformed input | **no** ("n/a") | **no** ("n/a") | yes |
  | C-011 frequency | yes | **no** ("Silent") | **no** ("Silent") |
  | C-012 reversibility | yes | yes | yes |
  | **Covered** | **14/16** | **14/16** | **15/16** |

- **IC.** Scorable claims = each bullet plus each prose claim paragraph (Position line; V1's citation-drift note), excluding headings and the citation-key line: V1 7 bullets + 2 = 9; V2 8 + 1 = 9; V3 9 + 1 = 10. Contradictions reuse Step 1 detection: the only variant-internal contradiction in `DA` is X-004 in V2 (L9 "The person still decides" against L13 "provenance rests on trusting the coordinator … the worker cannot detect"). X-001..X-003 are cross-variant.
- **SR.** Concrete = code spans (citations, commands, codes, file paths) plus bare numbers outside code spans, citation-key line excluded: V1 27 + 5 = 32, V2 22 + 7 = 29, V3 28 + 7 = 35. Vague = case-insensitive matches of the protocol's list (appropriate, as needed, properly, adequate, should consider, might, various, etc., best practices, industry standard): 0 in every variant.
- **DC.** Internal references = each use of a citation prefix (`SPEC:`, `QA:`, `LEDGER:`, `RETRY:`, `CAPS:`), resolved when the prefix is defined in the variant's own citation key (L5). V1: QA 9, SPEC 7, LEDGER 1 (key defines SPEC, QA, LEDGER, RETRY). V2: SPEC 7, QA 4, CAPS 4 (key: SPEC, QA, CAPS). V3: LEDGER 7, QA 6, SPEC 4, RETRY 1 (key: SPEC, QA, LEDGER, RETRY). Spec item names (WC-3, AC-4.1, non-goal 6) and full source paths are references to other documents and are excluded. No section cross-references exist. All resolve.
- **SC.** H2 count: V1 4, V2 5, V3 5; max 5.
- quant_score = 0.30·RC + 0.25·IC + 0.15·SR + 0.15·DC + 0.15·SC: V1 0.2625 + 0.2500 + 0.1500 + 0.1500 + 0.1200 = 0.9325; V2 0.2625 + 0.2222 + 0.1500 + 0.1500 + 0.1500 = 0.9347; V3 0.28125 + 0.2500 + 0.1500 + 0.1500 + 0.1500 = 0.98125.

## Qualitative Scoring (50% weight) — Additive Binary Rubric

Final verdicts after position-bias mitigation. Each cell is CLAIM (the criterion, met or not for that variant) → EVIDENCE → VERDICT. Where both passes agreed, the evidence is theirs (`P1`, `P2`); the four re-evaluated cells are marked **[re-eval]** and argued in "Position-Bias Mitigation". A concession made in the debate counts against the conceding variant.

### Completeness (5 criteria)

| Criterion | V1 | V1 evidence | V2 | V2 evidence | V3 | V3 evidence |
|-----------|----|-------------|----|-------------|----|-------------|
| 1. Covers all explicit requirements (safety, reliability, day-to-day, cost) | MET | `## Safety` L9, `## Reliability` L13, day to day L17, cost L21 (P1, P2) | MET | L12, L16, L19, L22 (P1, P2) | MET | L12, L16, L19, L23 (P1, P2) |
| 2. Addresses edge cases / failures | NOT MET | No edge case for its own route; row-H review and single writer omitted (`DA` C-005, C-009), conceded in R1-V1 concession 3 (P1, P2) | MET | Undetectable paraphrase (L13); late answer needs a new Task (L17) (P1, P2) | MET | No-lock writer (L14), malformed line (L21), coordinator-written line (L13) (P1, P2) |
| 3. Dependencies / prerequisites | MET | "the halt, the ledger and resume already exist (`LEDGER:149-156`; `implement.md:57`)" L14; WC-3 and implement row L22 (P1, P2) | MET | Orca `ask` durability `CAPS:60-61` (L9); required edits listed L23 (P1, P2) | MET | "Why this works with no protocol change" L7-L10; WC-6 settlement L14 (P1, P2) |
| 4. Success / completion criteria | MET | "AC-4.1 checks it live (`SPEC:274`)" L14 (P1, P2) | NOT MET | AC-4.1 (b) only as an edit target under cost (L23; `DA` S-006) (P1, P2) | MET | Extended AC-4.1 with expected `complete` and unchanged verdict, L17 (P1, P2) |
| 5. Out-of-scope items | NOT MET | No evidence found; searched L1-L22 for out of scope, non-goal, dispute, remote (P1, P2) | NOT MET | No evidence found; non-goal 6 cited as a cost, not a boundary (P1, P2) | NOT MET | No evidence found; `dispute` (A-011) and remote workers (A-009) not scoped (P1, P2) |
| **Subtotal** | **3/5** | | **3/5** | | **4/5** | |

### Correctness (5 criteria)

| Criterion | V1 | V1 evidence | V2 | V2 evidence | V3 | V3 evidence |
|-----------|----|-------------|----|-------------|----|-------------|
| 1. No factual errors | MET **[re-eval]** | SC-1 and SC-5 CONFIRMED; L19's cost is a true cost of route (a) itself (`QA:248` "Yes": the next task runs in the session that recorded the Ruling); see D1 | NOT MET | L8 "keeps … its retry state" against `RETRY:488` ("Any `halt` … is terminal"); L10 OVERSTATED (SC-6); both conceded (P1, P2) | NOT MET | L21 malformed line "is ignored" WRONG (SC-4; `LEDGER:123` gives `E-LEDGER-CORRUPT`); L8 OVERSTATED (SC-2); both conceded (P1, P2) |
| 2. Feasible with stated constraints | MET | Existing mechanics only: `QA:247`, `LEDGER:153-156`, `IMPL:57`; `SPEC:335` (P1, P2) | NOT MET | No resume path as written; WC-3 route does not fit (`SPEC:67`; `DA` C-005, X-003) (P1, P2) | MET | SC-3 CONFIRMED: row R before P/H, `RETRY:498` clause (a) (P1, P2) |
| 3. Consistent terminology | MET | Ruling, halt, ledger, worker, coordinator, `blocked` used one way (P1, P2) | MET | relayed Ruling, `ask`, coordinator used one way (P1, P2) | MET | operator-written / hand-written line name one object (P1, P2) |
| 4. No internal contradictions | MET | `DA` lists no V1-internal conflict (P1, P2) | NOT MET | X-004: L9 against L13; conceded (P1, P2) | MET | `DA` lists no V3-internal conflict (P1, P2) |
| 5. Claims supported by evidence | MET | Every bullet carries a source (L10-L22); SC-1, SC-5 CONFIRMED (P1, P2) | NOT MET | `DA` S-002: no LEDGER or RETRY anchor; L8 uncited (P1, P2) | NOT MET **[re-eval]** | Two load-bearing claims rest on citations that do not support them: L21 on `LEDGER:156` (row H, says nothing of malformed lines), L8 on backward-compatibility wording (`QA:256`, `LEDGER:195`); see D2 |
| **Subtotal** | **5/5** | | **1/5** | | **3/5** | |

### Structure (5 criteria)

| Criterion | V1 | V1 evidence | V2 | V2 evidence | V3 | V3 evidence |
|-----------|----|-------------|----|-------------|----|-------------|
| 1. Logical ordering | MET | Position → key → drift note → Safety → Reliability → day to day → cost (P1, P2) | MET | Position → key → strongest case → Safety → … (P1, P2) | MET | Mechanism section L7 precedes its dependents (P1, P2) |
| 2. Consistent hierarchy | MET | One H1, four H2, flat bullets (P1, P2) | MET | One H1, five H2 (P1, P2) | MET | One H1, five H2 (P1, P2) |
| 3. Separation of concerns | MET | Each section one topic (P1, P2) | NOT MET | Safety split across "Strongest case" (L9) and Safety (L13-L14) with opposite conclusions (`DA` S-004) (P1, P2) | MET | Mechanism, provenance, test, workflow, cost each in its own section (P1, P2) |
| 4. Navigation aids | MET | Citation key L5; WC-3, AC-4.1, implement row (P1, P2) | MET | Key L5; WC-3, non-goal 6, AC-4.1 (b) (P1, P2) | MET | Key L5; WC-3, WC-6, AC-4.1, option (a) (P1, P2) |
| 5. Artifact-type conventions | MET | Position line plus the shared section set (`DA` S-001) (P1, P2) | MET | Same set plus one (P1, P2) | MET | Same set plus one (P1, P2) |
| **Subtotal** | **5/5** | | **4/5** | | **5/5** | |

### Clarity (5 criteria)

| Criterion | V1 | V1 evidence | V2 | V2 evidence | V3 | V3 evidence |
|-----------|----|-------------|----|-------------|----|-------------|
| 1. Unambiguous language | MET | Hedge search: only normative "should make directly" (L11) (P1, P2) | MET | One "may" (L10), describing a spec permission (P1, P2) | MET | Zero hedge hits (P1, P2) |
| 2. Concrete | MET | "sends `worker_done --outcome failed`"; "`/sc:implement <plan>`" (L3) (P1, P2) | MET | `ask` → person → exact words → verbatim record (L3) (P1, P2) | MET | "types one ledger line", "Ruling written", `--resume` (L3, L20) (P1, P2) |
| 3. Clear section purpose | MET | Headings match content (P1, P2) | MET | Headings match content (P1, P2) | MET | Headings match content (P1, P2) |
| 4. Terms defined on first use | NOT MET | Ruling, WC-3, AC-4.1, `E-HALT-QA` undefined (P1, P2) | NOT MET | Ruling, WC-3, non-goal 6 undefined (P1, P2) | NOT MET | Ruling, WC-6, AC-4.1, row R undefined (P1, P2) |
| 5. Actionable next steps | MET | "Zero change to `sc-implement-protocol`"; person's step per halt (L18, L22) (P1, P2) | MET | Edit list L23 (P1, P2) | MET | "one sentence in D2/WC-3 and one AC-4.1 extension" (L24) (P1, P2) |
| **Subtotal** | **4/5** | | **4/5** | | **4/5** | |

### Risk Coverage (5 criteria)

| Criterion | V1 | V1 evidence | V2 | V2 evidence | V3 | V3 evidence |
|-----------|----|-------------|----|-------------|----|-------------|
| 1. ≥3 risks with probability and impact | NOT MET | Risks named (L10, L19, L22) but only one frequency statement (L15), no per-risk impact (P1, P2) | NOT MET | Risks named (L13, L14, L17), no probability (P1, P2) | NOT MET | Risks named (L13, L14, L21), no probability (P1, P2) |
| 2. Mitigation per risk | NOT MET | Context-switch cost (L19) unmitigated (P1, P2) | NOT MET | "two risk bullets, no mitigation" (`DA` S-004) (P1, P2) | MET | Each risk paired: invalid coordinator line (L13), write after settle (L14), (a) available (L20, L24), safe stop (L21) (P1, P2) |
| 3. Failure modes and recovery | MET **[re-eval]** | The halt (`E-HALT-QA`, `E-NO-RULING`) and its recovery: person opens the printed ledger path (`QA:247`) and resumes in own session (L3, L18); the route works per `LEDGER:155-156`; see D3 | MET | Timeout → resume by message ID (L9); late answer → new Task (L17) (P1, P2) | NOT MET | Its stated recovery for a malformed line is wrong (SC-4); no other recovery given (P1, P2) |
| 4. External dependencies and failure | NOT MET | Orca, worktree access (A-009) and halt notification (A-008) not treated (P1, P2) | MET | `ask` timeout `CAPS:60`, heartbeat `CAPS:64`, attribution `CAPS:62` (P1, P2) | NOT MET | Task creation and worktree placement assumed (A-009, INV-018) (P1, P2) |
| 5. Monitoring / validation mechanism | MET | AC-4.1 live check (`SPEC:274`, L14) (P1, P2) | NOT MET | Relay fidelity untestable (`DA` C-008), conceded (P1, P2) | MET | AC-4.1 extension with expected ledger result (L17) (P1, P2) |
| **Subtotal** | **2/5** | | **2/5** | | **2/5** | |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | V1 | V1 evidence | V2 | V2 evidence | V3 | V3 evidence |
|-----------|----|-------------|----|-------------|----|-------------|
| 1. Collection boundaries (empty, single, maximum) | NOT MET | No evidence found (P1, P2) | NOT MET | No evidence found (P1, P2) | NOT MET | Empty / placeholder fields and multiple lines not covered (INV-014, INV-012) (P1, P2) |
| 2. State interactions across component boundaries | NOT MET | Resume given only as "resumes from the ledger"; row-H review and single writer omitted, conceded (P1, P2) | NOT MET | L8 state claim false (`RETRY:488`), conceded (P1, P2) | MET | Row R before P/H, `RETRY:498`, WC-6 settlement (L9, L14); SC-3 CONFIRMED (P1, P2) |
| 3. Guard condition gaps | NOT MET | Cites existing guards (L10) but names no gap (P1, P2) | MET | Missing provenance check: the worker "cannot tell the person's words from the coordinator's" (L13) (P1, P2) | MET | No ledger lock (L14); the spec must forbid coordinator-written lines (L13) (P1, P2) |
| 4. Count divergence | NOT MET | No evidence found (P1, P2) | NOT MET | No evidence found (P1, P2) | NOT MET | One-line / final-newline divergence unaddressed (INV-012) (P1, P2) |
| 5. Interaction effects when components combine | MET **[re-eval]** | L10 combines the Orca coordinator with the `QA:254` gate ("An Orca coordinator is another agent", `SPEC:334`), so a relay cannot carry acceptance; L19 traces the rule combined with Orca plan execution (`QA:248` "Yes"); see D4 | MET | `ask` wait combined with Task settlement: late answer needs a new Task (L17) (P1, P2) | MET | WC-6 new Task combined with implicit `--resume` and row R (L10) (P1, P2) |
| **Subtotal** | **1/5** | | **2/5** | | **3/5** | |

### Qualitative Summary

| Dimension | V1 (option a) | V2 (option b) | V3 (option c) |
|-----------|---------------|---------------|---------------|
| Completeness | 3/5 | 3/5 | 4/5 |
| Correctness | 5/5 | 1/5 | 3/5 |
| Structure | 5/5 | 4/5 | 5/5 |
| Clarity | 4/5 | 4/5 | 4/5 |
| Risk Coverage | 2/5 | 2/5 | 2/5 |
| Invariant & Edge Case Coverage | 1/5 | 2/5 | 3/5 |
| **qual_score** | **20/30 = 0.6667** | **16/30 = 0.5333** | **21/30 = 0.7000** |

For reference, the raw passes before mitigation: P1 V1 18, V2 16, V3 22; P2 V1 19, V2 16, V3 21.

### Edge Case Floor Check

Rule: a variant scoring below 1/5 on Invariant & Edge Case Coverage is ineligible as base; the floor is suspended only when all variants score 0/5.

| Variant | Final I&EC | Eligible as base |
|---------|-----------|------------------|
| V1 (option a) | 1/5 (I5 MET after re-evaluation D4) | Yes |
| V2 (option b) | 2/5 | Yes |
| V3 (option c) | 3/5 | Yes |

Pass 1 had V1 at 0/5 (ineligible) and Pass 2 had it at 1/5. The disagreement was on criterion I5 only; the final verdict (D4) is MET, so V1 meets the floor at exactly 1/5. Not every variant scores 0/5, so the floor is not suspended. Sensitivity: had D4 gone NOT MET, V1 would be ineligible and V3 would be the base.

## Position-Bias Mitigation

Completed on resume (2026-11-02T17:56Z) after the 16:28 UTC interruption. This section and the three below were empty stubs on disk; they are assembled here from the final verdicts already written in the rubric tables above and from the two pass files. No verdict was changed or rescored. Verdicts per pass were read from `scoring/qual-pass-1.md` (columns V1, V2, V3) and `scoring/qual-pass-2.md` (columns V3, V2, V1).

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|-----------|---------|--------|--------|-----------|-------|
| Correctness 1 (no factual errors) | V1 | MET | NOT MET | DISAGREE | MET (D1) |
| Correctness 5 (claims supported by evidence) | V3 | MET | NOT MET | DISAGREE | NOT MET (D2) |
| Risk Coverage 3 (failure modes and recovery) | V1 | NOT MET | MET | DISAGREE | MET (D3) |
| Invariant & Edge Case 5 (interaction effects) | V1 | NOT MET | MET | DISAGREE | MET (D4) |

All other 86 criterion-variant pairs agreed between the passes.

- **D1 (V1 Correctness 1 → MET).** Pass 2 held V1 L19 ("the remaining tasks of that plan leave Orca") as a false claim because V1 conceded X-002. The re-evaluation found L19 is a true cost of route (a) as written: under (a) the person's own session records the Ruling and the Halt table then proceeds to T{i+1} (`QA:248`, "Yes"). V1 conceded that the rule does not force it, not that (a) avoids it. SC-1 and SC-5 are CONFIRMED.
- **D2 (V3 Correctness 5 → NOT MET).** Pass 1 accepted V3's citations as support. The re-evaluation found two load-bearing claims rest on citations that do not support them: L21 ("a malformed line is ignored") cites `LEDGER:156`, which is row H and says nothing about malformed lines (the real outcome is `E-LEDGER-CORRUPT`, `LEDGER:123`); L8's "already valid" footing cites backward-compatibility wording (`QA:256` "Existing operator-written records remain valid", `LEDGER:195`).
- **D3 (V1 Risk Coverage 3 → MET).** Pass 1 found no failure/recovery treatment. The re-evaluation found V1 names the failure (the `E-HALT-QA` / `E-NO-RULING` halt) and its recovery: the person opens the printed ledger path (`QA:247`) and resumes in their own session (V1 L3, L18), which `LEDGER:155-156` supports.
- **D4 (V1 Invariant & Edge Case 5 → MET).** Pass 1 found no interaction effect. The re-evaluation found V1 L10 combines the Orca coordinator with the `QA:254` gate (a coordinator reply is "another agent's message") and L19 traces the rule combined with Orca plan execution (`QA:248`).

Disagreements re-evaluated: 4
Final verdicts changed: 0 relative to both passes (each re-evaluation adopted one pass's verdict: D1 Pass 1, D2 Pass 2, D3 Pass 2, D4 Pass 2). Net effect against the raw passes: V1 18 (P1) / 19 (P2) → 20; V3 22 (P1) / 21 (P2) → 21; V2 16 in both.

## Combined Scoring

| Variant | Quant (×0.50) | Qual (×0.50) | **Final Score** | Debate Tiebreaker |
|---------|---------------|--------------|-----------------|-------------------|
| V1 (option a) | 0.46625 | 0.33333 | **0.79958** | 7 outright wins of 27 = 25.93% (15 incl. shared = 55.56%) |
| V2 (option b) | 0.46735 | 0.26667 | **0.73402** | not needed (third) |
| V3 (option c) | 0.49062 | 0.35000 | **0.84062** | 6 outright wins of 27 = 22.22% (14 incl. shared = 51.85%) |

Arithmetic run with `uv run python` in this resume; the win tallies are the debate's own (`debate-transcript.md`, "Win tally (used by the Step 3 tiebreaker)").

**Margin**: 0.04104 (V3 over V1), below the 0.05 threshold (`|score_A - score_B| < 0.05`, `refs/scoring-protocol.md` A.4).
**Tiebreaker applied**: Yes.
- Level 1, debate performance: V1 won more diff points than V3, 7 to 6 outright (15 to 14 counting shared "equal (…)" wins). Read as a share of the 27 points, the gap is 3.70 percentage points, which is within 5%, so Level 2 is also checked.
- Level 2, correctness count: V1 5/5 against V3 3/5. V1 wins.
- Result: V1 under every reading of Level 1 (raw count, share of points, outright or including shared wins). Level 3 (input order) is not reached; it would also give V1.

Sensitivity: the base depends on D4. Had D4 gone NOT MET, V1 would score 0/5 on Invariant & Edge Case Coverage, fall below the floor, and V3 would be the base (see Edge Case Floor Check).

## Selected Base: Variant 1 (option a, keep the Ruling rule; the person gives the Ruling in their own session)

### Selection Rationale
- **Tiebreaker.** V3 leads on the combined score by 0.041, inside the 0.05 tie band. V1 wins Level 1 (7 to 6 outright debate wins) and Level 2 (Correctness 5/5 against 3/5).
- **Correctness carries the decision.** V1 is the only paper with no wrong or overstated load-bearing claim: SC-1 and SC-5 CONFIRMED (`diff-analysis.md` citation spot-check). V3's malformed-line claim is WRONG (SC-4) and its "no protocol change" footing is OVERSTATED (SC-2); V2's retry-state claim is false (`RETRY:488`) and its paper contradicts itself (X-004).
- **The debate converged on V1's rule with V3's route added.** All three Round 2 recommendations are "(a)+(c)": keep the rule word for word, (a) as the default and the only route for a `dispute`, (c) as the way back into Orca (`debate-transcript.md`, "Advocates' final recommendations"). V2 withdrew (b). Taking (a) as the base and adding (c) matches that consensus; V3's paper already presents (c) as a superset of (a) (S-005).
- **Convergence is BLOCKED_BY_INVARIANTS** (6 HIGH UNADDRESSED: INV-001, INV-004, INV-014, INV-017, INV-018, INV-022). Every one becomes a mandatory change or an explicit accepted-risk entry in `refactor-plan.md`.

### Strengths to Preserve from Base
1. The Ruling rule unchanged and quoted from its current lines: "another agent's message ... not acceptance" (`QA:254`); "executor-invented approval" is a STOP (`QA:249`). Won C-001, C-003, X-001, A-010.
2. (a) as the default route and the only route for a `dispute` halt: the executor's own scoped explanation before acceptance (`QA:254`; C-003, A-011) and row P/H writing the `halt` that makes the Ruling eligible by construction (`LEDGER:155-156`; A-012).
3. Zero protocol change and the frequency argument: halts need a confirmed blocker a repair could not close (`QA:280`), minors never halt (`QA:274`), no other path prompts the user (`QA:288`) (C-007, C-011).
4. The corrected `qa.md` anchors (S-003): the spec's `qa.md:232,238` and `qa.md:231-238` now point at the Family probe section; the rule is at `QA:247-249` and `QA:254-256`.

### Strengths to Incorporate from Non-Base Variants
1. From V3, section "Why this works with no protocol change" (V3 L7-L10) and Position (L3): route (c), a hand-written `T<id>: Ruling:` line consumed by resume row R (`LEDGER:154`) in a new resume Task (WC-6). Won X-002, C-005, S-005.
2. From V3, Reliability (L17): the deterministic AC-4.1 extension (S-006, C-008).
3. From V3, Safety (L13-L14): a coordinator-written line is "executor-invented approval" (`QA:249`); the single-writer precondition (`LEDGER:145`, `SPEC:70`) (C-009).
4. From V3's Round 2 (r2-variant-3 response 9, recommendation item 3) and V1's Round 2 (new evidence 1-2): the coordinator freeze after a Ruling halt (`SPEC:84` against `QA:283`), the read-only pre-dispatch check (format `LEDGER:71`, both clauses of `RETRY:498`), and the `dispute` exclusion.
5. From V2, Round 2 recommendation and new evidence 4: the blocked contract carries the absolute ledger path and worktree (A-009); (b) is recorded only as a possible later opt-in that excludes `reason=dispute`.
6. From V2, Safety (L13-L14): the plain statement of why a relayed Ruling is unsafe (`CAPS:62`, `QA:254`), kept as the rationale for rejecting (b).
