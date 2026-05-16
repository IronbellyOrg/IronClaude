# Adversarial Debate Transcript

## Metadata
- Depth: standard (2 rounds + invariant probe)
- Rounds completed: 2 (Round 3 skipped — convergence achieved after Round 2)
- Convergence achieved: 92% (35 of 38 diff points resolved)
- Convergence threshold: 85%
- Focus areas: completeness, traceability, decision-readiness
- Advocate count: 2
- Variant-1 advocate: defends Draft A (completeness/traceability)
- Variant-2 advocate: defends Draft B (decision-readiness)

---

## Round 1: Advocate Statements

### Variant 1 Advocate (Draft A — completeness/traceability)

**Position summary.** Draft A is the only artifact in this comparison that meets the stated purpose of the adversarial pipeline: weeding out hallucination through per-claim traceability. Every concrete claim cites a file:line or extract; inferred claims are tagged `[inference]`; the synthesizer self-check enumerates Known gaps. This is the structural property that protects downstream consumers from sycophantic agreement.

**Steelman of Draft B.** B's central insight is that an evidence-backbone without decision verdicts is a research report, not a release artifact. Engineering teams need ADOPT/DEFER/REJECT pills, effort labels (S/M/L), and explicit Blocking? flags on questions because those are the artifacts a sprint planner can convert directly into work. B's tighter risk register with Owner column is a real accountability improvement A lacks. B's compression — 207 lines vs 656 — is itself a quality property when reviewers have 15 minutes. The fact that B does not need `[inference]` tags is because B does not commit to claims that require them; B's recommendations are stated as conclusions, not as research findings.

**Strengths claimed (with evidence in Draft A).**
1. **47-row overlap matrix (O1-O47)** — exhaustive concept-to-state mapping including artifact items (O30 sentinel, O31 caller string) and sprint surfaces (O38-O43). B's 21-row C1-C21 matrix drops 26 rows of traceability. Evidence: §5 of A.
2. **Coverage-notes self-check** lists 5 Known gaps (TFEP six-conditions not enumerated verbatim, telemetry consumer of `--caller` not identified, `--shadow-gates` not directly verified against `cli/sprint/`). B has no equivalent. Evidence: coverage-notes section of A.
3. **`[inference]` discipline** applied 15+ times. B states the same conclusions without distinguishing cited from inferred. Evidence: NG-6 in §1.2; RK-08 in §7; §6.3 ranking.
4. **§9.5 v3.7 test baselines** (921 passed, 57 failed; TUI Waves 1-2 125/125; `test_process.py` 16/16). B does not cite these baseline numbers; SE-002..SE-006 land on unstable foundations without them. Evidence: §9.5.
5. **§9.7 Wave-4 checkpoint parser regression** (pre-fix matched `### Checkpoint:` but not `### T<PP>.<NN> -- Checkpoint:`). SE-003 sub-phase resume changes prompt construction — A surfaces this regression risk; B does not. Evidence: §9.7.
6. **TU-006 candidate** (materialize missing skill sub-files referenced at `SKILL.md:359-365`). B has no equivalent — leaves operationally broken references unaddressed. Evidence: §6.1 TU-006; RK-17.

**Weaknesses identified in Draft B.**
1. B has no explicit `[inference]` markers, yet it makes inferential claims (effort labels S/M/L are uncited; assignment of "Lead", "Tier owner", "Skill owner" in Owner column is uncited). The verdict pills (ADOPT/DEFER/REJECT) project certainty without distinguishing cited recommendations from synthesized ones.
2. B's 12-row risk register drops 8 rows that A has. Specifically: RK-13 (regex collision), RK-14 (subprocess blocking), RK-18 (auto-diagnostic robustness), RK-19 (prompt-template testing), RK-20 (live execution not validated at v3.7 cutover). These are not noise — RK-19 directly affects SE-003 (B14/B13).
3. B's open-question count of 10 is achieved by collapsing A's Q1+Q2 (sentinel + caller string) into a single Q3. This loses the distinction that `/sc:forensic` may pattern-match on `task-unified` (A's Q2 `[inference]` tag flags this; B's Q3 does not).
4. B has no §9.5 test-baselines section. The release validity gate cannot be measured against unspecified baselines.
5. B's "Non-goals" bullet list (5 items) is shorter than A's NG-1..NG-6 because B folds non-goals into REJECT candidate rows (B8, B9, B19, B20). This works for items B does reject, but A's NG-5 (preserve naming carry-overs without explicit telemetry-compat plan) is not a candidate at all and has no row in B's tables — it disappears.

