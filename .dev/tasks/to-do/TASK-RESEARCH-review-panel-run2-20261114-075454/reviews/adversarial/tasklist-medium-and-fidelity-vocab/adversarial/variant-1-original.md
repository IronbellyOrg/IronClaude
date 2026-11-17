# Proposal A: slot X-15, tasklist Medium and the fidelity vocabulary

Status: Complete

Slot: X-15 (named C-15 in `synthesis/synth-06-conflict-log.md`); slug `tasklist-medium-and-fidelity-vocab`; conflict ids SV-6, CO-41, C-S3 (tasklist default).
Position: A. Code state read: HEAD `50d4d2b9d`, branch `ironbelly/shadow-runs`, 2026-11-14.
Paths below are repo-relative unless they start with `.dev/tasks/`; `RT` stands for `.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/`.

Evidence tags: [CODE-VERIFIED] = read in the file at HEAD in this session; [CODE-CONTRADICTED] = the document claim differs from the code; [UNVERIFIED] = not re-derived here, or an interpretation.

## 0. Inputs and dependencies

Read: the X-15 row of `RT phase-outputs/discovery/undecidable-conflicts.md` (line 32); `RT synthesis/synth-06-conflict-log.md` (rows C-S3 line 75, SV-6 line 173, CO-41 line 244, slot row C-15 line 376); `RT synthesis/synth-05-options.md` (axis 6.2 lines 103-172, axis 6.4 lines 247-310, the shared-item row for the `blocking` boolean and the Medium token at line 892); research files 12, 11 and 05 under `RT research/`; `gaps-and-questions.md` rows GQ-060 and GQ-160; and the code and tests cited below.

Adjudicated slots read before writing (outcomes kept as they stand):

| Slot | Outcome I rely on | Where my position touches it |
|---|---|---|
| C-01 `core-shape-and-finding-contract` | Variant B base: thin shared contract now, per-module engines; spec loop stays on v1 `findings.py` and the v1 ledger; reflect stays on the v2 kernel; unknown keys open; `T<PP>.<TT>` added once to the shared `refs_norm` token list; the shared repair step policy belongs to C-06 | Position A needs no engine change. It uses the severity and `blocking` fields that both parsers already validate and the `T<PP>.<TT>` token that C-01 adds. It does not depend on the INV-003 repair-policy question. |
| C-02 `ledger-clearing-and-verdict-authority` | Variant B base with A's quorum gate; typed `blocking` stays the authority plus a CRITICAL floor applied in `merge_round`; no category predicate and no grader in the core; `brief_ids`, `verify_ids`, `held_ids` derived on read | Position A is a module label map placed above this rule. It keeps typed `blocking` as the core authority and never needs a predicate in the core. It relies on the CRITICAL floor to make High always blocking. It depends on `brief_ids` holding blocking rows only (stated in section 2.3). |
| C-03 `merge-verdict-policy-and-quorum` | Variant A base: deterministic any-blocking union as the default policy, quorum `min(2, requested)` as a merge-time refusal, fail-closed only in profiles that set `degrade`; condition 2 says the union is the cheap-error side only while a Reviser-rejected row has a non-human exit (today it stays `open` and only `defer` clears it) | Position A narrows the set of rows the union can fail on (blocking rows only). Where this proposal argues from false-blocker cost it uses C-03's own condition 2 and does not claim to measure it. |

The result of slot C-05 (`consumer-entry-effect-and-delivery`) was not an input of this proposal. Where the tasklist entry point matters (section 2.2) the text says what is assumed.

## 1. The position

The tasklist module adopts `Medium` as a non-blocking warning and grades by definition, not by label. Its three labels map onto the core pair that both parsers already validate: High becomes `CRITICAL` with `blocking: true`; Medium becomes `MAJOR` with `blocking: false` plus the follow-up marker; Low becomes `MINOR` with `blocking: false`. This makes the tasklist skill agree with two sources that already agree with each other: the tasklist CLI fidelity gate, which counts MEDIUM and gates only on HIGH, and the repository review rule S1-S5, where Medium is a warning that never fails a review, never triggers a fix pass and never enters a reviser brief. Omissions of roadmap-stated deliverables stay blocking because the module's grading block puts them in High, as the CLI prompt already does. The tasklist fidelity prompt then becomes a vocabulary of the tasklist module under the core (label map, severity definitions, id grammar, document roles) instead of a separate vocabulary outside it. `Medium` stays out of the core schema, as in both positions. The fidelity gate, its frontmatter fields and its exit code do not change.

