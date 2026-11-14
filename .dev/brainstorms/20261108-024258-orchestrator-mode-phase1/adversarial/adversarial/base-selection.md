# Base Selection Report

- Step: 3 of 5 (hybrid scoring and base selection), Mode B, depth deep. Author: debate orchestrator (neutral; did not write any variant). Date: 2026-11-08.
- **Forced selection.** The base was force-selected by score because the gate was BLOCKED_BY_INVARIANTS (INV-005 accepted risk, no owner sign-off). Diff-point agreement was 1.00 and all taxonomy levels were covered, but one HIGH invariant stays UNADDRESSED, and Round 3 was the last round at `--depth deep` (convergence-tracking.md:282-302; SKILL:1380-1382, FR-006).
- Variants: V1 = `variant-1-opus-architect.md` (opus:architect, 333 lines), V2 = `variant-2-opus-analyzer.md` (opus:analyzer, 313 lines), V3 = `variant-3-haiku-backend.md` (haiku:backend, 431 lines). In the template's lettering, Variant A = V1, B = V2, C = V3. Citations "V1:N" mean line N of that variant.
- Requirement source: `seed-brief.md`, Constraints (Seed:52-59) and Success Criteria (Seed:63-69).
- Other inputs: `debate-transcript.md` (scoring matrix lines 128-229, convergence assessment lines 232-241), `convergence-tracking.md` section "Post-Round-3 Final Convergence" (lines 225-338), `invariant-probe.md` (used only for the Invariant and Edge Case dimension).
- Protocol: `~/.claude/skills/sc-adversarial-protocol/refs/scoring-protocol.md` (A.1 to A.5) and `refs/artifact-templates.md` Section 3.
- **Deviations from the Section 3 template, recorded on purpose.**
  1. The template shows five qualitative dimensions and a /25 denominator. The scoring protocol (A.2, "qual_score = total_criteria_met / 30") and its output item 4 require a sixth dimension, Invariant and Edge Case Coverage, and an Edge Case Floor Check. Both are added here, and the denominator is /30.
  2. The template has two variant columns; this report has three.
  3. The template heading for the qualitative section uses a dash; it is written here with a comma to keep the text free of em dashes.
- Every file was read in chunks of 150 lines or fewer. Read-only `grep` and `wc` were used only for counting and for locating cited lines.

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant A: V1 (opus:architect) | Variant B: V2 (opus:analyzer) | Variant C: V3 (haiku:backend) |
|--------|--------|-------------------|-------------------|-------------------|
| requirement_coverage | 0.30 | 0.944 (17 of 18 seed items; misses S1) | 0.944 (17 of 18; misses S1) | 0.944 (17 of 18; misses C8) |
| internal_consistency | 0.25 | 1.000 (0 contradictions / about 120 claims) | 0.965 (4 / about 115) | 0.987 (2 / about 150) |
| specificity_ratio | 0.15 | 0.900 (36 / 40 sampled) | 0.925 (37 / 40 sampled) | 0.700 (28 / 40 sampled) |
| dependency_completeness | 0.15 | 1.000 (about 40 / 40) | 1.000 (about 35 / 35) | 0.880 (22 / 25) |
| section_coverage | 0.15 | 0.933 (14 / 15 H2) | 1.000 (15 / 15 H2) | 0.933 (14 / 15 H2) |
| **quant_score** | | **0.958** | **0.963** | **0.907** |

Weighted terms: V1 = 0.2833 + 0.2500 + 0.1350 + 0.1500 + 0.1400 = 0.9583. V2 = 0.2833 + 0.2413 + 0.1388 + 0.1500 + 0.1500 = 0.9634. V3 = 0.2833 + 0.2467 + 0.1050 + 0.1320 + 0.1400 = 0.9070.

#### Requirement coverage (RC): the 18 seed items and the per-variant hit lists

The seed has no requirement IDs, so the protocol's edge case applies (topic matching). Seed:52 and Seed:63 each hold two separable requirements, and Seed:64 holds two test groups, so the 15 bullet lines give 18 items.

