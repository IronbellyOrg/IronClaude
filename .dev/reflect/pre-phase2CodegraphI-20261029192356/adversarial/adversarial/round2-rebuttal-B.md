# Round 2: Rebuttal for Variant B (reviewer 2 card, qa persona)

Read-only on the repository. This round I re-read plan:21, 27, 48, 79, 85-86, 237, 242-253, 272-287 and source.md:195-214, 445, 522-541, 623-625, 704-721, 755-765, along with round1-advocate-A.md and round2-rebuttal-A.md. Every shell check ran in a private `mktemp -d` git repo under /tmp, which was removed on exit.

## Response to criticisms

1. **P2R2-7 marks plan:48 benign with "Fix: None": CONCEDED (unchanged from Round 1).**
   - The guard's intent is an authorized expansion (source.md:755, plan:23).
   - Its command form is defective: under `pipefail` it exits 1 on every clean commit and 0 on a violation. I re-ran this.
   - The merged finding should read "authorized expansion, defective command form, important, fix required".

2. **P2R2-7 and P2R2-1's fix route output into the t16 file that source.md:706 forbids: CONCEDED, and P2R2-1's fix is withdrawn.**
   - source.md:706 says "Files: none in the repository; the outputs go only into the issue-#323 comment". source.md:719 says "nothing in the repository changes".
   - P2R2-1's fix destination becomes the G6 comment. That is A's version, and it is consistent with plan:286 and source.md:211.
   - The plan:272/287 t16 clause is drift. Fix: outputs go to `/tmp/p2-t16-*.txt` and are pasted into the comment.

3. **Four high/medium defects missed (U11, non-gating `&&`/`!` lines, Task 14 copy line, `connected` grep): CONCEDED on substance, with two weighting notes.**
   - Three of the four are inherited from the spec, not made by the plan:
     - U11 comes from source.md:466 vs :101.
     - The `&&`/`!` lines come from source.md:601, 604, 636 and 675. The spec knows the if-form rule (source.md:625: "set -e ignores a failing `! cmd`") but applies it only to T6.
     - The `connected` grep comes from source.md:714.
   - Under the A-002 rule both advocates now hold, all three are recorded as inherited, with necessary-deviation fixes. They are still real defects, and B should have found them.
   - The Task 14 copy line is plan-made: the spec has no `./artifacts` paths. But plan:237 does tell the executor in prose to "keep the run output as `./artifacts/t14-final-run.txt`". So the gap is "acceptance block does not perform the step its prose requires". That is medium, not a missing step. Classification: drift.

4. **P2R2-5 and P2R2-6 audit the reflect matrix, not the plan; P2R2-6 is overstated: PARTLY CONCEDED.**
   - P2R2-6 being overstated is conceded; §6 has INF-093 and §8 has INF-104.
   - On weight, I accept a drop from 75, but not to 55.
     - The coverage focus of this reflection is graded partly on the T1 matrix. A merged report that cites INF-037 as evidence that Task 7 carries U4 (coverage-matrix.yaml:319-325) would pass an evidence-validator citation check on a false attribution.
     - The same holds for INF-056, which maps U23 to Task 3 (:454-461).
     - So the finding protects the integrity of this reflection's coverage claim, even though no plan requirement is lost (variant-2:40).
   - New position: B, 60.

5. **Severity too low on the paths: PARTLY CONCEDED, split by line.**
   - **Important** for the executable lines:
     - plan:85 runs `jq -e … ./artifacts/t3-run2.json` from the repo root.
     - plan:253 requires both t14 files while the plan:242-250 block writes only `/tmp`.
     - Both cause a false failure or leave evidence that can never be staged (plan:24).
   - **Minor** for the prose-only references at plan:79 and plan:237. The calibrator noted that the "prose ./ refs [are] ambiguous rather than wrong".
   - **Minor** for C-002 (plan:86). A conceded this in Round 2, item 7: Leg A never runs `claude` and uses a sandbox HOME (plan:75, source.md:522).

6. **A's file-first fix for plan:48: ACCEPTED, with two refinements** (see New evidence 1-3).
   - I withdraw my Round 1 endorsement of a bare `test -z "$(pipeline)"`, and my A-001 condition that every "prints nothing" bullet should take that form. That form passes vacuously when `git diff` cannot run.
   - **Refinement 1:** the `{ … || true; }` brace groups inside A's second line are redundant. Bash does not propagate `-e`/`pipefail` from a command substitution to `test`'s exit status. Line 1 is what actually guarantees the file exists.
   - **Refinement 2:** the if-form `if rg '^\.claude/' F | rg -v '^\.claude/settings\.json$'; then exit 1; fi` is equally sound. It also prints the offending path into the log, which is better diagnostics for the G0 comment. It also matches the spec's own convention for negative checks (source.md:625).
   - Either form is acceptable. I prefer the if-form.