## 2. Design consequence for the shared core and the named modules

### 2.1 Shared core

- No new core token. `Medium` has no schema value in `cli/review`: `SEVERITIES = ("CRITICAL", "MAJOR", "MINOR")` (`src/superclaude/cli/review/findings.py:14`) and the only coupling rule is that MINOR cannot be blocking (`findings.py:100-101`). [CODE-VERIFIED] The tasklist label map is module data above that pair.
- Which engine hosts tasklist review is not decided by this slot. Both parsers accept the three mapped rows: v1 as above, v2 because the extra rule at `src/superclaude/cli/review/findings_v2.py:155-162` fires only when `reflect_category` is set. [CODE-VERIFIED] The tasklist module therefore must not set `reflect_category`: with it, a MAJOR finding must be blocking (`findings_v2.py:161-162`), which is the opposite of the Medium mapping. The lens set is closed to `spec`, `reflect-pre`, `reflect-post` (`findings_v2.py:36`, `:143-145`), so a v2 tasklist lens needs the module-declared lens set that the finding-contract axis already lists as a requirement. [CODE-VERIFIED for the lines; the requirement is from synth-05 section 6.2 and `RT phase-outputs/discovery/undecidable-conflicts.md` line 71]
- Enforcement has two forms. Form 1 (no core change): the tasklist brief defines the three grades and the reviewer types `severity` and `blocking` accordingly; the parser accepts `MAJOR` with either `blocking` value, so the rule rests on the brief. Form 2 (small core hook): the module declares a severity-to-blocking table and the parse edge rejects a line that breaks it, in the way `reflect_category` already does for the reflect lens. Form 2 is the one this proposal prefers, because Form 1 repeats the mismatch the loop brief already shows (brief line 31 says Medium, the schema allows `blocking: true`; `RT research/10-process-redesign.md:149`). Form 2 does not make the core a predicate engine and does not conflict with C-02: the core authority stays the typed `blocking` field with the CRITICAL floor; the table only constrains what a module's reviewers may type.
- C-01 adds `T<PP>.<TT>` to the shared `refs_norm` token list. Tasklist findings need it in either position: `_REF_TOKEN` at `findings.py:29` matches `FR-8` and `P3` but not `T03.02`. [CODE-VERIFIED] Nothing else in the core changes for this slot.

### 2.2 Tasklist module (skill `src/superclaude/skills/sc-tasklist-protocol/SKILL.md`)

- Stage 7 gets a grading block that defines High, Medium and Low. Today it defines none: the finding entry says only `Severity: High | Medium | Low` (`SKILL.md:1384-1391`). [CODE-VERIFIED] The definitions to adopt are the ones the CLI prompt already carries (`src/superclaude/cli/tasklist/prompts.py:51-69`): HIGH omits, contradicts or misrepresents a roadmap item so the tasklist cannot be used as-is; MEDIUM addresses the item with insufficient detail, ambiguous language or minor misalignment; LOW is formatting or organisation. [CODE-VERIFIED]
- Stage 8 to 10 act on High only. Text that now says "High and Medium (blocking)" or "High or Medium" changes to High: the short-circuit (`SKILL.md:1439`, `:1445`, `:1450`), PatchChecklist (`:1531`), Stage 9 purpose (`:1537`), Stage 10 purpose and loop (`:1567`, `:1571`), the patchable set `F_k` and the regression check inside the P2 loop (`:1608`, `:1610`), and the HALT at termination (`:1614`). The Medium section of `ValidationReport.md` (`:1478`) stays, listed with its evidence as follow-up candidates; the Low section keeps its "notes" label (`:1481`). [CODE-VERIFIED for the lines]
- The two TDD checks graded Medium (`SKILL.md:1421-1422`: migration stage without a task bucket; test pyramid level without a test task) are regraded by definition. A required deliverable with no task is an omission, which the module's High definition and S1 ("a missing required deliverable") both call blocking, and the table already puts the sibling check "Missing task for new component" at HIGH (`:1420`). They move to High, so their blocking behaviour does not change; only findings that describe a weakness (for example criteria that are weaker but still verifiable) stop blocking. [CODE-VERIFIED for the table; the regrade is a design choice of this position]
- The `--unattended` rule keeps its shape: unresolved open blocking findings resolve as `blocked` (`SKILL.md:1615`; pinned at `tests/skills/test_worker_contract.py:777` and `:1861`); the pinned phrase "the unresolved High or Medium HALT resolves as blocked" becomes "the unresolved High HALT resolves as blocked" in the skill and in both pins. [CODE-VERIFIED for the lines]
- Stage 10.5 (reflect UC-1, advisory) and the per-phase post gate T5 (`superclaude reflect run`) are unchanged. They do not read the tasklist severity labels (`RT research/11-consumers-tasklist-workflow.md` sections 2.2 and 2.3). [CODE-VERIFIED via research 11]

