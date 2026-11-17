# Round 2 rebuttal by the advocate for Variant B (slot X-13, process-redesign-modules)

Advocate: B (Recipe-Ledger-shaped). Round 2 of 2, sequential after A's Round 2. Code state: HEAD 50d4d2b9d plus the working tree, read in this worktree on 2026-11-14.
Tags: [VERIFIED] = I read it this session at the cited path:line, or ran the cited command. [UNVERIFIED] = relayed by a variant, a research file or the opponent, not re-read by me. [MY-MEASUREMENT] = a number from a script I ran this session. [MY-ARITHMETIC] = computed from verified counts. [DESIGN] = a choice, not a fact.
Files read in full first: round1-advocate-A.md, round1-advocate-B.md, round2-advocate-A.md, diff-analysis.md, variant-1-original.md, variant-2-original.md.
Code re-read this round: `findings_v2.py:60-100, 150-305`; `findings.py:36-77`; `ledger.py:7-15, 80-300, 440-484`; `verify_cmd.py:20-185`; `merge_cmd.py:60-119`; `cluster_cmd.py:105-165`; `panel.py:655-685`; `rules/prompts/document_review_loop_prompts.md:14-75`; `skills/sc-reflect-protocol/refs/reviewer-spec.md:28-79`; `skills/sc-reflect-protocol/SKILL.md:336-349`.
Searches and commands run (all under `.dev/` with `.dev/tasks/` excluded): `find` + `jq` over the 29 `precheck.json` files; `find` + `jq` over the 23 `coverage.json` files; two `uv run --no-project python -` scripts (read-only) that re-parse the reviewer cards next to each `precheck.json`; `grep` for the precheck, sidecar and loop tokens over `commands/ skills/ rules/ agents/ core/` of `src/superclaude`; `ls` of `cli/swarm/recipes/`; `grep` for `rows-v1|rowcheck|row_block` over `src/superclaude` (no hit).

## 0. Where I stand after Round 2

I keep the named hybrid and move it further toward A on mechanics, because every code claim A made that I re-read is true. In short:

1. I accept A's narrowing on C-002/X-007. `observed` computed from parsed rows has a consequence only for an EMPTY findings block (`findings_v2.py:291-298`). One finding plus zero rows is valid. The carrier is a record with one hard floor at the clean-report case, no more.
2. I drop everything in B that needs a host that does not exist: the `rowcheck: off | advisory | apply` profile value, the overlay, demotion, promotion, the `recipes` slot key. I no longer reserve `apply` in the schema; it is reserved in this document only (section 4, decision i).
3. I accept uniform per-module card binding, a per-engine row-block placement, CB-2 outside the core, and extractors reserved behind a per-class offline gate and not built now.
4. New evidence from my own re-run makes A's exactness number worse, not better: 9.9 percent per quote, 18.8 percent for a two-quote row (section 2, item d). This settles X-002 for A.
5. I hold four things. (a) The reviewer-side row block is the only thing in either variant that gives `observed` a reviewer-side source; A's R2 now agrees. (b) The row check lives in a second file so `review-precheck/1` stays byte-identical. (c) A single writer computes `observed` from parsed rows; an orchestrator must not write it. (d) The wiring of the v1 spec loop waits for a compliance spike and an RL-versus-K arm, because on v1 the row block has no hard consequence at all.

## 1. Steelman of A (short)

A's best form after Round 2: a process layer is worth its cost only where a script can decide a class, and everything else is words in a brief that arm K (a plain checklist) already supplies. A refuses every mechanism whose host is missing (merge hook, profile layer, brief renderer, slot key), refuses to let a quote check change a reviewer's typed flag, and names the measured facts that show why: 472 of 510 flags are `not-in-snapshot`, quote failures are frequent, a demoted row never reaches the Reviser brief, and the v1 loop has no precheck step to extend. A concedes the carrier and the separate rowcheck file, so what remains is small: who produces the items (cards now, scripts later), and whether names are reserved in code or only in this document.

## 2. Verification of A's new claims (a) to (g)

