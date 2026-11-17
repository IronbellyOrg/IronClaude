# QA Report - Fix Verification Cycle 2 (structure and regression)

**Topic:** A.10.5 fix cycle 2 (last cycle), Addendum 3 (V-1, V-2, V-3, three trivial wording fixes)
**Date:** 2026-11-14
**Phase:** fix-cycle (task-integrity lens)
**Fix cycle:** 2
**Task file:** .dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/TASK-RESEARCH-review-panel-run2-20261114-075454.md
**fix_authorization:** false (report only; task file not edited)

---

## Method notes

Task file read by line range (lines 580-604 in full via Read; lines 74, 336, 621, 637 via sed) and scanned with Grep and read-only Bash batches. The fix log was used only to know where to look; every verdict below rests on text seen in the task file. The run-1 folder and the RUN2-QUEUED note were not opened. Task file mtime 10:21:17, fix log 10:23:08 (task file not edited by this QA).

## 1. V-1 (item 6.58, line 580): FIXED

Text seen in line 580 (item 6.58, (6)(i)):
- The re-run agent is `subagent_type rf-analyst`; "whose spawn prompt you assemble by copying the AGENT PROMPT text of that agent's item (agents 1 to 4 = items 6.54 to 6.57) into the Agent call word for word", with the assigned-file list from `qa/gate5-partition.md`.
- "exactly these two substitutions and no other change": `.../qa/qa-anti-omission-report-<n>.md` becomes `...-report-<n>-rerun.md` and `.../qa/qa-anti-omission-enumeration-<n>.md` becomes `...-enumeration-<n>-rerun.md`, "every occurrence in the copied prompt, including its ENUMERATION FILE clause and its `Output path`".
- Appended sentence in quotes: "INDEPENDENCE OF THE RE-RUN: never read, list, grep into or cite `.dev/tasks/to-do/TASK-RESEARCH-review-panel-unify-20261113-155942/` or `.dev/tasks/to-do/REVIEW-PANEL-UNIFY-RUN2-QUEUED.md`; exclude `.dev/tasks/` from repo-wide greps and from `git log` (this task's own folder may be read)." Both literal paths and the grep/git-log exclusion are present.
- Substitution premise checked: lines 570, 572, 574, 576 (items 6.54-6.57) each contain exactly 2 occurrences of the full path `qa-anti-omission-report-<digit>.md` and 2 of `qa-anti-omission-enumeration-<digit>.md`, so the two substitutions cover every output-path occurrence; each of those prompts has an `ENUMERATION FILE:` clause and defines the `COUNT <file name>: <n>` line that 6.58 relies on.

Scan of every agent-spawning item: 151 checklist items contain `subagent_type`, and the same 151 contain both literal independence paths (a per-line loop over each `subagent_type` line printed no line missing either path). Lines 228, 546, 621, 629, 631, 637 mention "agent" only in prose (Gate 1 flag note, "one defect found by several agents", `.claude/agent-memory`, "later fix agents") and do not spawn. Result: no exception, 6.58 included.

## 2. V-2 (items 6.59-6.67): FIXED

- 6.59 (line 582) and 6.64 (line 594): the sentence from "every claim you DO recover" to "never dropped)" is byte-identical in the two items (same md5 925a7f6d... on both). Text seen: code/tests/scripts/configs/E2-tip claims -> `code-checked: <file:line or git path:line>`; web research, debate outcome, design option or E1 artifact claims -> checked against the URL, `ADJUDICATION-RESULT.md` path or artifact path:line and marked `source-checked: <citation>`; a claim that cannot be checked at all -> "tagged [UNVERIFIED], STAYS in its report section and is ALSO listed in Open Questions (it is never moved out of its section, never dropped)". This removes the old contradiction with "RECOVER it into the named section".
- Ensuring clause identical in both (same md5 f6072a8e... on both): "every recovered entry carries a `code-checked:` citation (a claim about code) or a `source-checked:` citation (...)".
- Fix-log format: 6.59 rule (5) and 6.64 closing clause both require the `code-checked:` or `source-checked:` citation on a RECOVERED entry (different shorthand wording, same rule).
- 6.60 (584), 6.61 (586), 6.65 (596), 6.66 (598): the span from "CODE RECHECK (mandatory)" to "otherwise STILL-OPEN." hashes identically on all four (md5 bd746eef...). It defines `RECOVERED_VERIFIED_AGAINST_CODE=<k> of <m>` with m = recovered claims that are code-derived (marked `code-checked:`), k = those verified against code, `source-checked:` claims in neither, `0 of 0` when none. Word diffs of 6.60 vs 6.65 and 6.61 vs 6.66 show differences only in cycle labels (c1/c2, F_1/F_2, "review 3"), the fix-log skip condition ("says No fix required" vs "starts with Skipped") and pre-existing shorter wording of the c2 clauses; none touch the V-2 text.
- 6.62 (588) and 6.67 (600): the open-count sentence is the same apart from the file name and F_1/F_2: the count is of code-derived recovered claims marked `code-checked:`; open = a code-derived recovered claim a verifier reports as not verified against code, a `source-checked:` claim whose cited source a verifier reports does not support it, and a `P6A-RC` row a verifier reports STILL-OPEN.
- 6.63 (592) and 6.68 (604) carry no code-check text that could conflict (6.63 only lists STILL-OPEN or NEW rows; 6.68 has no code-check requirement). No leftover old wording: "goes to Open Questions instead" 0 hits; "not verified against code" 2 hits (lines 588 and 600, the intended count sentences).

