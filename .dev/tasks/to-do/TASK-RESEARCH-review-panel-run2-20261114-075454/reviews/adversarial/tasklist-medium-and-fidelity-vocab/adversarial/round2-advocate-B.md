# Round 2 advocate for Variant B (slot X-15, tasklist Medium and fidelity vocabulary)

Status: Complete (Round 2 of 2, advocate B, goes second; HEAD `50d4d2b9d`). Position: hardened Hybrid H (called H+ below), with a registered, measurement-gated upgrade path to A's A+.

Tags: [READ] = re-read at HEAD in this session. [DIFF] = taken from diff-analysis.md or a Round 1/2 file, not re-read. [INFER] = my inference. Paths are repo-relative. SK = `src/superclaude/skills/sc-tasklist-protocol/SKILL.md`; PR = `src/superclaude/cli/tasklist/prompts.py`; PM = `src/superclaude/output-styles/pragmatic.md`; CMD = `src/superclaude/commands/tasklist.md`; FX = `tests/skills/fixtures/review_severity_sweep_edits.yaml`.

Re-read this session: SK:1340-1629; PR:1-120; PM:220-233; `sc-implement-protocol/refs/qa.md:81` and `:274` (grep); CMD:113 (grep); `tests/skills/test_worker_contract.py:777`, `:1861` (grep); `tests/tasklist/test_tasklist_fidelity.py:15-124`; `cli/tasklist/commands.py:160-186`; FX:1-32; both archived ValidationReports (v3.66 lines 1-60, test1 lines 1-45); callers of `build_tasklist_fidelity_prompt` and `TASKLIST_FIDELITY_GATE` (grep over `src/`).

## Responses to criticisms

### Round 1 weaknesses (A against B)

**W1 (B's S4 premise holds only after B's own edit). CONCEDED in R1, stays.** The skill defines no model today (SK:1384-1391 lists `High | Medium | Low` and defines none) [READ]. H+ adds the definition, so after the edit the skill "defines its own severity model" in PM:228's sense. qa.md:81 and :274 are another protocol's model; PM:228 says each protocol applies its own, so two protocols giving the word different meanings is what S4 anticipates [READ]. I rest on PM:225 and PM:231 (grade by consequence), not on S4 alone.

