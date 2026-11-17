# QA Report — Fix-cycle 2 verification (operational and gate semantics)

**Topic:** A.10.5 fix cycle 2 (last cycle), Gate 5 items 6.54-6.68, line 74, line 621, item 5.11, step 7.2
**Date:** 2026-11-14
**Phase:** task-qualitative (fix-verification, cycle 2)
**Fix cycle:** 2 (last; a blocking finding HALTs and goes to the owner)
**fix_authorization:** false (task file not edited)

---

## Overall Verdict: PASS (no blocking defect; minor notes in section 6)

**Drift baseline (AX-1):** BUILD-REQUEST line 47 (Gate 5 method), read verbatim: "exhaustive enumeration (not spot-check); judge coverage by MEANING, never by ID/reference-citation; every omission is recovered or explicitly justified as dedup/out-of-scope, never silently dropped." Line 102: "Builder MUST embed the complete agent prompt ... and the shared rules block (read-only, git-only access to the E2 tip, independence rule, stub-first, tags) in each checklist item per B2." The Addendum 3 text (V-1, V-2, V-3, three trivial fixes) is the fix specification.

## 1. Status of the three findings and the three trivial fixes

| Finding | Required fix (Addendum 3) | Evidence in the task file | Status |
|---|---|---|---|
| V-1 (6.58, line 580) | independence rule with both literal paths, the two path substitutions, prompt assembled by copying 6.54-6.57's prompt | Line 580 (6)(i): "spawn ONE Agent (subagent_type `rf-analyst`) whose spawn prompt you assemble by copying the AGENT PROMPT text of that agent's item (agents 1 to 4 = items 6.54 to 6.57) into the Agent call word for word ... with exactly these two substitutions and no other change" and "with this sentence appended at the end of the copied prompt: \"INDEPENDENCE OF THE RE-RUN: never read, list, grep into or cite `.dev/tasks/to-do/TASK-RESEARCH-review-panel-unify-20261113-155942/` or `.dev/tasks/to-do/REVIEW-PANEL-UNIFY-RUN2-QUEUED.md`; exclude `.dev/tasks/` from repo-wide greps and from `git log` (this task's own folder may be read).\"" plus "(this item itself never reads, lists, greps into or cites those two paths either)". Bash count: run-1 folder literal 1, QUEUED literal 1 on line 580. | RESOLVED |
| V-2 (6.59-6.62, 6.64-6.67) | scope code check to code-derived claims; `source-checked:`; `[UNVERIFIED]` stays in section; `m`/`k` code-derived only | 6.59 and 6.64 carry three rules (`code-checked:`, `source-checked:`, "a claim that cannot be checked at all is tagged [UNVERIFIED], STAYS in its report section and is ALSO listed in Open Questions"); 6.60, 6.61, 6.65, 6.66 define "m = the recovered claims that are code-derived, that is marked `code-checked:` ... `source-checked:` claims are counted in neither k nor m; `0 of 0` when no code-derived claim was recovered"; 6.62 and 6.67 count open only "a code-derived recovered claim that a verifier reports as not verified against code, a `source-checked:` claim whose cited source a verifier reports does not support it, and a `P6A-RC` row a verifier reports STILL-OPEN". Stale phrase "goes to Open Questions instead": 0 hits. | RESOLVED |
| V-3 (6.58-6.63, 6.68) | `P6A-RC` life cycle: closing rule, `CLOSED-BY-RERUN`, Ensuring clause, verifier outcome, JUSTIFIED-REMOVED in 6.63 | 6.58 (6)(i): "the row `P6A-RC-<n>` is CLOSED when the rerun report is `Status: Complete` and the recount of the rerun enumeration reaches at least 0.9 of the independent recount for each chosen file (`e` at least 0.9 times `r`) with every `COUNT` line present, and a closed row is written into the consolidated file as `CLOSED-BY-RERUN` (Blocking N, ..., not counted in F_0 after the rerun); a row whose rerun does not meet this rule stays Blocking Y and counted in F_0". 6.59/6.64 Ensuring "every blocking omission ID except `P6A-RC` rows". 6.60/6.61/6.65/6.66 "A `P6A-RC-<n>` row (listed as blocking, or marked `CLOSED-BY-RERUN`) is RECOVERED-OK when the rerun result recorded next to it ... meets the rule of Item 6.58 ..., otherwise STILL-OPEN". 6.63 Proposed handling "RECOVER, JUSTIFY or JUSTIFIED-REMOVED (cite the fix-log entry and the code evidence)". 6.68 item 21 counts `-rerun` reports for `CLOSED-BY-RERUN` rows. | RESOLVED |
| Line 74 | "only read-only recounts" overstated | now "the only commands run are read-only recounts plus the scratch fixtures under `/tmp/review-panel-run2-<item>/` and the staging commands in Phase 7" (25 `/tmp/review-panel-run2-` hits in the file) | RESOLVED (minor note N-3) |
| Step 7.2 (line 621) | count agrees with the list | Bash: line 621 has "four checks" x2 and "both checks" (the two `.claude` checks); no "three checks"/"three results". The item lists four checks (`.claude` diff, nested `.claude` grep, report path, `wc -l` count). Line 637 lists the same four and says "four results". | RESOLVED |
| Item 5.11 (line 336) | correct the cause of the Grep error | New text: "an unescaped `[` opens a character class that is never closed, so ripgrep rejects the pattern with a regex parse error (`invalid character class range, the start must be <= the end`)". Reproduced below (section 5). | RESOLVED (minor note N-1) |

