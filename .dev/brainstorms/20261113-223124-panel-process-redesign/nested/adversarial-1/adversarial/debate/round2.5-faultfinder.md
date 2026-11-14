# Round 2.5 invariant probe: fault-finder report

Scope: the emerging consensus on Redesign A (Sweep Sheet) and Redesign B (Recipe Ledger), checked against the six debate files, `diff-analysis.md`, the seed brief, the three variants, and the code and logs they cite. Paths: `D` = `.dev/brainstorms/20261113-223124-panel-process-redesign/nested/adversarial-1/adversarial`; `EVAL` = `.dev/eval-workspaces/tasklist-review-panel/20261111-a1`; `FIND` = `src/superclaude/cli/review/findings.py`; `MR` = `.dev/brainstorms/20261113-163248-panel-collaboration/merged-requirements.md`.

Gate chain for category 6, with the entries that attack each gate: item extraction (INV-001, INV-009) -> assignment (INV-011) -> reviewer answers (INV-004, INV-007, INV-010) -> finding line survives the merge (INV-002, INV-005) -> blind judge credit (INV-005, INV-006). The time claim is attacked in INV-003, INV-008, INV-010 and INV-012.

Recomputed numbers used below (from the matrices in `D/variant-1-original.md` 3.1(d), 3.2(d) and `D/variant-2-original.md` 3(d)):

- Matrix sums: V1-A 1.70-3.70, V2-A 1.63-3.55, V1-B 1.05-3.10, V2-B 1.25-3.10. All four reproduce the variants' own sums.
- Mean of the two matrices: A 1.665-3.625, B 1.15-3.10.
- Consensus formula, with H = 0.03 to 0.34 (central 0.14) and displacement 0.4 to 0.1: A total 3.13-5.70, mid about 4.37. B total 2.61-5.17, mid about 3.85.
- Per-issue midpoints of the mean matrix for A: B1 .29, B2 .29, B5 .26, I1 .11, I4 .625, I5 .525, B6 .16, B8 .20, I6 .19. They sum to 2.645.

---

ID: INV-001
CATEGORY: sufficiency_challenge
ASSUMPTION: An item exists in the 12-item sheet whenever its trigger shape is present ("Always extracted when the criterion carries the quantifier word", D/variant-2-original.md:164 and :173). The matrices therefore treat extraction as selection. The consensus adds a cap of 12 items with 1-2 per class, ranked by "trigger strength", with no ranking function defined.
STATUS: UNADDRESSED (the quota and the dropped-item log, round2-V1 Q3 and round2-V2 Q3, only make crowd-out visible. They do not state the selection recall, and no matrix value is conditioned on it.)
SEVERITY: HIGH
EVIDENCE: My own crude regex line counts on the two defect-rich candidates (`EVAL/TASK-WF-designSpec-20261107-075614/candidate.md`, 200 lines, and `EVAL/TASK-WF-makeTheAliasOnly-20261105-051649/candidate.md`, 134 lines). These are not extractor output. Lines with the C6 words (all, only, never, every, no other): 34 and 20. Lines with the C1 words (every, all, each, complete, exhaustive, found, covers, no remaining): 34 and 12. Lines with a backticked command-like span (C4): 55 and 16. With a cap of 2 per class, a blind pick lands on a given true-defect line with probability about 2/34 = 6% (C1 and C6 on the first plan) and 2/20 = 10% (C6 on the second). B1 and B2 are both C1 and sit in one plan; B6 and B8 are both C6 and sit in one plan (D/variant-2-original.md:26-35). Both must rank in the top 2 of one class to be asked, so the all-selected probability for a pair under a blind pick is about 1/561 and 1/190. Extraction is deterministic, so a missed item is missed in every run on that document. Per-issue reach is then a mixture (selected on this document, or reach 0 in all runs), not a per-run probability. The "consistent = reached in at least 60% of runs" measure and the bootstrap over 4 packages both hide this.
SUGGESTED RESOLUTION: Pre-register an offline selection-recall gate: before any model arm runs, the share of hold-out and planted defects whose trigger item is inside the 12 must be at least a stated floor. Log all candidates, not only the dropped ones, and publish the rank function with a test that it beats a random pick on the three derivation plans.

---

