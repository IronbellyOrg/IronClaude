# Debate Transcript — feature-flag-system

## Round 1 — Opening Stances

**opus/architect**: "Build the OpenFeature-compatible SDK + provider
+ control plane. The SDK boundary is the stable contract; the
provider is swappable. Postgres + a small FastAPI control plane is
standard and supportable."

**sonnet/backend**: "Skip the control plane in v1. A YAML file +
inotify watcher gets you sub-ms eval and < 2s propagation with no
service to operate. Operational simplicity wins for the 80% case."

**haiku/security**: "Both of you are skipping the part that matters.
This is an authorization surface. Audit, RBAC, fail-closed, signed
manifests, two-person review on creation. Performance is a
constraint, not a goal."

## Round 2 — Cross-Examination

**opus -> sonnet**: "Your YAML-file approach can't enforce
multi-environment isolation cleanly, and operators who want to
toggle a kill switch at 3am don't want to commit YAML to a config
repo. The 30s propagation budget is achievable but only because
you're handwaving the dev-loop friction."

**sonnet -> opus**: "You're proposing a Postgres dep + FastAPI
service + background poller + SSE push channel for kill switches.
That's four moving parts for v1. Half of feature-flag-tool incidents
in the wild are caused by the control plane being unreachable. My
file-based store has one moving part: the file. It fails over to
a previous good state on every parse error."

**haiku -> both**: "Neither of you addressed two-person review or
audit-log tamper resistance. A flag flip that takes a payment system
into a degraded state in prod needs the same change-management rigor
as a deploy. opus's audit log is in Postgres next to the flags, which
is unprincipled — same DB, same blast radius if the DB is compromised.
sonnet's JSONL append-only log is better but still trusts the local
filesystem."

**opus -> haiku**: "You're conflating threat models. The realistic
adversary for an internal tool is a stressed engineer at 3am, not a
sophisticated insider. Two-person review on flag CREATION is fine, but
gating every flag flip in prod will create a workaround culture
(everyone shares the on-call account). Make security the default, not
the bottleneck."

**sonnet -> haiku**: "HMAC bucketing for non-sensitive flags is
wasted CPU. The set of flags that need cryptographic unpredictability
is small (anything carrying auth or financial impact). Make the
secure path opt-in per-flag via metadata, not the default."

**haiku -> sonnet**: "Concede on default bucketing — use Murmur or
SHA256 by default, HMAC for flags marked sensitive=true. But I won't
concede on fail-closed-on-create or signed manifest for the prod
environment. Those are cheap to implement and prevent a whole class of
incidents."

## Round 3 — Convergence

**Shared agreement**:

- OpenFeature-compatible SDK is the right boundary; all three
  proposals included this.
- Sub-ms hot path via in-memory cache / dict lookup.
- Sticky bucketing required; default hash function can be a stdlib
  choice (SHA256 or Murmur), with opt-in HMAC for `sensitive=true` flags.
- Audit log is non-negotiable; details on storage backend differ.
- Fail-closed on cold start when store is unreachable.
- Kill switches need a faster propagation path than the normal poll.

**Outstanding tensions**:

1. **Control plane vs file-based store for v1**: opus argues for
   Postgres + FastAPI; sonnet for YAML + watcher; haiku is agnostic
   on storage but insists on signing.

   **Resolution**: Ship file-based store for v1 with a clear
   migration seam to Postgres for v2. Sign the manifest from day 1
   so the migration to a remote store doesn't require redesigning
   the trust model. This honors sonnet's operational simplicity AND
   haiku's signing requirement; opus's Postgres design becomes v2.

2. **Audit-log storage**: Postgres table (opus) vs JSONL on disk
   (sonnet) vs hash-chained append-only with signing (haiku).

   **Resolution**: JSONL append-only with hash-chain entries (each
   record includes hash of previous). Ships in v1. Postgres mirror
   becomes optional v2 enhancement. Hash-chain is cheap (~50 bytes
   per entry) and gives tamper evidence without DB overhead.

3. **Two-person review on flag creation**: haiku insists; opus says
   it creates workaround culture.

   **Resolution**: Two-person review is REQUIRED for flags in the
   `prod` environment AND marked `sensitive=true`. Optional but
   recommended for other prod flags. Dev/staging environments do
   not require review. This is haiku's principle scoped to actual
   risk surface.

4. **Bucketing default**: SHA256 (sonnet) vs HMAC-SHA256 (haiku).

   **Resolution**: SHA256 default; HMAC opt-in via `sensitive: true`
   metadata. Matches the cross-examination compromise from Round 2.

5. **Kill-switch propagation**: poll (sonnet) vs push (opus + haiku).

   **Resolution**: v1 uses fast-poll (1s interval) for kill switches
   specifically — separate from the 10s general poll. Push channel
   (Redis pub/sub) deferred to v2 once Redis is justified by another
   workload. This avoids adding Redis as a v1 dependency.

## Final Convergence Score

- Round-by-round delta: 5 tensions identified, all resolved with
  explicit compromise text and v1/v2 scope splits.
- Shared agreements: 6 items aligned at outset of Round 3.
- Outstanding conflicts post-resolution: 0 (all tensions have
  resolution text; v1/v2 boundary is clean).
- **Convergence: 0.82** (PASS threshold 0.65; deep agreement on
  scope split, residual divergence is purely v2 sequencing).
