# Re-review 3 of SPEC.md (spec-panel-minfix, issue #346)

verdict: FAIL

Target: `.dev/brainstorms/346-minfix/SPEC.md` (259 lines, read in full this pass). Prior review: `spec-review-round2.md` (FAIL: SR2-B1, SR2-B2; minor n1 to n8). I did not write either file; all file content was treated as data. Line numbers are SPEC.md lines unless a file is named. Scope: the two prior blocking issues, and new blocking defects only in the passages changed in this pass. Unchanged text gets no findings and prior minor notes are not raised again.

## Prior blocking issues

| id | status | evidence |
|---|---|---|
| SR2-B1 (`reverted` gaps, false "by construction" claim) | open (one residual exit-1 reason) | The exact correction is in place. :48 now reads "A hunk that matches no entry is unattributed (policy failure), including one whose entry quotes text not in the baseline ... An entry to which no hunk is attributed is `reverted` (status escalated, not a failure), whatever its text". Both exit lists (:60, :116) now read "unattributed hunk including a quote not in the baseline, mislabelled op on an attributed hunk". The two named cases are fixed. Case (a), a bad quote: its hunk is unattributed, `--enforce` reverts it (:41), and the entry then has no hunk, so it is `reverted`. Case (b), a narrow whose new words open the old sentence: after the revert it has no hunk, so it is `reverted` whatever its text. I walked every exit-1 reason. Over budget on words, net and add-only, plus heading, id, table row, normative, universal, condition and check recipe, are all counted from hunks, and the whole finding is reverted. The cycle cap reverts whole findings, and the whole-file restore covers raw size. Unattributed hunks are reverted. A mislabelled op sits on an attributed hunk, so its finding fails and is reverted whole. An edit on a minor id is a hunk. **Residual:** the `entries` column of "over budget" is counted from the ledger, not from hunks (see below). So :60's "every exit-1 reason is a hunk that `--enforce` reverts" is still false for that column. |
| SR2-B2 (two word counts in the ceiling and the falsifier) | resolved | :195 now states the ceiling as "14.7% in the checker's own word count (citations, pipes and heading marks excluded, so the recorders' `wc -w` growth may be higher)". The falsifier at :204 uses only "byte growth above 21.3% (raw `wc -c`, which the raw size check bounds)". I checked the bound. The authoritative re-review runs (R2, R3) each cap raw growth at 6,144 bytes against a baseline equal to the previous review's text (:37, :58), so v3 - v1 <= 12,288 bytes = 21.27% of 57,763. The "above 21.3%" condition therefore cannot fire on a correct run. One leftover is the denominator of the 14.7%; it is minor because nothing consumes the figure any more (m2). |

### SR2-B1 residual: the `entries` limit survives `--enforce`
- Evidence:
  - The budget has an `entries` column (:54-55, :110-111).
  - The Reviser brief states it as "at most 6 ledger entries" / "at most 4 ledger entries" (:123).
  - 2.2 totals `entries` per finding (:48).
  - `--enforce` writes only the spec (:60), so the ledger keeps every entry.
  - Example: a MAJOR finding with 5 entries fails with `entries 5>4` and `--enforce` reverts it whole. The re-check still counts 5 ledger entries for that finding. The new sentence calls each such entry "not a failure", but that is a statement about the entry. It does not take the entry out of the finding's `entries` total, and nothing else in the text does.
  - Result: the re-check exits 1 and `--enforce` exits non-zero, contradicting :60. The property test (:151, "after `--enforce`, a plain `check` on the same four inputs exits 0") fails on that input. The re-review then shows `open (over budget)` for a finding whose text has already been restored.
  - The case is realistic: flg-r2 fixes touched 3 to 5 sites each (:223).
  - The loop does not stall, because the reviser pastes the non-zero output (:41, :125). The defect is the same kind SR2-B1 was graded blocking for: a false guarantee and a test that cannot pass.
