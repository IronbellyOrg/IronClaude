persona: refactorer
model_class: opus
model: claude-gw-tier1a[1m]
model_observed: claude-opus-class (Anthropic Claude, served as claude-gw-tier1a) (self-report of the reviewer; matches the pin)

`PLAN:n` = line n of the plan file; `SPEC:n` = line n of `merged-requirements.md`; `STAGE2:n` and `STAGE4:n` = line n of the stage 2 and stage 4 plans. Card text below is the reviewer's hand-back, saved verbatim (de-indented).

## Findings

**R3-F1**
- blocking: no
- claim: Task 14 can make Task 15's T2 test fail inside this same package. Task 14 adds a digest-version reader to `src/superclaude/cli/doctor.py`, which is already a tracked file, and nothing stops that reader from containing the literal fence text `review-severity:digest`. T2 scans tracked `src/` files and fails on any file that holds a fence opener but has no registry row. doctor.py will never have a row, because Task 6 fixes the registry at 19 rows. The result is that "passes with all `digest` rows at `legacy`" (PLAN:238) fails. An executor who then gives doctor.py a registry row breaks Task 6's count of 19. The stage 4 plan already expects this literal to be in doctor.py.
- evidence: PLAN:222, PLAN:234, PLAN:238, PLAN:113; SPEC:917 ("a fence opener and is not a registry row"); STAGE4:114 ("for example a string in `src/superclaude/cli/doctor.py`, which stage 1 extends"); doctor.py:17 (`run_doctor` exists, so the file is tracked).
- repair: In Task 14, build the marker from parts. Add the acceptance line `grep -n "review-severity:digest" src/superclaude/cli/doctor.py` prints nothing, valid until stage 4.

**R3-F2**
- blocking: no
- claim: Task 15 names the `STRICT_T2` constant but never says what turning it on changes, and no acceptance line shows the switch has any effect. The stage 4 plan assumes a specific meaning: with the switch on, a registered file that still holds the old sentence fails. Stage 4 also still says stage 1 "did not name the switch". A no-op constant would pass stage 1. Stage 4's case (b) would then fail on a file stage 4 did not write.
- evidence: PLAN:234, PLAN:236-242; STAGE4:114, STAGE4:119; SPEC:917 ("from stage 4, any legacy definition sentence remains").
- repair: Add to Task 15: "with `STRICT_T2` True, a registered file that holds the old sentence also fails". Add a temporary-tree case that shows both modes. Note for stage 4: drop its "did not name the switch" sentence.

**R3-F3**
- blocking: no
- claim: The key used to look up a scale-map row and the ledger's `origin` value do not match. Task 9 takes the family key "from the `origin` of the ledger row". The spec defines `origin` as a protocol name plus a finding id (for example `P3-006`), not a key such as `lens-scale`. No task maps protocol or agent names to family keys, and Task 12 never says where it gets the key. For tech-research rows, `ReviewerJudge` would therefore return UNSET every time, and Task 12's disagreement matrix would put every label in the unmapped column. Tests that pass the key directly would still go green. Stage 2 avoids the problem only by hard-coding the lens-scale row.
- evidence: PLAN:62 (the 12 keys), PLAN:151, PLAN:192; SPEC:353 (`origin`), SPEC:355 (`source` = reviewing agent and native label); STAGE2:57.
- repair: Task 3 adds a `reviewers` column (for example, `rf-qa`, `rf-qa-qualitative` → `lens-scale`). Tasks 9 and 12 resolve the family from the reviewing agent in `source`. Task 11 adds a case for an origin that does not match any key.

**R3-F4**
- blocking: no
- claim: This confirms T1-F4 and adds the spec text that settles most of it. T1-F4 says the spec only calls the label "information" (SPEC:737). But REQ-02 says the reviewer's own label is read through the scale map, "for example, an rf-qa IMPORTANT reads as blocking", and SPEC:744 says the same. Task 3 still gives no lens-scale outcomes. Stage 2 Task 2 takes every imported row's tier from that row, so an executor who writes `Conditional` would leave every row without a tier.
- evidence: SPEC:211, SPEC:744, SPEC:737; PLAN:62, PLAN:151; STAGE2:57.
- repair: Task 3 fixes `CRITICAL=Blocking;IMPORTANT=Blocking;MINOR=Medium`, cites REQ-02 for IMPORTANT, and states that MINOR=Medium is the plan's own choice.

