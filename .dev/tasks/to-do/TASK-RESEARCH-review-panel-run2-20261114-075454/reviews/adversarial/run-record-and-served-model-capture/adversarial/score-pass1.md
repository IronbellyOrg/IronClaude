# Scoring Pass 1 (input order): slot C-08 run-record-and-served-model-capture

Variant 1 = Proposal A (`variant-1-original.md`, new per-run `events.jsonl`). Variant 2 = Proposal B (`variant-2-original.md`, extend the existing stores). Both scored as written, not as the hybrid the debate converged on. Scorer: Pass 1, input order (within every criterion Variant 1 is judged before Variant 2). `score-pass2.md` was not read.

## Quantitative Scoring (50% weight)

Computed by `ADV/quant-score.py` (stdlib regex, deterministic; two runs produced byte-identical `quant-score-output.json`, sha256 `b9e9e6ceae0395e16f307261d1c809d0a2b44a6e4caf76c4c8661a4e35820bea`). Full counts, the 30-topic list with per-topic match basis, and unresolved references are in `quant-score-output.json`.

| Metric | Weight | Variant 1 (Proposal A) | Variant 2 (Proposal B) |
|--------|--------|------------------------|------------------------|
| requirement_coverage | 0.30 | 0.9667 (29/30 topics; unmatched: T16 two labelled cost bases) | 0.9667 (29/30 topics; unmatched: T07 OQ-19 reviewer model actually used) |
| internal_consistency | 0.25 | 0.9487 (1 - 2/39; INTRA-A X-004, X-010) | 0.8718 (1 - 5/39; INTRA-B X-002, X-003, X-007, X-008, X-009) |
| specificity_ratio | 0.15 | 1.0000 (130 concrete, 0 vague of 161 substantive statements; 31 neutral) | 1.0000 (117 concrete, 0 vague of 134 substantive statements; 17 neutral) |
| dependency_completeness | 0.15 | 1.0000 (14/14 resolved: 4 section, 4 item, 5 M, 1 objection) | 1.0000 (16/16 resolved: 3 section, 10 B-NN, 3 objection) |
| section_coverage | 0.15 | 0.8889 (8 H2 of max 9) | 1.0000 (9 H2 of max 9) |
| **quant_score** | | **0.9605** | **0.9579** |

Computation notes and limits:

- RC: no formal requirement IDs, so topic-level matching (protocol edge case) over 30 topics drawn from the C-08 row (CO-19, CO-20, CO-11, C-S10, FX-16, FX-19, OQ-19, OQ-21, OQ-23, INV-F, INV-H, INV-A, INV-L) and the requirement list in the task brief (served model from transcript not orchestrator, cost row per agent attempt, two labelled cost bases, serialised concurrent writes, no document text in telemetry, strata module list, memory owner and study switch, PR-review and rf-qa effect, pre-registered measurement, strongest objection answered, consistency with C-01/C-02/C-03, null fallback, non-reviewer roles, contract 1.8.0, edit fence, E1 log replay). A topic matches on an ID hit or a keyword hit (protocol steps 2-3). RC does not discriminate: ID-only mentions count. Variant 1 names FX-16 and FX-19 only in its header and source list (lines 4 and 6), Variant 2 names FX-19 only in its section 4 list, so those matches are nominal and are handled in the qualitative Completeness criterion 1.
- IC: claims = tagged claims ([CODE-VERIFIED], [CODE-CONTRADICTED], [UNVERIFIED]); 39 in each variant. Contradictions = the INTRA rows in `diff-analysis.md` (parsed from the file by the script and asserted equal to the list in the task brief).
- SR: statement-level. A statement is concrete if it holds a number, backticked entity, file name, "percent" or "zero"; vague if it holds a protocol vague indicator (appropriate, as needed, properly, adequate, should consider, might, various, etc., best practices, industry standard). Both papers contain none, so SR = 1.0 for both and carries no signal.
- DC: only internal references (section, item, B-NN, M1-M5, objection N); references to SKILL.md, research files and other documents are excluded by a context filter. Both papers resolve every reference.
- SC: H2 counts 8 and 9.

## Qualitative Scoring, Pass 1 (50% weight), additive binary rubric

