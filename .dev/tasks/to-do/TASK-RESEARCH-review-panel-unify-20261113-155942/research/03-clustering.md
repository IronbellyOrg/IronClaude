# Research: Clustering of findings across reviewers

**Investigation type:** Code Tracer + Pattern Investigator
**Scope:** `src/superclaude/cli/review/findings.py`, `src/superclaude/cli/review/cluster.py`, `src/superclaude/cli/review/cluster_cmd.py`, `src/superclaude/cli/review/verify_cmd.py`, `src/superclaude/cli/review/telemetry.py`, E1 artifacts (`cluster-v2-known-weaknesses.md`, `pair-labels/README.md`, `stage0a-report.md`), `scripts/reflect_cluster_pairs.py`, `tests/review/test_reflect_cluster_pairs.py`, E2 `analysis/audits/audit-D/anch.py` and `COMBO-REPORT.md` (commit 4a22d742)
**Status:** Complete
**Date:** 2026-11-13

All source citations are to the working tree of branch `ironbelly/shadow-runs` at HEAD `792cf8c52` (read 2026-11-13). E2 citations are `git show 4a22d742:<path>:<line>`.

---

## 1. v1 clusterer: `src/superclaude/cli/review/findings.py` [E3]

The #346 findings-v1 module (stdlib only, docstring `findings.py:1-4`). It is the clusterer behind the review ledger (`ledger.merge_round`, `ledger.py:165`). [E3]; reused by E1 through `refs_norm` (section 2) and by E2 through `superclaude review merge` (the eval drove the product merge; replayed in E2 `audit-D/anch.py`, section 7).

### 1.1 Constants and the reference-id token

- `_REF_TOKEN = re.compile(r"\b(?:[A-Z]{1,4}-[0-9]+(?:\.[0-9]+)*|P[0-9])\b")` (`findings.py:29`). Matches 1-4 capital letters, a hyphen, digits, optional `.digits` groups; or the literal `P` plus ONE digit. [E3]
- `_SECTION_REF = re.compile(r"^\d+(?:\.\d+)*$")` (`findings.py:30`): bare section numbers such as `3.2` are accepted only when they are a whole entry of the finding's `refs` list, not when they appear in prose. [E3]
- `_HEADING` (`findings.py:28`) is used by `section_of`. [E3]

### 1.2 `section_of` (`findings.py:307-318`)

Walks up from the anchor's first line to the nearest Markdown heading. Returns the leading number of the heading (`3.2`) if it has one, else a slug of the heading text, else `"top"`. Annotation uses `"none"` when the anchor was not found (`findings.py:358`). [E3]

### 1.3 `refs_norm` (`findings.py:321-337`)

- Input text: `anchor`, `anchor2`, `claim` (`:323-327`) plus every string in `refs` (`:328-329`).
- Every `_REF_TOKEN` match in any of those is upper-cased into a set (`:331-333`); whole-entry section numbers from `refs` are added (`:334-336`).
- Tokens starting with `SHA-` are dropped (`:337`); output is sorted.
- Consequence: refs come from free prose (claim and anchor quote), not only from the declared `refs` list. Any `XX-n` token a reviewer happens to write in its claim becomes a clustering key. [E3]

### 1.4 `fingerprint` and `annotate` (`findings.py:340-360`)

- `fingerprint(section, refs) = sha256("v1|" + section + "|" + ",".join(refs))[:16]` (`:340-343`). [E3]
- `annotate(finding, text)` (`:346-360`) needs the candidate document text: it locates `anchor` (whitespace-normalised substring search, `locate`, ending `:304`), takes the FIRST match as `span` (`:352`) and flags `anchor_ambiguous` when there are several (`:351`); locates `anchor2` the same way (`:354-356`); sets `section` from the span or `"none"` (`:358`); sets `fp` (`:359`). A missing anchor keeps the finding with `span=None`, `section="none"` (D5). [E3]
- Spans are half-open `(start_line, end_line)` 0-based tuples (`:302`). [E3]

### 1.5 `same_defect` (`findings.py:367-379`)

Pairwise rule, in order:
1. If `a.fp == b.fp` and `a.refs_norm` is non-empty -> same defect (`:371-372`). Because fp hashes section + refs, this means "same section and identical ref set". The comment (`:369-370`) explicitly refuses the fp shortcut when refs are empty.
2. Else, if the ref sets intersect OR both are empty, the findings are the same defect when ANY span of a (anchor or anchor2) is within 3 lines of ANY span of b: `s1[0] <= s2[1] + 3 and s2[0] <= s1[1] + 3` (`:373-378`).
3. Else not the same defect (`:379`).

Notes [E3]:
- Rule 2 has no category, severity or claim-text check: two different defects on adjacent lines with no refs merge.
- Rule 2 accepts any single shared ref; two findings that share `AC-1` but sit on different lines do NOT merge by rule 2 (spans must still be close) but DO merge by rule 1 when they are in the same section with exactly the same ref set.
- Rule 2 uses `anchor2` spans too, so a finding with a second anchor far away gains a second "attachment point".
- Missing anchors (`span=None`) can only merge by rule 1, and their section is `"none"`, so two missing-anchor findings with equal non-empty refs always merge regardless of where they were meant to point.

### 1.6 `cluster` (`findings.py:382-407`)

- O(n^2) pairwise loop over all findings of one round from all reviewers in report order (`:393-395`); union-find with path halving (`:387-391`); the smaller root wins (`:398`), so the cluster root is the earliest finding in input order.
- Output: list of groups, ordered by first member, members in input order (`:399-407`).
- No size cap, no chain detection, no same-reviewer guard: two findings of the SAME reviewer can merge. [E3]

### 1.7 How the v1 cluster becomes a ledger row (`ledger.py:107-279`) [E3]

- Every reviewer's parsable findings are annotated and clustered, including findings from a reviewer whose block is invalid (`ledger.py:128-138`; docstring `:112`). [CODE-VERIFIED]
- A cluster is matched to an existing row if ANY member is `same_defect` with the row view (`ledger.py:166-171`); the row view is `{fp, span, span2, refs_norm=row.refs}` (`ledger.py:77-83`). The first matching row wins (`break`, `:171`).
- New row (`ledger.py:181-205`): `fp`, `category`, `anchor`, `anchor2`, `span`, `span2`, `claim` all from `group[0]` (`:182, :186, :191, :194-199`); `refs` = union of members' refs (`:183`); `blocking` = any member blocking (`:187`); `severity_max` = max (`:188-190`). So the row keeps the first member's claim and category (D6) [CODE-VERIFIED], while `fp` was computed from the first member's own refs and the row's `refs` is the union, so later matches against this row use a union ref set but a single-member fp. [E3]
- Matched row (`:207-238`): members appended, blocking recomputed from the current round (`:213-218`), re-anchored on the first member with a span (`:226-231`); the claim and category are NOT updated. [E3]

