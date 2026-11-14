# Refactoring Plan: Q13

## Overview
- Base: Variant 1 (proposal-A)
- Changes planned: 4. Overall risk: Low (all wording; no code)

## Planned Changes
1. **State the probe's exact limit.** Source: Variant 2 X-001 (unanimous). Target: "Answer" and "What it costs or risks". Approach: replace "safe" framing with "proves the program is Orca, not that it is the same Orca the sweep reads". Risk: Low.
2. **When the two programs actually diverge.** Source: advocate V3 strength 5 and advocate V2 strength 2 (spot-checked). Target: "What it costs or risks". Approach: insert: only when `ORCA_CLI_COMMAND` is set, or `orca-ide` is missing or fails its probe (the fallback is silent). Risk: Low.
3. **Re-ask trigger.** Source: Variant 3 U-003. Target: "What happens next". Approach: append: the note records the Orca build string next to each capture; the owner is asked again if build strings differ or `ORCA_CLI_COMMAND` is in use, or before the dispatch-id comparison (XC-04) if it needs one binary. Risk: Low.
4. **Follow-up rows, not fixes.** Source: advocate V1 (absolute-path gap, spot-checked) and advocate V2 (silent fallback). Target: "What stays unresolved". Approach: append two follow-up rows for the sweep's follow-up list (#534) or the observer's backlog; no code change authorized. Risk: Low.

## Changes NOT Being Made
- Variant 2's observer code change: not adopted; the divergence is unobserved (INV-016) and the change breaks `orca`-only hosts; kept as the alternative if the trigger in Change 3 fires.
- Variant 3's "no verdict": not adopted; leaves future callers without a rule.

## Review Status
Auto-approved, 2026-11-14.