| # | A's claim | Verdict | Evidence |
|---|---|---|---|
| a | `findings_v2.py:291-298` consults observed rows only for an empty findings block | CONFIRMED | `parse_block` loops findings at `:264-290` and checks each line's `coverage_rows` against `assigned` only through `check_finding` (`:174-176`). The `observed` set is read once, at `:291-298`, inside `if closed and not res["errors"] and not res["findings"]`. One finding plus no rows raises no error. [VERIFIED] |
| b | Three reviewer-id spaces | CONFIRMED, with a nuance | `panel.py:668` builds `f"{slot['slot_id']}-{i}"`; `cluster_cmd.py:146` and `verify_cmd.py:124` use `card.stem`; `merge_cmd.py:86-90` takes any `REVIEWER_ID=PATH` and joins models by the same string (`:94`). In the v1 loop the merge id is the resolution id in practice (`models.get(rid)`), so the two coincide there; in reflect shadow the card stem is `reviewer-<N>` (`SKILL.md:345`) and differs. A second asymmetry A did not list: a missing sidecar entry makes `cluster` degrade silently (`coverage_context(None)` returns `(None, [])`, `findings_v2.py:202-203`, so every empty block is invalid) but makes `verify-citations` stop (`verify_cmd.py:125-128`). [VERIFIED] |
| c | A demoted row never reaches the Reviser brief | CONFIRMED | `_brief_ids` returns only rows with `blocking` true and status open or regressed (`ledger.py:99-104`). A demoted row stays in `## Other findings` (`ledger.py:467-474`) and is never repaired. [VERIFIED] |
| d | Quote-failure floor of 5.5 percent per quote from the 29 `precheck.json` files | CONFIRMED as a lower bound, and the true figure is higher | Re-ran jq: 29 files, 1,047 checked, 510 flagged: `missing-file` 472, `out-of-range` 7, `quote-not-found` 31; all 472 have reason `not-in-snapshot`. 1,047 - 472 - 7 = 568 reached the quote test (`verify_cmd.py:66-72`). A's 31 / 568 = 5.5 percent counts citations with no quote. A script that joins each precheck row to its card citation (all 568 matched) shows 313 of the 568 carry a quote and 255 do not (`quote` is optional, `verify_cmd.py:68`). So 31 / 313 = 9.9 percent per quote; for a two-quote row, 1 - (1 - 0.099)^2 = 18.8 percent if independent. [MY-MEASUREMENT, MY-ARITHMETIC] Failures are not uniform: they sit in 8 of 29 runs, from 1 of 42 (2 percent) up to 4 of 7 (57 percent) in one run, and 8 of 33 (24 percent), 5 of 23 (22 percent) in three others. The 29 runs come from two experiment families, so independence is low. A whole-file test at HEAD content (a different script) also fails 31 quotes, so line-window drift does not explain them; that second script mixes non-snapshot files and HEAD content, so I do not rely on it. |
| e | Placement sentences `:33`, `:58` against a v2 precedent | CONFIRMED | `document_review_loop_prompts.md:33` says "end the report with the findings block"; `:58` says "The last section of every review report is `## Findings block`". In v2 an after-block addition has precedent: `reviewer-spec.md:39` appends a `reviewer_model_self_report` line after the block, `SKILL.md:344` writes a fenced `yaml` calibration block after it, and `_blocks_after` keeps only fences whose info string equals the requested one (`findings.py:73`). [VERIFIED] |
| f | The v1 spec loop has no precheck, sidecar or cluster step anywhere | CONFIRMED by absence | The tokens `verify-citations`, `review cluster`, `coverage.json`, `input-snapshot` appear in only two markdown files of `src/superclaude`: `skills/sc-reflect-protocol/SKILL.md` and one unrelated sentence in `skills/sc-implement-protocol/refs/managed-workspace.md:34` about reflect's own exclusion. `review panel resolve` and `review merge` appear only in `document_review_loop_prompts.md` and the reflect skill. `commands/spec-panel.md` has no precheck, sidecar, cluster or snapshot step (its "coverage" hits are persona text, lines 139-184, 446, and a rf-qa pointer at 262). Only `commands/spec-panel.md` exists as a spec-panel command in this tree. The installed variants named in the skill list (diffgate, ledger, stoprule) are not under `src/superclaude/skills` here [UNVERIFIED beyond that absence]. |
| g | A PROBLEM row without a finding is not listed by `ledger.py:467-474` | CONFIRMED | `others = [r for r in ledger["rows"] if not r["blocking"]]`: a ledger row is created only from a parsed finding (`ledger.py:165-205`). My R1 citation `ledger.py:468` for this was wrong. [VERIFIED] |

Two new facts I add from the same reads:

