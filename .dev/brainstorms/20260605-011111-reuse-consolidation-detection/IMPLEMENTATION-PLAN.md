# Plan: Implement reuse-and-consolidation detection via a `reuse-auditor` agent

## Context

The brainstorm (`.dev/brainstorms/20260605-011111-reuse-consolidation-detection/`)
produced an adversarially-merged spec (`merged-requirements.md`, convergence 0.82)
for **enforceable reuse-and-consolidation detection** — so agents stop building new
components when an existing one could be reused/mirrored/extracted. Driving case:
prd's `_bind_specs`/`_persist_bound_specs` re-implemented the roadmap `_inject_*`
post-LLM artifact-injection idiom, invisible to every existing gate because it is
spec-conformant + name-divergent.

**Delivery-vector revision (this plan):** the merged spec proposed shipping the
detection algorithm as a `refs/reuse-audit.md` doc duplicated into both skills
(`mirror-shape`, because skill-packaged refs can't be shared). That manufactures the
exact drift liability the feature exists to catch. The better vector is a single
**`reuse-auditor` agent** that both skills delegate to — a true `extract-shared`,
because agents install flat to `.claude/agents/` and are globally addressable by name
(unlike skill-packaged refs). This is the feature **taking its own advice** (N≥2
consumers, high overlap, extract-shared is achievable → extract-shared), and it is
endorsed by sc-reflect's own **§7.2 rubric**: *"Where the work is open-ended
hypothesis or judgement, agents stay."* Capability/skeleton equivalence ("do these do
the same thing despite different names?") is exactly judgement, not mechanical mapping.

Conformance facts (verified during the brainstorm; unchanged by this revision):
- sc-reflect **§17.7 Kill List item 6 (L1742) rejects a 5th deviation class** →
  Reuse-Miss is a *finding modifier* mapping onto Drift/Regression by evidence;
  low-confidence routes to **§10.6 Grounding Gaps**. The agent returns *findings*;
  the **gate integration stays inline in sc-reflect** — so the §17.7-conforming gate
  design is untouched. The agent relocates *detection*, not *gating*.
- Tooling supports a new agent fully: `make sync-dev` copies `src/superclaude/agents/*.md`
  → `.claude/agents/` (Makefile:126-130); `verify-sync` checks agents (Makefile:202-227);
  `superclaude install` installs them. Precedent: **`evidence-validator`** (128 ln) is
  *"reusable by any skill"*, invoked via `Task` with a defined contract — the exact
  template for `reuse-auditor`.

The duplicated-refs decision (old "O3") is **dissolved** — there is no shared ref to place.

## Scope — 3 file groups (source of truth = `src/superclaude/`; never edit `.claude/` directly)

### Group 1 — NEW agent: `src/superclaude/agents/reuse-auditor.md` (the single detection home)

Templated on `src/superclaude/agents/evidence-validator.md`. Read-only (never edits
files), tool-using, one I/O contract, reusable by any skill. ~150–200 lines.

Frontmatter (mirror evidence-validator):
```
name: reuse-auditor
description: Independent reuse/consolidation auditor. For each new or proposed component,
  fingerprints its behaviour, searches the repo for prior art (name-agnostic), scores a
  composite similarity signal, and returns reuse findings with a verdict
  (reuse-by-import | mirror-shape | extract-shared | distinct) + consolidation recommendation.
  Detection only — never classifies deviations or gates. Reusable by any skill (sc:reflect,
  /tdd, cleanup-audit, analyze, code-review).
category: analysis
tools: Read, Grep, Glob, mcp__auggie__codebase-retrieval, mcp__serena__find_symbol,
  mcp__serena__get_symbols_overview, mcp__serena__find_referencing_symbols
model: sonnet
maxTurns: 50
permissionMode: plan
```

Body holds the full algorithm from `merged-requirements.md` §§1–8 (moved out of the
SKILLs): Capability Fingerprint F1–F6; composite `S_reuse = 0.45·C_cap + 0.35·C_shape
+ 0.20·C_aug` with two floors (C_cap≥0.80 ∧ C_shape≥0.70) + three tiers
(confident-duplicate / maybe-related / distinct); the import-ban-first 4-verdict tree;
the consolidation N-rule; the 7-item false-positive exclusion list + confusion matrix;
the name-agnostic query template; auggie-down inline grep-skeleton fallback (results
capped at advisory); re-Read evidence discipline; the worked Ω=0.88 acceptance example.

**I/O contract** (the key new surface):
- *Input* (orchestrator passes via `Task`): `candidates` (new/changed symbols for post;
  proposed components for pre), `stage: pre|post`, `repo_root`, optional import-boundary
  markers. Caller scopes candidates (new-symbols-only, ≤12) before invoking.
- *Output*: `reuse-audit.yaml` findings — per candidate: `capability_tag`, `neighbours`
  (`file:line` re-Read-verified), `C_cap/C_shape/C_aug/S_reuse`, `tier`, `verdict`,
  `consolidation{N, recommend_centralize, centralize_target}`, `stage`, `evidence_grounded`;
  plus run-level `max_overlap`, `degraded`, `sampled`. **No deviation class, no gate verdict.**

### Group 2 — `src/superclaude/skills/sc-reflect-protocol/SKILL.md` (delegation + gate glue)
- **§6.1 chain (block L448-461):** insert step `4a` after step `4` (L454): `Task(reuse-auditor,
  candidates=new/changed symbols from steps 2a/4, stage=post)` → consume `reuse-audit.yaml`.
  **Placement: Wave 1A runs at Tier 1 / orchestrator level — orchestrator→agent, no nesting.**
  Fallback column behaviour: agent unavailable → inline grep-skeleton degrade (cap advisory),
  same as the auggie-down path. (replaces merged §9 R1; thinner — no algorithm inline.)
- **§7 Agent Delegation Map (table ~L553):** add a `reuse-auditor` row — Wave 1A, both modes,
  role "detect reuse/consolidation prior art for new/changed symbols; return findings",
  Fallback "inline grep-skeleton degrade (advisory-capped)".
- **§7.2 "No new agents required" (L~588):** amend — reuse-auditor IS introduced; explain it
  clears the judgement bar (semantic capability/skeleton equivalence, name-agnostic) unlike the
  rejected mechanical `deviation-classifier`, and is an extract-shared unit reused across skills
  (cf. evidence-validator). This honest amendment strengthens the §7.2 reasoning.
- **§10.8 / §5.3 / §14.5.2 / §9.1 / §10.6** — gate-integration deltas UNCHANGED from the prior
  plan (the skill maps `tier`→Drift/Regression, gates at L3, routes maybe-related→§10.6):
  - §10 taxonomy: new **§10.8 "Reuse-Miss (finding modifier — NOT a 5th class)"** after §10.7 (L966).
  - §5.3 rubric: row `3a` between rule 3 (L387) and rule 4 (L388) — ESCALATE on L3 Reuse-Miss.
  - §14.5.2 cond 4 (L1309): clarifying clause — L3 Reuse-Miss increments drift/regression; advisory doesn't gate.
  - §9.1: bump `contract_version` 1.2.0→1.3.0 (L640); add UC-2 fields after L683
    (`reuse_sweep_ran`, `reuse_audit_path`, `reuse_miss_blocking`, `reuse_miss_advisory`,
    `reuse_verdict_count_by_type`, `reuse_grounding_gap_count`, `neighbour_search_*`, `max_overlap_score`);
    **no `deviation_count_by_class.reuse_miss` key** (§17.7).
  - §10.6 schema (L949-956): add optional `reuse_candidate`, `nearest_neighbour`, `similarity_tier`, `composite_scores`.
- **§16 Refs table:** NO new ref row (the algorithm is in the agent, not a ref).
- `allowed-tools` already lists `mcp__auggie__codebase-retrieval` (L5) + Task — no change.

### Group 3 — `src/superclaude/skills/tdd/SKILL.md` (+ its refs)
- **A.3 discovery (after step 2, L209):** insert step `2a` — the **orchestrator** invokes
  `Task(reuse-auditor, candidates=proposed components, stage=pre)` during scope discovery and
  records findings. **Placement: orchestrator-level (A.3), explicitly NOT inside a nested
  Phase-2 research subagent** (avoids subagent→agent nesting). (replaces merged §10 T1.)
- **A.3 research-assignment-types table (L227-234):** add a **"Reuse Scout"** row whose
  "What the Agent Does" = "delegate to the `reuse-auditor` agent for each proposed component".
- **A.4 categories:** "8 categories"→"9 categories" (L246); add `## REUSE_AUDIT` before
  `## AMBIGUITIES_FOR_USER` (L283) — populated from the agent's findings (merged §10 T2).
- **A.5 sufficiency gate:** add **item 9** after item 8 (L300) — REUSE_AUDIT populated for every
  proposed component; hard verdicts carry grounded `file:line` (merged §10 T3).
- **`refs/build-request-template.md`:** add `REUSE_AUDIT_REQUIREMENTS` block (Phase-2 item must
  invoke reuse-auditor per proposed component; Phase-5 renders the audit section) (merged §10 T4/T5).
- **`refs/synthesis-mapping.md`:** add a "Reuse & Consolidation Audit" output section + synth row (merged §10 T5).
- **Phase Loading Contract (L415-422):** no new *ref* to register; if any prose names the agent,
  keep it consistent with the contract. tdd already uses generic `codebase-retrieval` (L193);
  agent invocation is via `Task` (already available) — no frontmatter change.

## The one real cost: placement / nesting discipline
The agent must be invoked at **orchestrator / Tier-1 level**, never inside an
already-spawned subagent (subagent→agent nesting can fail —
`mem:reference_subagent_cannot_nest_skill_fanout`). Both placements above honour this
(sc-reflect Wave 1A = orchestrator; tdd A.3 = orchestrator). Every call site carries the
inline grep-skeleton **fallback** so a blocked/unavailable agent degrades to advisory,
never STOPs — consistent with all other §7 agents' Fallback column.

## Explicitly deferred (Simplicity-Guard — merged §12 + open items)
- O1: stricter N=2 cross-module default (ship advisory + L3-escalation).
- O2: `import-boundaries.yaml` reader (v1 reads module-docstring NFR markers only).
- pre→post ×1.1 bridge multiplier (post re-detects independently — INV-003).
- standalone `superclaude reuse-audit` CLI.

## Verification
1. `make sync-dev` then `make verify-sync` — exit 0 (new agent + SKILL edits mirror to `.claude/`; agent picked up by Makefile:126-130 + verify-sync agents loop).
2. `make lint-architecture` — command↔skill link + frontmatter completeness (sc-reflect §16.x discipline, SKILL.md:1680-1685).
3. **Agent eval** (replaces the old byte-identity diff check): feed `reuse-auditor` the
   ground-truth pair (`prd/executor.py:1196` vs `roadmap/executor.py:715`) → assert it returns
   `confident-duplicate`, `verdict: extract-shared` (or `mirror-shape` under the NFR-PRD.7 ban),
   `S_reuse ≈ 0.88`; and a negative fixture (`validate_x` vs `validate_y`) → `distinct`.
4. Optional anti-bias gate: `/sc:reflect --mode post --diff <these changes>` against `merged-requirements.md`; `make reflect-eval-quick` if touching sc-reflect eval surface.
5. Staging: stage ONLY `src/` and `.dev/` paths; NEVER `.claude/`. Branch `feat/HolisticAudit`.

## Notes
- Design is already adversarially validated; this plan is the spec→file mapping with the
  delivery vector switched to an agent. Authoritative content: `merged-requirements.md`
  (read its §§1–8 into the agent body; §§9–11 become the thin SKILL glue above).
- Net implementation surface is **lower** than the duplicated-refs plan: one agent file
  replaces two ~250-line ref copies + the sync chore; SKILL deltas shrink to delegation + glue.
- All edits land in the `HolisticAudit` worktree on `feat/HolisticAudit`.