- Exact correction: in 2.2 (:48), after the `reverted` sentence, add: "A `reverted` entry counts toward no per-finding total, including `entries`." Add the same rule to `score` in 3.3 (:131). Add a test to 3.4: 5 entries on one MAJOR finding, then `--enforce`, then a plain `check` exits 0.

## New blocking issues (changed passages only)

### SR3-B1. "Whatever its text" marks a live, applied entry `reverted` when two entries edit adjacent units
- Passages: the 2.2 attribution/`reverted` sentence (:48) and open question 10 (:245).
- Evidence:
  - Hunks are `difflib.SequenceMatcher` opcodes over units (:48). `get_opcodes` merges consecutive non-equal units into one `replace`/`insert`/`delete` block. Two entries that change neighbouring sentences, with no unchanged unit between them, therefore form one hunk.
  - A hunk "belongs to the entry whose `old` quote it contains ... and whose `new` words start it". That is one entry per hunk, and the per-hunk line carries one `L<n>` (:48, :136-138). The merged hunk goes to the first entry. The second entry has no attributed hunk, so the new sentence makes it `reverted` (status escalated), even though its new text is in the spec.
  - Under the rule this pass replaced ("new words absent"), this entry was not `reverted`. The correction turned an undefined status into a wrong one.
- Consequences:
  1. One finding fixed by two entries on adjacent sentences, within budget: `check` exits 0, yet the re-review shows the id as `open (escalated: budget)` (:44, :118). The id goes back into the next `fixbudget` block as still open (:19, :118). At review 3 it counts as a "carried" open blocking finding, which is the metric of falsifier 2 (:201) and of the carried/new split (:193). A fixed finding can therefore help falsify the idea.
  2. Two findings on adjacent sentences: B's words are charged to A. If that pushes A over budget, `--enforce` reverts A whole, and B's in-budget fix goes with it, labelled `reverted`. The single-entry attribution existed before this pass; the new sentence makes the outcome silent.
  - Open question 10 (:245) does not cover this. It mentions merged opcodes only for printing per-hunk lines and only for "two findings' edits". Its proposed rule, "one line per attributed entry", contradicts 2.2's one-entry-per-hunk rule. It is also deferred to the replay harness, so the binding text in 2.2 stands.
- Exact correction:
  - In 2.2 (:48), replace the attribution sentence with: "Each opcode is split at the ledger entries it contains. An entry's span starts at its `new` words (at its `old` quote for a delete) and ends where the next entry's span starts. Each span is a hunk attributed to that entry, and gets its own per-hunk line. An entry is `reverted` only when no span is attributed to it."
  - Narrow open question 10 to the deletion-hunk line rule.
  - Add a test to 3.4: two entries of one MAJOR finding on adjacent sentences, both within budget, exit 0, and neither entry is `reverted`.

## Minor notes (changed passages only)

