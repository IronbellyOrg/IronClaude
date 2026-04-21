# Refactoring Plan: Merged Compression Strategy

## Overview
- **Base variant:** Position C (Normalized Table Format)
- **Incorporated from:** Position A (machine-readable format, prose summaries)
- **Incorporated from:** Position B (post-compression hash enhancement)
- **Total changes planned:** 4
- **Changes rejected:** 2
- **Overall risk:** Low

---

## Planned Changes

### Change #1: Adopt YAML over TSV for output format
- **Source:** Position A (S-001)
- **Target:** Replace Position C's TSV format with YAML structured output
- **Rationale:** YAML is both human-readable and machine-parseable. TSV requires escaping for fields containing tabs/commas. YAML handles nested structures (AC tags as arrays) natively. Debate evidence: A's YAML format won on programmatic consumption (S-001 partial win).
- **Integration:** Use YAML list-of-dicts for task rows instead of TSV. Preserve all C's columns.
- **Risk:** Low u2014 format change only, no data loss

### Change #2: Add one-line prose summaries for narrative sections
- **Source:** Position A (S-004)
- **Target:** Enhance Position C's metadata header
- **Rationale:** C's metadata header compresses executive summary to a single line. A's approach adds one-line summaries per narrative section (risks, resources, timeline), providing better contextual signal for deef. Debate evidence: S-004 won by C but A's summaries are additive.
- **Integration:** Add `summary` field to each metadata section (exec_summary, risk_summary, resource_summary, timeline_summary)
- **Risk:** Low u2014 adds ~200 bytes per file, well within compression budget

### Change #3: Implement controlled vocabulary for AC tag normalization
- **Source:** Debate round 2 (C's own concession on X-004)
- **Target:** Address the unbounded vocabulary problem
- **Rationale:** C conceded that naive AC extraction creates vocabulary drift. A bounded normalization dictionary of ~30-50 canonical terms covers 90%+ of auth-domain AC content. This is the key mitigation that makes C viable.
- **Implementation:** Define canonical tag vocabulary for common auth concepts: `valid-creds`, `invalid-creds`, `no-enum`, `lockout`, `rate-limit`, `bcrypt`, `rs256`, `jwt`, `ttl`, `redis`, `postgres`, etc.
- **Risk:** Medium u2014 requires domain-specific vocabulary, but auth domain is well-bounded

### Change #4: Add post-compression chunk hashes (optional enhancement)
- **Source:** Position B (Round 2 constructive contribution)
- **Target:** Optional enhancement layer after compression
- **Rationale:** After both files are compressed, compute section-level hashes. Append a hash manifest to each compressed file. Deef can use hash matches to skip identical sections.
- **Integration:** Add `chunk_hashes` section at end of compressed file
- **Risk:** Low u2014 purely additive, ~100 bytes

---

## Changes NOT Being Made

### Rejected: Strip AC entirely (Position A's core approach)
- **Rationale:** Debate evidence (C-001, X-001) shows AC differences are a primary source of meaningful roadmap divergence. Stripping them creates false negatives that undermine merge decision quality. The 10% extra compression is not worth the information loss.

### Rejected: Pre-comparison hash dedup (Position B's core approach)
- **Rationale:** Violates independence requirement (S-003, X-002). Achieves <5% compression on different-model outputs (C-004, C-005). Position B self-eliminated.

---

## Review Status
- Approval: auto-approved
- Timestamp: 2026-04-15
