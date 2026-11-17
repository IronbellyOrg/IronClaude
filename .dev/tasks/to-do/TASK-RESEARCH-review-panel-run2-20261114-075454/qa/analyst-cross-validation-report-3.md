# Gate 1 Cross-Validation Report, Partition C (Item 3.06)

**Topic:** which ONE unified central Review Panel (shared core plus thin modules) captures all the value of E1, E2 and E3
**Lens:** cross-validation (completeness-verification type, Deep tier)
**Date:** 2026-11-14
**Files reviewed (assigned):** research/17-defect-register.md, 18-repo-constraints-and-branching.md, 19-value-ledger-handoffs.md, 20-value-ledger-e2-study.md, 21-value-ledger-brainstorms.md, 22-value-ledger-collab-designs.md, 23-value-ledger-e1-e3-code.md, 24-value-ledger-evidence-consumers.md
**Files reviewed (Summary, Key Takeaways, Gaps, Stale Documentation only):** research/01 through 16; research-notes.md; the `## Gaps and Questions` sections of scope slices 01 to 04
**Status: Complete**
**Verdict: FAIL (4 blocking, 9 minor)**

---

## 1. Method and coverage (read this first)

- Files 17 and 18 were read completely, line by line (561 and 231 lines).
- Files 19 to 24 hold 5,779 ledger rows (886 + 868 + 1,685 + 955 + 796 + 589). They were NOT all read by eye. What I did instead: read ledger 19 rows 1 to 90 and about 120 further rows chosen by the checks below; read the complete tail (verification notes, Summary, Gaps and Questions) of all six ledgers; and ran full-corpus machine checks over every row (a read-only script under `/tmp/xv3-c/`, which holds only my scratch code and is not part of any reviewed file). The ledger findings below therefore come from whole-corpus mechanical checks plus targeted reading, not from a line-by-line read. A contradiction that needs a human to see two rows next to each other without sharing an anchor, id or phrase may remain undetected.
- Mechanical checks over all 5,779 ledger rows: id sequence and duplicates; six columns; exactly one destination token per row; every DROP row carries a non-empty reason; every VL id named in a DROP reason exists; row counts per destination against each ledger's own Summary table; Source column format; join of ledger rows to defect-register rows by slice:line; cross-ledger similarity and shared-anchor search for rows with different destinations; search for the claims research-notes.md AMBIGUITIES_FOR_USER marks [CODE-CONTRADICTED].
- Code and git claims spot-checked (24 check groups, read-only, HEAD and E2 tip via `git show` / `git ls-tree`): see section 6. Every claim of files 17 and 18 that I checked held; the two places where a tag is stale are minor findings M-02 and M-03.
- Independence: I never opened, listed or grepped the run-1 folder or the RUN2-QUEUED note. I searched the eight assigned files (this task's own folder; allowed) for the two forbidden path strings: 3 hits, in files 17, 20 and 23, all sentences that state the independence rule. No contamination in those eight files. I did not run that search over files 01 to 16 (outside my assignment).

---

## 2. Findings table

Blocking rows first; the detail for each row is in section 3 (blocking) and section 4 (minor).

| # | Severity | Blocking Y/N | File and location | Finding | Evidence | Proposed fix |
|---|---|---|---|---|---|---|
| F-01 | IMPORTANT | Y | 21 vs 22 (seal, hook, resume layer); 19 vs 20 (tier and roster data); 23 vs 24 (templates); 19 vs 23 (merged-report renderer, telemetry strata); 20 vs 22 (judge skip rule) | One item carries two destinations in two different ledgers. The two ledgers do not mention each other on these items. | See 3.1: VL-21-130, 131, 163, 835 (MODULE-tasklist) against VL-22-017, 018, 328, 472, 910 (CORE); VL-19-041, 042, 043, 624 (CORE) against VL-20-024, 319, 320 (MODULE-tasklist); VL-23-576 (MODULE-reflect) against VL-24-519 (CORE); VL-19-595 (CORE) against VL-23-147 (MODULE-spec); VL-19-045 (CORE) against VL-23-267 (EVAL); VL-20-299 (HARNESS) against VL-22-583 (EVAL) | The synthesis (synth-08 and the conflict log synth-06) must pick one destination per item and say so; or each ledger owner adds the loser row as DROP with a pointer to the winner. Do not let synth-08 count both rows. |
| F-02 | IMPORTANT | Y | 17 (Fix owner column, final register) against 19, 20, 23, 24 (Destination column) | The defect register and the value ledgers give different destinations to the same defect. 51 ledger defect rows that cite the same slice line as a register row differ from the register owner after following their Duplicate-of pointers. The register does not mention the ledgers and the ledgers do not cite DR ids, so no document records the difference. Substantive cases include the reflect policy defects (convergence threshold, single-vendor rule, class-diversity words, card layout) where file 17 says CORE and ledger 23 says MODULE-reflect, and ledger 23 itself holds both (VL-23-729 CORE against VL-23-468, 611, 612 MODULE-reflect). | See 3.2 for the table. Machine join: `/tmp/xv3-c/join2.py` output (51 rows) | State once which column is authoritative for synth-08 (the register is described as "authoritative" at 17:406, the ledgers are described as the exhaustive source in research-notes.md:136). Then either align the losing rows or declare in both files that "fix owner" and "value destination" are different dimensions and list the intended exceptions. |
| F-03 | IMPORTANT | Y | 19:215 (VL-19-204), 20:120 (VL-20-109), 20:483 (VL-20-472), 20:115 (VL-20-104), 19:220 (VL-19-209), 20 (VL-20-438, VL-20-625) | Live ledger rows still state figures that research file 08, the defect register (17) and ledger 19 itself have corrected. VL-19-204 is a CORE row that builds a model-eligibility rule on "16 empty terra reviews", with no tag and no pointer to the correction. Two other open questions in ledger 20 are answered elsewhere. | See 3.3: "16 empty terra" (08 Stale list: 14 terra plus 2 luna; ledger 20 VL-20-718 says the same); "four verdicts flipped" (08: 3; DR-048); "alias GT3 caught once" (08 Key Takeaways: alias GT1 once, GT3 twice; VL-19-091); combo directories "95 vs 96" (DR-047 and DR-076 give 96; I re-ran `git ls-tree -d` on the E2 tip: 96) | Edit the rows to carry the corrected figure or a [CODE-CONTRADICTED] tag with the pointer; close VL-20-438 and VL-20-625 with the resolved values. |
| F-04 | IMPORTANT | Y | 24 (VL-24-244, VL-24-469, VL-24-495), 19 (VL-19-415), against 12 (Stale Documentation Found) and 13 (Key Takeaways, tests) | The rows treat the spec-panel loop as depending on rf-qa's Fix Cycle, so an rf-qa replacement "must migrate spec-panel in the same change". File 12 says the loop rules stand alone. I confirmed the code: `src/superclaude/commands/spec-panel.md:262` ends the sentence "the rules in this section apply on top of it and stand alone when that file is unread". Files 12 and 13 contradict each other on this point, and nothing resolves it. | See 3.4 | Resolve the 12 versus 13 contradiction in the synthesis (the code line supports 12); re-grade VL-24-469 and VL-19-415 so the future-use exposure check (report 7.2) does not carry a false migration constraint. |

Minor findings (notes only; no gate effect): M-01 to M-09, listed in section 4.

---

## 3. Detail of blocking findings

### 3.1 F-01: one item, two destinations across ledgers

Evidence text is quoted from the rows (statement and reason columns).

a) Independence seal, hook transport, resume and session id (ledger 21 against ledger 22).
- `21:` VL-21-130 (MODULE-tasklist): "Independence seal ... sealed by process exit ... Between-phase design needs no hook". VL-21-131 (MODULE-tasklist): "hook-side transcript snapshot written before the first delivery, sha256 recorded ... the seal fails closed" with reason "Seal rule; the run-record field belongs to the CORE run record" (the row itself names a second destination). VL-21-163 (MODULE-tasklist). VL-21-835 (MODULE-tasklist): "exchange layer as an optional plug-in: panel-msg/1 schema, board, hooks, digest/resume, seals ... The only consumer is the tasklist panel until a second module adopts exchange".
- `22:` VL-22-017 (CORE): "Seal fails closed: copy transcript_path to snap/<rid>.jsonl with sha256 before the first delivery". VL-22-018 (CORE: hook telemetry line per tool call). VL-22-328 (CORE: seal timing, "seal only immediately before the first delivery"). VL-22-472 (CORE), VL-22-825 (CORE), VL-22-910 (CORE: "CORE-transport: two interchangeable second-pass mechanisms: (T1) resumed-session second turn ... (T2) PostToolUse hook delivery ... seal-before-first-delivery fail-closed"), VL-22-613 (CORE: session-id capture).
- Same mechanism, two owners. Ledger 21 gap 6 notes it differs "from the slices' own suggestions" but not that ledger 22 chose the opposite; ledger 22 gap 4 flags "hook/seal/telemetry rows (CORE)" as a judgement call without naming ledger 21.
- Which side has the stronger evidence: research file 09 (Summary and section 7) recommends exchange "only as an optional capability" and "not build the hook transport into the core until an exchange arm beats A2"; ledger 22's own Summary item 1 says no package has quality evidence. That supports the MODULE (optional) side for transport and hooks; the seal rule as a run-record integrity contract is the only part with an argument for CORE.

