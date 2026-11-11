# Adversarial Debate Transcript

## Metadata
- Depth: standard
- Rounds completed: 2 (plus Round 2.5 invariant probe, see invariant-probe.md)
- Convergence achieved: 97% (30 of 31 points; severity agreement 28 of 28 scored points, unanimous after Round 2)
- Convergence threshold: 80%
- Focus areas: correctness, coverage, deviation-classification
- Advocate count: 3 (general-purpose agents, default model; Variant 1 analyzer, Variant 2 qa, Variant 3 refactorer)
- Agent failures: none

## Round 1: Advocate Statements

### Variant 1 Advocate

#### Round 1 statement: Variant 1 (reviewer-1, analyzer)

#### Position summary

V1 is the only card that checks the plan as an executable sequence: it finds two places where a task's own acceptance test cannot pass without code a later task builds (C-002) or inputs no task provides (C-003). It also maps the plan's two declared deviations to the right taxonomy classes. Its severity grading is uneven: F2 (C-001) is overstated and I withdraw it to minor. Its reason for dismissing the measurement copy (C-008) was wrong even though its severity was right.

#### Steelman

**V2 (qa/haiku).** Strongest argument: plan:19 puts source.md section 4 in scope, and source.md:163 describes a concrete artifact, the measurement copy built from the 472-line Arm B base. No task builds or verifies it, and Task 13 only writes it into INSTALL.md as prose (plan:172). V2 is also the only card to find that a withdrawn *carried* claim loses its `prior` link. Task 3 keeps only `id` and `claimed` in the `form` line (plan:57), and Task 6 counts form-only claims as new findings (plan:87). That overcounts M0 against source.md:173 ("carried priors excluded"). Both observations are correct, and QA-002 is a real unique find.
**Critique.** Neither finding meets the blocking test. The measurement copy is an install-time action of the experiment; the plan installs nothing (plan:20, "nothing is installed by this plan"), and source.md:163 sits in the install procedure, not in section 3 "Exact changes". QA-002 affects only a reporting count (plan:22, "This is reporting only") and only in the narrow case where a carried MAJOR is withdrawn between seals. V2 classes both as drift but leaves the plan's two declared deviations unclassified (deviation_counts all zero for authorized and necessary, V2 line 5). Its own calibrator flagged that omission (V2 line 41). It audited 35 units and reported 2. It missed the ordering defects, the replay inputs, the Usage-line contradiction and the staging gap.

**V3 (refactorer/opus).** Strongest argument: R3-1 shows that the Usage-line contradiction is not just cosmetic. Task 10's equality test treats the Usage line as a name-change-only block (plan:135). Any fix that drops `[--unattended] [--report-dir <dir>] [--improve]` from spec-panel.md:23 would therefore fail the plan's own test, so the plan locks the defect in. V3 also adds the widest set of test-hygiene findings that V1 missed and that I verified:
- `_tracked_text()` uses `git ls-files`, so unstaged new files are not scanned (tests/skills/test_review_severity_rule.py:35-38) (C-015).
- Task 12 omits tests/agents, which scans agent files (C-016).
- The comment above `_POST_REFRESH_ADDITIONS` goes stale (tests/recommend/test_routing_refresh.py:29-33) (C-020).
- The plan's own scope carve-out does not cover the two section-5 templates (C-018).

That last one gives V3 a defensible third deviation (drift) that V1 did not count.
**Critique.** V3 calls R3-1 and R3-2 blocking, and neither meets the stated test:
- **R3-1 (Usage line).** The S1 briefs never pass `--unattended` (plan:21), so no deliverable behaves wrongly. The defect is a doc line that contradicts the variant's own no-unattended sentence.
- **R3-2 (counted-once case).** Task 3 imports "the begin and seal cases of section 3.4" (plan:57), so an exact follower would write the case. The real gap is that the counting rule is undefined, and that is a spec inheritance (source.md:128 names it without a rule).

V3 missed C-002 and C-003, the two findings that concern whether the plan can execute. R3-11 is not a defect: source.md:124 lists the exact frontmatter keys without `category:`.

#### Strengths claimed

1. **The only card to test task-by-task executability (C-002).** Task 3's acceptance (plan:60) requires "`begin` exits 5 ... on prior-verdict mismatch". Recomputing a prior verdict needs final statuses and `compute_verdict`, and those arrive in Tasks 4 and 5 (plan:68, plan:77; source.md:62, :71). /sc:implement runs per-task compliance QA against each task's own criteria, so Task 3 cannot pass as written. The implementer would have to pull Task 5's function forward, which Task 5's QA then has to reconcile.
2. **The replay fixture lacks its required input (C-003).** At review 3, `begin` needs a prior report carrying a valid sentinel, a `spec=` hash equal to the baseline sha256, and a recomputable verdict (source.md:62). I grepped the control r1 round-2 report (`exp346-ab-ctl-r1/.dev/orca-command-refactor/review/spec-panel-round2.md`) for `sentinel|stoprule` and found nothing. The fixture's three files (plan:99) include no prior report. Two literal readings of plan:96 both fail. Without `--re-review`, `begin` sets N=1, and the ratchet applies only at reviews 2 and 3 (plan:57), so every claim is anchored and the split assertion is vacuous or wrong. With `--re-review`, `begin` exits 5. The plan also bans synthetic substitutes (plan:96), which discourages exactly the scaffolding needed. No other card saw this, and diff-analysis rates it the highest-severity item.
3. **Correct deviation mapping (S-002, X-004).** Two of the plan's deviations are declared:
   - Removing the Unattended section is **authorized**: an explicit owner ruling (plan:21) departs from source.md:103 "exactly these edits".
   - Editing `_POST_REFRESH_ADDITIONS` is a **necessary** deviation from source.md:129 "run, do not edit". I verified that `assert shipped - _POST_REFRESH_ADDITIONS == active` at test_routing_refresh.py:648 forces the edit.

   V1 ties each count to a named deviation. V3's counts are not tied to ids, and V2's are missing.
4. **Spec-inherited gaps the others skipped (C-010, C-011).**
   - source.md:34 lists `final` and `verdict` as script-appended lines, but no subcommand in Tasks 3 to 5 is named as their writer.
   - `parent=` appears only in escalation item (g) (source.md:73) and is absent from the sentinel format (source.md:70).
   - `apply-audit` defines `real:true` only as "reinstates the claim" (plan:68). A seeded *unclaimed* hunk has no claim to reinstate, so that outcome is undefined.
5. **Usage-line defect found with the correct fix path (C-004).** F4 already said that Task 10's replaced-block list must include the Usage line (V1 line 31). That is the same lock-in V3 argues, without overstating the severity.
6. **Staging and ordering gaps shared with V3 (C-006, C-007).** Both cite plan:161, 172 and 182.

#### Weaknesses identified in others

1. **V2 grades severity without the blocking test.** QA-001's "artifact missing" ignores plan:20 ("nothing is installed by this plan"). QA-002 is a reporting-only overcount (plan:22). V2's own calibrator scored them 0.20 and 0.45 (V2 lines 38-39).
2. **V2's deviation count is wrong on its face.** It reports authorized 0 and necessary 0 while plan:21 and plan:135 declare one of each.
3. **V2's coverage is thin.** It audited 35 units and found 2 findings, while V1 and V3 each found 12. It missed the Usage contradiction (spec-panel.md:23 vs the removed section at :451) that both other cards verified.
4. **V3 inflates two doc and test-list gaps to blocking.** These are R3-1 (C-004) and R3-2 (C-005), for the reasons in its steelman. Its calibrator agrees: "Both blocking labels overstated" (V3 line 54).
5. **V3's deviation counts are not traceable** (V3 line 53, calibrator note), so drift 1 cannot be audited against a finding.
6. **V3's R3-11 is not a defect.** It contradicts source.md:124, which lists the exact frontmatter keys, and the plan follows that list (plan:44).
7. **V3 and V2 both missed the executability defects C-002 and C-003.**

