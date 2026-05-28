# Merge Log — feature-flag-system

| # | Source | Adopted Element | Target Section | Notes |
|---|--------|-----------------|----------------|-------|
| 1 | sonnet (base) | YAML flag store + watcher | Storage / Runtime | Base architecture |
| 2 | sonnet (base) | Pydantic schema enforcement | Schema | Base architecture |
| 3 | sonnet (base) | Atomic-write CLI mutator | CLI | Base architecture |
| 4 | opus | OpenFeature SDK conformance | SDK | Layered; conformance subset |
| 5 | opus | Provider abstract base | Provider | Layered; enables v2 migration |
| 6 | opus | Kill-switch fast-poll (1s) | Kill switch | Layered; v1 path |
| 7 | opus (v2) | Postgres-backed provider | Deferred | Out of v1 scope |
| 8 | opus (v2) | FastAPI control plane | Deferred | Out of v1 scope |
| 9 | haiku | Signed manifest verification | Trust model | Layered; scoped to prod env |
| 10 | haiku | Hash-chained JSONL audit log | Audit | Layered |
| 11 | haiku | `sensitive: true` metadata + HMAC bucketing | Bucketing | Layered; opt-in per flag |
| 12 | haiku | Two-person review for prod+sensitive | Governance | Layered; scoped |
| 13 | haiku | Fail-closed on cold start | Failure modes | Layered |
| 14 | haiku (v2) | Per-flag RBAC namespacing | Deferred | Out of v1 scope |

## Adoption Summary

- 3 base elements from sonnet.
- 3 layered elements from opus (v1) + 2 deferred to v2.
- 5 layered elements from haiku (v1) + 1 deferred to v2.
- 0 elements dropped without explanation; all proposal content
  either layered or explicitly deferred with v1/v2 boundary.
