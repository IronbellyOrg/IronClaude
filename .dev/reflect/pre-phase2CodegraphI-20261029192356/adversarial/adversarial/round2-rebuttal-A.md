# Round 2 — Rebuttal for Variant A (reviewer 1 card)

Read-only. In this round I re-read source.md:209-211, source.md:518-525, plan:73-77, plan:86, plan:274-287 and round1-advocate-B.md. I ran shell checks only in a private `mktemp -d` git repo under /tmp, which was removed afterwards.

## Response to criticisms (numbered, counter-evidence or concession)

1. **Inconsistent classification: CONCEDED, with one correction.** R1-02 and R1-07 are inherited from the spec (source.md:710; source.md:601, 604, 636, 675). They should be "inherited, fix = necessary deviation", not drift. R1-03 (`$E`) is a plan omission: source.md:534 defines `E` and plan:107 dropped it. It should be drift, not necessary.
   The correction: R1-05, R1-08 and R1-09 are inherited (source.md:466, 649-651, 714), so "necessary" is the correct class for them, not an inconsistency. Under the A-002 rule that both advocates now hold, A had three of five inherited findings right and one plan omission wrong.
2. **`$ART` unbound under `set -u`: CONCEDED.** Each block runs as its own `bash -euo pipefail` invocation (plan:21; source.md:445). A variable defined once in Constraints is not in scope there. The fix could be repaired by defining `ART=` at the top of each block, but B's literal path is simpler and cannot fail this way. Take B's form.
3. **R1-04 bundles three defects under one over-graded severity: PARTLY CONCEDED.**
   - The bundling is conceded. The merge should split R1-04 into three findings: path resolution, the Task 3 before-hash, and the Task 14 copy line.
   - The over-grading is not conceded for the executable parts. The calibrator's caveat ("prose ./ refs ambiguous rather than wrong") covers the prose at plan:79 and plan:237. It does not cover plan:85, an executable `jq -e ... ./artifacts/t3-run2.json` run from the repo root. Nor does it cover plan:253, which requires both t14 files to exist while the plan:242-250 block writes only `/tmp`.
   - Those two parts cause a false acceptance failure, or leave evidence where it can never be staged (plan:24). Grade them important. The prose-only part is minor.
4. **R1-06 and R1-11 overstated, plan:84 citation wrong: CONCEDED.** All three were already conceded in Round 1. R1-07 stands for plan:162, 165, 202-203 and 244. B's Round 1 steelman agrees with that list.
5. **No audit of the T1 coverage matrix: CONCEDED as a gap, disputed on weight.** P2R2-5 is real, with the U23 correction. By B's own card it is "No requirement lost" (variant-2:40). It corrects the reflection's evidence trail, not the plan, and the focus areas are plan correctness, coverage and deviation classification. A's `self_audit` (variant-1:84) re-checked the U1-U25 assignment directly and found the U11 misplacement, which the matrix did not surface. Weight: B 55, not 75.
6. **Missed the source.md:706 t16 conflict: CONCEDED.** Both cards missed it. B missed it more: P2R2-7 called the file benign, and P2R2-1 routed the local-scope report into it. A's C-001 fix sent the report to the G6 comment, which is consistent with source.md:706, but A never named the conflict.
7. **C-002 is minor because Leg A uses a sandbox HOME: CONCEDED.**
   - plan:75 and source.md:522 run Leg A with sandbox `HOME`/`CLAUDE_CONFIG_DIR` ("no login, no real HOME"), and Leg A never runs the `claude` CLI.
   - The plan:23 hard rule's hash assertion is scoped to runs of `claude mcp add/remove` or `superclaude install`. Leg A runs neither.
   - The real `.mcpServers` is therefore at near-zero risk outside Leg B, which has its own H0/H1 guard (source.md:525). plan:86 is an unmeetable criterion, not a safety hole, so "minor" fits.
   - I keep one point: the criterion must still get an H0-first line and a closing equality test. Otherwise an executor can only fail the task or assert it without evidence. Classification: drift, because the plan widened source.md:525's Leg-B-only guard to the whole task. I agree with B on this.

