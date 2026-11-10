# Re-review 2 of SPEC.md (spec-panel-minfix, issue #346)

verdict: FAIL

Target: `.dev/brainstorms/346-minfix/SPEC.md` (254 lines, read in full). Prior review: `spec-review.md` (FAIL, SR-B1 to SR-B6). The reviewer did not write either file, and all file content was treated as data. Line numbers are SPEC.md lines unless a file is named. Scope: the prior blocking issues, plus new defects only in the corrected passages. Prior minor notes are not raised again.

## Prior blocking issues

| id | status | evidence |
|---|---|---|
| SR-B1 (wrong cycle-2 baseline) | resolved | The reviser now always runs `snapshot`, and the script refuses with exit 4 when the spec's sha256 differs from `reviewed_sha256` (:37, Reviser brief item 1 at :122). The text says plainly that a re-review's `--baseline` is the previous review's copy (:37, :122), which matches D11 (`DECISIONS.md`: R2 gets v1, R3 gets v2). The re-review now also stops when the disposition's last `FIXCHECK` line shows exit 3, 4, 5 or 70 (:44, :118). The risk row now quotes T08's stricter clause (:220). The pilot covers both cycles and names a T08 fallback (:185). Walked with Arm B's flags: base-1 = v1 and base-2 = v2, so the reviser's run and the re-review's run use byte-identical baselines. |
| SR-B2 (ledger location) | resolved | The ledger's first line is `report: <file name>` (:40, :124). Without `--ledger`, the re-review finds the one matching file in the prior report's directory; none or more than one is exit 3 (:44, :118, `find_ledger` at :131). Tests are added (:151). Checked against the briefs: T05 writes `review/spec-panel.md` and T06 writes `review/disposition.md`, both in the same folder. T07/T08 write `review/spec-panel-round2.md` and `review/disposition-round2.md`. Each lookup therefore matches exactly one file, and the one-line brief substitution stays valid. |
| SR-B3 (state after `--enforce`) | resolved for the two cases it named | Case 1: an unanswered id is no longer an exit-1 reason (:48; it was dropped from the exit-1 list at :60 and :116). Case 2: a reverted entry scores `reverted` (:48). The reviser now has an action for a non-zero exit from `--enforce` (:41, :125). The property is restated (:151). One residual gap in the new `reverted` definition is filed as SR2-B1 below. |
| SR-B4 (`attacks:` not computable) | resolved | Entries are numbered `## L<n>` (:40, :124). Every hunk gets its own line `h<k> L<n>\|unattributed <id> revised:a-b +x/-y` (:48, :131, example :136-138). The reviewer takes `L<n>` from the hunk whose revised range contains the quoted line (:44, :118). A determinism test is added (:151). |
| SR-B5 (review-3 derivation) | resolved | The shapes are labelled A to E (:8). Recomputed: (2.7+1.8+1.0+0.9)/13 = 0.49. The ratios are 0.66 x (1 - 0.49 x {0.75, 0.5, 0.25}) = 0.42 / 0.50 / 0.58, and 12 x r^2 = 2.1 / 3.0 / 4.0. The baseline is 12 x 0.66^2 = 5.2, and the four 427 loops averaged 4.5 at review 3. The 3.3 is labelled a judgment adjustment and the band is labelled judgment. Arm B's R3 proxies of 6 and 1 match `phase4/ARMB-REPORT.md` (results table and bar (a)) (:193). |
| SR-B6 (growth in words, bar in bytes) | resolved as asked; a new defect in the word half is filed as SR2-B2 | The metric is M4 byte growth, the range is 8% to 21.3% in bytes, and "33.1% in words (32.1% in bytes)" is correct (:191). The falsifier has been rewritten (:200). The new raw file-size check makes the byte ceiling strict (:58, :114). Per cycle, the raw size is measured against the snapshot, and the snapshot equals the text the review saw, so two cycles add at most 12,288 bytes = 21.3% of 57,763. |

Open prior blocking issues: 0.

## New blocking issues

