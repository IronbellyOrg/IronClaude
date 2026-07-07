# Refactoring Plan

## Overview
- **Base:** Variant 1 (qwen3.6-plus) — cleaner, complete scaffold.
- **Incorporating from:** glm-5.2 (C2, I1, I4, test_cli_smoke sharpening) + adjudicator evidence (A-001/A-002, git verification).
- **Change count:** 8 planned changes, 2 rejected.
- **Overall risk:** Low (audit-document merge; no code touched).

## Planned Changes

| # | Title | Source | Target in base | Approach | Rationale (evidence) | Risk |
|---|-------|--------|----------------|----------|----------------------|------|
| 1 | Downgrade terminal-gate headline | Adjudicator A-001/A-002 | qwen Finding 1 → AUD-1 | restructure | This run IS the POST gate (path + return-contract `recommended_next_command`); status "Doing" is correct in-progress. INV-001. | Low |
| 2 | Add verification-round-skip finding | glm C2 (CONFIRMED) | New AUD-2 (IMPORTANT/HIGH) | insert | `qa-final-verification-{structural,content}.md` absent; 6.G9 FAIL→6.G10 fix→6.G11 required. Logged falsely "None material." | Low |
| 3 | Merge test-count drift (both axes) | qwen F3 + glm I2 | AUD-3 | replace | qwen owns 6/7/8; glm adds `test_cli_smoke.py` + "no authorizing Step." | Low |
| 4 | Add aienv.py scope-drift finding | glm I1 (CONFIRMED) | New AUD-4 (MINOR) | insert | Diffs 1 line vs start_commit; outside §10. | Low |
| 5 | Resolve additive-only as VERIFIED | qwen F4 + git | AUD-5 | replace | `contract.py`+`swarm/models.py` 0-diff CONFIRMED. Flip from "unverified" to "satisfied." | Low |
| 6 | Add xpass follow-up | glm I4 | New AUD-6 (MINOR) | insert | `1 xpassed` uninvestigated. | Low |
| 7 | Reframe `make sync-dev` as WARN | glm I5 (rejects qwen F2) | AUD-7 | replace | L130 prohibits *staging*, not *running* sync-dev; "nothing staged." X-001. | Low |
| 8 | Downgrade coverage/tcs to LOW | Adjudicator (rejects glm C3) | AUD-8 | replace | PRE-reflect provenance field, note explains 46/46; "fabricated" unsupported. | Low |

## Changes NOT Being Made (rejected alternatives)

| Diff point | Rejected approach | Rationale |
|------------|-------------------|-----------|
| C-001 | Keep glm's hard `FAIL — internally contradictory` / qwen `return to executor` | Rejected — A-001 falsifies the premise; the correct verdict is CONTINUE (the POST gate is running). |
| X-001 | Keep qwen's "Procedural Constraint **Violation**" (🟠) | Rejected — misreads L130; adopt glm's WARN. |
| C-006 | Keep glm's "coverage number is **fabricated**" (CRITICAL) | Rejected — over-reach on a PRE-reflect field the executor did not author. |
| — | Preserve qwen's suspect-source table + scoring weights | KEPT verbatim (base strength; U-004). |

## Review Status
Auto-approved (non-interactive). Timestamp: 2026-07-07.