#### Concessions

- **F2 / C-001 is minor, not blocking.** The phrase "built by the same function as Task 6's `count`" (plan:77) does not stop Task 5 from defining that function and Task 6 from wrapping it.
- **F1 / C-002 depends on A-001.** If per-task QA lets an implementer build `compute_verdict` early, it becomes a rework issue rather than a missing deliverable. I keep it blocking because Task 3's own acceptance criterion cannot pass from Task 3's text.
- **F3 / C-003 is fixable with tmp_path scaffolding.** My calibrator scored it 0.55. It stays blocking only because the plan as written gives an implementer no instruction to build that scaffolding.
- **F12 / C-008 had wrong reasoning.** I wrote "section 3 omits it", but plan:19 includes section 4. My conclusion (minor) stands for a different reason: it is an install-time action, and the plan installs nothing.
- **V3's test-hygiene findings are real, and V1 missed them:** C-014, C-015, C-016, C-020.
- **V2's QA-002 (C-009) is a real gap V1 missed.**
- **V3's drift count is probably more correct than mine.** If C-018 is accepted as drift, the plan has three deviations, and V1 counted only two.

#### Per-point positions

| id | finding real? | correct severity | superior variant |
|---|---|---|---|
| S-001 | yes | not-a-defect | tie (V1/V3) |
| S-002 | yes | minor | tie (V1 maps ids; V3 counts the C-018 drift) |
| S-003 | yes | not-a-defect | V3 |
| C-001 | partly | minor | V1 |
| C-002 | yes | blocking | V1 |
| C-003 | yes | blocking | V1 |
| C-004 | yes | minor | tie (V1 severity, V3 lock-in argument) |
| C-005 | yes | minor | V1 |
| C-006 | yes | minor | tie |
| C-007 | partly | minor | tie |
| C-008 | partly | minor | V1 |
| C-009 | yes | minor | V2 |
| C-010 | yes | minor | V1 |
| C-011 | yes | minor | V1 |
| C-012 | partly | minor | V1 |
| C-013 | partly | minor | tie |
| C-014 | yes | minor | V3 |
| C-015 | yes | minor | V3 |
| C-016 | yes | minor | V3 |
| C-017 | partly | minor | V3 |
| C-018 | partly | minor | V3 |
| C-019 | no | not-a-defect | V1 (correctly silent) |
| C-020 | yes | minor | V3 |
| C-021 | partly | minor | V3 |
| X-001 | yes | minor | V1 |
| X-002 | yes | minor | V1 |
| X-003 | partly | minor | V1 |
| X-004 | yes | minor | V1 |

#### Shared assumptions

- **A-001: QUALIFY.** Reading ahead is fair when later tasks only fix names in advance (C-001, C-007). It is not fair when a task's own acceptance criterion cannot pass without code a later task builds (C-002), because /sc:implement gates QA per task.
- **A-002: ACCEPT, narrowed.** The dated owner rulings at plan:21-24 outrank source.md text, and source.md section 7 defers to the owner. The plan's own scope additions without a ruling, such as the C-018 templates, do not inherit that authority.
- **A-003: QUALIFY.** I verified that the inputs exist today: the ctl-r1 review and spec history files, the S1 `task-text/` folder holding T05 to T10, and `/tmp/impl/exp/s1/`. Tasks 7 and 14 also stop as blocked on a missing file or a sha256 mismatch (plan:96, plan:182). Their absence at execution time would therefore block the run, not produce a wrong deliverable. `/tmp` remains the fragile input.

### Variant 2 Advocate

#### Round 1: Variant 2 (reviewer-2, qa persona)

#### Position summary

V2 is the narrowest card, but it holds the only finding about whether the plan's `count` subcommand computes the owner's pre-registered measure correctly (QA-002 / C-009), and none of the other cards raised it. I concede that V2's other finding (QA-001 / C-008) is overgraded and that V2 did not classify the plan's declared deviations. On severity, V1 is the best-calibrated card. V3 is the strongest on test hygiene and on why the Usage-line defect cannot be fixed at implementation time.

#### Steelman

**V1 (analyzer).** V1's strongest argument is that the plan cannot be run in order as written. Task 3's acceptance requires `begin` to exit 5 on a prior-verdict mismatch (plan:60), but `compute_verdict` only arrives in Task 5 (plan:77). Task 5's label-count line points at Task 6's `count` (plan:77, plan:87). Task 7's replay calls `begin`/`seal` on a review-3 fixture whose prior report has no sentinel. `begin` exits 5 on exactly that (plan:57, source.md:62), and the plan names no prior-report fixture (plan:96). I verified the control-r1 review folder. It holds only plain `spec-panel*.md` reports, so the replay test as described hits exit 5. V1 also grades my measurement-copy item correctly (F12: section 3 does not list it, and only the INSTALL.md sentence is unverified). It is the only card that classifies the declared deviations (A2 authorized, A3 necessary; plan:21, plan:135). **Critique:** F1 and F2 are forward references. An executor that holds the whole plan resolves them by reading ahead, so "blocking" overstates them (its own calibrator gave 0.60 and 0.50). V1 also missed the withdrawn-prior counting edge case.

**V3 (refactorer).** V3's strongest argument is that the Usage-line contradiction is locked in by the plan. Task 9 allows "exactly these changes" (plan:123). Task 10's equality test treats the Usage line as inherited except for name changes (plan:135). So the variant must ship `[--unattended] [--report-dir <dir>] [--improve]` (spec-panel.md:23) while also saying it does not accept `--unattended` (plan:21, plan:123). V3 is also uniquely right on test-ordering hygiene. `test_review_severity_rule.py` sweeps only `git ls-files` output (tests/skills/test_review_severity_rule.py:36-39, verified), and Tasks 10 and 12 run it before staging (plan:140, plan:161-165), so the new files pass unscanned. **Critique:** V3 overgrades R3-1 and R3-2 as blocking. The variant's behaviour still matches the owner ruling because the section is removed, and the missing counted-once test is one test case. R3-11 is not a plan defect, because source.md:124 lists the exact frontmatter keys without `category:`. R3-7 rests on an unlikely reading of "the literal recorded in" (plan:135). V3's deviation counts are not tied to finding ids.

#### Strengths claimed