| ID | Seed | Requirement | V1 | V2 | V3 |
|---|---|---|---|---|---|
| C1 | 52a | Read-only; report is the only write | HIT (FR-021 V1:71) | HIT (NFR-001 V2:97) | HIT (NFR-001 V3:118) |
| C2 | 52b | Every `_git` call carries `--no-optional-locks` | HIT (NFR-002 V1:82, V1:176) | HIT (NFR-002 V2:98) | HIT (V3:57, V3:279) |
| C3 | 53 | Coordinator-only, never a worker | HIT (V1:246) | HIT (V2:263, V2:126) | HIT (V3:338) |
| C4 | 54 | No new store, security model, service; no live Orca, ccsession or Claude launch | HIT (V1:47, all ACs mocked) | HIT (NFR-004 V2:100) | HIT (V3:414); defect noted under Correctness (V3:403) |
| C5 | 55 | Extend the contract; WC-6 and WC-10 hold | HIT (V1:38, V1:240) | HIT (V2:42, V2:228) | HIT (V3:52, V3:336) |
| C6 | 56 | Could not determine is its own class | HIT (FR-008 V1:58) | HIT (FR-009 V2:70) | HIT (V3:230) |
| C7 | 57 | `.dev/tasks/` never disposable | HIT (R7 V1:279: "no deletion advice for `.dev/tasks/`"; FR-013 V1:63) | HIT (V2:168) | HIT (V3:49, V3:429) |
| C8 | 58 | `~/.claude` paths, `make sync-dev`, never stage `.claude/`, UV | HIT (NFR-011 V1:91, NFR-012 V1:92) | HIT (V2:90, V2:104, V2:307; no staging rule stated) | MISS (no hit for `uv`, `UV`, `sync-dev` or `.claude/` in a whole-file grep) |
| C9 | 59 | Mock-testable at the two seams | HIT (V1:47) | HIT (NFR-004 V2:100) | HIT (V3:414) |
| S1 | 63a | Dated report under `.dev/sweeps`; every session and worktree with class, waiting-on and next action; people first | MISS (session row V1:228 has class, rule, safe-to-close, notes; no next action) | MISS (FR-022 V2:86 gives a next check only per waiting item, and only "may") | HIT (V3:303: "class, waiting-on, evidence, next inspection") |
| S2 | 63b | Exit 2 with no `--run` and no binding | HIT (FR-002 V1:52) | HIT (FR-002 V2:57; defective exception, see Correctness) | HIT (V3:166) |
| S3 | 64a | Allowlist argv test minus gate-list, worker-read, stash | HIT (V1:184-200, V1:193) | HIT (V2:170-200) | HIT (V3:267-286) |
| S4 | 64b | `--no-optional-locks` test, snapshot diff, one status per worktree | HIT (NFR-002 V1:82, FR-021 V1:71) | HIT (NFR-001 V2:97, FR-014 V2:75) | HIT (V3:57, V3:96) |
| S5 | 65 | Classifier tests: rules 1-7 plus idle, window, GQ-103(3), 102, 101, 105, 108, 107 | HIT (V1:145-154, section 12 V1:283-302) | HIT (FR-008 V2:69, section 13 V2:267-285) | HIT (V3:416) |
| S6 | 66 | `.dev/sweeps/` in `.gitignore` | HIT (FR-025 V1:75) | HIT (FR-026 V2:93) | HIT (V3:384, "add `.dev/sweeps/` to the project ignore rules"; the file name `.gitignore` is not written) |
| S7 | 67 | WC-14 and never-as-worker pinned; registries and docs | HIT (FR-023 V1:73, FR-024 V1:74) | HIT (FR-024 V2:91, FR-025 V2:92) | HIT (V3:322, V3:338, V3:426) |
| S8 | 68 | verify-sync, lint and tests pass | HIT (NFR-012 V1:92) | HIT (NFR-008 V2:104) | HIT (V3:422: "Affected tests, lint, sync verification") |
| S9 | 69 | Later phases recorded with blockers | HIT (V1:31-43) | HIT (V2:35-48) | HIT (V3:36-52) |
| | | **Hits** | **17 / 18** | **17 / 18** | **17 / 18** |

Partial hits counted as hits, stated so the reader can rescore: V2 on C8 (no "never stage `.claude/`" rule) and on S2 (the exception at V2:57), and V3 on S6 (V3:384 says "project ignore rules", not `.gitignore`). Scoring any one of them as a miss lowers that variant's RC by 0.056 and its quant by 0.017; none of these would change the ranking.

#### Internal consistency (IC)

Claim totals are estimates from sampling (scorable claims counted on three 40-line windows per variant, then scaled to the file). Contradictions were searched for across the whole file.

- V1: 0 contradictions found. The rule 2 decline issue (INV-007, V1:148) is an interaction effect between rules, not two opposing claims, and is scored under the Invariant dimension instead.
- V2: 4 contradictions.
  1. The rule table puts `idle` (V2:156) after rule 7 "anything else" (V2:155), so first-match-wins makes idle unreachable, while FR-008 (V2:69) requires a fixture per rule including idle.
  2. FR-002's exception (V2:57: Orca unavailable gives "a disk-only sweep and exits 0") conflicts with its own Seed:63 requirement it claims to meet (requirement-constraint conflict).
  3. The seam runs `["orca", *args]` (V2:175), while FR-020 (V2:84) handles "a missing `orca-ide` binary".
  4. NFR-006 (V2:102) says the report is byte-identical "apart from the header timestamp", and its AC says the two files are identical.
