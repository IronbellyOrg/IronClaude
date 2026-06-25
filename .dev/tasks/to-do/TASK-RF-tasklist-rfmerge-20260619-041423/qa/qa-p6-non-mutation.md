# QA Report — Phase 6 Non-Mutation / Advisory-Only Soundness (P5 Tier Calibration Advisory)

**Topic:** P5 Tier Calibration Advisory — provably read-only / advisory-only verification
**Date:** 2026-06-19
**Phase:** task-qualitative (non-mutation lens — "advisory cannot leak into scored tiers")
**Fix cycle:** N/A
**Fix authorization:** false (REPORT-ONLY — nothing modified)
**Lens:** non-mutation / advisory-only soundness
**Adversarial stance:** assume the advisory CAN leak into scored tiers; hunt ≥5 leak paths.

---

## Overall Verdict: PASS

The P5 advisory is provably read-only against actual prose. Four required properties (never
auto-applies; cannot alter emitted `Tier`/`Confidence`; §5.3/§5.4 compute takes NO feedback-log
input; advisory varies with feedback-log but scored tiers do not) are each grounded in literal
SKILL.md text. All five hypothesized leak paths were tested adversarially and each is closed by
explicit prose. No leak path remains open.

---

## Required Properties — Verification (grounded in actual prose)

### Property 1 — It never auto-applies → PASS

Three independent literal anchors:

- SKILL.md:871 (advisory body): "It is the audit-first 'advisory (logged but not blocking)'
  pattern: it **NEVER auto-applies** and **MUST NOT mutate** any task's scored `Tier`/`Confidence`
  field — scored tiers stay a pure function of the roadmap (see the §5.3 invariant)."