### 1.8 Span mapping across versions (`findings.py:413-457`, `ledger.py:301-347`) [E3]

- `opcodes` = line-level `difflib.SequenceMatcher` (`findings.py:413-416`); `map_span` maps a half-open old range into the new version, a replaced or deleted line maps to the start of its new range (`:430-439`); `hunks_touch` says whether a non-equal hunk overlaps the span (`:442-457`).
- `apply_revision` refuses an `old_text` whose sha256 differs from the reviewed round (`ledger.py:308-314`), marks fix-map rows `resolved_check` only when a hunk touches their span (`:330-339`), then maps every row's span and span2 into the new version (`:343-346`).
- Only spans are moved; `fp` is NOT recomputed, so a revision that renumbers the section heading changes the next round's finding fp, and re-match then depends on the span rule (rule 2) alone. [E3]

### Key Takeaways

- v1 clusters on (section + ref set) or (shared/no refs + spans within 3 lines), transitively, with no chain detection, no category/claim check and no same-reviewer guard. [E3]
- Refs are harvested from free prose with a narrow regex; ref extraction quality directly drives both the fp and the span rule. [E3]
- The ledger row keeps member 0's claim, category and fp forever (claim/category never updated on refound). [E3]
- v1 has real cross-version machinery (diff-mapped spans, sha-checked old text) that v2 lacks; this is the only existing answer to "a finding moves between versions". [E3]

---

## 2. v2 clusterer: `src/superclaude/cli/review/cluster.py` [E1]

Added by E1 (reflect Stage 0-2, commit `d2d8a2d16`). Pure function `cluster_v2(reviewer_records, snapshot_file_list)` returning a JSON dict (docstring `cluster.py:1-4`). Imports `refs_norm` from v1 (`cluster.py:64`) and `_check_citation` from `findings_v2` (`cluster.py:65`). Constants: `PRIMARY_ROLES` (`:67-71`: `reflect-pre` -> plan, `reflect-post` -> source/diff, `spec` -> spec), `SPAN_TOLERANCE = 3` (`:72`).

Every docstring rule below was checked against the code. [CODE-VERIFIED] unless noted.

### 2.1 Inputs and record validation (`_records`, `cluster.py:184-248`)

- A record is a 4-tuple `(reviewer_id, ordinal, block, calibration_map)` (`:194-202`); malformed records are reported in `problems` and dropped (`:195-210`).
- Block validity: a bare list is valid (`:218-219`); a dict is valid only when `block["state"] == "complete"` (`:220-221`); anything else is invalid with no findings (`:222-223`).
- Records are sorted by `(ordinal, input position)` (`:234`); duplicate reviewer ids are skipped (`:235-247`).

### 2.2 Members (`_members`, `cluster.py:251-299`) and Q5

- `if not r["valid"]: continue` (`:256-257`): every finding of a reviewer whose block state is not `complete` is left out. [CODE-VERIFIED docstring :9-11]
- `findings_v2.parse_block` sets state `invalid` on ANY error, including one bad line, and `truncated` when the block is not closed (`findings_v2.py:299-303`), but it still returns every line that passed `check_finding` in `findings` (`findings_v2.py:284-290`). So a block with 9 good lines and 1 over-long claim yields 9 parsed findings, and `cluster_v2` clusters none of them. **Answer to Q5: yes, `cluster_v2` drops all of a reviewer's findings when that reviewer's block is invalid or truncated.** The reviewer appears in `invalid_reviewers` (`cluster.py:416`) and is excluded from `complete_reviewers` (`:386`), so it also does not count toward the support denominator or the "fewer than 2 complete reviewers" agreement rule (`:405`). [E1]
- Contrast: v1 `merge_round` clusters the parsable findings of an invalid block (`ledger.py:135-138`). [E3] So v1 and v2 take OPPOSITE positions on invalid blocks (v1: keep and cluster; v2: drop all).
- Contrast inside E1: `verify_cmd` checks the citations of `block["findings"]` regardless of block state (`verify_cmd.py:139-157`), so findings that `cluster` drops can still appear in `precheck.json`. [E1]
- Per-finding: no string id or duplicate id -> skipped with a problem (`cluster.py:259-277`); calibration taken only if a finite number in [0, 1] and not a bool (`_confidence` `:79-83`; `:278-287`).

### 2.3 Annotation and fingerprint (`annotate`, `cluster.py:104-154`)

- Each citation is classified `malformed` (fails `_check_citation`: role in `plan, spec, source, test, diff, artifact`, repo-relative path, `1 <= line_start <= line_end`, quote 12-200 chars; `findings_v2.py:59-81`), `unresolved` (path not in the snapshot by exact string equality), or `resolved` (`cluster.py:104-116`).
- Primary citation: first citation whose role matches the finding's own `lens` field via `PRIMARY_ROLES`, else the first citation (`:133-134`). The block lens is not passed: `cluster_cmd` calls `parse_block` without `lens` (`cluster_cmd.py:151`), and `annotate` reads `finding.get("lens")` (`cluster.py:133`), so a finding with no per-line `lens` always uses its first citation as primary.
- `refs_norm` is v1's function applied to `anchor`, `anchor2`, `claim` and `refs` (`:135-141`).
- Fingerprint `sha256("v2|role|path||refs|class")`, full hex digest (`:119-123`), computed only when the primary citation is resolved (`:143-147`). The empty fourth field is the section, always `""` (docstring `:28`). Unlike v1, the fp includes `deviation_class`.

### 2.4 `same_defect_v2` (`cluster.py:157-181`)

1. Equal fp and non-empty `refs_norm` -> same (`:163-164`). Equal fp implies same role, same path, same ref set and same class.
2. Deviation classes must be compatible: equal, or either is `None` or `"none"` (`_compatible` `:157-158`; `:165-166`).
3. Ref sets intersect or are both empty (`:167-169`).
4. Some resolved citation of a and some resolved citation of b on the same path with line ranges within `SPAN_TOLERANCE` = 3 (`:170-180`). Any citation counts, not only the primary, and role is ignored in rule 4.

