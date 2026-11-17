# Adversarial Debate Transcript

## Metadata
- Depth: quick
- Rounds completed: 1 (Round 1 parallel advocate statements). Round 2 skipped: depth=quick. Round 2.5 (invariant probe) skipped: --depth quick. Round 3 skipped: depth=quick.
- Convergence achieved: 93.4% (57 of 61 diff points)
- Convergence threshold: 80%
- Focus areas: All
- Advocate count: 3
- Full advocate statements (verbatim, with every citation): `round1-advocate-1.md`, `round1-advocate-2.md`, `round1-advocate-3.md` in this folder. Each advocate re-read the live files, did not run pytest/ruff/uv, and answered all five shared assumptions. No `[OMISSION]` flags: every advocate addressed A-001 through A-005 and every C- and X- point.
- Taxonomy coverage gate (AD-5): L1 (13 points), L2 (21 points), L3 (23 points) were all addressed by all three advocates; no forced round needed.
- Orchestrator fact checks after Round 1 (read-only, neutral): test_view.py:864-869; pyproject `--strict-markers`; test_fixtures.py:25-30 and :226-230; test_golden_contract.py:206-216, 508-527; `CODES` grep; `count_text` grep; `unrecognised_keys` grep; export/SCHEMA imports; test_terminal.py:56-82; owner-decisions-20261111.md; SPEC.md:96-114; owner-decisions-and-risks.md:13-26; `git status --short src tests` (clean, HEAD f104ca51a). Results are folded into the scoring notes below.

## Round 1: Advocate Statements

### Variant 1 Advocate (opus:architect, ponytail maximalist) -> `round1-advocate-1.md`
**Position**: Strongest on dead code and real duplicates other variants kept (`adapter.CODES`, the no-blink copy in test_terminal.py, the redundant T51 spy test, T3/T4 scopes); conceded 16 matrix points after finding that its own T7 merge would fail on long-identifiers.json and its S2 scope would delete `SCHEMA_VERSION`.

**Steelman of Variant 2**: a cut is safe only when the surviving guard is shown, not assumed; found the T7 extras are not duplicates, R9 has no question-path tests, D1 must not collapse lists, S3's target is untracked.

**Steelman of Variant 3**: gives CUT only when every claim verifies; found R3's two dead aggregates, S2's `SCHEMA_VERSION`, S1 needs no golden regeneration, D6's current folder.

**Key strengths claimed**:
1. `CODES` has no production reader (adapter.py:66-82; comment :340; only test_adapter.py:719); :718 already pins the exact code.
2. R1 test ranges swallow the T28 no-blink test (test_terminal.py:65-70) and T11/T12 tests; test_fixtures.py:139-151 must be rewritten through `parse_page` + `apply_frozen`.
3. T9: delete the test_terminal copy (test-chosen styles on a bare console), keep test_render.py:182-190 (real screen, every width).
4. R4 "smaller option" is unsound: the `e` record (export.py:65-80) lacks the inspector fields.
5. T5 :148-171 duplicates assertions the fake makes on every call (test_question_quiet_scope.py:68-76) and `reads == 6` at :142.

**Weaknesses identified in Variants 2 and 3**: V2 R2 KEEP ignores the dead `count_text`; V2 T9 keeps a test of Rich, not of the observer; V3 T3 cuts spec pass criteria; V3 T6 cuts the only single-Console guard; V3 D1 pointer would orphan OQ-n labels (defined only in prd.md 12.1).

**Concessions**: R3 (V3), T7 (V2), S2 (V3), S6 (V3), D1 (V2), D6 (V3), D8 (V3), R2 comment edit, D7 keep list, S3 facts, R9 reason.

### Variant 2 Advocate (sonnet:qa, guard protector) -> `round1-advocate-2.md`
**Position**: Protects guards and the live files back it on CODES circularity, S6 ordering, D6 current folder, untracked-source rules, R10, T8; conceded 15 points where it over-kept (R2 `count_text`, R3 aggregates) or where the right framing is an owner question.

**Steelman of Variant 1**: only variant that turns "very low risk" into an executable symbol-level edit list and caught that R1 plus T9 together delete both no-blink tests.

**Steelman of Variant 3**: refuses CUT until every claim verifies; its R3 and S2 findings are exact.

**Key strengths claimed**:
1. `CODES` is the only closed-set pin; moving it into the test makes the assert circular.
2. S6 replacement sentence false: rows sorted newest first (view.py:842; :274).
3. S3/D4 touch untracked sources; write-back files not byte duplicates (5,069 vs 8,271 bytes).
4. D6 premise wrong: ux-orca-observer is current (updated 2026-11-12).
5. R9 has no question-path tests (RunnerFailure, OSError, overrun) so "behaviour identical" cannot be shown.

**Weaknesses identified in Variants 1 and 3**: V1 D8 row numbers off by one; V1 R3 unworkable (split `_FIELDS`); V3 T6 cuts guards (test_terminal.py:214-231); V3 T3 cuts the burst test that drives the production `KeySource`; V3 R9 optimistic.