1. **QA-002 is the only finding that touches the correctness of M0.** The owner decision keeps a critical or major finding that was dropped between the first and second `seal` in the count (plan:22). M0 excludes carried priors (source.md:173). Task 3's first-pass `form` line records only `id` and `claimed` (plan:57). Task 6's `count` needs "`prior` is null" and adds claims "present only in a first-pass `form` line" (plan:87). A dropped claim that was a carried prior therefore cannot be told apart from a dropped new claim, and it is counted as new. The Task 6 fixture (plan:90) has no withdrawn-carried-prior case. M0 is the pre-registered headline measure, and its bar is "<= 3 in both" (source.md:185), so a single miscount can flip it. Neither V1 nor V3 raised this.
2. **Coverage denominator.** V2 alone reports how many spec units it audited and how many were fully adherent (35 / 33), and it names the three lexical misses confirmed covered (INF-003 in Task 9, INF-009 in Task 3, INF-034 in Task 6). V1 confirms the same point in one line. V3 does not address it.
3. **The V2 calibration notes record coverage gaps that no other card raised, and I verified them with Grep.** The plan never mentions `same-class` (source.md:66, the sentinel's `grader_model=` marker) or the script-computed `origin=changed|unchanged` (source.md:111). The grep also confirms that "counted once" (source.md:128) and `parent=` (source.md:73) appear nowhere in the plan. V1 does cover those two (C-005, C-010).
4. **Deviation classification for the plan's own gaps.** Labelling QA-002 as drift is defensible. The plan departs from source.md:173 (carried priors excluded) without an owner ruling that authorizes it.

#### Weaknesses identified in others

1. **V1 F1 and F2 (C-002, C-001) are graded blocking, but read-ahead resolves them.** The names and behaviour are fully specified later in the same plan (plan:77, plan:87). The deliverable after Task 6 is correct. These are ordering defects that cost per-task QA friction, not a wrong deliverable.
2. **V3 R3-1 (C-004) is graded blocking, but the variant's behaviour is right.** With `## Unattended mode` removed (spec-panel.md:451-462), nothing implements the advertised flags. The defect is a stale Usage token, and the S1 briefs never pass `--unattended` (plan:21). It is a real defect that the plan must fix itself (V3's lock-in point), but it is minor.
3. **V3 R3-2 (C-005) is graded blocking for one missing test case.** The rule is unstated in source.md too (source.md:128 is only a test name), so the right fix is to state it and add the test, not to halt.
4. **V3 R3-11 (C-019) cites the confidence-calibrator pattern (confidence-calibrator.md:4 has `category: analysis`), but the spec lists the exact keys (source.md:124), and the plan follows the spec (plan:44).** This is not a defect.
5. **V1 and V3 both missed QA-002.** Neither card checks the `count` rule against the M0 definition at source.md:173.

#### Concessions

- **QA-001 (C-008) is overgraded.** Section 3 does not list the measurement copy. It is an experiment-install step (source.md:163), and the plan installs nothing (plan:20). What remains is V1's point: the INSTALL.md sentence "the measurement copy and the repo copy differ only in the lines that came from master" (plan:172) is asserted, not checked. Minor. V1 is superior on this point.
- **QA-002 should be minor, not blocking.** It is reporting only (plan:22), and the case is rare: a carried prior withdrawn during the one repair. The fix is one field on the `form` line plus one fixture row.
- **V2 did not classify the declared deviations:** the Unattended removal (owner-authorized, plan:21) and the `_POST_REFRESH_ADDITIONS` edit (necessary, plan:135). V1's classification is correct.
- **V2 missed C-003 (the replay prior-report gap).** It is the most consequential finding in the debate.
- V2 also missed the Usage-line contradiction, the staging gap after Task 12, and V3's test-ordering items.

#### Per-point positions

