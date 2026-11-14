# Refactoring Plan: Q15

## Overview
- Base: Variant 2 (proposal-B)
- Changes planned: 4. Overall risk: Low

## Planned Changes
1. **Coordinator decides worker corrections.** Source: A-001 consensus (advocates V1, V2). Target: "Answer". Approach: replace "corrections for workers go through the coordinator's pulled follow-ups" with "v2 hands a worker correction to the coordinator, which decides whether to send a WC-12 follow-up; v2 never sends one itself". Risk: Low.
2. **Reopening condition.** Source: Variant 1 weakness critique and advocates V1, V2 unassigned picks. Target: "What happens next" and "What stays unresolved". Approach: append: the question is reopened only when a delivery channel is named, a threat model for poisoned content exists, it is decided whether a person approves each correction, and Q16 is answered. Risk: Low.
3. **Unattended sessions named.** Source: Variant 3 U-003. Target: "What it costs or risks". Approach: replace the generic bullet with a named open case. Risk: Low.
4. **Design for later without building it.** Source: advocate V3 unassigned pick. Target: "What happens next". Approach: append: V2-03 shapes the typed fields and audit record so a later delivery release would not force a store migration; no delivery path is designed. Risk: Low.

## Changes NOT Being Made
- Variant 1's standing rule for "any later automated program": rejected (X-002, unanimous: do not bind unresearched designs). Its contract-adjacent sentence is kept only as an optional later PR.
- Variant 3's delivery goal and SW-12 on v2's path: rejected (C-003, X-003).

## Review Status
Auto-approved, 2026-11-14.