### 2.5 Union-find and chain detection (`cluster.py:302-378`)

- `_components` (`:302-320`): same O(n^2) pairwise loop and path-halving union-find as v1; groups ordered by root index (`:320`). Transitive.
- `_cluster` (`:323-378`): `chained = any(not same_defect_v2(a, b) for every pair)` (`:324-326`). A chained cluster is kept whole; chain detection only labels it. No size cap, no split, no same-reviewer guard.
- Support: per reviewer, the highest calibrated confidence among its members (`:328-335`); `support = sum(best) / total` unless any member is uncalibrated or `total` is None (`:336-337`).
- Representative: highest calibrated confidence, ties by resolution order (`:338-344`); the cluster `claim` is the representative's claim (`:374`). No category field is emitted for the cluster; members carry `deviation_class` (`:360`).
- `blocking_any`, `blocking_all` (`:375-376`); `disputed` when support < 0.5, blocking disagreement, or more than one non-null deviation class (`:345-351`).

### 2.6 `cluster_v2` result (`cluster.py:381-433`)

- Weight per complete reviewer = its highest calibrated confidence (`:389-396`); `total` is None unless every reviewer with findings is calibrated (`:397-398`); a zero sum becomes None (`:401`).
- `cluster_agreement`: None with < 2 complete reviewers (`:405-406`); 1.0 when no blocking cluster (`:407-408`); else mean support over blocking clusters that are NOT chained and have support (`:404`, `:410-412`). Chained clusters are listed (`:422`) but not split.
- Note the 1.0 value when there are no blocking clusters: the stage-2 exit evidence in scope slice 04 (F-18) reports `cluster_agreement` 1.000 everywhere, which this code path produces whenever the shadow runs had no blocking cluster or the agreement was otherwise trivially 1. [E1] (Which of these happened per run is UNVERIFIED here.)
- `citations` counts resolved/unresolved/malformed over all members (`:413`, `:429-431`).

### 2.7 `clusters_kept` (`cluster.py:436-487`)

Re-runs `cluster_v2` on copies of the records holding only the `(reviewer_id, finding id)` pairs in `kept`; block validity is unchanged (`:469-485`). This is the post-evidence-validator pass. [E1]

### 2.8 Q4: the "section always empty" over-merge path

Rule 1 (`cluster.py:163-164`) with the fp of `:119-123`: two findings whose primary citations are resolved, have the same role and the same path, the same non-empty ref set and the same (or both empty) deviation class merge **regardless of line distance**. For a single-file review target (a tasklist `plan` file, a spec), every finding cites the same path, so any two findings naming exactly the same requirement id (or set of ids) in the same class merge even if they are 400 lines apart and describe different defects. v1's fp includes the section (`findings.py:340-343`) and so is finer. Combined with transitive union-find (`:311-316`), one coarse fp match can bridge two otherwise separate span-based groups; the result is labelled `chained` (`:324-326`) only if some pair inside fails `same_defect_v2`. A cluster made entirely of fp matches (all same ref set) is never labelled chained even when members are far apart, because every pair matches by rule 1. [E1]

### 2.9 Q6: an anchor-only finding in `cluster_v2`

findings-v2 accepts a finding with no `citations` if it has an `anchor` of 12-200 chars (`findings_v2.py:122-126`). In `cluster_v2` such a finding has `citations = []` (`cluster.py:128-132`), `primary = None` (`:134`), `fp = None` (`:143-147`); rule 1 fails (no fp), rule 4 has no resolved citations (`:170-172`), so `same_defect_v2` is always False for it. **An anchor-only finding is always a singleton cluster.** Its anchor text is used only as input to `refs_norm` (`:138-141`). It still counts toward its reviewer's weight if calibrated (`:391-396`) and, if blocking, it forms a blocking singleton cluster whose support is that reviewer's share only. [E1] [CODE-VERIFIED; agrees with scope slice 02 section 3]

### Key Takeaways

- v2 changes the location unit (citations against a snapshot, no document text), adds deviation class to compatibility and fingerprint, adds chain detection, calibrated support and a confidence-chosen representative; it keeps v1's transitive union-find and v1's `refs_norm`. [E1 over E3]
- v2 is stricter than v1 on invalid blocks (drops every finding of the reviewer) and coarser than v1 on fingerprints (whole file instead of section). [E1]
- Anchor-only findings can never agree with anything in v2. [E1]
- v2 output is telemetry only: it neither drops nor routes findings (docstring and `cluster_cmd.py:9-13`). [E1]

---

## 3. `src/superclaude/cli/review/cluster_cmd.py` (197 lines) [E1]

- CLI `superclaude review cluster CARDS_DIR --snapshot --out [--calibration] [--coverage] [--kept]` (`cluster_cmd.py:96-133`).
- Cards: `*.md` in file-name order; file stem = reviewer id; ordinal = 1-based position in sorted order (`:138`, `:144-146`). So reviewer order (and thus representative tie-breaks and union-find roots) is alphabetical by card file name, not panel resolution order.
- Each card is parsed with `fv2.parse_block(text, assigned_rows, observed_rows)` (`:151`), no `lens` argument.
- Calibration: sidecar JSON `{reviewer_id: {finding_id: confidence}}` overrides embedded `calibration.per_finding` (`:152-153`); embedded calibration is read from fenced yaml or a bare `calibration:` block (`_embedded_calibration` `:31-47`).
- Snapshot: `card_convert._snapshot_entries` of the YAML (`:57-62`).
- Output: `<out>/panel/clusters.json` or `clusters_kept.json` (`:165-183`), plus a `cards` listing with `state`, `block_state` and `errors` per card (`:155-163`) and `calibration_coverage` (`:174-178`). The per-line parse errors ARE persisted in `cards[].errors` (`:161`), which answers the scope-02 open question for `cluster_cmd`. [E1]
- Card text is never modified (`:11-12`). [CODE-VERIFIED: only `target.write_text` at `:182`]

### Key Takeaways

- `review cluster` is the only CLI entry to `cluster_v2`; ordering is by card file name. [E1]
- Invalid cards are listed with all their errors, so the loss of findings is visible in the output, unlike v1's single warning (D1). [E1 vs E3]

---

