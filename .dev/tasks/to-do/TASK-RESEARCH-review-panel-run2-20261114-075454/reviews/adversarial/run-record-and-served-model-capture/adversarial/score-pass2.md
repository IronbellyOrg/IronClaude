# Qualitative Scoring, Pass 2 (reverse order)

Slot C-08 (run-record-and-served-model-capture). Variant 1 = Proposal A (new per-run `events.jsonl`), Variant 2 = Proposal B (extend the existing stores). Order of evaluation: Variant 2 first and completely, then Variant 1. Protocol: `scoring-protocol.md` A.2 (30-criterion additive binary rubric, CEV evidence) and A.5 (position-bias pass 2). Variants are scored as written, not as the hybrid the debate converged on. Debate-verified code facts are used as evidence for Correctness; where I re-read code myself it is stated (`telemetry.py:38-81`, `merge_cmd.py:96-117` at HEAD).

Each cell reads CLAIM (the criterion) then EVIDENCE then VERDICT. Column order is Variant 2 first because this is the reverse-order pass.

## Qualitative Scoring (50% weight): Additive Binary Rubric

### Completeness (5 criteria)

| Criterion | Variant 2 (B) | Evidence (V2) | Variant 1 (A) | Evidence (V1) |
|-----------|---------------|---------------|---------------|---------------|
| 1. Covers all explicit requirements | MET | Section 4 maps every decided requirement (CO-19, CO-20, CO-11, C-S10, FX-16, FX-19: served model from transcript, cost per agent on two labelled bases, serialising writes, no document text, strata list, memory writer) to a mechanism; OQ-3 and OQ-23 handled (section 2 adapter row, M2); INV-F/H/A/L covered in section 5. | NOT MET | Section 2 answers OQ-19, OQ-21, OQ-23 and the memory writer, but FX-16 and FX-19 occur only in the header line and "two labelled cost bases" is never stated as a deliverable (searched sections 1, 2, 3, 7, 8; "reviewer-only" appears only as the M3 test premise). |
| 2. Addresses edge cases and failure scenarios | MET | 7.2.3 "Residual B does not close: a run killed with no process left to commit `published`..."; section 2 "When it cannot read a value the field is `null`"; B-7 refused round records nothing; 5.2 INV-L stale-`rev` refusal. | MET | Section 1 "When the adapter cannot read a value the field is `null`"; section 3 INV-001 refusal rows, INV-005 and INV-007 "observable"; section 8 answer 2 concedes the M2 control may show the lock is hygiene. |
| 3. Includes dependencies and prerequisites | MET | Section 9 dependencies on C-01, C-02, C-03 outcomes; section 2 "availability across harnesses is open (OQ-3, GQ-215)"; M1 "not in a fresh checkout" for the untracked E1 logs; B-10 flock precedent. | MET | Section 3 (C-01 condition 2, C-03 "requested, not served" until the adapter exists); item 17 adapter availability "the one open dependency"; item 14 untracked logs; item 20 `fcntl` POSIX-only. |
| 4. Defines success/completion criteria | MET | Section 8 pre-registered pass rules, e.g. M2 "Pass: 100 attempts recorded, 0 lost. Fail: any loss"; M1 "15 of 15 runs ... within 1 percent". | MET | Section 6 M1 "supported if ... 13 of 15 runs within 2 percent"; M2 "all 400 lines are valid JSON with unique `seq` and all 3 attempts survive"; M3 wrongness rule. |
| 5. Specifies what is out of scope | MET | Section 1 "There is no `events.jsonl`, no `review-run-event/1` schema id, no `review record add/export` pair, and no `review-telemetry/2`"; section 2 "`metrics.json`, `runs.jsonl` stay non-contract artifacts"; section 6 E2's ~25 counters "have no place"; slot C-12 "not yet adjudicated". | MET | Module table "Left unchanged" column; section 3 "A does not make `merge` read events (that coupling belongs to C-02/C-03 follow-up)"; section 7 "It does not make reviewers read-only (INV-G stays a launch concern, C-07)". |
| **Subtotal** | **5/5** | | **4/5** | |

### Correctness (5 criteria)

