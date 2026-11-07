# Merge Log: /sc:issue --claim --worktree

- Base: `variant-1-opus-architect.md` (Variant A). Plan: `refactor-plan.md`, 16 changes, applied in order.
- Output: `merged-output.md`. Executed 2026-11-05 by the merge-executor. No repo file was edited; no Orca, gh or git write was run.
- Method: stub with all headings and TODO lines, then filled section by section with Edit; then one full rewrite of the filled file to meet the 3200-word limit (first fill was 4592 words).
- Result: 16 of 16 changes applied (11 applied, 5 applied-modified, 0 skipped).

## Changes

### Change 1: No new ref; Wave 7 in `refs/claim.md`
- Status: applied
- Before: Wave 7 in a new `refs/worktree.md`; FR-3 said that ref does not load; section 8 listed the new ref.
- After: Wave 7 is a section of `refs/claim.md`; the script gets one `SKILL.md` files-table row; sections 1, 3 (FR-3, FR-5), 5, 8 rewritten; notation paragraph added under the title.
- Provenance: `<!-- Source: Base (original, modified) - Changes #1, #2 -->` (s1), `<!-- Source: Round 2 / plan Notation - merged per Change #1 -->`.
- Validation: pass. `test_issue_protocol.py:165` (five refs) and `:131` (every `scripts/*.py` named in SKILL.md) re-read; both stay satisfied by the spec as written.

### Change 2: Name `issue-<N>`, no title text, no explicit branch
- Status: applied-modified
- Before: `--name issue-<N>-<slug>` with a 40-character rule; script took `--title`.
- After: exact create argv of the plan in section 4; 2.3 rewritten; the base edge row for an empty title-derived name dropped; `--title` removed from the script call (no longer used).
- Modification: dropping `--title` and the edge row were not named in the plan; both follow directly from removing the name suffix.
- Provenance: `<!-- Source: Base (original, modified) - Change #2 -->`.
- Validation: pass. The create argv occurs once (section 4) and matches the plan character for character.

### Change 3: Lookup keys and match rules
- Status: applied-modified
- Before: marker equals, else basename; "reuse first marker match" on several matches; path gone gives stale.
- After: 2.5 lists four keys (marker, record, basename, branch last segment), archived rows dropped, dedupe by row `id`, first key with a hit decides, exactly one live hit reused, stale-only stops, two or more live hits stop as ambiguous.
- Modifications: (1) the plan's "at least one live hit: reuse it (first by list order)" conflicts with its own "two or more live hits: ambiguous"; merged as "exactly one live hit". (2) "`comment` contains `sc:issue <R>#<N>`" would let issue 3 match a marker for issue 30; added "not followed by a digit".
- Provenance: `<!-- Source: Base (original, modified) - Changes #3, #7 -->`.
- Validation: pass. Edge rows FO-2, FO-3, FO-8, FO-10, FO-13 cite the rule.

### Change 4: List completeness and empty-list guards
- Status: applied
- Before: no truncation or partial-list check.
- After: FR-15 (`ok`, `result.truncated`, `result.hostScope.omittedHostIds`, zero rows, no `isMainWorktree` row), also on the after-create list; edge row and FO-12.
- Provenance: `<!-- Source: Round 2 / INV-001 - merged per Change #4 -->`.
- Validation: pass.

### Change 5: New path after create
- Status: applied
- Before: path and branch from the create JSON, else re-list by marker.
- After: section 5 step 5 and FR-20: snapshot ids, re-list after exit 0 or a timeout, set difference filtered by basename; 0 new ids create-failed "created but not listed", 2 or more ambiguous with no copy and no record; create JSON is not the source.
- Provenance: `<!-- Source: Variant B, Section 5 - merged per Change #5 -->`.
- Validation: pass.

### Change 6: Copy rule
- Status: applied
- Before: recursive copy, overwrite on re-claim; edge row "overwritten on re-claim".
- After: 2.4 per-file walk with tracked-skip, missing-copy, identical-skip, single `.prev`, realpath self-copy skip, `worktree.json` excluded, "untracked" line only when nothing is tracked; FR-19; edge rows FO-14, FO-15, FO-16.
- Provenance: `<!-- Source: Variant B, Section 2.4 - merged per Change #6 -->`.
- Validation: pass. The literal recursive-copy command does not occur.

### Change 7: Record file owned by the script
- Status: applied
- Before: the skill wrote script stdout to `<D>/worktree.json`, including failures.
- After: FR-18 (script writes `{"path", "status"}` only on created or reused, guard before use, never copied); record is key 2 in 2.5; list-failure reuse "reused from record, unverified" in section 5 step 3 and the warning table; B's dissent recorded in 2.5 and section 10.
- Provenance: `<!-- Source: Variant C, Section Q5 - merged per Change #7 -->`.
- Validation: pass.

