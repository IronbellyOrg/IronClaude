# S1 ledger variant vs controls and Arm B (DRAFT, no verdict)

One replicate of the ledger variant (`/sc:spec-panel-ledger`), worktree exp346-v-ledger, run 2026-11-08 23:44Z to 2026-11-09 05:10Z. Comparator numbers are copied from `exp346-ab-{ctl-r1,ctl-r2,flg-r1,flg-r2}/.dev/experiments/346-validation/phase4/<name>/metrics.json` without regrading. Every ledger number below is in `metrics.json` (this folder); validity facts are in `validity.md`. This file gives arithmetic only and no success verdict.

## Per-round table
Proxy = CRITICAL + MAJOR labels among the NEW numbered findings of that review (baseline `proxy_definition`, the rule all four comparator recorders used). Labels are not blocking.

| Measure | ctl-r1 | ctl-r2 | flg-r1 | flg-r2 | ledger |
|---|---|---|---|---|---|
| R1 findings / proxy | 19 / 11 | 21 / 12 | 22 / 16 | 22 / 17 | 17 / 13 |
| R2 new findings / proxy | 15 / 9 | 17 / 7 | 12 / 5 | 11 / 6 | 16 / 9 |
| R3 new findings / proxy | 11 / 8 | 7 / 4 | 10 / 6 | 4 / 1 | 3 / 3 |
| Ledger blocking (script) R1 / R2 / R3 | n/a | n/a | n/a | n/a | 13 / 7 / 2 new (3 open at close) |
| Spec growth after cycle 1 (bytes vs v1) | 23.83% | 31.94% | 17.53% | 21.63% | 15.10% |
| Spec growth after two cycles (bytes vs v1) | 57.72% | 69.3% | 27.78% | 32.14% | 22.16% |
| Lines growth after two cycles | 27.37% | 27.0% | 2.81% | 11.23% | 1.05% |
| Clean pass | none | none | none | none | none (R1, R2 FAIL; R3 ESCALATE; sweep FAIL) |
| Model of the R3 reviewer | claude-opus-5-5 | claude-opus-5-5 | claude-opus-5-5 | claude-opus-5-5 | **gpt-6.1-sol** (validity.md V5) |
| R3 review scope | full panel | full panel | re-review flags | re-review flags | hunk-limited verify pass by design |

Ledger fix-origin shares (metrics.json `rounds[].m3_origin`): R2 parent-tag 8 of 16 (50%), in-revised-hunk 9 of 16 (56.25%), re-derived fix-related 14 of 16 (87.5%, including 5 stale references the fixes left behind); R3 parent-tag 2 of 3 (66.7%), all 3 fix-related (R35 from cycle 1). A changed anchor does not prove the fix caused the finding; the re-derived figure is the recorder's reading of the finding text. Cycle 2 added 4081 bytes, 31.88% of the loop's 12802 bytes of growth.
## Separate counts (labels, unresolved, script blockers, owner-deferred, sweep, union)
Kept apart on purpose; none of these is "the number of blocking defects".

| # | Count | Value | What it is |
|---|---|---|---|
| 1 | Original new C+M labels per round | R1 13, R2 9, R3 3 | the proxy above |
| 2 | Unresolved prior C+M labels at R3 | 3 (R25, R27, R28) plus 7 MINOR | R25 fixed then open again; R27, R28 MAJOR deferred outside the hunks |
| 3 | Script-confirmed blockers open at close | 3 (R25, R34, R36) | `u_count`: blocking, scope in, status open/fixed/reopened; R34 is R25's child, same mechanism |
| 4 | Owner cumulative C+M deferred/demoted/withdrawn (D14 rule 1) | 12 (R27, R28, R35 + sweep R37-R44, R48) | 3 loop outside-scope deferrals + 9 sweep rows the script stores deferred; 0 demoted, 0 withdrawn |
| 5 | Script final metrics | U3 3, W 9, O 3, headline_raw 15, outcome ESCALATE, phase swept | U3 = in-scope C+M rows not verified; W = sweep C+M rows; O = outside-scope C+M rows; headline_raw = U3+W+O (SCRIPT:2389-2456). `status` U=3 is a different count (blocking open) that happens to name the same 3 rows |
| 6 | Independent sweep findings | 12 (9 MAJOR, 3 MINOR) | blinded one-time sweep on the frozen r3 copy |
| 7 | Sweep overlap with endpoint open findings | 3 definite (N6=R35 MAJOR, N9=R29 MINOR, N12=R31 MINOR in loop vs MAJOR in sweep); 2 ambiguous (N7~R36, N8~R34) | 5 sweep findings say verified rows' text still fails (N2, N3, N4, N5, N9); 4 endpoint-open mechanisms were not raised by the sweep (R25/R34, R27, R28, R36) |
| 8 | Audit-augmented C+M union | point 13, bounds 11-14 | 5 distinct endpoint C+M mechanisms + 9 sweep C+M - 1 definite C+M duplicate; upper bound counts R25 and R34 apart; lower bound also merges the 2 ambiguous pairs. All-severity union: 25 (23-26) |