### 2.3 Fidelity vocabulary under the core (CLI `src/superclaude/cli/tasklist/`)

- The tasklist module declares, once, as module data: the labels and their map to the core pair; the severity definitions above; the finding id grammars (`DEV-NNN` for fidelity entries, `T<PP>.<TT>` for task references; both fit the core id rule `^[A-Za-z0-9][A-Za-z0-9._-]{0,15}$`, `findings.py:26`); and the document roles. [CODE-VERIFIED for the id rule]
- The layering guard becomes the module's role table, not prompt prose: the roadmap is the driving document (`source`), the tasklist directory is the candidate (`plan`), and no `spec` role is declared. The roles exist in the core already (`ROLES = ("plan", "spec", "source", "test", "diff", "artifact")`, `findings_v2.py:35`). The guard text and its test stay (`prompts.py:6-8`, `:43-48`; `tests/tasklist/test_tasklist_fidelity.py:101-108`). [CODE-VERIFIED]
- What does not change: the gate (`TASKLIST_FIDELITY_GATE`, `src/superclaude/cli/tasklist/gates.py:23-46`), the shared check functions it imports from `src/superclaude/cli/roadmap/gates.py` (`_high_severity_count_zero` at `:118-142`, `_tasklist_ready_consistent` at `:195-239`), the six frontmatter fields, the exit code (`executor.py:189-216`, `:219-244`), and the roadmap pipeline's `SPEC_FIDELITY_GATE` (`roadmap/gates.py:1322-1345`), which uses the same HIGH/MEDIUM/LOW counts and stays outside this module. [CODE-VERIFIED]
- What the vocabulary buys later: the three counts and `tasklist_ready` can be derived from ledger rows instead of being typed by one reviewer. Today `_tasklist_ready_consistent` checks `tasklist_ready` only against the reviewer-typed `high_severity_count` and `validation_complete` (`roadmap/gates.py:208-239`); it does not look at the Deviation Report body. [CODE-VERIFIED] That derivation is a consequence this position allows, not a requirement of it.
- No single source across skill and package. The skill is an installed primitive and the CLI is package code that is not installed to `~/.claude/`; a shared file would break the installed-path rule. The two hand-kept definition texts are tied by a parity test (section 5), not by a shared file.

## 3. Evidence

`SK` = `src/superclaude/skills/sc-tasklist-protocol/SKILL.md`; `PR` = `src/superclaude/cli/tasklist/prompts.py`; `GT` = `src/superclaude/cli/tasklist/gates.py`; `RG` = `src/superclaude/cli/roadmap/gates.py`; `PM` = `src/superclaude/output-styles/pragmatic.md`.