- V3: 2 contradictions.
  1. Active-local evidence is a comparison with a "fixed base reference" (V3:246, V3:285, V3:366), but the allowlist (V3:256-286) holds only the single status form (V3:279, V3:96) and V3:285 defers the base-reading argv.
  2. V3:403 requires a live disposable-Run check before release, while V3:414 says all Phase 1 behaviour is tested with mocks (and Seed:54 bans live Orca launches in this work).

#### Specificity ratio (SR)

- A whole-file grep for the protocol's vague markers (`appropriate`, `as needed`, `properly`, `adequate`, `should consider`, `might`, `various`, `etc.`, `best practices`, `industry standard`) found 0 hits in each variant. A lexicon-only SR is therefore 1.0 for all three and does not discriminate.
- The metric table in A.1 defines SR as concrete statements over all substantive statements. So 40 substantive statements were sampled per variant (FR, NFR, seam and risk text, headings and metadata excluded) and each was marked concrete if it carried a number, threshold, named entity or measurable criterion. These are estimates from sampling: V1 36 / 40, V2 37 / 40, V3 28 / 40. V3's misses are goal statements such as FR-001 "Protect the live Git index before adding any other probe behavior." (V3:56) and FR-009 (V3:80).
- Supporting proxy (counted, not sampled): lines containing a digit are V1 178 / 333 (53%), V2 169 / 313 (54%), V3 108 / 431 (25%).

#### Dependency completeness (DC)

Internal references are FR, NFR, rule, section, failure and risk IDs and defined terms. References to the REPORT, GAPS log, `WORKER-CONTRACT.md` and seed are external and excluded. Totals for V1 and V2 are estimates from sampling.

- V1: about 40 references; every sampled one resolves (for example "section 7" at V1:47 resolves to V1:171, "FR-019" at V1:256 to V1:69, "NFR-010" to V1:79-93).
- V2: about 35 references; every sampled one resolves (for example "Section 7" at V2:69 to V2:131, "FR-026" at V2:262 to V2:93, "FR-006" at V2:247 to V2:64).
- V3: 25 references counted, 3 unresolved: "fixed base reference" (V3:246, never defined), "unread-report candidates" (V3:93, V3:237, never defined), "verified child-tree membership" (V3:290, no definition of how it is verified).

#### Section coverage (SC)

`grep -c '^## '` gives 14 (V1), 15 (V2) and 14 (V3). Maximum 15.

## Qualitative Scoring (50% weight), Additive Binary Rubric

Each table row is one Claim-Evidence-Verdict (CEV) triple per variant. CLAIM: "<criterion> is met in Variant X". EVIDENCE: the Evidence cell, a quote or file:line, or "No evidence found" with the places searched. VERDICT: the MET or NOT MET column. No partial credit; a MET without citable evidence defaults to NOT MET. Verdicts shown are the final ones after the two position-bias passes (see Position-Bias Mitigation).

### Completeness (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|-----------|----|----------|----|----------|----|----------|
| Covers all explicit requirements | NOT MET | S1 missed: the session row (V1:228) has class, rule, safe-to-close and notes but no next action (RC table) | NOT MET | S1 missed (V2:86 "may print" a next check per waiting item only); S2 carries an exit-0 exception (V2:57) against Seed:63 | NOT MET | C8 missed: no `uv`, `UV`, `sync-dev` or `.claude/` in the file (whole-file grep) |
| Addresses edge cases and failures | MET | Failure table, each mode with a fixture (V1:250-267), for example "Worktree removed mid-sweep" (V1:258) | MET | F1-F9 with evidence and test columns (V2:233-247), for example F9 symlink out of root (V2:247) | MET | Operational failure modes table (V3:343-358); oversized inputs (V3:137) |
| Includes dependencies and prerequisites | MET | GQ-103(1) "first commit and first test" (V1:289); PR #422 sequencing (V1:313) | MET | R5 PR #422 "step 1.16a gate" (V2:259) | MET | "FR-001 is the first build gate" (V3:376); PR #422 overlap check (V3:371) |
| Defines success and completion criteria | MET | "Each acceptance criterion (AC) is checked with the two seams mocked" (V1:47); AC column per FR (V1:49-75) | MET | *AC:* on each FR, for example FR-002 "three tests" (V2:57) | MET | "Acceptance:" lines, for example V3:57, V3:90, V3:134 |
| Specifies out-of-scope items | MET | Section 2 "Out of scope (later phases, recorded with blockers)" (V1:31-43) | MET | Section 3 "Out of Scope (Later Phases and Blockers)" (V2:35-48) | MET | "Out of scope and later-phase blockers" (V3:36-52) |
| **Subtotal** | **4/5** | | **4/5** | | **4/5** | |