| id | finding real? | correct severity | superior variant |
|---|---|---|---|
| S-001 | yes (V2 under-reports: 2 findings against 12/12+1) | not-a-defect | tie (V1/V3) |
| S-002 | yes (V2 omits the declared deviations; V3 counts are unmapped) | not-a-defect | V1 |
| S-003 | partly (an explicit verdict field helps triage; it does not change the plan) | not-a-defect | V3 |
| C-001 | yes (plan:77 forward-references Task 6 `count`) | minor | V1 |
| C-002 | yes (plan:60 needs `compute_verdict` and prior statuses from Task 5) | minor | V1 |
| C-003 | yes (control-r1 review folder has no sentinel report; `begin` exits 5, plan:57; no prior fixture named, plan:96) | blocking | V1 |
| C-004 | yes (spec-panel.md:23 advertises `--unattended`; plan:123/135 lock it in) | minor | V3 (analysis; V1 has the severity right) |
| C-005 | yes (source.md:128 is in no acceptance list; "counted once" is absent from the plan) | minor | V1 |
| C-006 | yes (Tasks 13 and 14 create files after Task 12's staging; plan:27 requires `.dev/tasks` staged) | minor | tie (V1/V3) |
| C-007 | partly (the Task 14 names are fixed in advance at plan:182-184; plan:190 checks the list) | not-a-defect | tie |
| C-008 | partly (not a deliverable; the INSTALL.md claim at plan:172 is unverified) | minor | V1 |
| C-009 | yes (plan:57 `form` has no `prior`; plan:87 needs `prior` null; source.md:173 excludes carried priors) | minor | V2 |
| C-010 | yes (source.md:34 `final`/`verdict` writers, `grader_model=` source, `parent=` at source.md:73 absent from the plan) | minor | V1 |
| C-011 | yes (source.md:68 defines `real:true` reinstatement only for claims) | minor | V1 |
| C-012 | yes (plan:96 leaves the quote line unspecified; the anchored/late split depends on it) | minor | V1 |
| C-013 | partly (the import grep runs only in Task 3, plan:61; Task 10's worker-contract run catches write verbs) | minor | tie (V1/V3) |
| C-014 | yes (the equality test excludes the replaced blocks, plan:135; no positive wording check) | minor | V3 |
| C-015 | yes (`git ls-files` sweep at test_review_severity_rule.py:36-39; run before staging, plan:140/161) | minor | V3 |
| C-016 | partly (the omitted suites read new files; likely pass) | minor | V3 |
| C-017 | partly ("the literal recorded in" most likely means a constant in the test) | not-a-defect | V3 (raised; low value) |
| C-018 | partly (plan:19 exception is circular through plan:172; 5.1 and 5.3 procedures are not owner-authorized) | minor | V3 |
| C-019 | no (source.md:124 lists exact keys without `category:`) | not-a-defect | tie (V1/V2 correctly silent) |
| C-020 | yes (comment at test_routing_refresh.py:29-32 names only #323/#302; plan:141 forbids touching it) | minor | V3 |
| C-021 | yes (spec-panel.md:430-436 critique examples stay plain; this follows source.md:104 literally) | minor | V3 |
| X-001 | yes (the conflict is real) | minor | V1 |
| X-002 | yes (the conflict is real) | minor | V1 |
| X-003 | yes (V1's reading holds) | minor | V1 |
| X-004 | yes (V2 left the declared deviations unclassified) | not-a-defect | V1 |

#### Shared assumptions

- **A-001: QUALIFY.** Read-ahead within the one plan is allowed, because the executor holds the whole plan. A forward reference is blocking only when no later task supplies what is missing. C-003 is that case: nothing in the plan supplies a sentinel-bearing prior report. C-001 and C-002 are not.
- **A-002: ACCEPT.** The dated owner rulings in the plan's Constraints (plan:21-24) settle questions that source.md left to the owner (source.md:248, 256), so they outrank the source text. V2's failure to classify them is a card weakness.
- **A-003: QUALIFY.** The inputs exist at debate time: `exp346-ab-ctl-r1/.dev/orca-command-refactor/review/spec-panel-round3.md` and `specs/history/spec-v2-after-round1.md` / `spec-v3-after-round2.md`, the T05-T10 briefs under `exp346-p1-logs`, and `/tmp/impl/exp/s1/filled-flg-r1-T07.txt` / `T09.txt`. But `/tmp` is volatile. Tasks 7 and 14 already stop as blocked or check sha256 (plan:96, plan:182), so a missing input surfaces at execution time. It is not a plan defect.

### Variant 3 Advocate

#### Round 1 statement: Variant 3 (reviewer-3, refactorer persona)

#### Position summary

V3 is the most complete map of where the plan's text lets the final deliverables disagree with the spec or with each other. It alone covers the test-harness layer: the equality test that locks in the Usage-line contradiction, the git-tracked sweep that runs before staging, omitted suites, the stale allow-list comment and missing positive wording checks. V3 is weaker than V1 on task ordering and inside-the-script gaps, and weaker on mapping deviations to ids. I drop the blocking label on R3-1. I keep it, narrowly, on R3-2.

#### Steelman

**V1 (analyzer).** Strongest argument: V1 is the only card that walked the dependency chain through the script tasks. Task 3's acceptance (plan:60) needs `begin` to exit 5 on a prior-verdict mismatch, but `compute_verdict` is only defined in Task 5 (plan:77). Task 5's label-count line is "built by the same function as Task 6's `count`" (plan:77), and Task 6 depends on Task 5 (plan:85). The replay in Task 7 (plan:96) cannot reach review 3 without a prior review-2 report that carries a sentinel, which `begin` requires (source.md:62). What V1 gets right: these are real, checkable defects that a per-task executor (`/sc:implement` checks each task against its own criteria) will hit. V1 also gets the deviation classification right: the Unattended removal is authorized (plan:21) and the routing-refresh edit is necessary (plan:135). Critique: V1 marks all three as blocking. Its own calibrator says they "fit major better than blocking" (variant-1:101), because an implementer who writes `compute_verdict` early, or builds a tmp_path prior report, still ends with the right files. V1 also misses the whole test-harness layer (C-014 to C-016, C-020).

**V2 (QA).** Strongest argument: QA-002 is a real, narrow correctness gap no one else found. The first-pass `form` line keeps `id` and `claimed` (plan:57) but not `prior`. Task 6's `m0_label_cm` counts claims "whose `prior` is null", plus claims present only in a `form` line (plan:87). So a withdrawn carried prior cannot be told apart from a withdrawn new finding. That breaks M0's rule "carried priors excluded" (source.md:173). What V2 gets right: it reads the owner-decision count against the ledger schema, which is exactly where a count bug would hide. Critique: QA-001 treats the measurement copy (source.md:163) as a missing repo deliverable. The plan installs nothing (plan:20), and section 4 describes it as an experiment-install step, so this is a hand-off note, not a missing file (calibrator 0.20, variant-2:38). V2's drift counts (2) ignore the two declared deviations its own calibrator flags (variant-2:41). V2 covers 2 findings against 12 and 12.

#### Strengths claimed

1. **R3-1 finds the lock-in, not just the inconsistency.** spec-panel.md:23 advertises `[--unattended] [--report-dir <dir>] [--improve]`. `--report-dir` and `--improve` are defined only inside `## Unattended mode` (spec-panel.md:456, :459), and the grep shows those three lines are the only places either flag appears. Task 9 removes that section and states the variant does not accept `--unattended` (plan:123, plan:21). Task 10's equality test exempts only the name changes on Usage (plan:135), so a fix that drops the tokens would fail it. V1 F4 saw the token. Only V3 names all three orphaned flags with evidence and the equality-test trap (V1 put `--report-dir` in a calibrator note only, variant-1:103).
2. **R3-2 gives the only actionable rule for the counted-once case.** Source.md:128 requires "two claims on one prior counted once". No acceptance list contains it (plan:60, :71, :80, :90), and no task defines what "counted once" applies to. V3 names the three counters it must apply to: the verdict, D1..Dk renumbering and `m1_open_confirmed`. V1 F5 says only "add the case and the rule".
3. **R3-4 is a verified false-pass path.** `_files_under` filters `_tracked_text()` (test_review_severity_rule.py:54-56), which comes from `git ls-files` (lines 36-41). Task 10 (plan:140) and Task 12 (plan:161-165) run the suite before the new files are staged, so the banned-phrase sweeps (lines 450, 508) never see the new command, skill or agent. The tests pass locally and can fail after commit.
4. **R3-5 is grounded.** `test_tavily_tool_parity.py:31-34` rglobs every agent and skill `.md` for `tools|allowed-tools`, which covers the new `finding-grader.md` and `SKILL.md`. `test_retired_docs_absent.py:40` reads `docs/` and `src/superclaude` markdown. Task 12 runs `tests/skills tests/recommend tests/unit tests/core tests/commands` only (plan:165).
5. **R3-3: no positive check for the new FR-8/FR-9 wording, the bullet-7 suffix or the no-unattended sentence.** The equality test exempts exactly these blocks (plan:135), and Task 9's acceptance list (plan:126) does not name them. A variant missing them passes every listed check.
6. **R3-12 is verified.** The `_POST_REFRESH_ADDITIONS` comment (test_routing_refresh.py:29-32) lists the issues behind each addition. Plan:141 lets only the set line change, so the comment goes stale or the check fails.
7. **R3-10 is the one scope-drift finding.** The `offline-demotion-audit.md` and `replay-gate.md` templates (plan:184) implement section 5.3 and 5.1 procedures. Plan:19 excludes sections 5-7 except "the brief templates the install note lists", and that list is written by this same plan (Task 13, plan:172), so the carve-out is circular.

#### Weaknesses identified in others

1. **V1 overstates three blocking labels.** For F1, F2 and F3 the final deliverable is correct once an implementer reorders the code or adds tmp_path scaffolding. Plan:96 forbids a synthetic substitute only for missing control-r1 files. Its own calibrator downgrades them (variant-1:101).
2. **V1 misses the harness layer.** V1 has nothing on C-014, C-015, C-016 or C-020, and these are where a passing plan ships a failing commit.
3. **V2 misreads scope on QA-001.** Plan:20 says nothing is installed, and source.md:163 sits in the install procedure. V1 F12 classifies it correctly: not a plan defect, only INSTALL.md's "differ only in lines from master" claim is unverified.
4. **V2's deviation classification is empty where it matters.** It records 0 authorized and 0 necessary, although plan:21 is an explicit owner ruling and plan:135 declares itself a necessary deviation.
5. **V2's coverage is too thin.** It audits 35 units, calls 33 adherent and reports 2 findings, but its own calibrator then lists three more unchecked spec items (variant-2:42-43). One of them is the counted-once case all three cards eventually touch.

#### Concessions

- **R3-1 is minor, not blocking.** Spec 3.1 says "copy with exactly these edits", so keeping the Usage line is literally spec-compliant. The contradiction comes from the owner ruling, and no S1 brief passes `--unattended` (plan:21), so no measured run takes a wrong path. It still needs fixing in Task 9 and Task 10.
- **R3-11 is not a defect.** Source.md:124 lists the exact frontmatter keys without `category:`. The plan follows the spec. Confidence-calibrator's `category: analysis` is only pattern similarity.
- **R3-7 is ambiguous at most.** "equals the literal recorded in" (plan:135) most naturally means a constant in the test.
- **R3-9 is ordering awkwardness.** The file names are fixed in advance (plan:184). V1 F7 states the real gap more sharply: Task 14 never tells anyone to update INSTALL.md, yet requires it to list eleven files (plan:190).
- **V3's deviation counts are not tied to ids.** To map them now: authorized = the Unattended removal (plan:21), necessary = the `test_routing_refresh.py` edit (plan:135), drift = R3-10. V1's classification is superior on this point.
- **V3 missed V1's ordering defects (F1, F2), the replay prerequisite (F3), the `real:true` seeded-hunk gap (F9) and V2's withdrawn-prior gap (QA-002).**

#### Per-point positions

| id | finding real? | correct severity | superior variant |
|---|---|---|---|
| S-001 | yes | not-a-defect | tie |
| S-002 | yes | minor | V1 |
| S-003 | yes | not-a-defect | V3 |
| C-001 | yes | minor | V1 |
| C-002 | yes | minor | V1 |
| C-003 | yes | minor | V1 |
| C-004 | yes | minor | tie |
| C-005 | yes | blocking | V3 |
| C-006 | yes | minor | tie |
| C-007 | partly | minor | V1 |
| C-008 | partly | minor | V1 |
| C-009 | yes | minor | V2 |
| C-010 | partly | minor | V1 |
| C-011 | yes | minor | V1 |
| C-012 | partly | minor | V1 |
| C-013 | partly | minor | tie |
| C-014 | yes | minor | V3 |
| C-015 | yes | minor | V3 |
| C-016 | partly | minor | V3 |
| C-017 | partly | not-a-defect | V3 |
| C-018 | partly | minor | V3 |
| C-019 | no | not-a-defect | tie |
| C-020 | yes | minor | V3 |
| C-021 | yes | minor | V3 |
| X-001 | yes | minor | V1 |
| X-002 | yes | blocking | V3 |
| X-003 | partly | minor | V1 |
| X-004 | yes | minor | V1 |

Notes on the contested rows:

- **C-005 / X-002 stays blocking.** Source.md:128 makes the case a required part of `test_stoprule_script.py`. A per-task executor treats the acceptance lists as its definition of done, and the case is in none of them. The behaviour is also undefined, so no implementer can write the test without inventing the rule. The strongest counter is plan:57's "the begin and seal cases of source.md section 3.4". It does not settle the point, because counted-once is about counting and verdicts, not about `begin` or `seal`.
- **C-003** is the most serious of the minors. It becomes blocking only if the executor reads plan:96's "no synthetic substitute" as covering test scaffolding.

#### Shared assumptions

- **A-001: QUALIFY.** Blocking means the final deliverable is wrong or missing after all tasks are done as written. Reading ahead is allowed, so ordering defects (C-001, C-002) are minor. Behaviour the plan never defines (C-005) cannot be read ahead to, so it can still be blocking.
- **A-002: QUALIFY.** Owner rulings outrank source.md only on the points they actually address (plan:21-24). They do not authorize side effects they never mention, such as the orphaned Usage flags.
- **A-003: QUALIFY.** All four inputs exist today (ls on 2026-11-08: the `exp346-ab-ctl-r1/.dev/orca-command-refactor` folder, the `exp346-p1-logs` S1 `task-text` folder and both `/tmp/impl/exp/s1/filled-flg-r1-T0{7,9}.txt`). `/tmp` is volatile, though. Plan:96 and plan:182 stop as blocked on a missing file or a sha256 mismatch, so a missing input gives a blocked task, never a wrong deliverable.

## Round 2: Rebuttals

### Variant 1 Rebuttal

#### Round 2 rebuttal: Variant 1 (reviewer-1, analyzer)

#### Response to criticisms

### 1. "F1 / C-002 is a forward reference that read-ahead resolves" (V2 weakness 1, V3 weakness 1)

**Steelman.** The blocking test asks about the deliverable, not about per-task friction. Task 3 says `begin` must exit 5 "when the recomputed prior verdict differs from its last line" (plan:57), and its acceptance list names "prior-verdict mismatch" (plan:60). The verdict rule is fully written down later in the same plan (plan:77, `compute_verdict` per step 9) and in source.md step 9. An implementer who holds the whole plan writes `compute_verdict` during Task 3, and Task 5 then only adds `status`, `verdict` and `finalize` around it. After Task 6 the script and its tests are correct.

**Response: conceded, now minor.** My Round 1 case rested on per-task QA rejecting Task 3. That is a cost in rework and QA friction. It is not a wrong or missing deliverable. Nothing has to be invented: every rule Task 3 needs is defined in plan:77 and source.md step 9. The fix is still worth making: move `compute_verdict` into Task 3, or move the mismatch case into Task 5's acceptance list. But it is minor.

### 2. "F3 / C-003 is minor because tmp_path scaffolding gives the right files" (V3 weakness 1, V3 per-point C-003)

**Steelman.** The rule "no synthetic substitute is written" (plan:96) covers only missing control-r1 files, so it does not forbid a test that builds a prior review-2 report in tmp_path. A competent implementer would see that `begin` needs a review-2 sentinel and would build one, and then the replay asserts a real split.

**Response: not conceded. New evidence makes this a silent wrong deliverable, not just a blocked step.** Take the text exactly as written. The test "runs `begin` and `seal` (no grader) on the fixture with `spec-v2.md` as baseline" (plan:96), and it names only three fixture files with no prior report (plan:96, acceptance at plan:99). With no `--re-review`, `begin` sets N = 1 (plan:57, "1 without `--re-review`"; source.md:62). The ratchet runs only "for reviews 2 and 3" (plan:57), and "review 1 has no baseline (`ratchet=off`, recorded)" (source.md:243). So every claim comes out anchored: 8 anchored, 0 late-found. The plan then tells the test to assert "the computed split ... without forcing it to 5 and 3" (plan:96). The 8/0 run therefore passes every acceptance criterion in Task 7 and gets recorded in `t7-fixture-sources.txt` as the replay result. The deliverable is wrong: a replay fixture that never exercises the ratchet. Every listed check still passes. The other reading, passing `--re-review`, needs a sentinel-bearing review-2 report, and the control r1 reports have none (the folder holds only plain `spec-panel*.md` reports; V2 verified this independently). On that reading `begin` exits 5. V3's scaffolding route is possible, but the plan never asks for it. The scaffold also has to satisfy four checks: a `review=2/3` sentinel, a `spec=` hash equal to the sha256 of `spec-v2.md`, a matching rubric hash, and a verdict that can be recomputed from its ledger (source.md:62). That is a design task the plan never gives. Blocking stands. V2 agrees.

### 3. "F2 / C-001 overstated" (V2, V3)

Already conceded in Round 1 (now minor). No change.

### 4. "V1 misses the harness layer" (V3 weakness 2)

Conceded in Round 1: C-014, C-015, C-016 and C-020 belong to V3. No change.

### 5. "V1 missed the withdrawn-prior counting gap" (V2 weakness 5)

Conceded in Round 1: C-009 belongs to V2. No change.

### 6. C-005 / X-002: V3 holds that the missing counted-once case is blocking

**Steelman (V3).** source.md:128 makes "two claims on one prior counted once" a required case. No acceptance list contains it (plan:60, :71, :80, :90). The rule is never defined, so an implementer cannot write the test without inventing one. A per-task executor treats the acceptance lists as its definition of done, so the case goes missing.

**Response: still minor.** Two points. (a) The case is not out of Task 3's reach. Task 3's body imports "the begin and seal cases of source.md section 3.4" (plan:57). In source.md:128 the counted-once case sits right after "valid and invalid prior links", which is the `seal` ratchet, so an exact follower writes some test there. V3's real point is (b): the rule is undefined. That point is right, but its effect is limited. Two claims on one prior can change a count. They cannot change the verdict: one confirmed claim already gives FAIL `confirmed` (plan:77). What they can affect is the D1..Dk listing and the `m1_open_confirmed` count, and those are reporting and display (plan:22, "This is reporting only"). An under-specified count with no effect on the verdict is minor. The fix: state the rule in Task 3 (dedupe by prior id for the verdict counts, the D list and `m1`) and add the case to Task 3's acceptance. V3's naming of the three counters is the better fix text, so V3 wins on fix quality. V1 keeps the severity.

### 7. C-007: V2 grades it not-a-defect

**Steelman (V2).** The Task 14 file names are fixed in advance (plan:182-184). Task 13 explicitly says to write "a list of the brief templates written by Task 14" (plan:172), which tells the writer to read ahead. Task 14's check "INSTALL.md lists all eleven files" (plan:190) then passes.

**Response: conceded, now not-a-defect.** My own Round 1 A-001 position said read-ahead is fair when a later task only fixes names in advance, and I named C-007 as that case. Grading C-007 minor contradicted my own position. Task 13 is told to list the eleven names, and the names exist in the plan text. INSTALL.md is briefly ahead of the files between Tasks 13 and 14. The final deliverable is correct.

### 8. C-017: rubric hash literal

**Steelman (V2, V3).** "Equals the literal recorded in `./artifacts/t1-rubric-sha256.txt`" (plan:135) most naturally means that the test holds the hash as a constant, copied from the artifact. Nothing reads the plan folder at test time.

**Response: conceded, now not-a-defect.** Even the bad reading corrects itself. pytest runs from the repo root, where `./artifacts/` is not the plan's folder, so a runtime read would fail at once in Task 10's own acceptance run (plan:137). It would not pass silently and then break later at archive. No wrong deliverable survives.

### 9. S-002 and X-004: deviation classification, minor vs not-a-defect

**Steelman (V2: not-a-defect).** These rows compare how the cards classified the plan's declared deviations. As facts about the plan, the Unattended removal (owner ruling, plan:21) and the `_POST_REFRESH_ADDITIONS` edit (plan:135, which calls itself "a necessary deviation") are authorized and necessary. By definition, those classes need no change to the plan. The one real drift, the section-5 templates, has its own row (C-018).

**Response: conceded, now not-a-defect.** Grading S-002 or X-004 minor would count C-018 a second time. The plan defect lives in C-018 (minor, V3). V1 is still the superior card on these rows, because it alone ties each count to a named, cited deviation.

#### Updated assessment of the other variants

- **V2.** Its Round 1 statement is well calibrated: it concedes QA-001 and QA-002 to minor, and it independently confirms that the control r1 report has no sentinel (C-003). Its read-ahead rule for A-001 is the right one, and I now apply it to C-002 and C-007. C-009 remains the only finding that touches M0's correctness, and it is a real addition. Its card coverage is still the thinnest: 2 findings.
- **V3.** It is strongest on the harness layer (C-014, C-015, C-016, C-020) and on the Usage lock-in argument (C-004, now minor by its own concession). It rightly says C-002 is minor, and I now agree. On C-003 its "minor" depends on an implementer building scaffolding the plan does not ask for. It also does not address the review-1 path, where the literal test passes with 8/0. On C-005 its blocking label confuses an undefined count with a wrong deliverable, because the verdict cannot change.

#### New evidence

1. **C-003 silent pass.** plan:57 ("1 without `--re-review`", "ratchet for reviews 2 and 3") together with source.md:243 ("review 1 has no baseline (`ratchet=off`, recorded)") and plan:96 ("asserts the computed split ... without forcing it to 5 and 3"). Read literally, the replay test computes 0 late-found and passes all Task 7 acceptance criteria. That is a wrong deliverable no check catches.
2. **C-005 bounded effect.** plan:77: any `confirmed` claim gives FAIL `confirmed`, so a duplicated prior link cannot flip the verdict. Only counts and the D list change.
3. Re-checked: the control r1 review folder holds `spec-panel.md`, `spec-panel-round2.md`, `spec-panel-round3.md` and two disposition files. A grep for `stoprule` in them finds no match.

#### Final per-point table (contested points only)

| id | severity | superior variant | changed since Round 1? |
|---|---|---|---|
| C-002 | minor | V1 | yes |
| C-003 | blocking | V1 | no |
| C-005 | minor | V1 (severity); V3 (fix text) | no |
| X-002 | minor | V1 | no |
| C-007 | not-a-defect | V2 | yes |
| C-017 | not-a-defect | V2 | yes |
| X-004 | not-a-defect | V1 | yes |
| S-002 | not-a-defect | V1 | yes |

### Variant 2 Rebuttal

#### Round 2 rebuttal: Variant 2 (reviewer-2, qa persona)

#### Response to criticisms

### 1. "V2's coverage is thin: 2 findings against 12 and 12+1" (V1 weakness 3, V3 weakness 5, V1 Round 2 assessment)

**Steelman.** A card that audits 35 units, calls 33 adherent and reports 2 findings missed real defects that the other cards verified. These include C-003 (the replay prerequisite), C-004 (the Usage-line lock-in), C-006 (staging after Task 12) and the harness layer (C-014, C-015, C-016, C-020). Its own calibrator then listed further unchecked spec items, one of them the counted-once case (C-005). A reader who relied on V2 alone would ship a plan with a blocking defect.

**Response: conceded in full.** This is the main weakness of V2. I do not claim that V2's 33/35 adherence figure is accurate, because C-003 alone falls inside a unit V2 marked adherent (the section 3.4 replay fixture). What V2 still adds is narrow: the only check of the `count` rule against the M0 definition (C-009), which V1 Round 2 accepts as "a real addition".

### 2. "QA-001 misreads scope; the measurement copy is not a deliverable" (V1 weakness 1, V3 weakness 3)

**Response: conceded in Round 1, no change.** plan:20 says nothing is installed, and source.md:163 is an install step. Only the INSTALL.md sentence at plan:172 ("differ only in the lines that came from master") is asserted without a check. Minor. V1 is superior on C-008.

### 3. "QA-002 is overgraded as blocking" (V1 weakness 1)

**Response: conceded in Round 1, no change.** The count is reporting only (plan:22). The finding itself stands, and both other cards now accept it. I re-checked it. Task 3's first-pass `form` line records `id` and `claimed` only (plan:57). Task 6's `m0_label_cm` needs "`prior` is null" (plan:87). So a carried prior withdrawn between seals cannot be excluded, as M0 requires (source.md:173). Minor, V2.

### 4. "V2's deviation counts are wrong: authorized 0, necessary 0" (V1 weakness 2, V3 weakness 4)

**Response: conceded in Round 1, no change.** plan:21 is an owner ruling (authorized). plan:135 calls its own edit "a necessary deviation". V1's mapping is correct, which settles S-002 and X-004 in V1's favour.

### 5. "V2 missed C-003" (V2 self-concession, V1)

**Response: conceded.** I add evidence on C-003 below, and the evidence changes how the defect shows up but not its severity.

#### Updated assessment of the other variants

- **V1.** Its Round 2 concessions on C-002, C-007, C-017, S-002 and X-004 apply the read-ahead rule that V2 and V3 proposed for A-001, so V1's table and mine now agree on every contested severity. Its C-003 severity is right. Its new "silent pass" argument is wrong on the text (New evidence 1). The steelman is that "the test asserts the computed split ... without forcing it to 5 and 3" (plan:96) could be read as "assert whatever split comes out". That reading drops the clause just before it, which tells the test what to assert for each claim: claims quoting changed lines "are not `late-found`", and claims on unchanged text "are `late-found`". So C-003 is a loud failure, not a silent wrong deliverable. It is still blocking, because the Task 7 deliverable cannot be produced from the plan's text. V1's bounded-effect argument on C-005 is correct, and I extend it below.
- **V3.** It is strongest on the harness layer and on the Usage lock-in. On C-005 it argues that the case is in no acceptance list and the rule is undefined. That is accurate, but it does not meet the blocking test. Task 3's body imports "the begin and seal cases of source.md section 3.4" (plan:57), and source.md:128 lists the counted-once case among those seal-adjacent cases, between "valid and invalid prior links" and "uncovered hunk". The undefined rule cannot change the verdict or M0 (New evidence 2). On C-003, V3's "minor" depends on tmp_path scaffolding the plan never asks for. A strict follower could also read plan:96's "no synthetic substitute is written" as forbidding it, since a sentinel-bearing review-2 report would be a synthetic stand-in for a control-r1 file that does not exist in that form.

#### New evidence

1. **C-003: the literal review-1 run fails loudly; it does not pass vacuously.** Without `--re-review`, `begin` sets N = 1 (plan:57; source.md:62), and the ratchet runs only "for reviews 2 and 3" (plan:57; source.md:64, :243). V1 is right that every claim then comes out anchored. But plan:96 makes the test assert two things for each claim. Claims quoting lines changed between v2 and v3 must not be `late-found`, and claims on text unchanged since v2 must be `late-found`. The expected set comes from the v2/v3 diff (`changed_lines`, plan:57), so it does not depend on `seal`'s output. source.md:193 records that 3 of the 8 control-r1 claims "sit on text the previous review already saw". Those 3 come out anchored at review 1, so the second assertion fails, and Task 7's acceptance check `uv run pytest ... -k replay` passes (plan:101) cannot be met. The only case where the review-1 run passes is the one where all 8 claims quote changed lines. In that case ratchet on and ratchet off give the same result, so even that pass is not a wrong deliverable. Two literal paths remain, and both block: no `--re-review` (the assertion fails) or `--re-review` on the plain control-r1 report (exit 5). The only way through is a hand-built review-2 report with its own checks, which the plan neither specifies nor clearly permits. Result: blocking (missing deliverable), V1 superior, mechanism corrected.
2. **C-005: neither the verdict nor M0 can change.** A frozen prior that is still open already gives FAIL `unresolved-prior` (plan:77), and any `confirmed` claim gives FAIL `confirmed` (plan:77). So a second claim on the same prior cannot flip the verdict, however it is counted. `m0_label_cm` counts only claims "whose `prior` is null" (plan:87), so claims carrying a prior link are outside M0 by definition. What remains is `m1_open_confirmed` and a possible duplicate entry in the D1..Dk listing. Both are reporting or display. Minor. V1 has the severity right. V3's naming of the three counters gives the better fix text.

#### Final per-point table (contested points only)

| id | severity | superior variant | changed since Round 1? |
|---|---|---|---|
| C-002 | minor | V1 | no |
| C-003 | blocking | V1 | no |
| C-005 | minor | V1 (severity); V3 (fix text) | no |
| X-002 | minor | V1 | no |
| C-007 | not-a-defect | V2 | no |
| C-017 | not-a-defect | tie (V2/V3) | no |
| X-004 | not-a-defect | V1 | no |
| S-002 | not-a-defect | V1 | no |

### Variant 3 Rebuttal

#### Round 2 rebuttal: Variant 3 (reviewer-3, refactorer persona)

#### Response to criticisms

### 1. "C-003 is blocking, not minor: V3's minor depends on scaffolding the plan never asks for" (V1 Round 2 item 2, V2 Round 2 assessment and new evidence 1)

**Steelman of my Round 1 position.** The phrase "no synthetic substitute is written" (plan:96) applies only when the control-r1 files cannot be found. Task 3 already builds every test on tmp_path fixtures (plan:57, source.md:128). A tmp_path prior report is therefore allowed, and a capable implementer would build one. The cheapest version is a review-2 PASS report with an empty sealed ledger whose sentinel carries `spec=` (the sha256 of `spec-v2.md`) and the rubric hash. `begin` accepts a prior PASS (source.md:62), sets N = 3, and the ratchet runs.

**Response: conceded, now blocking.** Taken as written, both paths fail, and V2's mechanism is the right one:

- **No `--re-review`.** `begin` sets N = 1 (plan:57, "1 without `--re-review`"). The ratchet runs only "for reviews 2 and 3" (plan:57, source.md:64), and "review 1 has no baseline (`ratchet=off`, recorded)" (source.md:243). Every claim comes out anchored. plan:96 then makes the test assert, for each claim, that claims on text unchanged since v2 "are `late-found`". The expected set comes from the v2/v3 diff, not from `seal`'s output. source.md:193 records that 3 of the 8 claims sit on unchanged text, so that assertion fails, and the acceptance check `-k replay passes` (plan:101) cannot be met.
- **With `--re-review` on the real control-r1 report.** That report has no sentinel (V1 and V2 both checked), so `begin` exits 5 (plan:57, source.md:62).

My scaffolding route works only if the implementer designs something the plan never describes (New evidence 1). A deliverable that cannot pass its own acceptance check without unplanned design work is a missing deliverable. V1 found the defect, so V1 is the superior variant. On mechanism, V2's "loud failure" reading is right and V1's "silent 8/0 pass" is not, because plan:96 says what to assert for each claim, not just "whatever split comes out".

### 2. "C-005 / X-002 is minor: an open frozen prior already fails the verdict, and M0 counts only prior-null claims" (V1 Round 2 item 6, V2 new evidence 2)

**Steelman of my Round 1 position.** source.md:128 makes "two claims on one prior counted once" a required case. The plan never states the rule; the word "once" in that sense appears nowhere in it. A per-task executor treats the acceptance lists (plan:60, :80, :90) as its definition of done, and the case is in none of them. Nobody can write the test without inventing the rule.

**Response: conceded, now minor.** Three points decide it:

- Both verdict facts are correct. Any `confirmed` claim gives FAIL `confirmed`, and an open frozen prior gives FAIL `unresolved-prior` (plan:77). A second claim on the same prior therefore cannot flip the verdict.
- `m0_label_cm` counts only claims "whose `prior` is null" (plan:87), so prior-linked claims are outside M0 by definition.
- **Parity with C-009.** C-009 is V2's withdrawn-prior gap. It can miscount M0, the headline measure with a "<= 3" bar (source.md:185), in a rare edge case. All three of us, me included (Round 1 table), graded it minor. C-005 can miscount M1, also in a rare edge case (two claims linking the same prior). Grading C-005 blocking while C-009 stays minor would be inconsistent.

The undefined rule is also inherited from the spec: source.md:128 names the case without a rule. Task 3's body imports "the begin and seal cases of source.md section 3.4" (plan:57), so an exact follower writes some test there.

One correction to the reasoning on the other side (New evidence 2): M1 is not "reporting or display" in the cosmetic sense. It is a pre-registered measure with a stop rule. The fix therefore matters more than V1's wording suggests. It remains minor.

### 3. "R3-1 and R3-2 overgraded as blocking" (V1 Round 1 weakness 4, V2 Round 1 weaknesses 2-3)

R3-1 was conceded in Round 1. R3-2 is conceded above. No V3 finding remains blocking.

### 4. "V3's deviation counts are not tied to ids" (V1 Round 1 weakness 5, V2 Round 1 critique)

This was conceded in Round 1. It is a defect in the review card, not in the plan, so it supports the not-a-defect grade for S-002 and X-004 in item 6 below.

### 5. "R3-7 / C-017 rests on an unlikely reading" (V2 Round 1 critique)

This was conceded in Round 1 (not-a-defect). V1 Round 2 adds that even the bad reading fails at once: pytest runs from the repo root, where `./artifacts/` is not the plan folder. The failure would therefore be loud during Task 10's own run, and nothing silently breaks at archive. I accept that. My card raised a non-defect, and V1 and V2 were right to stay silent, so the superior variant moves away from V3.

### 6. C-007, S-002, X-004: Round 1 minor, now not-a-defect

**Steelman of minor.** V1's F7 point: Task 14 never says to update INSTALL.md, yet its check needs INSTALL.md to list all eleven files (plan:190). For S-002 and X-004: the plan really does carry three deviations, and V1 counted two.

**Response: conceded on all three.**

- **C-007.** Task 13 itself tells the writer to list the brief templates "written by Task 14" (plan:172; the phrase is there). The names are fixed in advance at plan:182-184, and plan:190 checks them. That is the read-ahead case I accepted under A-001 in Round 1, so the final deliverable is correct.
- **S-002 and X-004.** The declared deviations are authorized (plan:21, an owner ruling) and necessary (plan:135, which calls itself "a necessary deviation"). Neither needs a plan change. The one drift, the section-5 templates, already has its own row (C-018, minor). Grading these rows minor would count it twice. V1 remains the superior card here because it ties each count to a cited deviation.

### 7. C-002: no change

I graded it minor in Round 1, and V1 now agrees. All three variants hold minor, and V1 is superior.

#### Updated assessment of the other variants

- **V1.** It is the strongest card on executability. C-003 is the one blocking defect in the plan, and only V1 found it. Its Round 2 concessions on C-002, C-007, C-017, S-002 and X-004 apply the read-ahead rule consistently. Two weak spots remain: its "silent 8/0 pass" mechanism for C-003 is wrong (V2's correction holds), and calling M1 "reporting only" stretches plan:22, whose "reporting only" sentence covers the owner's label-count measure.
- **V2.** It is the best calibrated on severity. Its C-003 mechanism is the correct one, and its C-005 argument is right on the verdict and on M0. Its coverage is still the thinnest, and it concedes that in full.
- **V3 (self).** It keeps the harness layer: C-014, C-015, C-016 and C-020. It also keeps the Usage lock-in analysis (C-004), the fix text for C-005 (dedupe by prior id in the verdict counts, the D1..Dk list and `m1_open_confirmed`), and the one drift finding (C-018). All of its blocking labels are withdrawn.

#### New evidence

1. **C-003: even the cheapest scaffold forces a design choice the plan does not make.** A prior PASS is accepted, but source.md:62 says that after a PASS "the fix cycle before it gets the `NONE` brief, so the spec does not change". The fixture's baseline-to-review-3 step is a real spec change (v2 to v3), so a PASS-prior scaffold contradicts that rule. A FAIL-prior scaffold instead needs a ledger whose verdict `begin` can recompute (plan:57), with grade lines and a seal. That brings in Task 4/5 structures that the "no grader" replay (plan:96) does not set up. Either way the implementer has to invent a review-2 report shape. **Fix:** Task 7 should specify the prior report. For example: a tmp_path review-2 FAIL report produced by running the script's own `begin`/`seal`/`apply-grades`/`finalize` on `spec-v2.md` with fixture grader replies. Then add it to plan:99's file list.
2. **C-005: M1 is a decision measure, not display.** `m1_open_confirmed` is "sentinel `confirmed` plus frozen `unresolved-prior`" (plan:87, source.md:174). It is pre-registered with a "<= 3 in both" bar (source.md:186), and F1a stops the experiment at "M1 >= 4 in either replicate" (source.md:201). Task 14's recorder template records it (plan:184). Two confirmed claims linking one prior, plus that prior frozen open, could count one defect up to three times. That makes the C-005 fix higher priority than the other minors. It does not make it blocking (parity with C-009, item 2).

#### Final per-point table (contested points only)

| id | severity | superior variant | changed since Round 1? |
|---|---|---|---|
| C-002 | minor | V1 | no |
| C-003 | blocking | V1 (finding); V2 (mechanism) | yes |
| C-005 | minor | V1 (severity); V3 (fix text) | yes |
| X-002 | minor | V1 | yes |
| C-007 | not-a-defect | V2 | yes |
| C-017 | not-a-defect | V1/V2 (correctly silent) | yes |
| X-004 | not-a-defect | V1 | yes |
| S-002 | not-a-defect | V1 | yes |

## Scoring Matrix

| Diff Point | Taxonomy | Final severity | Winner | Confidence | Evidence Summary |
|------------|----------|----------------|--------|------------|-----------------|
| S-001 | L1 | not-a-defect | tie | 90% | Granularity differs by persona; no plan impact |
| S-002 | L2 | not-a-defect | V1 | 90% | V1 maps the declared deviations to authorized/necessary; V2 and V3 conceded |
| S-003 | L1 | not-a-defect | V3 | 85% | Explicit verdict field aids triage only |
| C-001 | L2 | minor | V1 | 90% | Forward reference to Task 6 count; V1 withdrew blocking |
| C-002 | L3 | minor | V1 | 90% | Rules already written at plan:77; rework, no wrong deliverable |
| C-003 | L2 | BLOCKING | V1 | 95% | Replay assertion cannot pass as written (ratchet off at review 1; begin exit 5 with --re-review); all three concur after Round 2 |
| C-004 | L2 | minor | tie (V3 analysis) | 80% | Usage line advertises --unattended; equality test locks it in |
| C-005 | L3 | minor | V1 (V3 fix text) | 90% | Cannot change verdict or M0; affects m1 and D1..Dk only |
| C-006 | L2 | minor | tie | 90% | Files created after Task 12 are not staged |
| C-007 | L2 | not-a-defect | V2 | 90% | Names fixed in advance; checked at Task 14 |
| C-008 | L2 | minor | V1 | 90% | Measurement copy is coordinator work; INSTALL wording unverified; V2 conceded |
| C-009 | L3 | minor | V2 | 90% | Withdrawn carried prior miscount; reporting only |
| C-010 | L2 | minor | V1 | 90% | Writers and sentinel sources unspecified (inherited) |
| C-011 | L3 | minor | V1 | 90% | real:true on unclaimed hunk has no defined outcome |
| C-012 | L2 | minor | V1 | 90% | Quote-line selection rule unstated |
| C-013 | L2 | minor | tie | 85% | Import grep only in Task 3; write-verb risk caught by Task 10 |
| C-014 | L2 | minor | V3 | 90% | No positive wording checks |
| C-015 | L2 | minor | V3 | 90% | Severity-rule sweep reads only tracked files |
| C-016 | L2 | minor | V3 | 85% | Omitted suites likely pass |
| C-017 | L2 | not-a-defect | unresolved (V1/V2/tie) | 70% | Literal most naturally lives in the test; winner split |
| C-018 | L2 | minor | V3 | 85% | Section-5 templates outside stated scope |
| C-019 | L1 | not-a-defect | tie | 90% | source.md 3.3 lists exact keys without category |
| C-020 | L1 | minor | V3 | 90% | Allow-list comment goes stale |
| C-021 | L1 | minor | V3 | 85% | Integration Patterns follows source.md:104 literally |
| X-001 | L2 | minor | V1 | 90% | V3 conceded R3-1 to minor |
| X-002 | L3 | minor | V1 | 90% | V3 conceded R3-2 to minor in Round 2 |
| X-003 | L2 | minor | V1 | 90% | V2 conceded QA-001 is not a deliverable gap |
| X-004 | L2 | not-a-defect | V1 | 90% | Declared deviations are authorized/necessary |
| A-001 | L3 | QUALIFY (all) | agreed | 85% | Read-ahead allowed; blocking = final deliverable wrong or an acceptance check impossible |
| A-002 | L2 | ACCEPT x2, QUALIFY x1 | agreed | 85% | Owner rulings outrank source.md on the points they address |
| A-003 | L2 | QUALIFY (all) | agreed | 85% | Inputs exist today; Task 7/14 keep their blocked paths |

## Convergence Assessment
- Points resolved: 30 of 31
- Alignment: 97%
- Threshold: 80%
- Taxonomy coverage: L1 5, L2 20, L3 6 (all levels covered)
- Status: CONVERGED pending the Round 2.5 invariant gate (see invariant-probe.md)
- Unresolved points: C-017 (winner only; severity agreed)