ID: INV-002
CATEGORY: state_variables
ASSUMPTION: The ledger written "first" (round2-V2: "Each reviewer writes a ledger first, then reviews freely") ends up in the report body above the findings block, where `ledger-check` and the promotion step can read it.
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: The launcher builds the report file from the final result message only: `EVAL/tools/run-reviewer.sh:50` and `.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tools/run-reviewer.sh:58` both take `[.[]|select(.type=="result")|.result]|.[0]`. A reviewer that follows "do the ledger first, then review freely" with tool calls in between writes the ledger in an earlier assistant turn. It is then absent from the report file unless the model repeats it in its last message (cheap models do not reliably copy). Redesign A's promotion step and the demotion check read the report file, so the ledger rows are lost and so is the PROBLEM verdict. Redesign B's `ledger_missing` then fires on a reviewer that did the work. I did not run the harness to measure this. It must be measured before the +35% and gain claims are trusted.
SUGGESTED RESOLUTION: Require "copy the complete ledger into your final message directly above the findings block" in the brief, have the checker read the concatenated assistant text of the transcript as well, and make the `ledger_missing` rate in the timing spike a pre-registered precondition.

---

ID: INV-003
CATEGORY: count_divergence
ASSUMPTION: Redesign A fits +35% on per-package medians because the cost is about 2 s per item for at most 12 items on a pre-pass of 6-8 s. The fallback if luna is slow is "luna's share drops to 8 items" (round2-V2.md:11).
STATUS: UNADDRESSED (a luna timing spike is promised in round2-V2.md:11, but its fallback is a no-op and the break-even values are not stated.)
SEVERITY: HIGH
EVIDENCE: Recomputed critical path for the primary panel = pre-pass + split (1) + b + sheet read (3) + 8 items x 2 + check (1). At b = 100: 8+1+100+3+16+1 = 129 s (+29%), cap 135 s, so 6 s of slack. Break-even pre-pass is 14 s, which is below the 15 s kill. A pre-pass that ends at 14.5-15 s gives 136 s (+36%) and fails, so the kill does not protect +35% on the 100 s package. Break-even per-item cost with an 8 s pre-pass is (135-100-8-1-3-1)/8 = 2.75 s, a 37% error margin on an unmeasured number. At b = 122: 8+1+122+3+16+1 = 151 s (+23.8%), cap 164.7 s, break-even per item about 3.7 s. If "2 s per item for at most 12 items" is read as 12 items on the critical path (a two-reviewer panel, INV-011), the cost is 24 s: 8+1+100+3+24+1 = 137 s, +37%. The 2 s covers only writing a row (about 75 tokens with a 200-character quote at 48 tokens/s, `D/variant-1-original.md:249`, marked UNVERIFIED). It excludes judging thinking and tool calls (luna already spends a 3.6k median thinking budget). The fallback "drops to 8 items" does nothing because luna already carries 8 (`D/variant-2-original.md:132`). The effective fallback is 6 items per luna, which forces ember to hold all 12 items (24 slots - 6 - 6) and breaks "ember search, lunas read". Statistic mismatch: the 348 s baseline is a sum of per-package slowest-reviewer means (`EVAL/COMBO-REPORT.md:204`), but D1 gates on medians 100-122. Three medians in that range sum to at most 344 < 348. The launcher's `wall_s` is per reviewer attempt (`run-reviewer.sh:58, :72`), so the pre-pass and the check are not in any measured elapsed unless a panel-level clock is added. `COMBO-REPORT.md:239` also shows that adding a second luna alone cost +47 s elapsed (max-of-two effect), so overhead variance matters beyond the per-reviewer shift.
SUGGESTED RESOLUTION: State the break-even values (pre-pass 14 s and 2.75 s per item at b = 100), set the pre-pass kill to min(15 s, 0.10 x b), define a fallback of 6 items per luna with ember taking the remainder, and measure panel elapsed with one clock that starts before the pre-pass and reports both mean and median against the same-day Z0.

---

