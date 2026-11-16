<!-- Provenance: this verdict was merged by the orchestrator (main Sonnet session) from /sc:adversarial artifacts in adversarial/ -->
<!-- Base: V3 (sonnet:architect), amended with V1's no-source finding, V2's note list and the fault-finder's process gaps; see adversarial/base-selection.md -->
# Verdict: K-arm lead-in (DESIGN.md DD-14, 15.1 row 4)

## 1. Verdict: PASS

No blocking defect survived the debate. The default stands: approve `briefs/k-lead.txt` as drafted. All three advocates ended on NO to "is the default blocking" (the Sonnet prosecutor started on NO and held it after trying to break it). The fault-finder found 14 items and none is HIGH. A PASS changes no file, and no file outside this folder was changed.

The draft is not perfect. It has no verb telling the reviewer to apply the eight checks, it says "in your own review" next to a rule that keeps the checks apart from the reviewer's own review, and it was never run on any model. Those are notes in section 4, not defects under the verdict rule: none can be shown to make the experiment unfair, unmeasurable or misleading, and the fixes tried each move K in an unmeasured direction.

Text approved (line 2 of `briefs/k-lead.txt`, 151 characters, 33 words): "Eight kinds of defect to look for in your own review of the plan. Each one says what to look for. A plan may have none of them, one of them or several."

## 2. Surviving blocking defects

None. The verdict rule has four tests; each was attacked and none produced a blocking defect.

| Test | Result | Evidence |
|---|---|---|
| Unfair to an arm | Not shown | The draft is the owner's definition of K: "Z0 plus one paragraph naming the eight checks in plain words. No recipes, no sheet, no ledger" (MR 1035). K lists all eight class definitions, which the SS sheet never prints (the sheet shows an id, a location, the text, tool lines and a question: DESIGN 6.1 to 6.3). Direction of any bias is not established: "to look for" is already an instruction, and the cheapest fix ("Apply each one to the plan") would move K toward SS (MR 36, 1100). |
| Unmeasurable | No, for what the experiment claims | K runs on the same four documents, judge and clock as Z0 and SS (MR 5.4). Found fraction is computed the same way for every arm (`analysis/analyze.py` 253-254). What no spike measures is the lead-in's own effect: no real-model K run exists and none of the planned spikes runs K (DESIGN 14.2). That is true of every wording of K, so it is a limit, not a hole in the comparison. |
| Misleading | Not as drafted | REQ-40 reports K minus Z0 apart from the SS share (MR 1194; DESIGN 788). The reading rule in section 4 (N10) closes the one way a reader could over-read K. |
| Breaks a stated requirement | No | REQ-05 covers CB-1 to CB-5 only, and the lead-in is not a CB. REQ-23 concerns an empty-sheet SS brief, which has no K text. MR 1035 holds: the generated paragraph is one line, eight definitions in card order, no recipe, sheet or ledger (`tests/test_briefs.py` 187-204). REQ-33 order holds: decide at 14.3, freeze at 14.5, hold-out ground truth at 14.6 (IMPLEMENTATION.md 154-167). |

**The closest attacks, and why each failed.**
- *A soft K flatters SS at gate D7.* Derived arithmetic (not measured): if D2 passes (SS minus Z0 at least 0.12), D7 (SS minus K at least 0.04) fails only if K minus Z0 exceeds about 0.08. The study's own prior says a plain checklist does little (MR 120), so D7 rarely decides anything. The direction is unproven: V3 first named it, then withdrew it because no neutral wording exists. The arithmetic is exact only if D2 and D7 run on the same run sets (INV-007). Size: UNVERIFIED.
- *Definition (2) is printed where no source document exists.* Real, but it is a reporting gap for every arm: `analysis/analyze.py` has no read of `no_source` or "not applicable" (zero hits), although the design records them in `run.json` and `prepass.json` (DESIGN 273, 549, 563; `tests/test_prepass_inputs.py` 132). D2 and D7 read found fraction only. All three derivation packages have a source (`config/packages.json`); the hold-out list is not in this folder, so whether any decision document has `source: null` is UNVERIFIED.
- *"in your own review" against CB-5.* Two opposite readings (the checks sit inside the protected half of the time, or beside it), so no direction. CB-5 is verbatim by REQ-05.

## 3. The five attack questions, answered

**Q1. Is K a fair, strong control or a strawman?** Fair, and not a strawman. It is the owner's K, and it names every class. It is soft in two places (no apply verb; the "own review" wording) but the direction cannot be shown and a stronger wording is as untested as the draft. Not blocking.

