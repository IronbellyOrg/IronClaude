# Adjudication result: slot C-08 (run-record-and-served-model-capture)

Run: `/sc:adversarial --compare proposal-a.md,proposal-b.md --depth standard --focus correctness,risk,test-coverage` (Mode A, no `--merge`, no `--interactive`). Orchestrated by the debate-orchestrator; the diff analyst, advocates, fault-finder, scorers, plan reviewer and merge-executor were separate agents. Rounds: Round 1 (parallel), Round 2 (A then B), Round 2.5 invariant probe; no Round 3 at standard depth.

## Winner

**Variant 1 (Proposal A) as the base, merged as the hybrid the debate itself produced.** The debate's own base selection (`base-selection.md`): "Selected Base: Variant 1 (Proposal A; default model, default persona)". The merged resolution is `merged-run-record-and-served-model-capture.md`. Neither proposal won as written. After Round 2 both advocates named the same winner on 28 of 31 diff points, and in the Round 2 scoring matrix Variant 1 won 8 points, Variant 2 won 4, 13 went to the hybrid, 5 to neither and 1 (A-009) is unresolved.

The hybrid the debate produced (merged file sections 1 and 2): per-agent observation, refused actions and the orchestrator live in one append-only per-run `<out>/panel/events.jsonl` (`review-run-event/1`, closed keys), written only by code through `review record ingest` (transcript adapter, idempotent) and `review merge --events`; the manifest keeps its five-key entry and stage records and gains only a CLI-level blocking, timed lock (no `rev`, no `usage`/`model`/`agents[]`); the cross-run record stays `review-telemetry/1` with a `strict` mode at append (no `/2`) and one producer `review record export`; the memory writer, `### 6.3`, `### 9.1`, contract 1.8.0 and `derive_verdict` are untouched; an identity gate in `scripts/reflect_shadow_exit.py` reads events read-only.

## Rationale (quoted from the debate's base selection and scores)

- Quantitative layer: Variant 1 0.9605, Variant 2 0.9579 (requirement coverage 0.9667 each; internal consistency V1 0.9487, V2 0.8718; specificity 1.0 each; dependency completeness 1.0 each; section coverage V1 0.8889, V2 1.0).
- Qualitative layer (30 criteria, two position-bias passes, 8 of 60 pairs re-evaluated): Variant 1 25/30 = 0.8333, Variant 2 25/30 = 0.8333. Correctness V1 2/5, V2 1/5; Completeness 4/5 each; Structure 5/5 each; Clarity V1 4/5, V2 5/5; Risk Coverage 5/5 each; Invariant & Edge Case 5/5 each. Both are eligible under the edge-case floor.
- Combined: Variant 1 0.8969, Variant 2 0.8956. "Margin: 0.0013 (0.13%, below the 5% threshold)". "Tiebreaker applied: Yes, level 1 (debate performance)". Variant 1 won 8 diff points against 4 for Variant 2; the level 2 correctness count (V1 2, V2 1) points the same way.
- The debate's stated reason: both advocates named Proposal A's per-run events file as the observation store ("A is the right base for the observation store, the refusal rows and the loop path", Advocate B, Round 2), because a committed manifest takes no second write (`manifest.py:293-296`, `manifest_cmd.py:204`), non-reviewer agents and the orchestrator have no attempt row, and rows written during the run survive a kill. Proposal B contributed the `strict` keyword, the edit-fence analysis (no memory move), the in-process merge writer restricted by cause, the A3 identity-gate replay and the shadow fallback text. Variant 1's Correctness losses are three code-checked defects (refusal rows have no writer in its own module table, no location for the loop's events, a `cycle.py` docstring hit listed as a lock user); Variant 2's are five (`agents[]` has no code path, producer placed after the call that raises, append-time type check has no mechanism in `load`, no component for the Tier 2 `reviewer_run` producer, a run-level token check that can fail by construction); Variant 2 also leaves OQ-19 unanswered.
- Convergence: 28 of 31 diff points agreed (0.9032) against an 80% threshold. Status BLOCKED_BY_INVARIANTS (see below).

## Conditions under which the winner holds (all stated in `merged-run-record-and-served-model-capture.md`)