Why not 9 + 3 = 12 or 15: headline_raw adds U3 + W + O without deduplication, so N6 and R35 (the same AC-1.2 defect) count twice, and R25 and R34 (one residual) count twice. The union has no control counterpart because no control or Arm B run had a sweep.

Prose vs script and source mismatches found:
1. S1V says "same model" (00:52:31Z) and later "no model substitution"; the session files show `/model` switches to gpt-6.1-sol routing in T08, L4, T09, L5 and L6, not in the log (validity.md V5).
2. The brief and S1V quote the control mean growth as 63.51% (screen 44.457%); recomputing from the comparator bytes gives 63.53% (44.469%). The difference is ctl-r2's rounded 69.3% vs 69.34%. No effect on any comparison here.
3. The R3 report says its new-defect pass is limited to the revised hunks (REV/spec-panel-round3.md:7), yet its finding 2 (R35) sits outside them; the script stored it outside/deferred, consistent with the data, not with the stated scope.
4. Script `minor_touched answered=2` does not mean minor fixes were made: it counts deferred minor rows (R14, R32) whose text lies inside a claimed hunk. Both dispositions record 0 minor rows acted on.
5. The sweep's "did not open the ledger or earlier reports" holds for content (no tool read), but its resolution table works from the `(Rn)` row tags the revisers wrote into the spec, so the loop's row structure was visible to it.
Matches checked and confirmed: U=3, W=9, O=3, headline_raw=15, phase swept, outcome ESCALATE (recomputed from LED/ledger.json rows); 0 unclaimed hunks and 0 reverts in both cycles (ops `begin.unclaimed` empty, `reverted_bytes` 0); 0 reopened rows after cycle 2; spec sizes in the reviser receipts (57763 -> 66484 -> 70565).
## Arithmetic against D10/D11 screens
Screens as stated in D11 (control mean, 2 control replicates). Arithmetic only.

| Screen | Limit | Ledger value | Arithmetic |
|---|---|---|---|
| (a) R3 proxy at most 50% of control mean 6.0 | 3 | 3 (new labels) | 3 <= 3: holds, at the boundary. Ratio to control mean 50.0%; to Arm B mean 3.5: 85.7% |
| (a) same, if unresolved prior C+M labels are added | 3 | 6 | 6 > 3: does not hold. Comparators' R3 proxies count new findings only, so this line has no like-for-like comparator |
| (b) growth after two cycles at most 70% of control mean 63.51% | 44.457% (44.469% recomputed) | 22.16% | holds. Ratio to control mean 34.9%; to Arm B mean 29.96%: 74.0% |
| (c) effect larger than within-arm spread | control spread: proxy 4, growth 11.62 points; Arm B: 5 and 4.36 | proxy effect 3.0, growth effect 41.35 points | proxy effect 3.0 < control spread 4; growth effect 41.35 > 11.62. Ledger's own spread: unknown (n = 1) |
| every replicate on the better side | ctl-r1 8 / 57.72%, ctl-r2 4 / 69.3% | 3 / 22.16% | below both controls on both measures; untestable for a second ledger replicate |

