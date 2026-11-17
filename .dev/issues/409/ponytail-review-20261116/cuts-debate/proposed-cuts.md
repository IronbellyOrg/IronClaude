# Proposed cuts to the Orca observer (issue 409), for adversarial debate

Date: 2026-11-16. Branch 409-Phase2, worktree /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp. Baseline: `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/observe -q` gives 694 passed; `uv run ruff check src/superclaude/cli/observe tests/observe` is clean.

## Where these come from

Four read-only reviewers applied the ponytail lens (smallest change, no work without verifiable return) and wrote reports in /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/ponytail-review-20261116/: runtime-code.md (R items), tests-and-fixtures.md (T items), snapshot-and-future-stages.md (S items), design-docs-and-gates.md (D items). None of them ran any trim. Every claim below is the reviewer's claim; the reviewers marked several UNVERIFIED. Line numbers and "no caller" claims must be re-checked against the live files before any cut is accepted.

"Verifiable return" means one of: an acceptance criterion in /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/issue-body.md, a recorded owner decision (owner-decisions-20261108.md, owner-decisions-20261111.md, owner-pass-record-20261112.md in the same folder), a safety rule that prevents real harm, or behaviour a real user sees.

## Rules that bind every cut (not up for debate)

1. Never weaken: the sanitizer (src/superclaude/cli/observe/sanitize.py and its use), the argv allow-list and forbidden verbs (adapter.py), process-group kill and output caps, terminal restore on exit and signals, "message bodies, payload and to_handle are never kept", snapshot redaction (no subject, body, handle or payload in JSON), the disclosure label `bounded best effort; coverage unknown; bursts over 100 rows between reads may be lost`, and "unknown is never 0 or false".
2. Every cut must name the surviving test or behaviour that still guards the rule it touches.
3. Deleting or moving documents needs the owner's approval; files that are untracked in git cannot be recovered, so no cut may delete them (archive copy first, owner approves).
4. Do not write the owner's records. DIRECTION-SELECTED needs an owner-written selection record; an agent must not write it.
5. After any cut the 694-test baseline must still pass (minus tests deliberately removed with the code they test) and lint must stay clean.

## Verdict vocabulary for the debate

For each item ID: CUT (do now), CUT-SMALLER (a narrower version; say exactly which part), DEFER-OWNER (a decision that belongs to the owner; say which question), or KEEP. Give a confidence in percent and the evidence (file:line you read yourself).

## Items

Paths under /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/src/superclaude/cli/observe/ are written relative as `PKG/`; tests under .../tests/observe/ as `TESTS/`.

### Runtime code (R)

- **R1. Code only tests call (about 85 lines), reviewer says very low risk.** terminal.py:41-53 `PALETTE`, `_FORBIDDEN_ATTRS`, 161-172 `palette_style`; terminal.py:33,37,38 unused glyphs `sep`, `vrule`, `cross`; terminal.py:72-75 `TerminalPolicy.box_style` (keep `safe_box=policy.ascii` in `make_console`); adapter.py:65-82 `CODES` (move the set into the test); collector.py:97-104 and 128-140 `FixtureSource.question_fixture` and `read_questions` (move to a test double; `--questions` with `--fixture` is refused at commands.py:177-178); parse.py:723-733 `Fixture.parse`; questions.py:70-76 `QuestionState.closure_evidence` and `never_read`; commands.py:142 `Deps.extra`. Matching tests go with them (test_terminal.py:57-82 and :126, test_adapter.py:719, test_collector.py:662-669, test_fixtures.py:44,141,149, test_questions.py:46-98).
- **R2. Slim the 22-field coordinator-questions panel model and builder (about 100 lines), reviewer says medium risk.** view.py:52-81, 184-239, 589-744; render.py:304-323, 369-395. The panel itself is required; the claim is that its shape repeats the same facts as several pre-built strings. export.py:103-116 and 160-168 read `empty_text`, `window_full_text`, `notes`, `open_total`, `window_full`, `retained`, `evicted`. Golden text in tests must stay byte-equal. A cited "owner decision 2026-11-12" (oldest questions stay, newer cut with a count; view.py:222-238, render.py:380) was not found in the three owner files.
- **R3. Unrecognised-key counter plus five parsed-but-never-shown row fields (about 42 lines), low to medium risk.** parse.py:91-106, 317-324, count fields at 155, 177, 195, sums at 356, 409, 647, view.py:407 (inspector line "N unrecognised keys"); fields `resource_id`, `ownership_state`, `release_state`, `recovery_attempt_count`, `workspace_kind` (parse.py:65-67, 71, 78, 124-126, 130, 137). No acceptance criterion or owner decision found; the docstring cites AD-7 (not traced).
- **R4. Inspector scroll with d and u (about 35 lines), medium risk, reviewer says ask the owner.** view.py:93, 127, 975-981, 1009-1013; render.py:248-280; TESTS/test_inspector_scroll.py (7 tests). The spec says the inspector has no per-panel scrolling (.dev/issues/409/bmad/architecture-orca-observer/inputs/extract-prd-ux.md:106, rendering-rules.md:13); live-test-guide.md:68 and a release 2 task prompt ask for d/u. Smaller option: clip with one "n more lines, e exports all" line and no state.
- **R5. Table-driven width layouts (about 25 lines), medium risk.** render.py:148-223. The three layouts are required by issue AC 5; only how they are written changes. Golden pinning of column text is unverified. Reviewer says do it only after OQ-14 is answered.
- **R6. Simplify COUNTS strip protected-token and cut logic (about 20 lines), medium risk.** render.py:87-128, view.py:131-133. Denominators must never be cut (issue AC 3); a plain wrap meets that rule but the strip may take 3 or 4 lines at 80 columns. Which spec test pins the 2-line cap was not traced.
- **R7. Consolidate seven `question_*` fields of `CycleResult` into one frozen dataclass (about 15 lines), low to medium risk.** collector.py:55-68, 201-212, 215-254.
- **R8. Remove the permanently open question gate constant (about 13 lines).** commands.py:63-70, 168-170, 185-186. Reviewer: governance, not technical; release-gates.md calls it the control; leave unless the owner says so.
- **R9. De-duplicate the Orca-call error mapping (about 12 lines), low risk.** adapter.py:436-454 and 503-511 into one private helper. Behaviour must stay identical.
- **R10. Drop the evicted-key list in question retention (about 9 lines), low risk.** questions.py:47-50, 129-138. Two recent fix commits (bb1f0431c, 2083db2ae) touched this bookkeeping; the T46 retention bound and the `evicted` integer stay.