## 2. Scenario walk-throughs, Gate 5 items 6.54-6.68 (axis lens AX-1..AX-5 applied to each)

Common start for all four: 6.54-6.57 spawn four `rf-analyst` agents (read-only, enumeration file plus report; each AGENT PROMPT is 5.8 to 6.4 KB, Bash `awk` length of the quoted prompt: 6132, 5909, 5777, 6446 characters). 6.58 consolidates, runs the independent recount, writes `F_0`. 6.59 fixes (single `rf-qa`), 6.60/6.61 verify, 6.62 decides in the order regression, monotonicity, proceed.

### (a) A dropped web finding (web-01 to web-04) flagged by the anti-omission agent: reaches F = 0, no contradiction, no gap. axis: none

1. Agent 1 (web-01, web-02) or agent 2 (web-03, web-04) lists it OMITTED. 6.58 table (1) gets a `P6A-00x` row: Blocking Y (IMPORTANT or CRITICAL), Proposed handling RECOVER into the named section.
2. 6.59 fix agent: the claim's source is web research, so the rule "a recovered claim whose source is web research, a debate outcome, a design option or an E1 artifact (it cannot be verified against code) is checked against that source (the URL ...) and its fix-log entry is marked `source-checked: <citation>`". It is not forced into the old "[UNVERIFIED] and Open Questions instead" dead end (V-2 resolved).
3. 6.60/6.61 re-verify the `source-checked:` entry against the URL (rf-qa has Tavily and WebFetch). `m` excludes it (`0 of 0` when it is the only recovery). Supported: RECOVERED-OK, not counted in `F_1`. Not supported: STILL-OPEN, counted in `F_1` by 6.62's own clause ("a `source-checked:` claim whose cited source a verifier reports does not support it").
4. If the URL cannot be fetched at all: `[UNVERIFIED]` plus it stays in its section plus Open Questions. That is a defined disposition (not STILL-OPEN, not dropped). See minor note N-5.
Result: `F_1 = 0` possible, `PASS at review 2`, items 6.63-6.67 skip.

### (b) A dropped debate outcome (`synth-06` row or `reviews/adversarial/<slug>/ADJUDICATION-RESULT.md`) that must appear in Sections 6.12 and 7: reaches F = 0. axis: none

1. Agent 1's prompt owns synth-06 and the debate results: "For each conflict-log row of synth-06 and each debate result also check that its outcome is in Sections 6.12 and 7." An absent outcome is OMITTED, Source file `.../ADJUDICATION-RESULT.md`.
2. 6.59 recovers it into 6.12 and 7 (the section named in the finding) with `source-checked: <ADJUDICATION-RESULT.md path:line>` (the rule names "the `ADJUDICATION-RESULT.md` path" literally). The BUILD-REQUEST line 47 text "every omission is recovered or explicitly justified ... never silently dropped" is met.
3. Verifiers re-check against `ADJUDICATION-RESULT.md` (6.60/6.61: "an entry whose citation does not support the claim ... is STILL-OPEN"). Not counted in `k`/`m`. This is the exact case that N-1 of the cycle-1 verification said could never reach F = 0; it now can.
4. 6.59 rule (3) requires the 6.12 and 7 counts, the Table of Contents and reconciliation lines to stay consistent (same wording in 6.64).

