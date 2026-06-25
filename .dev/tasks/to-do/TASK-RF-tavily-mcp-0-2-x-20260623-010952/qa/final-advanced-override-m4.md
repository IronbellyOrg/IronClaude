VERDICT: PASS

# QA Report — M4 / X3-EXCEPTION (advanced-override divergence)

**Topic:** Tavily MCP 0.2.x upgrade — per-call `search_depth: advanced` override vs server DEFAULT_PARAMETERS baseline
**Date:** 2026-06-23
**Phase:** doc-qualitative (M4 / X3-EXCEPTION lens)
**Fix cycle:** N/A (fix_authorization: FALSE — report only)
**Stance:** Adversarial — assumed the divergence was under-documented or at risk of "correction" back to basic.

---

## Overall Verdict: PASS

The advanced-override divergence is explicitly, coherently documented across all four files with anti-normalization guards. An adversarial reader looking for the gap (where a future maintainer could "correct" troubleshoot back to basic) does NOT find one — every divergence point carries an inline justification and an explicit "MUST NOT be normalized back to basic" guard at the canonical doc.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | MCP_Tavily.md states per-call args override DEFAULT_PARAMETERS + names troubleshoot Tier-2 advanced as intentional/documented | PASS | MCP_Tavily.md:61-80 — dedicated "Per-call override (X3 exception — M4, intentional)" subsection |
| 2 | Troubleshoot SKILL `search_depth: advanced` carries inline justification; ≤2-query cap intact | PASS | troubleshoot SKILL.md:335 (justification + cap inline) + :510 (cap restated in MCP table) |
| 3 | Reflect SKILL inherits basic, names NO per-call params, annotated as inheriting server-level DEFAULT_PARAMETERS (C1) | PASS | reflect SKILL.md:1690 (explicit C1 annotation); grep confirms ZERO per-call `search_depth`/`extract_depth`/`max_results` tokens anywhere in the 1856-line file |
| 4 | RESEARCH_CONFIG.md gates `advanced` to deep/exhaustive only | PASS | RESEARCH_CONFIG.md:66-75 (Depth Profiles table + explicit "ONLY at deep and exhaustive" prose) |
| 5 | Coherence — would an engineer understand WHY troubleshoot=advanced, reflect=basic | PASS | Cross-file story is consistent; reflect:1690 explicitly contrasts itself against the troubleshoot override |

## Summary
- Checks passed: 5 / 5
- Checks failed: 0
- Critical issues: 0
- Important issues: 0
- Minor issues: 0
- Issues fixed in-place: 0 (fix_authorization FALSE)

## Issues Found

None. (Adversarial note below records what was specifically hunted for and not found.)

## Adversarial probe results (what I tried to break)

- **Probe A — "Is the override silently undocumented, so a maintainer normalizes it away?"** NOT FOUND. MCP_Tavily.md:79-80 carries the explicit guard: "These overrides are the documented exception to the `basic` baseline and MUST NOT be normalized back to `basic`." The X3/M4 subsection header itself flags it "(X3 exception — M4, intentional)".
- **Probe B — "Does reflect leak a per-call param that contradicts the basic-inherit claim?"** NOT FOUND. Grep for `search_depth|extract_depth|max_results` across the entire reflect SKILL returns only line 18/19 (`complexity: advanced` metadata — unrelated) and the C1 annotation at 1690. Reflect names zero Tavily call parameters. The only `advanced` tokens are the metadata `complexity: advanced`, not a search depth.
- **Probe C — "Is the troubleshoot cap claimed but not enforced/restated?"** NOT FOUND. Cap appears twice: inline at :335 ("at most 2 queries in this wave" + "≤2-query cap bounds cost") and again in the MCP availability table at :510 ("✓ rate-limited (≤2 queries)"). Consistent.
- **Probe D — "Does RESEARCH_CONFIG gate advanced loosely (e.g., standard tier)?"** NOT FOUND. Table at :66-71 shows quick=basic, standard=basic, deep=advanced, exhaustive=advanced; reinforced by prose at :73-74 "`search_depth: advanced` is used ONLY at the deep and exhaustive tiers; quick and standard stay basic." MCP_Tavily.md:76-77 corroborates ("raises ... at the deep and exhaustive Depth Profiles (see RESEARCH_CONFIG.md)").
- **Probe E — "Is the override mechanism (per-call > server default) asserted only once, fragile?"** NOT FOUND. Asserted in 3 places: MCP_Tavily.md:65-66 + :70-71, and RESEARCH_CONFIG.md:64 ("per-call tool args override the server default"). Mutually reinforcing, not single-point.

