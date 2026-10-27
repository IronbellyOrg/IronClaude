# Phase 3 -- Tier 2 Propagation & Discipline Layer

**Phase Goal:** Land the Tier 2 set (B4, A1, A4, B3, C3, C2) that Phase 5 says "compounds the Tier 1 set" and raises joint confidence on similar-shape regressions to ~0.99. B4 is the cross-session propagation block paired with B1's per-file substrate block; A5/A1/A4 form the verification-discipline triple paired with C4's migration audit; C3/C2 close the codebase-hazard surface beyond C1 alone.

### T03.01 -- Read-on-demand `CLAIM_TABLE` consensus across substrates

| Field | Value |
|---|---|
| Roadmap Item IDs | R-004 |
| Why | Cross-session/cross-substrate claim drift went undetected because no single substrate held the consensus state. B4 is the propagation-prevention block that pairs with B1's per-file substrate block. Rank 4 of 14 (Priority 0.852). |
| Effort | M |
| Risk | Low |
| Risk Drivers | cross-cutting (across substrates) |
| Tier | STANDARD |
| Confidence | [███████---] 70% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None Required \| Preferred: Sequential, Serena |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0005 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0005/spec.md`
- `TASKLIST_ROOT/artifacts/D-0005/notes.md`
- `TASKLIST_ROOT/artifacts/D-0005/evidence.md`

**Deliverables:**
- `/sc:reflect` protocol patch adding a read-on-demand `CLAIM_TABLE` builder that aggregates claims across all substrates (status docs, handoffs, mirror files) on each invocation and emits `DISCREPANCY: cross-substrate-claim-divergence` when two substrates disagree on the same `(claim_id, target)` pair.

**Steps:**
1. **[PLANNING]** Load `/sc:reflect` source; enumerate the substrates the protocol already reads (status docs, handoffs, mirror files, live sources); list the claim-shaped tokens in each.
2. **[PLANNING]** Define the `CLAIM_TABLE` schema: rows of `(claim_id, target, asserting_substrate, claim_value, evidence_locator)`.
3. **[EXECUTION]** Implement `build_claim_table()` that walks each registered substrate, extracts claim rows, and unions them.
4. **[EXECUTION]** Implement a divergence pass: group rows by `(claim_id, target)`, emit `DISCREPANCY: cross-substrate-claim-divergence` for any group where `claim_value` differs across asserting substrates.
5. **[VERIFICATION]** Add fixture: §4.2 status doc claims sync; mirror file lacks the hunk; confirm a DISCREPANCY row references both substrates and the diverging claim values.
6. **[COMPLETION]** Document the schema, builder, divergence rule, and fixture in `TASKLIST_ROOT/artifacts/D-0005/spec.md`; copy run log to `evidence.md`.

**Acceptance Criteria:**
- `/sc:reflect` skill source contains a named `build_claim_table` (or equivalent) subroutine and a divergence pass that emits `DISCREPANCY: cross-substrate-claim-divergence` on the documented schema.
- Running the patched protocol against the §4.2 fixture emits a divergence row referencing the status doc and the mirror file with their diverging claim values.
- Two consecutive runs produce byte-identical divergence output (deterministic).
- Schema, fixture, and run log recorded in `TASKLIST_ROOT/artifacts/D-0005/spec.md` and `evidence.md`.

**Validation:**
- Manual check: bringing the mirror into agreement with the status doc removes the divergence row on the next run.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc) under `TASKLIST_ROOT/artifacts/D-0005/`.

**Dependencies:** None (pairs with T01.01 per Phase 5 §"Synergy adjustments")
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Phase 4 redundancy note: B3 ⊂ B4 -- when shipping B4, B3 may be retired downstream. Mirror: shipping T03.01 may permit retiring T03.04; record the decision in `feedback-log.md` after T03.04 evaluation (per Phase 5 line 77).

### T03.02 -- Claim extraction & re-verification (regex -> grep -> DISCREPANCY)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-006 |
| Why | The §4.2 author wrote sync claims from the migration plan, not from a `grep` against the mirror; A1 mechanizes the extract-then-verify discipline so future claims cannot ship without re-grep evidence. Rank 6 of 14 (Priority 0.829). |
| Effort | S |
| Risk | Low |
| Risk Drivers | none |
| Tier | STANDARD |
| Confidence | [███████---] 70% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None Required \| Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0006 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0006/spec.md`
- `TASKLIST_ROOT/artifacts/D-0006/notes.md`
- `TASKLIST_ROOT/artifacts/D-0006/evidence.md`