ID: INV-004
CATEGORY: sufficiency_challenge
ASSUMPTION: "Consistently" and the headline gain. The consensus gain formula yields A about 3.1-5.7 and B about 2.6-5.2 of 14, and the consensus aim is that cheap panels find the missed issues "consistently" (60% of runs).
STATUS: UNADDRESSED (V1:313 and V2:193 flag that the upper end exceeds 4/14. Nobody tests the central estimate or the 60% threshold against the planning values.)
SEVERITY: HIGH
EVIDENCE: The central total is above the best single run ever recorded. A mid is about 4.37 (1.83 + 0.14 + 2.645 - 0.25), and the best single-run panel in `EVAL/COMBO-REPORT.md:306-309` is 4.00 of 14. This is a gain of +2.5 over a baseline of 1.83, about 2.4 times the baseline, from a script plus 8 ledger rows, on issues four of which (B1, B2, I5, I6) no one of 76 valid-era runs ever found (seed, Problem Statement). Against the 60% definition: at the planning midpoints only I4 clears 0.6 in A (0.625). I5 is 0.525 and every other in-14 issue is below 0.3. In B no issue clears it (best I4 is 0.49 = mean of V1 .425 and V2 .55). If the planning values are exactly right, an "at least +3 consistent items" gate (V2 D3) is met only when the hold-out is rich in mechanical C4/C5/C8 items. The consensus claim that A (or B) alone makes the panel "consistently" find missed issues is not supported by its own numbers; only a "sometimes" claim is. Also the judge is one Opus per (panel, package) with variance unmeasured (`COMBO-REPORT.md:71`) and one corrupted judge was already caught (`:146-148`).
SUGGESTED RESOLUTION: State the claim as "raises the per-run found fraction, with consistency expected only for the mechanical classes (C4, C5, C8)", report the planning central value without the word "consistent", and add a pre-registered check that the measured act rate for each class matches its planning midpoint within a stated band.

---

ID: INV-005
CATEGORY: interaction_effects
ASSUMPTION: A PROBLEM ledger row with no findings line can be turned into a MINOR non-blocking `src=ledger` finding by the harness, and the result survives the merge and earns judge credit.
STATUS: UNADDRESSED (V1 round 2 and the consensus add the tag and separate reporting. V1:178 notes a test is needed that extra keys are accepted. Nothing addresses the other parser gates below.)
SEVERITY: HIGH
EVIDENCE: `FIND` constraints. A second `findings-v1` block makes `ok=False` (`FIND:143-150`), so the harness must rewrite the single block, not append one. The id must match `^[A-Za-z0-9][A-Za-z0-9._-]{0,15}$` and be unique (`:92-95`). The anchor must be 12-200 characters after whitespace flattening and the claim at most 300 (`:104, :118`). A short pattern or quote (a literal such as a bare command) fails the 12-character floor and flips `ok=False` for the whole report. The category must be one of six (`:12-19`; "missing-requirement" and "other" exist). Unknown keys are not rejected by `_check_finding` (`:90-121`), so `src=ledger` itself is fine at parse level. The claim built from a ledger row is the row's 12-word "what you checked" text (`D/variant-2-original.md:114`), which describes the check, not a defect. The judge credits a finding by the defect it states, so many promoted rows will not be credited. The anchor must be locatable in the plan: `locate` (`:276-300`) flattens whitespace and `anchor_status` is "missing" when not found (`:350`). A ledger row for C2, C5 or C8 quotes the source, a root document or a test file, so its natural anchor is not in the plan. The substring check for ledger quotes must use the same `flat()` normalisation. A raw substring check demotes any quote that wraps across a plan line.
SUGGESTED RESOLUTION: Specify the promotion function as: build the line, validate it with the same `_check_finding`, take the anchor only from the plan-side quote, write the claim from the row's PROBLEM statement (not the "what you checked" field), insert it inside the existing block, and log and skip when any check fails. Use `flat()` and `locate` for every substring test.

---