### Correctness (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|-----------|----|----------|----|----------|----|----------|
| No factual errors or hallucinated claims | MET | Spot-checked citations hold: WC-9 at `WORKER-CONTRACT.md:44` (V1:180) matches V2's quote of the same line (V2:245); "A grep on 2026-11-08 found no `sweeps` entry" (V1:75) matches V2:93. No error found in the sampled claims | NOT MET | The WC-14 text and F7 state without scope that the sweep does not take `index.lock` (V2:228, V2:245); whether Orca read verbs take git locks is UNVERIFIED (invariant-probe.md:11), and V2R3:27 withdraws these sentences (convergence-tracking.md:275) | MET | Spot-checked: WC-6, WC-9 and WC-10 unchanged (V3:52), verb list (V3:267-271) consistent with the other variants' allowlists, unverified items marked UNVERIFIED (V3:272). No error found |
| Technical approaches feasible with stated constraints | MET | Both seams mocked for every AC (V1:47); seam argv fixed at V1:175-176 | NOT MET | FR-002's Orca-down exit 0 (V2:57) cannot satisfy Seed:63's exit 2 | NOT MET | A live disposable-Run check before release (V3:403) conflicts with Seed:54; active-local detection needs a base-reading argv that is not in the allowlist (V3:246, V3:285) |
| Terminology consistent and accurate | MET | One binary name, `orca-ide` (V1:175, V1:189); rule names used the same in V1:145-154 and V1:260 | NOT MET | `["orca", *args]` (V2:175) versus "a missing `orca-ide` binary" (V2:84) | MET | `orca-ide` throughout (V3:267-271); class names consistent (V3:209, V3:230, V3:235) |
| No internal contradictions (cross-checked with IC) | MET | IC found 0 contradictions | NOT MET | IC found 4, including idle placed after the catch-all (V2:155-156) against FR-008 (V2:69) | NOT MET | IC found 2: base comparison (V3:246) versus a single status form (V3:279, V3:96); live check (V3:403) versus mock-only testing (V3:414) |
| Claims supported by evidence or rationale | MET | "Why lock-free git" with the contract citation (V1:180); grep evidence dated (V1:75) | MET | Failure table has an evidence column (V2:239-247); root-cause notes (V2:22, V2:158, V2:265) | NOT MET | "recommend five minutes" with no rationale (V3:405); "proposed limits of 1 MiB ..., 256 KiB ... and 8 MiB" with no source (V3:137) |
| **Subtotal** | **5/5** | | **1/5** | | **2/5** | |

### Structure (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|-----------|----|----------|----|----------|----|----------|
| Logical section ordering | MET | Problem, scope, FR, NFR, architecture, data model, seams, report, contract, failures, risks, gaps, questions, rollback (V1:14-318) | MET | Same order, with root cause first (V2:11-300) | MET | Problem, scope, FR, NFR, CLI, data model, seams, report, contract, failures, risks, gaps, questions, verification (V3:8-412) |
| Consistent hierarchy depth | MET | 14 numbered H2 sections; no orphaned subsection found | MET | 15 numbered H2 sections; no orphaned subsection found | MET | 14 H2 sections; no orphaned subsection found |
| Clear separation of concerns | MET | Module table (V1:99-108) and boundary rules B1-B5 (V1:112-118) | MET | Component boundaries section (V2:107-129) | NOT MET | The classification section also holds safety values and package-state rules (V3:209, V3:246); verification and rollback share one section (V3:412-431) |
| Navigation aids | MET | Numbered sections with cross-references ("section 7" V1:47, "section 14" V1:296) | MET | Numbered sections with cross-references ("Section 7" V2:69, "Section 4" V2:41) | NOT MET | No section numbers and no section cross-reference; mentions such as "FR-001" (V3:376) name an ID, not a place in the document |
| Follows conventions of the artifact type | MET | FR and NFR tables with AC, rollback table (V1:318-333) | MET | FR and NFR with AC, rollback table (V2:300-313) | MET | Numbered FR and NFR with "Acceptance:" lines (V3:54-146) |
| **Subtotal** | **5/5** | | **5/5** | | **3/5** | |

### Clarity (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|-----------|----|----------|----|----------|----|----------|
| Unambiguous language | MET | 0 vague-lexicon hits (grep); requirements are stated as fixed behaviour, for example "with no binding it exits 2" (V1:52) | NOT MET | FR-022 "may print ... and may name" (V2:86) leaves the output optional | NOT MET | "add a collision suffix if needed" (V3:181); "recommend five minutes" (V3:405) |
| Concrete rather than abstract | MET | Exact argv `git --no-optional-locks -C <path>` (V1:82), `["orca-ide", *args]` (V1:175) | MET | Exact argv, env and `timeout=10` (V2:175-177) | NOT MET | FRs stated as goals: "Protect the live Git index before adding any other probe behavior." (V3:56), "Separate lifecycle classification from policy, result and closure assessments." (V3:80) |
| Each section has a clear purpose | MET | Each section opens with its subject, for example V1:47 (FR), V1:97 (architecture), V1:252 (failures) | MET | Each section opens with its subject, for example V2:22 (root cause), V2:207 (report path) | MET | First line after each H2 states its subject, for example V3:10, V3:150, V3:191, V3:258 |
| Acronyms and domain terms defined on first use | NOT MET | AC defined (V1:47), CND (V1:252) and A1 (V1:97) defined; GQ (V1:75) and WC (V1:38) used without expansion | NOT MET | GQ (V2:58), WC (V2:42) and K-1 (V2:263) used without expansion | NOT MET | GQ (V3:28, V3:376) and WC (V3:52) used without expansion |
| Actionable next steps or decision points | MET | Open questions with recommended answers (V1:304-316) | MET | Open questions with recommended answers (V2:287-298) | MET | Open questions with recommended answers (V3:396-410) |
| **Subtotal** | **4/5** | | **3/5** | | **2/5** | |

