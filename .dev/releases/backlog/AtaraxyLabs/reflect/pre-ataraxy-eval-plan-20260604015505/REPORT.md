# /sc:reflect UC-1 (pre-execution) — Ataraxy-Labs Eval Release Plan

- **Mode:** pre (UC-1 coverage / best-practice / gap audit)
- **Spec (driving):** original user ask + `seed-brief.md` (success criteria + constraints)
- **Strategy under review:** `.dev/releases/backlog/AtaraxyLabs/merged-requirements.md`
- **Tier reached:** 2 (3 heterogeneous reviewers: sonnet/analyzer, haiku/qa, opus/architect)
- **Merge method:** synthesized-inline (findings complementary, not competing) + evidence-validator gate
- **Calibrated confidence:** 0.87
- **Coverage estimate:** ~0.77 (19 covered / 10 partial / 1 unmapped of ~31 spec requirements)
- **Best-practice grade:** 3/5 — methodologically strong, but 6 HIGH execution gaps + 1 internal contradiction
- **Verdict:** ⚠️ **NOT-YET-EXECUTABLE** — close the 6 HIGH gaps before Phase 0 spend. The plan's *thinking* is sound; its *executability and completeness* have real holes — exactly what a pre-flight is for.

> Note: the brainstorm's adversarial pass debated the 3 variants against each other; it never audited the *merged output* against the spec. This audit fills that gap and confirms the merge **dropped material content** (owner fields, security, concrete harness artifacts).

---

## HIGH findings (close before Phase 0)

### H1 — Between-tool gating self-contradiction `[grounded: merged §3 L95-96 vs §8.2 L200]`
§3: "weave S0 **blocked until inspect S4 live + KEEP**." §8.2: "inspect KILL does **not** block weave." These contradict: if weave needs inspect at S4-KEEP, an inspect KILL blocks weave. **Fix:** gate on the prior tool reaching a *terminal* state (KEEP-and-live **OR** explicit KILL), and state plainly that weave depends on `sem-core`, not on inspect — so an inspect KILL lets weave proceed directly (this was V1's intent, lost in compression).

### H2 — No owner / decision authority / tie-break `[grounded: no Owner|RACI match in merged-requirements.md; dropped from variant-2 §10.5 `Owner:` + variant-3 C4 "named owner"]`
Kill/keep gates exist but **no one is named to pull the trigger**, and there is no rule for a borderline/tie gate result. **Fix:** add `Owner` + keep/kill decision authority + tie-break rule to the §5 scorecard (restore V2's decision-record `Owner:` field).

### H3 — No security / data-egress treatment at all `[grounded: zero security|egress|secret match in merged-requirements.md]`
inspect's `review` pipes changed entities to **external LLM providers**; all three tools read the whole repo. The plan never addresses code egress, provider retention, or secret handling. **Fix:** add a Security & Data-Handling section — provider-egress policy, secret-scrubbing before `inspect review`, and a stance on routing private fork code to third-party endpoints.

### H4 — Blind adjudication assumes a panel that doesn't exist `[grounded: merged §7 "hide tool source from judge"; dropped variant-2 §14.3 "human final say" + variant-3 senior-dev budget]`
The judging protocol demands blinding, but the framework is effectively a **solo operator** — the same person runs evals and labels findings → contamination. **Fix:** specify a solo-blinding mechanism (randomized tool naming + an LLM adjudicator with stripped provenance — reflect's *own* evidence-validator pattern is the template) OR explicitly staff + budget human adjudication.

### H5 — G0-1 corpus feasibility unverified + synthetic-backfill unspecified `[grounded: merged §2 G0-1, §7 tiered minimums; partially corrects reviewer-2 "PRs live upstream"]`
*Correction:* this fork hosts its own PRs (per the CLAUDE.md PR-target rule) and ~30 merge commits + 152 Python commits exist — so the corpus is **not** empty. The real gap: G0-1's "**OR** documented synthetic-backfill plan" is named but never specified, and the ≥20 PR / ≥10 merge volume is unverified against the actual fork. **Fix:** inventory actual fork PR/merge counts as the *first* Phase-0 action; if short, specify the synthetic-case construction (the §11 curated-defect list is the seed).

### H6 — Eval harness under-specified for execution `[grounded: merged §4 lists ~10 components, no runner contract; variant-3 bash latency-harness L109-163 compressed to a §6 path reference]`
The harness is named (corpus manifest, runners, token meter…) but has **no runner I/O contract, no per-scenario run steps, no output schema** — yet every downstream day-estimate rests on it (§2 budgets Phase-0 build at 1-2 days). V3's concrete, buildable bash harness — the one artifact you could run tomorrow — was reduced to a path mention. **Fix:** restore the concrete harness artifacts (latency bash, install matrix, token-counter) and define the runner contract before the day-counts hold.

---

## MED findings

| # | Finding | Grounding | Fix |
|---|---------|-----------|-----|
| M1 | "Broad variety of scenarios" (explicit user ask) reduced to a named, unspecified generalization appendix | merged §11 L245 / §14 step 5 L280 — "optional", no inventory | Add a skeleton multi-repo/multi-language scenario inventory + thresholds, or explicitly rescope the user's "broad" expectation to native-first |
| M2 | Token-reduction-vs-Auggie has no isolation method | merged §5 L125/136, §8.1 L190 "vs Auggie" — no measurement of how to separate Auggie's token share from the multi-wave prompt | Define the Auggie-baseline measurement harness (the headline sem metric depends on it) |
| M3 | Sample-size confidence interpolation gap | merged §7 — 5PR/3merge (shadow) vs 20PR/10merge (graduate); 12 PRs → undefined band | Define interpolation/banding between the two tiers |
| M4 | weave value-surface may be too small to hit sample size (reframed from reviewer-2 F3) | weave acts only on Python; ~92% repo is `.md` → falls back to git | Confirm enough Python worktree merges exist for the gate; `.md` is correctly out of weave's scope (not a measurability flaw) |
| M5 | Markdown-ceiling (most-probable sem-KILL outcome) buried; V1's honest self-assessment dropped | merged CP-1 + one risk row | Elevate the `.md`-substrate risk to a first-class plan assumption |

---

## Dropped-from-variant register (merge provenance loss)
- V1: rollback **step-ordering** (variant-1 §6 → merged §10 lost the sequence) → feeds H1/H2
- V2: per-scenario minimum-sample table + decision-record `Owner:` field → feeds H2/H5
- V3: glibc/musl install-matrix rows + the concrete bash latency-harness → feeds H6

---

## What the plan gets RIGHT (not all findings are gaps)
- Baseline-anchoring (beat Auggie, not raw git diff), vendor-claim skepticism (inspect keyword-judge rejected), kill-first gating, reversibility doctrine, multi-vendor token economics, and the statistical-validity guards are all **genuinely strong** and survive scrutiny. The plan's *methodology* is sound; the gaps are in *executability, ownership, security, and completeness*.

## Grounding gaps / honest limits
- Merge method was **inline synthesis**, not `sc-adversarial` Mode A (the 3 cards were complementary, not competing — inline merge is appropriate here and disclosed).
- Calibration was inline-orchestrator (disjoint from the 3 reviewer classes), not a separate `confidence-calibrator` spawn — documented fallback.
- Coverage_pct (~0.77) is a reviewer estimate, not a mechanical requirement-ID match (the spec is prose success-criteria, not enumerated IDs).
