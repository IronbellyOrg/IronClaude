# OQ-4 Precondition Record — `get_current_config` defensive parse

**Date:** 2026-06-02
**Source:** research 06 §OQ-4 (matrix:396–399, matrix:408, matrix:560, spec:265, spec:522) + the C2 invariant (review:106)
**Gates:** FR-7 parse robustness; transitively the FR-6 + FR-8 `serena_version` version gates. SHOULD be runtime-probed (spec:265); the **defensive-parse is MANDATORY** because the return shape is documented-unstable.

## (a) Runtime-probe + defensive field-presence requirement (FR-7)

- FR-7's implementation MUST **runtime-probe `get_current_config` at Wave 0** of the implementing reflect run (spec:522) — this is FR-7's own first step.
- Use **defensive field-presence checks** for every consumed field (spec:265): **never assume a field exists**. For each of `active context`, `active modes`, `loaded tools list`, and `version`, guard with a presence check; a **missing field → that derived value = `unknown`**.
- The return shape is "not surfaced" / not version-stable (inferred from the Serena startup-log shape, Issue #254) — context+modes evolved across v1.0 → v1.5 (matrix:408), so no field name may be assumed contractual.

## (b) Version-fingerprint is load-bearing (C2)

- `get_current_config` is the **source of `serena_version`**, which gates FR-6 and FR-8 (matrix:553, spec:265).
- `serena_version` MUST be **three-valued**: `{<v1.5, >=v1.5, unknown}`.
- `unknown` is the **fail-open default** and MUST be **treated as `<v1.5`** (conservative: write-only-no-retention, no rename-propagation) per review A4 + C2.
- This is stated in BOTH FR-8.4 and FR-7's fail-open clause.

## (c) Fail-open rule

On parse failure of `get_current_config`:

1. Emit a `degraded_components` entry: `["get_current_config"]`.
2. Skip the config snapshot.
3. Set `serena_version: unknown` (which is treated as `<v1.5` per C2).
4. **Continue Wave 0** (do not abort the run).

No fabricated field names are asserted here — only the four inferred consumed fields (active context, active modes, loaded tools list, version) named in research §OQ-4.
