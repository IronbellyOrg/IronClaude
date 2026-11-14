# Round 2 advocate for Variant 1 (Proposal A), slot C-08 run-record-and-served-model-capture

Status: Complete
Code state: HEAD 50d4d2b9d on `ironbelly/shadow-runs`. Paths repo-relative. Tags: [RE-READ] = read at HEAD in this round; [R1] = carried from a Round 1 file or the diff analysis, not re-read; [UNVERIFIED] = not re-derived.
Label meaning used in section 6 (made explicit because my Round 1 mixed two senses): ACCEPT = the assumption is sound as the design needs it; REJECT = it is unsound and must not be relied on; QUALIFY = sound only under a stated condition.

## 1. Response to criticisms of Variant 1 in B's Round 1

B's Round 1 raises ten criticisms of Variant 1 (its section 4) and four repairs to its own design (its section 5). Each is answered below. "Conceded" means the evidence forces it; "countered" means I hold the position and give the evidence.

**C1. X-004: the refusal row has no writer in A's design (conceded, and B's repair adopted with one restriction).**
The refusal is raised inside `merge_round` at `ledger.py:150-157` and surfaced as a `ClickException` at `merge_cmd.py:111-112` [RE-READ]. A's own table said `merge_cmd.py` changes "none", so "INV-001 closed" depended on the orchestrator calling the CLI after a failed merge. Fix, adopted from B: `review merge` writes the row in-process from its `except` branch. The restriction B's repair lacks: `LedgerError` is also raised for a replayed or out-of-order round (`ledger.py:114-118`) and a duplicate reviewer id (`:119-121`), both before the no-valid-block check [RE-READ]. B's text ("catch `LedgerError`, re-derive `block_ok`, write the reviewer records, re-raise") would therefore write a second set of reviewer-cost records every time the orchestrator replays a merge, which counts spend twice. Under the resolution merge writes an action row with a closed `reason` (`no_valid_block`, `round_order`, `duplicate_reviewer`, `other`), derived locally, and never writes reviewer cost rows (those come only from the transcript adapter).

**C2. X-010: no location, flag or caller for the spec-review loop (conceded).**
`review merge --out` is a file path (`merge_cmd.py:57-63` [RE-READ]) and the loop prompt names no panel directory. Resolution: an optional `review merge --events PATH`; the loop prompt passes it; without the flag merge is byte-identical to today.

**C3. X-001: A's objection 1 describes B's route incompletely (partly conceded).**
Three things I got wrong or overstated in Round 1, each checked in code:
- (1a) A finished sidechain's usage is final, so a payload recorded once with the attempt hashes stably; the `Conflict` at `manifest.py:355-368` only bites on a re-read, which B does not do. Withdrawn for a reviewer's final usage.
- `_recount` reads only the `completion` of `collected` entries (`manifest.py:269-274` [RE-READ]), so extra stored keys on an entry cannot change `reviewers_complete`. My Round 1 line "a wrong or late reading can never change a stage decision" is true of the file separation but is not an argument against B's reviewer route.
- A grep of `tests/` for the whole-entry dict or `payload_sha256` finds no assertion on entry shape; the only attempt-structure pin is `superseded_by` at `tests/review/test_review_manifest.py:169` [RE-READ]. So extending an entry is lower-risk to existing tests than I implied.
Still standing: (1c) non-reviewer agents have no attempt row (`manifest.py:53`), and the orchestrator's own usage is not final (it grows with every call), so it cannot ride in any hashed payload. B's route is workable for a reviewer's `collected` usage; it is not a complete carrier. I no longer claim otherwise.

**C4. "Cost lives only on event rows" versus `reviewer_run` requiring a `cost` group (countered in part, conceded in part).**
`validate_record` requires every key of all six groups, `cost` included (`telemetry.py:204-225`; group list `:40-81` [RE-READ]), so A's `export` does write cost into a second store. The sentence in my paper was loose. Two answers. (i) B's repaired design copies cost into `reviewer_run` as well (manifest to a `from-manifest` step), so "two places" is symmetrical; the only difference is that A's projection has one source file. (ii) D-17's fan-out came from outcomes joined to cost; `reviewer_run` is one record per reviewer run, so a one-way projection does not recreate it. The real hazard is idempotence: `new_record_id` is `uuid4` (`telemetry.py:118`) and `load` de-duplicates by primary key with `INSERT OR IGNORE` (`:417-424`), so a re-run of any producer with fresh ids doubles spend. The resolution requires deterministic ids and a skip-if-present check under the lock; this applies to B's producers equally.