| Criterion | Variant 2 (B) | Evidence (V2) | Variant 1 (A) | Evidence (V1) |
|-----------|---------------|---------------|---------------|---------------|
| 1. No factual errors or hallucinated claims | NOT MET | (a) Section 2 and B-7: producer "after `merge_round`, and before any refusal exit". I re-read `merge_cmd.py:109-112`: the no-valid-block refusal is raised inside `merge_round` and re-raised as `ClickException`, so code after `merge_round` never runs on it (debate X-003, B conceded). (b) Section 2 says the closed key set is "taken from `telemetry.REVIEWER_GROUPS["cost"]` and `["model"]`"; `telemetry.py:49,74-80` hold model = (resolved, launch, observed) and cost = five counters, so `requested`, `identity_source`, `usage_complete` are not there and `launch` is dropped. (c) 5.2 "`load` reports a failing legacy line instead of dropping it": `telemetry.py:411-414` counts it invalid and `continue`s (X-007, conceded). | NOT MET | (a) Item 20 lists `cli/issue_watch/cycle.py` as an `fcntl`/`flock` user; line 7 is only a docstring (A conceded, C9). (b) Section 2 SKILL row "nothing here requires editing outside the allowed sections" while the memory row moves the Wave 5 write that `### 6.3` governs, outside the fence (X-011, conceded). (c) Section 1 "cost lives only on these rows" while `record export` derives `reviewer_run` records whose required cost group is `telemetry.py:204-225` (conceded as loose). |
| 2. Technical approaches feasible with stated constraints | NOT MET | `agents[]` on `published`/`failed` has no code path: `fail()` sets only `state` and `failure_reason` (`manifest.py:389-397`), `advance --stage failed` passes no payload (`manifest_cmd.py:174-175`), hashing orchestrator usage breaks idempotent replay of `published` (`manifest.py:292-299`), and a committed manifest takes no second write (`manifest.py:293-296`; B withdrew `agents[]` in Round 2). "`save` and `load` gain `flock`" does not span the read-modify-write in `advance_cmd`. | NOT MET | The memory step conflicts with the stated edit fence (`test_shadow_skill_contract.py:52-75` forbids `### 6.3` diffs, X-011). `<out>/panel/events.jsonl` and `export` "at publish" are undefined for the spec-review loop, which has no panel directory or publish step (X-010, conceded). "Exclusive flock" with M2 expecting 400 lines, while the cited lock is `LOCK_EX\|LOCK_NB` fail-fast (X-006, conceded). |
| 3. Terminology consistent and accurate | NOT MET | The same `model` record is named by two vocabularies: B-3 gives the telemetry group as ("resolved","launch","observed"), section 2 and section 4 give `model` (requested, resolved, observed, identity_source) as "taken from" it; "published commit" (position paragraph 2) is used for the `published` stage commit. | MET | `review-run-event/1`, `record add/ingest/export`, `reviewer_run`, `agent_role` are used identically in sections 1, 2, 3, 8; the evidence tags [CODE-VERIFIED]/[CODE-CONTRADICTED]/[UNVERIFIED] are applied uniformly in 4.1-4.5. The "no `stage`" remark (section 8) is a naming slip (`REVIEWER_TOP` has `step`), not an inconsistency of usage. |
| 4. No internal contradictions | NOT MET | Section 8 "All four are pre-registered" but M1 to M5 are five; 7.2.2 excludes the post-`published` tail while M1 requires per-run output tokens within 1 percent of the run-level extractor total (X-009, conceded); position paragraph (2) promises a producer "at the published commit (Tier 2 path)" while the section 2 table names a producer only in `merge_cmd.py` and B-8 says the SKILL never calls `review merge` (X-008, conceded). | NOT MET | Section 1 "cost lives only on these rows" versus `record export` deriving `reviewer_run` records; section 3 says INV-001 "is closed by an event row with `completion` of `refused`" while the section 2 `merge_cmd.py` row says "none; merge does not read events" and the writer is the primitive-called `record add` (X-004, conceded); fence "respected" (section 2) versus the memory row. |
| 5. Claims supported by evidence or rationale | MET | Evidence tables B-1 to B-21 with file:line and tag (e.g. B-1 `manifest.py:347-354`, B-6 `merge_cmd.py:73-98`, `ledger.py:127-149`); each position claim has an answer in 7.2 or 5.2. UNVERIFIED rows are labelled and name their research source. | MET | 21 numbered items with file:line (e.g. item 2 `manifest.py:355-368`, `:378-381`, test `:144-159`); unverified items 5, 10, 17, 18 are tagged and sourced to `research/15`. |
| **Subtotal** | **1/5** | | **2/5** | |

