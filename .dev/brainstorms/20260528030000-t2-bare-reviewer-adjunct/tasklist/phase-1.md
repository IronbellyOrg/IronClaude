---
phase_id: 1
title: sc-bare-review v1.0 core
depends_on: []
blocks: [1.5, 2]
estimated_loc: 450
compliance_tier: STANDARD
acceptance_gates: [AC-1.1, AC-1.2, AC-1.3, AC-1.4, AC-1.5, AC-1.6, AC-1.7, AC-1.8, AC-1.9, AC-1.10, AC-1.11, AC-1.12]
---

# Phase 1 — sc-bare-review v1.0 core

## Scope

Implement the standalone `sc-bare-review` skill at `src/superclaude/skills/sc-bare-review/SKILL.md` with Bash+curl transport. No c7 enrichment (Phase 1.5). No adversarial integration beyond producing files that downstream `--compare` will accept.

## Tasks

### T-1.1 — Skill scaffold
- Create `src/superclaude/skills/sc-bare-review/SKILL.md`
- Frontmatter (name, description, allowed-tools, model: sonnet)
- Extended metadata block
- Section structure: Purpose, Required Input, Triggers, API, Behavioral Protocol, Return Contract, Failure Modes, Boundaries, MCP Integration, ACs
- LOC: ~80

### T-1.2 — Env var resolution (Wave A)
- Resolve T2ProxyUrl, T2ProxyKey (required) — STOP if unset
- Resolve T2Model01..T2Model04 with defaults (deepseek-v4-pro / qwen3.6-plus / kimi-k2.6 / glm-5.1)
- Resolve T2Model0N_Label optional
- Resolve T2Timeout, T2Temperature optional
- Validate `--reviewers ∈ [2, 4]`; STOP if requested N > configured T2Model count
- LOC: ~70

### T-1.3 — Target ingestion (Wave B)
- Read target file
- Truncate if line count > `--target-line-cap` (default 4000); set `truncated: true`
- **[IMM-4]** Empty-target guard: count non-whitespace bytes; if < 50 → STOP with `target-too-small`
- Compute SHA-256 first-12-hex hash for provenance
- LOC: ~50

### T-1.4 — Parallel dispatch (Wave C)
- **[IMM-3]** Single Claude message block with N parallel Bash tool calls (assert structurally pre-call)
- Each Bash: `curl -s --max-time <timeout> "${T2ProxyUrl}/chat/completions" ... | jq -r '.choices[0].message.content' > <out>/bare-review-NN-<model-slug>.md.raw`
- Per-reviewer hard timeout via `--max-time`
- HTTP 5xx → retry once with 2s backoff; 4xx → no retry
- LOC: ~100

### T-1.5 — Post-processing & template normalization (Wave D)
- Parse each .raw file; extract structured sections matching template
- If model output already conforms → wrap with frontmatter, write final .md
- If free-form → regex+heuristic extraction
- Atomic-write pattern (write-to-tmp + rename)
- Idempotent filenames (re-run safe; **[IMM-6]** requirement)
- Delete .raw files on successful normalization
- LOC: ~120

### T-1.6 — Return contract (Wave E)
- Emit per §3.3 Wave E schema
- **[IMM-5]** Status determination: M==N → success; 2≤M<N → partial; M<2 → failed (M==N==2 is success, not partial)
- Include `recommended_next_command` field with literal `/sc:adversarial --compare ... --suspect-source ...`
- Write-on-failure pattern (contract still emitted on aborts)
- LOC: ~30

## Acceptance Gate

All AC-1.1..AC-1.12 must pass before Phase 1.5 or Phase 2 can begin. Specifically:

- **AC-1.5** (v1.3-revised) — Single Claude message block structural assertion verified in test
- Empty-target guard (IMM-4) — Test fixture: <50-byte target → STOP, no proxy calls
- M==N==2 boundary (IMM-5) — Test fixture: explicit N=2, M=2 → status=success
- Idempotent filenames — Test: re-running on same target overwrites, no duplicates

## Risks

- **Bash+curl prompt-escaping for large targets** — mitigate with jq-based JSON encoding; document in `docs/t2-proxy-setup.md`
- **Vendor schema drift** — first proxy integration may surface JSON-shape mismatches; ship adapter notes