**C5. Large surface, unmeasured payoff (partly conceded).**
After B's own repairs B's change list is not smaller (section 2). I cut my surface instead of arguing: no `/2`, no `record add`, no `rev`, no `ext{}`, no swarm transport change, no memory move, and the non-reviewer rows are gated behind M3 (section 4).

**C6. X-011: the memory move against the fence (conceded in Round 1, unchanged).** `### 6.3` is at `SKILL.md:585` and the fence allows only `### 3.1`, `### 4.3a`, `### 5.4`, `### 9.2` (`test_shadow_skill_contract.py:65`) [RE-READ]. The resolution leaves memory alone.

**C7. C-006: A defers replacing the orchestrator's identity lines (conceded).** Step 2 (`model_observed:` header, `SKILL.md:341`) and step 9 (`identity_source`, `:348`) both sit inside `### 4.3a`, which the fence allows [RE-READ]. There was no fence reason to defer; the resolution edits them in this change.

**C8. `ext{<module>}` is an unguarded leak path (conceded).** The resolution drops `ext{}`; event rows have closed keys only, with a field-level type test.

**C9. X-012 small slips (conceded).** `issue_watch/cycle.py:7` is a docstring ("Nothing here touches `fcntl`..."), not a lock user; the only code lock in `cli/` is `issue_watch/record.py:389-417` [RE-READ]. B-8's "names" claim holds only through "or". Neither changes a design point.

**C10. X-006 / A-005 apply to A as much as to B (conceded).** The precedent lock is `LOCK_EX | LOCK_NB` and raises `LockHeld` on contention (`record.py:403-405`), needs a pre-existing lock file (`:393-395`) and imports `fcntl` lazily (`:389`) [RE-READ]. A said "exclusive flock" and expected 400 valid lines from 8 writers, which a fail-fast lock cannot give. The resolution specifies one shared helper: lazy import, blocking acquire with a timeout, lock file created on demand.

**B's four proposed repairs, assessed against code**

| Repair | Verdict | Evidence |
|---|---|---|
| Write-once unhashed top-level `agents` object | Works only for a single first call of `published` or `failed`; fails as the carrier for the orchestrator tail and for late rows | `advance_stage` returns False on an identical digest before writing anything (`manifest.py:293-296`); `advance_cmd` calls `save` only when `changed` (`manifest_cmd.py:204`); so a second `published` call cannot add `agents` to an already committed manifest, and a new mutating command on a committed manifest would be needed. A first-call write also needs `fail()` (`manifest.py:389-397`) to take a new argument, a change in the `--stage failed` branch (`manifest_cmd.py:174-175`) and one in the `--publish-from` branch (`:184-199`). `validate` accepts unknown top-level keys (`manifest.py:192-253`), so no schema bump is needed [all RE-READ] |
| `strict` keyword on `validate_record` | Sound; adopted | Exactly two call sites in `src/`: `telemetry.py:289` (append) and `:411` (load) [RE-READ via grep]. `append_record` passes `strict=True`; `load` keeps today's report-and-skip. This removes my reason for `review-telemetry/2` |
| `review telemetry from-manifest` step | Right idea, wrong name and input | A `reviewer_run` needs `slot`, `task`, `output`, `context` groups as well as `model` and `cost` (`telemetry.py:40-81, 204-225`); the manifest holds none of them (stage records `manifest.py:317-326`, entries `:348-354`). The producer must also read `panel/resolution.json`, the cards and the reviewed document. That is `record export` with a different input list |
| Catch `LedgerError` at `merge_cmd.py:111-112` | Sound only if restricted to the no-valid-block cause | See C1 |

## 2. Updated assessment of Variant 2

**What B's Round 1 changed.** B conceded X-002, X-003, X-007, X-008 and X-009 in its own words, accepted that the orchestrator tail and the killed-run residual are "where A is strongest", and landed on "B's base with four repairs, A's stream held behind A's own M3". I read that as a real move toward a hybrid, and most of it survives my re-check.