**R3-F5**
- blocking: no
- claim: The new skill text is never checked against the repository-wide banned-phrase scans. `tests/skills/test_review_severity_rule.py` scans tracked `src/` files. The stage 1 files stay untracked (only `.dev/tasks` is staged), so the scan cannot see them during stage 1. The spec's REQ-30 pattern list contains the banned phrase "regardless of severity", and Task 3's L6 sentence could copy it. A failure would first show in stage 2's run of that test, and stage 2 is not allowed to edit stage 1 files.
- evidence: test_review_severity_rule.py:28, 36-51, 117, 172-176; SPEC:849; PLAN:66; STAGE2:88, STAGE2:102.
- repair: Add to Task 5 one acceptance grep of `BANNED_SEVERITY_PHRASES` and `SWEEP_PHRASES` over `src/superclaude/skills/sc-review-severity` that must print nothing.

**R3-F6**
- blocking: no
- claim: Some text in other stages describes stage 1 output in a way that will be wrong after stage 1 runs. Stage 2 says `__init__.py` "registers nine subcommand modules today"; it will hold ten once Task 12 adds `classify_cmd`. This is the same kind of stale quote as T1-F5 and STAGE2:27. Both are harmless because they say "today".
- evidence: `__init__.py`:19-29 (nine names); PLAN:192; STAGE2:57.
- repair: Optional: reword in stage 2.

Checked and found clean:
- Task numbers run 1 to 16 and every `Depends on:` points to a lower task. Task 8's mention of Task 9 is only a pattern reference, not a code dependency.
- Exactly 11 files hold the definition sentence, and they are the 11 `digest` rows. No plugin file holds it, and no file holds a fence today.
- Every allow-list path, `origin_repo.py`, `reuse-auditor`, `sc-bare-review`, the PF sketch files and the named tests exist. Stoprule and `finding-grader` are absent from `src/`, which matches their `installed-only` rows.
- The tasklist count is 9. The live subcommands are seven, including `verify-citations`.
- Stage 3 takes `rf-analyst.md` (its Task 9), and its scan reads the allow-list in Task 3's grammar.
- Brief decisions 1, 2, 4 and 5 are honoured at PLAN:24-26, 66, 82, 109, 124 and 248.

## Earlier findings check

- F1, M-F1: fixed, PLAN:129 (`--include='*.py' --exclude-dir=__pycache__`, "lists no file other than", end point at stage 2).
- F2, F3: fixed, PLAN:64, 66, 70.
- F4: fixed, PLAN:124, 248, 22.
- F5, M-F2: fixed, PLAN:62, 151, 234. The family-key source is still open; see R3-F3.
- F6, F7: fixed, PLAN:151, 164, 166, 204.
- F8, F9: fixed, PLAN:52, 82, 192.
- M-F3: fixed, PLAN:124 (`earlier_decisions`). T1-F1 confirmed: `pending` is an Offers state (SPEC:375), not an item state (SPEC:381-390).
- M-F4: fixed, PLAN:166.
- M-F5: fixed, PLAN:124, 192.
- M-F6: fixed, PLAN:137, 141.
- M-F7: fixed, PLAN:82, 90, 99-100, 115.
- M-F8: fixed, PLAN:36.
- M-F9, M-F10: fixed, PLAN:72 (count 9 verified), 151, 160, 173, 192, 200, 213.

## Verdict

PASS
confidence: 0.8
blocking ids: none. R3-F1 is the one most likely to stop the executor partway; it is cheap to fix before the run.

Files: `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md`, `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/tests/skills/test_review_severity_rule.py`, `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/to-do/TASK-WF-blockerStage4-20261116-030206/TASK-WF-blockerStage4-20261116-030206.md`

Not checked: whether the spec section 9.3 defining files exist for the eight scale-map rows the plan names only by family.

reviewer_model_self_report: claude-opus-class (Anthropic Claude, served as claude-gw-tier1a)

## Calibration (blind, opus class)
```yaml
calibrated_C: 0.77
per_dimension: {citation_grounding: 0.92, coverage_completeness: 0.80, deviation_classification_clarity: 0.35, risk_surface_coverage: 0.85, recommendation_actionability: 0.92}
verified_citations: 22 re-read, all held; STAGE2:57 not checked
blocking_grade_support: none marked blocking; R3-F1 may be graded too low
calibrator_model_class: opus
```
