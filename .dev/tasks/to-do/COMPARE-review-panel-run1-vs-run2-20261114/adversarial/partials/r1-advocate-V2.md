# Round 1 Statement: Advocate for Variant 2 (run 2 report)

- Debate: /sc:adversarial Mode A, depth standard, Round 1
- Role: advocate for V2 (`variant-2-original.md`, 5,098 lines); a second advocate argues for V1 (`variant-1-original.md`, 4,476 lines)
- Inputs read in full: `diff-analysis.md` (730 lines), `debate-points.md` (189 lines)
- Id conventions: diff ids (S-nnn, C-nnn, X-nnn, U-nnn, A-nnn) are the ids of `diff-analysis.md`; ids that exist inside a report are always written with "V1" or "V2" in front (for example "V2 C-05" is a debate slot of run 2; "V1 C-05" is a conflict of run 1).
- Line numbers: "V1:n" and "V2:n" are lines of the two variant files (byte-identical to the original reports).
- Read-only: no repo file other than this one was changed; no git write command was run; nothing under `.claude/` was read.

(Sections are appended one at a time below.)

## Position

V2 should be the base of the merged document: it reads the newer E2 evidence (tip `6c09843`, four commits after V1's pin, holding the collaboration and process-redesign material V1 never saw), it covers the whole question (collaboration, process redesign, evaluation independence, repo constraints, a 171-row defect register), and its recommended shape (a thin shared contract with per-module engines, with named triggers for later convergence) rests on verified code facts, while V1 calls core-shape questions "DECIDED-BY-EVIDENCE" that no run decided. V2 is not the whole answer: V1's implementer-grade migration content (48 steps with files, per-gate replacement assertions and collected counts, rollback and persisted-format rules, the gap-to-step map, the ENS post-gate defects and the panel-size decision) must be carried into the merge, and V1 is right on several facts where V2 is wrong (the `KeyError` path, the calibrator 6-vs-5 mismatch, the 1,398 unit, the 0.704 definition, the over-length severity).

## Steelman of Variant 1

**Overall.** The strongest reading of V1 is: "the owner asked for ONE central panel; two stacks behind a shared contract is the status quo with a new name; so pick the superset (findings-v2 with v1 as a strict subset, one clusterer, one merge and verdict, one dispatcher, one run record), build it through the existing v2 code in small steps, keep every unproven decider behind shadow gates, and hand the later plan a migration path it can execute." V1 gets several things right that V2 does not:

- It is the more *usable* hand-off for a `/sc:workflow` plan. Its 8.2 gives 48 steps in four tracks with Action / Files (file:line) / Details / Closes-gaps (V1 8.2, V1:3826-3908); its 8.3 gives each no-regression gate with an exact `uv run pytest` command, a collected count and, per pinned test, the replacement assertion that must change on purpose (V1 8.3, V1:4033-4055, e.g. G1 at V1:4037 and G2 at V1:4038). I re-ran two of its counts: `tests/review` collects 651 and `tests/cli/reflect` collects 353, exactly as V1 states (V1:381, V1:4045).
- It found real defects V2 does not carry: `unauthorized_deviation_present` has no producer (MS-14, V1:641; SC-18 V1:543), the debate return contract has no `merge_method` and writes no `merged-verdict.yaml` (MS-24, V1:651; SC-16 V1:541), and the blocking post gate never produces `REPORT.md` or the per-task verdict matrix (ENS-4, V1:655; SC-21 V1:546).
- Its post-gate position (fix `ensemble.py` in place now, replace at UC-2 Stage 5) attacks a verified false-green production gate (V1 C-17 Status, V1:2314: "the false-green defects are verified in code ... only the fix-in-place-then-replace sequence is feasible"). V2 itself rates the same defects Critical (V2 G-42, G-43, G-44, V2:1277-1279) and then moves nothing.
- It is more often right on small facts: the v1 parser rejects a citation-only line before `annotate` (V1 BL-04, V1:608; V1 7.3 row, V1:3019), 1,398 counts all rows (V1 DOC-18, V1:680), the 0.704 compliance mean mixes definitions (V1 2.1, V1:162), the calibrator is 6-dimension against reflect's 5 (V1 2.1, V1:171), and `ensemble.py` predates E1 (V1 2.5, V1:414).
- It treats panel size and Tier 2 cost as a decision of its own with a recount and an owner-gated Decision D-1 (V1 C-14, V1:2107, V1:2117; Rationale 6, V1:2832), which V2 has no axis for.
- It is honest about its debates: all four ended `partial`, with 26 unaddressed HIGH invariants, and the Option B risk rating is stated as conditional on them (V1 6.X "Condition on the Option B ratings", V1:2620; Section 7 risk table, V1:2862-2867).

**By main cluster.**

- CL-01 core shape: V1's best argument is future-consumer fit: only Option B is "Strong" for both PR review and rf-qa replacement (V1 Rationale 1, V1:2827), and Option A is B's first stage, so the order costs nothing (V1 Rationale 2, V1:2828). Right: the future consumers do need open lenses, module-declared categories and severities, and a location union.
- CL-04 blocking: V1 keeps the hardened single-reviewer veto as the live decider and puts the blind grader in shadow behind a paired replay with a pre-fixed threshold (V1 C-05 resolution, V1:1537). Right: no alternative decider has accuracy data, so nothing should replace the veto without a measurement.
- CL-05 ledger: V1's staged hybrid applies the master-ledger fixes first (cap by refusal, quorum of valid blocks, atomic refusal) and gates the verify-only port on a pre-registered falsifier run (V1 C-13, V1:2052). Right: it does not ship an unmeasured round model.
- CL-09 reflect post gate: see above; V1's fix-in-place targets a verified false-green production gate.
- CL-15 severity: V1 rates by impact; its Critical for over-length drops (V1 D1, V1:589) follows from verdict flips FAIL to PASS, a fail-open outcome.
- CL-18 fact disputes: V1 is right on X-020/X-049/X-053, X-021, X-027, X-028, X-030/X-048 and X-032 (diff-analysis verification table, rows X-020 to X-064).
- CL-20 Section 8: V1's migration path, gate replacement assertions, rollback rules and gap-to-step map are exactly the migration content and no-regression gates the owner says the later plan needs.

## Strengths claimed for Variant 2

1. **Newer, stated, re-checkable evidence baseline.** "Baseline and Conventions" pins HEAD `50d4d2b9d` and the E2 tip `6c0984326...` and says the scope slices were not used as evidence (V2 Baseline, V2:108); the E2 tip is four commits after V1's `4a22d74` (V2 1. Problem Statement, Trigger, V2:135). I re-ran `git rev-list --count 4a22d74..6c09843` = 4 and `git merge-base --is-ancestor` = true; the diff analyst counted collaboration and process-redesign paths at 3 vs 1,145 (C-001). V2 also names what it did not read: the newer E2 commit `e2f2ac268` (axis 6, V2:3641; A-18, V2:3669; Q-39). I confirmed `e2f2ac268` exists, is 7 commits after `6c09843` and is titled "counted results, replicates and write-up for the five collaboration designs".
2. **Covers the half of E2 that V1 never saw.** 2.3 (V2:345-412) reads the r1-r5 collaboration packages and the Sweep Sheet / Recipe Ledger brainstorms; axes 6.6 and 6.7 (V2:2543-2690) give options; Section 7 axes 6 and 7 (V2:3641-3642) and choices A-18, A-19 (V2:3669-3670) give adjudicated, dormant-by-default outcomes with build and enable triggers. V1 has zero coverage (C-028, C-072, C-091: Grep "collaborat" in V1 Sections 2 and 6-9 returns only an external-literature hit at V1:984). The owner asked for ALL value of E2 captured, so this is not optional content.
3. **Evidence independence finding that changes acceptance.** E1's input is byte-identical to E2's designSpec candidate (sha256 `044809e3...`), and E2 tooling writes into the E1 tree (V2 1. Problem Statement, V2:132; 2.2, V2:278, V2:322; CO-14 in 6.12.5; axis 9, V2:3644: "E1 and E2 are one derivation set, so every Tier Q number is a lead until Tier G exists"). V1 treats E1 and E2 as separate support (C-029, U-042, U-075). A later plan that counts E1 and E2 as two replications would over-claim; this is a gate input the plan needs.
4. **Core shape rests on verified code facts and keeps a named path to one engine.** Axis 1 (V2 7. Rationale, V2:3636) argues from facts both advocates verified: the v1 parser rejects a citation-only line at `findings.py:104` before it can reach `annotate`, and `cluster_v2` cannot cluster anchor-only findings (`cluster.py:128-181`, `test_review_cluster.py:279-293`); one engine would rewrite the pinned v1 parser and ledger path. I re-read `findings.py:104` (`_check_flat(obj.get("anchor"), "anchor", 12, 200)`) and `ledger.py:128-136` (`parse_block`, then `annotate` only on `parsed["findings"]`): both facts hold at HEAD `ad8f57560`. V2 also states the cost it accepts (shared defects fixed twice behind one limits module and one repair step) and three triggers T-a, T-b, T-c for converging to one engine (V2:3636; 7.0.1, V2:3578). V1's rejection of Option C (V1 6.X, V1:2622: "leaves D1, D5, D9, the opposite invalid-block policies and the third merge path in place") is aimed at a weaker C than V2's, which shares the repair step that fixes D1 and keeps one drop-and-account contract (V2 delta row "3.2 Merge, cluster, verify", V2:1135).
5. **Honest status of what evidence can and cannot decide.** Every axis is marked UNDECIDABLE-BY-EVIDENCE for its main choice before debate (V2 "Axis status summary", V2:3004-3018); 15 debates are run with margins, tiebreaker level, convergence and conditions per outcome (V2 6.12.9.1, V2:3509-3525; choices A-3 to A-20, V2:3652-3671), and 244 invariant rows (60 HIGH) are carried with status (V2 7.3, V2:3960-4232). V1 calls 16 of 20 conflicts DECIDED-BY-EVIDENCE (V1 Rationale 4, V1:2830), including C-12 whose own acceptance needs human pair labels that do not exist (V1 C-12, V1:1986-1988) and C-04 whose default per consumer "stays an owner decision" (V1 C-04 Status, V1:1443). See X-052.
6. **Precedence is explicit.** The 16-row delta table states where Section 7 withdraws, narrows or replaces Section 3 and 4 cells (V2 3. Target State, V2:1125-1144), and 8.1.2 lists inventory rows whose ledger destination contradicts Section 7 with "Section 7 governs" (V2 8.1.2, V2:4300-4314). A merge of two 1.2 MB reports needs exactly this kind of override record; V1 has none (S-007, S-013).
7. **Ledger and verdict defects V1 misses, with an adjudicated fix.** `defer` rewrites an ESCALATE to PASS and never re-opens, the stored verdict is not derived, rounds after ESCALATE are accepted, and a round is not bound to the revised text (V2 G-14, G-15, V2:1249-1250; U-020). Axis 4 closes them: verdict derived on read and never stored, quorum-gated explicit `prior <lid> resolved`, `pending_new_sha256`, `defer` terminal and counted open, a round after ESCALATE refused (V2 7. axis 4, V2:3639; A-9, V2:3660). V1's own C-13 debate lists `defer` rewriting a FAIL as an open HIGH invariant (V1 risk table, V1:2866, INV-001) but its gap table has no row for it (C-011).
8. **Binding repo constraints, dependency facts and acceptance conditions for the later plan.** 8.2(a) C1-C29 (V2:4430-4458) give each constraint with file:line, enforcer and consequence, including layout traps a plan would otherwise hit: a skill directory without `SKILL.md` fails `verify-sync` (C5, V2:4434), reserved contract names under `cli/` (C6, V2:4435), `.gitignore:13` hides `lib/` (C28, V2:4457), `*_validator.py` triggers a PR-body rule (C14, V2:4443). 8.2(c) D1-D26 (V2:4498-4525) and 8.2(d) AE-1..AE-15 (V2:4529-4549) are dependency facts and acceptance conditions, which the owner says the plan needs. V2 also corrects a repo claim: `CLAUDE.md:31` says pre-commit enforces `verify-sync`; it does not (C5, V2:4434). I confirmed `.pre-commit-config.yaml:117` carries the comment that pre-commit "must not require" `make verify-sync`.
9. **The git-ref constraint observed, not asserted.** C4 (V2:4433) records the exact `fatal:` messages in both creation orders, `git update-ref` failing the same way, and that a dash sibling coexists. This is the constraint the owner names ("`feat/review-panel` and `feat/review-panel/<name>` cannot both exist") and the observed facts are what make the owner's `feat_review-panel/<name>` naming safe to adopt. V1 states the rule without observed output (V1 8.4, V1:4059; U-123).
10. **Defect register and per-family ownership.** 171 rows, owner buckets (CORE 75, MODULE-reflect 29, ...) and reproduction status (V2 1., V2:133; 2.5, V2:580; 7.1 defect-family table, V2:3768-3781 region). V1 carries D1-D16 (V1 6.D, V1:2517-2538; U-058).
11. **Dispatch and read-only risk grounded in the E2 launcher.** 2.6 (V2:592-655) separates five tier-data layers and four dispatch mechanisms; axis 5 (V2:3640) shows the raw-id `claude -p` lane is not read-only by construction (`run-reviewer.sh:48` leaves Bash open), which is why the launcher is gated (G1 identity, G2 read-only, G3 no regression) and not offered to PR review or rf-qa without a process-level tool restriction (7.2.4 verdicts, V2:3842-3849). V1 proposes one dispatcher with adapters (V1 C-09, V1:1792) without this risk.
12. **Future-use verdict per consumer.** 7.2.1 to 7.2.4 (V2:3789-3849) give PR review, rf-qa replacement and later reviewers a "does the final shape block it?" verdict with the condition that keeps it unblocked. This answers the owner's "future use cases not hindered" requirement directly.
13. **Re-derived E2 numbers, with one harness bug found.** V2 re-derives the E2 headline numbers with grades and finds the `final-table.py` `fullpkg()` 12-character-prefix bug that mis-applies EXCLUDE flags (V2 2.2, V2:294-320; C-026, U-039); V1 reports the numbers "doc-sourced ... not re-aggregated" (V1 2.2, V1:191). V2 is right on Qwen "3 of 4 runs" (X-025; `SPEC.md:3` "timed out twice (2 x 3000s) on 3 of 4 runs", which I re-read) and on the flips description (X-026).
14. **Code-decided values are separated from debate-decided ones.** The convergence threshold is 0.80 and single-vendor degrades by code (V2 note after the choices table, V2:3673), with the skill prose conflict flagged (`SKILL.md:703` "≥0.75 PASS", `contract.py:321` `< 0.80`: both re-read by me). V1 states the 0.80 floor (V1:3060) but does not flag the conflict in Sections 7-9 (U-121).
15. **Stage 2 exit failures traced to mechanism, plus an exit-script defect.** V2 2.1 (V2:219-229) traces each failure class to a mechanical cause with run ids and finds the empty-legacy-baseline defect at `scripts/reflect_shadow_exit.py:313`; I re-read line 313: `if (s_rate or 0.0) > (l_rate or 0.0):`, so an empty legacy baseline is compared as 0.0. V1 has one row (V1:162; U-037).
16. **Value inventory reconciles.** 5,950 rows with rows in = rows out and a DROP breakdown (V2 8.1.0, V2:4248-4263); the diff analyst verified 5,779 + 171 = 5,950 against `synth-08` (Partial D table). V1's 698 rows have no reconciliation check (diff-analysis Partial D table).

## Weaknesses identified in Variant 1

(Stated after the steelman above; each is checked against the cited lines.)

1. **Stale E2 pin, and the missing half of E2 follows from it.** V1 reads E2 "at commit 4a22d742... only" (V1 1. Problem Statement, V1:93, V1:102; K-11, V1:564) and so has no collaboration designs, no process-redesign brainstorms, no run-record/cost study, no evaluation-governance study (C-002: "collaborat" 0 hits in V1:1-782). The pin was imposed on V1 by its task (GQ O-6), which is a fair excuse for run 1, but it is not a reason to prefer V1's content for the merge: the owner asked for all E2 value, and V1 cannot supply it.
2. **"DECIDED-BY-EVIDENCE" is over-claimed.** V1 Rationale 4 adopts 16 of 20 resolutions "as written" because they are decided by evidence (V1:2830). Several are not decidable by the cited evidence: C-12 is "DECIDED" (V1:1986) yet its acceptance rule needs human pair labels (issues #525-#530) that do not exist (V1:1988); C-04 is "DECIDED-BY-EVIDENCE by code evidence alone" (V1:1443) although code evidence only shows today's soft re-admission, not which default each consumer should have (V1 itself says "the default per consumer stays an owner decision (G-11)", same line); C-01 rests on "strict subset", which V1's own Cons row says "needs code and tests, not only wording" (V1 C-01 Option A Cons, V1:1211). V2's classification (X-052: "no run compares core shapes", V2:3636) is the accurate one.
3. **"findings-v1 is a strict subset of findings-v2" is false at HEAD.** `findings_v2.py:4` says a v1-valid line with other keys may be rejected; `:96-97` rejects `calibrated_confidence`; `:279-281` rejects `prior` lines, which the v1 loop needs (`findings.py:175-186`). I re-read all four sites. V1's single-contract plan (V1 Recommended approach, V1:2823; C-01 row, V1:2839; constraint row V1:3065) therefore starts by changing the v2 grammar the reflect engine depends on, which is the cost V2's axis 1 avoids (V2:3636).
4. **The superset core is the largest and least measured surface, by V1's own rating.** Option B is XL effort and Medium-High risk (V1 6.X, V1:2578-2579 per C-050), and that risk "holds only if the four debate-gated conflicts ... are settled", which they are not (V1 "Condition on the Option B ratings", V1:2620). The rationale "A is B's first stage, so the order costs nothing" (V1:2828) is an assertion, not a measurement.
5. **E2 numbers are doc-sourced, with two description errors.** V1 says its E2 headline numbers were "not re-aggregated from raw score.json" (V1 2.2, V1:191), and two of its descriptions are wrong: Qwen "timed out 3 of 3 slots" (V1:204) against `SPEC.md:3` "3 of 4 runs" (X-025, re-read by me), and audit D "names 3 plus a merge that lost two blocking findings" (V1:201) double-counts the third flip (X-026). It also leans on scope slices and hand-offs as evidence (S-016, A-024).
6. **Fewer ledger and verdict defects.** V1's gap table has no row for `defer` rewriting the verdict, the stored verdict going stale after `revise`, rounds after ESCALATE, or a round not bound to the revised text (C-011; V2 G-14, G-15 at V2:1249-1250), although its own C-13 debate names the `defer` defect as an open HIGH invariant (V1:2866, INV-001).
7. **No precedence record, and inventory destinations follow an undecided design.** V1 has no table that says which Section 3/4 wording its Section 7 overrides (S-007, S-013), and its 698 inventory destinations are its own 16 core components (V1:3117-3119), so they inherit the four `partial` debates (A-056).
8. **Dispatch end state ignores the read-only risk of a raw-id lane.** V1's "one dispatcher interface with adapters (`agent-class`, `cli-model`, `swarm`)" (V1 C-09, V1:1792) does not price that E2's `claude -p` launcher leaves Bash open (`run-reviewer.sh:48`, cited by V2 axis 5, V2:3640), which matters for PR diffs.
9. **Counts with unstated units.** "43 spawning call sites in 11 skill files" (V1 BL-12, V1:616; V1 7.1.4, V1:2976) is not reproduced by any line count: I re-ran `grep -rEn 'subagent_type: *"?rf-' src/superclaude/skills` = 52 lines in 11 files (X-022, X-029, X-061). "33 keys, 11 outside" (V1 MS-13, V1:640) mixes a conditional key into the count without saying so (X-023, X-024). `tests/cli/reflect` "has 37 files" (V1:381) while `ls tests/cli/reflect/test_*.py` = 38 (V1 itself says 38 at V1:4045).
10. **Web research misses the runtime and git topics a plan depends on.** No hooks/headless semantics, no `--tools`/`--allowedTools`/`--restricted`, no ref-naming or stacked-PR facts (C-048: Grep "PostToolUse", "stacked", "check-ref-format" = 0 in V1:783-1153).
11. **Section 8 contains plan content the owner has now excluded.** Five branch layouts A-E (V1 8.4, V1:4057-4069), a 25-row risk register and a 17-item checklist (V1 8.5-8.6, V1:4075-4120) are a branch plan and a risk register; the owner has decided branch naming (`feat_review-panel/<name>`) and excluded branch, PR and schedule plans from the merged document. Only the git constraint itself (V1:4059) survives.

## Concessions

Genuine weaknesses of V2, each checked against V2's text and, where a fact is involved, against the code.

1. **The `KeyError` claim is wrong for the shipped merge path, and V2 uses it as evidence.** V2 says a v2 citation-only finding raises `KeyError: 'anchor'` on the ledger path in G-01 (V2:1236), SC-01 (V2:1177), G-99 (V2:1334), 6.1 "Shared facts" (V2:2177), CO-1 (6.12.5), axis 1 option D text (V2:3636, "a citation-only finding crashes the v1 ledger path"), axis 2 "Evidence for the adjudicated choice" (V2:3637, "crashes the v1 ledger path with `KeyError 'anchor'` ... REPRODUCED"), contradiction C-2 (V2:3882) and dependency fact D9 (V2:4508). At HEAD the v1 `parse_block` rejects the line at `findings.py:104` ("anchor must be a string") and `continue`s (`findings.py:188-192`), so `ledger.py:136` `annotate` never sees it; the `KeyError` (`findings.py:349`) happens only on a direct `annotate` call or a switch to the v2 parser. I re-read all four sites. V2's own axis 1 (V2:3636, "rejected at `findings.py:104` before it can reach `annotate`"), the C-01 outcome (V2:3511) and Appendix B (V2:5085) hold the correct form. V1 is right (X-020, X-049, X-053, A-057). The adjudicated choice still stands on the correct fact (the v1 path cannot carry citation-only findings), but every wrong instance must be corrected in the merge.
2. **True facts tagged [UNVERIFIED] or mis-described.** The calibrator is 6-dimension against reflect's 5 (`confidence-calibrator.md:3`; `sc-reflect-protocol/SKILL.md:1262,1835`, re-read by me), yet V2 tags it [UNVERIFIED] (2.9.3 row 12, V2:891; OQ-09, V2:1033; RE-4 in 6.12.4) (X-030, X-048). V2 calls 1,398 "multi-member rows" (G-133, V2:1368; 7.1 element 2) while `audit2.py` counts every row before the `< 3` filter (X-021, re-read by me at `git show 6c09843`). V2 labels the pilot 0.704 "first-parse" (V2:215) although the first-parse definition was introduced by commit `9874d63fb` after some pilot values were written (X-027). V2's `cluster_agreement` row omits shadow09's 0.9328 (X-028). V1 is right on all four.
3. **One severity contradicts V2's own rubric.** V2's rubric makes "a verdict that fails open" Critical (V2 3. source note, V2:1121), but G-06 (over-length drops: 49 blocking lost, 3 verdicts flipped FAIL to PASS) is rated Important (V2:1241). V1's Critical (V1 D1, V1:589) is the consistent rating (X-011).
4. **Critical post-gate defects are left in production.** V2 rates engine A's count-derived gate, dormant `--fix`/HALTED and missing executor exclusion Critical (G-42, G-43, G-44, V2:1277-1279), then adjudicates "no engine moves now" and only discloses that "the production T5 PASS is ... a convergence-and-diversity result with no deviation audit" (axis 8, V2:3643; C16 weak reading, V2:4445). V1's fix-in-place (V1 C-17, V1:2314-2316; M3-03..M3-07) is the better answer for a blocking gate that cannot HALT (X-043, X-054). I concede that cluster point.
5. **V1 contributions V2 lacks.** `unauthorized_deviation_present` with no producer (U-001), the debate return contract lacking `merge_method` and `merged-verdict.yaml` (U-002), `REPORT.md` and the per-task verdict matrix never produced (U-003), panel size and Tier 2 cost as a decision (C-073, C-093, U-086), calibration as its own decision (C-056, U-089), the PR router-vs-rubric divergences and `deep=True` dormancy (U-006, U-062), and the judge seeing the combo name (U-059) are all absent from V2 (diff-analysis U rows give the searched ranges).
6. **Section 8 is thinner where a plan executes.** V2's gates G1-G16 cite commands and pins but give no replacement assertion per pinned test and few collected counts (V2 8.2(b), V2:4464-4481), and G17-G27 are mostly "not run / not built" (V2:4482-4492). V1 has the replacement assertions (U-097), collected counts (U-098), persisted-format and rollback rules (U-100: Grep "rollback" in V2 = 0) and a gap-to-step map (U-101). V2's refusal of "plan content" (V2:4412) went further than the owner's exclusion, which is a roadmap, branch plan, PR plan and schedule, not migration content.
7. **Internal inconsistencies that a reader must resolve through the delta table.** SC-17 says the convergence threshold is a "decision, 0.75 or 0.80" (V2:1193) while the delta row says the code decides 0.80 (V2:1137) (C-017); G-85 (V2:1320) and 3.5 (V2:1227) still list DO4 as open while the delta row says decided (V2:1132) (X-005); SC-04 says the quorum is a "decision" (V2:1180) while the delta row fixes `min(2, requested)` (V2:1138) (X-004); 2.4 reports the E3i scripts as read (V2:432-448) while 2.9 OQ-01 tags every E3i cell [UNVERIFIED] (V2:1025) (X-034). The precedence statement (V2:120, V2:1125) resolves them formally, but the merge should fix the text.
8. **Count errors.** "50 test files" under `tests/pr_submit` (V2:1335, V2:2973, V2:3735, V2:3804, V2:4479, V2:4593) is wrong: `ls tests/pr_submit/test_*.py` = 47 (49 `.py` files with `conftest.py` and `__init__.py`); V2:3797 itself says 47. G-96 says `sc-reflect-protocol/SKILL.md` references `superclaude review` "(6)" times (V2:1331): `grep -c` = 5 lines, `grep -o | wc -l` = 7 occurrences (X-017).
9. **The adjudicated design rests on narrow tiebreaker wins.** All 15 debates ended `partial` with 60 HIGH invariants open (V2 7.3, V2:3960-4232); several margins are tiny: C-08 run record 0.13 percent (A-10, V2:3661), X-13 0.94 percent (A-19, V2:3670), X-14 0.97 percent (A-11, V2:3662), C-01 core shape 2.45 percent, settled by a tiebreaker in which B won 10 of 23 points (A-15, V2:3666). V2 states this, but the merged plan must treat these outcomes as defaults with conditions, not settled facts (A-031, A-052).
10. **The "one core" wording needs owner confirmation.** V2 itself flags that the adjudicated design is "a shared contract plus two engines ... not one engine on which every module is a profile" and asks the owner to confirm the reading (V2 7.0.1, V2:3582; Q-40). The owner's decision fixes the location and thin modules, not engine count, so this stays an open owner question in the merge.
11. **Some severities apply rule C8 to staging statements or to the adjudicated target itself.** G-21/G-84 call the panel's "ships in Stage 3" staging a C8 defect (V2:1256, V2:1409), and V2's own delta row then records that adjudicated outcomes defer it (V2:1144). G-24 rates "no dispatch contract / launches none" Critical (V2:1259) while the adjudicated design keeps "the core launches nothing" (V2:1139). V2's rule that a gap keeps its severity "as a statement about today's code" (V2:1125) is coherent but makes the Critical count (24, V2:1387) a poor guide to what a plan must do first.
12. **The value inventory is not in the report.** Only 8.1.0-8.1.4 are inline; the 5,950 rows live in `synth-08-value-inventory.md` (2,024,775 bytes) by pointer (V2 8.1.2, V2:4280-4296; Appendix A, V2:5072-5075; S-048). The merged document must carry that file as a named input or the inventory is lost.

## Cluster verdicts

| Cluster | Stronger on this topic | Confidence | Evidence (headings + lines, <= 2 sentences) |
|---|---|---|---|
| CL-01 Core shape and engine boundary | V2 | 65% | V2 7. axis 1 (V2:3636) argues from verified facts (v1 rejects citation-only at `findings.py:104`; `cluster_v2` cannot cluster anchor-only) and names convergence triggers T-a..T-c; V1's single contract needs v2 to accept `prior` lines and `calibrated_confidence`, which `findings_v2.py:96-97,279-281` reject today (V1 C-01 Cons, V1:1211). V1's future-consumer argument (V1:2827) is real but V2 meets it with module-declared sets and adapters (V2 7.2.4, V2:3842-3849). |
| CL-02 Finding contract, locations, PR fields | V2 | 60% | V2 A-14 keeps `pr_submit.Finding` untouched and computes `in_diff` from changed ranges in a pure converter (V2:3665); `in_diff` exists nowhere in `cli/review` today (diff-analysis X-059). V1's BL-18 lens-carried PR fields (V1:622) are a reasonable later option, not a first step. |
| CL-03 Over-length lines, claim cut, drop record | MERGE | 60% | V2's adjudicated repair (three location fields to 200 chars behind `repair=False`, itemised drop record with `blocking_state`, dropped-blocking refusal, one re-ask; V2 axis 3, V2:3638) is the stronger base; V1 adds that 10 of 49 blocking losses are claim overruns (V1 SC-2, V1:527) and the missing-anchor rule (V1 C-02, V1:1315). The claim cut stays an owner decision with the K2 test. |
| CL-04 Who decides blocking, quorum, grader, exit codes | V2 | 60% | No decider but the veto has ground-truth numbers (A-030), the stoprule integrity check returns `EXIT_OK` on a grader mismatch (diff-analysis X-039 verification) and V1's own debate found an always-demoting grader passes its replay criterion (V1 risk table INV-019, V1:2865); V2's typed `blocking` plus CRITICAL floor plus `min(2, requested)` refusal (V2 A-3, A-4, V2:3654-3655) is the safer core default. Keep V1's calibrator facts (C-056). |
| CL-05 Ledger rounds, clearing, verdict derivation | V2 | 65% | V2 axis 4 closes the reproduced D-1, D-2, D-11, D-13 defects with explicit quorum-gated clearing, derived verdict, `pending_new_sha256`, `defer` terminal (V2:3639; A-9, V2:3660); V1 leaves the round model to an unscheduled decision gate (V1 C-13, V1:2052) and has no row for `defer` or stored-verdict defects (C-011). |
| CL-06 Dispatch, identity, tier data, read-only | V2 | 65% | V2 2.6 (V2:592-655) and axis 5 (V2:3640) show the raw-id lane leaves Bash open (`run-reviewer.sh:48`) and gate the launcher on identity, read-only and no-regression; V1's adapter set (V1 C-09, V1:1792) does not price that. Keep V1's S-ID identity probes (U-060). |
| CL-07 Distinctness default | OPEN | 55% | Code shows only today's soft default (`panel.py:509,519`, re-read); neither report measured strict against soft at equal reviewer count (V2 A-6 "soft stands until A's M1", V2:3657; V1 C-04 says the per-consumer default "stays an owner decision", V1:1443). V2 is right that V1's "DECIDED" is over-claimed; V1's per-slot declaration is a good design option to keep. |
| CL-08 Run record, manifest, telemetry | V2 | 55% | V2 shows the manifest's lock-free lost update and the `model_scores` double count (V2 2.5, V2:569-578; U-083) and adds `events.jsonl` written only by code (A-10, V2:3661); the win is narrow (debate margin 0.13 percent) and V1's "telemetry as projection of the committed manifest" (V1 C-07, V1:1665) is a valid alternative. |
| CL-09 Reflect Tier 2 engines, shadow exit, contract writer | MERGE | 60% | V1 is right to fix the verified false-green post gate in place now (V1 C-17, V1:2314-2316) and to carry U-001/U-002/U-003; V2 is right that no engine replacement is ready, that deterministic shadow steps should be code-owned helpers writing comparison siblings, and on the exit-script defect at `reflect_shadow_exit.py:313` (V2 axis 8, V2:3643; 2.1, V2:229). |
| CL-10 Consumers and entry points | V2 | 65% | V2 decides the DO4 entry with reopen conditions (A-13, V2:3664) and maps 14 consumers incl. T1-T5 and `tasklist validate` (V2 2.7, V2:659-726); V1 leaves O-3 open (V1:2973, Q-03 V1:4138). V2's G-85 and 3.5 text must be aligned with its delta row (V2:1132). |
| CL-11 E2 collaboration and process redesign | V2 | 85% | V2 2.3 (V2:345-412), axes 6.6-6.7 (V2:2543-2690), A-18/A-19 (V2:3669-3670); V1 has no coverage (C-028, C-072, C-091). |
| CL-12 Installed-only E3 variants | V2 | 70% | V2 axis 10 "port contracts, not scripts" with the keep-or-archive owner decision (V2:3645; 6.10, V2:2862-2934) and the facts that `superclaude install` neither installs nor removes them (U-044); V1 uses variants as design sources without an axis (C-071). V2's 2.4 vs 2.9 verification status must be reconciled (X-034). |
| CL-13 Evaluation, ground truth, evidence independence | V2 | 70% | V2's three-tier acceptance and "E1 and E2 are one derivation set" (V2 axis 9, V2:3644; CO-14) and re-derived E2 numbers with the `fullpkg()` bug (V2 2.2, V2:294-320) beat V1's doc-sourced numbers (V1:191). Keep V1's "judge sees combo name" (U-059) and its 1,398 unit (X-021). |
| CL-14 Decisions only one report treats | MERGE | 70% | V1's panel size and Tier 2 cost (V1 C-14, V1:2107-2117) and calibration (V1 C-06, V1:1543-1604) have no V2 axis; V2's collaboration, process redesign, variants and harness owner (V2 6.6, 6.7, 6.10, 6.9.b) have no V1 axis. A plan needs both sets. |
| CL-15 Severity ratings and rule C8 | MERGE | 60% | Neither report applies one rule consistently: V2 is inconsistent on G-06 (Important despite fail-open flips, V2:1241 vs rubric V2:1121) and G-24 (V2:1259 vs V2:1139); V1 under-rates clearing by silence (V1 D2, V1:590). Carry both ratings with basis and re-rate per row against one stated rubric. |
| CL-16 Evidence baseline, pins, freshness | V2 | 75% | V2's tip `6c09843` is a descendant of V1's pin with 4 more commits (re-run: `rev-list --count` = 4); code at both HEADs and at HEAD `ad8f57560` is identical for `src tests scripts` (re-run: empty diffs). Both are now stale against `e2f2ac268` (7 commits after the tip), which only V2 names (Q-39). |
| CL-17 Section 6 method, statuses, debates | V2 | 65% | V2 marks every axis UNDECIDABLE before debate and records 15 adjudicated outcomes with conditions (V2:3004-3018, V2:3509-3525) and a 189-row conflict log (V2 6.12, V2:3130-3566); V1 over-claims 16 of 20 DECIDED (V1:2830). Keep V1's 6.D defect-to-test table (U-087) and 6.E implementer detail (U-088). |
| CL-18 Fact disputes settled by code or data | V1 | 60% | V1 is right on the `KeyError` path (X-020, X-049, X-053, A-057), 1,398 (X-021), the 0.704 definition (X-027), `cluster_agreement` (X-028), the calibrator mismatch (X-030, X-048) and `ensemble.py` provenance (X-032); V2 is right on the rf-* census (X-022, X-029, X-061), key count (X-023, X-024), `same_defect` (X-031) and the identity count (X-050). V1's wins carry more design weight (V2 used the wrong `KeyError` claim as evidence at V2:3637). |
| CL-19 Section 7 shape and override layer | V2 | 70% | V2's delta table (V2:1125-1144), 7.0.1 combination table and tensions CT-1..CT-6 (V2:3586-3617), facts F-1..F-6 (V2:3621-3628) and per-consumer verdicts (V2:3842-3849) make the recommendation auditable; V1 has no override layer (S-007, S-013). |
| CL-20 Section 8 form and value inventory | MERGE | 75% | The plan needs V1's migration content (48 steps with files, V1:3826-3908), replacement assertions and collected counts (V1:4033-4055), rollback rules (U-100) and gap-to-step map (V1:3910-4030), and V2's constraints C1-C29, dependency facts D1-D26, acceptance AE-1..AE-15 (V2:4430-4549) and reconciled 5,950-row inventory (V2:4248-4263). V1's branch layouts and risk register are dropped by owner decision. |
| CL-21 Sections 1, 3, 4 residual | MERGE | 60% | V2's SC-21..SC-33, K-5/K-6/K-8/K-9 and the 4.6 carry-over (V2:1197-1223, V2:1488-1536) plus V1's SC-18..SC-22, SC-6/SC-10/SC-14 pass rules and per-row track tags (V1:531-547, V1:761). |
| CL-22 Section 2 organisation and depth | V2 | 70% | V2's 9 subsections incl. dispatch (2.6), consumers (2.7) and eval/governance/repo constraints (2.8) with per-subsection "Not verified" lists (V2:139-1111); V1's 6 subsections lack 2.8-type content (S-020). Keep V1's D1-D16 table with "Reflect v2 shares it?" (U-058). |
| CL-23 Section 5 external research | MERGE | 75% | Source sets are nearly disjoint (diff-analysis Partial B term counts): V1 covers severity taxonomies, calibration methods and clustering algorithms (V1:853-1079); V2 covers hooks/headless, git refs and stacked PRs, finding schemas (V2:1698-2036). A plan needs both. |
| CL-24 Sections 9-10, open questions, id namespaces | V2 | 60% | V2's Q-01..Q-93 with a Source column (V2 9, V2:4689-4846) and 4.6 consolidated decisions D-1..D-14 and U-1..U-18 (V2:1494-1532) are easier to route; both reports' ids collide (A-006, A-058) and must be re-keyed. Keep V1's owner items O-1..O-6 incl. issues #525-#530 (U-105). |
| CL-25 Section 6 residual | MERGE | 55% | V1's "651 tests" is a collected count and is right (re-run: 651 collected; 380 `def test_` in 19 files); the E1 shadow numbers are valid with the "6 of 9" doc-sourced caveat (A-041); citation keys must be unified (S-042). |

Tally: V2 stronger in 15 clusters (CL-01, 02, 04, 05, 06, 08, 10, 11, 12, 13, 16, 17, 19, 22, 24); V1 stronger in 1 (CL-18); MERGE in 8 (CL-03, 09, 14, 15, 20, 21, 23, 25); OPEN in 1 (CL-07). CL-26 has no points.

## Per-point verdicts

### Contradictions (all 63)

| Point | Winner | Confidence | Evidence (<= 2 sentences) |
|---|---|---|---|
| X-001 | V2 | 75% | `6c09843` descends from `4a22d74` with 4 more commits holding the collaboration material (re-run: `rev-list --count` = 4, ancestor true). Both are behind `e2f2ac268`, 7 commits later. |
| X-002 | V2 | 65% | Two grammars avoid rewriting the pinned v1 path; v2 rejects `prior` and `calibrated_confidence` (`findings_v2.py:96-97,279-281`), so "one contract" is not a free unification. V2's pre-adjudication row (V2:1161) is superseded by its delta row (V2:1134). |
| X-003 | V2 | 60% | V1's measured decider is a precondition only (V1 SC-10, V1:535) and its D4 target names candidate deciders none of which has accuracy data (A-030). V2's typed boolean plus CRITICAL floor is a concrete, testable rule (V2:1137). |
| X-004 | BOTH | 55% | Both end at a `min(2, ·)` floor (V1 6.E.1 C13-06 per C-055; V2 A-3, V2:3654); V1 SC-3 "open" (V1:528) and V2 SC-04 "decision" (V2:1180) both lag their later text. |
| X-005 | V2 | 65% | V2 adjudicates keep `/sc:reflect --mode pre` with reopen conditions (A-13, V2:3664); neither skill passes `--t2-engine` (diff-analysis X-047 verification). V2's G-85 (V2:1320) and 3.5 (V2:1227) must be aligned. |
| X-006 | V2 | 60% | "Medium" has six uses and no schema value in `cli/review` (V2 axis 2, V2:3637); module label maps keep native words without a core token. V1's lossless mapping goal (V1 SC-11, V1:536) is kept as a module-map requirement. |
| X-007 | V2 | 60% | A pure converter leaves `Finding`, `Severity`, the FSM and `REVIEWERS` untouched (A-14, V2:3665); `in_diff` is absent from `cli/review` today (X-059 verification). |
| X-008 | V1 | 55% | V2's own Section 1 says PR review needs "an optional per-slot lens" (V2:134), and the C-11 withdrawal covers only the rf-qa first change (A-17, V2:3668). Keep V1's optional `role`/`lens`/`agent` slot keys (V1 BL-08, V1:612) as a reserved option. |
| X-009 | V2 | 60% | Gateway `launch: {}` and the raw-id lane's open Bash (V2 axis 5, V2:3640) make "core launches nothing" plus a gated launcher the safer end state than V1's adapter set (V1 MS-06, V1:633). |
| X-010 | V2 | 55% | V2's events record answers the manifest lost-update and cost double-count defects (U-083; A-10, V2:3661); margin 0.13 percent, so V1's manifest-projection design stays a recorded alternative. |
| X-011 | V1 | 70% | 3 verdicts flipped FAIL to PASS is fail-open, Critical under V2's own rubric (V2:1121); V2's Important (V2:1241) is inconsistent. |
| X-012 | V2 | 65% | A defect found by 3 of 3 reviewers cleared by one empty-block reviewer and the round passed (V2 G-12, V2:1247; `ledger.py:254-258`): fail-open, so Critical. |
| X-013 | V1 | 55% | `lint_cmd`/`estimate_cmd` are not panel capabilities and the swallowed `ModuleNotFoundError` (`__init__.py:30-35`) is a hygiene defect; "Important" (V1 D13, V1:601) is proportionate. |
| X-014 | V1 | 55% | V1 marks the "shipped" premise [UNVERIFIED] until Q-58 (V1 SC-12, V1:537); the diff analyst found the C8 premise not checkable by command, so V2's [CODE-VERIFIED] C8 tag (V2:1258) over-claims. |
| X-015 | V1 | 55% | The skill stages the panel ("rejected until Stage 3", `SKILL.md:87`) and V2's own delta row records the adjudicated deferral (V2:1144); Important (V1 MS-08, V1:635) is the more useful rating for a plan. |
| X-016 | V2 | 55% | The Stage 2 exit is the gate that enables the reflect panel, and its failures are deterministic steps done by the LLM (V2 G-47, V2:1282; V2 2.1, V2:229); the target cannot hold until fixed. |
| X-017 | V2 | 55% | The CLI has a prose caller (V1 D14, V1:602), so it is not unwired; Important is right. V2's "(6)" count is wrong (5 lines, 7 occurrences, re-run). |
| X-018 | V1 | 60% | V2 rates "launches none" Critical (V2:1259) while its adjudicated target keeps "the core launches nothing" (V2:1139); V1's Important (V1 MS-06, V1:633) fits the target. |
| X-019 | V2 | 55% | Without an acceptance definition no use case can be "accepted" (V2 axis 9, V2:3644), and the driving document not reaching reviewers is E2's measured H1 lever (V2 G-36, V2:1271). |
| X-020 | V1 | 90% | Re-read: `findings.py:104` rejects, `:188-192` `continue`s, `ledger.py:128-136` annotates only parsed findings; `KeyError` only on a direct `annotate` call. |
| X-021 | V1 | 85% | Re-read at `git show 6c09843`: `audit2.py` increments `rows_total` before `if len(mem) < 3: continue`. |
| X-022 | V2 | 75% | Re-run: 52 lines in 11 files, 44 in 8 `SKILL.md` files; V1's 43 has no reproducible unit. |
| X-023 | V2 | 65% | The literal has 32 keys plus a conditional `t2_fallback` (`ensemble.py:787-834`); V2 states the literal, V1 does not say which count it uses. |
| X-024 | V2 | 65% | Same fact as X-023; V2's 10 outside the frozen lists is reproduced by the analyst, V1's 11 depends on an unstated choice. |
| X-025 | V2 | 85% | Re-read `SPEC.md:3` at the tip: "timed out twice (2 x 3000s) on 3 of 4 runs". |
| X-026 | V2 | 75% | Audit D's third flip is the F1+F2 merge itself (analyst read `summary.md`), so V1's "plus a merge" double-counts; V1's number 3 stands. |
| X-027 | V1 | 70% | Commit `9874d63fb` changed the definition to first-parse; pilot values written before it are not first-parse values (analyst check). |
| X-028 | V1 | 65% | shadow09's `clusters.json` holds 0.9328 but its contract does not parse, so the exit script sees only 1.000 values; V1's statement is the complete one. |
| X-029 | V2 | 75% | Same census as X-022 (re-run). |
| X-030 | V1 | 85% | Re-read: `confidence-calibrator.md:3` "6-dimension"; `sc-reflect-protocol/SKILL.md:1262,1835` "5-dimension". |
| X-031 | V2 | 75% | `findings.py:367-379` has the both-empty-refs branch V1 omits (analyst check). |
| X-032 | V1 | 60% | `git log` of `ensemble.py` shows #203-#329 before E1; V2's "engine A inside E1" is a scope grouping that hides provenance. |
| X-033 | V2 | 55% | V2's table lists seven rows incl. tasklist skill vs CLI and `/sc:implement` (V2:687-695); definitional and not audited. |
| X-034 | V2 | 55% | V2 read the script bodies and matched 17 of 17 sha256 values (V2 2.4, V2:432-448) where V1 read descriptions only; V2 must drop its contradicting OQ-01 tag (V2:1025). Not checkable here (`.claude/` not read). |
| X-035 | V2 | 70% | SARIF 2.1.0 section 3.27.9 lists six `kind` values including `review` (from knowledge of the OASIS text; not fetched in this round). |
| X-036 | V2 | 55% | V2 states it read the paper's figure; V1 excluded a blog-attributed figure. Neither was re-checked here. |
| X-037 | V2 | 60% | V2 cites official OpenAI docs plus a prompt gist (V2 5.4.4, V2:1980); V1 had only a third-party blog (V1:878). |
| X-038 | V2 | 65% | Same as X-002; V2's shape is adjudicated with conditions (A-15, V2:3666); V1's is called decided without a comparison run. |
| X-039 | V2 | 60% | Grader safeguards are weak (stoprule `EXIT_OK` on mismatch; V1's own INV-019 at V1:2865); no grader has accuracy data. |
| X-040 | OPEN | 55% | Claim overruns are 10 of 49 blocking losses (V1 SC-2, V1:527), but a cut claim can lose a decision-relevant clause (V2 K2, G21 at V2:4486). Owner decision with the K2 measurement; record both facts. |
| X-041 | OPEN | 55% | Today's code is soft (`panel.py:509,519`); no measurement of strict vs soft exists (V2 A-6, V2:3657). V1's "decided by code evidence" (V1:1443) is over-claimed; V2's soft default is a placeholder pending M1. |
| X-042 | V2 | 65% | `cluster_v2` leaves anchor-only findings as singletons (`cluster.py:126-147`), and V1's acceptance needs human pair labels that do not exist (V1:1988). |
| X-043 | V1 | 60% | V1 C-17 targets verified false-green defects that V2 itself rates Critical (V2 G-42..G-44, V2:1277-1279); fixing in place is repair, not an engine move. |
| X-044 | V2 | 60% | Follows from the core shape; both keep reflect's `derive_verdict` and 36-test matrix (V1 C-11, V1:2849; V2 C19, V2:4448). |
| X-045 | V2 | 60% | Same evidence as X-009. |
| X-046 | V2 | 65% | V2's closed design fixes reproduced D-1, D-2, D-11, D-13 (V2 axis 4, V2:3639); V1's gate between designs is not scheduled and has 10 open HIGH invariants (V1:2866). |
| X-047 | V2 | 60% | Same as X-005; V1's "shared panel protocol reference" (V1:2536) adds a second entry path no consumer needs today. |
| X-048 | V1 | 85% | Same fact as X-030. |
| X-049 | V1 | 90% | Same fact as X-020; V2's later text (V2:3511) agrees with V1. |
| X-050 | BOTH | 70% | 1 of 15 combo contracts records `observed` (V2 DATA-10) and no Python writer exists (V1 6.0 C08, V1:1177); both statements hold. |
| X-051 | V2 | 65% | Same as X-002 and X-038. |
| X-052 | V2 | 75% | No run compares core shapes (V2 axis 1, V2:3636); V1 cites none for its DECIDED status (V1:2830). |
| X-053 | V1 | 90% | Same fact as X-020; V2 C-2 (V2:3882) and D9 (V2:4508) must be corrected. |
| X-054 | V1 | 60% | Same as X-043; V2's C16 "weak reading" (V2:4445) leaves the Critical post-gate defects untouched. |
| X-055 | V2 | 60% | Same as X-039; today `ledger.py:187` makes one reviewer's flag decide, and V2's floor plus quorum is the measurable improvement. |
| X-056 | OPEN | 55% | Same as X-040. |
| X-057 | OPEN | 55% | Same as X-041. |
| X-058 | OPEN | 55% | Both add exit 12 with different meanings (V1 PENDING, V1:3841; V2 quorum refusal, V2:3639); V1 notes the installed variant already uses 12 for CONTINUE (V1:3001). The merge must pick one meaning and check that collision. |
| X-059 | V2 | 60% | Same as X-007. |
| X-060 | V2 | 65% | Same as X-005. |
| X-061 | V2 | 75% | Same census as X-022. |
| X-062 | V2 | 75% | Same as X-001. |
| X-063 | BOTH | 90% | Re-run: `git diff --stat 792cf8c52 50d4d2b9d -- src tests scripts` and `50d4d2b9d HEAD` are both empty; HEAD is `ad8f57560`. |

### High-severity structural points (all 22)

| Point | Winner | Confidence | Evidence (<= 2 sentences) |
|---|---|---|---|
| S-004 | V2 | 60% | V2 numbers 3.1-3.5 and opens with the precedence table (V2:1125-1227); keep V1's consumer table C-A..C-E and core diagram (V1:496-520, U-009). |
| S-007 | V2 | 80% | Only V2 records which Section 3/4 cells Section 7 overrides (V2:1125-1144). |
| S-011 | BOTH | 60% | V2's flat topical G-01..G-148 (V2:1236-1383) is easier to search; V1's id families (D, BL, MS, ENS, DOC; V1:589-733) carry the consumer each row blocks. The merge re-keys both. |
| S-012 | V1 | 65% | V1's per-row `Track:` tag and the Critical/Important-by-track table (V1:761, V1:772-780) route each gap to a destination; V2 has no such column. |
| S-013 | V2 | 80% | Same as S-007 (V2:1232, V2:1125-1144). |
| S-015 | V2 | 75% | Same as X-001. |
| S-016 | V2 | 65% | V2 cites research files that re-derived values (V2:108); V1 uses scope slices as evidence (V1 2. citation key, V1:108-123), which A-024 shows carry wrong figures. |
| S-017 | V2 | 60% | V2's 9 subsections hold content a plan needs (2.6, 2.7, 2.8); its size (972 lines) is a cost. |
| S-018 | V2 | 85% | V2 2.3 (V2:345-412); V1 has no collaboration content (C-028). |
| S-020 | V2 | 80% | V2 2.8 (V2:730-826): eval harness, governance, repo rules, branch-ref test; absent in V1 Section 2. |
| S-022 | V2 | 60% | V2's classified matrix with ABSENT cells, CF/SS/PS/DU and RC/CC tables (V2:830-1110); V1's "same data contract / same code" columns (V1:436-461) are worth keeping. |
| S-027 | BOTH | 75% | Disjoint web source sets, both needed (CL-23). |
| S-032 | V2 | 60% | Axes plus a full conflict log (V2:2158-3566) separate options from decisions; V1's per-conflict blocks with resolutions (V1:1191-2515) are easier to read. |
| S-036 | V2 | 70% | V2's UNDECIDABLE-before-debate status is accurate (V2:3004-3018); V1's 16 of 20 DECIDED is over-claimed (X-052). |
| S-037 | V2 | 65% | 15 adjudicated debates (V2:3509-3525) vs 4 (V1:1383, 1541, 2054, 2121); V1's 6.E row tables carry implementer detail (U-088). |
| S-038 | V2 | 65% | 189 logged conflicts in Tables A-G with 14 named invariants INV-A..N (V2:3177-3425) vs a 20-row index (V1:1168-1189). |
| S-045 | BOTH | 70% | Same as CL-14: each report has stand-alone decisions the other lacks. |
| S-046 | V2 | 60% | V2's Section 7 is auditable (combination table, tensions, facts, A-3..A-20, register, 7.3); its 667 lines are a cost (V2:3567-4233). |
| S-047 | BOTH | 75% | Same as CL-20. |
| S-048 | BOTH | 65% | V2's 5,950-row inventory reconciles but lives in a 2 MB appendix file (V2:4280-4296); V1's 698 rows are inline (V1:3121-3820). Carry V2's file as a named input and fold V1's rows that V2 lacks. |
| S-049 | BOTH | 60% | V2's destinations add EVAL, HARNESS, KNOWLEDGE (V2:4250-4259); V1's 23 component destinations and Effort column are finer (V1:3117-3121). |
| S-056 | BOTH | 70% | V1's gates carry replacement assertions and collected counts (V1:4035-4055); V2 adds the adjudicated gates G17-G27 (V2:4482-4492). |

### High-severity content points (all 42)

| Point | Winner | Confidence | Evidence (<= 2 sentences) |
|---|---|---|---|
| C-001 | V2 | 75% | Same as X-001. |
| C-002 | V2 | 80% | V2's 24 research files cover collaboration, process redesign, run record/cost, eval governance and the defect register (V2:5, V2:126; C-002 rows). |
| C-003 | BOTH | 60% | Both counts verified (V1 145: 15/66/64; V2 148: 24/93/31) under different Critical rules (V1:581-583; V2:1121); carry both with their rule. |
| C-004 | V2 | 75% | Same as S-007. |
| C-005 | V2 | 65% | Same as X-038. |
| C-007 | BOTH | 70% | V2 SC-21..SC-33 (V2:1197-1209) and V1 SC-18..SC-22 plus the SC-6/SC-10/SC-14 pass rules (V1:531-547) are complementary. |
| C-009 | BOTH | 60% | V2's C8 table covers 10 capabilities (V2:1411-1422); V1's C8 rows add MS-14, ENS-4, ENS-5 (V1:583, V1:767), which V2 lacks. |
| C-011 | V2 | 70% | Same as X-046 and U-020. |
| C-013 | V2 | 75% | V2's 12 evaluation rows incl. G-123 and G-124 one evidence family (V2:1358-1365) vs V1's two rows (V1:644, V1:648). |
| C-016 | V2 | 70% | V2 4.6 consolidates D-1..D-14 and U-1..U-18 (V2:1494-1532); V1 scatters owner items in Notes cells. |
| C-022 | V2 | 70% | V2's 11-row A-vs-B table and six skill-vs-code disagreements (V2:173-197) vs V1's 9-row property table (V1:416-426). |
| C-023 | V2 | 70% | Failure classes by mechanism and the `:313` defect (V2:207-229; re-read line 313). |
| C-026 | V2 | 75% | Re-derived with grades and the `fullpkg()` bug (V2:294-320) vs doc-sourced (V1:191). |
| C-028 | V2 | 85% | Same as S-018. |
| C-029 | V2 | 80% | Same as U-042/U-075; sha256 `044809e3...` (V2:278, V2:322). |
| C-030 | V2 | 60% | V2 read the four scripts and matched sha256 (V2:432-459); V1 read descriptions only (V1:263-269); not checkable here. |
| C-032 | BOTH | 65% | V2's executed probes and 171-row register (V2:545-580); V1's D1-D16 status with "Reflect v2 shares it?" (V1:358-377). |
| C-044 | BOTH | 70% | Different evidence sets (production systems and Zenodo corpus in V1:806-821; benchmarks and aggregation in V2:1620-1684). |
| C-045 | V1 | 70% | V1's full severity research (V1:853-939) vs V2's short treatment (V2:1958-2034). |
| C-046 | V1 | 65% | V1 covers calibration methods (V1:941-1016); V2 has none (Grep "calibrat" = 0 in V2:1538-2137). |
| C-047 | V1 | 65% | V1 covers clustering algorithms and fingerprint tracking (V1:1018-1079); V2 covers location formats only. |
| C-048 | V2 | 75% | Hooks/headless and git ref topics (V2:1698-1911) bear on dispatch read-only and the branch constraint; absent in V1. |
| C-050 | V2 | 65% | Same as X-038. |
| C-051 | V2 | 60% | Two grammars with shared ids, limits, repair and ref list (V2:3637); V1's single contract needs grammar changes (weakness 3). |
| C-052 | BOTH | 60% | Same as CL-03. |
| C-054 | V2 | 60% | Same as X-039. |
| C-060 | OPEN | 55% | Same as X-041. |
| C-061 | V2 | 65% | Same as X-042. |
| C-062 | BOTH | 60% | Same as CL-09: V1's in-place repair plus V2's code-owned helpers. |
| C-069 | V2 | 60% | Consumer-first adapters with per-consumer conditions (V2:3520-3521, V2:3842-3849); keep V1's X1-X14 exposure list (U-102) as the exposure index. |
| C-071 | V2 | 70% | Same as CL-12. |
| C-072 | V2 | 85% | Same as CL-11. |
| C-076 | V2 | 65% | Same as X-051. |
| C-078 | V2 | 60% | Same as X-055. |
| C-079 | V2 | 65% | Same as X-046. |
| C-084 | V1 | 60% | Same as X-054. |
| C-088 | V2 | 60% | Same as X-059. |
| C-089 | V2 | 55% | V2's lens-level first step with a replay oracle (A-17, V2:3668) is narrower and testable; V1's coverage modes (X14, V1:2976) stay a reserved exposure. |
| C-090 | V2 | 65% | Same as X-042. |
| C-091 | V2 | 85% | Same as CL-11. |
| C-092 | V2 | 65% | V2's three-tier acceptance with independence (V2 axis 9, V2:3644); keep V1's portable benchmark gate G-bench (V1:4054). |
| C-095 | V2 | 70% | V2's I-1..I-9 and C1-C29 with layout traps (V2:3754-3764, V2:4430-4458) vs V1's 13 kept rows (V1:3058-3070). |

### Inherited points and exceptions

All Medium and Low S and C points, and the promoted A points (answered separately below), inherit the verdict of their cluster in the cluster table. Exceptions, where the evidence points the other way from the cluster verdict:

- C-010 (CL-09): V1, 65%. ENS-1..ENS-9 incl. `REPORT.md` and the verdict matrix never produced (V1:652-660); verified: `sc-tasklist-protocol/SKILL.md:1155,1171,1175` names `REPORT.md`, and neither `ensemble.py` nor `runner.py` writes one.
- C-018 (CL-09): V1, 65%. The adversarial protocol has no `merge_method` (MS-24, V1:651); verified: `merge_method` has 0 hits under `src/superclaude/skills/sc-adversarial-protocol`.
- C-033 (CL-22): V1, 60%. V1's test totals reproduce (651 and 353 collected, re-run); V1's "37 files" (V1:381) is off by one (38).
- C-038 (CL-06): BOTH, 60%. V1's S-ID probes (V1:167) and V2's re-derived collapse figures (V2:640-653) are different evidence.
- C-039 (CL-22): V1, 60%. V1's Tier 2 prevalence recount (38 of 39, 35 of 39; V1:164, V1:2821) is a counted figure V2 left unrecounted (V2 OQ-15, V2:1039).
- C-043 (CL-13): V1, 60%. The judge brief carries the combo name, which encodes model names (V1:208; analyst verified `judge-one.sh:21` at the tip).
- C-056 (CL-04): V1, 60%. Calibration as a decision with a class-disjoint calibrator (V1 C-06, V1:1602) is a real design question V2 does not axis.
- C-073 and C-093 (CL-14): V1, 70%. Panel size and Tier 2 cost with owner-gated D-1 (V1:2107-2117, V1:2832).
- C-096 (CL-20): V2, 65%. The owner has decided branch naming; V1's five layouts (V1:4057-4069) are dropped and only the git constraint stays.
- S-039 (CL-17): V1, 60%. V1's 6.D defect table with "tests that must change" (V1:2517-2538) has no V2 equivalent inside Section 6.
- C-014 (CL-10): BOTH, 60%. V1's BL-16/BL-17/BL-19 PR router divergences (V1:620-623) are absent from V2; V2's G-100..G-106 constraints are absent from V1.
- C-017 (CL-09): V2, 55%, on substance (the 0.75 vs 0.80 conflict is real: `SKILL.md:703` vs `contract.py:321`, re-read), but V2's SC-17 (V2:1193) must be aligned with its delta row (V2:1137).

## Shared assumption responses

| A-id | Response | Reason with evidence |
|---|---|---|
| A-002 | ACCEPT | Re-run: `git diff --stat 792cf8c52 50d4d2b9d -- src tests scripts` and `git diff --stat 50d4d2b9d HEAD -- src tests scripts` are both empty at HEAD `ad8f57560`, so code facts cited at either HEAD hold today; spot re-reads agree (`findings.py:104,188-192`, `ledger.py:128-136`, `panel.py:509,519`, `contract.py:321`, `reflect_shadow_exit.py:313`). |
| A-006 | ACCEPT | The namespaces collide and a merge will conflate them unless re-keyed: V1 "G-20" is a log row (V1:528) while V2 G-20 is a gap (V2:1255); V1 D1-D16 are hand-off defects (V1:492) while V2 has D-1..D-14 decision groups (V2:1492), D-n defect labels (V2 2.5, V2:549) and D1-D26 dependency facts (V2:4498-4525); V1 G1-G11 are gates (V1:4035-4047) while V2 G-01..G-148 are gaps and G1-G27 are gates. Prefix every id with V1-/V2- or re-key. |
| A-008 | QUALIFY | An unwired named capability is a defect of today's code in both reports, but Critical should depend on whether an on-record deferral exists: the skill's "rejected until Stage 3" is a staging statement (V2 G-21, V2:1256), and after adjudication V2's own delta row records the deferral (V2:1144). Rate the code fact as a defect and the plan priority by the adjudicated scope. |
| A-012 | ACCEPT | V1's "94 open rows, none Critical, 30 Important" is V1's own GQ log (V1:101); V2's 555 rows are a different log with different row kinds (V2:135). Both are internally stated; they are not comparable one to one. |
| A-018 | REJECT | The assumption is false and both reports already reject it: Qwen3.8-max is still listed though owner-excluded, `muse-ember-1.0` is absent, and gateway `launch` is `{}` (V1 2.2, V1:204; V2 2.6, V2:598-615, V2:647; analyst confirmed the tier JSON at HEAD). Dispatch design must not trust the tier file as a serving list. |
| A-019 | QUALIFY | The installed variants are one machine's private state; `superclaude install` neither installs nor removes them (V2 axis 10, V2:3645; U-044), so they show what this owner's machine runs, not what consumers elsewhere see. Use them as design evidence ("port contracts, not scripts"), never as a consumer baseline. |
| A-024 | REJECT | Slice and hand-off counts do not carry over unchanged: V2 corrects several (30/40 vs the hand-offs' 26/40 duplicate resolutions, V2 A-6, V2:3657; "4 flips" vs 3, V2 G-06, V2:1241; the hand-off's 185 prose spawn lines not reproduced, V2 7.2.2 per X-061). V1 used slices as evidence (S-016). |
| A-027 | QUALIFY | V2 adjudicates that the core need not pick one reflect engine now: engine A stays production Tier 2, engine B's data model stays the shadow engine, and the single-engine decision is named with a trigger (V2 axis 8, V2:3643; Q-09). The core serves the spec loop (v1) and reflect/PR (v2) through the thin contract, so "the core must pick one" is not a precondition. |
| A-036 | ACCEPT | Same evidence as A-002; the plan should still re-read line numbers before editing, because both reports quote lines taken from research files. |
| A-037 | QUALIFY | `6c09843` is the better of the two pins (descendant of `4a22d74`, 4 more commits, re-run), but neither is current: `e2f2ac268` is 7 commits after `6c09843` (re-run), and the owner will fold the newest tasklist-branch commits in later. The merged document should say "E2 as of `6c09843`" and list V2's [POST-BASELINE] items (Q-39). |
| A-038 | ACCEPT | Re-run: `uv run pytest --collect-only -qq -p no:cacheprovider tests/review` = 651 tests collected; there are 380 `def test_` functions in 19 files, so 651 is the collected (parametrized) count, as V1 says. |
| A-041 | QUALIFY | 13 of 20 and EV-1 8 of 13 come from the exit script both reports ran at identical code (V1:99; V2 G7, V2:4472); "6 of 9 collapse" rests only on `PLAN.md:66-69` because the logs are gone (analyst check), and V2 re-derives 1 of 3 and 0 of 12 instead (C-038). Valid for the exit script; "6 of 9" stays doc-sourced. |
| A-052 | QUALIFY | Partial winners are usable as defaults only with their conditions and open HIGH invariants attached: V2 states conditions per choice (V2:3654-3671) and carries 60 HIGH invariants (V2 7.3); V1 carries 26 (V1:2620). Narrow tiebreaker wins (C-08 0.13 percent, X-13 0.94, X-14 0.97; V2:3661-3670) must be marked as such, and each plan step that rests on one must name the invariants it leaves open. |
| A-055 | QUALIFY | Both read E2 through `git show` without modifying it (V1 M1-17, V1:3850; V2 D19, V2:4518), but the two pins give the same facts only for files that did not change: `COMBO-REPORT.md` is identical at both commits (analyst check), while collaboration and process-redesign paths are 3 vs 1,145 (C-001). |
| A-056 | REJECT | V2 itself lists 8 CORE inventory rows that contradict Section 7 and says 40 more keyword matches were not re-judged (V2 8.1.2, V2:4300-4314); V1's agreement holds only by construction against a design whose four debates are `partial` (V1:3117, V1:2620). The merge must re-check every destination against the merged architecture. |
| A-057 | REJECT | False at HEAD (re-read `findings.py:104,188-192`, `ledger.py:128-136`, `findings.py:349`): the v1 parser rejects the line before `annotate`; `KeyError` only on a direct `annotate` call. V1 is right; V2's G-01, G-99, SC-01, 6.1, axis 1 option D, axis 2 evidence, C-2 and D9 must be corrected. |
| A-058 | REJECT | Cross-report ids are not comparable: V1 C-05 is who decides blocking, V2 C-05 is consumer entry; V1 Q-47 is panel-size Decision D-1 (V1:4372), V2 Q-47 is C-01 details; V1 G-gates vs V2 G-gaps and G-gates (A-006). Every id needs a report prefix or a new key. |
| A-059 | REJECT | The units differ: V1's 698 inventory items are consolidated from slices and research files, V2's 5,950 are one row per ledger row plus 171 register rows (diff-analysis Partial D table); V1's 19 gates include collected-count suites, V2's 27 include unbuilt measurement gates; V1's 61 Q rows sit over 94 log gaps, V2's 93 over 555 rows. Do not compare the counts. |

## U-register verdicts

### High-value V1 contributions (all 20)

| U-id | Variant | Verdict | Reason |
|---|---|---|---|
| U-001 | V1 | KEEP | True: `unauthorized_deviation_present` is consumed by `contract.py:371,414` and listed in `panel_lint.py:119`, while engine A only copies `adversarial_result.unauthorized_deviation_present`, default `False` (`ensemble.py:104,451-452`); no rule sets it (re-run Grep). A plan needs the producer rule and SC-18 (V1:543). |
| U-002 | V1 | KEEP | True for the source copy: `merge_method` has 0 hits under `src/superclaude/skills/sc-adversarial-protocol` (re-run Grep); the installed copy was not read (`.claude/` excluded). It decides who writes `merged-verdict.yaml`, which V2's code-owned helper (axis 8, V2:3643) must also answer. |
| U-003 | V1 | KEEP | True: `sc-tasklist-protocol/SKILL.md:1155,1171,1175` require `REPORT.md`; `ensemble.py` and `runner.py` have no `REPORT.md` (re-run Grep). A blocking gate's missing output is a plan item (SC-21, V1:546). |
| U-005 | V1 | QUALIFY | Useful as a routing column (gap to destination), but M1-M4 are V1's track grouping; keep the tag as "destination module", re-derived against the merged architecture and not as an order. |
| U-010 | V1 | QUALIFY | SC-10 (measurement precondition with a proposed default, V1:535) and SC-14 (stub lens per consumer shape, V1:539) are needed; SC-6's single-clusterer pass rule (V1:531) applies to the v2 engine's chain guard only under the merged two-engine shape. |
| U-058 | V1 | KEEP | D1-D16 status against current code with "Reflect v2 shares it?" (V1 2.4, V1:358-377) is the compact defect-to-engine map V2's 171-row register lacks in Section 2. |
| U-064 | V1 | KEEP | External severity research (V1 5.2, V1:853-939) bears on module label maps and the PR five-tier mapping; V2 has a short version only (C-045). |
| U-065 | V1 | KEEP | Clustering and fingerprint research incl. complete-link and black-hole threshold (V1 5.4, V1:1018-1079) bears on the v2 chain guard and the convergence trigger T-c. |
| U-066 | V1 | KEEP | Calibration-method research (V1 5.3, V1:941-1016); V2 has none (C-046) and the calibrator stays a component of engine B. |
| U-068 | V1 | QUALIFY | Option lists (V1:842-851, 929-939, 1007-1016, 1068-1079, 1143-1151) are options, not decisions; keep as a reference appendix tagged [external context]. |
| U-086 | V1 | KEEP | Panel size and Tier 2 cost with the recount (38 of 39; flag decisive in 0 certain, at most 1) and owner-gated D-1 (V1:2107, V1:2117, V1:2821); V2 has no axis (C-073). The owner decision must survive. |
| U-087 | V1 | KEEP | D1-D16 with file:line, fix and tests that must change (V1 6.D, V1:2517-2538) is the test-edit list a plan needs; re-map each fix to the engine that owns it under the merged shape. |
| U-088 | V1 | QUALIFY | 6.E debate detail (V1:2624-2807) is implementer-grade, but rows tied to designs the merged shape does not adopt (e.g. the `<adapter>:<argument>` launch grammar, C03-05, V1:2776) must be tagged conditional. |
| U-096 | V1 | QUALIFY | The 48 steps with Files and Closes-gaps (V1:3826-3908) are the best migration content in either report, but steps built on V1-only outcomes (single contract, one clusterer M1-06, dispatcher adapters M1-09/10, claim truncation M1-02) conflict with V2's adjudicated outcomes; keep them as per-item migration content re-checked against the merged architecture, not as an ordered list. |
| U-097 | V1 | KEEP | Per-gate replacement assertions (V1:4037-4047) are what a no-regression gate needs; assertions that follow a V1-only design (e.g. `:117` claim truncation, `blocking_effective`) are marked conditional on that owner decision. |
| U-098 | V1 | KEEP | Verified: 651 and 353 collected (re-run); the exact commands and `--ignore` lists (V1:4045, V1:4048-4050) make the gates runnable. |
| U-099 | V1 | DROP | The five branch layouts (V1:4057-4069) are a branch plan; the owner has decided `feat_review-panel/<name>` and excluded branch plans. Keep only the git constraint sentence (V1:4059), which V2 C4 (V2:4433) states with observed output. |
| U-100 | V1 | KEEP | Persisted-format and rollback rules (schema strings kept, new keys optional, reload tests, re-validation of the 13 recorded shadow manifests; V1 M1 intro, V1:3830; M1-12, V1:3845) are no-regression constraints; V2 has none (Grep "rollback" = 0). |
| U-101 | V1 | QUALIFY | The gap-to-step coverage table (V1:3910-4030) is needed as a coverage check, but must be rebuilt over the merged gap list and merged destinations. |
| U-102 | V1 | KEEP | Exposure list X1-X14 with blocker file:line and change needed, incl. X14 coverage mode (V1 7.2, V1:2984-3006), complements V2's per-consumer verdicts and M1-M14 (V2:3785-3849). |

### High-value V2 contributions at risk in a merge

These V2 rows are true and needed but could be lost or distorted:

- **U-110 and U-111 (inventory and its conflict record)**: at risk because the 5,950 rows live in `synth-08-value-inventory.md` (2,024,775 bytes), not in the report (S-048). The merge must carry the file as a named input and re-check the 8 contradicting CORE rows plus the 40 un-judged matches (V2:4300-4314).
- **U-042 and U-075 (E1 and E2 are one evidence family)**: at risk if the merge keeps V1's evaluation text, which counts E1 and E2 as separate support. This changes what acceptance can claim.
- **U-021, U-022, U-040, U-117 (collaboration and process redesign)**: at risk if V1 is used as the base; V1 has no slot for them. They also carry a [POST-BASELINE] caveat (`e2f2ac268`).
- **U-018 (precedence delta table)**: at risk of becoming stale if the merge rewrites Sections 3 and 4; better to fold the governing cells into the merged Section 3 and keep the table as a change record.
- **U-046 (executed probes)**: at risk of being dropped wholesale because probe P-a's `KeyError` is over-claimed; keep it with the corrected scope (a direct `annotate` call or a switch to the v2 parser).
- **U-047 (171-row defect register)**: at risk because the register lives in research file R17; carry it as a named input with owner buckets.
- **U-115 and U-072/U-073 (15 debates, 244 invariants, INV-A..N)**: at risk by size; keep the per-choice conditions and the 60 HIGH invariants as open questions, the full 7.3 table by pointer.
- **U-112, U-113, U-114 (constraints C1-C29, dependency facts D1-D26, acceptance AE-1..AE-15)**: low risk on content, but their ids collide with V1's ids (A-006) and with V2's own G/D families; re-key.
- **U-118 (owner items Q-35, Q-39, Q-40, Q-90..Q-93)**: at risk if merged into V1's Q list without the [POST-BASELINE] and "one core" reading questions.
- **U-077 and U-049 (repo-constraint conflicts, layout traps)**: low risk, but the `verify-sync` pre-commit correction (`CLAUDE.md:31` vs `.pre-commit-config.yaml:117`) must survive.

## Merge-critical content

**Must survive the merge (by source).**

- From V2: the baseline section with HEAD and the E2 tip (V2:104-120) plus the [POST-BASELINE] list (`e2f2ac268`, Q-39); the precedence rule "Section 7 governs" (V2:120, V2:1125); the collaboration and process-redesign facts, options and dormant outcomes with triggers (V2 2.3, 6.6, 6.7, axes 6-7, A-18, A-19); E1/E2 one evidence family and three-tier acceptance (V2 axis 9, A-11, A-20); the ledger and verdict design of axis 4 (V2:3639) incl. U-020 defects; the dispatch read-only gate (V2 axis 5, A-7); constraints C1-C29, dependency facts D1-D26, acceptance AE-1..AE-15 (V2:4430-4549); the per-consumer verdicts (V2 7.2.4); the 171-row defect register and 5,950-row inventory as named inputs; the 15 debate outcomes with their conditions and the 60 open HIGH invariants; Q-01..Q-93.
- From V1: U-001, U-002, U-003 (post-gate and contract-writer defects); the fix-in-place of the post gate (V1 C-17) as the default for X-043/X-054; the panel-size and Tier 2 cost decision with D-1 (V1 C-14); the calibration decision facts (V1 C-06); the 6.D defect-to-test table and 6.E detail; SC-18..SC-22 and the SC-6, SC-10, SC-14 pass rules; the gate list with commands, collected counts and replacement assertions (V1 8.3); persisted-format and rollback rules; the gap-to-step coverage check (rebuilt); the X1-X14 exposure list; the Section 5 severity, calibration and clustering research; the judge-sees-combo-name fact; owner items O-1..O-6 incl. issues #525-#530.
- Neither report's branch layouts, risk register or schedule (owner decision). The git constraint stays, in V2's observed form (V2 C4, V2:4433).

**Corrections to apply.**

| # | Report | Where | Wrong | Correct (evidence) |
|---|---|---|---|---|
| 1 | V2 | G-01 (V2:1236), SC-01 (V2:1177), G-99 (V2:1334), 6.1 Shared facts (V2:2177), CO-1, axis 1 option D (V2:3636), axis 2 evidence (V2:3637), C-2 (V2:3882), D9 (V2:4508) | a v2 citation-only finding raises `KeyError: 'anchor'` on the ledger path | rejected by v1 `parse_block` at `findings.py:104`, skipped at `:188-192`; `annotate` (`ledger.py:136`) never sees it; `KeyError` (`findings.py:349`) only on a direct `annotate` call or a switch to the v2 parser |
| 2 | V2 | 2.9.3 row 12 (V2:891), OQ-09 (V2:1033), RE-4 | calibrator 6 vs 5 dimensions [UNVERIFIED] | [CODE-VERIFIED]: `confidence-calibrator.md:3` "6-dimension"; `sc-reflect-protocol/SKILL.md:1262,1835` "5-dimension" |
| 3 | V2 | G-133 (V2:1368), 7.1 element 2 | "195 of 1,398 multi-member rows are chains" | 1,398 is all ledger rows; `audit2.py` counts `rows_total` before the `< 3` filter (`git show 6c09843`) |
| 4 | V2 | 2.1 shadow-exit table (V2:215) | pilot 0.704 is "first-parse" compliance | mixed definitions: the first-parse wording entered with `9874d63fb` |
| 5 | V2 | 2.1 (V2:216), 2.9.1 row 5 (V2:874) | `cluster_agreement` 1.000 over 9 runs | add shadow09's 0.9328 (in `clusters.json`, not in the unparseable contract) |
| 6 | V2 | G-06 (V2:1241) | Important | Critical under V2's own rubric (3 verdicts flipped FAIL to PASS is fail-open, V2:1121) |
| 7 | V2 | V2:1335, 2973, 3735, 3804, 4479, 4593 | "50 test files" under `tests/pr_submit` | 47 `test_*.py` (49 `.py` incl. `conftest.py` and `__init__.py`), as V2:3797 says |
| 8 | V2 | G-96 (V2:1331) | `sc-reflect-protocol/SKILL.md` "(6)" | 5 lines, 7 occurrences of `superclaude review` |
| 9 | V2 | SC-17 (V2:1193); G-85 (V2:1320) and 3.5 (V2:1227); SC-04 (V2:1180); 2.9 OQ-01 (V2:1025) | stale "decision"/"open" wording | align with the delta rows V2:1137, V2:1132, V2:1138 and with 2.4's verified E3i reads (V2:432-448) |
| 10 | V1 | Qwen (V1:204) | "timed out 3 of 3 slots" | "timed out on 3 of 4 runs" (`SPEC.md:3` at the tip) |
| 11 | V1 | audit D (V1:201, V1:470) | "3 plus a merge that lost two blocking findings" | 3 flips, of which the third is the F1+F2 merge, plus 5 total-loss merges |
| 12 | V1 | BL-12 (V1:616), DOC-54 (V1:716), 7.1.4 (V1:2976) | "43 spawning call sites in 11 skill files" | 52 `subagent_type: rf-*` lines in 11 files, 44 of them in 8 `SKILL.md` files; prose spawn lines are a separate count |
| 13 | V1 | MS-13 (V1:640), ENS-7 (V1:658), 2.5 (V1:420) | 33 keys, 11 outside the lists (unit unstated) | 32 literal keys (`ensemble.py:787-832`) plus the conditional `t2_fallback` (`:833-834`); 10 outside both frozen lists for the literal |
| 14 | V1 | 2.4 test surface (V1:381) | `tests/cli/reflect` "37 files" | 38 `test_*.py` (V1:4045 says 38); 353 collected is right |
| 15 | V1 | Rationale 4 (V1:2830), C-04 (V1:1443), C-12 (V1:1986), C-17 (V1:2314) | DECIDED-BY-EVIDENCE | decided by evidence only for the code facts; the design choices are owner or debate decisions (X-052) |
| 16 | V1 | C-01 (V1:2839), constraint row (V1:3065) | findings-v1 accepted as a strict subset of findings-v2 | false at HEAD: `findings_v2.py:96-97` rejects `calibrated_confidence`, `:279-281` rejects `prior` lines |
| 17 | Both | id families | C-nn, Q-nn, G-nn, D-nn, A-n collide (A-006, A-058) | prefix every id with V1-/V2- or re-key in the merge |
| 18 | Both | E2 baseline | `4a22d74` (V1) or `6c09843` (V2) as "the" E2 state | "E2 as of `6c09843`"; `e2f2ac268` is 7 commits newer and not read by either report |

## Fact re-derivations you performed

All read-only, at HEAD `ad8f57560` of this worktree unless stated. One batched script (15 checks, `BATCH_OK failures=0`) plus four individual calls.

| # | What I checked | Command or file | Result | Which report was right |
|---|---|---|---|---|
| 1 | Citation-only finding on the ledger path | Read `findings.py:100-121, 184-196, 344-350`; `ledger.py:124-140` | `_check_flat(obj.get("anchor"), "anchor", 12, 200)` rejects; `parse_block` records the error and `continue`s; `merge_round` annotates only `parsed["findings"]`; `annotate` indexes `finding["anchor"]` | V1 (X-020, X-049, X-053, A-057) |
| 2 | Soft distinctness default | `grep -n strict_distinct panel.py` | `:509`, `:575` default `False`; `:519` hard set only with strict | Both describe today correctly (X-041, X-057) |
| 3 | E2 pins and newer commit | `git rev-list --count 4a22d74..6c09843`; `git merge-base --is-ancestor`; `git cat-file -t e2f2ac268`; `git rev-list --count 6c09843..e2f2ac268`; `git log -1 e2f2ac268` | 4; ancestor; commit; 7; 2026-11-14 19:19:40 "counted results, replicates and write-up for the five collaboration designs" | V2 reads the newer pin; both are stale against `e2f2ac268`, which only V2 names (X-001, X-062, A-037) |
| 4 | Code identity across HEADs | `git diff --stat 792cf8c52 50d4d2b9d -- src tests scripts`; same for `50d4d2b9d HEAD` | both empty | Both (X-063, A-002, A-036) |
| 5 | rf-* spawn census | `grep -rEn 'subagent_type: *"?rf-' src/superclaude/skills` lines and files | 52 lines, 11 files | V2 (X-022, X-029, X-061) |
| 6 | Calibrator rubric | `grep dimension confidence-calibrator.md`; `grep 5-dimension sc-reflect-protocol/SKILL.md` | `:3` "6-dimension"; `:1262`, `:1835` "5-dimension" | V1 (X-030, X-048) |
| 7 | Convergence threshold | `grep 0.75 sc-reflect-protocol/SKILL.md`; `grep 0.80 contract.py` | `SKILL.md:703` "≥0.75 PASS, ≥0.60 PARTIAL"; `contract.py:321` `_score_f < 0.80` | V2 flags the conflict (U-121); both state the 0.80 code value |
| 8 | Qwen timeouts | `git show 6c09843:.../combos/SPEC.md` line 3 | "timed out twice (2 x 3000s) on 3 of 4 runs" | V2 (X-025) |
| 9 | What 1,398 counts | `git show 6c09843:.../audit-D/audit2.py` lines 136-147 | `rows_total += 1` before `if len(mem) < 3: continue` | V1 (X-021) |
| 10 | `superclaude review` in reflect skill | `grep -c` and `grep -o ... | wc -l` | 5 lines, 7 occurrences | Neither matches V2's "(6)" (X-017) |
| 11 | Exit-script baseline defect | `sed -n '305,318p' scripts/reflect_shadow_exit.py` | `:313` `if (s_rate or 0.0) > (l_rate or 0.0):` | V2 (U-037) |
| 12 | `tests/review` size | `grep -c def test_` over `tests/review/*.py`; `ls tests/review/test_*.py`; `uv run pytest --collect-only -qq -p no:cacheprovider tests/review` | 380 functions, 19 files, 651 collected | V1's 651 is the collected count (A-038) |
| 13 | `tests/cli/reflect` size | `ls tests/cli/reflect/test_*.py`; `uv run pytest --collect-only ... tests/cli/reflect` | 38 files, 353 collected | V1's 353 right, its "37 files" (V1:381) wrong; V2's 352 passed + 1 xpassed agrees |
| 14 | `tests/pr_submit` size | `ls tests/pr_submit/test_*.py`; `ls tests/pr_submit/*.py` | 47; 49 | V2's "50 test files" wrong (V2:3797's 47 right) |
| 15 | Branch refs | `git branch -a --list '*review-panel*'`, `'*integration*'` | only `ironbelly/eval-tasklist-review-panel` (local and origin); no `integration`, only `origin/346Claude-integration` and `origin/346GPT-integration` | V2 (C4 and C9 statements, V2:4433, V2:4438) |
| 16 | `verify-sync` in pre-commit | `grep -n verify-sync .pre-commit-config.yaml` | `:117` comment: pre-commit "must not require" it; `:132` "continues to run `make verify-sync`" elsewhere | V2's correction of `CLAUDE.md:31` (C5, V2:4434) |
| 17 | v1 as a strict subset of v2 | `grep -n 'calibrated_confidence\|prior' findings_v2.py findings.py` | `findings_v2.py:4` docstring, `:96-97` rejects `calibrated_confidence`, `:279-281` rejects `prior` lines; `findings.py:175-186` accepts `prior` | V2 (axis 2, V2:3637); V1's "strict subset" (V1:2839) false today, as V1's own Cons row warns (V1:1211) |
| 18 | `unauthorized_deviation_present` producer | `grep -rn --include=*.py` over `src/superclaude/cli` | consumed at `contract.py:371,414`, listed `panel_lint.py:119`; engine A only copies `adversarial_result`'s default `False` (`ensemble.py:104,451-452`) | V1 (U-001) |
| 19 | `merge_method` in the adversarial protocol | `grep -rc merge_method src/superclaude/skills/sc-adversarial-protocol` | 0 | V1 for the source copy (U-002); installed copy not read |
| 20 | `REPORT.md` producer | `grep REPORT.md` in `ensemble.py`, `runner.py`, `sc-tasklist-protocol/SKILL.md` | named at `SKILL.md:1155,1171,1175`; no hit in `ensemble.py` or `runner.py` | V1 (U-003) |

Not checked: anything under `~/.claude/` or `.claude/` (X-034, U-044, the installed adversarial copy); external web claims (X-035 to X-037 rest on knowledge or the reports' own sources); V1's 48 steps row by row; V2's 7.3 invariant rows beyond those cited.

## Self-assessed strongest and weakest cluster for V2

V2's strongest cluster is CL-11 (E2 collaboration and process redesign, 85%): V1 has no content there at all, V2 reads the r1-r5 packages and the two brainstorms at the newer pin, gives options and adjudicated dormant-by-default outcomes with build and enable triggers, and names the newer commit that may change the premise; with CL-16 (baseline) and CL-13 (evidence independence) it is the part of V2 a merge cannot do without. V2's weakest cluster is CL-18 (fact disputes, V1 60%): V2 repeated a wrong `KeyError` claim in nine places and used it as evidence for an adjudicated choice, tagged a true calibrator fact [UNVERIFIED], and mis-described the 1,398 and 0.704 figures, while V1 got those facts right; close behind are CL-09 (V2 leaves Critical post-gate defects in production) and CL-20 (V2's Section 8 lacks the replacement assertions, rollback rules and gap-to-step map that V1 supplies).