**Q2. Does the lead-in leak anything about the hold-out answers?** No. Line 2 carries no document text and no class name; it discloses only the number "eight", which SS also implies. The eight definitions are class-level card text, frozen with the briefs before the hold-out ground truth is written (MR 1026; `bin/freeze.sh` 43). Two limits: approving line 2 does not approve the definitions (every `swap_test` is empty until step 14.2), and nothing ties the approval to bytes (N1). Not blocking.

**Q3. Does it differ in length or tone from the SS brief in a way that confounds?** It differs, and the difference is the treatment. K adds 1,226 characters (the paragraph is 1,224). SS adds 1,712 characters with a one-item dummy sheet, and a real sheet can run to 16,000 (DESIGN 6.3). K is descriptive; SS is imperative ("Do not skip an item", "Answer PROBLEM only when you can quote..."). Equalising them would make a different arm. The length risk MR names (934) is the recipe arm's. Not blocking.

**Q4. Does "a plan may have none" discourage findings?** Not materially. The base brief already says "not a minimum number of findings", CB-2 says "Do not leave a defect out because it looks small", and SS carries the stronger sentence ("Most items are fine"). If it has any effect it lowers K and so flatters SS; size UNVERIFIED. Every K document has at least 4 known items (MR 135-138), so the sentence describes none of them, but it says "may", which is true in general. Not blocking.

**Q5. Is the generated paragraph equivalent in information to what SS gives?** No, by design. K gives all eight definitions and no places, text, tool output, question or forced verdict. SS gives those for the triggered classes (at most 12 items) and prints no definitions. That gap is what D7 measures. One more difference: on a plan with a source, CB-1 in Z0 already says "A rule it states that the candidate does not carry is a finding", which is definition (2), so K adds seven checks net, not eight (INV-011). Not blocking.

## 4. Non-blocking notes

- **N1. Nothing ties the approval to bytes.** `briefs/` and `cards/` are untracked in git (`git status` shows `??`), the owner record has no hash field, and `bin/freeze.sh` hashes whatever is committed on the day (it refuses uncommitted files, exit 3, but compares nothing with an approved hash). The file today is 269 bytes, sha256 `6712596b3c8d3e60ad8edb86755613ca9b12550f2198d04d303e1e68019afb57`. `analysis/analyze.py` never reads the brief, freeze tag or registry version (zero hits), so "frozen before K runs" holds by procedure only (INV-001, INV-002).
- **N2. The draft marker stays in the frozen file.** Line 1 says "DRAFT, awaiting owner approval". `tests/test_briefs.py` 196-198 pins it, so approval does not remove it. It is never sent to a reviewer.
- **N3. No apply verb.** The draft says "to look for in your own review"; V3's alternative adds "Apply each one to the plan", which is untested and moves K toward SS-lite.
- **N4. "in your own review" beside CB-5, and the word "checks" is absent.** CB-5 says "The checks you were given do not replace your own review" and comes before the K paragraph; MR 1035 calls them "checks". SS states its separation outright (`sheet-block.txt`); K's is implicit.
- **N5. Definition (2) with no source, and the analysis ignores `no_source` for all arms** (section 2). Check the hold-out packages for `source: null` before step 14.5.
- **N6. The shared control with RL has no drift check.** `briefs/k-lead.txt` and all eight card definitions are identical in RL today (checked with `cmp` and `jq`). RL records hashes at copy time and nothing compares later edits. A swap-test edit on one side only would split K without any test failing (INV-004).
- **N7. No real-model K run exists, and no planned spike runs K.** Counted runs are never repeated and a reviewer with no usable findings block scores zero (DESIGN 566). A K-specific format problem would show only in counted data (INV-013). An optional five-run K panel on the sanity set before the freeze would settle it; it needs the owner's go-ahead.
- **N8. D7 is a bare point difference (at least 0.04, no interval) on about 36-40 items.** That is a property of MR 1091, not of the lead-in (INV-009). The "0.08" arithmetic assumes equal run sets for D2 and D7 (INV-007), and a run with an unavailable or killed reviewer lowers that arm's found fraction for a reason unrelated to the brief (INV-006).
- **N9. "Eight" is hard-coded.** `tests/test_briefs.py` 190 asserts exactly eight cards, so a ninth card fails a test. DESIGN 724 and `cards/README.md` step 3 say a new class "still enters the arm K paragraph" and need no other change, which leaves out the lead-in word and that test line.
- **N10. Reading rule for the report (advice).** Read K minus Z0 as the effect of this one paragraph as frozen (the approved lead-in plus the eight definitions), not as the most a plain checklist could add; no real-model K run exists and the wording was not tuned. Read SS minus K as the effect of everything SS adds over definitions alone (places, quoted text, search results, a question and a forced verdict per item, the ledger), not as the effect of automation alone.
- **N11. K ends the brief on definition (8) with no closing directive; SS ends on a per-item directive.** This is the treatment. It is also the one K-specific format risk in N7.
- **N12. The blind judge may see arm-revealing text in K reports** ("(4)", "eight kinds"); `bin/anon.sh` removes paths, run, reviewer and model names only. The effect is probably small (the judge matches defects, not arms) and nobody checked it (INV-012).
- **N13. Recommended records if the owner approves (advice only; a PASS changes no file).** In `results/owner-decisions.md`: the sha256 and size above, the words "line 2 only; the eight definitions stay open until step 14.5", and the date. Before step 14.5: `cmp` the SW and RL copies of `briefs/k-lead.txt` and of the eight card definitions, and check the hold-out packages for `source: null`. Decide this together with CB-2 at step 14.3 (debate 2, N6).