**Deliverables:**
- `/sc:reflect` protocol patch adding a `claim_extract_and_reverify(doc_path)` subroutine that regexes claim sentences out of doc-shaped substrates, derives a target+expected-token pair, runs `grep` against the named target, and emits a `DISCREPANCY: claim-not-supported-by-grep` when the grep result contradicts the claim.

**Steps:**
1. **[PLANNING]** Load `/sc:reflect`; survey existing claim-token regexes; choose a single pattern set (e.g., "X is in sync with Y", "X matches Y", "X applied to Y").
2. **[PLANNING]** Define the extraction output: `(claim_text, target_path, expected_token, evidence_anchor)`.
3. **[EXECUTION]** Implement the extractor + grep runner; emit `DISCREPANCY: claim-not-supported-by-grep` when grep returns zero matches for `expected_token` in `target_path`.
4. **[EXECUTION]** Add fixture: §4.2 status doc rows 18-29 (claims sync) + the mirror file (no matching post-migration tokens); confirm DISCREPANCY emits.
5. **[VERIFICATION]** Run on the project; review false-positive rate; tighten the regex set if any non-claim sentences are matched.
6. **[COMPLETION]** Document patterns, extractor, fixture, run log in `TASKLIST_ROOT/artifacts/D-0006/spec.md` and `evidence.md`.

**Acceptance Criteria:**
- `/sc:reflect` skill source contains a named `claim_extract_and_reverify` subroutine that emits `DISCREPANCY: claim-not-supported-by-grep` on the documented schema.
- Running the patched protocol on `phase4.2-multi-branch-validation.md:18-29` against the mirror file emits a DISCREPANCY row quoting the unsatisfied grep target.
- Two consecutive runs produce byte-identical DISCREPANCY output (deterministic).
- Patterns, extractor, fixture, and run log recorded in `TASKLIST_ROOT/artifacts/D-0006/spec.md` and `evidence.md`.

**Validation:**
- Manual check: a sentence that is not a sync claim (e.g., a question or a hypothetical) does not trigger the extractor.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc) under `TASKLIST_ROOT/artifacts/D-0006/`.

**Dependencies:** None (pairs with T03.03 and T02.01 as the verification-discipline triple per Phase 5)
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Phase 4 redundancy note: A2 ⊂ A5; not relevant here, but the verification-discipline triple {A1, A4, A5} has joint effectiveness ~0.97 on the broader claim-population per Phase 5.

### T03.03 -- `Verified by:` column enforcement on state tables

