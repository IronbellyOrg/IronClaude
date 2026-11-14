# Step 3, quantitative layer: five alignment reviews (V1 to V5)

Generated 2026-11-14 by the Step 3 quantitative scorer (read-only on the review folder; this file is the only thing written). Protocol: `~/.claude/skills/sc-adversarial-protocol/refs/scoring-protocol.md` section A.1. Folder D = `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/adversarial/`. Variants: `variant-1-original.md` to `variant-5-original.md`. Script: `/tmp/step3_quant.py` (standard library only, run with `uv run python /tmp/step3_quant.py`); full text in section 7, full output in section 8.

## 1. Result

`quant_score = 0.30 RC + 0.25 IC + 0.15 SR + 0.15 DC + 0.15 SC`. RC is the mean of RC against the whole requirement list and RC against the requirement the variant was meant to serve (section 3).

| variant | subject | RC | IC | SR | DC | SC | quant_score | rank |
|---|---|---|---|---|---|---|---|---|
| V1 | #409 TUI observer issue vs the sweep | 0.789 | 0.972 | 0.706 | 1.000 | 0.750 | **0.848** | 5 |
| V2 | #450 issue watcher rollout | 0.944 | 1.000 | 0.820 | 1.000 | 0.750 | **0.919** | 3 |
| V3 | Coder#477 workspace listener | 0.889 | 0.966 | 0.700 | 1.000 | 0.750 | **0.876** | 4 |
| V4 | #423 Orchestrator v2 and the #339 boundary | 1.000 | 0.970 | 0.788 | 1.000 | 0.750 | **0.923** | 2 |
| V5 | the built `superclaude observe` vs the sweep | 0.889 | 0.987 | 0.775 | 1.000 | 1.000 | **0.930** | 1 |

Reading it: V5, V4 and V2 sit within 0.011 of each other, which is inside the noise of these proxies (section 5 shows the order of V5 and V4 flips with the RC thresholds). V3 and V1 are lower in every threshold scenario tried. DC is 1.000 for all five and IC is 0.966 to 1.000 for all five, so neither separates anything; the spread comes from RC, SR and SC.

Five quant scores, in order V1 to V5: **0.848, 0.919, 0.876, 0.923, 0.930**.

## 2. Survival rate (reported separately from the quant score)

Survival rate = share of a variant's numbered findings that were not withdrawn by Round 2. "Numbered findings" are the rows the variant numbered: V1 C-01..C-39, F-01..F-18, A-01..A-15 (72); V2 W-01..W-16 (16); V3 CC-1..CC-12 (its eight path rows, three related-issue claims and the "Not known yet" Out of Scope line, in file order) plus F1..F17 (29); V4 C1..C11 and F1..F22 (33); V5 S1..S10 (its ten "what the observer is today" parts), O-01..O-16, RT-F01..RT-F18 (its re-test rows), BC-01..BC-23 (its numbered body corrections) and D1..D9 (76). The script asserts these counts.

Two measures: **strict** counts only items withdrawn in full as lost; **weighted** also counts an item that its own advocate narrowed, reworded or re-grounded (premise corrected, claim kept in smaller form) as half lost.

| variant | numbered findings | withdrawn in full | narrowed | strict survival | weighted survival | alignment findings only (strict / weighted) | including numbered proposals (strict / weighted) |
|---|---|---|---|---|---|---|---|
| V1 | 72 | 8 | 7 | **0.889** | **0.840** | 0.879 / 0.788 (n=33) | 0.886 / 0.823 (+7 wording items) |
| V2 | 16 | 0 | 3 | **1.000** | **0.906** | 1.000 / 0.906 (n=16) | 1.000 / 0.905 (+5 edits) |
| V3 | 29 | 0 | 0 | **1.000** | **1.000** | 1.000 / 1.000 (n=17) | 0.951 / 0.927 (+12 edits) |
| V4 | 33 | 1 | 10 | **0.970** | **0.818** | 1.000 / 0.795 (n=22) | 0.958 / 0.812 (+15 edits) |
| V5 | 76 | 2 | 5 | **0.974** | **0.941** | 0.970 / 0.932 (n=66) | 0.974 / 0.941 (BC and D already inside the 76) |

Which items, and where the debate record says so (ids as in the script output):

| variant | withdrawn in full | narrowed | evidence |
|---|---|---|---|
| V1 | C-02, C-03, C-21, C-26, A-01, A-05, A-06, A-07 | F-01, F-03, F-04, F-12, F-14, F-15, C-08 | `round1-advocate-V1.md` section 5 items 1 to 4; `round2-rebuttal-V1.md` section 1 "Net" ("I withdraw: C-02, C-03, C-21, C-26, A-01 'aligned', A-05..A-07 as gaps, F-01's '(1) observer reads the JSON', F-03's observer option, F-04 as an observer gap, F-12/F-14/F-15 as observer gaps ... W-3"); C-08 rebase part: same file section 3 row A-004. All rest on the false premise that no observer exists. |
| V2 | none | W-04 (downgraded to UNVERIFIED, "absent by construction" withdrawn), W-05 (labels partly inferred), W-10 (reworded: "no watcher panel in `observe` before FU-1") | `round1-advocate-V2.md` section 5 items 1, 3, 4; `round2-rebuttal-V2.md` section 1 rows 1, 4, 6 and "Net". |
| V3 | none | none | `round2-rebuttal-V3.md` section 1 "Net": "I withdraw: Edit 5 as written, the restated launch in Edit 8, all `/tmp` line cites, and the twelve-edit shape. I keep: F1, F2, F6, F8, F10 to F14, F17". The loss is in proposals (Edit 5, Edit 8 withdrawn; Edit 6, Edit 7 narrowed), not in findings. |
| V4 | C8 (the "boundary sentence is TRUE" proof was circular) | C7, F11 (omit the second governed agent), F3 (host-global worktrees), F7 (per-class AC unmeetable; WC-13 cite loose), F13 (two schemas, not one), F16 (cadence count wrong), F17 ("confines every path" holds for file reads only), F18 ("Collision Lens" is an unbuilt design), F19 (boundary proof circular, only "distinct" holds), F21 ("read-only" used loosely) | `round1-advocate-V4.md` section 5 items 1 to 8, 10; `round2-rebuttal-V4.md` section 1 rows 1 to 8. Proposals: #423 edit 3 withdrawn, #423 edits 4 and 7, #339 edit 4, #409 edit 2 narrowed. |
| V5 | O-05 (the sweep's "cannot read without consuming" is "stronger than the evidence": withdrawn, X-016 "unproven both ways"), BC-17 ("or the observer's snapshot" as a v2 input: withdrawn as worded) | RT-F04 ("CLOSED" only for the Orca ledger; "drop W-3 from the body" mislabel), RT-F16 (weak), D1 (omits the third party that carries data across hosts), D5 (option (ii) withdrawn), D9 (a guess; TUIBBS omitted) | `round1-advocate-V5.md` section 5 items 5 to 7, 10; `round2-rebuttal-V5.md` section 1 rows 1 to 4, 8 to 10 and the paragraph after the table. |

Advocates' point-table wins over the 36 X and A points (round-1 section 7 tables; a variant "wins" a point when at least 2 of the 5 advocates name it as winner, so this measures debate strength, not survival, and the advocates may favour their own variant):

| variant | round-1 points won by plurality (of 36) | round-1 points named by at least one advocate | round-2 final verdicts won by plurality (of the 13 contested points) |
|---|---|---|---|
| V1 | 11 | 15 | 4 |
| V2 | 4 | 9 | 4 |
| V3 | 2 | 12 | 3 |
| V4 | 7 | 12 | 2 |
| V5 | 24 | 28 | 6 |

(A winner cell that opens with "none", "neither", "process" or "all" names no variant; for example "none (V5 slip)" on X-019 and X-020 is not a V5 win. The first run of the script counted those cells as V5 wins; the fix is in `named()`.)

Contested digest cross-check: 13 of the 36 points were contested (`round1-contested-digest.md`: convergence 0.639). After Round 2 the advocates' own verdict tables agree on most of them: A-005, A-011, X-009, X-019, X-020 have no variant winner ("process" or "none"); A-002 goes to V1, V2 and V5 together (sweep unit, Run-less blind spot, observer unit); A-004 to V1 (V5 in two tables); A-008 to V2 with V5; A-013 to V5 (V2 in three tables); X-006 to V4 (venue) and V5 (two contracts), V2 in three tables; X-008 to V1 and V5 (V5 on the fact, V1's tables stand); A-007 to V1, V3 and V4 together; A-009 only V2 in one table. V3 is never the sole winner of a contested point in any of the five Round 2 tables (checked by script); it appears only as a co-winner on A-007 (all five tables), A-002 (two tables), A-013 and X-006 (a few tables).

## 3. How each metric was computed

All five metrics are computed by `/tmp/step3_quant.py` from the variant text (fences stripped). Counts and thresholds are in the output of section 8; the choices below are mine because the protocol leaves them open.