ID: INV-006
CATEGORY: state_variables
ASSUMPTION: The planning gain can be the mean of the V1 and V2 per-issue matrices, because each matrix describes the consensus design.
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: The matrices describe designs the consensus has dropped. (1) V1's A uses "at most 12 items per reviewer" (diff-analysis C-001), and the consensus caps 12 items in total with 1-2 per class (round2-V1 Q3). V1's I4, I5, B1 values were set under a larger item budget and per-reviewer routing. (2) V1's B has a second fresh ember session (V1 3.2, ember pass B, which holds C6 and C4) and lens sets {C8,C5}, {C6,C4}, {C2,C3}, {C1,C7,C6}. The consensus drops the second session (round2-V1 Q5 conceded to V2, round2-V2 Q5, round2-V3 Q5) and uses V2's lens sets {C4,C5,C6,C8}, {C1,C2,C3}, {C2,C4,C7}. In the consensus B, C1, C3 live only in luna 1, C7 only in luna 2, C5, C6, C8 only in ember. V1's B6 and B8 values assumed "ember B + luna 2" replication, which no longer exists. (3) The mean also mixes a design where the sheet is "two blind judges per item" (V2) with V1's values, which V1 derives from route and replicas as data. Averaging two models of different designs gives a number that fits neither.
SUGGESTED RESOLUTION: Recompute the planning matrices once from the consensus design only (cap 12 total, one session, the V2 lens sets), label them as planning values with the selection factor from INV-001 explicit, and drop V1's matrix values from the mean.

---

ID: INV-007
CATEGORY: guard_conditions
ASSUMPTION: The deterministic quote check is a safe filter: PROBLEM rows whose quotes are not substrings of the plan, source or tool output are demoted, and ledger rows can be split into fields reliably.
STATUS: UNADDRESSED (D/variant-2-original.md:336 lists 91.4% exact quoting as a compliance risk. It does not apply it to the demotion rule.)
SEVERITY: MEDIUM
EVIDENCE: Luna quotes anchors exactly in only 91.4% of cases (`D/variant-2-original.md:336`). Blocking needs two quotes (round2-V1, round2-V2 C-018), so the chance both pass is about 0.914^2 = 0.835. About 16% of true PROBLEM rows are demoted to non-blocking before any judgement, and tool-output lines are longer and copied less exactly. The rows are pipe-separated (`D/variant-2-original.md:114, :239`: `S<id> | OK or DEFECT or UNSURE | ... | <exact quote>`; B puts the quote in the 4th of 5 fields). The plans these panels review contain markdown tables (C3 is about lookup-table rows, and `|` is the table delimiter), so a quote containing `|` shifts the fields. In B the field after the quote ("what you ran") is then misread, and the quote check cuts the quote at the first pipe. The substring test must also normalise whitespace as `locate` does (INV-005).
SUGGESTED RESOLUTION: Write the ledger as JSON lines in a fenced `ledger-v1` block (the same format the models already produce for findings-v1), parse it with a real JSON parser, test substrings with the flattened form, and report the share of demotions that were format errors, not defects.

---

