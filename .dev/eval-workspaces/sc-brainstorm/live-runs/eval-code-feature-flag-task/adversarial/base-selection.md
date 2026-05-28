# Base Selection — feature-flag-system

## Scoring (Round 3 convergence-weighted)

| Criterion | Weight | opus/architect | sonnet/backend | haiku/security |
|-----------|--------|----------------|----------------|----------------|
| Operational simplicity (v1) | 0.25 | 2 | 5 | 3 |
| Sub-ms eval performance | 0.15 | 4 | 5 | 3 |
| OpenFeature compat | 0.15 | 5 | 4 | 4 |
| Audit / governance | 0.20 | 3 | 3 | 5 |
| Migration seam to v2 | 0.10 | 5 | 4 | 4 |
| Fail-mode rigor | 0.15 | 4 | 4 | 5 |
| **Weighted total** | 1.00 | **3.55** | **4.20** | **3.90** |

## Selected Base

**sonnet/backend** — highest weighted score (4.20).

Rationale:

- File-based store + watcher matches the v1/v2 scope split from
  debate Round 3.
- Operational simplicity dominates at v1 (one moving part vs four).
- Sub-ms eval is trivial in this design (dict lookup).
- OpenFeature-compat is preserved via the shim layer.
- Migration to opus's Postgres design is clean: swap the loader, keep
  the evaluator + SDK + audit log unchanged.

## Layered Adoptions

The following components from non-base variants are layered onto the
base in the merge:

- From **haiku/security**:
  - Signed manifest (`flags.yaml.sig`) verified at load.
  - Hash-chained JSONL audit log.
  - `sensitive: true` per-flag metadata with HMAC bucketing.
  - Two-person review gate for `prod` + `sensitive=true` flags.
  - Fail-closed-on-create state machine.

- From **opus/architect**:
  - OpenFeature SDK conformance subset (boolean + string + object).
  - Background poller pattern (adapted: file watcher in v1, HTTP
    poller in v2).
  - Migration-seam interface (`Provider` abstract base) so v2 can
    swap the file loader for a remote-fetch loader.
  - Kill-switch fast-poll path (1s) separate from general 10s
    propagation.
