# QA Report: R5 template-conformance lens

**Topic:** R5 edit (item 6.3) to `docs/designs/orchestrator-mode.md`, form and style only
**Date:** 2026-11-09
**Phase:** fix-cycle gate review, template-conformance lens
**fix_authorization:** false (no file edited except this report)
**Design file state:** `docs/designs/orchestrator-mode.md`, 1047 lines (`wc -l`), untracked in git (`?? docs/designs/orchestrator-mode.md`), so conformance was measured against `artifacts/design-base.md` and the sibling rows, not a git diff.

## Findings

No BLOCKING and no MAJOR finding. Five MINOR notes follow. Minor notes never fail the gate.

| id | severity | evidence | what is wrong | smallest fix |
|---|---|---|---|---|
| F1 | MINOR | `docs/designs/orchestrator-mode.md:824` (section 13 intro) against `:837` (D10 Source cell) | The intro says each deviation "comes from the PANEL, FIXREVIEW or the design review". D10's Source cell is "Owner decision R5, 2026-11-08", which is none of the three. The sentence is now slightly untrue. | Add "or an owner decision" to line 824. |
| F2 | MINOR | `docs/designs/orchestrator-mode.md:1039` against `:1047` | The `### Fix cycle 3` intro says the changes are "for the blocking findings of review 3 and the re-anchor to master `5dc29d23`". R5 is an owner decision, not a review finding or the re-anchor. Fix cycles 1 and 2 each state their source exactly. | Add "and the owner decision R5 of 2026-11-08" to line 1039. |
| F3 | MINOR | `docs/designs/orchestrator-mode.md:1047` (R5 revision row), `:719` and `:766` (routing row R5), `:976` ("R1, R2, R3, R4, R5 Revert together") | The revision ID `R5` collides with the section 9 routing row `R5`. The collision already existed for `R4` at `:1046`, so R5 follows the R4 precedent. | None required. Optionally write the ID as `R5 (owner)`. |
| F4 | MINOR | `docs/designs/orchestrator-mode.md:895` and `:914` ("Whether each template accepts its flags as written"), `:1000` ("A template that fails is dropped only with an owner note") | Step 1.0a issues only templates 1 to 8 (`:895`). Item 11 and open item 10 still say "each template", so the two new `--agent-wait` templates are covered by the NFR-014 pin but are never captured. | Say "each captured template (1 to 8)" at `:914` and `:1000`, or accept that the new templates stay unchecked. |
| F5 | MINOR | `docs/designs/orchestrator-mode.md:535` and `:536` | The two new comments start at columns 46 and 53; the older ones at `:533`, `:534` and `:537` start at 46. The longer tuple at `:536` forces the shift, so this is not a style break. | None. |

## Checks

