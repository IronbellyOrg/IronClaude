# Round 2 advocate for Variant A (slot X-15, tasklist Medium and fidelity vocabulary)

Status: Complete (Round 2 of 2, advocate A, goes first; HEAD `50d4d2b9d`). Position: hybrid A+ (consequence-graded Medium, adoption gated on measurement, fallback to B's H).

## Responses to Round 1 criticisms

Tags: [READ] = re-read at HEAD in this session. [DIFF] = from diff-analysis.md or a Round 1 file, not re-read. [INFER] = my inference. Paths are repo-relative. SK = `src/superclaude/skills/sc-tasklist-protocol/SKILL.md`; PR = `src/superclaude/cli/tasklist/prompts.py`; PM = `src/superclaude/output-styles/pragmatic.md`; CMD = `src/superclaude/commands/tasklist.md`.

Re-read this session: SK:1340-1625 (Stage 7 to Stage 10.5), PR:1-115, PM:222-233, CMD:113, `sc-implement-protocol/refs/qa.md:81` and `:274`, `tests/skills/test_worker_contract.py:768-781, 886-906, 1853-1905`, `tests/tasklist/test_tasklist_fidelity.py:38-112`, `src/superclaude/cli/tasklist/commands.py:165-186`, the sweep fixture header (`tests/skills/fixtures/review_severity_sweep_edits.yaml:23-29`).

**W1 (A copies the CLI Medium, but A's answer 2 says a weakened criterion that makes a roadmap-stated check unverifiable is High). CONCEDED.** PR:62 lists "Acceptance criteria are weaker than the roadmap's success criteria" as a MEDIUM example [READ]. Stage 7 dimension 4 is "weakened criteria" (SK:1381) [READ]. My R1 grading rule and my "adopt the CLI definitions" claim contradict each other on exactly that class, so parity test T2 cannot hold while they do. Fix: the weakened-criterion example at PR:62 must be split by consequence (see Hybrid). If PR:62 is not edited, then weakened-but-present criteria are Medium everywhere, with no carve-out.

**W2 (the union mitigation does not exist at Stage 7). CONCEDED in R1, stays conceded.** SK:1357-1366 gives each task slice to one agent [READ]. What replaces the union: the grading block, a tie-break-up rule, "keep the highest severity" at dedup, and a measurement (M-X15-5 below).

**W3 (a re-sampled grade becomes verdict-decisive under A). CONCEDED IN PART. This is B's best point and I do not fully rebut it.**
- Fact: SK:1608 recomputes `F_k` by re-running "the FULL Stage-7 2N validation set" with fresh agents [READ]. SK:1410 dedup says "keep only one entry" with no severity rule [READ]. A task's grade is therefore sampled up to three times, and the merge may keep either duplicate.
- Under A (`F_k` = High only): a defect typed High at pass 1 and Medium at pass 2 leaves `F_2` and nothing is patched or flagged unresolved. That is a false-clean path. The reverse (a new High on a previously-PASS task) trips the regression halt at SK:1610. Under B both directions are verdict-neutral because both labels count in `F_k`.
- What I keep: under B the same re-sampling acts on the Medium/Low boundary (Low is dropped from `F_k`, SK:1608), so B moves boundary sensitivity, it does not remove it. B's boundary is easier to define (CLI LOW: "do not affect execution correctness", PR:65-66) [READ]; whether it flips less is [UNVERIFIED]. And a false-clean under A is not silent: the Medium section of `ValidationReport.md` stays (SK:1478) and lists the row [READ].
- Fix: dedup keeps the highest severity (conceded in R1); the grading block says "when torn between High and Medium, grade High"; M-X15-5 below measures the flip rate directly. If it exceeds a pre-registered threshold, A falls back to B's H.

**W4 (A's edit list omits `commands/tasklist.md:113`). CONCEDED, and I now know more.** CMD:113 reads "Under `--unattended` the unresolved High or Medium HALT resolves as blocked ..." [READ]. Both worker-contract pins check that sentence in the `## Unattended mode` section of the command file, not in SK: `_unattended_section` reads `COMMANDS_DIR/<name>.md` (`test_worker_contract.py:893-906`); `UNATTENDED_EXPECT["tasklist"]` holds the phrase at `:777`; `P2_GATES` holds it at `:1861`, with a reversal check at `:1880-1905` [READ]. SK:1615 says only "this HALT resolves as blocked". A's full edit set is therefore: SK sites + CMD:113 + 2 test pins + 12 fixture rows + the byte-equal plan copy `.dev/review-severity-rule/sweep-edits.yaml` [DIFF for the plan copy].

**W5 (Form 2 is new core code the adjudicated shape excludes). CONCEDED. Form 2 withdrawn.** `findings_v2.py:155-162` forces `category` into a closed set and ties blocking to `severity != MINOR`, so it cannot be reused; C-02 ruled out a core predicate [DIFF]. Form 1 only: the brief and grading block define the map, no parse-edge rule. T4 is dropped.

**W6 (A reads S5 wider than written). CONCEDED.** PM:229 names CRITICAL/IMPORTANT/MINOR and PM:231 names CRITICAL/MAJOR/MINOR; nothing names High/Medium/Low [READ]. What I still rely on is narrower and written: PM:225 defines blocking by consequence (wrong behaviour, false claim, missing required deliverable, security or data-loss risk); PM:229 and :231 say grade by definition or consequence, not by label; PM:230 says what the word Medium means in this repo (a real, non-blocking weakness that never fails a review) [READ]. The claim is "the repo rule applied by analogy", not "S1-S5 as written".

**W7 ("one product" inconsistency). CONCEDED in R1, stays.** The accurate claim is one product family with one readiness question, not one code path. I also withdraw "the CLI is a gap" (X-007: both readings are inferences).

**W8 (A loosens the only hard gate on bundle shipping). TRUE, and it is the real cost.** Today a Medium residual HALTs at the P2 cap (SK:1614) [READ]. Under the hybrid below it completes with a follow-up list. That is acceptable only if every finding that is blocking by consequence is graded High, which is why the measurement gates adoption.

**Hybrid H of B.** Tested in the next section.

## Hybrid assessment / proposed hybrid

### Test of B's Hybrid H on its merits

H = blocking Medium defined as "incomplete or weakened against a stated roadmap requirement"; pure wording and ambiguity moved to Low; a grading block; a parity test; no pinned row, CMD:113 or CLI gate changed.

**Does H's Medium collapse into the CLI HIGH? Honest answer: no, my R1 dilemma (Weakness 2) was overstated for H.** It was correct for B's original undefined Medium. Mapped onto the CLI text [READ, PR:51-64]:
- roadmap item with no task (PR:53), fabricated ID (PR:55), contradicted dependency (PR:56), "deliverables omit outputs specified in the roadmap item" (PR:57) = CLI HIGH.
- "Acceptance criteria are weaker than the roadmap's success criteria" (PR:62) = CLI MEDIUM.
H's "incomplete or weakened" therefore equals the PR:62 class plus a thin edge of PR:57. That is a real, separate zone, not a relabelled High. So H is a coherent position and the dispute is narrower than R1 made it: **the two sides now disagree about one class, "weakened but still present", and about nothing else in outcome.**

**What still counts against H (checkable):**
1. H blocks on the one class the CLI passes (PR:62 under MEDIUM; `tasklist_ready` true at high count 0, PR:99-100; exit 1 on HIGH only, `commands.py:181-183`) [READ]. H keeps a skill-versus-CLI disagreement, reduced to one class, not removed.
2. H's Low swallows "ambiguous language ... that could lead to execution issues", which the CLI calls MEDIUM (PR:58-60) [READ]. So H also disagrees with the CLI at the Medium/Low boundary, and a skill Low is then "notes only" while the CLI Low is "do not affect execution correctness" (PR:65-66).
3. H's parity test is hollow or false: H's Medium blocks and the CLI's passes, so the test can assert agreement on blocking semantics only by failing, or assert only that the three label words exist.
4. H keeps the word "Medium" meaning blocking against PM:230, `qa.md:81` and `:274` (medium = minor or note), and `card_convert.py:81-83` (medium to MINOR) [READ for PM and qa.md; DIFF for card_convert]. B's own U-012 caution (a converter must not use the repo table for tasklist rows) is the cost of that collision, paid by every future consumer.

**What H gets right (and A cannot match):** (1) the High/Medium boundary is verdict-neutral under re-sampling (W3); (2) nothing pinned changes: 12 sweep rows, CMD:113, two worker-contract pins stay green. Those are real and I weigh them below.

### Proposed hybrid: A+ (consequence-graded Medium)

Same outcome as H on every class except "weakened but still checkable". It differs from H in labels and in the loop's counting.

**Grading block (new, inserted after SK:1391, at most 12 lines; text checkable by T2):**
- **High (blocking):** the task omits, contradicts or fabricates a roadmap item, deliverable, ID or dependency; or a criterion, validation step or exit condition is dropped or weakened so that a roadmap-stated check can no longer fail.
- **Medium (warning, not blocking):** the roadmap requirement is still present and still checkable but with insufficient detail, ambiguous language that could lead to execution issues, a diverging effort estimate, or a different verification method.
- **Low (notes):** formatting, organisation, terminology that does not change meaning.
- Rules: grade by consequence, not by label (PM:229, :231); when torn between High and Medium, grade High; the dedup step at SK:1410 keeps the highest severity.

**Skill sites that change (all High only):** SK:1439 (short-circuit), SK:1450 (guard line), SK:1531, SK:1537, SK:1567, SK:1571, SK:1608 (`F_k`), SK:1610 (regression check), SK:1614 (termination HALT); SK:1421-1422 regraded MEDIUM to High (omission-type; SK:1420 is already HIGH) [READ]; SK:1588-1589 example rows become High rows; SK:1478 heading gains "(warnings: follow-up candidates, not patched, not re-validated)". SK:1445 names no label and stays. Risk labels (SK:565, 581, 964, 1699) and `MEDIUM` as a complexity class (SK:735) stay untouched [READ].

**What happens to Medium-only residuals:** the bundle completes; Medium rows stay in `ValidationReport.md` with their evidence as follow-up candidates; no new prompt is added by this slot (PM:230's one-time user question is the session's existing behaviour, `--unattended` only records, per PM:230).

**What happens to the 12 pinned rows (S-119..S-130):** rewritten, not kept. Row count stays 139. CMD:113 becomes "the unresolved High HALT resolves as blocked"; the two pins at `test_worker_contract.py:777` and `:1861` follow; the byte-equal plan copy `.dev/review-severity-rule/sweep-edits.yaml` changes with the fixture. This is the price of the label rename and it is higher than H's price (zero). I state it as a cost.

**CLI side (prompt text only):** PR:62 is split: MEDIUM example becomes "Acceptance criteria are less detailed than the roadmap's success criteria but every roadmap success criterion is still checkable"; HIGH gains the example "An acceptance criterion or validation step drops or weakens a roadmap success criterion so that it can no longer fail". Gate, six frontmatter fields, exit code, `_tasklist_ready_consistent` unchanged. No existing test pins the PR:62 text (`tests/tasklist/test_tasklist_fidelity.py:23-97` checks only the `**HIGH**/**MEDIUM**/**LOW**` headings, field names, dimension names and DEV-NNN; a grep of `tests/` for "weaker" finds nothing relevant) [READ]. This is a classifier-behaviour change for the CLI (more HIGH on this class), so it needs the same measurement as the skill. If the owner will not touch PR, take H: a parity test with a documented exception is not worth having.

**Tests (static, no model call):** T1 rewrite 12 rows + CMD:113 + 2 pins (red before, green after). T2 parity: the skill block and `build_tasklist_fidelity_prompt` output both place omit/contradict/fabricate/criterion-can-no-longer-fail in High, insufficient-detail/ambiguity in Medium, formatting in Low; both say `F_k` / `tasklist_ready` count High only. T3 existing CLI pins pass unchanged (`test_tasklist_fidelity.py:208-225`, `test_tasklist_cli.py:165-179` [DIFF]). T4 (new, replaces Form 2): the skill states "keep the highest severity" at the dedup step and the tie-break-up rule.

**Diff points this resolves or narrows:**
- C-001, C-004, C-013 (one definition set, split on PR:62); C-002 (basis is PM:225 consequence test by analogy; S4 not needed); C-003 (Form 1 only); C-007 (loop counts High only, with highest-severity dedup and tie-break-up as boundary mitigation); C-008 (placement outside the core, parity-tied); X-004 (omission regrade is the rule, tested by M-X15-1); X-009 (no union claimed).
- Not resolved: C-005 and C-006 (A+ really edits more text and pins than H); X-003 (history); W3 residue (re-sampled High/Medium boundary is verdict-decisive; mitigated and measured, not removed).

**Fallback:** if the measurement gate fails (Central question c), adopt H exactly as B states it. I do not keep A+ against the data.

## Central questions

**(a) Does a tasklist Medium block?** No, under A+: Medium is a real but non-blocking weakness (the repo's own meaning, PM:230), and anything that is blocking by consequence is graded High by the definition. This answer is conditional on the measurement in (c). The disagreement with H is one class: a weakened criterion whose roadmap-stated check is still checkable. By the repo's consequence test (PM:225; PM:231 for MAJOR: blocking only when it names a concrete wrong outcome an implementer would produce) that class has no concrete wrong outcome, so it warns. I cannot prove that from code; the six archived Mediums contain two such items by my R1 read (v3.66 M3, M4) and B counts them as incomplete, so n is 2 and the answer is not decided by data.

**(b) Is the fidelity prompt a tasklist-module vocabulary under the core now?** No. I move to B's placement. Reasons I now accept: no core code consumes the vocabulary today (A-005: Stage 7 findings are prose, SK:1384-1391 [READ]); A's role table is a design intention, no module-declared role or pair table exists (X-005, `ROLES` closed, `findings_v2.py:35` [DIFF]); and moving it would add a second vocabulary in the core or touch the six-field frontmatter shared with `SPEC_FIDELITY_GATE` (`roadmap/gates.py:1322-1345` [DIFF]). The prompt stays in `cli/tasklist/`. What I keep from A: the parity test T2 tying the skill's grading block to the prompt's definitions, and the PR:62 split so that the two texts can actually agree. B's named seam (a read-only adapter from a finished deviation report to core rows, B U-013) is the later route if tasklist review ever enters the core.

**(c) What must be measured first, and is it a precondition?** It is a precondition for the loosening (the Stage 8-10 High-only edits, the 12 rows, CMD:113, the 2 pins), not for the grading block, T2 or the placement decision, which carry no behaviour change and can land first or separately. Measurements, all thresholds registered before any grader runs (a design choice, no evidence fixes the numbers; mine are proposals, B's 2/3 rule from M-X15-1 applies as written):
- **M-X15-1 (B's, retrospective):** blind-grade the six archived Medium findings (v3.66 M1-M4, test1 M1-M2) by the A+ block, 3 independent graders. Expectation I register: v3.66 M2 and test1 M1 graded High by at least 2 of 3. If either lands Medium by majority, A+ fails.
- **M1 (mine, seeded):** grading block only, a set of at least 10 seeded omission-class and criterion-dropped defects plus 10 seeded ambiguity or estimate defects; 3 blind graders. Proposed pass: at least 9 of 10 omission-class defects graded High by majority; proposed fail: any ground-truth blocking class (by the `/sc:implement` checklist, `qa.md:81`) with a Medium majority.
- **M-X15-5 (new, answers W3):** run Stage 7 grading twice with fresh agents on the same tasklist; count findings whose grade flips between High and Medium. Register the flip-rate threshold before the run (proposal: above 1 in 5 of High-class findings fails A+).
- If any of the three fails, adopt H as B states it. If all pass, adopt A+.

## Updated per-point positions

Key: A = Variant A, B = Variant B, Hybrid = A+ (above) unless another is named. "Moved" marks a change from my Round 1 position.

| Point | Position | One-line reason |
|---|---|---|
| S-001 | A | An inputs table up front lets a reader check dependencies first. |
| S-002 | A | One fact per row with its own tag is checkable; B's E1 bundles six cites. |
| S-003 | Neither | Heading depth does not affect the argument. |
| S-004 | B (moved) | Fidelity prompt stays outside the core with an adapter seam; no consumer or role table exists. |
| S-005 | Hybrid | A's static tests T1-T4 plus B's pre-registered thresholds and the new flip-rate measurement. |
| S-006 | Neither | Scope statements are cosmetic. |
| S-007 | B | B's stop condition is more useful; A+ adopts the same device (fall back to H if measurement fails). |
| C-001 | Hybrid | Medium warns, High is defined by consequence, adoption gated on M-X15-1, M1, M-X15-5. |
| C-002 | Hybrid (moved) | PM:225 consequence test applied by analogy decides; neither S4 (X-002) nor S5 as literally written (X-006). |
| C-003 | B (moved) | Form 2 withdrawn; Form 1 only, no core code. |
| C-004 | A | Grading block plus TDD checks at SK:1421-1422 to High; H also adds a block but keeps those blocking. |
| C-005 | B | B's edit is smaller; A+ pays about ten sites, CMD:113, 12 rows and 2 pins, stated as cost. |
| C-006 | B | B holds every pin; A+ rewrites 12 rows, CMD:113 and 2 pins. |
| C-007 | Hybrid | High-only `F_k` with highest-severity dedup, tie-break-up and M-X15-5; B is right that boundary re-sampling is the risk. |
| C-008 | Hybrid (moved) | B's placement outside the core; A's parity test T2; role table and adapter deferred. |
| C-009 | B | The shared six-field contract is a reason to leave the gate and prompt location alone. |
| C-010 | B | B has the only data; my re-reading corrects its interpretation (2 omissions, 2 acceptance gaps, 2 assumption items) but does not replace it. |
| C-011 | Hybrid | Static T1-T4 from A, B's pre-registered thresholds, plus M-X15-5. |
| C-012 | Neither | Boundary exposure exists under both; B's is Medium/Low, A's is High/Medium. |
| C-013 | Hybrid | Take High and Low from PR:51-69; split PR:62 by consequence; H's Low for ambiguity is rejected (CLI calls it Medium). |
| C-014 | A | Medium as warning matches rf-qa, `qa.md:81`, `card_convert`; H's blocking Medium needs a tasklist-specific exception. |
| X-001 | Neither | Both overread S4/S5; the PM:225 consequence test is the decider. |
| X-002 | A | Conceded by B: the skill states no model before B's edit. |
| X-003 | B | Fixture header (`:29`) records "open High/Medium findings HALT" as the intent; the dispute is only its framing. |
| X-004 | Hybrid | B on what reviewers did; A on the regrade; settled by M-X15-1, not by argument. |
| X-005 | B | No module-declared role table exists today. |
| X-006 | B | PM:229/:231 name no High/Medium/Low scale. |
| X-007 | Neither | "Gap" and "no fixer" are both inferences. |
| X-008 | B | One product family, not one code path. |
| X-009 | B | One grader per task slice; no union. |
| X-010 | A | B's ranges were wrong (`PR:49-69`, `:195-240`, `:208-225`); my `.py`-only count caveat stands. |

**A-004 to A-009.** Unchanged unless stated.
- A-004 QUALIFY (unchanged). A-005 QUALIFY (unchanged; it now also drives (b)). A-006 QUALIFY (unchanged). A-007 ACCEPT (unchanged).
- **A-008: QUALIFY changed to REJECT.** SK:1608 re-runs the full set with fresh agents and SK:1410 has no severity tie-break, so a task's grade is not final across passes (W3). I agree with B.
- **A-009: ACCEPT changed to QUALIFY.** Static counts hold, but no test was run by me, and the pin inventory was incomplete until CMD:113 and the `_unattended_section` read path were added (W4).

## Remaining disagreements

1. **The one class: weakened but still checkable.** B and H block it (Medium, blocking); A+ warns. Neither side has data beyond two archived items. Decided by M-X15-1 and M1, not by argument.
2. **Where the weight of the pinned text goes.** B weighs a zero-churn change (12 rows, CMD:113, 2 pins untouched) above naming consistency with PM:230, `qa.md:81`, `card_convert.py` and the CLI. I weigh the reverse, because the churn is one-time and static (T1 is red before, green after) while the naming collision is paid by every later consumer. This is a judgement, not a fact.
3. **Whether H's Low for ambiguity is acceptable.** I say no: the CLI calls "ambiguous language that could lead to execution issues" MEDIUM (PR:58-60). B has not said why the skill's Low may differ from the CLI's.
4. **Whether to edit PR:62.** A+ needs the split; H does not. B will likely call the CLI prompt edit scope creep and a classifier-behaviour change. I accept that cost only with the measurement gate; the alternative is H.
5. **How bad boundary re-sampling is.** W3 shows the mechanism in code (SK:1608, SK:1410) for both A+ and B at different boundaries. Which flips more is [UNVERIFIED]; M-X15-5 measures A+'s boundary only. For a fair comparison B's Medium/Low flip rate must be measured by the same run (I propose M-X15-5 records both).
6. **Not disputed any more:** Form 2, the union mitigation, S4 as B's basis, S5 as literal text for High/Medium/Low, the "one product" wording, B's line ranges.

## New evidence

All [READ] this session unless marked.
1. **The pinned HALT sentence lives in the command, not the skill.** CMD:113 ("the unresolved High or Medium HALT resolves as blocked"); SK:1615 says "this HALT resolves as blocked". `_unattended_section` reads `COMMANDS_DIR/<name>.md` (`test_worker_contract.py:893-906`); pins at `:777` (inside `UNATTENDED_EXPECT`) and `:1861` (inside `P2_GATES`, with a remove/reverse/add-reversed negative check at `:1893-1905`). Any change to the sentence must edit CMD:113.
2. **No test pins the CLI's weakened-criteria example.** `tests/tasklist/test_tasklist_fidelity.py:23-97` asserts headings, frontmatter field names, dimension names and `DEV-NNN`/`[MISSING]`; a grep of `tests/` for "weaker" and "insufficient detail" finds no assertion on the PR:58-64 text. A PR:62 split would not break an existing test; it would need its own (T2).
3. **H's Medium maps onto exactly one CLI example.** PR:62 is the only CLI line that says "weaker than the roadmap's success criteria"; PR:57 ("deliverables omit outputs specified") is HIGH. This narrows the dispute to one class (Hybrid section).
4. **`/sc:implement`'s model words, twice.** `qa.md:81` and `:274` both say medium maps to `minor` or `note` and every minor and note is "recorded in the notes file and cleared: no halt, no Ruling, no user prompt" (`:274`). S4's own exemplar therefore treats Medium as non-blocking in two places.
5. **Blocking-label sites in SK.** By grep of `Medium|MEDIUM` over SK plus my reads of SK:1340-1625, the sites that gate on High-and-Medium are SK:1439, 1450, 1531, 1537, 1567, 1571, 1608, 1610, 1614 (plus CMD:113). The TDD table rows (SK:1420-1423) set a finding level, and the Risk/complexity uses (SK:565, 581, 735, 964, 1699) are not severity gates. I did not grep other skills or refs for a consumer of the tasklist label (UNVERIFIED beyond SK and CMD).
6. **Not re-read, still [DIFF]:** `findings.py` and `findings_v2.py` line facts, `card_convert.py:71-83`, `roadmap/gates.py:195-240` and `:1322-1345`, `test_review_severity_rule.py:268-283`, the two archived ValidationReports, the C-01/C-02/C-03 adjudication files. I ran no tests.
