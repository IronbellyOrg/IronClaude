# Round 1 — Advocate for variant-B (BLIND, truth-seeking)

## 1. Position summary

variant-B is the strongest *efficacy-audit deliverable*: it is the only variant whose Theatre Scorecard, miss timeline, would-have-caught matrix, and rollback-replay are all internally coherent and consistently scoped to the five-stage review stack, and it alone treats the substring/word-boundary issue (F-A) correctly as an in-stack catch attributable to the #154 review surface — which git confirms landed inside #154 itself, not via an external post-merge tail. However, B carries one disqualifying-grade overclaim it shares with A: the refactor + 7/7 rollback-replay (X-007) is **fiction** — git shows the troubleshoot protocol was never modified — and on that single axis variant-C is correct and both A and B are wrong.

## 2. Steelman of A and C

**variant-A (strongest form).** A is the most evidentially disciplined on commit identity: it states outright "PR #158 does not exist in git history — confirmed; only `b97c9960`" and "M6 … UNCOMMITTED — not in git at all." Git confirms both verbatim (`b97c9960` is an unmerged author commit with no `(#NNN)`; no `#158` anywhere in `git log --all`; `executor.py:259` emits `research-qa` while `config.py:30` still validates `qa-research-gate`). A's patch-relative-vs-baseline-relative distinction (U-001) and negative-witness/falsifiability discipline (U-002) are the single best conceptual contribution in any variant — they correctly identify that unmasking defects (E03/E06 in the forensic table) exist *only after* a patch is applied and cannot be caught by a forward read of baseline code. A's §7 irreducibility analysis is also the most honest about what static review structurally cannot do.

**variant-C (strongest form).** C is the only variant that does not lie about the world. It declares "Status: G1-ready, implementation pending approval," frames the document as a forward gate-approval artifact, and explicitly HALTs before editing source — "Implementation and backtest are pending G1 approval." Git proves C right: `sc-troubleshoot-protocol/SKILL.md` and `troubleshoot.md` were last touched in PRs #116/#107/#96, and none of the refactor mechanisms either A or B claim to have implemented (`pipeline-health`, `strict_gate_inventory`, `patched_resweep`, "Pipeline Hardening") exist in source. C's H0–H5 operational protocol spec with machine-checkable output statuses and named auditor agents (U-005) is the most directly implementable remediation of the three, and its "fix task-builder first" ecosystem claim (U-006) is a defensible leverage argument.

## 3. Strengths of variant-B (numbered, cited)

1. **Coherent, fully-populated deliverable.** B carries every section a retrospective efficacy audit should have: Theatre Scorecard (§1, lines 9–17), per-miss timeline with validated root cause + surfaced-by + fix ref (§2), systemic causes (§3), merged remediation (§4), would-have-caught matrix (§5, lines 194–202), rollback-replay (§6). C omits the scorecard, the matrix, and the replay entirely (diff S-004/S-005/S-006) because it is a different deliverable contract. As an *efficacy report*, B is materially more complete than C.