**RC, requirement coverage (weight 0.30).** The source request has no requirement ids, so the protocol's edge case applies (topic matching). The requirement list is R1 every finding validated against the sources it cites; R2 a best course of action per point; R3 dependencies between points and systems; R4 coverage of #409, #450, #423, Coder#477 and the PRs and work behind them (split into five checks R4a #409, R4b #450, R4c #423, R4d Coder#477, R4e PRs/work); R5 alignment of Orchestrator mode with the TUI observer judged. That is 9 binary checks. A check is matched when its detector passes (final thresholds):
- R1: at least 80% of the variant's numbered items carry a source reference (a `file.ext:line` cite, a `#NNN` issue or PR number, a commit hash of 9 to 12 hex characters, or a body-line cite `Lnn`).
- R2: at least 80% of the variant's alignment findings (V1 F rows; V2 W rows; V3 and V4 F rows; V5 O, RT, BC and D items; claim-check rows excluded) have a non-empty proposal cell (last table column "proposed change" / "smallest change" / "replace with" / "what this changes", or the D item's first-step text).
- R3: at least 5 dependency markers ("waits for", "depends on", "dependency", "prerequisite", "blocked by", "gated on", "before ... merge/FU-1/#NNN", "after ... #NNN", "must precede") or a dedicated dependency section heading (matching depend, missing for integration, must supply, wait for, prerequisite).
- R4a to R4d: the issue is mentioned at least 5 times. R4e: at least 3 distinct numbers among #539, #503, #514, #447, #448, #485, #425, #541, #534.
- R5: a Verdict section exists, "observer"/"observe" appears at least 10 times and the verdict words aligned/gap/contradiction at least 5 times.