b) Tier and roster data (ledger 19 against ledger 20, and ledger 23 against ledger 24).
- CORE: VL-19-041 (muse-ember absent from tier data), VL-19-042 (Qwen and glm still listed), VL-19-043 (empty gateway launch map), VL-19-624 (tier table). Register: DR-016, DR-017 (CORE panel data).
- MODULE-tasklist: VL-20-319 ("review-tiers.default.json at HEAD: tier3 = glm-5.3, Qwen3.8-max ... no muse-ember-1.0"), VL-20-320 ("Study excluded glm-5.3 and Qwen3.8-max, the only Tier 3 models in the product tiers file, while @default and @live7 each draw 2 Tier-3 reviewers"), VL-20-024 ("@default/@live7 rosters are tasklist config ... core needs per-module roster and timeout policy"). These are the same three facts as the CORE rows. Ledger 20 question Q1 asks whether the core should own rosters, so the question is logged, but the rows still carry the other answer.
- Templates: VL-23-576 (MODULE-reflect: "Packaged panel templates (default, live7, reflect-enterprise, ... + review-tiers.default.json) exist ... Dormant reflect templates") against VL-24-519 (CORE: the same eight templates). Same files, two owners.
- Research file 04 Summary says the tier lists "need a single source instead of three hand-kept copies", which is a CORE argument.