## 5. Refactored value, files changed and test run

- Refactored value: not applicable (PASS).
- Files changed: none outside this output folder. The four files this task could edit were not touched: `briefs/k-lead.txt` (modified 2026-11-14 21:21), `DESIGN.md` (2026-11-15 04:00:43), `results/owner-decisions.md` (04:00:50), `tests/test_briefs.py` (2026-11-15 00:57); a search for files newer than the debate's first artifact (04:39) found nothing outside this folder except the code-index database files, which a background watcher maintains. Nothing was staged, committed or pushed (no staged path matches this folder or the four files).
- Test run: not run. The instruction to run `pytest ... -m 'not freeze'` applies on FAIL; a PASS changes no file, so there is nothing to test.
- Owner status: the owner has not confirmed row 4. If the owner confirms it, record the confirmation in `results/owner-decisions.md` (not done here, because a PASS changes no file).

## 6. How the debate was run, and its limits

- Advocates: Haiku defender (V1), Sonnet prosecutor (V2), Sonnet architect (V3); one Sonnet fault-finder for Round 2.5. Depth standard (Round 1, Round 2, Round 2.5). No Opus.
- The orchestration and the merge were done by the main Sonnet session, not by the `debate-orchestrator` and `merge-executor` agents (which prefer Opus). Scoring was condensed (`adversarial/base-selection.md`), because a dual pass by the orchestrating session would not be independent. There was no Round 3 at standard depth. Return contract status: partial.
- The Round 1 agents could not be resumed ("No transcript found"), so the Round 2 advocates were fresh agents that re-read their own Round 1 statement and the others. Round 2 ran in sequence (V1, V2, V3) as the protocol asks.
- The orchestrator's own evidence had seven corrections (`adversarial/work/corrections.md`). The largest: DESIGN 273 and 563 treat a no-source plan as a designed case (CORR-2), and `analysis/analyze.py` never reads that mark (CORR-7, found by V1 and confirmed by grep). None changed the verdict.
- Convergence was 13 of 13 points (100%). That is weak evidence on its own: all three advocates share one untested premise, that no real-model K run exists (A-001), and unanimity came in Round 1.
- No `ground-truth*.json` or score file was opened by the orchestrator. Every advocate and the fault-finder was told in writing not to open one. The advocates' transcripts are not kept on disk (the task output files do not exist), so that part rests on the written prohibition and on the output folder holding only the expected files.
- UNVERIFIED throughout: any effect of the wording on found fraction, finding count, time or format failures; whether any hold-out plan has no source document; every planning figure quoted from MR.
- Artifacts: `adversarial/` (`variant-1-haiku-defender.md`, `variant-2-sonnet-prosecutor.md`, `variant-3-sonnet-architect.md`, `diff-analysis.md`, `debate/` with `round2-V1.md`, `round2-V2.md`, `round2-V3.md`, `orchestrator-note-round2.md` and `invariant-probe.md`, `debate-transcript.md`, `base-selection.md`, `refactor-plan.md`, `merge-log.md`, `return-contract.yaml`, `work/evidence-pack.md`, `work/corrections.md`, `work/render_k.py`, `work/render_k.out`).