## 4. `src/superclaude/cli/review/verify_cmd.py` (184 lines) [E1]

- CLI `superclaude review verify-citations --cards --snapshot --root --out [--coverage]` (`verify_cmd.py:76-113`), schema `review-precheck/1` (`:25`).
- For each citation of each parsed finding (`:139-157`): skip malformed (`:141-142`); flag `missing-file` if the path is not in the snapshot (`:47-48`), resolves outside `--root` (`:51-53`, `:62-63`) or is unreadable (`:59-60`, `:64-65`); `out-of-range` if `line_end` exceeds the file length (`:66-67`); `quote-not-found` (advisory) if the whitespace-normalised quote is not in the cited lines (`:68-72`).
- Writes `precheck.json` with a `reread_set` for the evidence validator (`:158-177`). Drops nothing (`:11-12`).
- Relation to clustering: it does not cluster; it uses the same snapshot loader (`cluster_cmd._snapshot_files`, `:118`) and the same "path in snapshot" rule as `cluster._citation` (`cluster.py:115`). It is the only place in v2 that opens the cited file, so it is the only v2 code that could detect a citation whose line numbers are stale. It checks the quote against the lines, not against the rest of the file, so it cannot relocate a moved quote. [E1]
- It reads findings of invalid blocks too (no state check before `:139`), unlike `cluster_v2`. [E1]

### Key Takeaways

- Citation checking and clustering share path rules but not finding sets (verify sees findings that cluster drops). [E1]
- A quote that moved lines is flagged `quote-not-found`, never re-located. [E1]

---

## 5. Q3 / D7: the shared reference-id regex versus real ids [E3, inherited by E1, observed by E2]

### 5.1 Where the token lives

- `findings.py:29` `_REF_TOKEN` (used by `refs_norm`, v1 and v2). [E3, E1]
- `telemetry.py:23` `_ID_TOKEN = r"(?:[A-Z]{1,4}-[0-9]+(?:\.[0-9]+)*|P[0-9])\b"` and `telemetry.py:24` `_ID_RE` (the scope prompt cites `telemetry.py:22`; line 22 is `_TS`, the token is at :23) [STALE DOC: line off by one]; also used in `_BOLD_DEF` (`telemetry.py:27`) and at `:164`, `:172` (id counting for telemetry). Same pattern text as `findings.py:29`, duplicated, not imported. [E3]

### 5.2 Probe (run 2026-11-13, `uv run python -c` calling `findings.refs_norm({"claim": s})`, read-only)

| Input in claim | `refs_norm` result | Note |
|---|---|---|
| `T01.02`, `Task T01.02` | `[]` | sc:tasklist task ids (format shown at `src/superclaude/skills/sc-tasklist-protocol/SKILL.md:343`, `:433`) are never refs |
| `AC-0.4` | `['AC-0.4']` | matches |
| `AC-T01.02-3` | `[]` | an AC id that embeds a task id does not match |
| `FR-001`, `NFR-12.3`, `REQ-0001`, `SC-1`, `GT-3` | matched | letters-hyphen-digits works |
| `ABCDE-1` | `[]` | 5+ letters: no word boundary before a 4-letter tail, nothing matches |
| `D-P1` | `['P1']` | W-2 confirmed: `P1` is extracted from inside `D-P1` |
| `P1` / `P12` | `['P1']` / `[]` | `P[0-9]\b` matches only P1-P9 |
| `R1-F1` | `[]` | reviewer-scoped finding ids do not match |
| `S-3 and S-6` | `['S-3','S-6']` | any id mentioned in prose becomes a key |
| `section 3.2`, `task 1.2` in prose | `[]` | section numbers only count as whole `refs` entries (`refs: ['3.2']` -> `['3.2']`) |
| lower-case `ac-1`, `sha-1`; `SHA-256` | `[]` | case-sensitive; `SHA-` filtered (`findings.py:337`) |

[CODE-VERIFIED for every row by execution]

### 5.3 Effect on clustering

- For a tasklist review, a finding about `T01.02` has `refs_norm == []` unless it also names an `AC-`/`FR-`-style id. Two findings with empty refs merge by span proximity alone (`findings.py:373-378`; `cluster.py:167-180`), and two findings with no refs can never merge by fingerprint (both rules require non-empty refs: `findings.py:371`, `cluster.py:163`). So D7 is CONFIRMED in code for both clusterers: tasklist findings cluster by span only. Whether real tasklist reviews in E2 mention `AC-`/`FR-` ids often enough to compensate is UNVERIFIED (hand-off D7 marks it INFERENCE). [E3, E1, E2]
- Conversely, prose ids create false bridges: W-2 (`D-P1` -> `P1`, pair P12) and any claim that mentions a neighbouring requirement (`S-3 and S-6`, the W-1 bundled finding P09) gives the finding extra refs, so rule 2's "refs intersect" gate opens to more partners. [E1]
- Mixed-ref asymmetry: if finding a has refs `{AC-1}` and finding b has `{}`, rule 2's gate (`ra & rb or (not ra and not rb)`) is False, so they NEVER merge even on the same line (`findings.py:374`; `cluster.py:167-169`). A reviewer who writes an id and one who does not will not be clustered together. [E3, E1]

### Key Takeaways

- The regex covers letters-hyphen-digits ids and P1-P9 only; it misses the task-id format sc:tasklist actually emits, misses 5+-letter prefixes and lower case, and over-extracts `P1` from compound ids. [E3, E1]
- The same pattern is copied in `telemetry.py:23`, so a fix must touch two places (or the copy must import one). [E3]
- Ref extraction from free prose is both a recall aid and a chaining source; a unified clusterer should prefer the declared `refs` list plus a per-target id grammar. [E1, E2, E3]

---

## 6. E1 measurement of `cluster_v2`: replay, pair sheet, weaknesses, tests [E1]

### 6.1 Stage 0a replay (`.dev/tasks/done/TASK-WF-implementStages0-20261111-202912/artifacts/stage0a-report.md`)

