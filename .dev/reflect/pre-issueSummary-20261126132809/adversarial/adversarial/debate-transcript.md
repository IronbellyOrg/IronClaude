# Adversarial Debate Transcript

## Metadata
- Depth: standard
- Rounds completed: 2 (Round 1 parallel, Round 2 sequential) plus Round 2.5 invariant probe (see invariant-probe.md); Round 3 not run (depth standard)
- Convergence achieved: 94% (29 of 31 diff points). The two advocates agreed on all 31 after Round 2; two points (C-007b merged into the open Safety item, C-009 raised from Note to Medium) were decided by the orchestrator against both advocates. The invariant gate blocked convergence (10 HIGH UNADDRESSED probe items); the orchestrator dispositioned each in the merged card, four stay listed as unaddressed in the return contract.
- Convergence threshold: 80%
- Focus areas: correctness, coverage, deviation-classification
- Advocate count: 2 (Variant 1 advocate and Variant 2 advocate, both sonnet general-purpose agents that Read the real plan and spec)
- Orchestrator note: the advocates' statements are reproduced in substance (tables kept, repetition trimmed). No advocate edited any file.

## Round 1: Advocate Statements

### Variant 1 Advocate (reviewer-1-card, haiku-class analyzer)

**Position**: V1's three findings are real but narrow. C-001 and C-002 hold as blocking (C-001 better graded Decision); C-003 is overstated and should be Medium. V2 wins on breadth, evidence and decision-level grading; V2's C-005 and C-004 should be graded lower; C-007 stands only as an open item.

**Steelman of Variant 2**: V2 audited the whole plan against the spec and the two linked analysis files; found checks that cannot fail (PLAN:131 never names the answer supplied, PLAN:148 expects question counts only, PLAN:171 points at the wrong file); its spot-checked citations are accurate (`--type cli`/`--type skill` valid at commands/issue.md:42, `--base` at pr-submit.md:51, CI path trigger at contract3 yml:26-29, the 17-test count, the two-file package folder); it graded by consequence; it raised the only safety question, labelled open.

**Per-point table (V1 advocate)**

| Point | Verdict | Proposed grade, category | Note |
|---|---|---|---|
| C-001 | REAL | Blocking (Decision), Drift | PLAN:47,49,61,81,122-123,139-141,154,175; SPEC:23,35,43 |
| C-002 | REAL | Blocking (Missing), Drift | SPEC:35; PLAN:90,98,102 |
| C-003 | OVERSTATED | Medium, Drift | SPEC:11 matches accuracy-check.md:7 ("claim writes"); PLAN:22,24 |
| C-004 | REAL, overstated as Blocking | Medium, Drift | PLAN:171 false "quoted"; SPEC:43 lists scenarios |
| C-005 | REAL | Medium, Drift | post counts already recorded PLAN:108,128,169; create.md:86 mandates AskUserQuestion |
| C-006 | REAL | Blocking (Decision), Drift | "keep the draft" leaves body unchanged, check cannot fail; accuracy-check.md:17 |
| C-007 | UNVERIFIED | Blocking (Safety), open; (a) stronger than (b) | see detail |
| C-008 | REAL | Medium, Drift | |
| C-009 | OVERSTATED | Note, Drift | create.md:38,86; draft-notes.md:13; PLAN:125,148 |
| C-010 | REAL | Medium, Drift | |
| C-011 | REAL | Medium, Drift | fake gh refuses unknown calls PLAN:106 |
| C-012 | REAL | Medium, Drift | |
| C-013..C-016 | REAL, form | Note, Drift | C-013 "Task 7" incomplete not false |
| C-017 | REAL | Note, Authorized expansion | |
| C-018 | REAL | Note, Necessary deviation | |
| S-001 | n/a | Dropped | |
| S-002..S-005 | REAL | Note | S-003: "Regression" wrong for a pre-execution audit |
| X-001..X-004 | V2 right on X-001, X-002; X-003 V1 label wrong; X-004 breadth | | |

