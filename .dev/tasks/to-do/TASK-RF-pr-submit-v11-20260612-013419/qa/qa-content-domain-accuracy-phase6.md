# QA Report — Domain-Accuracy Lens (Phase 6)

**Task:** pr_submit V1.1 build — Phase 6
**Date:** 2026-06-12
**Lens:** Domain accuracy (adversarial stance, fix_authorization: false, report-only)
**Files read:** `review-retrigger.md`, `auggie-fallback.md`, `SKILL.md` (all under `src/superclaude/skills/sc-pr-submit-protocol/`)

---

## The four mandated claims

### Claim 1 — "do NOT take the App's bait" distinction — CORRECT
- `auggie-fallback.md:21-23`: the App's `augment review` decline comment is the App DECLINING to auto-review, explicitly "NOT our operator re-trigger"; fallback is `sc:pr-submit` invoking its OWN `/sc:auggie-review`, "distinct from honoring the App's comment."
- `SKILL.md:94`: "do **NOT** 'take the App's bait' by treating the App's `augment review` decline comment as our operator re-trigger. This is `sc:pr-submit` invoking its OWN review."
- Matches the domain fact: App refuses to auto-review an abnormally-large PR; the fallback is our own review, not honoring the bait. **Accurate and cross-file consistent.**

### Claim 2 — `--depth quick`→auggie-review (review, NOT troubleshoot `--fix`) non-conflict — CORRECT
- `SKILL.md:89` (Wave 2): troubleshoot routing "NEVER emit `--depth quick --fix`" — the STOP is specifically the `--fix` combination dispatched to `sc:troubleshoot`.
- `auggie-fallback.md:33`: `--depth quick` "goes to `/sc:auggie-review`, a **review** — there is NO `--fix`, so it does NOT conflict with the severity-routing / troubleshoot-dispatch STOP on `--depth quick --fix`."
- `SKILL.md:94`: same explanation inline. The two surfaces are distinct (auggie-review vs troubleshoot dispatch); the STOP only governs the troubleshoot `--fix` form. **Accurate and internally consistent.**

### Claim 3 — watermark / attribution mechanism — CORRECT
- `review-retrigger.md:36-41`: watermark = re-trigger comment `createdAt` + pushed `headRefOid`; S5 poll attributes a re-review ONLY when (a) newer than watermark AND (b) reviewed SHA matches `pushed_commit_shas`; older-than-watermark ignored (same EC-23 staleness guard the decline classifier uses).
- Cross-checks with `auggie-fallback.md:18-19` (decline must be "newer than the watermark", stale pre-watermark decline ignored, EC-23) — same mechanism, same guard name. **Accurate and cross-file consistent.**

### Claim 4 — strict-once + clamp + single-shot (INV-R2/R3) — CORRECT (with two naming nits, see I-1/I-2)
- INV-R2 strict-once: `auggie-fallback.md:40-43` — gated on durable `auggie_review_invoked` set, keyed on `pr_number`, comment-independent, survives resume, "at most once per PR"; `push_count <= max_rounds + 1`. Corroborated `SKILL.md:69` and `SKILL.md:94`.
- INV-R3 clamp: `auggie-fallback.md:44` — `min(effective_max_rounds, 1)`, "one-way, monotone non-increasing." Corroborated `SKILL.md:94`.
- Single-shot: `auggie-fallback.md:46-49` — re-enters pipeline ONCE, advances only `fallback_round_counter` (cap 1), `round_counter` FROZEN, "NO loop-back, NO second `/sc:auggie-review` invoke, NO second re-trigger." Corroborated `SKILL.md:70, 94`. **Semantically accurate.**

---