## Updated assessment of Variant B

- **B's Round 1 concessions are accurate.** X-001 mechanism, the P2R2-5 label, P2R2-6 overstated, the t16 conflict, the P2R2-4 spec_ref, and six missed defects. This narrows the dispute to classification and structure.
- **B accepts a plan:48 fix that is still unsound.** B says "A's `{ rg … || true; }` fix inside `test -z "$(…)"` is correct" (round1-B:37). Its A-001 condition goes further and proposes `test -z "$(…)"` for every "prints nothing" bullet (round1-B:71). That form hides a failed upstream command (New evidence 1).
  - The rule should be: the producing command is its own gating line writing to a file, and `test -z` runs only on the filtered file. That makes the output check and the exit check agree without a vacuous pass. My own R1-01 fix has the same flaw; I conceded it in Round 1, and it is now shown concretely.
- **B's taxonomy points hold.** S-003 (record authorized expansions), S-002 (one defect per finding), C-004 (literal paths) and X-002 (`$E` is drift) are genuine improvements the merge should adopt.
- **B's per-point rating on C-003 (75) is too high** for a finding that changes no plan requirement (see criticism 5).
- **B's A-002 row is a tie (50), and I now agree.** Both advocates hold the same REJECT rule, and both cards originally mislabeled inherited defects.

## New evidence

1. **`test -z "$(…)"` passes when `git diff` cannot run.** In a fresh one-commit repo (`HEAD~1` does not resolve), I ran `bash -euo pipefail -c 'test -z "$(git diff --name-only HEAD~1 HEAD 2>/dev/null | { rg "^\.claude/" || true; } | { rg -v "^\.claude/settings\.json$" || true; })"; echo ...'`. It printed the success line. The guard passes without checking anything.
   The file-first form `git diff --name-only HEAD~1 HEAD > files.txt` exits 128 under `-e` and stops the block. Recommended plan:48 replacement, as two gating lines in a block:
   ```bash
   git diff --name-only HEAD~1 HEAD > /tmp/p2-t1-files.txt
   test -z "$({ rg '^\.claude/' /tmp/p2-t1-files.txt || true; } | { rg -v '^\.claude/settings\.json$' || true; })"
   ```
   The second line's substitution reads a file that already exists, so the only way it masks an error is if `rg` itself is missing. That residual risk is acceptable.
2. **My Round 1 concession 10 (plan:277 user-scope exception): NARROWED, not withdrawn.**
   - The spec treats the two scopes differently on purpose:
     - source.md:211 (local scope) says a failure means the user runs `claude mcp remove <name> --scope local`, "not that the plan failed".
     - source.md:210 (user scope) says a failure caused by an entry the retire step reported as kept "means the user runs the printed command". It does not say "not that the plan failed".
     - source.md:706 says the executor "does not mark T12 done until all pass".
   - So for user scope, T12 stays open until the user acts and the check passes. plan:286 is right to grant the "not a plan failure" exemption to local scope only. My Round 1 claim that plan:286 should also cover plan:277 is withdrawn.
   - What remains (minor, drift, plan omission):
     - (a) plan:274-287 gives no instruction for the user-scope kept-entry case. The spec at source.md:210 says to surface the printed command to the user, and the plan drops this.
     - (b) That user action is not among the six human items at plan:27 ("Never stop to ask otherwise"), so an executor has no sanctioned path to wait on it.
     - (c) plan:277 is the first line of the exit-0 block. Under `-e` its failure aborts lines 278-284, which is the same mechanism as C-001, so the diagnostics for registration, version, `mcp get`, `--list` and doctor never run.
   - Fix: run the user-scope check as a reported line (`|| echo USER_SCOPE_KEPT`). Copy the retire step's printed command into the G6 comment. State that T12 stays open until it passes, as source.md:706 requires.

## Updated per-point positions (same 14-point table: S-001..S-004, C-001..C-004, X-001..X-004, A-001, A-002)