**C-007 detail**: PLAN:22 sets the boundary; PLAN:91 blocks only `gh` (empty GH_CONFIG_DIR, tokens unset, fake gh first on PATH), gives the run clone the real fork URL and asserts "no push is ever made"; PLAN:132 verifies only `gh`; PLAN:159 names an "uninterceptable write" with no detector; PLAN:88 asks Task 4 to read permission mode and deny lists but nothing requires using them; PLAN:89 lists a temporary home as one option only. Logs: CLAUDE.md:37 stages each package's `artifacts/`; .gitignore:85 re-includes `.dev/tasks/**/*.log`; PLAN:108 writes raw event logs; no scan before staging. Neither reviewer read user git/MCP config; stands as an open item, does not fall.

**Strengths claimed**: (1) C-001: Phase 1 count assertions (PLAN:47,61) fail only if the test's own function is mis-coded; SPEC:43 names seven scenarios, PLAN:122-123,139-141,154 run three. (2) C-002 is a spec-named step that is absent. (3) C-003 has a kernel: PLAN:195,176 assert current state without a fresh read. (4) PLAN:81's admission is not coverage. (5) V1 saw the broken SPEC:32-33 links. (6) No false citation in V1.

**Weaknesses found in V2**: C-009 contradicts create.md:38,86; C-004 over-graded; C-005 rests on a hypothetical; 16 Drift rows blur omission vs wrong statement; C-013/014 form-only; V2's own limits (V2:68); tag-neutralization header (V2:7).

**Concessions**: C-003 Medium not Blocking; V1 row 2 says Blocking with MEDIUM severity; "Regression" wrong; vague "affected action"; V1 raised 3 of 18 points and missed C-005, C-006, C-010, C-007.

**Shared assumptions**: A-001 REJECT (SPEC:11 is the claim orchestrator; PLAN:22 bans all writes, PLAN:24 leaves reopening to the lead); A-002 QUALIFY; A-003 ACCEPT; A-004 QUALIFY.

