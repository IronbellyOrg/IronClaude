Goal: Generate a paste-ready prompt that turns a scope matrix and a risk matrix into a project-conformant specification document.

Recommended delegation: `prd` skill (invoked via the Skill tool). Wins net value because (a) "scope-matrix + risk-matrix → spec" is the canonical PRD seam — scope and risk are PRD inputs, not generic spec inputs; (b) `prd` is template-anchored against `.claude/templates/workflow/05_prd_template.md` and enforces MDTM research/synthesis/QA gates that native Read+Write cannot reproduce without duplicating the template by hand; (c) `/sc:spec-panel` reviews existing specs (wrong direction), `/sc:design` lacks template/QA discipline, `/sc:workflow` consumes a PRD rather than produces one. If the user wants a downstream engineering spec after the PRD lands, the optional follow-on is the `tdd` skill (PRD → TDD is the documented chain).

Paste-ready prompt:

```text
Use the Skill tool to invoke the `prd` skill with the following inputs:

WHAT to document: A Product Requirements Document derived from two upstream matrices that already capture product scope and product/release risk.

WHY / decisions this PRD supports: Consolidate the scope and risk matrices into a single template-conformant PRD that downstream planning (TDD, roadmap, tasklist) can consume.

Source matrices (treat as authoritative input — extract scope, personas, jobs-to-be-done, success metrics, constraints, and risk register from these; do not invent content beyond what they imply):
- docs/scope-matrix.md
- docs/risk-matrix.md

WHERE to look: Start with the two matrices above. Use the project codebase only to verify any technical claims the matrices reference; do not expand scope beyond what the matrices define.

OUTPUT location: docs/PRD.md (or, if a stub already exists under docs/, populate the stub in place — surface the stub path before writing).

Tier: Standard, unless the scope matrix clearly indicates a single narrow feature (Lightweight) or platform-scale scope (Heavyweight).

Deliverable: A PRD conforming to .claude/templates/workflow/05_prd_template.md with every section populated, the risk register reflecting docs/risk-matrix.md, traceability from scope-matrix rows to functional requirements, and the standard MDTM research-synthesis-QA gates passed.

If either matrix file does not exist or is empty, stop and ask the user to confirm the matrix paths before spawning the task file.
```

Sources verified:

- src/superclaude/commands/spec-panel.md (Read) — confirmed it is a review-mode tool that ingests an existing spec; not a producer. Rejected as primary.
- src/superclaude/commands/design.md (Read) — confirmed generic design output, no template binding, no QA gates. Rejected.
- src/superclaude/commands/workflow.md (Read) — confirmed it consumes a PRD and emits an implementation workflow; wrong direction.
- src/superclaude/skills/prd/SKILL.md (Read) — confirmed template at `.claude/templates/workflow/05_prd_template.md`, MDTM pipeline, mandatory input is "WHAT to document" + optional "WHY/WHERE/OUTPUT". Hand-off compatible with the user's two-matrix input.
- src/superclaude/skills/tdd/SKILL.md (Read) — confirmed PRD-fed TDD path exists as the documented follow-on; held as optional next step, not bundled into the primary prompt.
- auggie semantic rank: top 5 returned were `spec-panel`, `prd`, `tdd`, `design`, `adversarial`. Only `prd` matches the production direction (matrices → spec); the rest are review, downstream, generic, or comparison surfaces.

## Trace

Auggie semantic-rank query was issued once with the verbatim user request and the full enumerated surface (commands + skills + agents + templates). Auggie surfaced — in capability-fit order against the request:

1. `/sc:spec-panel` — surfaced strongly because of the literal word "spec", but verification revealed it ingests an existing specification and produces expert critique. Direction mismatch: user wants to CREATE specs, spec-panel REVIEWS them. Dropped as primary; would be valid as a downstream review step after the PRD lands.
2. `prd` skill — surfaced as the canonical producer of a template-conformant requirements artifact, template at `.claude/templates/workflow/05_prd_template.md`, MDTM-backed, accepts matrix-style inputs in the WHAT/WHY/WHERE/OUTPUT contract. Verified and selected as primary.
3. `tdd` skill — surfaced as the engineering-spec producer; documented chain is PRD → TDD. Verified. Held as optional follow-on, not bundled into the primary prompt because the user said "create specs" without confirming they want both layers.
4. `/sc:design` — surfaced because of "design specifications" phrasing in its description. Verification showed it is a generic design generator with no template binding, no QA gates, and no MDTM persistence. Net-value rubric: skill protocol load cost not justified vs prd/tdd which own the template; dropped.
5. `/sc:adversarial` — surfaced because spec-generation prompts in the repo's research artifacts pair adversarial debate with spec-panel review. Verification confirmed it is a comparison/debate tool, not a generator. Dropped — out of scope for a single-pass "create specs from matrices" request.

Per-candidate verification outcomes (Phase 0 Step C):

| Candidate | Source resolved | Direction fit | Decision |
|---|---|---|---|
| `/sc:spec-panel` | yes (src/superclaude/commands/spec-panel.md) | reviewer, not producer | drop |
| `prd` skill | yes (src/superclaude/skills/prd/SKILL.md) | producer, template-anchored | primary |
| `tdd` skill | yes (src/superclaude/skills/tdd/SKILL.md) | producer, downstream of PRD | optional follow-on |
| `/sc:design` | yes (src/superclaude/commands/design.md) | generic, untemplated | drop |
| `/sc:adversarial` | yes (src/superclaude/commands/adversarial.md) | debate/compare | drop |

Phase 1 net-value check on the selected primary (`prd` skill):

- Specialized capability: template-conformant PRD assembly + MDTM research/synthesis/QA gates. Native Read+Write cannot reproduce the QA discipline.
- Scope: two-matrix input is small, but the *output structure* (full PRD template with risk register, traceability, success metrics) is load-bearing — template-owning skill wins.
- Output structure: PRD template is a project-template artifact; skill owns it.
- Token budget: `prd` skill body is large but justified — the user is asking for a complete structured document, not a one-liner.
- Discipline: matrices imply downstream consumers (TDD, roadmap, tasklist) that depend on the PRD being template-conformant — discipline wins.

Decision: delegate to `prd`. Recommendation kind: `delegation_prompt`. Auggie status: `ok`. No degradation notice required.
