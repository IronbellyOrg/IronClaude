# Round 1 advocate statement: Variant 1 (reviewer-1 card, sonnet, analyzer)

Paths: plan = /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P2/.dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/TASK-WF-writeTheP2Static-20261107-011441.md; spec = .dev/orca-command-refactor/specs/orca-worker-contract-spec.md. I re-read the plan (lines 20-122, 225-373), spec 138-187, source.md, and the cited skill and command anchors before relying on any claim below.

## Position summary

Variant 1 is the most even-handed card on classification and has the best "drift inside a converted gate" findings (R1-F3, R1-F2), but it is not the best card overall. It missed the single P1 that only a nested-call sweep finds (R3-F1), and it missed the F1/WC-4 coverage gap. The calibrator's 0.70 is fair. My position: the final merged finding list should take V3 as the spine (coverage, verified_ok, nested-call sweep), V2 for gate-semantics strength and the severity of the cli-eval gap, and V1 for three things only V1 found or framed correctly: the task-builder CLI-mode `--fix --promote` gap (R1-F3), the per-gate phrase gaps by task (R1-F10), and the differentiated deviation classes (corrected, see C-008).

## Steelman (V2, V3)

V2 strongest argument: a review of a plan whose whole safety value is "one assertion per gate" must test whether the assertions can actually fail when a gate's outcome is reversed. R2-F2 does this. Task 20 (plan:345) says `P2_GATES` phrases are "taken from the entries Tasks 2 to 16 added", and those entries are labels (plan:97 pins `Approval Required` and `not applied` as separate tokens; Task 8's `blocked_question`). That is the same failure mode as P1's "single token a clause can contain while saying the opposite" (plan:27). V2 is also the only card to call the cli-eval gap P1, which the calibrator accepts ("P1 fits"). V2 also found that Task 21's commit-path group list (plan:367) has no `.dev/tasks` group even though source.md:16 asks for "the exact list of paths for the owner-approved commit". V2 is compact: 5 findings, all confirmed by the calibrator (0.78), highest precision of the three.

V3 strongest argument: a converted command's nested calls must all follow the nested rule, including calls the spec row does not name. plan:26 says a nested call to a command that accepts `--unattended` at P2 passes the flag and `nested/<command>-<n>/`. I confirmed three misses: tasklist Stage 9 invokes `sc:task` via Skill and loops back to it (sc-tasklist-protocol/SKILL.md:1535-1557, 1607), while Task 16 nests only reflect (plan:290) and Task 12 gives `task` the flag; release-split Part 4 "Skill `sc:analyze` or inline verification" (SKILL.md:324) is unhandled by Task 8; reflect Wave 1B's optional `tech-research` (SKILL.md:632) is unhandled by Task 15. V3 also supplies `verified_ok`, the only negative evidence in any card, so a reader can see what was checked and found clean. 14 findings, calibrated 0.79, the highest.

## Strengths claimed (V1)

1. R1-F3 (U-004) is real and unique. Task 14 (plan:261) says only that "the CLI-mode reflect gate's staging step is not run". I confirmed task-builder/SKILL.md:1082: CLI mode emits the shell-out `superclaude reflect run ${TASK_FILE} --depth deep --fix --promote` behind a skip guard. `--fix` edits files and `--promote` moves task folders, which is exactly what WC-9/SA-1 forbid under `--unattended`. The plan leaves that call undefined. Calibrator: confirmed. No other card saw it.
2. R1-F2 identifies the cli-eval gap with the concrete remedy (name the safety flags, add their phrase to the entry, settle FR-G5/`--no-pty` or record as owner decision). I confirmed plan:248 blocks only a missing `--suite` and says "the run flags the brief passes are the confirmed invocation", while spec:164 says "`--suite` and the safety flags in the brief, else blocked". Calibrator: confirmed, "P1 defensible".
3. R1-F4 (U-005): plan:136 (Task 5) makes `--mode socratic` write questions and not wait; spec:162 shows the P1 precedent (business-panel refuses socratic because waiting is UNVERIFIED), spec-panel.md:123 documents the mode with no statement that it does not wait. grep shows the plan has exactly one mention. An unrecorded decision that departs from the P1 precedent. Calibrator: confirmed.
4. R1-F1 and R3-F3 agree on the stale workflow.md:72 clause (I re-read it: "each file the reflect step wrote in its `.dev/reflect/` run directory"), with V1 adding `refs/return-contract.md`, which Task 17 states "stays" (plan:303).
5. R1-F10 correctly traces which gates lack their own phrase (Tasks 5, 13, 16): the specific input for the AC-2.1 "one assertion per gate" requirement.
6. R1-F7 answers the Tier-1 question T1-F4 with a measured result (no code reader of `reflect-pre`), and R1-F5 shows the D-P2-1 skip is spec-compliant.
7. Honest self_audit listing exactly which skill files were not read.

## Weaknesses identified in others

