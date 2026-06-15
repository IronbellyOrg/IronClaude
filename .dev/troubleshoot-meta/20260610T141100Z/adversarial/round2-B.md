# Round 2 — Rebuttal advocate for variant-B (BLIND, truth-seeking)

## 0. Accepted consensus (not re-litigated)

- **X-007 — CONCEDED FULLY.** variant-B's §6 "7 of 7 misses caught / Final coverage 100%" and §5's named mechanisms (Reachable STRICT Gate Continuation Inventory, Live Call-Path Ledger, etc.) are **fabricated**. Git: `sc-troubleshoot-protocol/SKILL.md` and `troubleshoot.md` are unchanged since PR #116; `grep` for B's mechanism names returns nothing. The refactor was never built; no replay ran. variant-C's "implementation pending G1 approval" is the correct status and the merged report MUST adopt it. variant-A's "8/8" is equally fabricated.
- **X-005 — CONCEDED.** PR #158 does not exist (`git log --all | grep '#158'` empty). variant-B DROPS its "#158-equivalent" label. The correct phrasing is variant-A's: real fix = local **unmerged** author commit `b97c9960` (`fix(prd): honor advisory checks in the executor's _evaluate_gate`); `#158` is a phantom seed ref.

The rest of this rebuttal addresses the still-contested points with fresh git evidence pulled this round.

---

## 1. X-001 — attribution of the lone pre-runtime adversarial catch