Method: CLAIM (the criterion, per the Criterion column) / EVIDENCE (quote or section reference from that variant, or "No evidence found" with sections searched) / VERDICT (MET or NOT MET, no partial credit). Code facts used as counter-evidence were verified in the debate (`debate-transcript.md`, `diff-analysis.md`, `invariant-probe.md`), cited by their X-, A- or INV- ids.

### Completeness (5 criteria)

| Criterion | Variant 1 | Evidence (V1) | Variant 2 | Evidence (V2) |
|-----------|-----------|---------------|-----------|---------------|
| C1 Covers all explicit requirements from source input | NOT MET | Covers CO-19, CO-11, CO-20 (sections 1-2), C-S10 (section 2 telemetry row), OQ-19/21/23 (end of section 2), INV-F/H/A/L (section 5). But FX-16 and FX-19 appear only in the header and source list (lines 4, 6) with no design content, and the decided "two labelled cost bases" requirement is absent: searched sections 1, 2, 6, 8, no "all agents" or second basis anywhere (script T16 unmatched) | NOT MET | Covers CO-19, CO-11, C-S10, FX-16 (section 6), two labelled bases (section 2 `manifest summary`, section 4), OQ-23 (M2). But OQ-19 (reviewer model actually used, `spec-panel.md:258`) is not addressed anywhere (script T07 unmatched; 0 mentions), FX-19 is only named in the section 4 list, and CO-20 (memory written by one step at publish with a study switch) is declined: "Memory keeps its writer" (section 1, 7.3.3) |
| C2 Addresses edge cases and failure scenarios | MET | Section 1: "When the adapter cannot read a value the field is `null` and `identity_source` stays `requested-pinned`"; section 1 and 3: refusal rows with `completion` of `refused`; section 5: "`fcntl` is POSIX-only"; section 8 answer 4: A "degrades to `null`" | MET | Section 7.2.1: killed attempt recorded with `failed` or `timed_out` and `usage_complete: false`; 7.2.3: "a run killed with no process left to commit `published` or `failed` leaves no `agents[]`"; section 5.2 INV-L: stale-`rev` refusal gets "re-read, retry once, then record `panel_fallback_reason`" |
| C3 Includes dependencies and prerequisites | MET | Section 3: "Dependency: C-01 condition 2 says the location-reliability measurement runs only after the snapshot plumbing is fixed"; item 17: "the one open dependency of the whole position" (adapter availability); item 14: E1 logs untracked so the adapter can be validated only on logs on disk | MET | Section 9: "B depends on them" with C-03's refusal contract (exit 12); section 2 adapter row: availability "open (OQ-3, GQ-215)"; section 8 M1: E1 logs "sit untracked on the owner machine" |
| C4 Defines success/completion criteria | MET | Section 6 M1-M5: for example M1 "supported if ... in at least 13 of 15 runs within 2 percent", M2 "all 400 lines are valid JSON with unique `seq` and all 3 attempts survive", M4 lists tests that "must pass unmodified" | MET | Section 8 M1-M5: for example M2 "Pass: 100 attempts recorded, 0 lost", M4 "pass if `calibrator_diversity: full` is flagged ... and a run with three distinct served ids is not flagged" |
| C5 Specifies what is explicitly out of scope | MET | Section 2 "Left unchanged" column (merge, ledger, findings, cluster modules, `cli/reflect/*`, `derive_verdict`); section 3: merge reading dispatch rows "belongs to C-02/C-03 follow-up, not here"; section 7: "It does not make reviewers read-only (INV-G stays a launch concern, C-07)" | MET | Section 6: "B does not give rf-qa a per-check stage record"; PR panel non-reviewer agents "outside the record unless the PR module also keeps a manifest"; E2's ~25 counters "have no place" under B; section 2 `metrics.json`/`runs.jsonl` "stay non-contract artifacts" |
| **Subtotal** | **4/5** | | **4/5** | |

### Correctness (5 criteria)