**Concessions**: R2 (`count_text` dead), R3 (aggregates), R4 (owner), T2, T3 (resize only), T4, T5, T9, S2, S3, S5, D4, D6, D8, D9 (15 points).

### Variant 3 Advocate (opus:analyzer, evidence auditor) -> `round1-advocate-3.md`
**Position**: Fact corrections hold (R3 aggregates, S2 `SCHEMA_VERSION`, S1 needs no golden regeneration, T10 runs 8 variants, D1 is decisions 6 and 8, D6 current folder), but conceded 20 points: too eager on test cuts (T3, T5, T6, T9, T2, T7) and wrong on three facts of its own (X-004, X-005, S3 reference count).

**Steelman of Variant 1**: tested R4's smaller option against the code; saw the burst/resize spike criteria (ARCHITECTURE-SPINE.md:154); kept test_terminal.py:214-231 (single `Console`, markup off); caught rendering-rules.md:89.

**Steelman of Variant 2**: found R9's untested question path; saw CODES circularity; took the narrowest safe T7 scope; saw T2 :596 is a privacy check.

**Key strengths claimed**:
1. R3: pure-deletion cut of two never-read aggregates (parse.py:177, 195, 409, 647); `_BLOCK_FIELDS` (:91-93) is sanitizer block mode.
2. S2: `SCHEMA_VERSION` (export.py:23) is used at :195; also `resources` (export.py:14) goes, else ruff F401.
3. S1: golden has 0 `"questions"` keys; no regeneration needed.
4. D2: union of stale spots incl. prd.md:106, :491, adapter-contract.md:3, rendering-rules.md:89, commands.py:452-453.
5. T10 runs 8 variants; D1 stale decisions are 6 and 8.

**Weaknesses identified in Variants 1 and 2**: V1 T7 merge breaks on long-identifiers.json; V1/V2 S2 removes `SCHEMA_VERSION` (NameError at export.py:195); V1 D8 rows off by one; V2 R2 and R3 KEEP ignore dead code; V2 S5 KEEP treats an open question as settled.

**Concessions**: T3, T5, T6, T9, T2, T7, T4, R4, R9, S3, S6, X-001, R2 comment, S2 `resources`, D2, D8 (16 numbered, 20 matrix points).

## Round 2: Rebuttals
Skipped: depth=quick.

## Round 3: Final Arguments
Skipped: depth=quick.

## Scoring Matrix

Winner = the variant whose position the post-debate result matches (SYNTH = blend; all = unanimous). Confidence is the median of the supporting advocates' stated confidences (mean of two). Orchestrator fact checks are noted where they changed an input.

