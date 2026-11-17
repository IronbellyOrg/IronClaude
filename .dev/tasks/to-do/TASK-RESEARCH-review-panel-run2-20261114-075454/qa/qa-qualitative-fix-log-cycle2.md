# A.10.5 Qualitative Fix Log, Cycle 2 (last cycle)

**Date:** 2026-11-14
**Agent:** rf-qa fix agent (single), fix_authorization: true
**Target:** `.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/TASK-RESEARCH-review-panel-run2-20261114-075454.md`
**Findings in scope:** V-1, V-2, V-3 and three trivial wording fixes (line 74, step 7.2, item 5.11) (source: `qa/qa-task-validation-consolidated.md`, Addendum 3)
**Method:** Read each target line in full, Edit tool only (no sed -i, no scripts), re-read after each edit. Entries are appended as work proceeds.

---

## V-1: item 6.58 (line 580), the re-run spawn now carries the independence rule and the prompt-assembly rule

One Edit, one occurrence (old string unique; line 580 read before and after).

- Before: the re-run spawned an agent "with the verbatim prompt of Item 6.5x ... but with the output paths ...-rerun.md"; neither independence path was named.
- After (in (6)(i)): the executor assembles the spawn prompt by copying the AGENT PROMPT text of that agent's item (6.54 to 6.57) word for word, with the assigned-file list from `qa/gate5-partition.md` (including moved files or line ranges), and exactly two substitutions: `qa-anti-omission-report-<n>.md` becomes `...-rerun.md` and `qa-anti-omission-enumeration-<n>.md` becomes `...-rerun.md` (full `.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/qa/` paths written out, every occurrence including the ENUMERATION FILE clause and `Output path`). A sentence is appended at the end of the copied prompt: `INDEPENDENCE OF THE RE-RUN: never read, list, grep into or cite <run-1 folder> or <RUN2-QUEUED note>; exclude .dev/tasks/ from repo-wide greps and from git log (this task's own folder may be read).` Both literal paths are in the item (scan: `REVIEW-PANEL-UNIFY-RUN2-QUEUED` 1 hit and `TASK-RESEARCH-review-panel-unify-20261113-155942` 1 hit on line 580). The item also states that it never reads, lists, greps into or cites those paths itself.
- Status: FIXED.

## V-2: recovered-claim checking scoped to code-derived claims; `source-checked:` added (items 6.59-6.67)

| Item | Line | Edit | Mechanism | Occurrences |
|---|---|---|---|---|
| 6.59 and 6.64 | 582, 594 | the sentence "a claim you cannot verify against code is tagged [UNVERIFIED] and goes to Open Questions instead, and the fix log marks each RECOVERED entry with `code-checked:`" replaced by three rules: code/tests/scripts/configs/E2-tip claims are checked against code and marked `code-checked: <file:line or git path:line>`; claims whose source is web research, a debate outcome, a design option or an E1 artifact are checked against that source (URL, `ADJUDICATION-RESULT.md` path, artifact path:line) and marked `source-checked: <citation>`; a claim that cannot be checked at all is tagged [UNVERIFIED], STAYS in its report section and is ALSO listed in Open Questions | replace_all (Grep count before: 2) | 2 |
| 6.59 | 582 | rule (5) fix-log format: a RECOVERED entry carries a `code-checked:` or `source-checked:` citation | single Edit | 1 |
| 6.64 | 594 | closing fix-log format clause: same | single Edit | 1 |
| 6.59 and 6.64 | 582, 594 | Ensuring clause: "every recovered entry carries a `code-checked:` citation" now also allows a `source-checked:` citation (a claim whose source is web research, a debate outcome, a design option or an E1 artifact) | replace_all (count before: 2) | 2 |
| 6.60, 6.61, 6.65, 6.66 | 584, 586, 596, 598 | CODE RECHECK opening: "for EVERY RECOVERED entry marked `code-checked:` (a recovered claim about code, tests, scripts, configs or the E2 tip)" | replace_all (count before: 4) | 4 |
| 6.60, 6.61, 6.65, 6.66 | same | new rule: re-verify `source-checked:` entries against the cited source; a non-supporting citation, or a code claim carrying `source-checked:`, is STILL-OPEN | replace_all (count before: 4) | 4 |
| 6.60, 6.61, 6.65, 6.66 | same | `RECOVERED_VERIFIED_AGAINST_CODE=<k> of <m>`: m = recovered claims that are code-derived (marked `code-checked:`), k = those verified against code, `source-checked:` claims counted in neither, `0 of 0` when no code-derived claim was recovered | replace_all (count before: 4) | 4 |
| 6.62 | 588 | the sum counts code-derived recovered claims; open in `F_1` = a code-derived claim not verified against code, a `source-checked:` claim whose source a verifier reports as not supporting it, a `P6A-RC` row a verifier reports STILL-OPEN | single Edit | 1 |
| 6.67 | 600 | same, with `F_2` | single Edit | 1 |
| 6.62 and 6.67 | 588, 600 | Ensuring clause: "the count of recovered claims verified against code" now "the count of code-derived recovered claims verified against code" | replace_all (count before: 2) | 2 |

Read-back: lines 582, 584, 588, 592, 594, 598, 600 re-read in full after the edits (6.61 at 586 and 6.65 at 596 are the replace_all twins of 584 and 598, confirmed by scan). Scan: `source-checked` on lines 582, 584, 586, 588, 594, 596, 598, 600. "goes to Open Questions instead": 0 hits.

Status: FIXED.

## V-3: `P6A-RC` lifecycle (items 6.58-6.63, 6.68)

- 6.58 (line 580), four single Edits (one occurrence each): (a) the Proposed handling list adds, for a `P6A-RC-<n>` row only, `CLOSED-BY-RERUN as defined in (6)(i)`; (b) `F_0` counts every `P6A-RC-<n>` row that is not `CLOSED-BY-RERUN`, final value written after the re-runs; (c) the parenthetical "counted in F_0 like every blocking finding" now says it counts while open, until CLOSED-BY-RERUN; (d) in (6)(i) the closing rule: the row is CLOSED when the rerun report is `Status: Complete` and the recount of the rerun enumeration reaches at least 0.9 of the independent recount for each chosen file (e >= 0.9 r) with every `COUNT` line present; a closed row is written as `CLOSED-BY-RERUN` (Blocking N, with its rerun result, not counted in F_0 after the rerun); otherwise it stays Blocking Y and counted in F_0. (d) is the same Edit as V-1.
- 6.59 and 6.64 (582, 594): Ensuring clause says "every blocking omission ID except `P6A-RC` rows" (replace_all, count 2).
- 6.60, 6.61, 6.65, 6.66 (584, 586, 596, 598): sentence added after the `RECOVERED_VERIFIED_AGAINST_CODE` line: a `P6A-RC-<n>` row (listed as blocking, or marked `CLOSED-BY-RERUN`) is RECOVERED-OK when the rerun result recorded next to it in `qa-anti-omission-consolidated-findings.md` meets the rule of Item 6.58, otherwise STILL-OPEN (the same replace_all as the m/k edit, count 4). The cycle 2 twins 6.65 and 6.66 got the same sentence so the cycles stay consistent.
- 6.62 and 6.67 (588, 600): a `P6A-RC` row a verifier reports STILL-OPEN is counted as open in `F_1` / `F_2` (V-2 table).
- 6.63 (592): Proposed handling now `RECOVER, JUSTIFY or JUSTIFIED-REMOVED (cite the fix-log entry and the code evidence)`; a `P6A-RC-<n>` row is listed only while STILL-OPEN (with the rerun result), a `CLOSED-BY-RERUN` row is not listed. One Edit.
- 6.68 (604): checklist item 21 says Gate 5 has "4 anti-omission reports, plus a `-rerun` report for every agent re-run for a `P6A-RC` finding, that is for every row ... listed as `CLOSED-BY-RERUN`". One Edit.
- Scan: `CLOSED-BY-RERUN` on lines 580 (4 hits), 584, 586, 592, 596, 598, 604. JUSTIFIED-REMOVED on line 592: 1 hit.

Status: FIXED.

## Trivial wording fixes

| Fix | Line | Change | Read-back |
|---|---|---|---|
| Task Overview testing sentence | 74 | "the only commands run are read-only recounts" now "... read-only recounts plus the scratch fixtures under `/tmp/review-panel-run2-<item>/` and the staging commands in Phase 7" | Grep -o on line 74 shows the new text |
| Step 7.2 count | 621 | the item lists four checks (`.claude` diff, nested `.claude`, report path, staged-file count) but said "the four results" in one place and "the three checks" at its end. Now "the results of the four checks" and "until the four checks are recorded". Line 637 ("the four results", the separate re-stage item that also lists four checks) was left as it is | Read of line 621; "until the three checks": 0 hits |
| Item 5.11 cause of the Grep error | 336 | "rejected by ripgrep as an unclosed character class" now "an unescaped `[` opens a character class that is never closed, so ripgrep rejects the pattern with a regex parse error (`invalid character class range, the start must be <= the end`)". I reproduced the error with the Grep tool on `[PENDING-ADJUDICATION` (`rg: regex parse error ... invalid character class range, the start must be <= the end`), so the new text names both the unclosed class and the real error | Grep -o on line 336 shows the new text; "unclosed character class": 0 hits |

## Final scans (one read-only batch script, run after all edits)

| Scan | Result |
|---|---|
| `- [ ]` item lines (`^- \[ \]`) | 187 |
| `[x]` (case-insensitive) | 0 |
| `REVIEW-PANEL-UNIFY-RUN2-QUEUED` in line 580 | 1 (>= 1); run-1 folder literal in line 580: 1 |
| `source-checked` | lines 582, 584, 586, 588, 594, 596, 598, 600 (items 6.59, 6.60, 6.61, 6.62, 6.64, 6.65, 6.66, 6.67) |
| `CLOSED-BY-RERUN` | lines 580 (6.58), 584, 586 (6.60, 6.61), 592 (6.63), 596, 598 (6.65, 6.66), 604 (6.68) |
| Duplicate sentences (over 60 chars) within lines 580, 582, 584, 586, 588, 592, 594, 596, 598, 600, 604 | 0 on every line |
| Raw `TODO`, `TBD`, `FIXME` words | 0; the written form `T[O]DO|T[B]D|FIX[M]E` is on 5 lines (unchanged) |
| Escaped `\[PENDING-ADJUDICATION` / `\[CONTRADICTION` | 6 lines / 1 line (unchanged from cycle 1) |
| Halt messages | `[HALT-MONOTONICITY] |F|=<` on 14 lines, `Regression detected on Item X.Y, previously PASS at cycle` on 13 lines (not edited) |
| `.claude` staging guard `git diff --cached --name-only -- .claude` | 2 lines (step 7.2 and the re-stage item), unchanged |
| Item heads 6.58 to 6.68 | one each |
| File length | 724 lines, unchanged |

Items edited: 6.58 to 6.68, line 74, step 7.2 (line 621), item 5.11 (line 336). No new item, no renumbering, no change to agent counts, gates, Gate 5's partition mechanism (6.54) or the recount percentages (0.9 and 10 percent are only restated). Nothing under `.claude/` touched; the run-1 folder and the RUN2-QUEUED note were not opened.

**Status: V-1, V-2, V-3 and the three trivial wording fixes FIXED.**