| Criterion | Variant 1 | Evidence (V1) | Variant 2 | Evidence (V2) |
|-----------|-----------|---------------|-----------|---------------|
| K1 No factual errors or hallucinated claims | NOT MET | Debate-verified wrong claims: (a) section 2 SKILL.md row says the edit fence "is respected: nothing here requires editing outside the allowed sections" while its memory row moves the Wave 5 write that lives under `### 6.3` (`SKILL.md:585`), outside the fence in `test_shadow_skill_contract.py:52-75` (X-011, conceded); (b) item 20 lists `cli/issue_watch/cycle.py` as a `fcntl`/`flock` user, but its only hit is the docstring at `cycle.py:7` (X-012, conceded); (c) section 1 "cost lives only on these rows" while `export` writes `reviewer_run` records whose required `cost` group is a second copy (`telemetry.py:204-225`, conceded in Round 2 C4) | NOT MET | Debate-verified wrong claims: (a) section 2 and 7.2.1 put `agents[]` on `published`/`failed` stage records, but `fail()` sets only `state` and `failure_reason` (`manifest.py:389-397`), a stage record keeps four keys (`:317-326`) and a committed manifest takes no second write (`:293-296`) (X-002, B withdrew); (b) B-7 and section 2 place the producer "after `merge_round`, and before any refusal exit", but the refusal is raised inside `merge_round` (`ledger.py:150-157`) so that code never runs (X-003); (c) section 5.2 guard "`load` reports a failing legacy line instead of dropping it" describes today's skip-and-count behaviour (`telemetry.py:411-414`) (X-007); (d) section 2 says the aggregator "recomputes `identity_source` ... as it already recomputes parity", but the script reads no `observed` or `identity_source` today (B Round 1 concession 8) |
| K2 Technical approaches feasible with stated constraints | NOT MET | The events file with writer-assigned `seq` is feasible, but stated pieces are not as written: the M2 target of 400 valid lines from 8 writers needs a blocking lock while the cited precedent is `LOCK_EX` with `LOCK_NB`, fail-fast (X-006, `record.py:403`); the memory step violates the stated INV-K fence (X-011); the "refused" rows have no writer (X-004: section 2 says `merge_cmd.py` change is "none"); and the adapter oracle M1(c) "within 2 percent in at least 13 of 15" fails in 0 of 15 on the measured logs, with per-event usage sums over-counting 2.0x to 2.6x (INV-009, INV-010) | NOT MET | The central non-reviewer mechanism (`agents[]` on `published`/`failed`, section 7.2.1) has no code path (X-002); the orchestrator tail cannot be added after commit (`manifest.py:293-296`); the Tier 2 `reviewer_run` producer "at the published commit" has no carrying component (X-008; section 2 table lists only `merge_cmd.py`); M1 "within 1 percent" of run-level `out_tokens` conflicts with its own "through publish" exclusion (X-009) and fails the same measured oracle (INV-010) |
| K3 Terminology used consistently and accurately | MET | Section 1 and 2 use `events.jsonl`, `review record add/ingest/export`, `attempt_id`, `identity_source`/`requested-pinned` the same way in sections 3, 5, 6, 8; tag vocabulary defined in the header line and applied uniformly (39 tagged claims). Slips (orchestrator called an "agent attempt" in section 1) do not change meaning | NOT MET | Section 1 and 7.2.1 call `failed` a stage record ("its `published` and `failed` stage records"), but in the code `failed` is a `state`, not a stage (`manifest.py:389-397`, X-002a); B-8 "names the CLIs `review telemetry` or `review manifest`" is true only through the "or" (SKILL.md has 0 `review telemetry` hits, X-012) |
| K4 No internal contradictions (cross-validated with IC) | NOT MET | IC = 0.9487 (2 INTRA contradictions in 39 tagged claims): X-004 (refusal rows "close" C-03 INV-001, section 3, yet section 2 says `merge_cmd.py` changes "none" and the writer is the orchestrator-called `record add`); X-010 (`<out>/panel/events.jsonl` and export "at publish" for every module, but the spec-review loop has no panel directory or publish step) | NOT MET | IC = 0.8718 (5 INTRA contradictions in 39 tagged claims): X-002, X-003, X-007, X-008, X-009 as listed in `diff-analysis.md`, for example position (2) promises a Tier 2 producer "at the published commit" while the section 2 table names none and B-8 says the reflect SKILL never calls the merge step |
| K5 Claims supported by evidence or rationale within the document | MET | Section 4 holds 21 numbered evidence items with file:line and tags (for example item 2 cites `manifest.py:355-368`, test `:144-159`); section 8 gives a four-part answer; unverified items are tagged (items 5, 10, 17, 18) | MET | Section 3 holds evidence tables B-1 to B-21 with source and tag columns (for example B-1 `manifest.py:347-354`); section 7.2 answers the objection in four numbered points; unverified rows are tagged, though 8 rows are fully UNVERIFIED (S-002) |
| **Subtotal** | **2/5** | | **1/5** | |