### Risk Coverage (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|-----------|----|----------|----|----------|----|----------|
| At least 3 risks with probability and impact | NOT MET | Risk table columns are "Risk, Likelihood, Mitigation" (V1:271); no impact assessment | MET | R1-R9 with "likelihood / impact", for example R3 "medium / high" (V2:257) | NOT MET | Risks are bullets of risk plus mitigation only (V3:362-372); no probability or impact |
| Mitigation for each identified risk | MET | Mitigation column on R1-R9 (V1:271-281) | MET | Mitigation on R1-R9 (V2:253-263) | MET | Each bullet names its mitigation, for example V3:362, V3:366 |
| Failure modes and recovery procedures | MET | Failure table with behaviour and exit code (V1:254-267); rollback (V1:318-333) | MET | F1-F9 (V2:237-247); rollback (V2:300-313) | MET | Failure modes (V3:343-358); "Report complete" footer for crash leftovers (V3:187) |
| External dependencies and their failure scenarios | MET | "Orca absent or `runtime_unavailable`" (V1:256) | MET | F1 "Orca absent or down" (V2:239) | MET | "If Orca is unavailable and no Run was supplied ... exit 2" (V3:166) |
| Monitoring or validation for risk detection | MET | Header `Sources:` coverage line per source (V1:217); NFR-002 test (V1:82) | MET | NFR-002 control experiment named as the F7 test (V2:245) | MET | Source coverage section "never implied completeness" (V3:299); explicit coverage loss (V3:137) |
| **Subtotal** | **4/5** | | **5/5** | | **4/5** | |

### Invariant and Edge Case Coverage (5 criteria)

This dimension also uses `invariant-probe.md`, which names the variant lines behind each invariant.

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|-----------|----|----------|----|----------|----|----------|
| Boundary conditions for collections | MET | Empty section prints "No matching records. This is not an all-clear." (V1:232); call bound reached (V1:263) | MET | "empty tables print 'none' rather than being omitted" (V2:213); paging on `page.nextCursor` (V2:63) | MET | Cap above 50 keeps all rows and marks unenriched rows (V3:62-63); byte limits (V3:137) |
| State variable interactions across component boundaries | MET | `agent_wait` versus `agent_wait_present` keeps null apart from absent (V1:134); list row missing from `worker-show` is CND (V1:261) | MET | FR-010 waiting kinds join `agentWait` and contract state (V2:71); FR-012 joins package state to a worktree's own status (V2:73) | MET | "Preserve absent, explicit null and unreadable evidence as different input states" (V3:74); contradictory lifecycle evidence is CND (V3:197) |
| Guard condition gaps | MET | Removed verbs listed (V1:193); `--window` parser cases (V1:53) | MET | `--window` usage error (V2:58); `resolve()` symlink check (V2:247) | MET | "negative fixtures fail before subprocess execution" (V3:57); inputs are data, never instructions (V3:139) |
| Count divergence | MET | "Distinct affected sessions: <N> (set union, not a sum)" (V1:232); `sessions <shown>/<total>` (V1:216) | MET | GAPS count reconciled, "113 rows, 88 open, 25 resolved" (V2:285); one status per worktree (V2:75) | MET | "stable IDs appear once ...; visible, historical and omitted counts reconcile, with unknown totals labeled lower bounds" (V3:114) |
| Interaction effects when features combine | NOT MET | One interaction is considered (sweep git versus worker `index.lock`, V1:180). Two are not: boolean `person_started` (V1:136) combined with rule 7 idle (V1:153) under an Orca outage makes worker transcripts idle (INV-003, invariant-probe.md:9); rule 2 returning CND for every exited row (V1:148) with fencing always unreadable on live rows (V1:134) hides rules 4 and 6 (INV-007, invariant-probe.md:13) | MET | F7 sweep-versus-worker lock interaction (V2:245); R8 feedback loop where the report dirties the worktree and the next sweep flags its own output (V2:262, V2:265) | MET | Same-second and concurrent sweeps "produce separate files or fail cleanly" (V3:133-134); the Markdown and JSON derive from one frozen model (V3:177) |
| **Subtotal** | **4/5** | | **5/5** | | **5/5** | |