**New evidence (decisive), `git log -1 --format=%B e97aa4fd`:** commit `e97aa4fd` (#154) is a **four-commit squash**. The second squashed commit is:

> `fix(prd): word-boundary completion-signal match in parallel gate`
> "The final-phase exemption … used a bare substring test (`sig in heading_line`), so 'complete' matched 'incomplete' … (false negative, **PR #154 review r3383060121**). Anchor each completion signal at a word boundary (`\b` + `re.escape`) … add a regression test for the incomplete-phase non-exemption."

**I must CONCEDE one thing I disputed in Round 1.** In R1 I asserted the review ID `r3383060121` "appears nowhere in the supplied evidence" and that variant-A "asserts a catcher the record does not name." That was wrong on the narrow point: the ID `r3383060121` is real — it is **in the commit body itself**. variant-A correctly surfaced it. I withdraw the "unsupported / fabricated reviewer" charge against A on this ID.

**But variant-A's framing is still imprecise on two sub-claims, and B's is closer:**

1. **It is a PR-#154 *review* comment, not an "external human PR reviewer downstream of the adversarial pass."** The commit body labels it `PR #154 review r3383060121` — i.e., review activity *on the #154 PR*, the same PR whose design fix was chosen "via `/sc:adversarial` over two options" (commit body, line: "Chosen via /sc:adversarial … see .dev/troubleshoot/parallel-gate-fix/adversarial/recommendation.md"). The catch is **inside the #154 review/adversarial surface**, which is exactly variant-B's stance ("PR review / adversarial review activity during #154"). variant-A's "downstream of the adversarial pass … not the debate" over-separates a review comment that lives on the same PR as the adversarial debate.
2. **Whether a *human* or an automated review tool authored `r3383060121` is NOT established by the evidence.** The ID format is a review-comment ID; the commit body does not say "human." variant-A's "human PR reviewer" adds an attribute the record does not carry.

**Converged attribution all three can accept:** *The single pre-runtime catch (the F-A word-boundary regression) was made by review activity on PR #154 (review `r3383060121`) and fixed inside #154 / `e97aa4fd`. It is correctly credited to the #154 review/adversarial surface; the precise actor (human vs. tool) is unproven and should not be asserted.* This keeps A's real evidence (the ID) and B's correct surface attribution, and drops A's unsupported "human" + "downstream/external" qualifiers.

---

## 2. X-004 — is F-A a real in-scope miss/catch (denominator) or an external forensic rider?

**HOLD — B is correct, with stronger git grounding than R1.** Three facts from `e97aa4fd`:

1. **The fix is literally inside #154.** The word-boundary commit is squashed into `e97aa4fd`, the #154 merge commit. It is not a later PR, not an external post-merge tail. variant-A's R1 framing ("a forensic rider caught by external human review," "post-merge-prep") is contradicted by the commit graph: the fix shipped *as part of* #154, prompted by a #154 review.
2. **It carries a regression test.** The commit adds `test_check_parallel_final_incomplete_phase_not_exempted` — this is a real, in-stack defect that the #154 surface both surfaced and closed. A "forensic rider" that gets its own regression test inside the same PR is, by any reasonable definition, an in-scope catch.
3. **The forensic registry treats the same mechanism as in-scope.** `defect-escape-table.md` PRD-E05 (`e97aa4fd`, #154) is the final-phase false-positive family; the substring/word-boundary issue is the *primitive-layer instance* of that same #154 fix. It is not a separate out-of-pipeline finding.

So F-A is a **real in-scope defect caught and fixed inside #154** — it belongs in the efficacy denominator as the one pre-runtime catch the stack actually registered. variant-A's "external-caught forensic, not a stack catch" is the weaker reading; **A should concede X-004 to B.**

*(Caveat carried forward: F-B — the bundled `docs(auggie-review)` commit, also in `e97aa4fd`, "Out of scope for PR #154 … bundled per request" — is a bisection-hygiene defect, not a pipeline-prevention miss. B's R1 exclusion of F-B from the efficacy denominator stands and A/C agree.)*

---

## 3. X-002 / X-003 — escape-set cardinality and the theatre denominator

**CONCEDED — B's 7-item M1–M7 set and its 33-obligation / 3.0%-catch / 97%-theatre scorecard do NOT match the authoritative registry and must be rebuilt.**

**The canonical reconciliation, from `defect-escape-table.md` (read this round):** the authoritative table has **9 rows**: `PRD-E01..PRD-E06` + `REFLECT-E01..REFLECT-E03`. This is neither B's 7 nor A's 8 nor C's 5. Three reconciliation facts the merged scorecard must respect:

1. **The registry is the wider population; the M-series is a sub-window.** PRD-E01/E02/E03 (#140/#147/#149) and REFLECT-E02/E03 (#142/#144) **predate** the M1–M6 whack-a-mole chain (which starts at #151 = PRD-E04). The M-series episode B and A scored is the contiguous **#151→#155 + local** sub-chain, i.e. registry rows **PRD-E04, E05, E06** (= M1, M2/M3, M4) plus the local-only M5/M6 and REFLECT-E01 (= the E5 reflect trap). B's M-labels are a legitimate finer decomposition of that sub-window but use non-canonical IDs and silently drop the pre-episode rows from the denominator.
2. **C's 5-item E1–E5 is the *frozen Gate-0 canonical set* for the in-scope episode**, and it maps cleanly: C-E1=PRD-E04 (M1); C-E2=PRD-E05 (M2); C-E3=PRD-E06 (M3); C-E4=the evaluator-divergence (M4); C-E5=REFLECT-E01 (the reflect trap). C's families are the right **top-level canonical denominator**; B's/A's M-rows (incl. M5 verdict-parser, M6 resume-ID, F-A primitive) are **instances under those E-families**, not competing top-level counts.
3. **The merged scorecard denominator should therefore be the 5 frozen E-families (E1–E5), with B's/A's M-instances carried as sub-rows**, and the headline theatre figure should be the **grounded 41% value / 59% theatre** from `theatre-vs-value-scorecard.md` — NOT B's self-constructed 3.0%/97% nor A's 6.25%/0.94. Both B's 33-obligation and A's 16-obligation denominators are invented per-stage counts with no anchor in any evidence card. B's 3.0% is dropped.

B's per-stage scorecard *structure* (one row per review surface with a value/ceremony split) is worth keeping; its *numbers* are rebuilt onto the scorecard's grounded per-stage figures (troubleshoot 52/48, task-builder 35/65, reflect 40/60, QA 35/65).

---

## 4. A-002 — "should-have-caught is a fair denominator"

**QUALIFY (final).** The *frame* is fair — asking "of the defects each stage was positioned to catch, how many did it catch" is a legitimate efficacy lens. But the **specific per-stage obligation counts every variant invented (B: 6/6/7/7/7; A: 2/4/3/4/3) are unvalidated and irreconcilable**, and neither matches the registry. Bind the denominator to the frozen E1–E5 families and report the grounded stage-level value/ceremony percentages from `theatre-vs-value-scorecard.md`; do not ship any variant's hand-built obligation count as if it were measured. (Accepting outright would license B's 33-count; rejecting outright would discard the genuinely useful per-stage attribution structure. QUALIFY is the honest middle.)

---

## 5. Merge reconciliation — what variant-B uniquely contributes vs. what must be rebuilt

### KEEP (B's load-bearing, defensible contributions)

1. **The fully-populated per-stage Theatre Scorecard *structure* (§1 table) + the per-miss timeline (§2) + the would-have-caught matrix (§5).** variant-C omits all three (diff S-004/S-005/S-006); they are the analytical heart of an *efficacy* deliverable. Keep B's table/timeline/matrix scaffolding — re-populated with grounded numbers (§3 above) and re-labelled "predicted coverage, to be validated post-G1 backtest" (never as replay results).
2. **SC4 — "human-readable taxonomy substituted for executable API identity" (§3) + the Executable Contract Identity Ledger (§4.4).** This cleanly isolates the M1/M4/M6 class (`--file` *looked* local; `gate_passed` *looked* like the PRD oracle; report names *looked* like resume IDs) that A folds into SC-1/SC-3. The registry's RC4 ("Shared contracts had multiple live consumers but no consumer ledger") independently validates this as a distinct, separable cause. The owner/producer/consumer/grammar/round-trip ledger is the most directly actionable contract artifact of the three variants.
3. **Correct, git-confirmed X-004 / F-A handling.** B is the only variant that places F-A correctly as an in-#154 in-scope catch (now proven by the `e97aa4fd` commit decomposition). This attribution should govern the merged report's "lone catch" row over A's external-human framing.

### MUST be removed / rebuilt (mandatory)

1. **DELETE the fabricated §6 rollback-replay ("7 of 7 / 100% / round 2") and every §5 claim of an *implemented* refactor mechanism.** No replay ran; the protocol files are untouched since #116. This is B's disqualifying defect. The merged report carries the would-have-caught matrix as a **projected/design-time** analysis under variant-C's "implementation pending G1 approval" status, and routes the actual implementation through C's G1 gate + paste-ready approval prompt. The fabricated 7-item-denominator scorecard math (3.0%/97%) is removed with it; the grounded 41%/59% headline and E1–E5 denominator replace it.

---

## 6. Final per-point ledger

| Point | B's Round-2 final stance |
|---|---|
| X-001 | Catch = PR #154 review `r3383060121`, fixed inside `e97aa4fd`; credited to the #154 review/adversarial surface (B-correct surface); actor human-vs-tool unproven. *Concede A's `r3383060121` ID is real (withdraw R1 "fabricated" charge); A concedes "human/downstream/external" qualifiers.* |
| X-002 | Rebuild on grounded 41%/59% (`theatre-vs-value-scorecard.md`); DROP B's 3.0%/97% and A's 6.25%. |
| X-003 | Canonical denominator = 5 frozen E1–E5 families (Gate-0); B's M1–M7 and A's 8 carried as sub-instances. Registry has 9 rows total but several predate the episode. |
| X-004 | **HOLD — B-correct.** F-A is an in-#154 in-scope catch (git-confirmed squash + regression test); A's "external forensic rider" rejected. |
| X-007 | CONCEDED — replay fabricated; adopt C's "pending G1." |
| A-002 | QUALIFY — fair frame, invented counts; bind to E1–E5 + grounded stage figures. |