### Structure (5 criteria)

| Criterion | Variant 1 | Evidence (V1) | Variant 2 | Evidence (V2) |
|-----------|-----------|---------------|-----------|---------------|
| S1 Logical section ordering (prerequisites before dependents) | MET | H2 order: 1 position, 2 design consequence, 3 consistency with C-01/C-02/C-03, 4 evidence, 5 invariants, 6 measurements, 7 PR/rf-qa effect, 8 objection; evidence (section 4) precedes the invariants and measurements that cite its items; forward references (section 6, section 8) point only to later summaries | MET | H2 order: 1 position, 2 module table, 3 evidence, 4 how B meets decided requirements, 5 invariants, 6 PR/rf-qa effect, 7 objection, 8 measurements, 9 relation to C-01/C-02/C-03; evidence precedes the requirement mapping and invariants that rely on it |
| S2 Consistent hierarchy depth (no orphaned subsections) | MET | H3 appears only under section 4 (4.1 to 4.5, five siblings); no single-child subsection | MET | H3 under section 3 (3.1, 3.2), section 5 (5.1, 5.2), section 7 (7.1, 7.2, 7.3); every parent has at least two children |
| S3 Clear separation of concerns between sections | MET | Position, module consequences, adjudication consistency, evidence, invariants split into "Preserved" and "Endangered or only conditionally preserved", measurements, consumers, objection each in their own H2; section 2 table has a separate "Left unchanged" column | MET | Evidence split into "what the code already has" (3.1) and "what the code lacks" (3.2); invariants split into preserved (5.1) and endangered with guard (5.2); objection split into primary (7.1), answer (7.2), secondary (7.3) |
| S4 Navigation aids (table of contents, cross-references or index) | MET | Numbered evidence items 1-21 cited back from sections 2, 5, 8 ("item 17", "items 5, 10, 17, 18"); "see objection 2 in section 8", "measurement M2 in section 6" | MET | Row ids B-1 to B-21 cited from sections 2, 4, 5, 7 ("B-8", "B-18"); "See section 6", "(section 5)", "section 7, objection 3" |
| S5 Follows conventions of the artifact type (slot position paper) | MET | Carries every part the slot paper requires: position paragraph (section 1), design consequence for named modules (2), invariants (5), pre-registered test or measurement (6), PR-review and rf-qa effect (7), strongest objection with answer (8), plus Status line and tag legend | MET | Carries the same parts: position (1), module consequences (2), invariants (5), PR/rf-qa effect (6), strongest objection with answer (7), measurements (8), C-01/C-02/C-03 relation (9), Status line and tag legend |
| **Subtotal** | **5/5** | | **5/5** | |

### Clarity (5 criteria)