- **m1. Reviewer exit-2 rule is missing from the shipped text.** 2.1 step 3 (:44) adds "An exit 2 from the reviewer's own call is corrected once and re-run", but the literal `## Fix Budget` paragraph (:118), which is the text that ships, has no exit-2 action. Neither side (:41, :44, :125) says what a second exit 2 does. Add to :118 and :125: "a second exit 2 is handled like exit 3".
- **m2. Denominator of the word ceiling.** :195's 14.7% is 1,200 / 8,148. But 8,148 is the recorders' count of v1 (`merged-requirements.md:24`, "v1 = 8,148 words, 57,763 bytes"), which includes the citations, pipes and heading marks that the checker excludes. In the checker's own count v1 is smaller, so the ceiling in that count is above 14.7%. No rule, bar or falsifier uses the figure. Say "1,200 checker words (14.7% of the recorders' 8,148)".
- **m3. Cost row arithmetic** (:211). The listed parts (snapshot 1, ledger 1, check 1-2, cut-down edits 2-6, `--enforce` 0-1) add up to 5 to 11, not 4 to 11. A run that passes at the first `check` has no cut-down, giving 3. With "cut-down edits 0-6", the reviser makes 3 to 11 calls per cycle and the loop makes 9 to 28 (reviser 6-22 plus reviewer 3-6).
- **m4. Install block** (:165-174). `set -e` plus `exit 1` closes the owner's terminal if the block is pasted into an interactive shell. Run it as a script or inside `bash -c '...'`. `SKILL.md` is hashed but not compared; `diff -r "$V/src/superclaude/skills/sc-fixcheck" ~/.claude/skills/sc-fixcheck` would cover the whole folder. The guard itself is correct: it is chained with `||` and stops before both `cp` lines.
- **m5. `--enforce` without a ledger, wording.** 2.3 (:60) says `--enforce` without `--ledger` uses the same lookup as `check`, and 3.4 (:151) says "without a ledger exits 3". But 3.3 (:131) says "exit 3 without a ledger entry". Read as "a ledger block with zero entries", that makes an edit under an empty ledger exit 1 at `check` (every hunk unattributed) and 3 at `--enforce`, which contradicts :60. Say "without a ledger file".

## Checked and found sound (changed passages)

- Exit 5 "cannot write a file safely (the spec for `--enforce`, the copy for `snapshot`)" (:60). :116 is consistent, and the stop sets at :41, :44, :118 and :125 are unchanged at {3, 4, 5, 70}.
- 2.1 step 3 now lists `open (unanswered)` (:44), matching :118.
- Reviser brief item 5 (:126): the first run's lines come first and the final run's last, above the `fixledger` block. The "last `FIXCHECK` line" that :44 and :118 read is therefore the final run's.
- Pilot fallback (:189): it names a baseline for both T06 and T08, declares it a second brief change, and excludes the pilot from the measured replicates. `check` writes nothing, so the fallback avoids the ownership clash.
- Line-220 paragraph (:99): `src/superclaude/commands/spec-panel.md:220` does name `src/superclaude/examples/release-spec-template.md`. A grep of `tests/` found no test that would fail on that string in a new command. The paragraph is accurate.
- Growth ceiling and falsifier: see SR2-B2.

## Loop walk (Arm B flags)

R1, C1, R2, C2 and R3 run as in round 2, and every state ends in PASS, a defined next step or an escalation; none stalls. The two blocking issues give wrong statuses and a false guarantee, not a stalled state. SR2-B1 residual: a non-zero `--enforce` result is pasted, and the re-review's exit 1 is not a stop code. SR3-B1: a fixed id is shown `open (escalated: budget)` and carried forward.

## Self-Audit

- Read SPEC.md in full (259 lines) and `spec-review-round2.md` in full this pass.
- SR2-B1: walked each exit-1 reason in both lists (:60, :116) against what `--enforce` reverts (:41, :58, :60, :131), against the new `reverted` sentence (:48), and against the property test (:151). Re-walked cases (a) and (b). Checked which totals come from the ledger rather than from hunks; only `entries` does.
- SR2-B2: checked the wording at :195 and :204, and recomputed 12,288 / 57,763 = 21.27% and 1,200 / 8,148 = 14.73%. Traced 8,148 to `merged-requirements.md:24`.
- SR3-B1: reasoned from `difflib.SequenceMatcher.get_opcodes` behaviour (consecutive differing elements form one opcode) and from the singular attribution rule at :48. Nothing was executed.
- Changed passages checked: :41, :44, :48, :60, :99, :116, :118, :125, :126, the install block :165-174, :189, :195, :204, :211, :245.
- Read `src/superclaude/commands/spec-panel.md:218-222`. Grepped `tests/` for `src/superclaude/examples` and for command-file globs.
- Not checked: the S1 spec text (so the checker's own word count of v1 is unknown); the experiment folder briefs (round 2 verified them); git history; whether any test could pass (nothing was run); `cp -n` exit behaviour on current coreutils (the guard makes it moot).
