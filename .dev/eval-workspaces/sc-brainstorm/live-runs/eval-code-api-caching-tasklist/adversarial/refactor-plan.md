# Refactor Plan

## Overview

- Base variant: Variant 2 (backend:sonnet)
- Incorporated variants: Variant 1 (architect:opus), Variant 3 (security:haiku)
- Planned changes: 6
- Review status: auto-approved

## Planned Changes

1. **Add policy registry as control plane**
   - Source: Variant 1
   - Target: Functional requirements
   - Approach: Insert requirements for endpoint cache-policy registry and policy versioning.
   - Risk: Low

2. **Adopt deny-by-default eligibility posture**
   - Source: Variant 3
   - Target: Eligibility and security requirements
   - Approach: Replace broad approved-GET wording with classification-first approval.
   - Risk: Medium

3. **Expand cache key requirements**
   - Source: Variants 1 and 3
   - Target: Functional/security requirements
   - Approach: Require route, params, query, version, tenant, authorization, content negotiation, and feature-flag dimensions.
   - Risk: Low

4. **Qualify stale-if-error behavior**
   - Source: Variants 2 and 3
   - Target: Resilience requirements
   - Approach: Allow only for approved bounded-staleness endpoints and forbid for revocation-sensitive/sensitive responses.
   - Risk: Medium

5. **Merge observability and auditability**
   - Source: all variants
   - Target: Non-functional requirements
   - Approach: Combine performance metrics, fallback metrics, invalidation telemetry, and audit logs.
   - Risk: Low

6. **Add tasklist-ready acceptance criteria and open questions**
   - Source: seed brief plus all variants
   - Target: Final merged requirements
   - Approach: Make implementation planning explicit without choosing vendor/framework.
   - Risk: Low

## Changes Not Being Made

- No specific cache backend is selected; this belongs in design or implementation planning.
- No API contract changes are introduced; existing behavior must remain compatible.
- No write-endpoint caching is introduced by default.

## Risk Summary

Primary risks are security leakage, stale data after mutation, and operational fragility under cache outage. The merged requirements mitigate these with deny-by-default classification, key-dimension tests, event-driven invalidation, origin fallback, stampede protection, and auditability.