| Criterion | Variant 1 | Evidence (V1) | Variant 2 | Evidence (V2) |
|-----------|-----------|---------------|-----------|---------------|
| L1 Unambiguous language (no "should consider", "might", "as appropriate") | MET | Script SR check: 0 statements contain a protocol vague indicator (searched all 8 H2 sections). Open choices are named as open, for example section 2 "Whether this travels in the `*.meta.json` sidecar or a new `WorkerResult` field is left open" | MET | Script SR check: 0 vague-indicator statements (searched all 9 H2 sections). Open choices are named as open, for example section 1 "no `review-telemetry/2` unless the owner decides value tightening needs a version bump" and section 2 "B does not need to choose" |
| L2 Concrete rather than abstract | MET | 130 of 161 substantive statements carry a number, entity or file ref; named CLI calls (`record add`, `record ingest --transcript <file>`, `record export`), exact thresholds in M1-M3 (13 of 15, 2 percent, 10 percent) | MET | 117 of 134 substantive statements concrete; closed key set named in section 2 (tokens_in, tokens_cache_read, tokens_cache_write, tokens_out, wall_s, usage_complete); M2 "100 concurrent `manifest advance --reviewer-id` processes" |
| L3 Each section has a clear purpose statement or one-sentence summary | MET | Section 1 "(one paragraph)" position; section 3 opens "This position agrees with all three outcomes; the points where it depends on one of them ... are stated"; section 6 "Registered before any run, as the wrongness rules below"; section 8 "Objection ... Answer, in four parts" | MET | Section 4 opens with the six decided requirements then maps each; 5.1 "Preserved" and 5.2 "Endangered, with the guard B proposes"; 7.1 "The strongest objection", 7.2 "The answer"; section 8 "All four are pre-registered" |
| L4 Acronyms and domain terms defined on first use | NOT MET | Header line 4 lists "CO-19, CO-20, CO-11 (adapter), C-S10, FX-16, FX-19, OQ-19, OQ-21, OQ-23" and "INV-F (HIGH), INV-H, INV-A, INV-L (MEDIUM)" with no gloss (INV-F is glossed only in section 5, "installed-path rule"); "E2 commit", "E3 live-eval harness", "GQ-193", "OQ-3" and "R13 P11" are used without definition | NOT MET | Section 2 uses "D-17" and "D-31" without definition and "OQ-3, GQ-215" in the adapter row; section 3.2 B-21 uses "R-23" undefined; INV-F and INV-H are glossed in section 5 only, after use in section 2 ("INV-F" in the adapter row) |
| L5 Actionable next steps or decision points clearly identified | MET | Section 6 M1-M5 each end with a decision rule (for example M1 "A is wrong on per-agent cost if (c) fails in more than 2 runs ... falls back to the reviewer-run level"; M3 "only the identity half of A remains"); section 8 "What A concedes" | MET | Section 8 M1-M5 each carry Pass/Fail rules (for example M1 "Fail: the adapter cannot attribute usage per agent ... both positions fall back to `null`"); explicit owner decisions named (version bump, later `agent_run` kind, lint line in `panel_lint.py`) |
| **Subtotal** | **4/5** | | **4/5** | |

### Risk Coverage (5 criteria)

