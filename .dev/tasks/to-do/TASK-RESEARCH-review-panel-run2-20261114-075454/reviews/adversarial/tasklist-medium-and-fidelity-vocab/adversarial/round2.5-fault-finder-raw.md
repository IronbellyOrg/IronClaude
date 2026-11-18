# Round 2.5 invariant probe, fault-finder (slot X-15, tasklist Medium and fidelity vocabulary)

Scope: the emerging consensus after Round 2 (Form 1 only, H+ default, A+ upgrade gated on F1/F2/F3). HEAD `50d4d2b9d`. SK = `src/superclaude/skills/sc-tasklist-protocol/SKILL.md`; CMD = `src/superclaude/commands/tasklist.md`; PR = `src/superclaude/cli/tasklist/prompts.py`; PM = `src/superclaude/output-styles/pragmatic.md`. No `branch-trace.md` exists in the task folder (searched), so the Category 6 enumeration is inline (INV-019). All code facts below were read in this session; no tests were run.

ID: INV-001
CATEGORY: state_variables
ASSUMPTION: The record of earlier passes is complete enough to show a silent false-clean (A's reply to W3: "the Medium section of `ValidationReport.md` stays and lists the row") and to act as the follow-up list for the non-blocking class (B's "Low section ... is the follow-up list PM:230 asks for").
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: Stage 8 writes `ValidationReport.md` once, from the first Stage 7 merge (SK:1452-1483), and the loop-back target is Stage 9, not Stage 8 (SK:1561). The F_k re-run (SK:1608) produces only `|F_k|` and a FAIL-set of task ids. The only per-pass state is the loop table (SK:1594-1600): columns pass, `|F_{k-1}|`, `|F_k|`, FAIL-set, PASS-set, regression set, guard. It has no severity column and no finding ids, and no sentence says a re-run's findings are appended to the report. So (a) a finding typed High at pass 1 and Medium (A+) or Low (H+) at the re-run leaves F_k with no recorded reason; (b) a Medium or Low that first appears at a re-run is never listed anywhere. The mitigation both advocates cite exists only for pass-1 findings. F3 (a hand-run, two-sample experiment) does not exercise this path (round2-advocate-A.md W3; round2-advocate-B.md Final position, Low row).

ID: INV-002
CATEGORY: state_variables
ASSUMPTION: The byte-equal sweep fixture and its plan copy reliably guard the 12 tasklist rows: untouched under H+, rewritten together under A+ ("row count stays 139").
STATUS: UNADDRESSED
SEVERITY: LOW
EVIDENCE: `test_ej_fixtures_are_byte_copies_of_the_plan_tables` calls `pytest.skip` when `.dev/review-severity-rule/sweep-edits.yaml` is absent (`tests/skills/test_review_severity_rule.py:275-282`); here the copy exists and `cmp` reports it byte-equal to the fixture, but a checkout without it gets no drift signal. The "12 pinned rows" are pinned only by `len(rows) == 139` (`:268-270`) and per-row `old` absent / `new` present (`_failing_rows`, `:252-258`); the 12-row group is not asserted. The `line:` fields are never asserted and are already stale (S-125 says 1561, the text is at SK:1567; S-130 says 1608, it is at SK:1614). The fixture header's group tally (96+14+2+1+5+12+5 = 135) disagrees with the 139 rows; the actual groups are fixloop 99, reflect-gate 6, tasklist 12 (grep of `group:`). Because `_failing_rows` is substring based, H+'s insertion after SK:1391 breaks no test, but every SK line cite in the transcripts and in the F1-F3 protocols shifts by the block length without any signal.