### Tests and fixtures (T)

- **T1. Golden whole-screen file from 5 variants to 2 (about 320 JSON lines, optional).** TESTS/golden_release1_surface.json (545 lines), `VARIANTS` in TESTS/release1_surface.py:25, consumer TESTS/test_render.py:616-629. It is the only proof that questions-off output equals release 1 bytes (T47). One commit so far, no churn.
- **T2. Tests of the recorder scripts (about 221 lines, 6 tests).** TESTS/test_golden_contract.py:219-366 and :540-638, covering TESTS/record_golden.py and record_golden_questions.py. If the recorders will be rerun on a real capture keep the test at :282 (about 170 lines saved); if one-shot, the scripts (682 lines) could go too (owner question).
- **T3. Pty key tests (about 170 lines, split unverified).** TESTS/test_keys_spike.py:117-222 and spike_child.py: drop SIGTSTP, resize and burst tests; keep `test_terminal_attributes_restored` (:153) and the decoder tests (:224-270). Test_commands.py:303 also covers restore. Reviewer found no past defect in those paths.
- **T4. Tests of test support and fixture contents (about 150 lines).** TESTS/test_fixtures.py:81-134 and :208-308. Keep :36-72, :139-167, :185-202, :208-218 (subprocess blocker), :310-324.
- **T5. Tests of the fake mailbox (about 64 lines).** TESTS/test_question_quiet_scope.py:148-171, 174-179, 182-189, 192-203. Keep :137 (repeated reads leave the mailbox unchanged).
- **T6. Source-text grep tests (about 79 lines, 6 tests).** TESTS/test_adapter.py:158-192 and :585-589, test_view.py:864-869, test_export.py:238-244, test_terminal.py:214-231, test_collector.py:414-421. They restate how the implementation is written. Keep test_commands.py:578-594 (no subprocess outside the adapter). Note: the plan Task 6 acceptance criterion asked for a static test that `--ack`, `--wait`, `--retry-request`, `--peek` and `run-use` appear in adapter.py only inside the forbidden set (that is the test at test_adapter.py:158).
- **T7. Duplicate leak scans (about 20 lines).** TESTS/test_golden_contract.py:206-216 and :508-521 duplicate TESTS/test_fixtures.py:185-191; move the two extra regexes into the single test.
- **T8. Fix the vacuous assertion and shrink the matrix.** TESTS/test_render.py:95-100 ends in `or True` and can never fail (fix it to `assert len(overflow) == 1`). The 27-case matrix at :80-107 could be 12 cases.
- **T9. No-blink duplicate (9 lines).** TESTS/test_render.py:182-190 repeats test_terminal.py:65-71.
- **T10. Variant parametrization (no lines, about 14 cases).** test_snapshot_schema.py:80 and :297, test_collector.py:372 run all 10 variants; three would do.

### Snapshot export and future stages (S)