| Diff Point | Winner | Confidence | Evidence Summary |
|---|---|---|---|
| C-001 R1 | SYNTH (V1+V3; V2 on stub) | 80% | Zero production callers of every listed symbol; `CODES` deleted with test_adapter.py:719 (2 of 3; V2 dissents, :718 pins the exact code); read_questions stub kept (CycleSource). |
| C-002 R2 | V1+V3 | 80% | `count_text` only at view.py:209, :732 (orchestrator grep confirms no test reader). |
| C-003 R3 | V3 | 75% | Aggregates at parse.py:177/195/409/647 never read (orchestrator grep confirms); five fields stay (`_KNOWN` built from `_FIELDS`). |
| C-004 R4 | V1+V3 | 72% | KEEP: `e` record lacks inspector fields (export.py:65-80); spec/doc contradiction goes to the owner as a note, not a cut. |
| C-005 R5 | all | 80% | Rewrite must stay byte-identical for T47; no behaviour gain. |
| C-006 R6 | all | 75% | Only T47 golden pins the 2-line cap; plain wrap changes bytes. |
| C-007 R7 | all | 80% | About 15 lines for large test churn. |
| C-008 R8 | all | 85% | Constant pinned by test_commands.py:743-745 and the release-gates control. |
| C-009 R9 | V1+V2 | 70% | Question-path RunnerFailure/OSError/overrun untested. |
| C-010 R10 | all | 90% | `evicted_keys` fixes the double count (2083db2ae). |
| C-011 T1 | all | 80% | Only release-1 byte proof; golden cannot be regenerated from current code. |
| C-012 T2 | SYNTH (intersection) | 65% | Scope split: V1 cuts :333-366 and :596-638, V3 cuts :333-365 only, V2 defers; no 2/3 on exact scope. |
| C-013 T3 | V1+V3 | 72% | Burst/resize are written spike criteria (ARCHITECTURE-SPINE.md:154); V3 conceded. |
| C-014 T4 | V1+V3 | 65% | :258-278 and :291-297 unanimous; :226-230 contested. |
| C-015 T5 | V1 (+V3 concession) | 70% | :148-171 redundant with the fake's own argv assertion; V2 dissent: independent argv log. |
| C-016 T6 | SYNTH | 68% | test_view.py:864-869 excluded: orchestrator read shows it is the only check that export.py/render.py do not import `observe.parse`. |
| C-017 T7 | V2 | 75% | Only the duplicated SENSITIVE loops; the 32-char rule cannot move (long-identifiers.json). |
| C-018 T8 | all | 89% | Fix `or True`; 27 cases are the spec's T16. |
| C-019 T9 | V1+V3 | 70% | Delete the test_terminal copy (test-chosen styles); keep test_render.py:182-190. |
| C-020 T10 | all | 75% | Redaction per variant; 8 variants not 10. |
| C-021 S1 | V1+V2 | 70% | Additive-only rule (schema.json:4, owner-decisions-20261108.md:17): owner question. |
| C-022 S2 | V3 | 77% | Keep `SCHEMA_VERSION` (:23, used :195); remove `resources` (:14), `Draft7Validator` (:18), :24-25, :29-34. |
| C-023 S3 | V1+V2 | 88% | Not byte duplicates; target folder untracked. |
| C-024 S4 | all | 85% | Fields on screen (view.py:513-514, 905) and in the T47 golden (5 each). |
| C-025 S5 | all | 75% | UX-OQ-4 open owner question. |
| C-026 S6 | V2+V3 | 74% | Replacement text false (view.py:842); Options table is the only tracked record. |
| C-027 D1 | V2 | 70% | Median 65 + 5: orchestrator read of owner-decisions-20261111.md closed V2's stated reservation (decisions 6 and 8 verified decided). |
| C-028 D2 | SYNTH (union) | 77% | Stale QUESTION-OBSERVATION lines; leave `QUESTION_GATE_TEXT` (pinned test_commands.py:632). |
| C-029 D3 | all | 75% | Tracked, owner decision (rule 3). |
| C-030 D4 | V1+V3 | 85% | Untracked folder; track or archive first. |
| C-031 D5 | all | 75% | Owner decision; handoff-step5.md:6 link. |
| C-032 D6 | V1+V3 | 80% | ux-orca-observer is current; archive question for the owner. |
| C-033 D7 | all | 75% | Owner decision; keep list from V2. |
| C-034 D8 | V2+V3 | 52% | Only :52 supported; confidence below threshold. |
| C-035 D9 | V1+V3 | 75% | handoff-mvp-brainstorm.md untracked. |
| C-036 D10 | all | 75% | Owner's quoted words; release-gates.md:38. |
| C-037 D11 | all | 85% | Issue AC delivery; zip tracked. |
| C-038 D12 | all | 90% | Owner-written record only (rule 4). |
| C-039 D13 | all | 70% | Mark not built, strike nothing. |
| X-001 | SYNTH | 75% | Fact: CODES test-only; moving makes :719 circular; deleting with :719 is safe (:718). |
| X-002 | V1+V3 | 90% | R1 range swallows T28 (:65-70); keep test_render.py:182-190. |
| X-003 | V3 | 85% | Aggregates dead; `_BLOCK_FIELDS` is sanitizer block mode. |
| X-004 | V1+V2 | 70% | Both true: real Collector, but assertions duplicated by the fake. |
| X-005 | V1+V3 | 80% | Burst/resize spec-backed. |
| X-006 | V2+V3 | 92% | ux-orca-observer current. |
| X-007 | SYNTH | 90% | Two different sets (660K/36 files vs archive set). |
| X-008 | V2 | 90% | Not duplicates; target untracked; 19 files reference the name. |
| X-009 | all | 95% | Snapshot sorted by timestamp. |
| X-010 | all | 95% | T16 is 27 renders. |
| X-011 | all | 93% | Evicted-key list needed. |
| X-012 | all | 93% | Stale decisions 6 and 8. |
| X-013 | SYNTH | 88% | R2 rule recorded in EXPERIENCE.md:32-36 (not owner-written); no file holds "2026-11-10". |
| X-014 | all | 99% | 39 IDs. |

## Convergence Assessment
- Points resolved: 57 of 61 (C 38 of 39, X 14 of 14, A 5 of 5, S 0 of 3)
- Alignment: 93.4%
- Threshold: 80%
- Status: CONVERGED (taxonomy gate satisfied; invariant-probe gate not applied at depth quick)
- Unresolved points: C-012 (exact scope split on T2), S-001, S-002, S-003 (structural observations about variant format; no advocate took a position, counted as not agreed to stay conservative)
- Shared-assumption outcomes: A-001 QUALIFY (run pytest and ruff after each cut group; read-only reasoning already failed once: V1 T7, S2), A-002 ACCEPT (2 of 3; spec-named tests T2/T16/T37/T51 stay), A-003 QUALIFY (status fixes citing owner-written records are fine; edits that settle open owner questions are not), A-004 ACCEPT (additive-only rule applies), A-005 QUALIFY (re-grep targets right before each cut; T47 golden cannot be regenerated).