**Concessions (genuine weaknesses in Draft A).**
1. A has no Owner column in §7 risks. B's Owner column is a real accountability device A should adopt.
2. A has no Effort labels. Value/tractability is two axes conflated; B's S/M/L is cleaner for sprint sizing.
3. A has no ADOPT/DEFER/REJECT verdicts. A's value/tractability ranking at §6.3 lets a reviewer infer the verdict but does not commit to one. This is a real decision-readiness gap.
4. A's 656 lines impose a cognitive cost B does not. For scan-time review, B is faster.
5. A does not commit on Q6 (`--skip-compliance` ∧ BLOCKED state interaction). B does. A's framing as open question is defensible for an early-stage artifact but a FINAL-REPORT should commit.

### Variant 2 Advocate (Draft B — decision-readiness)

**Position summary.** Draft B is the artifact a release lead can ship with. Verdict pills, effort labels, owner assignments, and explicit blocking flags convert analytical content into a sprint-ready decision queue. The same factual content exists in both drafts — what B does that A does not is force the reader to a commitment. Without commitment, FINAL-REPORTs become permanent research stubs that block downstream work.

**Steelman of Draft A.** A's traceability discipline is genuine and would be the right choice for a research artifact whose primary consumer is a future maintainer doing forensics. The `[inference]` tagging convention is rigorous; the 47-row overlap matrix is exhaustive; the §9.x prior-art constraint sections are the kind of detail that prevents v3.7-style regressions. If this report's primary purpose is hallucination prevention, A clearly wins on that axis. B does not dispute this. B's claim is narrower: when the consumer is a release planner deciding which candidates to schedule, A's prose-and-citation density is friction, not value, and B's pills are decisive.

**Strengths claimed (with evidence in Draft B).**
1. **ADOPT/DEFER/REJECT verdicts** on every candidate (B1-B20). Reviewer reads §6 and immediately knows what ships, what defers, what dies. Evidence: §6 tables.
2. **Effort labels** S (≤½ day) / M (1-3 days) / L (>3 days) per candidate, decoupled from value. Sprint planning can size the release in minutes. Evidence: header definitions + §6 tables.
3. **Owner column in risks** (§7). Lead / Tier owner / Skill owner / Sprint owner / DevOps / Ops / Quality agent owner. Forces accountability per risk. Evidence: §7.
4. **Blocking? flags** on open questions. 4 of 10 questions (Q1, Q3, Q4, Q8) explicitly identified as scope-boundary blockers. The other 6 are non-blocking and can land without resolution. Evidence: §8.
5. **Q8 commits to release-split**: "Sprint-executor adoptables (B12-B18) — same release as tier-rigor candidates, or a sibling release? **(b) split** — natural seam: tier rigor is `/sc:task` surface; sprint UID/resume is `cli/sprint/`. Different reviewers, different blast radius. Reference: `sc-release-split-protocol`. Blocking=Y." A flags this as `[inference]` in §9.3 and does not commit. Evidence: §8 Q8.
6. **REJECT candidates in the same table as ADOPT** (B8, B9, B19, B20). Forces reviewer to acknowledge the four rejected ideas in the same scan as the ten adopted ones. A buries these in non-goals and prose. Evidence: §6.

**Weaknesses identified in Draft A.**
1. A has no verdict column. Reviewer must read prose to infer recommendation. §6.3 ranking is a partial fix but does not say "this ships."
2. A has no effort labels. Sprint sizing cannot be done from A directly.
3. A has no Owner column. No accountability assignment.
4. A's 14 open questions are not flagged as Blocking vs non-Blocking. Reviewer cannot triage.
5. A's 656 lines includes content (RK-13, RK-14, RK-18, RK-19, RK-20) that A itself acknowledges as out of scope. B argues out-of-scope content should not appear in a release report at all; if it must appear, it should be in an appendix.
6. A's §9.1-§9.9 prior-art constraints duplicate content already in the v3.7 HANDOVER. B's compressed §9 carries the same constraints by reference without copying them.

