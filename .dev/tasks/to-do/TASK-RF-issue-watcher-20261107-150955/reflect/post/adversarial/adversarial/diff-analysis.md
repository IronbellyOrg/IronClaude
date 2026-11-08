# Diff Analysis: Reflect reviewer deviation-card Comparison

## Metadata
- Generated: 2026-11-08T05:00:00+00:00
- Variants compared: 3 (variant-1-original.md, variant-2-original.md, variant-3-original.md)
- Total differences found: 57 (8 structural + 39 content + 10 contradictions)
- Categories: structural (8), content (39), contradictions (10)
- Focus areas: correctness, coverage, deviation-classification

## Structural Differences

Variant 1 = reviewer 1 (sonnet, analyzer, calibrated C = 0.70). Variant 2 = reviewer 2 (haiku, qa, C = 0.82). Variant 3 = reviewer 3 (opus, refactorer, C = 0.76). C values are carried as context only, not as truth.

| # | Area | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|------|-----------|-----------|-----------|----------|
| S-001 | Audit slice (what "spec units" means) | 38 units: FR-001..FR-029 plus 9 safety groups, self-labelled an estimate | 13 units: 12 assigned acceptance criteria plus the task's no-skip rule | 18 units: NFR-001..NFR-014 plus design 5.3, 5.4, 4.1, 4.3 | High (the slices barely overlap, so a card's silence on a topic is not agreement) |
| S-002 | Verdict | No verdict; headline "only MEDIUM item is the exit-code and reason-table drift" | Explicit **FAIL**, with a DONE/NEXT table and two blocking rows | No verdict | Medium |
| S-003 | Deviation-row count and mix | 12 rows: Authorized 3, Necessary 4, Drift 5, Regression 0 | 5 rows: Authorized 2, Necessary 1, Drift 1, Regression 1 | 11 rows: Authorized 1, Necessary 4, Drift 6, Regression 0 | Medium |
| S-004 | Advisory correctness-gap table | 13 gaps | None | 5 gaps | Medium |
| S-005 | Evidence provenance | Several rows rest on Tier-1 brief rows (C1a, C1b, C3b, C4a, C5); card says it did not read the decision register, OQ text, tests or spec-final.md | Reads tests, task file, research/06 and gate summaries directly; absolute paths | Reads design and runbook directly; admits `runner.py` and `main.py` citations come from pre-compaction reads | Medium |
| S-006 | Self-consistency of counts | Header says "1 MEDIUM, 11 LOW" but rows 1 and 2 are both MEDIUM (calibration confirms) | Consistent | Consistent; row 6(c) cites design :115 but not design :726, which lists status exits 0/1/6 | Low |
| S-007 | Recommendations | None | One recommended action (fix rows 1 and 2, add a slow-save test) | None, except the "do NOT consolidate `_fsync_dir`" guidance inside row 10 | Low |
| S-008 | Self-audit of adherent areas | Notes on at-most-once, prompt text, time windows | Acceptance-test assessment, runtime registration, verification claims | Itemized "checked and found adherent" list plus 13 runbook claims | Low |

## Content Differences

One row per finding topic. Cell format: category, severity, card row (D = deviation row, G = correctness gap, N = notes). "Silent" means the card does not address the topic. Severity column = the highest severity any card gives.