| Diff point | Superior variant (A/B/tie) | Confidence % | One-line evidence |
|---|---|---|---|
| S-001 self-audit block | A | 70 | variant-1:84 names checks and the UNVERIFIED item; B concedes (round1-B:48). |
| S-002 finding granularity | B | 65 | R1-04 should split three ways (conceded); executable parts stay important. |
| S-003 non-defect entries | B | 55 | Recording authorized expansions is correct taxonomy use; P2R2-7's plan:48 and t16 verdicts were wrong. |
| S-004 citation style | A | 60 | A cites spec lines throughout; P2R2-4 spec_ref :465 unsupported (B conceded). |
| C-001 local-scope `jq` in exit-0 block | A | 65 | Both advocates agree A's G6-comment fix respects source.md:706; B's t16-artifact fix does not. |
| C-002 Task 3 hash criterion | B | 60 | Conceded: Leg A never runs `claude` (plan:75, source.md:522), so minor; class drift (plan widened source.md:525). |
| C-003 audit scope | B | 55 | Matrix audit is real but changes no plan requirement (variant-2:40 "No requirement lost"). |
| C-004 `./artifacts/` fix approach | B | 65 | Conceded: `$ART` is unbound in separate `-euo pipefail` blocks (source.md:445). |
| X-001 plan:48 guard | A | 75 | Both advocates agree exit status inverts; the correct fix is file-first (New evidence 1), not B's accepted `test -z "$(…)"`. |
| X-002 class of undefined `$E` | B | 65 | Conceded: source.md:534 defines E; plan:107 dropped it, so drift, and it aborts under `-u`. |
| X-003 severity of `./artifacts/` paths | A | 60 | B concedes (round1-B:58); plan:85 and plan:253 are executable and cause false failure or unstaged evidence. |
| X-004 Task 14/16 evidence files | A | 65 | Only A found the missing copy line (plan:242-250 vs plan:253); both missed source.md:706, B more so. |
| A-001 bullets inherit exit-0 rule | A | 55 | Both QUALIFY alike; A's condition adds the file-first form, B's `test -z "$(…)"` form passes vacuously. |
| A-002 verbatim spec copies = drift | tie | 50 | Both advocates REJECT with the same inherited/necessary rule; both cards originally mislabeled. |

Tally: A 7, B 6, tie 1. A's wins are on the higher-impact points (X-001, X-003, X-004, C-001), and B's on structure and classification. The merge should take A's defect content and B's per-finding structure, literal paths and drift labels for plan-made omissions.

## Final shared-assumption stance (A-001, A-002)

**A-001 — QUALIFY (final).**
- plan:21 does not exempt bullets. A bullet that states "exits 0" inherits the rule directly.
- A bullet that states an output criterion ("prints nothing", "prints X") is judged by that output, and must also exit 0 when it passes, because executors and `/sc:implement` QA run it as a shell check.
- plan:48 fails that condition. The merge should mark it "authorized expansion (source.md:755, plan:23), defective command form", severity important, with the file-first two-line fix from New evidence 1. It should not use `test -z "$(pipeline)"`, which hides a failing `git diff`.
- Add one sentence to plan:21 that states this bullet rule.

**A-002 — REJECT (final).**
- A plan line copied verbatim from the spec is not drift. Classify it as inherited (origin: spec), and treat its fix as a necessary deviation from the spec text. This covers R1-02 / P2R2-1 (source.md:710, tension with source.md:211), R1-05 (source.md:466), R1-07 (source.md:601, 604, 636, 675), R1-08 (source.md:649-651) and R1-09 (source.md:714).
- Plan-made divergences stay drift: plan:107 (`$E`; R1-03 relabeled), plan:86 (Leg-B guard widened without H0), the `./artifacts/` paths, plan:272/287's t16 file (contradicts source.md:706), and the plan:274-287 omission of the source.md:210 user-scope instruction.
- plan:48 is an authorized expansion with a defective form, not drift.