**Concessions (genuine weaknesses in Draft B).**
1. B drops A's `[inference]` discipline. B's effort labels (S/M/L) are uncited; B's Owner assignments are uncited; B's Sev field uses High/Med/Low without derivation. A reviewer cannot tell which of B's claims are cited vs synthesized.
2. B drops 8 risk rows A has. Of those, RK-19 (sub-phase resume affects prompt-template format) is directly relevant to B's ADOPT'd B13. B should retain RK-19 even at the cost of one extra row.
3. B drops the §9.5 test-baselines (921 passed, 57 failed; TUI Waves 1-2 125/125). A reviewer cannot evaluate "does this release regress" without baselines.
4. B drops the §9.7 Wave-4 checkpoint heading parser regression note. SE-003 / B13 prompt-template work could regress this without B's reviewer knowing.
5. B's Q3 collapses A's Q1+Q2. The distinction matters because `/sc:forensic` consumer enumeration (A's Q2) is unresolved at the source level; B's collapse hides that uncertainty.
6. B has no TU-006 candidate (skill sub-files materialization). RK-17 in B does not have a candidate to address it. A's TU-006 closes that loop.
7. B has no coverage-notes self-check. The artifact does not surface what its author could not verify.

---

## Round 2: Rebuttals

### Variant 1 Advocate Rebuttal

Variant 2 advocate's central concession is the strongest argument for synthesis rather than selection: B explicitly grants A's evidence backbone is superior, then asks the reviewer to trade that backbone for decision pills. This is a false trade-off. Decision pills can be **added** to A's structure without removing the citations; A's evidence structure cannot be **added** to B without rewriting B to A's level of rigor.

Specific responses:

- **On B's claim that out-of-scope content (RK-13, RK-14, etc.) should not appear in a release report.** Disagree. These risks document the surface where future regressions can intrude. A flagging them is what prevents them silently sneaking into scope mid-implementation. RK-19 is the exemplar: B's own advocate concedes RK-19 must be retained.
- **On B's claim that A's §9.1-§9.9 duplicates HANDOVER content.** Partial concede — A could compress §9.x. But the constraint statements themselves (e.g., §9.7 Wave-4 parser regression) are not in HANDOVER; they are A's synthesis of HANDOVER + R7 §5 item 9. Removing them loses synthesis work.
- **On B's argument that prose-and-citation density is friction for sprint planners.** B should be the front matter, A should be the body. The merged artifact can lead with an executive summary in B's format (pills, effort, owners) and follow with A's evidence. Both consumer profiles served.

Additional concessions in light of B's advocate response:
- A's §6.3 ranking IS a verdict-by-inference. Pretending otherwise is uncharitable to A. But B's explicit ADOPT/DEFER/REJECT is strictly stronger and should be adopted.
- A's exhaustive non-goals (NG-1..NG-6) overlap with B's REJECT candidates. The overlap can be reconciled by treating REJECTs as the canonical non-goals when they map 1:1 (B8 ↔ NG-1, B9 ↔ NG-3 partial, B19+B20 ↔ NG-4) and keeping A's NG-5 (carry-over preservation) as a free-standing non-goal because B has no candidate equivalent.

### Variant 2 Advocate Rebuttal

Variant 1 advocate concedes the core point: A has no verdicts, no effort labels, no owners, no blocking flags. These are the artifacts a release lead consumes. A's response — "synthesize, do not select" — is the right answer for this debate, but it implicitly concedes A alone is insufficient.

Specific responses:

- **On A's claim that B's effort labels are uncited.** Concede partially. S/M/L are estimates, not citations. But A's value/tractability ratings have the same problem — A tags §6.3 with `[inference]` precisely because the rankings are uncited. B's labels are a more useful uncited synthesis than A's are.
- **On A's claim that B should add `[inference]` markers.** Concede fully. Any merged artifact should mark synthesized claims (effort labels, owner assignments, Sev ratings) as such. B's omission of this discipline is a genuine gap.
- **On A's claim that B drops 8 risk rows.** Concede selectively. Of the 8 dropped, retain RK-19 (sub-phase resume prompt-template format) and RK-20 (v3.7 live-execution not validated) because both directly affect B's ADOPT'd sprint-side work. The other 6 (RK-13 regex, RK-14 subprocess, RK-18 auto-diagnostic) map to DEFER'd or out-of-scope candidates and can stay in an appendix rather than the main register.
- **On A's claim that B's Q3 collapses Q1+Q2.** Concede. The merged artifact should split this back into two questions to preserve the `/sc:forensic` consumer-enumeration uncertainty.
- **On A's TU-006 candidate** (skill sub-files materialization). Concede this is a real gap in B. Adopt TU-006 (B's equivalent ID would be B-new). Suggest verdict: DEFER (alongside B10/B11 in the keyword-table-consolidation release) because TU-006 alone does not block this release.