**W2 (B's Medium is a dilemma: CLI text = non-blocking, S1-qualified text = CLI HIGH). CONCEDED IN PART; A's Round 2 already retreated, and I accept the retreat.** The dilemma is real for a Medium left undefined. For a defined Medium it fails: the only CLI line that says "weaker than the roadmap's success criteria" is PR:62 under MEDIUM; PR:57 ("deliverables omit outputs") is HIGH [READ]. H+ Medium = the PR:62 class, so it is not a relabelled High. What stays true: that class is CLI MEDIUM, which does not gate. I now state that as a declared divergence, not as a "calibrated apart" claim.

**W3 (two opposite readiness answers). CONCEDED, narrowed to one class.** CLI: `tasklist_ready` true at high count 0 (PR:99-100); exit 1 on HIGH only (`commands.py:181-183`) [READ]. Skill: a Medium residual HALTs (SK:1614). After H+ moves ambiguity and insufficient detail to Low (both non-blocking in both places), the two disagree on one class only: a criterion or check dropped or weakened. My Round 1 reason ("no fixer, so no gate") is an inference (X-007); H+ does not rely on it. It relies on the consequence test (below).

**W4 (E6/E7 overstate the archive). CONCEDED.** My re-read of all six archived Medium findings:
- Omission of a roadmap item: v3.66 M2 (section 9.7), test1 M1 (Phase 1 exit criterion, no task).
- Roadmap-required check dropped from the acceptance list while Steps/Deliverables still name it: v3.66 M3 (retention template), v3.66 M4 (4 of 5 refs files; the report says Deliverables lists all 5).
- Step text contradicts a roadmap target: test1 M2 (step says >60%, roadmap beta target >40%; acceptance criteria correct).
- A criterion hard-codes an "expected" value as fact: v3.66 M1.
So "mostly omission" was wrong, and E7 ("both bundles short-circuit with 4 and 2 Medium unpatched") assumed a label flip with no regrade. Neither is restored. One reader, six items: [UNVERIFIED] as a measurement.

**W5 (regression halt widens under blocking Medium). TRUE as a mechanism, but it is the status quo.** SK:1610 keys on "High or Medium (blocking)" today [READ]. H+ does not enlarge it relative to today; A+ shrinks it only if grading is right, and A+'s own tie-break-up (grade High when torn) pushes borderline findings back into the counted set, so A+'s counted set approaches H+'s from below. This point no longer separates the two.

**W6 (B's new text is unpinned; M-X15-1 cannot lose cleanly). CONCEDED.** H+ gets pins (static test of the block, the tie-break and dedup rules, the containment test) and a decision rule that maps every outcome band to an action (see Final position).

**W7 (`card_convert.py` supports A). CONCEDED as naming evidence, not as design evidence.** It is a fourth source where "medium" means non-blocking (qa.md:81, :274, PM:230, the CLI gate). It serves legacy reflect cards and never sees tasklist rows; the module map stays module data, so no consumer reads the word across modules [DIFF for card_convert]. It is a cost of the collision, which I price below.

### Round 2 (A's A+ and A's four counts against H)

**Four counts against H.** Tested honestly in "Assessment" below: count 1 true, count 2 true for wording and false for outcome, count 3 true for H as written and fixable only partly, count 4 true and measurable.

**A+ grading block, Stage 8-10 High-only, dedup-highest, tie-break-up, gating.** Dedup-highest and tie-break-up: ADOPTED into H+ (they answer my own W3 from Round 1 without changing any label). The grading block: ADOPTED with the consequence boundary (below). High-only counting and the label rename: NOT adopted now (reasons in Assessment). Gating adoption on M-X15-1, M1, M-X15-5: ACCEPTED as the right evidence bar, and it argues for H+ as the default, because loosening a pinned hard gate needs evidence and keeping it does not.

**CLI prompt line PR:62 split.** NOT adopted in H+. The prompt has exactly one caller (`executor.py:173`) and the gate one (`executor.py:180`) [READ]; the phrase occurs once in `src/` (`prompts.py:62`) [READ]. So the edit cannot reach SPEC_FIDELITY_GATE's classifier (that gate shares frontmatter checks, not this text); it would raise the exit-1 rate of `superclaude tasklist validate` on tasklists with weakened-but-present criteria. That is a behaviour change for a CLI nobody asked to change. I do not call it scope creep; I call it a separate owner decision that A+ cannot avoid and H+ can.

**W3-style boundary sampling.** I withdraw the claim that B's boundary is "easier to define". See Assessment: under the consequence boundary the blocking/non-blocking line has identical content in A+ and H+. The real asymmetry is the buffer tier (below).

## Assessment of A+ and of H

### What A+ gets right

1. **The consequence boundary is the right test.** PM:225 defines blocking by consequence (wrong behaviour, false claim, missing required deliverable); PM:231 says a MAJOR blocks only when it "names a concrete wrong outcome an implementer would produce" [READ]. "A roadmap-stated check can no longer fail" is that test applied to a weakened criterion. I adopt it as H+'s blocking boundary. It is better than my Round 1 "incomplete or weakened" because it is checkable per finding.
2. **One blocking tier matches every other written model.** PM:230, qa.md:81 and :274, the CLI gate and the sweep fixture's two-bucket rule all treat a middle word as non-blocking or leave it out (FX:4-6) [READ]. A+ is the only variant where "Medium" means the same thing in the skill and next to it.
3. **Dedup-highest and tie-break-up are real fixes** for SK:1410's missing severity rule [READ]. They are label-independent, so H+ takes them.
4. **Honest gating.** A+ states its loosening (Medium-only residuals complete, W8) and ties it to evidence. That is the correct bar.

### Where A+ and H+ are actually the same

With A's own boundary, the blocking set is identical by construction:
- A+ High = omits/contradicts/fabricates, or a criterion dropped or weakened so a roadmap-stated check can no longer fail. A+ Medium/Low = still present and checkable, plus ambiguity, detail, estimates, method, formatting.
- H+ High + Medium = the same first group, split into two words. H+ Low = the second group.
The blocking/non-blocking line has the same content in both, so its sampling risk is the same too: the same defect flips across the same line at the same rate if the same text grades it. That retires my Round 1 "B's boundary is more separable" and A's W3 "B's is easier" alike. A+ and H+ differ in four things only: (1) the label word on the second blocking sub-class; (2) the buffer tier (below); (3) churn: A+ edits about ten SK sites, CMD:113, two pins (`test_worker_contract.py:777`, `:1861`), 12 fixture rows and the byte-equal plan copy, H+ edits none of these; (4) A+ needs the PR:62 split to make its parity test true, H+ does not. I find no fifth difference, and A's Round 2 text lists none.

### What remains wrong or risky in A+

1. **No buffer tier.** Under H+ a defect typed High but graded Medium still blocks; under A+ it is a false-clean (Stage 8 short-circuit at SK:1439 can fire; `F_k` drops it at SK:1608). The one failure we have observed is exactly that: with no grading block, real reviewers typed two real omissions Medium (v3.66 M2, test1 M1) [READ]. A+ fixes it by an untested instruction (the block plus tie-break-up). H+ is robust to it whatever reviewers do. A concedes this is "a design assumption" (R1 X-004) and makes M1 the gate; I agree M1 is the gate, which is why H+ is the default until M1 runs.
2. **"Grade High when torn" enlarges High.** It is the right safety rule, but it makes A+'s blocking set approach H+'s from below on exactly the cases where the two differ. Then A+ pays roughly thirty edit sites by A's own list (about a dozen SK lines, CMD:113, two pins, 12 fixture rows, the plan copy) and a CLI change to approximate a set H+ already has. [INFER: the count is my sum of A's Round 2 list, not a grep.]
3. **The PR:62 split is a classifier change to the CLI.** `tasklist validate` has one prompt caller, `executor.py:173` [READ]. Moving "acceptance criteria dropped or weakened so a check can no longer fail" into CLI HIGH raises HIGH counts and so the exit-1 rate on real tasklists. A calls this "the same measurement as the skill"; the measurements in A's list (M-X15-1, M1, M-X15-5) all run on the skill's Stage 7 and none measures the CLI prompt's HIGH rate. [INFER] It needs its own run.
4. **Parity test content.** For A+ it is a real test only after PR:62 is edited; before that it can only assert label words, which A said of H.
5. **Label-driven loop state.** `F_k` counts High only; the regression halt (SK:1610) and the P2 termination HALT (SK:1614) all depend on one typed word at a boundary that a re-sampled agent decides. The buffer is what makes H+ verdict-neutral at the High|Medium word; A+ has no equivalent.

### Test of H against A's four counts (honest)

1. **H blocks on the one class the CLI passes. TRUE.** PR:62 is CLI MEDIUM (non-gating; test `test_tasklist_fidelity.py:208-225` pins the Medium-passes behaviour) [READ]. H+ states it as a declared divergence on one class, with the S1/PM:231 consequence test as the reason, and makes it a named exception in the parity test. It is not removed. If the owner accepts the PR:62 split, the structural answer is A+ (one blocking tier). That is the condition in my upgrade rule.
2. **H's Low swallows CLI-MEDIUM "ambiguous language". TRUE for wording, FALSE for outcome.** Both are non-blocking, so the verdict is identical. But the label text differs (skill Low "notes", CLI Low "do not affect execution correctness", PR:65-66) [READ]. Fix in H+: the skill's Low definition names "insufficient detail, ambiguity, estimate divergence, equivalent-method differences" explicitly and says Low findings are listed in `ValidationReport.md` (the SK:1481 section), which is the follow-up list PM:230 asks for. The sweep header calls "cosmetic, wording, style, optional polish" minor (FX:5-6) [READ], so Low for wording-class findings is the repo's own bucket.
3. **H's parity test is hollow. TRUE for H as written.** Full parity needs the PR:62 split. H+'s test is weaker but not empty: (a) every skill High example is a CLI HIGH example (PR:53-57); (b) every CLI LOW example (PR:67-69) is inside the skill's Low class; (c) no skill-Low example appears under CLI HIGH; (d) the skill block carries the exception sentence naming the PR:62 class. It fails if any text drifts or the exception is silently dropped. It does not assert agreement on that class, because there is none.
4. **Medium naming collision. TRUE and measurable.** Reviewers' priors may type ambiguity Medium (CLI and PM:230 taught that), and under H+ Medium blocks, so the false-block channel is real. Mitigation: inline "(blocking)" already follows Medium at SK:1439, :1567, :1610, :1614 and "blocking (High and Medium)" at :1537 [READ]; the block defines it; and M1's false-block count (FB below) measures the cost. If FB(H+) is large, that is the evidence that A+'s rename pays for itself.

### Is the remaining dispute naming versus churn?

Mostly yes, after the boundary converges. A's naming side: Medium means non-blocking in PM:230, qa.md:81 and :274, `card_convert.py:81-83`, the CLI. My churn side: zero pinned rows, CMD:113 and two pins untouched, no CLI behaviour change, no loosening before evidence. I weigh them as: the churn buys label consistency for a word that the skill already tags "(blocking)" inline at six or more sites; the loosening and the CLI change are behaviour changes. That is a judgement, not a fact, and the registered rule below lets measurement overrule it.

## Final position

**Position: H+ now; A+ only by a registered upgrade rule.** H+ is B's Hybrid H with four additions taken from A: A's consequence boundary, dedup-highest, tie-break-up, and a pinned containment test.

### H+ grading block (inserted after SK:1391, at most 12 lines)

- **High (blocking):** the task omits, contradicts or fabricates a roadmap item, deliverable, ID, dependency, exit criterion or validation step.
- **Medium (blocking):** the item is present, but a criterion, checkpoint or validation step is dropped from the acceptance list, narrower or softer than the roadmap's, so a roadmap-stated check can pass where the roadmap's would fail or is no longer run (the v3.66 M3/M4 pattern).
- **Low (note; listed in the Low section of `ValidationReport.md`; not patched, not re-validated):** insufficient detail, ambiguity, effort-estimate divergence, a different but equivalent verification method, formatting, terminology, wording, where every roadmap-stated check is still present and can still fail.
- **Rules:** grade by consequence, not by label (PM:225, :231); when torn between two grades, grade higher; same-task duplicates at the dedup step (SK:1410) keep the highest severity; this skill defines its own severity model (PM:228), in which High and Medium are blocking and Low is a note.

### Concrete terms

| Question | H+ answer |
|---|---|
| Skill sites that change | One insertion after SK:1391 (the block); one clause at SK:1410 ("keep the highest severity"). No existing sentence is edited. SK:1421-1422 stay MEDIUM and blocking. Risk labels (SK:565, :581, :964, :1699) and complexity `MEDIUM` (SK:735) untouched. |
| Medium-only residuals | Unchanged from today: patched at Stage 9, counted in `F_k` (SK:1608), re-verified at Stage 10, HALT at the P2 cap (SK:1614; `blocked` under `--unattended`, SK:1615). Only the Low class (ambiguity, detail, estimate, method, formatting) is a note, which is the one loosening H+ makes and the one the sweep header already calls minor (FX:5-6). |
| 12 pinned rows (S-119..S-130) | Untouched; `test_j` holds, count stays 139. |
| CMD:113 and the two worker-contract pins (`:777`, `:1861`) | Untouched ("the unresolved High or Medium HALT resolves as blocked" stays true). |
| CLI prompt | Unchanged. PR:62 stays CLI MEDIUM. `build_tasklist_fidelity_prompt` has one caller (`executor.py:173`), so any later edit is a separate owner decision. |
| Core | Gets nothing: no `Medium` token, no new field, no code. The module declares its map as data (High to CRITICAL/`blocking: true`; Medium to MAJOR/`blocking: true`; Low to MINOR/`blocking: false`), Form 1 only. The fidelity prompt, `DEV-NNN` ids and the layering guard stay outside the core; the only named seam is a read-only adapter from a finished deviation report. |
| New tests (static, no model call) | T1: SK contains the three definitions, the tie-break, the dedup clause and the S4 sentence. T2: containment test (skill High examples are CLI HIGH examples; CLI LOW examples are inside skill Low; no skill-Low example is under CLI HIGH; the skill block names the PR:62 class as the declared divergence). T3: no `Medium` token enters `findings.py`, `findings_v2.py`, `ledger.py`, the ledger JSON, plus one test pinning the label map as data (my M-X15-4). T4: existing pins run unchanged. |

### Measurements

**Preconditions for H+: none.** H+ edits no pinned sentence and loosens only the wording class. **Preconditions for the A+ upgrade: F2 and F3 below, plus the owner's acceptance of the PR:62 edit.** F1 is a follow-up for both.

Thresholds are registered here, before any grader runs. They are design choices, not evidence-derived.

- **F1 (M-X15-1, retrospective).** Three blind graders per finding, majority rule, on the 6 archived Medium findings: (i) S1 wording only (blocking or minor), (ii) the H+ block. Outcome: at least 4 of 6 blocking under (i) and the same 4 blocking under (ii) = H+ confirmed. At most 2 of 6 blocking under (i) = "the label is mostly wording"; this is my own Round 1 stop condition, so the skill's Medium is redefined and A+'s non-blocking Medium is adopted. 3 of 6 or disagreement between (i) and (ii) = mixed; H+ stays and the block text is revised once, then F1 re-runs.
- **F2 (A's M1, run under both blocks).** At least 10 seeded blocking-class defects (omission, contradiction, dropped or weakened criterion) and 10 seeded non-blocking-class defects (ambiguity, estimate, method, formatting); three blind graders; each defect graded under the H+ block and under the A+ block. FC = blocking-class defects with a non-blocking majority grade; FB = non-blocking-class defects with a blocking majority grade. A+ replaces H+ only if FC(A+) <= 1 and FC(A+) <= FC(H+) and FB(H+) - FB(A+) >= 3 (collision cost shown). If FC(H+) >= 2, the H+ block is rewritten and F2 re-runs once.
- **F3 (A's M-X15-5, both boundaries).** Run Stage 7 twice with fresh agents on the same bundle; count findings whose grade crosses the blocking/non-blocking line (A+: High|Medium; H+: Medium|Low). More than 1 in 5 blocking-class findings flipping fails that variant; both failing means neither block is adopted until revised. Record also the High|Medium flips under H+ (verdict-neutral by design).
- **Default:** a measurement not run, or any threshold not met, leaves H+ in place. A+ is never adopted by argument.

H+ resolves or narrows: C-001, C-002, C-004, C-007, C-011, C-012, C-013, X-004, X-009. It leaves open: C-005, C-006, C-014 (naming) and the PR:62 owner decision.

## Updated per-point positions

Key: A = Variant A, B = Variant B, H+ = the hybrid above, A+ = A's Round 2 hybrid. "Moved" marks a change from my Round 1 position.

| Point | Position | One-line reason |
|---|---|---|
| S-001 | A | An inputs table up front lets a reader check dependencies first. |
| S-002 | A | One fact per row with its own tag is checkable; my E1 bundled six cites. |
| S-003 | Neither | Heading depth does not affect the argument. |
| S-004 | B | The fidelity prompt stays outside the core; A moved here in Round 2 and no consumer or role table exists. |
| S-005 | H+ | A's static tests plus my pre-registered thresholds, now with a rule that maps each outcome to an action. |
| S-006 | Neither | Scope statements are cosmetic. |
| S-007 | B | A stop condition that measurement can trigger is more useful; H+ keeps it (F1) and A+ adopted the same device. |
| C-001 | H+ (moved) | Blocking set is A's consequence boundary; the word Medium stays on the second blocking sub-class until evidence says otherwise. |
| C-002 | H+ (moved) | PM:225 and PM:231 consequence test decides; S4 applies only after the block exists (X-002 conceded). |
| C-003 | B | Form 1 only, module data, no core code; A withdrew Form 2. |
| C-004 | H+ (moved) | Grading block from A; SK:1421-1422 stay blocking under either word. |
| C-005 | B | H+ edits one insertion and one clause; A+ edits roughly thirty sites by A's list. |
| C-006 | B | H+ holds 12 rows, CMD:113 and two pins; A+ rewrites all of them. |
| C-007 | H+ (moved) | Loop counts High and Medium as today; dedup-highest and tie-break-up taken from A; F3 measures both boundaries. |
| C-008 | Hybrid (B's placement, A's test) | Prompt stays in `cli/tasklist/`; containment test T2 with a named exception; role table and adapter deferred. |
| C-009 | B | The shared frontmatter contract is a reason to leave the gate alone; PR:62 text itself has one caller only. |
| C-010 | Hybrid | I have the data; A's re-read corrected my reading; mine now agrees (2 omissions, 2 dropped acceptance criteria, 1 contradiction, 1 assumption-as-fact). |
| C-011 | H+ (moved) | A's static T-tests, my pre-registered thresholds, F1-F3 with default-to-H+. |
| C-012 | Hybrid | The blocking line has identical content in A+ and H+; H+ adds a buffer tier for High-typed-Medium, A+ adds nothing equivalent. |
| C-013 | Hybrid (moved) | High and Low text from PR:51-69; Medium = the PR:62 class only (blocking in the skill, a declared divergence from the CLI); ambiguity goes to Low. |
| C-014 | Neither | Outcome matches rf-qa and qa.md (blocking by consequence) but the word collides with PM:230; priced as FB in F2. |
| X-001 | Neither | Both overread S4 and S5; PM:225/PM:231 consequence test decides. |
| X-002 | A | Conceded: the skill states no model before the block. |
| X-003 | B | FX:29 records "open High/Medium findings HALT"; the dispute is only the framing. |
| X-004 | Hybrid | A on the regrade, me on what reviewers did; M3/M4 read High or not depending on A+'s "dropped" clause, so only F1/F2 settle it. |
| X-005 | B | No module-declared role table exists today (`ROLES` closed, [DIFF]). |
| X-006 | B | PM:229 and :231 name no High/Medium/Low scale. |
| X-007 | Neither | "Gap" and "no fixer" are both inferences. |
| X-008 | B | One product family, not one code path. |
| X-009 | B | One grader per task slice (SK:1351-1368): no union. |
| X-010 | A | My ranges were wrong (`PR:49-69`, `:195-240`, `:208-225`); A's `.py`-only count caveat stands. |

**A-004 to A-009.** A-004 QUALIFY, A-005 QUALIFY, A-006 QUALIFY, A-007 ACCEPT: unchanged. **A-008: REJECT** (unchanged from Round 1; SK:1608 re-runs the full set with fresh agents and SK:1410 had no severity tie-break). **A-009: QUALIFY** (static counts hold, no test run by me; CMD:113 and the `_unattended_section` read path added to the pin inventory, which I now confirm at `test_worker_contract.py:777` and `:1861` by grep).

## Remaining disagreements

1. **Label word versus churn.** A weighs naming consistency (PM:230, qa.md:81 and :274, `card_convert.py`, the CLI) above zero churn and no loosening; I weigh the reverse, because the skill already tags Medium "(blocking)" inline and the outcome is the same set. A judgement, not a fact. F2's FB(H+) - FB(A+) >= 3 rule is the registered way to overrule me.
2. **The PR:62 edit.** A+ needs it for a true parity test; H+ declines it because it changes the exit-1 rate of `tasklist validate` and no measurement of the CLI prompt is on either list. A accepts it "only with the measurement gate"; I add that the gate must include a CLI-prompt run. Owner decision.
3. **The buffer tier versus tie-break-up.** I say a second blocking word tolerates the observed misgrade (High typed Medium, 2 of 6 real reviewers); A says the block plus tie-break-up fixes the cause. Neither is measured; F2 measures FC for both.
4. **Declared divergence on one class.** A calls H+'s exception hollow; I call it weaker but non-vacuous (T2 a-d). It is a real cost either way, and removing it requires the PR:62 edit.
5. **Whether H+'s Low for ambiguity is acceptable.** Outcome is identical to the CLI (non-blocking); only the label text differs. A may still hold that the CLI's MEDIUM text should be reused. I keep Low because the sweep header calls wording minor (FX:5-6) and PM:225 defines minor to include wording.
6. **No longer disputed:** Form 2, the union mitigation, S4 as my basis, S5 as literal text for High/Medium/Low, the "one product" wording, my line ranges, "B's boundary is easier to define", E6's "mostly omission", and the default (nothing loosens before F2 and F3 run).

## New evidence

All [READ] this session unless marked.
1. **The CLI prompt has one caller, and the PR:62 phrase occurs once.** `build_tasklist_fidelity_prompt` is called only at `cli/tasklist/executor.py:173`; `TASKLIST_FIDELITY_GATE` is used only at `executor.py:180` (grep over `src/`, plus the SK:153 documentation mention). "Acceptance criteria are weaker than the roadmap's success criteria" occurs only at `prompts.py:62`. SPEC_FIDELITY_GATE shares the frontmatter checks, not this text, so a PR:62 edit changes only `tasklist validate` classification and its HIGH-only exit (`commands.py:181-183`). This corrects the framing that the edit touches a classifier shared with SPEC_FIDELITY_GATE.
2. **The sweep header's own rule supports H+.** FX:4-6 defines blocking as "wrong, unsafe, incomplete against stated requirements, or unverifiable" and minor as "cosmetic, wording, style, optional polish". "Incomplete against stated requirements" is H+'s Medium class; "wording" is H+'s Low class. The header names CRITICAL/IMPORTANT/MINOR/LOW and no middle word, and the tasklist group line (FX:29) says "open High/Medium findings HALT at the cap".
3. **The skill already disambiguates its Medium inline.** SK:1439 ("High or Medium (blocking)"), :1567, :1610, :1614 carry the "(blocking)" tag; :1537 reads "blocking (High and Medium)"; :1608 reads "High and Medium, i.e. blocking". The collision with PM:230 is explicit in every gate sentence, which lowers (does not remove) its confusion cost.
4. **Archived Medium findings, re-read:** 2 omissions (v3.66 M2, test1 M1), 2 dropped acceptance criteria with Steps/Deliverables still present (v3.66 M3, M4), 1 step contradicting a roadmap target (test1 M2), 1 expected value asserted as fact (v3.66 M1). Under A+'s High clause ("dropped or weakened so a roadmap-stated check can no longer fail") M3 and M4 read High if "dropped" is independent of "can no longer fail", and Medium otherwise; A+'s own text does not say which. On this sample the A+ Medium class has at most about two members (M1 and perhaps M3/M4), so the dispute is about at most a third of six findings. [INFER; one reader.]
5. **A+'s tie-break-up and H+'s buffer are different mechanisms for one failure.** The failure is observed (two real omissions typed Medium by actual reviewers under a definition-less skill, v3.66 M2 and test1 M1). The buffer needs no reviewer cooperation; tie-break-up needs it. [INFER]
6. **The blocking line has identical content in A+ and H+** (derived above from A's Round 2 block text); it is an inference from reading both blocks, not a measured fact.
7. **Not re-read, still [DIFF]:** `findings.py`, `findings_v2.py` line facts, `card_convert.py:71-83`, `roadmap/gates.py:195-240` and `:1322-1345`, `test_review_severity_rule.py:268-283`, the C-01/C-02/C-03 adjudication files, the plan copy `.dev/review-severity-rule/sweep-edits.yaml`. The B3-10 source the fixture cites is absent from this checkout (unchanged). I ran no tests.

Status: Complete.