One replicate supplies no within-arm spread and no repeatability. The R3 proxy came from a gpt-6.1-sol reviewer running a hunk-limited pass, while every comparator R3 came from claude-opus-5-5 (validity.md V5). No success verdict is given.
## Not measured
- Within-arm spread and repeatability: one replicate.
- A blocking re-grade of labels in any run, including the sweep rows (labels are reported as written).
- A full-document R3 panel count for this run (the R3 pass was hunk-limited; the sweep is the only full read and it ran blinded in a separate session).
- The author of the five `/model` commands and their intent (UNVERIFIED).
- Worker system prompt content per session.
- Install state between the two hash checks (no watcher for this run).
- Active model time inside rate-limit windows; tokens spent on 429 attempts. Wall time per loop step includes 44.2 min (T08) and 17.4 min (T09) of interruption; the sweep includes 141.4 min. These are reported, not counted as zero or as work.
- Token comparability across providers: gpt-6.1-sol sessions report no cache-creation tokens and large input tokens.

Cost split (metrics.json `sessions`): loop steps T05-T09 237 tool calls, 241266 output tokens, 120.82 wall min; coordinator scripted steps L0-L7 plus setup 76 tool calls, 25602 output tokens; sweep 25 tool calls, 54984 output tokens, 8.5 active min inside 152.96 wall min.
## Limitations (max 8)
1. **Model not held constant.** The round-3 review, the second half of revise 2 and three scripted steps ran on gpt-6.1-sol after undocumented `/model` commands; all comparator steps were claude-opus-5-5. The R3 proxy is therefore not a like-for-like number.
2. **Instrument differs at R3.** The ledger R3 pass looks for new defects only inside the revised hunks; control R3 reviews read the whole document. A low R3 count is partly built into the variant. The sweep (9 more C+M) shows what the restricted pass did not count.
3. **n = 1.** No spread, no repeatability, and D11(c) cannot be evaluated for this arm.
4. **Labels are not blocking.** The proxy counts MAJOR labels the script stored as deferred; the script's own blocker count (3 open) uses a different rule. Neither is a severity-verified defect count.
5. **The union is unaudited for controls.** The audit-augmented union (13, 11-14) has no control counterpart; comparing it with the control proxy 6 would mix instruments.
6. **Environment drift from phase 4.** `~/.claude/WORKER-CONTRACT.md` was present (absent in phase 4 arms), the user-level spec-panel was the 486-line master text sha256 4115f2a97980 (DECISIONS.md D10, install-log.md; not the arm texts, though the ledger reviews loaded spec-panel-ledger.md instead), and the run happened about 17 hours after the controls. No step was seen reading the contract file.
7. **Monitoring gaps.** No install watcher during this run; terminals received typed input not in the run log; overlap and fix-origin judgments are the recorder's reading of finding text.
8. **Growth is measured by bytes on long lines.** Lines grew 1.05% while bytes grew 22.16%; the spec keeps most content in table rows, so line counts hide growth and byte growth is the comparable figure.
## Self-Audit and evidence-package quality verdict
Self-Audit (zero package defects found after the checks below; this judges the evidence package, not the ledger variant):
- Four outputs present: `metrics.json`, `validity.md`, `comparison.md`, `reviews/` (6 reports, 3 history specs, live spec, full review-ledger folder, sweep input copy, `sizes.txt`, `SHA256SUMS`; every copy `cmp`-equal to its source).
- `jq -e . metrics.json` parses; no template placeholder left in any output.
- Every number in this file was searched in `metrics.json` (mechanical grep); the one miss (486) now carries its source (DECISIONS.md D10).
- Frozen endpoint: v3 = r3 = live spec = sweep input by sha256 030b7a941cd3...; v1 = manifest hash d3cdbe573e57....
- Script terms re-derived from source (`u_count`, `metrics`, `tail_text`, `location_class`) and recomputed from ledger rows; all brief-quoted values (U=3, W=9, O=3, headline_raw=15, ESCALATE, swept, 12 sweep findings 9/3, no unclaimed edits or reverts) match.
- Sweep scope and overlap shown with point estimate and bounds; original proxy and audit-augmented union kept apart.
- Parser, grade, model and ownership limits disclosed (V1, V4, V5, limitations 1-7). Failed or unresolved validation attempts kept in validity.md.
- Not checked: tool_result text of every session for every new-command name (only WORKER-CONTRACT and origin/master); line-level attribution of each cycle-2 spec byte to a model.

Evidence-package quality verdict: **PASS** (package complete and traceable). This is not a verdict on the ledger variant: the loop itself ended FAIL/ESCALATE with no clean pass, and validity V5 is FAIL.