| # | Fact | Source | Tag |
|---|---|---|---|
| 1 | The tasklist skill treats High and Medium as blocking and Low as notes: Stage 9 and 10 purpose lines, the patchable set `F_k`, the regression check, and the HALT at termination | `SK:1537`, `:1567`, `:1608`, `:1610`, `:1614` | [CODE-VERIFIED] |
| 2 | The skill's Stage 7 finding entry names the three labels and defines none of them | `SK:1384-1391` | [CODE-VERIFIED] |
| 3 | The skill's own TDD table grades two omission-type checks Medium and the sibling "missing task for new component" High | `SK:1420-1422` | [CODE-VERIFIED] |
| 4 | The CLI gate requires `medium_severity_count` as a field but its two semantic checks look only at `high_severity_count` (and `validation_complete`); the CLI exits 1 on HIGH only | `GT:23-46`; `RG:118-142`, `:195-239`; `src/superclaude/cli/tasklist/executor.py:189-216`, `:244` | [CODE-VERIFIED] |
| 5 | CLI tests pin that a report with MEDIUM deviations passes the gate and does not set the exit code | `tests/tasklist/test_tasklist_fidelity.py:208-225`; `tests/tasklist/test_tasklist_cli.py:165-179` | [CODE-VERIFIED] |
| 6 | The CLI prompt defines HIGH (omits, contradicts, misrepresents; tasklist cannot be used as-is), MEDIUM (insufficient detail, ambiguity, minor misalignment) and LOW, and sets `tasklist_ready` true only when `high_severity_count` is 0 | `PR:51-69`, `:94-100` | [CODE-VERIFIED] |
| 7 | The repo rule: grade as blocking or minor; minor never fails a review; Medium is a minor finding that is a real but non-blocking weakness, a warning that never fails a review, never triggers a fix pass and never appears in a reviser brief; on a three-label scale grade by the definition, not the label | `PM:225-226`, `:229-231` | [CODE-VERIFIED] |
| 8 | The ten-file set that pins S1-S3 verbatim does not contain the tasklist skill; the tasklist wording is pinned only by twelve rows of the sweep table | `tests/skills/test_review_severity_rule.py:181-192`; fixture rows S-119..S-130 at `tests/skills/fixtures/review_severity_sweep_edits.yaml:976-1071`; `test_j` at `:268-272` (139 rows); the plan copy `.dev/review-severity-rule/sweep-edits.yaml` is tracked and holds 139 rows, 12 with `group: tasklist` | [CODE-VERIFIED] (counts by `grep -c` and `git ls-files`) |
| 9 | History: the skill's "High or Medium (blocking)" text entered with #343 (`80f934de5`, 2026-11-02), a sweep that applied "blocking or minor" to every review loop. The row S-130 shows the text it replaced: unresolved findings "logged for human review (the bundle still ships; the loop is an advisory remediation, not a hard blocker)". The commit message records no decision about Medium. Neither `GT` nor `PR` was touched by that commit (their `git log -3` lists no such commit; latest commits 2026-05-25 and 2026-09-18) | `git show -s 80f934de5`; fixture `:1069`; `git log -3 -- GT PR` | [CODE-VERIFIED] |
| 10 | Rule S4 lets "a protocol that defines its own severity model, such as `/sc:implement`" apply that model. `/sc:implement` defines a derived model in `refs/qa.md`; whether labels plus a blocking parenthetical without definitions (fact 2) count as such a model is an interpretation | `PM:228`; `RT research/12-consumers-spec-review.md:61` | [UNVERIFIED] (interpretation) |
| 11 | "Medium" has at least six uses; M4 (skill: blocking) against M1 (warning) and M5 (CLI: counted, not gated) is the one conflict inside one product, and research 12 says the tasklist module must settle it before mapping | `RT research/12-consumers-spec-review.md:84-97`, `:193`, `:210` (Q2) | [CODE-VERIFIED] per research 12; rows 4 and 1 above re-read |
| 12 | The fidelity vocabulary is shared beyond the tasklist CLI: `SPEC_FIDELITY_GATE` carries the same six fields and checks; `high_severity_count`, `medium_severity_count` or `tasklist_ready` occur on 76 lines in 10 files under `src/superclaude/cli/` | `RG:1322-1345`; `grep -c` over `src/superclaude/cli` | [CODE-VERIFIED] |
| 13 | The tasklist skill does not call `superclaude tasklist validate` except as a pipeline-chaining example; the CLI is a separate roadmap-pipeline validator | `SK:226`; `RT research/11-consumers-tasklist-workflow.md:69` | [CODE-VERIFIED] (grep over `src/superclaude/skills` lists `SK:153` (long line), `SK:226`, one roadmap ref and one auggie ref) |
| 14 | The reflect lens already uses a label-determined rule (`blocking == (severity != "MINOR")`) selected by `reflect_category`; the spec loop uses the consequence-graded rule where MAJOR may be non-blocking | `findings_v2.py:155-162`; `findings.py:96-101` | [CODE-VERIFIED] |
| 15 | The tasklist skill is not shipped in the plugin mirror (no `sc-tasklist-protocol`, no `tasklist.md` command) | `RT research/11-consumers-tasklist-workflow.md:155` | [CODE-VERIFIED] per research 11; not re-listed here |
| 16 | Pre-edit, the Stage 7 report template already prints `Total findings: X (High: H, Medium: M, Low: L)`, the same triple the CLI frontmatter counts | `SK:1462`; `PR:94-97` | [CODE-VERIFIED] |

