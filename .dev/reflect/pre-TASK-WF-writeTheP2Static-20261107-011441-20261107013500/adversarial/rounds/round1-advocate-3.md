# Round 1: Advocate for Variant 3 (reviewer-3 card, opus slot, refactorer persona)

Conventions: "plan:N" = line N of the P2 static plan; "spec:N" = line N of `orca-worker-contract-spec.md`; other paths are repo-relative to `OrcaCLICommandRefactor-P2`. Every citation below was re-read in this round.

## Position summary

Variant 3 is the strongest base for the merged card because it is the only card that checks the plan's nested-call coverage end to end. It finds three nested calls that the plan leaves unhandled: tasklist Stage 9 `sc:task` (R3-F1, P1), release-split Part 4 `sc:analyze` (R3-F4) and reflect Wave 1B `tech-research` (R3-F5). It also records six verified negatives (`verified_ok`), so the merge knows what not to re-check. Its calibrated score is the highest of the three (0.79 against 0.78 and 0.70), and so are its coverage (0.80) and actionability (0.85) scores. It has three real weaknesses. Its deviation classes are uniform: every finding is marked "drift". It overstates several findings (R3-F1 harm, R3-F2, R3-F3, R3-F6, R3-F7, R3-F12, R3-F13). It also misses two gaps the other cards found: V1's task-builder CLI gate (U-004) and V2's gate-assertion strength (C-004). The merged card should take V3 as its base, use V2's severity and assertion rules and V1's classification practice, and add U-004.

## Steelman

**V1 (analyzer, sonnet).** Its strongest argument is judgement. It is the only card that uses deviation classes with discrimination (necessary, drift, authorized, none), so the owner can see which findings are real departures from the spec. Its unique R1-F3 (U-004) is a genuine WC-9 hole that both other cards missed. I verified it: `src/superclaude/skills/task-builder/SKILL.md:2237` shows that the CLI-mode gate runs `git add -A` and then `superclaude reflect run {TASK_FILE} --depth deep --fix --promote`. Task 14 (plan:261) skips only "the CLI-mode reflect gate's staging step", so the `--fix` mutation and the `--promote` folder move stay undefined under `--unattended`. R1-F4 correctly points out that plan:136 has spec-panel `--mode socratic` "not wait". That decision is not recorded, even though business-panel's precedent (spec:162) refuses the mode because whether it waits is UNVERIFIED. R1-F7 closes an open Tier-1 question with grep evidence. V1 also sees the one point V3 frames too narrowly: the stale clause in workflow.md:72 needs an AC that checks it agrees with the new line 75.

**V2 (qa, haiku).** Its strongest argument is precision. With five findings it reaches 0.92 citation grounding, the best of the three, and it takes the right hard line on the cli-eval gate. Spec:164 names an "else blocked" that plan:248 and plan:60 (D-P2-15) drop, and the calibrator says "P1 fits". V2 alone sees the test-strength problem (C-004, R2-F2). A phrase list that pins a label such as "Approval Required" or `blocked_question` still passes when the resolution is reversed. AC-2.1 asks for assertions that state gate resolutions, so this matters more than any single missing phrase. R2-F4 is a real report defect. The repo-path AC at plan:372 is scoped to `src tests plugins`, but plan:367 stages the package under `.dev/tasks`, so the commit-path list the brief asks for is incomplete. R2-F3 also corrects the coverage matrix's overstated count of commands that pin "left out (WC-4)": the matrix claims 5 of 15, and the real number is 2.

## Strengths claimed (Variant 3)