- Generated by `scripts/reflect_stage0a_replay.py`, zero dispatch (`stage0a-report.md:3`). Inputs are legacy reflect cards converted by `card_convert`, NOT cards written under the findings-v2 brief (`stage0a-report.md:7-12`). 8 of 43 card runs had no usable snapshot, so none of their citations resolve (`:11`, `:14`).
- Totals (`stage0a-report.md:243`): 689 clustered findings, 461 clusters, 392 singletons, "55 clusters holding two or more reviewers (29 not chained), 29 chained", 55 blocking; citations 1178 resolved / 623 unresolved / 283 malformed.
- Per-run table (`:247-291`) shows heavy merging in some runs: e.g. `pre-TASK-WF-brainstormFixBri-20261106-001016` 27 findings -> 7 clusters (`:249`), `pre-TASK-WF-p1LivePlanBrief-...-172548` 27 -> 9 (`:259`), `pre-TASK-WF-scIssueCommand-...-081732` 22 -> 8 (`:265`), `pre-TASK-WF-workerContractFo-...` 13 -> 4 (`:267`). Runs with no resolved citations stay all singletons (e.g. `pre-TASK-WF-implementIronbel-...` 28 -> 28, 0 resolved, `:253`).
- `cluster_agreement` is `1.0000` exactly in the runs with 0 blocking clusters and `null` in every run with blocking clusters (`:249-291`), because no recorded card carries a numeric calibration (0 of 689, scope slice 04 section 0.3). This matches the code path `cluster.py:405-412`. **[STALE DOC]** scope slice 04 section 0.3 says "cluster_agreement null for every listed run"; the table shows 1.0000 in 11 runs (e.g. `:251`, `:252`, `:261`, `:266`). [CODE-CONTRADICTED for that summary sentence, verified against `stage0a-report.md` rows and `cluster.py:407-408`]
- Agreement with recorded merged verdicts 24/358 = 6.70%, descriptive only (`:295-297`). [E1]

### 6.2 The 50-pair sheet and scorer (`scripts/reflect_cluster_pairs.py`, 559 lines)

- Sample source: legacy cards via `card_convert.convert_card_file`, clustered with `cluster_v2`, one record per card in name order, NO calibration (`reflect_cluster_pairs.py:8-12`, `:166-175`). Unlisted-shape cards are passed as block `None` = invalid (`:169-171`).
- Pair pool (`:181-211`): two findings of the same run from DIFFERENT cards; **pairs inside a chained cluster are not drawn** (`:183`; docstring `:17-19`; pinned by `tests/review/test_reflect_cluster_pairs.py:158-177`); same-reviewer pairs are not drawn (`:183`; test `:128-135`); pairs with a claimless finding are dropped and counted (`:190-192`).
- Stratification: 25 "merged" + 25 "apart", each half same-file and half cross-file, seeded `random.Random(f"{SEED}|{side}|{relation}")`, `SEED = 20261111` (`:83-84`, `:243-255`).
- Score: TP merged&same, FP merged&not, FN apart&same, TN apart&not; precision TP/(TP+FP), recall TP/(TP+FN) (`:340-397`).

### 6.3 Q7: what precision 0.84 / recall 0.95 mean

- Result: TP 21, FP 4, FN 1, TN 24; precision 0.84 (21/25), recall 0.9545 (21/22) (`pair-labels/README.md:18`). [E1]
- Labels are AI labels from 3 labelers (opus, sonnet, skeptical opus), 46 unanimous, 4 split 2-1 sent to a debate; P38 is the one label differing from plain majority (`pair-labels/README.md:7-14`). Labelers and `cluster_v2` come from the same model family (`:22`). Model-behaviour evidence, dated 2026-11-12 (`pair-labels/README.md:27`). [E1]
- Owner hand labels are PENDING (`pair-labels/README.md:3`, `:29`). The GitHub issues #525-#530 are recorded here as pending human labels (not queried, per task rule). [E1]
- What the design of the sample means for the two figures (analysis of `reflect_cluster_pairs.py:183` and `:243-255`, my reading of the code, not a claim of the source docs):
  - Precision 0.84 is an estimate for **unchained** multi-reviewer merges only. Chained clusters, the over-merge mode the E2 audit found dominant (section 7), are excluded from the pool by construction, so the figure says nothing about them.
  - Recall 0.95 mixes a 25-pair sample of merged pairs with a 25-pair sample of apart pairs drawn from a far larger apart population; FN in the population scales with the apart population, so 1 FN out of 25 apart samples is not evidence of population recall. The README already says "sample figures, not rates" (`:18`) and W-4 says the same (`cluster-v2-known-weaknesses.md:10`).
  - Bundled findings (W-1) and same-reviewer merges are unmeasured (`pair-labels/README.md:31`, `cluster-v2-known-weaknesses.md:7`).
  - Inputs are converted legacy cards, not findings-v2-brief cards.

### 6.4 Known weaknesses (`cluster-v2-known-weaknesses.md`)

| # | Doc claim | Tag |
|---|---|---|
| W-1 | Bundled finding clusters with findings matching one part; sampler skips same-reviewer pairs (`:7`) | [CODE-VERIFIED] for the sampler (`reflect_cluster_pairs.py:183`); the clustering effect follows from the any-citation, any-ref rule (`cluster.py:167-180`) |
| W-2 | `refs_norm` takes `P1` out of "D-P1" (`:8`) | [CODE-VERIFIED] by execution (section 5.2) |
| W-3 | `spec:N` resolved against the short `source.md` brief, not the spec (`:9`) | [UNVERIFIED]: this is in `card_convert` path mapping (scope slice 02 cites `card_convert.py:124-125` mapping `source.md`/`spec` tokens to role `spec`), not in `cluster.py`; not re-read here |
| W-4 | 0.84 / 0.95 are AI sample figures (`:10`) | [CODE-VERIFIED] against the scorer (section 6.3) |

None is fixed; cluster output stays telemetry (`:3`). [E1]

### 6.5 Tests pinning the current behaviour

- `tests/review/test_review_cluster.py`: span tolerance 3 (`:77`, `:89`), chain a-b-c listed as chained (`:108`), fully matching cluster not chained (`:124`), unresolved paths never span-match (`:135`), deviation-class compatibility (`:210`), empty-section fingerprint (`:233`), equal fp only with non-empty refs (`:244`), anchor-only findings stay alone even with identical anchor and refs (`:279-293`), chained clusters excluded from agreement (`:471`), invalid-block findings not clustered (`:556`). [E1]
- `tests/review/test_reflect_cluster_pairs.py:158-177`: a chain at `src/a.py` lines 10 -> 13 -> 16 (each step within 3 lines, ends 6 apart) is chained, and its internal pairs are not drawn. This fixture is also the simplest demonstration that a run of findings each 3 lines apart can grow without limit. [E1]
- Any unified clusterer that changes anchor-only, invalid-block or chain behaviour must update these tests deliberately. [E1]