## 4. Invariants

### 4.1 Preserved

- Reflect contract 1.8.0 byte-identical: not touched. Reflect does not read the tasklist label map; the stable block `### 9.1` of `src/superclaude/skills/sc-reflect-protocol/SKILL.md` and the edit-fence tests (`tests/cli/reflect/test_shadow_skill_contract.py:42-98`) are outside every file this position edits. [CODE-VERIFIED via `RT research/11-consumers-tasklist-workflow.md` section 3.3]
- The 36-test verdict matrix (`tests/cli/reflect/test_verdict_mapping.py`): not touched. It pins `derive_verdict` over reflect contract fields; the tasklist label map is read by neither `contract.py` nor the matrix. [CODE-VERIFIED via research 11 section 4]
- INV-J (repo rule S1-S5, at most 2 fix cycles): this position is an application of S1-S5 to the one product where the skill does not follow it as written. `test_c_s1_s3_copied_verbatim`, `test_d_canonical_cap_text_in_style` and `test_f_no_old_cap_numbers_outside_implement_protocol` (`tests/skills/test_review_severity_rule.py:196-230`, `:320-339`) are not affected: the tasklist skill is outside the ten-file set and the P2 loop's cap text is not changed. [CODE-VERIFIED]
- INV-I (a review that did not happen never certifies PASS): the synthetic finding for a failed Stage 7 agent stays High, fixed and non-demotable (`SK:1400-1401`); a zero-success Stage 7 stays the report-validation-error terminal (`SK:1431`). [CODE-VERIFIED]
- INV-M (`reflect_status` and `reflect_report_path`, closed enum): not touched. [CODE-VERIFIED via research 11 section 5.3]
- INV-K and INV-N (sync and plugin parity): the skill is edited under `src/superclaude/skills/` and synced with `make sync-dev`; there is no plugin copy to keep in step (fact 15). The edited text must not name a `src/superclaude/` path (repository rule on installed primitives). [CODE-VERIFIED for fact 15 via research 11]
- Unchanged CLI behaviour: gate, six fields, exit code, guard text (section 2.3).

### 4.2 Endangered or changed (each is a cost of this position)