1. Every served-id and usage field depends on the transcript adapter, which is an unverified dependency in both papers. Measurement M1 gates `ingest`, `export` `model.observed` and `--print-identity`: replay on the 15 E1 logs plus one interactive transcript; if the first clauses fail the SKILL steps and gate do not ship and `identity_source` stays `requested-pinned`; unreadable values are null and nothing is estimated.
2. M1(c) as written (per-agent `tokens_out` plus orchestrator snapshot equals run-level `modelUsage` within 2 percent in 13 of 15 runs) was measured by the fault-finder at 0 of 15 on the E1 logs, so under the plan's own rule the `usage` field would ship null on that path. This is OPEN (INV-010), not resolved.
3. The non-reviewer and orchestrator rows are gated by M3 (reviewer-only tokens within 10 percent of all-agents tokens in at least 12 of 15 runs would remove them); `rev` is added only if M2 shows a lost update that survives with every writer locked.
4. Refusal rows exist only when `review merge` is run with `--events`, only for the causes its `except` branch sees (enum `no_valid_block`, `round_order`, `duplicate_reviewer`, `other`), as action rows, never cost rows. The merged file does not claim that C-03 INV-001 is closed.
5. The memory writer move and study switch are deferred; trigger: an observed lost update, or a study that needs the freeze. The reason is the edit fence (`### 6.3` at `SKILL.md:585` is outside the allowed sections, `test_shadow_skill_contract.py:65`).
6. All SKILL edits stay inside `### 4.3a`, add no `src/superclaude` string, and carry one deliberate edit to an existing test (the assertion at `tests/cli/reflect/test_shadow_skill_contract.py:228`).
7. Points the two advocates did not settle and the merged file marks OPEN, with each side stated: the join of a sidechain to a `reviewer_id` (A: order within role when counts are equal; B: Agent-call `description` equal to the reviewer id; `join: null` is the agreed failure value); the telemetry-append lock and the append-time one-live-outcome refusal (A-009: A keeps both, B ships neither because the refusal breaks `tests/review/test_review_telemetry.py:363-400` and offers a `live_outcome_conflicts` count at `load`); the relative order of SKILL steps 9 and 10 and the step 3 reviewer-id naming edit; the build order PR-1, PR-2, PR-3 (adopted from B Round 2 for PR-1 and PR-2, not answered by A).
8. Advocate B's Round 2 corrections to A's 15-item resolution (telemetry lock dropped, append-time refusal not shipped, join by `description`, `strict` label rule, `LedgerError.reason`, lock placement in `manifest_cmd.py`, the `:228` assertion edit, build order) came after A's last turn. The merge adopts them where B gave a code-verified reason and marks each "adopted from B Round 2, not answered by A".
9. The 28 of 31 count is by label: C-001 and X-006 are label splits with converged substance and are counted as not agreed; A-009 is a substantive split.
10. Merge-executor judgments recorded in `merge-log.md` (none changes a plan decision): the added section is numbered 6A to keep the base's section numbers; OQ-19 is narrowed to the Tier 2 reflect path with the spec-loop header line stated as not changed; the C-01 and C-02 bullets lost wording the hybrid's closed key list no longer supports.

## Invariants the debate left unaddressed

From `adversarial/invariant-probe.md` and the return contract: 22 findings, 2 ADDRESSED (INV-014 LOW, INV-019 LOW), 20 UNADDRESSED (13 HIGH, 7 MEDIUM, 0 LOW). Convergence was blocked by the 13 HIGH items; standard depth has no Round 3, so none was debated.