### (c) A dropped code-derived claim about `findings.py` that the fix agent recovers: verifiers re-check against code and count `k of m`. axis: none

1. 6.59: "a recovered claim about code, tests, scripts, configs or the E2 tip is checked against that code or E2 tip and its fix-log entry is marked `code-checked: <file:line or git path:line>`".
2. 6.60 and 6.61: "for EVERY RECOVERED entry marked `code-checked:` ... re-verify the recovered claim against the code at HEAD ... or, for the E2 branch, against `git show 6c0984326cbb8fb06c4a36065de58b171d3f8175:<path>` or `git ls-tree`"; each writes `RECOVERED_VERIFIED_AGAINST_CODE=<k> of <m>` with m = code-derived (marked `code-checked:`) claims. A recovered claim that code contradicts, or one a Gate 3/4 log lists as removed because false with evidence that still holds, is STILL-OPEN. A code claim wrongly labelled `source-checked:` is STILL-OPEN (no way around the check by relabelling).
3. 6.62: copies both lines and "their sum", and counts open "a code-derived recovered claim that a verifier reports as not verified against code". Consistent. Result: `k = m` and no STILL-OPEN gives `F_1 = 0`.
   (Notes N-4 and N-6 below: the sum double-counts when both verifiers check the same claims; the link between `k < m` and STILL-OPEN is implied, not written. Neither changes any F value.)

### (d) A recount shortfall `P6A-RC-<n>`: both branches walked

Branch d1, the rerun meets the 0.9 rule. axis: none
1. 6.58 (6)(i): shortfall (`e` below 0.9 times `r`), missing enumeration file or missing `COUNT` line gives `P6A-RC-<n>`, "Blocking Y, counted in F_0 while it is open".
2. The executor spawns ONE `rf-analyst` for that agent's whole partition (prompt assembled as in section 3), folds the rerun's omissions into table (1), repeats the recount on the same three files, and records the result next to the row.
3. Rerun `Status: Complete`, every `COUNT` line present, `e` at least 0.9 times `r` for each chosen file: the row is written `CLOSED-BY-RERUN` (Blocking N), and "(4) `F_0` ... counts every `P6A-RC-<n>` row that is not `CLOSED-BY-RERUN` ... write the final value after the re-runs". It is not in `F_0`.
4. 6.59 Ensuring "every blocking omission ID except `P6A-RC` rows" so the fix log is not required to carry it. 6.60/6.61/6.65/6.66: RECOVERED-OK. 6.62: not counted. 6.63: "a `CLOSED-BY-RERUN` row is not listed". 6.68 item 21: expects the `-rerun` report for each `CLOSED-BY-RERUN` row. All consistent. The cycle-1 N-2 defect (blocking row with no closing rule) is resolved.

Branch d2, the rerun still falls short (or the rerun agent cannot complete). axis: none
1. The row "stays Blocking Y and counted in F_0". The rerun is single and the recount is single: bounded, no loop (6.58 contains exactly one "spawn ONE Agent" per row and no re-entry clause).
2. 6.60/6.61: "otherwise STILL-OPEN", so it is in `F_1`. 6.62 repeats it: "a `P6A-RC` row a verifier reports STILL-OPEN [is] counted as open in `F_1`".
3. Order of 6.62: (1) regression is by report section, and a `P6A-RC` row belongs to no section, so it cannot cause a regression. (2) If `F_1 > 0` and `F_1 >= F_0` (for instance `F_0 = 1`, only the row) the result is `[HALT-MONOTONICITY] |F|=1`. (3) Otherwise `0 < F_1 < F_0`: "FAIL at review 2: continue with fix cycle 2".
4. In cycle 2 nothing can close the row (6.64: "rows `P6A-RC-<n>` ... are handled by the re-run in Item 6.58, not by you"; 6.63 lists it "only while it is STILL-OPEN"). So `F_2 >= 1` and `F_2 >= F_1` or the HARD CAP fires in 6.67: HALT and escalate. This is a defined, owner-bound halt, not a silent pass. The gate cannot pass with this finding open. The cost is one idle fix cycle (note N-7). Verdict for d2: the outcome is STILL-OPEN, counted, and ends in a stated halt per the stated precedence; no contradiction, no gap that lets it pass.