### SR2-B1. The new `reverted` rule does not cover every entry that `--enforce` leaves behind, so the "by construction" claim and the property test are false
- Corrected passages: 2.2 (:48), 2.3 (:60), 3.4 (:151).
- Evidence:
  - :60 claims that `--enforce` exits 0 "by construction: every exit-1 reason is a hunk that `--enforce` reverts". But two exit-1 reasons on that same list, "quote not in baseline" and "mislabelled op" (:60, :116), are properties of a ledger entry, not of a hunk. `--enforce` writes only the spec, never the ledger (:60), so those entries survive the revert.
  - :48 says an entry is `reverted` only when "its `old` or `anchor` text is intact and its `new` words are absent". Two common entries fail that test after a revert:
    - (a) An entry whose `old` quote never matched the baseline. The risk row itself names curly quotes as a cause (:218). Its `old` text is never "intact", so the entry is never `reverted`. "Quote not in baseline" still fires after `--enforce` and even after the whole-file restore, so the re-check exits 1.
    - (b) A `narrow` or `replace` entry whose first 10 new words are the start of the old sentence. Narrowing by cutting a trailing clause, the path the design prefers, produces exactly this. After the revert, the restored old sentence contains those words, so they are not "absent". The entry is then neither attributed nor `reverted`, and its status and exit effect are undefined.
  - The property test (:151) uses "random edits, random ledgers" and must hold "after `--enforce`, a plain `check` ... exits 0". A correct implementation of :48 fails it on case (a).
  - The loop does not stall. The reviser pastes the non-zero `--enforce` output (:41, :125), and the re-review's own run exits 1, which is not a stop code (:44). The defect is a false guarantee and a test that cannot pass. Under it, the re-review shows an entry of an already-escalated finding as a policy failure.
- Exact correction: in 2.2 (:48), replace the `reverted` sentence with: "An entry to which no hunk is attributed is `reverted` (status escalated, not a failure), whatever its text. A hunk that matches no entry, including one whose entry quotes text not in the baseline, is unattributed, and the report prints the reason (`quote not in baseline`) on that hunk's line." In 2.3 (:60) and in the Fix Budget exit line (:116), keep "quote not in baseline" and "mislabelled op" as exit-1 reasons only while the entry still has an attributed hunk, or fold them into "unattributed hunk". Every exit-1 reason is then a hunk, and the claim at :60 and the property at :151 hold.

### SR2-B2. The word half of the new "hard ceiling" and of the rewritten falsifier uses two different word counts, so a correct run can be voided as a checker bug
- Corrected passages: 5 growth paragraph (:191), falsifier "Not a test of the idea" (:200).
- Evidence:
  - The checker does not count `path:line` citations, pipes or heading marks as words (:48, :106).
  - The recorders' word metric is `wc -w` (flg-r2 `metrics.json` M4: "re-derived: wc -c -l -w", `words_growth_percent_cumulative_vs_v1` 33.05). `wc -w` counts every one of those tokens.
  - S1 requires "Cite path:line for every claim" (T05 to T09). Each allowed table row (one per finding, :54-55) adds about 14 pipe tokens in a 13-column table.
  - Exit 0 therefore bounds the checker's words at 1,200 net (14.7%) but not `wc -w` growth.
  - The spec's own supporting replay puts word growth at 14.4% (:191), 0.3 points under the threshold. A valid, mechanism-honouring replicate is therefore likely to show `wc -w` growth above 14.7% with exit 0. :200 would then class it "Not a test of the idea (re-run instead) ... (a checker bug)".
  - :191 calls 14.7% in words a "hard ceiling", which is false in the recorders' metric.
- Exact correction:
  - At :191, delete "and 14.7% in words", or change it to "and 14.7% in the checker's word count (citations, pipes and heading marks excluded; `wc -w` may be higher)".
  - At :200, make the falsifier "byte growth above 21.3% (raw `wc -c`, which the raw size check bounds) while the script reports exit 0 in both cycles". If a word condition is kept, it must name the checker's own word count recomputed on v1 and v3, not the recorders' `wc -w`.

## Minor notes (new, in corrected text only)

- **n1. Leftover exit-1 action.** Reviser brief item 4 (:125) still says that on exit 1 the reviser should "add the missing entry or `## deferred` line". An unanswered id no longer causes exit 1 (:48), so the `## deferred` clause never applies there, and an exit-0 run with unanswered ids prompts nothing. Separately, 2.1 step 3 (:44) lists `open (over budget)` and `open (escalated: budget)` but not `open (unanswered)`, which the literal command text has (:118). Align :44 with :118.
- **n2. Install guard does not stop.** In the block at :166-169, a failing `test ! -e ... && test ! -e ...` line does not stop the following `cp -n` and `cp -rn` lines; the stop exists only in the comment. If an agent pastes the block as one call, it silently keeps a stale `~/.claude/skills/sc-fixcheck/`, which is the risk this guard was added for. The block also prints hashes with no expected values to compare them against. Fix: chain the guard to the copies (`... || { echo stale; exit 1; }`, or `set -e`), and compare against `sha256sum` of the build files.
- **n3. Pilot fallback covers cycle 2 only.**
  - The fallback names a baseline for T08 only (:185). T06's "write ONLY your output file(s)" puts cycle 1's `snapshot` equally at risk, and open question 9 (:240) does consider naming v1 in T06. Make :185 match Q9.
  - :185 also does not say whether the pilot replicate counts as one of the two replicates. If the pilot leads to a wording change, the pilot is not comparable with the replicates that follow.
