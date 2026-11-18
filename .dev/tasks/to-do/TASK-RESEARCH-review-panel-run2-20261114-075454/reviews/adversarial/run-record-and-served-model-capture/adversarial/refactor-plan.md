# Refactoring Plan: Merge into Base (Variant 1)

## Overview
- Base: Variant 1 (Proposal A; `variant-1-original.md`)
- Incorporating strengths from: Variant 2 (Proposal B; `variant-2-original.md`) and from the two Round 2 resolutions (`round2-advocate-A.md` section 4, `round2-advocate-B.md` sections 4.1 to 4.3)
- Planned changes: 12
- Risk level: Medium (overall). The merge rewrites A's position, module table, invariants, measurements and objection sections to the hybrid the debate produced; it adds an "open conditions" section from the invariant probe. It adds no conclusion the debate did not reach.
- Governing rule for the executor: every statement in the merged file must be traceable to the base, to Variant 2, to a Round 2 advocate resolution item, to a scored or probed fact in the debate artifacts, or to a code fact the debate verified. Where the two Round 2 advocates did not agree, the merged file states both positions and marks the point OPEN; the executor must not choose. Round 2 content that Advocate A never answered (B's corrections to A's 15 items) is adopted only where B gave a code-verified reason; each such item is marked "adopted from B Round 2, not answered by A".
- Convergence context: 28 of 31 points agreed (90.3%); status BLOCKED_BY_INVARIANTS (13 HIGH UNADDRESSED, `invariant-probe.md`).

## Planned Changes

### Change 1: Replace the one-paragraph position with the hybrid position (from Round 2 resolutions)
- **Source**: `round2-advocate-A.md` section 4 items 1 to 4 and 7 to 8; `round2-advocate-B.md` section 4.3 items 1 to 3
- **Target**: Base section 1 (replace)
- **Rationale**: Base section 1 describes `review-telemetry/2`, `record add`, `rev`, `ext{}`, a script-written memory step and a study switch. The debate withdrew each: `/2` and `record add` by A (A Round 2 N5, item 13), `rev` deferred behind M2, `ext{}` as a leak path, the memory move by both (C-005, X-011; 95% confidence in the scoring matrix). The hybrid: per-agent observation in `<out>/panel/events.jsonl` (`review-run-event/1`) written only by code through `review record ingest` and `review merge --events`; manifest keeps its five-key entry and stage records and gains a CLI-level lock; cross-run record stays `review-telemetry/1` with a `strict` mode at append and one producer `review record export`.
- **Integration point**: Replace the paragraph; keep the closing sentence on hash pointers for INV-H only if restated with `strict`.
- **Risk**: Medium; restructures the base's headline.