**Where B is right, and the resolution takes it.**
- The fence analysis (`### 6.3` outside the allowed sections), so no memory move.
- A producer inside `review merge` for the spec-review loop, because the loop has no manifest and merge is the one code path every loop round passes through.
- A lock inside `append_record`, and the `strict` keyword (verified sound, section 1).
- The identity gate in `scripts/reflect_shadow_exit.py`, with an A3 replay; that script reads only `reviewers_resolved` and `reviewers_complete` today (`reflect_shadow_exit.py:244-245` [RE-READ]), so the gate is new code in either design.
- The shadow-mode fallback text for a refused write (`SKILL.md:338`: a step that cannot run records `panel_fallback_reason` and the run continues as legacy).

**Where B's design is weaker than its Round 1 admits.**
1. *After its repairs it is not the smaller change.* B must edit `manifest.py` (entry shape, `fail()`, the `published` path), `manifest_cmd.py` (three branches), `telemetry.py` (strict, lock, one-live-outcome check), add `telemetry_cmd.py` (`from-manifest`), `merge_cmd.py` (restricted producer) and a new adapter module, plus the new unhashed-field rules and a `manifest summary` command. A's repaired set is: a new `record` module and command (adapter, export, summary), `merge_cmd.py` (restricted row writer), `telemetry.py` (strict, lock, check) and a lock helper used by the manifest. The difference is that B's edits land in the stage state machine and A's land in a new file. Risk-wise that is the opposite of "fewest pinned behaviours changed".
2. *Its `agents[]` repair cannot carry what it was meant to carry.* Section 1: a committed manifest does not accept a second write through the stage path (`manifest.py:293-296`, `manifest_cmd.py:204`), so the orchestrator tail after `published` is out by construction, not just "labelled through publish".
3. *The call-order dependence is real for reviewers' usage, not only for `dispatched`.* Reviewer usage rides on `manifest advance --stage collected --reviewer-id ...` (`SKILL.md:342` [RE-READ]), which is a per-reviewer orchestrator call that must precede `advance collected` (`manifest.py:371`). R15 says 0 of 29 `collected` attempts were missing, so this is evidence for B, but 9 of 29 `dispatched` rows were refused for exactly this ordering, and a calibrator has no call site at all (`SKILL.md:344`, step 5: "Advance `calibrated`") [RE-READ; R15 figures UNVERIFIED]. A single idempotent `record ingest` has no ordering precondition and can run last.
4. *The kill residual is unfixed.* A run killed before `published`/`failed` leaves nothing in B; an events file keeps every row already written.
5. *Its producer set is still two.* The merge-time producer and the published-commit producer remain two code paths writing the same record shape; the resolution has one producer (`export`) and moves only capture into merge.

**Where A remains the weaker side after Round 2.** The adapter is a shared unverified dependency (A-001..A-003); my events file adds a new module, a new schema id and a new command family that B avoids; and the effort is larger than "extend a dict" for the reviewer-only part. If the owner decides that only reviewer and calibrator facts matter and the orchestrator share is not wanted, B's attempt-entry route is the smaller change for that subset, and M3 is the measurement that decides it.

**Net.** B is the better base for the telemetry side (strict, lock, check), the merge capture, the fence and the identity gate. A is the better base for the per-run observation store: one file for every agent role, no call-order precondition, no write to a committed manifest, kill-survival, refusals as first-class rows, and the loop path through the same format.

## 3. New evidence not in Round 1

All items re-read at HEAD this round unless tagged.

**N1. A committed manifest cannot take a second write through the stage path.** `advance_stage` returns False on an identical digest before it touches the manifest (`manifest.py:293-296`), and `advance_cmd` saves only when `changed` (`manifest_cmd.py:204`). The shadow SKILL calls `published` once, with no payload, to hash the files the legacy writers produced (`SKILL.md:349`; `manifest_cmd.py:200-203`). So any B variant of "agents on `published`" is a one-shot at that call; a tail read afterwards needs a new mutating subcommand on a committed manifest, which contradicts the rule B itself quotes ("a committed manifest should not change").

**N2. B's catch-all repair double-counts on replay.** `merge_round` raises `LedgerError` for round order (`ledger.py:114-118`) and duplicate reviewer id (`:119-121`) before the block check (`:150-157`). A producer in the `except` branch that writes reviewer-cost records for every `LedgerError` therefore writes them again for a replayed round. The restriction (action rows only, closed `reason`, cost from the adapter alone) is in the resolution.