### Structure (5 criteria)

| Criterion | Variant 2 (B) | Evidence (V2) | Variant 1 (A) | Evidence (V1) |
|-----------|---------------|---------------|---------------|---------------|
| 1. Logical ordering (prerequisites before dependents) | NOT MET | The adjudicated C-01/C-02/C-03 dependencies are stated only in section 9 (last), after sections 2, 5.2 and 6 already rely on them (C-S10, "C-01 reading, INV-020", FX-16); the measurements (section 8) come after the objection (section 7) that cites M-results. | MET | Order is position (1), module consequences (2), consistency with C-01/C-02/C-03 as section 3 before the evidence, evidence (4), invariants (5), measurements (6), PR/rf-qa effect (7), objection (8). |
| 2. Consistent hierarchy depth | MET | H2 sections 1-9; H3 only as 3.1/3.2, 5.1/5.2, 7.1-7.3, each with at least two siblings. | MET | H2 sections 1-8; H3 only 4.1-4.5 under section 4; sections 5-8 use bold lead-ins, no orphan subsections. |
| 3. Separation of concerns | MET | 3.1 "what the code has" versus 3.2 "what it lacks"; 5.1 preserved versus 5.2 endangered with a Guard column; section 4 requirements versus section 2 modules. | MET | 4.1 manifest, 4.2 telemetry, 4.3 served model, 4.4 precedents, 4.5 memory; 5 split into preserved and endangered. |
| 4. Navigation aids | MET | Evidence IDs B-1 to B-21 cross-referenced in 5.1, 7.2, 7.3, 9; "see section 6", "section 7, objection 3"; tag rule at the top. | MET | Numbered evidence items cross-referenced ("item 17", "item 20", "section 8", "see section 3"); source list in the header. |
| 5. Follows conventions of the artifact type | MET | Carries the position-paper sections shared with Variant 1 (position, design consequence for shared core and named modules, evidence, invariants, PR/rf-qa effect, strongest objection and answer, test or measurement) and closes with `Status: Complete`. Inferred from the shared headings; the template file was not read. | MET | Same section set and `Status: Complete` at top; adds a "What A concedes" paragraph. Same inference caveat. |
| **Subtotal** | **4/5** | | **5/5** | |

### Clarity (5 criteria)

| Criterion | Variant 2 (B) | Evidence (V2) | Variant 1 (A) | Evidence (V1) |
|-----------|---------------|---------------|---------------|---------------|
| 1. Unambiguous language | MET | A grep for might, should consider, as appropriate, perhaps, probably, various, etc. finds none; open choices are named as owner decisions ("unless the owner decides value tightening needs a version bump", section 1; "B does not need to choose", section 2 `metrics.json` row). | MET | Same grep finds no hedge words; the two open points are stated as explicit alternatives ("whether this travels in the `*.meta.json` sidecar or a new `WorkerResult` field is left open", section 2). |
| 2. Concrete rather than abstract | MET | File:line anchors throughout; named keys (`tokens_cache_read`, `usage_complete`), named commands (`manifest summary`, `review telemetry append --dir`). | MET | `record add` "one line per call, writer assigns `seq`, `ts_utc`, `run_id`, exclusive `flock`"; file:line in every module row. |
| 3. Each section has a clear purpose | MET | Each H2 states a purpose in its first sentence or title (section 4 "How B meets the decided requirements of the slot"; section 8 "The test or measurement that would show B right or wrong"). | MET | Section 1 "(one paragraph)" position; section 8 opens "Objection (the best case for position B ...)", then a four-part answer. |
| 4. Acronyms and domain terms defined on first use | MET | Section 4 glosses the six decided requirements in one sentence; 5.1/5.2 gloss INV-F ("installed-path rule"), INV-H, INV-L; the telemetry row states the D-31 and D-17 rules in the same clause; the header defines the tag set and R-file citations. | NOT MET | Header: "Conflict IDs: CO-19, CO-20, CO-11 (adapter), C-S10, FX-16, FX-19 ... INV-F (HIGH), INV-H, INV-A, INV-L" with no gloss; CO-19, FX-16, FX-19 are never defined anywhere in sections 1-8 (searched), and INV codes are glossed only from section 5. |
| 5. Actionable next steps or decision points | MET | 5.2 "If the owner prefers a lint line in `panel_lint.py`, it ... must be treated as a C-01 INV-020 case"; SKILL step edits "pass the adapter's output file to the existing `manifest advance` calls"; M1 to M5 with pass rules. | MET | M1 "the adapter is the first thing to measure"; the `SKILL.md:341`/`:348` replacement named as "a later change"; M1 to M5 with supported/wrong rules. |
| **Subtotal** | **5/5** | | **4/5** | |