### Change 2: Replace the module-consequence table rows for manifest, telemetry, merge, transport and memory (from Round 2)
- **Source**: A Round 2 section 4 items 1, 2, 6, 7, 8, 13; B Round 2 section 4.1 items 1, 2, 6, 7, 8, 13
- **Target**: Base section 2 table (replace rows `cli/review/manifest.py`, `cli/review/telemetry.py`, `cli/swarm/transports/openai_compat.py`, `cli/review/merge_cmd.py` ...; replace the memory row; add rows for the lock helper, `ledger.py` `LedgerError.reason`, `scripts/reflect_shadow_exit.py`)
- **Rationale**: manifest: lock at CLI level in `manifest_cmd.py`, held from `load` to `save`, no `rev`, five-key entry untouched (B N-B7: `publish_files` does two separate load/save pairs at `manifest.py:495, 521-524`). lock helper (agreed, A-005 Hybrid 90%): new `cli/review/lockfile.py`, lazy `import fcntl`, blocking acquire by polling `LOCK_EX | LOCK_NB` to a timeout (`LockTimeout`, `LockUnavailable`), two lock files `<out>/panel/manifest.lock` and `<out>/panel/events.lock`, lock file created on demand with `O_CREAT | O_NOFOLLOW | O_CLOEXEC` and never unlinked (B N-B8), a failed or timed-out lock recorded as `panel_fallback_reason` with the run continuing as legacy (`SKILL.md:338`). telemetry: `validate_record(rec, strict=False)`, `append_record` passes `strict=True`, `load` unchanged. The telemetry-append lock and the append-time one-live-outcome refusal are OPEN (A-009): A (Round 2 items 2 and 7, N6) keeps both, the lock for a check-then-append reason; B (Round 2 4.1 items 2 and 7) ships neither because the refusal breaks `tests/review/test_review_telemetry.py:363-400` and offers a `live_outcome_conflicts` count at `load` (beside `stratum_conflicts`, `telemetry.py:440-443`) instead; A had no turn to answer. merge: `--events PATH` option; `refused` rows from the `except` branch with a closed `reason` enum (`no_valid_block`, `round_order`, `duplicate_reviewer`, `other`); reason from a new optional `LedgerError.reason` set at `ledger.py:116, 121, 154` and defaulting to `other` (adopted from B Round 2, not answered by A); `merged` rows carry `counts` from `findings.parse_block`; action rows only, never cost rows (N2: a replayed round would otherwise double cost). Safety contract (agreed): without `--events` merge is byte-identical to HEAD; a failed events write is a stderr warning with stdout, exit code, ledger and merged report unchanged; merge never reads events. transport: the swarm HTTP hand-off moves to C-07 (A Round 2 item 13). memory: no change in this slot; the move is deferred with its trigger (an observed lost update, or a study that needs the freeze) and its fence reason (`### 6.3` at `SKILL.md:585` is outside the allowed sections, `test_shadow_skill_contract.py:65`). Fix A's own table slip: A's old row said `merge_cmd.py` "none"; that is replaced by the in-process writer (X-004 conceded by A; X-003 conceded by B, and A adopted B's repair with the by-cause restriction).
- **Integration point**: In place of each row's "Change under A" cell; keep the "Left unchanged" column.
- **Risk**: Medium; modifies existing rows.

### Change 3: Add the events-row schema, the two writers and the adapter rules (from A Round 2, with B's corrections)
- **Source**: `round2-advocate-A.md` section 4 items 3 to 5; `round2-advocate-B.md` section 4.1 items 3 to 5
- **Target**: Base, new subsection after section 2 ("The events file, its two writers and the adapter")
- **Rationale**: One schema `review-run-event/1` with closed keys, four kinds (`agent`, `orchestrator_snapshot`, `merged`, `refused`), writer-assigned `seq`, `ts_utc`, `run_id`; no `ext{}`; value rule per B N-B3 (strings without whitespace, at most 80 characters, nested shapes only `usage{}`, `counts{}` with `by_severity{}`, and `served_ids`) with a closed-key check on write and read; adapter: one immutable `agent` row per sidechain keyed by tool-use id, `served_ids` list, `model_observed` only when exactly one id, null with `usage_complete: false` when unreadable, `orchestrator_snapshot` appended on change with last-wins, idempotent re-ingest. The join of a sidechain to a `reviewer_id` is OPEN: A proposed order within role when counts are equal; B proposed an exact match on the Agent call's `description` equal to the reviewer id; B showed the ordinal join misattributes in the tested permuted case (`test_shadow_skill_contract.py:291-299`), and the fault-finder measured that the description equalled a reviewer id in 0 of 12 measured calls (INV-006). State both, state the measured failure, state that `join: null` is the agreed failure value. `record export` (agreed content, A Round 2 item 8 with B 4.1 item 8): the single producer of `reviewer_run`; inputs `--events`, `--resolution` (the `slot`, `model.resolved`, `model.launch` values and the `panel` group source from the resolution JSON), `--cards DIR` (Tier 2) or the `merged` rows (loop), `--doc FILE`; a required `--dir` or `SUPERCLAUDE_REVIEW_TELEMETRY_DIR` with no cwd-relative default (A-006, 90%); `record_id` a hash of `(run_id, step, round, reviewer_id, attempt)` and skip-if-present, so cost projects into `reviewer_run` once; a sidechain with a null join is skipped with a visible reason; an absent or empty events file prints `record_absent` (A-008, 90%; INV-013 notes the aggregator cannot see it, OPEN). The agreed identity rule: `identity_source` is `observed` only when every reviewer and calibrator row has exactly one served id; `export --print-identity` prints it.
- **Integration point**: New subsection; the executor lists the open points as such.
- **Risk**: Medium; additive.

### Change 4: Replace the consistency-with-C-01/C-02/C-03 section's claim of "no disagreement" with the debate-adjusted statements
- **Source**: A Round 2 C1 (refusal writer), X-004; B Round 2 section 1 (X-003 corrected); `invariant-probe.md` INV-016, INV-021
- **Target**: Base section 3 (modify; keep the C-01 and C-02 bullets)
- **Rationale**: A's base claim that an event row with `completion` of `refused` closes C-03 INV-001 is conditional (X-004, conceded). After the merge, the closing statement is: a `refused` row is written in-process by `review merge` only when `--events` is passed and only for the causes the `except` branch sees; how this composes with C-03's quorum refusal (exit 12) is OPEN: the `reason` enum has no `quorum` value, so such a refusal would fall under `other` or not be seen by the `except` branch (INV-016, UNADDRESSED, HIGH). The merged file must not say INV-001 is closed.
- **Integration point**: Rewrite the C-03 bullet.
- **Risk**: Medium; modifies a stated conclusion.

### Change 5: Update the evidence section with the debate's re-verified code facts and corrections
- **Source**: `diff-analysis.md` X-001 to X-012 code checks; A Round 2 N1 to N8; B Round 2 N-B1 to N-B10; `round2.5-fault-finder-raw.md` measurement base
- **Target**: Base section 4 (append items; correct item 20 in subsection 4.4)
- **Rationale**: correct item 20 (the `cycle.py` hit is a docstring, `cycle.py:7`; the lock precedent `issue_watch/record.py:389-417` uses `LOCK_EX | LOCK_NB` and raises `LockHeld`, so it is fail-fast, not a blocking serialiser; X-006, X-012); add the verified facts that bear on the position: a committed manifest takes no second write (`manifest.py:293-296`, `manifest_cmd.py:204`); `merge_round` raises `LedgerError` for round order and duplicate reviewer before the no-valid-block check (`ledger.py:114-121, 150-157`); `append_record` and `load` share `validate_record` (`telemetry.py:289, 411-414`); a pinned test appends three live outcomes for one reviewer record (`tests/review/test_review_telemetry.py:363-400`); the assertion at `test_shadow_skill_contract.py:228` pins the `model_observed:` header text; the aggregator is pinned read-only (`tests/cli/reflect/test_shadow_exit_script.py:313-319`). Each carries the tag the debate gave it. Add the fault-finder's measured facts as a labelled block "Measured in Round 2.5": per-event summation over-count 2.0x to 2.6x; per-message `output_tokens` in the E1 logs total 0.07% to 3.09% of `modelUsage` (none of the 15 sums is within 2% of equality with `modelUsage`); the interactive layout (`subagents/agent-<id>.jsonl`, `.meta.json`); non-Anthropic sidechain `output_tokens` 0; description equalled a reviewer id in 0 of 12 calls.
- **Integration point**: Subsection 4.4 (item 20 corrected) and a new subsection 4.6 (created) for the added facts and the Round 2.5 block.
- **Risk**: Medium; adds evidence and corrects one base item.

### Change 6: Rewrite the invariants section (preserved, endangered) with the hybrid's guards and the probe's open items
- **Source**: Base section 5; B section 5.2; A Round 2 section 4 items 9, 10, 14; `invariant-probe.md`
- **Target**: Base section 5 (modify)
- **Rationale**: INV-H: strengthened only by `strict` and a closed-key event row, with the label rule corrected so tier aliases and fixtures validate (N-B3); INV-F: adapter reached only as `superclaude review record ...`, no new `src/superclaude` string anywhere in the reflect skill directory (the pin counts the literal across the whole directory, `test_shadow_skill_contract.py:77-98`); INV-K: the edit fence; INV-L: a failed or timed-out lock is recorded as `panel_fallback_reason` and the run continues as legacy (`SKILL.md:338`), with the cascade finding INV-007 (stage order) carried as OPEN. Add a row for the one deliberate edit to an existing test (`test_shadow_skill_contract.py:228`) and state that the earlier "tests pass unmodified" statement carries that single exception.
- **Integration point**: Replace both lists.
- **Risk**: Medium.

### Change 7: Replace the measurements section (M1 to M5) with the Round 2 merged set and mark the probe's challenge to M1(c)
- **Source**: A Round 2 item 12; B Round 2 item 12; `invariant-probe.md` INV-009, INV-010, INV-011, INV-005
- **Target**: Base section 6 (modify)
- **Rationale**: Keep M1 to M5 and their thresholds as the advocates agreed (M1 gates `ingest`, `export` `model.observed` and `--print-identity`; M1 includes one interactive transcript; unit tests use a committed synthetic fixture and the 15 real logs are a measurement; M2 gates `rev`; M3 gates the non-reviewer rows; M4 existing tests unmodified except the one assertion; M5 replays A3 through the gate: it flags it and a run with three distinct served ids is not flagged). Add, as a debate finding the advocates had not seen: M1(c) as written compares per-agent `tokens_out` with run-level `modelUsage` and the fault-finder measured 0 of 15 runs within 2 percent on the E1 logs, so the usage field would ship null on that path under the plan's own rule; state it as OPEN (INV-010, HIGH), not as resolved.
- **Integration point**: Replace M1 to M5; append the open point.
- **Risk**: Medium.

### Change 8: Add the build order and the deferred list (from Round 2)
- **Source**: A Round 2 items 13 and 15; B Round 2 items 13 and 15
- **Target**: Base, new section "Build order and deferred items" after the measurements
- **Rationale**: Order (A's items 15 and B's changes; the order is adopted from B Round 2 for PR-1 and PR-2 and is OPEN-adopted, not agreed, because A had no turn to answer): PR-1 (lock helper, manifest lock in `manifest_cmd.py`, `strict` at append, `LedgerError.reason`, tests; whether PR-1 also carries the telemetry-append lock and the append-time live-outcome refusal (A) or the `live_outcome_conflicts` count at `load` (B) is OPEN, A-009); PR-2 (events writer and schema, `merge --events`, loop prompt argument, `record summary` on `merged`/`refused` rows); PR-3 after M1 passes (`record ingest`, `record export`, SKILL steps 2, 9 and 10 as A's resolution lists them with the single test edit at `:228`, the aggregator gate, M5). B additionally lists a step 3 edit (name each reviewer's Agent call with its reviewer id) that exists only to support the description join; that edit and the join are OPEN (Change 3). The relative order of SKILL steps 9 and 10 (identity copied at step 9, `ingest` at step 10) is OPEN (INV-017, HIGH). Deferred with reasons: `/2` and non-reviewer telemetry kinds, `record add`, `rev`, `ext{}`, the swarm transport hand-off (C-07), the memory writer move and study switch, PR-module producer (C-10), rf-qa (C-11), E2's per-design counters and any exchange (C-12).
- **Integration point**: New section.
- **Risk**: Low (additive).

### Change 9: Add the identity-gate section (from B)
- **Source**: Variant 2 section 2 (`reflect_shadow_exit.py` row), Variant 2 M4, B Round 2 item 10, N-B6
- **Target**: Base, new subsection in section 2 or 4 ("Identity gate")
- **Rationale**: Gate in `scripts/reflect_shadow_exit.py` recomputes `identity_source` and `identity_mismatch_suspected` from `<run>/panel/events.jsonl`, read-only, no lock helper, a missing file maps to `requested-pinned`; a replay of run A3 must flag `calibrator_diversity: full` over a collapsed panel and a run with three distinct served ids must not be flagged. State as OPEN what the probe found unaddressed: what the gate does with a printed finding (fail, line or count), the missing-events third state (INV-013), the vacuous mismatch when `model_requested` is None as on A3 (INV-020), and the class-versus-id definition of collapse (INV-015).
- **Integration point**: New subsection.
- **Risk**: Medium.

### Change 10: Rewrite the PR-review and rf-qa effect section (module-neutral claim narrowed)
- **Source**: Base section 7; Variant 2 section 6; A Round 2 item 13
- **Target**: Base section 7 (modify)
- **Rationale**: The record row is module-neutral and that is all this slot claims. A cross-run all-agents figure is a crawl of events files in both designs (A withdrew the contrary claim, A Round 2 "Round 1 positions I have changed" item 10; the crawl is stated in resolution item 11). PR reviewers served by gateway models need the adapter's served id; B's reviewer-only fit with no schema change is recorded as a position that the debate did not adopt for non-reviewer agents.
- **Integration point**: Replace paragraphs.
- **Risk**: Low.

### Change 11: Replace the strongest objection and answer with the objection and answer as the debate left them; extend the concessions
- **Source**: Base section 8; Variant 2 section 7; A Round 2 section 1 (C3, C5); B Round 2 section 1
- **Target**: Base section 8 (modify) and the closing "What A concedes" paragraph (extend)
- **Rationale**: Part 1 of the base answer (the B route runs into three pinned behaviours) is narrowed: a finished sidechain's usage hashes stably and `_recount` reads only `completion`, so the reviewer-attempt route is workable for a reviewer's final usage (A withdrew objection 1a for that case, X-001 winner Variant 2 at 85%); what stands is that non-reviewer agents and the orchestrator have no attempt row and a committed manifest takes no second write. Concessions list extended with what the advocates conceded: the adapter is an unverified dependency (A Round 1 concession 6; A-001 to A-003); after B's repairs B's change is not smaller than A's (A Round 2 section 2 point 1; B conceded this and countered that A's resolution is not small either, so size is not the differentiator). Part 4 of the base answer (the adapter dependency is shared) is kept. The objection paragraph's references to the `/2` bump and the memory writer are removed because the hybrid dropped both. Probe findings (for example INV-009, per-event usage double counting) are not concessions; they appear only in Change 12.
- **Integration point**: Rewrite part 1 of the answer, adjust the objection paragraph, append concessions.
- **Risk**: Medium.