| id | check | result |
|---|---|---|
| C1 | R5 row at `:1047` is inside the `### Fix cycle 3` table (header `:1041`, separator `:1042`) and is the row right after R4 (`:1046`) | PASS |
| C2 | R5 row has 4 unescaped pipes, which is 3 cells (`| ID | Finding | Change |`), the same as every row at `:1041`-`:1047` (awk pipe count: 4 on each) | PASS |
| C3 | R5 ID style matches R4 (bare `R<n>`, no `-B`/`-<n>` suffix) and its Change cell ends with a section list in the same form as R3-B1 to R4 | PASS (see F3 for the routing-row ID overlap) |
| C4 | Two new `ALLOWED_ORCA` tuples at `:535`-`:536` use the same tuple-of-quoted-tokens form, the same trailing comma and the same `# <reason>, not called in Phase 1` comment form as `:533`-`:534`; the closing comment `# 10 templates, 7 verbs (NFR-014)` at `:537` follows the old pattern; the code fence still opens at `:523` and closes at `:551` | PASS |
| C5 | `FORBIDDEN_TOKENS` at `:539` is a one-element `frozenset` with the same comment form as before | PASS |
| C6 | D10 row at `:837` has 6 unescaped pipes (5 cells), the same as D1 to D9 (`:828`-`:836`), with columns ID, SPEC text, Design, Source, Section in order; its Section list `2.2, 4, 7.3, 11, 12, 15.1` is the same form as D1 to D9 and agrees with the sections that carry the change (`:66`, `:221`, `:535`, `:759`, `:815`, `:895`) | PASS |
| C7 | The D10 SPEC citations are real: SPEC lines 132, 143, 310, 323, 500, 504, 510, 562 and 619 all contain `agent-wait`, an allowlist rule or the INV-005 pin (`grep -n` on `merged-requirements.md`) | PASS |
| C8 | `Total: 10 deviations.` at `:839` matches D1 to D10; no `9 deviations` or `D1 to D9` text remains | PASS |
| C9 | Section 13 REPORT-differences table (`:849`-`:857`) is untouched in cell count (4 pipes per row) and its 1.0a row at `:851` reads "templates 1 to 8 of the ten allowlisted templates", which agrees with `:895` | PASS |
| C10 | Section 4: the extension-point sentence at `:221` carries "(only after a capture or a recorded owner decision (R5, 2026-11-08), and never a write verb)" in the same parenthetical form; the diagram labels at `:181` and `:196` read `ALLOWED_ORCA (10)` and `10 read templates`, and every diagram line at `:179`-`:186` stays 86 characters with the column positions kept (31 and 37) | PASS |
| C11 | GQ-109 row at `:66` has 5 unescaped pipes (4 cells), the same as `:55`-`:67`; its Anchors cell is unchanged | PASS |
| C12 | NFR-014 row at `:815` has 4 pipes and reads "ten templates (7.3)"; all rows at `:774`-`:820` have 4 pipes | PASS |
| C13 | Section 11 row for `test_probes_allowlist.py` (`:759`) still has 4 pipes; the positive `--agent-wait` case and the ten-template pin sit in the same "Main cases" sentence style | PASS |
| C14 | Section 15.1 bullet at `:895` keeps the bullet form; the capture table at `:902`-`:916` keeps 4 pipes per row | PASS |
| C15 | Section numbering unchanged: the heading list of the edited file differs from `artifacts/design-base.md` only by the WC-14 to WC-16 renames at lines 34, 35 and 38 of the heading list (R4) and the added `### Fix cycle 3`; no `##` or `###` number was added, removed or moved | PASS |
| C16 | No em-dash or en-dash: `grep -n '—\|–'` returns nothing | PASS |
| C17 | No `TODO`, `TBD` or `FIXME`: `grep -nw` returns nothing | PASS |
| C18 | No trailing whitespace and no tab character anywhere in the file | PASS |
| C19 | `r5-mechanical.md` counts match my own run: 10 deviations (`:839`), 23 open items (`:1015`), 0 em-dash, `FORBIDDEN_TOKENS` at `:539`, three `ps` templates at `:532`, `:535`, `:536` | PASS |
| C20 | Cross-source agreement for the form of the claim: `WORKER-CONTRACT.md:110` names `worktree ps --agent-wait`; research/07 lines 114-119 quote the same text; `OQ-1-agent-wait-decision.md` lines 19-22 hold the owner words "Allow it, no conditions needed." that D10 (`:837`) and R5 (`:1047`) quote; SPEC `:143` states the old eight-template pin that D10 names as changed | PASS |
| C21 | Section 13 intro sentence (`:824`) still describes the sources of every row | FAIL (minor, F1) |
| C22 | `### Fix cycle 3` intro (`:1039`) still describes the sources of every row | FAIL (minor, F2) |
| C23 | Steps 1.0a item 11 and open item 10 wording still fits ten templates when 1.0a runs only eight | FAIL (minor, F4) |

C21 to C23 fail only on minor findings, so they do not fail the gate.

## Summary

- Checks passed: 20 / 23 (the 3 failures are all MINOR)
- BLOCKING findings: 0
- MAJOR findings: 0
- MINOR findings: 5 (F1 to F5)
- The R5 edit kept the design's form: the revision row, the two allowlist tuples, the D10 row and every touched table row keep their cell counts and style, section numbering is unchanged, and there is no em-dash, `TODO` or `TBD`.

Confidence: Verified: 20/23 | Unverifiable: 0 | Unchecked: 0 | Confidence: 87.0% by the raw ratio (the 3 non-verified items are the minor wording failures, each confirmed by a Read; no item is unchecked). The verdict rests on zero blocking findings, not on the ratio.
Tool engagement: Read: 12 | Grep: 2 | Glob: 0 | Bash: 4 (all read-only: `grep`, `sed -n`, `awk`, `wc`, `diff`, `git status`, `git log`, `ls`)

Verdict: PASS
Blocking count: 0