Note on fairness: the probe cites V1's lines for INV-003 and INV-007 because V1's rule table was the one the debate converged on. V2's idle row is unreachable (V2:155-156), so it cannot produce INV-003's false idle, but that is a correctness defect already scored under Correctness, not an interaction that V2 analysed.

### Qualitative Summary

| Dimension | V1 (opus:architect) | V2 (opus:analyzer) | V3 (haiku:backend) |
|-----------|-----------|-----------|-----------|
| Completeness | 4/5 | 4/5 | 4/5 |
| Correctness | 5/5 | 1/5 | 2/5 |
| Structure | 5/5 | 5/5 | 3/5 |
| Clarity | 4/5 | 3/5 | 2/5 |
| Risk Coverage | 4/5 | 5/5 | 4/5 |
| Invariant and Edge Case Coverage | 4/5 | 5/5 | 5/5 |
| **qual_score** | **26/30 = 0.867** | **23/30 = 0.767** | **20/30 = 0.667** |

## Edge Case Floor Check

Rule (scoring-protocol.md A.2): a variant scoring below 1/5 on Invariant and Edge Case Coverage cannot be the base.

| Variant | Invariant and Edge Case score | Floor (at least 1/5) | Eligible as base |
|---------|-------------------------------|----------------------|------------------|
| V1 (opus:architect) | 4/5 | Pass | Yes |
| V2 (opus:analyzer) | 5/5 | Pass | Yes |
| V3 (haiku:backend) | 5/5 | Pass | Yes |

No variant is below the floor, so the floor was not suspended and removes no candidate.

## Position-Bias Mitigation

Pass 1 scored the variants in input order (V1, V2, V3). Pass 2 scored them in reverse order (V3, V2, V1), from a fresh reading of the cited sections. 90 verdicts per pass (30 criteria by 3 variants). The two passes agreed on 87 and disagreed on 3. Each disagreement was re-evaluated by putting both passes' evidence side by side against the criterion text; the re-evaluation verdict is final.

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|-----------|---------|--------|--------|-----------|-------|
| Structure 3: clear separation of concerns | V3 | MET | NOT MET | DISAGREE | NOT MET. Pass 1 accepted the section titles; pass 2, read first, found safety values and package-state rules inside the classification section (V3:209, V3:246) and verification merged with rollback (V3:412-431). The titles do not separate the concerns the text mixes |
| Clarity 1: unambiguous language | V2 | NOT MET | MET | DISAGREE | NOT MET. Pass 2 read V2 right after V3's "if needed" and "recommend" and judged V2 better by comparison. The criterion is absolute, not relative: FR-022 "may print ... and may name" (V2:86) leaves a required output optional |
| Invariant 5: interaction effects | V1 | MET | NOT MET | DISAGREE | NOT MET. Pass 1 credited the git-lock interaction (V1:180). Pass 2, read last after V2's R8 and V3's concurrency analysis, checked V1's own state model and found the INV-003 and INV-007 interactions (V1:134, V1:136, V1:148, V1:153; invariant-probe.md:9, :13) that the variant does not consider. One considered interaction does not offset two unconsidered ones in the variant's core rule table |

Disagreements re-evaluated: 3
Final verdicts changed: 2 (relative to pass 1: V3 Structure 3 and V1 Invariant 5 moved from MET to NOT MET; V2 Clarity 1 kept its pass 1 verdict)

Effect of the re-evaluation on the totals: had the pass 1 verdicts stood, V1 would score 27/30 and V3 21/30. The selected base is the same either way.

## Combined Scoring

| Variant | Quant (×0.50) | Qual (×0.50) | **Final Score** | Debate Tiebreaker |
|---------|---------------|--------------|-----------------|-------------------|
| A: V1 (opus:architect) | 0.4792 | 0.4333 | **0.9125** | 30.7% (23 of 75 sole wins) |
| B: V2 (opus:analyzer) | 0.4817 | 0.3833 | **0.8650** | 12.0% (9 of 75) |
| C: V3 (haiku:backend) | 0.4535 | 0.3333 | **0.7868** | 21.3% (16 of 75) |

**Margin**: 4.75% between first (V1, 0.9125) and second (V2, 0.8650), below the 5% threshold (|0.9125 - 0.8650| = 0.0475 < 0.05). V2 to V3 is 7.82%.
**Tiebreaker applied**: Yes. Step 1 (debate performance) decides it; steps 2 and 3 were not needed.

Tiebreaker detail. Source: the scoring matrix in `debate-transcript.md` (lines 128-229), over the 75 S, C and X diff points (the 25 A points are shared assumptions, not contests). A sole win is a point whose winner is one variant alone; merged winners are counted separately.

