# Round 1: Advocate for Variant B (reviewer 2 card, qa persona)

## Position summary (1-3 sentences)

Variant B is the better-structured and more precisely classified card. It splits defects one per finding, classifies plan omissions correctly as drift (X-002), avoids the unbound-variable trap that Variant A's `$ART` fix would introduce (C-004), and is the only card that audits the T1 coverage matrix (C-003). Variant A is the stronger defect finder overall. On the merits I concede X-001 (plan:48 exits 1 on success), the severity in X-003, and the A-003 conflict my variant missed. Overall: B is superior on 7 of 14 diff points, A on 6, with 1 tie. Because A's wins are on the higher-impact points (X-001, A-001), the merge should take A's defect content into B's per-finding structure and classification.

## Steelman of Variant A

Variant A's strongest case is that it checks every acceptance line for its real exit status, and that is where this plan breaks. plan:21 says "every line must exit 0". A tested this rule line by line and found three exit-status defects that B missed or misjudged:

1. plan:48 inverts its own pass condition under `pipefail` (R1-01). The orchestrator's pre-check confirms it, and so does my own run: input `src/a.py` exits 1, input `.claude/skills/x` prints the path and exits 0.
2. `A && B` and `A && ! B` lines do not gate under `-e` (R1-07, calibrator: confirmed for plan:162, 165, 202-203, 244).
3. `grep -i connected` also matches "Disconnected" and "not connected" (R1-09). Layer 2 has the negative check at source.md:375; T12 at source.md:714 does not.

A also found a real task-ordering defect B missed. U11 (source.md:296, "`claude --version` fails") tests the phase function that source.md:101 places in `install_mcp.py` (Task 5), yet plan:92/96 assigns U11 to Task 4 (R1-05). And A's fix for C-001, printing the `claude mcp remove` command into the G6 comment, is consistent with source.md:706. Calibration agrees: A has C 0.80 against B's 0.74, and A has higher citation grounding (0.85 vs 0.75) and risk-surface coverage (0.85 vs 0.75). On the question "which card would stop more broken runs", A wins.

## Key strengths claimed (numbered, each with evidence)

1. **Correct classification of the `$E` omission (X-002).** In the spec, `E` is defined inside the same step-1 block that uses it (source.md:534, used at source.md:540). The plan includes step 1 only by reference (plan:104, "Step 1 is the sandbox `add-json` shape probe of `./source.md` T2") but lifts the `jq -e --argjson e "$E"` line into its own acceptance bullet (plan:107) without the definition. That is an unforced omission by the plan, which makes it drift, not a necessary deviation, because no constraint required dropping the definition. B also names the failure mechanism: under `set -u` (plan:21) the line aborts on an unbound variable. A's "necessary" label (R1-03) has no justification attached.
2. **One defect per finding (S-002, C-002).** P2R2-3 isolates the Task 3 hash problem: plan:86 requires before/after equality, but the only `H0` in the method is in Leg B (source.md:525), so outside the undecided band no step records the before-hash. The calibrator confirmed this ("H0 only in Leg B"). A folds this into R1-04 together with path resolution and the Task 14 copy line, so the merge cannot accept, reject or grade those three parts separately.
3. **The fix for `./artifacts/` does not introduce a new defect (C-004).** A proposes "Define ART=... once in Constraints ... use $ART everywhere" (R1-04). Each acceptance block runs as its own `bash -euo pipefail` invocation (plan:21; source.md:445 gives `bash -euo pipefail <<'EOF' … EOF`). A variable defined once in prose is unbound in every block, and `set -u` aborts it. That is the same defect class as `$E` (point 1). B's fix spells out the literal package path in Tasks 3, 14 and 16 (P2R2-4), which needs no shell state.
4. **Audit of the T1 artifact (C-003).** B is the only card that checked the coverage matrix the reflection relies on. coverage-matrix.yaml:319-325 maps INF-037 (source.md:289, U4) to Task 7. coverage-matrix.yaml:454-461 maps INF-056 (source.md:308, U23) to Task 3. Both are containment false positives: U4 belongs to Task 4 (plan:92) and U23 to Task 5 (plan:104). The calibrator confirmed both, with a mislabel. Without this, the merged report would cite matrix rows as coverage evidence for tasks that do not carry them.
5. **The deviation taxonomy is used fully (S-003).** A UC-1 reflection must classify every divergence, not only defects. P2R2-7 records plan-introduced additions as authorized: plan:54 commits only if a file changed, plus the plan:48 guard and the Task 14/16 evidence files. The plan:48 guard's intent is authorized by the hard rule at source.md:755 ("never commit anything under `.claude/` except `.claude/settings.json`") and by source.md:436. Without this entry, the merge has no record that these additions were reviewed.
6. **Correct severity for C-002.** plan:86 is unverifiable rather than violated. Leg A runs with a sandbox `HOME`/`CLAUDE_CONFIG_DIR` (plan:75, source.md:522), so the real `.mcpServers` is not at risk in the common path. "Minor" (P2R2-3) fits that better than "important".