The variants review different subjects, so two RCs are computed and averaged: **RC_whole** = matched checks / 9 (against the whole request) and **RC_own** = matched checks / 5 over R1, R2, R3, R5 and the one R4 target the variant was meant to serve (V1 R4a #409, V2 R4b #450, V3 R4d Coder#477, V4 R4c #423, V5 R4e the PRs and work behind the built observer: #503, #514, #539). `RC = 0.5 RC_whole + 0.5 RC_own`.

**IC, internal consistency (0.25).** `IC = 1 - contradictions / scorable claims`, with scorable claims = the variant's numbered items (72, 16, 29, 33, 76; vague statements are not numbered items). Contradictions are only those that can be pointed to: (a) script checks of the variant's own tallies (V3 and V4 stated verdict counts are recomputed from their F-row verdict cells and match; V1's claim-check tally is parsed and fails: "2 UNVERIFIED" lists three ids and C-07 and C-08 are counted in two groups, which is one defect, row X-009 of the diff analysis); (b) a curated list of self-contradictions documented in the debate record, each with its file and line: V1 verdict sentence vs its own C-02 and F-02 (X-008); V3 F12 vs Edit 7; V4 F7 vs C2 on WC-13; V5 "drop W-3 from the body" vs its own scope note (X-020). V2 has none on record.

**SR, specificity ratio (0.15).** The protocol gives two forms. Table form (used): concrete statements / substantive statements. A substantive statement is a non-heading line or table row of at least 6 words after the first H2 (so title and header block are excluded; "Verdicts:" and "Not done:" lines are skipped). A statement is concrete when it contains at least one of: a `file.ext:line` cite, `#NNN` or `PR NNN`, a 8 to 12 hex-character hash, an ISO date, a number with a unit (%, ms, s, minutes, rows, calls, workers, files, tests, bytes, columns, keys, Runs), a threshold (`<`, `>`, `>=`, `<=` followed by a digit), a backticked identifier, or a requirement tag (WC-n, FR-n, NFR-n, AC-n). YAML form (reference): concrete / (concrete + vague-only); it is 1.000 for all five because no statement contains a vague word without also being concrete, so it cannot rank.

**DC, dependency completeness (0.15).** Internal references are the variant's own id tokens (V1 C-nn, F-nn, A-nn, W-n; V2 W-nn; V3 Fn and "Edit n"; V4 Cn, Fn; V5 O-nn, F-nn, Dn) and question references (Qn, checked against the number of items in "Questions only the owner can answer"). A reference resolves when the id is defined by a table row, list item or heading of the same variant. The defining token itself is not a reference. Excluded as external: tokens prefixed "V1", "review 01", "Edit" in another report's wording, design-document section numbers and V4's "C1 to C19" (a different document's numbering).

**SC, section coverage (0.15).** Count of H2 headings (fences stripped) / the maximum over the five variants (8, V5). V1 to V4 have 6 H2 sections each.

**Quant score.** `0.30 RC + 0.25 IC + 0.15 SR + 0.15 DC + 0.15 SC`.

## 4. Assumptions the metrics made (they are weak proxies)

1. **RC measures presence, not correctness.** R1 counts items that carry a source reference, not items that are right: V1's C-03 "No observer code exists ... Verified" carries a cite and was wrong (withdrawn in Round 2). R2 checks that a proposal cell is not empty. R3 and R4 count words and mentions. R5 is saturated: all five have a Verdict section and discuss the observer, so it separates nothing. A reader should treat RC as "did the report address the request", not "did it answer it well".
2. **Mixing RC_whole and RC_own is a choice.** The five reports review five different subjects. RC_whole punishes a focused report (V2 never discusses #423; V3 has no #423 and one PR number) and RC_own forgives it. The 50/50 mean is arbitrary. Against the whole request alone the scores would be V4 1.000, V2 0.889, and V1, V3, V5 0.778 each (final thresholds); against each report's own target alone V2, V3, V4, V5 would be 1.000 and V1 0.800.
3. **IC cannot see wrong facts.** A script cannot detect a semantic contradiction, so IC counts only documented self-contradictions and tally errors (1 or 2 per variant). The big factual errors the debate found (V1's "the observer does not exist", V4's circular boundary proof, V3's "no write" status route) are errors against outside evidence, not internal contradictions, and do not lower IC. IC therefore sits at 0.966 to 1.000 and ranks almost nothing. The denominator also differs in kind: V1's 72 items are mostly "Verified" claim rows; V5's 76 include ten descriptive parts.
4. **SR rewards identifier density.** Any backticked token or `#NNN` makes a statement concrete, so a long report quoting many paths scores high whether or not the paths are right. V3 scores lowest (0.700), probably partly because its twelve paste-ready edits are blockquoted proposed issue text with few identifiers (UNVERIFIED; the script does not break SR down by section); V2 scores highest (0.820) because its statements are short table cells full of cites. The protocol's own vague-word list finds no vague-only statement in any variant, so the yaml form is 1.000 for all.
5. **DC is a well-formedness check.** It confirms that every id a report cites is defined in that report (all 5 pass, 21 to 81 references each). It says nothing about whether the dependency a report states is right, and cross-report references (V5's re-test of V1) are excluded by design.
6. **SC counts headings, not coverage.** V5 gets 8 H2 sections because it is a different kind of report (it adds a description of the built program and an overlap analysis); V1 to V4 share one six-section skeleton. A heading count is a size proxy.
7. **The metrics do not carry the debate's main result.** The central finding of the debate, that all four of V1 to V4 missed or assumed away the built observer and V5 corrects it, is not visible in any of RC, IC, SR, DC or SC. It shows up only in the survival rate (V1 loses 8 items in full and 7 in part) and in the point-table wins (V5 24 of 36).
8. **Survival depends on advocate candour and sampling.** An item nobody challenged counts as surviving. The withdrawn and narrowed lists are my reading of each advocate's own words (sources in section 2); "narrowed" is a judgement, so both strict and weighted forms are given. V3's finding set is untouched because its losses were all proposals (Edits), which the "including proposals" column shows. R2-V3 was written before R2-V4 and R2-V5 existed, so V3 never answered their criticisms. No fact was re-verified against code or GitHub in this step.
9. **Thresholds are arbitrary.** 80% for R1 and R2, 5 mentions per issue, 3 PR numbers, 5 dependency markers: section 5 shows how much the ranking moves if they move. V1's R1 share is 0.78, just under 0.80, which costs it one check.

## 5. What changed after the first run, and how much it matters

**The R3 detector was changed after the first run.** The RC thresholds were fixed before any number was looked at, with R3 defined as "at least 8 dependency markers". The first run (scenario S0 below) showed R3 failing for V1 (4 markers) and V5 (6 markers) although V1 has a section titled "Missing for integration" (10 items) and V5 a section "Integration decisions and dependencies" with a dependency table, and failing for V2 and V3 (6 markers each) although V2 lists what "Waits for" other work and V3 has "What IronClaude must supply or wait for". That was a detector false negative, so FINAL accepts either at least 5 markers or a dedicated dependency heading. The new marker threshold (5) was chosen after seeing counts of 4, 6, 6, 6 and 10; it is a post-hoc choice and is the reason the order of V5 and V4 is not stable.

**Bugs fixed while building the script (each changes no number reported before the fix except where stated):** V3 claim-check rows were first counted as 9 instead of 12 (header row counted, three related-issue bullets missed); V5 re-test ids were first mapped to "RT-F-04" instead of "RT-F04" (survival lists failed the id-existence assertion); the V1 tally parser first mis-grouped the "8 overstated" group; V4's "C1 to C19" (an external document's numbering) was first counted as an unresolved internal reference, which gave V4 DC 0.962 and quant 0.917 in S0; the point-table parser first counted "none (V5 slip)" cells as V5 wins (R2 plurality V5 was 9, now 6; V1 5, now 4; R1 plurality V5 was 25, now 24). All are fixed in the script printed below.

Sensitivity (computed by the script; IC, SR, DC, SC unchanged between scenarios, RC thresholds vary):

| scenario | thresholds (R1 and R2 share; R3 markers, or section; R4 mentions; R4e PR numbers) | RC V1 | RC V2 | RC V3 | RC V4 | RC V5 | quant V1 | quant V2 | quant V3 | quant V4 | quant V5 | order |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S0 first run | 0.80; 8 markers only; 5; 3 | 0.633 | 0.789 | 0.733 | 1.000 | 0.733 | 0.802 | 0.872 | 0.829 | 0.923 | 0.883 | V4 > V5 > V2 > V3 > V1 |
| **FINAL (reported)** | 0.80; 5 markers or section; 5; 3 | 0.789 | 0.944 | 0.889 | 1.000 | 0.889 | 0.848 | 0.919 | 0.876 | 0.923 | 0.930 | V5 > V4 > V2 > V3 > V1 |
| RELAXED | 0.70; 5 markers or section; 3; 2 | 1.000 | 0.944 | 0.889 | 1.000 | 0.944 | 0.912 | 0.919 | 0.876 | 0.923 | 0.946 | V5 > V4 > V2 > V1 > V3 |
| STRICT | 0.90; 8 markers or section; 10; 4 | 0.678 | 0.733 | 0.678 | 1.000 | 0.678 | 0.815 | 0.855 | 0.812 | 0.923 | 0.866 | V4 > V5 > V2 > V1 > V3 |

What is stable across the four scenarios: V5, V4 and V2 are always the top three and V2 is always third; V1 and V3 are always the bottom two, and their order swaps (V3 ahead in S0 and FINAL, V1 ahead in RELAXED and STRICT). What is not stable: first place between V5 and V4. V4 is ahead by 0.040 in S0 and by 0.057 in STRICT; V5 is ahead by 0.007 in FINAL and by 0.023 in RELAXED. The S0 row shows V4 at 0.923 because it is recomputed with the V4 DC fix; the 0.917 printed in the very first run is explained in the bug list above.

## 6. Ranking and how to read it

Quant ranking (FINAL): **V5 0.930 > V4 0.923 > V2 0.919 > V3 0.876 > V1 0.848.**

Tiers, which is the only part of the order that survives the sensitivity run: top tier V5, V4, V2 (0.919 to 0.930; order inside the tier is not reliable); then V3 (0.876); then V1 (0.848). V1 and V3 swap places under two of the four threshold sets.

What drives each score, from the RC detail in section 8: V4 is the only report that covers all five targets (#409, #450, #423, Coder#477 and four or more PR numbers), so RC_whole is 9/9. V5 has the highest SC (8 H2 sections against 6) and the highest IC, but fails R4b and R4c (#450 mentioned 2 times, #423 3 times) because it reviews built code, not those issues. V2 has the highest SR (0.820) and a full RC_own, but no #423 coverage. V3 has the lowest SR and misses #423 and the PR set. V1 is lowest on RC: it fails R1 (0.78 of items cited, threshold 0.80) and R4b (#450 mentioned 4 times).

Cross-reading with survival (section 2): V5's survival stays between 0.932 and 0.974 on every measure (top three on all but the alignment-only strict one, where V2, V3 and V4 are at 1.000; 0.974 strict, 0.941 weighted overall) and it has by far the most point-table wins (24 of 36), so its quant rank and its debate standing agree. V1 has the lowest strict survival (0.889) and the lowest quant score, so those agree too. V4 is second on quant but has the lowest weighted survival (0.818: ten of its 33 items were narrowed) and the fewest contested-point wins (2 of 13), so its quant rank overstates how much of its content stood after Round 2. V3 is the reverse: lower quant (0.876) but no finding withdrawn or narrowed (its Round 2 losses were edits, not findings). V2 is consistent: third on quant, 1.000 strict survival, weighted 0.906.

Use: this layer is 50% of the hybrid score under the protocol, and the four of its five metrics that are near-saturated (IC, DC, and R5 inside RC; SR yaml form) separate nothing. If the lead needs a single base variant, the quant layer alone cannot choose between V5, V4 and V2; the qualitative layer and the debate result should decide, and the survival table is the better guide to which findings to keep.

## 7. Script text (`/tmp/step3_quant.py`)

```python
#!/usr/bin/env python3
"""Step 3 quantitative layer (scoring-protocol A.1) for the five alignment reviews.

Standard library only. Read-only on the review folder. Run:
    uv run python /tmp/step3_quant.py
RC thresholds were set before the first run; the R3 rule was widened after it (scenario S0 keeps the
original rule; see report section 5). Lists of withdrawn and narrowed ids come from the debate record.
"""
import re
from collections import Counter, OrderedDict
from pathlib import Path

D = Path("/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/"
         ".dev/reviews/orchestrator-tui-alignment-20261113/adversarial/adversarial")
VIDS = [1, 2, 3, 4, 5]


def read(p):
    return p.read_text(encoding="utf-8")


def strip_fences(t):
    return re.sub(r"```.*?```", "", t, flags=re.S)


TEXT = {i: strip_fences(read(D / f"variant-{i}-original.md")) for i in VIDS}
LINES = {i: TEXT[i].split("\n") for i in VIDS}


# ----------------------------------------------------------------- parsing helpers
def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def is_sep(line):
    return bool(re.match(r"^\|[\s:|-]+\|?\s*$", line))


def clean_id(c):
    return re.sub(r"[*`]", "", c).strip()


def section(lines, h2_regex):
    """Lines of the H2 section whose title matches h2_regex (until next H2)."""
    out, on = [], False
    for ln in lines:
        if ln.startswith("## "):
            on = bool(re.search(h2_regex, ln))
            continue
        if on:
            out.append(ln)
    return out


def rows_with_id(lines, id_re):
    res = OrderedDict()
    for ln in lines:
        if ln.startswith("|") and not is_sep(ln):
            cs = cells(ln)
            if cs and re.fullmatch(id_re, clean_id(cs[0])):
                res.setdefault(clean_id(cs[0]), (ln, cs))
    return res


def h3_blocks(lines, h3_regex):
    """Return {key: text} for every '### ' heading whose title matches h3_regex (group 1 = key)."""
    blocks, key, buf = OrderedDict(), None, []
    for ln in lines:
        if ln.startswith("### ") or ln.startswith("## "):
            if key is not None:
                blocks[key] = "\n".join(buf)
            m = re.match(h3_regex, ln) if ln.startswith("### ") else None
            key, buf = (m.group(1) if m else None), []
            continue
        buf.append(ln)
    if key is not None:
        blocks[key] = "\n".join(buf)
    return blocks


# ----------------------------------------------------------------- item extraction
# item = dict(id, family, text, last)   family in {"claim", "finding"}
def extract_items(v):
    L = LINES[v]
    items = []

    def add(idd, fam, text, last, group):
        items.append(dict(id=idd, family=fam, text=text, last=last, group=group))

    if v == 1:
        for idd, (ln, cs) in rows_with_id(L, r"[CFA]-\d\d").items():
            fam = "claim" if idd[0] == "C" else "finding"
            add(idd, fam, ln, cs[-1], idd[0])
    elif v == 2:
        for idd, (ln, cs) in rows_with_id(L, r"W-\d\d").items():
            add(idd, "finding", ln, cs[-1], "W")
    elif v == 3:
        sec = section(L, r"Claim check")
        n, rel = 0, False
        for ln in sec:
            if ln.startswith("|") and not is_sep(ln):
                cs = cells(ln)
                if cs[0].lower().startswith("path as written") or set(cs[0]) <= set("-: "):
                    continue
                n += 1
                add(f"CC{n}", "claim", ln, cs[-1], "CC")
            elif ln.startswith("Related-issue claims"):
                rel = True
            elif rel and ln.startswith("- "):
                n += 1
                add(f"CC{n}", "claim", ln, ln, "CC")
            elif rel and ln.strip() and not ln.startswith("- "):
                rel = False
        for idd, (ln, cs) in rows_with_id(L, r"F\d+").items():
            add(idd, "finding", ln, cs[-1], "F")
    elif v == 4:
        for idd, (ln, cs) in rows_with_id(L, r"C\d+").items():
            add(idd, "claim", ln, cs[-1], "C")
        for idd, (ln, cs) in rows_with_id(L, r"F\d+").items():
            add(idd, "finding", ln, cs[-1], "F")
    elif v == 5:
        sec = section(L, r"What `superclaude observe` is today")
        for k, txt in h3_blocks(["### x"] + sec, r"### (\d+)\.").items():
            add(f"S{k}", "claim", txt, txt, "S")
        for idd, (ln, cs) in rows_with_id(L, r"O-\d\d").items():
            add(idd, "finding", ln, cs[-1], "O")
        retest = section(L, r"Re-test of review 01")
        for idd, (ln, cs) in rows_with_id(retest, r"F-\d\d").items():
            add("RT-" + idd.replace("-", ""), "finding", ln, cs[-1], "RT")
        corr = section(L, r"Corrections to the #409 body")
        for idd, (ln, cs) in rows_with_id(corr, r"\d+").items():
            add("BC-%02d" % int(idd), "finding", ln, cs[-1], "BC")
        integ = section(L, r"Integration decisions")
        for k, txt in h3_blocks(["### x"] + integ, r"### (D\d)\.").items():
            add(k, "finding", txt, txt, "D")
    return items


ITEMS = {i: extract_items(i) for i in VIDS}
EXPECTED_COUNTS = {1: 72, 2: 16, 3: 29, 4: 33, 5: 76}
for i in VIDS:
    assert len(ITEMS[i]) == EXPECTED_COUNTS[i], (i, len(ITEMS[i]), EXPECTED_COUNTS[i])

# ----------------------------------------------------------------- SC (section coverage)
H2 = {i: [ln for ln in LINES[i] if ln.startswith("## ")] for i in VIDS}
SC = {i: len(H2[i]) / max(len(H2[j]) for j in VIDS) for i in VIDS}

# ----------------------------------------------------------------- SR (specificity ratio)
CITE = r"[\w./-]+\.(?:py|md|tf|sh|json|mjs|yaml|yml|toml|js|ts):\d+"
CONCRETE = [
    re.compile(CITE),
    re.compile(r"(?<![\w])#\d{2,4}\b"),
    re.compile(r"\bPR\s?#?\d+\b"),
    re.compile(r"\b[0-9a-f]{8,12}\b"),
    re.compile(r"\b20\d\d-\d\d-\d\d"),
    re.compile(r"\b\d+(?:\.\d+)?\s?(?:%|ms\b|s\b|seconds?|minutes?|min\b|rows?|calls?|workers?|files?|tests?|bytes|characters|columns|MB|KB|threads?|keys?|Runs?)\b"),
    re.compile(r"[<>≥≤]=?\s?\d"),
    re.compile(r"`[A-Za-z_][\w./:=<>\[\]-]{2,}`"),
    re.compile(r"\b(?:WC|FR|NFR|SC|AC|OB|INV)-?H?\d+\b"),
]
VAGUE = re.compile(r"\b(appropriate|as needed|properly|adequate|adequately|should consider|might|various|etc\.?|"
                   r"best practices?|industry standard)\b", re.I)


def statements(v):
    out, seen_h2 = [], False
    for ln in LINES[v]:
        s = ln.strip()
        if ln.startswith("## "):
            seen_h2 = True
            continue
        if not seen_h2 or not s or s.startswith("#") or is_sep(ln):
            continue
        if re.match(r"^(Verdicts?( words)?|Status|Date|Not done|Not read)\b.*:", s):
            continue
        if s.startswith("|"):
            cs = cells(s)
            if cs and cs[0].lower() in ("id", "#", "claim", "release", "kind", "path", "point", "criterion", "q"):
                continue
            s = " ".join(cs)
        if len(re.findall(r"\w+", s)) < 6:
            continue
        out.append(s)
    return out


SR, SRSTAT = {}, {}
for i in VIDS:
    st = statements(i)
    conc = sum(1 for s in st if any(p.search(s) for p in CONCRETE))
    vague_only = sum(1 for s in st if VAGUE.search(s) and not any(p.search(s) for p in CONCRETE))
    SR[i] = conc / len(st)
    SRSTAT[i] = dict(n=len(st), concrete=conc, vague_only=vague_only,
                     sr_table=conc / len(st),
                     sr_yaml=conc / (conc + vague_only) if conc + vague_only else 1.0)

# ----------------------------------------------------------------- DC (dependency completeness)
ID_FAMILIES = {
    1: dict(pat=r"\b(?:[CFA]-\d\d|W-\d)\b", defined=lambda it: {x["id"] for x in ITEMS[1]} | {f"W-{k}" for k in range(1, 8)}),
    2: dict(pat=r"\bW-\d\d\b", defined=lambda it: {x["id"] for x in ITEMS[2]}),
    3: dict(pat=r"\bF\d{1,2}\b", defined=lambda it: {x["id"] for x in ITEMS[3] if x["group"] == "F"}),
    4: dict(pat=r"\b[CF]\d{1,2}\b", defined=lambda it: {x["id"] for x in ITEMS[4]}),
    5: dict(pat=r"\b(?:O-\d\d|F-\d\d|D\d)\b", defined=lambda it: {x["id"] for x in ITEMS[5] if x["group"] in ("O", "D")}
            | {"F-" + x["id"][4:] for x in ITEMS[5] if x["group"] == "RT"}),
}
QSEC = r"Questions only the owner can answer"
EDIT_DEF = re.compile(r"^\*\*Edit (\d+)\.")


def n_questions(v):
    sec = section(LINES[v], QSEC)
    n = 0
    for ln in sec:
        if re.match(r"^\d+\.\s", ln) or re.match(r"^- Q\d+\.", ln):
            n += 1
    return n


def external_prefix(text, start):
    """True when the token at `start` is a cross-report reference (e.g. 'V1 F-04', 'review 01 F-13')."""
    pre = text[max(0, start - 14):start]
    return bool(re.search(r"(?:\bV[1-5]['s]*\s?|review\s?0?\d\s|Review\s?0?\d\s|Edits?\s)$", pre))


DC, DCSTAT = {}, {}
for i in VIDS:
    fam = ID_FAMILIES[i]
    defined = fam["defined"](None)
    nq = n_questions(i)
    ned = sum(1 for ln in LINES[i] if EDIT_DEF.match(ln))
    refs, unresolved = 0, []
    for ln in LINES[i]:
        body = ln
        if "TECHNICAL-REFERENCE" in ln:  # ids of a document outside the variant (V4 'C1 to C19'): external, excluded
            continue
        # strip the defining token at the start of a row / list item / heading
        if ln.startswith("|"):
            cs = cells(ln)
            if cs and re.fullmatch(fam["pat"].replace(r"\b", ""), clean_id(cs[0])):
                body = ln.split("|", 2)[2] if ln.count("|") >= 2 else ln
        elif re.match(r"^- (W-\d|Q\d+)\b", ln) or re.match(r"^### (D\d)\.", ln):
            body = re.sub(r"^(- (W-\d|Q\d+)|### D\d)", "", ln)
        elif EDIT_DEF.match(ln):
            body = EDIT_DEF.sub("", ln)
        for mm in re.finditer(fam["pat"], body):
            if external_prefix(body, mm.start()):
                continue
            refs += 1
            if mm.group(0) not in defined:
                unresolved.append(mm.group(0))
        for mm in re.finditer(r"\bQ ?(\d{1,2})\b", body):
            if external_prefix(body, mm.start()):
                continue
            refs += 1
            if not (1 <= int(mm.group(1)) <= nq):
                unresolved.append("Q" + mm.group(1))
        if i == 3:
            for mm in re.finditer(r"\bEdits? (\d{1,2})\b", body):
                refs += 1
                if not (1 <= int(mm.group(1)) <= ned):
                    unresolved.append("Edit " + mm.group(1))
    DC[i] = (refs - len(unresolved)) / refs if refs else 1.0
    DCSTAT[i] = dict(refs=refs, unresolved=len(unresolved), sample=sorted(Counter(unresolved).items())[:12],
                     defined=len(defined), questions=nq, edits=ned)

# ----------------------------------------------------------------- IC (internal consistency)
# (a) automatic tally checks, (b) a fixed list of internal contradictions documented in the debate record.
AUTO = {i: [] for i in VIDS}


def verdict_class(cell):
    c = re.sub(r"[*`]", "", cell).strip().lower()
    for k, name in (("contradiction", "C"), ("gap", "G"), ("unknown", "U"), ("aligned", "A")):
        if c.startswith(k):
            return name
    return None


def stated_counts(v):
    sec = "\n".join(section(LINES[v], r"^## Verdict"))
    d = {}
    for key, rx in (("C", r"(\d+) contradictions?"), ("G", r"(\d+) gaps?"), ("U", r"(\d+) unknowns?"), ("A", r"(\d+) aligned")):
        m = re.search(rx, sec)
        if m:
            d[key] = int(m.group(1))
    return d


for v in (3, 4):
    cnt = Counter()
    for it in ITEMS[v]:
        if it["group"] == "F":
            cs = cells(it["text"])
            k = verdict_class(cs[2])
            if k:
                cnt[k] += 1
    st = stated_counts(v)
    bad = {k: (st[k], cnt[k]) for k in st if st[k] != cnt[k]}
    if bad:
        AUTO[v].append(f"verdict tally mismatch {bad}")

# V1: tally line of the claim check
sec1 = "\n".join(section(LINES[1], r"Claim check"))
mres = re.search(r"Result: (.*)", sec1)
if mres:
    groups = re.findall(r"(\d+) ([A-Za-z][A-Za-z ,]*?) \(([^()]*)\)", mres.group(1))
    seen_ids = Counter()
    for n, label, ids in groups:
        idl = sorted(set(re.findall(r"C-\d\d", ids or "")))
        for x in idl:
            seen_ids[x] += 1
        if idl and len(idl) != int(n):
            AUTO[1].append(f"claim tally: '{n} {label.strip()}' lists {len(idl)} ids {idl}")
    dup = [k for k, c in seen_ids.items() if c > 1]
    if dup:
        AUTO[1].append(f"claim tally: {dup} counted in more than one group")

# (b) curated, source-pointed list (diff-analysis.md Contradictions rows of type (c) plus conceded self-contradictions)
CURATED = {
    1: [("X-008", "verdict sentence 'share the same dimension names' (variant-1 line 171) vs its own C-02 'Overstated' and F-02 vocabulary gap")],
    2: [],
    3: [("R2-V3 row 5", "F12 says the watcher's trust is 'a different, local model' (variant-3 line 62) but Edit 7 states one grant format without reconciling it (line 119)")],
    4: [("R2-V4 self-correction", "F7 says 'A worker cannot message peers (WC-13)' (variant-4 line 74) but C2 states WC-13 only forbids starting workers or sessions (line 38)")],
    5: [("X-020", "RT-F04 'Drop W-3 from the #409 body' vs V5's own scope note: W-3 is V1's proposed wording, not body text")],
}
# the V1 tally defect is the same single row X-009; count it once whether found by script or by record
IC, ICSTAT = {}, {}
for i in VIDS:
    auto_n = 1 if AUTO[i] else 0  # one defect per variant, however many symptoms
    n_contra = len(CURATED[i]) + auto_n
    claims = len(ITEMS[i])
    IC[i] = 1 - n_contra / claims
    ICSTAT[i] = dict(claims=claims, contradictions=n_contra, auto=AUTO[i], curated=CURATED[i])

# ----------------------------------------------------------------- RC (requirement coverage)
SRC_REF = re.compile("|".join([CITE, r"(?<![\w])#\d{2,4}\b", r"\bPR\s?#?\d+\b", r"\b[0-9a-f]{9,12}\b", r"\bL\d{1,3}\b"]))


def share(items, pred):
    return sum(1 for x in items if pred(x)) / len(items) if items else 0.0


ALIGN_GROUPS = {1: {"F"}, 2: {"W"}, 3: {"F"}, 4: {"F"}, 5: {"O", "RT", "BC", "D"}}
OWN_TARGET = {1: "R4a", 2: "R4b", 3: "R4d", 4: "R4c", 5: "R4e"}
RC_DETAIL = {}


DEP_RX = re.compile(r"\b(waits? for|depends? on|dependenc(?:y|ies)|prerequisite|blocked (?:by|on)|gated (?:on|by)|"
                    r"before [^.|]{0,40}(?:merge|FU-1|#\d+)|after [^.|]{0,30}#\d+|must (?:precede|wait))", re.I)
DEP_HEADING = re.compile(r"^#{2,4} .*(depend|missing for integration|must supply|wait for|prerequisite)", re.I)

# Threshold sets. FINAL is the reported one. S0 is the first pre-registered run (R3 = markers only);
# its R3 detector turned out to miss dedicated dependency sections (V1, V5), so FINAL adds them (disclosed in the report).
CFGS = OrderedDict([
    ("S0 first run", dict(r1=0.80, r2=0.80, r3_markers=8, r3_section=False, r4=5, r4e=3)),
    ("FINAL", dict(r1=0.80, r2=0.80, r3_markers=5, r3_section=True, r4=5, r4e=3)),
    ("RELAXED", dict(r1=0.70, r2=0.70, r3_markers=5, r3_section=True, r4=3, r4e=2)),
    ("STRICT", dict(r1=0.90, r2=0.90, r3_markers=8, r3_section=True, r4=10, r4e=4)),
])


def req_checks(v, cfg):
    t = TEXT[v]
    its = ITEMS[v]
    al = [x for x in its if x["group"] in ALIGN_GROUPS[v]]
    r = OrderedDict()
    # R1: share of numbered items carrying a source reference
    s1 = share(its, lambda x: bool(SRC_REF.search(x["text"])))
    r["R1 validated against cited sources"] = (s1 >= cfg["r1"], f"{s1:.2f} of {len(its)} numbered items carry a source ref (need >= {cfg['r1']})")
    # R2: share of alignment findings carrying a non-empty proposal cell/step
    s2 = share(al, lambda x: len(re.sub(r"[\s|-]", "", x["last"])) > 0)
    r["R2 best course of action per point"] = (s2 >= cfg["r2"], f"{s2:.2f} of {len(al)} alignment findings carry a proposal cell (need >= {cfg['r2']})")
    # R3: dependency markers, or (FINAL and later) a dedicated dependency section
    dep = DEP_RX.findall(t)
    heads = [ln.strip() for ln in LINES[v] if DEP_HEADING.search(ln)]
    ok3 = len(dep) >= cfg["r3_markers"] or (cfg["r3_section"] and len(heads) > 0)
    r["R3 dependencies identified"] = (ok3, f"{len(dep)} dependency markers (need >= {cfg['r3_markers']})"
                                       + (f"; dedicated section heading(s): {[h[:50] for h in heads][:2]}" if cfg["r3_section"] else ""))

    # R4a-e coverage
    def cnt(rx):
        return len(re.findall(rx, t))
    c409, c450, c423, c477 = cnt(r"#409\b"), cnt(r"#450\b"), cnt(r"#423\b"), cnt(r"#477\b")
    prs = {p for p in re.findall(r"(?:PR\s?)?#(539|503|514|447|448|485|425|541|534)\b", t)}
    k = cfg["r4"]
    r["R4a issue #409"] = (c409 >= k, f"{c409} mentions (need >= {k})")
    r["R4b issue #450"] = (c450 >= k, f"{c450} mentions (need >= {k})")
    r["R4c issue #423"] = (c423 >= k, f"{c423} mentions (need >= {k})")
    r["R4d Coder#477"] = (c477 >= k, f"{c477} mentions (need >= {k})")
    r["R4e PRs/work behind them"] = (len(prs) >= cfg["r4e"], f"{len(prs)} distinct PR/issue numbers {sorted(prs)} (need >= {cfg['r4e']})")
    # R5 alignment with the TUI observer judged
    obs = cnt(r"observ(?:er|e)\b")
    verd = bool(re.search(r"^## Verdict", t, re.M))
    ali = cnt(r"\b(aligned|gap|contradiction)\b")
    r["R5 Orchestrator mode vs TUI observer judged"] = (verd and obs >= 10 and ali >= 5,
                                                         f"verdict section={verd}, observer mentions={obs} (>=10), verdict words={ali} (>=5)")
    return r


def rc_for(cfg):
    w, o, g, det = {}, {}, {}, {}
    for i in VIDS:
        r = req_checks(i, cfg)
        keys = list(r)
        det[i] = r
        w[i] = sum(1 for kk in keys if r[kk][0]) / len(keys)
        own = [kk for kk in keys if kk.startswith(("R1", "R2", "R3", "R5"))] + [kk for kk in keys if kk.startswith(OWN_TARGET[i])]
        o[i] = sum(1 for kk in own if r[kk][0]) / len(own)
        g[i] = 0.5 * w[i] + 0.5 * o[i]
    return w, o, g, det


RC_SCEN = {name: rc_for(cfg) for name, cfg in CFGS.items()}
RCW, RCO, RCG, RC_DETAIL = RC_SCEN["FINAL"]
RC = RCG

# ----------------------------------------------------------------- quant score
W = dict(RC=0.30, IC=0.25, SR=0.15, DC=0.15, SC=0.15)
QUANT = {i: W["RC"] * RC[i] + W["IC"] * IC[i] + W["SR"] * SR[i] + W["DC"] * DC[i] + W["SC"] * SC[i] for i in VIDS}

# ----------------------------------------------------------------- survival (debate record)
# W = withdrawn in full by its own advocate (R1 section 5 or R2 section 1 'Net'), N = narrowed / reworded / premise corrected.
WITHDRAWN = {
    1: dict(W={"C-02", "C-03", "C-21", "C-26", "A-01", "A-05", "A-06", "A-07"},
            N={"F-01", "F-03", "F-04", "F-12", "F-14", "F-15", "C-08"}),
    2: dict(W=set(), N={"W-04", "W-05", "W-10"}),
    3: dict(W=set(), N=set()),
    4: dict(W={"C8"}, N={"C7", "F3", "F7", "F11", "F13", "F16", "F17", "F18", "F19", "F21"}),
    5: dict(W={"O-05", "BC-17"}, N={"RT-F04", "RT-F16", "D1", "D5", "D9"}),
}
PROPOSALS = {  # numbered proposals outside the finding set (V5's BC/D already sit inside it)
    1: dict(n=7, W={"W-3"}, N={"W-1", "W-5", "W-7"}),
    2: dict(n=5, W=set(), N={"Edit 5"}),
    3: dict(n=12, W={"Edit 5", "Edit 8"}, N={"Edit 6", "Edit 7"}),
    4: dict(n=15, W={"#423 edit 3"}, N={"#423 edit 4", "#423 edit 7", "#339 edit 4", "#409 edit 2"}),
    5: dict(n=0, W=set(), N=set()),
}
SURV = {}
for i in VIDS:
    ids = {x["id"] for x in ITEMS[i]}
    assert WITHDRAWN[i]["W"] <= ids and WITHDRAWN[i]["N"] <= ids, (i, (WITHDRAWN[i]["W"] | WITHDRAWN[i]["N"]) - ids)
    n = len(ITEMS[i])
    w, nn = len(WITHDRAWN[i]["W"]), len(WITHDRAWN[i]["N"])
    non_claim = [x for x in ITEMS[i] if x["family"] == "finding"]
    ncl = len(non_claim)
    wf = len([x for x in non_claim if x["id"] in WITHDRAWN[i]["W"]])
    nf = len([x for x in non_claim if x["id"] in WITHDRAWN[i]["N"]])
    P = PROPOSALS[i]
    tot = n + P["n"]
    SURV[i] = dict(n=n, w=w, nn=nn,
                   strict=(n - w) / n, weighted=(n - w - 0.5 * nn) / n,
                   nf=ncl, wf=wf, nnf=nf, strict_f=(ncl - wf) / ncl, weighted_f=(ncl - wf - 0.5 * nf) / ncl,
                   np=P["n"], wp=len(P["W"]), nnp=len(P["N"]),
                   strict_all=(tot - w - len(P["W"])) / tot,
                   weighted_all=(tot - w - len(P["W"]) - 0.5 * (nn + len(P["N"]))) / tot)

# ----------------------------------------------------------------- point-table wins (36 points, round 1 and round 2)


def parse_tables(path, ids_rx=r"[XA]-\d\d\d"):
    out = {}
    hdr = None
    for ln in read(path).split("\n"):
        if ln.startswith("|") and not is_sep(ln):
            cs = cells(ln)
            low = [c.lower() for c in cs]
            if "winner" in low and any(x.startswith("id") for x in low[:1]):
                hdr = low.index("winner")
                continue
            if hdr is not None and re.fullmatch(ids_rx, clean_id(cs[0])) and len(cs) > hdr:
                out[clean_id(cs[0])] = cs[hdr]
        elif not ln.startswith("|"):
            if ln.startswith("#"):
                hdr = None if not re.search(r"point table|final verdict", ln, re.I) else hdr
    return out


def named(cell):
    # a cell that opens with none / neither / process / all names no winner (a variant in its parenthesis is a remark, not a winner)
    if re.match(r"\s*(none|neither|process|all)\b", cell, re.I):
        return set()
    return set("V" + m for m in re.findall(r"\bV([1-5])\b", cell))


def wins(prefix, points=None):
    tallies = {}
    for i in VIDS:
        tb = parse_tables(D / f"{prefix}{i}.md")
        for pid, cell in tb.items():
            if points and pid not in points:
                continue
            for vv in named(cell):
                tallies.setdefault(pid, Counter())[vv] += 1
    return tallies


R1T = wins("round1-advocate-V")
R2T = wins("round2-rebuttal-V")
ALL_POINTS = sorted({p for i in VIDS for p in parse_tables(D / f"round1-advocate-V{i}.md")})
CONTESTED = ["A-002", "A-004", "A-005", "A-007", "A-008", "A-009", "A-011", "A-013", "X-006", "X-008", "X-009", "X-019", "X-020"]
POINTS = {}
for i in VIDS:
    v = f"V{i}"
    r1 = sum(1 for p in ALL_POINTS if R1T.get(p, Counter())[v] >= 2)
    r1_any = sum(1 for p in ALL_POINTS if R1T.get(p, Counter())[v] >= 1)
    r2 = sum(1 for p in CONTESTED if R2T.get(p, Counter())[v] >= 2)
    POINTS[i] = dict(r1_plural=r1, r1_any=r1_any, r2_plural=r2)

# ----------------------------------------------------------------- output
NAMES = {1: "V1 #409 vs sweep", 2: "V2 #450 watcher", 3: "V3 Coder#477", 4: "V4 #423 v2", 5: "V5 built observer"}


def f(x):
    return f"{x:.3f}"


def main():
    p = print
    p("## Output of /tmp/step3_quant.py")
    p()
    p("### Numbered items per variant (the claim base for IC and survival)")
    p("| variant | items | claim rows | finding rows | H2 sections | statements (SR) |")
    p("|---|---|---|---|---|---|")
    for i in VIDS:
        p(f"| {NAMES[i]} | {len(ITEMS[i])} | {sum(1 for x in ITEMS[i] if x['family']=='claim')} | "
          f"{sum(1 for x in ITEMS[i] if x['family']=='finding')} | {len(H2[i])} | {SRSTAT[i]['n']} |")
    p()
    p("### RC detail (R1..R5; binary matches, FINAL thresholds; the other scenarios are listed under Sensitivity)")
    for i in VIDS:
        p(f"**{NAMES[i]}**")
        p("| requirement | matched | evidence |")
        p("|---|---|---|")
        for k, (ok, ev) in RC_DETAIL[i].items():
            p(f"| {k} | {'yes' if ok else 'no'} | {ev} |")
        p(f"RC_whole = {sum(1 for k in RC_DETAIL[i] if RC_DETAIL[i][k][0])}/{len(RC_DETAIL[i])} = {f(RCW[i])}; "
          f"RC_own = {f(RCO[i])} (own target {OWN_TARGET[i]}); RC = mean = {f(RC[i])}")
        p()
    p("### IC detail")
    p("| variant | scorable claims | internal contradictions | IC | what was counted |")
    p("|---|---|---|---|---|")
    for i in VIDS:
        s = ICSTAT[i]
        what = "; ".join([f"{a}: {b}" for a, b in s["curated"]] + [f"script: {a}" for a in s["auto"]]) or "none found"
        p(f"| {NAMES[i]} | {s['claims']} | {s['contradictions']} | {f(IC[i])} | {what} |")
    p()
    p("### SR detail")
    p("| variant | substantive statements | concrete | vague-only | SR (table form, used) | SR (yaml form, reference) |")
    p("|---|---|---|---|---|---|")
    for i in VIDS:
        s = SRSTAT[i]
        p(f"| {NAMES[i]} | {s['n']} | {s['concrete']} | {s['vague_only']} | {f(s['sr_table'])} | {f(s['sr_yaml'])} |")
    p()
    p("### DC detail")
    p("| variant | ids defined | internal refs | unresolved | DC | unresolved sample |")
    p("|---|---|---|---|---|---|")
    for i in VIDS:
        s = DCSTAT[i]
        p(f"| {NAMES[i]} | {s['defined']} | {s['refs']} | {s['unresolved']} | {f(DC[i])} | {s['sample']} |")
    p()
    p("### SC detail")
    p("| variant | H2 sections | max | SC |")
    p("|---|---|---|---|")
    mx = max(len(H2[i]) for i in VIDS)
    for i in VIDS:
        p(f"| {NAMES[i]} | {len(H2[i])} | {mx} | {f(SC[i])} |")
    p()
    p("### Quant score = 0.30 RC + 0.25 IC + 0.15 SR + 0.15 DC + 0.15 SC")
    p("| variant | RC | IC | SR | DC | SC | quant_score |")
    p("|---|---|---|---|---|---|---|")
    for i in VIDS:
        p(f"| {NAMES[i]} | {f(RC[i])} | {f(IC[i])} | {f(SR[i])} | {f(DC[i])} | {f(SC[i])} | **{f(QUANT[i])}** |")
    p()
    p("Ranking: " + " > ".join(f"{NAMES[i]} ({f(QUANT[i])})" for i in sorted(VIDS, key=lambda k: -QUANT[k])))
    p()
    p("### Sensitivity of RC (and so of quant_score) to the pre-set thresholds")
    p("| scenario | thresholds | RC V1 | RC V2 | RC V3 | RC V4 | RC V5 | quant V1 | quant V2 | quant V3 | quant V4 | quant V5 | ranking |")
    p("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for name, cfg in CFGS.items():
        g = RC_SCEN[name][2]
        q = {i: W["RC"] * g[i] + W["IC"] * IC[i] + W["SR"] * SR[i] + W["DC"] * DC[i] + W["SC"] * SC[i] for i in VIDS}
        rank = " > ".join("V%d" % i for i in sorted(VIDS, key=lambda k: -q[k]))
        p(f"| {name} | {cfg} | " + " | ".join(f(g[i]) for i in VIDS) + " | " + " | ".join(f(q[i]) for i in VIDS) + f" | {rank} |")
    p()
    p("RC detail per scenario (matched requirements out of 9, R1-R5 with R4a-e):")
    for name in CFGS:
        det = RC_SCEN[name][3]
        p(f"- {name}: " + "; ".join("V%d %s" % (i, "".join("1" if det[i][k][0] else "0" for k in det[i])) for i in VIDS)
          + "  (order: R1 R2 R3 R4a R4b R4c R4d R4e R5)")
    p()
    p("### Survival rate (Rounds 1 and 2)")
    p("| variant | numbered findings | withdrawn (W) | narrowed (N) | strict survival | weighted survival (N = 0.5) | alignment findings only: strict / weighted | incl. numbered proposals: strict / weighted |")
    p("|---|---|---|---|---|---|---|---|")
    for i in VIDS:
        s = SURV[i]
        p(f"| {NAMES[i]} | {s['n']} | {s['w']} | {s['nn']} | {f(s['strict'])} | {f(s['weighted'])} | "
          f"{f(s['strict_f'])} / {f(s['weighted_f'])} (n={s['nf']}, W={s['wf']}, N={s['nnf']}) | "
          f"{f(s['strict_all'])} / {f(s['weighted_all'])} (proposals n={s['np']}, W={s['wp']}, N={s['nnp']}) |")
    p()
    p("Withdrawn (W) and narrowed (N) ids:")
    for i in VIDS:
        p(f"- {NAMES[i]}: W = {sorted(WITHDRAWN[i]['W'])}; N = {sorted(WITHDRAWN[i]['N'])}; proposals W = {sorted(PROPOSALS[i]['W'])}, N = {sorted(PROPOSALS[i]['N'])}")
    p()
    p("### Point-table wins (advocate-named winners; plurality = named by >= 2 of 5 advocates)")
    p(f"Points parsed in Round 1: {len(ALL_POINTS)} ({', '.join(ALL_POINTS[:3])} ... {ALL_POINTS[-1]}).")
    p("| variant | R1 points won by plurality (of %d) | R1 points named by >= 1 advocate | R2 final verdicts won by plurality (of 13 contested) |" % len(ALL_POINTS))
    p("|---|---|---|---|")
    for i in VIDS:
        s = POINTS[i]
        p(f"| {NAMES[i]} | {s['r1_plural']} | {s['r1_any']} | {s['r2_plural']} |")


if __name__ == "__main__":
    main()
```

## 8. Script output (`/tmp/step3_output.txt`)

#### Numbered items per variant (the claim base for IC and survival)
| variant | items | claim rows | finding rows | H2 sections | statements (SR) |
|---|---|---|---|---|---|
| V1 #409 vs sweep | 72 | 39 | 33 | 6 | 126 |
| V2 #450 watcher | 16 | 0 | 16 | 6 | 50 |
| V3 Coder#477 | 29 | 12 | 17 | 6 | 110 |
| V4 #423 v2 | 33 | 11 | 22 | 6 | 113 |
| V5 built observer | 76 | 10 | 66 | 8 | 182 |

#### RC detail (R1..R5; binary matches, FINAL thresholds; the other scenarios are listed under Sensitivity)
**V1 #409 vs sweep**
| requirement | matched | evidence |
|---|---|---|
| R1 validated against cited sources | no | 0.78 of 72 numbered items carry a source ref (need >= 0.8) |
| R2 best course of action per point | yes | 1.00 of 18 alignment findings carry a proposal cell (need >= 0.8) |
| R3 dependencies identified | yes | 4 dependency markers (need >= 5); dedicated section heading(s): ['## Missing for integration'] |
| R4a issue #409 | yes | 39 mentions (need >= 5) |
| R4b issue #450 | no | 4 mentions (need >= 5) |
| R4c issue #423 | yes | 6 mentions (need >= 5) |
| R4d Coder#477 | yes | 5 mentions (need >= 5) |
| R4e PRs/work behind them | yes | 5 distinct PR/issue numbers ['447', '448', '534', '539', '541'] (need >= 3) |
| R5 Orchestrator mode vs TUI observer judged | yes | verdict section=True, observer mentions=35 (>=10), verdict words=11 (>=5) |
RC_whole = 7/9 = 0.778; RC_own = 0.800 (own target R4a); RC = mean = 0.789

**V2 #450 watcher**
| requirement | matched | evidence |
|---|---|---|
| R1 validated against cited sources | yes | 1.00 of 16 numbered items carry a source ref (need >= 0.8) |
| R2 best course of action per point | yes | 1.00 of 16 alignment findings carry a proposal cell (need >= 0.8) |
| R3 dependencies identified | yes | 6 dependency markers (need >= 5); dedicated section heading(s): [] |
| R4a issue #409 | yes | 12 mentions (need >= 5) |
| R4b issue #450 | yes | 17 mentions (need >= 5) |
| R4c issue #423 | no | 1 mentions (need >= 5) |
| R4d Coder#477 | yes | 8 mentions (need >= 5) |
| R4e PRs/work behind them | yes | 5 distinct PR/issue numbers ['425', '447', '448', '485', '534'] (need >= 3) |
| R5 Orchestrator mode vs TUI observer judged | yes | verdict section=True, observer mentions=11 (>=10), verdict words=19 (>=5) |
RC_whole = 8/9 = 0.889; RC_own = 1.000 (own target R4b); RC = mean = 0.944

**V3 Coder#477**
| requirement | matched | evidence |
|---|---|---|
| R1 validated against cited sources | yes | 0.83 of 29 numbered items carry a source ref (need >= 0.8) |
| R2 best course of action per point | yes | 1.00 of 17 alignment findings carry a proposal cell (need >= 0.8) |
| R3 dependencies identified | yes | 6 dependency markers (need >= 5); dedicated section heading(s): ['### What IronClaude must supply or wait for'] |
| R4a issue #409 | yes | 24 mentions (need >= 5) |
| R4b issue #450 | yes | 6 mentions (need >= 5) |
| R4c issue #423 | no | 0 mentions (need >= 5) |
| R4d Coder#477 | yes | 53 mentions (need >= 5) |
| R4e PRs/work behind them | no | 1 distinct PR/issue numbers ['539'] (need >= 3) |
| R5 Orchestrator mode vs TUI observer judged | yes | verdict section=True, observer mentions=22 (>=10), verdict words=18 (>=5) |
RC_whole = 7/9 = 0.778; RC_own = 1.000 (own target R4d); RC = mean = 0.889

**V4 #423 v2**
| requirement | matched | evidence |
|---|---|---|
| R1 validated against cited sources | yes | 0.91 of 33 numbered items carry a source ref (need >= 0.8) |
| R2 best course of action per point | yes | 1.00 of 22 alignment findings carry a proposal cell (need >= 0.8) |
| R3 dependencies identified | yes | 10 dependency markers (need >= 5); dedicated section heading(s): [] |
| R4a issue #409 | yes | 40 mentions (need >= 5) |
| R4b issue #450 | yes | 10 mentions (need >= 5) |
| R4c issue #423 | yes | 42 mentions (need >= 5) |
| R4d Coder#477 | yes | 18 mentions (need >= 5) |
| R4e PRs/work behind them | yes | 4 distinct PR/issue numbers ['447', '448', '534', '539'] (need >= 3) |
| R5 Orchestrator mode vs TUI observer judged | yes | verdict section=True, observer mentions=16 (>=10), verdict words=26 (>=5) |
RC_whole = 9/9 = 1.000; RC_own = 1.000 (own target R4c); RC = mean = 1.000

**V5 built observer**
| requirement | matched | evidence |
|---|---|---|
| R1 validated against cited sources | yes | 0.84 of 76 numbered items carry a source ref (need >= 0.8) |
| R2 best course of action per point | yes | 1.00 of 66 alignment findings carry a proposal cell (need >= 0.8) |
| R3 dependencies identified | yes | 6 dependency markers (need >= 5); dedicated section heading(s): ['## Integration decisions and dependencies', '### Dependencies for integrating Orchestrator mode'] |
| R4a issue #409 | yes | 28 mentions (need >= 5) |
| R4b issue #450 | no | 2 mentions (need >= 5) |
| R4c issue #423 | no | 3 mentions (need >= 5) |
| R4d Coder#477 | yes | 6 mentions (need >= 5) |
| R4e PRs/work behind them | yes | 5 distinct PR/issue numbers ['503', '514', '534', '539', '541'] (need >= 3) |
| R5 Orchestrator mode vs TUI observer judged | yes | verdict section=True, observer mentions=195 (>=10), verdict words=29 (>=5) |
RC_whole = 7/9 = 0.778; RC_own = 1.000 (own target R4e); RC = mean = 0.889

#### IC detail
| variant | scorable claims | internal contradictions | IC | what was counted |
|---|---|---|---|---|
| V1 #409 vs sweep | 72 | 2 | 0.972 | X-008: verdict sentence 'share the same dimension names' (variant-1 line 171) vs its own C-02 'Overstated' and F-02 vocabulary gap; script: claim tally: '2 UNVERIFIED' lists 3 ids ['C-07', 'C-08', 'C-37']; script: claim tally: ['C-07', 'C-08'] counted in more than one group |
| V2 #450 watcher | 16 | 0 | 1.000 | none found |
| V3 Coder#477 | 29 | 1 | 0.966 | R2-V3 row 5: F12 says the watcher's trust is 'a different, local model' (variant-3 line 62) but Edit 7 states one grant format without reconciling it (line 119) |
| V4 #423 v2 | 33 | 1 | 0.970 | R2-V4 self-correction: F7 says 'A worker cannot message peers (WC-13)' (variant-4 line 74) but C2 states WC-13 only forbids starting workers or sessions (line 38) |
| V5 built observer | 76 | 1 | 0.987 | X-020: RT-F04 'Drop W-3 from the #409 body' vs V5's own scope note: W-3 is V1's proposed wording, not body text |

#### SR detail
| variant | substantive statements | concrete | vague-only | SR (table form, used) | SR (yaml form, reference) |
|---|---|---|---|---|---|
| V1 #409 vs sweep | 126 | 89 | 0 | 0.706 | 1.000 |
| V2 #450 watcher | 50 | 41 | 0 | 0.820 | 1.000 |
| V3 Coder#477 | 110 | 77 | 0 | 0.700 | 1.000 |
| V4 #423 v2 | 113 | 89 | 0 | 0.788 | 1.000 |
| V5 built observer | 182 | 141 | 0 | 0.775 | 1.000 |

#### DC detail
| variant | ids defined | internal refs | unresolved | DC | unresolved sample |
|---|---|---|---|---|---|
| V1 #409 vs sweep | 79 | 81 | 0 | 1.000 | [] |
| V2 #450 watcher | 16 | 32 | 0 | 1.000 | [] |
| V3 Coder#477 | 17 | 73 | 0 | 1.000 | [] |
| V4 #423 v2 | 33 | 21 | 0 | 1.000 | [] |
| V5 built observer | 43 | 64 | 0 | 1.000 | [] |

#### SC detail
| variant | H2 sections | max | SC |
|---|---|---|---|
| V1 #409 vs sweep | 6 | 8 | 0.750 |
| V2 #450 watcher | 6 | 8 | 0.750 |
| V3 Coder#477 | 6 | 8 | 0.750 |
| V4 #423 v2 | 6 | 8 | 0.750 |
| V5 built observer | 8 | 8 | 1.000 |

#### Quant score = 0.30 RC + 0.25 IC + 0.15 SR + 0.15 DC + 0.15 SC
| variant | RC | IC | SR | DC | SC | quant_score |
|---|---|---|---|---|---|---|
| V1 #409 vs sweep | 0.789 | 0.972 | 0.706 | 1.000 | 0.750 | **0.848** |
| V2 #450 watcher | 0.944 | 1.000 | 0.820 | 1.000 | 0.750 | **0.919** |
| V3 Coder#477 | 0.889 | 0.966 | 0.700 | 1.000 | 0.750 | **0.876** |
| V4 #423 v2 | 1.000 | 0.970 | 0.788 | 1.000 | 0.750 | **0.923** |
| V5 built observer | 0.889 | 0.987 | 0.775 | 1.000 | 1.000 | **0.930** |

Ranking: V5 built observer (0.930) > V4 #423 v2 (0.923) > V2 #450 watcher (0.919) > V3 Coder#477 (0.876) > V1 #409 vs sweep (0.848)

#### Sensitivity of RC (and so of quant_score) to the pre-set thresholds
| scenario | thresholds | RC V1 | RC V2 | RC V3 | RC V4 | RC V5 | quant V1 | quant V2 | quant V3 | quant V4 | quant V5 | ranking |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S0 first run | {'r1': 0.8, 'r2': 0.8, 'r3_markers': 8, 'r3_section': False, 'r4': 5, 'r4e': 3} | 0.633 | 0.789 | 0.733 | 1.000 | 0.733 | 0.802 | 0.872 | 0.829 | 0.923 | 0.883 | V4 > V5 > V2 > V3 > V1 |
| FINAL | {'r1': 0.8, 'r2': 0.8, 'r3_markers': 5, 'r3_section': True, 'r4': 5, 'r4e': 3} | 0.789 | 0.944 | 0.889 | 1.000 | 0.889 | 0.848 | 0.919 | 0.876 | 0.923 | 0.930 | V5 > V4 > V2 > V3 > V1 |
| RELAXED | {'r1': 0.7, 'r2': 0.7, 'r3_markers': 5, 'r3_section': True, 'r4': 3, 'r4e': 2} | 1.000 | 0.944 | 0.889 | 1.000 | 0.944 | 0.912 | 0.919 | 0.876 | 0.923 | 0.946 | V5 > V4 > V2 > V1 > V3 |
| STRICT | {'r1': 0.9, 'r2': 0.9, 'r3_markers': 8, 'r3_section': True, 'r4': 10, 'r4e': 4} | 0.678 | 0.733 | 0.678 | 1.000 | 0.678 | 0.815 | 0.855 | 0.812 | 0.923 | 0.866 | V4 > V5 > V2 > V1 > V3 |

RC detail per scenario (matched requirements out of 9, R1-R5 with R4a-e):
- S0 first run: V1 010101111; V2 110110111; V3 110110101; V4 111111111; V5 110100111  (order: R1 R2 R3 R4a R4b R4c R4d R4e R5)
- FINAL: V1 011101111; V2 111110111; V3 111110101; V4 111111111; V5 111100111  (order: R1 R2 R3 R4a R4b R4c R4d R4e R5)
- RELAXED: V1 111111111; V2 111110111; V3 111110101; V4 111111111; V5 111101111  (order: R1 R2 R3 R4a R4b R4c R4d R4e R5)
- STRICT: V1 011100011; V2 110110011; V3 011100101; V4 111111111; V5 011100011  (order: R1 R2 R3 R4a R4b R4c R4d R4e R5)

#### Survival rate (Rounds 1 and 2)
| variant | numbered findings | withdrawn (W) | narrowed (N) | strict survival | weighted survival (N = 0.5) | alignment findings only: strict / weighted | incl. numbered proposals: strict / weighted |
|---|---|---|---|---|---|---|---|
| V1 #409 vs sweep | 72 | 8 | 7 | 0.889 | 0.840 | 0.879 / 0.788 (n=33, W=4, N=6) | 0.886 / 0.823 (proposals n=7, W=1, N=3) |
| V2 #450 watcher | 16 | 0 | 3 | 1.000 | 0.906 | 1.000 / 0.906 (n=16, W=0, N=3) | 1.000 / 0.905 (proposals n=5, W=0, N=1) |
| V3 Coder#477 | 29 | 0 | 0 | 1.000 | 1.000 | 1.000 / 1.000 (n=17, W=0, N=0) | 0.951 / 0.927 (proposals n=12, W=2, N=2) |
| V4 #423 v2 | 33 | 1 | 10 | 0.970 | 0.818 | 1.000 / 0.795 (n=22, W=0, N=9) | 0.958 / 0.812 (proposals n=15, W=1, N=4) |
| V5 built observer | 76 | 2 | 5 | 0.974 | 0.941 | 0.970 / 0.932 (n=66, W=2, N=5) | 0.974 / 0.941 (proposals n=0, W=0, N=0) |

Withdrawn (W) and narrowed (N) ids:
- V1 #409 vs sweep: W = ['A-01', 'A-05', 'A-06', 'A-07', 'C-02', 'C-03', 'C-21', 'C-26']; N = ['C-08', 'F-01', 'F-03', 'F-04', 'F-12', 'F-14', 'F-15']; proposals W = ['W-3'], N = ['W-1', 'W-5', 'W-7']
- V2 #450 watcher: W = []; N = ['W-04', 'W-05', 'W-10']; proposals W = [], N = ['Edit 5']
- V3 Coder#477: W = []; N = []; proposals W = ['Edit 5', 'Edit 8'], N = ['Edit 6', 'Edit 7']
- V4 #423 v2: W = ['C8']; N = ['C7', 'F11', 'F13', 'F16', 'F17', 'F18', 'F19', 'F21', 'F3', 'F7']; proposals W = ['#423 edit 3'], N = ['#339 edit 4', '#409 edit 2', '#423 edit 4', '#423 edit 7']
- V5 built observer: W = ['BC-17', 'O-05']; N = ['D1', 'D5', 'D9', 'RT-F04', 'RT-F16']; proposals W = [], N = []

#### Point-table wins (advocate-named winners; plurality = named by >= 2 of 5 advocates)
Points parsed in Round 1: 36 (A-001, A-002, A-003 ... X-020).
| variant | R1 points won by plurality (of 36) | R1 points named by >= 1 advocate | R2 final verdicts won by plurality (of 13 contested) |
|---|---|---|---|
| V1 #409 vs sweep | 11 | 15 | 4 |
| V2 #450 watcher | 4 | 9 | 4 |
| V3 Coder#477 | 2 | 12 | 3 |
| V4 #423 v2 | 7 | 12 | 2 |
| V5 built observer | 24 | 28 | 6 |
