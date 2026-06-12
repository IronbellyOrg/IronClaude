# OI-5 — Human-Decision PENDING Marker

**STATUS: PENDING HUMAN DECISION**

**Date:** 2026-06-11
**Spec source:** RELEASE-SPEC v1.1.0 §11 (Open Items) OI-5.

## Verbatim OI-5 question (spec §11)

> OI-5 — `target_release` exact version (proposed 4.3.0) — Low — G1 approval.

**Proposed value:** `4.3.0`

## Binding instruction (applies to ALL authored artifacts)

**No authored artifact may stamp a `target_release` version until OI-5 is resolved.**

CRITICAL DISTINCTION — do NOT conflate two different version concepts:
- `contract_version` — the **output-contract semver**, default `1.0.0` per §5.5. This IS authored (in `hardening-output-contract.md` and the SKILL.md Output Contract). It is the contract field's own version, NOT the release version.
- `target_release` — the **release version** this work ships in (proposed `4.3.0`). This is OI-5 and is **PENDING**. Do NOT auto-default a `target_release` stamp into any ref, SKILL.md, command, or test.

## Resolution state

G1 implementation approval was granted (2026-06-11). The §11 table marks OI-5's resolution target as "G1 approval," but **no explicit `target_release` version was supplied with the approval**. Therefore OI-5 remains **PENDING** and no `target_release` is stamped. `contract_version: 1.0.0` is authored normally (distinct field, not gated by OI-5). If/when the operator names the release version, stamp it then.