### Key Takeaways

- E1's only quality number for `cluster_v2` (0.84 / 0.95) is AI-labelled, excludes chained clusters and same-reviewer pairs, and uses converted legacy cards; it does not measure over-merge by chaining. [E1]
- The replay shows strong merging in several runs (27 -> 7) and 29 chained clusters out of 461. [E1]
- `cluster_agreement` is 1.0 or null on recorded data; it has never been computed from real calibration in the replay. [E1]

---

## 7. E2 chaining evidence (commit `4a22d742`, read-only via `git show`) [E2 on E3 code]

Paths below are relative to `.dev/eval-workspaces/tasklist-review-panel/20261111-a1/` at `4a22d742`.

### 7.1 `analysis/audits/audit-D/anch.py` (31 lines)

- Reads each row's `ledger.json` and each reviewer's `findings-v1` block (`anch.py:13-19`), and counts findings by `(block_ok, kept in ledger, anchor in candidate, anchor2 in candidate)` (`:23-26`); prints up to 4 examples of dropped findings from invalid blocks (`:27-28`). The anchor test is a raw substring `a1 in cand[pkg]` (`:24`), not the whitespace-normalised `locate` of `findings.py`.
- **It does not compute chaining.** The task prompt names it as "E2 chaining evidence"; the chaining replay is in `audit-D/audit2.py` (section 7.2). [CODE-CONTRADICTED for that description; flagged in Stale Documentation] Its relevance to clustering is anchor resolution (missing anchors cannot span-cluster, D5 / X2). [E2]
- `anch.py:2` hard-codes the other worktree's absolute path, so it cannot be re-run from this checkout as committed. [E2]

### 7.2 `analysis/audits/audit-D/audit2.py` (the real chaining replay)

- Contains a line-for-line copy of `findings.py` clustering: `REF` (`audit2.py:41`) identical to `findings.py:29`; `refs_norm` (`:59-68`), `section_of` (`:69-76`), `ann` with the v1 fp (`:77-85`), `same` (`:87-94`) mirror `findings.py:307-379`. [CODE-VERIFIED by side-by-side read]
- For every ledger row with >= 3 members, re-annotates the members against the candidate and counts member pairs that are NOT directly `same` (`:139-155`); a row with any such pair is "chained". Width = max span end - min span start (`:151-152`). Mega-row = >= 8 members or >= 4 distinct sections (`:174`, `:179`).
- Counting caveat: `rows_total` is incremented for every row before the `< 3 members` filter (`:140`, `:145`), so "195 of 1398" means 195 chained rows among 1398 rows in total, not among rows with >= 3 members. **[STALE DOC]** `audit-D/summary.md:29` and scope slice 01 H16 say "195 of 1398 rows with >=3 members". [CODE-CONTRADICTED by `audit2.py:140-145`]
- Results (`audit-D/summary.md:29`, X1): 195 chained rows; 144 of them span > 60 candidate lines; **83 mega-rows**; example `r2-sonnet-ember/designSpec` L1: 19 members across 8 sections, 142/171 pairs unrelated; `n2-terra/design` L1 14 members; `n4-terra/design` L1 13 members; `g1-ember-luna2-r1/design` L1 merges a mode-label contradiction with unrelated artifacts-path findings. Effects stated: row anchor/claim = first member only, one mega blocking row counts as one row, overlap confidence and per-row recall inflated or hidden; verdict unaffected. Model-behaviour evidence dated 2026-11-12/13 (valid era, `COMBO-REPORT.md:289`). [E2]
- `audit-D/summary.md:30` (X2): 46 rows with null span (anchor not found), 13 blocking; they cannot span-cluster, so duplicates stay separate. [E2]

### 7.3 `COMBO-REPORT.md` from line 289

- `COMBO-REPORT.md:289` "FINAL RESULTS AND DECISION (2026-11-13)" supersedes earlier tables.
- `COMBO-REPORT.md:292` item 2 (audit D): "83 merged rows lump unrelated findings into one row (chaining), which can distort matching to ground truth"; the same paragraph reports the merge drops (56 / 18 / 14) and 49 blocking findings lost. The scorer judged rows against ground truth, so chained rows bias recall upward (a mega-row can "cover" several GT items) or misattribute (claim of member 0). How much the study's per-panel catch numbers moved because of chaining is not quantified in the report. [E2]

### Key Takeaways

- E2 is the only effort that measured v1 over-merge on real multi-reviewer output: 195 chained rows, 83 mega-rows, up to 19 members over 8 sections. [E2 on E3]
- E2's replay code is a faithful copy of `findings.py`, so the numbers describe the shipped v1 clusterer, and by the shared union-find and `refs_norm`, they are the expected failure class of `cluster_v2` too (E1 detects but keeps chains). [E2, E3, E1]
- Under v2's invalid-block rule, the 80 reviewer-level invalid blocks of E2 would lose ALL their findings, not just the 92 bad lines (inference from `cluster.py:256-257` applied to `audit-D/summary.md:7-8, :16-18`; not measured). [E1, E2]

---

## 8. Answers to the research questions

### Q1. Step-by-step comparison of the two algorithms

