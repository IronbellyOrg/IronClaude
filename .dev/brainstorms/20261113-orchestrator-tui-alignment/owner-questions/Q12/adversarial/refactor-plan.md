# Refactoring Plan: Q12

## Overview
- Base: Variant 3 (proposal-C)
- Changes planned: 4. Overall risk: Low

## Planned Changes
1. **Name the routing table.** Source: advocates V2 and V3 (C-002, C-005). Target: base "Answer" and "What happens next". Approach: replace "which table" with "the routing table", and record that the other-commands table cannot take it without changing its pinned member list (test :297-298). Risk: Low.
2. **Test edits only if a run shows they are needed.** Source: advocate V3 strength 2, orchestrator spot-check (test :105, :336-340; HOW-WE-WORK.md:376 precedent). Target: base "What happens next" and "What it costs or risks". Approach: replace "at least one routing test must change" with "run the routing tests first; name any edit they force". Risk: Low.
3. **Describe only what works on master.** Source: Variant 1 U-001. Target: "What happens next". Approach: append. Risk: Low.
4. **Person only, twice.** Source: Variant 2 U-003 and the existing `/sc:sweep` pattern (HOW-WE-WORK.md:335). Target: "What happens next". Approach: append (notes cell, plus an optional one-line pointer beside the never-as-worker bullet, HOW-WE-WORK.md:405). Risk: Low.

## Changes NOT Being Made
- Variant 1's deferral: rejected; no advocate picked it unassigned, and the tool is merged with no mention anywhere (C-001).
- Variant 2's placement as the only entry: rejected; not routable (SKILL.md:50-54, C-005 unanimous).
- Variant 2's rewrite of OB-07: rejected (X-003).

## Risk Summary
All additive wording on the answer; rollback is deleting it.

## Review Status
Auto-approved, 2026-11-14.