### (e) A claim removed as false by a Gate 3 or Gate 4 fix: JUSTIFIED-REMOVED, not re-added. axis: none (note N-2)

1. 6.54-6.57 (identical EARLIER-GATE REMOVALS clause, Bash comparison: 1054 characters in all four) tell the agent to read the four fix logs and four consolidated findings files and classify such a finding JUSTIFIED-REMOVED when it cites the fix-log entry and the code evidence; otherwise OMITTED. JUSTIFIED-REMOVED is explicitly "NOT an omission".
2. 6.58 (ii) opens the cited entry and code evidence for the findings (at least 10 when more than 10); no code evidence turns it into an omission row in table (1). Proposed handling lists JUSTIFIED-REMOVED.
3. 6.59/6.64 (identical clause, 749 characters each): "you MUST NOT re-add such a claim unless your own code evidence ... shows the evidence in that log is wrong, and you then record that code evidence in the fix log". 6.60/6.61/6.65/6.66: "a JUSTIFIED-REMOVED entry is decided JUSTIFIED-OK only when its fix-log entry and the code evidence it cites exist and hold"; a re-added removed claim is STILL-OPEN. 6.63 now lists JUSTIFIED-REMOVED in Proposed handling (V-3 resolved).
4. Evidence availability: the Gate 3/4 consolidated findings tables carry an `Evidence` column (line 510: "Report section, Finding, Evidence, Proposed fix"; line 546: "Source, Report section, Finding, Evidence"), and the Gate 5 agents are told to read them, so the usual case is usable. The corner case where only the fix-log entry exists with no code evidence is in note N-2 (a known, accepted note of Addendum 3; ends in a defined halt, never a pass).

## 3. Twin consistency, cycle 1 (6.59-6.63) versus cycle 2 (6.64-6.68)

Method: one Bash script extracted the shared passages from the task-file lines and compared them as strings.

| Compared passage | Result |
|---|---|
| 6.59 (l.582) versus 6.64 (l.594), from "every claim you DO recover" to "RULES" (code-checked / source-checked / [UNVERIFIED] rules) | byte-identical, 784 characters |
| 6.59 versus 6.64, the JUSTIFIED-REMOVED clause ("THIRD allowed disposition" to "every claim you DO recover") | byte-identical, 749 characters |
| 6.60 (l.584) versus 6.65 (l.596), CODE RECHECK passage to "Output:" (m and k, `source-checked:`, `P6A-RC` sentence) | byte-identical, 1894 characters |
| 6.61 (l.586) versus 6.66 (l.598), same passage | byte-identical, 1894 characters; also identical to 6.60 |
| 6.62 (l.588) versus 6.67 (l.600), the closing "which is the count of code-derived recovered claims ... counted as open in `F_n`" sentence | identical apart from `F_1` and `F_2` |
| Precedence literals | 6.62: (1) REGRESSION, (2) MONOTONICITY, (3) otherwise; 6.67: (1) REGRESSION, (2) MONOTONICITY, (3) HARD CAP, (4) otherwise. Halt strings byte-exact `Regression detected on Item X.Y, previously PASS at cycle 1|2, now FAIL. Halt overrides monotonicity check.` and `[HALT-MONOTONICITY] |F|=<F_1|F_2>`, matching the Task Overview line 444 text. Unchanged by cycle 2 |
| Self-skip when cycle 1 passed | 6.63 writes `Skipped: Gate 5 passed at review 2`; 6.64 keys on "starts with `Skipped`" and writes the same note; 6.65 and 6.66 key on the fix-log "starts with `Skipped`"; 6.67 appends `Cycle 2 skipped; Gate 5 verdict PASS` on `PASS at review 2`. Step 6.11 header: "execute only if Item 6.62 recorded `FAIL at review 2: continue with fix cycle 2`", which is the literal 6.62 writes. A HALT in 6.62 stops the executor, so 6.63+ never run |
| Control arithmetic with the new dispositions | `F_n` = STILL-OPEN plus NEW, union, deduplicated; the three new categories (code-derived unverified, `source-checked:` unsupported, `P6A-RC` STILL-OPEN) are additive in the same union and are STILL-OPEN rows in the verifier tables already, so nothing is double-counted by the dedup. `CLOSED-BY-RERUN`, `[UNVERIFIED]`-tagged-and-kept and `source-checked:`-supported entries add nothing. Monotonicity (`F_n > 0 and F_n >= F_(n-1)`) and regression precedence are untouched |