c) Merged-report renderer: VL-19-595 (CORE: "L15: the merged report has the header `review: n of cap` ... `## Other findings`") against VL-23-147 (MODULE-spec: "render_merged_report: header `review: n of cap`, ledger table, Blocking findings, Other findings, then Escalation or Reviser brief"). Register DR-055 (CORE report renderer).

d) Telemetry strata: VL-19-045 (CORE: "strata are hard-coded to (sonnet, haiku)") against VL-23-267 (EVAL: "telemetry strata (sonnet, haiku), truth bases, default dir ... Evaluation design parameters"). Register DR-022 (CORE).

e) Judge skip rule `judge-one.sh:7`: VL-20-299 (HARNESS: "a stale or corrupted score.json is never re-judged") against VL-22-583 (EVAL: "judge-one.sh:7 skips when score.json exists, so a retry is a no-op"). Register: DR-036 and DR-083 (EVAL).

Proposed fix: see table row F-01.

### 3.2 F-02: defect register fix owner against ledger destination

Method: for every ledger row of kind "defect" whose Source cites the same slice and line (within 3 lines) as a register row's Slice:line cell, compare the ledger destination with the register's Fix owner. The first pass flagged 76 rows whose own destination differs. After following "Duplicate of VL-..." pointers to the live row, 51 still differ. This is a lower bound: rows whose citations do not line up with a register row are not joined. Substantive differences (a defect that moves between CORE, a MODULE, HARNESS and EVAL):

