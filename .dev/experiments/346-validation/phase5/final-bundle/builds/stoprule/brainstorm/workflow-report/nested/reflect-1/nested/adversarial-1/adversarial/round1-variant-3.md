# Round 1 statement: Variant 3 (reviewer-3, refactorer persona)

## Position summary

V3 is the most complete map of where the plan's text lets the final deliverables disagree with the spec or with each other. It alone covers the test-harness layer: the equality test that locks in the Usage-line contradiction, the git-tracked sweep that runs before staging, omitted suites, the stale allow-list comment and missing positive wording checks. V3 is weaker than V1 on task ordering and inside-the-script gaps, and weaker on mapping deviations to ids. I drop the blocking label on R3-1. I keep it, narrowly, on R3-2.

## Steelman

**V1 (analyzer).** Strongest argument: V1 is the only card that walked the dependency chain through the script tasks. Task 3's acceptance (plan:60) needs `begin` to exit 5 on a prior-verdict mismatch, but `compute_verdict` is only defined in Task 5 (plan:77). Task 5's label-count line is "built by the same function as Task 6's `count`" (plan:77), and Task 6 depends on Task 5 (plan:85). The replay in Task 7 (plan:96) cannot reach review 3 without a prior review-2 report that carries a sentinel, which `begin` requires (source.md:62). What V1 gets right: these are real, checkable defects that a per-task executor (`/sc:implement` checks each task against its own criteria) will hit. V1 also gets the deviation classification right: the Unattended removal is authorized (plan:21) and the routing-refresh edit is necessary (plan:135). Critique: V1 marks all three as blocking. Its own calibrator says they "fit major better than blocking" (variant-1:101), because an implementer who writes `compute_verdict` early, or builds a tmp_path prior report, still ends with the right files. V1 also misses the whole test-harness layer (C-014 to C-016, C-020).

**V2 (QA).** Strongest argument: QA-002 is a real, narrow correctness gap no one else found. The first-pass `form` line keeps `id` and `claimed` (plan:57) but not `prior`. Task 6's `m0_label_cm` counts claims "whose `prior` is null", plus claims present only in a `form` line (plan:87). So a withdrawn carried prior cannot be told apart from a withdrawn new finding. That breaks M0's rule "carried priors excluded" (source.md:173). What V2 gets right: it reads the owner-decision count against the ledger schema, which is exactly where a count bug would hide. Critique: QA-001 treats the measurement copy (source.md:163) as a missing repo deliverable. The plan installs nothing (plan:20), and section 4 describes it as an experiment-install step, so this is a hand-off note, not a missing file (calibrator 0.20, variant-2:38). V2's drift counts (2) ignore the two declared deviations its own calibrator flags (variant-2:41). V2 covers 2 findings against 12 and 12.

## Strengths claimed

1. **R3-1 finds the lock-in, not just the inconsistency.** spec-panel.md:23 advertises `[--unattended] [--report-dir <dir>] [--improve]`. `--report-dir` and `--improve` are defined only inside `## Unattended mode` (spec-panel.md:456, :459), and the grep shows those three lines are the only places either flag appears. Task 9 removes that section and states the variant does not accept `--unattended` (plan:123, plan:21). Task 10's equality test exempts only the name changes on Usage (plan:135), so a fix that drops the tokens would fail it. V1 F4 saw the token. Only V3 names all three orphaned flags with evidence and the equality-test trap (V1 put `--report-dir` in a calibrator note only, variant-1:103).
2. **R3-2 gives the only actionable rule for the counted-once case.** Source.md:128 requires "two claims on one prior counted once". No acceptance list contains it (plan:60, :71, :80, :90), and no task defines what "counted once" applies to. V3 names the three counters it must apply to: the verdict, D1..Dk renumbering and `m1_open_confirmed`. V1 F5 says only "add the case and the rule".
3. **R3-4 is a verified false-pass path.** `_files_under` filters `_tracked_text()` (test_review_severity_rule.py:54-56), which comes from `git ls-files` (lines 36-41). Task 10 (plan:140) and Task 12 (plan:161-165) run the suite before the new files are staged, so the banned-phrase sweeps (lines 450, 508) never see the new command, skill or agent. The tests pass locally and can fail after commit.
4. **R3-5 is grounded.** `test_tavily_tool_parity.py:31-34` rglobs every agent and skill `.md` for `tools|allowed-tools`, which covers the new `finding-grader.md` and `SKILL.md`. `test_retired_docs_absent.py:40` reads `docs/` and `src/superclaude` markdown. Task 12 runs `tests/skills tests/recommend tests/unit tests/core tests/commands` only (plan:165).
5. **R3-3: no positive check for the new FR-8/FR-9 wording, the bullet-7 suffix or the no-unattended sentence.** The equality test exempts exactly these blocks (plan:135), and Task 9's acceptance list (plan:126) does not name them. A variant missing them passes every listed check.
6. **R3-12 is verified.** The `_POST_REFRESH_ADDITIONS` comment (test_routing_refresh.py:29-32) lists the issues behind each addition. Plan:141 lets only the set line change, so the comment goes stale or the check fails.
7. **R3-10 is the one scope-drift finding.** The `offline-demotion-audit.md` and `replay-gate.md` templates (plan:184) implement section 5.3 and 5.1 procedures. Plan:19 excludes sections 5-7 except "the brief templates the install note lists", and that list is written by this same plan (Task 13, plan:172), so the carve-out is circular.

