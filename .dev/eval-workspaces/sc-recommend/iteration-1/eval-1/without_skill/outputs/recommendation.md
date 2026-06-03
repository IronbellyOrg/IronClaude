# Recommendation: Generating Specs from `scope-matrix.md` + `risk-matrix.md`

## Approach

Use the existing **`prd`** and **`tdd`** skills as the spec generators, with the two matrices supplied as **authoritative, frozen inputs**. This project already has:

- `src/superclaude/skills/prd/SKILL.md` — produces a PRD conforming to `templates/workflow/05_prd_template.md` (MDTM-backed, codebase-verified, anti-hallucination gates).
- `src/superclaude/skills/tdd/SKILL.md` — produces the engineering counterpart, can be fed directly from the PRD.
- `templates/documents/release-spec-template.md` — the canonical spec schema if a single release spec is preferred over PRD+TDD.

Running PRD then TDD sequentially gives you a product spec and an engineering spec that share traceability back to every row in the two matrices. If you want a single document instead, swap the two-step flow for one `release-spec` pass — the prompt below has a toggle for that.

Why this beats a generic "write me a spec" prompt:

- The matrices become **the contract**: every in-scope row must appear as a requirement; every risk row must appear as a mitigation, acceptance criterion, or open-question.
- The skills already enforce template conformance, evidence-backed claims, and QA gates — you don't have to reinvent that scaffolding in the prompt.
- Out-of-scope rows from `scope-matrix.md` become explicit non-goals (a class of bug specs routinely miss).

## Paste-ready prompt

Paste this verbatim into a fresh Claude Code chat in the repo. Replace the two path lines at the top if the matrices live elsewhere.

```
Inputs (treat as authoritative, frozen — do not re-derive scope or risk from memory):
- SCOPE_MATRIX: docs/scope-matrix.md
- RISK_MATRIX:  docs/risk-matrix.md

Goal: Produce specifications for the product/feature described by these two matrices. The matrices ARE the source of truth — every in-scope row must land in the spec as a requirement, every out-of-scope row as an explicit non-goal, and every risk row as a mitigation, acceptance criterion, or tracked open-question.

Deliverables (default — two documents, traceable to each matrix row):
1. A PRD at docs/specs/<slug>-PRD.md — invoke the `prd` skill.
2. A TDD at docs/specs/<slug>-TDD.md — invoke the `tdd` skill, feeding it the PRD from step 1 plus both matrices.

(If I instead want a single combined release spec, ignore the two-doc plan and produce one document at docs/specs/<slug>-release-spec.md using templates/documents/release-spec-template.md. Ask me which mode I want before starting if it is ambiguous.)

Hard requirements for both specs:
- Read both matrices fully before drafting anything. Do not paraphrase rows from memory.
- Every requirement, non-goal, mitigation, and acceptance criterion must cite the matrix row it traces to, e.g. `[scope-matrix.md row: <id-or-heading>]` or `[risk-matrix.md row: <id-or-heading>]`.
- Include a "Traceability" appendix in each spec: two tables (scope-row → spec-section, risk-row → spec-section) covering 100% of in-scope and risk rows. Any uncovered row must appear in an "Open Questions / Gaps" section with a concrete next action — never silently dropped.
- Out-of-scope rows from the scope matrix become an explicit Non-Goals section, not an omission.
- Risk severity/likelihood (or whatever columns the risk matrix uses) must drive priority in the spec: high-severity risks get acceptance criteria + monitoring/rollback plans, not just prose.
- Verify any technical claim against the codebase before writing it — use `mcp__auggie__codebase-retrieval` (or Grep + Read) when the matrix references existing components, files, or behaviors. No hand-waving.
- Conform exactly to the project templates (`templates/workflow/05_prd_template.md`, the tdd skill's template, or `templates/documents/release-spec-template.md` for combined mode). The template is the schema.

Pre-flight (do this first, before drafting):
1. Read both matrices in full. Extract: feature name/slug, in-scope row list, out-of-scope row list, risk row list with severities.
2. Run a confidence check: do you have ≥90% clarity on what the feature IS? If not, list the top 3 ambiguities and ask me — don't guess.
3. Confirm the deliverable mode (two-doc PRD+TDD vs. single release spec) and the output directory.
4. Then invoke the `prd` skill (or `release-spec` flow) with the matrices passed as inputs.

Output: the spec file paths, plus a short summary of which matrix rows landed where and which rows (if any) are in the Open Questions section with the reason.
```

## Notes / framing for the user

- If the matrices don't yet exist at `docs/scope-matrix.md` / `docs/risk-matrix.md`, create or move them there before pasting — the prompt treats those paths as frozen inputs.
- The "Traceability appendix + Open Questions" pattern is the part that's load-bearing: it converts the matrices from background reading into a checklist the spec must satisfy, which is what makes specs-from-matrices reliably good instead of vaguely on-topic.
- If you only want one spec, the inline toggle in the prompt covers that; otherwise the default PRD→TDD chain gives you both product and engineering perspectives without duplicated traceability work.