- **n4. Cost table is stale.** The cost row at :207 still reads "`snapshot` 0-1". Snapshot now runs in every cycle (:37), so it should read 1. This is a knock-on of the change; the row itself is unchanged text.
- **n5. Inherited source path in a new primitive.** Leaving line 220 unchanged (:99) means the new installed command `spec-panel-minfix.md` carries a `src/superclaude/examples/` reference. The project rule says "Do not add new references to them from a primitive" (CLAUDE.md, "Never Hardcode `src/superclaude/` Paths"). :99's "the new text adds no `src/superclaude/` path" is true only of the new regions. State it as a known inherited hit that needs owner acceptance, rather than leaving it implicit.
- **n6. Per-hunk line format gaps.** The format (:48) cannot express two cases:
  - A pure-deletion hunk has no revised line range, so a finding on the text around a deletion gets no `attacks:` value.
  - Two findings' edits in adjacent units merge into one `SequenceMatcher` opcode, but the line carries one `L<n>`. State how such a hunk is split per entry, or that it is printed once per entry.
- **n7. "Last `FIXCHECK` line" depends on paste order.** Item 5 (:126) asks for the lines of the final run "and of the first run when it was not exit 0", without an order. The ledger also sits "at the end" of the same file (:40). So which line the re-review stop rule (:44, :118) and V7 (:187, "ends with `FIXCHECK exit=0`") read depends on paste order. Say "final run last".
- **n8. Exit codes for `snapshot` and the re-review.**
  - Exit 5 is "cannot write the spec safely" (:60, :116), yet `snapshot` writes `.fixcheck/base-<N>.md`, not the spec. A failed snapshot write has no named code.
  - The re-review rules (:44, :118) give no action for exit 2 from the reviewer's own call; the reviser has "correct once".
  - :131 says "exit 3 without a ledger entry" for `--enforce`, while the test at :151 says "without a ledger". Neither says whether `--enforce` without `--ledger` uses `find_ledger`.

## Loop walk (Arm B flags, D11)

- **R1 (T05, first review).**
  - Step 0: `hash` fails, giving `E-FIXCHECK-MISSING`, an escalation.
  - PASS ends the loop. FAIL produces `fixbudget` and the Reviser brief.
- **C1 (T06).**
  - `snapshot` writes base-1 = v1. If the spec was already edited, it exits 4: paste, stop.
  - The reviser edits, then runs `check`:
    - 0: done.
    - 1: cut down once, then run `check` again: 0, or 1, then `--enforce`. `--enforce` gives 0, or non-zero: paste (SR2-B1 cases).
    - 2: correct the call once.
    - 3, 4, 5 or 70: paste.
- **R2 (T07, `--re-review review/spec-panel.md --baseline v1`).**
  - Bullets 1 and 4 run, then `check`. The baseline v1 hashes to R1's `reviewed_sha256`, and the ledger is the unique `review/disposition.md`.
  - Exit 3, 4, 5 or 70, or a disposition `FIXCHECK` line showing one of them: escalate.
  - Exit 0 or 1: the table, then `hash` and `fixbudget`, then PASS or FAIL.
- **C2 (T08).** Same as C1, with base-2 = v2.
- **R3 (T09, `--re-review review/spec-panel-round2.md --baseline v2`).** Same checks as R2, then PASS, or escalate at the cap.

Every state reaches PASS, a defined next step or an escalation. No state stalls. The exit-code lists at :41, :44, :60, :116, :118, :125, :131, :151, :187 and :200 agree on codes 0, 1, 2, 3, 4, 5 and 70 and on the stop set {3, 4, 5, 70}. The two exceptions are the gaps in n8 and the exit-1 reasons in SR2-B1.

## Self-Audit

What I read:
- SPEC.md in full (254 lines) and `spec-review.md` in full.
- From the experiment folder:
  - `DECISIONS.md` D9 to D13.
  - The brief templates T07, T08 and T09, and the task texts T05 and T06, including the output paths and ownership clauses.
  - `phase4/ARMB-REPORT.md` results.
  - flg-r2 `metrics.json` M4, where the word metric is `wc -w`.
- From `src/superclaude/commands/spec-panel.md`: the Review Loop (256-264), line 220, the section headings and the line count (486).
- `merged-requirements.md:113,441` for the word replay.
- A grep of `tests/` and the primitives for `src/superclaude/examples`.

Recomputed: 0.49, 0.42/0.50/0.58, 2.1/3.0/4.0, 5.2, 4.5, 21.3% and 14.7%. I counted `/sc:spec-panel @` occurrences: once in each of T05, T07 and T09, and none in T06 or T08.

Not checked:
- The content of 95f2c6e4 (no git).
- `nested/` artifacts.
- Whether the tests could pass; nothing was run.
- Exact coreutils `cp -n` exit behaviour.