V2:
- Only 5 findings; no finding about any nested call (misses the A-003 class entirely), no F1 finding about the stale workflow clause, no per-task phrase gaps for the gates other than cleanup/release-split.
- Self-confidence 0.94 against a calibrated 0.78: it overstated. R2-F3 claims the matrix overstates pinned tasks; calibrator corrects the real count to 2, and R2-F3 is a coverage-matrix defect as much as a plan defect.
- R2-F5 is a gap in the reflect run's own coverage matrix, not plan drift; filing it as a plan finding misattributes it (calibrator: "matrix gap, not plan drift").
- R2-F4 overstates: plan:371 already requires `git diff --cached --name-only -- .dev/tasks` to list the package's files; what is missing is the group in the report list (plan:367), a P3.
- R2-F1's fix ("identify safety inputs from the fresh digest") cannot be done by a static plan: the digest is loaded at run time by the eval-docs-loader agent. A static fix must name the flags in the plan (see A-001).
- Every finding "Drift": no differentiation.

V3:
- R3-F13 is wrong on its own example: plan:372 limits the equality to `-- src tests plugins`, so an unrelated `.dev/reflect` folder cannot fail it (calibrator agrees). The residual fragility (pre-existing dirty files in those three trees) is real but unproven.
- R3-F1's harm is overstated ("commit/push"): the actual harm is the attended `sc:task` prompts gating an unattended run (calibrator).
- R3-F2 covers the same gap as C-001 but rates it only P2 while its own self_audit says a reader could argue otherwise; the card does not settle severity (and, like R1-F2, over-reads FR-G5/`--no-pty` as unresolved).
- R3-F6 is half-wrong: the stated reason is still true for the `task` handoff (calibrator).
- R3-F12's second half (skill name) is already recorded in D-P2-1 (plan:46).
- R3-F14 and R3-F10 are tidy but P3 filler; 8 of 14 findings are P3.
- All findings "drift", including R3-F9 which the calibrator calls "an observation, not a spec deviation".

## Concessions

1. I missed R3-F1, a real P1. I read tasklist SKILL.md 1590-1650 only (Stage 10.5) because spec:182 names only that stage, and I applied the spec row as the boundary rather than plan:26's rule. Stage 9 invokes `sc:task` through Skill at SKILL.md:1539 and 1607, and the same file lists `Skill` for "Invoke sc:task" at 1776. I also did not read release-split or the reflect Wave 1B text (my self_audit admitted release-split was unread). V3's three nested-call findings are correct.
2. I made no finding about `left out (WC-4)` coverage (C-003), although T1-F1 was the first Tier-1 item. V2 and V3 are right; the real number pinned is 2 (plan:97, plan:110).
3. R1-F6 misreads D-P2-13: plan:58 already maps both HALTs to blocked, and the High/Medium HALT at SKILL.md:1608 is Stage 10, not 10.5. Only the `depth-map.yaml` question (SKILL.md:1641) survives.
4. R1-F9 duplicates plan:45, which already records every one of those decisions "for owner approval". Dropped.
5. R1-F8 is partly handled by plan:42 ("no classified line is edited"); the risk is the wording "added sentence", not the rule.
6. I used "none" as a deviation class on R1-F7, R1-F8, R1-F10 and "authorized" on R1-F9. The taxonomy has four classes (authorized expansion, necessary deviation, drift, regression); "none" is not one, and a plan-made decision is not "authorized" until the owner approves it. This weakens my differentiation claim.
7. I rated the cli-eval gap P2; V2's P1 is better supported (see X-001).
8. R1-F2's FR-G5/`--no-pty` clause is half-weak: Task 13 replacing W3 with "the command line as given" implicitly resolves both (calibrator, on R3-F2). The safety-flag "else blocked" is the real gap.

## Diff-point positions

| Point | Superior | One-line reason |
|---|---|---|
| S-001 sections | V3 | `verified_ok` is the only negative evidence and lets the orchestrator skip re-checking dependency chains and mirrors. |
| S-002 count/granularity | merge (V3 spine) | V3's coverage with V2's precision; V1's per-gate granularity in R1-F10 is worth keeping; V2's 5 findings leave whole classes unexamined. |
| S-003 evidence form | V2 | Full repo paths with line numbers verify without a legend; `plan:N` shorthand is acceptable only if the legend is carried (V1/V3 both did). Low stakes. |
| C-001 cli-eval | merge | V2's severity (P1), V1/V3's remedy: name the flag set (SKILL.md:138-139), blocked resolution, own phrase, FR-G5/`--no-pty` as an owner note only. |
| C-002 workflow.md:72 | merge (V3 spine) | V3 adds the test pin at 837-844; V1 adds `refs/return-contract.md`; V2 missed it. |
| C-003 F1 WC-4 coverage | V2 (form from V3) | V2 lists the five clauses to test (run-written files, named exclusions, WC-4 pointer, absence of the repeated reason, conditional sentence); V3's single parametrized test is the right shape; V1 silent. |
| C-004 label vs resolution | merge | V2 gets the semantic point (join condition to outcome, negative reversal case); V1 gets the per-task gap list (Tasks 5, 13, 16). |
| C-005 Task 21 list | V2 | V2's group-list omission is real (plan:367 has no `.dev/tasks` group); V3's example is wrong (plan:372 scoped), keep only the baseline-compare suggestion as optional. |
| C-006 D-P2-1 | V3 | R3-F12's path mismatch (`enrichment/research-light.md` vs `claudedocs/research_*`, research.md:103, spec:176) is a concrete defect; V1's alternative is already an owner option via source.md:12. |
| C-007 collisions | merge | R3-F8 is a hard Check ADDITIVE failure if line 44 is edited; R1-F8 is wording risk; both need the same "new line after" wording fix. |
| C-008 classification | merge | Differentiated classes are right in principle (D-P2-1 skip is "necessary", R3-F9 is not a deviation) but V1 misused "none"/"authorized"; use the four taxonomy classes only. |
| X-001 severity | V2 | P1: a gate resolution the spec states as "else blocked" is dropped, leaving the unattended run to launch with unchecked flags; needs an owner decision on the flag set. |
| X-002 class | V3 (drift) | The stale clause comes from the plan's own one-line cap (A-002), so it is plan drift, not a deviation forced on the plan; V1's "necessary" is a stretch. |

