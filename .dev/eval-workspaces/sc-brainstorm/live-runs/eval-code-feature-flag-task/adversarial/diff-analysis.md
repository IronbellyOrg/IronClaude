# Diff Analysis — feature-flag-system

## Pairwise Conflicts

### opus vs sonnet

- **Storage**: Postgres (opus) vs YAML file (sonnet). Resolved → YAML
  file v1, Postgres v2.
- **Control plane**: FastAPI service (opus) vs CLI-only (sonnet).
  Resolved → CLI-only v1, optional service v2.
- **Propagation**: 10s poll (opus) vs inotify (sonnet). Resolved →
  inotify primary, 1s fast-poll for kill switches.

### opus vs haiku

- **Audit log**: Postgres table (opus) vs hash-chained JSONL (haiku).
  Resolved → hash-chained JSONL.
- **Bucketing**: MurmurHash (opus) vs HMAC-SHA256 (haiku). Resolved →
  SHA256 default, HMAC for sensitive.
- **Flag creation flow**: direct write (opus) vs two-person review
  (haiku). Resolved → two-person for prod + sensitive only.

### sonnet vs haiku

- **Trust model**: filesystem-trusted (sonnet) vs signed manifest
  (haiku). Resolved → signed manifest for prod environment.
- **Audit storage**: JSONL (both) — agreement; haiku adds hash chain.

## Pairwise Shared Ground

- All three: OpenFeature SDK boundary.
- All three: sub-ms eval via in-memory map.
- All three: sticky bucketing required.
- All three: fail-closed default when store unavailable.
- opus + sonnet: kill switch needs faster path than general flag poll.
- sonnet + haiku: append-only audit log on filesystem.

## Conflict-to-Resolution Density

- Total pairwise conflicts: 8
- Resolved with clean v1/v2 split: 6
- Resolved with opt-in metadata: 2 (bucketing, two-person review)
- Unresolved post-merge: 0