### Change 8: Base ref checks
- Status: applied-modified
- Before: none.
- After: FR-16 and the section 4 command list (`git fetch origin`, `git rev-parse --verify origin/<B>`, 120 s); `W-ORIGIN-BASE-MISSING`, `W-ORIGIN-BASE-STALE`.
- Modification: the check runs only before a create (section 5 step 5), not on reuse, since the base ref matters only to a create.
- Provenance: `<!-- Source: Round 2 / INV-009 - merged per Change #8 -->`.
- Validation: pass.

### Change 9: Post-condition before success
- Status: applied
- Before: none.
- After: FR-17; section 5 step 7; failure gives `failed` with a named warning (copy or stale).
- Provenance: `<!-- Source: Round 2 / INV-016 - merged per Change #9 -->`.
- Validation: pass.

### Change 10: Return contract and warning codes
- Status: applied-modified
- Before: four fields; six codes including the dropped "multiple" code.
- After: five fields including `worktree_match_key`; eight codes in one table with status, trigger and remedy line; "reused a worktree not created by /sc:issue" on basename or branch keys; script JSON gains `match_key`.
- Modifications: (1) a one-line definition of `skipped` versus `failed` added so each code has one status. (2) The single `worktree_warning` field cannot carry two codes; recorded as an open item in section 9 with a proposal, not decided.
- Provenance: `<!-- Source: Base (original, modified) - Change #10 -->`; remedy column `<!-- ... remedy column from Variant C, Section 4 -->`.
- Validation: pass. All eight codes defined; no other `W-` code used.

### Change 11: Tests
- Status: applied
- Before: one fake-orca file, static pins, AC-1 to AC-6.
- After: ST-1 to ST-6, FO-1 to FO-17 (adjusted to Changes 3 to 9), OB-1 to OB-4, real-shape fixtures; AC-1 to AC-7, each tied to a test ID. FO expected results live in section 6 to avoid a duplicate table.
- Provenance: `<!-- Source: Base (original, modified) - Change #11, IDs from Round 2 / C O7 -->`.
- Validation: pass. Every FO, ST and OB ID is defined in section 7 and cited at least once in section 6 or the AC list.

### Change 12: Design-doc decision wording
- Status: applied
- Before: "recorded as B16"; 2.1 said the worktree "stays inside B2".
- After: 2.7 states B16 as an addition to B2, allowed only because no next-step command runs, owner confirmation required, flag withdrawn without it; 2.1 aligned; R9 rates it.
- Provenance: `<!-- Source: Base (original, modified) - Change #12 -->`.
- Validation: pass. The overstated "B2 untouched" wording does not occur.

### Change 13: Risks with ratings, out-of-scope list, FR wording
- Status: applied
- Before: unrated risks; FR-4 "after Wave 6 step 3 succeeded"; FR-8 unconditional.
- After: FR-4 "after both Wave 6 comments are posted"; FR-8 "unless `W-WORKTREE-COPY-FAILED` names the reason"; risk table R1 to R11 with likelihood and impact; R7 upstream project id; out-of-scope list.
- Provenance: `<!-- Source: Base (original, modified) - Changes #13, #14 (Variant B, Section 9) -->`, `<!-- Source: Variant B, Section 9 - merged per Change #13 -->`.
- Validation: pass.

### Change 14: Manual-run verification list
- Status: applied
- Before: AC-1 checked row, location and merge-base only.
- After: AC-1 also records `comment`, basename, prefixed branch, create JSON shape, suffix on a taken name, `projectId`, `.claude/` presence, empty `linkedIssue`/`linkedPR`; AC-4 byte-identical; `make sync-dev` hint in Wave 7 step 2; every UNVERIFIED item in section 9 names its check.
- Provenance: `<!-- Source: Base (original, modified) - AC-1 per Change #14; AC-4 per Variant C -->`.
- Validation: pass.

### Change 15: Accepted risks recorded, not built
- Status: applied
- After: section 9 "Accepted, not built" for INV-006 and INV-008.
- Provenance: `<!-- Source: Round 2 / INV-006, INV-008 - merged per Change #15 -->`.
- Validation: pass.

### Change 16: Edge-case table merge
- Status: applied-modified
- Before: 11 behavior-only rows.
- After: 21 rows with a Test column; C's rows added (record deleted, deleted worktree, claim from another worktree, unflagged after flagged, daemon down, wrong repo inferred, `E-POST-FAILED`).
- Modification: to meet the word limit, some related cases share a row (one live hit with record deleted; user edit with tracked file). The base row for an empty name was dropped (Change 2).
- Provenance: `<!-- Source: Base (original, modified) - empty-name row dropped (Change #2); Variant C, Section 6 rows merged per Change #16 -->`.
- Validation: pass.

