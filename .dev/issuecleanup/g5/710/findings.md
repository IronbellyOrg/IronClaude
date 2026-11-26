## Verdict
**still-relevant.** Issue [#710](https://github.com/IronbellyOrg/IronClaude/issues/710), credential allowance visibility and explicit account routing, is OPEN with no comments as read on 2026-11-24. The reviewed checkout is `a7ae3dd30fcf88aaab655c37e94e58e121c2d863`. The current proxy selects models rather than credential accounts: `src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py:839-847` iterates model slots and rewrites the model field. Lines 603-608 forward generic headers and lines 783-812 send the upstream request; neither demonstrates a recognized account selector.

No quota/reset reader, credential-listing command or explicit credential-selector implementation was found in the package inventory and source searches. The source-wide search for `auth_index|CPAMP|CPA.Manager|weekly.*(quota|reset)|credential.selection` returned no matches; the package search for `quota|auth_index|reset|credential` found usage-error handling, redaction and unrelated reset text, not the requested feature. These negative results are bounded source evidence, not proof that no unlinked implementation exists elsewhere. The quick analysis is in `.dev/issuecleanup/g5/710/analyze/analyze-report.md`.

Merged PR [#738](https://github.com/IronbellyOrg/IronClaude/pull/738), image-related model fallback, produced commit `720cbaf96653c1c983497ba480f76ca6e60e5369` and touches this proxy, but does not supply allowance reporting or account selection. No implementation PR is identified by the issue. UNVERIFIED: deployed CPA/CPA Manager Plus quota/reset APIs, provider coverage, authentication requirements, credential selection, actual account used and concurrent live behavior. No gateway contact or test execution was performed. Nothing in the evidence warrants closing or marking the feature actively in progress.

## Complexity and size
**Complexity: complex. Size: L.** The full issue combines external-interface experiments, provider-specific quota/reset interpretation, account-level routing across launcher/proxy/gateway boundaries, concurrent-session isolation, failover compatibility and secret-safe tests; it is not a small model-picker change. This is an estimate of the full requested scope, not just the first experiment; exact effort remains UNVERIFIED until the external interfaces are established.

## Priority
**P2.** This is planned capacity-use improvement: unused allowance may expire, but the live issue supplies no failing command, blocked delivery, data loss or exposed secret that establishes P0/P1 urgency. No dependent issue or release blocker was verified.

## Concrete next steps
1. First run authorized, sanitized experiments against the account-management and gateway interfaces. Record authentication requirements without values, actual provider coverage, quota units, response freshness, missing versus zero data, reset timezone and a documented look-ahead window. The issue's proposed endpoint/header forms are hypotheses, not supported interfaces.
2. Independently prove explicit account selection through the configured ccsession upstream, not merely a direct CPA request. Obtain gateway-side non-secret evidence of the account used across repeated requests and model retries; choosing a model or receiving a successful response is insufficient.
3. Settle invalid, unsupported and exhausted-selection behavior before building: an explicit selection must fail visibly instead of silently switching accounts. Verify concurrent different selections and no-selection behavior, including launch/resume, streaming, tier access and discovery.
4. Only if the experiments establish support, build the quota reader and the smallest explicit-selection route in the existing ccsession package. Process-scoped selection would need inclusion in shim identity/reuse checks; a request-scoped route needs demonstrated per-request isolation. Keep authentication environment-based, identifiers non-secret and defaults gateway-neutral. If either capability is unavailable, record the external blocker instead of inventing a selector.
5. Add quota-boundary/unknown-data tests and account-selection forwarding, concurrency, failover and launch/resume regression tests; preserve the existing no-personal-routing safeguard. Run the issue's regression and sync gates in an authorized implementation run, not this read-only review. Automatic reset-aware scheduling inside CPA remains outside this issue's required build.

## Dependencies
**Needs:** no numbered prerequisite issue was identified in the issue body/comments or related searches. The real external prerequisites are a usable quota/reset interface and a verified account-selection mechanism through the deployed gateway; both remain UNVERIFIED. Authorized access to eligible accounts and account-level gateway evidence is needed for the live acceptance checks.

**Blocks:** no numbered dependent issue was verified. Automatic reset-aware selection is explicitly not a prerequisite.

## Related issues
None verified. Read-only issue searches for `CPA` and `quota credential reset` found #710 itself; the `CPA` search also returned unrelated branch-protection issue #702, which is not treated as a dependency or substantive relation. The issue body says related issues/PRs are not known and its comments list is empty.

## Related PRs
- [#738](https://github.com/IronbellyOrg/IronClaude/pull/738), merged image-related model fallback, is adjacent work in the same proxy, not an implementation of #710. Its body, files, comments, reviews and merge metadata were read. Merge commit: `720cbaf96653c1c983497ba480f76ca6e60e5369`.
- No PR is linked or numbered in #710. Read-only PR searches for `CPA` and `credential quota` returned none. Searches for `710` and `"#710"` returned #637, #110 and #120 because their bodies mention numeric test counts; their returned titles/bodies establish they concern review labels, roadmap scanning and sprint execution, not credential allowance or selection. No implementation relation is inferred.
- UNVERIFIED: unlinked work on other branches or PRs outside these bounded searches. All GitHub operations in this review were issue/PR reads; no labels, comments, closure, linkage or other outward changes were made.