| # | Topic | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|-------|-----------|-----------|-----------|----------|
| C-001 | `cycle_crashed`, `once` exit 1 (`cli.py:35,123-129`, `audit.py:55-57`) | Necessary deviation, MEDIUM (D1, bundled with `cycle_complete`) | Silent | Drift, MEDIUM (D1) | Medium |
| C-002 | `cycle_complete` reason (`cycle.py:1134-1137`, `audit.py:62-64`) | Necessary deviation, MEDIUM (D1, bundled) | Silent | Necessary deviation, LOW (D7) | Medium |
| C-003 | Design 4.3/10.1 and spec never amended for the added names (code 59, spec 52, runbook 59) | Drift, MEDIUM (D2); also "AC-17 arguably contradicted for exit 1" | Silent | Not a row; N "evidence pathologies": "the 57-reason count in the spec and tasklist is stale" | Medium |
| C-004 | Five DF-authorized reasons beyond the spec (`marker_unreadable`, `edits_unreadable`, `dry_run_shadow_reset`, `reset_refused`, `operator_reset`) | Authorized expansion, LOW (D10; register not read) | Silent | Silent (only the 59 total in N) | Low |
| C-005 | `record` imports predicate functions (`record.py:23-29`) | Authorized expansion, LOW for 3 functions (D8) plus Necessary deviation, LOW for `valid_operation_id` (D9) | Authorized expansion, LOW (D5, located at `test_module_boundaries.py:57`) | Drift, LOW (D2: 4 functions + `ApprovalResult`, absolute import, docstring miscount) | Low |
| C-006 | `cli` reaches `predicates.format_utc` via `cycle.format_utc` (`cli.py:319`) | Drift, LOW (D4) | Silent | Drift, LOW (D5) | Low |
| C-007 | Duplicated issue-number bound 999_999_999 (`predicates.py:20`, `launch.py:30`, `audit.py:203`, `record.py:132`) | Drift, LOW (D5) | Silent | Necessary deviation, LOW (D10, forced by design 5.3) plus G2 (no parity test for `launch` copy) | Low |
| C-008 | Duplicated login regex (`cycle.py:468` vs `github.py:134`) | Drift, LOW (D5) | Silent | Drift, LOW (D3) plus G2 | Low |
| C-009 | Duplicated UTC format (`cycle.py:76` vs `predicates.py:23`; `audit.py:200`) | Silent | Silent | Drift for the `cycle` copy (D3); Necessary for the `audit` copy (D10) | Low |
| C-010 | `OPERATION_ID_PATTERN` twice (`predicates.py:57`, `launch.py:36`) | Necessary deviation, LOW (D7) | Silent | Silent | Low |
| C-011 | `_fsync_dir` and `_ENTRY_STATES` copies (`record.py:310-315`, `audit.py:110-115,204-206`) | Silent | Silent | Necessary deviation, LOW (D10, explicit "do not consolidate"); G2 `_ENTRY_STATES` pinned to a literal, not to `record.ENTRY_STATES` | Low |
| C-012 | Wall-clock reads vs NFR-014 (`audit.py:395-397` `stderr_fallback`; `runner.py:89-129` `time.monotonic`) | Drift, LOW for both, alternative reading "NFR-014 regression, behaviour-neutral" (D6) | Silent | `stderr_fallback`: Drift, LOW (D4); `runner` monotonic: Necessary deviation, LOW (D9) | Low |
| C-013 | Root-dependent and platform skips (`test_cli.py:967,1070`, `test_record.py:739`, `test_cycle.py:735,4694`) | Necessary deviation, LOW (D12; tests not read) | Drift, MEDIUM, **blocking** (D2) | Silent | Medium |
| C-014 | Late launch after the pending save (design :647; `cycle.py:1048-1062`) | No row (N: save-before-launch order confirmed for at-most-once; Regression 0) | Regression, HIGH, **blocking** (D1) | Silent | High |
| C-015 | DISABLED checked before the origin call, not re-checked before `mark_pending` | G3 (cites `cycle.py:308`; calibration says 693 and 1033) | Silent | N: "DISABLED is checked first under the lock" at `cycle.py:693-694`, adherent | Low |
| C-016 | Day cap fails open after a backward clock step (`record.py:689-703`) | G3-class advisory G1, "possibly MEDIUM (inferred)", design-conformant | Silent | Silent | Medium (inferred) |
| C-017 | Dangling DISABLED symlink: `disabled()` vs `disabled_since()` (`record.py:421-431`) | G2: status says "disabled since: no"; non-FileNotFound OSError escapes | Silent | G1: same, plus ELOOP gives traceback and exit 1 (read as unhealthy), contradicting runbook `setup.md:298,302` | Low |
| C-018 | Exception other than `_Stop` after the spawn skips `_commit` (`cycle.py:685-690`) | G4: entry left `pending`, id and retry hint lost, no audit line | Silent | No row (runbook claim 6 "cycle_crashed behaviour" checked adherent) | Medium |
| C-019 | Pipe hang on real Orca (`runner.py:91-101`, 120 s timeout) | G5, inferred, not testable with stubs | Silent | Silent | Medium (inferred) |
| C-020 | Dead code (`MAX_LAUNCHES_PER_CYCLE`, `record.disabled_present`, `status_report` audit arg, `CommandResult.duration_s`) | G6 | Silent | D9 notes `duration_s` is never read | Low |
| C-021 | `mark_pending` checks state, not `launches == 0` (`record.py:538-568`) | G7, safe today via `validate` | Silent | Silent | Low |
| C-022 | Same-second trigger and approval events stay `events_incomplete` forever (`predicates.py:205-209`) | G8 | Silent | Silent | Medium |
| C-023 | `OSError` after spawn classified `spawn_error` (`launch.py:318-319`) | G9, triage only | Silent | Silent | Low |
| C-024 | Exit-0 reply carrying `error.operation_id` accepted as `launched` (`launch.py:326-334`) | G10 | Silent | Silent | Medium |
| C-025 | Operation-id pattern allows a leading `-` before shell printing (`predicates.py:57`) | G11 | Silent | N: "`retry_argv` validates the operation id before `status` prints it", adherent | Low |
| C-026 | Stderr 500-byte cap vs `agent_session_operation_unknown` search (`runner.py:15,63`; `launch.py:322`) | G12, inferred | Silent | Silent | Medium |
| C-027 | Approvers file: `lstat` then `open(O_NOFOLLOW)` with no `fstat`; parent dir mode unchecked | G13 (card finding, not confirmed line by line) | Silent | Silent | Low |
| C-028 | Unreachable `re-approved` note branch (`cycle.py:635-641`) | Drift, LOW (D3) | Silent | Silent | Low |
| C-029 | Seven anchored departures (dry-run skips, Retry-After on user call, full retry argv, halt on any launch outcome, `cwd=worktree`) | Authorized expansion, LOW (D11; DF text not read) | Silent | N: "the launch is the only call that passes `cwd`", adherent | Low |
| C-030 | Multi-day acceptance test reads "the rest launch" as further rolling caps (`test_cycle.py:4150-4154`) | Silent | Necessary deviation, LOW (D3) | Silent | Low |
| C-031 | Local gate runs affected subsets, full suite deferred to CI | Silent | Authorized expansion, LOW (D4, DF-05) | Silent | Low |
| C-032 | Eager registration of `issue_watch_group` in `main.py` vs design "lazily" | Silent | Silent | Authorized expansion, LOW (D11, DF-29/OQ-21; path wrong, real file `src/superclaude/cli/main.py:563-565`) | Low |
| C-033 | `cycle` reads private `launch._ORCA_CLIS` (`cycle.py:1227,1230`) | Silent | Silent | Necessary deviation, LOW (D8; calibration: closer to aligned) | Low |
| C-034 | Runbook platform list, `reset` exit 2, `status` exit codes (`setup.md:53,432`; `cli.py:84-91,314`) | Silent | Silent | Drift, LOW (D6; part (c) ignores design :726 which itself lists status 0/1/6) | Low |
| C-035 | `reset --rate-limit --forfeit-guarantee` accepted; "not both" message also used for neither (`cli.py:310-311`) | Silent | Silent | G3 | Low |
| C-036 | Retry list silently drops `unknown` entries lacking `launch_cwd` or with an id `retry_argv` refuses (`cycle.py:1271-1280`) | Silent | Silent | G4 | Medium |
| C-037 | `stderr_fallback` checks reason membership but not exit, and always writes `"kind": "cycle"` (`audit.py:393-402`) | Silent | Silent | G5 | Low |
| C-038 | Boundary test docstring says "three functions and one type" (`test_module_boundaries.py:20-21`) | Silent | Silent | Part of D2 and N | Low |
| C-039 | Command wiring and subprocess coverage (`main.py:563`) | Silent | N: wiring correct; only `init-state` and `once` have real-subprocess tests | N: five commands match runbook | Low |