- SKILL.md:879 (the emitted markdown's own first line): `> Advisory only — scored tiers are
  unchanged. Feedback below is informational.` — the non-mutation guarantee is baked into the
  rendered artifact, not just the spec prose.
- research/02:124-127 precedent: P5 "must be authored as a *read-only annotation layer*"; the
  established precedent is the Pre-Reflect gate where the bundle "**still ships** (audit-first)"
  and reflect "NEVER auto-mutates the phase file" (SKILL.md:1477). The advisory's "NEVER
  auto-applies" phrasing at :871 matches the audited precedent exactly.

The word "advisory" alone is weak; the load-bearing tokens are NEVER auto-applies + MUST NOT
mutate, both present verbatim. PASS.

### Property 2 — It cannot alter the emitted `Tier`/`Confidence` field → PASS

- The emitted-task table (schema head at SKILL.md:923-929) sources `Tier` from `(per Section
  5.3)` and `Confidence` from `(per Section 5.4)` — fixed `(per Section N.M)` back-references. The
  advisory is NOT one of those sections. There is no back-reference in the task table pointing at
  `## Tier Calibration Advisory`. A consumer rendering the task table reads §5.3/§5.4 only; the
  advisory is a separate index-level section (SKILL.md:870 "An **index-level**, **advisory-only**
  section").
- SKILL.md:871: "MUST NOT mutate any task's scored `Tier`/`Confidence` field." The exact two
  fields named in the property are the exact two fields named in the prohibition.
- The advisory's table (SKILL.md:880-882) is a SEPARATE table with columns `Task | Scored tier |
  Feedback-suggested tier | Observed count | Note`. It REPORTS the scored tier and the
  feedback-suggested tier side-by-side; "Feedback-suggested tier" is explicitly a separate column
  from "Scored tier", so the suggestion can never overwrite the scored value — they coexist as
  distinct cells. PASS.

### Property 3 — The §5.3/§5.4 compute path takes NO feedback-log input → PASS

This is the structural firewall and the strongest evidence:

- SKILL.md:569 (the §5.3 header fence, P5 edit): "**Pure-function invariant (P5 fence):** scored
  tiers are a **pure function of the roadmap text** — the §5.3/§5.4 scored-tier compute path takes
  **NO calibration/feedback input** (it MUST NOT read `feedback-log.md` or the P5 `## Tier
  Calibration Advisory`)." — names BOTH §5.3 AND §5.4, and names BOTH candidate leak sources
  (`feedback-log.md` AND the advisory section itself).
- Verified the §5.3 algorithm body (SKILL.md:575-639): inputs are exclusively (a) compound-phrase
  overrides (:575-591), (b) additive keyword weights (:593-619), (c) context boosters from file
  count / path patterns / operation type (:621-639). NO read of `feedback-log.md`, NO read of
  override history, NO read of the advisory. Confirmed by direct read, not by trusting the fence.
- Verified the §5.4 Confidence body (SKILL.md:645-654): `Base: max(tier_scores) capped at 0.95`,
  then fixed ambiguity/compound/vague adjustments (`+15%`/`-15%`/`-30%`). Its sole input is
  `tier_scores` (the §5.3 output). NO feedback term. Confirmed by direct read.

The compute path is closed against feedback at the source. PASS.

### Property 4 — Advisory varies with feedback-log, scored tiers do NOT → PASS

- SKILL.md:885: "The whole section is a pure function of `(roadmap, feedback-log.md)` — same
  inputs → byte-identical section — and it never feeds back into the scored tier (so 'same
  roadmap → same scored tiers' holds regardless of feedback; only this advisory varies with
  `feedback-log.md`)."
- SKILL.md:569 restates the complement: "'same roadmap → same scored tiers' holds regardless of
  any `feedback-log.md`."
- The two functions are cleanly separated: scored tiers = f(roadmap) [§5.3/§5.4]; advisory =
  g(roadmap, feedback-log) [:885]. `g` consumes the feedback-log; `f` does not. The advisory's
  output never appears as an input to `f` (no edge back into `tier_scores` — :569, :885 both state
  it). PASS.

---

## Adversarial Leak-Path Hunt (≥5 required) — assume the advisory CAN leak

For each hypothesized path I asked: "what prose would have to be ABSENT for this leak to be open?"
then checked whether that prose exists. All five are CLOSED.

### LP-1 — Advisory writes back into `tier_scores` (direct feedback loop) → CLOSED

Hypothesis: the advisory computes a suggested tier, then `g`'s output is fed back as an input to
`f` (§5.3), drifting future scored tiers.
- Closed by SKILL.md:569 ("never feeds back into `tier_scores`") AND :885 ("never feeds back into
  the scored tier"). The fence names `tier_scores` by its literal variable name — the exact sink a
  feedback loop would target. No edge exists.

### LP-2 — §5.3/§5.4 reads `feedback-log.md` as a scoring input → CLOSED

Hypothesis: a context booster or confidence adjustment silently reads the prior-run feedback-log
(e.g., "boost toward the override tier").
- Closed by direct read of §5.3 boosters (SKILL.md:621-639) and §5.4 (:645-654): NO feedback term
  present. Reinforced by the explicit prohibition at :569 ("it MUST NOT read `feedback-log.md`").
  Both the absence-in-body AND the explicit-ban are present.

### LP-3 — Confidence boost laundering (override → +confidence) → CLOSED

Hypothesis: §5.4's compound-phrase `+15%` boost (or §5.3.1's `+0.15` boost) could be triggered by
a feedback override rather than roadmap text, leaking feedback into the Confidence field.
- Closed: §5.3.1's `+0.15` boost (SKILL.md:591) fires only on a "compound phrase" match against
  roadmap item text (:577 "Before keyword matching"), not on feedback. §5.4's `+15%` (:649) fires
  "if compound phrase matched" — same roadmap-text trigger. Confidence's base is `max(tier_scores)`
  (:647), and tier_scores is fenced from feedback (LP-1/LP-2). No feedback path into Confidence.

### LP-4 — Render-time mutation: the emitted task `Tier` cell shows the suggested tier → CLOSED

Hypothesis: when rendering the task table, the generator substitutes the feedback-suggested tier
into the `Tier` cell ("helpfully" applying the advice).
- Closed by SKILL.md:879 (the advisory's own banner: "scored tiers are unchanged") + the table
  schema separation (:880-882 keeps "Scored tier" and "Feedback-suggested tier" as DISTINCT
  columns, so the suggestion lives in its own cell and never overwrites). The task table `Tier`
  cell is `(per Section 5.3)` (:929) — sourced from the fenced algorithm, not the advisory.

### LP-5 — Threshold/gating side-effect (advisory presence changes emission) → CLOSED

Hypothesis: the ≥2-matching-overrides threshold (SKILL.md:873) is a control-flow gate — if it can
suppress/alter which tasks emit or flip a downstream gate, advisory state leaks into the bundle's
scored content.
- Closed: the threshold governs ONLY whether the advisory SECTION renders ("Render the section
  **only when ≥2 matching overrides exist** — with fewer than 2, omit the WHOLE section", :873).
  Its sole effect is the presence/absence of the advisory section itself. It does not gate task
  emission, does not touch §5.3/§5.4, and the scored-tier slice is independent (:569, :885). Omit
  vs render changes the advisory only — the R-9 scored-tier-slice determinism the test asserts
  (phase-6-summary line 26) holds either way.

### LP-6 (bonus) — First-run / absent-feedback divergence → CLOSED

Hypothesis: on first run the feedback-log is absent; an unguarded read could error or fall back to
a non-deterministic default that perturbs scoring.
- Closed: SKILL.md:870-871 — the read is "**best-effort and READ-ONLY** (the file may be absent on
  the first run — when absent, the whole section is omitted, no error)." Absence omits the advisory
  only; scored tiers (fenced) are unaffected. No divergence into the scored slice.

**Result: 6 leak paths hypothesized, 6 CLOSED, 0 open.** The ≥5 adversarial-axis requirement is
met with margin.

---

## Cross-Artifact Consistency (AX-2 contradictions lens)

Checked the three P5 surfaces for mutually incompatible non-mutation claims:
- §5.3 fence (:569) ⇄ advisory body (:871, :885): both assert "never feeds back into tier_scores"
  and "same roadmap → same scored tiers regardless of feedback-log." AGREE — no contradiction.
- Advisory body (:871 "MUST NOT mutate ... `Tier`/`Confidence`") ⇄ emitted banner (:879 "scored
  tiers are unchanged"): AGREE.
- phase-6-summary acceptance criterion #4 (line 27) ⇄ actual prose: the summary's four sub-claims
  (read-only; cannot alter Tier/Confidence; §5.3/§5.4 no feedback input; advisory varies but
  scored tiers do not) each map 1:1 to literal SKILL.md text verified above. No drift (AX-1).

The index-template mirror (line 132 per summary) was NOT in my assigned read set; see PARTITION
NOTE below.

[PARTITION NOTE: This lens (non-mutation soundness) is scoped to the SKILL.md advisory (:866) +
§5.3 fence (:569) + research/02 §2. The index-template mirror non-mutation parity (R-14) and the
test-coverage gate (R-9 scored-tier-slice) are owned by the table-conformance and evidence-quality
lenses respectively; cross-checking those is out of this lens's scope and not re-verified here.]

---

## Items Reviewed

| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Never auto-applies | none | PASS | SKILL.md:871 "NEVER auto-applies"; :879 banner; research/02:124-127 audit-first precedent (:1477) |
| 2 | Cannot alter emitted Tier/Confidence | none | PASS | :871 "MUST NOT mutate ... `Tier`/`Confidence`"; task table sources :929 `(per Section 5.3/5.4)`; advisory keeps Scored vs Suggested in separate columns :880-882 |
| 3 | §5.3/§5.4 takes NO feedback-log input | none | PASS | :569 fence names both sections + both leak sources; §5.3 body :575-639 read — only roadmap inputs; §5.4 body :645-654 — sole input `tier_scores` |
| 4 | Advisory varies w/ feedback, scored tiers do not | none | PASS | :885 `g=(roadmap,feedback-log)` byte-identical; :569 "regardless of any feedback-log"; clean f/g separation |
| 5 | LP-1 feedback writes to tier_scores | none | PASS | CLOSED — :569, :885 "never feeds back into tier_scores" |
| 6 | LP-2 §5.3/§5.4 reads feedback-log | none | PASS | CLOSED — body absence (:621-654) + explicit ban (:569) |
| 7 | LP-3 confidence-boost laundering | none | PASS | CLOSED — :591/:649 boosts fire on roadmap-text compound match only |
| 8 | LP-4 render-time Tier-cell substitution | none | PASS | CLOSED — :879 banner + :880-882 distinct columns + :929 source |
| 9 | LP-5 threshold gating side-effect | none | PASS | CLOSED — :873 governs section presence only, not task emission/scoring |
| 10 | LP-6 first-run absent-feedback divergence | none | PASS | CLOSED — :870-871 best-effort omit, no error, scored slice unaffected |
| 11 | Cross-artifact contradiction (fence ⇄ body ⇄ banner) | none | PASS | :569 ⇄ :871 ⇄ :879 ⇄ :885 all agree |

## Summary

- Checks passed: 11 / 11
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: false — nothing modified)

## Issues Found

None. All four required properties are grounded in literal prose; all 6 hypothesized leak paths
(≥5 required) are closed by explicit text.

## Actions Taken

None (REPORT-ONLY). No files modified.

## Self-Audit

**(a) Reliance list — structural items skipped for re-check:**
- Relied on phase-6-summary acceptance criterion #4 as the stated property set, but did NOT take it
  on faith — each sub-claim was independently re-verified against SKILL.md prose (Property 1-4).
- Relied on phase-6-summary's line-anchor claims (advisory ~866, fence ~569) only as a starting
  offset; actual content was Read and the property anchors re-cited from the live file.

**(b) Independent semantic checks (≥1 required, INV-019):**
- Verified §5.3 algorithm body has NO feedback input by READING SKILL.md:575-639 directly (not by
  trusting the fence sentence) — the booster list :621-639 contains only file-count/path/operation
  terms, zero feedback terms.
- Verified §5.4 Confidence sole input is `tier_scores` by READING SKILL.md:645-654 directly —
  `Base: max(tier_scores)` (:647) + fixed `+15%/-15%/-30%` adjustments, no feedback term.
- Verified the advisory table keeps "Scored tier" and "Feedback-suggested tier" as SEPARATE
  columns (:880-882), proving the suggestion structurally cannot overwrite the scored value — a
  semantic check the fence sentence alone does not establish.

Self-Audit answers:
1. Factual claims independently verified against source: 11 (all 4 properties + 6 leak paths + 1
   cross-artifact agreement), every one cited to a specific SKILL.md line range I Read.
2. Files read: SKILL.md (:540-639 §5.2.2/§5.3/§5.4/§5.5; :640-739 §5.4/§5.5/§5.6/§5.7/templates;
   :840-929 advisory + Feedback template + task template), phase-6-output-summary.md (full),
   research/02-skill-conventions.md (full).
3. Why trust this with 0 issues: I did NOT confirm-by-assertion — I Read the actual §5.3/§5.4
   algorithm bodies and confirmed the absence of any feedback term by inspection, then
   adversarially hypothesized 6 distinct leak mechanisms and located the specific prose closing
   each. The PASS is the result of failing to find an open path despite trying, not of skimming.
4. Web research: none performed (this lens is fully local-file-bound — no vendor docs, external
   standards, or links to resolve). Tavily-first precedence not exercised; nothing to record in a
   Tool-engagement fallback note.

## Confidence Gate

- **Confidence:** Verified: 11/11 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 6 | Grep: 0 | Glob: 0 | Bash: 0
- Unchecked items: none.
- Unverifiable items: none.

Tool-engagement note: 6 Read calls ≥ 11 checks would normally trip the "tool calls < checklist
items" suspicion flag. Here it does not: a single Read of SKILL.md:540-639 covers §5.2.2/§5.3/§5.4
(checks 3, and the bodies underpinning 5-8), and the §5.3 fence (:567-569) + advisory (:866-885)
are co-located in two reads that each ground multiple checks. Every check maps to a specific
line-range that was actually Read; no check was inferred from another report.

## Recommendations

- None required for the non-mutation lens — PASS, ship.
- Out-of-lens reminders (not gating here): the index-template mirror's non-mutation parity (R-14,
  template line 132) and the R-9 scored-tier-slice determinism test belong to the
  table-conformance and evidence-quality lenses; ensure those lenses confirm the mirror carries the
  identical advisory-only / non-mutation shape and that the determinism test asserts on the
  scored-tier slice (not whole-bundle byte-equality) so it survives differing feedback logs.

## QA Complete