1. Pinned tasklist wording. The twelve sweep rows S-119..S-130 assert the "High or Medium (blocking)" strings; `test_j` fails on any edit until both fixture copies change. `test_ej_fixtures_are_byte_copies_of_the_plan_tables` (`tests/skills/test_review_severity_rule.py:275-283`) compares the fixture with `.dev/review-severity-rule/sweep-edits.yaml`, so both files must change together and stay byte-equal (the test skips only when the plan copy is absent; it is present and tracked). The two pinned phrases at `tests/skills/test_worker_contract.py:777` and `:1861` change too. The example verification table at `SK:1588-1589` (rows `M2`, `M3`) becomes High rows.
2. Behaviour change for users. A run whose only residual findings are Medium used to HALT at the P2 cap (`SK:1614`); under this position it completes with a follow-up list. That is the S2 direction (minor findings never fail a review) and is also a loosening against today's skill.
3. P2 monotonicity. `|F_k|` counts High only, so the monotonicity halt (`SK:1611`) stops firing on Medium churn.
4. Grade-boundary sensitivity. Under the skill's current rule a High-versus-Medium misgrade changes nothing about the verdict; under this position it decides blocking. C-02's own residual applies: the CRITICAL floor keys on the reviewer-typed severity, and a re-classification to MAJOR non-blocking still drops the row (C-02 INV-016, MEDIUM, unaddressed). The mitigations are the definitions in the grading block, the any-reviewer union of C-03 (a High typed by one reviewer of the cluster keeps the row blocking), and the blind grading test in section 5.
5. Omission regrade (section 2.2) is a judgement: an omission graded Medium by a reviewer who follows the old habit becomes non-blocking. The grading block must say that an omission of a roadmap-stated deliverable is High.
6. Hand-kept parity. Two definition texts (skill, CLI prompt) stay hand-kept and are tied only by a test, so drift is possible between releases.

## 5. Test or measurement that would show this position right or wrong

Static tests (red before the change, green after; none needs a model call):

- T1. Rewrite the twelve sweep rows and the two worker-contract phrases (4.2 item 1); the count of 139 rows stays.
- T2. A parity test over three artefacts: the skill's Stage 7 grading block, the output of `build_tasklist_fidelity_prompt`, and the tasklist label map. Each must say that High blocks and that Medium and Low do not, and the two TDD checks at `SK:1421-1422` must be graded High.
- T3. The existing CLI pins pass unmodified: `tests/tasklist/test_tasklist_fidelity.py:101-108` (guard), `:208-225` (Medium passes the gate) and `tests/tasklist/test_tasklist_cli.py:165-179`. They show the CLI side is untouched.
- T4. If Form 2 is taken: a test that a tasklist-module line with `MAJOR` and `blocking: true` is rejected, and that a `CRITICAL` line typed `blocking: false` is flipped by the C-02 floor with one warning.

Measurement (not run here):

- M1. Blind grade of known defects. Write the grading block first. Take a set of tasklists with known seeded or ground-truth defects (the E2 tasklist-review study has classes `unpassable-ac`, `missing-task`, `ambiguity`, `contradiction`; `RT research/05-input-delivery-brief.md:135`, [UNVERIFIED] as slice-only). A reviewer who has only the grading block grades each defect High, Medium or Low. The position is wrong if defects that the implement rule would block (the four yes/no answers of `sc-implement-protocol/refs/qa.md`, [CODE-VERIFIED] via research 12 row V5) land in Medium at a rate above a threshold that must be registered before the run. No evidence fixes the threshold; it is a design choice and is not set here.
- M2. Medium-row audit on real Stage 7 or fidelity reports. Take the reports that exist for real tasklist packages, apply the implement rule to each Medium row, and count how many are blocking by that rule. Whether such a corpus exists is [UNVERIFIED]: this proposal did not search `.dev/tasks/`, which the independence rule excludes. The person who runs M2 locates the corpus; if none exists M2 cannot be run and M1 is the only measurement.
- The result that would show the position right: few Medium rows are blocking by the implement rule in M2 and M1 shows no ground-truth blocking class landing in Medium once omissions are defined as High. The result that would show it wrong: either of those fails.

## 6. Effect on future PR code review and rf-qa replacement

- PR code review. The PR module's five tiers carry routes, not a verdict, and its Medium means "fix in this PR if cheap" (`RT research/12-consumers-spec-review.md:88`, M3). This position keeps `Medium` out of the core and makes tasklist Medium a warning, so the core can offer one rule for any module that uses the word on a three-label scale: Medium is a warning, a follow-up marker on a non-blocking row. The PR module still needs its own map from five tiers to `blocking` (research 12 gap 1, [UNVERIFIED]); this position neither helps nor blocks it.
- rf-qa and the `/task` phase gate. Those use CRITICAL, IMPORTANT and MINOR with IMPORTANT blocking (`PM:229`), and the tasklist phase files this module produces are the files `/task` later gates. With this position a tasklist Medium reaches `/task` as an open warning and not as a blocking finding, in line with the rf-qa rule; with the skill's current rule, tasklist and rf-qa would label the same weakness blocking in one place and minor in the other. The rf-qa replacement path needs a module label map either way; this position adds no requirement to it.
- Both futures need module-declared severity sets (the finding-contract axis, synth-05 section 6.2); the tasklist module under this position is a worked example of one set with a deterministic map.

