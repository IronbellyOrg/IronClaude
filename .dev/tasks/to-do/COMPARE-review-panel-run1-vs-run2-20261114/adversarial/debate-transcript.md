# Adversarial Debate Transcript

## Metadata
- Depth: standard
- Rounds completed: 2 (Round 1 parallel, Round 2 sequential) plus Round 2.5 invariant probe; no Round 3 (depth standard)
- Convergence achieved: 94.0% strict (220 of 234 points resolved); 96.6% if the 6 both-open points count as agreement; Round 1 alone: 82.5%
- Convergence threshold: 80%
- Focus areas: recommendation and architecture, conflict outcomes, value-inventory destinations, evidence accuracy, gaps and risks, open questions
- Advocate count: 2 (Variant 1 = run 1 report, Variant 2 = run 2 report), plus 1 independent fault-finder (Round 2.5)
- Debate points: 234 (S 56, C 97, X 63, promoted A 18) grouped into 25 topic clusters; levels L1 50, L2 126, L3 58 (see debate-points.md)
- Gates: taxonomy coverage PASS; invariant probe BLOCKS convergence (7 HIGH UNADDRESSED: INV-003, INV-006, INV-018, INV-024, INV-027, INV-028, INV-029; see invariant-probe.md)
- Scope adaptation: the two inputs are about 1.2 MB each, so advocates argued by clusters and per-point tables over the cited line ranges instead of reading whole reports; Low and Medium S/C rows inherited their cluster verdict unless an advocate listed an exception.
- Embedded below: the advocates' own files, verbatim (headings demoted). Originals: partials/r1-advocate-V1.md, r1-advocate-V2.md, r2-advocate-V1.md, r2-advocate-V2.md, invariant-probe.md, partials/r25-fault-finder-notes.md.

## Round 1: Advocate Statements

### Variant 1 Advocate (opus: general-purpose advocate for the run 1 report)

#### Round 1 Statement: Advocate for Variant 1 (run 1 research report)

- Debate: /sc:adversarial Mode A, depth standard, Round 1
- Variant 1 (V1) = `adversarial/variant-1-original.md` (run 1, 4,476 lines). Variant 2 (V2) = `adversarial/variant-2-original.md` (run 2, 5,098 lines).
- Inputs read in full: `diff-analysis.md` (730 lines), `debate-points.md` (189 lines), `partials/orchestrator-verification.md`.
- Citation form: `V1:L` / `V2:L` = line in the variant file; ids from `diff-analysis.md` are written bare (S-nnn, C-nnn, X-nnn, A-nnn, U-nnn); ids that exist inside a report are prefixed "V1" or "V2" (for example "V1 C-05").
- Read-only: no repo file changed except this one; no git write; nothing under `.claude/` read.

#### Position

V1 is the stronger base for the parts a later `/sc:workflow` plan executes against: verified code facts (it is right on the `KeyError` path, the 1,398 unit, the calibrator 5-vs-6 mismatch and `ensemble.py` provenance where V2 is wrong or unverified), an implementer-grade no-regression gate list with per-test replacement assertions and collected counts, persisted-format and rollback rules, a gap-to-step map, and the decisions V2 never treats (panel size and cost, calibration, clustering). V2 is the stronger base for scope, evidence independence, adjudication and plan constraints (E2 collaboration and process redesign, E1/E2 one evidence family, 15 adjudicated debates, 29 binding constraints, 26 dependency facts, 15 acceptance conditions), so the truest merged document takes V2's adjudicated design as the governing default and V1's verified facts, gates and implementer detail as mandatory content, with V1's single-core design kept as the recorded convergence target behind V2's triggers T-a/T-b/T-c.

#### Steelman of Variant 2