## 3. V-3 (`P6A-RC-<n>` lifecycle): FIXED, no contradiction found

- 6.58 (line 580): Proposed handling adds "for a `P6A-RC-<n>` row only, CLOSED-BY-RERUN as defined in (6)(i)"; F_0 "including every `P6A-RC-<n>` recount finding from (6) that is not `CLOSED-BY-RERUN`; write the final value after the re-runs of (6)(i) are done"; the row is "counted in F_0 while it is open"; closing rule: rerun report `Status: Complete` and recount of the rerun enumeration at least 0.9 of the independent recount for each chosen file (`e` at least 0.9 times `r`) with every `COUNT` line present, written as `CLOSED-BY-RERUN` (Blocking N, with its rerun result, "not counted in F_0 after the rerun"); otherwise it "stays Blocking Y and counted in F_0". The 0.9 threshold agrees with the opening shortfall rule ("above 10 percent (`e` below 0.9 times `r`)").
- 6.59/6.64 Ensuring: "every blocking omission ID except `P6A-RC` rows"; the prompt rule says P6A-RC rows "are handled by the re-run in Item 6.58, not by you". Consistent.
- 6.60/6.61/6.65/6.66: "A `P6A-RC-<n>` row (listed as blocking, or marked `CLOSED-BY-RERUN`) is RECOVERED-OK when the rerun result recorded next to it in `qa-anti-omission-consolidated-findings.md` meets the rule of Item 6.58 (the rerun report is `Status: Complete` and the recount of the rerun enumeration reaches at least 0.9 of the independent recount), otherwise STILL-OPEN." Matches 6.58 and is present in all four.
- 6.62/6.67: a `P6A-RC` row a verifier reports STILL-OPEN counts as open in F_1/F_2.
- 6.63 (592): Proposed handling "RECOVER, JUSTIFY or JUSTIFIED-REMOVED (cite the fix-log entry and the code evidence)"; a `P6A-RC` row listed only while STILL-OPEN, a `CLOSED-BY-RERUN` row not listed.
- 6.68 (604) item 21: Gate 5 = "4 anti-omission reports, plus a `-rerun` report for every agent re-run for a `P6A-RC` finding, that is for every row `qa-anti-omission-consolidated-findings.md` lists as `CLOSED-BY-RERUN`". 6.68 only runs after Gate 5 passed, so every P6A-RC row is closed by then; consistent.
- Unhappy path (note, by design, not a defect): a `P6A-RC` row whose rerun fails stays Blocking Y in F_0, the fix agent is told not to handle it, the verifiers report it STILL-OPEN, so that row never leaves the count; if it is the only open row, 6.62 or 6.67 fires `[HALT-MONOTONICITY]` and escalates to the owner. That is the stated halt-and-ask behaviour, not a loop.

## 4. Trivial fixes: FIXED

- Line 74: "Testing requirements: not applicable (documentation-only research task; the only commands run are read-only recounts plus the scratch fixtures under `/tmp/review-panel-run2-<item>/` and the staging commands in Phase 7)." The `/tmp/review-panel-run2-` path appears 25 times in the file, so the new clause is grounded.
- Step 7.2 (line 621): the text now says "the results of the four checks" and "until the four checks are recorded"; the item lists four checks (`.claude` diff, nested `.claude`, report path, staged-file count). "the three checks" 0 hits in line 621. The final "re-run both checks" refers to the two `.claude` checks, which is correct. Line 637 (re-stage item) says "the four results" and lists four checks.
- Item 5.11 (line 336): "an unescaped `[` opens a character class that is never closed, so ripgrep rejects the pattern with a regex parse error (`invalid character class range, the start must be <= the end`)". I reproduced it with the Grep tool on `[PENDING-ADJUDICATION:`: output `rg: regex parse error ... error: invalid character class range, the start must be <= the end`. The quoted error text is real.