**N3. Sidechain usage is final; orchestrator usage is not.** Hash stability (B's argument) holds for a finished sidechain and fails for the orchestrator session, so the two must be different row kinds: an immutable `agent` row per sidechain, and an `orchestrator_snapshot` row of which the last one wins at read time. This is a design rule neither paper had.

**N4. Entry extension is lower-risk to tests than I said, higher-risk to behaviour than B says.** No test asserts the entry dict or `payload_sha256` (grep of `tests/`; only `superseded_by` at `tests/review/test_review_manifest.py:169`), and `validate` ignores entry contents (`manifest.py:251-252`). But every future reader of `attempts` (the shadow shortfall at `reflect_shadow_exit.py:244-245` reads the derived counters, not entries) would see a shape that is no longer five keys. This is a minor point that favours B on tests and A on blast radius.

**N5. `strict` removes the only reason for `/2`.** With two call sites (`telemetry.py:289, 411`), a `strict` flag on append gives value checks without invalidating legacy lines at load. Non-reviewer rows no longer enter telemetry in the resolution, so no new kind is needed either. `/2` is dropped.

**N6. A lock in `append_record` has a correctness reason once D-17 ships at append.** The "one live outcome per `(reviewer_record_id, truth_basis)`" rule (both papers, C-S10/D-17) is a check-then-append over the existing outcome file; `append_record` today is a bare `open(path, "a")` and write (`telemetry.py:287-307`) with no check. Without a lock two concurrent outcome appends can both pass the check. This is the reason I give for the telemetry lock; the torn-line reason (A-009) stays unproven.

**N7. `export` and any other producer must be idempotent by id, not by hope.** `new_record_id()` is `uuid4().hex` (`telemetry.py:118`) and the loader keys on `record_id` (`:417-424`), so re-running a producer doubles rows. Required: record id = hash of `(run_id, step, round, reviewer_id, attempt)` and skip-if-present under the telemetry lock.

**N8. The unverified core is the transcript path, not the format.** Every reader cited by either paper reads a headless run: E1 stream logs (`extract.py`, [R1]), E2 `claude -p` JSON ([R1]), sprint stream-json (`sprint/monitor.py:631-637`, [R1]). The interactive orchestrator's own transcript path and format are shown by neither paper. M1 must include one interactive transcript before any default relies on `--transcript`. [UNVERIFIED]

## 4. Proposed RESOLUTION for slot C-08

One line of map: stage state stays in the manifest; per-agent observation and refusals live in one per-run events file; the cross-run reviewer record stays `review-telemetry/1`; memory stays as it is. Code writes every number; the orchestrator writes none.

1. **Manifest (stage state): unchanged shape, plus a lock.** Entry shape (`manifest.py:348-354`), stage records (`:317-326`), `COMPLETIONS`, `PER_REVIEWER_STAGES`, the digest rules and `reviewers_complete` counting are untouched. No `usage`, `model` or `agents[]` is added to the manifest. `manifest init`, `advance` and the `--publish-from` path run under the shared lock (item 2), held from `load` to `save`. `rev` is not added now (item 12, M2).
2. **One lock helper for the manifest, the events file and the telemetry append.** New `cli/review/lockfile.py` (name chosen to avoid the `*_validator.py` / `gates.py` generator check). `locked(path, timeout_s=10)`: `import fcntl` inside the function, lock file created on demand, `LOCK_EX | LOCK_NB` polled every 50 ms until the timeout, then `LockTimeout`. On a runner without `fcntl` it raises `LockUnavailable`. A CLI that hits either exits non-zero with `lock_timeout` or `lock_unavailable`; inside the reflect shadow steps that is a failed step, recorded as `panel_fallback_reason` with the run continuing as legacy (`SKILL.md:338`). Locks: `<out>/panel/manifest.lock`, `<out>/panel/events.lock`, `<telemetry dir>/.append.lock`.
3. **Per-run record: `<out>/panel/events.jsonl`, schema `review-run-event/1`.** One JSON object per line, append-only, never rewritten. Closed keys: `seq, ts_utc, run_id, kind, role, agent_key, reviewer_id, attempt_id, join, model_requested, model_observed, served_ids, usage{tokens_in, tokens_cache_read, tokens_cache_write, tokens_out, wall_s, usage_complete}, completion, reason, round, block_ok, counts{findings, blocking, by_severity}`. `kind` is one of `agent`, `orchestrator_snapshot`, `merged`, `refused`; `reason` is a closed enum; every value is an int, a bool, null or a short label (the `_RUN_ID` pattern `telemetry.py:243-251` applies), so no document text can enter. `seq`, `ts_utc` and `run_id` are assigned by the writer under the events lock; no caller supplies them. No `ext{}`.
4. **Exactly two writers of events, both code.** (a) `superclaude review record ingest --out <output> --transcript <file>`: the transcript adapter, a pure file parser with no network, reached only as a CLI command (INV-F). (b) `superclaude review merge ... --events PATH`: in-process rows from `merge_cmd.py`. Nothing the orchestrator says reaches `model_observed`, `served_ids` or `usage`. A `record add` command is not built.
5. **Adapter rules (`ingest`).** One immutable `agent` row per sidechain, `agent_key` = the Agent call's tool-use id; re-running `ingest` skips keys already present, so it is idempotent and can run at any time, more than once, and after `published`. `role` from the call's `subagent_type` (`reflect-reviewer` is reviewer, `confidence-calibrator` is calibrator, other known names by name, unknown is helper). `served_ids` = the sorted distinct `message.model` values over the sidechain; `model_observed` = that id only when there is exactly one, otherwise null with the list kept. `usage` = the sum of the sidechain's `message.usage`; unreadable counters are null and `usage_complete` is false; nothing is estimated. `reviewer_id` and `attempt_id` are null unless the join succeeds: by order within role against `panel/resolution.json` when the counts are equal (`join: ordinal`), otherwise `join` is null. The orchestrator's own main-thread usage goes in an `orchestrator_snapshot` row appended only when it differs from the previous snapshot; the reader takes the last one. Where the adapter cannot read a value the field is null and `identity_source` stays `requested-pinned`.
6. **Merge rows (`merge_cmd.py`, only when `--events` is given).** Success: one `merged` row per reviewer with `round`, `block_ok` and `counts` (no model, no usage). Refusal: one `refused` row from the `except` branch at `merge_cmd.py:111-112`, `reason` derived locally: `n != len(ledger["rounds"]) + 1` is `round_order`, duplicate ids is `duplicate_reviewer`, every report failing `findings.parse_block` is `no_valid_block`, else `other`. `ledger.py` is not edited. Merge never reads events. A failed events write (timeout, unwritable path) prints a warning on stderr and leaves stdout, exit code, the ledger and the merged report exactly as they would be without `--events`. Without the flag merge is byte-identical to HEAD. The loop prompt passes `--events <loop dir>/events.jsonl`.
7. **Cross-run record stays `review-telemetry/1`. No `/2`, no new kind.** `validate_record(rec, strict=False)`: `append_record` passes `strict=True` and holds the telemetry lock across the whole check-and-append; strict means group values must be ints, floats, bools, null or short labels, and one live outcome per `(reviewer_record_id, truth_basis)` is enforced (a later outcome must name the earlier one in `supersedes`). `load` is unchanged: it still reports and skips an invalid line, and legacy lines still load. Non-reviewer agents never enter telemetry.
8. **One producer of `reviewer_run`: `superclaude review record export`.** Inputs: `--events`, `--resolution` (the `slot`, `model.resolved`, `model.launch` values), `--cards DIR` (Tier 2: the `output` group from `findings.parse_block` over the cards) or the `merged` rows (loop), `--doc FILE` for the `task` group (null where there is no document), and `--dir` for the telemetry directory. `--dir` or `SUPERCLAUDE_REVIEW_TELEMETRY_DIR` is required: no cwd-relative default. `record_id` is a hash of `(run_id, step, round, reviewer_id, attempt)`; a record already present is skipped, so a second export appends nothing. An absent or empty events file prints `record_absent` and exits 0, so the gap is visible and not silent. `export` also prints the `identity_source` and mismatch values (`--print-identity`): `observed` only when every reviewer and calibrator row has exactly one served id.
9. **Reflect SKILL edits, all inside `### 4.3a`, none in `### 6.3` or `### 9.1`, no new `src/superclaude` string.** Step 2: remove the instruction to write a `model_observed:` header line (the `model:` pin stays). Step 9: `identity_source` and `identity_mismatch_suspected` are copied from the `export --print-identity` output. Step 10: run `record ingest` before `advance published` and `record export` after it; a second `ingest` after the legacy writers is optional and marks the figure `tail_included`.
10. **Identity gate in `scripts/reflect_shadow_exit.py`.** It recomputes `identity_source` and `identity_mismatch_suspected` from `<run>/panel/events.jsonl`, not from the recorded values, and flags a run whose contract printed `calibrator_diversity: full` while the observed ids collapse. `cli/reflect`, `panel_lint.py`, contract 1.8.0 and `derive_verdict` are not edited.
11. **Two labelled cost bases, derived on read, never stored.** `superclaude review record summary --events PATH` prints (a) reviewer-only = reviewer rows; (b) all-agents = every `agent` row plus the last `orchestrator_snapshot`, with `tail_included`. A cross-run all-agents figure is a crawl of events files, the same cost as B's crawl of manifests; no cross-run store is added.
12. **Measurement gates.**
    - **M1 gates `ingest` and everything that reads a served id** (items 5, 9, 10). Replay on the 15 E1 stream logs plus at least one interactive-session transcript. Pass: every reviewer and calibrator call yields a row with `model_observed` or an explicit null; combo A run 3 shows the requested-versus-observed mismatch; per-agent `tokens_out` plus the orchestrator snapshot equals the run-level `modelUsage` output within 2 percent in at least 13 of 15 runs, compared over the same transcript window on both sides. If the sum check fails in more than 2 runs, `usage` ships null and only identity and refusal rows remain. If the first two fail, items 9 and 10 are not shipped and `requested-pinned` stays.
    - **M2 gates `rev`.** The R15 interleaving as a test that fails on HEAD and passes with the lock; a real-process stress of 8 x 50 event appends (400 valid lines, unique `seq`) and 100 concurrent `manifest advance --reviewer-id` (100 attempts kept); control: unlocked `advance_cmd` over 1000 trials. `rev` is added only if a lost update survives with every writer locked or comes from a writer that does not take the lock.
    - **M3 gates the non-reviewer rows.** If reviewer-only tokens are within 10 percent of all-agents tokens in at least 12 of 15 runs, `ingest` writes reviewer and calibrator rows only, with no `orchestrator_snapshot`.
    - **M4** the existing tests pass unmodified; **M5** replay of A3 through the item 10 gate flags it, and a run with three distinct served ids is not flagged.
13. **Deferred, each with a reason.** `/2` and any non-reviewer telemetry kind (not needed: `strict` and events cover it). `record add` (nothing in this slot needs an orchestrator-written row). `rev` (M2). `ext{}` (leak path). The swarm HTTP transport hand-off of `model` and `usage` (`openai_compat.py:467-470`; belongs to the dispatch slot C-07). The memory writer move and the study read-freeze (needs `### 6.3` and Wave 0 edits plus a fence-test update, so its own change; trigger: an observed lost update, or a study that needs the freeze). PR-module producer (C-10) and rf-qa (C-11): the event row is module-neutral and that is all this slot claims. E2's ~25 per-design counters and any exchange (C-12 decides whether a per-run stream is extended). `manifest summary`.
14. **Tests required before merge.** (a) The 35 manifest, 10 telemetry and 36 verdict-matrix tests, the contract-lint and the fence tests pass unmodified (counts [R1]). (b) A manifest pin: `record_attempt` still writes exactly the five-key entry. (c) Merge: success rows; all-invalid gives one `refused(no_valid_block)` row with the ledger unchanged; a replayed round gives `refused(round_order)` and no cost rows; duplicate ids give `refused(duplicate_reviewer)`; no `--events` gives identical stdout, exit and ledger bytes to HEAD; an unwritable events path gives a warning and the same exit and ledger. (d) Adapter: closed keys; a sidechain with two served ids gives `model_observed` null and both ids in `served_ids`; ordinal join only when counts match; re-ingest is a no-op; the last orchestrator snapshot wins; each sidechain lands in exactly one row and the rows sum to the total. (e) Export: deterministic ids; a second run appends nothing; `record_absent` is visible; `test_no_document_text_in_any_record` (`tests/review/test_review_telemetry.py:156`) is extended to event rows. (f) Strict: a sentence in `model.resolved` is rejected at append, the same line already in a legacy file still loads with no invalid entry, and two processes appending an outcome for the same key leave one live outcome. (g) Lock helper: blocks until released; times out to `lock_timeout`; importing the package without `fcntl` works. (h) SKILL: the fence test passes, no `src/superclaude` line is added, and a recipe test runs steps 2, 9 and 10 literally, as `test_shadow_skill_contract.py:104` does for the manifest recipe.
15. **Build order.** PR-1 (needs no adapter): lock helper, manifest lock, telemetry lock plus `strict` plus the live-outcome check, the events writer and schema, `merge --events`, `record export` and `record summary` reading events, tests (b), (c), (e), (f), (g). PR-2 (after M1 is run): `record ingest`, test (d). PR-3 (after M1 passes): reflect SKILL steps 2, 9, 10, the aggregator gate, the loop prompt argument, test (h) and M5.

**Round 1 positions I have changed (11).**
1. `review-telemetry/2` dropped; `strict` at append instead (N5).
2. `record add` dropped; two code writers only.
3. `rev` deferred behind M2; lock spans load to save.
4. "The manifest cannot carry usage without re-specifying pinned behaviour" withdrawn for a reviewer's final usage (C3); kept only for non-reviewer agents and the orchestrator.
5. Orchestrator identity lines replaced in this change, not later (C7).
6. `merge` writes action rows in-process, restricted by cause (C1); refusal rows no longer depend on an orchestrator call.
7. Spec-review loop gets an explicit `--events` flag and prompt argument (C2).
8. A telemetry-append lock added, with a correctness reason (N6); lock is blocking with a timeout and a lazy import (C10).
9. `ext{}` and the swarm transport change removed.
10. The claim that A has a cross-run all-agents store is withdrawn; it is a crawl in both designs.
11. A-002 and A-003 relabelled (section 6).

## 5. Per-point table (all 31 points)

Every Hybrid row matches section 4. "Changed" compares with my Round 1 table.

| Point | Superior approach | Changed since Round 1? | One-sentence reason |
|---|---|---|---|
| S-001 | Neither | Yes (was Variant 1) | Section order carries no evidence; I withdraw the claim that A's order is easier to audit. |
| S-002 | Variant 1 | No | Fewer fully unverified rows (4 against 7 after B upgraded B-12), but my own two key claims (adapter, orchestrator share) are among the unverified ones, so the weight is small. |
| C-001 | Variant 1 (narrowed) | Yes (narrowed) | Per-agent observation, refusals and the loop need one non-stage store, but B's attempt entry is a workable carrier for a reviewer's final usage and I no longer say it is blocked (C3). |
| C-002 | Variant 1 | No | Rows written during the run and an idempotent `ingest` that can run last survive a kill and cover the tail; B's `published` write cannot be repeated on a committed manifest (N1). |
| C-003 | Hybrid | Yes (the `/2` half) | One producer (`export`, A) on `review-telemetry/1` with `strict` at append (B); `/2` is not needed (N5). |
| C-004 | Hybrid | Yes | One blocking lazy-import lock helper for manifest (load to save), events and telemetry append, plus the live-outcome check as the telemetry lock's reason (N6); `rev` waits for M2. |
| C-005 | Variant 2 | No | The move needs a `### 6.3` edit outside the fence and answers a race nobody observed. |
| C-006 | Hybrid | Yes (was Variant 2) | Replace the hand-written lines now inside `### 4.3a` (B), sourced from events and gated in the aggregator by events (A and B). |
| C-007 | Variant 1 | No (claim narrowed) | Both labelled bases come from one per-run file; the cross-run all-agents figure is a crawl in both designs. |
| C-008 | Hybrid | No | A's premise-testing M3, the unlocked-control M2 and the unmodified-test list, plus B's A3 identity-gate replay (M5) and the new merge, adapter, export and strict tests. |
| X-001 | Variant 2 | Yes (was Variant 1) | On the narrow question B is right: A's objection 1a/1b is overstated for a finished sidechain's usage (C3); A is right only that non-reviewer agents and the orchestrator have no attempt row. |
| X-002 | Variant 1 | No | Verified, and reinforced: a second write to a committed manifest is impossible through the stage path (N1). |
| X-003 | Hybrid | Yes (was Variant 1) | B's code-owned writer in the `except` branch is the right mechanism, but it must be restricted by cause and write action rows only (C1, N2). |
| X-004 | Hybrid | No | Both need an in-process writer inside `review merge`; A writes it into the events file. |
| X-005 | Neither | No | 0 of 29 missing `collected` attempts favours B for reviewers, 9 of 29 refused `dispatched` rows and no `calibrated` call site favour A. |
| X-006 | Hybrid | Yes (was Variant 1) | The cited lock is fail-fast `LOCK_NB`; both need a blocking, lazily imported helper with a stated span (C10). |
| X-007 | Variant 2 | Yes (was Variant 1) | The `strict` keyword on the two call sites is a smaller mechanism than `/2` (N5). |
| X-008 | Variant 1 | No | `export` is the one named carrier for both paths; B's `from-manifest` converges to it once its missing inputs are added. |
| X-009 | Variant 1 | No | B excludes the post-`published` tail yet checks a run-level total; an idempotent `ingest` can include it. |
| X-010 | Hybrid | Yes (was Variant 2) | The loop's capture sits in `review merge` (B) and writes the same events format through an explicit `--events` flag (A). |
| X-011 | Variant 2 | No | Moving the memory writer needs an edit the fence forbids. |
| X-012 | Neither | No | Small slips on both sides; no design effect. |
| A-001 | Neither | No | Shared unverified dependency; both degrade to null, M1 decides. |
| A-002 | Neither | No | Neither shows an interactive transcript path; M1 must include one. |
| A-003 | Hybrid | No | One row per sidechain with a served-id list, `model_observed` null when ambiguous, and an ordinal join only when the counts match. |
| A-004 | Variant 1 | No | `ingest` has no ordering precondition; B's attempt route is order-bound, though the `collected` call site exists. |
| A-005 | Hybrid | No | One lazily imported, blocking, timed lock helper shared by all three writers. |
| A-006 | Hybrid | Yes (was Variant 2) | The loop path is opt-in through `--events`, and `export` has no cwd-relative default directory. |
| A-007 | Variant 1 | No | Per-sidechain rows with a caller-supplied attempt join make the partition checkable, but test (d) is required. |
| A-008 | Hybrid | No | B's `panel_fallback_reason` rule plus a visible `record_absent` at export. |
| A-009 | Variant 2 | Yes (was Neither) | Include the telemetry lock, for the check-then-append reason (N6), not for torn lines. |

## 6. Shared assumptions A-001 to A-009

Labels as defined at the top of this file.

- **A-001: QUALIFY.** A transcript adapter is sound only if M1 passes on the 15 E1 logs plus one interactive transcript; until then every served-id and usage field is null and `identity_source` stays `requested-pinned`.
- **A-002: QUALIFY** (Round 1: ACCEPT). The input is a file path, but every cited reader works on a headless run; the interactive path and format are shown by neither paper and the E1 logs are untracked, so M1 runs only on this machine. [UNVERIFIED]
- **A-003: REJECT** (Round 1: ACCEPT, used in the other sense). "One sidechain is exactly one `(reviewer_id, attempt_id)` with one served id" must not be assumed; the resolution keys on tool-use id, keeps `served_ids`, nulls `model_observed` when ambiguous and joins by ordinal only when counts match.
- **A-004: QUALIFY.** The orchestrator must make at least one `ingest` call (and, for the loop, pass `--events`), but `ingest` is idempotent with no order precondition, unlike B's record-before-advance attempts (`manifest.py:371`); a skipped call shows as `record_absent`.
- **A-005: QUALIFY.** `fcntl` is POSIX-only and the precedent imports it lazily (`record.py:389`) and fails fast (`:403`); the helper must import lazily, block with a timeout, and a runner without `fcntl` gets `lock_unavailable` and a legacy fallback.
- **A-006: QUALIFY.** `<out>/panel/events.jsonl` exists where a panel directory exists; the loop uses `--events`, and the telemetry directory has no cwd-relative default in `export` (it stays in `telemetry append`, unchanged).
- **A-007: QUALIFY.** One row per agent is the right grain only with the partition test (each sidechain in exactly one row, rows sum to the total) and a rule for a retried reviewer (separate rows by tool-use id; the attempt join is by ordinal or null).
- **A-008: QUALIFY.** The `superclaude` command can be absent (the loop prompt says so); the gap must be visible (`record_absent`, `panel_fallback_reason`) and not a silent "behaves as today".
- **A-009: QUALIFY.** Torn lines on the cross-run file are unproven (`telemetry.py:305-306` is one write in append mode, [UNVERIFIED] on buffer behaviour); the telemetry lock is justified by the one-live-outcome check-then-append, not by interleaving.

Status: Complete
