# Round 1 Statement: Advocate for Variant 1 (run 1 research report)

- Debate: /sc:adversarial Mode A, depth standard, Round 1
- Variant 1 (V1) = `adversarial/variant-1-original.md` (run 1, 4,476 lines). Variant 2 (V2) = `adversarial/variant-2-original.md` (run 2, 5,098 lines).
- Inputs read in full: `diff-analysis.md` (730 lines), `debate-points.md` (189 lines), `partials/orchestrator-verification.md`.
- Citation form: `V1:L` / `V2:L` = line in the variant file; ids from `diff-analysis.md` are written bare (S-nnn, C-nnn, X-nnn, A-nnn, U-nnn); ids that exist inside a report are prefixed "V1" or "V2" (for example "V1 C-05").
- Read-only: no repo file changed except this one; no git write; nothing under `.claude/` read.

## Position

V1 is the stronger base for the parts a later `/sc:workflow` plan executes against: verified code facts (it is right on the `KeyError` path, the 1,398 unit, the calibrator 5-vs-6 mismatch and `ensemble.py` provenance where V2 is wrong or unverified), an implementer-grade no-regression gate list with per-test replacement assertions and collected counts, persisted-format and rollback rules, a gap-to-step map, and the decisions V2 never treats (panel size and cost, calibration, clustering). V2 is the stronger base for scope, evidence independence, adjudication and plan constraints (E2 collaboration and process redesign, E1/E2 one evidence family, 15 adjudicated debates, 29 binding constraints, 26 dependency facts, 15 acceptance conditions), so the truest merged document takes V2's adjudicated design as the governing default and V1's verified facts, gates and implementer detail as mandatory content, with V1's single-core design kept as the recorded convergence target behind V2's triggers T-a/T-b/T-c.

## Steelman of Variant 2