## Issues Found (adversarial sweep)

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| I-1 | MINOR | `auggie-fallback.md:44` vs `SKILL.md:94` | Clamp variable mismatch: ref says `effective_max_rounds := min(effective_max_rounds, 1)`; SKILL says "clamp the budget to `max_rounds=1`". The clamped subject is named `effective_max_rounds` in one place and `max_rounds` in the other. Cap-1 semantics agree, but the variable name does not — a reader implementing the seam cannot tell which field is clamped. | Use one variable name in both (recommend `effective_max_rounds`, since `push_count <= max_rounds + 1` treats `max_rounds` as the *unclamped* user budget). |
| I-2 | MINOR | `auggie-fallback.md:45` vs `SKILL.md:94` | Event/seam name mismatch: ref records the clamp via the `max_rounds_clamped` event; SKILL names the seam `clamp_max_rounds`. Verb-noun vs noun-verb — likely intended as function (`clamp_max_rounds`) + emitted event (`max_rounds_clamped`), but neither file states that pairing, so it reads as a contradiction. | Disambiguate: state that `clamp_max_rounds` (the seam) emits the `max_rounds_clamped` event, or unify the token. |
| I-3 | MINOR | `review-retrigger.md:5` | Accepted-trigger phrasing lists `augment review` / `auggie review` / `augmentcode review` as the operator phrases; `review-retrigger.md:31` then asserts the body is "exactly `auggie review`" and "one of the contract's `accepted_trigger_phrases`." `auggie-fallback.md:16` independently names the decline regex matching "augment/auggie/augmentcode review". Consistent set, but `review-retrigger.md:3-5` uses `augment review` while line 25 POSTs `auggie review` — the chosen body is the middle variant. Not an error (any accepted phrase is valid), but the prose flips between `augment review` and `auggie review` within four lines, which can read as the App-bait phrase leaking into our own POST. | Optional: add one clause noting our POST deliberately uses `auggie review` (not the App's `augment review` from the decline), reinforcing the I-claim-1 boundary. |

### Adversarial checks that PASSED (no error found)
- **Decline trigger source:** `auggie-fallback.md:13-19` requires BOTH `decline_phrase_regex` ("abnormally large") AND `decline_retrigger_regex` to match — matches the domain fact that "abnormally large" = the App refusing to auto-review. Correct; not a single-regex over-match.
- **Decline observable at two poll points:** `auggie-fallback.md:19` (S2 OR S5 poll) matches `SKILL.md:94`. Consistent.
- **Counter independence:** `round_counter` frozen at fallback entry vs `fallback_round_counter` cap-1 — `auggie-fallback.md:46-49` and `SKILL.md:70` agree; no double-counting.
- **Re-trigger does NOT tick round_counter:** `review-retrigger.md:43-52` (INV-R1) + `SKILL.md:93` — tick happens only at `S5_AWAITING_REREVIEW → S2_CLASSIFY` on attributed re-review; timed-out re-trigger → `terminal_timeout`, no tick. Consistent.
- **Core-purity boundary:** `review-retrigger.md:8-13` (carries `gh` token by design → T-104 fork-pin, excluded from `CORE_PURE_FILES`) vs `auggie-fallback.md:8-11` (zero shell tokens → IN `CORE_PURE_FILES`). The two refs make the OPPOSITE membership claim, which is internally consistent given their differing surfaces (one POSTs via `gh api`, the other only documents a `> Skill` invocation). Not a contradiction. Correct.
- **`--post-pr` default:** `auggie-fallback.md:36` says default-true for a PR target, "`--no-post-pr` must NOT be passed" — consistent with the fallback report being auto-posted; no conflict with the strict-once invoke.
- **Fork-pin on re-trigger POST:** `review-retrigger.md:25,28-30` pins `repos/IronbellyOrg/IronClaude/...`, flags bare/upstream path as T-104 defect, notes `gh api` takes no `--repo`. Domain-correct (gh api uses path segment, not `--repo`).

---

## Self-Audit
1. **Factual claims verified against source:** 11 (4 mandated claims + 7 adversarial cross-file consistency checks), each cited to specific file:line.
2. **Files read in full:** all three named files (`review-retrigger.md` 54 lines, `auggie-fallback.md` 61 lines, `SKILL.md` 138 lines). No spot-checking.
3. **Why trust the result:** the three issues found are real cross-file naming/phrasing mismatches located by diffing the ref text against the SKILL.md orchestration prose line-by-line; the seven PASS checks each carry their own file:line evidence so a reviewer can re-verify independently.
4. **Web research:** none performed (instructed: read only named files, no web search). Tavily precedence N/A this review.

## Summary
- Mandated claims 1-4: all **CORRECT** on domain semantics.
- Issues: 0 CRITICAL, 0 IMPORTANT, 3 MINOR (two cross-file naming mismatches I-1/I-2; one optional phrasing clarification I-3).
- No domain-logic error found in the bait-distinction, the `--depth quick` non-conflict, the watermark attribution, or the INV-R2/R3 semantics. The three MINOR findings are nomenclature drift between the refs and SKILL.md, not behavioral defects.

**Note on the adversarial mandate:** the prompt asked me to assume ≥5 errors exist. After full reads I can substantiate only 3, all MINOR naming/phrasing drift. I am not inflating to reach 5 — the four core domain mechanisms are accurate and cross-file consistent. The honest count is 3 MINOR.

VERDICT: FAIL