| Field | Value |
|---|---|
| Roadmap Item IDs | R-007 |
| Why | State tables in status docs lacked a "Verified by:" column, so claims could ship without an evidence locator; A4 makes the column mandatory and the protocol enforces presence. Rank 7 of 14 (Priority 0.794). |
| Effort | S |
| Risk | Low |
| Risk Drivers | none |
| Tier | STANDARD |
| Confidence | [███████---] 70% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None Required \| Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0007 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0007/spec.md`
- `TASKLIST_ROOT/artifacts/D-0007/notes.md`
- `TASKLIST_ROOT/artifacts/D-0007/evidence.md`

**Deliverables:**
- `/sc:reflect` protocol patch adding a `state_table_verified_by_check(doc_path)` subroutine that detects markdown state tables and emits `DISCREPANCY: state-table-missing-verified-by` for any table whose header row lacks a `Verified by` column or whose data rows leave that column empty.

**Steps:**
1. **[PLANNING]** Load `/sc:reflect`; identify the markdown table parser already in use or pick one.
2. **[PLANNING]** Define the rule: a "state table" is any markdown table whose first column heading is one of `Item|Component|File|Path|Resource` and whose row count is >= 2.
3. **[EXECUTION]** Implement the detector and the column check; emit a DISCREPANCY row per missing-column or empty-cell occurrence with `(doc_path, table_anchor, row_index)`.
4. **[EXECUTION]** Add fixture: a state table with no `Verified by` column; confirm DISCREPANCY emits with the correct anchor.
5. **[VERIFICATION]** Run on the project; review which existing tables would need to be updated and stage that as a separate doc-update task (not part of this T03.03).
6. **[COMPLETION]** Document the rule, detector, fixture, and run log in `TASKLIST_ROOT/artifacts/D-0007/spec.md` and `evidence.md`.

**Acceptance Criteria:**
- `/sc:reflect` skill source contains a named `state_table_verified_by_check` subroutine emitting `DISCREPANCY: state-table-missing-verified-by` on the documented schema.
- Running the patched protocol on a fixture table with no `Verified by` column emits a DISCREPANCY row referencing the table anchor.
- Two consecutive runs produce byte-identical DISCREPANCY output (deterministic).
- Rule, detector, fixture, and run log recorded in `TASKLIST_ROOT/artifacts/D-0007/spec.md` and `evidence.md`.

**Validation:**
- Manual check: adding a `Verified by:` column with non-empty values to the fixture removes the DISCREPANCY on the next run.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc) under `TASKLIST_ROOT/artifacts/D-0007/`.

**Dependencies:** None
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Pairs with T03.02 and T02.01 as the verification-discipline triple.

### T03.04 -- Structural-fact harvest (bind-mounts -> MEMORIZATION_PROPOSAL)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-008 |
| Why | Structural facts (like the §4.2 host:container bind change) were not being lifted into the always-loaded substrate, so they decayed into per-doc folklore; B3 harvests bind-mount-shaped facts and proposes them for memorization. Rank 8 of 14 (Priority 0.761). |
| Effort | S |
| Risk | Low |
| Risk Drivers | none |
| Tier | STANDARD |
| Confidence | [███████---] 70% |
| Requires Confirmation | Yes |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None Required \| Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0008 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0008/spec.md`
- `TASKLIST_ROOT/artifacts/D-0008/notes.md`
- `TASKLIST_ROOT/artifacts/D-0008/evidence.md`

**Deliverables:**
- `/sc:reflect` protocol patch adding a `structural_fact_harvest()` subroutine that scans `docker-compose.yml` bind-mount lines and any `docs/migrations/*.md` registry entries, then emits a `MEMORIZATION_PROPOSAL: <fact>` block per non-trivial structural fact (non-identity bind, registered host-path migration).

**Steps:**
1. **[PLANNING]** Load `/sc:reflect`; locate the existing memory-write surface (auto-memory or session-memory).
2. **[PLANNING]** Define the harvest scope: every non-identity bind-mount + every entry in the migrations registry.
3. **[EXECUTION]** Implement the harvester; emit `MEMORIZATION_PROPOSAL: bind-mount <service>: <host>:<container>` and `MEMORIZATION_PROPOSAL: migration <id>: <pre> -> <post>` blocks.
4. **[EXECUTION]** Add fixture: the `jenkins` bind-mount line and the §4.2 migration entry produced by T01.02; confirm two MEMORIZATION_PROPOSAL blocks emit.
5. **[VERIFICATION]** Run on the project; sanity-check that proposals are deduplicated against any existing always-loaded memory.
6. **[COMPLETION]** Document the harvester, fixtures, and run log in `TASKLIST_ROOT/artifacts/D-0008/spec.md` and `evidence.md`.

