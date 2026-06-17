# Phase 3 Output Summary — `--context` / `--caller` Flag Ingestion

**Date:** 2026-06-16
**Files edited:** `src/superclaude/commands/troubleshoot.md`, `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`
**verify-sync:** EXIT 0, no drift, no `.claude/` staged (`test-results/phase-3-verify-sync.txt`)

All 10 ingestion edits below are drawn verbatim from the captured `git diff`.

## Command file (`commands/troubleshoot.md`)

### Step 3.1 — argument-hint
- **After (appended):** `... [--no-doc-discovery] [--no-mcp] [--context <path>] [--caller <name>]"`

### Step 3.2 — `--context` Options row (after `--no-mcp`)
- `| \`--context\` | (none) | Path to a caller-supplied context file (e.g. TFEP \`return-contract.yaml\` consumer brief). Ingested in Wave 0; recorded in the audit-log header and echoed in the Wave 5 return. |`

### Step 3.3 — `--caller` Options row (after `--context`)
- `| \`--caller\` | (none) | Name of the invoking pipeline/command (e.g. \`task-unified\`). When set, Wave 5 emits a \`return-contract.yaml\` adapter and the audit header records \`caller:\`. |`

### Step 3.4 — parse-step enumeration
- **After:** `1. **Parse arguments** → resolve \`--type\` (auto-detect if absent), \`--scope\`, \`--depth\`, \`--context\`, \`--caller\`, etc.`

### Step 3.5 — "On skill return, surface:" list
- **After (appended):** `..., and (if caller=task-unified) the emitted return-contract.yaml path.`

## Skill file (`skills/sc-troubleshoot-protocol/SKILL.md`)

### Step 3.6 — Wave 0 parse sentence (step 1)
- **After (appended to Optional:):** `..., \`--reset-diagnosability-rounds\`, \`--context\`, \`--caller\`.`

### Step 3.7 — new Wave 0 step 6 (resolve sub-step)
- `6. If \`--caller\` is set, record it in the audit header \`caller:\` field (see the TARGET header below). If \`--context <path>\` is set, read it (the caller brief) and resolve it to an absolute path; STOP if the path is unreadable. When \`caller=task-unified\`, mark Wave 5 to emit \`return-contract.yaml\` (see Wave 5).`
- Inserted between the audit-header fenced block and `**Exit criteria**:`.

### Step 3.8 — Wave 0 STOP conditions
- **After (appended):** `..., \`--output-dir\` not writable, \`--context\` path unreadable.`

### Step 3.9 — audit-log TARGET header keys (after `output_dir:`)
- `caller: <name|none>`
- `context_path: <abs-path|none>`

### Step 3.10 — SUMMARY footer keys (after `duration_sec:`)
- `caller: <name|none>`
- `return_contract_path: <abs-path|none>`

### Step 3.11 — sync + verify-sync → EXIT 0.

## Convention fidelity notes
- Options-row default uses unbackticked `(none)` sentinel matching the `--scope` row.
- Audit-block keys use lowercase-key + `<placeholder|none>` convention matching `scope: <path|symbol|none>`.
- Surface clause uses the parenthetical-conditional style matching `(if --fix) ...`.
- Command stays thin: it ADVERTISES the flags + SURFACES the return-contract path; the skill does the parse/resolve/emit (NFR-5).

No fabrication: every snippet above is from the captured `git diff`.