1. **R3-F1, the only P1 finding on nested coverage (U-001). Confirmed.** `src/superclaude/skills/sc-tasklist-protocol/SKILL.md:1535-1557` has Stage 9 "Invoke `sc:task` via the `Skill` tool" with `--compliance strict`, and line 1557 and line 1607 loop back to it. Plan:26 requires every nested call to a command that accepts `--unattended` at P2 to pass the flag and a nested directory. Spec:62 states the same rule for any command "that invokes another `/sc:` command or protocol skill, through the Skill tool or the Agent tool". Task 12 (plan:233) gives `task` the flag, yet Task 16 (plan:290) nests only the Stage 10.5 reflect call. Task 20's literal `"tasklist": ["reflect"]` (plan:345) would lock the gap into the tests. Plan:233 shows that a STRICT `sc:task` run also invokes `sc:impact-protocol`, so an attended nested task would write outside the report directory as well as reach its confidence, TFEP and FULL STOP prompts.
2. **R3-F4 and R3-F5 (U-002, U-003). Confirmed.** `sc-release-split-protocol/SKILL.md:324` says "Invoke appropriate analysis (Skill `sc:analyze` or inline verification)", and Task 8 (plan:179) nests only brainstorm and adversarial. `sc-reflect-protocol/SKILL.md:632` lists `tech-research` for "Wave 1B (optional, `--depth deep` only)". Task 15 (plan:276) settles the MDTM `task-builder` route but not this step, although plan:26 names `tech-research` as a callee that must be made gate-free or skipped and recorded.
3. **R3-F8 (C-007). Confirmed.** Plan:233 says to add the flags "to the flag list line and the flag table (the existing lines are not reworded; add new lines)". The flag list is the single line `Key flags: ...` in `src/superclaude/commands/task.md`. Adding to it changes the line, which Check ADDITIVE (plan:41) counts as a deletion. The instruction contradicts itself.
4. **R3-F14 (U-014). Confirmed.** Plan:78 says to "drop only the case that relied on equality for an extra P2-shaped key". The existing cases at `tests/skills/test_worker_contract.py:1004-1012` (a missing P1 name, an `extra` key, a repeated name, `without_test`, `extra={}`) all still fail under the subset rule, so the instruction has no target.
5. **R3-F11 (C-003)** gives the most executable fix for F1: one parametrized test over all 15 commands, run on the text after the first backticked `artifacts`. This matches the rule at plan:27 that text read by `_artifacts_clause` sits after that key.
6. **`verified_ok` (S-001, U-015).** This is the only negative evidence in any card. It covers the dependency chains, the 11 `deferred:P2` entries, the `EXPECTED_NESTING` edits, the mirror rule and the auggie options. It stops the merged card from re-raising settled items.

## Weaknesses identified in others

- **V1.** R1-F6 misreads the plan. Plan:58 (D-P2-13) already maps both HALTs to blocked, and the High/Medium HALT at `sc-tasklist-protocol/SKILL.md:1608` belongs to Stage 10, not Stage 10.5. Only the `depth-map.yaml` point (SKILL.md:1641) survives. R1-F9 asks for an owner-approval table that plan:45 and plan:367 already require (D-P2-1 to D-P2-17 "for owner approval"). Plan:42 already forbids editing classified lines, which partly covers R1-F8. V1 read tasklist SKILL.md 1590-1650 but not Stage 9 at 1535-1557, so it missed U-001. Its self-audit admits it did not open the release-split file, which is where U-002 lives. The labels "authorized" and "none" are not the taxonomy names ("Authorized expansion", "Necessary deviation", "Drift", "Regression").
- **V2.** It has the largest overconfidence: a self-score of 0.94 against a calibrated 0.78. Every finding is marked "Drift", which is the same weakness V3 has. It raises no nested-call coverage findings (U-001 to U-004 are all absent), and that is the plan's main structural risk at P2. R2-F5 is a gap in the reflect run's own coverage matrix, not drift in the plan (calibrator). It is silent on C-002, the stale workflow.md:72 clause.
- **diff-analysis A-001** is factually wrong. `src/superclaude/skills/sc-cli-eval-protocol/SKILL.md:137-139` reads "the safety flags from the digest (`--no-pty`, `--no-mcp`, `--json`, `--junit`, `--timeout-mult`, `--keep-home`, `--max-disk-mb`, `--output-dir`)". The set is labelled; what is missing is a required subset (see A-001 below).

## Concessions