**Acceptance Criteria:**
- `/sc:reflect` skill source contains a named `structural_fact_harvest` subroutine emitting `MEMORIZATION_PROPOSAL` blocks on the documented schema.
- Running the patched protocol against the project emits at least two MEMORIZATION_PROPOSAL blocks: one for the `jenkins` bind-mount and one for the §4.2 migration entry.
- Two consecutive runs produce byte-identical proposals (deterministic; deduplication is content-based).
- Harvester, scope rules, fixture, and run log recorded in `TASKLIST_ROOT/artifacts/D-0008/spec.md` and `evidence.md`.

**Validation:**
- Manual check: removing the §4.2 migration registry entry suppresses the corresponding MEMORIZATION_PROPOSAL on the next run.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc) under `TASKLIST_ROOT/artifacts/D-0008/`.

**Dependencies:** T01.02 (the migrations registry must exist for the harvester to reference)
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Phase 4 redundancy note: B3 ⊂ B4. If T03.01 (B4) ships and is sufficient for this bug class, T03.04 may be retired downstream; track the decision in feedback-log. Confirm B4 (T03.01) coverage is insufficient before committing T03.04 effort -- record the confirmation in `feedback-log.md`.

### T03.05 -- Confirm: C3 tier classification (LIGHT vs STANDARD)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-009 |
| Why | C3 keyword "comment" matched LIGHT (+0.3) but the work is a multi-file scan with non-trivial detection logic; algorithm produced LIGHT by max-score with confidence 65%. Confirmation required before C3 ships at LIGHT verification budget. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | none |
| Tier | LIGHT |
| Confidence | [██████----] 60% |
| Requires Confirmation | Yes |
| Critical Path Override | No |
| Verification Method | Quick sanity check |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0009 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0009/spec.md`
- `TASKLIST_ROOT/artifacts/D-0009/notes.md`
- `TASKLIST_ROOT/artifacts/D-0009/evidence.md`

**Deliverables:**
- A written tier-classification decision for C3 (T03.06): either confirm LIGHT (algorithm result) or override to STANDARD with a documented reason.

**Steps:**
1. **[PLANNING]** Read the algorithm's classification rationale (LIGHT keyword "comment" vs implied STANDARD implementation; LIGHT won by max-score per Section 5.3.2).
2. **[PLANNING]** Read the practical scope of T03.06: multi-file grep, parser, comparison logic.
3. **[EXECUTION]** Decide LIGHT or STANDARD; record the decision in `TASKLIST_ROOT/artifacts/D-0009/spec.md` with one-paragraph rationale.
4. **[VERIFICATION]** Update T03.06 metadata (Tier, Confidence, Verification Method, MCP Requirements) to match the decision.
5. **[COMPLETION]** Note the decision in `feedback-log.md` Override Tier column for T03.06.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/artifacts/D-0009/spec.md` exists and records exactly one decision (LIGHT or STANDARD) with a written rationale.
- T03.06 metadata in `phase-3-tasklist.md` is updated to match the decision (Tier field, Verification Method field).
- Decision recorded; impacts on T03.06 verification budget and MCP requirements identified in the rationale.
- Reviewed with stakeholder(s).

**Validation:**
- Manual check: T03.06 Tier value matches the decision recorded in `D-0009/spec.md`.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc) under `TASKLIST_ROOT/artifacts/D-0009/`.

**Dependencies:** None (blocks T03.06)
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Tier conflict: LIGHT vs STANDARD -> resolved to LIGHT by max-score (keyword "comment" matched). This clarification confirms or overrides that algorithmic result.

### Checkpoint: Phase 3 / Tasks T03.01-T03.05