## Coherence assessment (Check 5 detail)

The divergence story is internally consistent and an engineer would understand the WHY:
- **Mechanism** is stated once canonically (MCP_Tavily.md DEFAULT_PARAMETERS subsection) and other docs point there rather than restating the baseline value — good SoT discipline, no drift surface.
- **Troubleshoot=advanced** is justified by cost-bounding: "only hard cases reach Tier-2, and the ≤2-query cap bounds cost" (:335). The reader sees both the override AND why it's affordable.
- **Reflect=basic** is justified by contrast: reflect's evidence searches are broad/iterative grounding, not rate-limited hard-case lookups, so it inherits the baseline. Line 1690 explicitly names the troubleshoot override as the counterpoint, closing the loop.
- **Deep-research=advanced** is gated structurally by tier (deep/exhaustive only), a different axis than troubleshoot's per-query override — both documented, no conflation.

## Self-Audit (MANDATORY)

1. **Factual claims independently verified against source:** 5 checks, each tied to a specific file:line confirmed by direct Read and/or Grep — not inferred from another report.
2. **Files read:** All 4 targets fully/relevantly read — MCP_Tavily.md (full, 363 lines), troubleshoot SKILL.md (lines 1-441 covering the load-bearing :335 + targeted grep hit :510), reflect SKILL.md (lines 1-491 + targeted Read of :1683-1694 + full-file grep for params), RESEARCH_CONFIG.md (full, 144 lines). Grep used to prove ABSENCE in reflect (the load-bearing negative for Check 3).
3. **Why trust the 0-issue verdict:** I did not merely confirm presence — I ran 5 adversarial probes (A–E) each targeting a specific failure mode (silent override, param leak, unenforced cap, loose gating, single-point fragility). Each probe cites the exact line that defeats it. The hardest check (reflect names NO per-call params) was verified by a whole-file grep returning zero hits, not by spot-reading.
4. **Web research:** None performed — this lens is entirely local-file-bound (documentation cross-consistency). Tavily-first rule not triggered; nothing to record in Tool-engagement.

## Confidence

Verified: 5/5 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
Tool engagement: Read: 5 | Grep: 4 | Glob: 0 | Bash: 3 (grep wrappers)

## Verified list

- MCP_Tavily.md:61-66 — DEFAULT_PARAMETERS server-level baseline `{"search_depth":"basic","max_results":10}` documented as canonical-in-install_mcp.py.
- MCP_Tavily.md:68-80 — "Per-call override (X3 exception — M4, intentional)" subsection: per-call args override DEFAULT_PARAMETERS; troubleshoot Tier-2 advanced named intentional; deep-research raise named; explicit MUST-NOT-normalize-back-to-basic guard at :79-80.
- troubleshoot SKILL.md:335 — `search_depth: advanced` for error-string query WITH inline justification ("only hard cases reach Tier-2, and the ≤2-query cap bounds cost") + ≤2-query cap.
- troubleshoot SKILL.md:510 — ≤2-query rate-limit cap restated in MCP availability table.
- reflect SKILL.md:1690 — C1 annotation: inherits server-level DEFAULT_PARAMETERS, "reflect passes no per-call overrides (unlike the troubleshoot Tier-2 advanced override)."
- reflect SKILL.md (whole-file grep) — ZERO per-call `search_depth`/`extract_depth`/`max_results` tokens (the load-bearing absence for C1).
- RESEARCH_CONFIG.md:64 — "per-call tool args override the server default."
- RESEARCH_CONFIG.md:66-75 — Depth Profiles: advanced gated to deep/exhaustive ONLY; quick/standard stay basic (table + reinforcing prose).

## QA Complete