| Criterion | Variant 1 | Evidence (V1) | Variant 2 | Evidence (V2) |
|-----------|-----------|---------------|-----------|---------------|
| R1 Identifies at least 3 risks with probability and impact assessment | NOT MET | Section 5 "Endangered" names five risks (INV-H leak via `ext{<module>}`, INV-F installed-path, INV-K generator check, existing `/1` pins, POSIX-only `fcntl`) with consequences, but gives no probability for any; the only likelihood datum is the manifest race ("29 real manifests show no lost attempt", item 5, [UNVERIFIED]) and "HIGH in the slot row" for INV-F is impact only | NOT MET | Section 5.2 names three endangered invariants (INV-H, INV-L, `cli/reflect` untouched) with how each is endangered and a guard, plus the 7.2.3 residual; no probability is stated for any; the only frequency data are "0 lost attempts in 29 real manifests" and "9 of 29 manifests" (both [UNVERIFIED], section 3) |
| R2 Provides mitigation strategy for each identified risk | MET | Section 5: INV-H "must be type-checked like a group"; INV-F "preserved only if no primitive text names the adapter as a script path"; INV-K "the module names above avoid it"; `/1` pins "stay as they are and `/2` gets its own"; section 8 answers the objection with M2/M3 fallbacks | MET | Section 5.2 "Guard" column answers every row (INV-H: closed key sets, type checks at `append`, extend `test_no_document_text_in_any_record`; INV-L: re-read, retry once, `panel_fallback_reason`; `cli/reflect`: keep the check in a script); section 7.2 mitigates the objection point by point |
| R3 Addresses failure modes and recovery procedures | MET | Section 1 adapter unreadable gives `null` and `requested-pinned`, "nothing is estimated"; section 2: "export can run after the fact on the transcript"; section 8 answer 4: A "degrades to `null` plus `requested-pinned`, never to a made-up value" | MET | Section 7.2.1 killed attempt keeps `failed`/`timed_out` plus `usage_complete: false`; 7.2.3 "The adapter can be run later over a manifest left in a non-terminal state, but that is a recovery action"; 5.2 stale-`rev` fallback continues as legacy (`SKILL.md:338`) |
| R4 Considers external dependencies and their failure scenarios | MET | Item 17: transcript adapter availability "in every harness" and gateway alias pricing, [UNVERIFIED]; item 14: E1 logs untracked so M1 runs only on disk; item 20: `fcntl` POSIX-only; section 7 gateway models and `--revagent` limit | MET | Section 2 adapter row: availability "open (OQ-3, GQ-215) in both"; section 6 gateway models "adapter is the only part that must see non-Claude reviewers' served ids"; section 8 M1 "Fail: the adapter cannot attribute usage per agent" |
| R5 Includes monitoring or validation mechanism for risk detection | MET | Section 6 M1 (replay on 15 E1 logs), M2 (8 x 50 concurrent writes with unlocked control over 1000 trials), M3 (premise test), M5 (compare rendered `telemetry:` block with hand-written values) | MET | Section 8 M1 (adapter fidelity), M2 (100 concurrent `manifest advance` plus committed interleaving test), M3 (share of refused `collected` attempts and empty `agents[]`), M4 (A3 identity-gate replay) |
| **Subtotal** | **4/5** | | **4/5** | |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | Variant 1 | Evidence (V1) | Variant 2 | Evidence (V2) |
|-----------|-----------|---------------|-----------|---------------|
| E1 Boundary conditions for collections (empty, single-element, maximum size) | NOT MET | Only the empty case is touched, and only incidentally: section 7 "a consumer that never calls `record add` behaves as today". No treatment of a single-reviewer panel, a maximum panel or event count, an empty or torn `events.jsonl` (searched sections 1, 2, 5, 6, 8; the probe later found the empty-file case unhandled, INV-001, INV-013) | NOT MET | Only the empty case is touched, and only as a measurement: section 8 M3 counts runs "whose `agents[]` is empty because the transcript was unreadable". No treatment of single-element or maximum-size collections (searched sections 2, 3, 5, 7, 8) |
| E2 State variable interactions across component boundaries | MET | Section 8 answer 1: the manifest decides `reviewers_complete` and "feeds the shadow shortfall (`scripts/reflect_shadow_exit.py` reads `reviewers_resolved` and `reviewers_complete`, lines 244-245). Observation and state are different kinds of fact; A keeps them in different files so a wrong or late reading can never change a stage decision" | MET | Section 5.2 INV-L: the revision check "adds a new refusal to `manifest advance` inside shadow mode"; section 2: "The payload hash stays computed over the full payload so replay and conflict behave as today (`manifest.py:353`)"; 5.1: lock and `rev` protect `reviewers_complete` as a verdict input |
| E3 Guard condition gaps (missing validation, unguarded type assumptions) | MET | Item 7: group values are checked "for key presence only (`telemetry.py:213-225`)" and a sentence in `model.resolved` validates [CODE-CONTRADICTED]; item 6: `manifest.validate` checks only that `attempts` is a list; section 5: `ext{<module>}` "must be type-checked like a group" | MET | Section 5.2 INV-H (b): "`validate_record` checks key presence in the six groups, not value types, so a sentence in `model.resolved` validates today"; (c) tightening at `load` "would turn existing E3 harness records into bad lines" |
| E4 Count divergence scenarios (off-by-one, inclusive/exclusive ranges) | MET | M1(c): sum of per-agent `tokens_out` against run-level `modelUsage` "within 2 percent"; item 10: two live outcomes double a run's cost "400 versus 200 per true positive"; section 5: counts "110 stable and 27 telemetry names" and "36 `def test_` functions" stay equal | MET | M1: per-run output tokens "within 1 percent of the extractor's `out_tokens`"; B-18: "9 of 29 real manifests only `collected` attempts exist"; section 2: "one live outcome per `(reviewer_record_id, truth_basis)` is enforced (D-17)"; B-12: 110 stable and 27 telemetry names |
| E5 Interaction effects when features or components combine | MET | Section 3: `verdict_mismatch` "computed at export from the derived verdict and is never an event field" (C-02 interaction); C-03 INV-001/INV-005/INV-007 interaction with refusal rows; section 5: line-count pin in `test_shadow_skill_contract.py` plus the generator-constraint check on new module names | MET | Section 9: `output.verdict_mismatch` "follows whatever C-02's CRITICAL floor changes"; per-reviewer `block_ok` "makes C-02's open INV-009 countable"; section 5.2: stale-`rev` refusal inside shadow mode and a `panel_lint.py` lint line as a C-01 INV-020 case |
| **Subtotal** | **4/5** | | **4/5** | |

