# Round 1 statement: Variant 1 (reviewer-1, analyzer)

## Position summary

V1 is the only card that checks the plan as an executable sequence: it finds two places where a task's own acceptance test cannot pass without code a later task builds (C-002) or inputs no task provides (C-003). It also maps the plan's two declared deviations to the right taxonomy classes. Its severity grading is uneven: F2 (C-001) is overstated and I withdraw it to minor. Its reason for dismissing the measurement copy (C-008) was wrong even though its severity was right.

## Steelman

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

## Strengths claimed

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

## Weaknesses identified in others

1. **V2 grades severity without the blocking test.** QA-001's "artifact missing" ignores plan:20 ("nothing is installed by this plan"). QA-002 is a reporting-only overcount (plan:22). V2's own calibrator scored them 0.20 and 0.45 (V2 lines 38-39).
2. **V2's deviation count is wrong on its face.** It reports authorized 0 and necessary 0 while plan:21 and plan:135 declare one of each.
3. **V2's coverage is thin.** It audited 35 units and found 2 findings, while V1 and V3 each found 12. It missed the Usage contradiction (spec-panel.md:23 vs the removed section at :451) that both other cards verified.
4. **V3 inflates two doc and test-list gaps to blocking.** These are R3-1 (C-004) and R3-2 (C-005), for the reasons in its steelman. Its calibrator agrees: "Both blocking labels overstated" (V3 line 54).
5. **V3's deviation counts are not traceable** (V3 line 53, calibrator note), so drift 1 cannot be audited against a finding.
6. **V3's R3-11 is not a defect.** It contradicts source.md:124, which lists the exact frontmatter keys, and the plan follows that list (plan:44).
7. **V3 and V2 both missed the executability defects C-002 and C-003.**

## Concessions

- **F2 / C-001 is minor, not blocking.** The phrase "built by the same function as Task 6's `count`" (plan:77) does not stop Task 5 from defining that function and Task 6 from wrapping it.
- **F1 / C-002 depends on A-001.** If per-task QA lets an implementer build `compute_verdict` early, it becomes a rework issue rather than a missing deliverable. I keep it blocking because Task 3's own acceptance criterion cannot pass from Task 3's text.
- **F3 / C-003 is fixable with tmp_path scaffolding.** My calibrator scored it 0.55. It stays blocking only because the plan as written gives an implementer no instruction to build that scaffolding.
- **F12 / C-008 had wrong reasoning.** I wrote "section 3 omits it", but plan:19 includes section 4. My conclusion (minor) stands for a different reason: it is an install-time action, and the plan installs nothing.
- **V3's test-hygiene findings are real, and V1 missed them:** C-014, C-015, C-016, C-020.
- **V2's QA-002 (C-009) is a real gap V1 missed.**
- **V3's drift count is probably more correct than mine.** If C-018 is accepted as drift, the plan has three deviations, and V1 counted only two.

## Per-point positions

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

## Shared assumptions

- **A-001: QUALIFY.** Reading ahead is fair when later tasks only fix names in advance (C-001, C-007). It is not fair when a task's own acceptance criterion cannot pass without code a later task builds (C-002), because /sc:implement gates QA per task.
- **A-002: ACCEPT, narrowed.** The dated owner rulings at plan:21-24 outrank source.md text, and source.md section 7 defers to the owner. The plan's own scope additions without a ruling, such as the C-018 templates, do not inherit that authority.
- **A-003: QUALIFY.** I verified that the inputs exist today: the ctl-r1 review and spec history files, the S1 `task-text/` folder holding T05 to T10, and `/tmp/impl/exp/s1/`. Tasks 7 and 14 also stop as blocked on a missing file or a sha256 mismatch (plan:96, plan:182). Their absence at execution time would therefore block the run, not produce a wrong deliverable. `/tmp` remains the fragile input.
