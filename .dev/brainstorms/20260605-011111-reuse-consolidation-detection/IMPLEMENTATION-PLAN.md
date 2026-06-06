# Plan: Implement reuse-and-consolidation detection in sc:reflect + /tdd

## Context

The brainstorm (`.dev/brainstorms/20260605-011111-reuse-consolidation-detection/`)
produced an adversarially-merged spec (`merged-requirements.md`, convergence 0.82)
for **enforceable reuse-and-consolidation detection** — so that agents stop building
new components when an existing one could be reused/mirrored/extracted. The driving
case: prd's `_bind_specs`/`_persist_bound_specs` re-implemented the roadmap
`_inject_*` post-LLM artifact-injection idiom, invisible to every existing gate
because it is spec-conformant + name-divergent. This plan implements that merged
spec as concrete edits to two protocol skills + one new (duplicated) ref doc.

Two design facts were verified against the codebase during the brainstorm and
re-confirmed in exploration:
- sc-reflect **§17.7 Kill List item 6 (L1742) rejects a 5th deviation class** →
  Reuse-Miss is a *finding modifier* mapping onto Drift/Regression by evidence;
  low-confidence routes to **§10.6 Grounding Gaps**. (Never a new counted class.)
- `superclaude.cli.pipeline` exists and prd already imports it → the `extract-shared`
  verdict has a real legal home for the *code* case. (Not relevant to skill packaging.)

## Decision: O3 (where the shared ref lives) → **Option A, duplicated per-skill `refs/`**

Tooling evidence (decisive):
- `make sync-dev` only copies skill dirs containing `SKILL.md`, recursively (Makefile:112-123).
- `superclaude install` / `install-skill` copy each skill dir wholesale via `shutil.copytree`
  and **skip underscore-prefixed dirs** (`install_skill.py:49-52,136-138`).
- `make verify-sync` diffs each skill dir against `.claude/` (Makefile:171-180); no cross-skill identity check.

⇒ A `_shared/refs/` is uninstallable; a cross-skill pointer breaks `install-skill tdd`.
The skill-packaging boundary (each skill = self-contained installable payload) is an
NFR-PRD.7-class constraint, so the design's own verdict is **`mirror-shape`: two
byte-identical copies**, each carrying a header noting they must stay in sync. This is
the *self-containment* invariant, not the code-duplication anti-pattern.

## Scope — 3 file groups (source of truth = `src/superclaude/`; never edit `.claude/` directly)

Content source for every delta is `merged-requirements.md` §§1–11. SKILL.md edits are
thin integration glue + load-on-demand pointers; the heavy algorithm lives in the new
ref (keeps the always-loaded SKILL surface small, matching existing convention).

### Group 1 — NEW shared ref (identical copy in each skill)
- `src/superclaude/skills/sc-reflect-protocol/refs/reuse-audit.md`
- `src/superclaude/skills/tdd/refs/reuse-audit.md`

Contents (from merged-requirements §§1–8, 11): the Capability Fingerprint (F1–F6);
composite signal `S_reuse = 0.45·C_cap + 0.35·C_shape + 0.20·C_aug` with two floors
(C_cap≥0.80 ∧ C_shape≥0.70) and three tiers (confident-duplicate / maybe-related /
distinct); the L0–L4 escalation ladder; the import-ban-first 4-verdict decision tree
(reuse-by-import / mirror-shape / extract-shared / distinct); the 7-item false-positive
exclusion list + confusion matrix; the consolidation N-rule; auggie-down fallback
(cap at advisory L2); the name-agnostic query template; the worked Ω=0.88 acceptance
example. Header: `<!-- DUPLICATED REF — keep byte-identical with the tdd/sc-reflect copy -->`.