**Purpose:** Mid-phase checkpoint after the first 5 tasks of Phase 3 to confirm the propagation/discipline detectors land cleanly and the C3 tier decision is settled before C3/C2 ship.

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P03-T01-T05.md`

**Verification:**
- T03.01 through T03.04 each report Acceptance Criteria 1 satisfied with named subroutines and run logs at `TASKLIST_ROOT/artifacts/D-0005/`..`D-0008/`.
- T03.05 produced a written tier decision and T03.06 metadata is updated to match.
- A combined `/sc:reflect` run against the project surfaces at least one finding from each new subroutine without duplicating Phase 1/2 outputs.

**Exit Criteria:**
- Tier 2 propagation/discipline subset (T03.01-T03.04) merged; T03.05 decision recorded; T03.06 metadata updated.
- Checkpoint report at `TASKLIST_ROOT/checkpoints/CP-P03-T01-T05.md` records Pass.
- T03.06 and T03.07 are unblocked.

### T03.06 -- Stale-comment drift scan (`(path, host)` pairs vs compose)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-009 |
| Why | A stale comment at `pipeline-script-phase3.1.groovy:48` ("`/opt/jenkins/artifacts/` on IBCore") agreed with the buggy SCP lines, creating a self-reinforcing wrong narrative; C3 detects (path, host) tokens in code comments that disagree with the live `docker-compose.yml`. Rank 9 of 14 (Priority 0.731). |
| Effort | S |
| Risk | Low |
| Risk Drivers | none |
| Tier | LIGHT |
| Confidence | [██████----] 65% |
| Requires Confirmation | Yes |
| Critical Path Override | No |
| Verification Method | Quick sanity check |
| MCP Requirements | None Required \| Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0010 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0010/spec.md`
- `TASKLIST_ROOT/artifacts/D-0010/notes.md`
- `TASKLIST_ROOT/artifacts/D-0010/evidence.md`

**Deliverables:**
- `/sc:reflect` protocol patch adding a `stale_comment_drift_scan()` subroutine that scans code comments for `(path, host)` token pairs and emits `DISCREPANCY: comment-vs-compose-drift` when the comment's pair disagrees with the bind-mount table built from `docker-compose.yml`.

**Steps:**
1. **[PLANNING]** Load `/sc:reflect`; reuse the bind-mount parser from T01.03 if present.
2. **[PLANNING]** Define the comment-token regex: `(/\\S+/?)` adjacent to `on <hostname>` or `on <service>` within a comment line.
3. **[EXECUTION]** Implement the scanner; for each comment match, look up the host's expected paths in the compose-derived table; emit `DISCREPANCY: comment-vs-compose-drift` when they disagree.
4. **[EXECUTION]** Add fixture: `pipeline-script-phase3.1.groovy:48` comment "`/opt/jenkins/artifacts/` on IBCore" against the post-§4.2 compose host path; confirm DISCREPANCY emits.
5. **[VERIFICATION]** Run on the project; review false-positive rate.
6. **[COMPLETION]** Document scan rules, fixture, run log in `TASKLIST_ROOT/artifacts/D-0010/spec.md` and `evidence.md`.

**Acceptance Criteria:**
- `/sc:reflect` skill source contains a named `stale_comment_drift_scan` subroutine emitting `DISCREPANCY: comment-vs-compose-drift` on the documented schema.
- Running the patched protocol against the fixture (`pipeline-script-phase3.1.groovy:48`) emits a DISCREPANCY row referencing the comment text and the compose-derived expected host path.
- Two consecutive runs produce byte-identical DISCREPANCY output (deterministic).
- Scan rules, fixture, and run log recorded in `TASKLIST_ROOT/artifacts/D-0010/spec.md` and `evidence.md`.

**Validation:**
- Manual check: editing the stale comment to the post-migration host path removes the DISCREPANCY on the next run.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc) under `TASKLIST_ROOT/artifacts/D-0010/`.

**Dependencies:** T03.05 (tier decision must be recorded before T03.06 ships)
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Tier conflict: LIGHT vs STANDARD -> resolved to LIGHT by max-score (keyword "comment" matched); confirm/override outcome from T03.05 should be reflected in this row's Tier field before merge.