## Weaknesses identified in Variant A (numbered, each with evidence)

1. **Inconsistent classification.** A labels inherited spec defects "drift" in R1-02 (copied from source.md:710-711) but "necessary" in R1-05, R1-08 and R1-09, which are inherited from source.md:466, :649-651 and :714. It also labels a pure plan omission "necessary" (R1-03, `$E`). Within one card, the same origin gets two classes. This is the source of shared assumption A-002.
2. **The `$ART` fix would itself fail under `set -u`** (see strength 3). R1-04's fix repeats the defect pattern it sits next to.
3. **Bundled finding R1-04.** Three independent defects share one severity ("important"), and the calibrator downgraded part of it ("prose ./ refs ambiguous rather than wrong"). Because they are bundled, the over-grading spreads to the parts that are only ambiguous prose (plan:79, plan:237).
4. **Two findings overstated, one citation wrong.** R1-06 is overstated: Task 6's acceptance (plan:123-125) never checks the Ready line. R1-11 is overstated: the fallback is included by reference through plan:19 and plan:223. In R1-07, plan:84 is a standalone `&&` bullet, not a line inside a block, so that citation is wrong.
5. **No look at the T1 artifact.** A missed the two false attributions (strength 4), so a merge based on A alone would inherit the T1 matrix's errors.
6. **A also missed the source.md:706 conflict.** R1-04 argues only about the path of `./artifacts/t16-live-verify.txt` (plan:272, 287). It never notices that source.md:706 says T12 writes no file in the repository at all.

## Concessions

- **X-001, conceded on the mechanism.** My variant called plan:48 a benign authorized addition with "Fix: None" (P2R2-7). The intent, a `.claude/` staging guard, is authorized by source.md:755. The command, however, is defective. In the success case the first `rg` matches nothing and exits 1. With only `.claude/settings.json` changed, the `rg -v` selects nothing and exits 1. Under `pipefail` the line exits 1 on every clean commit and exits 0 only when it prints a violation. I ran both cases: clean exit=1, violation exit=0. It contradicts plan:21, and an executor that judges by exit status would either fail a correct commit or pass a bad one. The right split is "authorized expansion (intent) + drift (mechanics)". A's `{ rg … || true; }` fix inside `test -z "$(…)"` is correct.
- **P2R2-5 mislabel.** I wrote "U25 -> Task 3". INF-056 is U23 at source.md:308 (coverage-matrix.yaml:456). U25 is INF-058 and is unmatched. The finding holds, but its identifier was wrong.
- **P2R2-6 overstated.** I claimed §6 and §8 have no rows. The calibrator found INF-093 (§6) and INF-104 (§8). The other spans are rowless, so the finding is real but smaller than stated.
- **P2R2-7 missed the t16 conflict (A-003).** plan:272/287 require `./artifacts/t16-live-verify.txt`, while source.md:706 says "Files: none in the repository; the outputs go only into the issue-#323 comment". That is not benign. Post-merge there is no commit point (plan:272), so the file would stay untracked, which conflicts with the always-staged rule (plan:24). Committing it would conflict with source.md:706 and :719. My fix for P2R2-1 ("record ... in the t16 artifact") makes this worse. A's fix (print into the G6 comment) is the better one.
- **P2R2-4 spec_ref.** source.md:465 does not support the claim; the spec has no `./artifacts` paths (calibrator). The finding is plan-introduced and should cite `none`, as R1-04 does.
- **Missed defects.** B missed U11 (R1-05), the non-gating `&&` lines (R1-07), `grep -i connected` (R1-09), the `--no-project` yaml import (R1-08), the dropped T0b reporting duty (R1-10), and Task 14's block having no copy line into `artifacts/`. A is the better defect finder.

## Per-point positions (table: Diff point | Superior variant (A/B/tie) | Confidence % | One-line evidence)