## Contradictions

Each row names the dispute, each card's position, and one line of what the cited source actually says (read from disk for this analysis). Disputes are recorded, not resolved.

| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Variant 3 Position | Source (verified) | Impact |
|---|-------------------|--------------------|--------------------|--------------------|-------------------|--------|
| X-001 | Is `cycle_crashed` / `once` exit 1 a Necessary deviation or Drift? | Necessary deviation, MEDIUM (an uncaught exception needs some exit; the gap was not invented) | Silent | Drift, MEDIUM (design gives a crash no exit 1 and no reason) | `cli.py:35` `_EXIT_CRASH = 1  # [PROPOSAL] C-3: an unexpected exception out of the cycle`; `docs/designs/issue-watcher.md:114` lists `once` exits as "0, 2, 3, 4, 5, 6, 7, 75" | Medium |
| X-002 | Severity of `cycle_complete` | MEDIUM (bundled in D1 with `cycle_crashed`) | Silent | LOW (D7, standalone) | `cycle.py:1137` `return "cycle_complete"`; design:157 exit-0 row does not list `cycle_complete` | Low |
| X-003 | `record` importing predicate functions: authorized or Drift? | Authorized for 3 functions (PRE-11, tasklist :332) plus Necessary for `valid_operation_id` | Authorized (tasklist :332) | Drift (4 functions + `ApprovalResult`, beyond both design and tasklist) | `record.py:23-29` imports `ApprovalResult, format_utc, parse_utc, valid_issue_number, valid_operation_id`; design:239 says `predicates` "(types only...)"; tasklist :332 permits `parse_utc`, `format_utc`, `valid_issue_number` | Medium (three cards, three answers; the code imports more than the tasklist allowed) |
| X-004 | Duplicated issue-number bound: Drift or forced by design 5.3? | Drift, LOW | Silent | Necessary deviation, LOW | `audit.py:203` `_MAX_ISSUE = 999_999_999  # the same bound as predicates.MAX_ISSUE_NUMBER`; `launch.py:30` `MAX_ISSUE_NUMBER = 999_999_999` | Low |
| X-005 | `runner` timing with `time.monotonic` vs NFR-014 | Drift, LOW (alternative reading: behaviour-neutral NFR-014 regression) | Silent | Necessary deviation, LOW (a subprocess timeout needs a real clock) | `runner.py:89` `start = time.monotonic()`; spec-final.md:231 NFR-014 routes every time read through the clock | Low |
| X-006 | Root and platform test skips | Necessary deviation, LOW (did not read the tests) | Drift, MEDIUM, blocking | Silent | Task file :188 "No test may use `pytest.skip`, `skipif` or `xfail`, because gates G-1 and G-3 require zero skipped tests."; `test_cli.py:1070` `NOT_ROOT = pytest.mark.skipif(os.geteuid() == 0, reason="root ignores file modes")`; `test_cycle.py:4694` `pytest.skip("/proc/self/mountinfo exists on Linux only")` | Medium |
| X-007 | Launch path after the pending save: adherent or Regression? | Adherent: Regression count 0; notes confirm save-before-launch for at-most-once (cited 335-337, actual 1060-1062) | Regression, HIGH, blocking: no deadline check between save and launch | Silent | `cycle.py:1048` `if not self.deadline.launch_allowed(): raise _Skip("budget_exhausted")`; `cycle.py:1061` `self._save()  # FR-010: durable before the launch call`; `cycle.py:1062` `outcome = d.launcher.launch(orca, cfg.worktree, prompt, LAUNCH_TIMEOUT_S)`; design:647 Orca launch "not started when `elapsed() > 120`; the step ends with no entry..." | High (the cards looked at different properties of the same lines: V1 at FR-010 ordering, V2 at the design 647 cutoff) |
| X-008 | Operation-id shell safety before `status` prints a retry command | G11: pattern lets an id start with `-` | Silent | Adherent: `retry_argv` validates the id first | `predicates.py:57` `OPERATION_ID_PATTERN = re.compile(r"^[A-Za-z0-9._:-]{1,128}$")`; `launch.py:127-130` `retry_argv` validates against that pattern | Low |
| X-009 | Where DISABLED is checked in a cycle | G3: "checked once" at `cycle.py:308`, not re-checked before `mark_pending` | Silent | Checked first under the lock at `cycle.py:693-694`, adherent | `cycle.py:693` `if self.deps.store.disabled(): raise _Stop("disabled")`; `cycle.py:1033` `if d.store.disabled(): raise _Stop("disabled_mid_cycle", stamp=True)` (a second check exists; V1's line is wrong) | Low |
| X-010 | Reason count in the spec and tasklist | Spec has 52; code 59 adds 7 | Silent | "the 57-reason count in the spec and tasklist is stale" | Task file :199 "exactly 57 entries (52 from spec lines 332-358 plus the five proposals above)"; `setup.md:344` "only the 59 names"; 59 names counted in `audit.py:26-101` | Low |

## Unique Contributions

Value assessment: High = could change the verdict; Medium = a real behaviour or test gap worth a fix decision; Low = hygiene or documentation.

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | Variant 2 | Late-launch Regression: no deadline check between the pending save (`cycle.py:1061`) and the launch (`cycle.py:1062`), against design :647 (C-014) | High (only blocking HIGH item; calibrator questions severity and the card's fix) |
| U-002 | Variant 2 | Direct reading of the skip expressions and the task's no-skip ban, counted as 6 functions / 7 cases (C-013) | Medium (V1 mentions skips but did not read the tests) |
| U-003 | Variant 2 | Multi-day acceptance test interpretation of "the rest launch" (C-030) | Low |
| U-004 | Variant 2 | Local gate used affected subsets, full suite deferred to CI (DF-05) (C-031) | Low |
| U-005 | Variant 2 | Subprocess coverage only for `init-state` and `once` (C-039) | Low |
| U-006 | Variant 1 | Design and spec never amended for the added reasons and exit 1, a Drift row of its own (C-003) | Medium |
| U-007 | Variant 1 | Day cap fails open after a backward clock step (C-016) | Medium |
| U-008 | Variant 1 | Exception other than `_Stop` after the spawn skips `_commit`, leaving the entry `pending` (C-018) | Medium |
| U-009 | Variant 1 | Pipe hang on real Orca, inferred (C-019) | Medium (unverified) |
| U-010 | Variant 1 | Dead code list (C-020) | Low |
| U-011 | Variant 1 | `mark_pending` does not check `launches == 0` (C-021) | Low |
| U-012 | Variant 1 | Same-second events stay `events_incomplete` (C-022) | Medium |
| U-013 | Variant 1 | `OSError` after spawn labelled `spawn_error` (C-023) | Low |
| U-014 | Variant 1 | Exit-0 reply carrying `error.operation_id` accepted as `launched` (C-024) | Medium |
| U-015 | Variant 1 | Leading-dash operation id (C-025) | Low (V3 disputes, X-008) |
| U-016 | Variant 1 | Stderr 500-byte cap may hide the operation-unknown marker (C-026) | Medium (inferred) |
| U-017 | Variant 1 | Approvers file opened without `fstat` (C-027) | Low (unconfirmed) |
| U-018 | Variant 1 | Unreachable `re-approved` branch (C-028) | Low |
| U-019 | Variant 1 | `OPERATION_ID_PATTERN` duplicate classified (C-010) | Low |
| U-020 | Variant 1 | Bundle of seven DF-anchored departures (C-029) | Low (DF text not read) |
| U-021 | Variant 1 | Five DF-authorized extra reasons named individually (C-004) | Low |
| U-022 | Variant 3 | Runbook platform list, `reset` exit 2, `status` exit codes (C-034) | Low (part (c) conflicts with design :726) |
| U-023 | Variant 3 | `cycle` reads private `launch._ORCA_CLIS` (C-033) | Low |
| U-024 | Variant 3 | Eager command registration vs design "lazily" (C-032) | Low (cited path wrong) |
| U-025 | Variant 3 | `reset` accepts both flags; one message for both and neither (C-035) | Low |
| U-026 | Variant 3 | Retry list silently drops `unknown` entries (C-036) | Medium |
| U-027 | Variant 3 | `stderr_fallback` does not check the exit and always writes kind `cycle` (C-037) | Low |
| U-028 | Variant 3 | UTC format duplicate (C-009) and `_fsync_dir` / `_ENTRY_STATES` copies with "do not consolidate" advice (C-011) | Low |
| U-029 | Variant 3 | Boundary-test docstring miscount (C-038) | Low |
| U-030 | Variant 3 | ELOOP on the DISABLED path gives a traceback and exit 1, against runbook `setup.md:298,302` (part of C-017) | Low |
| U-031 | Variant 3 | No parity tests pinning copied constants to their source (G2) | Medium |
| U-032 | Variant 3 | Itemized "checked and found adherent" list plus 13 runbook claims | Medium (only card that records negative evidence per area) |

## Shared Assumptions

| # | Assumption | Held by | Classification | Note |
|---|------------|---------|----------------|------|
| A-001 | The executor registers (DF, OQ, PRE entries in `research/06-gap-fill-decisions.md` and the task file) are authoritative for "Authorized expansion" | All three | UNSTATED | V1 classifies from them without reading the register; V2 reads DF-05 directly; V3 cites DF-29/OQ-21 |
| A-002 | A `[PROPOSAL]` comment by the executor (for example `cli.py:35`, `audit.py:55-57`) counts as authority for the departure | V1 yes (Necessary), V3 no (Drift) | CONTRADICTED | Root of X-001 and X-002 |
| A-003 | Classification is made against the design and spec text, with the tasklist as an amending layer | All three | STATED | V2 and V3 cite design lines directly; V1 cites spec FR numbers |
| A-004 | The cards' line citations are correct | All three | CONTRADICTED | Calibration and this analysis found V1 `cycle.py:335-337` (real 1060-1062) and `cycle.py:308` (real 693, 1033); V3 `src/superclaude/main.py:563-565` (real file `src/superclaude/cli/main.py`, same lines); V2 one line off (`p9-g2-summary.md:9`, not :8) |
| A-005 | No tests or commands were run; findings come from reading source | All three | STATED in V2 (":55 no tests or commands were run"); UNSTATED in V1 and V3 | V1 and V3 inferred findings (pipe hang, stderr cap) carry no runtime check |
| A-006 | The diff `e8db2fe6..26f551f4` is the full change under audit | All three | STATED | Header of each card |
| A-007 | The Orca reply shape (`receipt.operation_id`, `error.operation_id`) is as the code assumes | V1 (C-024), V3 (adherent launch checks) | UNSTATED | `launch.py:39-45` marks `OPERATION_ID_PATHS` `[PROPOSAL, UNVERIFIED]` |
| A-008 | Precedence when spec and design disagree | All three | UNSTATED | V3 D6(c) cites design :115 but not :726, which conflict on `status` exits |
| A-009 | The three persona slices together cover the change | Orchestrator framing, implicit in all three | UNSTATED | S-001: slices of 38, 13 and 18 units barely overlap, so silence is not agreement |
| A-010 | Calibrated confidence below 0.85 for all three cards | Calibrator annotations | STATED | Context only (0.70, 0.82, 0.76); not used as truth here |

## Summary

- **Total structural differences**: 8 (S-001..S-008)
- **Total content differences**: 39 (C-001..C-039)
- **Total contradictions**: 10 (X-001..X-010)
- **Total unique contributions**: 32 (U-001..U-032: Variant 1 16, Variant 2 5, Variant 3 11)
- **Total shared assumptions surfaced**: 10 (A-001..A-010: STATED 3, UNSTATED 5, CONTRADICTED 2; A-005 is STATED in V2 and UNSTATED in V1 and V3, counted as STATED)
- **Highest-severity items**:
  - X-007 / C-014 / U-001 (High): late launch after the pending save. V2 Regression HIGH blocking; V1 calls the same lines adherent; source at `cycle.py:1048-1062` and design :647.
  - S-001 (High): the three audit slices barely overlap, so a card's silence on a topic is not agreement.
  - X-001 / C-001 (Medium): `cycle_crashed` and `once` exit 1, Necessary (V1) vs Drift (V3).
  - X-006 / C-013 (Medium): test skips against the task's no-skip ban, Necessary LOW (V1) vs Drift MEDIUM blocking (V2).
  - X-003 / C-005 (Medium): `record` predicate imports, three different classifications across three cards.
  - C-003 (Medium): design and spec not amended for 59 reasons and exit 1 (V1 only).
- Disputes are recorded only; resolution belongs to the debate step.