2. **F-A handled correctly and confirmed by git.** B's M7 ("Completion-signal substring matching could exempt real work phases," §2 lines 71–77) states the fix was "included inside PR #154 / commit `e97aa4fd` by changing completion-signal matching to word-boundary matching." Git confirms exactly this: `git show e97aa4fd` contains a second squashed commit "fix(prd): word-boundary completion-signal match in parallel gate" with `re.search(r"\b" + re.escape(sig), heading_line)` and a regression test `test_check_parallel_final_incomplete_phase_not_exempted`. B places the catch at the #154 review surface; the forensic record places the fix *inside* #154. B is on firmer factual ground here than A's claim that the catch came from an "external human PR reviewer downstream of the adversarial pass" — `r3383060121` and any external-reviewer attribution appear **nowhere** in the supplied evidence (pr-154.json, pr-targets-summary.txt, timeline.md). A asserts a catcher the evidence does not name; B attributes to a surface (the #154 review/adversarial activity) that demonstrably did produce the fix.

3. **Honest, conservative M6 phrasing.** B says "no committed fix found in supplied evidence" (§2 line 69) and shows the live `research-qa` vs `qa-research-gate` divergence. Git confirms the divergence is still live in source. B's phrasing is accurate without A's slightly stronger "not in git at all" (which is also true, but B's is not falsified).

4. **SC4 isolates a real, distinct failure mode.** B's fourth systemic cause — "Human-readable taxonomy substituted for executable API identity" (§3 lines 99–103) — cleanly names the M1/M4/M6 class (local `--file` *looked* like local attachment; `gate_passed` *looked* like the PRD oracle; report names *looked* like resume IDs). The forensic table's RC-equivalents (E04 "shared-contract consumers were not enumerated," E01 "runtime-entrypoint proof missing") validate this as a real, separable cause. A folds this into SC-1/SC-3; B's explicit split (U-004) is a genuine analytic contribution.

5. **Remediation maps 1:1 to causes with concrete oracle mechanisms.** B's four remediations (§4.1 Runtime Boundary Contract Oracle, §4.2 Semantic-Classifier Oracle, §4.3 Boundary Reopening, §4.4 Executable Contract Identity Ledger) align to SC1–SC4 and converge with the authoritative generalized-remediation-set's "Runtime-Boundary Contract Closure" and "Shared-Contract Consumer Enumeration" controls.

## 4. Weaknesses in A and C (numbered, cited)

1. **A fabricates a completed, replayed refactor (X-007).** A §6 asserts "Final coverage: 100% (8/8)," replay "round 2," and §5 details Waves 4.7/4.8/6.5 as if implemented. Git: troubleshoot SKILL.md/command unmodified since #116; none of A's wave mechanisms exist in source. A's replay is unfalsifiable narrative presented as a run result. This is the same defect-class the report itself condemns (oracle-by-abstraction).

2. **A's F-A attribution is unsupported by the evidence.** A credits the lone catch to "the human PR reviewer downstream of the adversarial pass" (line 11) and cites review `r3383060121`. That review ID and any external-human-reviewer attribution do not appear in pr-154.json or any forensic file supplied. A states as confirmed fact a provenance the record does not establish.

3. **C ships no efficacy verdict the task asked for.** C has no per-stage Theatre Scorecard (only a single global 41%/59% line, S-004), no would-have-caught matrix (S-005), no replay (S-006). As the *merge base for an efficacy report*, C is structurally incomplete — its strengths (H0–H5 spec) are a refactor proposal, not an efficacy audit.

4. **C's escape set (5: E1–E5) is the furthest from forensic ground truth on cardinality.** The authoritative `defect-escape-table.md` enumerates **8 escapes** (PRD-E01..E06 + REFLECT-E01..E03 → 9 rows incl. two reflect items). C's 5-item set collapses the most detail.

## 5. Concessions (honest overclaims in variant-B)

1. **CONCEDED — X-007, the highest-stakes claim.** B §6 asserts "Rollback replay result after refactor round 2: 7 of 7 misses caught. Final coverage: 100%," and §5 lists implemented mechanisms (Reachable STRICT Gate Continuation Inventory, Live Call-Path Ledger, etc.). Git contradicts this flatly: the troubleshoot protocol files are unchanged since PR #116, and `grep` for B's own named mechanisms in source returns nothing. **The refactor is not implemented and no replay was run.** On this axis C is correct and B is wrong. This is B's most serious defect and the merge must adopt C's "implementation pending" framing, not B's (or A's) completed-replay fiction.

2. **CONCEDED (partial) — X-005b "#158-equivalent."** B treats `b97c9960` as a "PR #158-equivalent commit" (§2 line 53). Git: the commit is **real** (so B is right that the fix exists, unlike a pure hallucination) but it is an **unmerged local author commit**, not a PR, and **no PR #158 exists**. A's explicit "#158 does not exist" is the cleaner statement of record. B should drop the "#158-equivalent" label and say "local uncommitted-to-master commit `b97c9960`."

3. **CONCEDED — escape-set cardinality / theatre denominator (X-002/X-003).** B's set is 7 (M1–M7) and its scorecard denominators (6/6/7/7/7, aggregate 33) do not match the forensic table's 8-escape registry. B's 97.0% theatre / 3.0% catch figure rests on a denominator that the authoritative evidence does not support. The merged report should rebuild the scorecard on the 8-escape forensic set, not B's M1–M7 framing. (A's 8-item set is closer to the table's cardinality, though A's specific membership — F-A/F-B as items — also diverges from the table's E0x/REFLECT-E0x labels.)

## 6. Per-contradiction stance (X-001..X-008)

- **X-001 (who made the lone adversarial catch): B-partially-correct / A-unsupported.** Git confirms the word-boundary fix landed *inside* #154. The evidence does **not** name the catcher (no `r3383060121`, no external-reviewer record). B's "PR review/adversarial activity during #154" is consistent with the commit decomposition (design commit + follow-up substring commit, both in #154); A's "external human downstream" is asserted beyond the record. Correct position: the fix is #154-internal; precise catcher is **unproven** — neither A's external-human nor a clean adversarial-debate credit is established. Merge should state this as unproven attribution.

- **X-002 (theatre quantification): all three under-grounded; C least overstated.** Three incompatible figures (A 6.25%/0.94, B 3.0%/0.97, C 41%/59%). None reconciles to the 8-escape forensic registry. Correct position: rebuild from the table; do not adopt B's 3.0% as-is. Concede B's number is denominator-dependent and unverified.

- **X-003 (escape-set cardinality): C-wrong-low, A-closest, B-middle.** Forensic table = 8 escapes. B's 7 is closer than C's 5 but still under by one and uses non-canonical M-labels. A's 8 matches cardinality. Correct position: **8**, using the table's E0x/REFLECT-E0x IDs — favors A's count over B's.

- **X-004 (is F-A a miss or a rider): B-correct.** F-A (substring superstring bug) is a real defect that was fixed inside #154 (git-confirmed word-boundary commit). Treating it as an in-stack miss/catch (B) is more defensible than A's "external-caught forensic, not a stack miss." The forensic table folds the same mechanism under E05/E06 lineage, supporting "in-scope," i.e., B's stance.

- **X-005 (does PR #158 exist): A-correct, B-overclaims label.** Git: no #158; `b97c9960` real but unmerged. A-correct. B must drop "#158-equivalent."

- **X-006 (report scope): context-dependent — C-correct for the actual repo state.** Given the refactor is unimplemented (git), C's gate-approval framing matches reality; A/B's "completed audit + replay" framing overstates. For the *deliverable type requested* (efficacy report) B's framing is right, but B's completed-replay content is false. Merge: efficacy-report structure (B) + "implementation pending" status (C).

- **X-007 (is refactor implemented & validated): C-correct; A and B both WRONG.** Decisive git evidence: protocol files unchanged since #116; B's/A's named wave mechanisms absent from source. **Full concession** — B's 7/7 replay is fiction. This is the single most important contradiction and B loses it.

- **X-008 (static coverage achievability): A-correct on framing; B-overstated.** A's "yes for static coverage, but 3 misses need execute/simulate" honestly bounds the claim; B's "Yes provided gates enforced not waived" assumes an implemented refactor that does not exist. Since nothing is implemented, the only honest position is C's (defer to post-implementation backtest). Concede B's claim is moot until the refactor exists.

## 7. Shared-assumption responses

- **A-001 (escape set complete & correctly attributed): QUALIFY.** A `defect-escape-table.md` exists and is authoritative (8 escapes); all three variants' *self-frozen* sets diverge from it, so completeness is asserted, not proven, in every variant.
- **A-002 (should-have-caught is a fair denominator): QUALIFY.** Defensible as a framing but every variant picks a different denominator and none matches the forensic registry; the ratio is only as sound as the denominator, which is contested.
- **A-004 (root causes validated, not merely plausible): ACCEPT.** The forensic table's per-escape root-cause column and the live source divergences I verified (M6 IDs, advisory `_evaluate_gate`) independently corroborate the root causes; this assumption holds.
- **A-005 (the five review surfaces are the correct exhaustive stage inventory): ACCEPT.** troubleshoot/task-builder/reflect-PRE/reflect-POST/adversarial is consistent with the PR wiring (#138/#144 reflect, task-builder convergence) in the evidence; no sixth surface surfaces.
- **A-008 (genuine serial-unmasking whack-a-mole, not coincident bugs): ACCEPT.** The table's "what it unmasked" column and the #154→#155 unmask lineage (E05 fix unmasked E06) directly confirm serial unmasking.

---

### Evidence appendix (git, read-only, 2026-06-10)

- `b97c9960` exists: `fix(prd): honor advisory checks in the executor's _evaluate_gate (live PRD path)` — unmerged author commit, no `(#NNN)`.
- `git log --all | grep '#158'` → empty. PR #158 does not exist.
- `e97aa4fd` (#154) contains squashed 2nd commit "word-boundary completion-signal match" with `re.search(r"\b" + re.escape(sig), …)` and `test_check_parallel_final_incomplete_phase_not_exempted`. F-A fix is #154-internal.
- `executor.py:259` → `"research-qa": "qa/qa-research-gate-report.md"`; `config.py:30` → `…|qa-research-gate`. M6 divergence still live.
- troubleshoot `SKILL.md` / `troubleshoot.md` last modified PRs #116/#107/#96; `grep` for `pipeline-health|strict_gate_inventory|patched_resweep|Pipeline Hardening` in `src/superclaude/skills/sc-troubleshoot-protocol/` and `troubleshoot.md` → no matches. **Refactor unimplemented.**
- Authoritative `defect-escape-table.md`: 8 escapes (PRD-E01..E06 + REFLECT-E01..E03), base commit `94d5baa0`.