- **S1. Drop the `questions` group from the JSON snapshot (about 55 production and schema lines, about 150 test lines), reviewer says low risk but check owner files first.** export.py:160-182 and 209-210; snapshot.schema.json:65-94; TESTS/test_snapshot_schema.py:413-558; assertion edits in TESTS/test_question_cap.py (lines 84, 129, 134); golden file regeneration (unverified how much of it embeds questions). Nothing reads snapshot.json; the group was not in the owner's field list or the snapshot spec doc. The text record (`e` key, `--once`) keeps its question panel. Reviewer did not read owner-decisions-20261111.md and 20261112.md in full.
- **S2. Stop validating the schema at import in production code (about 8 lines), very low risk.** export.py:18 and 23-34 move into TESTS/conftest.py; imports at test_commands.py:34 and test_snapshot_schema.py:15 change.
- **S3. Collapse write-back-future-stage.md to a pointer (about 44 doc lines).** .dev/issues/409/bmad/spec-orca-observer/write-back-future-stage.md duplicates .dev/issues/409/tuibbs-review/write-back-stage.md; keep the file name so about 20 links stay valid.
- **S4. Drop `collection.changedDuringRead` and `collection.duplicatesIgnored` (about 10 lines).** export.py:211-217, snapshot.schema.json:61-62, view.py:180-181 and 569-572, TESTS/test_snapshot_schema.py:368-390, golden file. Keep `collection.state`. Whether the screen shows them is unverified.
- **S5. Make the per-cycle live snapshot write opt-in (about 12 lines, 2-3 tests), reviewer says ask the owner.** commands.py:276-300, 355-369; the spec default destination is still open.
- **S6. Trim snapshot-export-schema.md (about 12 lines).** Delete "Options considered" (:80-91), replace Ordering (:70-74) with "Rows are in ledger order; a consumer sorts" (this removes OQ-12).

### Design documents and gates (D)

- **D1. Replace the three-way copy of open and decided owner questions with one list.** Keep .dev/issues/409/bmad/spec-orca-observer/SPEC.md "Open Questions" as the single list; make owner-decisions-and-risks.md "Open owner decisions" and prd.md 12.1 and 12.3 (lines 415-473) point to it; correct the stale rows in the same edit (decisions 5 and 6 are still listed as open in several copies).
- **D2. Stale status sweep.** prd.md:25, 84, 104, 106, 464, 491; SPEC.md:74; unverified-register.md:27; owner-decisions-and-risks.md:9, 17, 66; handoff-mvp-brainstorm.md:35, 71, 72; adapter-contract.md:3 and :62; commands.py:63 and :87 comment and help text. QUESTION-OBSERVATION lines say "not passed" although it passed on 2026-11-12 (owner-pass-record-20261112.md). DIRECTION-SELECTED lines say "R0 only" although R1 and R2 shipped; fixing those needs the owner's word.
- **D3. Archive the step-5 review rounds.** .dev/issues/409/bmad/final-review/raw, graded, verify, fixes, briefs, progress.md, workflow-input.md, inputs (about 560 KB, 30 files); keep REPORT.md and findings.md. Tracked in git.
- **D4. Brainstorm adversarial rounds and duplicate file.** /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/brainstorms/20261108-132433-orca-observer-mvp/adversarial (about 600 KB); `merged-output.md` is byte-identical to `merged-requirements.md` (78,427 bytes). The folder is untracked in git, so a delete is unrecoverable.
- **D5. Second copy of ARCHITECTURE-SPINE.md (54,129 bytes, byte-identical) plus architecture-orca-observer reviews, inputs and .memlog.md (about 160 KB).** Keep the spec copy; leave a one-line pointer.
- **D6. UX folders.** Keep one of ux-orca-observer or ux-orca-observer-r2-review (about 500 KB of 688 KB in the other); which is current is unverified, probably r2.
- **D7. PRD build scaffolding.** prd-orca-observer extract-*.md, reconcile-*.md, polish-*, adversarial-review.json, review-rubric.md, validation-report.*, .memlog.md (about 175 KB of 260 KB); nothing outside the folder reads them.
- **D8. Eight low-value rows of the unverified register** (proof (a) withdrawn, Q-3, inbox lease fields, human-question row, production-integration reading, stack-table facts, AC-1..AC-10 restated, Orca reply sender).
- **D9. handoff-step1 to 5.md and handoff-mvp-brainstorm.md (17 KB plus).** Snapshots before later decisions; handoff-mvp-brainstorm.md is untracked.
- **D10. Executor-typed twin owner-decisions-20261112.md (1.4 KB).** release-gates.md:38 already calls it history; release-gates.md must be edited in the same change.
- **D11. Binary packages.** orca-observer-design-package.zip (14 MB, a copy of .dev/design/orca-observer-20261106, 52 MB) and attachments (4.3 MB). The issue README links the zip. Owner decision.
- **D12. Collapse the DIRECTION-SELECTED gate.** The gate text says only offline R0 work is allowed, which contradicts the shipped state. Smallest fix per the reviewer: the owner says in one sentence that the staged choice of 2026-11-08 plus the 2026-11-10 authorization satisfies it, recorded in release-gates.md, then drop OQ-1, OQ-2 and the AC-S text. Needs the owner.
- **D13. Fix acceptance-tests.md bookkeeping.** Strike T45 and T50 (not built or reviewer-only), add the snapshot schema test id; T7 and T17 have no test citation (coverage under another name unverified).
