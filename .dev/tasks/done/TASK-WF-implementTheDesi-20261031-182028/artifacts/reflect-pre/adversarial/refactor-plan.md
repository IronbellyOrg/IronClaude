# Refactoring Plan

## Overview
- Base: variant-3-original.md (reviewer-3, opus:refactorer)
- Incorporated: variant-2 (qa), variant-1 (analyzer), invariant-probe.md
- Output: merged-verdict.yaml (one merged finding list for sc:reflect)
- Overall risk: Low (additive findings list)

## Planned Changes

1. Reclassify per debate: R3-F2 -> gap/medium (X-002); withdraw R3-F7 (merged into R1-6 equality test, refinement/low); X-001 stays drift/medium with INV-009 key-presence semantics added; C-006 rereview_requested{reviewer} medium, other events low.
2. Add invariant probe items INV-001 (HIGH: Codex completion = max(marker updated_at, Codex review submitted_at) + fixture with root createdAt > marker time), INV-002 (HIGH: absent set is an input to the wait outcomes), INV-003 (watermark persisted on rereview_requested), INV-004 (Augment-silent path continues with Codex in SKILL step 3, Wave 8 arming, Error Handling), INV-005 (newest valid Codex marker wins), INV-006 (resume reuses the dangling cycle_id), and LOW INV-007, INV-008, INV-011.
3. Add V2 obligations: R2-01+R2-03+R2-04+R2-09 as one C-008 finding (medium: Wave 6 reply/resolve each verified member, group max tier, fix_applied per member, flagged-by); R2-02+R2-07 (C-009, medium); R2-06 (medium); R2-08 (low); R2-13 (low).
4. Add V1 items: R1-2 (medium: tests for Tasks 7-9 live in Task 10; dry check best-effort with recorded fallback), R1-9 (low), R1-5 merged into C-005 with models.py:211-212 (low), R1-8/R3-F8 merged (low).
5. X-004: keep V3 location; add V3's Round-2 test design (fixture: augment rereview_requested only -> resolve_crash_window S5, pending_retriggers ["codex"]) and Task 12 grep.

## Changes NOT Being Made
- R1-3 recovery.py change: rejected (design:277 keeps the rule; recovery.py:60-80 never sees the post-push crash).
- R2-01 high severity: rejected (SKILL.md:196 per-thread reply exists) -> medium.
- R2-11 "record toward empty": rejected in favour of X-001 fallback.

## Review Status
- Auto-approved (non-interactive), 2026-10-31.