7. **A's narrowed plan:277 user-scope finding: QUALIFIED.** I accept the scope split, accept part (c) but as inherited, accept part (b) as inherited, and judge part (a) overstated.
   - **Scope split: accepted.** source.md:210 (user scope) says a kept-entry failure "means the user runs the printed command" and has no "not that the plan failed". source.md:211 (local scope) does have that phrase. source.md:705 says the executor "does not mark T12 done until all pass". So plan:286 is right to exempt local scope only, and A's withdrawal of its Round 1 concession 10 is correct.
   - **(a) No instruction for the user-scope kept-entry case: overstated.**
     - plan:272 says Task 16 "Implements `./source.md` T12 and §2.12", and plan:19 says details not repeated in the plan are in that section.
     - The source.md:210 instruction is part of §2.12's acceptance, so it is included by reference.
     - The calibrator ruled R1-11 overstated on exactly this basis (plan:19, plan:223). The same rule should apply here.
   - **(b) The user action is not one of the six human items at plan:27: real, but inherited.** The spec's own list (source.md:757-765, items 1-6) also has no "user runs the printed retire command" item. So the plan faithfully copies a spec gap. Classification: inherited, minor. The necessary-deviation fix adds it as a non-blocking human item, or states in Task 16 that T12 stays open, and is reported in G6, until the user acts.
   - **(c) plan:277 is the first line of the exit-0 block, so its failure aborts lines 278-284: real, but inherited, not drift.**
     - The block is verbatim source.md:709-716.
     - The consequence matters for reporting. plan:272 and source.md:721 require "every T12 command and its output" in the G6 comment, and an abort at line 1 loses six outputs.
     - Under A's own A-002 rule this is inherited, with a necessary-deviation fix, not "drift, plan omission" as A labels it.
   - **Fix: accepted.** Run each line as a reported line (`|| echo USER_SCOPE_KEPT`, `|| echo LOCAL_SCOPE_HIT`). Copy the retire step's printed commands into the G6 comment. State that T12 stays open until the user-scope line passes. This is the same mechanism and fix as C-001, so the merge should fold them into one finding covering plan:277-278.

## Updated assessment of Variant A

- **A's Round 2 concessions are accurate and close most of the classification dispute.**
  - A conceded `$ART` (C-004), the bundling (S-002), the `$E` class (X-002), the C-002 severity, and the R1-02/R1-07 labels.
  - On each of these, Variant B's structure or classification is the one the merge should adopt.
- **A's correction to the inconsistency charge holds.** Under the shared A-002 rule, R1-05, R1-08 and R1-09 are inherited, so "necessary" is right for them. My Round 1 weakness 1 overstated A's inconsistency. The real mislabels were R1-02, R1-03 and R1-07.
- **A's new plan:277 finding repeats the error A has just conceded.** A labels it "drift, plan omission". Parts (b) and (c) are verbatim spec content (source.md:757-765 and :709-716), and part (a) is included by reference (plan:19, plan:272).
- **A's defect-finding lead stands.** U11, the non-gating lines, the Task 14 copy gap and the `connected` grep are all real. Through the merge's defect content, they decide the points that matter most for execution safety: X-001, X-003 and X-004.

## New evidence

All runs were in a throwaway repo under `/tmp/ironclaude-batch.*`, removed on exit.

1. **Vacuous pass confirmed.**
   - In a one-commit repo, `test -z "$(git diff --name-only HEAD~1 HEAD 2>/dev/null | { rg … || true; } | { rg -v … || true; })"` printed `VACUOUS_PASS` and exited 0.
   - A's file-first form, `git diff --name-only HEAD~1 HEAD > f.txt` as its own line, exited 128 and stopped the block.
2. **A's file-first fix is correct on every case.**
   - Clean commit (`src/a.py` plus `.claude/settings.json`): `PASS`, exit 0.
   - Violation (`.claude/skills/x.md`): exit 1.
3. **The `|| true` groups are redundant, and the masking risk sits in line 1, not line 2.**
   - Without the brace groups, line 2 gives the same results: clean `PASS` exit 0, violation exit 1.
   - With them, `rg` on a missing file is still masked (`MASKED_PASS`, exit 0).
   - So the only real protection is line 1 creating the file, exactly as A says. The groups add nothing.
   - The if-form alternative printed `.claude/skills/x.md` and exited 1 on a violation.