| Variant | S (13) | C (43) | X (19) | Sole wins | Share of 75 | Merged wins that include it |
|---|---|---|---|---|---|---|
| V1 | 5 | 11 | 7 | 23 | 30.7% | 20 |
| V2 | 6 | 2 | 1 | 9 | 12.0% | 14 |
| V3 | 1 | 11 | 4 | 16 | 21.3% | not needed for the V1 / V2 decision |

V1 leads V2 on sole wins (23 against 9, a gap of 18.7 points, far outside the 5% band) and on merged wins (20 against 14), so step 1 selects V1. Round 3 moved X-001 and C-015 to V3 (convergence-tracking.md:254); those are already counted under V3's sole wins. The same order holds on the correctness count (V1 5/5 against V2 1/5), so step 2 would have chosen V1 as well.

## Selected Base: Variant 1 (opus:architect)

### Selection Rationale

- The base was force-selected by score because the gate was BLOCKED_BY_INVARIANTS (INV-005 accepted risk, no owner sign-off). The selection does not resolve INV-005; it is carried forward as an unresolved conflict for the return contract (convergence-tracking.md:302).
- V1 has the highest combined score (0.9125). Its quant score (0.958) is 0.005 below V2's (0.963), a gap that comes from one more H2 section in V2 and a higher sampled specificity. Its qual score (26/30) is 3 criteria above V2 and 6 above V3.
- The decisive difference is Correctness: V1 5/5, V2 1/5, V3 2/5. A base must carry the fewest defects into the merge. V2's four defects sit in load-bearing places: the rule table (idle unreachable, V2:155-156), the seam (binary name, V2:175 against V2:84), the CLI exit rule (V2:57 against Seed:63) and the WC-14 text (unscoped lock claim, V2:228). V3's defects sit in its probe surface (V3:246, V3:285) and its test policy (V3:403).
- The margin to V2 is under 5%, so the debate tiebreaker applied, and V1 won it clearly (23 sole wins to 9).
- V1's two known gaps are both fixable by merging, not rewriting: the missing per-session next action (S1) comes from V3:303, and the missing impact column comes from V2's risk format (V2:257). The INV-003 and INV-007 interactions in V1's rule table (V1:136, V1:148, V1:153) are already resolved by agreed Round 3 text (convergence-tracking.md:255-256, :274).
- Every variant passed the edge-case floor, so no candidate was excluded before ranking.

### Strengths to Preserve from Base

1. The total, ordered rule table with idle as rule 7 and an explicit fallback rule 8 (V1:145-154), with precedence pinned by a named `RULES` tuple (NFR-010; R4 at V1:276). Apply the Round 3 amendments listed below to rules 2 and 7.
2. The module boundary table and boundary rules B1-B5 (V1:99-118), including B3: the read allowlist lives only in `probes.py` (V1:116).
3. The read and write split: the sweep package holds no write verb (FR-021, V1:71; R5 at V1:277).
4. The seam that builds the git prefix itself, `git --no-optional-locks -C <path>`, so no call site can omit it (V1:176; INV-019, invariant-probe.md:25), and the smallest git surface: one status form, no `git log`, `git branch`, `git stash list` or `git worktree list` (V1:202).
5. JSON `schema_version: 1`, additive keys only, with the row key `class` (V1:127, V1:234).
6. The call and time bounds and the "call bound reached" coverage note (FR-020, V1:263).
7. The WC-14 placement and never-as-worker pins (V1:238-246), with the contract test renamed so it does not state a count (C-026).
8. The extension-point table for later phases (V1:122-127).
9. The GQ-101 to GQ-113 resolution table (section 12, V1:283-302).
10. The rollback table (section 14, V1:318-333).
11. The fixed report strings: "No matching records. This is not an all-clear." and the set-union count line (V1:232), and "Messages coverage: partial" (V1:221).

### Strengths to Incorporate from Non-Base Variants

**From V2 (opus:analyzer)**

1. The single isolated real-git control test for the lock-free claim (NFR-002, V2:98; F7 test column, V2:245; X-010).
2. The per-row `rule` id and `evidence` tuple in the classification record (V2:139; C-037), and in JSON per C-017: `rule`, `evidence`, `notes` and `safe_to_close`, never `yes` in Phase 1 (convergence-tracking.md:264).
3. FR-026 `.gitignore` with `git check-ignore` in both directions (V2:93), and the R8 feedback-loop rationale (V2:262, V2:265).
4. The likelihood / impact risk format (V2:253-263), which fixes V1's missing impact column (V1:271).
5. The test column in the failure table (V2:237-247).
6. The 101-row pagination AC, enabled only once the step 1.0a cursor capture exists (C-014; convergence-tracking.md:263).
7. The path-walk root for disk discovery (C-012) and the `resolve()` symlink check (FR-006, V2:64; F9, V2:247).
8. "Could not determine" rows placed before working rows, "because an unknown can hide a person-wait" (V2:211; C-018).
9. Reading only the needed `worker-show` fields (FR-005, V2:63).