1. **R3-F1's harm is overstated** (calibrator). Commit and push are EXEMPT-tier operations (spec:181), and Stage 9 runs at `--compliance strict`. The real harm is that `sc:task`'s confidence prompt below 0.70, its TFEP "present to user" step, its FULL STOP and its attended STRICT impact path would gate or escape an unattended run. Commit and push should be dropped from the claim.
2. **R3-F2 is partly settled.** Plan:248 makes "the run flags the brief passes" the confirmed invocation, which settles `--no-pty`, and it implicitly removes the FR-G5 offer. The real gap is the safety-flag "else blocked", which V1 and V2 state equally well.
3. **R3-F3 overstates the test-pin update.** `tests/skills/test_worker_contract.py:837-844` pins "reflect", "deviation-patterns", "runs.jsonl", "left out" and "WC-4", not the `.dev/reflect/` path. An added line would leave the pin green. The fix only needs to keep those tokens in the clause.
4. **R3-F6 is partly wrong.** The brainstorm "do not accept the flag at this phase" reason (`brainstorm.md:158`, `sc-brainstorm-protocol/SKILL.md:352`) becomes false only for the `tasklist` handoff after Task 16. It stays true for the `task` handoff.
5. **R3-F7 is partly wrong.** Plan:110 does name improve's anchors ("Approval Required", "Explicitly Will NOT"). Only D-P2-8's "Safety Threshold" clause has no target: `improve.md:113-128` has no Safety Threshold section.
6. **R3-F12's second half duplicates the plan.** Plan:46 (D-P2-1) already records the missing `sc-research-protocol` skill. Only the output-path mismatch stands.
7. **R3-F13 is weaker than stated.** The AC at plan:372 is scoped to `src tests plugins`, so `.dev/reflect` folders cannot fail it. `git status --short --untracked-files=all -- src tests plugins` in the P2 worktree prints nothing today, so the risk is theoretical. V2's R2-F4 is the real defect at this AC.
8. **Uniform "drift" classification.** Marking R3-F9 (an observation), R3-F10 (a baseline omission) and R3-F14 (a confirmation) as drift loses information. V1's practice is better.
9. **Missed findings.** V3 missed U-004 (the task-builder CLI gate's `--fix --promote`) and C-004 (assertion strength). Both belong in the merged card.
10. **C-001 severity.** P1 is the better severity, because spec:164 names a blocked outcome that the plan drops.

## Diff-point positions

| Point | Superior | Reason |
|---|---|---|
| S-001 | V3 | Only V3 records verified negatives (`verified_ok`), which stop the merged card from re-raising settled items. |
| S-002 | V3 | Most coverage (14 findings, coverage 0.80) at equal calibrated quality; V2's five findings are precise but miss the nested-call class. |
| S-003 | V2 | Full repo paths with line numbers are the least ambiguous; the plan:N shorthand depends on the prompt's definition. |
| C-001 | merge | V2's P1 severity and its separate missing-suite and missing-safety-flag assertions, plus V3's owner-decision fallback, because the spec never defines a required safety-flag set. Drop V3's FR-G5 and `--no-pty` part (settled by plan:248). |
| C-002 | merge | V1's fix (an added line plus an AC that lines 72 and 75 agree, and the same for refs/return-contract.md) with V3's drift class; drop V3's "update the 837-844 pin". |
| C-003 | merge | V2's scope (assign the local report sentence, correct the matrix count) with V3's single parametrized test over all 15 commands. |
| C-004 | V2 | Only V2 demands phrases that join condition to outcome, plus negative cases that reverse the outcome; V3 is silent. |
| C-005 | V2 | R2-F4 finds the real defect (the commit list leaves out the staged `.dev/tasks` package); V3's R3-F13 concern cannot fire under the AC's path scope. |
| C-006 | V3 | R3-F12 is a correctness gap: brainstorm's table expects `enrichment/research-light.md` (SKILL.md:189), but `/sc:research` writes `claudedocs/research_*` (research.md:103). The fix: read `report_path` from the nested contract. V1's point is an owner preference. |
| C-007 | merge | Both instances are valid and distinct: V3's task.md flag-list line (confirmed) and V1's "added sentence" wording at classified lines (partly covered by plan:42). |
| C-008 | V1 | V1 alone tells real departures from observations; map its labels to the taxonomy names. |
| X-001 | V2 | P1: spec:164's "else blocked" is dropped outright, and all three calibrations call P1 fitting or defensible. |
| X-002 | V3 | Drift: the plan did not decide the stale clause, it overlooked it. A "necessary deviation" needs a deliberate, constrained departure, and an additive fix is available without one. |

## Shared assumptions

- **A-001: QUALIFY.** The premise that no flag is labelled a safety flag is false. `sc-cli-eval-protocol/SKILL.md:137-139` names "the safety flags from the digest" and lists eight of them. But every one of them is optional at the CLI, and spec:164 does not say which must appear in a brief before `run` proceeds. So the set can be named, but a required subset cannot be derived. The merged finding must state the gate as an owner decision: for example, "blocked unless the brief states its value or absence for each listed safety flag". A plan-only fix is not enough.
- **A-002: QUALIFY.** The one-deleted-line budget comes from the plan (plan:41), not from the spec. SA-4 (spec:211) allows existing-line changes "where section 3 names a defect fix", including "workflow contract gaps", and the workflow row (spec:152) names the P2 reflect-step change. So the owner can widen the budget. The assumption is not load-bearing, though. Both C-002 fixes can be made with an added line that needs no extra exemption. Only U-010 (the brainstorm handoff reason) might need a reworded line, and even there an added post-P2 line works.
- **A-003: ACCEPT, reclassified from UNSTATED to STATED.** Spec:62 states the rule generally: "a command that invokes another `/sc:` command or protocol skill, through the Skill tool or the Agent tool, passes `--unattended` when the invoked command accepts it ... or the caller skips it under `--unattended` and records the skip". It adds that "each command's `## Unattended mode` section names its nested invocations". Spec:60 confirms that nested calls are governed by this rule. The plan restates it as its own constraint (plan:26). So it binds tasklist Stage 9, release-split Part 4 and reflect Wave 1B even though their section 3 rows do not name them. The rows describe gate resolutions; they do not list every nested call exhaustively.

## Unique contributions

| # | Verdict | Reason |
|---|---|---|
| U-001 | keep (correct) | Confirmed at tasklist SKILL.md:1535-1557 and 1607; keep P1, but replace the commit/push harm with task's confidence, TFEP and FULL STOP prompts and its attended STRICT impact path. |
| U-002 | keep | release-split SKILL.md:324 names Skill `sc:analyze` or inline verification; Task 8 must choose one under `--unattended`. |
| U-003 | keep | reflect SKILL.md:632 `tech-research` in Wave 1B has no resolution; skip it and record it, as D-P2-1 does. |
| U-004 | keep | Verified at task-builder SKILL.md:2237: the gate runs `git add -A`, then `reflect run --fix --promote`; skipping only the staging leaves a mutation and a folder move undefined (High). |
| U-005 | keep | Plan:136 decides that socratic mode "does not wait" against the business-panel refusal precedent (spec:162) with no recorded decision. |
| U-006 | correct | Drop "D-P2-13 covers only the move" (plan:58 records both HALTs); keep the `depth-map.yaml` location point (SKILL.md:1641). |
| U-007 | keep | A cheap `reflect-pre` grep AC for Task 16; low value but no cost. |
| U-008 | drop | Plan:45 and plan:367 already list D-P2-1 to D-P2-17 for owner approval. |
| U-009 | keep (reclassify) | Valid as a reflect-internal gap in the coverage matrix, not as drift in the plan. |
| U-010 | correct | The reason is stale only for the `tasklist` handoff; still true for `task`. |
| U-011 | correct | Narrow it to D-P2-8's "Safety Threshold" clause, which has no improve section (improve.md:113-128). |
| U-012 | keep (observation) | `cleanup.md` and `improve.md` list no Write tool, against the P1 explain precedent (test_worker_contract.py:847); this is not a spec deviation. |
| U-013 | keep | The baseline at plan:73 omits `test_sc_recommend_routing_contract.py`, which Task 6 edits (plan:149). |
| U-014 | keep | Verified: plan:78's "drop only the case" has no matching case at test_worker_contract.py:1004-1012. |
| U-015 | keep | The only negative evidence in any card; it saves re-verification in later rounds. |