ID: INV-008
CATEGORY: interaction_effects
ASSUMPTION: A hang guard of 1.5 x baseline protects against hangs without discarding legitimate slow reports, while the redesign's added seconds are judged on medians.
STATUS: UNADDRESSED (the 1.5 x guard replaces the 1.35 x kill in round2-V2 and round2-V1. Its interaction with the added overhead and with the retry loop is not examined.)
SEVERITY: MEDIUM
EVIDENCE: `MR:329`: "the largest alias run was 171 s against 1.5 x 120 = 180 s", so the guard has 9 s of headroom on the baseline tail. A redesign that adds about 29 s (INV-003) to every critical-path run pushes that run to about 200 s, which a 1.5 x 120 guard kills. Any baseline run above about 151 s (180 - 29) is lost. This is the same discard problem V2 raised against the 1.35 kill (X-005), moved to 1.5. It also depends on where the clock starts (before or after the 6-8 s pre-pass). The launcher retries the whole review when the findings fence opener is missing (`EVAL/tools/run-reviewer.sh:61-63`, `:57` tests only `^```findings-v1`; the collab script `:78-81` retries only if at least 30 s of hang budget remains), and the attempts add up in elapsed. A ledger above the block and long quotes raise the chance of a truncated or missing block, so retries may rise in the redesign arms. Kills and retries must be counted intention-to-treat or the arms are not comparable.
SUGGESTED RESOLUTION: Define the hang guard as 1.5 x (b + expected overhead) from the reviewer launch time, report kill and retry counts per arm, and score killed reviewers as zero findings in the arm total (intention-to-treat).

---

ID: INV-009
CATEGORY: sufficiency_challenge
ASSUMPTION: The planted-defect documents with clean twins show that the mechanism detects each class on fresh text (gate D5: detection at least 0.40 on 3 of 5 general classes).
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: `D/variant-2-original.md:379-382`: 6 documents with one planted defect per class, written from the class definitions "in each document's own vocabulary". A synthetic document with one instance of each class has few competing candidates, so the cap-2 quota selects the planted item almost surely, and the C1 and C6 word lexicons do not fire on dozens of unrelated lines as they do on real plans (INV-001: 34, 34 and 20 candidate lines). The planted set therefore tests the model's act rate but not selection, which is the weak gate. Quota pressure, rubber-stamping on many OK items, and displacement are all weaker than on a real plan, so D5 overstates generality.
SUGGESTED RESOLUTION: Plant defects into full-size real hold-out plans (at least 8 competing candidates per class), log candidate counts per class per document, and gate D5 on detection among documents with at least that many candidates.

---

ID: INV-010
CATEGORY: collection_boundaries
ASSUMPTION: Redesign B's lenses fit a 12-line ledger, no lens is a single point of failure that matters, and the one resume re-ask repairs a missing or malformed ledger.
STATUS: UNADDRESSED (V2:338 reports class loss by class and duplicates only C2 and C4. The ledger cap and the re-ask arithmetic are not examined.)
SEVERITY: MEDIUM
EVIDENCE: Cap conflict: the ledger rule says "Write at most 12 lines" (`D/variant-2-original.md:239`). R-C2 alone asks for up to 10 rules and traces for 3 (`:245`). Luna 1 holds C1, C2, C3, so C1 (one row per quantified criterion, unbounded), C2 (>= 10-13 rows) and C3 (one row per value) need well over 12. The cap forces the reviewer to choose rows by salience, which is the T2 failure the design was built to remove. Single points of failure: with the consensus lens sets, C5, C6 and C8 live only in ember (four recipes, one session), C1 and C3 only in luna 1, C7 only in luna 2. If ember is killed or its ledger is missing, three of the eight classes (I5, B6, B8, I7 in the ten) vanish with no replica. Re-ask arithmetic: the condition is `now + 30 s <= 1.35 x baseline` (`D/variant-2-original.md:233`). A luna ends at about b + 22. At b = 100: 122 + 30 = 152 > 135. At b = 122: 144 + 30 = 174 > 164.7. A luna never qualifies, and the re-ask can only fire for ember (ends near 81 s). The repair path does not exist for the two critical-path reviewers.
SUGGESTED RESOLUTION: Give each recipe its own row budget (a total of about 14 for a 3-recipe lens, ledger cap computed from the lens), replicate every class on two reviewers when ember has idle time, and drop the re-ask for lunas from the spec, replacing it with a logged `ledger_missing` outcome.

---

ID: INV-011
CATEGORY: count_divergence
ASSUMPTION: 12 items, each to exactly 2 of the 3 reviewers, gives about 8 items per reviewer with at most 6 for the slowest model, search items go to ember and reading items to lunas, and every item gets two independent blind judgements.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: 12 x 2 = 24 slots, 24 / 3 = 8 each. The variants' own assignments do not sum to 24: V2's primary panel has ember 9 + luna 8 + luna 8 = 25 (`D/variant-2-original.md:132`), V1's has about 10 + 8 + 8 = 26 (`D/variant-1-original.md:237`). The haiku and sonnet panels do sum to 24 (6 + 9 + 9) but then give each luna 9 items. The cap of 6 for "the slowest model" cannot apply to luna on the primary panel, where luna is the slowest (b = 100-122 against ember 41 s) and carries 8 in the time arithmetic. Applying it makes ember hold all 12 items. A search-routed item with two replicas puts its second copy on a luna, who "almost never searches" (seed). Unless the pre-pass attaches the search output (V2's extractors do, V1's C6 item asks the model to "run one search"), replicas on C5, C6, C8 are effectively 1. If one reviewer fails, "exactly 2 of 3" cannot hold: both remaining reviewers must take all 12 items (+24 s each, INV-003).
SUGGESTED RESOLUTION: Specify the assignment as an algorithm with a stated total (24 slots) and per-model caps that sum to it, allow replica 1 for items whose evidence is not attached by the pre-pass, and define the reassignment rule when a reviewer fails (drop to replica 1, no growth in the load of the others).

---

ID: INV-012
CATEGORY: state_variables
ASSUMPTION: The pre-pass can be taken off the critical path by building the sheet while reviewers do their first reads, and a pre-pass kill at 15 s still falls back to the isolated brief.
STATUS: UNADDRESSED (the option is in `D/variant-2-original.md:150`, the kill and fallback in round2-V1 and round2-V2 A-004. They are listed together without checking that they exclude each other.)
SEVERITY: MEDIUM
EVIDENCE: If reviewers start before the sheet exists, their briefs already say "the sheet appears at {{SHEET_PATH}} within 15 s; read the candidate first" (`:150`). A kill at 15 s cannot change a running reviewer's brief, so the "isolated brief" fallback is impossible. A reviewer that reads the path early gets "no such file" and may conclude there is no sheet, or reads a half-written file. The per-reviewer assignment and shuffle exist only after extraction, so the brief cannot name the items. Under the serial option the fallback works but the pre-pass is on the critical path (INV-003). Under the parallel option the fallback and the "empty sheet equals baseline hash" test (R-17) do not hold.
SUGGESTED RESOLUTION: Make the serial pre-pass the single specified mode. List the parallel mode as a separate arm with its own brief ("if the file is absent after your first read, proceed without it and record `sheet_late`"), atomic write (rename into place) and a per-reviewer path.

---

ID: INV-013
CATEGORY: guard_conditions
ASSUMPTION: Every review target has a driving document and a base commit: the brief names the source ("name the source document"), extractors read "the plan, the source and the checkout", and H3 supplies a pre-implementation snapshot.
STATUS: UNADDRESSED (V1 and V2 list "location of truth" as something to re-derive per target. The brief wording and the extractor behaviour for a missing source are not specified.)
SEVERITY: MEDIUM
EVIDENCE: The hold-out set includes a spec, a documentation set and planted documents (`D/variant-2-original.md:371-381`). None of them has a `source.md` or a parent of an "implementing commit" (H3 is defined as "the parent of its first implementing commit", `MR:317`). CB-1 ("Driving document: {{SOURCE_ABS}}. Read it in full") would render with an empty or non-existent path. The C2 extractor (source rules not in the plan) has no input and either emits nothing or items about nothing. `EVAL/tools/run-reviewer.sh:10-11` treats the source as optional (`|| true`). The reflect and "artifacts" leak removal (H4) is also undefined for documents with no package folder. `D/variant-2-original.md:382` also says that equality of the base commit with the reviewed plan is UNVERIFIED and "must be done first".
SUGGESTED RESOLUTION: Render CB-1 and the C2 extractor only when a source file exists, log `no_source` and count C2 as not applicable in that document's metrics, and define the snapshot rule for documents without a commit (use the working tree and record it).

---

ID: INV-014
CATEGORY: interaction_effects
ASSUMPTION: Item questions displace baseline-found issues by a flat 0.1 to 0.4 of 14, and replicating items across two reviewers costs nothing else.
STATUS: UNADDRESSED (V1:350 and REQ-33 measure non-probe findings per run, and V2 D6 sets a non-regression gate. Those handle measurement. The planning range is still asserted as flat.)
SEVERITY: MEDIUM
EVIDENCE: The baseline 1.83 is a union over three reviewers whose free-review attention is diverse (luna run-to-run Jaccard 0.12 on one package, `D/variant-2-original.md:18`). With 12 items each going to 2 of 3 reviewers, every item a reviewer holds is also held by exactly one other reviewer, so the shared item attention replaces some of the independent salience that produced the union (24 slots cover only 12 distinct questions). V1:350 itself lists "Sheet anchors reviewers on items only | free-review findings fall". The displacement range 0.1-0.4 equals 5-22% of 1.83, a figure chosen without a measurement. If the sheet removes half the free-review finds (about 0.9), the central gain in INV-004 drops by about 0.65. The ledger tokens add 25-42% output tokens (`D/variant-2-original.md:197`), a further sign of crowding.
SUGGESTED RESOLUTION: Report displacement as a measured quantity with a planning range of 0.1 to 0.9 until Z0 versus A is observed, reserve a free-review floor in the brief (for example "keep at least half your time for your own review"), and keep the D6 non-regression gate as a blocking gate.