Result: the twins carry the same rules, JUSTIFIED-REMOVED included. axis: none.

## 4. Item 6.58: bounded, executable re-run, both independence literals. axis: none (minor note N-8)

- Bounded: exactly one "spawn ONE Agent" (Bash count 1) per `P6A-RC` row; the recount is repeated once "(same method, the same three files)"; a row that still fails "stays Blocking Y and counted in F_0". No clause re-enters the rerun, so it cannot loop. At most four reruns (one per original agent), well under 20 concurrent subagents (rerun agents are the only agents alive at that point).
- Prompt assembly is mechanical. Bash check on items 6.54-6.57: inside each AGENT PROMPT there are exactly two path mentions that need changing, `.../qa/qa-anti-omission-report-<n>.md` (the `Output path`) and `.../qa/qa-anti-omission-enumeration-<n>.md` (the ENUMERATION FILE clause), both written with the full `.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/qa/` prefix (per line: report-mentions 2 of which full-path 2, enumeration-mentions 2 of which full-path 2, within AGENT PROMPT 2 in total, i.e. one each). So "every occurrence in the copied prompt, including its ENUMERATION FILE clause and its `Output path`" is exactly two replacements per prompt, and the substitution cannot miss a short-form path. The prompt to copy is 5.8 to 6.4 KB (the 9.2 KB figure is the whole item 6.54 line, which includes the partition check that is not copied).
- "Copy without paraphrase" is no harder than what 6.54-6.57 already require of the executor for their first spawn ("pass verbatim", same size). The text gives the executor the source (the item's AGENT PROMPT), the two substitutions, the file-list rule and the appended sentence, in the order in which it assembles them. A fidelity check exists in effect: the rerun report must carry `Status: Complete` and the `-rerun.md` paths for the row to close.
- Independence literals: both are on line 580, once each, inside the appended sentence (`.dev/tasks/to-do/TASK-RESEARCH-review-panel-unify-20261113-155942/` and `.dev/tasks/to-do/REVIEW-PANEL-UNIFY-RUN2-QUEUED.md`), together with the verbs "never read, list, grep into or cite" and the exclusions ("exclude `.dev/tasks/` from repo-wide greps and from `git log` (this task's own folder may be read)"); the item states for itself "this item itself never reads, lists, greps into or cites those two paths either". V-1 resolved.

## 5. Trivial fixes, reproduced with tools. axis: none

- Item 5.11 (line 336), Grep tool, pattern `[PENDING-ADJUDICATION:` (unescaped) on BUILD-REQUEST.md: `rg: regex parse error: (?:[PENDING-ADJUDICATION:) ... error: invalid character class range, the start must be <= the end`. The same file with `\[PENDING-ADJUDICATION:` returns a normal "No matches found" without an error. The error text quoted in 5.11 is exact. One precision point (note N-1): that exact message is produced by the reversed range `N-A` inside `PENDING-ADJUDICATION` (an unclosed class on its own gives a different message: Grep with `[CONTRADICTION` returned `error: unclosed character class`). The sentence "opens a character class that is never closed, so ripgrep rejects the pattern with a regex parse error (`invalid character class range ...`)" is therefore accurate on both facts but joins them by "so"; it is correct enough for an executor and does not mislead on the action (escape the bracket).
- Line 74: the sentence is accurate against the file: the task does run `uv run python scripts/reflect_shadow_exit.py` and `uv run pytest tests/cli/reflect -p no:cacheprovider -q` (line 181, which calls them "Read-only commands you MUST run to re-confirm the numbers"), `git show`/`git ls-tree`/`wc -l`/`sha256sum` reads, 25 `/tmp/review-panel-run2-` scratch uses and the Phase 7 staging. "Read-only recounts" covers the re-confirmation runs loosely; BUILD-REQUEST line 55 names the test suites explicitly (note N-3).
- Step 7.2 (line 621): four checks listed, "four checks" x2, no "three"; line 637 (re-stage item) lists four and says "four results". Agreement confirmed.

## 6. New-defect scan over every changed item (6.58-6.68, line 74, line 621, item 5.11) and minor notes

Scan performed: items 6.58-6.68 read in full from the file (lines 580, 582, 584, 586, 588, 592, 594, 596, 598, 600, 604) plus 6.54-6.57 (570-576) and 6.69 (606); all Gate 5 mentions outside those items (lines 72, 87, 288, 441, 444, 566, 568, 629, 631, 710, 716, 718) read for contradictions; stale-phrase scan: "goes to Open Questions instead", "verbatim prompt of Item 6.5x", "unclosed character class", "the three checks", "counted in F_0 like every blocking finding" all 0 hits; item heads 6.54-6.70 once each; 187 `- [ ]` items, 0 checked; file 724 lines (unchanged against the fix log); `.claude` staging guard intact.

| Axis | Question | Finding |
|---|---|---|
| AX-1 Drift | did the fix paraphrase the BUILD-REQUEST goal weaker? | No. Line 47 "never silently dropped" is kept: every disposition (RECOVERED with check tag, JUSTIFIED, JUSTIFIED-REMOVED, `[UNVERIFIED]` kept in section and in Open Questions) leaves the substance in the report or on record. |
| AX-2 Contradictions | changed text versus untouched text | None blocking. Items 6.59 and 6.64 now say a claim "STAYS in its report section", which matches the Gate 3 fix rule (item 6.30: "flag an unverifiable one [UNVERIFIED] and list it in Section 9") and removes the cycle-1 contradiction with "RECOVER it into the named section". Overview lines 87, 568, 716 say "4 rf-analyst" for Gate 5 while 6.58 may add up to four conditional reruns (note N-9, wording). |
| AX-3 Omissions | a required step or consumer missing | None blocking. The only gap in the chain is that nothing in cycle 2 can close an open `P6A-RC` row (note N-7), which is a defined halt. |
| AX-4 Weakened criteria | did the fix soften a pass condition so a gate passes with an open finding? | No. `[UNVERIFIED]`-kept is the same disposition the Gate 3 rule uses; a code claim cannot be relabelled `source-checked:` (it becomes STILL-OPEN); the recount closure uses the same 0.9 as the shortfall trigger (complement, no gap); `CLOSED-BY-RERUN` requires `Status: Complete`, all `COUNT` lines and `e >= 0.9 r`. A failed rerun keeps the row in `F_0`/`F_1`/`F_2`, and `F_2 > 0` always HALTs (6.67 (3)). |
| AX-5 Invented content | new names or files | `CLOSED-BY-RERUN`, `source-checked:` and `...-rerun.md` are specified by Addendum 3 itself; `qa/gate5-partition.md` is defined in 6.54. Nothing else new. |
| Concurrency | above 20 subagents | No. Max 4 reruns in 6.58, otherwise 1 fix agent and 2 verifiers at a time. |

### Minor notes (non-blocking, not rechecked in later rounds)

- N-1 (item 5.11, wording): the quoted Grep error comes from the reversed range `N-A`, not from the missing `]` (the missing `]` yields "unclosed character class"). Suggest "an unescaped `[` opens a character class, so ripgrep rejects the pattern (`invalid character class range ...`)". No effect on any executor action.
- N-2 (6.54-6.57 / 6.59 / 6.64, JUSTIFIED-REMOVED evidence): the Gate 5 agents may use the consolidated-findings `Evidence` column, but the 6.59/6.64 clause lets the fix agent use JUSTIFIED-REMOVED "only when a Gate 3 or Gate 4 fix log ... quotes code evidence". Gate 3 and 4 fix-log entries are specified as "finding ID, change (section, one line before and after)" with no evidence field (items 6.30 and 6.45). If an agent reads that strictly, a removed false claim is classed OMITTED and the fix agent has no allowed disposition: STILL-OPEN, then a defined HALT to the owner, never a pass and never a silent re-add. This is the note Addendum 3 already recorded ("consider adding an `Evidence:` line to those fix-log entries"). Not re-graded.
- N-3 (line 74): add "and the read-only re-confirmation runs named in the items (`uv run python scripts/...`, `uv run pytest ... -p no:cacheprovider`)" to match BUILD-REQUEST line 55 and line 181.
- N-4 (6.62/6.67): "their sum, which is the count of code-derived recovered claims ... verified against code" adds `k` of two verifiers that check the same claims, so it is up to twice the count. Informational only; not used in any `F` value (pre-existing wording).
- N-5 (6.59/6.64, verifiers): nothing lets a verifier challenge an `[UNVERIFIED]` tag put on a claim that was checkable. The tag keeps the claim visible in its section and in Open Questions, and "a recovered claim that the code contradicts" is STILL-OPEN, so the risk is a lazy tag, not a wrong claim.
- N-6 (6.60/6.61/6.65/6.66/6.62): a code claim the verifier cannot confirm is "not verified against code" (6.62) but only a contradicted claim is named STILL-OPEN in the verifier text; `k < m` implies an open claim and the verifier table will show it. Suggest one clause "a `code-checked:` entry the verifier cannot confirm is STILL-OPEN".
- N-7 (6.58/6.62-6.67): a `P6A-RC` row whose rerun failed is not closable in cycle 2, so a full idle cycle 2 runs before the (certain) halt unless `F_1 >= F_0` fires first. Safe, wasteful. A direct HALT at 6.62 when only `P6A-RC` rows remain would save one cycle; not required.
- N-8 (6.58): the item's own sentence names the four verbs but not the "exclude `.dev/tasks/` from repo-wide greps and git log" clause (it is in the appended sentence for the rerun agent). 6.58 only reads files in `qa/`, so no repo-wide search happens; wording only. Also `<n>` in the substitution rule means the agent number; the source prompts hold the literal digits 1 to 4; `qa/gate5-partition.md` is specified to hold per-agent line sums and every move, not the final file lists, so the executor derives the final list from the item plus the moves; and `F_0` should be written after both (6)(i) and (6)(ii) (ii can add omission rows), which the text says only for (i).
- N-9 (lines 87, 568, 716): "4 rf-analyst" does not mention the conditional `-rerun` agents of 6.58 (6.68 item 21 does).

## Items Reviewed

| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | V-1 item 6.58 independence literals, substitutions, copy rule | none | PASS | line 580: both literals once each, "exactly these two substitutions", appended sentence; Bash count of path mentions per prompt 2 of 2 full-path |
| 2 | V-2 code-derived scoping, `source-checked:`, `[UNVERIFIED]` stays | none | PASS | 6.59/6.64 identical 784-character passage; 6.60/61/65/66 identical 1894-character passage; 0 stale phrases |
| 3 | V-3 `P6A-RC` life cycle and `CLOSED-BY-RERUN` | none | PASS | 6.58 (4) and (6)(i); 6.59/6.64 Ensuring; verifier sentence in four items; 6.62/6.67; 6.63; 6.68 item 21 |
| 4 | Scenario (a) web finding | none | PASS | section 2 (a) |
| 5 | Scenario (b) debate outcome in 6.12 and 7 | none | PASS | section 2 (b) |
| 6 | Scenario (c) code claim, `k of m` | none | PASS | section 2 (c) |
| 7 | Scenario (d1)/(d2) recount shortfall | none | PASS | section 2 (d); d2 ends in a defined halt |
| 8 | Scenario (e) JUSTIFIED-REMOVED not re-added | none | PASS (minor note N-2) | section 2 (e); lines 510, 546 Evidence column |
| 9 | Twin consistency 6.59-6.63 versus 6.64-6.68, control arithmetic | none | PASS | section 3 byte comparison, precedence literals |
| 10 | 6.58 bounded, executable, both independence literals | none | PASS (minor note N-8) | section 4 |
| 11 | Trivial fixes (line 74, step 7.2, item 5.11) | none | PASS (minor notes N-1, N-3) | section 5; Grep error reproduced |
| 12 | New-defect scan, gate cannot pass with open blocking finding, concurrency at most 20 | none | PASS (minor notes N-2, N-4 to N-9) | section 6 |

## Summary
- Checks passed: 12 / 12
- Checks failed: 0
- Critical issues: 0; blocking issues: 0; minor notes: 9 (N-1 to N-9)
- Issues fixed in-place: 0 (fix_authorization: false; the task file was not edited)
- V-1, V-2, V-3 and the three trivial fixes are resolved in substance. Blocking count after cycle 2: 0 (cycle 1 left 3).

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| - | none blocking | - | Nine minor notes (N-1 to N-9) listed in section 6; none can pass a gate with an open blocking finding or halt a correct run | none required |

## Actions Taken
None (report only). The only files written are this report.

## Inherited Structural Verdict — Reliance Audit (PR-04, INV-019)
No `## Inherited Structural Verdict` section was in the spawn prompt; standalone behaviour applied (see Self-Audit).

## Self-Audit

**(a) Reliance list: rf-qa PASS items skipped for structural re-check:**
- None relied on. The cycle-2 structure verification report (`qa-qualitative-fix-verification-structure-cycle2.md`) and the fix log were not used as evidence; the fix log (qa-qualitative-fix-log-cycle2.md) was read only to know what to check, and every claim in it that I repeat was re-derived from the task file (see (b)).

**(b) Independent semantic checks (at least 1 required, INV-019):**
- Prompt-substitution mechanics: verified by Bash/awk on lines 570-576 that each AGENT PROMPT holds exactly two path strings to substitute, both with the full folder prefix (counts 2/2/2 per line).
- Twin identity: verified by Bash string comparison that the 6.59/6.64, 6.60/6.65, 6.61/6.66 changed passages are byte-identical (784, 749, 1894, 1894 characters) and that 6.62/6.67 differ only in `F_1`/`F_2`.
- Both independence literals in 6.58: Bash `grep -o` counts (1 and 1 on line 580).
- Ripgrep error: Grep tool reproduced `invalid character class range, the start must be <= the end` for `[PENDING-ADJUDICATION:` and a different message (`unclosed character class`) for `[CONTRADICTION`.
- Step 7.2 count: Bash `grep -o` on lines 621 and 637 ("four checks" x2, "both checks"; no "three").
- Line 74 against the file: Bash counts of `/tmp/review-panel-run2-` (25) and line 181 `uv run pytest` / `uv run python scripts/reflect_shadow_exit.py` runs.
- Gate 3/4 evidence availability for JUSTIFIED-REMOVED: Read of items 6.30 (l.512) and 6.45 (l.548) and Bash extraction of the consolidated-findings column lists (l.510, l.546).
- Gate flow for `P6A-RC` failure path: derived from 6.58, 6.62, 6.63, 6.64, 6.67 (quoted in section 2 (d2)).

Counts: factual claims independently verified: about 45 (line, count and string checks plus the scenario traces). Files read: the task file (lines 336, 510-512, 546-548, 568-576, 578-606, 621, 637, 74 and the Gate 5 mentions), BUILD-REQUEST.md (lines 45-47, 55, 80-140 and a Grep), qa-task-validation-consolidated.md (Addendum 3), qa-qualitative-fix-log-cycle2.md, qa-qualitative-fix-verification-semantics.md (N-1, N-2 and the review headings). I did not open the run-1 task folder or the RUN2-QUEUED note. No web research was needed, so no Tavily call was made (nothing to record).

## Confidence
Verified: 12/12 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (computed over the 12 checks above; the live behaviour of the executor and the agents is judged from the text, since the research and report files do not exist yet).
Tool engagement: Read: 21 | Grep: 9 | Glob: 0 | Bash: 12 (Read + Grep + Glob = 30 against 12 checks).

## Recommendations
- Proceed: the build need not HALT on A.10.5. No fix is required. If the owner reopens the file, apply N-2 (an `Evidence:` line in the Gate 3 and Gate 4 fix-log entries) and N-6 (one clause) first; the rest are wording.

## QA Complete

VERDICT: PASS