**Hallucinations**: none in V1 line citations (V1#3 puts "already closed" at plan 24; the wording is at plan 195); V2#9 wrong reading; V2#13 incomplete; V2#14 installed-copy claim partly confirmed.

### Variant 2 Advocate (reviewer-2-card, opus-class qa)

**Position**: V2 is the better card, but only three of its six Blocking labels hold: C-001 (Decision), C-002 (Missing) and the non-`gh` half of C-007 (Safety, open). C-004, C-005, C-006 and C-007b are real but Medium; C-009 and C-013 are Notes.

**Steelman of Variant 1**: precision-first; all three findings real and independently reached by V2 (rows 4, 5, 8); anchors correct; anchors only to SPEC and PLAN, avoiding reliance on the linked analysis files (A-004); PLAN:81's admission is honest but not coverage.

**Per-point table (V2 advocate)**

| Point | Verdict | Grade, category |
|---|---|---|
| S-001 | presentation | Dropped |
| S-002, S-003, S-004 | REAL (V1 card defects) | Note |
| S-005 | useful | Dropped |
| C-001 | REAL | Blocking (Decision), Drift |
| C-002 | REAL, contingent | Blocking (Missing), Drift |
| C-003 | V1 overstated | Medium, Drift |
| C-004 | REAL, overstated | Medium, Drift |
| C-005 | REAL, overstated | Medium, Drift |
| C-006 | REAL, overstated | Medium (borderline), Drift |
| C-007a | UNVERIFIED, text-confirmed | Blocking (Safety), open, Drift |
| C-007b | REAL as hardening, overstated | Medium, Drift |
| C-008, C-010, C-011, C-012 | REAL | Medium, Drift |
| C-009 | OVERSTATED | Note, Drift |
| C-013..C-016 | REAL, trivial | Note, Drift |
| C-017 | not a defect | Dropped, Authorized expansion |
| C-018 | not a defect | Dropped, Necessary deviation |
| X-001 | V2 right | Drift |
| X-002 | V2 right | Medium |
| X-003 | V2 label right, "HIGH" overstated | Blocking (Missing), low margin |
| X-004 | V2 closer | n/a |

**C-007 ruling**: plan text confirmed at PLAN:22, 91, 132, 159; no non-gh write check and no log scan anywhere (Grep for scan, redact, credential, MCP, push, insteadOf finds only PLAN:22, 89, 91, 113). (a) Stands as an open item, Blocking (Safety): the declared boundary is wider than the mechanism; the run model has Bash; a credential helper, `insteadOf` rewrite, GitHub-capable MCP server or other env token could write; unverifiable without reading config. (b) Falls to Medium: no evidence a secret would land in a log; inputs are synthetic (PLAN:22); .gitignore:85 re-includes only `*.log` and the plan never names the extension, so that citation is marginal.

**Strengths claimed**: (1) C-001 is exactly what SPEC:35 forbids; PLAN:175 bans only "a static wording test alone". (2) C-007a is a gap in the plan's own declared scope. (3) C-004 verified false statement (PLAN:171; SPEC:9-11; accuracy-check.md:16-21; SPEC:32-33 links unresolved). (4) C-010/011/012 ordering and method defects V1 missed; Task 11 copies Task 9's table (PLAN:195) so its "every criterion delivered" branch cannot be reached. (5) C-016 verified at create.md:38 and 86. (6) C-005/C-006 observability gaps.

**Weaknesses found in V1**: wrong category and "Missing" on C-001; Blocking prose vs MEDIUM column (V1:20-21); C-003 over-graded on a doubtful assumption; saw the link problem (V1:36) but graded nothing; missed safety; ran nothing.

**Concessions**: four of V2's six Blocking labels are too high; C-009 mostly wrong; C-013 incomplete not false; V2's "add runs for empty/mixed/multiple" may be infeasible for a description-only run (alternative: contract-test labelling or notes-injection runs); V2 rows 2 and 5 lean on non-binding analysis files though SPEC:11 and SPEC:43 independently say "actual question/post counts"; V2 did not verify live git/MCP safety. One miss in both cards: PLAN:108 writes the run directory's `.dev/issues` tree into `./artifacts/runs/` (always-staged `.dev/tasks/`) while PLAN:25 and PLAN:189 forbid staging under `.dev/issues/` (Note-level ambiguity, not verified mechanically).

**Shared assumptions**: A-001 QUALIFY (claim orchestrator, but PLAN:24,176,195 restate closure as current fact, so a read is worthwhile; Medium); A-002 QUALIFY (contract-test Phase 1 is a legitimate reading only if Task 9 does not count it as behaviour evidence for scenarios the runs skip); A-003 ACCEPT; A-004 QUALIFY (binding for the six criteria's wording since SPEC:33 points to accuracy-check.md; advisory for approach).

**Hallucinations**: none wrong in line numbers in either card; V2 overstatements: row 9, row 13, row 6 .gitignore:85 marginal; unchecked by the advocate: coverage-matrix.json figures, installed create.md:82.

### Round 1 contested points (orchestrator extraction)
Disagreements after Round 1: C-006 grade (V1 adv Blocking (Decision) vs V2 adv Medium); C-007b (V1 adv keeps inside the open Safety item vs V2 adv Medium); C-017/C-018 (Note vs Dropped); A-001 (REJECT vs QUALIFY); X-003 label. All other points agree on grade.

## Round 2: Rebuttals

Sequential: Variant 1 advocate first (saw both Round 1 statements), then Variant 2 advocate (saw both Round 1 statements and the Variant 1 Round 2 position).

### Variant 1 Rebuttal
- **C-006**: conceded to Medium (borderline). PLAN:131 and 143 record an honest "applied yes/no" that can come out "no"; it is vacuous only for the "keep the draft" choice; the exit is "not evidenced" then "partly evidenced" (PLAN:171); PLAN:174 requires counts recomputable from raw files; naming "keep my wording" plus a body comparison would not flip the AC2 verdict.
- **C-007a**: Blocking (Safety), open, upheld. PLAN:22 declares "no GitHub writes of any kind"; PLAN:91 and 132 enforce and verify only `gh`; PLAN:91 gives the run clone the real fork URL and asserts "no push is ever made"; PLAN:159 names an "uninterceptable write" with nothing to detect one; no one read user git or MCP configuration. Narrow fix: disabled push URL on the run clone, deny `git push` in Task 4's allow and deny lists (PLAN:88).
- **C-007b**: Medium. A secret reaching a log needs the model to read credentials, which PLAN:22 and create.md:59 forbid; the plan never names the log extension so .gitignore:85 is marginal; CLAUDE.md:37 stages `artifacts/` either way; a scan is hardening.
- **PLAN:108 vs PLAN:25 and PLAN:189**: Note. The copy lands under `.dev/tasks/<pkg>/artifacts/`, which CLAUDE.md:37 requires staged; PLAN:25 and 189 forbid staging `.dev/issues/` itself (a path match).
- **C-001**: Blocking (Decision) stands; "Missing" ground withdrawn. PLAN:81 admits Phase 1 does not prove model behaviour; PLAN:175 forbids only "a static wording test alone" and PLAN:171 lets "the new tests and run records" back a verdict, so Phase 1 can back AC2 and AC5 for the scenarios the runs skip (PLAN:122-123, 139-141, 154). Correction (relabel Phase 1 as contract tests, cap AC2/AC5 at "partly evidenced") changes the PLAN:171 and 175 checks: a Decision.
- **C-002**: Blocking (Missing) stands, narrowed. The no-answer branch is handled (PLAN:90, 98, 171), so that half is Medium. A failing interception self-test (PLAN:111) has no stop, no revisit-the-estimate and no ask-the-lead step (SPEC:35; SPEC:43 "no live test issues without asking the lead").
- **C-017, C-018**: list under Dropped (classifications, not defects); keep the categories in the audit trail. (Reverses its Round 1 Note rows.)
- **A-001**: QUALIFY (moved from REJECT). The plan executor is not the SPEC:11 "orchestrator", but PLAN:176 and 195 restate "already closed" as current fact with no fresh read; a read-only `gh issue view` is worth adding. Medium.
- Final grades: C-001 Blocking (Decision); C-002 Blocking (Missing); C-003 Medium; C-004 Medium; C-005 Medium; C-006 Medium; C-007a Blocking (Safety, open); C-007b Medium; C-008 Medium; C-009 Note; C-010 Medium; C-011 Medium; C-012 Medium.

### Variant 2 Rebuttal
- Agrees with every grade of the Variant 1 rebuttal, with one narrowing and one correction.
- **C-001**: agree, "Missing" withdrawn. Fix: relabel Phase 1 as contract tests and cap AC2 and AC5 at "partly evidenced" in PLAN:171 and 175; second acceptable fix: runs that inject prepared notes, because a description-only run cannot force empty notes or three contradictions.
- **C-002**: agrees with the narrowing, corrects the reason. The self-test at PLAN:111 covers fake `gh` interception only; it makes no model call (PLAN:108) so it cannot show that an `AskUserQuestion` event appears in the log; that is learned only in Task 4 (PLAN:90) or in the first real run. A failing self-test fails Task 5's acceptance (PLAN:110-113) and Tasks 6-8 depend on Task 5 (PLAN:119, 136, 152), so the `gh` half stops by dependency though not by an explicit stop-and-report. The question-observation half has no stop: Task 4 may write "not available here" (PLAN:98) and Phase 3 proceeds degraded (PLAN:171). The step missing in both branches is SPEC:35's "the estimate must be revisited" plus telling the lead; low margin, but absent in substance. Narrow fix: a Task 4 checkpoint that stops, revises the estimate and reports to the lead before Task 5 when question observation or interception is unavailable.
- **PLAN:108 vs PLAN:25/189**: Note is right. `.gitignore` has no `.dev/issues` rule and `.gitignore:83-85` protects `.dev/tasks/`, so `git add .dev/tasks` stages the nested copy. Residual risk: a hook matching `.dev/issues/` as a substring (not verified to exist). One-word fix: name the copied folder `issues-tree/`.
- **C-004**: do not make the fix a pointer to `.dev/issues/834/accuracy-check.md:16-21` as a cited source (PLAN:25 bans staging it, so a PR would cite a file it does not carry). Inline the six criteria text in PLAN:171 including AC4's "no full-body approval"; add SKILL.md:76,102-103, refs/claim.md:83,89-95 and templates/launch-prompt.md:23-28 to the AC4 citation list; the accuracy-check path may appear only as a local, not-staged read reference.
- Final grades: C-001 Blocking (Decision); C-002 Blocking (Missing), narrowed, low margin; C-007a Blocking (Safety, open); C-003, C-004, C-005, C-006, C-007b, C-008, C-010, C-011, C-012 Medium; C-009 Note.

### Round 2 convergence note (orchestrator)
After Round 1, 25 of 31 points agreed on grade (contested: C-006, C-007b, C-017, C-018, A-001, X-003). After Round 2 the two advocates agree on every point. Because the Variant 2 advocate saw the Variant 1 concessions, the agreement is checked independently by the Round 2.5 fault-finder, which does not see either advocate's stake.