| Step | v1 `findings.cluster` [E3] | v2 `cluster.cluster_v2` [E1] |
|---|---|---|
| Entry | `ledger.merge_round` (`ledger.py:165`) via `superclaude review merge` | `superclaude review cluster` (`cluster_cmd.py:169`), `clusters_kept` (`cluster.py:447`), E1 scripts |
| Input | findings-v1 of all reviewers of one round + candidate document text (`ledger.py:128-138`) | records `(rid, ordinal, findings-v2 block, calibration)` + snapshot path list; no text (`cluster.py:3-15`) |
| Invalid block | parsable lines kept and clustered (`ledger.py:135-138`) | whole reviewer dropped (`cluster.py:256-257`) |
| Location | anchor quote located in text -> 0-based line span; optional anchor2 (`findings.py:346-360`) | citations `(role, path, line_start, line_end)`, resolved iff path in snapshot (`cluster.py:104-116`) |
| Refs | `refs_norm` over anchor/anchor2/claim/refs (`findings.py:321-337`) | same function (`cluster.py:64`, `:135-141`) |
| Fingerprint | `sha256("v1|section|refs")[:16]` (`findings.py:340-343`) | `sha256("v2|role|path||refs|class")` over primary citation; section "" (`cluster.py:119-123`) |
| Same-defect | fp+refs, else (refs intersect or both empty) and spans within 3 lines (`findings.py:367-379`) | fp+refs, else class compatible and (refs intersect or both empty) and a resolved citation pair on the same path within 3 lines (`cluster.py:161-181`) |
| Merge | transitive union-find, O(n^2) (`findings.py:382-407`) | same (`cluster.py:302-320`) |
| Chains | not detected | `chained` flag, excluded from agreement, not split (`cluster.py:324-326`, `:404`, `:422`) |
| Representative | member 0 gives fp, category, anchor, claim (`ledger.py:182-199`) | highest calibrated confidence, tie -> resolution order (`cluster.py:338-344`); with no calibration this is member 0 |
| Blocking | any member (`ledger.py:187`) | `blocking_any` / `blocking_all`, `disputed` (`cluster.py:345-351`, `:375-376`) |
| Output | ledger rows driving PASS/FAIL (`ledger.py:273-274`) | `clusters.json` telemetry: clusters, support, agreement, chained, citation counts (`cluster.py:414-433`) |
| Versions | spans diff-mapped between versions (`ledger.py:343-346`) | none |

### Q2. D6: transitive chaining and the first member's claim and category

- [E3] CONFIRMED: union-find (`findings.py:382-407`) is transitive; a chain of findings each within 3 lines of the next joins regardless of total width (E2: 144 chained rows wider than 60 lines). The new row takes `category` and `claim` from `group[0]` (`ledger.py:191`, `:199`) and never updates them on refound (`ledger.py:207-238`).
- [E1] v2 keeps transitivity (`cluster.py:311-316`), labels chains (`:324-326`), drops them from `cluster_agreement` only (`:404`); the cluster's `claim` is the representative's (`:374`), which on uncalibrated data (all recorded data, 0/689) falls back to resolution order, i.e. member 0 (`:338-344`). The v2 cluster has no single category; members keep `deviation_class` and `disputed` flags a class conflict (`:346-351`).

### Q3. D7: see section 5. CONFIRMED by execution: `T01.02` and `AC-T01.02-3` give no refs; `AC-0.4` matches; `D-P1` yields `P1`.

### Q4. v2 chain detection and the "section always empty" over-merge: see sections 2.5 and 2.8. Equal non-empty ref sets + same class + same primary path merge at any distance; such all-fp clusters are never flagged `chained`.

### Q5. Yes. `cluster_v2` drops every finding of a reviewer whose block state is not `complete` (`cluster.py:220-221`, `:256-257`), and one bad line makes the block `invalid` (`findings_v2.py:299-303`). Pinned by `tests/review/test_review_cluster.py:556`.

### Q6. An anchor-only finding is always a singleton in `cluster_v2` (`cluster.py:128-147`, `:163-181`); pinned by `tests/review/test_review_cluster.py:279-293`.

### Q7. Precision 0.84 / recall 0.95 are AI-labelled sample figures over unchained, cross-reviewer pairs from converted legacy cards; human labels pending (GitHub #525-#530, recorded as pending, not queried). See section 6.3.

### Q8. A code finding with path+line that moves between commits

- Inside one `cluster_v2` call every reviewer is matched against one snapshot path list (`cluster.py:86-101`); only the path string is used, never a commit id or file hash (`cluster.py:96`, `card_convert.py:434-441`). If two reviewers cite the same defect at different line numbers because they read different commits (or the working tree changed between dispatches), the citations merge only if within 3 lines (`cluster.py:177-178`); otherwise only an equal fingerprint can join them, which needs equal non-empty refs (`:163`). Code findings typically carry no requirement ids (refs harvested only by `_REF_TOKEN`), so in practice they stay apart. [E1] (Typical-refs claim is an inference, not measured.)
- Across review rounds (re-review after a new commit) v2 has no ledger and no line mapping; there is nothing to move a citation. [E1]
- v1 has diff mapping (`findings.py:413-457`, `ledger.py:301-347`) but for ONE document's text only, keyed by sha256 of the reviewed text (`ledger.py:308-314`); it cannot map multi-file code citations. [E3]
- `verify-citations` will flag a moved quote as `quote-not-found` (`verify_cmd.py:68-72`) but does not relocate it. [E1]
- Nothing in E2 addresses code (E2 targets were tasklist documents). [E2]

### Q9. Design input for one clusterer

Each item names the existing code it would reuse or replace. These are design inputs, not verified behaviour.

1. **One location model**: a finding location = list of `(role, path, line_start, line_end, quote?)`; an anchor-only finding is converted to a citation by locating its anchor in the snapshot file of its role (reuse `findings.locate`, `findings.py:276-304`, and v2 `_citation`, `cluster.py:104-116`). This removes the anchor-only singleton (Q6) and lets v1 consumers use one path. [E1, E3]
2. **Version pinning**: snapshot entries carry a content hash or commit; citations resolve only against the pinned version; across versions, map lines with `findings.opcodes`/`map_span` per file, or relocate by quote (extend `verify_cmd._check`). Answers Q8. [E1, E3]
3. **Section back in the fingerprint**: compute section from the cited file text when it is Markdown (reuse `findings.section_of`), and for code use the enclosing symbol (codegraph or a simple def/class scan; not in the codebase today). Removes the "section always empty" path (Q4). [E1, E3]
4. **Per-target id grammar**: replace the single `_REF_TOKEN` with a list of id patterns per review module (tasklist `T\d{2}\.\d{2}`, `AC-...`, spec `FR-`/`NFR-`, none for code), prefer declared `refs` over prose, and match whole tokens only (fixes W-2 `D-P1`). One definition imported by `findings.py` and `telemetry.py:23`. [E1, E2, E3]
5. **Chain control**: after union-find, split any component that fails a complete-link (every pair `same_defect`) or a size/width cap (E2 evidence: mega-rows at >= 8 members, > 60 lines) by re-running agglomeration with complete or average linkage; keep v2's `chained` flag for whatever survives. Same-reviewer merges should need stronger evidence (W-1). [E1, E2, E3]
6. **Invalid blocks**: one explicit policy instead of two opposite ones (v1 keep, v2 drop all): cluster the valid lines, mark the reviewer `partial`, exclude it from agreement denominators, and persist per-line errors (as `cluster_cmd.py:161` already does). [E1, E2, E3]
7. **Representative and row fields**: row claim/category from the highest-confidence member (v2), and recomputed on refound (fixes v1 `ledger.py:191`, `:199`); with no calibration, prefer the member with most resolved citations rather than member 0. [E1, E3]
8. **Measurement**: extend `reflect_cluster_pairs.py` to sample pairs inside chained clusters and same-reviewer pairs, and score on findings-v2-brief cards; reuse E2's ground-truth packages and `audit2.py` chain counter as a regression check. [E1, E2]