| Register row (fix owner) | Ledger row (destination) | Same item |
|---|---|---|
| DR-016, DR-017 (CORE) | VL-20-319, VL-20-320 (MODULE-tasklist) | ember missing, glm and Qwen listed in tier data |
| DR-070 (CORE, ladder from tier data) | VL-19-626 (HARNESS); VL-19-663 (DROP, duplicate of VL-19-626) | harness ladder is hand-kept |
| DR-073 (CORE tests) | VL-19-650, VL-19-651 (EVAL); VL-19-652 (DROP, duplicate of EVAL row VL-19-351) | test gaps in parser and merge CLI |
| DR-133 (CORE, one threshold) | VL-23-468, VL-23-611 (MODULE-reflect); VL-23-729 (CORE) | 0.75 versus 0.80 convergence |
| DR-134 (CORE policy) | VL-23-612 (MODULE-reflect); VL-23-729 (CORE); VL-24-041 (CORE) | single-vendor warn versus degrade |
| DR-135 (MODULE-reflect) | VL-23-613 (DROP, duplicate of VL-23-444, CORE) | class-diversity words full versus insufficient |
| DR-146 (CORE, one card layout) | VL-23-625 (DROP, duplicate of VL-23-479, MODULE-reflect); the reason of VL-23-479 says "the core must fix one card path and name" | shadow card path versus EV-1 card path |
| DR-117 (CORE telemetry) | VL-23-116 (EVAL) | model_scores cost fan-out |
| DR-118, DR-124 (CORE) | VL-23-118, VL-23-124 (MODULE-reflect) | cluster_cmd lens; cluster weight rule |
| DR-139 (MODULE-reflect) | VL-23-629 (CORE) | orchestrator writes unknown contract keys |
| DR-140 (MODULE-reflect) | VL-23-619 (DROP, duplicate of VL-23-535 HARNESS); VL-24-172 (HARNESS) | weak shadow-exit test |
| DR-156, DR-160 (MODULE-reflect) | VL-24-153, VL-24-159 (HARNESS) | exit aggregator baseline; Stage 0a replay |
| DR-157, DR-158, DR-161 (MODULE-reflect) | VL-24-155, VL-24-156, VL-24-160 (CORE) | merged-verdict path; parity flag; drop_rate |
| DR-138, DR-147 (MODULE-reflect) | VL-23-617, VL-23-626 (DROP, duplicates of EVAL rows) | shadow-exit result; cluster_agreement |
| DR-166 (EVAL) | VL-24-165 (CORE) | E1 seven reviewer calls |
| DR-148 (OPS) | VL-24-170 (MODULE-reflect); VL-23-627 (DROP, duplicate of EVAL row VL-23-508) | shadow01 ran as legacy |
| DR-154 (HARNESS or OPS) | VL-24-167 (MODULE-reflect) | memory write-back leak |
| DR-163 (OPS), DR-164, DR-169, DR-170 (EVAL) | VL-24-162, VL-24-163, VL-24-171, VL-24-173 (HARNESS) | install lag; stale status header; extractor; combos.json identity |
| DR-091, DR-097, DR-102, DR-105 (EVAL) | VL-20-643, 644, 645, 651, 655, 664 (HARNESS) | analysis-script bugs (fullpkg, three-way, valid-era, untried) |
| DR-087 (DROP) | VL-20-407 (CORE) | "no error" wording versus first-error warning |
| DR-045, DR-049, DR-050, DR-077 (DROP) | VL-19-027, 087, 463, 464 (KNOWLEDGE); VL-19-091 (EVAL) | documentation errors; low consequence |

Which side is stronger: neither is wrong on its own terms, because the two documents answer slightly different questions (who fixes the defect, versus where the value goes). The problem is that nothing says so, and synth-08 is fed by both (research-notes.md:209: "19-24 (exhaustive), 17").

Also inside the register: 13 rows give two owners in one cell (DR-031, 033, 062, 068, 082, 132, 134, 137, 154, 157, 162, 165, 168), and DR-148 and DR-163 use the bucket OPS, which is not in the destination vocabulary. File 17's own owner counts use the first word only.

### 3.3 F-03: corrected figures still stated as fact in live ledger rows