Updated assessment of A: Stronger than B for the report's stated purpose (hallucination prevention). Weaker than B for release planning. The synthesis path is clear: base = A, overlay = B's decision instruments.

---

## Scoring Matrix

Per-point winner determination from Round 1 + Round 2 evidence. Confidence calibrated per scoring-matrix protocol.

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|------------------|
| S-001 (section depth) | Variant A | 70% | A's depth = traceability backbone; B's flatness is achieved by losing detail. Both advocates agree on this. |
| S-002 (source index format) | Variant A | 80% | A's absolute paths + line ranges (18 entries) is strictly more informative than B's R-ID compact table (8 entries). B does not contest. |
| S-003 (overlap matrix scale) | Variant A | 85% | A's 47 rows include 26 rows B's 21-row matrix drops; specifically the artifact items (O30, O31) and sprint surfaces (O38-O43) needed for traceability. B concedes. |
| S-004 (candidate inventory format) | Variant B | 88% | B's ADOPT/DEFER/REJECT verdicts + S/M/L effort labels are the decision-readiness device. A concedes its §6.3 ranking is a weaker substitute. |
| S-005 (non-goals representation) | Tie/Merge | 70% | A's NG-1..NG-6 and B's REJECT candidates (B8/B9/B19/B20) are equivalent for items both cover; reconcile by mapping REJECTs → non-goals and keeping A's NG-5 stand-alone. Both advocates concede this is a merge. |
| S-006 (prior-art constraint structure) | Variant A | 78% | A's §9.1-§9.9 includes §9.5 baselines and §9.7 parser regression that B drops. B's advocate concedes retaining these in any merged output. |
| C-001 (scope statement) | Tie/Merge | 65% | B's TL;DR for scan time; A's per-candidate citations for audit. Merge: B's TL;DR up top, A's detail below. |
| C-002 (recommendation format) | Variant B | 92% | ADOPT/DEFER/REJECT pills are the central decision-readiness contribution. A's advocate explicitly concedes. |
| C-003 (REJECT visibility) | Variant B | 80% | Putting B8/B9/B19/B20 in the candidate table forces acknowledgement. A's hiding in non-goals + prose is weaker for review. A's advocate concedes. |
| C-004 (risk schema) | Variant B | 88% | B's Owner + Sev columns add accountability A lacks. A's advocate explicitly concedes. |
| C-005 (risk volume) | Variant A | 75% | A's 20 rows including RK-19 and RK-20 are operationally relevant. B's advocate concedes RK-19 and RK-20 must be retained; the other 6 dropped rows are out-of-scope and can go to appendix. |
| C-006 (open-question format) | Variant B | 87% | B's Blocking? flag + Options + Recommendation triad is decision-ready. A concedes. |
| C-007 (naming-artifact policy) | Variant A | 70% | A's Q1+Q2 split preserves the `/sc:forensic` consumer uncertainty B's Q3 collapses. B's advocate concedes splitting back. |
| C-008 (source mapping rigor) | Variant A | 95% | A's `[inference]` discipline is the report's central anti-hallucination instrument. B has no equivalent and concedes the gap. |
| C-009 (effort sizing) | Variant B | 90% | S/M/L labels are planning-grade; A has none. A's advocate concedes. |
| C-010 (owner column) | Variant B | 90% | Owner field is uncontested; A's advocate concedes. |
| C-011 (status legend / pills) | Variant B | 82% | B's ✅⚠❌🛑 + ADOPT/DEFER/REJECT vocabulary is the decision-readiness device A lacks. Merge by adopting both. |
| C-012 (coverage-notes self-check) | Variant A | 92% | A's Known gaps list directly serves hallucination prevention; B has no equivalent. Uncontested. |
| X-001 (--skip-compliance + BLOCKED) | Variant B | 78% | B commits to a resolution (yes with `--reason`, audited); A leaves it open. The merged report should adopt B's resolution as the default while preserving A's Q6 as an audit trail. |
| U-001 (47-row matrix) | Variant A | 95% | Uncontested unique contribution. |
| U-002 (coverage-notes self-check) | Variant A | 92% | Uncontested. |
| U-003 (`[inference]` discipline) | Variant A | 95% | Uncontested. |
| U-004 (v3.7 test baselines) | Variant A | 90% | B's advocate concedes retaining these. |
| U-005 (Wave-4 parser regression) | Variant A | 88% | B's advocate concedes retaining. |
| U-006 (telemetry metering Q11) | Variant A | 78% | Surfaces a measurement gap B does not. |
| U-007 (v3.7 unfinished follow-ups Q13) | Variant A | 75% | Cross-cutting prerequisite reference B lacks. |
| U-008 (TU-006 skill sub-files candidate) | Variant A | 85% | B's advocate concedes this is a real gap; adopt TU-006 with DEFER verdict in merged artifact. |
| U-009 (effort labels S/M/L) | Variant B | 92% | Uncontested. |
| U-010 (ADOPT/DEFER/REJECT pills) | Variant B | 95% | Uncontested. |
| U-011 (Owner column) | Variant B | 90% | Uncontested. |
| U-012 (Q8 release-split commitment) | Variant B | 85% | B commits to splitting tier-rigor from sprint-side; A flags as inference. Both advocates concede B's commitment is the right call. |
| A-001 (MCP hard-req re-evaluation) | Unresolved | 50% | Neither advocate addresses promotion of this UNSTATED assumption. RK-11 partial coverage in B; out of scope for this merge. |
| A-002 (candidate-set closure) | Unresolved | 50% | Neither advocate addresses. Treated as acknowledged constraint of Wave-1 extract boundary. |
| A-003 (effort methodology) | Variant B | 60% | B's advocate concedes effort labels are estimates not citations; merged artifact should mark them `[inference]`. |
| A-004 (six-principles soundness) | Tie | 50% | Both drafts adopt without re-derivation. No advocate contests. Accepted as shared assumption. |
| A-005 (`--caller task-unified` consumer enumeration) | Variant A | 80% | A's Q2 surfaces this `[inference]`; B's R-5 mitigation ("Inventory consumers before renaming") aligns. Merged artifact should preserve both A's open question and B's owner-mitigation framing. |

