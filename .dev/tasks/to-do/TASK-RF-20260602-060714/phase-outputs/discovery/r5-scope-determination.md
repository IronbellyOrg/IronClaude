# R5 Path-(b) Scope Determination

**Captured:** 2026-06-02 07:00
**Decision input:** evidence from `r5-reproduction.md` + PR #111 oracle at commit `861047c2`

## The Question
Does adding the MD family (+ canonicalizer + trailing-D dedup) ALONE close the FP, or is PR #111's separate **Explicit non-references allowlist** subsystem also required for path (b)?

## Evidence

### From the reproduction (Phase 2.3)
The minimal reproduced FP — milestone deliverables (`M1-D02`, `M2-D03`) mis-tokenized as bare-`D` phantoms — is closeable by the **MD family + canonicalizer + trailing-D dedup** alone: once `M1-D02` tokenizes as MD `M1-D02` (not bare `D02`) and the bare-`D` trailing portion is stripped, those two HIGH phantom_id FPs disappear. No allowlist needed for *that minimal shape*.

### From PR #111's oracle (the mandatory port target — `git show 861047c2 -- tests/roadmap/test_structural_checkers.py`)
PR #111 shipped THREE MD oracle tests (path-b acceptance requires porting all three):

| Oracle test | Fixture helper | Requires allowlist? | Status on current branch |
|---|---|---|---|
| `test_phantom_id_honors_explicit_non_references_for_milestone_d_ids` ("canonical v1-MVP bug-trigger shape") | `_write_md_fixture_with_allowlist` | **YES** — roadmap body carries `M{n}-D{nn}` IDs **AND** bare `D01..D05` as roadmap-internal indices, exempted by the `**Explicit non-references (do not resolve against spec):**` annotation. Expects 0 signatures findings. | Would FAIL (no MD family, no allowlist) |
| `test_phantom_id_backward_compatible_without_explicit_non_references` | `_write_id_fixture` (plain) | No | Already PASSES (legacy canonicalization → 3 MEDIUM drift) |
| `test_phantom_id_bare_d_still_resolves_when_spec_uses_bare_d` | `_write_id_fixture` (plain) | No | Already PASSES (D9 → 1 HIGH phantom) |

The first oracle test is the canonical real-world incident shape: a roadmap that legitimately references both milestone IDs (`M1-D01`) **and** the bare deliverable-sequence indices (`D01..D05`) as roadmap-internal annotations. The MD family alone canonicalizes `M1-D01 != M2-D01` distinctly, but it does NOT exempt the *standalone* bare-`D` `D01..D05` tokens the roadmap text also contains — only the Explicit-non-references allowlist does. Without the allowlist, those standalone bare-D tokens remain HIGH phantom_id FPs and the test fails.

## Recommendation: **MD-FAMILY-PLUS-ALLOWLIST**

**Rationale:**
1. **The mandatory oracle port requires it.** Path-b acceptance (design doc R5) requires porting PR #111's 3 oracle tests to green. Oracle test #1 — the canonical bug-trigger shape — structurally depends on the Explicit non-references allowlist; it cannot pass with the MD family alone.
2. **It is the realistic incident shape, not a speculative addition.** PR #111's 51-HIGH incident came from roadmaps that carry both milestone IDs and roadmap-internal bare-`D` indices. The allowlist is part of the proven, reviewed fix for exactly that shape — porting it whole is lower-risk than cherry-picking a subset that leaves the canonical case unaddressed.
3. **The minimal reproduction (MD-only-closeable) is a strict subset** of what the full oracle exercises; choosing the broader scope closes both the minimal FP and the canonical incident shape, with no regression to the already-passing backward-compat / bare-D tests.

**Carried into Phase 3:** `decision: PROCEED`, `scope: MD-FAMILY-PLUS-ALLOWLIST`. Phase 4 item 4.4 (allowlist port) is therefore IN scope (not skipped), and the ported oracle (item 4.12) must include all 3 MD tests + the `_write_md_fixture_with_allowlist` helper.