### Qualitative Summary (Pass 1)

| Dimension | Variant 1 | Variant 2 |
|-----------|-----------|-----------|
| Completeness | 4/5 | 4/5 |
| Correctness | 2/5 | 1/5 |
| Structure | 5/5 | 5/5 |
| Clarity | 4/5 | 4/5 |
| Risk Coverage | 4/5 | 4/5 |
| Invariant & Edge Case Coverage | 4/5 | 4/5 |
| **qual_score (Pass 1)** | **23/30 = 0.7667** | **22/30 = 0.7333** |

Where the passes will be most sensitive to position bias: Correctness K2 and K3 (feasibility and terminology rest on debate-verified code facts), Completeness C1 (two named gaps per variant), and Invariant E1 (both variants touch only the empty case).

Consistency with the quant layer: K4 is NOT MET for both and matches IC below 1.0 (0.9487 and 0.8718); the larger Correctness gap for Variant 2 matches its five INTRA contradictions against two for Variant 1.

### Edge Case Floor Check

| Variant | Invariant & Edge Case score | Eligible as base (>= 1/5) |
|---------|-----------------------------|---------------------------|
| Variant 1 (Proposal A) | 4/5 | Eligible |
| Variant 2 (Proposal B) | 4/5 | Eligible |

## VERDICTS

```
V1|completeness|1|NOT MET
V1|completeness|2|MET
V1|completeness|3|MET
V1|completeness|4|MET
V1|completeness|5|MET
V1|correctness|1|NOT MET
V1|correctness|2|NOT MET
V1|correctness|3|MET
V1|correctness|4|NOT MET
V1|correctness|5|MET
V1|structure|1|MET
V1|structure|2|MET
V1|structure|3|MET
V1|structure|4|MET
V1|structure|5|MET
V1|clarity|1|MET
V1|clarity|2|MET
V1|clarity|3|MET
V1|clarity|4|NOT MET
V1|clarity|5|MET
V1|risk_coverage|1|NOT MET
V1|risk_coverage|2|MET
V1|risk_coverage|3|MET
V1|risk_coverage|4|MET
V1|risk_coverage|5|MET
V1|invariant_edge_case|1|NOT MET
V1|invariant_edge_case|2|MET
V1|invariant_edge_case|3|MET
V1|invariant_edge_case|4|MET
V1|invariant_edge_case|5|MET
V2|completeness|1|NOT MET
V2|completeness|2|MET
V2|completeness|3|MET
V2|completeness|4|MET
V2|completeness|5|MET
V2|correctness|1|NOT MET
V2|correctness|2|NOT MET
V2|correctness|3|NOT MET
V2|correctness|4|NOT MET
V2|correctness|5|MET
V2|structure|1|MET
V2|structure|2|MET
V2|structure|3|MET
V2|structure|4|MET
V2|structure|5|MET
V2|clarity|1|MET
V2|clarity|2|MET
V2|clarity|3|MET
V2|clarity|4|NOT MET
V2|clarity|5|MET
V2|risk_coverage|1|NOT MET
V2|risk_coverage|2|MET
V2|risk_coverage|3|MET
V2|risk_coverage|4|MET
V2|risk_coverage|5|MET
V2|invariant_edge_case|1|NOT MET
V2|invariant_edge_case|2|MET
V2|invariant_edge_case|3|MET
V2|invariant_edge_case|4|MET
V2|invariant_edge_case|5|MET
```

Totals from the block: V1 23 MET, V2 22 MET. Edge-case-floor eligibility: V1 eligible (4/5), V2 eligible (4/5).
