# Research: Reflect UC-1 findings → exact edits for merged-requirements.md

**Topic type:** Findings consolidation (research already complete — audit IS the evidence)
**Scope:** `.dev/releases/backlog/AtaraxyLabs/merged-requirements.md` (the only file edited)
**Status:** Complete
**Date:** 2026-06-04
**Provenance:** All findings grep-verified against the real file during the audit (see
`.dev/reflect/pre-ataraxy-eval-plan-20260604015505/REPORT.md` + return-contract.yaml).

---

## Target file (single)
`.dev/releases/backlog/AtaraxyLabs/merged-requirements.md` — 14 sections, frontmatter,
provenance tags [V1]/[V2]/[V3]/[MERGE]. Edits are surgical additions/reconciliations.

## Source-of-evidence files (for the builder's Context fields)
- `.dev/reflect/pre-ataraxy-eval-plan-20260604015505/REPORT.md` — the audit (6 HIGH + 5 MED)
- `.dev/releases/backlog/AtaraxyLabs/adversarial/variant-1-opus-architect.md` — rollback ordering source (V1 §6)
- `.dev/releases/backlog/AtaraxyLabs/adversarial/variant-2-sonnet-analyzer.md` — Owner field (§10.5), per-scenario sample table (§11.2)
- `.dev/releases/backlog/AtaraxyLabs/adversarial/variant-3-haiku-devops.md` — bash latency harness (L109-163), install matrix, glibc/musl rows

## Grep-verified anchor points in merged-requirements.md (confirmed during audit)
- L95-96: "weave S0 blocked until inspect S4 live + KEEP" (§3 Between-tool gate)
- L200: "inspect KILL does not block weave" (§8.2)
- No `Owner`/`RACI` match anywhere (H2)
- No `security`/`egress`/`secret` match anywhere (H3)
- L13/245/280: generalization "gated behind native success" / "optional" — no structure (M1)
- L125/136/190: "vs Auggie" with no isolation method (M2)
- §7 blind-adjudication language assumes a panel (H4)
- §2 G0-1 corpus + §7 tiered minimums (H5)
- §4 ~10 harness components, no runner contract (H6)

## The 11 edits (authoritative — one checklist item each)

### HIGH
- **H1 (§3 + §8.2):** Redefine the between-tool gate to require the prior tool to reach a
  **terminal state (KEEP-and-live OR explicit KILL)**; add one sentence that weave depends on
  `sem-core`, not inspect, so an inspect KILL lets weave's S0 proceed. ACCEPT: §3 and §8.2 no
  longer contradict; both reference the terminal-state rule.
- **H2 (§5):** Add an `Owner` field to the scorecard template + a "Decision Authority &
  Tie-Break" subsection (who calls keep/kill; borderline/ambiguous gate handling). ACCEPT:
  `grep -i owner` returns a real assignment; tie-break rule present.
- **H3 (new section):** Add "Security & Data-Handling" — inspect `review` egress + provider
  retention; secret-scrubbing before external calls; private-fork-code-to-3rd-party stance.
  ACCEPT: `grep -i "security\|egress\|secret"` returns the new section.
- **H4 (§7):** State the solo-operator blinding mechanism — randomized tool naming + an LLM
  adjudicator with stripped provenance (reflect's evidence-validator pattern), OR explicitly
  staff/budget human adjudication. ACCEPT: §7 names a concrete solo-blinding mechanism.
- **H5 (§2 G0-1):** Make a fork PR/merge-count inventory the FIRST Phase-0 action; specify the
  synthetic-backfill construction (seed from §11 curated-defect list); note corpus is NOT empty
  (~30 merges). ACCEPT: G0-1 has a concrete inventory step + a defined backfill method.
- **H6 (§4):** Add the runner I/O contract (input fields → normalized JSON output schema) +
  restore concrete artifacts (V3 bash latency harness, install matrix). Phase-0 1-2 day estimate
  references these as deliverables. ACCEPT: §4 has a runner contract + references concrete artifacts.

### MED
- **M1 (§11/§14):** Give the generalization appendix a skeleton — scenario inventory +
  thresholds — or explicitly rescope "broad" to native-first with rationale.
- **M2 (§5/§8.1):** Define the token-vs-Auggie isolation method (how to separate Auggie's token
  share from the multi-wave prompt).
- **M3 (§7):** Define sample-size confidence interpolation between 5PR/3merge and 20PR/10merge.
- **M4 (§8.3):** State weave acts on Python only (`.md` → git fallback, not a measurability
  flaw); add a Phase-0 check that enough Python worktree merges exist.
- **M5 (CP-1/§12):** Elevate the `.md`-substrate risk to a first-class plan assumption; add the
  borderline-confidence tie-break resolver (shared with H2).

## Constraints (from BUILD_REQUEST + CLAUDE.md)
- DOCS-ONLY: edit only `merged-requirements.md`. No `src/superclaude/`, no `make sync-dev`, no
  `.claude/` staging. No code, no tests.
- Preserve structure, frontmatter, provenance tags. Surgical edits, not a rewrite.
- TESTING_REQUIREMENTS: NONE (docs change). VALIDATION_REQUIREMENTS: a final re-run of
  `/sc:reflect --mode pre` on the patched file to confirm HIGH findings closed.

## Open questions / ambiguities
None — intent is clear; fixes are authoritative and grep-verified. H2 and M5 share the
tie-break resolver (build as one edit referenced by both items).