**Overall.** V2 is the more complete and more honest research record. It reads the E2 branch four commits further (tip `6c09843`, which holds 1,145 collaboration/process-redesign paths against 3 at V1's pin, C-001), so it covers work V1 never saw (E2 collaboration designs r1-r5 and the Sweep Sheet / Recipe Ledger brainstorms, V2 2.3 V2:345-412). It refuses to call a design choice "decided by evidence" when no run compares the options (every axis UNDECIDABLE before debate, V2:3004-3018), and it then adjudicated all 15 open slots by debate and folded each winner, its margin, its conditions and its open HIGH invariants into Section 7 (V2 "Choices the evidence cannot decide" V2:3648-3671). It is transparent about its own internal drift: the 16-row precedence table (V2:1125-1144) says exactly which Section 3/4 cells Section 7 withdraws, narrows or replaces. Its Section 8 obeys the "no roadmap" scope more strictly (V2:4236) and still hands a plan the inputs it cannot invent: 29 binding constraints with enforcing test or hook (V2 8.2(a) V2:4430-4458), 26 dependency facts (V2:4498-4525), 15 acceptance conditions with recomputed hashes (V2:4529-4549) and a 5,950-row inventory that reconciles rows in = rows out (V2:4261).

**By cluster (what V2 gets right).**
- CL-01 core shape. The verified facts favour caution: findings-v1 requires an anchor (`findings.py:104`), `cluster_v2` cannot cluster anchor-only findings (V2 axis 1, V2:3636), and a single superset engine would rewrite the pinned v1 parser and ledger path that the loop and E2 tools use. A thin shared contract (id grammar, one limits module, one repair step, `refs_norm`, hash helpers, resolution, run record) captures the duplicated-constant value now, at low risk, with explicit convergence triggers T-a/T-b/T-c (V2:3636). V2 also states honestly that this differs from the owner's wording and asks the owner to confirm (V2 7.0.1, V2:3582, Q-40).
- CL-04/CL-05 blocking and ledger. V2 closes the ledger design instead of leaving a gate open: silence never clears, quorum-gated explicit `prior <lid> resolved`, `pending_new_sha256`, `defer` terminal and counted open, verdict derived on read and never stored (V2 axis 4, V2:3639). It catches two ledger defects V1's gap table lacks (G-14 `defer` rewrites the verdict, G-15 stored verdict stale, V2:1249-1250). Refusing a blind grader in the core is defensible because no decider other than the veto has ground truth and the stoprule integrity check returns `EXIT_OK` on a mismatch (X-039 verification row in diff-analysis). Rejecting a core `Medium` token follows from "Medium has six meanings" (V2:3637).
- CL-06 dispatch. "The core launches nothing" matches the code (`gateway` has `launch: {}`), and V2 adds a verified safety condition V1 lacks: the raw-id `claude -p` lane is not read-only (E2 launcher leaves Bash open, `run-reviewer.sh:48`), so any lane must enforce read-only at process level before PR or rf-qa may use it (V2 axis 5, V2:3640).
- CL-10 consumers. V2's consumer map is twice as deep (14 consumers incl. tasklist T1-T5, `tasklist validate`, `/task`, `/sc:implement`, V2 2.7 V2:659-726) and its future-consumer path (pure converter to `pr_submit.Finding`, report-only first release; rf-qa lens-level first step at the `/task` gate with a replay oracle) changes no pinned PR code (V2 axis 11, V2:3646).
- CL-11, CL-12, CL-13. Collaboration and process redesign are V2-only and adjudicated (V2:3641-3642). V2 read the installed variant scripts and matched 17 of 17 files to the install log by sha256 (U-074). V2's evidence-independence finding is the single most important evaluation fact in either report: E1's input package is byte-identical to E2's designSpec candidate (sha256 `044809e3...`), so E1 and E2 are one derivation set and acceptance needs a hold-out neither used (U-042, U-075; V2 axis 9 V2:3644).
- CL-16, CL-22. V2 does not use scope slices as evidence (V2:108), re-derives E2 headline numbers from committed files and found the `final-table.py` `fullpkg()` prefix bug (C-026), and is right on three E2 counts where V1 is wrong or narrower (Qwen 3 of 4, X-025; audit D 3 flips plus 5 total-loss merges, X-026; `same_defect` both-empty-refs branch, X-031).
- CL-17, CL-19, CL-20, CL-24. A 189-row conflict log, 14 named invariants INV-A..INV-N (U-073), a 244-row invariant table, and a consolidated carry-over (decision groups D-1..D-14, unverified U-1..U-18, V2:1494-1532) are the right shape for a document a planner must not misread.

## Strengths claimed for Variant 1

1. **V1 states the shipped merge path correctly where V2 does not.** V1 Section 4 row BL-04 (V1:608): a citation-only finding "is rejected by the v1 `parse_block` ('anchor must be a string')... `findings.annotate` would raise `KeyError`... only if called directly or if the ledger were switched to the v2 parser"; repeated in 7.2 exposure list (V1:2992) and 7.3 blockers (V1:3019). Re-checked at HEAD by me and by the orchestrator: `findings.py:104` rejects, `parse_block` `continue`s at `:188-192`, `ledger.py:135-136` calls `annotate` only on `parsed["findings"]`. This matters for the plan because V2 uses the false version as **evidence for an adjudicated choice** (V2 axis 2 "Evidence for the adjudicated choice: a v2 citation-only line crashes the v1 ledger path with `KeyError 'anchor'`", V2:3637) and as a dependency fact (V2 8.2(c) D9, V2:4508). X-020, X-049, X-053, A-057.
2. **V1 is right on five more verified facts V2 gets wrong or leaves unverified.** 1,398 counts all rows (V1 DOC-18, V1:680; V1 D6 V1:594; X-021 VERIFIED-V1). The calibrator is a 6-dimension troubleshoot rubric against reflect's 5-dimension claim, tagged [CODE-CONTRADICTED] (V1 2.1 V1:171; V1 C-06 Cons V1:1563; V2 tags it [UNVERIFIED], V2:891, V2:3323; X-030, X-048). `ensemble.py` predates E1 and is master baseline (V1 2.5 V1:414; X-032 VERIFIED-V1). The 0.704 compliance mean mixes first-parse and after-re-ask values (V1 2.1 V1:162; X-027, definition changed in commit `9874d63fb`). The shadow09 `cluster_agreement` 0.9328 exists but never enters the exit script because the contract does not parse (V1 V1:163; X-028, V1 the more complete statement).
3. **V1's no-regression gate list is implementer-grade and V2 has no equivalent.** V1 8.3 (V1:4031-4055) gives 19 gates, each with the exact `uv run pytest ...` command, the collected count (651 + 353 + 178 = 1182; G8 82, G9 271 with its `--ignore` list, G-pr 2258, G-skills 1327) and, per pinned test, the replacement assertion that must change on purpose (for example G1 `test_review_findings.py:113,117` become `ok is True` with a `truncated` entry; G2 `test_review_ledger.py:385` becomes `resolved_check`). I re-collected `tests/review` = 651 and `tests/cli/reflect` = 353 (Fact re-derivations). V2's G1-G16 cite pins without replacement assertions and G17-G27 are mostly "not run / not built" (S-056; V2:4464-4492). U-097, U-098.
4. **Persisted-format compatibility and rollback rules exist only in V1.** Schema strings kept (`review-ledger/1`, `review-panel-manifest/1`, `review-telemetry/1`), new keys optional, reload tests for ledgers and manifests written before each step, re-validation of the 13 recorded shadow manifests (V1 8.2 M1 intro V1:3830, M2 V1:3861, M1-12 V1:3845). V2 has no "rollback" at all (U-100). A no-regression plan cannot skip this.
5. **Every Critical and Important gap has a destination in V1.** Each Section 4 Notes cell starts with `Track: M1|M2|M3|M4|none (drop: reason)`, script-checked (M1 56, M2 21, M3 18, M4 16, none 34 = 145; V1 4.2 V1:756-770), a Critical/Important-by-track table feeds Section 8 (V1 4.3 V1:772-780), and the 8.2 gap-coverage table maps every Critical and Important row to a step id or a DROP reason (V1 V1:3910-4030). U-005, U-017, U-101. V2 has no gap-to-destination map (S-012).
6. **V1 decides topics V2 has no axis for.** Panel size and Tier 2 cost (V1 C-14 V1:1992-2122; Rationale 6 V1:2832; recount 38 of 39 Tier 2, flag decisive in 0 certain / at most 1, coupled edit sites; U-086, U-104, U-108). Calibration as a routing signal, not a decider (V1 C-06 V1:1543-1604; U-089). Per-lens blocking predicate as data (V1 C-16, resolution V1:2251; U-090). The invalid-block unit of loss: keep valid lines, mark the reviewer `partial`, never let an invalid reviewer clear a row (V1 C-15 V1:2184; C-053). One clusterer with complete-link admission and a stated acceptance metric (83 mega-rows must fall, human pair labels #525-#530 confirm; V1 C-12 V1:1988). S-045.
7. **V1 records defects V2 does not.** `unauthorized_deviation_present` is declared in contract 1.8.0 and consumed by `classify_fix` but has no producer (V1 MS-14 V1:641; U-001). The installed `sc-adversarial-protocol` return contract has no `merge_method` and writes no `merged-verdict.yaml`, so EV-1 reads a file the orchestrator writes (V1 MS-24 V1:651, MS-12 V1:639; U-002). The post gate never produces `REPORT.md` or the per-task verdict matrix the tasklist skill names (V1 ENS-4 V1:655; U-003). PR router diverges from its rubric on seven points and `deep=True` agreement never changes severity (V1 BL-16, BL-17 V1:620-621; U-006, U-062). The D1-D16 table with current file:line, fix and tests that must change (V1 6.D V1:2517-2538; U-087, U-058).
8. **V1's external research covers the three topics the core design must decide.** Severity taxonomies and the 5-to-3 collapse non-invertibility (V1 5.2 V1:853-939; U-064), calibration methods and judge bias (V1 5.3 V1:941-1016; U-066), fingerprinting and clustering incl. complete-link and the black-hole threshold (V1 5.4 V1:1018-1079; U-065), each closing with an options list (U-068). V2 Section 5 has 0 "calibrat" hits (C-046) and no clustering-algorithm source (C-047).
9. **V1's severity ratings follow a stated rule more consistently on the verdict-changing rows.** V1 rates D1 (49 blocking findings lost, 3 merged verdicts flipped to PASS) Critical by impact (V1:589). V2's own rubric says "a verdict that fails open" is Critical (V2 3. Target State V2:1121) yet rates the same facts Important (G-06 V2:1241). V1 checks the C8 premise row by row and says where it is unverified (V1 "How the rule is applied" V1:583; D13 "planned modules, not typos" V1:601; D14 premise carried to Q-58 V1:602).
10. **V1 matches the owner's chosen wording.** V1 Recommended approach (V1:2823) is one core plus thin per-consumer modules. V2 states its adjudicated design "differs in one respect" from the owner-approved wording and asks the owner to confirm (V2 7.0.1 V2:3582, Q-40); in V2 the spec-review "module" keeps a whole v1 engine (parser, ledger, clustering), which is not thin (V2 Recommended approach V2:3578).
11. **V1 is internally consistent between its sections.** V1 Sections 3-4 and 7 agree (no override layer is needed; S-007); its inventory destinations are its own Section 7 components (V1 V1:3117-3119; A-056 holds by construction). V2 needs a 16-row override table because Section 7 overturned Sections 3-4 (V2:1125-1144), states that the table "is not a second review of every row" (V2:1125), and its inventory has 8 CORE rows that contradict Section 7 plus 40 not re-judged (V2:4300-4314).
12. **V1 carries runtime and evaluation facts V2 lacks.** Spike S-ID identity probes (self-report matched pin 0 of 3; `message.model` honoured 2 of 3; V1 V1:167; U-060); the judge sees the combo name, which encodes model names (`judge-one.sh:21`, verified by analyst B at the E2 tip; V1 V1:208; U-059).

## Weaknesses identified in Variant 2

(Stated after the steelman; each is a defect a merge must repair, not a reason to drop V2.)

1. **A false code fact is used as decision evidence.** V2 axis 2 cites "a v2 citation-only line crashes the v1 ledger path with `KeyError 'anchor'` (r01 §3 P-a, r17 DR-113, REPRODUCED)" as "Evidence for the adjudicated choice" (V2 7 Rationale V2:3637); the same claim appears in G-01 (V2:1236), G-99 (V2:1334), SC-01 (V2:1177), 6.1 shared facts (V2:2177), CO-1 (V2:3330), 7 contradictions C-2 (V2:3882), the axis-1 option D text (V2:3636) and dependency fact D9 (V2:4508). Code at HEAD shows the line is rejected at `findings.py:104` before `annotate`; V2's own axis 1 (V2:3636) and Appendix B (V2:5085) have the correct form. The probe P-a called `annotate` directly, which is not the merge path. A plan reading D9 would schedule a "crash fix" that is not needed and misjudge the engine-separation benefit.
2. **V2's severity rubric is applied inconsistently.** By its own rubric a verdict that fails open is Critical (V2:1121), but G-06 (3 verdicts flipped FAIL to PASS) is Important (V2:1241). G-24 is Critical for "One dispatch contract ... covering gateway models" (V2:1259) while the adjudicated design says the core launches nothing (V2:1139, V2:3640). G-42/G-43 are C8 Critical (C-009) while axis 8 moves no engine and leaves the post gate as it is (V2:3643). The delta row says the gaps "keep their Critical rating as statements about today's code" (V2:1144), which is honest, but it means a planner cannot read V2's Critical column as "must fix in this plan".
3. **Several true facts are tagged [UNVERIFIED], and some counts do not reproduce.** The calibrator 6-vs-5 mismatch (V2 2.9.3 row 12 V2:891, OQ-09 V2:1033, RE-4 V2:3323; X-030, X-048). The installed-variant facts are "verified" in 2.4 (V2:432-448) and "all UNVERIFIED" in OQ-01 (V2:1025; X-034). "`sc-reflect-protocol/SKILL.md` (6)" reproduces as 5 lines and 7 occurrences (X-017). "195 of 1,398 multi-member rows" mislabels the 1,398 (V2 G-133 V2:1368; X-021).
4. **Two designs in one document.** V2 Sections 3-4 state engine B inside engine A's shell (T-2 V2:1151), one finding model (V2:1161), one dispatch contract (V2:1163); Section 7 overturns all three (V2:1129-1139). Residual mismatches remain after the delta table: SC-17 says "decision, 0.75 or 0.80" (V2:1193) while the delta row says 0.80 is decided by code (V2:1137; C-017); G-85 and 3.5 list DO4 open (V2:1320, V2:1227) while the delta row says decided (V2:1132; X-005); SC-04 says quorum is a "decision" (V2:1180) while A-3 fixes `min(2, requested)` (X-004).
5. **Debate winners are written as governing although they are as weak as V1's "decided" labels.** Of V2's 15 debates, most were decided by tiebreaker inside the 5 percent band (for example C-01 margin 2.45 percent, C-02 1.48, C-08 0.13, X-13 0.94, X-14 0.97; V2:3654-3671), all returned `partial`, and 60 HIGH invariants stay open (V2:3981). In C-05 the tiebreaker selected Variant A although B scored higher (A 0.8728, B 0.8904; V2:3664). V2 is right to carry these as conditions; it is not right to treat them as more settled than V1's evidence-decided rows without saying so in the governing text (V2 "Section 7 governs", V2:1125).
6. **Section 8 hands a planner the constraints but not the test edits.** V2 G1-G16 cite pins without the replacement assertion; G17-G27 are mostly unbuilt (V2:4464-4492). There is no rollback or persisted-format rule (0 "rollback" hits; U-100) and no gap-to-destination map (S-012). A `/sc:workflow` plan must re-derive all three.
7. **Measured clustering defect left in place twice.** V2 keeps two clusterers, one per engine (V2 7.1 V2:3743), and withdraws `cluster_v2` for new ledgers (V2:3511), but transitive union-find over-merge (83 mega-rows, 195 chained rows) is measured on both stacks (V1 D6 V1:594). V2 has no clustering axis and no remedy (C-061, C-090); the spec loop keeps the measured over-merge.
8. **Decisions missing.** No panel-size or Tier 2 cost axis (C-073, C-093), no calibration axis (C-056), no invalid-block policy of its own (C-053), no producer rule for `unauthorized_deviation_present`, no `merge_method` writer gap, no `REPORT.md` gap (strength 7).
9. **"Thin module" is stretched.** V2's spec-review module owns the v1 parser, `ledger.py`, `review-ledger/1` and v1 clustering (V2:3578); this is a second engine under a module label, and V2 itself flags the owner-wording difference (V2:3582).

## Concessions (genuine weaknesses of Variant 1)

1. **Older and narrower E2 evidence.** V1 pins E2 at `4a22d74` (V1:93, V1:2814) and misses the 4 later commits with the collaboration and process-redesign work (C-001, X-001, X-062). Collaboration and process redesign are absent from V1 entirely (0 "collaborat" hits in V1:1-782; C-028, C-072, C-091). V2 is the only source for CL-11.
2. **V1 over-labels design choices as decided by evidence.** "Sixteen of the twenty conflicts are DECIDED-BY-EVIDENCE" (V1 Rationale 4 V1:2830) includes C-01 (core contract), C-04 (distinctness default; "decided by code evidence alone", V1:1443), C-12 (clusterer; V1:1986) and C-17 (fix `ensemble.py`; V1:2316). Code shows the defects; it does not choose between remedies. No run compares core shapes. V2's UNDECIDABLE label is the truer status (X-052, X-041, X-043).
3. **Slice- and hand-off-sourced numbers.** V1 cites scope slices S00-S05 as evidence (V1 citation key V1:108-123) and takes E2 headline numbers from `COMBO-REPORT.md` without re-aggregating (V1:191; C-026, A-024). V2 re-derived them and found the `fullpkg()` prefix bug (U-039).
4. **Wrong or narrower counts.** Qwen "timed out 3 of 3 slots" (V1:204) is 3 of 4 runs (X-025). Audit D "3 plus a merge that lost two blocking findings" (V1:201, V1:470) double-describes the third flip (X-026). "43 spawning call sites in 11 skill files" (V1:410, V1:616, V1:2976) does not reproduce; the pattern gives 52 lines in 11 files, 44 in 8 `SKILL.md` files (X-022, X-029, X-061; re-run here: 52). `same_defect` omits the both-empty-refs branch (V1:305; X-031). Engine-A contract "33 keys" counts the conditional `t2_fallback` without saying so (V1:640, V1:658; X-023).
5. **Under-rated ledger defect and an internal inconsistency.** D2 clearing by silence is Important (V1:590) while D3 is Critical (V1:591); clearing by silence produced a reproduced false PASS (V2 G-12 V2:1247), so V1 should rate it Critical (X-012). V1 Section 4 says the quorum value is an owner decision (V1:528, V1:591) while V1 6.E C13-06 sets `quorum = min(2, panel_size)` (V1:2641; X-004).
6. **Ledger defects missing from V1's gap table.** `defer` rewriting the verdict and the stale stored verdict (V2 G-14, G-15) are not Section 4 rows; V1 has the `defer` defect only as debate invariant INV-001 (V1:2866).
7. **No evidence-independence finding.** V1 never states that E1's package is byte-identical to E2's candidate (U-042, U-075), so its "portable E2-style benchmark" (V1 C-20; G-bench V1:4054) would measure on the same derivation set.
8. **Out-of-scope plan content.** V1 8.4 branch layouts A-E (V1:4057-4069), 8.5 risk register and 8.6 checklist (V1:4075-4120) are a branch plan and planning content; the owner has fixed branch names as `feat_review-panel/<name>` and excluded branch, PR and risk plans from the merged document. Only the git ref constraint (V1:4059) survives.
9. **Missing safety and repo constraints.** V1 has no read-only requirement for a raw-id lane (V2 axis 5 V2:3640), no repository layout traps (`SKILL.md` needed for `verify-sync`, reserved contract names, `lib/` at `.gitignore:13`; U-049, U-112) and no evaluation-governance subsection (S-020).
10. **Weak core-token call on `Medium`.** "`medium` is a first-class tier" (V1 SC-11 V1:536, BL-03 V1:607) ignores that "Medium" has six distinct uses in the repo (V2:3637; X-006).

## Cluster verdicts

| Cluster | Stronger on this topic | Confidence | Evidence (headings + lines) |
|---|---|---|---|
| CL-01 Core shape | MERGE (both needed) | 65% | V2's thin shared contract (V2 7 Recommended approach V2:3578, axis 1 V2:3636) is the evidence-safe first stage; V1's superset core (V1 7 Recommended approach V1:2823, Rationale 1 V1:2827) is the target future consumers need and matches the owner wording. Merge: V2 shape now, V1 shape as the recorded convergence target under V2's triggers T-a/T-b/T-c. |
| CL-02 Finding contract, PR fields | V2 | 60% | A converter on the `pr_submit` side leaves `Finding`, FSM and `REVIEWERS` untouched (V2 axis 2 V2:3637, A-14 V2:3665); V1's lens extensions (V1 BL-18 V1:622, M4-04 V1:3905) widen the contract. Exception: C-053 goes to V1 (explicit invalid-block policy, V1 C-15 V1:2184). |
| CL-03 Over-length lines, claim cut | V1 | 60% | V1 truncates `claim` too (V1 C-02 V1:1315; 7 table V1:2840) and 10 of the 49 lost blocking findings were claim-length (V1 D1 V1:589); `card_convert.py:200-201` already cuts claims to 297 + "..." (re-read). V2 leaves the claim cut unresolved (V2 axis 3 V2:3638). |
| CL-04 Who decides blocking, quorum | V2 | 60% | No decider except the veto has ground truth and the grader's integrity check returns `EXIT_OK` on mismatch (X-039 verification); V2 keeps typed `blocking` plus a CRITICAL floor (V2 A-4 V2:3655) and a concrete quorum refusal (A-3 V2:3654). Both converge on `min(2, ·)` (V1 C13-06 V1:2641). |
| CL-05 Ledger rounds and verdict | V2 | 65% | V2 closes the design (silence never clears, verdict derived on read, `defer` terminal; V2 axis 4 V2:3639) and has G-14/G-15 (V2:1249-1250); V1 leaves a decision gate open (V1 C-13 V1:2052, risk row V1:2866). |
| CL-06 Dispatch, identity, read-only | V2 | 65% | "The core launches nothing" fits the code, and V2 adds the process-level read-only condition for raw-id lanes (V2 axis 5 V2:3640, `run-reviewer.sh:48`). V1 contributes S-ID probes (V1:167) and `panel verify` (V1 C-03 V1:1379). |
| CL-07 Distinctness default | MERGE | 60% | Both remove silence: V2 records `requested_slots` and `distinct_models` with soft default (V2 A-6 V2:3657); V1 declares policy per slot (V1 C-04 V1:1445). V1's "decided by code evidence" overclaims status; V2's availability argument (strict gives 2 reviewers in anthropic-only) is real. |
| CL-08 Run record, telemetry | MERGE | 60% | V2's `events.jsonl` avoids the lock-free manifest race (V2 A-10 V2:3661, D-23); V1's audits A and D as built-in checks before `published` (V1 MS-04 V1:631, C-07 V1:2845) have no V2 counterpart. |
| CL-09 Reflect Tier 2 engines | MERGE | 55% | V2's "no engine moves now" won its strongest debate (C-04, 6.91 percent, V2 A-8 V2:3659); V1's fix-in-place targets verified production defects the post gate has today (V1 ENS-1..ENS-5 V1:652-656, C-17 V1:2855). Plan needs V2's governance and V1's ENS defect list as scope. |
| CL-10 Consumers and entry points | V2 | 60% | V2's 14-consumer map and adjudicated entry (V2 2.7 V2:659-726; A-13 V2:3664) are deeper; V1 adds coverage modes X14 (V1 7.2 V1:2984-3006) and router-vs-rubric points (V1 BL-17 V1:621). Caveat: in C-05 the tiebreaker chose the lower-scored variant (V2:3664). |
| CL-11 E2 collaboration and process redesign | V2 | 90% | V2-only (V2 2.3 V2:345-412; axes 6-7 V2:3641-3642); V1 has 0 "collaborat" hits in V1:1-782 (C-028). |
| CL-12 Installed-only E3 variants | V2 | 70% | V2 read the scripts and matched 17 of 17 files by sha256 (V2 2.4 V2:432-459; axis 10 V2:3645, "port contracts, not scripts"); V1 read descriptions only (V1 2.3 V1:263-269). Caveat X-034. |
| CL-13 Evaluation and evidence independence | V2 | 75% | E1/E2 one evidence family (V2 2.2 V2:278, V2:322) and three-tier acceptance (V2 axis 9 V2:3644); V2 re-derived E2 numbers (C-026). V1 is right on X-021. |
| CL-14 Panel size and cost | V1 | 80% | V1 C-14 recount and owner-gated D-1 (V1 C-14 V1:2107-2117; Rationale 6 V1:2832); V2 has no axis (C-073, C-093). |
| CL-15 Severity ratings, C8 | V1 | 55% | V1 checks the C8 premise per row (V1:583, V1:601-602) and rates the fail-open D1 Critical (V1:589); V2's rubric (V2:1121) contradicts its G-06 rating (V2:1241). V2 is right on X-012 and X-016. |
| CL-16 Evidence baseline | V2 | 70% | V2 reads the later E2 tip, not slices (V2 Baseline V2:108); V1 pinned older (V1:93). Code at both HEADs identical (X-063). |
| CL-17 Section 6 method | V2 | 65% | V2's UNDECIDABLE labels and 189-row log (V2 6.12 V2:3130-3566) are the truer method; V1 over-labels "decided" (V1:2830). V1's 6.E implementer detail (V1:2624-2807) still must survive. |
| CL-18 Fact disputes | V1 | 65% | V1 wins 10 point rows (X-020, X-021, X-027, X-028, X-030, X-032, X-048, X-049, X-053, A-057), V2 wins 6 (X-022, X-025, X-026, X-029, X-031, X-061), 3 reconcile (X-023, X-024, X-050). The V1 wins include the one fact V2 uses as decision evidence (V2:3637). |
| CL-19 Section 7 shape, override layer | V2 | 60% | V2's precedence table (V2:1125-1144), invariants I-1..I-9 and 29 constraints (C-095) are needed in a merged document that has several sections; V1 needed no override only because it ran fewer debates. |
| CL-20 Section 8 form, inventory | MERGE | 75% | Plan needs V1's gates with replacement assertions, rollback rules and gap-to-step map (V1 8.2-8.3 V1:3826-4055) and V2's constraints, dependency facts, acceptance conditions and full inventory (V2 8.2 V2:4430-4549, 8.1 V2:4248-4263). V1 8.4-8.6 dropped (owner scope). |
| CL-21 Sections 1, 3, 4 structure | MERGE | 60% | V1's track tags and detailed SC pass rules (V1 4 V1:761, V1 3 V1:526-548) plus V2's C8 table, 33 SCs and 4.6 carry-over (V2 4.2 V2:1407-1422, 3.3 V2:1171-1209, 4.6 V2:1488-1536). |
| CL-22 Section 2 organisation | V2 | 70% | V2's 9 subsections incl. dispatch, eval governance, repo constraints and executed probes (V2 2.5-2.8 V2:486-826); V1 compact (V1:106-480) but carries D1-D16 status with a v2-shares column (V1 2.4 V1:358-377). |
| CL-23 Section 5 external research | MERGE | 80% | Disjoint source sets: V1 severity, calibration, fingerprinting (V1 5.2-5.4 V1:853-1079); V2 benchmarks, hooks/headless, git refs, finding schemas (V2 5.1-5.4 V2:1620-2036). Both feed the plan. |
| CL-24 Sections 9, 10, ids | V2 | 60% | V2 consolidates carry-over with GQ sources (V2 9 V2:4700) and flags the unread later E2 commit (Q-39); V1 adds owner items O-1..O-6 and issue ids #525-#530 (V1 V1:4136-4141). Ids must be namespaced in the merge (A-006, A-058). |
| CL-25 Section 6 residual | MERGE | 60% | V1's 651-test figure reproduces (A-038, re-run here); citation keys (S-042) need one scheme in the merge. |

Tally: V1 4 (CL-03, CL-14, CL-15, CL-18); V2 13 (CL-02, CL-04, CL-05, CL-06, CL-10, CL-11, CL-12, CL-13, CL-16, CL-17, CL-19, CL-22, CL-24); MERGE 8 (CL-01, CL-07, CL-08, CL-09, CL-20, CL-21, CL-23, CL-25); NEITHER 0; OPEN 0. CL-26 has no points.

## Per-point verdicts

### Contradictions (all 63)

| Point | Winner | Confidence | Evidence (<=2 sentences) |
|---|---|---|---|
| X-001 | V2 | 70% | Both pins exist and are 4 commits apart (orchestrator); V2's `6c09843` holds the collaboration work V1's `4a22d74` lacks (V2:108, V1:93). |
| X-002 | V2 | 55% | Two grammars avoid rewriting the pinned v1 path (V2 delta V2:1134, axis 2 V2:3637); V1's single contract (V1:494) stays the convergence target. |
| X-003 | V2 | 60% | Only the veto has ground truth; V2 keeps typed `blocking` plus CRITICAL floor (V2:1137, A-4 V2:3655); V1's "separate measured decider" (V1 D4 V1:592) is a measurement precondition, not buildable now. |
| X-004 | BOTH | 70% | Both reports end at `min(2, ·)` (V1 6.E C13-06 V1:2641; V2 A-3 V2:3654); each has a stale "decision" sentence elsewhere (V1:528, V1:591; V2 SC-04 V2:1180). |
| X-005 | V2 | 60% | V2 adjudicated reflect UC-1 as the entry (V2:1132, A-13 V2:3664); V1 leaves O-3 open (V1:635). V2's own G-85 and 3.5 still say open, and the tiebreaker chose the lower-scored side. |
| X-006 | V2 | 65% | "Medium" has six meanings in the repo (V2:3637); a core token would fix one meaning (V1 SC-11 V1:536). |
| X-007 | V2 | 60% | A converter computes `in_diff` without touching findings-v2 or `pr_submit.Finding` (V2 delta V2:1141, V2:3735); V1 BL-18 (V1:622) widens the core. |
| X-008 | V2 | 55% | Per-slot `lens` was withdrawn by debate C-11 (V2:1141); V1's optional keys (V1 BL-08 V1:612) are additive and cheap, so the merge can keep them as an option. |
| X-009 | V2 | 65% | `gateway` `launch: {}` and the raw-id lane is not read-only (V2:1139, V2:3640); V1's adapters (V1 MS-06 V1:633) need that safety condition first. |
| X-010 | MERGE | 60% | `events.jsonl` (V2:1142) for the per-run record plus V1's built-in audits before `published` (V1 MS-04 V1:631). |
| X-011 | V1 | 70% | 3 merged verdicts flipped FAIL to PASS is a fail-open verdict, Critical by V2's own rubric (V2:1121); V2 G-06 says Important (V2:1241), V1 D1 Critical (V1:589). |
| X-012 | V2 | 70% | Clearing by silence reproduced a false PASS (V2 G-12 V2:1247); V1 D2 Important (V1:590) is inconsistent with its own D3 Critical. |
| X-013 | V1 | 60% | `lint_cmd`/`estimate_cmd` belong to unmerged experiment branches (V1 D13 V1:601); V2 asserts "named as shipped" (V2:1372) without a driving spec cite. |
| X-014 | V1 | 55% | A manual CLI caller exists (`telemetry_cmd.py:67`); V1 rates Important and carries the C8 premise as UNVERIFIED (V1 SC-12 V1:537), which is the accurate status. |
| X-015 | V1 | 60% | `SKILL.md:87` stages the panel "until Stage 3", so the C8 premise "spec names it as shipped or enabled" is not met for the skill path (V1 MS-08 V1:635); V2 counts #519 as the naming (V2 G-21 V2:1256), which is arguable. |
| X-016 | V2 | 55% | The Stage 2 exit is the rollout gate and the target cannot hold until it passes (V2 G-47 V2:1282); shadow changes no verdict, so Important (V1 MS-12 V1:639) is defensible but weaker. |
| X-017 | V1 | 60% | V1 cites the merge commit `9163bd1c7` and the single prose caller (V1 D14 V1:602); V2's "(6)" count does not reproduce (orchestrator: 5 lines, 7 occurrences). |
| X-018 | V1 | 60% | V2's adjudicated design keeps "the core launches nothing" (V2:1139), so G-24 Critical (V2:1259) rates a gap the governing design does not close. |
| X-019 | OPEN | 50% | G-123 (no acceptance definition) is plausibly Critical; G-36 (input manifest) has an unverified causal link (V1 D8 V1:596). Split per row in the merge. |
| X-020 | V1 | 90% | `findings.py:104` rejects, `:188-192` skips, `ledger.py:135-136` annotates only accepted findings (re-read here). |
| X-021 | V1 | 90% | `audit2.py` increments `rows_total` before the `< 3` filter (orchestrator, `git show 6c09843`). |
| X-022 | V2 | 80% | `grep -rn 'subagent_type: *"\?rf-'` = 52 lines (re-run here); V1's 43 is unreproducible. |
| X-023 | BOTH | 85% | 32 literal keys plus conditional `t2_fallback` = 33 (`ensemble.py:787-834`). |
| X-024 | BOTH | 85% | Same reconciliation; V2 states its basis (110 stable + telemetry lists), V1 does not. |
| X-025 | V2 | 85% | E2 `combos/SPEC.md` line 3: "timed out ... on 3 of 4 runs". |
| X-026 | V2 | 75% | The "merge that lost two blocking findings" is the third flip itself (n5-sonnet-ember F1+F2); V1's final 3 stands but its description double-counts. |
| X-027 | V1 | 75% | Commit `9874d63fb` changed the definition to first-parse; pre-commit values were not first-parse, so "mixed definitions" (V1:162) is accurate. |
| X-028 | V1 | 70% | shadow09 holds 0.9328 but its contract does not parse, so it never reaches the exit script; V2's "all 1.000" omits it (V2:216). |
| X-029 | V2 | 80% | 44 structured lines in 8 `SKILL.md` files reproduce; V1's 43 does not. |
| X-030 | V1 | 90% | `confidence-calibrator.md:3` "6-dimension" vs `sc-reflect-protocol/SKILL.md:1262,1835` "5-dimension" (orchestrator). |
| X-031 | V2 | 85% | `findings.py:367-379` has the `(not ra and not rb)` branch V1 omits. |
| X-032 | V1 | 75% | `git log` of `ensemble.py` (#203-#329) predates E1; #519 touched only `panel_lint.py` in `cli/reflect`. |
| X-033 | V2 | 55% | V2 lists seven rows incl. tasklist skill vs CLI and `/sc:implement` (V2:687-695); V1's five omits them. Definitional. |
| X-034 | NEITHER | 60% | V1 never read the bodies; V2 is internally inconsistent (2.4 vs OQ-01). Not checkable here (`~/.claude/` excluded). |
| X-035 | V2 | 70% | SARIF 2.1.0 §3.27.9 enumerates six `kind` values including `review`; from the published schema as I know it, not fetched in this task. |
| X-036 | OPEN | 50% | Possibly different figures from one paper; neither report is falsified here. |
| X-037 | V2 | 55% | V2 cites official OpenAI docs (V2:1980); V1 found only a blog (V1:878). Not fetched. |
| X-038 | MERGE | 60% | See CL-01: V2 shape now, V1 shape as gated convergence target. |
| X-039 | V2 | 60% | No accuracy data for any grader; stoprule integrity returns `EXIT_OK` on mismatch. V1 keeps the grader shadow-only, so its live behaviour already matches V2. |
| X-040 | V1 | 60% | 10 blocking losses were claim-length (V1:589); a claim cut exists in code already (`card_convert.py:200-201`). V2 leaves it unresolved (V2:3516). |
| X-041 | V2 | 55% | On status: the default is a choice, not code-decided (V1:1443 overclaims); on substance both record repeats. |
| X-042 | V1 | 55% | Chaining is measured on both stacks (V1 D6 V1:594) and V1 gives an acceptance metric (V1:1988); V2 keeps both clusterers with no remedy (V2:3743). V2 is right that the clusterer choice is not evidence-decided. |
| X-043 | V2 | 60% | On status: "fix now vs replace" is a choice (V2 RE-1 V2:3320); V1's DECIDED (V1:2316) overclaims. |
| X-044 | V2 | 55% | `derive_verdict` is 36-test pinned and engine-neutral (V2 A-4 area V2:3639); V1's one machine verdict (V1:2447) needs a contract change reflect forbids without a bump. |
| X-045 | V2 | 65% | Same as X-009. |
| X-046 | V2 | 65% | V2 closes the ledger design; V1 leaves a gate (V1:2052). |
| X-047 | V2 | 60% | Both keep `/sc:reflect` as today's path (0 `t2-engine` hits in workflow/tasklist skills); V2 adjudicated, V1's protocol reference (V1:2536) remains a useful doc artifact. |
| X-048 | V1 | 90% | Same fact as X-030. |
| X-049 | V1 | 90% | Same fact as X-020; V2's own L3511 agrees with V1. |
| X-050 | BOTH | 80% | V1 "no code writes `observed`" is right; V2's "1 of 15 combo contracts" count is right. |
| X-051 | MERGE | 60% | See CL-01. |
| X-052 | V2 | 75% | No run compares core shapes; V1's "DECIDED-BY-EVIDENCE" (V1:2830) overclaims. |
| X-053 | V1 | 90% | Same code as X-020; V2:3882 and V2:4508 must be corrected. |
| X-054 | MERGE | 55% | Governance from V2 (no engine move, helpers as comparison siblings, V2:3643); the verified production defects ENS-1..ENS-5 from V1 (V1:652-656) stay in plan scope as C8 rows. |
| X-055 | V2 | 60% | Same as X-003. |
| X-056 | V1 | 60% | Same as X-040. |
| X-057 | MERGE | 55% | Status quo soft (`panel.py:509,575`); V2 records repeats, V1 declares per slot; both are compatible. |
| X-058 | OPEN | 55% | Both add exit 12 with different meanings (V1 PENDING grader V1:3841; V2 quorum refusal V2:3639); V1 notes an installed variant already uses 12 for CONTINUE (V1:3001). The merge must fix one meaning. |
| X-059 | V2 | 60% | Same as X-007; `in_diff` has 0 hits today. |
| X-060 | V2 | 60% | Same as X-005. |
| X-061 | V2 | 80% | Same as X-022. |
| X-062 | V2 | 70% | Same as X-001. |
| X-063 | BOTH | 90% | `git diff --stat 792cf8c52 50d4d2b9d -- src tests scripts` is empty (orchestrator). |

### High-severity structural (22)

| Point | Winner | Confidence | Evidence |
|---|---|---|---|
| S-004 | MERGE | 60% | V1 conventions, consumer table and core diagram (V1:483-520) plus V2 numbered 3.1-3.5 with precedence (V2:1114-1227). |
| S-007 | V2 | 65% | An override layer is needed once Section 7 adjudications differ from Sections 3-4 (V2:1125-1144). |
| S-011 | MERGE | 55% | V2's flat topical G-ids read better; V1's itemised DOC rows (V1:663-733) carry corrected values a plan needs. |
| S-012 | V1 | 75% | Track tags and the by-track table (V1:761, V1:772-780) tell a plan where each gap lands; V2 has none. |
| S-013 | V2 | 65% | Same as S-007. |
| S-015 | V2 | 70% | Same as X-001. |
| S-016 | V2 | 65% | Not using slices as evidence is cleaner (V2:108); V1 relies on S00-S05 (V1:108-123). |
| S-017 | V2 | 65% | V2 2.1-2.9 covers dispatch, eval, repo rules V1 lacks. |
| S-018 | V2 | 85% | Collaboration subsection exists only in V2 (V2:345-412). |
| S-020 | V2 | 80% | Eval harness, governance and repo constraints only in V2 (V2:730-826). |
| S-022 | MERGE | 60% | V2's classification table and CF/RC/CC tooling (V2:830-1110) plus V1's "same code? / divergent choices" columns (V1:436-461). |
| S-027 | MERGE | 80% | Disjoint Section 5 source sets (CL-23). |
| S-032 | V2 | 60% | Decision axes are the right organising unit for a plan; V1's conflict blocks (V1:1191-2515) hold detail that must survive. |
| S-036 | V2 | 70% | UNDECIDABLE is the truer status (X-052). |
| S-037 | V2 | 70% | 15 debates cover more slots; V1's 4 debates carry deeper 6.E detail (V1:2624-2807). |
| S-038 | V2 | 70% | 189-row log with evidence status (V2:3194-3425). |
| S-045 | MERGE | 75% | Each report has stand-alone decisions the other lacks (calibration, panel size, clustering in V1; collaboration, process, variants, harness owner in V2). |
| S-046 | V2 | 60% | V2's Section 7 carries winners, conditions and 244 invariants (V2:3567-4233); V1's 20-row adopted-resolution table (V1:2837-2858) and 4-row risk table (V1:2862-2867) are compact inputs. |
| S-047 | MERGE | 75% | See CL-20. |
| S-048 | MERGE | 60% | Keep V2's full inventory by pointer (V2:4240) and V1's 698-row items mapped to merged destinations. |
| S-049 | MERGE | 60% | V2's EVAL/HARNESS/KNOWLEDGE destinations plus V1's Effort column and finer core components (V1:3117-3121). |
| S-056 | V1 | 75% | See strength 3. |

### High-severity content (42)

| Point | Winner | Confidence | Evidence |
|---|---|---|---|
| C-001 | V2 | 70% | Same as X-001. |
| C-002 | V2 | 80% | 24 vs 13 research files; V2 covers collaboration, run record, eval governance, defect register (V2:126, V2:1305-1383). |
| C-003 | BOTH | 70% | Both counts verified by awk (145: 15/66/64; 148: 24/93/31); different rubrics. |
| C-004 | V2 | 60% | Two-layer target with stated precedence is honest about overturned cells (V2:1125-1144). |
| C-005 | MERGE | 60% | See CL-01. |
| C-007 | MERGE | 70% | V1-only SC-18, SC-19, SC-21, SC-22 (V1:543-547) and V2-only SC-21..22, SC-26..33 (V2:1197-1209) are all needed. |
| C-009 | V1 | 55% | See CL-15 and X-015. |
| C-011 | V2 | 65% | G-14, G-15, G-133..135 (V2:1249-1250, V2:1368-1370). |
| C-013 | V2 | 70% | 12 evaluation rows incl. G-123, G-124 (V2:1358-1365) vs V1 MS-17 (V1:644). |
| C-016 | V2 | 65% | Consolidated D-1..D-14 and U-1..U-18 (V2:1494-1532). |
| C-022 | V2 | 65% | A-vs-B table and six skill-vs-code disagreements (V2:173-197); V1's 9-row engine table (V1:416-426) is narrower. |
| C-023 | V2 | 65% | Failure classes by cause, `reflect_shadow_exit.py:313` defect (V2:207-229). |
| C-026 | V2 | 75% | Re-derived from files, `fullpkg()` bug found (V2:294-320). |
| C-028 | V2 | 85% | V2-only collaboration evidence (V2:345-412). |
| C-029 | V2 | 85% | sha256 `044809e3...` and `snap.py:4` (V2:278, V2:322). |
| C-030 | V2 | 60% | V2 read the bodies; X-034 caveat. |
| C-032 | MERGE | 65% | V1 D1-D16 with "v2 shares it?" (V1:358-377) plus V2 probes and 171-row register (V2:545-580). |
| C-044 | MERGE | 75% | Production systems and corpus (V1:806-821) plus benchmarks and aggregation (V2:1620-1684). |
| C-045 | V1 | 75% | Full severity research (V1:853-939) vs a brief section (V2:1958-2034). |
| C-046 | V1 | 75% | Calibration methods only in V1 (V1:941-1016). |
| C-047 | V1 | 70% | Clustering-algorithm sources only in V1 (V1:1018-1079). |
| C-048 | V2 | 75% | Hooks/headless and git-ref topics only in V2 (V2:1698-1911). |
| C-050 | MERGE | 60% | See CL-01. |
| C-051 | V2 | 55% | Two grammars with shared ids, limits, repair (V2:3027); V1's single contract as target. |
| C-052 | V1 | 55% | See CL-03; V2's three-field cut plus itemised drop record (V2:3028) should be merged in. |
| C-054 | V2 | 60% | See X-039. |
| C-060 | MERGE | 55% | See CL-07. |
| C-061 | V1 | 55% | See X-042. |
| C-062 | MERGE | 55% | See X-054. |
| C-069 | V2 | 60% | Consumer-first adapters (V2:3040); V1's X1-X14 exposure list (V1:2984-3006) kept as the checklist. |
| C-071 | V2 | 70% | Keep/archive/fold axis only in V2 (V2:2862-2934). |
| C-072 | V2 | 85% | Collaboration and process-redesign axes only in V2. |
| C-076 | MERGE | 60% | See CL-01. |
| C-078 | V2 | 60% | See X-003. |
| C-079 | V2 | 65% | See X-046. |
| C-084 | MERGE | 55% | See X-054. |
| C-088 | V2 | 60% | See X-007. |
| C-089 | V2 | 60% | Lens-level first step with replay oracle (V2:3668); V1's coverage modes (V1:2976) kept as an option. |
| C-090 | V1 | 55% | See X-042. |
| C-091 | V2 | 85% | Same as C-072. |
| C-092 | V2 | 70% | Three-tier acceptance and independence (V2 axis 9 V2:3644). |
| C-095 | V2 | 70% | 29 binding constraints incl. layout traps (V2:4430-4458) vs 13 rows (V1:3058-3070). |

### Inherited verdicts and exceptions

All Low and Medium S and C rows inherit their cluster verdict from the cluster table above. Exceptions:
- C-053 (CL-02, V2 cluster): **V1** 65%. V1 C-15 states an explicit invalid-block policy (V1:2184); V2 has none of its own (V2:3334).
- C-056 (CL-04, V2 cluster): **V1** 70%. Calibration as a routing signal is a V1-only decision (V1 C-06 V1:1602).
- C-065 (CL-04): **V1** 55%. Per-lens predicate as data (V1:2251); V2 leaves tasklist Medium unresolved.
- C-073, C-093 (CL-14): V1 as cluster.
- C-010 (CL-09, MERGE): **V1** 65%. `REPORT.md` and per-task verdict matrix gap only in V1 (V1 ENS-4 V1:655).
- C-018 (CL-09): **V1** 65%. The installed debate contract has no `merge_method` (V1 MS-24 V1:651).
- C-017 (CL-09): **V2** 65%. V2 names the 0.75 vs 0.80 conflict (V2:1252), though its SC-17 contradicts its delta row.
- C-025 (CL-09): **V2** 70%. Reflect memory write path only in V2 (V2:249).
- C-033 (CL-22): **V1** 70%. Total 1182 and per-suite counts; 651 and 353 re-collected here.
- C-038 (CL-06): **MERGE** 60%. V1 S-ID probes plus V2 collapse re-derivation.
- C-039 (CL-22): **V1** 65%. V1 recounted 38 of 39; V2 lists it as not recounted.
- C-043 (CL-13): **V1** 65%. Judge sees combo name (`judge-one.sh:21`).
- C-014 (CL-10): **V1** 55%. BL-16, BL-17, BL-19 have no V2 analogue (V1:620-623).
- C-096 (CL-20): **V2** 70%. Branch layouts are excluded by owner decision; only the git constraint stays.
- S-039 (CL-17): **V1** 65%. The D1-D16 defect-to-test table (V1:2517-2538) is plan input.
- S-044 (CL-17): **V1** 55%. Post-debate re-rating paragraphs (V1:1381, V1:1539, V1:2119) record effort and risk after the debate.

## Shared assumption responses

| A-id | Response | Reason with evidence |
|---|---|---|
| A-002 | ACCEPT | Code is identical between `792cf8c52` and `50d4d2b9d` (X-063) and the spot-checked lines hold at `ad8f57560`; I re-read `findings.py:104,188-192,346-349`, `ledger.py:127-138,187,254-258`, `card_convert.py:86,200-201` and all match both reports. |
| A-006 | ACCEPT | True and merge-critical: V1 "G-20" is a log row, V2 G-20 a gap; V1 D1-D16 are hand-off defects, V2 D-1..D-14 decision groups (V2:1492). The merged document must prefix every id with its source (for example `R1:D2`, `R2:G-12`). |
| A-008 | QUALIFY | C8 applies only when the driving spec names the capability as shipped or enabled (rule text V1:581). A skill line that says "rejected until Stage 3" (`SKILL.md:87`) is evidence the premise fails for that path, but a merged PR description (#519) may meet it. Decide per row with the cited driving text, as V1 does (V1:583), and record "premise unverified" where it is not read. |
| A-012 | ACCEPT | V1's 94-row gaps log and V2's 555-row log come from different research sets and units (V1:101, V2:135); neither is a subset of the other. |
| A-018 | REJECT | The assumption is false: `review-tiers.default.json` still lists the owner-excluded Qwen3.8-max, lacks `muse-ember-1.0`, and `gateway` has `launch: {}` (diff-analysis A-018; V2 2.6 V2:598-615). A plan must treat the tier file as a requested list, not a served one. |
| A-019 | QUALIFY | Valid only for this machine: the variants are under `~/.claude/` and not in `src/`, and `superclaude install` neither installs nor removes them (V2 F-4 V2:3626). They are evidence of design ideas, not of what any other consumer sees. |
| A-024 | QUALIFY | Slice- and hand-off numbers may stand only when tagged DOC-SOURCED and never decide (V1's own rule, V1:2815). V1 used slices as evidence (V1:108-123); the merged document should prefer V2's re-derived values where they exist (C-026). |
| A-027 | QUALIFY | The core serves engine B's data model (findings-v2, kernel, contract 1.8.0) in shadow while engine A stays production Tier 2 (V2 axis 8 V2:3643); the core does not have to pick one engine now, but the single-engine decision must stay a named owner decision (V2 Q-09; V1 G-65 V1:2316). |
| A-036 | QUALIFY | The checked lines hold today (A-002), but a plan must re-read every cited line before editing, because the tasklist-branch commits (newest `e2f2ac268`) are folded in later and may move lines. |
| A-037 | QUALIFY | V2's `6c09843` is the better baseline (it contains V1's pin plus 4 commits, X-062); neither is final, because `e2f2ac268` is newer and is folded in later by owner decision. |
| A-038 | ACCEPT | Re-run here: `uv run pytest --collect-only -q -p no:cacheprovider tests/review` = 651 tests collected (380 `def test_` functions; the rest are parametrised cases). "651" counts collected tests. |
| A-041 | QUALIFY | 13 of 20 and EV-1 8 of 13 reproduce from the exit script (V1 G-exit V1:4051); "6 of 9" collapse is only in `PLAN.md:66-69` with `/tmp/shadow-logs` absent, so it is DOC-SOURCED. These describe recorded runs, not current behaviour. |
| A-052 | QUALIFY | `partial` winners are usable only as default positions whose open HIGH invariants become plan gates or owner questions (V1 risk table V1:2862-2867; V2 7.3 V2:3985-4232). Neither report may present them as settled, and the merged text must say "adjudicated default, partial" wherever it says "governs". |
| A-055 | ACCEPT | E2 files are not tracked at HEAD and both reports read them by `git show`; the two pins differ by 4 commits that add collaboration paths and no `src/` or `tests/` change (C-001, A-015). |
| A-056 | QUALIFY | Holds for V1 by construction (V1:3117) and fails for V2 (8 CORE rows contradict Section 7, 40 not re-judged, V2:4300-4314). The merged inventory must be re-routed against the merged Section 7 before a plan consumes it. |
| A-057 | REJECT | Code-contradicted: `findings.py:104` rejects the line, `parse_block` skips it (`:188-192`), `ledger.py:135-136` annotates only accepted findings. `KeyError` occurs only on a direct `annotate` call or after switching the ledger to the v2 parser. |
| A-058 | REJECT | V1 C-05 (who decides blocking) is not V2 C-05 (consumer entry); V1 Q-47 is not V2 Q-47; V1 G1-G11 test suites are not V2 G1-G27 gates (diff-analysis A-058). Ids must be namespaced. |
| A-059 | REJECT | 698 consolidated items vs 5,950 ledger rows, 19 vs 27 gates, 61 vs 93 questions measure different units (Partial D value-inventory table). Counts must be quoted with their unit and never compared as quality. |

## U-register verdicts

### High-value V2 contributions

| U-id | Variant | Verdict | Reason |
|---|---|---|---|
| U-018 | V2 | KEEP | The precedence table is how a merged document with adjudicated overrides stays readable (V2:1125-1144); rebuild it against the merged Section 7, since it "is not a second review of every row". |
| U-020 | V2 | KEEP | `defer` rewrites the verdict and the stored verdict goes stale (V2 G-14, G-15); V1 has the `defer` defect only as debate invariant INV-001 (V1:2866). True and plan-relevant. |
| U-021 | V2 | KEEP | Collaboration designs and their gaps are V2-only and in scope of E2. |
| U-022 | V2 | KEEP | Process-redesign gaps, same reason. |
| U-023 | V2 | KEEP | Evaluation governance and SC-29..SC-31 are acceptance inputs a plan needs. |
| U-024 | V2 | KEEP | Run-record race, `model_scores` double count and memory read-modify-write are verified defects. |
| U-025 | V2 | KEEP | Defect-register families are the plan's defect backlog. |
| U-026 | V2 | KEEP | Repository constraints and gates bind every plan step. |
| U-027 | V2 | KEEP | Evidence-quality gaps (citation verification blind in 7 of 15 combo runs, calibrator without class) qualify every E1 number. |
| U-029 | V2 | KEEP | Tasklist six review shapes and plugin-mirror gaps are needed for the tasklist module. |
| U-031 | V2 | KEEP | E3i variants are one machine's state and shadow same-name commands; mark as machine-specific (A-019). |
| U-032 | V2 | KEEP | The consolidated decision and unverified-claim carry-over is what Section 9 should be built from; re-label ids to avoid V1/V2 collisions. |
| U-035 | V2 | KEEP | E2 tip baseline with the 4 named commits; note that `e2f2ac268` is newer and folded in later. |
| U-036 | V2 | KEEP | Skill-vs-code disagreements of the two engines are verified and drive reflect fixes. |
| U-037 | V2 | KEEP | Stage 2 failure causes by mechanism and the `reflect_shadow_exit.py:313` defect are plan input for the gate repair. |
| U-040 | V2 | KEEP | E2 collaboration packages facts (`lib/` absent from the commit) are verified at the tip. |
| U-042 | V2 | KEEP | E1/E2 one evidence family (byte-identical input, sha256 `044809e3...`) is the most important evaluation constraint; it changes V1's G-bench into a derivation-set check, not an acceptance test. |
| U-044 | V2 | QUALIFY | Facts about the installed variants cannot be re-checked in this debate (`~/.claude/` excluded) and V2 contradicts itself (X-034); keep with the tag "verified by run 2 only". |
| U-045 | V2 | KEEP | Five tier-data layers, `T2bModel01` in 11 files, `muse-ember-1.0` absent: needed by the dispatch and tier-file work. |
| U-046 | V2 | QUALIFY | Probes P-b..P-d stand; probe P-a shows `KeyError` only for a direct `annotate` call. The merged text must say so and must not claim a crash of the merge path (X-020). |
| U-047 | V2 | KEEP | The 171-row register is the most complete defect list; map V1's D1-D16 onto its ids. |
| U-048 | V2 | KEEP | Tasklist T1-T5 stage map and HARD/SOFT blocker table are module inputs. |
| U-049 | V2 | KEEP | `verify-sync`, `lint-architecture`, fence tests and layouts the gates reject are binding constraints V1 lacks. |
| U-051 | V2 | KEEP | Acceptance-evidence state (six audits, no `verify-run`, rule-vs-data timing) is needed for the acceptance tiers. |
| U-054 | V2 | KEEP | Hooks/headless facts (PostToolUse success-only, `--bare` drops hooks, `--tools` vs `--allowedTools`) bound any `claude -p` lane; external, keep the source tags. |
| U-056 | V2 | KEEP | Finding-schema research (SARIF, rdjson, GitHub review API 422 out-of-diff) is needed by the PR adapter. |
| U-071 | V2 | KEEP | The 189-row conflict log by pointer or appendix; too large inline, but the plan needs its decided rows. |
| U-072 | V2 | KEEP | The 15 adjudicated outcomes with margins and conditions; carry each as "adjudicated default, partial" (A-052). |
| U-073 | V2 | KEEP | INV-A..INV-N name the invariants every change must preserve; they are the no-regression contract in prose. |
| U-074 | V2 | QUALIFY | Keep "port contracts, not scripts"; the sha256 match is not re-checkable here (U-044). |
| U-075 | V2 | KEEP | Same as U-042, with three-tier acceptance. |
| U-076 | V2 | KEEP | M1-M14 exposures and "only M1-M4 outright reject a use case today"; merge with V1's X1-X14 (U-102) under one id scheme. |
| U-077 | V2 | KEEP | Branch refs cannot be path prefixes, reserved contract names, `SKILL.md` requirement, reflect edit fence: all binding. |
| U-110 | V2 | QUALIFY | Keep the 5,950-row inventory by pointer and its reconciliation, but re-route the 8 contradicting CORE rows and re-judge the 40 keyword matches against the merged Section 7 (A-056). |
| U-111 | V2 | KEEP | Inventory-conflict resolution rules (authoritative column, duplicate groups, re-routing) are how the merged inventory stays consistent. |
| U-112 | V2 | KEEP | 29 binding constraints with enforcing test or hook; the plan's constraint list. |
| U-113 | V2 | QUALIFY | Keep D1-D26 but correct D9 (`KeyError` on the ledger path is false for the default merge path; X-053). |
| U-114 | V2 | KEEP | AE-1..AE-15 with recomputed hashes are testable acceptance conditions. |
| U-115 | V2 | KEEP | The 244-row invariant table is where the open HIGH invariants become plan gates; keep by pointer. |
| U-116 | V2 | KEEP | Per-consumer "does this block?" verdicts with conditions; merge with V1's exposure list. |
| U-117 | V2 | KEEP | Collaboration and process-redesign design decisions with Q-17..Q-21. |
| U-118 | V2 | KEEP | Q-35, Q-39, Q-40, Q-90..Q-93; Q-39 is now answered by the owner (newer tasklist commits folded in later) and Q-40 remains the core-shape confirmation. |

### High-value V1 contributions at risk in a merge

| U-id | Variant | Verdict | Reason |
|---|---|---|---|
| U-001 | V1 | KEEP (at risk) | No producer for `unauthorized_deviation_present` (V1 MS-14 V1:641); absent from V2, Critical by C8. |
| U-002 | V1 | KEEP (at risk) | The installed debate contract has no `merge_method` and writes no `merged-verdict.yaml` (V1 MS-24 V1:651); V2's "merged-verdict copy by code" (V2:1168) depends on it. |
| U-003 | V1 | KEEP (at risk) | `REPORT.md` and per-task verdict matrix never produced by the post gate (V1 ENS-4 V1:655). |
| U-005 | V1 | KEEP (at risk) | Track tags per gap and the by-track table; re-label tracks if the merged design changes M1-M4. |
| U-010 | V1 | KEEP | SC-6, SC-10 and SC-14 pass rules are concrete acceptance tests. |
| U-058 | V1 | KEEP | D1-D16 with "v2 shares it?" column; map onto V2's register ids. |
| U-064, U-065, U-066, U-068 | V1 | KEEP (at risk) | Severity, clustering and calibration research with options lists; V2 Section 5 has none of these topics. |
| U-086 | V1 | KEEP (at risk) | Panel-size and cost decision with recount and owner-gated D-1; V2 has no axis. |
| U-087 | V1 | KEEP | Defect-to-test table (V1:2517-2538). |
| U-088 | V1 | KEEP (at risk) | 6.E debate detail (decisions, test pins, coupled edit sites) for C-03, C-05, C-13, C-14. Where V2's adjudication replaced a V1 decision, keep the V1 row as the alternative with its invariants. |
| U-096 | V1 | QUALIFY | The 48 steps are migration content the owner wants, not a schedule; re-base them on the merged design and remove ordering language that reads as a roadmap. |
| U-097 | V1 | KEEP (at risk) | Per-gate replacement assertions; V2's no-plan stance would drop them. |
| U-098 | V1 | KEEP (at risk) | Collected counts and exact commands per gate; 651 and 353 re-collected here. |
| U-099 | V1 | DROP (keep the constraint) | Branch layouts A-E are a branch plan; the owner fixed `feat_review-panel/<name>`. Keep only the ref constraint sentence (V1:4059). |
| U-100 | V1 | KEEP (at risk) | Persisted-format and rollback rules; V2 has none. |
| U-101 | V1 | KEEP (at risk) | Gap-to-step coverage map; rebuild against the merged gap table. |
| U-102 | V1 | KEEP | X1-X14 exposure list incl. coverage mode X14; merge with V2's M1-M14 (U-076). |

## Merge-critical content

**Must survive (from V1):** verified-fact statements on the merge path (BL-04 V1:608, 7.2 V1:2992, 7.3 V1:3019); the 8.3 gate list with commands, collected counts and replacement assertions (V1:4031-4055); persisted-format and rollback rules (V1:3830, V1:3845, V1:3861); track tags and the gap-to-destination map (V1:761, V1:772-780, V1:3910-4030), rebuilt against the merged gap table; MS-14, MS-24, ENS-4, BL-16, BL-17 (V1:620-621, V1:641, V1:651, V1:655); the D1-D16 defect-to-test table (V1:2517-2538); C-14 panel size and D-1 (V1:2107-2117), C-06 calibration (V1:1602), C-15 invalid-block policy (V1:2184), C-12 clustering acceptance metric (V1:1988); Section 5.2-5.4 research and options (V1:853-1079); the git ref constraint sentence (V1:4059).

**Must survive (from V2):** E2 collaboration and process-redesign evidence and axes; E1/E2 one evidence family and three-tier acceptance; the adjudicated defaults with margins, conditions and open HIGH invariants (marked "adjudicated default, partial"); the precedence table rebuilt for the merged text; 29 binding constraints, 26 dependency facts (D9 corrected), 15 acceptance conditions; INV-A..INV-N; the 5,950-row inventory by pointer with re-routing; the read-only condition on any launch lane; repo layout traps; Section 5.2-5.4 hooks, git refs and finding schemas.

**Corrections to V2:**
1. `KeyError` wording at G-01 (V2:1236), SC-01 (V2:1177), G-99 (V2:1334), 6.1 shared facts (V2:2177), CO-1 (V2:3330), axis 1 option D text (V2:3636), axis 2 evidence (V2:3637), 7 contradictions C-2 (V2:3882) and 8.2(c) D9 (V2:4508): replace with "rejected by v1 `parse_block` at `findings.py:104`; `annotate` raises `KeyError` at `findings.py:349` only on a direct call or after a switch to the v2 parser". Remove it from the evidence for the axis-2 choice.
2. Calibrator 6-vs-5 (V2:891, V2:1033, V2:3323): CODE-VERIFIED, not UNVERIFIED.
3. G-133 (V2:1368): 1,398 is all rows, not multi-member rows.
4. G-96 (V2:1331): "(6)" becomes 5 lines / 7 occurrences.
5. 2.4 vs OQ-01 (V2:432-448 vs V2:1025): one status for the installed-variant facts.
6. SC-17 (V2:1193): 0.80 decided by code, as the delta row says (V2:1137).
7. G-85 and 3.5 (V2:1320, V2:1227): DO4 adjudicated (A-13), not open.
8. SC-04 (V2:1180): quorum floor `min(2, requested)` (A-3).
9. First-parse compliance 0.704 (V2:215): mixed definitions before commit `9874d63fb` (X-027).
10. `cluster_agreement` "all 1.000" (V2:216, V2:874): add shadow09 0.9328, excluded only because its contract does not parse (X-028).
11. `ensemble.py` "E1 engine A" (V2:845): master-baseline code predating E1 (X-032); keep "engine A" as a label.
12. G-06 (V2:1241): Critical by V2's own rubric (V2:1121).
13. A-13 (V2:3664): state that the tiebreaker selected the lower-scored variant.

**Corrections to V1:**
1. Qwen "3 of 3 slots" (V1:204) becomes 3 of 4 runs (X-025).
2. Audit D "3 plus a merge that lost two blocking findings" (V1:201, V1:470) becomes 3 flips plus 5 total-loss merges (X-026).
3. rf-* "43 call sites in 11 files" (V1:410, V1:616, V1:716, V1:2976) becomes 52 structured lines in 11 files, 44 in 8 `SKILL.md` files (re-run here).
4. `same_defect` (V1:305) gains the both-empty-refs branch (X-031).
5. Engine-A contract "33 keys, 11 outside" (V1:420, V1:640, V1:658) becomes "32 literal keys plus conditional `t2_fallback`" with the counting basis stated (X-023, X-024).
6. D2 (V1:590) becomes Critical (X-012).
7. Quorum "owner decision" (V1:528, V1:591) aligned with C13-06 `min(2, panel_size)` (V1:2641).
8. "DECIDED-BY-EVIDENCE" for C-01, C-04, C-12, C-17 (V1:2830) becomes "defect decided by code, remedy chosen by design" (X-052).
9. Section 8.4-8.6 branch layouts, risk register and checklist (V1:4057-4120) dropped; branch naming is the owner's `feat_review-panel/<name>`.
10. E2 pin (V1:93, V1:2814, V1:3069, V1:4390) re-stated against V2's tip `6c09843`; any V1 E2 figure that differs at the tip is replaced by V2's re-derived value.

**Structural requirements for the merged document:** namespace every id by source (A-006, A-058); quote every count with its unit (A-059); one meaning for exit code 12 (X-058); mark every debate result "adjudicated default, partial" with its open HIGH invariants as plan gates (A-052); re-route the inventory against the merged Section 7 (A-056).

## Fact re-derivations performed

| What was checked | Command or file | Result | Which report was right |
|---|---|---|---|
| Collected tests in `tests/review` | `PYTHONDONTWRITEBYTECODE=1 uv run pytest --collect-only -q -p no:cacheprovider tests/review` | 651 collected; `def test_` count over `tests/review/*.py` = 380 | V1 (651 collected, V1:381, V1:4033); A-038 is about collected tests |
| Collected tests in `tests/cli/reflect` | same command on `tests/cli/reflect` | 353 collected | V1 (353, V1:381); consistent with V2's "352 passed + 1 xpassed" (V2:217) |
| `KeyError` on the ledger merge path | Read `findings.py:104,186-193,346-349`; `ledger.py:127-138` | `_check_flat(obj.get("anchor"), ...)` at :104 rejects; `parse_block` `continue`s at :192; `ledger.py:135-136` annotates only `parsed["findings"]`; `annotate` dereferences `finding["anchor"]` at :349 | V1 (X-020, X-049, X-053, A-057); V2 wrong at the 9 sites listed above |
| Clearing by silence and blocking union | `ledger.py:187`, `:254-258` | `any(m["blocking"] ...)`; `resolved_check` row absent next round becomes `resolved`, no `block_ok` read | Fact agreed by both; rating V2 (X-012) |
| Existing claim cut | `card_convert.py:86,200-201` | `MAX_CLAIM = 300`; `text[: MAX_CLAIM - 3] + "..."` | Both cite it; supports V1's claim truncation as an existing precedent (X-040) |
| rf-* structured spawn lines | `grep -rn 'subagent_type: *"\?rf-' src/superclaude/skills \| wc -l` | 52 | V2 (X-022, X-029, X-061) |
| V2 uses the false `KeyError` as decision evidence | Read V2:3636-3637 | axis 1 states the correct form; axis 2 "Evidence for the adjudicated choice" states the crash | V2 internally inconsistent; V1 correct |
| V2 rubric vs G-06 | Read V2:1121 and V2:1241 | rubric: fail-open verdict = Critical; G-06 (3 FAIL-to-PASS flips) = Important | V1's D1 Critical (X-011) |
| V1 quorum in debate output | Read V1:2641 | `quorum = min(2, panel_size)` in 6.E C13-06 | Both converge (X-004); V1 Section 4 stale |
| V1 knew of the `defer` defect | Read V1:2866 | INV-001 "`defer` rewrites an unverified FAIL to PASS, `ledger.py:350-360`" | Qualifies U-020 "absent in V1" (absent only from V1 Section 4) |
| C-05 adjudication score | Read V2:3664 | A 0.8728, B 0.8904, "B ahead; the tiebreaker selects A" | Caveat on X-005, X-060 |

Not re-derived by me (taken from the orchestrator table or analysts, with their commands): X-021 `audit2.py`, X-025 `SPEC.md`, X-026 `summary.md`, X-027 commit `9874d63fb`, X-028 shadow09 files, X-030 calibrator lines, X-031 `findings.py:367-379`, X-032 `git log ensemble.py`, X-023 key count, X-063 HEAD diff. X-035 rests on my knowledge of the SARIF 2.1.0 schema; nothing was fetched.

## Self-assessed strongest and weakest cluster for V1

Strongest: CL-18 (fact disputes), because the decisive one, the `KeyError` path, is re-verified at HEAD, V2 states it wrongly at nine places, and V2 uses the wrong form as evidence for its axis-2 adjudication and as dependency fact D9; close behind is CL-20, where V1's gate list with replacement assertions, rollback rules and gap-to-step map is content a `/sc:workflow` plan cannot get from V2. Weakest: CL-11 (E2 collaboration and process redesign), where V1 has nothing because it pinned the older E2 commit; and V1's method in CL-17, where labelling 16 of 20 conflicts "DECIDED-BY-EVIDENCE" overstated what code evidence can decide.