| Diff point | Superior variant (A/B/tie) | Confidence % | One-line evidence |
|---|---|---|---|
| S-001 | A | 65 | A's `self_audit` names what was checked and the one UNVERIFIED item (directory-level pytest vs baseline); B gives no audit trail. |
| S-002 | B | 70 | P2R2-3 and P2R2-4 separate the hash and path defects that R1-04 bundles under one over-graded severity (calibrator: "prose ./ refs ambiguous rather than wrong"). |
| S-003 | B | 55 | UC-1 classifies every divergence; P2R2-7 records the plan:48/54/237/253 additions (intent backed by source.md:755), though its verdict on plan:48 was wrong. |
| S-004 | A | 55 | A cites spec lines throughout; B's P2R2-4 spec_ref (source.md:465) does not support the claim. B's matrix citations still add value. |
| C-001 | A | 60 | Both find the defect at plan:278 vs plan:286/source.md:211; A's "print into the G6 comment" fix respects source.md:706, and B's "record in the t16 artifact" does not. |
| C-002 | B | 65 | P2R2-3 is a standalone finding with the exact gap (H0 only at source.md:525, Leg B) and a correct minor severity, since Leg A uses a sandbox HOME (plan:75). |
| C-003 | B | 75 | Only B audits the T1 matrix: coverage-matrix.yaml:319-325 (U4 to Task 7) and :454-461 (U23 to Task 3) are false; the carriers are Task 4 (plan:92) and Task 5 (plan:104). |
| C-004 | B | 65 | `$ART` defined "once in Constraints" is unbound in each separately run `bash -euo pipefail` block (plan:21, source.md:445); B's literal paths need no shell state. |
| X-001 | A | 80 | plan:48 exits 1 on a clean commit and 0 on a violation under pipefail (tested); this contradicts plan:21, so B's "Fix: None" is wrong. |
| X-002 | B | 70 | source.md:534 defines E in the same block it is used; the plan lifts the use (plan:107) and drops the definition with no justification, which is drift, and `set -u` aborts the line. |
| X-003 | A | 60 | plan:85 is an executable `jq` on `./artifacts/t3-run2.json`; from the repo root it reads or writes the never-staged project-root `artifacts/`, so evidence is lost. That is more than minor. |
| X-004 | A | 55 | A found that Task 14's block (plan:242-250) writes only /tmp with no copy line; B called the files benign and missed the source.md:706 conflict. Neither card caught that conflict. |
| A-001 | A | 60 | A applied the plan:21 exit-0 rule to bullet commands; I QUALIFY that rule below, but the plan:48 failure is real under either reading. |
| A-002 | tie | 50 | Both cards label inherited spec defects "drift" (R1-02, P2R2-1); A is also internally inconsistent (R1-05/08/09 necessary), and B also over-applies drift. |

Tally: A 6, B 7, tie 1.

## Shared assumption responses (A-001, A-002: ACCEPT/REJECT/QUALIFY + reason; A-003 comment)

**A-001 (bullet-form acceptance commands inherit the plan:21 exit-0 rule): QUALIFY.**
- plan:21 says "Every acceptance *block* runs under `bash -euo pipefail`". Most bullets state their own pass test: "exits 0" (plan:46, 82, 97), "prints `coder-handoff-prompt.md`" (plan:47), "prints nothing" (plan:48). So the condition is:
  - a bullet that says "exits 0" inherits the rule;
  - a bullet that states an output criterion is judged by that output, but must not exit non-zero when it passes, because executors (and `/sc:implement` per-task QA) run it as a shell check.
- Under that qualified reading, plan:48 still fails. Its output criterion ("prints nothing") passes, but its exit status (1) signals failure, so the two signals disagree. Fix: every bullet whose criterion is "prints nothing" should be written as `test -z "$(…)"`, so the output check and the exit check agree.
- The same applies to plan:84, where `A && B` as a standalone line is fine. It is inside blocks (plan:162, 165, 202-203, 244) that `&&` stops gating.

**A-002 (a defect copied verbatim from the spec is plan drift): REJECT as a blanket rule, with this condition.**
- Drift means the plan departs from its spec without justification. A plan that copies the spec verbatim has not departed.
- Classify such defects as **inherited** (origin: spec). Their fix, once applied, is a **necessary deviation** from the spec text, justified by the defect.
- Under that rule:
  - C-001 (plan:278 = source.md:710, with the tension already present at source.md:211), R1-05 (source.md:466), R1-07 (source.md:601, 604, 636, 675) and R1-09 (source.md:714) are inherited, with necessary-deviation fixes. This changes R1-02 and P2R2-1 from drift.
  - Plan-introduced defects stay drift: plan:48 (no spec line; source.md:440-442 has only two lines), plan:107 (the plan dropped E's definition from source.md:534), the `./artifacts/` paths (spec has none), and plan:86 (the plan widened source.md:525's Leg-B-only hash guard to the whole task without adding a before-hash). That keeps P2R2-2 and P2R2-3 as drift and moves R1-03 from necessary to drift.

**A-003 (Task 16 may write an in-repository artifact; CONTRADICTED by source.md:706).**
- I accept the contradiction, and it counts against both cards, mine more (P2R2-7 called it benign).
- source.md:706 says "Files: none in the repository; the outputs go only into the issue-#323 comment", and source.md:719 repeats "nothing in the repository changes". plan:272 and plan:287 add `./artifacts/t16-live-verify.txt`.
- This is drift, not an authorized expansion. Post-merge there is no commit point, so the file is either left untracked, against plan:24 and the always-staged rule, or committed, against source.md:706.
- Fix: write the outputs to `/tmp/p2-t16-*.txt`, paste them into the G6 comment (as plan:272 already requires), and delete the `./artifacts/t16-live-verify.txt` clause from plan:272 and plan:287.
- The fix for C-001 should follow A's version (print into the comment), not B's (record in the artifact).