### Merge-requirement additions
- Section 2.8 (plan's rejected-decisions table) and section 10 (provenance checklist) added, as the task required.

## Post-Merge Validation

### (a) Structural
- One H1 (`# Spec: /sc:issue --claim --worktree`), YAML frontmatter with the five required keys, a 3-line provenance header after it, a Notation paragraph under the title.
- H2: sections 1 to 9 in the base order and numbering, plus `## 10. Provenance and verification checklist`. 10 H2 total.
- H3: 2.1 to 2.8, all under section 2. No orphan H3, no skipped level.
- Result: PASS.

### (b) Internal references
- Requirement and test IDs: 66 distinct IDs, 139 uses. Defined in the document: FR-1 to FR-20, AC-1 to AC-7, ST-1 to ST-6, FO-1 to FO-17, OB-1 to OB-4 (54). INV-001 to INV-011 and INV-016 (12) resolve to `invariant-probe.md`. Risk IDs R1 to R11 defined in the section 9 table.
- Section references: section 4, 5, 6, 7, 9 and 2.4, 2.5, 2.7: all exist.
- Warning codes: 8 used, 8 defined in the section 4 table. STOP codes: `E-CLAIM-ONLY-FLAG` defined in section 4; `E-CREATE-ONLY-FLAG`, `E-POST-FAILED` are existing codes of the command (`refs/claim.md:89`).
- External IDs (B2, B16, D3, D24, X-00n, C-00n, S-001, "C R5") resolve to the design doc or `diff-analysis.md`.
- Totals: 66 distinct internal IDs, 66 resolved, 0 broken.

### (c) Contradiction re-scan
- (i) MUST-exist versus a failing edge row: FR-8 now carries "unless `W-WORKTREE-COPY-FAILED` names the reason"; the copy-error edge row reports `failed` with that code. No conflict. The FR-17 text was checked against the `.prev` and tracked rows: consistent.
- (ii) Banned residue: grep for the name-suffix word, the recursive-copy command, the dropped ref name, the "literally true" phrase, the dropped "multiple" code, "first of several" and "first by list order": 0 hits. Explicit-branch and setup flags occur only in the FR-6 forbidden list. Fixed in place during the merge: the plan's "reuse it (first by list order)" was replaced by "exactly one live hit is reused" (it conflicted with the ambiguity rule).
- (iii) Argv: the list and create command lines occur once each, in section 4 only. FR-7 names `orca worktree create` without arguments. An earlier draft repeated a list command in a remedy cell; removed.
- (iv) Codes: the eight codes of the section 4 table equal the set used in sections 2, 3, 5, 6, 7 and 9. Section 6 uses the short forms "base-missing", "base-stale", "create-failed", "ambiguous" only in rows whose code is named in section 4 or FR-16.
- Fixed in place, beyond the plan text: marker match tightened to "not followed by a digit" (issue 3 versus 30); base-ref check placed before create only. Both logged under Changes 3 and 8.
- Result: PASS after fixes.

### (d) Grep checks
- Em dashes (U+2014) and en dashes (U+2013): 0.
- Orca link flags and agent, setup, branch, activate flags (`--issue`, `--pr`, `--reference`, `--linear-issue`, `--gitlab`, `--agent`, `--prompt`, `--model`, `--effort`, `--surface`, `--setup`, `--branch`, `--activate`, `--run-hooks`): 1 line matches, line 107, the FR-6 forbidden list. 0 outside it.
- Result: PASS.

### Word count
- 3199 words that contain a letter or digit (limit 3200). `wc -w` gives 3730 because it also counts table pipes and list bullets.

### Orchestrator corrections after the merge (2026-11-05, found on re-reading the merged file)
The merge-executor's contradiction re-scan passed, but three defects remained; the orchestrator fixed them in `merged-output.md`:
1. Section 6 had one row "Two live hits, or two keys on different rows | ambiguous ... first key decides", which contradicts 2.5 (the first key decides; ambiguity counts only inside that key). Split into two rows: two or more live hits in the deciding key give `W-WORKTREE-AMBIGUOUS`; two keys hitting different rows reuse the first key's single live hit.
2. Section 4 ran `git -C <wt> rev-parse --git-common-dir` without `--path-format=absolute`, so FR-17's comparison against `<main>` could compare a relative path; added the flag.
3. Section 2.1 paraphrased B2 as "forbids running a next-step command"; the design doc (line 27) says the claim "stops after writing the next-step prompt". Reworded.
Also changed the edge row "Wrong repo inferred | impossible" to "not inferred: `--repo path:<main>` is explicit; the upstream project-id exposure is risk R7", because "impossible" overstated what the explicit repo selector proves.
After the fixes: 0 em or en dashes, 0 stale terms (slug, recursive copy, new ref, "stays literally true", `W-WORKTREE-MULTIPLE`), forbidden flags only in the FR-6 list. Final length 3779 `wc -w` words (about 3200 words excluding table pipes).

### Not resolved
- `worktree_warning` holds one code; which code wins when two apply is not decided by the plan. Recorded in section 9 "Open items" with a proposal.
- Several Orca behaviours stay UNVERIFIED by design (R1 to R7); each names its check in AC-1.
