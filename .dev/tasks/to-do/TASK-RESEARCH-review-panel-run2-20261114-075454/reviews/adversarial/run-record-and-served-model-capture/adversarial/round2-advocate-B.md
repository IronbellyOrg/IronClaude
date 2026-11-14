# Round 2 advocate for Variant 2 (Proposal B), slot C-08 run-record-and-served-model-capture

Status: Complete
Role: ADVOCATE for Variant 2 in Round 2 (sequential rebuttal, second speaker). Debate focus: correctness, risk, test-coverage.
Code state: HEAD 50d4d2b9d on `ironbelly/shadow-runs`; repo root `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel`; paths below are repo-relative.
Tags: [RE-READ] = read at HEAD in this round; [R1] = carried from a Round 1 file or the diff analysis, not re-read; [UNVERIFIED] = not re-derived.
Label meaning in section 6 (as set by the lead): ACCEPT = sound as the design needs it; REJECT = unsound; QUALIFY = sound only under a stated condition.

## 1. Response to criticisms of Variant 2

Sources: A's Round 1 section 4 (nine weaknesses), A's Round 2 section 1 (C1-C10, the repair table) and section 2 (five weaknesses). Each is conceded or countered with code.

**X-002, `agents[]` on `published`/`failed` (conceded, and A's N1 makes it worse).** I re-read it: `advance_stage` returns False on an identical digest before touching the manifest (`manifest.py:293-296`), and `advance_cmd` saves only when `changed` (`manifest_cmd.py:204-205`) [RE-READ]. My Round 1 repair (a write-once unhashed `agents` object) works only on the single first call of `published`, so the orchestrator tail after `published` cannot be added and a second mutating command on a committed manifest would contradict the rule that a committed manifest does not change. I withdraw the `agents[]` route and, with it, the claim that the manifest should carry non-reviewer observation.

**X-001 / C-001, manifest-resident `usage`/`model` on attempts (conceded as the carrier, kept as a narrow fact).** The narrow fact stands and A now says so: a finished sidechain's usage is final, so one payload recorded with the attempt hashes stably; `_recount` reads only `completion` of `collected` entries (`manifest.py:269-274`); no test pins the entry shape (grep of `tests/`: only `superseded_by` at `tests/review/test_review_manifest.py:169`) [RE-READ]. But two things decide it against the manifest as carrier. (1) Non-reviewer agents and the orchestrator have no attempt row (`manifest.py:53`), so a manifest carrier is never complete and the observation would live in two stores that must be reconciled. (2) The route is order-bound: usage rides on `manifest advance --stage collected --reviewer-id ...` (`SKILL.md:342`), which must precede `advance collected` (`manifest.py:371`), and a calibrator has no call site at all (`SKILL.md:344` says only "Advance `calibrated`") [RE-READ]. One store with no ordering precondition is the better correctness position. I move to A's store.

**X-003, producer "after `merge_round`" (conceded, and N2 corrects my repair).** My Round 1 repair wrote reviewer records from the `except` branch for every `LedgerError`. `merge_round` raises `LedgerError` for round order (`ledger.py:114-118`) and duplicate reviewer id (`:119-121`) before the no-valid-block check (`:150-157`) [RE-READ], so a replayed round would write cost records a second time. Conceded. The writer in `merge` may write action rows only, never cost rows (section 4, item 6).

**X-007, type check at append with no mechanism (conceded; my own `strict` repair stands, but A's wording of it fails the fixtures).** See section 3, N-B3: the label rule A reuses rejects strings that the repo's own fixtures and tier file contain.

**X-008, no Tier 2 producer (conceded).** A is right that a `reviewer_run` needs `panel`, `slot`, `model`, `task`, `output`, `cost` and `context` plus the top keys (`telemetry.py:205`) [RE-READ], and the manifest holds none of `slot`, `task`, `output`, `context`. My `from-manifest` step was `export` under another name with fewer inputs. One producer: `export`.

**X-009, M1 can fail by construction (conceded).** Moot once the orchestrator row comes from an idempotent `ingest` that can run after `published`.

**C-002 / C-007, tail, kill residual, cross-run all-agents basis (conceded).** Rows written during the run survive a kill; I do not claim otherwise. A cross-run all-agents figure is a crawl of events files in the resolution, the same cost as a crawl of manifests in B, so this is not a differentiator any more (A withdrew its Round 1 claim, A Round 2 item 10).

**X-005 (conceded, partly).** `collected` 0 of 29 missing and `dispatched` 9 of 29 refused (R15 figures [R1], UNVERIFIED by me) both stand; either way the attempt route is order-bound and `calibrated` has no call site.

**A's section 2 point 1, "after repairs B is not smaller" (conceded as stated, with a counter).** After the repairs B edits `manifest.py`, `manifest_cmd.py` (three branches), `telemetry.py`, `merge_cmd.py` and adds a producer step; that is not smaller than A. Counter: A's resolution is not small either (new lock module, new `record` module and command family, a ~20-key event schema with four kinds, plus `merge_cmd.py`, `telemetry.py`, ledger edits, SKILL, aggregator and loop prompt). Size is therefore not the differentiator; correctness against existing tests is (sections 3 and 4).

**N6, telemetry-append lock justified by the one-live-outcome check (countered).** The check is introduced by this change and contradicts a pinned test (section 3, N-B2). With the check gone, no check-then-append remains, and with deterministic record ids plus `INSERT OR IGNORE` at load (`telemetry.py:417-424`) a duplicate line is harmless. The lock stays out.

**A's repair table, `strict` row (accepted), "producer name and input" row (accepted), "catch `LedgerError`" row (accepted with N2).** The `agents[]` row is accepted as stated.

**C-005 / X-011 / X-010 / C-006 (A conceded these, no counter needed).** I re-read the fence: `test_skill_changes_are_confined_to_the_allowed_sections` allows only `### 3.1`, `### 4.3a`, `### 5.4`, `### 9.2` (`tests/cli/reflect/test_shadow_skill_contract.py:65`), `### 6.3` is at `SKILL.md:585` [RE-READ]. The memory writer stays where it is.


## 2. Updated assessment of Variant 1 after A's Round 2

**What A moved on, and I agree with.** A dropped `review-telemetry/2`, `record add`, `rev`, `ext{}`, the swarm transport change and the memory move; wrote the refusal row from inside `merge`; added an explicit `--events` flag for the loop; replaced the orchestrator identity lines inside `### 4.3a` now; split `agent` rows (immutable) from `orchestrator_snapshot` (last wins); and gated the non-reviewer rows behind its own M3. Every one of those removes a risk I raised or removes surface. A's base for the observation store (one append-only per-run file, no ordering precondition, survives a kill, carries refusals) is better than mine, and I adopt it.

**What still fails against the code (A's resolution as written, five items).**
1. **Item 9 against an existing test.** Removing the `model_observed:` header instruction (`SKILL.md:341`) breaks `assert "`model_observed:`" in shadow` at `tests/cli/reflect/test_shadow_skill_contract.py:228` [RE-READ], while A's item 14(a) and M4 say the fence tests pass unmodified.
2. **Item 7 against an existing test.** The append-time "one live outcome per `(reviewer_record_id, truth_basis)`" refusal would reject outcomes o2 and o3 in `tests/review/test_review_telemetry.py:363-400`, which appends three live outcomes for one reviewer record and pins their sum (`("sonnet", 3)` at `:400`) [RE-READ].
3. **Item 7 label rule against fixtures.** The "short label" rule A points at (`_RUN_ID`, `telemetry.py:21`) rejects `slot.alias = "claude-gw-tier3[1m]"` and `seed = "1|t3|1"` in the unit-test fixture (`test_review_telemetry.py:40, :42`) and the real tier aliases `claude-gw-tier1a[1m]` (`src/superclaude/cli/review/data/review-tiers.default.json:5-7`) [RE-READ]; `append_record(strict=True)` would refuse the repo's own valid record.
4. **Item 5 ordinal join.** Equal counts with permuted order is a documented, tested shadow outcome (`panel_parity` false, nothing blocked: `SKILL.md:340-341`; the fixture at `test_shadow_skill_contract.py:291-299`), and the dispatch is the legacy one (`SKILL.md:342`). An ordinal join attaches the wrong `reviewer_id`, hence the wrong slot, model and output groups, to a sidechain's cost with no signal.
5. **Item 6 derived-locally reason.** In `merge_cmd.py` the `try` at `:100` also covers `led.load`/`new_ledger`; `LedgerError` is raised by `load` at `ledger.py:46, 48` before `ledger` is bound, so A's `n != len(ledger["rounds"]) + 1` in the `except` branch raises `UnboundLocalError` and replaces the `ClickException`. That breaks A's own rule "same exit code as without `--events`".

**What remains weak by design.** (a) The transcript adapter is still an unverified dependency, and every reader cited is a headless run (A's N8; I agree). (b) Size: a new lock module, a `record` module with three subcommands, a ~20-key row with four kinds, four measurement gates and fifteen test groups. (c) Build order: item 15's PR-1 ships a lot of code with no caller (events writer, `merge --events`, `export`, `summary` all wait for PR-2 or PR-3), and `export` reads served ids before M1 has run, which A's own rule says is gated by M1.

**Net.** A is the right base for the observation store, the refusal rows and the loop path. B contributes the fence analysis, the strict keyword (once its label rule is fixed), the in-process merge writer restricted by cause, the A3 identity-gate replay and the fallback text. The hybrid in section 4 takes A's 15 items with the corrections above.


## 3. New evidence not in Round 1

All re-read at HEAD this round unless tagged.

**N-B1. Item 9 edits a line a test pins.** `test_shadow_steps_pin_the_header_model_the_verdict_file_and_the_first_pass_metric` asserts `"`model_observed:`" in shadow` (`test_shadow_skill_contract.py:221-238`, assertion at `:228`). The only consumers of the `model_observed:` header text are `SKILL.md:341`, `:348` and that assertion (grep outside `.dev`, `docs`, `.claude`: the other hits are the SQL alias `model_observed` in `telemetry.py:364, 378`, its tests, and `identity_source`/`identity_mismatch_suspected` in the §9.2 telemetry list at `SKILL.md:974-975`). So removing the instruction is safe for behaviour, but the same change must edit that one assertion and list it as a deliberate test change. `SKILL.md:348` already defines `identity_source: observed` as "the adapter read the reviewer's resolved model id from its transcript", so the SKILL already anticipates the adapter.

**N-B2. The one-live-outcome rule contradicts a pinned test and removes N6's reason.** `outcome_record()` defaults `truth_basis` to `theme-v1` and `supersedes` to None (`test_review_telemetry.py:88-108`). `test_outcome_with_a_conflicting_stratum_is_excluded_and_counted` appends o1 (sonnet), o2 (haiku) and o3 (untagged) for the same `reviewer_record_id` and asserts `rows == [("sonnet", 3)]`, "1 + 2" (`:363-400`). So today two live outcomes for one reviewer record are accepted and summed, and the repo's idiom for a conflict is to count it on load (`counts["stratum_conflicts"]`, `telemetry.py:440-443`), not to refuse at append. An append-time refusal makes that test fail unless it is edited in the same change. Whether the decided D-17 text requires refusal rather than visibility I could not re-derive [UNVERIFIED]; both papers state the rule. Consequence for A's N6: with no check-then-append, the telemetry lock has no correctness reason, and `new_record_id` being `uuid4` (`telemetry.py:118-119`) is solved by deterministic ids, after which `INSERT OR IGNORE` on `record_id` (`:417-424`) makes a duplicated line harmless.

**N-B3. `strict` needs its own label rule.** `_RUN_ID` is `^[A-Za-z0-9._-]{1,64}$` (`telemetry.py:21`) and is applied to `context` (`:243-251`). The fixture record that `append_record` accepts today has `slot.alias "claude-gw-tier3[1m]"` and `seed "1|t3|1"` (`test_review_telemetry.py:40, :42`), `panel.template_sha256 "x"`, `task.doc_sha256 "d"`; the real aliases are `claude-gw-tier1a[1m]`, `claude-gw-tier1b[1m]`, `claude-gw-tier2[1m]` (`review-tiers.default.json:5-7`). A served model id read from a transcript can be such an alias. A usable rule that keeps text out and keeps these in: a string value must contain no whitespace and be at most 80 characters; a dict is allowed only for `output.by_severity` (ints or null); numbers, bools and null otherwise. Tests derive from the data: every alias and model string in `review-tiers.default.json` passes strict.

**N-B4. Ordinal join misattributes in a tested case.** `recompute_parity` is tested with legacy `[(analyzer, sonnet), (qa, opus), (refactorer, haiku)]` against a resolution order `[sonnet, haiku, opus]`: three against three, permuted, parity false (`test_shadow_skill_contract.py:291-299`). SKILL step 1 says the resolution "can differ" from the legacy run and step 3 says "Dispatch is the legacy dispatch" (`SKILL.md:340, :342`). The reviewer id is an identity claim the orchestrator already makes on every `manifest advance --reviewer-id` call (`SKILL.md:342`). A deterministic join: name each reviewer's Agent call with its reviewer id in the call's `description` (a required parameter of the Agent tool in this session's tool schema; its presence in transcripts is shown only through the E1 extractor reading each call's `model`, [R1]) and have the adapter join on exact match; no match means `join` null.

**N-B5. Merge refusal reason needs a code-owned source, not three copied predicates.** `LedgerError` is a bare `Exception` subclass (`ledger.py:29-30`) raised at `:46, :48` (load), `:116` (round order), `:121` (duplicate), `:154` (no valid block), and later at `:306, :312, :365, :379` [RE-READ]. In `merge_cmd.py` everything from `led.load` to `render_merged_report` is in one `try` (`:100-112`). An optional `reason` attribute on `LedgerError`, set at `:116` (`round_order`), `:121` (`duplicate_reviewer`), `:154` (`no_valid_block`) and defaulting to `other`, avoids the unbound `ledger`, cannot drift from the ledger's own guards, and leaves verdict logic untouched. `merge_round`'s result exposes `block_ok` but no per-reviewer finding counts (`ledger.py:286-298`), so `counts` in a `merged` row needs one `findings.parse_block` per report inside `merge_cmd`.

**N-B6. The aggregator is pinned read-only.** `test_report_file_and_no_other_writes` lists every path under the runs root before and after (`tests/cli/reflect/test_shadow_exit_script.py:313-319`). A gate in `scripts/reflect_shadow_exit.py` must read `events.jsonl` without the lock helper (which creates lock files) and must treat a missing file as `requested-pinned`. The aggregator only inspects published manifests (`reflect_shadow_exit.py:215-223`), so failed or incomplete runs are not gated; that is acceptable.

**N-B7. Where the manifest lock goes.** `publish_files` does its own `load` (`manifest.py:495`) and `commit_published` does a second `load` and `save` (`:521-524`), and the 35 manifest tests call library functions directly (`test_review_manifest.py:279-367`). A lock inside `save` or `load` would not span the read-modify-write, and a library-level lock would touch every test. Place the lock in `manifest_cmd.py` (`init_cmd`, `advance_cmd` including the `--publish-from` branch), acquired only after `manifest.json` is known to exist for `advance`, so a mistyped `--out` creates no directory. The extra file `panel/manifest.lock` does not trip the `.tmp-` directory scans (`test_review_manifest.py:288, :367`). Counts verified by grep: 35 manifest and 10 telemetry test functions; the 36 verdict-matrix figure is [R1].

**N-B8. Precedent lock details A's helper must decide.** `record.py:389-419` opens with `O_NOFOLLOW`, rejects a non-regular or foreign-owned file and re-checks the inode after acquiring, because its state directory can be deleted. A helper whose lock file is never unlinked needs only `O_CREAT | O_NOFOLLOW | O_CLOEXEC`; it should say so.

**N-B9. Fixtures for the adapter.** The 15 E1 logs are untracked and hold prompts [R1], so unit tests need a small committed synthetic transcript; the real-log replay (M1) is a measurement, not a test. A's test (d) does not say this, so a green (d) would prove only the author's reading of the format.

**N-B10. What is verified about the transcript path.** Nothing in either paper shows how an interactive orchestrator finds its own transcript or its subagent transcripts [UNVERIFIED, agree with A's N8]; step 10 of A's item 9 asks the orchestrator to pass `--transcript`, so M1 must include that path before item 9 ships.


## 4. Proposed RESOLUTION for slot C-08

### 4.1 Verdict on each of A's 15 items

1. **Manifest unchanged shape plus lock: AGREE-WITH-CHANGE.** Keep the five-key entry, stage records, counters and digest rules; no `usage`/`model`/`agents[]`; no `rev` (M2). Change: the lock lives in `manifest_cmd.py` only (`init_cmd`, `advance_cmd` including the `--publish-from` branch), held from `load` to `save`, because `publish_files` does two separate load/save pairs (`manifest.py:495, 521-524`) and the library functions are called directly by the 35 tests. For `advance`, acquire only after `manifest.json` is confirmed present (no stray directories for a wrong `--out`). Evidence: N-B7.
2. **One lock helper: AGREE-WITH-CHANGE.** Keep: new `cli/review/lockfile.py` (the generator-name rationale is [UNVERIFIED]; harmless), lazy `import fcntl`, blocking acquire by polling `LOCK_EX | LOCK_NB` to a timeout, `LockTimeout`/`LockUnavailable`, failed step recorded as `panel_fallback_reason` and the run continues as legacy (`SKILL.md:338`). Change: only two locks, `<out>/panel/manifest.lock` and `<out>/panel/events.lock`; the telemetry `.append.lock` is dropped (N-B2: no check-then-append, deterministic ids plus `INSERT OR IGNORE`); the helper opens `O_CREAT | O_NOFOLLOW | O_CLOEXEC` and never unlinks (N-B8).
3. **Event row `review-run-event/1`: AGREE-WITH-CHANGE.** Keep the key list, four kinds, closed `reason` enum, writer-assigned `seq`/`ts_utc`/`run_id`, no `ext{}`. Change: the value rule is not `_RUN_ID`: strings are no-whitespace, at most 80 characters; allowed nested shapes are exactly `usage{}`, `counts{}` with `by_severity{}` (ints or null) and `served_ids` (a list of such strings); a closed-key check runs on write and on every read (`export`, `summary`, the aggregator gate), and an unknown key is an error, not skipped (N-B3).
4. **Exactly two code writers: AGREE.** `record ingest` and `merge --events`; no orchestrator-written row, no `record add`.
5. **Adapter rules: AGREE-WITH-CHANGE (the join) and DISAGREE with "ordinal".** Keep: one immutable row per sidechain keyed by tool-use id, role from `subagent_type`, `served_ids` as the sorted distinct list, `model_observed` only when exactly one id, `usage` summed with null plus `usage_complete: false` when unreadable, `orchestrator_snapshot` appended only on change with the last one winning, idempotent re-ingest. Change: replace "ordinal within role when counts match" with a join on the Agent call's `description`: SKILL step 3 (inside `### 4.3a`) says each reviewer's call is named with its reviewer id; the adapter sets `reviewer_id` only on exact match to a `reviewer_id` of `panel/resolution.json`, and `attempt` = 1-based order among calls with the same description; no match gives `join` null and no `reviewer_run` for that sidechain. Evidence: N-B4 (permuted equal-count case at `test_shadow_skill_contract.py:291-299`). The identity check uses the call's own `model_requested` against `served_ids`, never the pin, so a parity-false run is not read as identity collapse.
6. **Merge rows: AGREE-WITH-CHANGE.** Keep: only with `--events`; `merged` rows on success; one `refused` row from the `except` branch; failed events write is a stderr warning with unchanged stdout, exit code, ledger and merged report; byte-identical without the flag; the loop prompt passes the flag. Change: the refusal `reason` comes from a new optional `LedgerError.reason` set at `ledger.py:116, :121, :154` (default `other`), not from predicates copied into `merge_cmd.py`, so a corrupt ledger (`ledger.py:46, 48`) gives `other` and the `ClickException`, not an `UnboundLocalError`; `counts` come from `findings.parse_block` inside `merge_cmd` (N-B5). "ledger.py is not edited" is relaxed to these four additions.
7. **`strict` plus supersedes rule: AGREE-WITH-CHANGE on `strict`, DISAGREE on the append-time live-outcome refusal.** `validate_record(rec, strict=False)`; `append_record` passes `strict=True`; strict uses the N-B3 rule; `load` unchanged (two call sites, `telemetry.py:289, 411`). Not shipped: refusing a second live outcome at append (breaks `test_review_telemetry.py:363-400`). Instead `load` returns `live_outcome_conflicts` beside `stratum_conflicts` (`telemetry.py:440-443`), counting outcomes that share `(reviewer_record_id, truth_basis, effective stratum)` with none superseded. If the D-17/C-S10 text does require refusal, the owner of outcomes edits that test in the same change; that is not this slot's call.
8. **One producer `record export`: AGREE-WITH-CHANGE.** Keep: `--events`, `--resolution`, `--cards DIR` or `merged` rows, `--doc`, required `--dir`/`SUPERCLAUDE_REVIEW_TELEMETRY_DIR` (no cwd default), deterministic `record_id` = hash of `(run_id, step, round, reviewer_id, attempt)`, `record_absent` visible, `--print-identity`. Change: name the `panel` group source (`template_id`, `template_version`, `template_sha256`, `tiers_version`, `tiers_sha256`, `environment` from the resolution JSON, `panel_size` = number of reviewers; `panel.py:690-698`), skip a sidechain whose join is null and say why, and take the skip-if-present check without a lock (duplicates are harmless at load).
9. **Reflect SKILL edits inside `### 4.3a`: AGREE-WITH-CHANGE.** Keep steps 2, 9, 10 as A writes them and the rule of no new `src/superclaude` string. Change: (a) add to step 3 the reviewer-id Agent-call naming (item 5); (b) the removal of the `model_observed:` header instruction changes the assertion at `test_shadow_skill_contract.py:228`, so that one assertion is edited in the same change to assert the new text (`record ingest` named in the shadow steps), and item 14(a) lists it as the single deliberate edit to an existing test; (c) the recipe test (`:104-139`) is extended to run the new commands literally against the synthetic fixture.
10. **Identity gate in the aggregator: AGREE-WITH-CHANGE.** Keep: recompute `identity_source` and `identity_mismatch_suspected` from `<run>/panel/events.jsonl`; flag a run whose contract printed `calibrator_diversity: full` while served ids collapse; no edit to `cli/reflect`, `panel_lint.py`, contract 1.8.0 or `derive_verdict`. Change: it reads without the lock and creates no file (N-B6), a missing events file gives `requested-pinned`, and collapse is measured on `served_ids` against `model_requested`, with `panel_parity` reported separately as today.
11. **Two labelled cost bases derived on read: AGREE.** `record summary` is read-only and ships last.
12. **Measurement gates: AGREE-WITH-CHANGE.** Keep M1 to M5 and their thresholds. Change: M1 also gates item 8's `model.observed` and `--print-identity`, not only items 5, 9, 10; M1 includes one interactive transcript (N-B10); unit tests use a committed synthetic transcript, the 15 real logs are a measurement (N-B9); M4 reads "the existing tests pass unmodified except the one assertion named in item 9".
13. **Deferred list: AGREE, with two additions.** Add: the append-time live-outcome refusal (outcomes owner) and the telemetry append lock (no reproduced race).
14. **Tests: AGREE-WITH-CHANGE.** (a) Existing 35 manifest, 10 telemetry and 36 verdict-matrix tests [36 is R1], the contract lint and the fence tests pass, except the single assertion in item 9. (b) as A. (c) as A, plus: a corrupt ledger with `--events` gives `refused(other)` with the same exit code and message as without the flag; a replayed round gives `refused(round_order)` and writes no cost row. (d) adapter tests on the synthetic fixture, including: equal counts with permuted order joins correctly by description; no description gives `join` null; a sidechain with two served ids gives `model_observed` null. (e) as A, with a field-level type test on event rows. (f) replaces A's (f): strict accepts every fixture in `test_review_telemetry.py` and every alias and model string of `review-tiers.default.json`; strict rejects a sentence in `model.resolved`; the same line in a legacy file still loads; `load` returns `live_outcome_conflicts` for the o1/o2/o3 case and nothing is refused. (g) lock helper: blocks until released, times out, imports without `fcntl`, creates no directory when the manifest is absent, and an aggregator run leaves the runs root unchanged (`test_shadow_exit_script.py:313-319` stays green). (h) as A.
15. **Build order: AGREE-WITH-CHANGE.** PR-1 (each item changes a path that has a caller and tests today, no adapter needed): lock helper, manifest lock in `manifest_cmd.py`, `strict`, `live_outcome_conflicts`, `LedgerError.reason`, tests (b), (f), (g) and the reason half of (c). PR-2 (the loop path has a real caller through the loop prompt): events writer and schema, `merge --events`, loop prompt argument, `record summary` on `merged`/`refused` rows, tests (c), (e). PR-3 (after M1): `record ingest`, `record export`, SKILL steps 2, 3, 9, 10 with the test edit, the aggregator gate, tests (d), (h) and M5. This keeps dormant code to PR-2's `export`-less writer and puts everything that reads a served id behind M1.

### 4.2 Items A omitted

1. The `panel` group source for `reviewer_run` (item 8).
2. The reviewer-id naming of Agent calls as the join key, and the three-way identity comparison (call `model_requested`, pin, served), so parity and identity are not conflated (items 5, 10).
3. A lock acquired before the manifest exists would create directories; the aggregator must stay read-only (item 1, 10).
4. `LedgerError.reason` and the unbound-`ledger` hazard (item 6).
5. The strict label rule and the fixture-derived test (item 7).
6. The committed synthetic transcript and what M1 is allowed to claim (item 12).
7. What `export` does for a null join: skip with a visible reason (item 8).

### 4.3 The hybrid in short form (the text the merge builds from)

1. Observation lives in `<out>/panel/events.jsonl` (`review-run-event/1`), append-only, closed keys, written only by code: `record ingest` (transcript adapter, idempotent, any time) and `merge --events` (`merged` and `refused` rows). The manifest keeps its shape and gains only a CLI-level lock. No manifest `usage`/`model`/`agents[]`.
2. Cross-run record stays `review-telemetry/1`; `validate_record(strict=False)` with a strict mode at `append_record` (no whitespace, at most 80 characters, no nested text); `load` unchanged, plus a `live_outcome_conflicts` count. One producer, `record export`, with deterministic ids and a visible `record_absent`. No `/2`, no telemetry lock, no append-time outcome refusal.
3. Two locks, one blocking, timed, lazily imported helper; failed lock is a recorded fallback to legacy in shadow mode.
4. Join by Agent-call `description` equal to the reviewer id; null otherwise; identity measured on `served_ids` against `model_requested`.
5. `merge` refusal reason comes from `LedgerError.reason`; merge output is byte-identical without `--events`.
6. SKILL edits only inside `### 4.3a` (steps 2, 3, 9, 10) plus one deliberate assertion edit at `test_shadow_skill_contract.py:228`; memory writer, `### 6.3`, `### 9.1` and contract 1.8.0 untouched.
7. Aggregator gate reads events read-only and flags `full` over a collapsed panel; replay of A3 flags it and a run with three distinct served ids is not flagged.
8. Order: PR-1 (locks, strict, count, reason) then PR-2 (events, merge, loop, summary) then PR-3 after M1 (`ingest`, `export`, SKILL, gate).

### 4.4 Round 1 positions I changed

1. Manifest-resident `usage`/`model` and `agents[]`: withdrawn; observation store is A's events file (C-001, C-002, X-001 route, X-002).
2. Two producers: withdrawn; one `export` (C-003, X-008).
3. Merge writer: now restricted to action rows by cause with `LedgerError.reason` (X-003, X-004).
4. Telemetry-append lock: stays out (Round 1 "drop from must-have" is now "not shipped", A-009).
5. C-006 moved from Variant 2 to Hybrid, X-010 from Variant 2 to Hybrid, X-007 from Variant 1 to Variant 2 (repaired `strict`, not `/2`).
6. Held: no memory move (C-005, X-011), fence analysis, A3 identity-gate replay, fallback text, no `/2`, no `ext{}`.


## 5. Per-point table (all 31 S-, C-, X-, A- points)

"Changed" compares with my Round 1 table. Every Hybrid row matches section 4.3.

| Point | Superior approach | Changed since Round 1? | One-sentence reason |
|---|---|---|---|
| S-001 | Neither | No | Section order carries no evidence. |
| S-002 | Variant 1 | No | A re-read more of its evidence (4 fully unverified items against 8), even though five of A's resolution items fail against code (section 2). |
| C-001 | Hybrid | Yes (label same, base moved to A) | A's events file is the observation store and the manifest stays a pure state machine with a lock; B contributes the cross-run `review-telemetry/1` record, the fence analysis and `strict`. |
| C-002 | Variant 1 | No | Rows written during the run and an idempotent `ingest` cover non-reviewer agents, the tail and killed runs; a committed manifest takes no second write (`manifest.py:293-296`). |
| C-003 | Hybrid | No | One producer `export` (A) on `review-telemetry/1` with a repaired `strict` (B), no `/2`. |
| C-004 | Hybrid | Yes (was Neither) | A's manifest and events locks through one blocking, lazily imported helper in `manifest_cmd.py`; B's telemetry lock is not shipped (N-B2) and `rev` waits for M2. |
| C-005 | Variant 2 | No | The move needs a `### 6.3` edit outside the fence (`test_shadow_skill_contract.py:65`) and answers a race nobody observed. |
| C-006 | Hybrid | Yes (was Variant 2) | Replace the hand-written identity lines now inside `### 4.3a` (B), sourced from events and gated read-only in the aggregator (A and B), with the one pinned assertion at `:228` edited deliberately. |
| C-007 | Variant 1 | No | Both labelled bases derive from one per-run file; the cross-run all-agents figure is a crawl in either design. |
| C-008 | Hybrid | Yes (was Variant 1) | A's M3 premise test, M2 control and test list plus B's A3 replay, with M1 widened to every served-id reader, a synthetic fixture and M4's one named exception. |
| X-001 | Variant 2 | No | On the narrow question B is right (a final sidechain's usage hashes stably, `manifest.py:269-274`); the design still leaves the manifest because it cannot be complete. |
| X-002 | Variant 1 | No | Verified, and a second write to a committed manifest is impossible (`manifest.py:293-296`, `manifest_cmd.py:204-205`). |
| X-003 | Hybrid | Yes (was Variant 2) | The code-owned writer in the `except` branch is the right mechanism but writes action rows only, with the reason taken from `LedgerError.reason` (N2, N-B5). |
| X-004 | Hybrid | Yes (was Variant 2) | Both need an in-process writer in `review merge`; its store is A's events file. |
| X-005 | Neither | No | 0 of 29 missing `collected` attempts favours B for reviewers, 9 of 29 refused `dispatched` rows and no `calibrated` call site favour A (R15 [R1]). |
| X-006 | Neither | No | The cited lock is fail-fast (`record.py:403`) and neither text states a span; items 1 and 2 of section 4.1 supply both. |
| X-007 | Variant 2 | Yes (was Variant 1) | A `strict` keyword on the two call sites (`telemetry.py:289, 411`) is smaller than `/2`, provided its label rule admits brackets and the pipe character (N-B3). |
| X-008 | Variant 1 | No | `export` is the one named carrier for both paths; B's `from-manifest` converges to it. |
| X-009 | Variant 1 | No | B excludes the post-`published` tail yet checks a run-level total; an idempotent `ingest` can include it. |
| X-010 | Hybrid | Yes (was Variant 2) | The loop's capture sits in `review merge` (B) and writes A's events format through an explicit `--events` flag. |
| X-011 | Variant 2 | No | Moving the memory writer needs an edit the fence forbids. |
| X-012 | Neither | No | Small slips on both sides with no design effect. |
| A-001 | Neither | No | Shared unverified dependency; both degrade to null, M1 decides. |
| A-002 | Neither | No | Neither shows an interactive transcript path; M1 must include one and unit tests need a synthetic fixture (N-B9, N-B10). |
| A-003 | Hybrid | Yes (was Neither) | One row per sidechain keyed by tool-use id with a served-id list (A), joined by Agent-call description, not ordinal (N-B4). |
| A-004 | Variant 1 | Yes (was Neither) | `ingest` has no ordering precondition; B's attempt route is order-bound (`manifest.py:371`) and `calibrated` has no call site (`SKILL.md:344`). |
| A-005 | Hybrid | Yes (was Neither) | One lazily imported, blocking, timed helper with a stated CLI-level span for two locks. |
| A-006 | Hybrid | Yes (was Neither) | The loop path is opt-in through `--events`, and `export` takes a required `--dir`; no cwd-relative default. |
| A-007 | Variant 1 | Yes (was Neither) | Per-sidechain rows plus a description join make the partition checkable, if test (d) includes the permuted case. |
| A-008 | Hybrid | Yes (was Neither) | B's `panel_fallback_reason` rule plus a visible `record_absent` at export. |
| A-009 | Variant 1 | No | The events lock has a reason (idempotent ingest, `seq`); a telemetry lock has none that survives the pinned test at `test_review_telemetry.py:363-400`. |


## 6. Shared assumptions A-001 to A-009

- **A-001: QUALIFY.** An adapter is sound only if M1 passes on the 15 E1 logs plus one interactive transcript; until then every served-id and usage field is null and `identity_source` stays `requested-pinned`.
- **A-002: QUALIFY.** A transcript file path is a workable input, but every cited reader is a headless run and the interactive path is unshown; unit tests need a committed synthetic fixture (N-B9, N-B10).
- **A-003: REJECT.** "One sidechain is one reviewer attempt with one served id" is unsound as stated; the design keys on tool-use id, keeps `served_ids`, nulls `model_observed` when ambiguous and joins by Agent-call description, never by order.
- **A-004: QUALIFY.** The orchestrator must still call `ingest` (and pass `--events` in the loop), but `ingest` is idempotent with no order precondition and a skipped call shows as `record_absent`.
- **A-005: QUALIFY.** `fcntl` is POSIX-only; sound only with a lazy import, a blocking timed acquire, a CLI-level span and a legacy fallback when unavailable.
- **A-006: QUALIFY.** `<out>/panel/events.jsonl` exists where a panel directory exists; the loop uses `--events` and `export` has no cwd-relative default directory.
- **A-007: QUALIFY.** One row per agent is the right grain only with a partition test (each sidechain in exactly one row, rows sum to the total) and the permuted-order join case.
- **A-008: QUALIFY.** The `superclaude` command can be absent (the loop prompt says so); the gap must be visible through `record_absent` and `panel_fallback_reason`, not silent.
- **A-009: QUALIFY.** Interleaved lines on the cross-run file are unproven; a telemetry lock is justified only by a reproduced race, and none exists, so none is added; the events lock stands on idempotent ingest and `seq`.

Status: Complete

