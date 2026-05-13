# D-0005 -- Evidence: `lint-architecture` Check 10 outputs

Captured 2026-05-13 against `Makefile` after the T02.02 edit landed.

## Probe A — `*-workspace/` directory present

**Setup:**
```
mkdir -p .claude/skills/_probe-workspace
```

**Command:** `make lint-architecture`

**Filtered output (Check 10 + summary):**
```
=== Check 10: Workspace Suffix Blocklist ===
  ❌ ERROR [Check 10]: _probe-workspace — Workspace directories belong under `.dev/eval-workspaces/`, not `.claude/skills/`.

=== Summary ===
  Errors:   4
  Warnings: 1
  ❌ FAIL — 4 error(s) found. Fix before proceeding.
```

**Exit code:** `2` (non-zero; `make: *** [Makefile:252: lint-architecture] Error 1`).

**Acceptance check:**
- ✅ Verbatim message matches FR-L2.3 (backticks preserved literally).
- ✅ Check 10 increments the error accumulator → exit non-zero.

(The Summary shows 4 errors because three pre-existing errors are
present on every run of `lint-architecture` regardless of probes — see
`notes.md`. Those errors pre-date T02.02 and are not in scope.)

## Probe B — clean tree (no `*-workspace/`)

**Setup:** all probe directories removed.

**Command:** `make lint-architecture`

**Filtered output (Check 10 only):**
```
=== Check 10: Workspace Suffix Blocklist ===
  ✅ [Check 10]: no *-workspace directories under .claude/skills/
```

**Exit code:** `2` (driven by the three pre-existing errors, NOT
Check 10).

**Acceptance check:**
- ✅ Check 10 contributes zero errors on a clean tree (no false
  positive).
- ⚠️ Overall exit is non-zero only because of pre-existing, unrelated
  Check 1/Check 4/Check 6 errors. T02.02's deliverable is the Check 10
  contribution; the pre-existing errors are outside this task's scope
  and will be addressed independently.

## Summary table

| Probe | `*-workspace/` present? | Check 10 emits | Check 10 contributes errors |
|---|---|---|---|
| A `_probe-workspace` | Yes | `❌ ERROR [Check 10]: _probe-workspace — Workspace directories belong under \`.dev/eval-workspaces/\`, not \`.claude/skills/\`.` | +1 |
| B clean | No | `✅ [Check 10]: no *-workspace directories under .claude/skills/` | +0 |

## Acceptance criteria mapping (from T02.02)

| Acceptance criterion | Status |
|---|---|
| Verbatim message emitted on `*-workspace/` probe, exit non-zero | ✅ Probe A |
| Clean-tree run produces no Check 10 errors (no false positive) | ✅ Probe B |
| Target choice documented with Section 4.9 tie-breaker rationale | ✅ `notes.md` |
| Probe outputs captured | ✅ this file |