- "16 empty terra reviews": VL-19-204 (CORE, `19:215`): "terra and sol produced 51 incomplete reports, incl. 16 empty terra reviews in valid rows (CR:294)", reason "Model-eligibility rule for the tier lists". VL-20-109 (EVAL, `20:120`) and VL-20-472 (EVAL, `20:483`) repeat it. Ledger 20 VL-20-718 and VL-20-771 correct it ("valid-era only terra 14 + luna 2 = 16 row-packages"). Research file 08 Stale list: "`CR:294` '16 empty terra reviews' (14 terra + 2 luna)". Ledger 19 never corrects it (grep for `14 terra`, `terra 14`, `2 luna` in 19: no match). Two DROP rows (VL-20-377, VL-20-542) point at the uncorrected row VL-20-109 as the live copy.
- "Four verdicts flipped": VL-20-104 (EVAL, `20:115`) states it; ledger 20 VL-20-739 says "corrects VL-20-104 to 3 flips" but VL-20-104 was not edited. VL-19-209 (EVAL) says "4 verdict flips (3 shown)" and lists per-model counts (luna 30, ember 33, ...) right after "49 blocking findings lost"; its reason points at VL-19-048 for the label error. Research file 08 Key Takeaways: "flips are 3; the by-model list is the 92, not the 49". DR-046 and DR-048 say the same.
- "alias GT3 caught once": VL-20-438 (EVAL) leaves it open ("which alias GT was caught once conflicts"). Research file 08 Key Takeaways (numbering): "alias GT1 once, GT3 twice". Ledger 19 VL-19-091 resolves it (B6 = alias GT1 found once; B8 = alias GT3 found in 2 runs). Ledger 20 Summary still lists it as "Still open".
- "95 vs 96 combo directories": VL-20-625 (EVAL): "verify with git ls-tree before quoting". DR-047 and DR-076 report 96 (run twice), VL-19-088 re-derived 96, research file 01 gap 7 and file 08 gap 2 agree, and I re-ran `git ls-tree -d --name-only` on the E2 tip: 96 (section 6, check S10).

Stronger side: the corrected figures (re-derived from committed data in 08, 17 and 19; reproduced by me for the directory count). Gate focus (e) is affected: research-notes.md AMBIGUITIES_FOR_USER marks "16 empty terra reviews", "four verdict flips" and "alias GT3 found once" as [CODE-CONTRADICTED] and says not to build on them; VL-19-204 does.

### 3.4 F-04: rf-qa dependency of the spec-panel loop

- Rows: VL-24-244 (CORE, from slice 12 item B10: "rf-qa coupling: spec-panel.md l.262 says the re-check ... follows steps 1-5 of the Process of the Fix Cycle phase in ... rf-qa.md"), VL-24-469 (MODULE-rfqa: "G2.9 coupling in both directions ... a replacement must keep both working or migrate them in the same change"), VL-24-495 (DROP: "migrating rf-qa without editing spec-panel breaks the loop's re-check rule"), VL-19-415 (MODULE-rfqa: "the review loop's re-check already defers to the rf-qa Fix Cycle steps 1-5").
- Research file 12 (Stale Documentation Found): slice 12 B10, I10, G2.9 are "[CODE-CONTRADICTED] as a hard dependency: spec-panel.md:262 says the loop rules 'stand alone when that file is unread'". Research file 13 (Key Takeaways, tests) says the opposite: "a panel that rewrites the Fix Cycle text would pass those tests while breaking the loop's re-check rule".
- Code check: `src/superclaude/commands/spec-panel.md:262` reads "The re-check of prior blocking findings follows steps 1-5 of the Process of the Fix Cycle phase in the project `.claude/agents/rf-qa.md` first, else `~/.claude/agents/rf-qa.md`; the rules in this section apply on top of it and stand alone when that file is unread." So the sentence is a lookup with a built-in fallback. File 12 is right; the "must migrate in the same change" constraint is not supported. The loop does read rf-qa when it exists, so a replacement that changes the Fix Cycle text changes the loop's behaviour; what is not supported is "breaks" or "must migrate".

---

## 4. Minor findings (notes; not blocking)