## Weaknesses identified in others

1. **V1 overstates three blocking labels.** For F1, F2 and F3 the final deliverable is correct once an implementer reorders the code or adds tmp_path scaffolding. Plan:96 forbids a synthetic substitute only for missing control-r1 files. Its own calibrator downgrades them (variant-1:101).
2. **V1 misses the harness layer.** V1 has nothing on C-014, C-015, C-016 or C-020, and these are where a passing plan ships a failing commit.
3. **V2 misreads scope on QA-001.** Plan:20 says nothing is installed, and source.md:163 sits in the install procedure. V1 F12 classifies it correctly: not a plan defect, only INSTALL.md's "differ only in lines from master" claim is unverified.
4. **V2's deviation classification is empty where it matters.** It records 0 authorized and 0 necessary, although plan:21 is an explicit owner ruling and plan:135 declares itself a necessary deviation.
5. **V2's coverage is too thin.** It audits 35 units, calls 33 adherent and reports 2 findings, but its own calibrator then lists three more unchecked spec items (variant-2:42-43). One of them is the counted-once case all three cards eventually touch.

## Concessions

- **R3-1 is minor, not blocking.** Spec 3.1 says "copy with exactly these edits", so keeping the Usage line is literally spec-compliant. The contradiction comes from the owner ruling, and no S1 brief passes `--unattended` (plan:21), so no measured run takes a wrong path. It still needs fixing in Task 9 and Task 10.
- **R3-11 is not a defect.** Source.md:124 lists the exact frontmatter keys without `category:`. The plan follows the spec. Confidence-calibrator's `category: analysis` is only pattern similarity.
- **R3-7 is ambiguous at most.** "equals the literal recorded in" (plan:135) most naturally means a constant in the test.
- **R3-9 is ordering awkwardness.** The file names are fixed in advance (plan:184). V1 F7 states the real gap more sharply: Task 14 never tells anyone to update INSTALL.md, yet requires it to list eleven files (plan:190).
- **V3's deviation counts are not tied to ids.** To map them now: authorized = the Unattended removal (plan:21), necessary = the `test_routing_refresh.py` edit (plan:135), drift = R3-10. V1's classification is superior on this point.
- **V3 missed V1's ordering defects (F1, F2), the replay prerequisite (F3), the `real:true` seeded-hunk gap (F9) and V2's withdrawn-prior gap (QA-002).**

## Per-point positions

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

## Shared assumptions

- **A-001: QUALIFY.** Blocking means the final deliverable is wrong or missing after all tasks are done as written. Reading ahead is allowed, so ordering defects (C-001, C-002) are minor. Behaviour the plan never defines (C-005) cannot be read ahead to, so it can still be blocking.
- **A-002: QUALIFY.** Owner rulings outrank source.md only on the points they actually address (plan:21-24). They do not authorize side effects they never mention, such as the orphaned Usage flags.
- **A-003: QUALIFY.** All four inputs exist today (ls on 2026-11-08: the `exp346-ab-ctl-r1/.dev/orca-command-refactor` folder, the `exp346-p1-logs` S1 `task-text` folder and both `/tmp/impl/exp/s1/filled-flg-r1-T0{7,9}.txt`). `/tmp` is volatile, though. Plan:96 and plan:182 stop as blocked on a missing file or a sha256 mismatch, so a missing input gives a blocked task, never a wrong deliverable.
