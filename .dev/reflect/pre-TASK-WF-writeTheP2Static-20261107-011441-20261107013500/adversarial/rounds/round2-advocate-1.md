# Round 2 Rebuttal: Advocate for Variant 1 (reviewer-1 card, sonnet, analyzer)

Paths: `plan` = `.dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/TASK-WF-writeTheP2Static-20261107-011441.md`; `spec` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`; `D` = this debate directory. Repo-relative paths are under `src/superclaude/` unless stated.

Method: steelman first, then critique. Every new factual claim below was re-read in this round. Re-read this round: `skills/sc-tasklist-protocol/SKILL.md:1535-1557` and `:1598-1608`, `skills/sc-cli-eval-protocol/SKILL.md:124-155`, `skills/task-builder/SKILL.md:2225-2247`. Re-read earlier in the debate: plan tasks 1 and 12-21 and the Constraints, spec rows 2.1, WC-2..WC-13, 3.1 and 3.2, and `source.md`.

---

## Part 1. Response to Round 1 criticisms of Variant 1

### Conceded

1. **R3-F1 (tasklist Stage 9 `sc:task`) was missed by V1; V3 found it and it is a real P1.** `skills/sc-tasklist-protocol/SKILL.md:1539-1541` says Stage 9 invokes `sc:task` via the `Skill` tool with `--compliance strict`. `:1557` and `:1607` say the P2 loop-back re-delegates `sc:task --compliance strict` against a residual checklist. Task 12 (plan:233) gives `task` an `--unattended` flag. The plan's own nested rule (plan:26) and spec:62 say a caller passes the flag to every callee that accepts it at P2. Task 16 (plan:290) nests only reflect. V1 read the same tasklist skill and recorded only the HALT mapping (R1-F6). V1 stopped at spec row 182 ("Stage 10.5") instead of sweeping every nested call. That is the single largest coverage gap in V1.
2. **The F1 gap (C-003).** `source.md:7` asks each P2 command's `artifacts` clause to say "left out (WC-4)". V1 is silent; V2 (R2-F3) and V3 (R3-F11) both caught it. V1 concedes the omission. V1 also concedes that V1's self-audit did not list F1 among the brief lessons it checked.
3. **R1-F6 as written (tasklist HALT mappings) is partly wrong.** The calibrator was right: the plan records both HALTs. Only the `depth-map.yaml` location observation survives (see Part 5).
4. **R1-F9 (single owner-approval table)** duplicates what plan:45 already records. Drop.
5. **R1-F8 overreach.** The claim that an "added sentence" at WRITE_VERB-classified lines changes keys applies to the Task 10, 14 and 15 wording only as a wording risk, not as a check failure. V1 over-stated it as a collision. Keep as P3 wording advice at most (C-007 merge, below).
6. **Deviation classes.** V1's "none" and "authorized" classes were generous. A finding that asks the plan to change is, at best, a necessary deviation or drift. V1 concedes the calibrator's point that "none"/"authorized" on a finding that asks for a change is a category error.
7. **Severity of C-001.** V1's P2 was too low. The calibrator said P1 was defensible. See X-001.
8. **The FR-G5 / `--no-pty` half of R1-F2.** V1 asked the plan to settle both. That is an owner decision (spec:164 names no flag), so V1 should have asked for the decision to be recorded, not for the plan to settle it. V3's wording ("or record as an owner decision") is the better remedy.

### Countered (with evidence)

1. **U-004 / R1-F3 stands and is strengthened.** Task 14 (plan:261) skips only the CLI-mode gate's staging step. The gate's Action (`skills/task-builder/SKILL.md:2237`) has two parts: `git add -A` and then the `superclaude reflect run {TASK_FILE} --depth deep --fix --promote` shell-out. `--fix` applies edits and `--promote` lets the `task` adapter move the task directory to `done/` (`:2237`). Under `--unattended` the second half is also an outward action (a move, and a fix loop that edits). Spec:77 names the same CLI-mode `git add -A` at `task-builder/SKILL.md:2237` as refused under WC-9; the plan resolves only that half. No Round 1 advocate disputed the point.
2. **U-005 / R1-F4 stands.** P1 recorded a refusal for business-panel. spec-panel `--mode socratic` "does not wait" is an unrecorded decision of the same kind. P3 is right.
3. **The R1-F10 per-gate phrase gaps stand (C-004).** V2's R2-F2 is the stronger statement of the principle (phrases must join condition to outcome, with negative tests). V1's contribution is the concrete task list: Tasks 5, 13 and 16 lack a per-gate phrase. The two compose; neither displaces the other.
4. **Differentiated classification (C-008) is a method point in V1's favour.** V2 and V3 label every finding Drift. The brief for the taxonomy has four classes; a finding about the plan's own wording versus a finding about the plan departing from the spec are different things. V1's mistake was the "none"/"authorized" labels, not the differentiation.
5. **R1-F1 / C-002: V1 is right that a second place needs the line (`refs/return-contract.md`).** V3 flagged `workflow.md:72` and the test pin; V1 added the `refs/return-contract.md` copy of the clause. On the class, V1 said necessary and V3 said drift. See X-002: V3 wins that label, and V1 yields.

---

## Part 2. Updated assessment of V2 and V3 after their Round 1 defenses

### V2 (haiku:qa)

Steelman: V2 is the most precise card. Its five findings have few false claims, its evidence is repo-relative with line numbers, and it is the only card to rate the cli-eval gap P1 and to say why (a missing block is a launch of a long-running process with no safety flags, and the fix is assertions that join condition to outcome). R2-F3 (clause-scoped F1 check across all 15) is correctly scoped.

Critique:
- **No nested-call findings at all.** V2 never opened the skill bodies for nested calls. The 0.94 self-confidence is overstated for a card that left A-003 untouched.
- **R2-F4 is P3, not P2.** plan:371 already requires the `.dev/tasks` files via `git diff --cached`, and plan:372 scopes the equality check to `-- src tests plugins`. The report group list lacks a `.dev/tasks` group, which is a report-completeness gap, not a clean-tree breakage.
- **R2-F5 is a matrix gap** (two `source.md:14` lessons without matrix rows), a reflect-internal gap rather than plan drift. Keep as an observation (U-009).
- Net: V2 is excellent on depth, thin on breadth. Its Round 1 defense did not answer why it skipped the skill bodies.

### V3 (opus:refactorer)

Steelman: V3 is the broadest card. It is the only one with a nested-call sweep (R3-F1, F4, F5), the only one with `verified_ok` negative evidence, and it carries the highest calibration (0.79). Its R3-F1 is a genuine P1 that neither other card found.

Critique (each verified):
- **R3-F13 is wrong.** It claims Task 21's exact equality with `git status` fails on unrelated dirty files such as `.dev/reflect` folders. plan:372 scopes the equality check to `-- src tests plugins`, so `.dev/` is outside the comparison. The example cannot fire.
- **R3-F1's harm is overstated.** The card says an unattended run "would start sc:task as an attended run with its default outward behaviour (commit/push and the committed TFEP report)". The stage is real and the missing flag is real, but the outward behaviour of an attended `sc:task` inside a tasklist run is the callee's own attended prompts plus the STRICT-compliance impact path, not an automatic commit/push. The finding stands at P1 for the missing nested rule; the stated harm should be corrected.
- **R3-F3's "update the 837-844 test pin" is wrong.** The pin tests tokens, not the path text. The remedy of an additive line plus an agreement AC between line 72 and line 75 is sufficient, and updating the pin is not needed.
- **R3-F6 and R3-F7 are partly wrong.** R3-F6's reason text is still true for the task handoff. R3-F7 is true only for the D-P2-8 Safety Threshold clause and not for improve as a whole.
- **Uniform "drift" classification** gives the merge no information about which findings are true spec departures and which are plan wording.
- Net: V3 is the best base. Its coverage is what the other two lack, and its errors are small and fixable.

---

## Part 3. New evidence not presented in Round 1

1. **Task 16 lacks a dependency on Task 12.** plan:290 makes Task 16 depend only on Task 15 (reflect). If Task 16 must nest `task` calls (R3-F1), it must also depend on Task 12, or the nested call would be written against a flag that does not exist yet when Task 16 runs.
2. **Task 20's literal `EXPECTED_NESTING` must change if R3-F1 is accepted.** plan:345 gives `EXPECTED_NESTING` as a literal with `"tasklist": ["reflect"]`. Accepting R3-F1 means `"tasklist": ["reflect", "task"]`. V3 said "update the Task 20 literal"; the new point is that the `P2_GATES` phrases come from the Tasks 2-16 entries (plan:345), so the new Task 16 gate phrase for Stage 9 must be added to the Task 16 entry first or Task 20 will not pin it.
3. **Spec:77 names the same task-builder CLI-mode gate that R1-F3 flags.** `skills/task-builder/SKILL.md:2237` is cited by the spec itself as refused (the `git add -A`), and the same line carries the `--fix --promote` shell-out. This strengthens U-004: the spec already treats this exact gate as an outward action, so the plan's partial resolution of it is a gap in the spec's own terms.
4. **The nested rule is stated generally.** spec:62 and plan:26 say a caller passes `--unattended` and a nested directory to every callee that accepts it at P2. Spec row 182 names only Stage 10.5, but a row is not a limit on a general rule. So A-003 is STATED (in spec:62), not UNSTATED, and V3's three nested findings are rule applications, not new rules. Diff-analysis classifies A-003 as UNSTATED; that should be corrected.
5. **A-001's premise is false in one respect.** `skills/sc-cli-eval-protocol/SKILL.md:137-139` introduces the option list as "the safety flags from the digest". So the set is nameable (it is the digest's set), and the diff-analysis claim that none is "labelled safety flag" is wrong. What is unresolved is which subset a brief must carry for `run` to proceed. That is an owner decision. plan:330 shows the brief row for cli-eval carries "`run` with `--suite <name>` and the run flags".
6. **`:1607` makes the Stage 9 call repeatable.** The loop-back re-delegates `sc:task` against a residual checklist (a second nested call in the same run). The nested directory therefore needs an index: `nested/task-<n>/`, as V3 proposed.
7. **Task 13's nested calls are valid.** The `document`, `analyze`, `impact` and `adversarial` commands accept the flag by P1, so Task 13's nested calls to them are correct as written. This closes an open worry about Task 13 and means the cli-eval problem is confined to the safety-flag gate.
8. **Task 12 (plan:233) is self-contradictory.** "Add to the flag list line" and "add new lines only" cannot both hold against `commands/task.md:44` under Check ADDITIVE. V3's remedy (add a row to the flag table at lines 46-48) is right.

---

## Part 4. Final per-point position table

| Point | Winner | Position |
|---|---|---|
| S-001 | V3 | `verified_ok` section is a real value-add; a card that records what it checked gives the merge negative evidence. |
| S-002 | merge (V3 spine) | Use V3's 14-finding granularity as the spine; fold V1's and V2's unique findings into it. Do not use V2's 5-finding scale. |
| S-003 | V2 | Repo-relative paths with line numbers are the best evidence form. Keep `[INFERRED]` tags. |
| C-001 | merge | Severity P1 from V2. Assertions split per gate from V2. Remedy from V1/V3: name the flag set (the digest's list at `sc-cli-eval-protocol/SKILL.md:137-139`), add the spec's "else blocked" phrase, and record which subset a brief must carry as an owner decision. |
| C-002 | merge | V3 spine (stale `workflow.md:72` and `:75`). Add V1's `refs/return-contract.md` copy. Remedy: an additive line plus an AC that line 72 and line 75 agree. Drop V3's test-pin update. |
| C-003 | merge | V2's clause-scoped scope (all 15 commands; assign the "one short local sentence"; correct the matrix claim) plus V3's single parametrized test. |
| C-004 | merge | V2's semantic point (phrase joins condition to outcome, with a negative test) plus V1's per-task list (Tasks 5, 13, 16). |
| C-005 | V2 (P3) | `.dev/tasks` package is missing from the Task 21 report groups. Severity P3. V3's R3-F13 is wrong (plan:372 scopes the check). |
| C-006 | V3 | The research-light output path ambiguity is a real, minor gap. V1's alternative (show `/sc:research --depth deep` to the owner) is advisory only. |
| C-007 | merge | Task 12 flag-list contradiction (V3) plus V1's wording caution for Tasks 10, 14, 15. Both P3. |
| C-008 | merge | Four-class taxonomy, differentiated per finding. Not uniform "drift", and not V1's "none"/"authorized". |
| X-001 | P1 (V2) | I now support P1. Spec:164 says "else blocked". The plan keeps `--suite` and drops the block, so `run` launches a long-running process with no safety inputs. |
| X-002 | drift (V3) | The stale clause is the plan departing from internal consistency; it is not forced by the spec. V1's "necessary" is withdrawn. |
| A-001 | qualify | The set is nameable (the digest's list, `SKILL.md:137-139`). What is unstated is the required subset for a brief. Record as an owner decision. |
| A-002 | qualify | The one-deleted-line budget is a plan decision (plan:41), not a spec limit. It is a fixed constraint for this merge, but flag that the plan chose it. |
| A-003 | accept (STATED) | spec:62 states the nested rule generally; it governs every nested call. |

---

## Part 5. Unique contributions U-001..U-015: keep, drop or correct

| # | Verdict | Note |
|---|---|---|
| U-001 | keep (correct harm) | R3-F1, P1. Correct the harm to the attended prompts plus the STRICT-compliance impact path, not automatic commit/push. Add the Task 12 dependency and the Task 20 literal change (Part 3, items 1-2). |
| U-002 | keep | R3-F4, release-split Part 4 `sc:analyze` or inline verification. |
| U-003 | keep | R3-F5, reflect Wave 1B optional `tech-research`. |
| U-004 | keep | R1-F3. Strengthened by spec:77 (Part 3, item 3). |
| U-005 | keep | R1-F4, spec-panel `--mode socratic`. |
| U-006 | correct | Keep only the `depth-map.yaml` location (`sc-tasklist-protocol/SKILL.md:1641`). The "D-P2-13 covers only the move" part is wrong. |
| U-007 | keep | R1-F7, add the `reflect-pre` grep AC to Task 16. |
| U-008 | drop | Duplicates plan:45. |
| U-009 | keep as observation | A matrix gap, not plan drift. |
| U-010 | correct | Stale only for the tasklist handoff; the task handoff reason remains true. |
| U-011 | correct | Narrow to the D-P2-8 Safety Threshold clause in improve. |
| U-012 | keep as observation | Not a spec deviation; P1 precedent suggests explaining the Write tool. |
| U-013 | keep | Task 1 format baseline omits `test_sc_recommend_routing_contract.py`. |
| U-014 | keep | Task 1 "drop the equality case" has no target (= T1-F2). |
| U-015 | keep | `verified_ok` list; carry it into the merged report as negative evidence. |

---

## Part 6. Recommended base variant for the merge

**Base: Variant 3.**

Reason: V3 has the highest calibrated score (0.79), the broadest coverage, the only nested-call sweep (U-001..U-003, which is where the one finding no other card found sits), and the only `verified_ok` section. Its errors (R3-F13, the R3-F1 harm wording, the test-pin remedy in R3-F3, parts of R3-F6 and R3-F7) are small and each is corrected above.

Graft onto V3:
- From V2: P1 severity on the cli-eval gap (R2-F1) and the rule that gate assertions join condition to outcome with a negative test (R2-F2). Also the clause-scoped F1 scope (R2-F3).
- From V1: U-004 (task-builder CLI-mode `--fix --promote` under `--unattended`), U-005 (spec-panel socratic), the per-gate phrase list for Tasks 5, 13 and 16, the `refs/return-contract.md` copy, and the Task 16 `reflect-pre` grep AC.
- Corrections to carry: A-003 is STATED; A-001's premise is false; R3-F13 is dropped; each retained finding gets a differentiated class.