### Risk Coverage (5 criteria)

| Criterion | Variant 2 (B) | Evidence (V2) | Variant 1 (A) | Evidence (V1) |
|-----------|---------------|---------------|---------------|---------------|
| 1. At least 3 risks with probability and impact | MET | (1) Manifest lost update: B-16 deterministic interleaving ends with one reviewer and `reviewers_complete = 1` (impact), 0 lost in 29 real manifests (frequency); (2) call-order loss: B-18 9 of 29 manifests have only `collected` attempts, impact stated in 7.1; (3) 5.2 INV-L: stale-`rev` refusal exits non-zero where today it overwrites. | MET | (1) lost update, item 5: 0 lost in 29 manifests; (2) item 10 D-17 fan-out, 400 versus 200 per true positive; (3) item 18 orchestrator share median 0.59 of output tokens (cost under-report); (4) item 7 sentence in `model.resolved` validates. No formal probability labels in either paper; frequencies and quantified impacts are used. |
| 2. Mitigation for each identified risk | NOT MET | 5.2 gives a Guard per endangered invariant, but 7.2.3 "Residual B does not close: a run killed with no process left to commit `published` or `failed` leaves no `agents[]`" and 7.2.2 "The orchestrator's tail after `published` is not in the manifest" are identified risks left without a mitigation (only a recovery action and a label). | MET | Section 5 pairs each endangered item with a condition or guard: INV-H "only if the new value type checks ship with `/2`"; INV-F "the edit ... must add no such line"; INV-K module names avoid the generator check; `/1` tests stay and `/2` gets its own; adapter failure degrades to `null` plus `requested-pinned`; `fcntl` limit names the need for a different lock. |
| 3. Failure modes and recovery procedures | MET | 7.2.1 killed attempt recorded with `failed`/`timed_out` and `usage_complete: false`; 5.2 stale `rev`: "re-read, retry once, then record `panel_fallback_reason` and continue as legacy"; 7.2.3 the adapter "can be run later over a manifest left in a non-terminal state". | MET | Section 1 null when unreadable and "nothing is estimated"; M1 "falls back to the reviewer-run level that `telemetry/1` already has" if per-agent usage is not recoverable; refused and failed core-action rows (sections 1, 3). |
| 4. External dependencies and their failure scenarios | MET | Section 2 adapter "availability across harnesses is open (OQ-3, GQ-215)"; section 6 gateway models: `resolvedModel` is the requested alias, not identity proof; M1 fail case "both positions fall back to `null`". | MET | Item 17 harness availability and gateway alias pricing "the one open dependency of the whole position"; item 14 E1 logs untracked; item 20 `fcntl` POSIX-only. |
| 5. Monitoring or validation mechanism | MET | M2 100-process lock stress; M3 re-scan of new manifests for refused `collected` attempts and empty `agents[]`; M4 replay of A3 through the aggregator recompute; the Stage 2 aggregator keeps recomputing `identity_mismatch_suspected`. | MET | M1 replay with a mismatch check on combo A run 3; M2 control over 1000 trials; M5 renders the `telemetry:` block from events and diffs it against the hand-written fields. |
| **Subtotal** | **4/5** | | **5/5** | |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | Variant 2 (B) | Evidence (V2) | Variant 1 (A) | Evidence (V1) |
|-----------|---------------|---------------|---------------|---------------|
| 1. Boundary conditions for collections | MET | M3 measures "the share of runs whose `agents[]` is empty because the transcript was unreadable"; B-18 "9 of 29 real manifests only `collected` attempts exist (no `dispatched` rows)"; B-13 `identity_source` observed in 1 of 15 and requested-pinned in 14. | MET | Section 7 "a consumer that never calls `record add` behaves as today" (empty record); item 21 `last-pass` holds 5 entries against "overwritten whole" (collection size versus rule); M2 400 lines from eight writers. |
| 2. State variable interactions across component boundaries | MET | 5.2 INV-L: the new `rev` refusal inside shadow mode, fallback "re-read, retry once"; 5.1 `reviewers_complete` feeds the shadow shortfall and is protected by lock plus `rev`; section 2 payload hash "computed over the full payload so replay and conflict behave as today" (`manifest.py:353`). | MET | Item 2 attempt identity rules (`Conflict`, "would add a vote", open-stage only) versus late or re-read usage; section 8 answer 1 observation and state "different kinds of fact" because the manifest decides `reviewers_complete` and the shortfall (`reflect_shadow_exit.py:244-245`). |
| 3. Guard condition gaps | MET | 5.2 INV-H (b): `validate_record` "checks key presence in the six groups, not value types, so a sentence in `model.resolved` validates today"; section 2 `manifest.py:251-252` checks `attempts` only as a list. | MET | Item 7 same finding, "[CODE-CONTRADICTED] the docstring's 'No document text ... ever enters a record' as an enforced rule"; item 6 `manifest.validate` checks only that `attempts` is a list; item 4 "One coordinator writes" not enforced. |
| 4. Count divergence scenarios | MET | B-18 (9 of 29 manifests without `dispatched` rows versus all 29 with every reviewer's `collected` attempt); B-16 `reviewers_complete = 1` after a lost update; M1 per-run output tokens within 1 percent of the extractor total. | MET | M1(c) sum of per-agent `tokens_out` equals run-level `modelUsage` in 13 of 15 runs within 2 percent; M3 reviewer-only within 10 percent of all-stages tokens in 12 of 15; item 13 recounted sums. |
| 5. Interaction effects when components combine | MET | Section 9: C-02 `output.verdict_mismatch` "follows whatever C-02's CRITICAL floor changes"; per-reviewer `block_ok` makes C-02 INV-009 countable; C-03 INV-001 gets a landing place; 7.3.2 two producers, "no run has both today". | MET | Section 3: `verdict_mismatch` "computed at export from the derived verdict and is never an event field" (C-02); INV-001/005/007 of C-03; section 5 INV-K generator-constraint check avoided by module names. |
| **Subtotal** | **5/5** | | **5/5** | |

### Qualitative Summary

| Dimension | Variant 2 (B) | Variant 1 (A) |
|-----------|---------------|---------------|
| Completeness | 5/5 | 4/5 |
| Correctness | 1/5 | 2/5 |
| Structure | 4/5 | 5/5 |
| Clarity | 5/5 | 4/5 |
| Risk Coverage | 4/5 | 5/5 |
| Invariant & Edge Case Coverage | 5/5 | 5/5 |
| **qual_score** | **24/30 = 0.800** | **25/30 = 0.833** |

### Edge Case Floor Check

| Variant | Invariant & Edge Case score | Floor (>= 1/5) | Eligible as base |
|---------|-----------------------------|----------------|------------------|
| Variant 1 (A) | 5/5 | passed | yes |
| Variant 2 (B) | 5/5 | passed | yes |

## VERDICTS

V2|completeness|1|MET
V2|completeness|2|MET
V2|completeness|3|MET
V2|completeness|4|MET
V2|completeness|5|MET
V2|correctness|1|NOT MET
V2|correctness|2|NOT MET
V2|correctness|3|NOT MET
V2|correctness|4|NOT MET
V2|correctness|5|MET
V2|structure|1|NOT MET
V2|structure|2|MET
V2|structure|3|MET
V2|structure|4|MET
V2|structure|5|MET
V2|clarity|1|MET
V2|clarity|2|MET
V2|clarity|3|MET
V2|clarity|4|MET
V2|clarity|5|MET
V2|risk_coverage|1|MET
V2|risk_coverage|2|NOT MET
V2|risk_coverage|3|MET
V2|risk_coverage|4|MET
V2|risk_coverage|5|MET
V2|invariant_edge_case|1|MET
V2|invariant_edge_case|2|MET
V2|invariant_edge_case|3|MET
V2|invariant_edge_case|4|MET
V2|invariant_edge_case|5|MET
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
V1|risk_coverage|1|MET
V1|risk_coverage|2|MET
V1|risk_coverage|3|MET
V1|risk_coverage|4|MET
V1|risk_coverage|5|MET
V1|invariant_edge_case|1|MET
V1|invariant_edge_case|2|MET
V1|invariant_edge_case|3|MET
V1|invariant_edge_case|4|MET
V1|invariant_edge_case|5|MET