4. **The spec's human-intervention list has no item for "user runs the printed retire command"** (source.md:757-765, items 1-6). This makes A's part (b) inherited.
5. **The T12 block is verbatim spec** (plan:276-285 = source.md:709-716). This makes A's part (c) inherited.

## Updated per-point positions (same 14-point table)

| Diff point | Superior variant (A/B/tie) | Confidence % | One-line evidence |
|---|---|---|---|
| S-001 | A | 70 | variant-1:84 names its checks and its UNVERIFIED item; B has no audit trail (conceded). |
| S-002 | B | 70 | A concedes R1-04 must split three ways; B's per-defect findings (P2R2-3, P2R2-4) are the merge structure. |
| S-003 | B | 55 | Recording authorized expansions is correct taxonomy use (source.md:755 backs plan:48's intent); P2R2-7's plan:48 and t16 verdicts were wrong. |
| S-004 | A | 60 | A cites spec lines throughout; P2R2-4's source.md:465 does not support it (conceded). |
| C-001 | A | 65 | A's G6-comment fix respects source.md:706; P2R2-1's t16-file fix is withdrawn. Fold plan:277 in (same mechanism). |
| C-002 | B | 65 | A concedes minor; P2R2-3 isolates the gap (H0 only at source.md:525). Class drift (plan:86 widens the Leg-B guard). |
| C-003 | B | 60 | False matrix attributions (coverage-matrix.yaml:319-325, :454-461) would pass a citation check in this reflection; no plan requirement lost. |
| C-004 | B | 70 | A concedes `$ART` is unbound in separately run `-euo pipefail` blocks (plan:21, source.md:445). |
| X-001 | A | 80 | Exit status inverted (re-run); B's "Fix: None" was wrong. A's file-first fix is accepted (refined: if-form or no `|| true` groups). |
| X-002 | B | 70 | A concedes: source.md:534 defines E, plan:107 drops it, so drift, and it aborts under `-u`. |
| X-003 | A | 60 | Important for executable plan:85 and plan:253, minor for prose plan:79 and plan:237. A wins the important part. |
| X-004 | A | 65 | Only A found that plan:242-250 has no copy to plan:253's files; both missed source.md:706, and B called the t16 file benign. |
| A-001 | A | 55 | Both QUALIFY alike; A supplied the file-first form, and my Round 1 `test -z "$(…)"` condition is withdrawn. |
| A-002 | tie | 50 | Same REJECT rule held by both; both cards mislabeled originally. A's new plan:277 "drift" label repeats the error. |

Tally: A 7, B 6, tie 1. A's wins are on defect content (X-001, X-003, X-004, C-001), and B's on structure and classification (S-002, C-002, C-004, X-002). The merge should take A's defect content, framed in B's one-defect-per-finding structure, using B's literal paths and drift labels for plan-made omissions.

## Final shared-assumption stance (A-001, A-002)

**A-001: QUALIFY (final).**
- plan:21 has no bullet exemption.
  - A bullet that states "exits 0" inherits the rule.
  - A bullet that states an output criterion ("prints nothing", "prints X") is judged by that output, and must also exit 0 when it passes, because executors and `/sc:implement` QA run it as a shell check.
- Every bullet whose criterion is "prints nothing" is rewritten in one of two forms:
  - file-first: the producing command runs as its own gating line that writes a file, then `test -z "$(rg … F | rg -v …)"`;
  - if-form: `if <filter on F>; then exit 1; fi` (source.md:625).
- `test -z "$(producer | filter)"` with the producer inside the substitution is never used, because it passes vacuously.
- plan:48 is "authorized expansion (source.md:755, plan:23), defective command form, important".
- Add one sentence to plan:21 stating this rule for bullets.

**A-002: REJECT (final).**
- A defect copied verbatim from the spec is inherited (origin: spec), not drift. Its fix is a necessary deviation from the spec text. This covers:
  - R1-02 / P2R2-1 (source.md:710, in tension with :211);
  - the plan:277 abort, and the missing human item for the user-scope retire command (source.md:709-716, :757-765);
  - R1-05 (source.md:466), R1-07 (source.md:601, 604, 636, 675), R1-08 (source.md:649-651) and R1-09 (source.md:714).
- Plan-made divergences stay drift:
  - plan:107 (`$E`, so R1-03 is relabeled and P2R2-2 stands);
  - plan:86 (the Leg-B-only H0 guard of source.md:525 widened without a before-hash);
  - the `./artifacts/` paths and the Task 14 missing copy line;
  - the t16 in-repository file at plan:272/287 (it contradicts source.md:706).
- Plan-added items that are backed by a spec rule are authorized expansions, even when their form is defective. Examples: plan:48 (source.md:755) and plan:54's "commit only if a file changed".