### Group 2 — `src/superclaude/skills/sc-reflect-protocol/SKILL.md` (anchors confirmed)
- **§6.1 chain (block L448-461):** insert steps `4a/4b` after step `4` (L454), before `4.5` — the auggie capability-keyed neighbour search + re-Read grounding (merged §9 R1).
- **§10 taxonomy:** insert **§10.8 "Reuse-Miss (finding modifier — NOT a 5th class)"** after §10.7 Reporting (L966), cross-referencing §10.6; maps to Drift/Regression by evidence; blocking only at rung L3 (merged §9 R2; conforms to §17.7).
- **§5.3 rubric:** add row `3a` between rule 3 (L387) and rule 4 (L388) — ESCALATE on L3 Reuse-Miss mapped to Drift/Regression (merged §9 R3).
- **§14.5.2 cond 4 (L1309):** append clarifying clause — L3 Reuse-Miss increments existing drift/regression counters; advisory does not gate. No structural gate change (merged §9 R4).
- **§9.1 contract:** bump `contract_version` "1.2.0"→"1.3.0" (L640) and add additive UC-2 fields after L683 — `reuse_sweep_ran`, `reuse_audit_path`, `reuse_miss_blocking`, `reuse_miss_advisory`, `reuse_verdict_count_by_type`, `reuse_grounding_gap_count`, `neighbour_search_sampled`, `neighbour_search_degraded`, `max_overlap_score`. **No `deviation_count_by_class.reuse_miss` key** (§17.7) (merged §9 R5).
- **§10.6 schema (L949-956):** add optional `reuse_candidate`, `nearest_neighbour`, `similarity_tier`, `composite_scores` fields (merged §9 R6).
- **§16 Refs table (L1601-1613):** add a `refs/reuse-audit.md` row (Wave 1A / Stage-A; purpose = shared reuse-detection contract).
- `allowed-tools` already lists `mcp__auggie__codebase-retrieval` (L5) — no change.

### Group 3 — `src/superclaude/skills/tdd/SKILL.md` (+ its refs)
- **A.3 discovery steps:** insert `2a/2b/2c` after step 2 (L209), before step 3 (L211) — mandatory reuse-neighbour search + model-after check + composite triage (merged §10 T1).
- **A.3 research-assignment-types table (L227-234):** add a **"Reuse Scout"** row (merged §10 T1).
- **A.4 categories:** change "8 categories"→"9 categories" (L246); add `## REUSE_AUDIT` before `## AMBIGUITIES_FOR_USER` (L283) (merged §10 T2).
- **A.5 sufficiency gate:** add **item 9** after item 8 (L300) — REUSE_AUDIT populated for every proposed component, hard verdicts carry grounded file:line (merged §10 T3).
- **`refs/build-request-template.md`:** add `REUSE_AUDIT_REQUIREMENTS` payload block + a Phase-5 synthesis instruction to render the audit section (merged §10 T4/T5).
- **`refs/synthesis-mapping.md`:** add a "Reuse & Consolidation Audit" output section + a synth-mapping row (merged §10 T5).
- **Phase Loading Contract (L415-422):** register `refs/reuse-audit.md` (declared load at the phase the Reuse Scout/triage runs; not loaded at invocation) (merged §11).
- tdd already uses generic `codebase-retrieval` (L193); no frontmatter tool change needed.

## Explicitly deferred (Simplicity-Guard — merged §12 + open items)
Not built now; left as marked open items / future enhancement:
- O1: stricter N=2 cross-module default (ship advisory + L3-escalation).
- O2: `import-boundaries.yaml` reader (v1 reads module-docstring NFR markers only).
- The pre→post ×1.1 bridge multiplier (post re-detects independently — INV-003).
- A standalone `superclaude reuse-audit` CLI.

## Verification
1. `make sync-dev` then `make verify-sync` — must exit 0 (confirms the two new ref copies + SKILL edits mirror to `.claude/`).
2. `make lint-architecture` — confirms command↔skill link + frontmatter completeness for sc-reflect (its §16.x build discipline, SKILL.md:1680-1685).
3. Byte-identity check on the two ref copies: `diff src/superclaude/skills/sc-reflect-protocol/refs/reuse-audit.md src/superclaude/skills/tdd/refs/reuse-audit.md` → empty.
4. Optional anti-bias gate (recommended): `/sc:reflect --mode post --diff <these changes>` to audit the implementation against the merged spec, and/or `make reflect-eval-quick` if touching sc-reflect eval surface.
5. Staging discipline: stage ONLY `src/` and `.dev/` paths; NEVER `.claude/` (gitignored sync output). Branch is `feat/HolisticAudit`.

## Notes
- Design is already adversarially validated (the brainstorm); this plan is the
  spec→file mapping, not a re-design. Authoritative content: `merged-requirements.md`.
- All edits land in the `HolisticAudit` worktree on `feat/HolisticAudit`.