**From V3 (haiku:backend)**

1. A per-session next-inspection field: "class, waiting-on, evidence, next inspection" (V3:303; C-038, X-015). This closes V1's S1 gap.
2. The re-run contract: collision suffix and exclusive reservation, so a report never overwrites another (V3:181, NFR-006 at V3:133-134; C-019, C-020).
3. Success JSON printed only after publication, and no success JSON after a failed write (V3:167, V3:185; C-017, INV-014). "Exit 0 means collection completed and the report was successfully published" (V3:161; C-016).
4. The `Report complete` footer for crash leftovers (V3:187), and the "What I could not determine" section (V3:307).
5. Symlink-safe output that does not overlap inputs (C-040), byte limits of 1 MiB, 256 KiB and 8 MiB with explicit coverage loss (V3:137; C-029, recorded as proposed limits needing a rationale), and neutralizing of HTML in rendered text (C-030).
6. "Ownership review", never a definitive "foreign" label for ready Tasks (V3:226, V3:301; C-005).
7. The WC-14 end condition "until every Task it created is settled and every result has been inspected and its admission or rejection recorded" (V3:324-325), plus "It never stops watching on its own." (C-022; INV-012).
8. A periodic sweep duty without a scheduler (C-023, X-008), tied to the owner order of 2026-11-05 (INV-011). V3's five-minute cadence (V3:405) is not adopted, because it has no rationale.
9. The "recommends nothing" verb list: "no stop, retry, release, merge or removal" (V3:335; C-024).
10. Exit 2 without `--run` when Orca is down (V3:166; X-001, C-015), which became the agreed rule in Round 3.
11. The Shift Brief section (V3:306), duplicate-dispatch handling (V3:63) and lower-bound totals (V3:114, V3:299).

**Round 3 resolutions to merge (agreed text in convergence-tracking.md:272-275)**

1. INV-001 (RESOLVED): merged text from V3R3:31. Without `--run`, an unavailable lookup exits 2 with `Orca unavailable; no Run binding could be established: pass --run <id>`, and a confirmed missing binding exits 2 with `no Run bound: pass --run <id>`; neither writes a report or success JSON. With an explicit Run, or a binding already established, a later unavailable result stops Orca reads, keeps collected evidence, marks remaining Orca sources unscanned and continues disk-only. Exit 0 needs successful publication; a write failure exits 1. Sources: V1R3:22, V2R3:24, V3R3:31.
2. INV-002 (RESOLVED): each `_orca` result is classified once as `ok`, `no_binding`, `unavailable` or `call_failed`. A nonzero exit or invalid response on the first Orca call is unavailable; no `_orca` call follows an unavailable result; `no_binding` needs the captured explicit no-binding shape and `ok` the captured success shape, both UNVERIFIED until step 1.0a, so that capture is a precondition for the parser. Sources: V1R3:23, V2R3:25, V3R3:32.
3. INV-003 (RESOLVED): `person_started` is True, False or None. True only when every scoped worker list is complete, nothing relevant is unscanned or truncated, and the tab-map join completed; None never becomes idle or Historical and falls to rule 8. This replaces `person_started: bool` at V1:136. Sources: V1R3:24, V2R3:26, V3R3:33.
4. INV-007 and C-003 / X-002: rule 2 declines (no match) and attaches its note instead of returning could not determine (convergence-tracking.md:255). The test must use a rule 4 or rule 6 case, not a `blocked` contract that rule 1 already catches (convergence-tracking.md:326).
5. X-009: the binary is `ORCA_CLI_COMMAND` if set, else `orca-ide` (2 of 3 majority, convergence-tracking.md:247). This replaces the fixed `["orca-ide", *args]` at V1:175.
6. C-014, C-017, C-022 and C-034 as agreed in convergence-tracking.md:263-266. C-034: new package, command, skill and docs first; check the PR #422 overlap before the contract edit; WC-14 and its pins land in this PR.

**Carried forward, not resolved by the merge**

- INV-005 (HIGH, ACCEPTED-RISK-OWNER-SIGNOFF, no sign-off recorded): lock-free claims are scoped to the sweep's own `_git` calls, and the report states `Orca read verbs' git effects on worker worktrees: UNVERIFIED` (V3R3:34). V2R3:27's `GIT_OPTIONAL_LOCKS=0` on `_orca` is a candidate mitigation only, not merged text (convergence-tracking.md:275).
- MEDIUM warnings: INV-008 (untracked-directory reporting gap disclosed, not closed), INV-011 (no required cadence), INV-017 (whether the sweep environment carries `ORCA_CLI_COMMAND` is UNVERIFIED) (convergence-tracking.md:310-318).