ID: INV-003
CATEGORY: guard_conditions
ASSUMPTION: "High maps to CRITICAL/blocking:true and the C-02 CRITICAL floor keeps it blocking; the residual (reviewer-typed severity can drop a row) is accepted by both", so the label-to-blocking map is equally safe under A+ and H+ (diff A-003; B R2: the blocking line "has identical content in A+ and H+").
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: No floor exists in code. `grep` of `cli/review` finds CRITICAL only in the severity tuples, `_SEV_RANK` (`ledger.py:20`) and the card word maps. Both parse edges reject only MINOR with blocking true (`findings.py:100-101`, `findings_v2.py:107-108`), so CRITICAL with `blocking: false` parses; the ledger lets the current report's flag decide (`ledger.py:210-218`). The floor is an adjudicated design for `merge_round` with residual INV-016 (C-02 ADJUDICATION-RESULT, table row INV-016: "a re-classification to MAJOR non-blocking still drops the row"). Where it will apply it covers CRITICAL only. A+ puts the dropped-criterion class under High, so CRITICAL, protected. H+ puts it under Medium, so MAJOR with `blocking: true`, which the floor does not cover; a MAJOR typed `blocking: false` drops the row. The "identical blocking set" holds for the prose block, not for the engine-level protected set, and B R2 says "I find no fifth difference". Also, today a Stage 7 finding is a prose entry with a Severity word and no typed blocking field (SK:1384-1391, A-005), so the module's label map has no consumer, and a test pinning it "as data" (B's T3) pins data nothing reads.

ID: INV-004
CATEGORY: guard_conditions
ASSUMPTION: The orchestrator applies "same-task duplicates at the dedup step keep the highest severity" correctly and without side effects.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: SK:1410 leaves "the same issue on the same task" to the orchestrating model: no sameness key, no order, no tie rule; the core's `same_defect` (`findings.py:367-379`) is not used by the skill. No test pins SK:1410 (grep of `tests/` for "keep only one entry" and "same issue on the same task" has no hit). Keep-highest keeps the entry with the higher label, not the entry whose `Exact fix` covers the defect: two different defects judged "same" collapse to the higher-labelled one, and the dropped entry's fix never reaches PatchChecklist (items come from the kept entries, SK:1531). The synthetic `severity: HIGH` finding is "never demoted at merge" (SK:1401) and shares the stream; no clause says a real finding must not be merged into it. No variant states a compliance check for this clause.

ID: INV-005
CATEGORY: guard_conditions
ASSUMPTION: The parity/containment test (A's T2, B's T2 a-d) can detect drift between the skill's grading block and the CLI prompt.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: B's T2(a) says "every skill High example is a CLI HIGH example". Consensus point 3 puts omission of an exit criterion or validation step in skill High, but the CLI HIGH examples are PR:53-57 (roadmap item with no task, fabricated deliverable ID, contradicted dependency, omitted deliverable outputs); the CLI puts "Acceptance criteria are weaker" at MEDIUM (PR:62) and names Acceptance Criteria Completeness only as a dimension with no severity (PR:81-82). T2(b) says every CLI LOW example sits inside the skill Low class; the CLI LOW list includes "Missing cross-references that don't affect understanding" (PR:69), which B's Low text does not name. TDD and PRD coverage gaps are MEDIUM in the CLI (PR:134, PR:152) and HIGH for components in the skill (SK:1420); no T2 clause covers them. A static test (no model call) over natural-language classes can only check keyword presence, so it detects deletion of chosen phrases and cannot detect a change of meaning. As written, T2(a) cannot pass without editing PR or loosening it.

ID: INV-006
CATEGORY: guard_conditions
ASSUMPTION: The CLI exit code and `tasklist_ready` read typed counts only, so the skill-side change cannot reach them.
STATUS: ADDRESSED
SEVERITY: LOW
EVIDENCE: `_tasklist_ready_consistent` (`roadmap/gates.py:195-240`) and `TASKLIST_FIDELITY_GATE` (`tasklist/gates.py:34-45`) read frontmatter `high_severity_count` and `validation_complete` only; the exit comes from `_has_high_severity` (`tasklist/executor.py:189-216`, `:244`) and `commands.py:181-183`. Consensus point 2 leaves all of it untouched and diff U-006 records that counts are not derived from the body. Residual, not relied on by the consensus: nothing checks that high+medium+low equals `total_deviations`, and the convergence report writes `medium_severity_count: 0` with `total_deviations` equal to the high count (`roadmap/executor.py:1763-1766`), so the Medium count in the shared frontmatter is not a reliable cross-producer signal.

ID: INV-007
CATEGORY: count_divergence
ASSUMPTION: F_k, the PASS/FAIL sets and the pass counts are the same kind of count across passes, so "strictly shrank" means a patch worked, and "2 total passes" equals S3's "2 fix cycles (3 reviews)".
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: SK:1608 defines `F_k` as the post-dedup cardinality of failing findings; the loop table and the regression check work on items (task ids) (SK:1596-1602, :1610); monotonicity compares counts (SK:1611). One task with two blocking findings counts 2 in `|F_k|` and 1 in the FAIL-set. A re-grade of one of the two out of the blocking class (A+: High to Medium; H+: Medium to Low) lowers `|F_k|` while the task still fails, so "strictly shrank" can hold with no patch applied, and the table (no severity column) cannot show it. Sample count: by my reading of SK:1604-1608, a bundle gets the initial Stage 7 run plus a full re-run at the end of each of the two passes, so up to 3 full 2N-agent samples and 2 patch cycles; that matches PM:227 ("2 fix cycles (3 reviews)") but F3 compares only 2 samples, so its flip rate is not the rate over the loop's two transitions. Neither advocate states the sample count.

ID: INV-008
CATEGORY: count_divergence
ASSUMPTION: The edit sites both variants list (H+: one insertion plus one clause; A+: about ten sites) cover every skill sentence that states which severities block, so the skill ends with one severity semantics.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: Four further severity statements are in neither list. SK:1703 ("OR clean report if zero issues"); SK:1705 ("All findings from ValidationReport.md re-verified", against SK:1567, which limits Stage 10 to High and Medium); SK:1716 ("If Stage 7 produces zero findings, Stages 9-10 are skipped", against SK:1439 "zero High or Medium (blocking)"); SK:1766 ("X high / Y medium / Z low", "clean - no drift"). The totals line SK:1462 is also in neither. The sweep rows S-119 to S-130 edited SK:1439 but not these, so today a Low-only bundle has two instructions. H+ edits no existing sentence and enlarges the Low class (ambiguity, detail, estimate, method), so Low-only bundles become more common; A+'s ten-site list omits them too. No test pins these lines.

ID: INV-009
CATEGORY: count_divergence
ASSUMPTION: The "76 lines in 10 files" (A) versus "88 lines in 14 files" (diff X-010) count is settled, and "the CLI side is untouched" rests on a known set of files.
STATUS: UNADDRESSED
SEVERITY: LOW
EVIDENCE: Neither count records its token list. My measurement: `medium_severity_count` alone occurs on 10 lines in 7 source files (`cli/roadmap/{gates,prompts,executor}.py`, `spec_fidelity.md.j2`, `spec_fidelity.schema.json`, `cli/tasklist/{gates,prompts}.py`, excluding `.pyc`); the 76/88 figures cover a wider unrecorded token set. Consensus point 2 does not use the number, and no decision turns on it, but diff X-010 leaves it open and A's `.py`-only caveat is the only reconciliation. The fixture header tally (135 against 139 rows, INV-002) is the same kind of stale prose count.

ID: INV-010
CATEGORY: collection_boundaries
ASSUMPTION: A Medium-only bundle under A+ ends with a clean report plus a Medium follow-up list ("Medium-only residuals ... the bundle completes; Medium rows stay in `ValidationReport.md` with their evidence").
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: A+ rewrites the short-circuit at SK:1439 to "zero High" and says SK:1445 "names no label and stays" (round2-advocate-A.md, skill sites). The clean template (SK:1441-1446) says only "(Low findings, if any, listed as notes)", and SK:1439 says "any Low findings are listed after it as notes". A Medium-only bundle takes the short-circuit and writes a four-line CLEAN report that has no slot for Medium warnings, while the full report structure (SK:1458-1483) is only written on the non-short-circuit path. SK:1450's synthetic guard also says "real High or Medium findings". Under H+ Medium blocks and the case does not arise; it applies only if A+ is adopted, so the A+ edit list is short by at least SK:1445 and the SK:1439 parenthetical.

ID: INV-011
CATEGORY: collection_boundaries
ASSUMPTION: F1 (6 archived findings, 3 graders), F2 (at least 10 plus 10 seeded defects) and F3 (more than 1 in 5 blocking-class findings flipping) have enough observations to separate the variants, and a per-finding threshold bounds the bundle outcome.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: The only archive data are two bundles (High 0, Medium 4, Low 5 and High 0, Medium 2, Low 6; diff C-010). On a bundle with 2 to 6 blocking-class findings one flip is 17 to 50 percent, so the 1-in-5 rule is decided by a single event. A per-finding rate does not bound the loop outcome: with p = 0.2 and 4 blocking-class findings, P(at least one flip) = 1 - 0.8^4 = 0.59. Under SK:1610 one Low-to-Medium flip on a previously PASS item halts the skill, while a false-clean needs every residual blocking finding to flip at once (F_k empty), so the two harms have different per-bundle rates from the same per-finding p. All three measurements register a threshold; none registers the number of bundles, the number of repeats, or the unit (finding or bundle). N = 1 (one phase file) gives only 2 agents per sample.

ID: INV-012
CATEGORY: collection_boundaries
ASSUMPTION: One typed grade per task slice is a usable base (after C-03's union was dropped) at every phase size.
STATUS: UNADDRESSED
SEVERITY: LOW
EVIDENCE: SK:1356 sets `split = ceil(task_count / 2)`; a phase with one task (allowed, self-check 13 requires at least 1 task, SK:1270) gives Agent A task 1 and Agent B tasks `split+1` to `task_count`, which is 2 to 1, an empty slice (SK:1364). The cohort still counts 2N agents and the empty agent's "No issues found" counts as a success in the some-vs-zero branch (SK:1393, :1427-1431). In such a phase one agent grades the one task and nothing reviews its grade; "grade higher when torn" and dedup-highest are per-agent and cannot act. Not a defect of the severity change, but the consensus's "one grader per task slice" has no redundancy at the smallest size.

ID: INV-013
CATEGORY: interaction_effects
ASSUMPTION: "Grade higher when torn" plus the regression check, the P2 HALT and `--unattended` `blocked` compose safely; extra blocking findings cost only a patch pass.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: Tie-break-up enlarges the blocking set at whichever line is blocking (A+: High/Medium; H+: Medium/Low). The regression check (SK:1610) fires on "a patchable item that PASSED at pass k ... FAILing with a High or Medium (blocking) finding at pass k+1" and halts with a byte-exact string. Under H+ an item whose pass-1 findings were Low (PASS; not patched, not re-verified) and that is re-graded Medium by a fresh sample halts the whole skill. At termination the skill HALTs (SK:1614); Stage 10.5 is fenced to start only after P2 terminates (SK:1621) and nothing says it runs after a HALT, so a spurious halt can remove the pre-reflect sign-off for that bundle. Under `--unattended` the run ends `blocked` with the open findings in `blocked_question` (SK:1615, CMD:113); the default worker policy is "report blocked" (`src/superclaude/core/WORKER-CONTRACT.md:54`) and a coordinator retry is a new Task (`:73`), which re-samples the same graders. A grade flip therefore becomes a blocked worker plus a retry that draws again. The consensus lists none of these links.

ID: INV-014
CATEGORY: interaction_effects
ASSUMPTION: The grading block and the agreed H+/A+ edits do not collide with the skill's existing TDD finding-level table or its label spellings.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: SK:1418-1423 fixes levels in capitals (HIGH/MEDIUM/LOW) for the `--spec` checks, while Stage 7 returns `High | Medium | Low` (SK:1386) and the synthetic finding is `severity: HIGH` (SK:1401); a label map declared "as module data" has one key spelling. H+ keeps SK:1421-1422 MEDIUM and blocking (B R2 table), yet its Medium definition is a dropped or softened criterion only, and consensus point 3 calls omissions High: a migration stage with no task bucket and a test-pyramid level with no task are omissions with a fixed MEDIUM level, so the agent gets two incompatible instructions ("grade by consequence, not by label" against a fixed level). A+ regrades them High, but the CLI treats all missing TDD coverage as MEDIUM, including §15 test cases (PR:124-125, :134; PRD gaps PR:152), so regrading SK:1422 to High widens the skill/CLI gap that A+ is meant to narrow. Not among the 32 agreed or 5 split points.

ID: INV-015
CATEGORY: interaction_effects
ASSUMPTION: CMD:113 versus SK sentence skew, the plugin mirror and `make verify-sync` add no further breakage.
STATUS: ADDRESSED
SEVERITY: LOW
EVIDENCE: CMD:113 reads "Under `--unattended` the unresolved High or Medium HALT resolves as blocked"; both worker-contract pins read the command file through `_unattended_section` (`tests/skills/test_worker_contract.py:893`, phrases at `:777`, `:1861`), which A R2 W4 and consensus point 4 already cover (untouched under H+, rewritten with CMD:113 under A+). No plugin mirror of `sc-tasklist-protocol` exists (`plugins/superclaude/skills` holds confidence-check, sc-implement-protocol, sc-recommend, sc-workflow-protocol). `make verify-sync` compares `src/superclaude/skills` against `.claude/skills` only, so an SK edit needs `make sync-dev` and nothing else. Residual: an SK sentence edited without CMD:113 stays green in the pins (they read CMD only) while the fixture rows catch the SK side, so partial landings are caught on one side only under A+.

ID: INV-016
CATEGORY: interaction_effects
ASSUMPTION: A later tasklist module on the core (the C-05 entry point) can use the label map without engine hazards.
STATUS: ADDRESSED
SEVERITY: LOW
EVIDENCE: Recorded in diff-analysis (U-004, U-012) but not carried into the consensus text. `reflect_category` forces `blocking == (severity != MINOR)` and a closed category set (`findings_v2.py:155-162`, `:41-48`), so a tasklist row on v2 must not set it. `card_convert.py` maps `high` to MAJOR and lists `medium` among MINOR words (`:71-83`), so a converter must use the module map, not that table. With the consensus (core gets nothing) both remain hazards for the future slot, and the C-05 entry text should name them.

ID: INV-017
CATEGORY: sufficiency_challenge
ASSUMPTION: "Nothing loosens before measurement, so H+ is behaviour-preserving" (consensus point 4; B R2: "Preconditions for H+: none").
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: H+ inserts its block immediately. Its Low class (B R2 block) holds "insufficient detail, ambiguity, effort-estimate divergence, a different but equivalent verification method, formatting, terminology, wording". Today every Medium blocks: SK:1439 (short-circuit needs zero High or Medium), SK:1537, SK:1571, SK:1608 (F_k counts High and Medium), SK:1614 (HALT). So a finding that reviewers type Medium today and that the block now routes to Low is no longer patched, re-verified, counted or halting: a loosening. B R2 itself calls Low the "one loosening H+ makes". The Low class uses the CLI MEDIUM wording "insufficient detail" (PR:58-59), the usual phrasing of a weakened or partial requirement (PR:62), so a real omission described as "insufficient detail" can be graded Low; the one observed failure is reviewers typing omissions Medium without any definition (v3.66 M2, test1 M1; B R2 W4). The false-clean measure FC(H+) is taken only in F2, after the block has landed, and the repair rule ("If FC(H+) >= 2 the H+ block is rewritten") assumes it is live. The tie-break-up rule tightens in the other direction. So H+ changes behaviour both ways before any measurement; point 4 and the H+ "default" must say so. Falsifying condition: any bundle in which a blocking-by-consequence defect is graded Low.

ID: INV-018
CATEGORY: sufficiency_challenge
ASSUMPTION: "A grading block + tie-break-up + dedup-highest makes the High|Medium (or Medium|Low) boundary safe" (A's W3 fix; B's adoption).
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: The W3 mechanism is across runs: SK:1608 re-runs the full Stage 7 set with fresh agents at the end of each pass, and F_k, the regression check (SK:1610) and monotonicity (SK:1611) compare separate samples. Dedup (SK:1410) acts inside one run and only on "the same issue on the same task"; slices are disjoint (SK:1357-1366), so each task has one grader per run and duplicates for one task arise only if an agent comments outside its slice. No merge step ever sees two samples, so dedup-highest cannot reduce between-sample variance. Tie-break-up changes each draw's bias, not the variance between draws, and relies on the grader recognising that it is torn (an unmeasured compliance, INV-004). The block gives the grader definitions, but nothing in the text makes the same finding land on the same side twice. The only evidence is F3, later, on 2 samples (INV-007) and with a per-finding threshold that does not bound the bundle outcome (INV-011). Falsifying condition: a fixed bundle whose blocking-class findings flip across the line between two fresh Stage 7 runs at a rate that makes `|F_2| < |F_1|` or a regression halt occur without any patch.

ID: INV-019
CATEGORY: sufficiency_challenge
ASSUMPTION: The consensus alone gives "consistent tasklist severity semantics without behaviour loss".
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: No branch-trace exists; inline enumeration of every filter between a Stage 7 finding and the verdict, with whether the change's target input (a finding typed by the new block) was shown to pass it. (1) Stage 7 agent types the label from the brief (SK:1384-1391): not shown; no run, F2 pending. (2) Merge/dedup (SK:1410): target input (same-task duplicates) is structurally rare, INV-018: not shown. (3) Stage 8 short-circuit (SK:1439): label keyed; shown by reading for H+; contradicted by SK:1716 (INV-008): not shown. (4) PatchChecklist and Stage 9 (SK:1531, :1537): Low never produces items; that `sc:task` can patch an H+ Medium "dropped criterion" is not shown by either variant. (5) Stage 10 spot-check (SK:1567-1576): label keyed; shown by reading. (6) F_k re-run (SK:1608): fresh draw; not shown (F3 pending). (7) Regression check (SK:1610): Low-to-Medium flip halts; not addressed (INV-013). (8) Monotonicity (SK:1611): count-based; relabel can shrink F_k (INV-007): not addressed. (9) P2 cap HALT and `--unattended` blocked (SK:1614-1615, CMD:113, pins `:777`, `:1861`): unchanged under H+; shown by pins. (10) Stage 10.5 after a HALT (SK:1621): not addressed. (11) CLI gate and exit (`commands.py:181-183`, `gates.py:34-45`): a separate producer the skill-side change never reaches; H+ keeps PR:62 (weakened criteria) MEDIUM there and blocking in the skill by declared exception, and the CLI keeps TDD/PRD gaps MEDIUM (PR:134, :152). So the outcome is falsified by construction for the weakened-criteria class (consensus point 3 concedes it) and by items 1, 2, 3, 6, 7, 8 and 10 until measured or specified. Falsifying condition: any one of those filters passing a mis-graded finding or blocking a correctly graded one.

ID: INV-020
CATEGORY: sufficiency_challenge
ASSUMPTION: F1/F2/F3 can overturn H+ ("A+ is never adopted by argument"; a not-run or unmet threshold leaves H+ in place), so the default is a neutral resting point.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: H+'s Medium class is written from the six archived findings (B's block cites "the v3.66 M3/M4 pattern"; B R2 W4 re-reads all six to define it), and F1 grades the same six, so F1 cannot fail H+ by construction; B's outcome rule for a "mixed" result is that H+ stays, the block text is revised once and F1 re-runs on the same six (tuning to the test set). Every unmeasured or inconclusive path maps to H+, which is not behaviour-neutral (INV-017), so the default favours one position while presenting itself as the status quo. The two archived bundles are the only data, both with High 0 (diff C-010), so F1 contains no High finding to test the High/Medium line at all. The decision rule maps each F2/F3 outcome to an action for the A+ upgrade; the only outcome that touches H+ itself (FC(H+) >= 2) rewrites the block text once, and no registered outcome withdraws the Low class. Falsifying condition: a seeded or archived blocking-class defect graded Low by a majority under H+ while F1 reports "H+ confirmed".

## Summary

Total findings: 20 (state_variables 2, guard_conditions 4, count_divergence 3, collection_boundaries 3, interaction_effects 4, sufficiency_challenge 4).

By status: ADDRESSED 3 (INV-006, INV-015, INV-016); UNADDRESSED 17.

By severity: HIGH 2 (INV-017, INV-018); MEDIUM 12 (INV-001, 003, 004, 005, 007, 008, 010, 011, 013, 014, 019, 020); LOW 6 (INV-002, 006, 009, 012, 015, 016).

Both HIGH items are in Category 6 and are UNADDRESSED: H+ is not behaviour-preserving because its block lands unmeasured and moves the "insufficient detail / ambiguity" class to a non-blocking Low (INV-017), and dedup-highest plus tie-break-up do not act on the across-run re-sampling that SK:1608 creates (INV-018).