### Aggregate per-point summary

- **Resolved with winner: 33 of 38**
  - Variant A wins: 14 (U-001..U-008 unique + S-001, S-002, S-003, S-006, C-005, C-007, C-008, C-012, A-005)
  - Variant B wins: 14 (U-009..U-012 unique + S-004, C-002, C-003, C-004, C-006, C-009, C-010, C-011, X-001, U-012, A-003)
  - Tie/Merge resolutions: 4 (S-005, C-001, A-004; structural reconciliation rather than winner-take-all)
  - Plus 1 explicit tie at A-004 = 4 ties net.
- **Unresolved: 3** (A-001, A-002 — out-of-merge-scope shared assumptions; one A-004 partial tie counted under tie)
- **Convergence: (33 of 38) = 86.8% ≥ 85% threshold → CONVERGED**

The split is approximately balanced because the drafts are complementary, not competing. The merge follows naturally: A's evidence backbone hosts B's decision instruments.

---

## Round 2.5: Invariant Probe — Fault-Finder Analysis

See `invariant-probe.md` for the complete five-category fault-finder table. Summary: 0 HIGH-severity UNADDRESSED items. Convergence gate NOT BLOCKED by invariant probe.

---

## Convergence Assessment

- Points resolved: 33 of 38 (with 4 tie-merges counted as resolved via synthesis)
- Alignment: 86.8% (33/38)
- Threshold: 85% (configured `--convergence 0.85`)
- Taxonomy coverage: L1 (style/cosmetic) covered by S-001, S-002, C-011; L2 (structural) covered by S-003..S-006, C-001..C-012; L3 (state-mechanics) covered by X-001 (state interaction with `--skip-compliance`), C-008 (citation provenance discipline), U-002/U-003 (hallucination prevention machinery). All three taxonomy levels covered.
- Invariant probe gate: 0 HIGH UNADDRESSED → not blocking
- **Status: CONVERGED**
- Unresolved points: A-001 (MCP hard-req re-evaluation — out of merge scope), A-002 (candidate-set closure — acknowledged as Wave-1 boundary)
- Round 3 SKIPPED — convergence achieved at Round 2.

**Decision:** Proceed to base selection.