### Change 12: Add a section "Open conditions from the invariant probe and unresolved points"
- **Source**: `invariant-probe.md` (22 findings), `debate-transcript.md` Convergence Assessment, A-009
- **Target**: Base, new final section
- **Rationale**: Transparency: 13 HIGH UNADDRESSED (INV-001, 002, 005, 006, 009, 010, 011, 013, 016, 017, 020, 021, 022), 7 MEDIUM UNADDRESSED (INV-003, 004, 007, 008, 012, 015, 018), 2 LOW ADDRESSED (INV-014, INV-019); points unresolved between the advocates: C-001 and X-006 (label splits, substance converged), A-009 (the telemetry-append lock: A yes for a check-then-append reason, B no because that reason depends on an append-time one-live-outcome refusal that breaks `tests/review/test_review_telemetry.py:363-400`); items B corrected that A never answered (telemetry lock dropped, append-time one-live-outcome refusal not shipped, join by `description`, `strict` label rule, `LedgerError.reason`, lock placement in `manifest_cmd.py`, the `:228` assertion edit, build order). One line per item with its severity and the INV ID; no resolution is invented.
- **Integration point**: Final section.
- **Risk**: Low (additive).

## Base Weaknesses Addressed

| Base weakness | Better variant / source | Fix approach |
|---------------|-------------------------|--------------|
| `merge_cmd.py` "none" leaves refusal rows without a writer (X-004) | Variant 2 (in-process writer in `merge`) with A's restriction by cause | Change 2 and Change 4 |
| No location, flag or caller for the loop's events (X-010) | Variant 2 (loop path rides on `merge`) | Change 2: `--events` |
| Memory move outside the edit fence (X-011) | Variant 2 | Change 2: defer with trigger |
| Fail-fast lock cited as a serialiser (X-006, A-005); manifest lock placement unstated | Variant 2 for the manifest-lock placement in `manifest_cmd.py` (N-B7); both advocates for the blocking, lazily imported helper | Change 2 |
| No lock on `append_record` (C-004) | Not decided: A keeps a telemetry-append lock, B dropped it (A-009) | Not addressed; carried as OPEN in Change 2 and Change 12 |
| `/2` bump as the way to get value checks (X-007) | Variant 2 (`strict` keyword) | Change 1 and 2 |
| Identity lines left hand-written "in a later change" (C-006) | Variant 2 | Change 2 and Change 9 |
| `ext{}` unguarded leak path | Both (A conceded) | Dropped in Change 1 |
| Cost "lives only on events" versus `reviewer_run` requiring a `cost` group (B R1 weakness 4) | A Round 2 C4 | Change 3 (`record export` paragraph): `export` projects cost into `reviewer_run`; deterministic ids |

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|------------|-------------------|---------------------------|
| C-001, C-002, X-002, X-009 | Manifest attempt entries carry `usage`/`model`; `agents[]` on `published`/`failed` stage records | Withdrawn by Advocate B in Round 2: no code path for `failed`/`--publish-from` (`manifest.py:389-397`, `manifest_cmd.py:174-199`); a committed manifest takes no second write (`manifest.py:293-296`, `manifest_cmd.py:204`); the observation would live in two stores. C-002 and X-002: 95% for the base. |
| C-003, X-008 | Two producers of `reviewer_run` (merge step and the published commit) and a `review telemetry from-manifest` step | Withdrawn by B in Round 2: the manifest holds none of `slot`, `task`, `output`, `context`; one producer `record export`. |
| C-007 | Reviewer-only cost from `reviewer_run` plus a manifest-reading `manifest summary` | Both labelled bases derive from one per-run events file (85%); the cross-run all-agents figure is a crawl in both designs. |
| X-009 | M1 compared with the extractor's run-level `out_tokens` within 1 percent | B conceded it could fail by construction; replaced by the merged M1 (note INV-010 remains OPEN). |
| A-004 | Order-bound `collected` and `calibrated` attempt calls as the carrier | `ingest` has no ordering precondition; `calibrated` has no call site (`SKILL.md:344`). |
| A-009 | Telemetry-append lock (A) and its absence (B) | Not decided by the debate; carried as OPEN (Change 12). |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|----------|------|------------------|----------|
| 1 | Medium | Headline position inconsistent with sections 2 to 8 | Revert to base section 1 |
| 2 | Medium | Module table contradicts the new subsection | Revert rows to base |
| 3 | Medium | Open join method presented as decided | Mark OPEN, remove any choice |
| 4 | Medium | INV-001 stated closed | Restore "conditional" wording |
| 5 | Medium | Misquoted line numbers | Drop the unverified item, keep tags |
| 6 | Medium | Test-edit exception omitted | Re-add the `:228` row |
| 7 | Medium | M1(c) challenge lost | Re-append the OPEN note |
| 8, 10, 12 | Low | Additive | Remove the section |
| 9 | Medium | Gate presented as closing A3 | Keep the INV-020 OPEN note |
| 11 | Medium | Objection answer overstated | Restore the narrowed answer |

## Review Status
- [x] Auto-approved (default)
- [ ] User-approved (--interactive)
- Analytical review: `plan-review.md` (29 statements verified OK; 9 defects and 5 missing items found, all applied to this plan before execution: merge `reason` enum, size-concession direction, probe finding listed as concession, SKILL step 3 and the telemetry lock marked OPEN, weakness-table rows, item 20 location, `record export` and lock-helper content added, attribution of X-003)
- Approved by: auto
- Approval timestamp: 2026-11-14T16:53:33Z
