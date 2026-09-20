# Diagnosability Tasklist

**Verdict**: insufficient; **Complexity**: non-trivial; **Round**: 1/3.
**Status**: evidence requirements only; no verified executable instrumentation patch. No CI dispatch or unchanged collector rerun requested.

## Hard constraints

Invocation sites only; additive, reversible changes only. Never alter production startup/askpass logic, ownership checks, deadlines, auth behavior or cleanup to obtain evidence. No shell xtrace, verbose credential transport, raw syscall/stdout/stderr/environment dumps, or bulk artifact upload. Any future instrumentation addition must carry `# Diagnosability-tasklist instrumentation: revert after defect closed.` Separate implementation authorization remains valid; no new approval gate is introduced.

## 1. Retain the original T51 invocation's typed failure evidence

- Invocation site: `/config/workspace/Coder/.claude/worktrees/sysbox-retry-astra/.github/workflows/coder-ci-validate.yml`, pre-live self-test step and its artifact-retention boundary.
- Current code: `if ! bash .github/contract-tests/test-51-selector-onboarding-wiring.sh >/dev/null 2>&1; then`.
- Existing producer: `/config/workspace/Coder/.claude/worktrees/sysbox-retry-astra/.github/contract-tests/test-51-selector-onboarding-wiring.sh` defaults RESULT_FILE to `artifacts/test-51-evidence/test-51-selector-onboarding-wiring.txt`; `_row` records status/name/detail and EXIT finalization copies the scratch rows and appends counts.
- Additive requirement, not supplied code: an invocation-bound, allowlisted projection of failed fixture identifiers/status and safe expected/observed values, finalizer summary or explicit missing-record state, original exit status, source SHA and matrix/run identity; retain only that projection through an always-run upload. Do not expose arbitrary detail fields without reviewing their producers. Keep failure semantics unchanged.
- Rationale: identifies the failed T51 row, or distinguishes an abnormal exit with no failed row; it does not diagnose the production seed failure.
- Current limitation: original job's published archives contain no T51 row file. A capture addition cannot recover that historical file. No replacement run is proposed here.
- Rollback: remove only the annotated projection/upload additions after closure; preserve assertions and original exit propagation.

## 2. Resolve the production branch-evidence gap before designing a new collection

- Invocation site boundary: `/config/workspace/Coder/.claude/worktrees/sysbox-retry-astra/.github/workflows/coder-ci-validate.yml`, RC-1 boot-gate invocation of `/config/workspace/Coder/.claude/worktrees/sysbox-retry-astra/.github/contract-tests/test-startup-boot.sh`; NOT production supervisor or adapter source.
- Missing evidence: exact setup/dependency/control-file stage; monotonic read/parse/deadline result; proc identity predicate outcome; handshake/go transition; result presence/validity/producer; relevant exit status, bound to the failing startup invocation. Fixed enums/booleans and bounded timing only, never credentials or raw proc/transport dumps.
- **Blocked on capability, not permission**: no verified invocation-only instrument currently recovers cleaned internal channels or emits all required branch distinctions. No LOG_LEVEL override, existing collector rerun, or working diagnostic wrapper is claimed. Post-cleanup collection cannot reconstruct deleted/non-emitted evidence.
- Rationale: determines where/why internally; later DNS/HTTPS booleans and the final enum cannot supply this witness or prove a fix.
- Concrete patch intentionally not emitted: manufacturing an executable wrapper would violate the evidence boundary. This deviates from the protocol's per-task patch skeleton explicitly rather than supplying unsafe or ineffective code.
- Rollback: none now (no patch); any subsequently demonstrated invocation-only addition must be independently removable and revert-annotated without changing production logic.

## Verification and resumption

Resume diagnosis only with an actual source-bound branch witness and the original T51 row/exit boundary (or an explicitly identified new observation, never relabeled historical evidence). Review safe projections and unchanged failure semantics before any future Actions-based validation. No local tests, host probes, or raw capture were performed. This hard-stop count is one; no instrumentation has been applied or exercised.