### T03.07 -- Heredoc context decomposition (ssh/scp prefix detection)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-010 |
| Why | The bug literal `/opt/jenkins/artifacts/` was inside a multi-context heredoc where ssh/scp lines used host paths and inline lines used container paths; C2 detects the prefix context and flags non-tagged literals. Rank 10 of 14 (Priority 0.725). |
| Effort | S |
| Risk | Low |
| Risk Drivers | none |
| Tier | STANDARD |
| Confidence | [███████---] 70% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None Required \| Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0011 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0011/spec.md`
- `TASKLIST_ROOT/artifacts/D-0011/notes.md`
- `TASKLIST_ROOT/artifacts/D-0011/evidence.md`

**Deliverables:**
- `/sc:reflect` protocol patch adding a `heredoc_context_decomposition()` subroutine that detects `ssh `/`scp ` prefixes inside heredoc bodies, classifies each line as host-context or container-context, and emits `HAZARD: heredoc-context-mixed` for any literal path that is ambiguous between the two.

**Steps:**
1. **[PLANNING]** Load `/sc:reflect`; identify heredoc-aware lexing in any existing subroutine or pull in a minimal heredoc lexer.
2. **[PLANNING]** Define the classifier: lines starting with `ssh `, `scp `, or wrapped in `ssh <host> '...'` are host-context for paths in their argument list; everything inside a remote heredoc body is container-context.
3. **[EXECUTION]** Implement the classifier; for each path literal, compare against a `host_paths`/`container_paths` table (from T01.03's compose parser); emit `HAZARD: heredoc-context-mixed` on mismatch.
4. **[EXECUTION]** Add fixture: `pipeline-script-phase3.1.groovy:289-297` heredoc; confirm the SCP target line emits a HAZARD on the host-context path that resolves to a container-only literal.
5. **[VERIFICATION]** Run on the project; sanity-check false positives on heredocs that legitimately mix.
6. **[COMPLETION]** Document classifier, fixture, run log in `TASKLIST_ROOT/artifacts/D-0011/spec.md` and `evidence.md`.

**Acceptance Criteria:**
- `/sc:reflect` skill source contains a named `heredoc_context_decomposition` subroutine emitting `HAZARD: heredoc-context-mixed` on the documented schema.
- Running the patched protocol against the §4.2 fixture emits a HAZARD row for `pipeline-script-phase3.1.groovy:289-297` identifying the host-context line that uses a container-only literal.
- Two consecutive runs produce byte-identical HAZARD output (deterministic).
- Classifier, fixture, and run log recorded in `TASKLIST_ROOT/artifacts/D-0011/spec.md` and `evidence.md`.

**Validation:**
- Manual check: rewriting the SCP line to the post-§4.2 host path removes the HAZARD on the next run.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc) under `TASKLIST_ROOT/artifacts/D-0011/`.

**Dependencies:** T01.03 (reuses the compose-derived host/container path table)
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Phase 5 §"Synergy adjustments" notes {C1, C2, C4} as the codebase-hazard stack with joint effectiveness ~0.98 at ~210 LOC.

### Checkpoint: End of Phase 3

**Purpose:** Confirm Phase 3 lands cleanly and joint confidence on similar-shape regressions reaches the Phase-5-promised ~0.99 with the Tier 2 stack shipped on top of Tier 1 (per Phase 5 line 58-59).

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P03-END.md`

**Verification:**
- All Phase 3 base tasks (T03.01..T03.04, T03.06, T03.07) report Acceptance Criteria 1 satisfied with named subroutines and run logs.
- T03.05 decision is reflected in T03.06 Tier metadata.
- A single `/sc:reflect` run against the bug fixture surfaces findings from all Phase 1, Phase 2, and Phase 3 subroutines without contradiction or duplication.

**Exit Criteria:**
- Tier 2 set merged; T03.05 decision recorded; T03.06 Tier metadata aligned.
- Checkpoint report at `TASKLIST_ROOT/checkpoints/CP-P03-END.md` records Pass.
- Phase 4 (Tier 3 deferred / conditional) is unblocked but not required to ship.