| ID | Severity | Category | What is unaddressed |
|----|----------|----------|---------------------|
| INV-001 | HIGH | state_variables | A torn final line from a killed writer is not handled; the file is append-only and never rewritten, so one torn or glued line breaks `export`, `summary` and the gate for that run. |
| INV-002 | HIGH | state_variables | `ingest` is called idempotent because "a finished sidechain's usage is final", but a row for an unfinished sidechain is frozen by skip-if-present and by `export`'s deterministic `record_id` plus `INSERT OR IGNORE`. |
| INV-005 | HIGH | guard_conditions | The interactive layout stores sub-agent messages in separate `subagents/agent-<id>.jsonl` files with `parent_tool_use_id` null and the join key in `.meta.json`; the adapter as specified (E1 grouping, one `--transcript` file) finds zero sidechains there. |
| INV-006 | HIGH | guard_conditions | Neither join works as written: the Agent-call `description` equalled a reviewer id in 0 of 12 measured calls and is orchestrator-typed; the ordinal join misattributes in the tested permuted case. |
| INV-009 | HIGH | count_divergence | Per-event usage summation over-counts 2.0x to 2.6x (one event per content block repeats the message usage); dedup by `message.id` is not specified and a fixture using the same sum cannot catch it. |
| INV-010 | HIGH | count_divergence | M1(c) measured at 0 of 15 runs within 2 percent on the E1 logs; there is no `modelUsage` in an interactive session. |
| INV-011 | HIGH | count_divergence | A non-Anthropic sidechain reports `output_tokens` 0 and no cache key as readable values, so `usage_complete` would be true for a zero-cost record. |
| INV-013 | HIGH | collection_boundaries | `record_absent` is printed by `export` only; a skipped `ingest` is invisible to the aggregator and passes as `requested-pinned`; no existing E1 run has `panel/events.jsonl`, so a hard failure would fail the corpus. |
| INV-016 | HIGH | interaction_effects | The `refused` row composes with C-03's quorum refusal (exit 12) only if raised as `LedgerError` inside the `try`; the enum has no `quorum` value; `merge_cmd.py` writes the report before `led.save`, so a `merged` row could precede a refused or unsaved merge. |
| INV-017 | HIGH | interaction_effects | SKILL step 9 (identity) precedes step 10 (`ingest`); at step 9 no `events.jsonl` exists, so the contract would get the old value; the copy is an LLM transcription. |
| INV-020 | HIGH | sufficiency_challenge | The hybrid alone does not close the A3 identity gap: `model_requested` is None on A3 so the mismatch is vacuous and the output can read `observed` with no mismatch; the stable `calibrator_diversity` stays orchestrator-computed under contract 1.8.0; no code reads `identity_source` today; the gate's effect (fail, print, count) is unspecified. |
| INV-021 | HIGH | sufficiency_challenge | The hybrid alone does not close C-03 INV-001: the row exists only with `--events`, only for `LedgerError`, a failed events write is a stderr warning, the loop never calls `export`, and nothing consumes `refused` rows. |
| INV-022 | HIGH | sufficiency_challenge | The hybrid alone does not close cost under-reporting: `cost_per_confirmed_tp` stays reviewer-only (`telemetry.py:371`); adapter readings are wrong on the measured formats (INV-009, INV-010, INV-011); the orchestrator snapshot is 0 or stale. |
| INV-003 | MEDIUM | state_variables | The last `orchestrator_snapshot` by events-file order can be a stale one; no monotone key. |
| INV-004 | MEDIUM | state_variables | One run is assumed to be one transcript file; resumes and restarts split sidechains across files and a partial ingest looks complete. |
| INV-007 | MEDIUM | guard_conditions | `init` has no manifest yet for the lock; one `lock_timeout` cascades through stage order and the aggregator reports the run `incomplete`; no lock-acquisition order is stated. |
| INV-008 | MEDIUM | guard_conditions | What `export` does when `strict` refuses one record is unstated; the 80-character rule passes an underscore-joined sentence; `strict` also changes the existing `telemetry append` CLI. |
| INV-012 | MEDIUM | count_divergence | The events-side `attempt` and the manifest `attempt_id` are numbered independently; a retried reviewer yields two `reviewer_run` records and `model_scores` counts two runs. |
| INV-015 | MEDIUM | collection_boundaries | A served id is not normalised (`qwen3.8-max` against `Qwen3.8-max`) and "collapse" as id-equality or class-equality is unwritten. |
| INV-018 | MEDIUM | interaction_effects | Deterministic `record_id` makes `export` idempotent per id only; a record from another route under a different id is counted twice; the append-time one-live-outcome refusal breaks a pinned test. |

ADDRESSED, LOW: INV-014 (a sidechain with two served ids: `served_ids` list and null `model_observed`), INV-019 (SKILL edits, fence, line-count pin and aggregator read-only pin do not collide).

Return contract `unaddressed_invariants` (HIGH only): INV-001, INV-002, INV-005, INV-006, INV-009, INV-010, INV-011, INV-013, INV-016, INV-017, INV-020, INV-021, INV-022.

## Return contract

Status `partial`; convergence score 0.90 (28 of 31 = 0.9032); base variant `variant-1 (Proposal A; default model, default persona)`; unresolved conflicts 3 (C-001, X-006, A-009); fallback mode false; failure stage null; invocation method `task-agent`. Merge: 12 of 12 changes applied, post-merge validation PASS.

## Artifact paths

Output folder: `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/reviews/adversarial/run-record-and-served-model-capture/`

- Merged file: `.../run-record-and-served-model-capture/merged-run-record-and-served-model-capture.md`
- Adversarial artifacts (`.../run-record-and-served-model-capture/adversarial/`): `variant-1-original.md`, `variant-2-original.md`, `diff-analysis.md`, `debate-transcript.md`, `invariant-probe.md`, `base-selection.md`, `refactor-plan.md`, `merge-log.md`, `return-contract.yaml`
- Supporting files in the same folder: `round1-advocate-A.md`, `round1-advocate-B.md`, `round2-advocate-A.md`, `round2-advocate-B.md`, `round2.5-fault-finder-raw.md`, `score-pass1.md`, `score-pass2.md`, `score-reeval.md`, `quant-score.py`, `quant-score-output.json`, `plan-review.md`