### Key Takeaways

- The two clusterers share the core weakness (transitive union-find + prose regex refs) and differ in location model, invalid-block policy, fingerprint grain and representative choice. [E1, E3]
- A unified clusterer needs one location type, a version pin, section/symbol in the fingerprint, per-target ids and chain splitting; each has an existing code piece to start from. [E1, E2, E3]

---

## Gaps and Questions

1. **[UNVERIFIED] W-3** (`cluster-v2-known-weaknesses.md:9`): `spec:N` resolved against the short `source.md` brief. The mapping lives in `card_convert` (not re-read here); it affects which file a spec citation resolves to, so it matters for the unified location model. [E1]
2. **[UNVERIFIED] D7 effect on real tasklists**: whether real tasklist findings in E2 carried `AC-`/`FR-` ids often enough to avoid span-only clustering was not measured (hand-off D7 marks it INFERENCE). The E2 reports could be replayed with `refs_norm` to count empty-ref findings. [E2, E3]
3. **[UNVERIFIED] Population precision/recall of `cluster_v2`**: the 0.84 / 0.95 figures exclude chained clusters and same-reviewer pairs; human labels (GitHub #525-#530) are pending and were not queried. [E1]
4. **[UNVERIFIED] Shadow-run `cluster_agreement` 1.000**: scope slice 04 F-18 reports 1.000 everywhere in Stage 2 shadow runs; whether that is the "no blocking cluster" branch (`cluster.py:407-408`) or real calibrated agreement was not checked against the run files. [E1]
5. **[UNVERIFIED] Invalid-block loss under v2 on E2 data**: the statement that v2 would drop all findings of E2's 80 invalid reviewer blocks is an inference from code; not replayed. [E1, E2]
6. **[CODE-CONTRADICTED] Prompt description of `anch.py` as chaining evidence**: `anch.py` measures anchor presence and kept status; the chaining replay is `audit2.py:139-179`. [E2]
7. **[CODE-CONTRADICTED] "195 of 1398 rows with >=3 members"** (`audit-D/summary.md:29`, repeated in scope 01 H16): code counts 1398 as all rows (`audit2.py:140-145`). [E2]
8. **[CODE-CONTRADICTED] "cluster_agreement null for every listed run"** (scope 04 section 0.3): 11 runs show 1.0000 (`stage0a-report.md:251` etc.). [E1]
9. **Ambiguous replay total**: `stage0a-report.md:243` says "55 clusters holding two or more reviewers (29 not chained), 29 chained"; how many of the 29 chained clusters are multi-reviewer is not derivable from the totals line alone. [E1]
10. **Line-number convention mismatch**: v1 spans are 0-based half-open (`findings.py:302`), v2 citations are 1-based inclusive (`findings_v2.py:77`). Both apply a tolerance of 3; the effective tolerance differs by one line at the end boundary. A unified clusterer must pick one convention. [E1, E3]
11. **No code-level symbol or section for v2** exists anywhere in `cli/review`; Q9 item 3 needs new code or a codegraph call. [E1]
12. **Question for E3 owners**: should invalid-block findings keep counting toward a blocking verdict (v1, `ledger.py:135-138`), given D1-D3? The unified policy must decide. [E3]
13. **Ordering dependence**: both clusterers pick member 0 by input order (v1 report order, v2 card file-name order in `cluster_cmd.py:138`), so representative claims depend on reviewer naming when uncalibrated. Not measured. [E1, E3]

## Stale Documentation Found

- **[STALE DOC]** Task prompt: `telemetry.py:22` (`_ID_TOKEN`) - the token is at `telemetry.py:23`; line 22 is `_TS`. (Scope 02 D7 row already notes the hand-off said :23 for `_ID_RE`, which is at :24.)
- **[STALE DOC]** Task prompt calls `audit-D/anch.py` the E2 chaining evidence; chaining is computed in `audit-D/audit2.py:139-179`.
- **[STALE DOC]** `audit-D/summary.md:29` and scope 01 H16: "195 of 1398 rows with >=3 members"; 1398 is all rows (`audit2.py:140-145`).
- **[STALE DOC]** Scope 04 section 0.3: "cluster_agreement null for every listed run"; 11 runs show 1.0000 (`stage0a-report.md:247-291`).
- **[STALE DOC]** `audit-D/summary.md:2` and `anch.py:2` point to `/tmp/audit-D/...` and to the other worktree's absolute path (already noted in scope 01 gap 5).
- `cluster-v2-known-weaknesses.md:8` cites `findings.py:29` "re-read before relying": re-read, still correct (no staleness).
- `cluster.py` module docstring (`:1-56`): every rule checked against the code in section 2; no contradiction found.

## Summary

The two clusterers differ in inputs, location model and fingerprint grain but share their weakest parts: v1 `findings.cluster` [E3] and v2 `cluster_v2` [E1] both use transitive O(n^2) union-find and the same prose-harvested `refs_norm` regex. That regex misses sc:tasklist ids such as `T01.02` and pulls `P1` out of `D-P1`, as the probe run on 2026-11-13 showed. E2's faithful replay of v1 (`audit2.py`) found 195 chained rows and 83 mega-rows (up to 19 members over 8 sections). v2 only flags chains, does not split them, and adds a coarser over-merge path: the section is always empty, so equal refs on the same file merge at any distance. v2 also drops every finding of an invalid reviewer block and leaves anchor-only findings as singletons. Its only quality figures (precision 0.84, recall 0.95) are AI-labelled sample figures that exclude chained and same-reviewer pairs; human labels are still pending. A unified clusterer should use one citation-based location model with version pinning, put the section or symbol back into the fingerprint, use per-target id grammars, split chains with complete-link or size caps, and adopt one invalid-block policy, reusing v1's diff mapping and v2's chain flag, support and representative logic.