- Recorded sidecars are not clean even where they are non-empty. Of the 23 `coverage.json` files, 2 have `observed` empty for all three reviewers (the `analyzeCodegraph` and `renameTheScIssue` runs) and 3 more have at least one empty entry (A's count holds). Among the 10 combo runs, `comboC-r3` has assigned 11, 13, 10 and observed 3, 2, 1; `comboA-r3` has assigned 11, 12, 7 and observed 7, 11, 6; `comboA-r2` has observed 18 against assigned 17. So an orchestrator-written `observed` is partial and not even a subset. That is the data behind "the writer must be a parser" (section 6, component 3). [MY-MEASUREMENT, jq]
- `ledger.py` imports the v1 `findings` module as `fnd` (`ledger.py:15`) and `merge_round` parses with `fnd.parse_block` (`ledger.py:128`). The reflect shadow flow never calls `merge_round`: its steps "change no verdict" and `verify-citations` and `cluster` "neither drop anything nor feed the debate" (`SKILL.md:338, :345`). This matters for A's R1 weakness 7 (below).

## 3. Responses to every criticism

Legend: ACCEPT = concede; REBUT = new evidence against; QUALIFY = true in part.

### 3.1 A's Round 1, section 4 (weaknesses 1 to 9)

| # | A's criticism | Response | Reason and evidence |
|---|---|---|---|
| 1 | Demotion is a second authority over `blocking`, against C-02 | ACCEPT in effect | Not built. New grounds beyond my R1: `ledger.py:210-213` makes the current report's typed flag the authority; `_brief_ids` (`ledger.py:99-104`) hides a demoted row from the Reviser brief. Also `SKILL.md:343` forbids the orchestrator to edit a reviewer's findings, and an overlay that lowers a flag has to change merge input (item 4 below). |
| 2 | Exactness risk is B's own number (16.5 percent) | ACCEPT, data now confirms it | 9.9 percent per quote, 18.8 percent per two-quote row on recorded data (section 2, item d). Model-dependent: 2 to 57 percent by run. No consequence may hang on an exact-match check. |
| 3 | Demotion by flag alone is invalid in v2 (`findings_v2.py:161-162`) | ACCEPT, narrowed as A narrowed it | The check sits inside `if rcat is not None` (`findings_v2.py:155-162`): true when `reflect_category` is set, not for a plain v2 line, and not in v1 (`findings.py:100-101` rejects only blocking MINOR, per A, [UNVERIFIED by me]). Moot now: demotion is not built. |
| 4 | The switch has no host; the brief renderer does not exist | ACCEPT | I conceded the renderer in R1. New: `merge_cmd.command` takes `(ledger_path, doc, round_n, reports, resolution, out, cap)` (`merge_cmd.py:71`) and hands raw text to `merge_round` (`:109`), which parses it itself (`ledger.py:128`). No place exists for a profile value or an overlay without a new option and a change in `ledger.py`. So I drop the `rowcheck` profile key altogether (section 4, decision i). |
| 5 | B's primary target (v1 loop) has no precheck to extend | ACCEPT | Verified by absence (section 2, item f). The loop needs new prose steps, not an engine hook: see A-003 in section 8. |
| 6 | B's CB-2 route cites the wrong list | ACCEPT | Section 2, item g. A reviewer-side route exists with no code: the first-review brief already tells reviewers to "list Medium and minor findings under follow-up candidates" (`document_review_loop_prompts.md:32`), so the row instruction can ask the reviewer to copy a PROBLEM row's sentence there. That is brief text for a module, not core behaviour. |
| 7 | Round-1 compliance is coupled to the quorum floor through the empty-block rule | QUALIFY | True where a quorum exists. In the v2 reflect shadow flow no merge runs and nothing is refused: an invalid card is listed by `cluster` (`cluster_cmd.py:151-162`) and the legacy debate is untouched (`SKILL.md:338, :345`). The v1 parser has no coverage rule, so on the spec loop a missing row block cannot refuse a round (`ledger.py:150-157` refuses only when no reviewer has a valid findings block). I accept A's R2 invariant 8: the consensus must say the empty-block rule is the only hard consequence. [C-03 floor text is relayed, [UNVERIFIED]] |
| 8 | Row-block placement conflicts with the brief | ACCEPT | Per-engine placement, section 4 decision (iii). |
| 9 | The per-row answer is still a self-report | ACCEPT | `ran` is unverified until the C-08 adapter. The only thing the carrier adds is that the reviewer must type each id, and the clean-report rule then fails a report that typed none. |

### 3.2 A's Round 2, sections 2 and 3 and 8 (criticisms aimed at B or at my R1)

| Item | Response | Reason |
|---|---|---|
| §2 weakness 1 narrowing (hard floor only for the empty block) | ACCEPT, with one defence | The floor sits where the cost is highest: a clean report is the case that turns into a PASS, and a reviewer who writes one finding has at least shown reading. I do not claim more than that. |
| §2 recorded sidecars (2 of 13 empty; 10 combos non-empty) | ACCEPT, refined | A's counts hold; the combo sidecars are non-empty but not full or not subsets (section 2, last bullets). Strengthens the case for a parsing writer. |
| §2 weakness 3 (uniform sheet obeys the loop's same-brief sentence `:70`) | ACCEPT | Uniform binding is the default. It also removes my need for a per-slot key. |
| §2 weakness 3b (reflect brief has exactly three sections) | ACCEPT | `reviewer-spec.md:33` fixes three sections; additions go inside them (`:39, :53-59`). The reflect row instruction therefore goes inside `## T1 card excerpt` after the excerpt, the same way the shadow findings instruction does (`:39`). |
| §2 weakness 4 (M1 measures selection recall only; no value in A's fallback) | ACCEPT | Same for my fallback unless measured; that is why G-2 and G-3 exist. |
| §2 weakness 5 (`ledger.py:3-4` is a status rule) | ACCEPT the reading, and I thank A for the replacement grounds | `ledger.py:210-213` is the right citation; it is stronger. |
| §2 weakness 6 (listing route needs a new consumer) | ACCEPT | Replaced by the brief-text route above. |
| §2 weakness 7 (per-class build burden) | ACCEPT | Nothing is built now; the unit of commitment is one extractor behind one gate. |
| §3.1 to 3.3 | ACCEPT | Section 2. |
| §3.4 overlay needs a merge hook; B's profile value has no host | ACCEPT | Dropped. |
| §3.5 re-review resurrection, plus the Reviser-brief gap | ACCEPT | I had the first half in R1; the second half (`ledger.py:99-104`) is new and makes a demoted true blocker permanent unless re-found. |
| §3.6 three id spaces | ACCEPT | A mapping is part of the writer (component 3). |
| §3.7 `recipes` collides with `cli/swarm/recipes/` | ACCEPT | `ls` shows the package with `findings_table_v1.py`, `bare_review_v1.py`, `verdict_only_v1.py`, `hypothesis_table_v1.py`, `passthrough.py`, `custom.py`, `_primitives.py`, `__init__.py`. I drop the slot key; the noun for module data is "class card". |
| §3.8, §3.9 (472 of 510; 5.5 percent) | ACCEPT, with the correction that the per-quote rate is 9.9 percent | Section 2, item d. |
| §3.10 (v2 demotion scope) | ACCEPT | Section 3.1, row 3. |
| §3.11 (placement `:33`, `:58` and v2 precedent) | ACCEPT | Section 4, decision (iii). |
| §8 invariants 1 to 15 | ACCEPT all, with additions in section 9 | I disagree with none; I rank invariant 6 (row quote length) higher in importance after the 9.9 percent figure, and I add the UNSURE-as-observed hole and the id-namespace collision. |

## 4. Where A's merged resolution and mine differ

### 4.1 The five decisions you asked for

| Decision | My answer | Why |
|---|---|---|
| (i) reserve a `rowcheck: apply` schema or profile value | NO. Reserved in this document only, behind gate G-4 | No reader exists (`merge_cmd.py:71`, `ledger.merge_round`); the profile layer is unspecified in C-03 (relayed, [UNVERIFIED]); an unread key is code for nobody (rung 1 of the ladder). A's D-3 is conceded. The real prerequisites are not a switch: per-row persistence across rounds (`ledger.py:99-104, 210-218`), a merge hook, and a severity rewrite for v2 reflect findings (`findings_v2.py:161-162`). |
| (ii) slot key now or uniform binding | Uniform per-module binding now. A slot-keyed binding is reserved in this document, named anything but `recipes`, and needs (1) a golden test of the `review panel resolve` output, (2) a decision on the `review-panel/1` hash, (3) a slot-to-card-stem map | `_SLOT_KEYS` stays closed (`panel.py:46, 214-216`, read in R1); `SKILL.md:340` requires the resolution to be the unmodified output; the loop's same-brief sentence (`:70`). Uniform binding costs me nothing the spike needs. |
| (iii) row-block placement per engine | v1: row block BEFORE the findings block, under its own heading; the findings block stays last. v2: AFTER the findings block, copied verbatim into the panel card. A truncated row block must never invalidate a complete findings block | v1: `:33` and `:58` fix the findings block as last. The price is more truncation exposure for the findings block, so rows are capped and one line each. v2: precedent at `reviewer-spec.md:39` and `SKILL.md:344`; and `_blocks_after` ignores fences with another info string (`findings.py:73`). The panel card of reflect shadow holds only the findings block and the calibration block (`SKILL.md:344`), so copying the row block into it is a prose edit of reflect step 5, which A did not price. |
| (iv) script extractors: now, reserved or dropped | RESERVED, per class, each behind its own offline gate (A's M1); NOT built now. The card schema carries no `extractor` field until one exists | Zero extractor code exists; research/10 rates the build XL [UNVERIFIED]; the ground truth for the gate does not exist. A script stays strictly better than a Grep form for C4 and C8 if it ever passes, so I do not drop the idea. |
| (v) CB-2 inside or outside the core | OUTSIDE the core | Agreement with A. No promotion; modules may ask reviewers to copy PROBLEM sentences into follow-up candidates by brief text, and a module may print the rowcheck file's PROBLEM-without-finding rows. |

### 4.2 A's numbered components, one by one

| A's component | Accept / amend / reject | Detail |
|---|---|---|
| 1 Card file format and loader | AMEND | Accept. Drop the `extractor` field until an extractor is built (a field with no reader). Keep `requires_tools` and tool-keyed `search_forms`. |
| 2 Card-to-sidecar writer, fills `assigned` only | AMEND | The same entry point must also compute `observed` from the parsed row block. If `observed` stays orchestrator-written (`SKILL.md:345`) the empty-block rule is a rubber stamp; the recorded sidecars already show the orchestrator's `observed` is partial and not a subset (section 2). It must write one entry per card, `{}` included (`verify_cmd.py:125-128`), and carry the id map (section 2, item b). |
| 3 Row block, record-only, placement per engine | ACCEPT | With the limits in section 6, component 2. A's placement split is adopted. |
| 4 Row check in a separate file `review-rowcheck/1`, advisory; reuse the normaliser; `check_skipped` rules | ACCEPT | One addition: use one of the two identical normalisers by import and pin equality by test (`verify_cmd._norm` at `:28-29` is verified; `findings.flat` is relayed [UNVERIFIED]). |
| 5 Counts-only telemetry | ACCEPT | |
| 6 Uniform binding | ACCEPT | |
| 7 Tool wall (lint) | ACCEPT | Same as my T-B5. |
| 8 Reserved: slot-keyed binding | ACCEPT | |
| 9 Reserved: extractors | ACCEPT | |
| 10 Reserved: `ran` cross-check (C-08) | ACCEPT | |
| 11 Reserved: `rowcheck: apply`; A would not reserve a schema key | ACCEPT A's position | I concede D-3 (section 7). |
| 12 Not built: demotion, promotion, CB-2 in core, changes to v1/v2/ledger/derive_verdict/contract 1.8.0, reviewer shell, class constants | ACCEPT | |
| 13 G-0 code tests | AMEND | Add: the writer rejects duplicate ids and range tokens; `observed` equals the parsed ids and nothing else; the id-map test; a truncated row fence leaves both parser results equal (T-B3 extended); a v1 report with the row block before the heading parses identically. |
| 14 G-1 per-class offline recall | ACCEPT | Applies only when an extractor exists. |
| 15 G-2 compliance spike | ACCEPT | |
| 16 G-3 arms Z0, K, RL, SS | ACCEPT | SS only for classes that passed G-1. |
| 17 G-4 before any `apply` | ACCEPT | |
| 18 Spec loop (v1) | AMEND | Wiring waits for G-2 and G-3. Until then the card text and row instruction exist only in the experiment harness. On v1 nothing computes `observed` and nothing refuses a report, so the carrier's only production value there is the checklist effect that arm K already tests (section 7, D-5). |
| 19 Tasklist and workflow via reflect UC-1 (v2) | AMEND | Accept the Coverage slice as the item host for C2. Add: class rows need an id namespace that cannot collide with requirement-row ids; the row block reaches the panel card by a verbatim copy (prose edit of reflect step 5); every assigned row must be answered or a clean report is invalid, so the burden grows on a duty the recorded sidecars show is uneven (2 of 13 reflect sidecars with zero observed rows). |
| 20 Reflect UC-2: no cards | ACCEPT | |
| 21 PR review and rf-qa reserved | ACCEPT | The OK/UNSURE/missing to `[x]`/`[?]`/`[ ]` mapping stays a design inference. |

### 4.3 Points on which A and I already agree (stated for the consensus)

1. Classes are module data; the core holds no class constants; the vocabularies at `findings_v2.py:36-48` stay untouched.
2. The reviewer-side row block exists, is record-only, and is the source of `observed`.
3. The row check is advisory and writes a second file; `review-precheck/1` and `reread_set` stay byte-identical.
4. No demotion, no promotion, no CB-2, no profile value, no overlay in the core.
5. Uniform per-module binding; no `_SLOT_KEYS` change now.
6. Tool wall by lint test; no reviewer-side shell.
7. Counts-only telemetry with a text-leak test.
8. Gates in the order: code tests, per-class offline gate, compliance spike, arms, demotion safety.
9. A-001 is a precondition for any effect claim; A-004 needs `check_skipped` outside the snapshot.

## 5. Updated positions on the 29 debate points

"Hybrid" is named in the phrase. CHANGED marks a change since my Round 1 (label or confidence), with the reason.

| ID | Position | Conf. | CHANGED? | Reason |
|---|---|---|---|---|
| S-001 | Neither | 85 | no | Order changes no behaviour. |
| S-002 | B | 60 | no | A tag column is easier to audit. |
| S-003 | B | 60 | no | An explicit "does not claim" section guards scope. |
| S-004 | Neither | 60 | no | Both list preserved and endangered invariants; B's consistency table is easier to check, A's labelled prose is as complete. |
| C-001 | Hybrid: A's card loader, one writer entry point, B's record-only row block and separate rowcheck file; no overlay, no profile value, no slot key, no precheck flags | 75 | CHANGED (60 to 75; overlay and apply reserve removed) | Merge hook missing (`merge_cmd.py:71`); verified. |
| C-002 | Hybrid: card-derived items (script-derived later), reviewer-typed rows, `observed` computed by the writer | 65 | CHANGED (B 70 to Hybrid 65) | Hard consequence only for an empty block (`findings_v2.py:291-298`); `ran` unverified. |
| C-003 | Hybrid: shared fields, `requires_tools`, tool-keyed `search_forms`; no `extractor` field yet | 70 | CHANGED (B 60 to Hybrid 70) | Both sides want the lint; an unread field is waste. |
| C-004 | B | 80 | CHANGED (65 to 80) | `_check` reaches only v2 citations (`verify_cmd.py:139-143`); a second file protects the pinned bytes (test names `:165, :176` are from both R1 files, [UNVERIFIED by me]). |
| C-005 | Hybrid: v1 loop cards plus rows, wired after G-2 and G-3; tasklist and workflow via UC-1 v2 with a copied row block; reflect default and UC-2 none; PR review and rf-qa reserved | 60 | no | Section 6, per-module list. |
| C-006 | Neither | 70 | CHANGED (B 55 to Neither 70) | The engine split is a C-01 outcome; `observed` is computed only where the v2 parser runs. |
| C-007 | Hybrid: B's code tests (extended) plus A's per-class M1 plus G-2 and G-3 arms; M-B3 only if `apply` is planned | 75 | CHANGED (70 to 75) | Code tests need no model and no harness; they run first. |
| C-008 | Hybrid: carrier plus rowcheck as the leftover, A's per-class gate for extractors | 55 | CHANGED (B 55 to Hybrid 55) | A's leftover is a loader plus card text, which is arm K with a loader; the carrier leftover is measurable. |
| C-009 | Hybrid: carrier now, extractors after M1 | 60 | no | Now-build is smaller than both R1 forms (no overlay, no slot key, no renderer, no extractors); line counts are planning values. |
| C-010 | A | 65 | CHANGED (55 to 65) | `ledger.py:467-474` verified; the brief-text route needs no builder change; promotion has no unique value. |
| C-011 | Hybrid: script for reverse-dependency and whole-tree search over untrusted diffs, card text for lens wording | 55 | no | `codegraph_callers` is in the reviewer allowlist (`reflect-reviewer.md:5`, read in R1). |
| C-012 | B | 60 | no | OK, UNSURE, missing to `[x]`, `[?]`, `[ ]` (`rf-qa.md:484-511`, read in R1) is usable; equivalence untested. |
| C-013 | Neither | 60 | CHANGED (55 to 60) | `recipes` collides with `cli/swarm/recipes/`; dropping the slot key removes the collision; `rows-v1` and `review-rowcheck/1` stay (no hit in `src/superclaude`). |
| X-001 | Hybrid: cards now, a script per class only after G-1 | 65 | CHANGED (60 to 65) | Both sides now land on A's reserved extractors. |
| X-002 | A | 85 | CHANGED (Hybrid leaning A, 60 to A, 85) | 9.9 percent per quote, 18.8 percent per row; `ledger.py:99-104, 210-218`; no host. |
| X-003 | A | 70 | CHANGED (Hybrid 55 to A 70) | A's conclusion on better grounds: `ledger.py:210-213`, `SKILL.md:343`, the fail-closed asymmetry; `ledger.py:3-4` is a status rule. |
| X-004 | Hybrid: B's tool lint and tool-keyed forms now, A's script for C4 and C8 reserved | 70 | CHANGED (B 65 to Hybrid 70) | Grep is ripgrep, not the shell dialect of the plan [UNVERIFIED equivalence]. |
| X-005 | Hybrid: uniform per-module binding now; slot-keyed binding reserved with a golden test | 65 | CHANGED (B 55 to Hybrid 65) | Section 4.1 (ii). |
| X-006 | A | 65 | CHANGED (55 to 65) | Same as C-010. |
| X-007 | Hybrid: B's record-only row block over card-derived (later script-derived) items | 60 | CHANGED (70 to 60) | Only the empty-report case has a hard consequence; `ran` unverified until C-08. |
| X-008 | A (conditional) | 55 | CHANGED (60 to 55) | A's first gate needs extractors (0 code) and ground truth (none); B's needs a model. Neither runs today; only code tests do. |
| X-009 | Neither | 60 | CHANGED (55 to 60) | Neither size is measured; both R1 core lists shrink. |
| A-001 | Neither | 80 | CHANGED (75 to 80) | Code tests need no harness; every effect claim needs X-14. |
| A-003 | Neither | 80 | CHANGED (65 to 80) | The v1 loop host has no such step (section 2, item f). |
| A-004 | Hybrid: script evidence restricted to snapshot paths (A), reviewer-typed `quote_other` outside the snapshot is `check_skipped` (B) | 75 | CHANGED (Neither to Hybrid) | 472 of 510 re-run; `_check` returns `not-in-snapshot` before any quote test (`verify_cmd.py:46-48`). |

## 6. The single best merged resolution I can defend

### Built now (all optional; with no cards declared the run equals today's run by hash)

1. Class-card format, loader and validator. Module data. Fields: `id`, `name`, `version`, `definition`, `recipe_text` (at most 120 words), `question_template`, `route`, `applies_to`, `instances`, `known_weakness`, `requires_tools`, `search_forms` keyed by tool name. No `extractor` field. No class constant in the core.
2. Row block `rows-v1`: a fenced block with its own info string, its own parser (stdlib), and its own limits. Row fields: `row`, `class`, `verdict` (OK, PROBLEM, UNSURE), optional `quote_plan`, `quote_other`, `problem`, `ran`. Limits: `quote_plan` 12 to 200 flattened characters, `quote_other` at most 200 and checked only when 12 or more, `problem` at most 300, rows at most N per reviewer (cap set by the module; fixture for 0, 1 and N). A bad row line is an error line in the parser's own output and never invalidates the findings block. Placement per section 4.1 (iii).
3. One CLI entry point `review rowcheck`, two outputs, deterministic and idempotent: (a) `panel/coverage.json` with `assigned` from the module's bound cards and `observed` computed from the parsed row ids, one entry per card or report including `{}`, with the id map between resolution id, card stem and `--report` id; (b) `panel/rowcheck.json`, schema `review-rowcheck/1`: per row `check_skipped`, `quote_plan_not_found`, `quote_other_not_found`, `rows_missing`, `rows_unsure`, plus the PROBLEM-without-finding list. Advisory only. It changes no flag, status, verdict or finding. `review-precheck/1` and `reread_set` are not touched.
4. Check rules: `quote_plan` is tested against the candidate file with the shared normaliser; `quote_other` only against a path in the input snapshot; a printed tool line, a path outside the snapshot, and any `quote_other` on the v1 loop (no snapshot) are `check_skipped`.
5. Counts-only telemetry (ids and counts: assigned, observed, problem, unsure, missing, item-linked findings, quote_not_found per reviewer) and a test that no record serialises a quote or `problem` text.
6. Binding: uniform per module. Every reviewer of a module gets the same cards; the loop's same-brief sentence (`:70`) holds.
7. Tool wall: a test fails when a card's only form needs a tool outside the bound agent's allowlist.

### Reserved (named here; no schema key, no code)

8. Slot-keyed card binding (name not `recipes`), with a golden test of the resolution output, a decision on the `review-panel/1` hash, and a slot-to-card-stem map.
9. Script extractors per class (C4 and C8 first, listers for C2 and C5), each behind its own offline gate.
10. A cross-check of `ran` against transcript tool calls (the C-08 adapter).
11. Demotion and promotion (`apply`), behind G-4 and three prerequisites: per-row persistence across rounds (`ledger.py:99-104, 210-218`), a merge hook (`merge_cmd.py:71`), a severity rewrite for v2 reflect lines (`findings_v2.py:161-162`).

### Not built

12. Demotion, promotion, a profile value, an overlay, CB-2 in the core, any change to findings v1 or v2, `review-ledger/1`, `derive_verdict`, reflect contract 1.8.0 or its 36-test matrix, any reviewer-side shell, any class constant, any precheck flag.

### Gates, in order

13. G-0 code tests, no model: `_SLOT_KEYS` and the resolve output unchanged (golden); a row fence leaves `findings.parse_block` and `findings_v2.parse_block` results identical including `ok` and `state`, for a row block before the heading (v1), after the block (v2) and truncated; card-to-tool lint; telemetry text test; no-cards byte identity of the brief files, `coverage.json` and the resolution; `review-precheck` golden bytes unchanged; the writer rejects duplicate ids and range tokens, writes an entry for every card, and sets `observed` only from parsed rows; the id-map test; normaliser equality.
14. G-1 per class, offline, only for an extractor that exists.
15. G-2 compliance spike on the plan-review package: rows missing and invalid row lines at or below a pre-registered rate (X-14's rule).
16. G-3 arms Z0 (control), K (plain checklist), RL (cards plus rows), SS (only for classes that passed G-1). RL must beat K by the pre-registered margin or K wins.
17. G-4 before any `apply` exists.

### Per-module behaviour

18. Spec review loop (v1): uniform cards, row block before the findings block, advisory rowcheck on `quote_plan` against the candidate, PROBLEM sentences copied by the reviewer into follow-up candidates. Wired in the loop's prose (`document_review_loop_prompts.md` and `commands/spec-panel.md`) only after G-2 and G-3. No consequence of any kind; `observed` is not computed by the v1 parser.
19. Tasklist and workflow via reflect UC-1 (v2): cards declared by the module (not in any packaged reflect template); class-row ids namespaced apart from requirement rows; row instruction inside `## T1 card excerpt`; verbatim copy of the row block into the panel card after the findings block; sidecar from the writer. The only hard consequence is the empty-report rule.
20. Reflect default and UC-2: no cards, byte-identical.
21. PR review and rf-qa: reserved; row verdicts map to `[x]`, `[?]`, `[ ]` as a design inference.

## 7. Disagreements that remain, and the evidence that settles each

| ID | Disagreement | Evidence that settles it |
|---|---|---|
| D-1 | Does the row duty crowd out the free review (A-002)? | G-2 and the Z0 versus RL arms. |
| D-2 | Do script-made items beat card-derived rows on C4 and C8? | G-1 and the SS versus RL arms. |
| D-3 | Reserve `apply` in the schema? | CLOSED: I concede to A (section 4.1 (i)). |
| D-4 | Placement per engine | CLOSED by agreement; T-B3 pins it. |
| D-5 | Is a row block worth shipping on the v1 loop, where `observed` is not computed and no snapshot exists? | The RL versus K arm run on the spec loop. A says wiring costs more than it returns; I say wiring is gated and the carrier costs nothing until then. |
| D-6 | Does UNSURE count as observed? I say yes, with `rows_unsure` visible; A did not decide | The `rows_unsure` rate in G-2. If it exceeds a pre-registered rate with zero findings, UNSURE stops counting. |
| D-7 | Is editing reflect step 5 to copy the row block into the panel card acceptable under the frozen contract? | `panel_lint` passes (no new top-level key, `panel_lint.py:318` per A) and the 36-test matrix passes unchanged. |

## 8. Round 2 responses to A-001, A-003, A-004

- A-001 (a harness, ground truth and the pre-registration rule exist): QUALIFY, unchanged. The code tests in G-0 need none; every effect claim needs X-14. D2 (0.12 x 14 = 1.68 items) exceeds both designs' own central shares (+1.33 and +1.05 items, [UNVERIFIED], r10); a design that meets its own estimate still fails D2, so the threshold is the owner's choice.
- A-003 (every coordinator can host one more deterministic step without a new engine hook): REJECT as stated, changed from REJECT-in-part. Advisory steps need no engine hook, but the v1 loop has no precheck, sidecar or cluster step at all (section 2, item f), so each is a new prose edit of a primitive. A step that alters merge input needs a change in `merge_cmd.py:71` and `ledger.merge_round`. Reflect already hosts such steps (`SKILL.md:345`), so that engine is fine.
- A-004 (cited evidence lies inside the input snapshot): REJECT for reviewer-typed quotes, ACCEPT for script-attached evidence made true by construction and a unit test. 472 of 510 flags are `not-in-snapshot` (re-run). On the v1 loop there is no snapshot at all, so `quote_other` is `check_skipped` there.

## 9. Invariants the consensus still leaves open

1. HIGH. The computed `observed` binds only an empty findings block (`findings_v2.py:291-298`); one finding plus zero rows is valid. The consensus must not claim the row block proves examination, and must name who reads `rows_missing`.
2. HIGH. Three reviewer-id spaces (`panel.py:668`, `cluster_cmd.py:146`, `merge_cmd.py:86-90`); a missing sidecar entry degrades `cluster` silently and stops `verify-citations` (`findings_v2.py:202-203`, `verify_cmd.py:125-128`).
3. HIGH. Quote exactness is 9.9 percent per quote and 18.8 percent per two-quote row on recorded data, 2 to 57 percent by run (8 of 29 runs have any failure). Any future consequence needs per-model data on row quotes first; the check stays advisory.
4. HIGH if `apply` is ever built, otherwise MEDIUM. A demoted row leaves the Reviser brief (`ledger.py:99-104`) and is recomputed from typed flags on a re-find (`ledger.py:213-218`).
5. MEDIUM. Orchestrator-written `observed` is partial and not a subset in recorded sidecars (comboC-r3, comboA-r3, comboA-r2); it must come only from parsed rows.
6. MEDIUM. Row-id namespace: class rows and requirement rows (Coverage slice) must not collide; every assigned row must be answered for a clean report to be valid, which raises the burden on a duty the recorded reflect sidecars show is uneven.
7. MEDIUM. UNSURE counts as observed, so an all-UNSURE clean report passes the guard; `rows_unsure` must be visible (D-6).
8. MEDIUM. v1 placement: a row block before the findings block adds truncation exposure to the findings block (`findings.py:36-77` treats an unclosed target fence as truncated); the row cap and one-line rows are the mitigation.
9. MEDIUM. Reflect needs a prose edit (verbatim copy of the row block into the panel card, `SKILL.md:344`); contract 1.8.0 and the 36-test matrix must still pass.
10. MEDIUM. The v1 loop needs prose edits of `document_review_loop_prompts.md` and `commands/spec-panel.md`; the INV-N mirror pins are [UNVERIFIED].
11. MEDIUM. Row quote limits: 12 to 200 is the citation rule (`findings_v2.py:79-80`); a short literal pattern is below 12 and needs the explicit rule in component 2.
12. MEDIUM. A Grep form of a C4 pattern is not the shell dialect of the plan (Grep is ripgrep) [UNVERIFIED equivalence].
13. MEDIUM. Extractor determinism (directory order, locale, `git grep` order) pinned by tests before any M1 means anything.
14. LOW. Zero, one and cap rows each need a fixture.
15. LOW. Line bases differ by engine; script-attached spans must use the checking engine's base (C-01 INV-009, relayed).
16. LOW. Telemetry cleanliness is a convention (`telemetry.py:3`) and needs the leak test.
17. LOW. The installed spec-panel variants named in the skill list (diffgate, ledger, stoprule) are not in this tree; the consensus should say which loop host gets the step [UNVERIFIED beyond absence].
18. LOW. rf-qa mark mapping is a design inference, not a tested equivalence.

Not re-read, relied on as relayed [UNVERIFIED]: MR2 text, research/05, 06, 13, 16, slice 06, synth-05 and synth-06 rows, test names `test_review_verify_citations.py:165, :176`, `findings.py:100-101` and `:272`, `rf-qa.md` beyond my R1 read, C-03's `min(2, requested)` floor text, INV-N mirror pins, `telemetry.py:243-251`, all planning numbers (760 versus 1,100 to 1,250 lines; the 0.835 per-row figure; +1.33 and +1.05 items).

Status: Complete