## 7. Strongest objection and the answer

Objection. The skill's Medium-as-blocking is deliberate, recent and pinned twelve times; its dimensions include "Weakened criteria", and a weakened criterion is a defect worth fixing. The CLI gate that "counts MEDIUM but gates nothing" may be a gap in the CLI and not a model, and the repo rule's Medium paragraph was written for the spec-panel scale, not for High, Medium and Low. The E2 study shows what demotion to Medium can do: a brief rule that graded "a requirement the document never states" as Medium left all seven true I7 findings non-blocking (`RT research/12-consumers-spec-review.md:93`, [UNVERIFIED] as a measurement). Rule S4 allows a protocol to keep its own severity model. No code or data prefers Position A.

Answer.

1. Deliberate. The commit that introduced the text (#343) states its decision as "minor findings never fail a review" and records no decision about Medium; the row that replaced the old text shows the previous rule was advisory (fact 9). The skill defines none of its three labels (fact 2), so what "Medium" means there was never written down; the only written definition in the product is the CLI's (fact 6), and it puts Medium below the gate.
2. Weakened criteria and the E2 harm. The E2 harm came from a label rule: a class of finding was routed to Medium by the brief (`document_review_loop_prompts.md:31`). This position replaces a label rule by a definition rule: High is "omits, contradicts or misrepresents so the tasklist cannot be used as-is", and the two omission checks move to High (section 2.2). A weakened criterion that makes a roadmap-stated criterion unverifiable is High; only a criterion that is weaker but still checkable is Medium. Whether reviewers apply that boundary is exactly what M1 tests; this proposal does not claim it is shown.
3. The CLI as a gap. The CLI behaviour is pinned by tests that name MEDIUM as passing (fact 5) and was not changed by #343 (fact 9); two sources against one is not proof, and the proposal does not claim it is. Its claim is narrower: one product should not have a gate that passes a report and a skill that halts on the same row, and the repo's only stated rule (S1-S5) sides with the gate.
4. S4. This proposal does not say S4 forbids Position B. It says S4's example (`/sc:implement`) defines a model in a reference file and the tasklist skill defines labels only (fact 10), so whether S4 applies is open.
5. What the objection correctly leaves standing. Position A loosens a gate (4.2 items 2 and 3) and makes the High-versus-Medium boundary carry the verdict (4.2 item 4). Those are real costs of A, stated as such.

## 8. Where this proposal depends on the adjudicated slots

- C-01: depends on `T<PP>.<TT>` being added once to the shared reference-token list (decided there). Does not depend on the engine choice, on the unknown-key policy or on the INV-003 repair question. Agrees with all of its outcomes.
- C-02: depends on typed `blocking` staying the core authority with the CRITICAL floor (decided there), and on `brief_ids` holding blocking rows only, so that Medium rows never reach the Reviser brief. Inherits C-02's unaddressed INV-016 (4.2 item 4). Agrees with all of its outcomes; asks for nothing from the core beyond Form 2's optional module-declared severity table.
- C-03: depends on the any-blocking union and on condition 2 (a Reviser-rejected row has no non-human exit). Under the union, fewer rows are blocking, which lowers the false-blocker cost that condition 2 describes; this proposal does not measure that. Agrees with all of its outcomes.
- Not an input: C-05 (tasklist entry point). If the tasklist module is entered only through reflect UC-1, the Stage 7 to 10 text this proposal edits is still the module's own review, and nothing in sections 2 to 4 changes.

## 9. Not claimed

- No claim that Position B is wrong; section 7 states the costs of Position A.
- No claim that a measurement exists for either position; M1 and M2 are unrun.
- No branch, PR or sequence plan, and no risk register.

Status: Complete