## Shared assumptions

- A-001: QUALIFY. The diff-analysis states that none of the run options is "labelled safety flag". That is wrong: sc-cli-eval-protocol/SKILL.md:138-139 says "the safety flags from the digest (`--no-pty`, `--no-mcp`, `--json`, `--junit`, `--timeout-mult`, `--keep-home`, `--max-disk-mb`, `--output-dir`)", and cli-eval.md:27 uses "safety flags" too. So the set is nameable. What is genuinely unstated: which of them the brief must pass, since "from the digest" means the digest decides at run time, and spec:164 says only "the safety flags in the brief". A static plan cannot read a digest, so it must either name a required subset or treat the whole W3 list as the brief's inventory. The assumption holds for naming, fails for the required subset: this is an owner decision.
- A-002: QUALIFY. The one-deleted-line cap is the plan's own reading (plan:41, "the only two command files exempt"), not a spec sentence: the spec names AC-C5/SA-4 (spec:380) but its P2 workflow/brainstorm rows (spec:142, 152) require changing the existing P1 reflect/research lines, which already forces at least one deleted line each. The cap is therefore fixed only for as long as the owner does not widen it. The fixes for R3-F3 and R3-F6 can stay additive (a new line after), so the assumption is workable for R3-F3; but for line 72 an additive line leaves two contradictory clauses, so widening to two lines is a legitimate owner option, not a prohibited one.
- A-003: ACCEPT. plan:26 states the rule for "a nested call to a command that accepts `--unattended` at P2" without limiting it to calls a spec row names. I confirmed tasklist Stage 9 (`sc:task` via Skill, SKILL.md:1539, 1607), release-split Part 4 (SKILL.md:324) and reflect Wave 1B (SKILL.md:632) are such calls or the same-case skip. The rule needs a decision per callee: `sc:task` and `sc:analyze` accept the flag at P2 so get nested directories; `tech-research` does not, so the plan:26 skip-and-record default applies and Task 15 must say so.

## Unique contributions

| # | Verdict | One line |
|---|---|---|
| U-001 | keep (P1) | Confirmed against SKILL.md:1535-1557 and plan:26; harm wording should say attended prompts, not commit/push. |
| U-002 | keep | Part 4 "Skill `sc:analyze` or inline verification" confirmed; resolve as inline verification or nested analyze. |
| U-003 | keep | Wave 1B `tech-research` confirmed at SKILL.md:632; settle by the plan:26 skip-and-record rule. |
| U-004 | keep | Confirmed: task-builder SKILL.md:1082 emits `reflect run --depth deep --fix --promote` in CLI mode; plan:261 skips only staging. |
| U-005 | keep | Plan has one socratic mention (Task 5); record as an owner decision or refuse as P1 did. |
| U-006 | correct | Drop the HALT-mapping claim (plan:58 already covers both); keep only where `depth-map.yaml` goes under `--unattended`. |
| U-007 | keep | Cheap AC addition (grep `reflect-pre` over src and tests) to Task 16. |
| U-008 | drop | plan:45 already records every decision for owner approval. |
| U-009 | keep as note | A coverage-matrix gap in the reflect run, not plan drift; do not file against the plan. |
| U-010 | correct | Stale only for the tasklist handoff; still true for the task handoff. |
| U-011 | correct | Task 3 does name improve's anchors; only the Safety Threshold clause lacks a target. |
| U-012 | keep as observation | Not a spec deviation; a Write line plus a parallel test to `explain` is a cheap P1-precedent match. |
| U-013 | keep | Trivial baseline-list fix, real (plan:73 vs Task 6). |
| U-014 | keep | Duplicate of T1-F2; remove the instruction or state its target. |
| U-015 | keep | Negative evidence belongs in the merged result. |