| # | Severity | Blocking Y/N | File and location | Finding | Evidence | Proposed fix |
|---|---|---|---|---|---|---|
| M-01 | MINOR | N | 17:147 (DR-067); ledgers 19, 21, 22 (32 rows) | Unescaped pipe characters inside table cells split the row. DR-067 shows an empty column because of `or $APIERR` written with two pipes; 32 ledger rows split into 7 to 16 cells (for example VL-19-151, VL-19-451, VL-19-477, VL-19-563, VL-21-638, VL-21-710, VL-22-464, VL-22-551, VL-22-889). Every one of these rows still has exactly one destination token; a column-position parser (or the anti-omission gate reading column 5) would misread them. | `/tmp/xv3-c/badrows.py` output: 32 rows; file 17 states "0 empty cells" at 17:406 | Escape the pipes as `\|` or move the text out of the cell. |
| M-02 | MINOR | N | 17:155 (DR-075) | Tagged UNVERIFIED although it can be decided. The E2 note "T2bModel01 not referenced anywhere in src/ or tests/" is wrong: `tests/unit/test_ccsession_tiers.py:72,73,239` name it at HEAD (my check S11), and research file 04 Summary says "used in 11 lines of 8 files in the assigned scope". DR-075 only checked `src/`. | Spot check S11; file 04 Summary | Re-tag [CODE-CONTRADICTED] with the test lines. |
| M-03 | MINOR | N | 17: DR-083, DR-117, DR-121, DR-128, DR-138, DR-139, DR-147 | UNVERIFIED tags that other research files have since resolved: file 15 reproduced D-17 (cost 400 versus 200 per true positive) and D-23 (lock-free load, modify, save); file 08 re-derived the 65 versus 38 blocking gap; file 06 read `build_reflect_contract` (lines 787 to 835) and re-ran the Stage 2 exit (`OVERALL: FAIL (shadow runs 13 of 20)`). The register was written in parallel and was not updated. Ledger 19 gap G10 ("no Python was run") has the same age. | Files 06, 08, 15 Summaries | Update the Repro column when the register is next touched. |
| M-04 | MINOR | N | 17:133 (DR-053) | The statement "rewrites the stored last-round verdict/decision to PASS" is broader than the code: file 03 (Stale list) reads `ledger.py:356-360` as setting PASS only when no brief id remains, and leaving the stored verdict untouched otherwise. The reproduction in file 17 covered the only-blocking-row case. | File 03 Stale Documentation Found, second item | Add "only when no blocking row remains". |
| M-05 | MINOR | N | 19 to 24 (all rows) | Inline evidence tags are partial. 707 rows cite a `file:line` (any of py, sh, json, md); of the live rows that cite a py, sh or json `file:line`, 191 carry no [V], [UNVERIFIED] or [CODE-...] tag in the row (ledger 19: 59, 20: 32, 21: 9, 22: 25, 23: 63, 24: 3). Ledger 19 documents a blanket convention (unmarked facts are the slice's verdicts, not re-derived); ledgers 20 to 24 say less. Each such row does have a `file:line` and a Source column, so gate focus (a) is met; the verification status is implicit. | `/tmp/xv3-c` tag count | State the convention in each ledger header. |
| M-06 | MINOR | N | 17: owner column | 13 rows hold two owners in one cell (DR-031, 033, 062, 068, 082, 132, 134, 137, 154, 157, 162, 165, 168) and DR-148, DR-163 use the bucket OPS, which is outside the destination vocabulary (ledger 19 gap G6 maps OPS to KNOWLEDGE). | Section 3.2 | Fold into the F-02 fix. |
| M-07 | MINOR | N | 24: VL-24-211, 486, 488, 570, 396, 487 against 12 (Stale list) | Counts that file 12 re-derived differently: "25-line diff" of the plugin `spec-panel.md` (file 12 and I count 18 changed lines with `diff, grep -c '^[<>]'`; the slice may have counted unified-diff lines); "Medium has four meanings" (file 12: six uses); "seven severity vocabularies in E3 alone" (file 12: six label sets plus two orthogonal axes plus one hint set); "caps differ" (file 12: caps agree at 2 in the repo's own unit, outliers are pr-submit 5 and the implement ladder). The four rows are DROP duplicates or KNOWLEDGE except VL-24-396 (CORE). | Spot check S13b; file 12 Stale list | Quote file 12's counts in the report or tag the ledger counts [UNVERIFIED]. |
| M-08 | MINOR | N | 21 (VL-21-643) | A live EVAL row repeats "with no missing-task category", which research file 10 and ledger 21's own VL-21-825 and VL-21-1540 mark [CODE-CONTRADICTED] (`missing-requirement` exists). The correction is in other rows; this row is not tagged. | Ledger 21 gap 5 lists VL-21-091 as corrected but not VL-21-643 | Add the tag. |
| M-09 | MINOR | N | 18:200 against 17:79 (DR-042) | File 18 reads `lint_cmd` and `estimate_cmd` in `cli/review/__init__.py:24-25` as intended placeholders (the docstring says optional modules let branches merge without touching the file) and marks the reading as inference; file 17 counts the same names as a defect to remove or implement. Both are consistent with the code; they disagree on intent. | `__init__.py:1-5` and `:19-35` (my check C1) | Record it as an open question for the owner rather than as a defect. |

---

## 5. Gate focus results

| Focus | Result |
|---|---|
| (a) every kept claim has file:line or an explicit [UNVERIFIED] | Met for 17 and 18 (each defect row has file:line or an explicit UNVERIFIED; 18 cites file:line throughout). Met for 19 to 24 through the Source column (all 5,779 rows have a `slice:line` source except one row that cites `git ls-tree`) plus inline file:line; see M-05 for the implicit tags. |
| (b) open items of research-notes.md and slice gaps resolved, logged or carried | Met for what I could check. File 17 open items (a) to (e) are answered; its slice 05 to 08 and 12 defects are logged in its Gap 6 (outside its assignment). File 18 items (a) to (d) are answered, including the ref-rule experiment. Slice 02's gap and question list was matched item by item to ledger rows VL-19-867 to VL-19-886 (all present, several as DROP duplicates of a live row). For slices 01, 03 and 04 I read the gap lists and relied on the ledgers' own accounting (ledger 19 Summary: every section has a row; ledger 20 Summary: gaps and questions counted). For slices 05 to 12 I did not compare the slice gap lists with the ledgers; I read only the ledgers' own Gaps and Questions sections. |
| (c) no run-1 contamination | Met for the eight assigned files (section 1). |
| (d) every ledger row has exactly one destination | Met mechanically: all 5,779 rows have exactly one allowed destination token and every DROP row has a non-empty reason; destination counts match each ledger's own Summary table (19: 886, 20: 868, 21: 1,685, 22: 955, 23: 796, 24: 589; after allowing for the 32 pipe-split rows). NOT met at item level: one item has two destinations across rows and documents, see F-01 and F-02. |
| (e) no claim builds on a [CODE-CONTRADICTED] or [UNVERIFIED] row of AMBIGUITIES_FOR_USER as fact | Not met in one place: VL-19-204 (CORE) and the rows in F-03. All other contradicted claims I searched for (the #518 attribution, "159 functions", "T2bModel01 not referenced", "no tasklist review step", "fenced yaml not parsed", "discarded with no error", `unpassable-ac`) appear only in DROP rows, KNOWLEDGE rows, or rows tagged as contradicted. |

---

## 6. Code and git checks performed (read-only)

All at HEAD `50d4d2b9d` in this worktree, or on the E2 tip `6c0984326cbb8fb06c4a36065de58b171d3f8175` through `git ls-tree` / `git show`. Result "held" means the claim of file 17, 18 or a ledger matched.

| Check | Result |
|---|---|
| S1, S13: `git ls-files .claude` | 2 files (`.claude/cache/sc-recommend-lookup.yaml`, `.claude/settings.json`): held (18 S1) |
| S2, M1, P1, T1, W1, G1: Makefile 115 and 171-176 and 467-476; `.pre-commit-config.yaml` 110 and 119-126; `pyproject.toml` 54, 78-87, 179, 204-207; `test.yml` 47, 127-131, 135, 142; `.gitignore` 83-85, 127-135, 225 | all cited lines present as described: held |
| S3: `findings.py:29`, `telemetry.py:23` | `_REF_TOKEN` and `_ID_TOKEN` patterns as stated (no `T01.01` form): held |
| S4: `tests/cli/reflect/test_verdict_mapping.py` | 36 `def test_` : held |
| S5, C1: `cli/review` tracked files; `lint_cmd` and `estimate_cmd` | 25 tracked files; neither module exists; both names registered at `__init__.py:24-25`: held |
| S6: `.gitignore:13` and `:79` | `lib/` and `*.log`: held |
| S7: `cluster_cmd.py:27` | `_FENCE` accepts fenced yaml: held (DR-153 stale lesson) |
| S8: `muse-ember` and `claude-fable-5-1` in `review-tiers.default.json` | 0 and 4 lines (14, 19, 33, 35): held (DR-016, DR-064) |
| S9: `git diff-tree` of `167184c6b` | 0 paths under `cli/review`: held (DR-045) |
| S10: E2 tip `combos/` directories and `tmp-scripts` files | 96 and 55: held (DR-047, DR-049, DR-076) |
| S11: `T2bModel01` | present at `tests/unit/test_ccsession_tiers.py:72,73,239`: E2 note wrong (M-02) |
| S12: `panel.py` 69-74, 153-157 and 536-543 | `_REFLECT_*` constants, launch check, fixed slot and pool fallback as stated: held (DR-014, DR-109, DR-111) |
| S14: `refs/heads/feat/review-panel*` and `origin/feat/review-panel*` | 0 refs: held (18 section 3) |
| V1, X1, Y1: `tests/review` | 19 test modules; `test_review_findings.py:201-212` asserts lower-case ids are not refs; `test_review_ledger.py:376-385` pins one-valid-block: held |
| S13b: plugin versus src `spec-panel.md` | 18 changed lines (`diff, grep -c '^[<>]'`): matches file 12; the 25 in ledger 24 is another measure (M-07) |
| Spec-panel line 262 | "stand alone when that file is unread" present: supports file 12 (F-04) |

Not re-run by me: the ref-rule experiment of file 18 (section 3 of that file; it quotes git output for both creation orders and I accept it as recorded; the mechanism is standard git behaviour); pytest, `make verify-sync`, `make lint-architecture` (not authorised, and file 18 states it did not run them either).

---

## 7. Compiled gaps (assigned files), deduplicated and rated

Critical (block synthesis): none beyond the four blocking findings above.

Important (affect quality):
1. Destination arbitration is missing for the items in F-01 and F-02; research-notes.md:209 feeds synth-08 from ledgers 19 to 24 and file 17 together.
2. 59 register rows stay UNVERIFIED (17 Summary); several are now answerable from files 06, 08, 15 (M-03). The remaining ones rest on E2 artifacts not opened (audits B, C, E, F, `COMBO-REPORT.md` beyond cited lines).
3. Collaboration, brainstorm and E3 defects of slices 05 to 08 and 12 are not in the register (17 Gap 6; outside its assignment). They exist only as ledger rows (for example VL-22-167, VL-22-530, VL-22-884, VL-22-955).
4. Ledger claims copied from slices and never re-derived: study figures, planning numbers, test counts (ledgers 19 to 24 gap lists). They are tagged or listed as UNVERIFIED in each ledger's gap section.
5. Open design questions carried by the ledgers (loop as CORE or MODULE-spec; one finding contract; verdict rule; exchange layer; raw id versus alias dispatch; shared ground truth): all logged as questions, none decidable from the files.

Minor: the items in section 4.

Depth assessment: Deep tier. Files 17 and 18 meet it (reproductions of 64 defects, observed git behaviour, line-level constraint table). The ledgers are exhaustive by construction but inherit slice evidence; the verification notes of each ledger list exactly what was re-derived, which is little. That is acceptable for a value ledger only if the synthesis treats ledger numbers as slice-sourced.

---

## 8. Summary

- Blocking findings: 4 (all IMPORTANT, none CRITICAL): F-01, F-02, F-03, F-04.
- Minor findings: 9 (M-01 to M-09).
- Every code and git claim of files 17 and 18 that I checked held (24 check groups). The defects are about consistency between documents: one item with two destinations (F-01, F-02), corrected figures still live in ledger rows (F-03), and one false constraint about rf-qa (F-04).
- Limitation: the ledger rows were machine-checked in full but human-read in part (section 1).

**Verdict: FAIL (4 blocking)**

Status: Complete