## 5. Regression scan: PASS

| Check | Result | Evidence |
|---|---|---|
| Length, items | 724 lines, 187 `- [ ]` items | wc -l, grep -c |
| Checked or nested items | none | `[x]` case-insensitive 0 hits; indented checkbox 0; other bullet forms 0 |
| Numbering contiguous | yes | Phase 2: 01-24, Phase 3: 01-26, Phase 4: 01-04, Phase 5: 01-50, Phase 6: 01-70 (6.58-6.70 present once); 13 unnumbered items are Phase 1 (3), the Phase 3 preamble item at line 228, and Phase 7 (9); 174 + 13 = 187 |
| Phase headings once each | yes | `### Phase 1` to `### Phase 7` at lines 150, 164, 221, 290, 305, 441, 610; findings headings 665-689; no duplicate heading |
| Halt messages | unchanged, consistent | `[HALT-MONOTONICITY] \|F\|=` on 14 lines (variants `<F_1>`, `<F_2>`, `<n>` only); `Regression detected on Item X.Y, previously PASS at cycle <1, 2 or N>, now FAIL. Halt overrides monotonicity check.` 13 mentions, all 13 full-form |
| Placeholders | none | Grep for the three plain words: 0 hits; the written-out form `T[O]DO\|T[B]D\|FIX[M]E` (literal text) 5 hits; the same text used as a regex: 0 hits |
| Escaped patterns | intact, no regex error | Grep `\[PENDING-ADJUDICATION`: 20 matches; `\[CONTRADICTION`: 3 matches; both returned normal results |
| `.claude` staging guards | intact | `git diff --cached --name-only -- .claude` on lines 621 and 637; nested-`.claude` grep on lines 621, 629, 637; no `git add -f`; the only `git add` plus `.claude` co-occurrences (lines 621, 637) are the "ensuring NO ... git add of a path outside .dev/tasks" guard text |
| Duplicated paragraphs | none | 0 repeated lines over 80 chars across the file; 0 repeated sentences over 80 chars inside any single line |
| Agents per item | at most one spawned agent per item, none above 20 | items 2.13, 3.17, 3.22 mention `subagent_type` 2-3 times (analysis-target phrase, the fix agent, an optional per-gap researcher); Phase 2 wave 1 is 18 agents |
| Gate 5 agent count | still 4 | Step 6.9 heading "4 rf-analyst"; items 6.54-6.57 one `rf-analyst` each; 6.58 re-runs are one agent each, only for a flagged partition |
| Item sizes | no blow-up | largest line 9,193 bytes (item 6.54, line 570, the known size); edited items 6.58-6.68 range 1.7 KB to 5.8 KB |
| New facts without evidence | none found | cycle 2 added rules and wording; the one factual addition (ripgrep error text) reproduced above; the line-74 `/tmp` path has 25 uses in the file |

## Notes (minor, not blocking)

1. Item 6.58 says "this item itself never reads, lists, greps into or cites those two paths either" in the same item that spells both literal paths inside the quoted sentence. The meaning (the executor never opens or reports them) is clear, and the same phrasing exists in the other agent items. Wording only.
2. Line 74 still says "read-only recounts"; the task also runs read-only `git show`, `git ls-tree`, Grep and Glob. Wording only; the sentence is not an acceptance criterion.
3. An [UNVERIFIED]-tagged code claim is in neither `k` nor `m`, so 6.62/6.67 do not count it open. This is the requested shape of the V-2 fix (the claim stays in its section and is listed in Open Questions); recorded so the owner is not surprised.
4. The c2 structural and content verifier prompts (6.65, 6.66) are shorter than the c1 ones (6.60, 6.61) in clauses unrelated to V-1, V-2 and V-3. Pre-existing, not part of Addendum 3.

## Summary

- V-1 FIXED (item 6.58, line 580; all 151 agent-spawning items name both literal independence paths).
- V-2 FIXED (items 6.59/6.64 identical rule; 6.60/6.61/6.65/6.66 identical CODE RECHECK span; 6.62/6.67 count per the new rule).
- V-3 FIXED (6.58 closing rule; 6.59/6.64 Ensuring; 6.60/6.61/6.65/6.66 verifier rule; 6.62/6.67 count; 6.63 JUSTIFIED-REMOVED; 6.68 item 21 `-rerun` reports). No remaining contradiction among these items.
- Trivial fixes (line 74, step 7.2, item 5.11) FIXED.
- Regression scan clean. STILL-OPEN blocking findings: 0. New blocking defects: 0.
- Confidence: Verified: 20/20 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- Tool engagement: Read: 14 | Grep: 8 | Glob: 0 | Bash: 10

VERDICT: PASS
