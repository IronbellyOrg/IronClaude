# OQ-M5 — Cross-spec FR-7 Substrate Status + `read_only` Derivation Gap

**Date:** 2026-06-03
**Step:** Phase 1, Step 1.4
**Status:** RESOLVED

## (a) Has the low-spec FR-RV3-LOW.7 Wave-0 probe landed? — YES (grep evidence)

```
$ grep -nE "get_current_config|serena_config_snapshot_path|0\.5c" src/superclaude/skills/sc-reflect-protocol/SKILL.md
5:   allowed-tools: ... mcp__serena__get_current_config ...
133: 0.5c get_current_config probe (active context/modes/version fingerprint)   [Wave-0 outline]
214: **Step 0.5c (active-project config probe, FR-7).** ... invoke `mcp__serena__get_current_config` ...
216: ... extract serena_active_context, serena_active_modes, loaded-tools list (→ serena_tool_count,
        serena_excluded_tools), Serena version ...
218: Write the parsed snapshot to <output>/serena-config-snapshot.yaml and record serena_config_snapshot_path
686: serena_config_snapshot_path: <abs path>   # FR-7   [§9.2 telemetry]
```

**Conclusion:** FR-7 is MERGED. The medium FR-4 Wave-0 step (Phase 2 Step 2.2) **CONSUMES the existing
`0.5c get_current_config` snapshot** (`serena_config_snapshot_path` → `<output>/serena-config-snapshot.yaml`)
rather than shipping a fresh duplicate probe. It still authors the spec §4.5 / M-ARC3 four-field surface
(`backend | execute_shell_command_available | onboarding_available | read_only`) as the cohesive Wave-0
contract FR-1/FR-2 consume, deriving three of the four fields from FR-7's snapshot and adding the one
gap field (`read_only`) itself.

## (b) Derivation rule — three fields come from FR-7's snapshot

| Field | FR-7 source | Derivation | Status |
|---|---|---|---|
| `backend` | "Language backend" string in snapshot (verified live: `Language backend: LSP`) | direct parse → `lsp` \| `jetbrains` \| `none` | **derivable from FR-7** — gates FR-1 step 4.5 |
| `execute_shell_command_available` | loaded/active-tools list | membership test on the ACTIVE-tools list | **derivable from FR-7** — gates FR-4 step 5.5 |
| `onboarding_available` | loaded/active-tools list (verified live: `onboarding` IS active) | membership test on the ACTIVE-tools list | **derivable from FR-7** — gates FR-2 step 0.7b |

Field names are a strict subset of FR-7's output → the post-merge swap is non-breaking (spec §4.5 last para).

## (c) THE LOAD-BEARING FINDING — `read_only` is the ONE field FR-7 does NOT provide

`get_current_config`'s live output surfaces context + modes + tools + version + project, but **NOT** a
`read_only` boolean (CODE-VERIFIED via live runtime probe, research-06 §OQ-M5 lines 103–137). `read_only`
is a Serena *project-config* setting (`read_only: true` in `.serena/project.yml`).

**Therefore: FR-4's Wave-0 step MUST add a small project-config `read_only` derivation** — read `read_only`
from the project's `.serena/project.yml` (or equivalent active project config) — **regardless of merge order**.
This derivation persists even post-FR-7-merge (FR-7 will never emit `read_only`), so it is NOT pure duplication.

- `read_only: true` → the FR-4 verification triangle is DISABLED with a loud WARN
  (`verification_skip_reason: read-only-project`, FR-4.7).
- Missing `.serena/project.yml` / parse failure → fail-open: treat as `read_only: false` is UNSAFE for the
  triangle's safety posture? No — research/spec posture: on inability to determine, degrade the *capability*
  (treat verification as unavailable, emit skip reason, continue) — never STOP. The Wave-0 block fails open
  on any parse failure of any of the four fields.

## Summary for downstream phases
- Phase 2 Step 2.2 authors the unified §4.0 four-field availability block (consume FR-7 for 3 fields; derive
  `read_only` from `.serena/project.yml`).
- FR-1 (Phase 5 Step 5.1/5.3) and FR-2 (Phase 3 Step 3.3) READ this Wave-0 `backend` / `onboarding_available`
  baseline rather than re-probing; their phase-opening runtime probes confirm/refine, not replace, it.

No fabricated field — `read_only`'s absence from `get_current_config` is CODE-VERIFIED.