**Overall.** V2 is the more complete and more honest research record. It reads the E2 branch four commits further (tip `6c09843`, which holds 1,145 collaboration/process-redesign paths against 3 at V1's pin, C-001), so it covers work V1 never saw (E2 collaboration designs r1-r5 and the Sweep Sheet / Recipe Ledger brainstorms, V2 2.3 V2:345-412). It refuses to call a design choice "decided by evidence" when no run compares the options (every axis UNDECIDABLE before debate, V2:3004-3018), and it then adjudicated all 15 open slots by debate and folded each winner, its margin, its conditions and its open HIGH invariants into Section 7 (V2 "Choices the evidence cannot decide" V2:3648-3671). It is transparent about its own internal drift: the 16-row precedence table (V2:1125-1144) says exactly which Section 3/4 cells Section 7 withdraws, narrows or replaces. Its Section 8 obeys the "no roadmap" scope more strictly (V2:4236) and still hands a plan the inputs it cannot invent: 29 binding constraints with enforcing test or hook (V2 8.2(a) V2:4430-4458), 26 dependency facts (V2:4498-4525), 15 acceptance conditions with recomputed hashes (V2:4529-4549) and a 5,950-row inventory that reconciles rows in = rows out (V2:4261).

**By cluster (what V2 gets right).**
- CL-01 core shape. The verified facts favour caution: findings-v1 requires an anchor (`findings.py:104`), `cluster_v2` cannot cluster anchor-only findings (V2 axis 1, V2:3636), and a single superset engine would rewrite the pinned v1 parser and ledger path that the loop and E2 tools use. A thin shared contract (id grammar, one limits module, one repair step, `refs_norm`, hash helpers, resolution, run record) captures the duplicated-constant value now, at low risk, with explicit convergence triggers T-a/T-b/T-c (V2:3636). V2 also states honestly that this differs from the owner's wording and asks the owner to confirm (V2 7.0.1, V2:3582, Q-40).
- CL-04/CL-05 blocking and ledger. V2 closes the ledger design instead of leaving a gate open: silence never clears, quorum-gated explicit `prior <lid> resolved`, `pending_new_sha256`, `defer` terminal and counted open, verdict derived on read and never stored (V2 axis 4, V2:3639). It catches two ledger defects V1's gap table lacks (G-14 `defer` rewrites the verdict, G-15 stored verdict stale, V2:1249-1250). Refusing a blind grader in the core is defensible because no decider other than the veto has ground truth and the stoprule integrity check returns `EXIT_OK` on a mismatch (X-039 verification row in diff-analysis). Rejecting a core `Medium` token follows from "Medium has six meanings" (V2:3637).
- CL-06 dispatch. "The core launches nothing" matches the code (`gateway` has `launch: {}`), and V2 adds a verified safety condition V1 lacks: the raw-id `claude -p` lane is not read-only (E2 launcher leaves Bash open, `run-reviewer.sh:48`), so any lane must enforce read-only at process level before PR or rf-qa may use it (V2 axis 5, V2:3640).
- CL-10 consumers. V2's consumer map is twice as deep (14 consumers incl. tasklist T1-T5, `tasklist validate`, `/task`, `/sc:implement`, V2 2.7 V2:659-726) and its future-consumer path (pure converter to `pr_submit.Finding`, report-only first release; rf-qa lens-level first step at the `/task` gate with a replay oracle) changes no pinned PR code (V2 axis 11, V2:3646).
- CL-11, CL-12, CL-13. Collaboration and process redesign are V2-only and adjudicated (V2:3641-3642). V2 read the installed variant scripts and matched 17 of 17 files to the install log by sha256 (U-074). V2's evidence-independence finding is the single most important evaluation fact in either report: E1's input package is byte-identical to E2's designSpec candidate (sha256 `044809e3...`), so E1 and E2 are one derivation set and acceptance needs a hold-out neither used (U-042, U-075; V2 axis 9 V2:3644).
- CL-16, CL-22. V2 does not use scope slices as evidence (V2:108), re-derives E2 headline numbers from committed files and found the `final-table.py` `fullpkg()` prefix bug (C-026), and is right on three E2 counts where V1 is wrong or narrower (Qwen 3 of 4, X-025; audit D 3 flips plus 5 total-loss merges, X-026; `same_defect` both-empty-refs branch, X-031).
- CL-17, CL-19, CL-20, CL-24. A 189-row conflict log, 14 named invariants INV-A..INV-N (U-073), a 244-row invariant table, and a consolidated carry-over (decision groups D-1..D-14, unverified U-1..U-18, V2:1494-1532) are the right shape for a document a planner must not misread.

#### Strengths claimed for Variant 1

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

#### Weaknesses identified in Variant 2

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

#### Concessions (genuine weaknesses of Variant 1)

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

#### Cluster verdicts

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

#### Per-point verdicts

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

#### Shared assumption responses

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

#### U-register verdicts

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

#### Merge-critical content

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

#### Fact re-derivations performed

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

#### Self-assessed strongest and weakest cluster for V1

Strongest: CL-18 (fact disputes), because the decisive one, the `KeyError` path, is re-verified at HEAD, V2 states it wrongly at nine places, and V2 uses the wrong form as evidence for its axis-2 adjudication and as dependency fact D9; close behind is CL-20, where V1's gate list with replacement assertions, rollback rules and gap-to-step map is content a `/sc:workflow` plan cannot get from V2. Weakest: CL-11 (E2 collaboration and process redesign), where V1 has nothing because it pinned the older E2 commit; and V1's method in CL-17, where labelling 16 of 20 conflicts "DECIDED-BY-EVIDENCE" overstated what code evidence can decide.

### Variant 2 Advocate (opus: general-purpose advocate for the run 2 report)

#### Round 1 Statement: Advocate for Variant 2 (run 2 report)

- Debate: /sc:adversarial Mode A, depth standard, Round 1
- Role: advocate for V2 (`variant-2-original.md`, 5,098 lines); a second advocate argues for V1 (`variant-1-original.md`, 4,476 lines)
- Inputs read in full: `diff-analysis.md` (730 lines), `debate-points.md` (189 lines)
- Id conventions: diff ids (S-nnn, C-nnn, X-nnn, U-nnn, A-nnn) are the ids of `diff-analysis.md`; ids that exist inside a report are always written with "V1" or "V2" in front (for example "V2 C-05" is a debate slot of run 2; "V1 C-05" is a conflict of run 1).
- Line numbers: "V1:n" and "V2:n" are lines of the two variant files (byte-identical to the original reports).
- Read-only: no repo file other than this one was changed; no git write command was run; nothing under `.claude/` was read.

(Sections are appended one at a time below.)

#### Position

V2 should be the base of the merged document: it reads the newer E2 evidence (tip `6c09843`, four commits after V1's pin, holding the collaboration and process-redesign material V1 never saw), it covers the whole question (collaboration, process redesign, evaluation independence, repo constraints, a 171-row defect register), and its recommended shape (a thin shared contract with per-module engines, with named triggers for later convergence) rests on verified code facts, while V1 calls core-shape questions "DECIDED-BY-EVIDENCE" that no run decided. V2 is not the whole answer: V1's implementer-grade migration content (48 steps with files, per-gate replacement assertions and collected counts, rollback and persisted-format rules, the gap-to-step map, the ENS post-gate defects and the panel-size decision) must be carried into the merge, and V1 is right on several facts where V2 is wrong (the `KeyError` path, the calibrator 6-vs-5 mismatch, the 1,398 unit, the 0.704 definition, the over-length severity).

#### Steelman of Variant 1

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

#### Strengths claimed for Variant 2

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

#### Weaknesses identified in Variant 1

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

#### Concessions

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

#### Cluster verdicts

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

#### Per-point verdicts

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

#### Shared assumption responses

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

#### U-register verdicts

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

#### Merge-critical content

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

#### Fact re-derivations you performed

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

#### Self-assessed strongest and weakest cluster for V2

V2's strongest cluster is CL-11 (E2 collaboration and process redesign, 85%): V1 has no content there at all, V2 reads the r1-r5 packages and the two brainstorms at the newer pin, gives options and adjudicated dormant-by-default outcomes with build and enable triggers, and names the newer commit that may change the premise; with CL-16 (baseline) and CL-13 (evidence independence) it is the part of V2 a merge cannot do without. V2's weakest cluster is CL-18 (fact disputes, V1 60%): V2 repeated a wrong `KeyError` claim in nine places and used it as evidence for an adjudicated choice, tagged a true calibrator fact [UNVERIFIED], and mis-described the 1,398 and 0.704 figures, while V1 got those facts right; close behind are CL-09 (V2 leaves Critical post-gate defects in production) and CL-20 (V2's Section 8 lacks the replacement assertions, rollback rules and gap-to-step map that V1 supplies).

## Round 1 convergence snapshot

#### Convergence snapshot after R1

- Debate points: 234; agreed: 193; disagree: 41; no verdict from one side: 0
- Convergence = agreed / total = 0.825

#### Cluster-level verdicts

| Cluster | V1 advocate says | V2 advocate says |
|---|---|---|
| CL-01 | MERGE | V2 |
| CL-02 | V2 | V2 |
| CL-03 | V1 | MERGE |
| CL-04 | V2 | V2 |
| CL-05 | V2 | V2 |
| CL-06 | V2 | V2 |
| CL-07 | MERGE | OPEN |
| CL-08 | MERGE | V2 |
| CL-09 | MERGE | MERGE |
| CL-10 | V2 | V2 |
| CL-11 | V2 | V2 |
| CL-12 | V2 | V2 |
| CL-13 | V2 | V2 |
| CL-14 | V1 | MERGE |
| CL-15 | V1 | MERGE |
| CL-16 | V2 | V2 |
| CL-17 | V2 | V2 |
| CL-18 | V1 | V1 |
| CL-19 | V2 | V2 |
| CL-20 | MERGE | MERGE |
| CL-21 | MERGE | MERGE |
| CL-22 | V2 | V2 |
| CL-23 | MERGE | MERGE |
| CL-24 | V2 | V2 |
| CL-25 | MERGE | MERGE |

#### Points where the advocates disagree (winner by V1 advocate | by V2 advocate)

| Point | Cluster | V1 advocate | V2 advocate |
|---|---|---|---|
| S-040 | CL-01 | MERGE (cluster) | V2 (cluster) |
| C-005 | CL-01 | MERGE (explicit) | V2 (explicit) |
| C-050 | CL-01 | MERGE (explicit) | V2 (explicit) |
| C-061 | CL-01 | V1 (explicit) | V2 (explicit) |
| C-076 | CL-01 | MERGE (explicit) | V2 (explicit) |
| C-090 | CL-01 | V1 (explicit) | V2 (explicit) |
| X-038 | CL-01 | MERGE (explicit) | V2 (explicit) |
| X-042 | CL-01 | V1 (explicit) | V2 (explicit) |
| X-051 | CL-01 | MERGE (explicit) | V2 (explicit) |
| C-053 | CL-02 | V1 (explicit) | V2 (cluster) |
| C-052 | CL-03 | V1 (explicit) | BOTH (explicit) |
| C-077 | CL-03 | V1 (cluster) | MERGE (cluster) |
| X-040 | CL-03 | V1 (explicit) | OPEN (explicit) |
| X-056 | CL-03 | V1 (explicit) | OPEN (explicit) |
| C-065 | CL-04 | V1 (explicit) | V2 (cluster) |
| C-060 | CL-07 | MERGE (explicit) | OPEN (explicit) |
| C-081 | CL-07 | MERGE (cluster) | OPEN (cluster) |
| X-041 | CL-07 | V2 (explicit) | OPEN (explicit) |
| X-057 | CL-07 | MERGE (explicit) | OPEN (explicit) |
| C-034 | CL-08 | MERGE (cluster) | V2 (cluster) |
| C-057 | CL-08 | MERGE (cluster) | V2 (cluster) |
| C-083 | CL-08 | MERGE (cluster) | V2 (cluster) |
| X-010 | CL-08 | MERGE (explicit) | V2 (explicit) |
| C-025 | CL-09 | V2 (explicit) | MERGE (cluster) |
| C-084 | CL-09 | MERGE (explicit) | V1 (explicit) |
| X-043 | CL-09 | V2 (explicit) | V1 (explicit) |
| X-054 | CL-09 | MERGE (explicit) | V1 (explicit) |
| C-014 | CL-10 | V1 (explicit) | BOTH (explicit) |
| X-034 | CL-12 | NEITHER (explicit) | V2 (explicit) |
| C-009 | CL-15 | V1 (explicit) | BOTH (explicit) |
| X-017 | CL-15 | V1 (explicit) | V2 (explicit) |
| X-019 | CL-15 | OPEN (explicit) | V2 (explicit) |
| A-008 | CL-15 | V1 (cluster) | MERGE (cluster) |
| S-044 | CL-17 | V1 (explicit) | V2 (cluster) |
| X-023 | CL-18 | BOTH (explicit) | V2 (explicit) |
| X-024 | CL-18 | BOTH (explicit) | V2 (explicit) |
| S-056 | CL-20 | V1 (explicit) | BOTH (explicit) |
| X-036 | CL-23 | OPEN (explicit) | V2 (explicit) |
| S-004 | CL-21 | MERGE (explicit) | V2 (explicit) |
| S-022 | CL-22 | MERGE (explicit) | V2 (explicit) |
| X-008 | CL-21 | V2 (explicit) | V1 (explicit) |

## Round 2: Rebuttals

### Variant 1 Rebuttal

#### Round 2 Rebuttal: Advocate for Variant 1 (run 1 research report)

- Debate: /sc:adversarial Mode A, depth standard, Round 2 (sequential rebuttals; V1 advocate goes first)
- V1 = `adversarial/variant-1-original.md` (4,476 lines); V2 = `adversarial/variant-2-original.md` (5,098 lines)
- Inputs read: `diff-analysis.md` (rows for the 38 disputed points and the verification table), `debate-points.md` (full), `partials/r1-advocate-V1.md` (full), `partials/r1-advocate-V2.md` (full), `partials/convergence-r1.md` (full)
- Citation form: `V1:L` / `V2:L` = line of the variant file; bare ids (S-, C-, X-, A-, U-) = `diff-analysis.md` ids; ids inside a report carry a "V1"/"V2" prefix
- Verdict labels: V1 / V2 / BOTH / NEITHER / OPEN. My Round 1 "MERGE" is treated as BOTH; a MERGE-to-BOTH relabel is not counted as a move
- Read-only: only this file was written; no git write; nothing under `.claude/` or `~/.claude/` read. New checks this round: three batched read-only scripts over the two variant files (each `BATCH_DONE rc=0`), one Grep, and one web fetch of `https://arxiv.org/abs/2606.19544` (for X-036)

#### Response to V2's criticisms

The V2 advocate's eleven "Weaknesses identified in Variant 1" (r1-advocate-V2.md lines 60-70) are answered one by one, then the cluster and point verdicts that favour V2.

1. **Stale E2 pin and the missing half of E2 (weakness 1).** **Conceded in full.** V1 pins E2 at `4a22d74` (V1 "1. Problem Statement", V1:93) and its own Integration Checklist still says "every E2 citation names commit 4a22d74... only" (V1 8.6, V1:4119), which must be rewritten for the merge. V1 has nothing on collaboration or process redesign; V2 2.3 (V2:345-412) and axes 6-7 (V2:3641-3642) are the only source. This is the largest single reason V2 must supply the evidence base.

2. **"DECIDED-BY-EVIDENCE" over-claimed (weakness 2).** **Conceded for the label, contested in three details.** V1 Rationale 4 (V1:2830) calls 16 of 20 conflicts decided; no run compares core shapes, so that label is wrong for C-01, C-12 and the remedy half of C-17. Three details of the criticism are wrong:
   - **C-04 is a split status, not a blanket claim.** V1 C-04 "Status" (V1:1443) says only "remove silent re-admission and declare distinctness per slot" is decided by code evidence, and calls replicas "a design option, not a decided one". The decided part (silence must go) is also V2's position: V2 always writes `requested_slots` and `distinct_models` (C-081 row; V2:3657). The strict-or-soft default is the open part, and V1's "Recommended resolution" (V1:1445) does not label that default decided.
   - **C-17 does not claim the remedy is decided.** V1 C-17 "Status" (V1:2314) says only fix-then-replace is *feasible* because no UC-2 producer exists on the panel side; the next line (V1:2316) leaves "replaces `ensemble.py` or ... repaired permanently" to the owner's UC-2 decision (G-65).
   - **C-12's acceptance needing pending labels is disclosed, not hidden.** V1:1988 names the labels as the acceptance condition, and V1 8.5 says "human labels (#525-#530) are pending ... Not presented as measured accuracy (O-5)" (V1:4098). A gate that cannot run yet is legitimate; V2's own adjudicated gates G17-G27 are mostly "not run / not built" (S-056 row; V2:4482-4492).

3. **"findings-v1 is a strict subset of findings-v2" is false at HEAD (weakness 3).** **Partly conceded.** The code facts hold (`findings_v2.py:96-97,279-281`, re-read by both advocates in Round 1). But V1 states the subset as a *target to build*, not as today's fact: the C-01 Option A "Cons" row says "'strict subset' needs code and tests, not only wording" (V1:1211), and migration step M1-01 is "Make `findings_v2.check_finding` the only validator and accept findings-v1 lines as a strict subset" (V1 8.2, V1:3834). What I concede: the constraint row "findings-v1 lines stay valid input (strict subset of v2)" (V1 7, V1:3065) reads as a present-tense guarantee and must be reworded, and the cost of making v2 accept `prior` lines and `calibrated_confidence` is real; it is the cost V2's axis 1 avoids (V2:3636).

4. **The superset core is the largest and least measured surface (weakness 4).** **Conceded.** V1's own Options table rates Option B XL and Medium-High (V1 6.X, V1:2578-2579) and adds that the rating "holds only if the four debate-gated conflicts ... are settled" with 26 HIGH invariants open (V1:2620). "A is B's first stage, so the order costs nothing" (V1:2828) is an argument, not a measurement. I also concede that V1's rejection of Option C (V1:2622: "leaves D1, D5, D9, the opposite invalid-block policies and the third merge path in place") is aimed at a weaker C than V2's: V2's C shares one limits module, one repair step and one drop-and-account contract (V2 delta row "3.2 Merge, cluster, verify", V2:1135), which answers D1; and the third merge path (`ensemble.py`) stays in V1's own design until UC-2 Stage 5 (V1:2316).

5. **E2 numbers doc-sourced, two description errors (weakness 5).** **Conceded.** Qwen is "3 of 4 runs" (X-025) and audit D's third flip is the F1+F2 merge itself (X-026); V1 says it did not re-aggregate (V1 2.2, V1:191). V2's re-derived values and the `fullpkg()` bug (V2 2.2, V2:294-320) replace V1's numbers in the merge.

6. **Fewer ledger and verdict defects (weakness 6).** **Conceded for the gap table.** V1 knew the `defer` defect (risk table INV-001, V1:2866; risk input V1:4079) and builds a narrow fix ("`defer` accepts only a live blocking row", M1-07, V1:3840), but its Section 4 has no row for `defer` rewriting the verdict, the stale stored verdict, rounds after ESCALATE or a round not bound to the revised text (V2 G-14, G-15, V2:1249-1250). V2's axis 4 (V2:3639) is the more complete design.

7. **No precedence record; inventory destinations follow an undecided design (weakness 7).** **Conceded for the merge, not as a defect of V1.** V1 needed no override layer because its Sections 3-4 and 7 agree (S-007). But the merged document will adopt several V2 adjudications, so it needs V2's precedence table (V2:1125-1144) rebuilt against the merged Section 7, and V1's 698 inventory destinations (V1:3117-3119) must be re-routed like V2's (A-056).

8. **"Dispatch end state ignores the read-only risk of a raw-id lane" (weakness 8; also strength 11 and the CL-06 verdict).** **Rejected: the claim is false.** V1 has a whole conflict on it, "C-18: Read-only enforcement for reviewers" (V1:2320-2383). Its E2 row states the exact fact V2 relies on: "A deny list `--disallowedTools Edit Write NotebookEdit` under `bypassPermissions`; Bash stays available and auto-approved; the judge has no deny list at all", citing "E2 `run-reviewer.sh:48`" (V1:2327). The resolution is "allowlisted reviewer agents or an equivalent `claude -p` allowlist ... test the `claude -p` allowlist behaviour before relying on it (G-45)" (V1:2381), backed by SC-9 (V1:534) and K-7 (V1:560). My own Round 1 concession 9 ("V1 has no read-only requirement for a raw-id lane", r1-advocate-V1.md line 65) was wrong and is withdrawn. **What V2 adds and V1 gets wrong:** V1 names `claude -p --allowedTools` as the mechanism (V1:2332, V1:2381), but V2's external research finds that `--allowedTools` only pre-approves tools and does not restrict them; restriction needs `--tools`, `--disallowedTools Bash` or `--restricted` (V2 5.2, V2:1725-1728; summary row 11, V2:2054). V1's hedge "test before relying on it" would have caught it, but the merge must carry V2's mechanism with V1's requirement.

9. **Counts with unstated units (weakness 9).** **Conceded.** "43 call sites" does not reproduce (52 lines in 11 files, 44 in 8 `SKILL.md` files); "33 keys, 11 outside" includes the conditional `t2_fallback` without saying so (I still hold BOTH on X-023/X-024 below, because V1's two numbers are consistent with each other under that basis); `tests/cli/reflect` "has 37 files" (V1 2.4, V1:381) is wrong, 38 is right (V1 8.3, V1:4045).

10. **Web research misses runtime and git topics (weakness 10).** **Conceded for Section 5.** V1 Section 5 (V1:783-1153) has no hooks/headless, `--tools`/`--allowedTools` or ref-naming research; the `--allowedTools` error in point 8 is the cost. V1 states the git ref rule (V1:4059) from first principles; V2 C4 (V2:4433) has observed output.

11. **"Section 8 contains plan content the owner has now excluded ... Only the git constraint itself (V1:4059) survives" (weakness 11).** **Partly rejected: overbroad.** Only the layout table A-E (V1 8.4, V1:4063-4069) is a branch plan. The rest of 8.4-8.6 is constraint and no-regression content, which the owner says the plan needs:
   - V1 8.4 "Facts that shape the options" (V1:4061): local `master` is stale, so cut from `origin/master`; reflect pins C1, C6, C14 are HEAD-relative, so pinned-section edits go in separate commits and G8 runs before each commit; the live7 test couples `review-tiers.default.json` to `ccsession-models.json`; both panel goldens regenerate on any tier-file byte change; the rollback unit is one merged PR.
   - V1 8.5 is headed "Inputs for the risk register, not the register itself" (V1:4073). Rows such as persisted artifacts failing to load after a core change, with `scripts/reflect_shadow_exit.py:209-232` re-validating the 13 recorded shadow manifests (V1:4100), HEAD-relative pins passing trivially after a commit (V1:4085), golden and test-flip conflicts (V1:4086) and the false-green post gate (V1:4087) are no-regression constraints.
   - V1 8.6 (V1:4105-4120) is mostly gate operations: re-collect 1182 tests before any change (V1:4106), G8 before a commit near the reflect skill (V1:4107), replacement assertions changed with their fix (V1:4108), persisted-format reload tests (V1:4109), no top-level contract key (V1:4111), the Stage 2 exit must not worsen (V1:4117). Two items must change: V1:4116 (refers to an 8.4 layout; replace with the owner's `feat_review-panel/<name>`) and V1:4119 (E2 pin).
   My own Round 1 concession 8 (r1-advocate-V1.md line 64) made the same overbroad drop and is narrowed here.

12. **Cluster verdicts that favour V2.** I accept V2 as the stronger base on CL-02, CL-04, CL-05, CL-10, CL-11, CL-12, CL-13, CL-16, CL-17, CL-19, CL-22 and CL-24 (agreed in Round 1; no new evidence against). I contest or adjust four:
   - **CL-01 (V2 65%)**: V2 is right for the shape *now* (I move X-038 to V2). I hold that V1's superset stays in the merged document as the recorded one-engine target, on three pieces of evidence: the owner's wording is "thin modules" and V2 itself flags that its design "differs in one respect" because the spec "module" keeps a whole v1 engine (V2 7.0.1, V2:3582); V2's own trigger T-c ("a verified defect fix needs a non-helper edit to both parsers or both clusterers", V2:3636) is likely to fire on D6, whose chaining is confirmed on both clusterers (V1 D6, V1:594); and withdrawing the per-slot key left an open HIGH invariant in V2 (C-11 INV-009, V2:4144).
   - **CL-06 (V2 65%)**: moves to BOTH, because the read-only basis of V2's verdict is false (point 8). V2 keeps the dispatch-layer analysis (V2 2.6, V2:592-655), the `--tools` fact and launcher gating; V1 keeps C-18's allowlist decision and the S-ID identity probes (V1:167).
   - **CL-08 (V2 55%)**: BOTH. V2's `events.jsonl` answers the manifest lost update and the `model_scores` double count, which V1 does not address (no lock or race design in V1; Grep over V1:1-4476 for "lost update|lock-free|timed lock|manifest.save|race" finds no relevant hit). V1's audits A and D as built-in checks before `published` (V1 MS-04, V1:631) have no V2 counterpart. The record shape is V2's; the audit placement is V1's.
   - **CL-09 (MERGE 60%)**: the V2 advocate concedes the post-gate point to V1 (concession 4, r1-advocate-V2.md line 79); I now agree on V1 for the post gate (C-084, X-043, X-054 below).

13. **Per-point verdicts that favour V2 outside the 38.** Agreed, with one change this round: C-067 (CL-06, inherited V2) becomes BOTH for the reason in point 8 (V1 C-18 decision; V2 mechanism fact).

#### Updated assessment of V2

**Steelman (stronger than in Round 1).** After re-reading the lines both advocates cite, V2 is the better *base* for the merged document, not just the broader one. It is the only report that covers the whole question at the newer E2 tip (V2 Baseline, V2:108; 2.3, V2:345-412), the only one that tells a planner which evidence is not independent (E1 and E2 one derivation set, axis 9, V2:3644), and the only one that refuses to call a design choice decided when no run compares the options (axis status, V2:3004-3018). Its adjudicated outcomes come with conditions and open invariants (V2:3654-3671; 7.3, V2:3960-4232), its precedence table records exactly where Section 7 overrode Sections 3-4 (V2:1125-1144), and its Section 8 hands the plan binding constraints with enforcers (C1-C29, V2:4430-4458), dependency facts and acceptance conditions that V1 does not have. V2 is also correct on the one external fact that changes V1's read-only mechanism (`--allowedTools` pre-approves, does not restrict; V2:1725-1728). And V2 is candid about its own tension with the owner's wording (V2 7.0.1, V2:3582) and about the cost it accepts (shared defects fixed twice, V2:3636).

**What changed in my assessment this round.**
- **Up for V2:** the `--tools` finding (above) makes V2's external research decision-relevant for dispatch, not only background; V2's C-06 adjudication (drop record with `blocking_state` plus dropped-blocking refusal, V2:3516, V2:3638) closes the fail-open path that made D1 Critical, so the remaining claim-cut question is about recovery efficiency, not safety (moved X-040, X-056 to OPEN); and V2 C16 (V2:4445) shows that V2 does not forbid an `ensemble.py` repair, it only requires "its own decision", which makes the post-gate point a shared owner decision rather than a V1-versus-V2 conflict.
- **Down for V2:** the V2 advocate's main dispatch criticism of V1 (weakness 8) is false; V2's verbosity takeaway rests on a paper arXiv now shows as withdrawn (X-036 below); V2's own Section 1 says PR review needs "an optional per-slot lens" (V2:134) and its dependency fact D11 says the per-slot key "stays true for a later panel-engine step" (V2:4510), while Section 7 withdrew it and left HIGH invariant C-11 INV-009 open (V2:4144), so V1's reserved slot keys are the consistent position (X-008); and the wrong 1,398 unit appears in Section 7 as well, "195 of 1,398 multi-member rows chained" (V2 7.1 row 2, V2:3743).

**Remaining weaknesses of V2 that the merge must repair** (unchanged from Round 1 unless noted): the `KeyError` claim at nine sites, used as axis-2 evidence (V2:3637) and as dependency fact D9 (V2:4508); calibrator fact tagged [UNVERIFIED]; G-06 rated Important against its own rubric (V2:1121 vs V2:1241); stale "decision"/"open" wording in SC-04, SC-17, G-85, 3.5 and OQ-01; "50 test files"; the inventory and defect register held only by pointer (S-048); no per-test replacement assertions, rollback rules or gap-to-destination map in Section 8 (U-097, U-100, U-101); no clustering remedy for the measured v1 over-merge (V2:3743 keeps v1 clustering for the spec loop with "a verified merge defect ... fixed in the engine that has it" and no named remedy); new this round, the withdrawn-paper citation (X-036).

#### Final verdicts on the 38 disputed points

Round 1 verdict in brackets in the last column. "Moved" counts a change of verdict, not MERGE relabelled BOTH.

| Point | Final verdict | Confidence 50-99% | Evidence | Moved? (yes/no vs Round 1) |
|---|---|---|---|---|
| S-040 | BOTH | 60% | V2 6.1 has the fuller option set A-D incl. "fix the harness only" (V2:3636 lists all four); V1 6.X adds the layer diagram (V1:2544-2555) and the future-consumer fit rows (V1:2618) that V2 has only per consumer in 7.2.4. Base = V2's option set; carry V1's fit rows. | no [MERGE] |
| C-005 | BOTH | 60% | Shape now = V2's thin shared contract (delta rows V2:1129-1131); target = V1's one core (V1:494). Kept because the owner wording is "thin modules" and V2 flags that its spec module keeps a whole v1 engine (V2:3582, Q-40). | no [MERGE] |
| C-050 | BOTH | 60% | V2 axis 6.1 Option C adjudicated with triggers (V2:3636); V1's Option B rated XL, Medium-High (V1:2578-2579) stays the recorded one-engine target. V1's rejection of C (V1:2622) is aimed at a weaker C than V2's (V2:1135), conceded. | no [MERGE] |
| C-061 | BOTH | 60% | Which clusterer: follows the core-shape default, so V2's per-engine placement (V2:3743). The remedy: V1-only (complete-link admission, no merge on an empty location, anchor-to-citation step, acceptance by the 83 mega-rows falling plus pending labels; V1:1988, V1:4098). V2 names no remedy for the v1 over-merge that audit D measured (audit D copies `findings.py` rules, V2:1361). | yes [V1] |
| C-076 | BOTH | 60% | Same as C-005, at Section 7. V2's Recommended approach governs as "adjudicated default, partial" (V2:3578); V1's Recommended approach (V1:2823) is carried as the target behind T-a/T-b/T-c, with D6 named as the likely T-c trigger (V2:3636, V1:594). | no [MERGE] |
| C-090 | BOTH | 60% | Same as C-061 at Section 7: V2's "two deterministic merges, one per engine" (V2:3743) plus V1's clustering remedy and acceptance metric (V1:2850, V1:1988) as the "verified merge defect ... fixed in the engine that has it". | yes [V1] |
| X-038 | V2 | 65% | The disagreement is where to *start*: V1 starts from findings-v2 as the single contract (V1:2622), which needs v2 to accept `prior` lines and `calibrated_confidence` (`findings_v2.py:96-97,279-281`; V1's own Cons V1:1211); V2 starts from the thin contract and changes no pinned v1 path. | yes [MERGE] |
| X-042 | BOTH | 55% | V2's objection "`cluster_v2` leaves anchor-only findings as singletons" is answered in the cited V1 line itself ("an anchor-to-citation step", V1:1988); V1's objection that V2 has no remedy stands (V2:3743). Under the two-engine default each engine keeps its clusterer and gets V1's remedy. | yes [V1] |
| X-051 | BOTH | 60% | End shape is not evidence-decided (X-052, agreed). V2 shape governs now; V1 shape is the documented one-engine target, an owner question (V2 Q-40, V2:3582). | no [MERGE] |
| C-052 | BOTH | 65% | V2's adjudicated repair (three location fields to 200 behind `repair=False`, itemised drop record, dropped-blocking refusal, one re-ask; V2:3516) is the base; V1 adds the loss breakdown 24 anchor, 14 anchor2, 10 claim, 1 refs (V1 SC-2, V1:527) and the missing-anchor rule (V1:1315). | yes [V1] |
| C-077 | BOTH | 60% | Same as C-052 at Section 7 (V1:2840 vs V2:3638). | yes [V1, cluster] |
| X-040 | OPEN | 60% | Both designs close the fail-open path (V1 SC-2 "cannot compute PASS", V1:527; V2 dropped-blocking refusal, V2:3516). What remains is whether to cut `claim` (10 of 49 blocking losses, V1:527; precedent `card_convert.py:200-201`) or re-ask/raise the limit to 450 (V2:3516). Neither K2 nor a length distribution of the 10 claims was measured. Owner decision with the K2 test. | yes [V1] |
| X-056 | OPEN | 60% | Same as X-040 at Section 7 (V1:2840 vs V2:3638, V2:3656). | yes [V1] |
| C-060 | OPEN | 60% | Removing silent re-admission is agreed by both (V1:1443; V2 always records `requested_slots`/`distinct_models`, V2:3657). The default (strict vs soft) has no measurement in either report (V2 A-6 "soft stands until A's M1"); V1's per-slot declaration is carried as an option. | yes [MERGE] |
| C-081 | BOTH | 55% | The record fields are complementary, not competing: V2's `requested_slots`, `distinct_models`, tier-file guard test (V2:3594, V2:3657, V2:3747); V1's per-slot `none/model/class`, optional `replicas`, optional `role/lens/agent`, `tiers_as_of` (V1:2842, V2-side support for the slot key at V2:134, V2:4510). The default itself is OPEN (C-060). | no [MERGE] |
| X-041 | OPEN | 60% | Code shows soft today (`panel.py:509,519,575`; analyst ran `panel resolve` and reproduced V1:1436); no strict-vs-soft measurement exists. V1 labels only silence removal decided (V1:1443), V2 labels the default UNDECIDABLE (FX-15, V2:3235). | yes [V2] |
| X-057 | OPEN | 60% | Same as X-041 at Section 7 (V1:2842 vs V2:3657). | yes [MERGE] |
| C-034 | V2 | 70% | Section 2 evidence: V2's writer/cost table with the `model_scores` double count (D-17) and the `manifest.save` lost update with a deterministic interleaving (D-23) (V2:569-578); V1 rows 13-14 (V1:454-455) state no race, and V1 has no lock or race design anywhere (Grep V1:1-4476). | yes [MERGE] |
| C-057 | BOTH | 60% | V2's `events.jsonl` written only by code (V2:3518) for the record; V1's audits A and D as built-in checks before `published` (V1:1665, V1 MS-04 V1:631) for where checks live. V2's own margin is 0.13 percent (A-10, V2:3661). | no [MERGE] |
| C-083 | BOTH | 60% | Same as C-057 at Section 7 (V1:2845, V1:2954-2955 vs V2:3596, V2:3661, V2:3749). | no [MERGE] |
| X-010 | BOTH | 60% | The point has two halves: record shape (V2, events record; V1 has 0 `events.jsonl` hits) and audit placement (V1, MS-04 V1:631; V2 defers `verify-run`, V2:1143). | no [MERGE] |
| C-084 | V1 | 65% | Fix `ensemble.py` in place now (V1:2855; M3-03..M3-07 V1:3886-3890) answers defects V2 itself rates Critical (G-42..G-44, V2:1277-1279). V2's "no change to `cli/reflect`" is only an adjudicated reading with enforcer "none" that says "any edit of `ensemble.py` ... needs its own decision" and itself contemplates an H1 edit at `ensemble.py:601-630` (C16, V2:4445). So the merge carries fix-in-place as the default, explicitly owner-gated (V1 G-65, V1:2316; V2 C16). The V2 advocate agrees (r1-advocate-V2.md line 79). | yes [MERGE] |
| X-043 | V1 | 60% | Same evidence as C-084. On status I keep my Round 1 correction: "DECIDED" is wrong for the remedy; V1:2314 actually argues feasibility and V1:2316 leaves the final choice to the owner, so the corrected wording is "fix in place now (feasible, owner-gated); replace-or-keep at UC-2 Stage 5 is an owner decision". | yes [V2] |
| X-054 | V1 | 65% | Same as C-084 (V1:2855, V1:3890 vs V2:3643, V2:4445); V2's code-owned shadow helpers writing comparison siblings (V2:3643) are compatible and also carried. | yes [MERGE] |
| X-034 | V2 | 55% | V2 2.4 gives file sizes and line-level defects in the script bodies (`diffgate.py:23-25,729-796`, `fix_audit.py:877,1028`; V2:432-448); V1 says "bodies not read, description only" (V1:267-269). V2 has the information; its OQ-01 "all UNVERIFIED" (V2:1025) must be aligned. Not re-checkable here (`~/.claude/` excluded); tag "verified by run 2 only". | yes [NEITHER] |
| C-073 | V1 | 75% | Not actually disputed: the V2 advocate's exception list gives "C-073 and C-093 (CL-14): V1, 70%" (r1-advocate-V2.md line 276); the convergence table recorded the cluster verdict instead. V1 C-14 recount and owner-gated D-1 (V1:2107, V1:2117); V2 has no axis. | no [V1] |
| C-093 | V1 | 75% | Same as C-073 (V1:2832, V1:4372-4375). | no [V1] |
| C-009 | BOTH | 65% | V2's C8 table covers 10 capabilities and states its premise test (V2:1409-1422); V1 adds MS-14, ENS-4, ENS-5 as C8 rows V2 lacks (V1:583, V1:767). Neither covers the other. | yes [V1] |
| X-017 | V2 | 55% | V1 D14 itself names a live caller, the prose at `document_review_loop_prompts.md:70` read by `/sc:spec-panel --mode critique` (V1:602), so the CLI as a whole is not unwired; Important (V2 G-96, V2:1331) fits. V1's sub-finding stands (`ledger defer`, `ledger verdict`, `ledger capture`, `review telemetry` have no caller, V1:602). V2's "(6)" count is wrong (5 lines, 7 occurrences). | yes [V1] |
| X-019 | BOTH | 55% | Split per row: G-123 (no acceptance-evidence definition, V2:1358) meets V2's "target cannot hold" rule (V2:1121) because no use case can be accepted without it, and E1/E2 being one derivation set removes the fallback, so Critical (V2). G-36 / D8 (driving document not delivered) stays Important: V1 records 156 of 665 runs never opened `source.md` with "the causal link stays [UNVERIFIED]" (V1:596). | yes [OPEN] |
| A-008 | BOTH | 60% | Both advocates answered QUALIFY in the same direction (r1-advocate-V1.md line 270; r1-advocate-V2.md line 288): rate the code fact as a defect, set plan priority by the cited driving text and any on-record staging (V1 premise check V1:583; V2 delta row V2:1144). | yes [V1, cluster] |
| X-023 | BOTH | 60% | Diff analyst: "VERIFIED-BOTH (reconcile)": 32 literal keys (`ensemble.py:787-832`) plus conditional `t2_fallback` (`:833-834`) = 33. V1's "33 keys, 11 of them in neither list" (V1:640) is internally consistent because `t2_fallback` has 0 hits in `panel_lint.py`, so 10 + 1 = 11. Both numbers are true for a case; the merge states both with the basis. | no [BOTH] |
| X-024 | BOTH | 55% | Same fact as X-023. The analyst tagged V2 verified and said V1 "does not say which" basis; under the `t2_fallback` basis V1's 11 matches V1's own 33. V1's fault is an unstated unit (conceded, point 9), not a wrong number. | no [BOTH] |
| S-056 | BOTH | 70% | V1's gates carry commands, collected counts and per-test replacement assertions (V1:4033-4055); V2's G17-G27 are gates imposed by adjudicated winners (measurements, kill lines, replays; V2:4482-4492) that the plan also needs once those outcomes are adopted. Base = V1's form. | yes [V1] |
| X-036 | V1 | 65% | New check: `https://arxiv.org/abs/2606.19544` (fetched 2026-11-15) shows the abstract's "verbosity bias is small (<0.011) ... under a single pairwise rubric", matching V2:1647, but the page states "This paper has been withdrawn by arXiv Admin", last revised 3 Nov 2026 (v2). V2 cites the v1 HTML (V2:1648) and builds a takeaway on it (V2:2044) without noting the withdrawal; V1 excluded the figure as unconfirmed (V1:1003). V1's outcome (exclude) is the right one. | yes [OPEN] |
| S-004 | V2 | 60% | V2's numbered 3.1-3.5 with the precedence table first (V2:1114-1227) is the better skeleton for a merged document that adopts adjudications; V1's consumer table C-A..C-E and core diagram (V1:496-520) are carried into it (the V2 advocate agrees, r1-advocate-V2.md line 195). | yes [MERGE] |
| S-022 | V2 | 60% | V2's classified matrix with ABSENT cells, CF/SS/PS/DU and RC/CC tables (V2:830-1110) is the base; V1's "Same data contract? / Same code? / Divergent choices" columns (V1:436-461) are carried. | yes [MERGE] |
| X-008 | V1 | 65% | V2's own Section 1 says PR review needs "an optional per-slot lens" (V2:134); D11 says the per-slot key "stays true for a later panel-engine step" (V2:4510); the C-11 withdrawal covers only the first rf-qa change (V2:1141) and left HIGH invariant C-11 INV-009 open ("no slot id exists in `/task` once the per-slot key was withdrawn", V2:4144). V1's optional `role`/`lens`/`agent` keys (V1 BL-08, V1:612) are additive and are carried as reserved. | yes [V2] |

**Tally:** moved 25 of 38 (C-061, C-090, X-038, X-042, C-052, C-077, X-040, X-056, C-060, X-041, X-057, C-034, C-084, X-043, X-054, X-034, C-009, X-017, X-019, A-008, S-056, X-036, S-004, S-022, X-008); held 13 (S-040, C-005, C-050, C-076, X-051, C-081, C-057, C-083, X-010, C-073, C-093, X-023, X-024). Of the 25 moves, 20 land exactly on the V2 advocate's Round 1 verdict (including C-084, X-043, X-054 and X-008, where that verdict is V1); 4 move from V1 to BOTH where the V2 advocate says V2 (C-061, C-090, X-042, X-019); 1 moves away from the V2 advocate on new evidence (X-036, OPEN to V1).

#### Verdict changes on other points or clusters

| Point or cluster | Round 1 verdict | Round 2 verdict | Why |
|---|---|---|---|
| CL-03 Over-length lines, claim cut | V1 | BOTH | V2's adjudicated repair closes the fail-open path with a dropped-blocking refusal (V2:3516); the claim cut is an OPEN owner decision (X-040, X-056), not a V1 win. |
| CL-06 Dispatch, identity, read-only | V2 | BOTH | The V2-side argument that V1 ignores the raw-id lane's open Bash is false (V1 C-18, V1:2320-2383, V1:2327). V2 contributes the correct restriction mechanism (`--tools`, not `--allowedTools`; V2:1725-1728) and the dispatch-layer analysis (V2:592-655). |
| C-067 Reviewer read-only enforcement (CL-06, inherited V2) | V2 | BOTH | V1 C-18 decides "allowlist everywhere; shell evidence computed by the orchestrator" (V1:2381); V2 adds INV-G and the `--tools` mechanism. V1's `--allowedTools` wording (V1:2332, V1:2381) must be corrected. |
| CL-07 Distinctness default | MERGE | OPEN (default) / BOTH (record fields) | See C-060, C-081, X-041, X-057. |
| CL-09 Reflect Tier 2 engines, post gate | MERGE | V1 on the post gate; BOTH on the rest | Post gate: C-084, X-043, X-054. V2 keeps the exit-script defect (`reflect_shadow_exit.py:313`), the code-owned shadow helpers and the "no engine moves" governance (V2:3643). |
| CL-15 Severity ratings, C8 | V1 | BOTH | V2 wins X-012, X-016, X-017 and the G-123 half of X-019; V1 wins X-011, X-013, X-014, X-015, X-018; C-009 and A-008 are shared. One rubric must be stated and applied per row in the merge. |
| CL-20 Section 8 form, inventory | MERGE | BOTH, with a narrower drop list | Only V1 8.4's layout table A-E (V1:4063-4069) is dropped. V1:4059 (constraint), V1:4061 (facts), V1 8.5 rows that are no-regression risks and V1 8.6 gate operations are carried (point 11 above). |
| CL-23 Section 5 external research | MERGE | BOTH, with one exclusion | X-036: the arXiv 2606.19544 figure is from a withdrawn paper; V2's takeaway at V2:2044 must be dropped or marked "withdrawn source". |
| U-099 (V1 branch layouts) | DROP (keep the constraint) | DROP the layout table only | V1:4061 facts and the rollback-unit sentence are constraints, not a layout. |
| My Round 1 concession 9 (V1 lacks a raw-id read-only requirement) | conceded | withdrawn | False against V1:2327, V1:2381, SC-9 V1:534, K-7 V1:560. |
| My Round 1 concession 8 (only V1:4059 survives from 8.4-8.6) | conceded | narrowed | V1 8.5 is "inputs, not the register" (V1:4073); see point 11. |

#### Corrections to V2 you found

Claims in the V2 advocate's Round 1 or in V2 itself that are wrong, each with the check run this round.

| # | Where | Claim | Check | Finding |
|---|---|---|---|---|
| 1 | r1-advocate-V2.md weakness 8 (line 67), strength 11 (line 49), CL-06 verdict (line 98) | V1's dispatcher "does not price that E2's `claude -p` launcher leaves Bash open (`run-reviewer.sh:48`)" | Grep V1 for "read-only\|allowedTools\|disallowedTools"; read V1:2322-2336 and V1:2379-2381 | False. V1 C-18 states that exact fact with the same citation (V1:2327) and decides an allowlist (V1:2381); SC-9 (V1:534), K-7 (V1:560). |
| 2 | r1-advocate-V2.md weakness 11 (line 70); U-099 reason | "Only the git constraint itself (V1:4059) survives" from V1 8.4-8.6 | Read V1:4057-4121 | Overbroad. V1:4061 is a facts paragraph of constraints; V1 8.5 is labelled "Inputs for the risk register, not the register itself" (V1:4073) and holds no-regression risks (V1:4085-4087, V1:4100); most of V1 8.6 is gate operations (V1:4106-4111, V1:4117). |
| 3 | r1-advocate-V2.md X-036 (line 162); V2 5.1.5 (V2:1647-1648), takeaway (V2:2044) | V2 is right because it read the paper's figure | Fetched `https://arxiv.org/abs/2606.19544` (2026-11-15, Tavily extract) | The figure matches the abstract, but the page says "This paper has been withdrawn by arXiv Admin", last revised 3 Nov 2026 (v2). V2 cites the v1 HTML and does not mention the withdrawal. Not checked: the withdrawal reason (not shown on the page). |
| 4 | r1-advocate-V2.md weakness 2 (line 61) and X-042 (line 168) | C-12's acceptance "needs human pair labels ... that do not exist (V1:1988)"; `cluster_v2` leaves anchor-only findings as singletons | Read V1:1984-1989 and V1:4098 | V1:1988 does not say the labels are missing; V1:4098 says they are pending and refuses to present AI labels as measured accuracy. V1:1988 also includes "an anchor-to-citation step", which answers the singleton objection in the cited line. The status-label criticism stands; the implication of a hidden gap does not. |
| 5 | r1-advocate-V2.md weakness 3 (line 62) and corrections table row 16 (line 374) | "findings-v1 is a strict subset of findings-v2" is a false V1 claim at HEAD | Read V1:1211, V1:2823, V1:3834, V1:3065 | V1 presents the subset as a build target (M1-01, V1:3834; Cons row V1:1211 "needs code and tests"). Only the constraint row V1:3065 reads as present tense and needs rewording. |
| 6 | V2 7.1 row 2 (V2:3743) | "195 of 1,398 multi-member rows chained" | Read V2:3743 | Same wrong unit as G-133 (X-021): 1,398 is all rows. The V2 advocate's correction row 3 names "7.1 element 2"; this is that line. |
| 7 | convergence-r1.md rows C-073, C-093 | The V2 advocate's verdict is MERGE (cluster) | Read r1-advocate-V2.md line 276 | The V2 advocate gave an explicit exception "C-073 and C-093 (CL-14): V1, 70%". These two points are agreed (V1), not disputed. This is a tally error in the convergence table, not a V2 error. |
| 8 | r1-advocate-V2.md CL-09 framing and V2 axis 8 (V2:3643) read as "V2 forbids edits to `cli/reflect`" | — | Read V2 C16 (V2:4445) | V2 holds "no change to `cli/reflect`" only "in the weak reading", with enforcer "none (a reading adopted by two debates)", and says "any edit of `ensemble.py` ... needs its own decision"; it even lists an H1 edit at `ensemble.py:601-630`. So V1's fix-in-place conflicts with no binding constraint, only with an owner decision both reports require. |

Corrections to V1 found or confirmed this round (for the merge): V1:2332 and V1:2381 name `claude -p --allowedTools` as the read-only mechanism; it must become `--tools` or `--disallowedTools Bash` (V2:1728). V1:381 "37 files" becomes 38. V1:3065 "strict subset of v2" becomes "target: v1 lines accepted by the v2 validator (M1-01)". V1:4116 and V1:4119 are rewritten (owner branch naming; E2 as of `6c09843`, newer `e2f2ac268` folded in later). The Round 1 correction list for V1 (r1-advocate-V1.md lines 379-389) otherwise stands.

#### Must-carry content for the merge

**From V1** (none of it found false this round, except as corrected above):
1. Verified code facts V2 gets wrong: the citation-only path (BL-04, V1:608), 1,398 is all rows (DOC-18, V1:680), the 6-vs-5 calibrator mismatch (V1:171), the 0.704 mixed definitions (V1:162), shadow09's 0.9328 (V1:163), `ensemble.py` provenance (V1:414).
2. Defects only V1 has: `unauthorized_deviation_present` with no producer (MS-14, V1:641), no `merge_method` and no `merged-verdict.yaml` writer (MS-24, V1:651), no `REPORT.md` or per-task verdict matrix from the post gate (ENS-4, V1:655), PR router-vs-rubric divergences and `deep=True` dormancy (BL-16, BL-17, V1:620-621), judge sees the combo name (V1:208), S-ID identity probes (V1:167).
3. Decisions only V1 has, as owner-gated items: panel size and Tier 2 cost with D-1 (C-14, V1:2107-2117), calibration as a routing signal (C-06, V1:1602), invalid-block policy (C-15, V1:2184), the clustering remedy with its acceptance metric (C-12, V1:1988; labels pending V1:4098) and D6 as the likely T-c trigger, reviewer read-only allowlist (C-18, V1:2381, mechanism corrected).
4. Post-gate fix-in-place as the default, owner-gated (C-17, V1:2316; M3-03..M3-07, V1:3886-3890), consistent with V2 C16.
5. Implementer-grade no-regression content: 8.3 gates with commands, collected counts and replacement assertions (V1:4033-4055); persisted-format and rollback rules (M1 intro V1:3830, M1-12 V1:3845, V1:4100); the 8.4 facts paragraph (V1:4061); 8.5 rows that are no-regression risks (V1:4085-4087, V1:4100); 8.6 gate operations (V1:4105-4118, two items rewritten); the 48 steps as per-item migration content re-based on the merged design, with ordering language removed (U-096); the gap-to-step coverage check rebuilt over the merged gap list (V1:3910-4030); track tags as "destination module" (V1:761).
6. The 6.D defect-to-test table (V1:2517-2538), 6.E implementer detail (V1:2624-2807, rows tied to non-adopted designs tagged conditional), X1-X14 exposures (V1:2984-3006), SC-18..SC-22 and the SC-6, SC-10, SC-14 pass rules (V1:531-547), optional per-slot `role`/`lens`/`agent` keys as reserved (V1:612; X-008).
7. Section 5.2-5.4 research on severity, calibration and clustering (V1:853-1079), with the exclusion of the arXiv 2606.19544 figure (V1:1003).
8. Owner items O-1..O-6 incl. issues #525-#530 (V1:4136-4141).

**From V2:**
1. Evidence base: HEAD and E2 tip `6c09843` (V2:108), [POST-BASELINE] `e2f2ac268` (Q-39); collaboration and process-redesign facts, options and dormant outcomes with triggers (V2 2.3, 6.6, 6.7, A-18, A-19); re-derived E2 numbers and the `fullpkg()` bug (V2:294-320); Stage 2 failure mechanisms and the `reflect_shadow_exit.py:313` defect (V2:207-229).
2. Evaluation: E1 and E2 one derivation set (sha256 `044809e3...`, V2:278, V2:322) and three-tier acceptance (axis 9, V2:3644); G-123 as Critical.
3. Adjudicated design as "adjudicated default, partial" with margins, conditions and the 60 open HIGH invariants (V2:3654-3671; 7.3): thin shared contract with per-module engines and triggers T-a/T-b/T-c (V2:3636), ledger axis 4 with G-14/G-15 (V2:3639, V2:1249-1250), typed `blocking` plus CRITICAL floor and `min(2, requested)` quorum (A-3, A-4), C-06 repair and drop record (V2:3516), `events.jsonl` run record (A-10), launcher gating and the core launching nothing (axis 5, V2:3640), dormant collaboration designs.
4. Precedence table rebuilt against the merged Section 7 (V2:1125-1144); Q-40 (owner wording) kept open.
5. Binding constraints C1-C29 (V2:4430-4458) incl. C4's observed git-ref output and the `verify-sync` pre-commit correction; dependency facts D1-D26 with D9 corrected; acceptance AE-1..AE-15 (V2:4529-4549); per-consumer verdicts (V2:3842-3849); adjudicated gates G17-G27 (V2:4482-4492).
6. External research on hooks/headless, `--tools` vs `--allowedTools`, git refs, stacked PRs and finding schemas (V2:1698-2036), minus the withdrawn-paper takeaway (V2:2044).
7. The 171-row defect register and the 5,950-row inventory as named inputs with re-routing (S-048, A-056); Q-01..Q-93 with sources.
8. The 0.75 vs 0.80 convergence-threshold conflict (`SKILL.md:703` vs `contract.py:321`).

**False or unsafe content that must not be carried as stated:** V2's `KeyError` crash on the merge path (nine sites incl. V2:3637 and D9 V2:4508); V2's [UNVERIFIED] calibrator tag; V2's 1,398 "multi-member" label (incl. V2:3743); V2's "first-parse" 0.704; V2's "all 1.000" `cluster_agreement`; V2 G-06 as Important; V2 "50 test files" and "(6)"; V2's verbosity takeaway from a withdrawn paper; V1's `--allowedTools` mechanism; V1's 43 call sites, Qwen "3 of 3", audit D wording, "37 files"; V1's "DECIDED-BY-EVIDENCE" labels for C-01, C-12 and the C-17 remedy; V1's branch layout table A-E.

#### Remaining disagreements (if any) and final evidence

1. **CL-01 end state (C-005, C-050, C-076, X-051, S-040): BOTH vs the V2 advocate's V2.** I accept V2's shape as the governing default. The disagreement is only whether V1's superset core stays in the merged document as the documented one-engine target. Final evidence: the owner's "thin modules" wording and V2's own flag (V2:3582); V2's T-c is satisfied by any non-helper fix of D6, which is measured on both clusterers (V2:3636; V1:594); and without V1's target text, a plan reaching T-a/T-b/T-c would have no design to converge to.
2. **Clustering (C-061, C-090, X-042): BOTH vs V2.** V2 keeps the measured v1 over-merge (83 mega-rows, audit D replays `findings.py` rules, V2:1361) with no named remedy (V2:3743). V1's remedy and acceptance metric (V1:1988) apply under either shape.
3. **Run record (C-057, C-083, X-010): BOTH vs V2.** V1's built-in audits before `published` (V1:631) are not in V2, which defers `verify-run` (V2:1143); V2's debate margin for its own record design is 0.13 percent (V2:3661).
4. **X-023, X-024: BOTH vs V2.** V1's 33 and 11 are both true under the `t2_fallback` basis (`ensemble.py:833-834`; 0 hits in `panel_lint.py` per the analyst); the defect is an unstated basis.
5. **X-036: V1 vs V2.** The source is withdrawn (fetched page). If the V2 advocate can show the figure in a non-withdrawn source, I would move to BOTH.
6. **X-019: BOTH vs V2.** G-123 Critical (V2), G-36/D8 Important (V1), because the causal link of D8 is [UNVERIFIED] in V1 (V1:596) and V2 gives no measurement that changes that.
7. **C-081: BOTH vs OPEN.** The default is OPEN (agreed); the record fields of both reports are additive and conflict nowhere.

Everything else in the 38 is now agreed with the V2 advocate's Round 1 verdict.

### Variant 2 Rebuttal

#### Round 2 Rebuttal: Advocate for Variant 2 (run 2 research report)

- Debate: /sc:adversarial Mode A, depth standard, Round 2 (sequential rebuttals; the V1 advocate went first, this file answers it)
- V1 = `adversarial/variant-1-original.md` (4,476 lines); V2 = `adversarial/variant-2-original.md` (5,098 lines)
- Inputs read: `partials/convergence-r1.md`, `partials/r2-advocate-V1.md`, `partials/r1-advocate-V1.md`, `partials/r1-advocate-V2.md` (all in full), `partials/orchestrator-verification.md`, and the `diff-analysis.md` rows of the disputed points
- Citation form: `V1:L` / `V2:L` = line of the variant file; bare ids (S-, C-, X-, A-, U-) = `diff-analysis.md` ids; ids inside a report carry a "V1"/"V2" prefix. Verdict labels: V1 / V2 / BOTH / NEITHER / OPEN; my Round 1 "MERGE" counts as BOTH (not a move)
- Read-only: only this file was written; no git write; nothing under `.claude/` or `~/.claude/` read; no web fetch (not authorised). New checks this round: Read of V1:996-1007, 1982-1989, 2318-2385, 4057-4120; V2:1640-1650, 1718-1731, 2038-2047; single-line reads of V1:596, 631, 640, 1665, 2845 and V2:134, 1135, 1141, 1143, 1271, 1358, 1361, 1368, 3511, 3582, 3636, 3644, 3661, 3743, 3771, 4144, 4445, 4510, 2184; Grep of `.dev/` for `2606.19544` and of the run 2 task folder for `P6-054`; `claude --help` (local CLI 2.1.325); a key count of `ensemble.py:785-836`, `grep -c t2_fallback panel_lint.py`; `git rev-list --count origin/master..HEAD` and `git diff --stat origin/master HEAD -- src/superclaude/cli/review`

(Sections are appended one at a time below.)

#### Response to V1's criticisms

Items 1-9 answer the nine "Weaknesses identified in Variant 2" (r1-advocate-V1.md lines 45-53). Items 10-17 answer the Round 2 file (r2-advocate-V1.md), including its two claims that my Round 1 criticisms were wrong. Items 18-21 are the high-risk re-checks the orchestrator asked for.

1. **False `KeyError` fact used as decision evidence (V1 weakness 1).** **Conceded in full (as in Round 1, concession 1).** The nine sites stand as listed (G-01 V2:1236, SC-01 V2:1177, G-99 V2:1334, 6.1 V2:2177, CO-1 V2:3330, axis 1 option D V2:3636, axis 2 evidence V2:3637, C-2 V2:3882, D9 V2:4508). One limit on the damage: the C-01 debate that decided the core shape moved to its outcome "after both advocates verified that a citation-only line is rejected at `findings.py:104` before it reaches `annotate`" (V2 6.12.9.1 row C-01, V2:3511), so the adjudicated shape rests on the correct fact; only the axis-2 evidence sentence and D9 carry the wrong one.

2. **Severity rubric applied inconsistently (V1 weakness 2).** **Conceded for G-06 and G-24; answered for G-42/G-43.** G-06 Important contradicts V2's own rubric (V2:1121 vs V2:1241); G-24 Critical rates the adjudicated target's own "core launches nothing" (V2:1259 vs V2:1139). For G-42/G-43 the delta row says the Critical ratings are "statements about today's code" (V2:1144), which is coherent; the tension the V1 advocate names (Critical, yet axis 8 moves no engine) disappears in the merge, because both advocates now agree the post gate is fixed in place, owner-gated (C-084, X-043, X-054 V1; V2 C16 permits it with "its own decision", V2:4445).

3. **True facts tagged [UNVERIFIED], counts that do not reproduce (V1 weakness 3).** **Conceded** (calibrator V2:891, V2:1033; OQ-01 V2:1025 vs 2.4 V2:432-448; "(6)" at V2:1331; 1,398 at V2:1368 and V2:3743). New this round, a further V2 source-tier error from V2's own QA: "Rating Roulette" (arXiv 2510.27106) is listed "peer review not confirmed" (V2:1648) while run 2's phase-6 QA recorded "arXiv shows 'Accepted at EMNLP 2025'" (`TASK-RESEARCH-review-panel-run2-20261114-075454/qa/qa-consolidated-findings-phase6.md:76`, row P6-054).

4. **Two designs in one document (V1 weakness 4).** **Conceded for the residual text, defended for the mechanism.** SC-17 (V2:1193), G-85 (V2:1320), 3.5 (V2:1227) and SC-04 (V2:1180) lag the delta rows (V2:1132, V2:1137, V2:1138). The delta table (V2:1125-1144) is the right mechanism for a document whose Section 7 overrode Sections 3-4; the merge should fold the governing cells into the merged text and keep the table as a change record.

5. **Debate winners written as governing although narrow (V1 weakness 5).** **Conceded on the label, not on hiding.** Each choice row carries margin, tiebreaker level, convergence, conditions and open HIGH invariants (V2:3654-3671; 60 HIGH open, 7.3). I accept that the governing text must say "adjudicated default, partial" (A-052). I also concede the C-05 detail: "B ahead; the tiebreaker selects A" (A 0.8728, B 0.8904; V2:3664) must be stated wherever A-13 is used.

6. **Section 8 gives constraints but not test edits, rollback or a gap map (V1 weakness 6).** **Conceded** (my Round 1 concession 6). U-097, U-100, U-101 come from V1.

7. **Measured clustering defect left in place (V1 weakness 7).** **Conceded this round; I move C-061, C-090, X-042 to BOTH.** Check: V2's Section 3 target was "One cluster rule with a chain guard" (V2:1164); after adjudication it became "Two deterministic merges, one per engine ... A verified merge defect is fixed in the engine that has it" (delta row, V2:1135; 7.1 element 2, V2:3743), and the defect-family row puts the "chain guard in the v2 engine" only (V2:3771). The v1 `findings.cluster` keeps union-find with no chain guard (V2:1368, V2:3331), and audit D's 83 mega-rows replay those v1 rules (`audit2.py` "copies `findings.py` rules", V2:1361). So V2 names no remedy for a measured v1 over-merge. My Round 1 objection ("`cluster_v2` leaves anchor-only findings as singletons") is answered in the very V1 line I cited: "an anchor-to-citation step" (V1:1988). New interaction the merge must state (see item 15): applying V1's remedy to both clusterers is "a non-helper edit to ... both clusterers", which is V2's convergence trigger T-c (V2:3636).

8. **Decisions missing (V1 weakness 8).** **Conceded**, with one narrowing: V2 does have loss accounting for invalid content (itemised drop record with `blocking_state`, dropped-blocking refusal, V2:3516, V2:1135), but not V1's reviewer-level policy "keep valid lines, mark the reviewer `partial`, never let an invalid reviewer clear a row" (V1 C-15, V1:2184). Panel size and cost (V1 C-14), calibration (V1 C-06), the `unauthorized_deviation_present` producer (MS-14), `merge_method` (MS-24) and `REPORT.md` (ENS-4) are V1-only and must be carried.

9. **"Thin module" stretched (V1 weakness 9).** **Conceded as a fact, defended as disclosure.** The spec-review module keeps the v1 parser, ledger and clustering (V2:3578), and V2 says so and asks the owner (V2:3582, Q-40). That is an open owner question, not a hidden defect; it stays Q-40 in the merge.

10. **Claim that my Round 1 weakness 8 ("V1's dispatcher ignores the raw-id lane's open Bash") is false (r2-advocate-V1.md point 8, correction row 1).** **Conceded in full; withdrawn.** Re-read V1 "C-18: Read-only enforcement for reviewers" (V1:2320-2385): the E2 row states the exact fact with the same citation ("A deny list `--disallowedTools Edit Write NotebookEdit` under `bypassPermissions`; Bash stays available and auto-approved; the judge has no deny list at all", `run-reviewer.sh:48`, V1:2327; again at V1:2374), and the resolution is "allowlisted reviewer agents or an equivalent `claude -p` allowlist ... test the `claude -p` allowlist behaviour before relying on it (G-45)" (V1:2381). C-18 covers "every reviewer" (V1:2332), so it binds V1's `cli-model` adapter (C-09, V1:1792) too. V1 even goes further than V2 on rf-qa: it records that `rf-qa.md` declares Bash and calls it "the primary verification surface" and leaves Q-61 open (V1:2383). What remains of my point is narrower and is item 12.

11. **Claim that my Round 1 weakness 11 ("only V1:4059 survives from 8.4-8.6") is overbroad (point 11, correction row 2).** **Conceded in part.** Re-read V1:4057-4120. Correct: V1:4061 is a facts paragraph of constraints; 8.5 is headed "Inputs for the risk register, not the register itself" (V1:4073); most 8.6 items are gate operations. Three limits on the concession: (a) one V1:4061 fact is stale: "the branch `ironbelly/shadow-runs` is 3 commits ahead of `origin/master`" is now 5 (`git rev-list --count origin/master..HEAD` = 5), while "the `cli/review` package on this branch equals `origin/master`" still holds (`git diff --stat origin/master HEAD -- src/superclaude/cli/review` empty); (b) the 8.6 PR item (V1:4115: remote check, rebase, `/sc:pr-submit --monitor 3`, URL check) is PR-process content that restates project rules the owner already fixed, so it is referenced, not carried; (c) the last 8.6 item ends "mark the steps that wait on each" (V1:4120), which is ordering language and goes with the schedule exclusion. V1:4116 (8.4 layout) and V1:4119 (E2 pin `4a22d74`) are rewritten, as the V1 advocate says.

12. **V1 is wrong about `claude -p --allowedTools` (point 8).** **Agreed; this is V2's remaining contribution on read-only.** V2 5.2.4 (V2:1725-1728): `--allowedTools` "lists tools that run WITHOUT a permission prompt; it does NOT restrict availability"; "use `--tools` or `--disallowedTools Bash`, not `--allowedTools`". V1 names `--allowedTools` as the mechanism (V1:2332, V1:2381); its own Cons cell flags it as untested (V1:2342). Local check (item 19) supports V2's mechanism. Under `bypassPermissions`, which V1 itself records for the E2 launcher (V1:2327), a pre-approval list adds nothing, so V1's mechanism would not have restricted Bash.

13. **Correction row 4: my Round 1 said C-12's human labels "do not exist" (V1:1988).** **Conceded on wording.** V1:1988 names the labels as the acceptance condition; V1:4098 says they are pending and refuses to present AI labels as measured accuracy. "Pending" is the right word. The status point (V1:1986 calls the remedy "DECIDED-BY-EVIDENCE") still stands and the V1 advocate concedes it.

14. **Correction row 5: "strict subset" is a build target, not a claim about today.** **Conceded**, except V1:3065, which the V1 advocate also concedes must be reworded. My Round 1 correction row 16 is narrowed to that line plus V1:2823/V1:2839, which read as design statements and must carry "target: requires `findings_v2.py:96-97,279-281` to change".

15. **Point 12, CL-01: "without V1's target text, a plan reaching T-a/T-b/T-c would have no design to converge to" (r2-advocate-V1.md, Remaining disagreement 1).** **Rejected as stated.** V2 carries a one-engine alternative inline: axis 6.1 "Option A: v2 kernel as the core, v1 loop as a thin module" with its effort basis (V2:2184), and the C-01 outcome names the convergence path: "if one fires, the recorded path is A's one-engine design after an anchor-span precondition" (V2:3511). V1's superset (V1:2823) adds detail to that alternative (pluggable lens, category and location namespaces, layer diagram V1:2544-2555, future-consumer fit rows V1:2618), so it is carried as enrichment of that one alternative, not as a second "target". The V1 advocate's T-c argument is right in substance and stronger than it says: once the merge adopts V1's clustering remedy for both engines (item 7), T-c is met by the merge's own content, so the plan must either apply the remedy to the v2 engine only (and record the v1 over-merge as accepted) or take the one-engine path. That is a decision the merged document must surface, not settle.

16. **Point 12, CL-08 and Remaining disagreement 3: "V2 defers `verify-run` (V2:1143)".** **Half right.** V2 defers only a *kernel* `verify-run` command; it assigns the verifier now: "the verifier (identity, completeness, conservation, seeded from audits B, D and F) ... a tested `scripts/` plus `tests/` set that reads the kernel and never writes it" (axis 9, V2:3644; delta row V2:1143 "Narrowed"). The real difference with V1 is placement: V1 runs audits A and D "as built-in checks before `published`" (V1 MS-04, V1:631; C-07, V1:1665, V1:2845), V2 runs them outside the publish path. I move C-057, C-083, X-010 to BOTH on that basis (record shape V2; check placement an open design choice with both positions carried). V1's manifest-as-record was rejected in V2's debate because it "inherits the lock-free write" (V2:3661); the V1 advocate already conceded the race (C-034 to V2).

17. **Point 12: "V2's verbosity takeaway rests on a paper arXiv now shows as withdrawn" (X-036).** **Conceded; I move X-036 to V1.** Evidence in item 18.

### High-risk re-checks

18. **X-036 (arXiv 2606.19544 withdrawn).** I could not fetch the page (web fetch not authorised), so the withdrawal is **not verified by me**. It is, however, **corroborated by a second, independent in-repo record that predates this debate**: run 2's own phase-6 QA, row P6-054 (`.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/qa/qa-consolidated-findings-phase6.md:76`): "arXiv shows that paper as WITHDRAWN by arXiv Admin on 2026-11-03 (v2: 'does not meet arXiv's research content quality standards'); the withdrawal predates the report date and is not mentioned", evidence "Tavily extract of https://arxiv.org/abs/2606.19544". The row was graded "minor under grading override" (same file, :164) and left unfixed, so V2 shipped with a known withdrawn source. The paper feeds V2 5.1.5 (V2:1647: the 33-41 point kappa deflation, 14 ranking positions, 541,000 judgments and the <0.011 verbosity figure) and takeaway 1 "Verbosity bias appears much smaller in recent judges" (V2:2044). V1 excluded the verbosity figure (V1:1003), for a different reason (blog-attributed, primary not confirmed), so V1's outcome is right and its stated reason must gain "source withdrawn per arXiv, recorded by run-2 QA P6-054". Status for the merge: "withdrawal [UNVERIFIED by this advocate; recorded independently by run-2 QA and the V1 advocate's fetch]". The chance-corrected-agreement point survives on 2510.27106 and the three blogs (P6-054 says the same).

19. **`--tools` versus `--allowedTools` (V2:1725-1728 vs V1:2332, V1:2381).** Local `claude --help` (Claude Code 2.1.325): `--tools <tools...>` "Specify the list of available tools from the built-in set. Use "" to disable all tools ... or specify tool names"; `--restricted` "removes the built-in tools that run commands or code (Bash, ...) ... unless --tools names them"; `--allowedTools` "list of tool names to allow"; `--disallowedTools` "list of tool names to deny". The help text supports V2's mechanism (`--tools` sets availability; `--restricted` and `--disallowedTools Bash` remove Bash). The specific sentence "`--allowedTools` does NOT restrict availability" is from V2's cited docs (V2:1726) and is not stated verbatim in the local help, so it is consistent with, not proven by, this check. Verdict: V2's mechanism, V1's requirement (C-18).

20. **33 vs 32 keys (X-023, X-024).** Re-counted: 32 key lines in the dict literal at `ensemble.py:785-836`; `t2_fallback` added only `if t2_fallback is not None` (`:833-834`); 0 hits for `t2_fallback` in `panel_lint.py`; the default path is "byte-equivalent to today (t2_fallback=None)" (`ensemble.py:363`). So the default contract has 32 keys, 10 outside both lists; with the fallback flag on, 33 and 11. V2 states the executed default with its basis ("R06: executed probe (1.0, 32 keys, 10 outside lists ...)", V2:1430; V2:179). V1 states 33/11 as what `ensemble.py:886-895` "writes" with no condition (V1:640, V1:3687), which is wrong for the default run and true only with the flag. Both numbers are true for a stated case; I move to BOTH for the merge (state both with the condition), with the note that V1's sentence as written describes the non-default case.

21. **Open-Bash risk of the raw-id lane (V1 C-18 V1:2320-2383 vs V2 axis 5 V2:3640).** Both reports have the risk and both require process-level read-only before the lane is used by a consumer. V1's contribution: the decision (allowlist everywhere; shell evidence computed by the orchestrator; V1:2381), E3's re-review `diff -w`/`grep -nF` conflict (V1:2375) and the rf-qa Bash dependency (V1:2383, Q-61). V2's contribution: the correct CLI mechanism (V2:1728), the launcher gating G1 identity / G2 read-only / G3 no regression and "the core launches nothing" (V2:3640), and per-consumer verdicts (V2:3842-3849). CL-06 and C-067 go to BOTH.

#### Updated assessment of V1

**Steelman (stronger than in Round 1).** V1 is more right than I credited on the two places where I attacked it hardest. On read-only it already holds the decision a plan needs: one conflict, C-18, states the E2 open-Bash fact with the launcher line, rejects the deny list because "Bash can still write through redirects, `sed -i` or git" (V1:2356), decides an allowlist for every reviewer with shell evidence moved to the orchestrator (V1:2381), and flags the one consumer the decision may break, rf-qa, with a concrete evidence test (V1:2383, Q-61). On Section 8 its "risk" and "checklist" blocks are mostly no-regression content: persisted artifacts reloading, HEAD-relative reflect pins passing trivially after a commit, the false-green post gate, the 13 recorded shadow manifests re-validated by `reflect_shadow_exit.py` (V1 8.5, V1:4073-4100), and gate operations such as re-collecting 1182 tests and running G8 before any commit near the reflect skill (V1 8.6, V1:4105-4118). On clustering it is the only report with a remedy and an acceptance metric for a measured over-merge (V1:1988), and V2's adjudication left the v1 engine with no chain guard (V2:1135, V2:3771). Add the Round 1 strengths both advocates already accept: the verified facts V2 got wrong (`KeyError` path, 1,398 unit, calibrator 6-vs-5, 0.704 definitions, shadow09 0.9328, `ensemble.py` provenance), the gates with commands, collected counts and replacement assertions (V1:4033-4055), persisted-format and rollback rules (V1:3830, V1:3845), the gap-to-step map (V1:3910-4030), the post-gate fix-in-place (V1:2314-2316) and the V1-only decisions (C-14, C-06, C-15). For the parts a `/sc:workflow` plan executes against, V1 is the more usable hand-off, and its source exclusion on the withdrawn paper (V1:1003) was the safer call.

**What changed in my assessment this round.**
- **Up for V1:** C-18 (my Round 1 weakness 8 was false); 8.4-8.6 content (my weakness 11 was overbroad); the clustering remedy (V2 has none for v1); the X-036 exclusion; X-019, where V1's Important for D8 matches the unverified causal link that V2 itself tags [UNVERIFIED] at G-36 (V2:1271) and that I wrongly called "measured" in Round 1 (r1-advocate-V2.md line 145).
- **Down for V1 (new this round):** the read-only mechanism V1 names (`--allowedTools`, V1:2332, V1:2381) would not restrict anything under the `bypassPermissions` launcher V1 itself describes (V1:2327); one V1:4061 fact is stale ("3 commits ahead", now 5); V1's "33 keys ... written" (V1:640) is the non-default case; V1's clustering remedy is written for "one clusterer on the v2 location model" (V1:1988), which under the adopted two-engine default is reachable only through V2's trigger T-c (V2:3636), so the merge cannot adopt it unchanged.
- **Unchanged:** V1's stale E2 pin and absence of collaboration and process redesign (C-001, C-028; conceded by the V1 advocate); its over-labelled DECIDED statuses (V1:2830; conceded); the E2 numbers V1 took from hand-offs (V1:191; conceded); no evidence-independence finding (U-042; conceded).

**Net.** V2 stays the better base for scope, evidence baseline, evidence independence, adjudicated defaults with conditions, the precedence record and the binding constraints. V1 supplies verified corrections, implementer-grade gates and migration content, the read-only decision, the clustering remedy and the decisions V2 lacks. Both advocates now agree on this split; what remains is labelling on three CL-01 points (see the last section).

#### Final verdicts on the 38 disputed points

"Moved" compares with my Round 1 verdict (in brackets); MERGE relabelled BOTH is not a move. Where the V1 advocate moved to my side I checked the evidence it gives; each such row says "checked".

| Point | Final verdict | Confidence 50-99% | Evidence | Moved? (yes/no vs Round 1) |
|---|---|---|---|---|
| S-040 | BOTH | 65% | Option sets: V2 6.1 A-D incl. "fix the harness only" (V2:2158-2238, A at V2:2184); V1 6.X adds the layer diagram (V1:2544-2555) and future-consumer fit rows (V1:2618). Base = V2's set; V1's fit rows and diagram carried into V2's Option A. | yes [V2] |
| C-005 | V2 (governing), V1 detail carried | 60% | Governing shape = V2's thin shared contract, "adjudicated default, partial" (V2:3511, V2:3578). The one-engine alternative already exists in V2 (6.1 Option A, V2:2184; "recorded path is A's one-engine design", V2:3511); V1's superset (V1:494) enriches it and Q-40 (V2:3582) stays open. Not BOTH as "a second target". | no [V2] |
| C-050 | BOTH | 60% | Same as S-040 at axis level: V2's Option C adjudicated with triggers (V2:3636); V1's Option B XL / Medium-High (V1:2578-2579) carried as the detailed form of the one-engine option. V1's rejection of C (V1:2622) is aimed at a weaker C (conceded by the V1 advocate). | yes [V2] |
| C-061 | BOTH | 60% | Placement V2 (one clusterer per engine, V2:3743); remedy V1 (complete-link admission, no merge on an empty location, anchor-to-citation step, acceptance by the 83 mega-rows falling plus pending labels; V1:1988, V1:4098). V2 has a chain guard in the v2 engine only (V2:3771). Applying the remedy to both clusterers fires T-c (V2:3636); the merge must surface that choice. | yes [V2] |
| C-076 | V2 (governing), V1 detail carried | 60% | Same as C-005 at Section 7 (V2:3578 vs V1:2823). | no [V2] |
| C-090 | BOTH | 60% | Same as C-061 at Section 7 (V2:3743 vs V1:2850, V1:1988). | yes [V2] |
| X-038 | V2 | 65% | Agreed (V1 advocate moved; checked): V1's start needs v2 to accept `prior` lines and `calibrated_confidence` (`findings_v2.py:96-97,279-281`; V1's own Cons, V1:1211). | no [V2] |
| X-042 | BOTH | 60% | My Round 1 objection is answered at V1:1988 ("anchor-to-citation step"); V2 names no v1 remedy (V2:1135, V2:3743). Same T-c caveat as C-061. | yes [V2] |
| X-051 | V2 (governing), V1 detail carried | 60% | Same as C-005; end shape not evidence-decided (X-052 agreed), V2's adjudicated default governs with Q-40 open. | no [V2] |
| C-052 | BOTH | 65% | Agreed (checked): V2's repair and drop record (V2:3516) as base, V1's loss breakdown 24/14/10/1 (V1:527) and missing-anchor rule (V1:1315). | no [BOTH] |
| C-077 | BOTH | 60% | Agreed: same as C-052 at Section 7 (V1:2840 vs V2:3638). | no [MERGE] |
| X-040 | OPEN | 60% | Agreed (checked): both close the fail-open path (V1:527; V2:3516); the claim cut (10 of 49 losses, precedent `card_convert.py:200-201`) vs re-ask/limit is unmeasured (K2). Owner decision. | no [OPEN] |
| X-056 | OPEN | 60% | Agreed: same as X-040 at Section 7 (V1:2840 vs V2:3638, V2:3656). | no [OPEN] |
| C-060 | OPEN | 60% | Agreed (checked): silence removal agreed (V1:1443; V2:3657); default unmeasured (V2 A-6 "soft stands until A's M1"). | no [OPEN] |
| C-081 | BOTH (record fields); default OPEN | 55% | Fields are additive: V2 `requested_slots`, `distinct_models`, tier-file guard (V2:3657); V1 per-slot `none/model/class`, optional `replicas`, optional `role/lens/agent`, `tiers_as_of` (V1:2842). Exclusion: V1's launch grammar `<adapter>:<argument>` in the same cell conflicts with "the core launches nothing" (V2:3640) and is carried only as a conditional option. | yes [OPEN] |
| X-041 | OPEN | 60% | Agreed (checked): code soft today (`panel.py:509,575`, orchestrator); no strict-vs-soft measurement. | no [OPEN] |
| X-057 | OPEN | 60% | Agreed: same as X-041 at Section 7. | no [OPEN] |
| C-034 | V2 | 70% | Agreed (checked): V2's writer/cost table with the `model_scores` double count and the `manifest.save` lost update (V2:569-578); V1 has no race design (V1 advocate's Grep). | no [V2] |
| C-057 | BOTH | 60% | Record shape V2 (`events.jsonl` written only by code, A-10, V2:3661; V1's manifest-as-record "inherits the lock-free write", same line). Check placement differs: V1 audits A and D "before `published`" (V1:631, V1:1665); V2 verifier as tested `scripts/` reading the kernel, seeded from audits B, D, F (V2:3644). Both carried; placement is a design choice. | yes [V2] |
| C-083 | BOTH | 60% | Same as C-057 at Section 7 (V1:2845 vs V2:3661, V2:3644). | yes [V2] |
| X-010 | BOTH | 60% | Same two halves (record shape V2; check placement both). Correction to the V1 advocate: V2 does not defer verification, only a kernel `verify-run` command (V2:1143, V2:3644). | yes [V2] |
| C-084 | V1 | 65% | Agreed (checked): fix `ensemble.py` in place now (V1:2855; M3-03..M3-07, V1:3886-3890) answers V2's own Critical G-42..G-44 (V2:1277-1279); V2 C16 requires "its own decision" for any `ensemble.py` edit (V2:4445), so it is owner-gated. | no [V1] |
| X-043 | V1 | 60% | Agreed: same as C-084; status wording "fix in place now (feasible, owner-gated); replace-or-keep at UC-2 Stage 5 is an owner decision" (V1:2314-2316). | no [V1] |
| X-054 | V1 | 65% | Agreed: same as C-084; V2's code-owned shadow helpers writing comparison siblings (V2:3643) also carried. | no [V1] |
| X-034 | V2 | 55% | Agreed (V1 advocate moved): V2 read the script bodies (V2:432-448); its OQ-01 "all UNVERIFIED" (V2:1025) must be aligned; tag "verified by run 2 only" (`~/.claude/` excluded here). | no [V2] |
| C-073 | V1 | 75% | Not disputed: my Round 1 exception list gives "C-073 and C-093 (CL-14): V1, 70%" (r1-advocate-V2.md line 276); the convergence table recorded my cluster verdict instead. Checked. | no [V1] |
| C-093 | V1 | 75% | Same as C-073 (V1:2832, V1:4372-4375). | no [V1] |
| C-009 | BOTH | 65% | Agreed: V2's C8 table, 10 capabilities (V2:1409-1422); V1's MS-14, ENS-4, ENS-5 C8 rows (V1:583, V1:767). | no [BOTH] |
| X-017 | V2 | 55% | Agreed (V1 advocate moved; checked): D14 itself names a live prose caller (V1:602), so Important; V1's sub-finding (four subcommands with no caller) kept; V2's "(6)" becomes 5 lines / 7 occurrences. | no [V2] |
| X-019 | BOTH | 60% | Split per row: G-123 Critical (V2:1358: no acceptance definition; E1/E2 one derivation set). G-36 / D8 Important: V2's own G-36 says "Whether naming `source.md` changes how often it is read is [UNVERIFIED] (... an inference)" (V2:1271), and V1 D8 says "the causal link stays [UNVERIFIED]" (V1:596). My Round 1 "measured H1 lever" was wrong. | yes [V2] |
| A-008 | BOTH | 60% | Agreed: rate the code fact as a defect; plan priority from the cited driving text and on-record staging (V1:583; V2:1144). | no [QUALIFY = BOTH] |
| X-023 | BOTH | 60% | Item 20: default path 32 keys / 10 outside (V2:1430, executed); with `tier2_fallback_enabled`, 33 / 11 (`ensemble.py:833-834`; 0 `t2_fallback` hits in `panel_lint.py`). Merge states both with the condition; V1's unconditional "writes 33" (V1:640) is the non-default case. | yes [V2] |
| X-024 | BOTH | 60% | Same fact as X-023. | yes [V2] |
| S-056 | BOTH | 70% | Agreed: V1's gate form with commands, counts and replacement assertions (V1:4033-4055) as base; V2's adjudicated gates G17-G27 (V2:4482-4492) added. | no [BOTH] |
| X-036 | V1 | 70% | Item 18: run 2's own QA row P6-054 records the paper as withdrawn by arXiv Admin on 2026-11-03 (`qa-consolidated-findings-phase6.md:76`), the V1 advocate's fetch agrees; not re-fetched by me. V1 excluded the figure (V1:1003); V2 cites it and builds takeaway 1 on it (V2:1647-1648, V2:2044). | yes [V2] |
| S-004 | V2 | 60% | Agreed (V1 advocate moved): V2 3.1-3.5 with the precedence table first (V2:1114-1227) as skeleton; V1's consumer table C-A..C-E and core diagram (V1:496-520) carried. | no [V2] |
| S-022 | V2 | 60% | Agreed: V2's classified matrix (V2:830-1110) as base; V1's "Same data contract? / Same code? / Divergent choices" columns (V1:436-461) carried. | no [V2] |
| X-008 | V1 | 65% | Agreed (checked): V2:134 says PR review needs "an optional per-slot lens"; D11 "the fact stays true for a later panel-engine step" (V2:4510); C-11 INV-009 HIGH OPEN "no slot id exists in `/task` once the per-slot key was withdrawn" (V2:4144). V1's optional keys (V1:612) carried as reserved. | no [V1] |

**Tally:** moved 13 of 38 (S-040, C-050, C-061, C-090, X-042, C-081, C-057, C-083, X-010, X-019, X-023, X-024, X-036); held 25. Of the 25 held, 22 are now agreed with the V1 advocate because it moved to my Round 1 verdict or the convergence table mis-recorded my verdict (C-073, C-093); 3 stay in dispute on labelling only (C-005, C-076, X-051: V2 governing with V1 detail carried, against the V1 advocate's BOTH). Every move rests on a re-read line, not on agreement: V2:1135/3743/3771 and V1:1988 (clustering), V2:3644/3661 (run record), V2:1271 (X-019), `ensemble.py:363,833-834` (key count), the run-2 QA record P6-054 (X-036).

#### Verdict changes on other points or clusters

| Point or cluster | Round 1 verdict | Round 2 verdict | Why |
|---|---|---|---|
| CL-01 Core shape | V2 65% | V2 governs; BOTH on option content (S-040, C-050) and clustering (C-061, C-090, X-042) | Governing shape V2 (V2:3511, V2:3578); V1's Option B detail enriches V2's own one-engine Option A (V2:2184); V1's clustering remedy fills a gap V2 left for the v1 engine (V2:1135, V2:3771), with the T-c interaction stated (V2:3636). |
| CL-06 Dispatch, identity, read-only | V2 65% | BOTH | My weakness 8 was false (V1 C-18, V1:2320-2385). V1: decision and rf-qa open point; V2: mechanism (`--tools`, V2:1728), launcher gating and dispatch layers (V2:592-655, V2:3640). |
| C-067 Reviewer read-only enforcement | V2 (cluster) | BOTH | Same as CL-06; V1:2332 and V1:2381 must change `--allowedTools` to `--tools` / `--disallowedTools Bash` / `--restricted`. |
| CL-07 Distinctness | OPEN | OPEN (default); BOTH (record fields, C-081) | Fields additive (V1:2842, V2:3657); V1's launch grammar excluded (conflicts with V2:3640). |
| CL-08 Run record | V2 55% | BOTH | Record shape V2 (A-10, V2:3661; race C-034 agreed V2); check placement both (V1:631 vs V2:3644). |
| CL-13 Evaluation | V2 70% | V2 70%, with X-019 split | G-123 Critical (V2); G-36 Important, because V2's own G-36 tags the causal link [UNVERIFIED] (V2:1271). |
| CL-18 Fact disputes | V1 60% | V1 60%; X-023/X-024 become BOTH | Key count: 32 default, 33 with the fallback flag (`ensemble.py:363,833-834`). |
| CL-20 Section 8 form | MERGE | BOTH, narrower drop list | Drop V1 8.4 layout table A-E (V1:4063-4069), the PR-process item (V1:4115) and the ordering clause of V1:4120; carry V1:4059, V1:4061 (with "3 commits" corrected to 5), 8.5 no-regression rows and 8.6 gate operations; rewrite V1:4116, V1:4119. |
| CL-23 Section 5 research | MERGE | BOTH with one exclusion and one tier fix | Exclude the 2606.19544 figures and takeaway 1's verbosity clause (V2:1647, V2:2044; withdrawn per run-2 QA P6-054); 2510.27106 re-tiered "accepted at EMNLP 2025" (same QA row). |
| U-099 (V1 branch layouts) | DROP; keep only V1:4059 | DROP the layout table only | V1:4061 facts and 8.5/8.6 no-regression content are constraints (r2-advocate-V1.md point 11, checked). |
| My Round 1 weakness 8 (V1 lacks a raw-id read-only requirement) | claimed | withdrawn | False against V1:2327, V1:2374, V1:2381. |
| My Round 1 weakness 11 (only V1:4059 survives) | claimed | narrowed | See item 11 of the first section. |
| My Round 1 X-019 evidence ("E2's measured H1 lever") | claimed | withdrawn | V2:1271 itself says [UNVERIFIED]. |
| My Round 1 X-042 evidence ("labels that do not exist"; "anchor-only singletons") | claimed | withdrawn | Labels are pending (V1:4098); the anchor-to-citation step is in V1:1988. |

#### Corrections to V1 you found

Claims in V1 (or in the V1 advocate's Round 2) that are wrong, each with the check run this round. The Round 1 V1 corrections both advocates agree on (Qwen 3 of 4, audit D wording, 43 call sites, `same_defect`, "37 files", D2 rating, quorum wording, DECIDED labels, E2 pin) stand and are not repeated.

| # | Where | Claim | Check | Finding |
|---|---|---|---|---|
| 1 | V1 C-18 Option A and resolution (V1:2332, V1:2381) | `claude -p --allowedTools` is the read-only allowlist mechanism | Read V2:1725-1728; local `claude --help` (2.1.325) | `--tools` sets the available built-in tools; `--restricted` removes Bash unless `--tools` names it; `--allowedTools` is an allow (pre-approval) list. Under the `bypassPermissions` launcher V1 records (V1:2327) a pre-approval list restricts nothing. Replace with `--tools` (or `--disallowedTools Bash` / `--restricted`), and keep V1's "test before relying on it" (G-45). |
| 2 | V1 8.4 facts (V1:4061) | `ironbelly/shadow-runs` "is 3 commits ahead of `origin/master`" | `git rev-list --count origin/master..HEAD` | 5 now (which two commits were added since V1's count was not checked). Still true: `cli/review` equals `origin/master` (`git diff --stat origin/master HEAD -- src/superclaude/cli/review` empty). State as "as of the run 1 baseline". |
| 3 | V1 MS-13 (V1:640), V-565 (V1:3687) | `ensemble.py:886-895` "writes a version-1.0 contract with 33 keys, 11 of them in neither `panel_lint` list" | Count of the dict literal `ensemble.py:785-836` (32); `:833-834`; `:363`; `grep -c t2_fallback panel_lint.py` (0) | Default run writes 32 keys, 10 outside; 33 and 11 only with the fallback flag. State the condition. |
| 4 | V1 C-12 resolution (V1:1988, V1:2850) | "one clusterer on the v2 location model" as the clustering baseline | Read V2:3636 (T-c), V2:3743 | Under the adopted two-engine default this is reachable only through trigger T-c; the merge carries V1's remedy elements (complete-link admission, no merge on an empty location, anchor-to-citation step, acceptance metric) per engine and surfaces the T-c consequence, not the single clusterer as decided. |
| 5 | V1 8.6 (V1:4115, V1:4120) | PR-process checklist item; "mark the steps that wait on each" | Read V1:4114-4120 | PR-process content duplicates project rules the owner fixed; "mark the steps that wait" is ordering. Not carried (reference only). |
| 6 | V1 5.3.5 (V1:1003) | verbosity figure excluded because blog-attributed and unconfirmed | Grep `.dev/` for `2606.19544`; run-2 QA P6-054 (`qa-consolidated-findings-phase6.md:76`) | Outcome right; reason incomplete: the primary is recorded as withdrawn by arXiv Admin on 2026-11-03. Not verified by me (no fetch). |
| 7 | r2-advocate-V1.md CL-08, Remaining disagreement 3 | "V2 ... defers `verify-run` (V2:1143)" | Read V2:1143, V2:3644 | V2 defers only a kernel `verify-run` command; the verifier (identity, completeness, conservation, seeded from audits B, D, F) is assigned now as tested `scripts/` + `tests/`. The difference is placement, not presence. |
| 8 | r2-advocate-V1.md Remaining disagreement 1 | without V1's target text "a plan reaching T-a/T-b/T-c would have no design to converge to" | Read V2:2184, V2:3511 | False: V2 6.1 Option A (one engine, v2 kernel as core) and the C-01 "recorded path is A's one-engine design after an anchor-span precondition". V1's text enriches that alternative. |
| 9 | r2-advocate-V1.md X-024 | "V1's fault is an unstated unit, not a wrong number" | Item 20 above | For the default run (fallback disabled, `ensemble.py:363`) "writes 33" is a wrong number; it is right only under the flag. The merge states both. |

#### Must-carry content for the merge

**From V1** (with the corrections above):
1. Verified facts V2 gets wrong: `KeyError` only on a direct `annotate` call or a parser switch (BL-04, V1:608); 1,398 = all rows (DOC-18, V1:680); calibrator 6-vs-5 [CODE-CONTRADICTED] (V1:171); 0.704 mixes definitions (V1:162); shadow09 0.9328 (V1:163); `ensemble.py` predates E1 (V1:414); judge sees the combo name (V1:208); S-ID identity probes (V1:167).
2. Defects only V1 has: `unauthorized_deviation_present` with no producer (MS-14, V1:641); no `merge_method` / `merged-verdict.yaml` writer (MS-24, V1:651); no `REPORT.md` or per-task verdict matrix from the post gate (ENS-4, V1:655); PR router-vs-rubric divergences and `deep=True` dormancy (BL-16, BL-17, V1:620-621); D1-D16 with "v2 shares it?" (V1:358-377) and the 6.D defect-to-test table (V1:2517-2538).
3. Decisions only V1 has, carried as owner-gated: panel size and Tier 2 cost with D-1 (C-14, V1:2107-2117); calibration as a routing signal (C-06, V1:1602); invalid-block policy (C-15, V1:2184); reviewer read-only for every reviewer with orchestrator-computed shell evidence (C-18, V1:2381; mechanism per correction 1) and the rf-qa Bash open point (V1:2383, Q-61); clustering remedy and acceptance metric (C-12, V1:1988; labels #525-#530 pending, V1:4098) with the T-c consequence; post-gate fix-in-place now (C-17, V1:2314-2316; M3-03..M3-07, V1:3886-3890), consistent with V2 C16.
4. No-regression and migration content: 8.3 gates with commands, collected counts (651 + 353 + 178 = 1182, re-collected in Round 1) and per-test replacement assertions (V1:4033-4055; assertions tied to a non-adopted design tagged conditional); persisted-format and rollback rules (V1:3830, V1:3845, V1:3861); V1:4059 git constraint (merged with V2 C4's observed output); V1:4061 facts (corrected); 8.5 rows that are no-regression risks (V1:4085-4087, V1:4100); 8.6 gate operations (V1:4106-4111, V1:4117); the 48 steps as per-item migration content re-based on the merged design with ordering language removed (U-096); the gap-to-step coverage check rebuilt over the merged gap list (V1:3910-4030); track tags as "destination module" (V1:761).
5. SC-18..SC-22 and the SC-6, SC-10, SC-14 pass rules (V1:531-547); X1-X14 exposures incl. coverage mode X14 (V1:2984-3006); 6.E implementer detail (V1:2624-2807), rows tied to non-adopted designs tagged conditional (e.g. the launch grammar); optional per-slot `role`/`lens`/`agent` keys reserved (V1:612; X-008).
6. Section 5.2-5.4 research on severity, calibration and clustering (V1:853-1079) and the exclusion at V1:1003 (reason extended).
7. Owner items O-1..O-6 incl. issues #525-#530 (V1:4136-4141).

**From V2:**
1. Evidence base: HEAD and the E2 tip `6c09843` (V2:108), the [POST-BASELINE] commit `e2f2ac268` (Q-39; owner: folded in later); collaboration and process-redesign facts, options and dormant outcomes with build/enable triggers (V2 2.3 V2:345-412, axes 6-7 V2:3641-3642, A-18, A-19); re-derived E2 numbers and the `fullpkg()` bug (V2:294-320); Stage 2 failure mechanisms and the `reflect_shadow_exit.py:313` defect (V2:207-229).
2. Evaluation: E1 and E2 one derivation set (sha256 `044809e3...`, V2:278, V2:322); three-tier acceptance and the verifier owner (axis 9, V2:3644); G-123 Critical.
3. Adjudicated design, labelled "adjudicated default, partial", with margins, tiebreaker levels, conditions and the 60 open HIGH invariants (V2:3654-3671; 7.3 V2:3960-4232): thin shared contract with per-module engines and triggers T-a/T-b/T-c (V2:3636) plus the one-engine alternative (6.1 Option A, V2:2184) enriched by V1; ledger axis 4 with G-14/G-15 (V2:3639, V2:1249-1250); typed `blocking` plus CRITICAL floor and `min(2, requested)` quorum (A-3, A-4); C-06 repair and drop record (V2:3516); `events.jsonl` run record (A-10, V2:3661); launcher gating and "the core launches nothing" (axis 5, V2:3640) with the `--tools` mechanism (V2:1725-1728); code-owned shadow helpers (V2:3643); the C-05 tiebreaker caveat (V2:3664).
4. Precedence table rebuilt against the merged Section 7 (V2:1125-1144); Q-40 (owner wording, V2:3582) open.
5. Binding constraints C1-C29 (V2:4430-4458) incl. C4's observed git-ref output and the `verify-sync` pre-commit correction (C5); dependency facts D1-D26 (D9 corrected; D11 kept with its note, V2:4510); acceptance conditions AE-1..AE-15 (V2:4529-4549); per-consumer verdicts (V2:3842-3849); adjudicated gates G17-G27 (V2:4482-4492).
6. External research on hooks/headless, tool-restriction flags, git refs, stacked PRs and finding schemas (V2:1698-2036), minus the 2606.19544 figures and the verbosity clause of takeaway 1 (V2:1647, V2:2044), with 2510.27106 re-tiered.
7. The 171-row defect register and the 5,950-row inventory as named inputs, re-routed against the merged Section 7 (S-048, A-056; V2:4300-4314); Q-01..Q-93 with sources; the 0.75 vs 0.80 convergence-threshold conflict (`SKILL.md:703` vs `contract.py:321`).

**False or stale content that must not be carried as stated.** From V2: the `KeyError` crash on the merge path (nine sites incl. V2:3637 and D9 V2:4508); the [UNVERIFIED] calibrator tag; "multi-member" for 1,398 (V2:1368, V2:3743); "first-parse" 0.704; "all 1.000" `cluster_agreement`; G-06 Important; G-36's Critical resting on an [UNVERIFIED] causal link (rate Important unless a measurement appears); "50 test files" and "(6)"; the withdrawn-paper figures and 2510.27106's tier; the stale "decision"/"open" wording in SC-04, SC-17, G-85, 3.5 and OQ-01. From V1: `--allowedTools` as the restriction mechanism; "33 keys written" without the condition; "3 commits ahead"; 43 call sites; Qwen "3 of 3"; audit D wording; "37 files"; DECIDED-BY-EVIDENCE for C-01, C-04 (default), C-12 and the C-17 remedy; "strict subset" at V1:3065 as present tense; the E2 pin at V1:4119; the 8.4 layout table A-E, V1:4115 and the ordering clause of V1:4120.

#### Remaining disagreements (if any) and final evidence

1. **C-005, C-076, X-051 (labelling): V2 governing with V1 detail carried, against the V1 advocate's BOTH.** Content is agreed: V2's thin shared contract governs as "adjudicated default, partial"; V1's superset text is carried; Q-40 stays open. The disagreement is whether V1's superset is recorded as *the* one-engine target. Final evidence: V2 already has an inline one-engine option (V2:2184) and a named convergence path (V2:3511); recording V1's design as a second "target" would give the plan two one-engine targets with different contracts (V1: findings-v2 single contract, V1:2823; V2 Option A: v2 kernel with v1 loop as module, V2:2184). The merged document should present one one-engine alternative, built from V2 6.1 Option A and enriched by V1's namespaces, fit rows and diagram, with the strict-subset precondition stated as a code change (`findings_v2.py:96-97,279-281`). If the V1 advocate means exactly that by "BOTH", the disagreement is only a label.
2. **T-c interaction (new, both sides).** Not a dispute between the advocates but a decision the merge must not hide: adopting V1's clustering remedy for both engines satisfies V2's trigger T-c (V2:3636). The plan needs an owner choice: remedy in the v2 engine only (v1 over-merge accepted and recorded), or remedy in both and the one-engine path.
3. **X-036 status wording.** Agreed on V1; I keep the label "withdrawal not re-verified by this advocate" because I could not fetch the page. Two independent records agree (run-2 QA P6-054 at `qa-consolidated-findings-phase6.md:76`; the V1 advocate's fetch, r2-advocate-V1.md line 101), so the merge should exclude the figures either way.

Everything else in the 38 is agreed with the V1 advocate's Round 2 verdicts.

## Round 2 convergence snapshot

#### Convergence snapshot after R2

- Debate points: 234; agreed: 226; disagree: 8; no verdict from one side: 0
- Convergence = agreed / total = 0.966

#### Points where the advocates still disagree after Round 2

| Point | Cluster | V1 advocate | V2 advocate |
|---|---|---|---|
| C-005 | CL-01 | BOTH | V2 |
| C-076 | CL-01 | BOTH | V2 |
| X-051 | CL-01 | BOTH | V2 |
| C-053 | CL-02 | V1 | V2 |
| C-065 | CL-04 | V1 | V2 |
| C-025 | CL-09 | V2 | MERGE |
| C-014 | CL-10 | V1 | BOTH |
| S-044 | CL-17 | V1 | V2 |

## Round 2.5: Invariant Probe (independent fault-finder)

### Invariant Probe Results

### Round 2.5 — Fault-Finder Analysis

| ID | Category | Assumption | Status | Severity | Evidence |
|---|---|---|---|---|---|
| INV-001 | state_variables | The line numbers both reports cite (checked at HEAD only, A-002 ACCEPT, A-036 QUALIFY) are the lines a later plan will edit | UNADDRESSED | MEDIUM | Own check: `git diff --stat 50d4d2b9d HEAD -- src tests scripts` empty and tree clean, so cites hold at HEAD `ad8f57560`. But `origin/master` (`d4d1662a8`) is 3 commits past merge-base `d2d8a2d16` and differs from HEAD in 50 src/tests/scripts files; the plan's branches are cut from `origin/master` (V1:4061 fact). Cited pins moved there: `tests/skills/test_worker_contract.py:777`->787, `:1861`->1872, `:786`->796; `output-styles/pragmatic.md:225`->229, `:231`->235; reflect `SKILL.md:343` has different text. These lines are cited by V2 C14, C26 (V2:4443, 4455) and the X-15 basis (V2:3525). Advocates checked only `cli/review` against `origin/master` (r2-advocate-V2.md:35). Downstream gate: only the A-036 "re-read before editing" rule (r1-advocate-V1.md:276); the merged constraint cells stay stale |
| INV-002 | state_variables | The E2 evidence pinned at `6c09843` is the E2 state the plan will meet | ADDRESSED | LOW | Owner decision: newer commits folded in later; V2 Q-39 and the C-12 [POST-BASELINE] condition are carried (r2-advocate-V2.md:164). Quantified here: `git rev-list --count 6c09843..e2f2ac268` = 7, `git diff --stat` = 767 files, +43,936 lines; none of the cited E2 files (`audit2.py`, `combos/SPEC.md`, `judge-one.sh`, `final-table.py`, `anon-combos`) changed in that range (`git diff --name-only` grep: no hit) |
| INV-003 | state_variables | Keeping schema string `review-ledger/1` while changing its semantics is safe because new keys are optional and old readers tolerate them | UNADDRESSED | HIGH | Consensus takes V2 A-9 "keep `review-ledger/1`" with new semantics (silence never clears; stored `verdict`, `decision`, `brief_ids` dropped from new rounds; V2:3639, V2:3660) AND V1's persisted-format rule "keeps its schema string ... new keys are optional ... previous reader tolerates unknown keys" (V1:3830, carried in both R2 must-carry lists). V1's own debate C13-22 INV-014 (V1:2657) rejected exactly this: "an older installed binary would continue a new-key ledger with the old rules (silence clears, re-find un-blocks) while the file still looks valid", remedy `min_writer` plus `review-ledger/2`. Code: `ledger.verdict` returns `last["verdict"]` (`ledger.py:363-372`, read here), so old binaries KeyError on new rounds while old `merge_round` keeps clearing by silence. Neither advocate carries `min_writer` or the bump. Downstream gate: V1's reload test "previous reader tolerates unknown keys" would PASS and so certify the hazard; none catches it |
| INV-004 | state_variables | The debate state (r2-state.json, consensus-summary) records each advocate's final verdict | UNADDRESSED | MEDIUM | r2-state.json gives the V1 advocate CL-09 = "V1" and lets C-010, C-017, C-018, C-020, C-021, C-024, C-025 inherit it, but that advocate set C-017 = V2 and C-025 = V2 explicitly (r1-advocate-V1.md:253-254) and said "CL-09: V1 on the post gate; BOTH on the rest" (r2-advocate-V1.md:116). So 7 of the 10 "still disputed" points (convergence-r2.md) are inheritance artefacts; the only real disputes are C-005, C-076, X-051 (labelling). A merger reading the state or the CL-09 "V1" label would drop V2-only content: the C-025 reflect memory write path (U-043) is in neither R2 must-carry list. Downstream gate: none |
| INV-005 | state_variables | The quorum floor `min(2, requested)` has a defined `requested` at merge time | UNADDRESSED | MEDIUM | V2 leaves it open: "the source of `requested` when `--resolution` is absent is open (synth-10 Q-42)" (V2:3639); Q-52 "`merge_round` has no such parameter; 24 test call sites" (V2:4802). V1 already designed the answer: the round entry records `panel_size`, `quorum`, `valid`, `denominator_source` (V1 6.E C13-06, V1:2641; C13-22, V1:2657). Consensus adopts V2 (CL-04, CL-05) and neither R2 must-carry list carries `denominator_source`. Downstream gate: V2 G18 replay (not built, V2:4483) does not test the denominator |
| INV-006 | guard_conditions | `--tools` / `--restricted` (or `--disallowedTools Bash`) make a raw-id `claude -p` reviewer read-only | UNADDRESSED | HIGH | Shared error: both advocates adopt this mechanism (r2-advocate-V1.md:31; r2-advocate-V2.md:53, :142). Own check `claude --help` (2.1.325): `--tools` picks "from the built-in set"; `--restricted` says "add --strict-mcp-config to skip MCP servers too"; `--strict-mcp-config` "Only use MCP servers from --mcp-config". So user-configured MCP servers (write-capable ones included) stay available under the agreed flags. Grep `strict-mcp-config` in V1, V2 and all four advocate files: 0 hits. Also `--restricted` "refuses bypassPermissions", which E2's launcher uses (V1:2327). Downstream gate: C-07 G2 "read-only plus tool surface" (not built, V2:3640) would catch it only if it reads the `system/init` MCP list (V2:1718); not specified |
| INV-007 | guard_conditions | No product `claude -p` reviewer launcher exists, so the raw-id launcher is "gated, not built" and designed from scratch | UNADDRESSED | MEDIUM | Own read: `src/superclaude/cli/pipeline/process.py:145-154` already builds a restricted reviewer argv (`reviewer_profile=True` drops `--dangerously-skip-permissions` and `--tools default`), used by reflect Tier 1 (`runner.py:493-499`, `:566`) and the adversarial scorer (`ensemble.py:548`). Grep: `pipeline/process.py` 0 hits in V1, V2 and all advocate files; `reviewer_profile` 0 in V1, 1 unrelated in V2. Its read-only basis is permission prompts in print mode, which settings allow-rules can widen; reuse and that basis are unexamined. Downstream gate: C-07 G1-G3 test a new launcher, not this one |
| INV-008 | guard_conditions | V2's C-06 dropped-blocking refusal closes the fail-open path that made D1 Critical (V1 advocate R2 concession) | UNADDRESSED | MEDIUM | The concession (r2-advocate-V1.md:56) rests on an overstatement. V2's own open items: C-06 INV-006 "the acknowledgement is not bound to the dropped item ids or hashes" (V2:4067, OPEN); X-14 INV-019 HIGH "an acknowledged drop needs a defined flag state" (V2:4196, OPEN); Q-60 "an unbound acknowledgement, a dropped `prior` line, `blocking_state` from the line's own untrusted flag" (V2:4810); repair is `repair=False` by default and may stay off at v2 call sites (V2:3638). The path is narrowed, not closed. Downstream gate: G21 kill lines K1-K5 (not run, V2:4486) |
| INV-009 | guard_conditions | A re-review round still has a meaningful quorum | ADDRESSED | LOW | Own read `panel.py:600-605`: when `review_kind` is not in `apply_to`, only fixed slots resolve with count 1, so re-review is one reviewer and `min(Q, requested)` = 1. V2 states and accepts it ("re-review relies on explicit verify answers rather than quorum", V2:3639; C-02 condition, V2:3512) |
| INV-010 | guard_conditions | A quorum of 2 valid reviewers means 2 independent opinions | ADDRESSED | MEDIUM | Soft distinctness re-admits duplicates (`panel.py:539-543`; analyst `panel resolve` run: Qwen at two slots, anthropic-only 6 haiku + 1 sonnet; V2 A-6: 30 of 40 live7 resolutions hold a duplicate). V2 C-03 records independence "requested, not served" as data, not as a gate (V2:3513, C19 V2:4448); consensus keeps the default OPEN (X-041, X-057, C-060), so the precondition stays visible |
| INV-011 | guard_conditions | V1's per-slot keys (`role`, `lens`, `agent`; distinctness `none/model/class`; `replicas`) can be carried "as reserved" without code impact | UNADDRESSED | MEDIUM | Consensus X-008 = V1 "carried as reserved" (r2-advocate-V1.md:104; r2-advocate-V2.md:113), C-081 BOTH. Own read: `panel.py:46` `_SLOT_KEYS = {"slot_id", "tier", "count", "strategy", "seed"}` and `:215` reject any other slot key. A reserved key is therefore either code (validator, template hash and goldens move; cf. V2 C29 for the `exchange` key, V2:4458) or document-only; neither advocate says which. Downstream gate: golden tests (V1 G3, V2 G8) fail only once a template uses the key |
| INV-012 | count_divergence | The test counts both reports quote are right | ADDRESSED | LOW | Re-collected with `uv run pytest --collect-only -q -p no:cacheprovider`: `tests/review` 651, `tests/cli/reflect` 353, `tests/pr_submit` 2258 (V1 right on all three); 38 reflect test files (V1:381 "37" wrong), 19 review test files, 47 `test_*.py` in pr_submit (V2 G14 "50" wrong). Both corrections are already in the R2 lists |
| INV-013 | count_divergence | Engine-A contract key counts (V1 33/11, V2 32/10) | ADDRESSED | LOW | `uv run python` over `ensemble.py:787-832`: 32 literal keys; `t2_fallback` only conditional (`:833-834`, default None at `:363`); outside STABLE (110) and TELEMETRY (27) = 10; outside STABLE only = 11; 21 stable present (89 absent). V1's "in neither list" pins its 11 to the `t2_fallback` basis. Consensus BOTH with the condition stated (r2-advocate-V2.md:55) is right |
| INV-014 | count_divergence | Counts of invariants, gates, constraints, questions and inventory rows were re-derived | ADDRESSED | LOW | Own counts: V2 7.3 = 244 rows, HIGH 60 / MEDIUM 161 / LOW 23, all 60 HIGH OPEN (awk over V2:3962-4232); V1 26 HIGH = 2+11+10+3 (V1:2620, stated only); gates V1 19 (G1-G11 + 8 named, V1:4035-4055), V2 27; V2 C1-C29 = 29, D1-D26 = 26; unique Q ids V1 61 (122 rows with sub-tables), V2 93; inventory V1 698 rows (91 DROP), V2 5,950 (5,779 ledger + 171 DR; DROP 1,969). Units differ; both advocates reject comparing them (A-059) |
| INV-015 | count_divergence | The convergence denominator is the skill's | UNADDRESSED | LOW | diff-analysis.md Summary says "Debate-point denominator per the skill (S + C + X + A): 275" (all 59 A rows) while debate-points.md uses 234 (18 promoted). The skill counts promoted A-NNN only (`sc-adversarial-protocol/SKILL.md:864-870`, `:1392`), so 234 is right; 275 would give 224/275 = 0.815. Stale number in an input artefact. Downstream gate: none reads it |
| INV-016 | count_divergence | Convergence 0.957 means 224 points are resolved | UNADDRESSED | MEDIUM | r2-state.json: both advocates say OPEN on X-040, X-041, X-056, X-057, X-058, C-060 and these count as "agreed"; resolved = 218/234 = 0.932. consensus-summary.md hides them under cluster labels: X-058 (exit 12) under CL-04 "V2", X-040/X-056 (claim cut) under CL-03 "BOTH/MERGE". A merger working from the cluster table adopts V2's exit-12 meaning and claim stance as decided. Downstream gate: none in the merge path |
| INV-017 | count_divergence | "V1's code-fact corrections win the fact disputes" (CL-18 = V1) | ADDRESSED | LOW | Of 17 CL-18 points the final point verdicts are V1 9 (X-020, X-027, X-028, X-030, X-032, X-048, X-049, X-053, A-057), V2 5 (X-022, X-029, X-031, X-033, X-061), BOTH 3. Orchestrator VERIFIED-V2 on X-022/X-029/X-061 (re-run here: 52 lines, 11 files, 8 `SKILL.md`). Point verdicts and both must-not-carry lists ("43 call sites") are correct; only the cluster label misleads |
| INV-018 | collection_boundaries | Merging the gate lists as "V1's form as base, V2's G17-G27 added" keeps every no-regression gate | UNADDRESSED | HIGH | Recipe: S-056 rows (r2-advocate-V1.md:100; r2-advocate-V2.md:109). It drops V2's current-code gates G1-G16. With no V1 counterpart: V2 G9 (`make lint-architecture`, ruff check and format, `make verify-deps`), G10 (installed-path baseline, 148 lines in 56 files), G12 in part (`tests/commands/test_routing_plugin_parity.py`), G15 (about 23 rf-qa pin files, 17 under `tests/audit/`), G16 (contract-constant and generator-constraint gates) (V2:4474-4481 against V1:4035-4055). Carried V2 items cite V2 gate numbers: C19->G1, C20->G8, C21->G8, C23->G14, C25->G15, C26->G11, C27->G8/G1, G17->G8, G19->G3/G7, G20->G1, G22->G8 (V2:4448-4456, 4482-4487); under V1 numbering G1, G8, G11 are other suites and G14, G15 do not exist. Downstream gate: none; mis-bound ids pass any structural check |
| INV-019 | collection_boundaries | Prefixing ids by report (A-006, A-058) removes id collisions | UNADDRESSED | LOW | Prefixing solves cross-report clashes only. Intra-report clashes found: V1 C-01..C-20 conflicts (V1:2839-2858) and C-01..C-25 closed items (V1:4266-4290); V2 AE-1 web finding (V2:1647) and AE-1 acceptance condition (V2:4535); V2 table G1-G3 and C-07 launcher G1-G3 (V2:4449); V2 D-1 decision group and defect D-1 (V2:3639); V2 M1 exposure and measurement M1; per-debate INV-nnn reused in 19 debates (348 "INV-0" hits in V2, 109 in V1); this probe's INV-001.. ids also collide. Needs composite keys (slot + id). Downstream gate: none |
| INV-020 | collection_boundaries | V1's 698 rows and V2's 5,950 rows can be carried side by side after re-routing | UNADDRESSED | MEDIUM | Both advocates require re-routing against the merged Section 7 (A-056) but state no cross-report de-duplication, though both inventories derive from overlapping hand-offs and V2 alone dropped 1,753 of 5,950 rows (29.5 percent) as duplicates (synth-08 8.1.0, read here). V1 rows aimed at V1 components the merged design does not adopt (own count of V1 destinations): Blocking decider hook 18, Calibration 21, Built-in run audits 20, Clustering 22, Run manifest 12 = 93. Downstream gate: V2's duplicate-group rule P3-011 is scoped to V2 ledgers |
| INV-021 | collection_boundaries | Dropping V2:1647, V2:1648 and V2:2044 removes every use of the withdrawn arXiv 2606.19544 | UNADDRESSED | MEDIUM | Withdrawal confirmed independently (WebFetch `arxiv.org/abs/2606.19544`: "withdrawn by arXiv Admin", v2 3 Nov 2026; run-2 QA P6-054 at `qa-consolidated-findings-phase6.md:76`). Grep finds uses the drop list misses: V2:1655 ("AE-1 found it much reduced", verbosity-guard rationale), V2:2829 (Section 6 second-judge Cons: "33 to 41 points ... (W01 AE-1)"), coverage rows V2:2072, V2:2078 ("5.1.5 AE-1 ... Included"). Downstream gate: none |
| INV-022 | collection_boundaries | One-sided unique rows were cross-checked by the other advocate | UNADDRESSED | LOW | Both R1 U-verdict sections cover only High rows (r1-advocate-V1.md:289-356; r1-advocate-V2.md:305-346), so 62 Medium/Low U rows had no cross-check. Spot checks here found no error: U-001 (no producer: `ensemble.py:451-454` and docstring `:527-530` "deviation booleans default CLEAN"), U-002 (`src/superclaude/skills/sc-adversarial-protocol`: 0 hits for `merge_method` or `merged-verdict`), U-052 (125 tracked plugin files), U-122 (47 test files). Downstream gate: merge provenance tags only |
| INV-023 | collection_boundaries | V2's inventory can be carried by pointer | UNADDRESSED | LOW | The 5,950 rows exist only in `.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/synthesis/synth-08-value-inventory.md` (tracked; 2,024,775 bytes, 6,127 lines; per-source totals 886+868+1,685+955+796+589+171 re-added here). A path pointer breaks if the task folder moves (to-do/done moves are routine). Pin the pointer to commit `ad8f57560` plus path. Downstream gate: none |
| INV-024 | interaction_effects | Carrying V1's clustering remedy is a local choice between "v2 engine only" and "both engines" | UNADDRESSED | HIGH | Advocates name the T-c choice (r2-advocate-V2.md:43, :177) but not its cascade. If T-c fires, C-01 reopens ("the recorded path is A's one-engine design", V2:3511). V2's own conditions chain on C-01: C-05 "Holds while C-01 to C-03 stand" (V2:3515); X-15 "holds while C-01, C-02 and C-03 stand" (V2:3525); constraint C26 "Reopened together with C-01, C-02 or C-03" (V2:4455); C-06 depends on C-02/C-03 `block_ok` (V2:3516); C-11's later swap waits on C-02/C-03 (V2:3521). So the choice can reopen up to 5 further adjudications. Downstream gate: none |
| INV-025 | interaction_effects | Exit code 12 can have one meaning in the merged design | UNADDRESSED | MEDIUM | V2's adopted policy uses 12 for the quorum refusal (V2:3513) AND the dropped-blocking refusal: C-06 INV-020 "two refusals can occur in sequence (quorum, then `dropped_blocking`, both exit 12) and record nothing" (V2:4078, LOW, CARRIED). V1 6.E rows carried "tagged conditional" use 12 = PENDING (V1:2648, V1:3841); the installed experiment ledger uses 12 = CONTINUE (V1:617, V1:3001). The V1 advocate's own requirement "one meaning for exit code 12" (r1-advocate-V1.md:391) is unmet by the adopted design; X-058 stays OPEN for both. Code today: `ledger_cmd.py:13` `{PASS 0, REVISE 10, ESCALATE 11}`, no 12 in `cli/review` or `cli/reflect` (grep). Downstream gate: none |
| INV-026 | interaction_effects | V1's gate rows can be carried while V2's verdict design governs | UNADDRESSED | MEDIUM | V1 G2 says `test_review_ledger.py:299-304` (exact `verdict()` dict `{verdict, decision, brief_ids, round}`) and `:468-472` (final `verdict:` line) "Must NOT change" (V1:4038). V2's adopted axis 4 drops stored `verdict`, `decision`, `brief_ids` from new rounds and derives `brief_ids`, `verify_ids`, `held_ids`, `next` on read (V2:3639), while `ledger.verdict` returns `last["verdict"]` today (`ledger.py:363-372`; test lines read here). V2's own rewrite list C18 (V2:4447) also omits these two pins. Downstream gate: G2 fails only at implement time |
| INV-027 | sufficiency_challenge | V1's 48 migration steps can be carried "re-based on the merged design, ordering removed" (both R2 must-carry lists) and still feed `/sc:workflow` without contradicting Section 7 | UNADDRESSED | HIGH | Enumeration (own classification of the 48 step rows V1:3834-3908 against the 15 V2 adjudications V2:3511-3525 and the consensus): conflict 13 (M1-01 single validator vs C-01; M1-05 location union with `in_diff` vs C-10; M1-06 one clusterer vs C-01; M1-08 grader and PENDING vs C-02/C-03; M1-12 manifest payloads and M1-13 telemetry projection vs C-08; M1-21 verify stage in the kernel vs X-14; M3-02 hooks that change call sites vs C24; M4-01 edits `fsm.py`, M4-03 edits `severity_router.py`, M4-04 PR fields vs C-10/C23; M4-05, M4-07 rf-qa engine vs C-11), partial 14 (M1-02, M1-04, M1-07, M1-09, M1-10, M1-16, M1-17, M2-02, M2-04, M2-08, M2-10, M3-01, M4-02, M4-06), compatible 21. No step-level re-adjudication exists, and V1's gap-to-step map (V1:3910-4030) keys on these ids. Falsifier: if any of the 13 is carried as written, Section 8 contradicts Section 7 |
| INV-028 | sufficiency_challenge | The adjudicated outcomes carried as the recommended design are V2's debated results (with their conditions and invariants) | UNADDRESSED | HIGH | Enumeration of V2 adjudications the consensus changes without a new debate or fault-finder pass: (1) C-04 "no engine moves now" (6.91 percent, no tiebreaker, CONVERGED, 0 HIGH; V2:3514) replaced by V1 C-17 fix-in-place as default (C-084, X-043, X-054 = V1), and V1 never debated C-17 (V1 debated only C-03, C-05, C-13, C-14; S-036, S-037), so that remedy has no invariant probe; (2) C-11 per-slot `lens` withdrawal (6 HIGH open incl. INV-009) reversed to "reserved" (X-008); (3) C-09 soft default (CONVERGED, no HIGH) reopened to OPEN; (4) X-14 verifier outside the kernel (12 HIGH open) reopened to "placement open, both carried" (C-057, C-083, X-010); (5) C-01 two clusterers with `cluster_v2` withdrawn, now with V1's remedy carried (INV-024). Only (1) has a downstream gate: V2 C16 "any edit of `ensemble.py` ... needs its own decision" (V2:4445). Falsifier: a precedence table "rebuilt against the merged Section 7" that lists these 5 as V2 outcomes is wrong |
| INV-029 | sufficiency_challenge | C-01's governing shape holds now because "convergence triggers T-a, T-b, T-c have not fired" (V2:3511) | UNADDRESSED | HIGH | Trace: T-c = "a verified defect fix needs a non-helper edit to both parsers or both clusterers" (V2:3636). The consensus carries D6 as verified: "CONFIRMED on both stacks" (v1 `findings.py:382-407`, v2 `cluster.py:302-320` same union-find, chains flagged not split), remedy "complete-link or size-capped components" (V1:594). V2's design avoids T-c only by keeping v1 union-find and adding a chain guard in v2 only (V2:3743, V2:3771), i.e. by leaving the measured over-merge (83 mega-rows replay v1 rules, V2:1361) in the spec loop. So T-c's condition is met by an agreed fact unless the owner accepts that defect; advocates frame it as a future "if the merge adopts the remedy" choice (r2-advocate-V2.md:43). Falsifier for "V2 base yields a usable plan input": the plan cannot fix an engine layout until this owner decision is made |
| INV-030 | sufficiency_challenge | Carried V1 debate outcomes bring their open HIGH invariants with them | UNADDRESSED | MEDIUM | Enumeration of V1's 4 debates (V1:2862-2867): C-03 (2 HIGH), C-05 (11), C-13 (10) superseded by V2 outcomes; C-14 panel size (3 HIGH, e.g. INV-009 "the rollback tripwire cannot observe the legacy path", INV-012) is carried (C-073, C-093 = V1) but neither R2 must-carry list carries its invariants or V1 Q-47..Q-50, and the merged register is V2 7.3 only (244 V2 rows). One superseded V1 invariant still binds the adopted design: C13-22 INV-014 (version skew, see INV-003). Downstream gate: none |
| INV-031 | sufficiency_challenge | Carrying V2 C4 ("`feat/review-panel` and `feat/review-panel/<name>` cannot both exist") keeps the git-ref constraint the plan needs | UNADDRESSED | MEDIUM | Owner names are `feat_review-panel/<name>`, i.e. V1 layout B with a new prefix; the operative constraint is now "no branch `feat_review-panel` (bare, local or remote-tracking) while any `feat_review-panel/<name>` exists" (C4's W03 note on packed and remote-tracking refs, V2:4433). Dropping V1's layout table also drops layout B's consequence "cannot later create an umbrella ... without deleting all children" (V1:4066). Own check: `git check-ref-format --branch` accepts both `feat_review-panel` and `feat_review-panel/core` (the clash appears only at creation); `git for-each-ref` and `git ls-remote --heads origin` show no such refs today. Neither advocate restates C4 for the chosen prefix (grep `feat_review`: naming mentions only). Downstream gate: git refuses at creation (exit 128 per C4), loud but late |
| INV-032 | sufficiency_challenge | The merged gate set is runnable as no-regression gates for the plan | ADDRESSED | MEDIUM | Enumeration of gates that cannot run before the build: V2 G18 (no command), G21 (not run), G23-G27 (named measurements, none exists in code) (V2:4483-4492); V1 G-bench "does not exist until M1-17 builds it" (V1:4054); "accepted" unreachable while identity is `unrecorded` (V2:3644, Q-44). Both advocates state this (S-056 rows; r1-advocate-V1.md:50) and require "adjudicated default, partial" labels (A-052) |

### Summary

- Total findings: 32
- ADDRESSED: 8 (INV-002, INV-009, INV-010, INV-012, INV-013, INV-014, INV-017, INV-032)
- UNADDRESSED: 24
  - HIGH: 7 (INV-003, INV-006, INV-018, INV-024, INV-027, INV-028, INV-029)
  - MEDIUM: 13 (INV-001, INV-004, INV-005, INV-007, INV-008, INV-011, INV-016, INV-020, INV-021, INV-025, INV-026, INV-030, INV-031)
  - LOW: 4 (INV-015, INV-019, INV-022, INV-023)
- No consensus verdict conflicts with a fact in "Orchestrator Verification of Contradictions"; the only tension is the CL-18 cluster label (INV-017).
- Id note: the INV-nnn ids of this file collide with debate-local INV ids in both reports (INV-019); cite them as "R25-INV-nnn" in the merge.

### Fault-finder notes (re-derived numbers, reasoning by category, corrections the merge must apply)

#### Round 2.5 Fault-Finder Notes (long form)

- Role: independent fault-finder, not an advocate. Output table: `adversarial/invariant-probe.md` (32 findings: 8 ADDRESSED, 24 UNADDRESSED; 7 UNADDRESSED HIGH).
- Inputs read: `partials/consensus-summary.md`, `convergence-r1.md`, `convergence-r2.md`, `r2-state.json`, `orchestrator-verification.md`, `point-cluster.json`, `debate-points.md` (full), `diff-analysis.md` (lines 1-470 in full), `r2-advocate-V1.md` and `r2-advocate-V2.md` (full), `r1-advocate-V1.md` (lines 1-110 and 244-413), and range reads of both variants (V2:1640-1735, 3505-3674, 4426-4493; V1:594, 2641-2657, 2862-2867, 3826-3908, 4030-4069) plus Grep over both.
- Read-only: only this file and `invariant-probe.md` were written. No git write. Nothing under `.claude/` or `~/.claude/` read. Python only through `uv run`. Two batched read-only scripts followed the batching policy (both `BATCH_OK failures=0`, private dirs removed). Test collection used `--collect-only -p no:cacheprovider` with `PYTHONDONTWRITEBYTECODE=1`. One external fetch (arXiv abstract page).
- Citation form: `V1:L` / `V2:L` = line of `variant-1-original.md` / `variant-2-original.md`; X-, C-, S-, A-, U- ids are `diff-analysis.md` ids.

#### 1. Re-derived numbers

| # | What | Command or file | Result | Who was right |
|---|---|---|---|---|
| 1 | Code at HEAD equals the reports' HEADs | `git diff --stat 50d4d2b9d HEAD -- src tests scripts`; `git status --porcelain -- src tests scripts` | empty; clean | Both (cites hold at `ad8f57560`) |
| 2 | HEAD against `origin/master` | `git diff --stat origin/master HEAD -- src tests scripts`; `git rev-list --count HEAD..origin/master`; merge-base | 50 files differ; `origin/master` (`d4d1662a8`, 2026-11-14 12:42) is 3 commits past merge-base `d2d8a2d16`; HEAD is 5 commits past it | Neither report; V1:4061 "3 commits ahead" is now 5 (V2 advocate caught that); nobody noticed `origin/master` moved |
| 3 | Cited lines on `origin/master` | `git show origin/master:<file> \| sed -n` vs HEAD | `test_worker_contract.py:777`->787, `:1861`->1872, `:786`->796; `pragmatic.md:225`->229, `:231`->235; reflect `SKILL.md:343` text differs; `SKILL.md:703` same | V2's C14/C26 citations are HEAD-only |
| 4 | E2 commits | `git rev-list --count 4a22d74..6c09843`; `6c09843..e2f2ac268`; `git diff --stat 6c09843 e2f2ac268` | 4; 7; 767 files, +43,936/-152; cited E2 files untouched | V2 (pins the later tip); the 7-commit gap is new information |
| 5 | Tests collected | `uv run pytest --collect-only -q -p no:cacheprovider <dir>` | `tests/review` 651; `tests/cli/reflect` 353; `tests/pr_submit` 2258 | V1 |
| 6 | Test files | `ls tests/cli/reflect/test_*.py`, `tests/review/test_*.py`, `tests/pr_submit/test_*.py`; `git ls-files 'tests/pr_submit/*.py'` | 38; 19; 47 (49 tracked .py) | V1 G9 "38" right, V1:381 "37" wrong; V2 G14 "50 test files" wrong, V2 U-122 "47" right |
| 7 | Engine-A contract keys | `uv run python` regex over `ensemble.py:787-832` plus `panel_lint` constants | 32 literal keys; `t2_fallback` at `:833-834` (default None `:363`); outside STABLE (110) and TELEMETRY (27) = 10; outside STABLE only = 11; stable present 21 (89 absent) | Both, with basis: default run 32/10 (V2), with the fallback flag 33/11 (V1); V1's "in neither list" rules out the "outside STABLE only" reading of its 11 |
| 8 | rf-* spawn lines | `grep -rEn 'subagent_type: *"?rf-' src/superclaude/skills` | 52 lines, 11 files, 8 of them `SKILL.md` | V2 (orchestrator agrees; V1's 43 is an unstated unit, not reproducible) |
| 9 | `superclaude review` in reflect skill | `grep -c` / `grep -o \| wc -l` | 5 lines, 7 occurrences | Neither (V2 "(6)" wrong) |
| 10 | Exit codes today | `ledger_cmd.py:13`; grep for 12 in `cli/review`, `cli/reflect` | `{PASS 0, REVISE 10, ESCALATE 11}`; no 12 | Both (status quo) |
| 11 | Citation-only line on the merge path | `findings.py:102-106, 186-193, 346-350`; `ledger.py:127-138` | rejected at `:104`, skipped at `:191-192`, `annotate` only on accepted findings | V1 (orchestrator agrees) |
| 12 | Clearing by silence, union | `ledger.py:186-188, 252-258` | `any(m["blocking"]...)`; `resolved_check` absent next round becomes `resolved` | Both (fact) |
| 13 | Distinctness default, re-review size | `panel.py:509, 575` (`strict_distinct: bool = False`), `:539-543`, `:600-605` | soft by default; re-review resolves fixed slots only, count 1 | Both; V2's "re-review is one reviewer" right |
| 14 | Slot key schema | `panel.py:46`, `:215` | closed `_SLOT_KEYS = {slot_id, tier, count, strategy, seed}`; unknown slot keys rejected | New fact (affects carried V1 per-slot keys) |
| 15 | Calibrator dimensions | `confidence-calibrator.md:3`; reflect `SKILL.md:1262, 1835` | 6-dimension vs 5-dimension | V1 |
| 16 | Plugin mirror size | `git ls-files plugins/superclaude \| wc -l` | 125 | V2 |
| 17 | Lint registration | `cli/review/__init__.py:19-37` | `lint_cmd`, `estimate_cmd` in the tuple; `ModuleNotFoundError` for the module itself swallowed | Both (fact) |
| 18 | Invariants in V2 7.3 | awk over V2:3962-4232 rows `^\| (C\|X)-n INV` | 244 rows: HIGH 60, MEDIUM 161, LOW 23; every HIGH row status OPEN | V2 (60) matches C-075's per-debate sum 1+3+2+0+7+4+1+13+0+5+6+2+2+12+2 = 60 |
| 19 | V1 invariants | V1:2620, V1:2862-2867 | stated 26 = 2+11+10+3; C-03 row lists one id only, so the "2" is not recountable from the table | V1 stated; partly unverifiable |
| 20 | Gates | grep of V1:4030-4056 and V2:4464-4492 | V1 19 (G1-G11 + G-all, G-bench, G-exit, G-new, G-pr, G-replay, G-skills, G-sync); V2 27 (G1-G16 code pins, G17-G27 adjudicated) | Both; different units |
| 21 | Constraints, dependency facts | grep V2:4428-4528 | C1-C29 = 29; D1-D26 = 26 | V2 |
| 22 | Open questions | `grep -oE '^\| Q-[0-9]+' \| sort -u` | V1 61 unique (122 rows incl. sub-tables); V2 93 | Both |
| 23 | Inventories | `grep -c '^\| V-'` V1; synth-08 per-source table | V1 698 (91 DROP; plus 4 parse-artefact destination cells); V2 886+868+1,685+955+796+589+171 = 5,950, DROP 1,969 (1,753 duplicates) | Both; different units |
| 24 | Debate-point denominator | `debate-points.md` vs diff-analysis Summary vs `sc-adversarial-protocol/SKILL.md:864-870, 1392` | 234 (56+97+63+18) vs 275 (all 59 A); skill counts promoted A only | 234 is right; diff-analysis Summary line is stale |
| 25 | Convergence resolution | r2-state.json | 224 agreed include 6 both-OPEN points | Resolved 218/234 = 0.932 |
| 26 | arXiv 2606.19544 | WebFetch `https://arxiv.org/abs/2606.19544`; run-2 QA P6-054 (`qa-consolidated-findings-phase6.md:76`) | "withdrawn by arXiv Admin", v1 17 Jun 2026, v2 3 Nov 2026 (withdrawn) | V1's exclusion; V2 uses it at V2:1647-1648, 1655, 2044, 2829 (and coverage rows 2072, 2078) |
| 27 | CLI tool-restriction flags | `claude --help` (2.1.325) | `--tools` = built-in set only; `--restricted` removes code-running tools and WebFetch, ignores settings files, refuses bypassPermissions, and needs `--strict-mcp-config` to skip MCP servers | V2's mechanism is right for built-in tools, incomplete for MCP; both advocates missed MCP |
| 28 | Existing restricted launcher | `pipeline/process.py:134-166`; `runner.py:488-499, 566`; `ensemble.py:535-561` | `reviewer_profile=True` drops `--dangerously-skip-permissions` and `--tools default` | Neither report mentions it |
| 29 | `unauthorized_deviation_present` producer | grep over `src/superclaude/**/*.py`; `ensemble.py:451-454, 527-561` | only defaults; the Mode-A child populates convergence and report path only | V1 (MS-14, U-001) |
| 30 | `merge_method` in debate contract | grep `src/superclaude/skills/sc-adversarial-protocol` | 0 hits for `merge_method` or `merged-verdict` | V1 (MS-24, U-002) for the src copy |
| 31 | Branch names | `git check-ref-format --branch feat_review-panel/core` and `feat_review-panel`; `git for-each-ref`; `git ls-remote --heads origin` | both names valid alone; no `feat/review-panel*` or `feat_review-panel*` ref locally or on origin; only `ironbelly/eval-tasklist-review-panel` contains `review-panel` | V2 C4 facts hold; the constraint text needs the new prefix |

#### 2. Reasoning by category

### Category 1: state variables

- **Line-number base (INV-001).** Both advocates accepted A-002/A-036 after checking lines at HEAD. That is the wrong reference for a plan: by project rule and V1:4061, new branches are cut from `origin/master`, and `origin/master` has moved 3 commits since the merge base. It removes nothing the reports cite in `cli/review`, but it does move test and output-style lines that V2 cites as binding constraints (C14, C26) and as the basis of the X-15 adjudication (`pragmatic.md:225,231`). It also lacks the 3 shadow-run commits, so the reflect `SKILL.md` text at `:343` and the pins in `test_shadow_skill_contract.py` differ until `ironbelly/shadow-runs` merges. The A-036 rule "re-read every cited line before editing" protects edits but not the merged document's own cells.
- **Ledger persistence (INV-003).** This is the clearest shared error. V1's persisted-format rule (V1:3830) and V2's "keep `review-ledger/1`" (A-9) each look safe alone. Together, with V2's semantic change (silence never clears, verdict derived and no longer stored), they recreate the version skew that V1's own ledger debate closed with `min_writer` and a `/2` bump (C13-22 INV-014, V1:2657). An older installed `superclaude` (pipx installs on other machines are normal) loads the ledger because `load` checks only the schema string, then `merge_round` clears rows by silence again; `ledger.verdict` raises `KeyError` on the new round because it reads `last["verdict"]`. V2 itself records the second half (A-9 "older binaries that read `last["verdict"]` fail (INV-018, open)"). V1's reload test ("previous reader tolerates unknown keys") would pass and so would certify the hazard.
- **Debate state (INV-004).** The 10 disputed points are mostly an artefact of cluster inheritance. The V1 advocate's own R1 exceptions (C-017 V2, C-025 V2) were overwritten when the R2 cluster label became "V1". The merge must use point-level verdicts from the advocate files, not `r2-state.json` inheritance or the consensus-summary cluster column.
- **Quorum denominator (INV-005).** V2 Q-42/Q-52 leave `requested` undefined at merge time; V1 C13-06 already answers it (`panel_size`, `quorum`, `valid`, `denominator_source` on the round entry). Neither must-carry list carries that answer.

### Category 2: guard conditions

- **Read-only lane (INV-006, INV-007).** Both advocates corrected V1's `--allowedTools` to `--tools` / `--restricted` / `--disallowedTools Bash`. The local help shows the corrected set still leaves MCP servers loaded (`--tools` is "from the built-in set"; `--restricted` explicitly needs `--strict-mcp-config` to skip MCP). In this environment MCP servers include write-capable tools, so INV-G ("mechanically read-only") is not met by the agreed flags. `--restricted` also refuses `bypassPermissions`, so E2's launcher pattern cannot be reused as is, and it confines file tools to the working directories (the reviewer's snapshot root must be the cwd or an `--add-dir`). Separately, the product already has a restricted `claude --print` child (`pipeline/process.py` `reviewer_profile`), used by engine A; neither report considers reusing it or the soundness of its permission-prompt basis.
- **Fail-open claim (INV-008).** The V1 advocate's R2 concession that V2's C-06 refusal "closes the fail-open path" overstates V2. The acknowledgement is unbound (C-06 INV-006), the acknowledged-drop flag state is undefined (X-14 INV-019 HIGH), and `blocking_state` is taken from the reviewer's own flag (Q-60). The merged text must say "narrowed", not "closed".
- **Boundaries checked and found handled:** one-reviewer re-review (INV-009), duplicate models filling a quorum (INV-010, recorded as data by V2 C-03; the default itself is OPEN), zero valid blocks (`ledger.py:148-152` still refuses at zero valid blocks; V2 C18 says the quorum refusal rewrites that pin). Citation-only findings in the spec loop are rejected (fact verified) and, under C-06, a dropped blocking one triggers the refusal, which is fail-closed.
- **Reserved slot keys (INV-011).** `panel.py` rejects unknown slot keys, so "reserved" must be defined as document-only (as V2 X-13 does for its reserved items) or as a code change with golden regeneration.

### Category 3: count divergence

All disputed counts were re-derived (table above). Results: V1 is right on test counts, the 1,398 unit, the calibrator mismatch and the 33/11 key count under its basis; V2 is right on spawn lines, pr_submit file count (47, in U-122) and plugin size; both are wrong somewhere (V1 "37 files", V2 "50 test files", V2 "(6)"). Two counting-method problems were not raised by anyone: the diff-analysis Summary's 275 denominator (INV-015) and the convergence figure counting six both-OPEN points as resolved (INV-016). The cluster-level summary also masks point-level OPEN verdicts (X-058 under CL-04, X-040/X-056 under CL-03) and the 5 V2-verified points under CL-18's "V1" label (INV-017).

### Category 4: collection boundaries

- **Gate list (INV-018).** The agreed recipe for S-056 keeps V1's gate list and appends V2's G17-G27. That silently drops V2's G1-G16. Five of those have no V1 counterpart (lint-architecture, ruff, verify-deps; installed-path baseline; routing plugin parity; the rf-qa static pins under `tests/audit/`; contract-constant and generator-constraint checks). Worse, carried V2 constraints and adjudicated gates refer to V2 gate numbers (C19 "(G1)", C20/C21/C27/G17/G22 "(G8)", C23 "(G14)", C25 "(G15)", C26 "(G11)", G19 "(G3, G7)", G20 "(G1)"). Under V1 numbering those names bind to other suites or to nothing. Fix: keep both gate lists, re-keyed (for example R1-G8, R2-G8), and rewrite every cross-reference.
- **Ids (INV-019).** Report prefixes fix cross-report clashes; intra-report clashes (V1 C-nn twice; V2 AE-1 twice, G1-G3 twice, D-1 twice, M1 three ways, INV-nnn per debate) need composite keys.
- **Inventories (INV-020, INV-023).** No cross-report de-duplication rule exists; 93 V1 rows point at V1 components the merged design does not adopt; V2's rows live only in a 2 MB task-folder file, so the pointer must carry a commit.
- **Withdrawn source (INV-021).** The drop list misses V2:1655 and V2:2829 (and two coverage rows).
- **Unique rows (INV-022).** 62 Medium/Low U rows were never cross-checked; four spot checks found no error.
- **Empty or single-element cases:** CL-26 has 0 points (no verdict needed); U rows with one source were spot-checked; one-reviewer and zero-finding rounds are handled (Category 2).

### Category 5: interaction effects

- **T-c cascade (INV-024).** Both advocates found that V1's clustering remedy in both engines fires T-c. They did not trace what reopening C-01 does: by V2's own conditions it reopens C-05 and X-15 directly, reopens constraint C26, and touches C-06 and C-11 through C-02/C-03. The owner question must be stated with that cascade.
- **Exit code 12 (INV-025).** V2's adopted design already gives 12 two meanings (quorum refusal and dropped-blocking refusal, which "record nothing" in sequence); V1's carried 6.E rows use 12 for PENDING and the installed ledger uses it for CONTINUE. "One meaning for exit 12" is a V1-advocate requirement the consensus does not meet. Proposal: 12 = "refusal" with a mandatory `refusal.kind` record, or separate codes.
- **V1 G2 must-not-change pins (INV-026).** V1's G2 forbids changing the exact `verdict()` dict and the final `verdict:` line; V2's adopted axis 4 removes stored verdicts and derives new fields. V2's own rewrite list (C18) also omits these pins.
- **E2 pins in one document.** No contradiction found from mixing V1 facts at `4a22d74` with V2 facts at `6c09843`: every V1 E2 fact the consensus carries (judge sees combo name, 1,398 unit, audit D flips, Qwen 3 of 4) was verified at `6c09843` by the analysts or corrected to V2's value, and the 7 later commits do not touch the cited E2 files.
- **"No engine moves now" vs fix-in-place.** Covered as a sufficiency item (INV-028 (1)): the consensus moves the default without the invariant analysis that V2's C-04 had.
- **Branch layouts vs git-ref constraint.** Covered as INV-031.

### Category 6: sufficiency challenge

**(a) "V2 as base plus V1 insertions yields a merged document a later `/sc:workflow` plan can use."** Falsifying conditions found:
1. INV-027: 13 of V1's 48 steps conflict outright with adopted V2 outcomes and 14 partly. Carrying them "re-based" requires a step-by-step re-adjudication nobody has done; V1's gap-to-step map depends on those ids.
2. INV-018: the agreed gate recipe loses five no-regression gates and mis-binds 11 gate references.
3. INV-029: the governing core shape is conditional on an owner decision that is already due (T-c is met by the agreed D6 fact unless the v1 over-merge is accepted).
4. INV-003: the carried persistence rule plus the adopted ledger design re-open a version-skew hazard.

**(b) "The adjudicated outcomes are safe to carry as the recommended design."** V2's 60 HIGH invariants are all OPEN (verified) and are carried as plan gates and questions, which is the right treatment. But INV-028 enumerates five V2 adjudications the consensus changed without a new debate or fault-finder pass, including the replacement of V2's strongest outcome (C-04: 6.91 percent margin, no tiebreaker, no HIGH invariant) by V1's never-debated C-17 remedy. INV-030: V1's carried C-14 outcome loses its 3 HIGH invariants.

**Gates between the consensus and the merged output, and whether the consensus input passes them:**

| Gate | Passes? | Why |
|---|---|---|
| Merge executor applies per-point verdicts | No, not as handed over | consensus-summary is cluster-level; it masks point-level OPEN (INV-016), mis-labels CL-09 and CL-18 (INV-004, INV-017) |
| Precedence table rebuilt against the merged Section 7 (both R2 lists) | Not yet | the five changed adjudications (INV-028) must be rows in it |
| Id namespacing (A-006, A-058) | Partly | cross-report rule agreed; intra-report and gate cross-references not handled (INV-018, INV-019) |
| Owner scope filter: no roadmap, branch plan, PR plan or schedule | At risk | the 48 steps carry implicit order (M-numbering) and conflicting content (INV-027); V1 8.6 ordering clause is dropped (agreed) |
| Owner constraints: `feat_review-panel/<name>`, fork-only PRs | Partly | C4 carried literally for `feat/review-panel` (INV-031); fork-only rule carried (C9) |
| Facts re-verified at the base the plan will use | No | checked at HEAD only (INV-001) |
| Withdrawn or wrong sources removed | Partly | 2 of 4 arXiv-dependent sites missed (INV-021) |

#### 3. Concessions and one-sided rows

- **Concessions resting on a wrong or overstated fact:** V1 advocate R2 "V2's C-06 closes the fail-open path" (INV-008); both advocates' "`--tools`/`--restricted` gives read-only" (INV-006). Earlier wrong concessions were already withdrawn in R2 (V1 advocate's "no raw-id read-only requirement"; V2 advocate's "V1 ignores open Bash", "measured H1 lever", "labels do not exist").
- **Concession slightly overstated:** "43 call sites does not reproduce" is treated as a wrong count; the orchestrator calls it an unstated unit. The merge should say "43 (unit unstated, not reproducible); 52 lines in 11 files, 44 in 8 `SKILL.md` files", not "43 is false".
- **One-sided U rows never challenged:** all 62 Medium and Low U rows (U-004, U-006..U-009, U-011..U-017, U-019, U-028, U-030, U-033, U-034, U-038, U-039, U-041, U-043, U-050, U-052, U-053, U-055, U-057, U-059..U-063, U-067, U-069, U-070, U-078..U-085, U-089..U-095, U-103..U-109, U-119..U-124). Spot-checked U-001, U-002, U-052, U-122: correct.
- **Orchestrator-verified facts vs consensus verdicts:** no conflict. Every VERIFIED-V1 / VERIFIED-V2 / VERIFIED-BOTH row maps to the matching point verdict; design-choice rows were debated, not verified.

#### Corrections the merge must apply

Wrong or incomplete facts that both advocates accepted, or that nobody caught:

1. **Read-only mechanism:** a raw-id `claude -p` reviewer needs `--tools <read-only set>` (or `--restricted`) PLUS `--strict-mcp-config` with no or a read-only `--mcp-config`; `--restricted` refuses `bypassPermissions` and confines file tools to the working directories. The C-07 G2 gate must check the MCP server list from the `system/init` event. (INV-006)
2. **Existing launcher:** record `src/superclaude/cli/pipeline/process.py:145-154` (`reviewer_profile=True`) as an existing restricted `claude --print` child launcher used by reflect (`runner.py:566`, `ensemble.py:548`); the "gated, not built" launcher must say whether it reuses or replaces it. (INV-007)
3. **Ledger version skew:** do not combine "keep `review-ledger/1`" with changed clearing and verdict semantics under V1's "keep schema string, new keys optional" rule; carry V1 C13-22's `min_writer` plus `review-ledger/2` remedy (or an explicit owner acceptance of the skew), and drop the claim that an old reader tolerating unknown keys is safe. (INV-003)
4. **Quorum denominator:** carry V1 C13-06's round-entry fields (`panel_size`, `quorum`, `valid`, `denominator_source`) as the answer candidate to V2 Q-42/Q-52. (INV-005)
5. **Fail-open wording:** V2's C-06 refusal narrows, not closes, the fail-open path (unbound acknowledgement, C-06 INV-006; X-14 INV-019). (INV-008)
6. **Gate list:** keep V2 G1-G16 as well as V1's gates and V2 G17-G27, re-keyed by source, and rewrite the gate cross-references in V2 C19-C27 and G17-G22. Remove V1 G2's "must NOT change" on `test_review_ledger.py:299-304` and `:468-472` or mark it conditional on the non-adopted V1 verdict design; add them to V2 C18's rewrite list. (INV-018, INV-026)
7. **Withdrawn paper:** also remove or re-source V2:1655 (verbosity rationale) and V2:2829 (33-41 points in the Section 6 Cons cell) and fix coverage rows V2:2072 and V2:2078. (INV-021)
8. **T-c:** state that D6 (confirmed on both clusterers, V1:594) already meets T-c unless the owner accepts the v1 over-merge, and list the cascade C-01 -> C-05, X-15, C26 (and C-06, C-11 via C-02/C-03). (INV-024, INV-029)
9. **Reopened adjudications:** mark C-04, C-09, C-11, X-14 and C-01 (clustering) as "reopened or changed by the compare debate" in the rebuilt precedence table, with V1 C-17's fix-in-place labelled "never debated; no invariant probe". (INV-028)
10. **Exit 12:** state that V2's adopted design uses 12 for two refusals (C-06 INV-020) and that V1's PENDING and the installed CONTINUE are other meanings; either one code with a mandatory `refusal.kind` or separate codes; keep X-058 as an open owner question. (INV-025)
11. **Line base:** state that line numbers are valid at `ad8f57560` (`ironbelly/shadow-runs`); on `origin/master` `d4d1662a8` the pins in V2 C14/C26 sit at `test_worker_contract.py:787, :796, :1872` and `pragmatic.md:229, :235`. (INV-001)
12. **Git-ref constraint:** restate C4 for the owner's prefix: no branch `feat_review-panel` (local, packed or remote-tracking) while any `feat_review-panel/<name>` exists; an umbrella branch, if wanted later, needs a non-prefix name. (INV-031)
13. **Reserved slot keys:** say "reserved in the document only" or name the `_SLOT_KEYS` change (`panel.py:46, :215`) and its golden regeneration. (INV-011)
14. **Debate bookkeeping:** C-017 and C-025 are V2 (V1 advocate R1 exceptions); the real remaining disputes are C-005, C-076, X-051; convergence of resolved points is 0.932 (218/234), and the diff-analysis Summary's "275" denominator is wrong (234). (INV-004, INV-015, INV-016)
15. **Inventories:** de-duplicate V1's 698 rows against V2's 5,950 before carrying both; re-route the 93 V1 rows aimed at non-adopted V1 components; pin the synth-08 pointer to commit `ad8f57560`. (INV-020, INV-023)
16. **V1 C-14 invariants:** carry its 3 HIGH invariants (INV-009, INV-012 and the third, V1:2867) and Q-47..Q-50 with the C-14 outcome. (INV-030)
17. **Counts to state with units:** engine-A contract 32 keys / 10 outside both lists by default, 33 / 11 with the fallback flag; rf-* 52 lines in 11 files (44 in 8 `SKILL.md`), V1's 43 unit unstated; pr_submit 47 test files; reflect 38 test files; `superclaude review` in the reflect skill 5 lines / 7 occurrences; E2 later commits: 7 after `6c09843`. (INV-012, INV-013, INV-017)

## Scoring Matrix

Winner = the verdict both advocates converged on after Round 2 (cluster-level verdicts inherited by points without their own row; point rows override). `Both (merge)` means both reports' content is needed. `Open` means both advocates mark it undecidable by the evidence (owner decision). `Unresolved split` means the advocates' final verdicts still differ. Confidence = mean of the advocates' stated confidences, capped at 95%, 50% for open and split points. Evidence is the advocate's own evidence cell (truncated); full evidence is in partials/r1-*.md and partials/r2-*.md.

| Diff Point | Cluster | Winner | Confidence | Evidence Summary |
|---|---|---|---|---|
| S-040 Whole-design options | CL-01 | Both (merge) | 62% | V2 6.1 has the fuller option set A-D incl. "fix the harness only" (V2:3636 lists all four); V1 6.X adds the layer diagram (V1:2544-2555) and the future-consumer fit rows (V1:2618) that V2 has only per consumer in 7.2.4. Base = V2' |
| C-005 Shape of the shared core | CL-01 | Unresolved split | 50% | V1 advocate: Both (merge); V2 advocate: Variant 2. Governing shape = V2's thin shared contract, "adjudicated default, partial" (V2:3511, V2:3578). The one-engine alternative already exists in V2 (6.1 Option A, V2:2184; "recorded p |
| C-050 Core location and shape | CL-01 | Both (merge) | 60% | V2 axis 6.1 Option C adjudicated with triggers (V2:3636); V1's Option B rated XL, Medium-High (V1:2578-2579) stays the recorded one-engine target. V1's rejection of C (V1:2622) is aimed at a weaker C than V2's (V2:1135), conceded. |
| C-061 Clustering | CL-01 | Both (merge) | 60% | Which clusterer: follows the core-shape default, so V2's per-engine placement (V2:3743). The remedy: V1-only (complete-link admission, no merge on an empty location, anchor-to-citation step, acceptance by the 83 mega-rows falling  |
| C-076 Shape of the recommended core (Sec 7) | CL-01 | Unresolved split | 50% | V1 advocate: Both (merge); V2 advocate: Variant 2. Same as C-005 at Section 7 (V2:3578 vs V1:2823). |
| C-090 Clustering | CL-01 | Both (merge) | 60% | Same as C-061 at Section 7: V2's "two deterministic merges, one per engine" (V2:3743) plus V1's clustering remedy and acceptance metric (V1:2850, V1:1988) as the "verified merge defect ... fixed in the engine that has it". |
| X-002 One finding contract / one clusterer / one merge vs two grammars and t | CL-01 | Variant 2 | 60% | Two grammars avoid rewriting the pinned v1 path (V2 delta V2:1134, axis 2 V2:3637); V1's single contract (V1:494) stays the convergence target. |
| X-038 Shape of the shared core | CL-01 | Variant 2 | 65% | The disagreement is where to *start*: V1 starts from findings-v2 as the single contract (V1:2622), which needs v2 to accept `prior` lines and `calibrated_confidence` (`findings_v2.py:96-97,279-281`; V1's own Cons V1:1211); V2 star |
| X-042 Which clusterer the core uses | CL-01 | Both (merge) | 58% | V2's objection "`cluster_v2` leaves anchor-only findings as singletons" is answered in the cited V1 line itself ("an anchor-to-citation step", V1:1988); V1's objection that V2 has no remedy stands (V2:3743). Under the two-engine d |
| X-051 Which engine shape the unified Review Panel should have | CL-01 | Unresolved split | 50% | V1 advocate: Both (merge); V2 advocate: Variant 2. Same as C-005; end shape not evidence-decided (X-052 agreed), V2's adjudicated default governs with Q-40 open. |
| C-051 Finding contract / grammar | CL-02 | Variant 2 | 58% | Two grammars with shared ids, limits, repair (V2:3027); V1's single contract as target. |
| C-053 Invalid-block unit of loss | CL-02 | Unresolved split | 50% | V1 advocate: Variant 1; V2 advocate: Variant 2. V2 A-14 keeps `pr_submit.Finding` untouched and computes `in_diff` from changed ranges in a pure converter (V2:3665); `in_diff` exists nowhere in `cli/review` today (diff-analysis X- |
| C-066 Brief / input contract | CL-02 | Variant 2 | 60% | A converter on the `pr_submit` side leaves `Finding`, FSM and `REVIEWERS` untouched (V2 axis 2 V2:3637, A-14 V2:3665); V1's lens extensions (V1 BL-18 V1:622, M4-04 V1:3905) widen the contract. Exception: C-053 goes to V1 (explicit |
| C-088 PR code review integration | CL-02 | Variant 2 | 60% | See X-007. |
| X-007 PR-review fields in the finding contract | CL-02 | Variant 2 | 60% | A converter computes `in_diff` without touching findings-v2 or `pr_submit.Finding` (V2 delta V2:1141, V2:3735); V1 BL-18 (V1:622) widens the core. |
| X-059 Whether PR-specific fields enter the finding contract | CL-02 | Variant 2 | 60% | Same as X-007; `in_diff` has 0 hits today. |
| C-052 Over-limit lines (200/300 limits) | CL-03 | Both (merge) | 65% | V2's adjudicated repair (three location fields to 200 behind `repair=False`, itemised drop record, dropped-blocking refusal, one re-ask; V2:3516) is the base; V1 adds the loss breakdown 24 anchor, 14 anchor2, 10 claim, 1 refs (V1  |
| C-077 Length limits and over-length lines | CL-03 | Both (merge) | 60% | Same as C-052 at Section 7 (V1:2840 vs V2:3638). |
| X-040 Does the claim field get truncated | CL-03 | Open (owner or evidence) | 50% | Both designs close the fail-open path (V1 SC-2 "cannot compute PASS", V1:527; V2 dropped-blocking refusal, V2:3516). What remains is whether to cut `claim` (10 of 49 blocking losses, V1:527; precedent `card_convert.py:200-201`) or |
| X-056 Whether to truncate the `claim` field | CL-03 | Open (owner or evidence) | 50% | Same as X-040 at Section 7 (V1:2840 vs V2:3638, V2:3656). |
| C-011 Ledger and verdict defects | CL-04 | Variant 2 | 68% | G-14, G-15, G-133..135 (V2:1249-1250, V2:1368-1370). |
| C-054 Who decides blocking | CL-04 | Variant 2 | 60% | See X-039. |
| C-056 Calibration role | CL-04 | Variant 1 | 65% | Round 1 exception to the cluster verdict (advocate's own exception list) |
| C-065 Blocking predicate / severity vocabulary | CL-04 | Unresolved split | 50% | V1 advocate: Variant 1; V2 advocate: Variant 2. No decider but the veto has ground-truth numbers (A-030), the stoprule integrity check returns `EXIT_OK` on a grader mismatch (diff-analysis X-039 verification) and V1's own debate f |
| C-078 Blocking decider | CL-04 | Variant 2 | 60% | See X-003. |
| C-080 Quorum and degraded outcome | CL-04 | Variant 2 | 60% | No decider except the veto has ground truth and the grader's integrity check returns `EXIT_OK` on mismatch (X-039 verification); V2 keeps typed `blocking` plus a CRITICAL floor (V2 A-4 V2:3655) and a concrete quorum refusal (A-3 V |
| C-087 "Medium" severity | CL-04 | Variant 2 | 60% | No decider except the veto has ground truth and the grader's integrity check returns `EXIT_OK` on mismatch (X-039 verification); V2 keeps typed `blocking` plus a CRITICAL floor (V2 A-4 V2:3655) and a concrete quorum refusal (A-3 V |
| X-003 Who decides blocking | CL-04 | Variant 2 | 60% | Only the veto has ground truth; V2 keeps typed `blocking` plus CRITICAL floor (V2:1137, A-4 V2:3655); V1's "separate measured decider" (V1 D4 V1:592) is a measurement precondition, not buildable now. |
| X-004 Reviewer quorum value | CL-04 | Both (merge) | 62% | Both reports end at `min(2, ·)` (V1 6.E C13-06 V1:2641; V2 A-3 V2:3654); each has a stale "decision" sentence elsewhere (V1:528, V1:591; V2 SC-04 V2:1180). |
| X-006 `medium` severity as a core token | CL-04 | Variant 2 | 62% | "Medium" has six meanings in the repo (V2:3637); a core token would fix one meaning (V1 SC-11 V1:536). |
| X-039 Who decides "blocking" in the core | CL-04 | Variant 2 | 60% | No accuracy data for any grader; stoprule integrity returns `EXIT_OK` on mismatch. V1 keeps the grader shadow-only, so its live behaviour already matches V2. |
| X-055 Who decides a blocking finding in the core | CL-04 | Variant 2 | 60% | Same as X-003. |
| X-058 Meaning of the new exit code 12 | CL-04 | Open (owner or evidence) | 50% | Both add exit 12 with different meanings (V1 PENDING grader V1:3841; V2 quorum refusal V2:3639); V1 notes an installed variant already uses 12 for CONTINUE (V1:3001). The merge must fix one meaning. |
| C-055 Ledger rounds, clearing, quorum | CL-05 | Variant 2 | 65% | V2 closes the design (silence never clears, verdict derived on read, `defer` terminal; V2 axis 4 V2:3639) and has G-14/G-15 (V2:1249-1250); V1 leaves a decision gate open (V1 C-13 V1:2052, risk row V1:2866). |
| C-063 Reflect merge path / contract | CL-05 | Variant 2 | 65% | V2 closes the design (silence never clears, verdict derived on read, `defer` terminal; V2 axis 4 V2:3639) and has G-14/G-15 (V2:1249-1250); V1 leaves a decision gate open (V1 C-13 V1:2052, risk row V1:2866). |
| C-064 Verdict contract and exit codes | CL-05 | Variant 2 | 65% | V2 closes the design (silence never clears, verdict derived on read, `defer` terminal; V2 axis 4 V2:3639) and has G-14/G-15 (V2:1249-1250); V1 leaves a decision gate open (V1 C-13 V1:2052, risk row V1:2866). |
| C-079 Round / ledger model | CL-05 | Variant 2 | 65% | See X-046. |
| C-085 Reflect contract writer / merge step | CL-05 | Variant 2 | 65% | V2 closes the design (silence never clears, verdict derived on read, `defer` terminal; V2 axis 4 V2:3639) and has G-14/G-15 (V2:1249-1250); V1 leaves a decision gate open (V1 C-13 V1:2052, risk row V1:2866). |
| X-044 One verdict contract vs per-engine verdicts | CL-05 | Variant 2 | 58% | `derive_verdict` is 36-test pinned and engine-neutral (V2 A-4 area V2:3639); V1's one machine verdict (V1:2447) needs a contract change reflect forbids without a bump. |
| X-046 Ledger rounds: open gate vs closed design | CL-05 | Variant 2 | 65% | V2 closes the ledger design; V1 leaves a gate (V1:2052). |
| C-012 Dispatch, identity and resolver | CL-06 | Both (merge) | 60% | The V2-side argument that V1 ignores the raw-id lane's open Bash is false (V1 C-18, V1:2320-2383, V1:2327). V2 contributes the correct restriction mechanism (`--tools`, not `--allowedTools`; V2:1725-1728) and the dispatch-layer an |
| C-037 Tier and class configuration | CL-06 | Both (merge) | 60% | The V2-side argument that V1 ignores the raw-id lane's open Bash is false (V1 C-18, V1:2320-2383, V1:2327). V2 contributes the correct restriction mechanism (`--tools`, not `--allowedTools`; V2:1725-1728) and the dispatch-layer an |
| C-038 Identity spike and collapse figures | CL-06 | Both (merge) | 60% | Round 1 exception to the cluster verdict (advocate's own exception list) |
| C-058 Dispatch mechanism | CL-06 | Both (merge) | 60% | The V2-side argument that V1 ignores the raw-id lane's open Bash is false (V1 C-18, V1:2320-2383, V1:2327). V2 contributes the correct restriction mechanism (`--tools`, not `--allowedTools`; V2:1725-1728) and the dispatch-layer an |
| C-059 Model tier source and environment | CL-06 | Both (merge) | 60% | The V2-side argument that V1 ignores the raw-id lane's open Bash is false (V1 C-18, V1:2320-2383, V1:2327). V2 contributes the correct restriction mechanism (`--tools`, not `--allowedTools`; V2:1725-1728) and the dispatch-layer an |
| C-067 Reviewer read-only enforcement | CL-06 | Both (merge) | 60% | V1 C-18 decides "allowlist everywhere; shell evidence computed by the orchestrator" (V1:2381); V2 adds INV-G and the `--tools` mechanism. V1's `--allowedTools` wording (V1:2332, V1:2381) must be corrected. |
| C-082 Dispatch and identity | CL-06 | Both (merge) | 60% | The V2-side argument that V1 ignores the raw-id lane's open Bash is false (V1 C-18, V1:2320-2383, V1:2327). V2 contributes the correct restriction mechanism (`--tools`, not `--allowedTools`; V2:1725-1728) and the dispatch-layer an |
| X-009 Core launches reviewers / gateway launch adapters | CL-06 | Variant 2 | 62% | `gateway` `launch: {}` and the raw-id lane is not read-only (V2:1139, V2:3640); V1's adapters (V1 MS-06 V1:633) need that safety condition first. |
| X-045 End-state dispatch design | CL-06 | Variant 2 | 62% | Same as X-009. |
| C-060 Distinctness default | CL-07 | Open (owner or evidence) | 50% | Removing silent re-admission is agreed by both (V1:1443; V2 always records `requested_slots`/`distinct_models`, V2:3657). The default (strict vs soft) has no measurement in either report (V2 A-6 "soft stands until A's M1"); V1's p |
| C-081 Panel resolution and distinctness | CL-07 | Both (merge) | 55% | The record fields are complementary, not competing: V2's `requested_slots`, `distinct_models`, tier-file guard test (V2:3594, V2:3657, V2:3747); V1's per-slot `none/model/class`, optional `replicas`, optional `role/lens/agent`, `t |
| X-041 Default distinctness of panel models | CL-07 | Open (owner or evidence) | 50% | Code shows soft today (`panel.py:509,519,575`; analyst ran `panel resolve` and reproduced V1:1436); no strict-vs-soft measurement exists. V1 labels only silence removal decided (V1:1443), V2 labels the default UNDECIDABLE (FX-15,  |
| X-057 Default distinctness behaviour of the resolver | CL-07 | Open (owner or evidence) | 50% | Same as X-041 at Section 7 (V1:2842 vs V2:3657). |
| C-034 Run record / telemetry | CL-08 | Variant 2 | 70% | Section 2 evidence: V2's writer/cost table with the `model_scores` double count (D-17) and the `manifest.save` lost update with a deterministic interleaving (D-23) (V2:569-578); V1 rows 13-14 (V1:454-455) state no race, and V1 has |
| C-057 Run record, manifest, telemetry | CL-08 | Both (merge) | 60% | V2's `events.jsonl` written only by code (V2:3518) for the record; V1's audits A and D as built-in checks before `published` (V1:1665, V1 MS-04 V1:631) for where checks live. V2's own margin is 0.13 percent (A-10, V2:3661). |
| C-083 Run record and telemetry | CL-08 | Both (merge) | 60% | Same as C-057 at Section 7 (V1:2845, V1:2954-2955 vs V2:3596, V2:3661, V2:3749). |
| X-010 Run record shape and where audit checks live | CL-08 | Both (merge) | 60% | The point has two halves: record shape (V2, events record; V1 has 0 `events.jsonl` hits) and audit placement (V1, MS-04 V1:631; V2 defers `verify-run`, V2:1143). |
| C-010 Post-gate engine (`ensemble.py`) | CL-09 | Variant 1 | 65% | Round 1 exception to the cluster verdict (advocate's own exception list) |
| C-017 Reflect Tier 2 convergence threshold | CL-09 | Variant 2 | 60% | Round 1 exception to the cluster verdict (advocate's own exception list) |
| C-018 Merge decision source for reflect (`merge_method`, `merged-verdict.yam | CL-09 | Variant 1 | 65% | Round 1 exception to the cluster verdict (advocate's own exception list) |
| C-020 E1 kernel merge facts | CL-09 | Both (merge) | 60% | V1 is right to fix the verified false-green post gate in place now (V1 C-17, V1:2314-2316) and to carry U-001/U-002/U-003; V2 is right that no engine replacement is ready, that deterministic shadow steps should be code-owned helpe |
| C-021 Where the swarm ensemble belongs | CL-09 | Both (merge) | 60% | V1 is right to fix the verified false-green post gate in place now (V1 C-17, V1:2314-2316) and to carry U-001/U-002/U-003; V2 is right that no engine replacement is ready, that deterministic shadow steps should be code-owned helpe |
| C-022 Engine A vs engine B depth | CL-09 | Variant 2 | 68% | A-vs-B table and six skill-vs-code disagreements (V2:173-197); V1's 9-row engine table (V1:416-426) is narrower. |
| C-023 Stage 2 shadow exit | CL-09 | Variant 2 | 68% | Failure classes by cause, `reflect_shadow_exit.py:313` defect (V2:207-229). |
| C-024 5x3 combination experiment | CL-09 | Both (merge) | 60% | V1 is right to fix the verified false-green post gate in place now (V1 C-17, V1:2314-2316) and to carry U-001/U-002/U-003; V2 is right that no engine replacement is ready, that deterministic shadow steps should be code-owned helpe |
| C-025 Reflect memory writes | CL-09 | Unresolved split | 50% | V1 advocate: Variant 2; V2 advocate: Both (merge). V1 is right to fix the verified false-green post gate in place now (V1 C-17, V1:2314-2316) and to carry U-001/U-002/U-003; V2 is right that no engine replacement is ready, that de |
| C-062 Reflect Tier-2 engines | CL-09 | Both (merge) | 58% | Same as CL-09: V1's in-place repair plus V2's code-owned helpers. |
| C-084 Reflect Tier 2 engine and post gate | CL-09 | Variant 1 | 65% | Fix `ensemble.py` in place now (V1:2855; M3-03..M3-07 V1:3886-3890) answers defects V2 itself rates Critical (G-42..G-44, V2:1277-1279). V2's "no change to `cli/reflect`" is only an adjudicated reading with enforcer "none" that sa |
| X-043 Fate of the code-driven Tier 2 engine | CL-09 | Variant 1 | 60% | Same evidence as C-084. On status I keep my Round 1 correction: "DECIDED" is wrong for the remedy; V1:2314 actually argues feasibility and V1:2316 leaves the final choice to the owner, so the corrected wording is "fix in place now |
| X-054 Reflect Tier 2 engine: touch `ensemble.py` now or not | CL-09 | Variant 1 | 65% | Same as C-084 (V1:2855, V1:3890 vs V2:3643, V2:4445); V2's code-owned shadow helpers writing comparison siblings (V2:3643) are compatible and also carried. |
| S-021 Consumers + future-use blockers | CL-10 | Variant 2 | 62% | V2's 14-consumer map and adjudicated entry (V2 2.7 V2:659-726; A-13 V2:3664) are deeper; V1 adds coverage modes X14 (V1 7.2 V1:2984-3006) and router-vs-rubric points (V1 BL-17 V1:621). Caveat: in C-05 the tiebreaker chose the lowe |
| C-006 Consumers in the target | CL-10 | Variant 2 | 62% | V2's 14-consumer map and adjudicated entry (V2 2.7 V2:659-726; A-13 V2:3664) are deeper; V1 adds coverage modes X14 (V1 7.2 V1:2984-3006) and router-vs-rubric points (V1 BL-17 V1:621). Caveat: in C-05 the tiebreaker chose the lowe |
| C-014 Future consumers (PR code review, rf-qa) | CL-10 | Unresolved split | 50% | V1 advocate: Variant 1; V2 advocate: Both (merge). Round 1 exception to the cluster verdict (advocate's own exception list) |
| C-040 Consumers: depth | CL-10 | Variant 2 | 62% | V2's 14-consumer map and adjudicated entry (V2 2.7 V2:659-726; A-13 V2:3664) are deeper; V1 adds coverage modes X14 (V1 7.2 V1:2984-3006) and router-vs-rubric points (V1 BL-17 V1:621). Caveat: in C-05 the tiebreaker chose the lowe |
| C-041 Entry-point decision for tasklist review | CL-10 | Variant 2 | 62% | V2's 14-consumer map and adjudicated entry (V2 2.7 V2:659-726; A-13 V2:3664) are deeper; V1 adds coverage modes X14 (V1 7.2 V1:2984-3006) and router-vs-rubric points (V1 BL-17 V1:621). Caveat: in C-05 the tiebreaker chose the lowe |
| C-068 Consumer entry for tasklist/workflow | CL-10 | Variant 2 | 62% | V2's 14-consumer map and adjudicated entry (V2 2.7 V2:659-726; A-13 V2:3664) are deeper; V1 adds coverage modes X14 (V1 7.2 V1:2984-3006) and router-vs-rubric points (V1 BL-17 V1:621). Caveat: in C-05 the tiebreaker chose the lowe |
| C-069 Future consumers (PR review, rf-qa) | CL-10 | Variant 2 | 60% | Consumer-first adapters (V2:3040); V1's X1-X14 exposure list (V1:2984-3006) kept as the checklist. |
| C-086 Tasklist / workflow entry | CL-10 | Variant 2 | 62% | V2's 14-consumer map and adjudicated entry (V2 2.7 V2:659-726; A-13 V2:3664) are deeper; V1 adds coverage modes X14 (V1 7.2 V1:2984-3006) and router-vs-rubric points (V1 BL-17 V1:621). Caveat: in C-05 the tiebreaker chose the lowe |
| C-089 rf-qa / rf-qa-qualitative replacement | CL-10 | Variant 2 | 58% | Lens-level first step with replay oracle (V2:3668); V1's coverage modes (V1:2976) kept as an option. |
| X-005 Entry point for workflow/tasklist review (DO4) | CL-10 | Variant 2 | 62% | V2 adjudicated reflect UC-1 as the entry (V2:1132, A-13 V2:3664); V1 leaves O-3 open (V1:635). V2's own G-85 and 3.5 still say open, and the tiebreaker chose the lower-scored side. |
| X-047 How tasklist and workflow reach the panel | CL-10 | Variant 2 | 60% | Both keep `/sc:reflect` as today's path (0 `t2-engine` hits in workflow/tasklist skills); V2 adjudicated, V1's protocol reference (V1:2536) remains a useful doc artifact. |
| X-060 Status of "is workflow/tasklist review reflect pre or a direct panel c | CL-10 | Variant 2 | 62% | Same as X-005. |
| S-018 E2 split | CL-11 | Variant 2 | 85% | Collaboration subsection exists only in V2 (V2:345-412). |
| C-002 Scope of the underlying research | CL-11 | Variant 2 | 80% | 24 vs 13 research files; V2 covers collaboration, run record, eval governance, defect register (V2:126, V2:1305-1383). |
| C-028 E2 collaboration and process-redesign work | CL-11 | Variant 2 | 85% | V2-only collaboration evidence (V2:345-412). |
| C-072 Collaboration and process redesign | CL-11 | Variant 2 | 85% | Collaboration and process-redesign axes only in V2. |
| C-091 Collaboration designs and process redesign (E2 brainstorms) | CL-11 | Variant 2 | 85% | Same as C-072. |
| S-023 E3 split in matrix | CL-12 | Variant 2 | 70% | V2 read the scripts and matched 17 of 17 files by sha256 (V2 2.4 V2:432-459; axis 10 V2:3645, "port contracts, not scripts"); V1 read descriptions only (V1 2.3 V1:263-269). Caveat X-034. |
| C-030 E3 installed variants | CL-12 | Variant 2 | 60% | V2 read the bodies; X-034 caveat. |
| C-031 Phase-5 experiment numbers | CL-12 | Variant 2 | 70% | V2 read the scripts and matched 17 of 17 files by sha256 (V2 2.4 V2:432-459; axis 10 V2:3645, "port contracts, not scripts"); V1 read descriptions only (V1 2.3 V1:263-269). Caveat X-034. |
| C-071 Installed-only E3 variants | CL-12 | Variant 2 | 70% | Keep/archive/fold axis only in V2 (V2:2862-2934). |
| C-094 Experiment variants (E3-installed) | CL-12 | Variant 2 | 70% | V2 read the scripts and matched 17 of 17 files by sha256 (V2 2.4 V2:432-459; axis 10 V2:3645, "port contracts, not scripts"); V1 read descriptions only (V1 2.3 V1:263-269). Caveat X-034. |
| X-034 Verification status of diffgate, ponytail/fix-audit, armb | CL-12 | Variant 2 | 55% | V2 2.4 gives file sizes and line-level defects in the script bodies (`diffgate.py:23-25,729-796`, `fix_audit.py:877,1028`; V2:432-448); V1 says "bodies not read, description only" (V1:267-269). V2 has the information; its OQ-01 "a |
| A-019 The installed `~/.claude/` variants on this machine represent what con | CL-12 | Variant 2 | 70% | V2 read the scripts and matched 17 of 17 files by sha256 (V2 2.4 V2:432-459; axis 10 V2:3645, "port contracts, not scripts"); V1 read descriptions only (V1 2.3 V1:263-269). Caveat X-034. |
| S-020 Eval harness, governance, repo constraints | CL-13 | Variant 2 | 80% | Eval harness, governance and repo constraints only in V2 (V2:730-826). |
| C-013 Evaluation and ground truth | CL-13 | Variant 2 | 72% | 12 evaluation rows incl. G-123, G-124 (V2:1358-1365) vs V1 MS-17 (V1:644). |
| C-026 E2 headline numbers | CL-13 | Variant 2 | 75% | Re-derived from files, `fullpkg()` bug found (V2:294-320). |
| C-027 E2 model-by-role observations | CL-13 | Variant 2 | 75% | E1/E2 one evidence family (V2 2.2 V2:278, V2:322) and three-tier acceptance (V2 axis 9 V2:3644); V2 re-derived E2 numbers (C-026). V1 is right on X-021. |
| C-029 E1 and E2 provenance entanglement | CL-13 | Variant 2 | 82% | sha256 `044809e3...` and `snap.py:4` (V2:278, V2:322). |
| C-043 Judge blinding facts | CL-13 | Variant 1 | 62% | Round 1 exception to the cluster verdict (advocate's own exception list) |
| C-070 Evaluation and rollout | CL-13 | Variant 2 | 75% | E1/E2 one evidence family (V2 2.2 V2:278, V2:322) and three-tier acceptance (V2 axis 9 V2:3644); V2 re-derived E2 numbers (C-026). V1 is right on X-021. |
| C-092 Evaluation / acceptance | CL-13 | Variant 2 | 68% | Three-tier acceptance and independence (V2 axis 9 V2:3644). |
| X-021 What 1,398 counts in the E2 chain replay | CL-13 | Variant 1 | 88% | `audit2.py` increments `rows_total` before the `< 3` filter (orchestrator, `git show 6c09843`). |
| X-025 How many Qwen3.8-max runs timed out | CL-13 | Variant 2 | 85% | E2 `combos/SPEC.md` line 3: "timed out ... on 3 of 4 runs". |
| X-026 Verdict flips and what else audit D lists | CL-13 | Variant 2 | 75% | The "merge that lost two blocking findings" is the third flip itself (n5-sonnet-ember F1+F2); V1's final 3 stands but its description double-counts. |
| S-045 Decisions that are stand-alone in only one report | CL-14 | Both (merge) | 72% | Same as CL-14: each report has stand-alone decisions the other lacks. |
| C-073 Panel size and Tier 2 escalation cost | CL-14 | Variant 1 | 75% | Not actually disputed: the V2 advocate's exception list gives "C-073 and C-093 (CL-14): V1, 70%" (r1-advocate-V2.md line 276); the convergence table recorded the cluster verdict instead. V1 C-14 recount and owner-gated D-1 (V1:210 |
| C-093 Panel size versus cost | CL-14 | Variant 1 | 75% | Same as C-073 (V1:2832, V1:4372-4375). |
| C-003 Gap-table size and Critical definition | CL-15 | Both (merge) | 65% | Both counts verified by awk (145: 15/66/64; 148: 24/93/31); different rubrics. |
| C-009 Rule C8 and which gaps it touches | CL-15 | Both (merge) | 65% | V2's C8 table covers 10 capabilities and states its premise test (V2:1409-1422); V1 adds MS-14, ENS-4, ENS-5 as C8 rows V2 lacks (V1:583, V1:767). Neither covers the other. |
| X-011 Severity: over-length fields drop whole findings (49 blocking lost) | CL-15 | Variant 1 | 70% | 3 merged verdicts flipped FAIL to PASS is a fail-open verdict, Critical by V2's own rubric (V2:1121); V2 G-06 says Important (V2:1241), V1 D1 Critical (V1:589). |
| X-012 Severity: ledger clears a row by silence | CL-15 | Variant 2 | 68% | Clearing by silence reproduced a false PASS (V2 G-12 V2:1247); V1 D2 Important (V1:590) is inconsistent with its own D3 Critical. |
| X-013 Severity: `lint_cmd` / `estimate_cmd` registered but absent | CL-15 | Variant 1 | 58% | `lint_cmd`/`estimate_cmd` belong to unmerged experiment branches (V1 D13 V1:601); V2 asserts "named as shipped" (V2:1372) without a driving spec cite. |
| X-014 Severity and verification status: telemetry store with no producer | CL-15 | Variant 1 | 55% | A manual CLI caller exists (`telemetry_cmd.py:67`); V1 rates Important and carries the C8 premise as UNVERIFIED (V1 SC-12 V1:537), which is the accurate status. |
| X-015 Severity and C8 status: reflect panel kernel not reachable (shadow onl | CL-15 | Variant 1 | 58% | `SKILL.md:87` stages the panel "until Stage 3", so the C8 premise "spec names it as shipped or enabled" is not met for the skill path (V1 MS-08 V1:635); V2 counts #519 as the naming (V2 G-21 V2:1256), which is arguable. |
| X-016 Severity: Stage 2 exit FAIL and orchestrator-written steps | CL-15 | Variant 2 | 55% | The Stage 2 exit is the rollout gate and the target cannot hold until it passes (V2 G-47 V2:1282); shadow changes no verdict, so Important (V1 MS-12 V1:639) is defensible but weaker. |
| X-017 Severity: #346 `merge`/`ledger`/`panel` CLI has no production caller | CL-15 | Variant 2 | 55% | V1 D14 itself names a live caller, the prose at `document_review_loop_prompts.md:70` read by `/sc:spec-panel --mode critique` (V1:602), so the CLI as a whole is not unwired; Important (V2 G-96, V2:1331) fits. V1's sub-finding stan |
| X-018 Severity: no dispatch contract / resolver policy | CL-15 | Variant 1 | 60% | V2's adjudicated design keeps "the core launches nothing" (V2:1139), so G-24 Critical (V2:1259) rates a gap the governing design does not close. |
| X-019 Severity: evaluation and driving-document input | CL-15 | Both (merge) | 58% | Split per row: G-123 (no acceptance-evidence definition, V2:1358) meets V2's "target cannot hold" rule (V2:1121) because no use case can be accepted without it, and E1/E2 being one derivation set removes the fallback, so Critical  |
| A-008 Unwired-but-named capability is Critical even when the skill text stag | CL-15 | Both (merge) | 60% | Both advocates answered QUALIFY in the same direction (r1-advocate-V1.md line 270; r1-advocate-V2.md line 288): rate the code fact as a defect, set plan priority by the cited driving text and any on-record staging (V1 premise chec |
| S-015 E2 baseline pin | CL-16 | Variant 2 | 72% | Same as X-001. |
| S-016 Evidence-source basis | CL-16 | Variant 2 | 65% | Not using slices as evidence is cleaner (V2:108); V1 relies on S00-S05 (V1:108-123). |
| S-041 Evidence baseline pinned | CL-16 | Variant 2 | 72% | V2 reads the later E2 tip, not slices (V2 Baseline V2:108); V1 pinned older (V1:93). Code at both HEADs identical (X-063). |
| C-001 E2 evidence baseline (which commit) | CL-16 | Variant 2 | 72% | Same as X-001. |
| X-001 Which E2 commit is the evidence base | CL-16 | Variant 2 | 72% | Both pins exist and are 4 commits apart (orchestrator); V2's `6c09843` holds the collaboration work V1's `4a22d74` lacks (V2:108, V1:93). |
| X-062 E2 study pin commit | CL-16 | Variant 2 | 72% | Same as X-001. |
| X-063 Baseline HEAD of the code read | CL-16 | Both (merge) | 90% | `git diff --stat 792cf8c52 50d4d2b9d -- src tests scripts` is empty (orchestrator). |
| A-002 Code facts and line numbers cited at HEAD 792cf8c52 (V1:489, V1:99) or | CL-16 | Variant 2 | 72% | V2 reads the later E2 tip, not slices (V2 Baseline V2:108); V1 pinned older (V1:93). Code at both HEADs identical (X-063). |
| A-024 Research-file counts taken from hand-offs or scope slices carry over u | CL-16 | Variant 2 | 72% | V2 reads the later E2 tip, not slices (V2 Baseline V2:108); V1 pinned older (V1:93). Code at both HEADs identical (X-063). |
| A-036 Code line citations from older HEADs (V1 `792cf8c52`, V2 `50d4d2b9d`)  | CL-16 | Variant 2 | 72% | V2 reads the later E2 tip, not slices (V2 Baseline V2:108); V1 pinned older (V1:93). Code at both HEADs identical (X-063). |
| A-037 The E2 pinned commit is the right baseline (V1 `4a22d74` 2026-11-13; V | CL-16 | Variant 2 | 72% | V2 reads the later E2 tip, not slices (V2 Baseline V2:108); V1 pinned older (V1:93). Code at both HEADs identical (X-063). |
| A-055 E2 harness files are not tracked at HEAD and are read through `git sho | CL-16 | Variant 2 | 72% | V2 reads the later E2 tip, not slices (V2 Baseline V2:108); V1 pinned older (V1:93). Code at both HEADs identical (X-063). |
| S-032 Organising unit of Section 6 | CL-17 | Variant 2 | 60% | Decision axes are the right organising unit for a plan; V1's conflict blocks (V1:1191-2515) hold detail that must survive. |
| S-033 Option labels reused with different meaning | CL-17 | Variant 2 | 65% | V2's UNDECIDABLE labels and 189-row log (V2 6.12 V2:3130-3566) are the truer method; V1 over-labels "decided" (V1:2830). V1's 6.E implementer detail (V1:2624-2807) still must survive. |
| S-034 Where the recommendation sits | CL-17 | Variant 2 | 65% | V2's UNDECIDABLE labels and 189-row log (V2 6.12 V2:3130-3566) are the truer method; V1 over-labels "decided" (V1:2830). V1's 6.E implementer detail (V1:2624-2807) still must survive. |
| S-035 Option scoring layout | CL-17 | Variant 2 | 65% | V2's UNDECIDABLE labels and 189-row log (V2 6.12 V2:3130-3566) are the truer method; V1 over-labels "decided" (V1:2830). V1's 6.E implementer detail (V1:2624-2807) still must survive. |
| S-036 Status taxonomy and classification result | CL-17 | Variant 2 | 70% | UNDECIDABLE is the truer status (X-052). |
| S-037 Number and depth of adversarial debates | CL-17 | Variant 2 | 68% | 15 debates cover more slots; V1's 4 debates carry deeper 6.E detail (V1:2624-2807). |
| S-038 Conflict log form | CL-17 | Variant 2 | 68% | 189-row log with evidence status (V2:3194-3425). |
| S-039 Defect register inside Section 6 | CL-17 | Variant 1 | 62% | Round 1 exception to the cluster verdict (advocate's own exception list) |
| S-043 Corrected-claims, open-question and coverage tables inside Section 6 | CL-17 | Variant 2 | 65% | V2's UNDECIDABLE labels and 189-row log (V2 6.12 V2:3130-3566) are the truer method; V1 over-labels "decided" (V1:2830). V1's 6.E implementer detail (V1:2624-2807) still must survive. |
| S-044 Post-debate re-rating of options | CL-17 | Unresolved split | 50% | V1 advocate: Variant 1; V2 advocate: Variant 2. V2 marks every axis UNDECIDABLE before debate and records 15 adjudicated outcomes with conditions (V2:3004-3018, V2:3509-3525) and a 189-row conflict log (V2 6.12, V2:3130-3566); V1  |
| S-055 Meaning of "C-nn" ids | CL-17 | Variant 2 | 65% | V2's UNDECIDABLE labels and 189-row log (V2 6.12 V2:3130-3566) are the truer method; V1 over-labels "decided" (V1:2830). V1's 6.E implementer detail (V1:2624-2807) still must survive. |
| C-074 Evidence-number reconciliation | CL-17 | Variant 2 | 65% | V2's UNDECIDABLE labels and 189-row log (V2 6.12 V2:3130-3566) are the truer method; V1 over-labels "decided" (V1:2830). V1's 6.E implementer detail (V1:2624-2807) still must survive. |
| C-075 Open invariants after debates | CL-17 | Variant 2 | 65% | V2's UNDECIDABLE labels and 189-row log (V2 6.12 V2:3130-3566) are the truer method; V1 over-labels "decided" (V1:2830). V1's 6.E implementer detail (V1:2624-2807) still must survive. |
| C-097 Status wording for debated conflicts | CL-17 | Variant 2 | 65% | V2's UNDECIDABLE labels and 189-row log (V2 6.12 V2:3130-3566) are the truer method; V1 over-labels "decided" (V1:2830). V1's 6.E implementer detail (V1:2624-2807) still must survive. |
| X-052 Whether the core-shape question can be decided by evidence | CL-17 | Variant 2 | 75% | No run compares core shapes; V1's "DECIDED-BY-EVIDENCE" (V1:2830) overclaims. |
| A-052 All debates ended `partial` with unaddressed HIGH invariants, yet thei | CL-17 | Variant 2 | 65% | V2's UNDECIDABLE labels and 189-row log (V2 6.12 V2:3130-3566) are the truer method; V1 over-labels "decided" (V1:2830). V1's 6.E implementer detail (V1:2624-2807) still must survive. |
| X-020 Does `ledger.merge_round` raise `KeyError` on a v2 citation-only findi | CL-18 | Variant 1 | 90% | `findings.py:104` rejects, `:188-192` skips, `ledger.py:135-136` annotates only accepted findings (re-read here). |
| X-022 Count of rf-* agent spawn sites | CL-18 | Variant 2 | 78% | `grep -rn 'subagent_type: *"\?rf-'` = 52 lines (re-run here); V1's 43 is unreproducible. |
| X-023 Key count of the engine-A reflect contract | CL-18 | Both (merge) | 60% | Diff analyst: "VERIFIED-BOTH (reconcile)": 32 literal keys (`ensemble.py:787-832`) plus conditional `t2_fallback` (`:833-834`) = 33. V1's "33 keys, 11 of them in neither list" (V1:640) is internally consistent because `t2_fallback |
| X-024 Keys of the swarm ensemble contract outside the frozen 1.8.0 lists | CL-18 | Both (merge) | 58% | Same fact as X-023. The analyst tagged V2 verified and said V1 "does not say which" basis; under the `t2_fallback` basis V1's 11 matches V1's own 33. V1's fault is an unstated unit (conceded, point 9), not a wrong number. |
| X-027 Definition behind `findings_block_compliance_rate` 0.704 | CL-18 | Variant 1 | 72% | Commit `9874d63fb` changed the definition to first-parse; pre-commit values were not first-parse, so "mixed definitions" (V1:162) is accurate. |
| X-028 `cluster_agreement` in the shadow runs | CL-18 | Variant 1 | 68% | shadow09 holds 0.9328 but its contract does not parse, so it never reaches the exit script; V2's "all 1.000" omits it (V2:216). |
| X-029 rf-qa family call-site census | CL-18 | Variant 2 | 78% | 44 structured lines in 8 `SKILL.md` files reproduce; V1's 43 does not. |
| X-030 Calibrator rubric dimension mismatch | CL-18 | Variant 1 | 88% | `confidence-calibrator.md:3` "6-dimension" vs `sc-reflect-protocol/SKILL.md:1262,1835` "5-dimension" (orchestrator). |
| X-031 What `findings.same_defect` links | CL-18 | Variant 2 | 80% | `findings.py:367-379` has the `(not ra and not rb)` branch V1 omits. |
| X-032 Whether `ensemble.py` is E1 work | CL-18 | Variant 1 | 68% | `git log` of `ensemble.py` (#203-#329) predates E1; #519 touched only `panel_lint.py` in `cli/reflect`. |
| X-033 Count of severity label sets in the repo | CL-18 | Variant 2 | 55% | V2 lists seven rows incl. tasklist skill vs CLI and `/sc:implement` (V2:687-695); V1's five omits them. Definitional. |
| X-048 Is the 5-versus-6-dimension calibrator mismatch a verified fact | CL-18 | Variant 1 | 88% | Same fact as X-030. |
| X-049 Is a v2 citation-only finding a crash of the v1 ledger path | CL-18 | Variant 1 | 90% | Same fact as X-020; V2's own L3511 agrees with V1. |
| X-050 Identity source of shadow and combo runs | CL-18 | Both (merge) | 75% | V1 "no code writes `observed`" is right; V2's "1 of 15 combo contracts" count is right. |
| X-053 What a v2 citation-only finding does on the shipped merge path | CL-18 | Variant 1 | 90% | Same code as X-020; V2:3882 and V2:4508 must be corrected. |
| X-061 rf-qa spawn-site census | CL-18 | Variant 2 | 78% | Same as X-022. |
| A-057 A v2 citation-only finding reaches the shipped merge path and crashes  | CL-18 | Variant 1 | 65% | V1 wins 10 point rows (X-020, X-021, X-027, X-028, X-030, X-032, X-048, X-049, X-053, A-057), V2 wins 6 (X-022, X-025, X-026, X-029, X-031, X-061), 3 reconcile (X-023, X-024, X-050). The V1 wins include the one fact V2 uses as dec |
| S-007 Adjudication-override layer | CL-19 | Variant 2 | 72% | An override layer is needed once Section 7 adjudications differ from Sections 3-4 (V2:1125-1144). |
| S-013 Where precedence between Section 4 and the recommendation is recorded | CL-19 | Variant 2 | 72% | Same as S-007. |
| S-046 Section 7 shape and size | CL-19 | Variant 2 | 60% | V2's Section 7 carries winners, conditions and 244 invariants (V2:3567-4233); V1's 20-row adopted-resolution table (V1:2837-2858) and 4-row risk table (V1:2862-2867) are compact inputs. |
| S-054 Debate-invariant presentation | CL-19 | Variant 2 | 65% | V2's precedence table (V2:1125-1144), invariants I-1..I-9 and 29 constraints (C-095) are needed in a merged document that has several sections; V1 needed no override only because it ran fewer debates. |
| C-004 Status of the Section 3 target | CL-19 | Variant 2 | 68% | Two-layer target with stated precedence is honest about overturned cells (V2:1125-1144). |
| C-095 Constraints and invariants carried | CL-19 | Variant 2 | 70% | 29 binding constraints incl. layout traps (V2:4430-4458) vs 13 rows (V1:3058-3070). |
| S-047 Section 8 purpose and contents | CL-20 | Both (merge) | 75% | Same as CL-20. |
| S-048 Where the value inventory lives | CL-20 | Both (merge) | 62% | V2's 5,950-row inventory reconciles but lives in a 2 MB appendix file (V2:4280-4296); V1's 698 rows are inline (V1:3121-3820). Carry V2's file as a named input and fold V1's rows that V2 lacks. |
| S-049 Inventory row schema and destination vocabulary | CL-20 | Both (merge) | 60% | V2's destinations add EVAL, HARNESS, KNOWLEDGE (V2:4250-4259); V1's 23 component destinations and Effort column are finer (V1:3117-3121). |
| S-056 No-regression gate list form | CL-20 | Both (merge) | 70% | V1's gates carry commands, collected counts and per-test replacement assertions (V1:4033-4055); V2's G17-G27 are gates imposed by adjudicated winners (measurements, kill lines, replays; V2:4482-4492) that the plan also needs once  |
| C-096 Branching / PR sequencing content | CL-20 | Variant 2 | 68% | Round 1 exception to the cluster verdict (advocate's own exception list) |
| A-056 The inventory destinations agree with the architecture recommended in  | CL-20 | Both (merge) | 60% | Only V1 8.4's layout table A-E (V1:4063-4069) is dropped. V1:4059 (constraint), V1:4061 (facts), V1 8.5 rows that are no-regression risks and V1 8.6 gate operations are carried (point 11 above). |
| A-059 The counts of "rows", "gates", "constraints" and "open questions" in e | CL-20 | Both (merge) | 60% | Only V1 8.4's layout table A-E (V1:4063-4069) is dropped. V1:4059 (constraint), V1:4061 (facts), V1 8.5 rows that are no-regression risks and V1 8.6 gate operations are carried (point 11 above). |
| S-027 Sec 5 source set | CL-23 | Both (merge) | 78% | Disjoint web source sets, both needed (CL-23). |
| S-028 Sec 5 entry format | CL-23 | Both (merge) | 60% | X-036: the arXiv 2606.19544 figure is from a withdrawn paper; V2's takeaway at V2:2044 must be dropped or marked "withdrawn source". |
| S-029 Sec 5 options lists | CL-23 | Both (merge) | 60% | X-036: the arXiv 2606.19544 figure is from a withdrawn paper; V2's takeaway at V2:2044 must be dropped or marked "withdrawn source". |
| S-030 Sec 5 summary | CL-23 | Both (merge) | 60% | X-036: the arXiv 2606.19544 figure is from a withdrawn paper; V2's takeaway at V2:2044 must be dropped or marked "withdrawn source". |
| S-031 Within-subsection conflicts | CL-23 | Both (merge) | 60% | X-036: the arXiv 2606.19544 figure is from a withdrawn paper; V2's takeaway at V2:2044 must be dropped or marked "withdrawn source". |
| C-044 Sec 5 aggregation evidence | CL-23 | Both (merge) | 72% | Different evidence sets (production systems and Zenodo corpus in V1:806-821; benchmarks and aggregation in V2:1620-1684). |
| C-045 Sec 5 severity | CL-23 | Variant 1 | 72% | Full severity research (V1:853-939) vs a brief section (V2:1958-2034). |
| C-046 Sec 5 judge and calibration | CL-23 | Variant 1 | 70% | Calibration methods only in V1 (V1:941-1016). |
| C-047 Sec 5 fingerprinting and clustering | CL-23 | Variant 1 | 68% | Clustering-algorithm sources only in V1 (V1:1018-1079). |
| C-048 Sec 5 runtime and git topics | CL-23 | Variant 2 | 75% | Hooks/headless and git-ref topics only in V2 (V2:1698-1911). |
| C-049 Sec 5 handling of codebase context | CL-23 | Both (merge) | 60% | X-036: the arXiv 2606.19544 figure is from a withdrawn paper; V2's takeaway at V2:2044 must be dropped or marked "withdrawn source". |
| X-035 SARIF `kind` values | CL-23 | Variant 2 | 70% | SARIF 2.1.0 §3.27.9 enumerates six `kind` values including `review`; from the published schema as I know it, not fetched in this task. |
| X-036 Use of arXiv 2606.19544 verbosity finding | CL-23 | Variant 1 | 68% | New check: `https://arxiv.org/abs/2606.19544` (fetched 2026-11-15) shows the abstract's "verbosity bias is small (<0.011) ... under a single pairwise rubric", matching V2:1647, but the page states "This paper has been withdrawn by |
| X-037 Evidence status of Codex P0-P3 behaviour | CL-23 | Variant 2 | 58% | V2 cites official OpenAI docs (V2:1980); V1 found only a blog (V1:878). Not fetched. |
| S-050 Section 9 organisation | CL-24 | Variant 2 | 60% | V2 consolidates carry-over with GQ sources (V2 9 V2:4700) and flags the unread later E2 commit (Q-39); V1 adds owner items O-1..O-6 and issue ids #525-#530 (V1 V1:4136-4141). Ids must be namespaced in the merge (A-006, A-058). |
| S-051 Section 9 column set | CL-24 | Variant 2 | 60% | V2 consolidates carry-over with GQ sources (V2 9 V2:4700) and flags the unread later E2 commit (Q-39); V1 adds owner items O-1..O-6 and issue ids #525-#530 (V1 V1:4136-4141). Ids must be namespaced in the merge (A-006, A-058). |
| S-052 Section 10 evidence trail | CL-24 | Variant 2 | 60% | V2 consolidates carry-over with GQ sources (V2 9 V2:4700) and flags the unread later E2 commit (Q-39); V1 adds owner items O-1..O-6 and issue ids #525-#530 (V1 V1:4136-4141). Ids must be namespaced in the merge (A-006, A-058). |
| S-053 Appendices | CL-24 | Variant 2 | 60% | V2 consolidates carry-over with GQ sources (V2 9 V2:4700) and flags the unread later E2 commit (Q-39); V1 adds owner items O-1..O-6 and issue ids #525-#530 (V1 V1:4136-4141). Ids must be namespaced in the merge (A-006, A-058). |
| C-016 Open decisions and unverified claims carried from Section 4 | CL-24 | Variant 2 | 68% | Consolidated D-1..D-14 and U-1..U-18 (V2:1494-1532). |
| A-006 Gap ids G-nn, D-nn and C-nn are different namespaces in each report (V | CL-24 | Variant 2 | 60% | V2 consolidates carry-over with GQ sources (V2 9 V2:4700) and flags the unread later E2 commit (Q-39); V1 adds owner items O-1..O-6 and issue ids #525-#530 (V1 V1:4136-4141). Ids must be namespaced in the merge (A-006, A-058). |
| A-012 The two gap logs (V1 "94 open rows, none Critical, 30 Important", V2 " | CL-24 | Variant 2 | 60% | V2 consolidates carry-over with GQ sources (V2 9 V2:4700) and flags the unread later E2 commit (Q-39); V1 adds owner items O-1..O-6 and issue ids #525-#530 (V1 V1:4136-4141). Ids must be namespaced in the merge (A-006, A-058). |
| A-058 Cross-report ids (C-nn, Q-nn, A-n, G-nn) can be compared one to one wh | CL-24 | Variant 2 | 60% | V2 consolidates carry-over with GQ sources (V2 9 V2:4700) and flags the unread later E2 commit (Q-39); V1 adds owner items O-1..O-6 and issue ids #525-#530 (V1 V1:4136-4141). Ids must be namespaced in the merge (A-006, A-058). |
| S-001 Header metadata and scope note | CL-21 | Both (merge) | 60% | V1's track tags and detailed SC pass rules (V1 4 V1:761, V1 3 V1:526-548) plus V2's C8 table, 33 SCs and 4.6 carry-over (V2 4.2 V2:1407-1422, 3.3 V2:1171-1209, 4.6 V2:1488-1536). |
| S-002 Table of Contents shape | CL-21 | Both (merge) | 60% | V1's track tags and detailed SC pass rules (V1 4 V1:761, V1 3 V1:526-548) plus V2's C8 table, 33 SCs and 4.6 carry-over (V2 4.2 V2:1407-1422, 3.3 V2:1171-1209, 4.6 V2:1488-1536). |
| S-003 Preamble before Section 1 | CL-21 | Both (merge) | 60% | V1's track tags and detailed SC pass rules (V1 4 V1:761, V1 3 V1:526-548) plus V2's C8 table, 33 SCs and 4.6 carry-over (V2 4.2 V2:1407-1422, 3.3 V2:1171-1209, 4.6 V2:1488-1536). |
| S-004 Section 3 internal organization | CL-21 | Variant 2 | 60% | V2's numbered 3.1-3.5 with the precedence table first (V2:1114-1227) is the better skeleton for a merged document that adopts adjudications; V1's consumer table C-A..C-E and core diagram (V1:496-520) are carried into it (the V2 ad |
| S-005 External research inside Section 3 | CL-21 | Both (merge) | 60% | V1's track tags and detailed SC pass rules (V1 4 V1:761, V1 3 V1:526-548) plus V2's C8 table, 33 SCs and 4.6 carry-over (V2 4.2 V2:1407-1422, 3.3 V2:1171-1209, 4.6 V2:1488-1536). |
| S-006 Architecture diagram in Section 3 | CL-21 | Both (merge) | 60% | V1's track tags and detailed SC pass rules (V1 4 V1:761, V1 3 V1:526-548) plus V2's C8 table, 33 SCs and 4.6 carry-over (V2 4.2 V2:1407-1422, 3.3 V2:1171-1209, 4.6 V2:1488-1536). |
| S-008 Section 1 length and format | CL-21 | Both (merge) | 60% | V1's track tags and detailed SC pass rules (V1 4 V1:761, V1 3 V1:526-548) plus V2's C8 table, 33 SCs and 4.6 carry-over (V2 4.2 V2:1407-1422, 3.3 V2:1171-1209, 4.6 V2:1488-1536). |
| S-009 Section 10 ToC items | CL-21 | Both (merge) | 60% | V1's track tags and detailed SC pass rules (V1 4 V1:761, V1 3 V1:526-548) plus V2's C8 table, 33 SCs and 4.6 carry-over (V2 4.2 V2:1407-1422, 3.3 V2:1171-1209, 4.6 V2:1488-1536). |
| S-010 Section 4 subsections | CL-21 | Both (merge) | 60% | V1's track tags and detailed SC pass rules (V1 4 V1:761, V1 3 V1:526-548) plus V2's C8 table, 33 SCs and 4.6 carry-over (V2 4.2 V2:1407-1422, 3.3 V2:1171-1209, 4.6 V2:1488-1536). |
| S-011 Gap table row-id scheme and grouping | CL-21 | Both (merge) | 58% | V2's flat topical G-01..G-148 (V2:1236-1383) is easier to search; V1's id families (D, BL, MS, ENS, DOC; V1:589-733) carry the consumer each row blocks. The merge re-keys both. |
| S-012 Migration-track tagging inside Section 4 | CL-21 | Variant 1 | 70% | Track tags and the by-track table (V1:761, V1:772-780) tell a plan where each gap lands; V2 has none. |
| S-014 Contradiction table column order and population | CL-21 | Both (merge) | 60% | V1's track tags and detailed SC pass rules (V1 4 V1:761, V1 3 V1:526-548) plus V2's C8 table, 33 SCs and 4.6 carry-over (V2 4.2 V2:1407-1422, 3.3 V2:1171-1209, 4.6 V2:1488-1536). |
| S-017 Sec 2 size and subsection plan | CL-22 | Variant 2 | 62% | V2 2.1-2.9 covers dispatch, eval, repo rules V1 lacks. |
| S-019 Dispatch/tier/identity | CL-22 | Variant 2 | 70% | V2's 9 subsections incl. dispatch, eval governance, repo constraints and executed probes (V2 2.5-2.8 V2:486-826); V1 compact (V1:106-480) but carries D1-D16 status with a v2-shares column (V1 2.4 V1:358-377). |
| S-022 Overlap matrix design | CL-22 | Variant 2 | 60% | V2's classified matrix with ABSENT cells, CF/SS/PS/DU and RC/CC tables (V2:830-1110) is the base; V1's "Same data contract? / Same code? / Divergent choices" columns (V1:436-461) are carried. |
| S-024 Where contradictions are recorded | CL-22 | Variant 2 | 70% | V2's 9 subsections incl. dispatch, eval governance, repo constraints and executed probes (V2 2.5-2.8 V2:486-826); V1 compact (V1:106-480) but carries D1-D16 status with a v2-shares column (V1 2.4 V1:358-377). |
| S-025 Unverified items | CL-22 | Variant 2 | 70% | V2's 9 subsections incl. dispatch, eval governance, repo constraints and executed probes (V2 2.5-2.8 V2:486-826); V1 compact (V1:106-480) but carries D1-D16 status with a v2-shares column (V1 2.4 V1:358-377). |
| S-026 Diagrams | CL-22 | Variant 2 | 70% | V2's 9 subsections incl. dispatch, eval governance, repo constraints and executed probes (V2 2.5-2.8 V2:486-826); V1 compact (V1:106-480) but carries D1-D16 status with a v2-shares column (V1 2.4 V1:358-377). |
| S-042 Citation keys | CL-25 | Both (merge) | 58% | V1's 651-test figure reproduces (A-038, re-run here); citation keys (S-042) need one scheme in the merge. |
| C-007 Success criteria | CL-21 | Both (merge) | 70% | V2 SC-21..SC-33 (V2:1197-1209) and V1 SC-18..SC-22 plus the SC-6/SC-10/SC-14 pass rules (V1:531-547) are complementary. |
| C-008 Constraints list | CL-21 | Both (merge) | 60% | V1's track tags and detailed SC pass rules (V1 4 V1:761, V1 3 V1:526-548) plus V2's C8 table, 33 SCs and 4.6 carry-over (V2 4.2 V2:1407-1422, 3.3 V2:1171-1209, 4.6 V2:1488-1536). |
| C-015 Stale-documentation treatment | CL-21 | Both (merge) | 60% | V1's track tags and detailed SC pass rules (V1 4 V1:761, V1 3 V1:526-548) plus V2's C8 table, 33 SCs and 4.6 carry-over (V2 4.2 V2:1407-1422, 3.3 V2:1171-1209, 4.6 V2:1488-1536). |
| C-019 Section 1 evidence emphasis | CL-21 | Both (merge) | 60% | V1's track tags and detailed SC pass rules (V1 4 V1:761, V1 3 V1:526-548) plus V2's C8 table, 33 SCs and 4.6 carry-over (V2 4.2 V2:1407-1422, 3.3 V2:1171-1209, 4.6 V2:1488-1536). |
| C-032 Defect enumeration against current code | CL-22 | Both (merge) | 65% | V2's executed probes and 171-row register (V2:545-580); V1's D1-D16 status with "Reflect v2 shares it?" (V1:358-377). |
| C-033 Test surface | CL-22 | Variant 1 | 65% | Round 1 exception to the cluster verdict (advocate's own exception list) |
| C-035 Brief and input delivery | CL-22 | Variant 2 | 70% | V2's 9 subsections incl. dispatch, eval governance, repo constraints and executed probes (V2 2.5-2.8 V2:486-826); V1 compact (V1:106-480) but carries D1-D16 status with a v2-shares column (V1 2.4 V1:358-377). |
| C-036 Severity vocabularies | CL-22 | Variant 2 | 70% | V2's 9 subsections incl. dispatch, eval governance, repo constraints and executed probes (V2 2.5-2.8 V2:486-826); V1 compact (V1:106-480) but carries D1-D16 status with a v2-shares column (V1 2.4 V1:358-377). |
| C-039 Tier-2 prevalence | CL-22 | Variant 1 | 62% | Round 1 exception to the cluster verdict (advocate's own exception list) |
| C-042 Overlap-matrix interpretive stance | CL-22 | Variant 2 | 70% | V2's 9 subsections incl. dispatch, eval governance, repo constraints and executed probes (V2 2.5-2.8 V2:486-826); V1 compact (V1:106-480) but carries D1-D16 status with a v2-shares column (V1 2.4 V1:358-377). |
| X-008 Per-slot `role`/`lens`/`agent` in panel templates | CL-21 | Variant 1 | 65% | V2's own Section 1 says PR review needs "an optional per-slot lens" (V2:134); D11 says the per-slot key "stays true for a later panel-engine step" (V2:4510); the C-11 withdrawal covers only the first rf-qa change (V2:1141) and lef |
| A-018 Tier lists in `review-tiers.default.json` describe what the gateway ca | CL-22 | Variant 2 | 70% | V2's 9 subsections incl. dispatch, eval governance, repo constraints and executed probes (V2 2.5-2.8 V2:486-826); V1 compact (V1:106-480) but carries D1-D16 status with a v2-shares column (V1 2.4 V1:358-377). |
| A-027 The skill panel (engine B) will be the Tier-2 path the shared core ser | CL-23 | Both (merge) | 60% | X-036: the arXiv 2606.19544 figure is from a withdrawn paper; V2's takeaway at V2:2044 must be dropped or marked "withdrawn source". |
| A-038 `tests/review` size claim "651 tests" counts collected tests | CL-25 | Both (merge) | 58% | V1's 651-test figure reproduces (A-038, re-run here); citation keys (S-042) need one scheme in the merge. |
| A-041 Section 6 numbers about E1 shadow runs (13 of 20, EV-1 8 of 13, 6 of 9 | CL-25 | Both (merge) | 58% | V1's 651-test figure reproduces (A-038, re-run here); citation keys (S-042) need one scheme in the merge. |

## Convergence Assessment

- Points resolved: 220 of 234 (agreed on a superior approach, including `Both (merge)`)
- Points where both advocates agree it is open (owner decision or no decisive evidence): 6
- Points where the advocates still differ after Round 2: 8
- Alignment (strict, resolved only): 94.0%  (alignment counting both-open as agreement: 96.6%; after Round 1 it was 82.5%)
- Threshold: 80%
- Taxonomy coverage gate: L1 (50 points), L2 (126), L3 (58) all addressed in both advocates' Round 1 and Round 2: PASS
- Invariant probe gate: 7 HIGH-severity UNADDRESSED invariants (INV-003, INV-006, INV-018, INV-024, INV-027, INV-028, INV-029): CONVERGENCE BLOCKED_BY_INVARIANTS (score meets threshold; gate does not)
- Status: BLOCKED_BY_INVARIANTS (agreement 94.0% >= 80%, taxonomy covered, 7 HIGH UNADDRESSED invariants). Depth `standard` has no Round 3, so the HIGH items are carried into the refactor plan and the merged document as explicit corrections or open owner decisions, and are listed in the return contract.
- Points won (strict tally): Variant 1 33, Variant 2 123, Both (merge) 64, Neither 0
- Unresolved points: C-005, C-076, X-051, C-053, X-040, X-056, C-065, X-058, C-060, X-041, X-057, C-025, C-014, S-044
